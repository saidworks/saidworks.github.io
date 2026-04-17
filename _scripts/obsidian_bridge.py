#!/usr/bin/env python3
"""
Obsidian Bridge — Pre-processing script for GitHub Actions.

Runs BEFORE Jekyll build. Does three things:
1. Converts [[wiki-links]] to standard markdown links
2. Generates _data/backlinks.json (reverse link index)
3. Generates _data/graph.json (nodes + edges for D3 visualization)

Only modifies files in the working copy (CI checkout), never the repo source.
"""

import json
import os
import re
import sys
from pathlib import Path

ARTICLES_DIR = Path("_articles")
DATA_DIR = Path("_data")

# Match [[target]], [[target|alias]], [[target#heading]], [[target#heading|alias]]
# Negative lookbehind for backtick to skip inline code
WIKILINK_RE = re.compile(r'(?<!`)(?<!`)`*\[\[([^\]]+)\]\]')

# Detect fenced code blocks
FENCE_RE = re.compile(r'^(`{3,}|~{3,})')


def parse_frontmatter(text):
    """Extract YAML front-matter fields we need."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('---', 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 3:].lstrip('\n')

    meta = {}
    for line in fm_text.split('\n'):
        if ':' in line and not line.startswith(' ') and not line.startswith('-'):
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                meta[key] = val
    # Parse tags and categories as lists
    in_list = None
    items = {'tags': [], 'categories': []}
    for line in fm_text.split('\n'):
        stripped = line.strip()
        if stripped in ('tags:', 'categories:'):
            in_list = stripped.rstrip(':')
        elif in_list and stripped.startswith('- '):
            items[in_list].append(stripped[2:].strip())
        elif not stripped.startswith('-') and ':' in stripped:
            in_list = None
    meta['tags'] = items['tags']
    meta['categories'] = items['categories']

    return meta, body


def find_articles():
    """Find all markdown files in _articles/."""
    if not ARTICLES_DIR.exists():
        return {}
    articles = {}
    for p in ARTICLES_DIR.glob("*.md"):
        slug = p.stem
        text = p.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(text)
        articles[slug] = {
            'path': p,
            'slug': slug,
            'title': meta.get('title', slug.replace('-', ' ').title()),
            'tags': meta.get('tags', []),
            'categories': meta.get('categories', []),
            'url': f'/articles/{slug}/',
            'full_text': text,
            'body': body,
        }
    return articles


def convert_wikilinks(articles):
    """Convert [[wiki-links]] to standard markdown links. Returns link map."""
    all_links = {}  # source_slug -> [target_slug, ...]

    slug_lookup = {s.lower(): s for s in articles}

    for slug, article in articles.items():
        text = article['full_text']
        links_from = []
        lines = text.split('\n')
        in_fence = False
        new_lines = []

        for line in lines:
            fence_match = FENCE_RE.match(line)
            if fence_match:
                in_fence = not in_fence
                new_lines.append(line)
                continue

            if in_fence:
                new_lines.append(line)
                continue

            # Also skip lines that are entirely inside inline code
            def replace_wikilink(m):
                inner = m.group(1)
                # Parse target and alias
                if '|' in inner:
                    target_part, alias = inner.split('|', 1)
                else:
                    target_part = inner
                    alias = None

                # Parse heading
                if '#' in target_part:
                    target_name, heading = target_part.split('#', 1)
                else:
                    target_name = target_part
                    heading = None

                target_slug = target_name.strip().lower().replace(' ', '-')

                # Find matching article
                if target_slug in slug_lookup:
                    actual_slug = slug_lookup[target_slug]
                    display = alias or target_name.strip()
                    url = f'/articles/{actual_slug}/'
                    if heading:
                        url += '#' + heading.strip().lower().replace(' ', '-')
                    links_from.append(actual_slug)
                    return f'[{display}]({url})'

                # No match — leave as-is but format as plain text
                display = alias or target_name.strip()
                return display

            new_line = WIKILINK_RE.sub(replace_wikilink, line)
            new_lines.append(new_line)

        new_text = '\n'.join(new_lines)
        if new_text != text:
            article['path'].write_text(new_text, encoding='utf-8')

        all_links[slug] = list(set(links_from))

    return all_links


def generate_backlinks(articles, links):
    """Generate _data/backlinks.json from the link map."""
    backlinks = {}
    for source_slug, targets in links.items():
        source = articles[source_slug]
        for target_slug in targets:
            if target_slug not in backlinks:
                backlinks[target_slug] = []
            backlinks[target_slug].append({
                'title': source['title'],
                'url': source['url'],
            })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / 'backlinks.json'
    out.write_text(json.dumps(backlinks, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Backlinks: {sum(len(v) for v in backlinks.values())} links across {len(backlinks)} targets")


def generate_graph(articles, links):
    """Generate _data/graph.json for D3 visualization."""
    nodes = []
    edges = []
    seen_edges = set()

    for slug, article in articles.items():
        cat = article['categories'][0] if article['categories'] else 'Uncategorized'
        nodes.append({
            'id': slug,
            'title': article['title'],
            'category': cat,
            'url': article['url'],
            'connections': len(links.get(slug, [])),
        })

    for source_slug, targets in links.items():
        for target_slug in targets:
            edge_key = tuple(sorted([source_slug, target_slug]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({
                    'source': source_slug,
                    'target': target_slug,
                })

    graph = {'nodes': nodes, 'links': edges}
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / 'graph.json'
    out.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Graph: {len(nodes)} nodes, {len(edges)} edges")


def main():
    articles = find_articles()
    if not articles:
        print("No articles found in _articles/")
        # Write empty data files so Jekyll doesn't fail
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        (DATA_DIR / 'backlinks.json').write_text('{}', encoding='utf-8')
        (DATA_DIR / 'graph.json').write_text('{"nodes":[],"links":[]}', encoding='utf-8')
        return

    print(f"Processing {len(articles)} articles...")
    links = convert_wikilinks(articles)
    generate_backlinks(articles, links)
    generate_graph(articles, links)
    print("Obsidian bridge complete.")


if __name__ == '__main__':
    main()
