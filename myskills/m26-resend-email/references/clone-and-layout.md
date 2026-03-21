# Clone and layout (reference)

Canonical source: `scripts/emails/MINIMAL_CLONE.md` in **m26pipeline**.

## Why cone-mode sparse checkout fails for `scripts/emails`

`git sparse-checkout set scripts/emails` in **cone** mode can still populate **all** of `scripts/`. Use **non-cone** and an explicit path with a **leading slash**:

```bash
git sparse-checkout init --no-cone
git sparse-checkout set --no-cone '/scripts/emails/'
```

Add **`/scripts/__init__.py`** as a second path only if you run **`python -m scripts.emails...`** from the **clone root** (optional).

## GitHub CLI

```bash
gh repo clone OWNER/m26pipeline m26pipeline-email-checkout -- --filter=blob:none --sparse
cd m26pipeline-email-checkout
git sparse-checkout init --no-cone
git sparse-checkout set --no-cone '/scripts/emails/'
```

## Venv and execution

```bash
cd m26pipeline-email-checkout/scripts/emails
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python send_campaign.py --help
```

## Workspace link (optional)

**Windows (junction — target must be absolute):**

```powershell
New-Item -ItemType Junction -Path ".\m26pipeline-emails-workspace" -Target "D:\path\to\m26pipeline-email-checkout\scripts\emails"
```

**Linux / macOS:**

```bash
ln -s /absolute/path/to/m26pipeline-email-checkout/scripts/emails m26pipeline-emails-workspace
```

Then **`cd`** into the junction/symlink path before running **`python *.py`**.

## Updates

```bash
cd m26pipeline-email-checkout
git pull
```
