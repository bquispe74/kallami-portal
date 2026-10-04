document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav?.classList.toggle('is-open', open);
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded', 'false');
  }));
  const evaluationLink = document.getElementById('evaluation-link');
  const url = window.KALLAMI_LINKS?.autoevaluacion?.trim();
  if (evaluationLink && url && /^https:\/\//i.test(url)) {
    evaluationLink.href = url;
    evaluationLink.target = '_blank';
    evaluationLink.rel = 'noopener noreferrer';
  }
});
