(function () {
  var input = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  var countEl = document.getElementById('search-count');
  var index = null;
  var articles = null;
  var articleMap = {};
  var debounceTimer = null;

  function loadIndex() {
    return fetch('/assets/js/lunr-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        index = lunr.Index.load(data);
      })
      .catch(function () {
        // Fallback: build index at runtime if pre-built not available
        return loadArticles().then(function () {
          index = lunr(function () {
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
        });
      });
  }

  function loadArticles() {
    if (articles) return Promise.resolve();
    return fetch('/search.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        articles = data;
        data.forEach(function (a) { articleMap[a.url] = a; });
      });
  }

  function search(query) {
    if (!index || !query.trim()) {
      resultsEl.innerHTML = '';
      countEl.textContent = '';
      return;
    }
    var results;
    try {
      results = index.search(query + '~1');
    } catch (e) {
      results = index.search(query);
    }
    countEl.textContent = results.length + ' result' + (results.length !== 1 ? 's' : '');
    resultsEl.innerHTML = results.slice(0, 30).map(function (r) {
      var article = articleMap[r.ref];
      if (!article) return '';
      var tags = (article.tags || []).map(function (t) {
        return '<span class="tag-chip">' + t + '</span>';
      }).join('');
      return '<div class="search-result">' +
        '<div class="search-result-title"><a href="' + article.url + '">' + article.title + '</a></div>' +
        '<div class="search-result-meta">' + article.date + '</div>' +
        (tags ? '<div class="tag-chips" style="margin-top: 0.5rem;">' + tags + '</div>' : '') +
        '</div>';
    }).join('');
  }

  Promise.all([loadIndex(), loadArticles()]).then(function () {
    input.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        search(input.value);
      }, 200);
    });
    // Handle URL param
    var params = new URLSearchParams(window.location.search);
    if (params.get('q')) {
      input.value = params.get('q');
      search(params.get('q'));
    }
  });
})();
