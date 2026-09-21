# Hermes external CLI delegation

Skills that teach a Hermes agent how to hand work to an external coding-agent
CLI, plus the shared supervision workflow those runs use.

| Directory | CLI |
| --- | --- |
| `codex/` | OpenAI Codex (`codex exec`) |
| `opencode/` | OpenCode (`opencode run`) |
| `grok-build-cli/` | xAI Grok Build (`grok -p`) |
| `antigravity-cli/` | Antigravity (`agy -p`) |
| `muse-code-cli/` | Meta Muse Code (`muse exec`) |
| `coding-agent-supervision/` | Class workflow for background runs: liveness, recovery, review |

Each directory is a skill (`SKILL.md` plus any `references/`). The live copies
Hermes loads are the profile originals; this folder is the published snapshot.
