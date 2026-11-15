/* Tabs: one panel at a time; the URL hash (#tool-<id>) picks a tab, so
   links like the table's "#tool-ngspice" open the right one. */
(() => {
  document.querySelectorAll('[data-tabs]').forEach(box => {
    box.classList.add('js');
    const tabs = [...box.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));
    function select(k, focus) {
      tabs.forEach((t, j) => {
        const on = j === k;
        t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; panels[j].hidden = !on;
      });
      if (focus) tabs[k].focus();
    }
    tabs.forEach((t, k) => {
      t.addEventListener('click', () => { select(k); history.replaceState(null, '', '#' + panels[k].id); });
      t.addEventListener('keydown', e => {
        const d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); select((k + d + tabs.length) % tabs.length, true); }
        else if (e.key === 'Home') { e.preventDefault(); select(0, true); }
        else if (e.key === 'End') { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
    function fromHash(scroll) {
      const k = panels.findIndex(p => '#' + p.id === location.hash);
      if (k < 0) return false;
      select(k);
      if (scroll) box.scrollIntoView({ block: 'start' });
      return true;
    }
    if (!fromHash(false)) select(0);
    addEventListener('hashchange', () => fromHash(true));
    // In-page links to a tab (the table) switch tabs even when the hash is already that one.
    document.querySelectorAll('a[href^="#tool-"]').forEach(a => a.addEventListener('click', e => {
      const k = panels.findIndex(p => '#' + p.id === a.getAttribute('href'));
      if (k < 0) return;
      e.preventDefault(); select(k); history.replaceState(null, '', a.getAttribute('href'));
      box.scrollIntoView({ block: 'start', behavior: 'smooth' });
    }));
  });
})();

/* Shared step player, lightbox and copy buttons for every guide page. */
(() => {
  if (!document.getElementById('player')) return;  // pages without steps (the index)
  const steps = [...document.querySelectorAll('.step[data-title]')].map(el => ({
    el,
    n: el.querySelector('.num').textContent,
    title: el.dataset.title,
    doText: el.dataset.do,
    img: el.dataset.img || null,
  }));
  const player = document.getElementById('player');
  const stage = document.getElementById('p-stage');
  const pN = document.getElementById('p-n'), pTitle = document.getElementById('p-title');
  const pDo = document.getElementById('p-do'), pBar = document.getElementById('p-bar');
  const playBtn = document.getElementById('p-play');
  const SECONDS = 7;
  let i = 0, timer = null, mode = 'video';

  function render() {
    const s = steps[i];
    pN.textContent = mode === 'video' ? `Step ${s.n} of ${steps.length}` : `Step ${s.n}`;
    pTitle.textContent = s.title;
    pDo.textContent = s.doText;
    stage.replaceChildren();
    if (s.img) {
      const im = new Image(); im.src = s.img; im.alt = s.title; stage.append(im);
    } else {
      const p = document.createElement('p');
      p.className = 'do-line'; p.style.fontSize = '1.4rem'; p.textContent = '⌨  ' + s.doText;
      stage.append(p);
    }
    pBar.style.width = ((i + 1) / steps.length * 100) + '%';
    document.getElementById('p-prev').disabled = i === 0;
    document.getElementById('p-next').disabled = i === steps.length - 1;
  }
  function stop() { clearInterval(timer); timer = null; playBtn.textContent = '▶ Play'; }
  function play() {
    stop(); playBtn.textContent = '⏸ Pause';
    timer = setInterval(() => { if (i < steps.length - 1) { i++; render(); } else stop(); }, SECONDS * 1000);
  }
  function open(at, asVideo) {
    i = at; mode = asVideo ? 'video' : 'still';
    player.hidden = false; document.body.style.overflow = 'hidden';
    render(); asVideo ? play() : stop();
    playBtn.hidden = !asVideo;
    document.getElementById('p-close').focus();
  }
  function close() {
    stop(); player.hidden = true; document.body.style.overflow = '';
    steps[i].el.scrollIntoView({ block: 'start' });
  }
  document.getElementById('play-all').addEventListener('click', () => open(0, true));
  document.getElementById('p-close').addEventListener('click', close);
  document.getElementById('p-prev').addEventListener('click', () => { if (i > 0) { i--; render(); if (timer) play(); } });
  document.getElementById('p-next').addEventListener('click', () => { if (i < steps.length - 1) { i++; render(); if (timer) play(); } });
  playBtn.addEventListener('click', () => timer ? stop() : play());
  document.addEventListener('keydown', e => {
    if (player.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') document.getElementById('p-next').click();
    else if (e.key === 'ArrowLeft') document.getElementById('p-prev').click();
    else if (e.key === ' ' && mode === 'video') { e.preventDefault(); playBtn.click(); }
  });
  // Clicking a screenshot opens it full size (still mode, arrows still page through the steps).
  document.querySelectorAll('.shot').forEach(btn => btn.addEventListener('click', () => {
    const src = btn.querySelector('img').getAttribute('src');
    const at = steps.findIndex(s => s.el.contains(btn));
    if (steps[at].img === src) return open(at, false);
    // a secondary image (the plot close-up): show it alone
    open(at, false);
    stage.replaceChildren(Object.assign(new Image(), { src, alt: btn.querySelector('img').alt }));
  }));
  document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', async () => {
    const text = b.dataset.copy;
    try { await navigator.clipboard.writeText(text); b.textContent = 'Copied'; }
    catch {
      const pre = b.parentElement.querySelector('pre');
      const r = document.createRange(); r.selectNodeContents(pre);
      const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
      b.textContent = 'Selected: press Ctrl+C';
    }
    setTimeout(() => (b.textContent = 'Copy'), 2000);
  }));
})();
