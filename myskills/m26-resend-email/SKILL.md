---
name: m26-resend-email
description: Operate Resend email campaigns, webhooks, Gmail reply sync, and Google Sheets tracking for the m26pipeline scripts/emails toolkit. Use when sending batch mail via send_campaign, syncing replies, running the email webhook server, UTM links, Resend API keys, sparse-clone setup, idempotency, or follow-up cohorts. Applies to any environment once scripts/emails is present or fetched from GitHub.
---

# M26 Resend email automation

Assume the upstream layout **`scripts/emails/`** exists (or will be materialized). All procedures below use **`cd` into `scripts/emails`**, a **venv**, and **`python <script>.py`** unless the user is in a **full monorepo** from the repository root, where **`python -m scripts.emails.<name>`** is also valid.

## First: materialize `scripts/emails`

If the folder is missing, obtain a **sparse checkout** of only that path (not the whole monorepo working tree). Full step-by-step commands, Windows junctions, and Linux symlinks live in **`scripts/emails/MINIMAL_CLONE.md`** in the upstream repo.

Minimum idea:

1. Clone with `--filter=blob:none --sparse`, then **`git sparse-checkout init --no-cone`** and **`git sparse-checkout set --no-cone '/scripts/emails/'`**.
2. **`cd scripts/emails`**, create **`.venv`**, **`pip install -r requirements.txt`**, copy **`.env`** from **`.env.example`** (or from another machine — see below).
3. Updates: **`git pull`** from the sparse clone root.

**New machine / copied workspace:** Copy **`.env`** *and* **every file paths inside it** (service account JSON, Gmail OAuth client JSON, `gmail_token.json`, etc.), then **edit paths** so they match the new filesystem. Copying `.env` alone often breaks because paths still point at the old PC. Agents should **ask for missing keys or files** before sending. Full checklist: **`references/required-credentials.md`**.

Do **not** run **`python scripts/emails/foo.py` from the monorepo root** (path through `scripts/emails/`). Either **`cd scripts/emails`** and run **`python foo.py`**, or from full repo use **`python -m scripts.emails.foo`**.

Secrets stay in **`.env`** or the environment — never commit API keys, webhook secrets, or Gmail token files.

## Core scripts (from `scripts/emails`)

| Script | Role |
|--------|------|
| `send_campaign.py` | Batch sends via Resend + Google Sheet rows |
| `sync_replies_gmail.py` | Pull inbox replies (Resend webhooks do not replace this) |
| `webhook_server.py` | Receives Resend events → Sheet columns (`opened_N`, `clicked_N`, …) |
| `reply_followups.py` | Threaded Gmail/Resend replies |
| `build_utm_link.py` | Build tracked links with consistent UTM params |

Details, flags, and examples: **`scripts/emails/README.md`**. Operational guardrails: **`scripts/emails/AGENTS.md`**.

## Resend behavior (short)

- **Opens/clicks:** Emitted when **domain-level** open/click tracking is enabled in Resend; webhooks can fire **`email.opened`** / click events. Open rates are imperfect (clients blocking images, etc.).
- **Inbox replies:** Not a substitute for **`sync_replies_gmail.py`** before follow-up sends.

## UTM and readable links

Put long query strings in the **HTML `href`** (or Markdown **`[visible text](url)`**). Visible copy stays short; parameters stay on the URL. Parameter pattern and generators: see **`references/utm-and-links.md`**.

## Idempotency and safety

- **`send_campaign`:** idempotency keys tie to campaign + chunk; reuse within 24h with a different body → **409**. Use a test campaign id or **`--idempotency-suffix`** for experiments.
- Before production sends: **`--dry-run`**, **`--show-selected`**, validate templates.

## When to load bundled references

- Clone/symlink mechanics, sparse-checkout pitfalls → **`references/clone-and-layout.md`**
- **`.env`, paths, copied key files, webhook vs send-only, PostHog** → **`references/required-credentials.md`**
- UTM + link presentation → **`references/utm-and-links.md`**
- Checklists (reply sync timing, batch columns, GIF env vars) → **`references/operational-rules.md`**

Upstream canonical copies evolve in **`scripts/emails/MINIMAL_CLONE.md`** and **`scripts/emails/AGENTS.md`**; refresh this skill when those change materially.
