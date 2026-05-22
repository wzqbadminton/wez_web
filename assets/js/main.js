(function () {
  'use strict';

  const els = document.querySelectorAll('.fade-in');
  if (!('IntersectionObserver' in window)) {
    els.forEach((el) => el.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          observer.unobserve(e.target);
        }
      });
    },
    { threshold: 0.08 }
  );

  els.forEach((el) => observer.observe(el));

  // ----- Lightbox -----
  const overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-hidden', 'true');
  overlay.innerHTML = '<button type="button" class="lightbox-close" aria-label="Close">&times;</button><img alt="">';
  document.body.appendChild(overlay);
  const overlayImg = overlay.querySelector('img');
  const closeBtn = overlay.querySelector('.lightbox-close');

  function openLightbox(src, alt) {
    overlayImg.src = src;
    overlayImg.alt = alt || '';
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    setTimeout(() => { overlayImg.src = ''; }, 250);
  }

  overlay.addEventListener('click', (e) => { if (e.target === overlay || e.target === closeBtn) closeLightbox(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && overlay.classList.contains('open')) closeLightbox(); });

  // Program cards (background-image)
  document.querySelectorAll('.program-img').forEach((el) => {
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
    const activate = () => {
      const bg = el.style.backgroundImage || getComputedStyle(el).backgroundImage;
      const m = bg && bg.match(/url\((['"]?)(.*?)\1\)/);
      if (m && m[2]) {
        const title = el.parentElement && el.parentElement.querySelector('h3');
        openLightbox(m[2], title ? title.textContent : '');
      }
    };
    el.addEventListener('click', activate);
    el.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(); } });
  });

  // Gallery slides
  document.querySelectorAll('#gallery-track img, .slide img').forEach((img) => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => openLightbox(img.src, img.alt));
  });
})();
