// Navbar + progress bar
const navbar = document.getElementById('navbar');
const progressBar = document.getElementById('progress-bar');
window.addEventListener('scroll', () => {
  if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 60);
  if (progressBar) {
    const pct = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = pct + '%';
  }
});

function toggleMenu() {
  const nav = document.getElementById('navLinks');
  if (nav) nav.classList.toggle('open');
}
document.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => {
  const nav = document.getElementById('navLinks');
  if (nav) nav.classList.remove('open');
}));

// Reveal on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Counter animation
function animateCounter(el) {
  const target = parseInt(el.dataset.target);
  if (!target) return;
  const suffix = el.dataset.suffix || (el.dataset.format === 'year' ? '' : el.dataset.pct ? '%' : '');
  let start = el.dataset.format === 'year' ? 2000 : 0;
  const duration = 1800;
  const step = (target - start) / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) { start = target; clearInterval(timer); }
    el.textContent = Math.round(start) + suffix;
  }, 16);
}
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      document.querySelectorAll('[data-target]').forEach(animateCounter);
      statsObserver.disconnect();
    }
  });
}, { threshold: 0.4 });
document.querySelectorAll('.hero-stats, .stats-row').forEach(el => statsObserver.observe(el));

// Contact form
function handleSubmit(e) {
  e.preventDefault();
  const form = document.querySelector('.contact-form');
  const success = document.getElementById('form-success');
  if (form) form.style.display = 'none';
  if (success) success.style.display = 'block';
}

// Project filter
document.querySelectorAll('.project-filter button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.project-filter button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('.proj-card').forEach(card => {
      card.style.display = (filter === 'all' || card.dataset.cat === filter) ? '' : 'none';
    });
  });
});
