---
name: voiceuse-computer-control
description: Use when the VoiceUse Computer Control plugin is available and you need to control the local desktop through MCP tools. Guides agent to run the full observe, reason, act, verify loop using VoiceUse tools for screenshots, windows, clicks, typing, keys, waiting, and app focus.
---

# VoiceUse Computer Control

## Loop

1. Call `voiceuse_observe_screen` before acting.
2. Decide the smallest safe next action.
3. Use `voiceuse_click`, `voiceuse_type_text`, `voiceuse_press_key`, `voiceuse_wait`, `voiceuse_open_app`, or `voiceuse_focus_window`.
4. Call `voiceuse_observe_screen` again to verify.
5. Continue until the user-visible result is complete.

## Rules

- Prefer `voiceuse_press_key` and `voiceuse_type_text` when they are more reliable than clicking.
- Use `voiceuse_list_windows` when app focus is unclear.
- Do not use shell commands for desktop control. This plugin intentionally does not expose a shell tool.
- Stop and report the blocker if the task requires credentials, destructive confirmation, hidden UI, or ambiguous controls.
- Treat every action as operating on the user's real desktop.
