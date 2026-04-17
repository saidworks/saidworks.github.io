# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Jekyll-powered blog for GitHub Pages with client-side search (Lunr.js), tag navigation, and Obsidian knowledge graph integration (wiki-links, backlinks, D3 graph visualization). The repo doubles as an Obsidian vault.

## Architecture

```
Push to main -> GitHub Actions:
  1. obsidian_bridge.py (convert [[wiki-links]], generate backlinks + graph data)
  2. Jekyll builds HTML from markdown + layouts + data files
  3. build-search-index.js (Lunr.js pre-built index)
  4. Deploy to GitHub Pages
```

### Key Directories

- `_articles/` — Blog articles (also the Obsidian vault notes folder). Jekyll collection.
- `_layouts/` — HTML templates: `default.html` (base), `home.html`, `article.html`
- `_includes/` — Reusable partials: `head.html`, `nav.html`, `footer.html`, `tag-chips.html`, `backlinks.html`
- `_data/` — Generated JSON: `backlinks.json`, `graph.json` (produced by `obsidian_bridge.py`; seed files checked in, overwritten at build time)
- `_scripts/` — Build scripts (excluded from Jekyll output)
- `_templates/` — Article templates (excluded from Jekyll output)
- `assets/` — CSS (`main.css`, `syntax.css`) and JS (`search.js`, `tag-filter.js`, `graph.js`)

### Build Pipeline (`.github/workflows/deploy.yml`)

1. `python _scripts/obsidian_bridge.py` — wiki-link conversion + data generation
2. `actions/jekyll-build-pages` — Jekyll build
3. `node _scripts/build-search-index.js` — Lunr index from `_site/search.json`

**GitHub Pages source must be set to "GitHub Actions" (not "Deploy from branch").**

### Front-matter format

```yaml
---
title: "Article Title"
date: 2026-04-05
tags:
  - tag1
categories:
  - Category Name
---
```

### Obsidian Features

- `[[note-name]]` wiki-links are converted to standard links at build time
- `[[note|alias]]` and `[[note#heading]]` syntax supported
- Backlinks rendered from `_data/backlinks.json` via `_includes/backlinks.html`
- Graph data at `_data/graph.json`, served via `assets/data/graph.json` (Liquid passthrough)

## Local Development

```bash
gem install jekyll kramdown-parser-gfm webrick   # Jekyll 4 + deps
python3 _scripts/obsidian_bridge.py               # generate _data/ files
jekyll serve
```

On Ruby 3.4+, you may also need: `gem install base64 bigdecimal csv erb ostruct logger`.

The Gemfile targets Jekyll 4 for local dev. GitHub Actions uses `actions/jekyll-build-pages` which runs its own Jekyll — the Gemfile is not used in CI.

`obsidian_bridge.py` modifies `_articles/*.md` in-place (wiki-link conversion) and writes `_data/backlinks.json` + `_data/graph.json`. In CI this runs on the checkout copy, not the repo source.

## Adding Articles

```bash
# Single file
python3 _scripts/import_article.py path/to/note.md

# Bulk import from structured directory (maps subdirs to categories/tags)
python3 _scripts/migrate_cheatsheets.py path/to/notes/

# Manual: copy to _articles/ with front-matter, then git push
```

### Liquid Escaping

Articles containing `{{ }}` syntax (Blade, Handlebars, Jinja, Go templates) must be wrapped with `{% raw %}` / `{% endraw %}` after the front-matter. Jekyll interprets `{{ }}` as Liquid and will error or produce broken output without this.

## Design

Dark theme. JetBrains Mono headings, Inter body text. Accent: `#f0883e` (warm amber). Content column: 680px max-width. All design tokens in `:root` in `assets/css/main.css`.

## Commits

Use conventional commits: `feat:` for new articles/features, `docs:` for content updates, `fix:` for corrections.
