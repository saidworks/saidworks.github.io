# Article Reference Guide

## Blog Structure

```
github-blog/
├── articles/
│   ├── devops-template.md          # DevOps articles
│   ├── software-design-template.md # Software design/patterns
│   ├── ai-inference-template.md    # AI/Local inference
│   ├── raspberry-pi-template.md    # Raspberry Pi/IoT
│   └── best-practices-template.md  # Best practices
├── blog-index.md                   # Main index page
├── template-article.md             # Generic article template
├── SETUP_GUIDE.md                  # Setup instructions
├── README.md                       # Repository readme
└── ARTICLE_REFERENCE.md            # This file
```

## Category Templates

### DevOps (`articles/devops-template.md`)
Use for: CI/CD, Docker, Kubernetes, infrastructure, automation

### Software Design (`articles/software-design-template.md`)
Use for: Design patterns, architecture, system design

### AI / Local Inference (`articles/ai-inference-template.md`)
Use for: LLMs, local models, AI tools, inference optimization

### Raspberry Pi / IoT (`articles/raspberry-pi-template.md`)
Use for: Hardware projects, sensors, edge computing

### Best Practices (`articles/best-practices-template.md`)
Use for: Methodologies, coding standards, workflow improvements

## Writing an Article

1. Copy appropriate template to `articles/your-topic.md`
2. Update front matter:
   - `title`: Article title
   - `date`: Publication date
   - `tags`: Relevant tags
   - `categories`: Category name
3. Fill in content sections
4. Add code examples with syntax highlighting
5. Add references/links
6. Update `blog-index.md` with new post link

## Front Matter Format

```yaml
---
title: "Your Article Title"
date: 2026-04-05
tags:
  - tag1
  - tag2
categories:
  - Category Name
---
```

## Code Block Syntax

```markdown
```python
# Python code
```

```bash
# Bash commands
```

```yaml
# YAML config
```

```javascript
# JavaScript
```

```typescript
# TypeScript
```

## Example Article

See `articles/devops-template.md` for a complete example.
