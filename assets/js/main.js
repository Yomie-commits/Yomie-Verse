// YomieVerse site scripts: mobile menu, scroll reveal, footer year, form redirect.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('visible'); });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Contact email comes from assets/js/config.js so it lives in one place.
  var email = (window.SITE && window.SITE.email) || '';
  if (email) {
    document.querySelectorAll('[data-email]').forEach(function (a) {
      var subject = a.getAttribute('data-subject');
      a.href = 'mailto:' + email + (subject ? '?subject=' + encodeURIComponent(subject) : '');
      if (a.hasAttribute('data-email-text')) a.textContent = email;
    });
    document.querySelectorAll('form[data-formsubmit]').forEach(function (f) {
      f.action = 'https://formsubmit.co/' + email;
    });
  }

  // FormSubmit needs an absolute "thank you" URL; build it from wherever the site is hosted.
  document.querySelectorAll('input[name="_next"]').forEach(function (input) {
    input.value = new URL('thank-you.html', window.location.href).href;
  });
  document.querySelectorAll('input[name="_url"]').forEach(function (input) {
    input.value = window.location.href;
  });

  // Pre-select a package when arriving from the pricing page (contact.html?package=Professional).
  var params = new URLSearchParams(window.location.search);
  var pkg = params.get('package');
  var needs = document.getElementById('needs');
  if (pkg && needs && !needs.value) {
    needs.value = 'I am interested in the ' + pkg + ' package.';
  }
  var type = params.get('type');
  var reqType = document.getElementById('request_type');
  if (type && reqType) {
    for (var i = 0; i < reqType.options.length; i++) {
      if (reqType.options[i].value.toLowerCase().indexOf(type.toLowerCase()) === 0) { reqType.selectedIndex = i; }
    }
  }
})();
