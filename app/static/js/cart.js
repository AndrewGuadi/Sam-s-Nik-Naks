const confetti = () => {
  const burst = document.createElement('div');
  burst.className = 'pointer-events-none fixed inset-0 overflow-hidden';
  burst.innerHTML = '<div class="absolute inset-0 animate-ping opacity-60 bg-gradient-to-r from-sky-400/30 via-cyan-300/30 to-emerald-300/30"></div>';
  document.body.appendChild(burst);
  setTimeout(() => burst.remove(), 600);
};

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-add-to-cart]').forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      confetti();
    });
  });
});
