const fs = require('fs');
const path = require('path');
const lunr = require('lunr');

const searchJsonPath = path.join(__dirname, '..', '_site', 'search.json');
const outputPath = path.join(__dirname, '..', '_site', 'assets', 'js', 'lunr-index.json');

const articles = JSON.parse(fs.readFileSync(searchJsonPath, 'utf8'));

const idx = lunr(function () {
  this.ref('url');
  this.field('title', { boost: 10 });
  this.field('tags', { boost: 5 });
  this.field('content');

  articles.forEach(function (article) {
    this.add({
      url: article.url,
      title: article.title,
      tags: (article.tags || []).join(' '),
      content: article.content
    });
  }.bind(this));
});

const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(outputPath, JSON.stringify(idx));
console.log('Lunr index built: ' + articles.length + ' articles indexed');
