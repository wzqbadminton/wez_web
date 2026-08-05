(function () {
  'use strict';

  const PHOTOS = [
    'gallery-01.jpg','gallery-02.jpg','gallery-03.jpg',
    'gallery-04.jpg','gallery-05.jpg','gallery-06.jpg',
    'gallery-07.jpg','gallery-08.jpg','gallery-09.jpg',
    'gallery-10.jpg','gallery-11.jpg','gallery-12.jpg',
    'gallery-13.jpg'
  ];
  const AUTO_MS = 3000;

  function init() {
    const root = document.getElementById('gallery');
    const track = document.getElementById('gallery-track');
    const dotsWrap = document.getElementById('gallery-dots');
    if (!root || !track || !dotsWrap) return;

    PHOTOS.forEach((file, i) => {
      const slide = document.createElement('div');
      slide.className = 'slide';
      slide.setAttribute('role', 'group');
      slide.setAttribute('aria-roledescription', 'slide');
      slide.setAttribute('aria-label', (i + 1) + ' of ' + PHOTOS.length);

      const img = document.createElement('img');
      img.src = 'pic/' + encodeURIComponent(file);
      img.alt = 'WZQ Badminton Club photo ' + (i + 1);
      img.loading = i === 0 ? 'eager' : 'lazy';
      img.decoding = 'async';
      slide.appendChild(img);
      track.appendChild(slide);

      const dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Photo ' + (i + 1));
      dot.addEventListener('click', () => go(i, true));
      dotsWrap.appendChild(dot);
    });

    let idx = 0;
    let timer = null;
    const dots = dotsWrap.querySelectorAll('button');

    function render() {
      track.style.transform = 'translateX(' + (-idx * 100) + '%)';
      dots.forEach((d, i) => d.classList.toggle('active', i === idx));
    }
    function go(n, userAction) {
      idx = (n + PHOTOS.length) % PHOTOS.length;
      render();
      if (userAction) restart();
    }
    function next() { go(idx + 1); }
    function prev() { go(idx - 1); }

    function start() { stop(); timer = setInterval(next, AUTO_MS); }
    function stop()  { if (timer) { clearInterval(timer); timer = null; } }
    function restart() { start(); }

    root.querySelector('.gallery-arrow.next').addEventListener('click', () => { next(); restart(); });
    root.querySelector('.gallery-arrow.prev').addEventListener('click', () => { prev(); restart(); });

    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);
    root.addEventListener('focusin', stop);
    root.addEventListener('focusout', start);

    root.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); next(); restart(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); prev(); restart(); }
    });

    // Touch swipe
    let startX = null;
    root.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', (e) => {
      if (startX == null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) { dx < 0 ? next() : prev(); restart(); }
      startX = null;
    });

    render();
    start();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
