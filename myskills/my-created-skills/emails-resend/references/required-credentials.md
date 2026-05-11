# Credentials and files on a new machine (reference)

Agents should **remind the user** when any of these are missing before running sends, Sheets updates, Gmail sync, or the webhook.

## Copy more than `.env`

Copying **only** `scripts/emails/.env` from another PC is usually **not** enough.

1. **Edit every path inside `.env`**  
   Keys like `GOOGLE_SERVICE_ACCOUNT_JSON`, `GMAIL_OAUTH_CLIENT_SECRET_JSON`, and `GMAIL_OAUTH_TOKEN_JSON` point to **files**. Those paths must exist on the new machine (update drive letters, usernames, and folders).

2. **Copy the files those paths reference**  
   Typical examples:
   - **Google Sheets:** service account JSON (path in `GOOGLE_SERVICE_ACCOUNT_JSON`). Share the Sheet with that service account’s **client email**.
   - **Gmail scripts** (`sync_replies_gmail.py`, `reply_followups.py`, etc.): OAuth **client** JSON (see below) + **`gmail_token.json`** (or whatever `GMAIL_OAUTH_TOKEN_JSON` is). If the token file is missing, the user may need to **run OAuth again** on the new machine.

3. **Never commit user tokens**  
   Files like **`gmail_token.json`** (refresh/access tokens) are **user-specific secrets**. Keep them out of git and copy them securely if moving machines.

## OAuth desktop client JSON (`scripts/emails/credentials/google_oauth_desktop.json`)

- **Committed template:** `credentials/google_oauth_desktop.json.example` — copy to `google_oauth_desktop.json` and fill from [Google Cloud Console](https://console.cloud.google.com/) (OAuth 2.0 Client ID, Desktop app). Point `GMAIL_OAUTH_CLIENT_SECRET_JSON` at the real file.
- The real **`google_oauth_desktop.json` is gitignored**. It is **not** a public secret: it contains **`client_id`** and **`client_secret`**. If those were ever pushed to a remote, **rotate the OAuth client** in Google Cloud and replace local files.
- **`gmail_token.json`** (user refresh token) is gitignored — never commit; copy securely between machines or re-run OAuth.
- Agents should **not** paste OAuth JSON or tokens into chat.

## What each workflow needs (minimal)

| Goal | Typical env / files |
|------|---------------------|
| **Batch send** (`send_campaign.py`) | `RESEND_API_KEY`, `RESEND_FROM`, `GOOGLE_SHEETS_ID`, `GOOGLE_SHEETS_TAB`, `GOOGLE_SERVICE_ACCOUNT_JSON` (or ADC on GCP) |
| **Gmail reply sync** | Above + `GMAIL_OAUTH_CLIENT_SECRET_JSON` + `GMAIL_OAUTH_TOKEN_JSON` (token file after OAuth) |
| **Resend webhook server** (`webhook_server.py`) | `RESEND_WEBHOOK_SECRET`, Sheet vars, bind/port (e.g. `WEBHOOK_PORT`). Optional PostHog (below). |
| **PostHog from webhook** | `POSTHOG_PROJECT_API_KEY`, `POSTHOG_HOST`, `POSTHOG_ENABLED` (if you forward events) |

Sending mail **does not** require webhook or PostHog vars on the **same** laptop if the webhook runs elsewhere (e.g. VM). You still need Resend + Sheets for `send_campaign.py`.

## Example: `.env` slices (placeholders only)

**Resend + Sheets (sending and sheet updates from this tool):**

```env
RESEND_API_KEY=re_xxxxxxxx
RESEND_FROM="Name <send@verified.domain>"
RESEND_REPLY_TO="inbox@yourdomain.com"
GOOGLE_SHEETS_ID=your_sheet_id
GOOGLE_SHEETS_TAB=Email Tracking
GOOGLE_SERVICE_ACCOUNT_JSON=/home/you/keys/service-account.json
```

**Gmail OAuth paths (adjust paths after copying files):**

```env
GMAIL_OAUTH_CLIENT_SECRET_JSON=/home/you/m26pipeline/scripts/emails/credentials/google_oauth_desktop.json
GMAIL_OAUTH_TOKEN_JSON=/home/you/m26pipeline/scripts/emails/gmail_token.json
```

**Webhook server (only when running `webhook_server.py` on this host):**

```env
RESEND_WEBHOOK_SECRET=whsec_xxxxxxxx
WEBHOOK_PORT=8787
```

**PostHog (optional, if webhook forwards analytics):**

```env
POSTHOG_PROJECT_API_KEY=phc_xxxxxxxx
POSTHOG_HOST=https://us.i.posthog.com
POSTHOG_ENABLED=true
```

Resend’s dashboard must point the **webhook URL** at this server’s public URL (or tunnel), with the **same** signing secret you configure locally.

## Checklist for the user on a new PC

1. Sparse clone or copy **`scripts/emails`**, **`python -m venv .venv`**, **`pip install -r requirements.txt`**.  
2. Copy **`.env`** and **every JSON/key file** referenced inside it; **fix paths**.  
3. Copy **`gmail_token.json`** if Gmail tools should work without re-auth (or complete OAuth once).  
4. Confirm **Google Sheet** is shared with the service account email.  
5. Confirm **Resend** domain/`RESEND_FROM` is verified.  
6. Run **`--dry-run`** before real sends.
