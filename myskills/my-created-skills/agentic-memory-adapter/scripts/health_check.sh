#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  health_check.sh --repo /abs/path [--bin codememory] [--search-query "text"]

Examples:
  health_check.sh --repo /repo
  health_check.sh --repo /repo --search-query "auth flow"
EOF
}

REPO=""
CODEMEMORY_BIN="${CODEMEMORY_BIN:-codememory}"
SEARCH_QUERY=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/run_codememory.sh"
HAS_PYTHON3=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo)
            REPO="${2:-}"
            shift 2
            ;;
        --bin)
            CODEMEMORY_BIN="${2:-}"
            shift 2
            ;;
        --search-query)
            SEARCH_QUERY="${2:-}"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [[ -z "$REPO" || ! -d "$REPO" ]]; then
    echo "Provide an existing repository path via --repo /abs/path" >&2
    exit 2
fi

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "[PASS] $*"
}

warn() {
    WARN_COUNT=$((WARN_COUNT + 1))
    echo "[WARN] $*"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "[FAIL] $*"
}

if command -v "$CODEMEMORY_BIN" >/dev/null 2>&1; then
    pass "Found CLI binary: $CODEMEMORY_BIN"
else
    fail "Missing CLI binary: $CODEMEMORY_BIN"
fi

if [[ -f "$REPO/.codememory/config.json" ]]; then
    pass "Found repo config: $REPO/.codememory/config.json"
else
    warn "Missing $REPO/.codememory/config.json (run codememory init if this repo is new)"
fi

if [[ -x "$RUNNER" ]]; then
    pass "Found adapter runner: $RUNNER"
else
    fail "Runner missing or not executable: $RUNNER"
fi

if command -v python3 >/dev/null 2>&1; then
    HAS_PYTHON3=true
    pass "Found python3 for config/network checks"
else
    warn "python3 not found; skipping config parsing and socket reachability checks"
fi

NEO4J_URI="${NEO4J_URI:-}"
if [[ "$HAS_PYTHON3" == "true" && -z "$NEO4J_URI" && -f "$REPO/.codememory/config.json" ]]; then
    NEO4J_URI="$(
        python3 - "$REPO/.codememory/config.json" <<'PY'
import json
import sys

cfg = {}
try:
    with open(sys.argv[1], "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
except Exception:
    pass
print(cfg.get("neo4j", {}).get("uri", ""))
PY
    )"
fi

if [[ "$HAS_PYTHON3" == "true" ]]; then
    if [[ -n "$NEO4J_URI" ]]; then
        if python3 - "$NEO4J_URI" <<'PY'
import socket
import sys
from urllib.parse import urlparse

uri = sys.argv[1]
parsed = urlparse(uri)
host = parsed.hostname or "localhost"
port = parsed.port or 7687

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2.0)
try:
    sock.connect((host, port))
except OSError:
    sys.exit(1)
finally:
    sock.close()
PY
        then
            pass "Neo4j endpoint is reachable (${NEO4J_URI})"
        else
            fail "Neo4j endpoint is not reachable (${NEO4J_URI})"
        fi
    else
        warn "NEO4J_URI not found in env or repo config"
    fi
fi

if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    pass "OPENAI_API_KEY found in shell environment"
elif [[ -f "$REPO/.env" ]] && grep -q '^OPENAI_API_KEY=' "$REPO/.env"; then
    pass "OPENAI_API_KEY entry found in $REPO/.env"
else
    warn "OPENAI_API_KEY not found (semantic search checks may fail)"
fi

STATUS_OUT="$(mktemp "${TMPDIR:-/tmp}/codememory-health-status-out.XXXXXX")"
STATUS_ERR="$(mktemp "${TMPDIR:-/tmp}/codememory-health-status-err.XXXXXX")"
if "$RUNNER" --repo "$REPO" --bin "$CODEMEMORY_BIN" --timeout 30 --retries 1 -- status >"$STATUS_OUT" 2>"$STATUS_ERR"
then
    pass "codememory status returned healthy output"
else
    fail "codememory status failed (see $STATUS_OUT and $STATUS_ERR)"
fi

if [[ -n "$SEARCH_QUERY" ]]; then
    SEARCH_OUT="$(mktemp "${TMPDIR:-/tmp}/codememory-health-search-out.XXXXXX")"
    SEARCH_ERR="$(mktemp "${TMPDIR:-/tmp}/codememory-health-search-err.XXXXXX")"
    if "$RUNNER" --repo "$REPO" --bin "$CODEMEMORY_BIN" --timeout 30 --retries 1 -- \
        search "$SEARCH_QUERY" --limit 1 >"$SEARCH_OUT" 2>"$SEARCH_ERR"
    then
        pass "codememory search check succeeded"
    else
        warn "codememory search check failed (likely missing key/index); see $SEARCH_OUT and $SEARCH_ERR"
    fi
fi

echo
echo "Health summary: pass=$PASS_COUNT warn=$WARN_COUNT fail=$FAIL_COUNT"
if (( FAIL_COUNT > 0 )); then
    echo "Health result: FAIL"
    exit 1
fi
if (( WARN_COUNT > 0 )); then
    echo "Health result: WARN"
    exit 0
fi
echo "Health result: PASS"
