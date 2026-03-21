# UTM parameters and readable links (reference)

## Keep copy clean

- **HTML:** Short anchor text, full URL (including `utm_*`) in **`href`**.
- **Markdown → HTML:** `[Get started](https://example.com/?utm_...)` so readers see “Get started,” not the raw query string.
- **Plain-text part:** Long URLs are normal; optional branded short links add moving parts.

## Typical UTM shape (Resend campaigns)

Base idea (replace host and merge fields):

```
https://YOUR_SITE/?utm_source=resend&utm_medium=email&utm_campaign={campaign_id}&utm_content={content_variant}&utm_term={recipient_email}
```

Cold-email tools that use merge syntax may use `{{email}}` instead of `{email}` for the last parameter.

## CLI helper

From **`scripts/emails`** with venv active:

```bash
python build_utm_link.py --utm-campaign YOUR_CAMPAIGN --utm-content YOUR_VARIANT --utm-term someone@example.com
```

From a **full** monorepo root:

```bash
python -m scripts.emails.build_utm_link --utm-campaign YOUR_CAMPAIGN ...
```

## GIF vs UTM

`--utm-content` is analytics metadata only. The GIF shown in templates comes from **`--gif-url`** or **`EMAIL_GIF_URL` / `GIF_URL`** env vars — see **`send_campaign.py`** and **`scripts/emails/AGENTS.md`**.
