document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('[data-filter-form]');
  if (!form) return;

  form.addEventListener('change', () => {
    const params = new URLSearchParams(new FormData(form));
    const target = form.getAttribute('action') || window.location.pathname;
    window.location.href = `${target}?${params.toString()}`;
  });
});
