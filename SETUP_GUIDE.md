# GitHub Blog Setup Guide

## Prerequisites

- GitHub account
- Git installed on your machine

## Step-by-Step Setup

### Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `yourusername.github.io` (replace with your actual username)
3. Make it **Public**
4. Click **Create repository**

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
```

### Step 3: Add Blog Files

Copy all files from this folder:

```bash
cp /home/saidworks/Desktop/workspace/github-blog/* .
```

### Step 4: Create Articles Folder

```bash
mkdir -p articles
```

### Step 5: Create First Article

```bash
cp template-article.md articles/my-first-post.md
# Edit the article with your content
```

### Step 6: Initial Commit

```bash
git add .
git commit -m "docs: add blog skeleton"
git push -u origin main
```

### Step 7: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** > **Pages**
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

### Step 8: Wait for Deployment

GitHub Pages takes 1-2 minutes to deploy. Your blog will be at:
`https://yourusername.github.io`

## Creating New Articles

1. Create a new markdown file in `articles/`:
   ```bash
   cp template-article.md articles/your-topic-here.md
   ```

2. Edit the file with your content

3. Update `blog-index.md` to link to your new article

4. Commit and push:
   ```bash
   git add .
   git commit -m "feat: add article on [topic]"
   git push
   ```

## Article Front Matter

Each article should have YAML front matter:

```yaml
---
title: "My Article Title"
date: 2026-04-05
tags:
  - python
  - tutorial
categories:
  - Python
---
```

## Styling (Optional)

Add a `styles.css` in the root for custom styling:

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
```

## Navigation

Add links to your blog index by referencing them in `blog-index.md`:

```markdown
## Recent Posts

- [Article Title](articles/article-name.md)
```

## Troubleshooting

### Pages not loading?

- Wait 2-3 minutes after pushing
- Check Settings > Pages for deployment status
- Ensure files are at root of `main` branch

### Images not showing?

- Create `images/` folder
- Reference as: `![alt](images/image.png)`

### Custom domain?

- Settings > Pages > Custom domain
- Add CNAME record to your domain
