#!/usr/bin/env python3
"""
Import a markdown or text file as a blog article.

Usage:
    python _scripts/import_article.py path/to/note.md
    python _scripts/import_article.py path/to/note.txt
    python _scripts/import_article.py path/to/notes/  (bulk import)

Adds YAML front-matter if missing, converts .txt to .md,
copies to _articles/ with a slugified filename.
"""

import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ARTICLES_DIR = Path("_articles")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def has_frontmatter(text):
    return text.strip().startswith('---')


def extract_title(text, filename):
    """Try to extract a title from the content."""
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            return line[:80]
    return filename


def build_frontmatter(title, tags=None, categories=None):
    tags = tags or []
    categories = categories or ['Uncategorized']
    tag_lines = '\n'.join(f'  - {t}' for t in tags)
    cat_lines = '\n'.join(f'  - {c}' for c in categories)
    return f"""---
title: "{title}"
date: {date.today().isoformat()}
tags:
{tag_lines}
categories:
{cat_lines}
---

"""


def import_file(filepath):
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"Error: {filepath} not found")
        return False

    text = filepath.read_text(encoding='utf-8')
    stem = filepath.stem
    slug = slugify(stem)
    dest = ARTICLES_DIR / f"{slug}.md"

    if dest.exists():
        print(f"Skip: {dest} already exists")
        return False

    if not has_frontmatter(text):
        title = extract_title(text, stem)
        text = build_frontmatter(title) + text
        print(f"  Added front-matter (title: {title})")

    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')
    print(f"  Imported: {filepath} -> {dest}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python _scripts/import_article.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    count = 0

    if target.is_dir():
        files = list(target.glob('*.md')) + list(target.glob('*.txt'))
        print(f"Found {len(files)} files in {target}")
        for f in sorted(files):
            if import_file(f):
                count += 1
    elif target.is_file():
        if import_file(target):
            count += 1
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)

    print(f"\nImported {count} article(s)")


if __name__ == '__main__':
    main()
