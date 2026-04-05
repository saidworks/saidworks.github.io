# GitHub Tech Blog

A simple markdown-based blog for technical articles, hosted on GitHub.

## Setup

### 1. Create Repository

```bash
# Create a new repository on GitHub (user name must match your GitHub username)
# Repository name should be: yourusername.github.io
```

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
```

### 3. Add Blog Content

Copy articles from this folder to the root of your GitHub repository:

```bash
# Copy the template and create new articles
cp template-article.md my-first-post.md
```

### 4. Push to GitHub

```bash
git add .
git commit -m "docs: add blog skeleton"
git push -u origin main
```

### 5. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** > **Pages**
3. Select **Deploy from a branch**
4. Choose branch: `main`
5. Folder: `/ (root)`
6. Click **Save**

Your blog will be live at: `https://yourusername.github.io`

## Structure

```
yourusername.github.io/
├── blog-index.md    # Main index page
├── template-article.md  # Article template
├── SETUP_GUIDE.md   # This guide
└── README.md        # Repository readme
```

## Creating a New Article

1. Copy `template-article.md` to `articles/your-article-name.md`
2. Fill in the content
3. Update `blog-index.md` with the new post link
4. Push to GitHub

## Tips

- Use `template-article.md` for consistent formatting
- Keep articles focused and well-structured
- Add code examples with proper syntax highlighting
- Include references/links to resources
- Update the index page with new posts
