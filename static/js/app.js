// Animated counters
document.querySelectorAll('[data-counter]').forEach(el => {
  const target = parseInt(el.dataset.counter, 10) || 0;
  const duration = 900;
  const step = Math.max(1, Math.ceil(target / (duration / 16)));
  let cur = 0;
  const tick = () => {
    cur = Math.min(target, cur + step);
    el.textContent = cur;
    if (cur < target) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
});

// Sidebar toggle
const toggle = document.getElementById('toggleSidebar');
const sidebar = document.getElementById('sidebar');
if (toggle && sidebar) {
  toggle.addEventListener('click', () => sidebar.classList.toggle('collapsed'));
}

// Auto-dismiss flash alerts after 4s
setTimeout(() => {
  document.querySelectorAll('.alert-dismissible').forEach(a => {
    try { new bootstrap.Alert(a).close(); } catch (e) {}
  });
}, 4000);