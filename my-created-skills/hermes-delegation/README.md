# Hermes external CLI delegation

One router skill (`SKILL.md` here) plus its subskills: skills that teach a
Hermes agent how to hand work to an external coding-agent CLI, and the shared
supervision workflow those runs use.

The subskills are physical subdirectories of the router, matching the Hermes
skill-router convention (`m26-security-skill-router`, `frontend-design-skill-router`):
the skill index lists them as one group — `hermes-delegation` with each child
beneath it — and the router's routing questions send you to exactly one child
`SKILL.md` at a time.

| Subskill | CLI |
| --- | --- |
| `codex/` | OpenAI Codex (`codex exec`) |
| `opencode/` | OpenCode (`opencode run`) |
| `grok-build-cli/` | xAI Grok Build (`grok -p`) |
| `antigravity-cli/` | Antigravity (`agy -p`) |
| `muse-code-cli/` | Meta Muse Code (`muse exec`) |
| `devin-cli/` | Cognition Devin (`devin -p`) |
| `coding-agent-supervision/` | Class workflow for background runs: liveness, recovery, review |

Each subskill is a `SKILL.md` plus any `references/`. The live copies Hermes
loads are the profile originals; this folder is the published snapshot.
