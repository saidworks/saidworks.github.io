# Article Reference Guide

## Article Location

All articles live in `_articles/`. Each `.md` file with YAML front-matter becomes a page at `/articles/<slug>/`.

## Front-Matter Format

Every article requires this at the top:

```yaml
---
title: "Article Title"
date: 2026-04-14
tags:
  - tag1
  - tag2
categories:
  - Category Name
---
```

**Required fields:** `title`, `date`, `tags`, `categories`

## Current Categories

| Category | Count | Topics |
|----------|-------|--------|
| DevOps | 9 | Docker, AWS, Jenkins, Linux, CI/CD |
| AI | 7 | LLM inference, AI assistants, Copilot |
| Frontend | 5 | Angular, Vue.js, CSS, HTML, JavaScript |
| Backend | 5 | Spring, Laravel, .NET, Hibernate |
| Programming | 4 | Python, Java, PHP, C, scripting |
| IoT | 3 | Raspberry Pi, Home Assistant |
| Tools | 1 | Git, IDEs, markdown |
| Databases | 1 | PostgreSQL, SQL |
| Architecture | 1 | System design |
| Best Practices | 1 | Methodologies, workflows |

## Category Templates

Templates are in `_templates/` (excluded from the site build):

| Template | Use for |
|----------|---------|
| `template-article.md` | Generic article with intro/sections/conclusion |
| `devops-template.md` | CI/CD, Docker, infrastructure (Prerequisites + Steps) |
| `software-design-template.md` | Design patterns, architecture (Problem + Solution + Trade-offs) |
| `ai-inference-template.md` | LLMs, local models (Model Selection table + Setup/Inference) |
| `raspberry-pi-template.md` | Hardware, IoT (Hardware Requirements + Wiring + Code) |
| `best-practices-template.md` | Methodologies (Problem + Guidelines + Bad/Good examples) |

To use a template:

```bash
cp _templates/devops-template.md _articles/my-docker-guide.md
# Edit front-matter and content
```

## Cross-Referencing

Link to other articles using Obsidian-style wiki-links:

```markdown
See [[other-article]] for details.
See [[other-article|custom display text]] for details.
See [[other-article#section-heading]] for a specific section.
```

These are converted to standard HTML links at build time by `_scripts/obsidian_bridge.py`. The target must match the filename (slug) of an article in `_articles/`.

## Code Blocks

Use fenced code blocks with language identifiers for syntax highlighting:

````markdown
```python
def hello():
    print("Hello")
```

```bash
docker run -it ubuntu
```

```yaml
services:
  web:
    image: nginx
```
````

## Liquid Escaping

Articles containing template syntax like `{{ variable }}` (Blade, Handlebars, Jinja, Go templates) must be wrapped:

```markdown
---
title: "Laravel Blade Cheatsheet"
...
---

{% raw %}
{{ $var }} - Echo content
@foreach($items as $item) ...
{% endraw %}
```

Without this, Jekyll interprets `{{ }}` as Liquid template syntax and the build will produce warnings or broken output.
