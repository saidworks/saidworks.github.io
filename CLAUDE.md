# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static markdown-based blog template for GitHub Pages. No build step or dependencies — plain `.md` files hosted directly on GitHub.

## Architecture

**Simple flat structure:**
- `blog-index.md` — Homepage with post links and category navigation
- `template-article.md` — Front-matter template for new articles
- `articles/` — Directory for article drafts before publishing

**Front-matter format (YAML):**
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

## Key Files

| File | Purpose |
|------|----------|
| `blog-index.md` | Main entry point; update when adding new articles |
| `template-article.md` | Copy this for new articles |
| `articles/*.md` | Draft articles (move/link to root for publishing) |

## Common Tasks

### Create a new article

```bash
cp template-article.md articles/my-article.md
# Edit content, then update blog-index.md with link
```

### Publish an article

1. Add article file to root or `articles/` folder
2. Update `blog-index.md` with link: `- [Title](articles/my-article.md)`
3. Commit: `git commit -m "feat: add article on [topic]"`

### Styling

Add `styles.css` in root for custom CSS. GitHub Pages serves static files as-is.

## Notes

- No linter, formatter, or test runner — plain markdown
- Deployment: GitHub Pages from `main` branch, `/ (root)` folder
- Use conventional commits: `feat:` for new articles, `docs:` for updates
