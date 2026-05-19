# Creator System — Authorship & Attribution

## Overview

Every workflow template has a **creator** (who built the workflow) and optionally a **model brand** (the AI model it uses). These are independent:

- **Creator** = person/team who made the workflow (stored as `username`)
- **Model brand** = AI provider logo shown on thumbnails (stored in `logos[]`)

## Data Model

### `templates/creators.json`

Single source of truth for creator profiles, keyed by username:

```json
{
  "ComfyUI": {
    "displayName": "ComfyUI",
    "handle": "ComfyUI",
    "summary": "Official ComfyUI workflow templates created by the Comfy team.",
    "social": "x.com/comaboratory"
  },
  "hellorob": {
    "displayName": "RobTheMan",
    "handle": "hellorob",
    "summary": "Rob is a core member of the ComfyUI creative team...",
    "social": "x.com/hellorob"
  }
}
```

Fields:
- `displayName` — Shown on cards, profile pages, spotlights
- `handle` — Used in URLs and @mentions (usually matches the key)
- `summary` — Bio text for profile pages
- `social` — Social link (without `https://` prefix)
- `avatarUrl` — (optional) URL to avatar image; if absent, initial-based avatar is generated
- `coverUrl` — (optional) Profile cover image

### `templates/index.json` — The `username` Field

Every template entry links to a creator:

```json
{
  "name": "flux_text_to_image",
  "title": "Flux Text to Image",
  "username": "ComfyUI",
  "logos": [{ "provider": "Flux" }]
}
```

- `username` maps to a key in `creators.json`
- Default is `"ComfyUI"` for official templates
- `logos[].provider` is **model branding only** (thumbnail overlay) — NOT authorship

## Adding a New Creator

1. Add entry to `templates/creators.json`
2. Set `"username": "newuser"` on their templates in `templates/index.json`
3. Run `pnpm run sync` in `site/` to propagate changes
4. Profile page at `/workflows/newuser/` is automatically generated

## Common Mistakes

- **Don't use `logos[0].provider` as the author** — that's model branding (e.g. "Grok", "Flux"), not who made the workflow
- **Don't hardcode creator data in components** — always resolve from `creators.json` via username
- **Remember to run sync** after changing `index.json`

## URL Structure

- `/workflows/` — Hub page with all templates
- `/workflows/{username}/` — Creator profile page
- `/workflows/{template-name}/` — Individual template detail page
