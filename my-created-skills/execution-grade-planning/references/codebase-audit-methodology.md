# Codebase Audit Methodology

A structured approach for comparing two or more repos before planning infrastructure work. Derived from actual session work comparing `subagent-tool` (Python execution engine) vs `agent-communication-server` (Rust communication bus).

## When to use

The user mentions "check out my other project" or "we already built most of this" during planning. Stop planning and audit.

## Step-by-step

### 1. Discover & clone

```bash
git clone https://github.com/<owner>/<repo>.git <temp-dir>
```

### 2. Surface-level scan

```bash
# File tree by extension
find . -name "*.py" -o -name "*.rs" -o -name "*.toml" -o -name "*.md" | head -80

# Top-level structure
ls -la && cat README.md 2>/dev/null

# Dependencies / build system
cat Cargo.toml 2>/dev/null || cat pyproject.toml 2>/dev/null

# Project docs (AI instructions may reveal architecture)
cat AGENTS.md 2>/dev/null
cat SKILL.md 2>/dev/null
```

### 3. Deep-read the core modules

For each significant module/file:
- **What it does** (docstring or first few lines)
- **What NATS subjects it touches** (publish only? subscribe only? both?)
- **What external APIs it calls** (HTTP, SDK, subprocess?)
- **What state it manages** (in-memory? SQLite? filesystem?)
- **What lifecycle patterns it has** (spawn? cancel? cleanup?)

### 4. Build a capability matrix

| Dimension | Repo A | Repo B | Gap / Overlap Type |
|---|---|---|---|
| NATS pub | Yes | Yes | Overlap |
| NATS sub | Yes | No | A has, B lacks |
| Provider abstraction | No | Yes | B has, A lacks |
| Structured protocol | Yes (Envelope) | Raw JSON | A has, B lacks |
| Persistence | None | SQLite | B has, A lacks |
| Language | Rust | Python | Different stack |
| ... | ... | ... | ... |

### 5. Classify the relationship

**Overlapping**: same language, same layer, same function.
→ Candidate for dedup or replace with one winner.

**Complementary**: different layers of the same stack.
→ Candidate for absorb (add as dependency/submodule).
→ Example from real session: agent-communication-server = communication bus (Rust, NATS messaging, agent registration, presence). subagent-tool = execution engine (Python, provider abstraction, session lifecycle, automation, persistence, REST API). They solve different problems on the same NATS backbone.

**Unrelated**: different domain.
→ No reuse. Plan from scratch.

### 6. Report with the decision fork

Present the user a three-option fork:

```
  OPTION A — Overwrite:  Replace repo B with repo A. Only if they overlap entirely.
  OPTION B — Absorb:     Import repo A as a dependency of repo B. Extend where needed.
  OPTION C — Build:      Nothing reusable, plan fresh.

  Recommendation: [your pick + reasoning]
```

Let the user decide — do not assume.

## Exit criteria

- You know exactly which capabilities exist in which repo.
- You have a clear "build vs absorb vs overwrite" answer for each missing capability.
- The user has chosen a direction before you move to execution packets.

## Pitfalls from real usage

- **README optimism**: READMEs describe what the author intended, not what actually compiles/runs. Read source.
- **NATS ≠ bidirectional**: A repo with NATS code may only publish (one-directional). Check `subscribe` calls explicitly.
- **Same library, different patterns**: Both repos may use `async-nats` but one uses it for pub-only while the other does full sub/pub. The library alone doesn't tell you the architecture.
- **Language boundary**: Absorbing a Rust crate into a Python project requires a bridge (subprocess, FFI, or sidecar). Factor that cost into the decision.
