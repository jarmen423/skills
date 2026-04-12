# Publishing Workflow Templates Packages

## Package Structure

Seven wheels are produced:
- `comfyui-workflow-templates-core`
- `comfyui-workflow-templates-media-api`
- `comfyui-workflow-templates-media-video`
- `comfyui-workflow-templates-media-image`
- `comfyui-workflow-templates-media-other`
- `comfyui-subgraph-blueprints`
- `comfyui-workflow-templates` (meta package, built from root `pyproject.toml`)

## CI Automation

Publishing is **largely automated**:
- `.github/workflows/version-check.yml` runs `scripts/ci_version_manager.py` on PRs touching templates or `bundles.json`, auto-bumping affected package versions
- `.github/workflows/publish.yml` triggers on pushes to `main` that change `pyproject.toml`, builds and publishes all packages, then creates a GitHub Release

## Manual Publishing

### Prerequisites

```bash
pipx install build twine
# Have API tokens for TestPyPI and PyPI (project:comfyui-workflow-templates-*)
```

### Build Locally

```bash
git checkout main && git pull
./run_full_validation.sh
```

Regenerates manifest, builds all wheels into `./dist/`, runs lint/tests, runs `twine check`.

### Version Bumping

```bash
python scripts/ci_version_manager.py
```

Detects changed packages and applies patch-level bumps.

### Upload to TestPyPI

```bash
export TWINE_REPOSITORY=testpypi
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-<testpypi-token>"

for pkg in core media_api media_video media_image media_other; do
  twine upload dist/comfyui_workflow_templates_${pkg}-*.whl dist/comfyui_workflow_templates_${pkg}-*.tar.gz
done
twine upload dist/comfyui_subgraph_blueprints-*.whl dist/comfyui_subgraph_blueprints-*.tar.gz
twine upload dist/comfyui_workflow_templates-*.whl dist/comfyui_workflow_templates-*.tar.gz
```

### Publish to PyPI

Switch `TWINE_REPOSITORY=pypi` and repeat the upload loop.

## Full Contribution Workflow

1. Create workflow JSON with embedded model metadata
2. Generate thumbnails (WebP, 512×512+, under 1MB)
3. Add entry to `templates/index.json` in appropriate category
4. Add template ID to `bundles.json` (required — CI enforces this)
5. Run `python scripts/sync_bundles.py` to regenerate manifests
6. Run `python scripts/sync_data.py` for translation syncing
7. Bump version in `pyproject.toml`
8. Run `./run_full_validation.sh`
9. Submit PR

## Troubleshooting

- **Upload interrupted**: Rerun `twine upload`; already-uploaded files are rejected (that's OK)
- **Wrong file uploaded**: Delete from TestPyPI UI; contact admins for PyPI (no overwriting)
- **Missing token permissions**: Ensure scope includes `project:comfyui-workflow-templates-*`
- **Packages out of sync**: Trigger publish workflow manually via `workflow_dispatch` (recovery mode detects mismatches)
