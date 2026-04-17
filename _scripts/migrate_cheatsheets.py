#!/usr/bin/env python3
"""
Migrate notes from a cheatsheets repo into the blog's _articles/ folder.

Usage:
    python _scripts/migrate_cheatsheets.py ../Notes/cheatsheets

Walks the source directory, maps subdirectories to categories and tags,
adds YAML front-matter, copies referenced images, and generates a report.
"""

import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ARTICLES_DIR = Path("_articles")
IMAGES_DIR = Path("assets/images")

# Directory path (relative to source root) -> (category, [tags])
# Matches the deepest matching prefix
DIR_MAP = {
    "AI/agentic": ("AI", ["ai", "agentic"]),
    "AI/ai_assistants": ("AI", ["ai", "assistants", "tools"]),
    "AI/inference": ("AI", ["ai", "inference", "llm"]),
    "AI": ("AI", ["ai"]),
    "algorithms": ("CS Fundamentals", ["algorithms"]),
    "API/openapi_specs": ("DevOps", ["api", "openapi"]),
    "API": ("DevOps", ["api"]),
    "build_tools": ("DevOps", ["build-tools"]),
    "c_language": ("Programming", ["c", "language"]),
    "crm/salesforce": ("Tools", ["crm", "salesforce"]),
    "crm": ("Tools", ["crm"]),
    "cs_fundamentals/OOP": ("CS Fundamentals", ["cs", "oop"]),
    "cs_fundamentals": ("CS Fundamentals", ["cs"]),
    "databases/postgres": ("Databases", ["postgres", "sql", "database"]),
    "databases/sql": ("Databases", ["sql", "database"]),
    "databases": ("Databases", ["database"]),
    "data_engineering/bigdata": ("Data Engineering", ["data", "bigdata"]),
    "data_engineering": ("Data Engineering", ["data"]),
    "devOps/cloud_computing/AWS": ("DevOps", ["cloud", "aws", "devops"]),
    "devOps/cloud_computing": ("DevOps", ["cloud", "devops"]),
    "devOps/devenv": ("DevOps", ["devops", "devenv"]),
    "devOps/jenkins": ("DevOps", ["devops", "jenkins", "ci-cd"]),
    "devOps": ("DevOps", ["devops"]),
    "frameworks/Angular": ("Frontend", ["angular", "framework"]),
    "frameworks/DotNet": ("Backend", ["dotnet", "csharp"]),
    "frameworks/Laravel": ("Backend", ["laravel", "php"]),
    "frameworks/Spring": ("Backend", ["spring", "java"]),
    "frameworks/Vue.js": ("Frontend", ["vuejs", "framework"]),
    "frameworks": ("Backend", ["framework"]),
    "frontend_fundamentals/css": ("Frontend", ["css", "frontend"]),
    "frontend_fundamentals/design_tools": ("Frontend", ["design", "tools"]),
    "frontend_fundamentals/HTML": ("Frontend", ["html", "frontend"]),
    "frontend_fundamentals/javascript": ("Frontend", ["javascript", "frontend"]),
    "frontend_fundamentals": ("Frontend", ["frontend"]),
    "git": ("Tools", ["git", "version-control"]),
    "ide/Pycharm": ("Tools", ["ide", "pycharm"]),
    "ide/vs_code": ("Tools", ["ide", "vscode"]),
    "ide": ("Tools", ["ide"]),
    "iot/raspberry_pi": ("IoT", ["raspberry-pi", "iot"]),
    "iot": ("IoT", ["iot"]),
    "java": ("Programming", ["java"]),
    "linux/wsl": ("DevOps", ["linux", "wsl"]),
    "linux": ("DevOps", ["linux", "cli"]),
    "markdown": ("Tools", ["markdown"]),
    "php/htaccess": ("Programming", ["php", "htaccess"]),
    "php": ("Programming", ["php"]),
    "Python": ("Programming", ["python"]),
    "scripting": ("Programming", ["scripting", "shell"]),
    "system_design": ("Architecture", ["system-design", "architecture"]),
    "udacity_mac": ("Tools", ["udacity", "mac"]),
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
IMAGE_REF_RE = re.compile(r'!\[.*?\]\(([^)]+)\)|<img[^>]+src=["\']([^"\']+)["\']')


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def extract_title(text, filename):
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    # Fallback: humanize filename
    name = filename.replace('_', ' ').replace('-', ' ')
    return name.title()


def get_file_date(filepath):
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')


def resolve_category_tags(rel_dir):
    """Find the best matching directory mapping."""
    rel_dir = str(rel_dir).replace('\\', '/')
    # Try longest prefix first
    parts = rel_dir.split('/')
    for i in range(len(parts), 0, -1):
        key = '/'.join(parts[:i])
        if key in DIR_MAP:
            return DIR_MAP[key]
    return ("Uncategorized", [])


def has_frontmatter(text):
    return text.strip().startswith('---')


def build_frontmatter(title, date, tags, category):
    tag_lines = '\n'.join(f'  - {t}' for t in tags) if tags else '  - uncategorized'
    return f"""---
title: "{title}"
date: {date}
tags:
{tag_lines}
categories:
  - {category}
---

"""


def find_image_refs(text):
    """Find image paths referenced in markdown."""
    refs = []
    for m in IMAGE_REF_RE.finditer(text):
        path = m.group(1) or m.group(2)
        if path and not path.startswith(('http://', 'https://', 'data:')):
            refs.append(path)
    return refs


def copy_referenced_images(source_file, text, source_root):
    """Copy images referenced in the file to assets/images/. Returns updated text."""
    refs = find_image_refs(text)
    if not refs:
        return text

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for ref in refs:
        # Resolve relative to the source file's directory
        img_path = (source_file.parent / ref).resolve()
        if not img_path.exists():
            # Try relative to source root
            img_path = (source_root / ref).resolve()
        if img_path.exists() and img_path.suffix.lower() in IMAGE_EXTENSIONS:
            dest = IMAGES_DIR / img_path.name
            if not dest.exists():
                shutil.copy2(img_path, dest)
            # Update reference in text
            new_ref = f'/assets/images/{img_path.name}'
            text = text.replace(ref, new_ref)

    return text


def migrate_file(source_file, source_root):
    """Migrate a single file. Returns (success, slug, message)."""
    text = source_file.read_text(encoding='utf-8', errors='replace')

    # Get relative directory from source root
    rel_dir = source_file.parent.relative_to(source_root)
    category, tags = resolve_category_tags(rel_dir)

    # Extract metadata
    title = extract_title(text, source_file.stem)
    date = get_file_date(source_file)
    slug = slugify(source_file.stem)

    dest = ARTICLES_DIR / f"{slug}.md"
    if dest.exists():
        return False, slug, f"SKIP (exists): {slug}"

    # Handle images
    text = copy_referenced_images(source_file, text, source_root)

    # Add front-matter if missing
    if not has_frontmatter(text):
        text = build_frontmatter(title, date, tags, category) + text

    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')
    return True, slug, f"OK: {source_file.relative_to(source_root)} -> {slug} [{category}]"


def main():
    if len(sys.argv) < 2:
        print("Usage: python _scripts/migrate_cheatsheets.py <source_directory>")
        sys.exit(1)

    source_root = Path(sys.argv[1]).resolve()
    if not source_root.is_dir():
        print(f"Error: {source_root} is not a directory")
        sys.exit(1)

    print(f"Migrating from: {source_root}")
    print(f"Destination: {ARTICLES_DIR.resolve()}")
    print()

    files = sorted(
        f for f in source_root.rglob('*')
        if f.suffix.lower() in ('.md', '.txt')
        and '.git' not in f.parts
        and '.idea' not in f.parts
    )

    print(f"Found {len(files)} markdown/text files\n")

    imported = 0
    skipped = 0
    errors = 0

    for f in files:
        try:
            success, slug, msg = migrate_file(f, source_root)
            print(f"  {msg}")
            if success:
                imported += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {f.relative_to(source_root)} — {e}")
            errors += 1

    print(f"\n--- Migration Report ---")
    print(f"Imported: {imported}")
    print(f"Skipped:  {skipped}")
    print(f"Errors:   {errors}")
    print(f"Total:    {imported + skipped + errors}")


if __name__ == '__main__':
    main()
