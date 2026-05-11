---
name: comfyui-workflow-templates
description: >
  Work with ComfyUI workflow templates and subgraph blueprints from the
  Comfy-Org/workflow_templates repository. Use when: creating new workflow
  templates (JSON + thumbnails + index.json metadata), adding or modifying
  subgraph blueprints, managing creator attribution, understanding the
  template/blueprint file format and schema, running validation scripts,
  contributing to the templates repository, or publishing the Python packages.
  Source of truth: https://github.com/Comfy-Org/workflow_templates
---

# ComfyUI Workflow Templates

## Overview

The `Comfy-Org/workflow_templates` repo distributes ComfyUI workflow templates and subgraph blueprints as Python packages (`comfyui-workflow-templates-*`). It is a Python monorepo with Nx, producing 7 wheels across 4 media-type bundles.

**Two distinct artifact types:**
- **Workflow templates** — full standalone workflows (`.json` + `.webp` thumbnails + `index.json` metadata)
- **Subgraph blueprints** — reusable node components that appear as single nodes in the ComfyUI palette

## Key Directories

```
templates/          # Workflow JSONs, thumbnails, index.json (+ 10 locale variants)
blueprints/         # Blueprint JSONs, thumbnails, index.json (generated)
packages/           # Python source: core, media_api, media_image, media_video, media_other, blueprints
scripts/            # validate_templates.py, sync_bundles.py, sync_data.py, import_blueprints.py, etc.
bundles.json        # Maps templates to packages (media-api, media-image, media-video, media-other)
docs/               # SPEC.md, BLUEPRINTS.md, CREATORS.md, publishing-workflow-templates.md
```

## Adding a Workflow Template

1. Create `templates/<name>.json` — valid ComfyUI workflow JSON with embedded model metadata
2. Create `templates/<name>-1.webp` (and optionally `-2.webp`) — WebP thumbnail, 512×512+, under 1MB
3. Add metadata entry to `templates/index.json` under the appropriate category
4. Add template name to `bundles.json` under the correct media bundle
5. Run validation: `python scripts/validate_templates.py`
6. Run sync: `python scripts/sync_bundles.py && python scripts/sync_data.py`
7. Bump version in `pyproject.toml`

**Naming**: `^[a-zA-Z0-9._-]+$` only (no spaces). Thumbnails must be `{name}-{N}.{mediaSubtype}`.

For the full schema (all index.json fields, model metadata format, thumbnail variants, validation details): read **[references/spec.md](references/spec.md)**

## Adding a Blueprint

1. Create blueprint JSON in `blueprints/` using native ComfyUI subgraph format (`snake_case.json`)
2. Run `python scripts/import_blueprints.py` — normalizes filenames, generates `blueprints/index.json`
3. Run `python scripts/sync_blueprints.py` — syncs assets to packages

For the full blueprint JSON schema, Python API, and comparison with workflow templates: read **[references/blueprints.md](references/blueprints.md)**

## Creator Attribution

Templates link to creators via `"username"` in `index.json`. Creator profiles live in `templates/creators.json`. The `logos[].provider` field is model branding only — not authorship.

For the full creator data model, component architecture, and how to add creators: read **[references/creators.md](references/creators.md)**

## Validation & Publishing

```bash
# Validate before any PR
python scripts/validate_templates.py
python scripts/validate_blueprints.py

# Full validation + build
./run_full_validation.sh
```

CI auto-bumps versions and publishes to PyPI on merge to `main`. For manual publishing procedures, TestPyPI workflow, and troubleshooting: read **[references/publishing.md](references/publishing.md)**

## Embedded Model Metadata (Required in Workflow JSONs)

```json
{
  "properties": {
    "models": [
      {
        "name": "model_filename.safetensors",
        "url": "https://huggingface.co/...",
        "hash": "sha256_hash",
        "hash_type": "SHA256",
        "directory": "models/checkpoints"
      }
    ]
  }
}
```
