/* Lumen&Form — shared behaviour.
   Depends on data.js (window.LF_DATA). Every feature is progressive:
   the static HTML is complete and readable without this file. */
(function () {
  'use strict';
  var D = window.LF_DATA;
  var root = document.documentElement;
  window.__lfReady = true;

  var reduceMQ = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var motion = root.classList.contains('motion') && !reduceMQ.matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function pkgById(id) {
    if (!D) return null;
    for (var i = 0; i < D.packages.length; i++) if (D.packages[i].id === id) return D.packages[i];
    return null;
  }
  function pkgByName(name) {
    if (!D) return null;
    for (var i = 0; i < D.packages.length; i++) if (D.packages[i].name === name) return D.packages[i];
    return null;
  }
  function currency(code) {
    if (!D) return null;
    for (var i = 0; i < D.currencies.length; i++) if (D.currencies[i].code === code) return D.currencies[i];
    return null;
  }

  /* ---------- Header state ---------- */
  var header = $('#site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Footer year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ---------- Currency switching (Home + Pricing) ----------
     USD by default. Another currency is used only after the visitor picks it;
     that explicit choice is remembered for this browsing session only. */
  var CUR_KEY = 'lf-currency';
  function storedCurrency() {
    try { var v = window.sessionStorage.getItem(CUR_KEY); return currency(v) ? v : null; } catch (e) { return null; }
  }
  function storeCurrency(code) { try { window.sessionStorage.setItem(CUR_KEY, code); } catch (e) {} }

  function applyCurrency(code, announce) {
    if (!D || !currency(code)) return;
    $$('[data-price]').forEach(function (el) {
      var p = pkgById(el.getAttribute('data-price'));
      if (p) el.textContent = p.prices[code];
    });
    $$('[data-package-cta]').forEach(function (a) {
      a.setAttribute('href', '/contact/?package=' + encodeURIComponent(a.getAttribute('data-package-cta')) +
        '&currency=' + code + '#enquiry');
    });
    $$('[data-currency-switch] input[type="radio"]').forEach(function (r) { r.checked = (r.value === code); });
    $$('[data-currency-name]').forEach(function (el) { el.textContent = currency(code).name; });
    if (announce) {
      $$('[data-currency-live]').forEach(function (el) {
        el.textContent = 'Prices now shown in ' + currency(code).name + '.';
      });
    }
  }

  if ($('[data-currency-switch]')) {
    applyCurrency(storedCurrency() || (D && D.defaultCurrency) || 'USD', false);
    $$('[data-currency-switch] input[type="radio"]').forEach(function (r) {
      r.addEventListener('change', function () {
        if (!r.checked) return;
        storeCurrency(r.value);
        applyCurrency(r.value, true);
      });
    });
  }

  /* ---------- Contact form: package preselection ---------- */
  var form = $('#enquiry-form');
  if (form && D) {
    var pkgSelect = $('#f-package', form);
    var curSelect = $('#f-currency', form);
    var banner = $('#selection-banner');
    var bannerText = $('#selection-text');
    var clearBtn = $('#selection-clear');
    var changeBtn = $('#selection-change');

    var params = new URLSearchParams(window.location.search);
    var qp = pkgById(params.get('package'));
    var qc = currency((params.get('currency') || '').toUpperCase());
    if (qp) pkgSelect.value = qp.name;
    if (qc) curSelect.value = qc.code;
    else if (!qp && storedCurrency()) curSelect.value = storedCurrency();

    var updateBanner = function () {
      var p = pkgByName(pkgSelect.value);
      var c = currency(curSelect.value) || currency('USD');
      if (!p) { banner.hidden = true; return; }
      bannerText.innerHTML = '';
      var lead = document.createTextNode('Selected package: ');
      var strong = document.createElement('strong');
      strong.textContent = p.name + ' · ' + (p.from ? 'from ' : '') + p.prices[c.code] + ' (' + c.code + ')';
      bannerText.appendChild(lead);
      bannerText.appendChild(strong);
      if (p.id === 'extended') {
        bannerText.appendChild(document.createTextNode('. Staged payment: 30% after homepage approval, balance after final approval.'));
      } else {
        bannerText.appendChild(document.createTextNode('. Paid after final approval.'));
      }
      banner.hidden = false;
    };
    pkgSelect.addEventListener('change', updateBanner);
    curSelect.addEventListener('change', updateBanner);
    clearBtn.addEventListener('click', function () {
      pkgSelect.value = '';
      curSelect.value = 'USD';
      updateBanner();
      pkgSelect.focus();
    });
    changeBtn.addEventListener('click', function () { pkgSelect.focus(); });
    updateBanner();

    /* ---------- Contact form: validation, native POST ----------
       Netlify Forms receives a normal form POST and redirects to /thank-you/.
       Nothing here simulates success: if the fields are valid, the browser submits. */
    form.noValidate = true;
    var summary = $('#form-errors');
    var submitBtn = $('#form-submit');
    var submitLabel = submitBtn ? submitBtn.textContent : '';
    var rules = [
      { id: 'f-name', msg: 'Please enter your name.' },
      { id: 'f-business', msg: 'Please enter your business name.' },
      { id: 'f-email', msg: 'Please enter an email address I can reply to, for example name@business.com.', email: true },
      { id: 'f-message', msg: 'Please tell me briefly what the new site should do for you.' }
    ];
    var setError = function (input, msg) {
      var field = input.closest('.field');
      var err = $('#' + input.id + '-error');
      if (msg) {
        field.classList.add('has-error');
        input.setAttribute('aria-invalid', 'true');
        if (err) err.textContent = msg;
      } else {
        field.classList.remove('has-error');
        input.removeAttribute('aria-invalid');
        if (err) err.textContent = '';
      }
    };
    var check = function (rule) {
      var input = $('#' + rule.id, form);
      var v = input.value.trim();
      var bad = !v || (rule.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
      setError(input, bad ? rule.msg : '');
      return !bad;
    };
    rules.forEach(function (rule) {
      var input = $('#' + rule.id, form);
      input.addEventListener('blur', function () { if (input.value.trim() || input.closest('.has-error')) check(rule); });
      input.addEventListener('input', function () { if (input.closest('.has-error')) check(rule); });
    });
    form.addEventListener('submit', function (e) {
      var firstBad = null;
      rules.forEach(function (rule) { if (!check(rule) && !firstBad) firstBad = $('#' + rule.id, form); });
      if (firstBad) {
        e.preventDefault();
        summary.hidden = false;
        summary.textContent = 'Some required details are missing. Please check the highlighted fields.';
        firstBad.focus();
        return;
      }
      summary.hidden = true;
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
    });
    /* If the visitor returns with the back button, restore the button. */
    window.addEventListener('pageshow', function () {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitLabel; }
    });
  }

  /* ---------- Motion ---------- */
  if (!motion) return;

  /* Scroll reveals (content is visible unless this runs) */
  if ('IntersectionObserver' in window) {
    root.classList.add('io');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    $$('.reveal, .reveal-mask').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.95) el.classList.add('is-in');
      else io.observe(el);
    });
  }

  /* Signature transition: the dark field behind Selected websites opens like
     light widening across a surface, driven by normal scrolling (desktop only). */
  var stage = $('.reveal-stage');
  var desktop = window.matchMedia('(min-width: 901px)');
  if (stage) {
    var ticking = false;
    var update = function () {
      ticking = false;
      if (!desktop.matches) { stage.style.setProperty('--p', '1'); return; }
      var r = stage.getBoundingClientRect();
      var vh = window.innerHeight || 800;
      var p = (vh - r.top) / (vh * 0.65);
      p = Math.max(0, Math.min(1, p));
      p = 1 - Math.pow(1 - p, 2); /* ease-out */
      stage.style.setProperty('--p', p.toFixed(3));
    };
    var req = function () { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } };
    update();
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
  }
})();
