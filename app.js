'use strict';
(() => {
  const grid = document.querySelector('#project-grid');
  if (grid) {
    const cards = [...grid.querySelectorAll('.project-card')];
    const tabs = [...document.querySelectorAll('[data-discipline]')];
    const search = document.querySelector('#project-search');
    const tool = document.querySelector('#tool-filter');
    const skill = document.querySelector('#skill-filter');
    const clear = document.querySelector('#clear-filters');
    const count = document.querySelector('#result-count');
    const empty = document.querySelector('#empty-state');
    const form = document.querySelector('#project-filters');
    const dialog = document.querySelector('#project-dialog');
    const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    let discipline = 'all';
    let returnFocus = null;
    let projectsPromise = null;
    const projectData = () => projectsPromise || (projectsPromise = fetch('/projects.json').then(response => {
      if (!response.ok) throw new Error('Project data unavailable');
      return response.json();
    }).catch(error => { projectsPromise = null; throw error; }));

    function syncURL() {
      const params = new URLSearchParams();
      if (discipline !== 'all') params.set('discipline', discipline);
      if (search.value.trim()) params.set('q', search.value.trim());
      if (tool.value) params.set('tool', tool.value);
      if (skill.value) params.set('skill', skill.value);
      const query = params.toString();
      history.replaceState(null, '', location.pathname + (query ? '?' + query : '') + location.hash);
    }

    function filter(updateURL = true) {
      const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let visible = 0;
      for (const card of cards) {
        const match = (discipline === 'all' || card.dataset.category.split(' ').includes(discipline)) &&
          (!tool.value || JSON.parse(card.dataset.tools).includes(tool.value)) &&
          (!skill.value || JSON.parse(card.dataset.skills).includes(skill.value)) &&
          terms.every(term => normalize(card.dataset.search).includes(term));
        card.hidden = !match;
        if (match) visible++;
      }
      tabs.forEach(tab => {
        const active = tab.dataset.discipline === discipline;
        tab.classList.toggle('active', active);
        tab.setAttribute('aria-pressed', String(active));
      });
      const filtered = discipline !== 'all' || !!search.value || !!tool.value || !!skill.value;
      count.textContent = filtered ? `Showing ${visible} of ${cards.length} case studies` : `Showing all ${cards.length} case studies`;
      clear.hidden = !filtered;
      empty.hidden = visible !== 0;
      grid.hidden = visible === 0;
      if (updateURL) syncURL();
    }

    function readURL() {
      const params = new URLSearchParams(location.search);
      discipline = ['BA', 'PM', 'DA'].includes(params.get('discipline')) ? params.get('discipline') : 'all';
      search.value = params.get('q') || '';
      tool.value = [...tool.options].some(o => o.value === params.get('tool')) ? params.get('tool') : '';
      skill.value = [...skill.options].some(o => o.value === params.get('skill')) ? params.get('skill') : '';
      filter(false);
    }

    function reset() {
      discipline = 'all'; search.value = ''; tool.value = ''; skill.value = '';
      filter(); search.focus();
    }
    tabs.forEach(tab => tab.addEventListener('click', () => { discipline = tab.dataset.discipline; filter(); }));
    search.addEventListener('input', () => filter());
    tool.addEventListener('change', () => filter());
    skill.addEventListener('change', () => filter());
    clear.addEventListener('click', reset);
    document.querySelector('#empty-reset').addEventListener('click', reset);
    form.addEventListener('submit', event => { event.preventDefault(); filter(); });
    window.addEventListener('popstate', readURL);
    readURL();

    function fillTags(target, values, className) {
      target.replaceChildren(...values.map(value => {
        const span = document.createElement('span');
        span.className = className; span.textContent = value;
        return span;
      }));
    }
    function closeDialog() { dialog.close(); }
    dialog.querySelector('.dialog-close').addEventListener('click', closeDialog);
    dialog.addEventListener('keydown', event => {
      if (event.key !== 'Tab') return;
      const first = dialog.querySelector('.dialog-close');
      const last = dialog.querySelector('#dialog-link');
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus();
      }
    });
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
      if (returnFocus?.isConnected) returnFocus.focus({preventScroll:true});
    });
    grid.addEventListener('click', async event => {
      const button = event.target.closest('[data-summary]');
      if (!button) return;
      returnFocus = button;
      button.setAttribute('aria-busy', 'true');
      try {
        const projects = await projectData();
        const p = projects.find(project => project.slug === button.dataset.summary);
        if (!p) throw new Error('Project not found');
        document.querySelector('#dialog-sector').textContent = p.kind + ' / ' + p.sector;
        document.querySelector('#dialog-title').textContent = p.company;
        document.querySelector('#dialog-subtitle').textContent = p.subtitle;
        document.querySelector('#dialog-description').textContent = p.summary;
        document.querySelector('#dialog-status').textContent = p.status;
        const badges = document.querySelector('#dialog-badges');
        badges.replaceChildren(...p.categories.map(c => {
          const badge = document.createElement('span');
          badge.className = 'badge ' + c.toLowerCase();
          badge.textContent = {BA:'Business Analysis',PM:'Project Management',DA:'Data Analytics'}[c];
          return badge;
        }));
        document.querySelector('#dialog-metrics').replaceChildren(...p.metrics.map(([value, label]) => {
          const div = document.createElement('div');
          const strong = document.createElement('strong'); strong.textContent = value;
          const span = document.createElement('span'); span.textContent = label;
          div.append(strong, span); return div;
        }));
        fillTags(document.querySelector('#dialog-skills'), p.skills, 'tag');
        document.querySelector('#dialog-link').href = '/projects/' + p.slug + '/';
        document.body.classList.add('dialog-open');
        dialog.showModal();
        dialog.querySelector('.dialog-close').focus();
      } catch (error) {
        // A full static case study is always available if the summary cannot load.
        window.location.href = '/projects/' + button.dataset.summary + '/';
      } finally { button.removeAttribute('aria-busy'); }
    });
  }

  const trackTabs = [...document.querySelectorAll('.track-switch [role="tab"]')];
  function selectTrack(tab, focus = false) {
    trackTabs.forEach(t => {
      const active = t === tab;
      t.setAttribute('aria-selected', String(active));
      t.tabIndex = active ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) tab.focus();
  }
  trackTabs.forEach((tab, i) => {
    tab.addEventListener('click', () => selectTrack(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (i + 1) % trackTabs.length;
      if (event.key === 'ArrowLeft') next = (i - 1 + trackTabs.length) % trackTabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = trackTabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectTrack(trackTabs[next], true); }
    });
  });
  const sectionLinks = [...document.querySelectorAll('.case-contents nav a')];
  if (sectionLinks.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        sectionLinks.forEach(link => {
          const active = link.hash === '#' + entry.target.id;
          link.classList.toggle('active', active);
          if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
        });
      }
    }, {rootMargin:'-120px 0px -55% 0px',threshold:0});
    document.querySelectorAll('.case-section').forEach(section => observer.observe(section));
  }
})();
