#!/usr/bin/env python3
"""Create a compact repository snapshot for Excalidraw learning-aid planning.

The output is intentionally concise: tree, language/file counts, likely entrypoints,
manifest/config files, and a light import/dependency sample. It is not a static
analysis engine; use it as a map before reading important files.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "bower_components",
    "dist",
    "build",
    "coverage",
    "target",
    "out",
    "vendor",
    "__pycache__",
}

IGNORE_FILES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "uv.lock",
    "poetry.lock",
    "Pipfile.lock",
    "Cargo.lock",
    "go.sum",
}

MANIFEST_NAMES = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "Gemfile",
    "composer.json",
    "mix.exs",
    "deno.json",
    "tsconfig.json",
    "vite.config.ts",
    "next.config.js",
    "next.config.mjs",
    "Dockerfile",
    "docker-compose.yml",
    "compose.yaml",
}

BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
    ".gz", ".tar", ".tgz", ".mp4", ".mov", ".woff", ".woff2", ".ttf",
    ".otf", ".sqlite", ".db", ".lockb", ".wasm",
}

EXT_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript/react",
    ".ts": "typescript",
    ".tsx": "typescript/react",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".swift": "swift",
    ".scala": "scala",
    ".ex": "elixir",
    ".exs": "elixir",
    ".sql": "sql",
    ".tf": "terraform",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".md": "markdown",
}

ENTRYPOINT_HINTS = (
    "main", "index", "app", "server", "router", "routes", "handler", "controller",
    "cli", "command", "worker", "job", "consumer", "producer", "middleware",
)

IMPORT_PATTERNS = {
    "python": [
        re.compile(r"^\s*import\s+([\w\.]+)", re.MULTILINE),
        re.compile(r"^\s*from\s+([\w\.]+)\s+import\s+", re.MULTILINE),
    ],
    "javascript": [
        re.compile(r"^\s*import(?:[\s\S]*?)\sfrom\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
        re.compile(r"^\s*export(?:[\s\S]*?)\sfrom\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
        re.compile(r"require\(['\"]([^'\"]+)['\"]\)"),
    ],
    "go": [
        re.compile(r"^\s*import\s+\"([^\"]+)\"", re.MULTILINE),
        re.compile(r"^\s*\"([^\"]+)\"", re.MULTILINE),
    ],
    "java": [re.compile(r"^\s*import\s+([\w\.]+);", re.MULTILINE)],
    "ruby": [re.compile(r"^\s*require(?:_relative)?\s+['\"]([^'\"]+)['\"]", re.MULTILINE)],
}


def should_skip(path: Path) -> bool:
    name = path.name
    if path.is_dir() and name in IGNORE_DIRS:
        return True
    if path.is_file() and name in IGNORE_FILES:
        return True
    if path.suffix.lower() in BINARY_EXTS:
        return True
    return False


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_files(root: Path, max_depth: int, max_files: int) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        depth = len(current.relative_to(root).parts)
        dirnames[:] = [d for d in sorted(dirnames) if not should_skip(current / d)]
        if depth >= max_depth:
            dirnames[:] = []
        for filename in sorted(filenames):
            path = current / filename
            if should_skip(path):
                continue
            files.append(path)
            if len(files) >= max_files:
                return files
    return files


def build_tree(root: Path, max_depth: int, max_entries: int) -> list[str]:
    lines: list[str] = [root.name + "/"]
    count = 0

    def walk(directory: Path, prefix: str, depth: int) -> None:
        nonlocal count
        if count >= max_entries or depth > max_depth:
            return
        entries = [p for p in sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())) if not should_skip(p)]
        for idx, entry in enumerate(entries):
            if count >= max_entries:
                lines.append(prefix + "...")
                return
            connector = "└── " if idx == len(entries) - 1 else "├── "
            suffix = "/" if entry.is_dir() else ""
            lines.append(prefix + connector + entry.name + suffix)
            count += 1
            if entry.is_dir():
                extension = "    " if idx == len(entries) - 1 else "│   "
                walk(entry, prefix + extension, depth + 1)

    walk(root, "", 1)
    return lines


def read_text(path: Path, max_bytes: int = 200_000) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="ignore")
    except OSError:
        return ""


def language_for(path: Path) -> str:
    ext = path.suffix.lower()
    return EXT_LANGUAGE.get(ext, ext.lstrip(".") or "no extension")


def import_family(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext == ".py":
        return "python"
    if ext in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        return "javascript"
    if ext == ".go":
        return "go"
    if ext in {".java", ".kt"}:
        return "java"
    if ext == ".rb":
        return "ruby"
    return None


def extract_imports(path: Path) -> list[str]:
    family = import_family(path)
    if not family:
        return []
    text = read_text(path)
    found: list[str] = []
    for pattern in IMPORT_PATTERNS.get(family, []):
        for match in pattern.finditer(text):
            value = match.group(1).strip()
            if value and value not in found:
                found.append(value)
    return found[:20]


def find_entrypoint_hints(files: Iterable[Path], root: Path) -> list[str]:
    hints: list[str] = []
    for path in files:
        lower = path.stem.lower()
        parent = path.parent.name.lower()
        if any(token == lower or token in lower or token in parent for token in ENTRYPOINT_HINTS):
            hints.append(rel(path, root))
    return hints[:60]


def summarize(root: Path, args: argparse.Namespace) -> str:
    files = iter_files(root, args.max_depth, args.max_files)
    language_counts = Counter(language_for(path) for path in files)
    ext_counts = Counter(path.suffix.lower() or "[no extension]" for path in files)
    manifests = [rel(path, root) for path in files if path.name in MANIFEST_NAMES]
    entrypoints = find_entrypoint_hints(files, root)

    imports_by_file: dict[str, list[str]] = {}
    for path in files:
        imports = extract_imports(path)
        if imports:
            imports_by_file[rel(path, root)] = imports
        if len(imports_by_file) >= args.max_import_files:
            break

    lines: list[str] = []
    lines.append(f"# Repository snapshot: `{root.name}`")
    lines.append("")
    lines.append(f"Scanned {len(files)} files with max depth {args.max_depth}.")
    lines.append("")

    lines.append("## Language/file mix")
    for lang, count in language_counts.most_common(20):
        lines.append(f"- {lang}: {count}")
    lines.append("")

    lines.append("## Extension counts")
    for ext, count in ext_counts.most_common(20):
        lines.append(f"- {ext}: {count}")
    lines.append("")

    lines.append("## Manifests and config anchors")
    if manifests:
        for item in manifests[:80]:
            lines.append(f"- {item}")
    else:
        lines.append("- none found in scanned files")
    lines.append("")

    lines.append("## Likely entrypoint or boundary files")
    if entrypoints:
        for item in entrypoints:
            lines.append(f"- {item}")
    else:
        lines.append("- none detected from filename heuristics")
    lines.append("")

    lines.append("## Tree")
    lines.append("```text")
    lines.extend(build_tree(root, args.max_depth, args.max_tree_entries))
    lines.append("```")
    lines.append("")

    lines.append("## Import/dependency samples")
    if imports_by_file:
        for path, imports in imports_by_file.items():
            joined = ", ".join(imports[:12])
            lines.append(f"- `{path}` -> {joined}")
    else:
        lines.append("- no imports detected in scanned files")
    lines.append("")

    lines.append("## Diagram planning prompts")
    lines.append("- Which entrypoint starts the mechanism to teach?")
    lines.append("- Which runtime boundaries are real, and which are only folders/packages?")
    lines.append("- What data object or event moves through the system?")
    lines.append("- Which 3-8 files/functions deserve source-anchor labels?")
    lines.append("- What should a newcomer remember after one minute?")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a concise repo snapshot for visual explanation planning.")
    parser.add_argument("repo", help="Path to repository root")
    parser.add_argument("--output", "-o", help="Markdown output path; defaults to stdout")
    parser.add_argument("--max-depth", type=int, default=5, help="Max directory depth to scan")
    parser.add_argument("--max-files", type=int, default=600, help="Max files to scan")
    parser.add_argument("--max-tree-entries", type=int, default=250, help="Max entries in tree output")
    parser.add_argument("--max-import-files", type=int, default=80, help="Max files to include in import sample")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"repo path does not exist or is not a directory: {root}")
    markdown = summarize(root, args)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.write_text(markdown, encoding="utf-8")
        print(f"wrote {output}")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
