#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  run_codememory.sh --repo /abs/path [--timeout 45] [--retries 2] [--backoff 2] [--bin codememory] -- <subcommand> [args...]

Examples:
  run_codememory.sh --repo /repo -- status
  run_codememory.sh --repo /repo --timeout 120 --retries 1 -- index
  run_codememory.sh --repo /repo -- search "auth logic" --limit 5

Notes:
  - Runs the CLI from the target repo to avoid implicit cwd issues.
  - Supported subcommands: init, status, index, watch, serve, search.
EOF
}

REPO=""
TIMEOUT_SECONDS="${CODEMEMORY_TIMEOUT_SECONDS:-45}"
RETRIES="${CODEMEMORY_RETRIES:-2}"
BACKOFF_SECONDS="${CODEMEMORY_BACKOFF_SECONDS:-2}"
CODEMEMORY_BIN="${CODEMEMORY_BIN:-codememory}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo)
            REPO="${2:-}"
            shift 2
            ;;
        --timeout)
            TIMEOUT_SECONDS="${2:-}"
            shift 2
            ;;
        --retries)
            RETRIES="${2:-}"
            shift 2
            ;;
        --backoff)
            BACKOFF_SECONDS="${2:-}"
            shift 2
            ;;
        --bin)
            CODEMEMORY_BIN="${2:-}"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [[ -z "$REPO" ]]; then
    echo "Missing required --repo /abs/path" >&2
    usage >&2
    exit 2
fi

if [[ ! -d "$REPO" ]]; then
    echo "Repo does not exist: $REPO" >&2
    exit 2
fi

if [[ $# -lt 1 ]]; then
    echo "Missing codememory subcommand after --" >&2
    usage >&2
    exit 2
fi

if ! [[ "$TIMEOUT_SECONDS" =~ ^[0-9]+$ && "$RETRIES" =~ ^[0-9]+$ && "$BACKOFF_SECONDS" =~ ^[0-9]+$ ]]; then
    echo "--timeout, --retries, and --backoff must be non-negative integers." >&2
    exit 2
fi

COMMAND=( "$@" )
SUBCOMMAND="${COMMAND[0]}"
case "$SUBCOMMAND" in
    init|status|index|watch|serve|search) ;;
    *)
        echo "Unsupported subcommand: $SUBCOMMAND" >&2
        echo "Allowed: init, status, index, watch, serve, search" >&2
        exit 2
        ;;
esac

if ! command -v "$CODEMEMORY_BIN" >/dev/null 2>&1; then
    echo "Command not found: $CODEMEMORY_BIN" >&2
    echo "Set CODEMEMORY_BIN if your install uses a different executable name." >&2
    exit 127
fi

TIMEOUT_WRAPPER=()
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT_WRAPPER=(timeout "${TIMEOUT_SECONDS}s")
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT_WRAPPER=(gtimeout "${TIMEOUT_SECONDS}s")
fi

run_once() {
    if [[ ${#TIMEOUT_WRAPPER[@]} -gt 0 ]]; then
        "${TIMEOUT_WRAPPER[@]}" bash -lc 'cd "$1" && shift && "$@"' _ \
            "$REPO" "$CODEMEMORY_BIN" "${COMMAND[@]}"
    else
        bash -lc 'cd "$1" && shift && "$@"' _ \
            "$REPO" "$CODEMEMORY_BIN" "${COMMAND[@]}"
    fi
}

hard_failure_in_output() {
    local output="$1"
    [[ "$output" == *"Error"* ]] || \
    [[ "$output" == *"Traceback (most recent call last)"* ]] || \
    [[ "$output" == *"Exception:"* ]] || \
    [[ "$output" == *"ServiceUnavailable"* ]] || \
    [[ "$output" == *"Could not connect to Neo4j"* ]] || \
    [[ "$output" == *"OpenAI API key not configured"* ]]
}

print_recovery_guidance() {
    local exit_code="$1"
    local output="$2"
    local cmd_display="$CODEMEMORY_BIN ${COMMAND[*]}"

    echo "Recovery guidance:" >&2
    if [[ "$output" == *"Agentic Memory is not initialized"* ]]; then
        echo "  - Initialize first: (cd \"$REPO\" && $CODEMEMORY_BIN init)" >&2
    elif [[ "$output" == *"Could not connect to Neo4j"* ]] || \
         [[ "$output" == *"ServiceUnavailable"* ]] || \
         [[ "$output" == *"Connection refused"* ]]; then
        echo "  - Verify Neo4j is running and reachable at NEO4J_URI." >&2
        echo "  - Re-check NEO4J_USER and NEO4J_PASSWORD." >&2
    elif [[ "$output" == *"OpenAI API key not configured"* ]] || \
         [[ "$output" == *"OPENAI_API_KEY"* ]]; then
        echo "  - Export OPENAI_API_KEY or add it to \"$REPO/.env\"." >&2
    elif [[ "$exit_code" -eq 124 ]]; then
        echo "  - Command timed out. Increase --timeout (seconds)." >&2
        echo "  - For large repos, run index with larger timeout and fewer retries." >&2
    elif [[ "$output" == *"Invalid --repo path"* ]]; then
        echo "  - Verify --repo is an existing absolute directory path." >&2
    else
        echo "  - Re-run with the same command to confirm reproducibility." >&2
        echo "  - If failure persists, run manually from repo root: (cd \"$REPO\" && $cmd_display)" >&2
    fi
}

MAX_ATTEMPTS=$((RETRIES + 1))
attempt=1
attempts_made=0
last_exit=0
last_output=""
ok=false

while (( attempt <= MAX_ATTEMPTS )); do
    attempts_made="$attempt"
    set +e
    current_output="$(run_once 2>&1)"
    current_exit=$?
    set -e

    last_output="$current_output"
    last_exit="$current_exit"

    if [[ "$current_exit" -eq 0 ]] && ! hard_failure_in_output "$current_output"; then
        ok=true
        break
    fi

    if (( attempt < MAX_ATTEMPTS )); then
        sleep "$BACKOFF_SECONDS"
    fi
    attempt=$((attempt + 1))
done

echo "adapter.ok=$ok"
echo "adapter.repo=$REPO"
echo "adapter.command=$CODEMEMORY_BIN ${COMMAND[*]}"
echo "adapter.attempts=$attempts_made/$MAX_ATTEMPTS"
echo "adapter.exit_code=$last_exit"
echo "--- command output ---"
echo "$last_output"

if [[ "$ok" == "true" ]]; then
    exit 0
fi

print_recovery_guidance "$last_exit" "$last_output"
if [[ "$last_exit" -eq 0 ]]; then
    exit 1
fi
exit "$last_exit"
