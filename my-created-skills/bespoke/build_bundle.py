"""Bundle the bespoke router skill into one uploadable zip (e.g. for claude.ai).

In the repo, bespoke/SKILL.md is the router and each specialist is a nested
sub-skill (<sub-skill>/SKILL.md), read on demand. Uploaders that scan for every
SKILL.md would see seven skills, so the zip renames the sub-skills to GUIDE.md:

    bespoke/SKILL.md              <- the router, with sub-skill paths pointed at GUIDE.md
    bespoke/references/sources.md
    bespoke/<sub-skill>/GUIDE.md  <- each sub-skill's SKILL.md, frontmatter stripped
    bespoke/<sub-skill>/references/..., scripts/...

Run: python build_bundle.py
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SUBSKILLS = [
    "interface-guidelines",
    "interface-motion",
    "devtool-visual-system",
    "bento-grids",
    "signature-effects",
    "command-menu",
]
# Root files that are repo tooling, not skill content.
ROOT_EXCLUDE = {"build_bundle.py", "README.md", "SKILL.md"}


def split_frontmatter(text: str) -> str:
    m = re.match(r"---\r?\n.*?\r?\n---\r?\n+", text, re.S)
    assert m, "missing frontmatter"
    return text[m.end():]


def build_entry() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    body = split_frontmatter(text)
    frontmatter = text[: len(text) - len(body)]
    body = body.replace("`SKILL.md`", "`GUIDE.md`").replace("/X/SKILL.md", "/X/GUIDE.md")
    for name in SUBSKILLS:
        body = body.replace(f"{name}/SKILL.md", f"{name}/GUIDE.md")
    assert "SKILL.md" not in body, "router still references SKILL.md"
    return frontmatter + body


def main() -> None:
    DIST.mkdir(exist_ok=True)
    out = DIST / "bespoke.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("bespoke/SKILL.md", build_entry())
        for f in sorted(ROOT.iterdir()):
            if f.is_file() and f.name not in ROOT_EXCLUDE:
                z.write(f, "bespoke/" + f.name)
        for f in sorted((ROOT / "references").rglob("*")):
            if f.is_file():
                z.write(f, "bespoke/" + f.relative_to(ROOT).as_posix())
        for name in SUBSKILLS:
            for f in sorted((ROOT / name).rglob("*")):
                if not f.is_file():
                    continue
                if f.name == "SKILL.md":
                    body = split_frontmatter(f.read_text(encoding="utf-8"))
                    z.writestr(f"bespoke/{name}/GUIDE.md", body)
                else:
                    z.write(f, f"bespoke/{f.relative_to(ROOT).as_posix()}")
    with zipfile.ZipFile(out) as z:
        for n in z.namelist():
            print(n)
    print(f"-> {out}")


if __name__ == "__main__":
    main()
