/* ============================================================
   RK Perfume – main.js
   Minor enhancements: auto-dismiss alerts, smooth scroll, etc.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss flash alerts after 4 seconds ────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });

  // ── Smooth scroll for any in-page # links ─────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Navbar: add shadow on scroll ──────────────────────────
  const navbar = document.querySelector('.rk-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 20) {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.06)';
      } else {
        navbar.style.boxShadow = 'none';
      }
    });
  }

});