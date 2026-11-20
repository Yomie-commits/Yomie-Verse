/* YomieVerse — navigation, reveal, enquiry form, analytics hooks */
(function () {
  "use strict";
  window.__yv = true;
  var SITE = window.SITE || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Analytics (only if configured) ---------- */
  function track(name, params) {
    try {
      if (window.gtag) window.gtag("event", name, params || {});
      if (window.dataLayer) window.dataLayer.push(Object.assign({ event: name }, params || {}));
    } catch (e) { /* analytics must never break the page */ }
  }
  (function analytics() {
    if (SITE.cloudflareAnalyticsToken) {
      var s = document.createElement("script"); s.defer = true; s.src = "https://static.cloudflareinsights.com/beacon.min.js";
      s.setAttribute("data-cf-beacon", JSON.stringify({ token: SITE.cloudflareAnalyticsToken })); document.head.appendChild(s);
    }
    if (SITE.ga4MeasurementId) {
      var g = document.createElement("script"); g.async = true; g.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(SITE.ga4MeasurementId); document.head.appendChild(g);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date()); window.gtag("config", SITE.ga4MeasurementId, { anonymize_ip: true });
    }
  })();
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-track]"); if (a) track(a.getAttribute("data-track"), { label: (a.textContent || "").trim().slice(0, 60), page: location.pathname });
  });

  /* ---------- Mobile navigation ---------- */
  var toggle = $(".nav-toggle"), menu = $("#menu");
  function closeMenu() { if (!menu) return; menu.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); toggle.setAttribute("aria-label", "Open menu"); }
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) closeMenu(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && menu.classList.contains("is-open")) { closeMenu(); toggle.focus(); } });
    window.addEventListener("resize", function () { if (window.innerWidth > 1060) closeMenu(); });
  }

  /* ---------- Reveal on scroll ---------- */
  var items = $$(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  } else items.forEach(function (el) { el.classList.add("in"); });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Email links come from config.js (kept out of the HTML) ---------- */
  $$("[data-email]").forEach(function (el) {
    if (!SITE.email) return;
    el.href = "mailto:" + SITE.email;
    if (el.hasAttribute("data-email-show")) el.textContent = SITE.email;
  });

  /* ---------- Dropdown menus (Our Products) ---------- */
  $$(".dd-toggle").forEach(function (b) {
    var item = b.closest(".has-dd");
    b.addEventListener("click", function (e) {
      e.preventDefault();
      var open = b.getAttribute("aria-expanded") !== "true";
      $$(".dd-toggle[aria-expanded=true]").forEach(function (o) { if (o !== b) { o.setAttribute("aria-expanded", "false"); o.closest(".has-dd").classList.remove("dd-open"); } });
      b.setAttribute("aria-expanded", String(open)); item.classList.toggle("dd-open", open);
    });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".has-dd")) $$(".has-dd.dd-open").forEach(function (i) { i.classList.remove("dd-open"); i.querySelector(".dd-toggle").setAttribute("aria-expanded", "false"); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") $$(".has-dd.dd-open").forEach(function (i) { i.classList.remove("dd-open"); var t = i.querySelector(".dd-toggle"); t.setAttribute("aria-expanded", "false"); if (i.contains(document.activeElement)) t.focus(); }); });

  /* ---------- Booking link (optional) ---------- */
  if (SITE.bookingUrl) $$("[data-booking]").forEach(function (el) { el.hidden = false; el.href = SITE.bookingUrl; });

  /* ---------- Enquiry form ---------- */
  var form = $("#enquiry-form");
  if (!form) return;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^[+()\d\s-]{7,20}$/;

  // Prefill from links such as contact.html?service=leadflow&type=demo
  try {
    var q = new URLSearchParams(location.search);
    var svc = q.get("service"), type = q.get("type");
    if (svc) { var opt = form.querySelector('select[name="Service of interest"] option[data-key="' + svc.replace(/[^a-z-]/gi, "") + '"]'); if (opt) opt.selected = true; }
    if (type) { var r = form.querySelector('input[name="Request type"][data-key="' + type.replace(/[^a-z-]/gi, "") + '"]'); if (r) r.checked = true; }
  } catch (e) { /* ignore */ }

  // No-JavaScript fallback posts straight to FormSubmit; with JS we send it in the background.
  form.action = "https://formsubmit.co/" + encodeURIComponent(SITE.email || "");
  var next = form.querySelector('input[name="_next"]'); if (next) next.value = new URL("thank-you.html", location.href).href;

  function fieldWrap(el) { return el.closest(".field"); }
  function setErr(el, msg) {
    var w = fieldWrap(el); if (!w) return;
    var e = w.querySelector(".err");
    if (msg) { w.classList.add("has-error"); if (e) e.textContent = msg; el.setAttribute("aria-invalid", "true"); if (e && e.id) el.setAttribute("aria-describedby", e.id); }
    else { w.classList.remove("has-error"); el.removeAttribute("aria-invalid"); }
  }
  function check(el) {
    var v = (el.value || "").trim(), msg = "";
    if (el.type === "radio") {
      var group = form.querySelectorAll('input[name="' + el.name + '"]'), any = Array.prototype.some.call(group, function (x) { return x.checked; });
      if (el.required && !any) msg = el.getAttribute("data-msg") || "Please choose an option.";
      setErr(group[0], msg); return !msg;
    }
    if (el.type === "checkbox") { if (el.required && !el.checked) msg = el.getAttribute("data-msg") || "Please confirm to continue."; }
    else if (el.required && !v) msg = el.getAttribute("data-msg") || "This field is required.";
    else if (v && el.type === "email" && !EMAIL_RE.test(v)) msg = "Please enter a valid email address, like name@business.com.";
    else if (v && el.type === "tel" && !PHONE_RE.test(v)) msg = "Please enter a valid phone number, e.g. +254 712 345 678.";
    else if (v && el.minLength > 0 && v.length < el.minLength) msg = "Please add a little more detail (at least " + el.minLength + " characters).";
    setErr(el, msg); return !msg;
  }
  function validate() {
    var first = null, seen = {};
    $$("[required], input[type=email], input[type=tel]", form).forEach(function (el) {
      if (el.type === "radio") { if (seen[el.name]) return; seen[el.name] = 1; }
      if (!check(el) && !first) first = el;
    });
    if (first) first.focus();
    return !first;
  }
  form.addEventListener("blur", function (e) { if (e.target.matches("input, select, textarea") && e.target.value) check(e.target); }, true);
  form.addEventListener("input", function (e) { if (fieldWrap(e.target) && fieldWrap(e.target).classList.contains("has-error")) check(e.target); });
  form.addEventListener("change", function (e) { if (e.target.type === "radio" || e.target.type === "checkbox") check(e.target); });

  var msgBox = $("#form-msg"), btn = form.querySelector("[type=submit]"), btnHtml = btn ? btn.innerHTML : "";
  function showMsg(kind, html) { msgBox.hidden = false; msgBox.className = "form-msg form-msg--" + kind; msgBox.innerHTML = html; msgBox.setAttribute("role", kind === "err" ? "alert" : "status"); }
  function waLink() { return "https://wa.me/" + (SITE.whatsapp || "") + "?text=" + encodeURIComponent("Hello " + (SITE.brand || "YomieVerse") + ", I tried to send an enquiry on your website."); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    msgBox.hidden = true;
    if (form.querySelector('input[name="_honey"]').value) return; // spam trap
    if (!validate()) { showMsg("err", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg><span>Please fix the highlighted fields and try again.</span>'); return; }
    if (location.protocol === "file:") { showMsg("ok", "<span><strong>Preview:</strong> the form is valid. Enquiries are delivered once the site is online.</span>"); return; }

    var data = {};
    new FormData(form).forEach(function (v, k) { if (k !== "_next") data[k] = data[k] ? data[k] + ", " + v : v; });
    data._subject = "New " + (SITE.brand || "YomieVerse") + " enquiry — " + (data["Service of interest"] || data["Product"] || "General") + " (" + (data["Request type"] || "Enquiry") + ")";
    btn.disabled = true; btn.innerHTML = '<span class="spinner" aria-hidden="true"></span> Sending…';
    var ctrl = window.AbortController ? new AbortController() : null, timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 20000);

    fetch("https://formsubmit.co/ajax/" + encodeURIComponent(SITE.email || ""), {
      method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data), signal: ctrl ? ctrl.signal : undefined
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        clearTimeout(timer);
        var ok = res.ok && (res.j.success === true || res.j.success === "true");
        if (!ok) {
          var needsActivation = /activat/i.test(String(res.j.message || ""));
          throw new Error(needsActivation ? "activation" : "failed");
        }
        track("generate_lead", { service: data["Service of interest"], type: data["Request type"] });
        var name = String(data["Full name"] || "").split(" ")[0];
        form.hidden = true;
        var done = $("#form-done"); done.hidden = false;
        var n = $("#done-name"); if (n) n.textContent = name ? ", " + name : "";
        var how = $("#done-how"); if (how) how.textContent = (data["Preferred contact method"] || "email").toLowerCase();
        done.focus();
      })
      .catch(function (err) {
        clearTimeout(timer);
        var act = err && err.message === "activation";
        showMsg("err", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg><span><strong>' +
          (act ? "Our form is being set up." : "Sorry, your message couldn't be sent.") + "</strong> " +
          (act ? "Please reach us directly for now: " : "Please check your connection and try again, or reach us directly: ") +
          '<a href="' + waLink() + '" target="_blank" rel="noopener">WhatsApp</a> or <a href="mailto:' + (SITE.email || "") + '">' + (SITE.email || "email") + "</a>.</span>");
        track("form_error", { reason: act ? "activation" : "network" });
      })
      .then(function () { btn.disabled = false; btn.innerHTML = btnHtml; });
  });
})();
