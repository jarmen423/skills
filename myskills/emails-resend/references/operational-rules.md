# Operational rules (reference)

Canonical source: **`scripts/emails/AGENTS.md`**.

## Invocation

- **Preferred in sparse / email-only tree:** `cd scripts/emails`, venv on, `python send_campaign.py`, etc.
- **Full monorepo from root:** `python -m scripts.emails.send_campaign` (avoids `python scripts/emails/foo.py` from root).

## Pipeline

1. **Sends:** `send_campaign.py` (dry-run first).
2. **Opens/clicks:** Resend → webhook → Sheet columns `opened_N`, `clicked_N` (see `webhook_server.py`).
3. **Replies:** Run **`sync_replies_gmail.py`** before follow-ups — Resend webhooks do not replace inbox replies. **`RESEND_REPLY_TO`** should route to the Gmail inbox you sync.

## Follow-up timing

- Do **not** sync replies immediately after the first send.
- Sync **right before** a scheduled follow-up window; then send with **`--reply-status no`** where appropriate.
- Sheet must have **`sent_date_N`** populated for batch **`N`** or sync may find no rows.

## Sheet columns

Batch suffix pattern: **`sent_date_N`**, **`opened_N`**, **`clicked_N`**, **`reply_status_N`** (see upstream README).

## Idempotency (Resend)

Keys derive from campaign id + chunk. Reusing the same key within ~24h with a different body → **409 conflict**. Tests: **`--campaign-id *_test`** or **`--idempotency-suffix`**.

## Threaded replies

**`reply_followups.py`** — respect **`In-Reply-To` / `References`**; subject **`Re:`** unless disabled.

## Pre-send checklist

1. `--dry-run` + `--show-selected`
2. Template renders; links and GIF correct
3. Test campaign id or idempotency suffix for experiments
4. Before follow-ups: Gmail reply sync
5. Batch columns present and consistent
