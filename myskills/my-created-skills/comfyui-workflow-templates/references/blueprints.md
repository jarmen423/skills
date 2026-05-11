# Subgraph Blueprints

Subgraph Blueprints are pre-built workflow components that appear as single nodes in ComfyUI. They abstract complex node configurations into user-friendly creative primitives (e.g., "Text to Image" or "Style Transfer").

## Directory Structure

```
blueprints/
├── index.json                        # Blueprint metadata index (generated)
├── index.schema.json                 # JSON schema for index validation
├── text_to_image_flux_1_dev.json     # Blueprint definition (native ComfyUI format)
└── text_to_image_flux_1_dev-1.webp   # Preview thumbnail (optional)

blueprints_bundles.json               # Maps blueprints to package

scripts/
├── import_blueprints.py              # Import and normalize external blueprints
└── sync_blueprints.py                # Generate manifest + sync assets

packages/core/src/comfyui_workflow_templates_core/
├── blueprints_manifest.json          # Generated manifest
└── loader.py                         # Python API (extended for blueprints)
```

## Blueprint JSON Format

Blueprint files use the **native ComfyUI subgraph format** (same format exported by ComfyUI when saving a subgraph).

### Structure Overview

```json
{
  "id": "78bdb6eb-f866-4a7f-98fd-1dca28934520",
  "revision": 0,
  "last_node_id": 48,
  "last_link_id": 0,
  "nodes": [
    {
      "id": -1,
      "type": "82187329-39e2-40fd-ac5b-4554be4b2cec",
      "inputs": [...],
      "outputs": [...],
      "properties": {
        "proxyWidgets": [["-1", "text"], ["31", "seed"]]
      },
      "widgets_values": ["", 1024, 1024]
    }
  ],
  "links": [],
  "groups": [],
  "definitions": {
    "subgraphs": [
      {
        "id": "82187329-39e2-40fd-ac5b-4554be4b2cec",
        "version": 1,
        "name": "Text to Image (Flux.1 Dev)",
        "inputs": [...],
        "outputs": [...],
        "nodes": [...],
        "links": [...],
        "groups": [...]
      }
    ]
  },
  "version": 0.4
}
```

### Key Components

| Path | Description |
|------|-------------|
| `id` | UUID of the workflow file |
| `nodes[0]` | The subgraph node instance (id=-1, type=subgraph UUID) |
| `nodes[0].properties.proxyWidgets` | Widget values exposed on the node UI |
| `definitions.subgraphs[0]` | The actual subgraph definition |
| `definitions.subgraphs[0].name` | Display name shown in node palette |
| `definitions.subgraphs[0].inputs` | Exposed input slots |
| `definitions.subgraphs[0].outputs` | Exposed output slots |
| `definitions.subgraphs[0].nodes` | Internal ComfyUI nodes |
| `definitions.subgraphs[0].links` | Internal connections |

### Input/Output Slot Format

```json
{
  "id": "669e384e-5e26-4291-9bac-e1d1f04b4a16",
  "name": "text",
  "type": "STRING",
  "linkIds": [68],
  "pos": [-990, 431]
}
```

Supported slot types: `IMAGE`, `LATENT`, `MODEL`, `STRING`, `INT`, `FLOAT`, `CLIP`, `VAE`, `CONDITIONING`

### Internal Node with Model Metadata

```json
{
  "id": 38,
  "type": "UNETLoader",
  "pos": [-810, 140],
  "properties": {
    "cnr_id": "comfy-core",
    "ver": "0.3.40",
    "models": [
      {
        "name": "flux1-dev.safetensors",
        "url": "https://huggingface.co/...",
        "directory": "diffusion_models"
      }
    ]
  },
  "widgets_values": ["flux1-dev.safetensors", "default"]
}
```

## Index Metadata (index.json)

Generated from blueprint JSON files using `scripts/import_blueprints.py`. Do not edit manually.

```json
[
  {
    "moduleName": "default",
    "title": "Text to Image",
    "blueprints": [
      {
        "name": "text_to_image_flux_1_dev",
        "title": "Text to Image (Flux.1 Dev)",
        "description": "Text to Image (Flux.1 Dev) blueprint",
        "mediaType": "image",
        "mediaSubtype": "webp",
        "inputs": [
          {"name": "text", "type": "STRING"},
          {"name": "width", "type": "INT"},
          {"name": "height", "type": "INT"}
        ],
        "outputs": [
          {"name": "IMAGE", "type": "IMAGE"}
        ],
        "models": ["ae.safetensors", "flux1-dev.safetensors"]
      }
    ]
  }
]
```

## Adding New Blueprints

### Option 1: Import from External Source

```bash
# 1. Place blueprint JSON files in blueprints/ directory
# 2. Import and normalize
python scripts/import_blueprints.py
# 3. Sync to packages
python scripts/sync_blueprints.py
```

### Option 2: Create in ComfyUI

1. Build workflow in ComfyUI
2. Select nodes → Create Subgraph
3. Export workflow JSON
4. Copy to `blueprints/` with `snake_case` filename
5. Run import and sync scripts

### Naming Conventions

- **Filename**: `snake_case.json` (e.g., `text_to_image_flux_1_dev.json`)
- **Display name**: Stored in `definitions.subgraphs[0].name`
- **Thumbnails**: `blueprint_name-1.webp`, `blueprint_name-2.webp`

## Python API

```python
from comfyui_workflow_templates_core.loader import (
    iter_blueprints,
    get_blueprint_entry,
    get_blueprint_asset_path,
)

# List all blueprints
for bp in iter_blueprints():
    print(f"{bp.blueprint_id}: {bp.version}")

# Get asset path and load JSON
path = get_blueprint_asset_path("text_to_image_flux_1_dev", "text_to_image_flux_1_dev.json")
import json
with open(path) as f:
    blueprint = json.load(f)
    subgraph = blueprint["definitions"]["subgraphs"][0]
    print(f"Name: {subgraph['name']}")
    print(f"Inputs: {[i['name'] for i in subgraph['inputs']]}")
```

## Workflow Templates vs Subgraph Blueprints

| Aspect | Workflow Templates | Subgraph Blueprints |
|--------|-------------------|---------------------|
| Purpose | Full standalone workflows | Reusable node components |
| Appears as | Workflow template picker | Node in palette |
| Packages | Split by media type | Single package |
| Format | Standard workflow JSON | Subgraph definition with `definitions.subgraphs` |
| Use case | Starting point for users | Building blocks for workflows |

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/import_blueprints.py` | Normalize filenames, generate index.json and bundles |
| `scripts/sync_blueprints.py` | Generate manifest, copy assets to package directories |
