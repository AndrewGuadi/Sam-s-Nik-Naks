document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('[data-mobile-toggle]');
  const menu = document.querySelector('[data-mobile-menu]');
  const openIcon = document.querySelector('[data-icon-open]');
  const closeIcon = document.querySelector('[data-icon-close]');

  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const hidden = menu.classList.toggle('hidden');
      toggle.setAttribute('aria-expanded', String(!hidden));
      if (openIcon && closeIcon) {
        openIcon.classList.toggle('hidden', !hidden);
        closeIcon.classList.toggle('hidden', hidden);
      }
    });
  }

  document.addEventListener('pointermove', (event) => {
    document.querySelectorAll('.gloss-track').forEach((el) => {
      const rect = el.getBoundingClientRect();
      el.style.setProperty('--mx', `${event.clientX - rect.left}px`);
      el.style.setProperty('--my', `${event.clientY - rect.top}px`);
    });
  });

  const yearTarget = document.querySelector('[data-year]');
  if (yearTarget) {
    yearTarget.textContent = new Date().getFullYear();
  }

  const countdown = document.querySelector('[data-countdown]');
  if (countdown) {
    const targetDate = countdown.dataset.target
      ? new Date(countdown.dataset.target)
      : new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);

    const render = () => {
      const now = new Date();
      const diff = Math.max(0, targetDate - now);
      const seconds = Math.floor(diff / 1000);
      const days = Math.floor(seconds / 86400);
      const hours = Math.floor((seconds % 86400) / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = seconds % 60;

      const pad = (value) => String(value).padStart(2, '0');
      countdown.querySelector('[data-dd]').textContent = pad(days);
      countdown.querySelector('[data-hh]').textContent = pad(hours);
      countdown.querySelector('[data-mm]').textContent = pad(minutes);
      countdown.querySelector('[data-ss]').textContent = pad(remainingSeconds);
    };

    render();
    setInterval(render, 1000);
  }
});
