# Wave Orchestration

Use with the **wave-execution** skill. The orchestrator (main agent) registers tasks, spawns parallel sub-agent sessions, monitors progress, and closes when merge gates pass.

## Task registry JSON

```json
{
  "tasks": [
    {
      "taskId": "T1",
      "goal": "Refactor auth middleware. Owned paths only.",
      "ownedPaths": ["src/auth/"],
      "handoffPath": ".planning/execution/handoffs/wave-auth-refactor/T1.md",
      "provider": "cursor-composer"
    },
    {
      "taskId": "T2",
      "goal": "Add auth regression tests.",
      "ownedPaths": ["tests/auth/"],
      "handoffPath": ".planning/execution/handoffs/wave-auth-refactor/T2.md",
      "provider": "cursor-composer"
    }
  ]
}
```

## Orchestrator flow

1. Start stack: `cursor-subagent bus start` and `cursor-subagent daemon start`
2. Lock wave goal, task ids, dependencies, write ownership, verification commands
2. `cursor-subagent wave create --wave-id wave-auth-refactor --goal "..." --tasks tasks.json`
3. `cursor-subagent wave spawn wave-auth-refactor --cwd . --json`
4. Monitor: `cursor-subagent wave status wave-auth-refactor --json`
5. Per-session: `cursor-subagent watch <sessionId>` or `send` for corrections
6. Verify handoff files exist at declared paths
7. Run project gate commands (typecheck, tests, build)
8. `cursor-subagent wave close wave-auth-refactor --json`

## Rules

- Parallelize by **disjoint write scope** only
- One session per wave task
- Sub-agents must write handoff artifacts before the orchestrator marks tasks complete
- Do not close the wave until integration review and verification pass
