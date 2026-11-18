#!/usr/bin/env python3
"""Check that plugins/undertow-en and plugins/undertow-ru stay in sync.

Compares the file tree, manifest versions, SKILL.md frontmatter and, per Markdown
file, the URLs, fenced code block count and heading structure. Text is not compared:
the plugins are translations of each other. Exit code 1 on any drift.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RU, EN = ROOT / "plugins/undertow-ru", ROOT / "plugins/undertow-en"
# The original scanned methodology exists only in Russian; undertow-en ships its translation.
RU_ONLY = {"skills/detection-audit/sources/original/_VPN_proxy_.pdf"}
URL = re.compile(r"https?://[^\s)<>\]`\"']+")
CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def tree(base):
    return {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file() and p.name != ".DS_Store"}


def outline(text):
    """URLs, code block count and heading levels of a Markdown file, ignoring code inside fences."""
    urls, levels, fences, in_code = set(), [], 0, False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            fences += in_code
            continue
        urls.update(u.rstrip(".,;:") for u in URL.findall(line))
        if not in_code and (m := re.match(r"(#{1,6}) ", line)):
            levels.append(len(m.group(1)))
    return urls, fences, levels


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"^(\w[\w-]*): *(.*)$", m.group(1), re.M)) if m else {}


def main():
    errors = []
    ru, en = tree(RU), tree(EN)
    for p in sorted(ru - en - RU_ONLY):
        errors.append(f"missing in undertow-en: {p}")
    for p in sorted(en - ru):
        errors.append(f"missing in undertow-ru: {p}")

    versions = {}
    for base in (RU, EN):
        for m in (".claude-plugin/plugin.json", "plugin.json"):
            data = json.loads((base / m).read_text())
            versions[f"{base.name}/{m}"] = data["version"]
            if data["name"] != base.name:
                errors.append(f"{base.name}/{m}: name is {data['name']!r}")
    if len(set(versions.values())) > 1:
        errors.append(f"version mismatch: {versions}")

    for rel in sorted((ru & en)):
        if not rel.endswith(".md"):
            continue
        r_text, e_text = (RU / rel).read_text(), (EN / rel).read_text()
        (ru_urls, ru_fences, ru_levels), (en_urls, en_fences, en_levels) = outline(r_text), outline(e_text)
        if ru_urls != en_urls:
            errors.append(f"{rel}: URLs differ, ru-only {sorted(ru_urls - en_urls)}, en-only {sorted(en_urls - ru_urls)}")
        if ru_fences != en_fences:
            errors.append(f"{rel}: code blocks ru={ru_fences} en={en_fences}")
        if ru_levels != en_levels:
            errors.append(f"{rel}: heading structure differs (ru {len(ru_levels)}, en {len(en_levels)} headings)")
        r_fm, e_fm = frontmatter(r_text), frontmatter(e_text)
        for key in ("name", "license", "tools"):
            if r_fm.get(key) != e_fm.get(key):
                errors.append(f"{rel}: frontmatter {key} ru={r_fm.get(key)!r} en={e_fm.get(key)!r}")
        if CYRILLIC.search(e_text):
            n = sum(1 for line in e_text.splitlines() if CYRILLIC.search(line))
            errors.append(f"{rel}: {n} lines with Cyrillic in undertow-en")

    for e in errors:
        print(e)
    print(f"{len(errors)} problems" if errors else "undertow-en and undertow-ru are in sync")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
