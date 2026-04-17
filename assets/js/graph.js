(function () {
  var container = document.getElementById('graph');
  var tooltip = document.getElementById('graph-tooltip');
  var legendEl = document.getElementById('graph-legend');

  var categoryColors = {
    'DevOps': '#f0883e',
    'Architecture': '#58a6ff',
    'AI / Local Inference': '#d2a8ff',
    'Python': '#7ee787',
    'JavaScript/TypeScript': '#ffa657',
    'Raspberry Pi / IoT': '#ff7b72',
    'Best Practices': '#a5d6ff',
    'Uncategorized': '#7d8590'
  };

  function getColor(category) {
    return categoryColors[category] || categoryColors['Uncategorized'];
  }

  fetch('/assets/data/graph.json')
    .catch(function () {
      // Try alternate path (Jekyll copies _data to site root differently)
      return fetch('/graph.json');
    })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
    .catch(function () {
      // Read from inline data if available, or show empty state
      container.innerHTML = '<p style="text-align:center;padding:3rem;color:var(--text-muted);">No graph data yet. Add articles with [[wiki-links]] to build the knowledge graph.</p>';
      return null;
    })
    .then(function (graph) {
      if (!graph || !graph.nodes.length) {
        if (graph && !graph.nodes.length) {
          container.innerHTML = '<p style="text-align:center;padding:3rem;color:var(--text-muted);">No articles yet. Add markdown files to <code>_articles/</code> to get started.</p>';
        }
        return;
      }

      var width = container.clientWidth;
      var height = container.clientHeight;

      // Build legend
      var cats = {};
      graph.nodes.forEach(function (n) { cats[n.category] = true; });
      legendEl.innerHTML = Object.keys(cats).map(function (c) {
        return '<div class="graph-legend-item"><span class="graph-legend-dot" style="background:' + getColor(c) + '"></span>' + c + '</div>';
      }).join('');

      var svg = d3.select('#graph').append('svg')
        .attr('width', width)
        .attr('height', height);

      var g = svg.append('g');

      // Zoom
      svg.call(d3.zoom()
        .scaleExtent([0.2, 5])
        .on('zoom', function (event) {
          g.attr('transform', event.transform);
        }));

      var simulation = d3.forceSimulation(graph.nodes)
        .force('link', d3.forceLink(graph.links).id(function (d) { return d.id; }).distance(100))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide(20));

      var link = g.append('g')
        .selectAll('line')
        .data(graph.links)
        .enter().append('line')
        .attr('stroke', '#30363d')
        .attr('stroke-width', 1)
        .attr('stroke-opacity', 0.6);

      var node = g.append('g')
        .selectAll('circle')
        .data(graph.nodes)
        .enter().append('circle')
        .attr('r', function (d) { return Math.max(6, Math.min(16, 6 + d.connections * 2)); })
        .attr('fill', function (d) { return getColor(d.category); })
        .attr('stroke', '#0d1117')
        .attr('stroke-width', 1.5)
        .style('cursor', 'pointer')
        .call(d3.drag()
          .on('start', function (event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
          })
          .on('drag', function (event, d) {
            d.fx = event.x; d.fy = event.y;
          })
          .on('end', function (event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
          }));

      var label = g.append('g')
        .selectAll('text')
        .data(graph.nodes)
        .enter().append('text')
        .text(function (d) { return d.title; })
        .attr('font-size', '10px')
        .attr('font-family', 'JetBrains Mono, monospace')
        .attr('fill', '#7d8590')
        .attr('dx', 12)
        .attr('dy', 4)
        .style('pointer-events', 'none');

      node.on('mouseover', function (event, d) {
        tooltip.style.opacity = 1;
        tooltip.textContent = d.title + ' (' + d.category + ')';
        tooltip.style.left = event.pageX + 10 + 'px';
        tooltip.style.top = event.pageY - 10 + 'px';

        // Highlight connected
        var connected = new Set();
        graph.links.forEach(function (l) {
          if (l.source.id === d.id) connected.add(l.target.id);
          if (l.target.id === d.id) connected.add(l.source.id);
        });
        connected.add(d.id);

        node.attr('opacity', function (n) { return connected.has(n.id) ? 1 : 0.15; });
        link.attr('stroke-opacity', function (l) {
          return l.source.id === d.id || l.target.id === d.id ? 0.8 : 0.05;
        });
        label.attr('opacity', function (n) { return connected.has(n.id) ? 1 : 0.1; });
      });

      node.on('mouseout', function () {
        tooltip.style.opacity = 0;
        node.attr('opacity', 1);
        link.attr('stroke-opacity', 0.6);
        label.attr('opacity', 1);
      });

      node.on('click', function (event, d) {
        window.location.href = d.url;
      });

      simulation.on('tick', function () {
        link
          .attr('x1', function (d) { return d.source.x; })
          .attr('y1', function (d) { return d.source.y; })
          .attr('x2', function (d) { return d.target.x; })
          .attr('y2', function (d) { return d.target.y; });
        node
          .attr('cx', function (d) { return d.x; })
          .attr('cy', function (d) { return d.y; });
        label
          .attr('x', function (d) { return d.x; })
          .attr('y', function (d) { return d.y; });
      });

      // Resize handler
      window.addEventListener('resize', function () {
        width = container.clientWidth;
        height = container.clientHeight;
        svg.attr('width', width).attr('height', height);
        simulation.force('center', d3.forceCenter(width / 2, height / 2));
        simulation.alpha(0.3).restart();
      });
    });
})();
