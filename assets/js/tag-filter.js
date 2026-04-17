(function () {
  var sections = document.querySelectorAll('.tag-section');
  var chips = document.querySelectorAll('.tags-nav .tag-chip');

  function filterByHash() {
    var hash = window.location.hash.replace('#', '');
    if (!hash) {
      sections.forEach(function (s) { s.style.display = ''; });
      chips.forEach(function (c) { c.classList.remove('tag-chip--active'); });
      return;
    }
    sections.forEach(function (s) {
      s.style.display = s.dataset.tag === hash ? '' : 'none';
    });
    chips.forEach(function (c) {
      c.classList.toggle('tag-chip--active', c.dataset.tag === hash);
    });
  }

  window.addEventListener('hashchange', filterByHash);
  filterByHash();

  chips.forEach(function (chip) {
    chip.addEventListener('click', function (e) {
      if (window.location.hash === '#' + this.dataset.tag) {
        e.preventDefault();
        history.pushState(null, '', window.location.pathname);
        filterByHash();
      }
    });
  });
})();
