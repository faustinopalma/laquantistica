// Navigation: mobile toggle + highlight current page
(function () {
  var body = document.body;
  var toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      body.classList.toggle('nav-open');
    });
  }
  var scrim = document.querySelector('.scrim');
  if (scrim) {
    scrim.addEventListener('click', function () { body.classList.remove('nav-open'); });
  }
  // Mark active nav link based on current file name
  var current = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.sidebar nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === current) { a.classList.add('active'); }
  });
})();
