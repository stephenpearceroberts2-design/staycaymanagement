/* Staycay Management — site behaviour
   Settings come from data attributes on <html>, written by tools/build.py:
   data-ga (GA4 measurement ID) and data-calendly (Calendly event URL). */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var GA_ID = doc.getAttribute("data-ga") || "";
  var CALENDLY = doc.getAttribute("data-calendly") || "";
  var GA_READY = /^G-[A-Z0-9]{6,}$/.test(GA_ID) && GA_ID !== "G-XXXXXXXXXX";
  var CONSENT_KEY = "stc_consent";          // "granted" | "denied"
  var FIRST_TOUCH_KEY = "stc_first_touch";  // stored only with analytics consent

  function store(type) { try { return window[type]; } catch (e) { return null; } }
  function getLS(k) { var s = store("localStorage"); try { return s ? s.getItem(k) : null; } catch (e) { return null; } }
  function setLS(k, v) { var s = store("localStorage"); try { if (s) s.setItem(k, v); } catch (e) {} }
  function getSS(k) { var s = store("sessionStorage"); try { return s ? s.getItem(k) : null; } catch (e) { return null; } }
  function setSS(k, v) { var s = store("sessionStorage"); try { if (s) s.setItem(k, v); } catch (e) {} }
  function delSS(k) { var s = store("sessionStorage"); try { if (s) s.removeItem(k); } catch (e) {} }

  /* ---------------- Analytics (GA4, loaded only after consent) ---------------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag("consent", "default", { analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
  var gaLoaded = false;

  function loadGA() {
    if (gaLoaded || !GA_READY) return;
    gaLoaded = true;
    gtag("consent", "update", { analytics_storage: "granted" });
    gtag("js", new Date());
    gtag("config", GA_ID, { anonymize_ip: true });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
  }

  function track(name, params) {
    params = params || {};
    params.page_path = location.pathname;
    if (gaLoaded) window.gtag("event", name, params);
    if (window.console && doc.hasAttribute("data-debug")) console.log("[track]", name, params);
  }
  window.staycayTrack = track;

  /* ---------------- Cookie consent ---------------- */
  var consentEl = document.getElementById("consent");
  function consent() { return getLS(CONSENT_KEY); }
  function openConsent() { if (consentEl) { consentEl.classList.add("is-open"); var b = consentEl.querySelector("button"); if (b) b.focus(); } }
  function closeConsent() { if (consentEl) consentEl.classList.remove("is-open"); }
  function setConsent(v) {
    setLS(CONSENT_KEY, v);
    closeConsent();
    if (v === "granted") { loadGA(); saveFirstTouch(); }
    else if (gaLoaded) { window.gtag("consent", "update", { analytics_storage: "denied" }); }
  }
  if (consentEl) {
    consentEl.addEventListener("click", function (e) {
      var b = e.target.closest("[data-consent]");
      if (b) setConsent(b.getAttribute("data-consent"));
    });
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-open-consent]")) { e.preventDefault(); openConsent(); }
  });
  if (consent() === "granted") { loadGA(); }
  else if (!consent() && consentEl) { setTimeout(openConsent, 600); }

  /* ---------------- Attribution ---------------- */
  function currentTouch() {
    var p = new URLSearchParams(location.search);
    var ref = document.referrer && document.referrer.indexOf(location.host) === -1 ? document.referrer : "";
    return {
      landing_page: location.pathname,
      referrer: ref,
      utm_source: p.get("utm_source") || "",
      utm_medium: p.get("utm_medium") || "",
      utm_campaign: p.get("utm_campaign") || "",
      utm_term: p.get("utm_term") || "",
      utm_content: p.get("utm_content") || ""
    };
  }
  var pageTouch = currentTouch();
  function saveFirstTouch() {
    if (consent() !== "granted" || getLS(FIRST_TOUCH_KEY)) return;
    setLS(FIRST_TOUCH_KEY, JSON.stringify(pageTouch));
  }
  saveFirstTouch();
  function attribution() {
    var ft = null;
    try { ft = JSON.parse(getLS(FIRST_TOUCH_KEY) || "null"); } catch (e) {}
    return ft || pageTouch;
  }

  /* ---------------- Header & nav ---------------- */
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (header && header.classList.contains("site-header--overlay")) {
    var onScroll = function () { header.classList.toggle("is-solid", window.scrollY > 40); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = !document.body.classList.contains("nav-open");
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) { toggle.click(); toggle.focus(); }
    });
  }

  /* ---------------- Reveal on scroll ---------------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("is-in"); }); }

  /* ---------------- CTA + outbound tracking ---------------- */
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track]");
    if (!el) return;
    var name = el.getAttribute("data-track");
    var params = { cta_location: el.getAttribute("data-track-location") || "", link_text: (el.textContent || "").trim().slice(0, 80) };
    if (el.hasAttribute("data-property")) params.property = el.getAttribute("data-property");
    if (el.href) params.link_url = el.href;
    track(name, params);
  });

  /* ---------------- Calendly (15-minute call) ---------------- */
  var modal = document.getElementById("call-modal");
  var lastFocus = null;
  function openCalendly(source) {
    if (!modal || !CALENDLY) { if (CALENDLY) location.href = CALENDLY; return; }
    var frame = modal.querySelector("iframe");
    if (!frame.getAttribute("src")) {
      var u = CALENDLY + (CALENDLY.indexOf("?") > -1 ? "&" : "?") +
        "embed_domain=" + encodeURIComponent(location.hostname) +
        "&embed_type=Inline&hide_gdpr_banner=1&background_color=f3f0e9&text_color=272727&primary_color=263b32";
      var a = attribution();
      if (a.utm_source) u += "&utm_source=" + encodeURIComponent(a.utm_source);
      if (a.utm_medium) u += "&utm_medium=" + encodeURIComponent(a.utm_medium);
      if (a.utm_campaign) u += "&utm_campaign=" + encodeURIComponent(a.utm_campaign);
      frame.setAttribute("src", u);
    }
    lastFocus = document.activeElement;
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
    modal.querySelector(".modal__close").focus();
    track("calendly_open", { cta_location: source || "" });
  }
  function closeCalendly() {
    if (!modal) return;
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-calendly-open]");
    if (b) { e.preventDefault(); openCalendly(b.getAttribute("data-track-location")); }
    if (e.target.closest("[data-modal-close]") || e.target === modal) closeCalendly();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal && modal.classList.contains("is-open")) closeCalendly();
  });
  window.addEventListener("message", function (e) {
    if (!/calendly\.com$/.test((function () { try { return new URL(e.origin).hostname; } catch (x) { return ""; } })())) return;
    var ev = e.data && e.data.event;
    if (ev === "calendly.date_and_time_selected") track("calendly_time_selected", {});
    if (ev === "calendly.event_scheduled") {
      var a = attribution();
      track("calendly_booking", { landing_page: a.landing_page, source: a.utm_source || a.referrer || "direct" });
    }
  });

  /* ---------------- Forms ---------------- */
  document.querySelectorAll("form[data-staycay-form]").forEach(function (form) {
    var formName = form.getAttribute("name");
    var started = false;
    form.addEventListener("input", function () {
      if (started) return;
      started = true;
      track(formName === "appraisal" ? "appraisal_form_start" : "form_start", { form_name: formName });
    });
    // fill hidden attribution fields
    var a = attribution();
    Object.keys(a).forEach(function (k) {
      var f = form.querySelector('input[name="' + k + '"]');
      if (f) f.value = a[k];
    });
    var pageField = form.querySelector('input[name="form_page"]');
    if (pageField) pageField.value = location.pathname;
    // service interest pre-selection, e.g. ?service=full-management
    var svc = new URLSearchParams(location.search).get("service");
    if (svc) {
      var radio = form.querySelector('input[name="service_interest"][data-key="' + svc + '"]');
      if (radio) radio.checked = true;
    }

    function validateField(f) {
      var wrap = f.closest(".field");
      var ok = f.checkValidity();
      if (wrap) wrap.classList.toggle("has-error", !ok);
      if (f.type !== "radio") f.setAttribute("aria-invalid", ok ? "false" : "true");
      return ok;
    }
    form.addEventListener("blur", function (e) {
      if (e.target.matches("input:not([type=radio]):not([type=hidden]), select, textarea") && e.target.value) validateField(e.target);
    }, true);
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", function (e) {
      var fields = form.querySelectorAll("input:not([type=hidden]), select, textarea");
      var first = null;
      fields.forEach(function (f) { if (f.closest(".hp")) return; if (!validateField(f) && !first) first = f; });
      if (first) { e.preventDefault(); first.focus(); return; }
      setSS("stc_submitted", formName);
      track(formName === "appraisal" ? "appraisal_form_submit" : "form_submit", { form_name: formName, service_interest: (form.querySelector('input[name="service_interest"]:checked') || {}).value || "" });
    });
  });

  // Thank-you page: count the conversion once
  if (document.body.hasAttribute("data-thank-you")) {
    var submitted = getSS("stc_submitted");
    if (submitted) {
      delSS("stc_submitted");
      var att = attribution();
      var fire = function () { track(submitted === "appraisal" ? "generate_lead" : "contact_submit", { form_name: submitted, landing_page: att.landing_page, source: att.utm_source || att.referrer || "direct", medium: att.utm_medium || "" }); };
      if (gaLoaded) setTimeout(fire, 300); else fire();
      var msg = document.querySelector("[data-thanks-" + submitted + "]");
      if (msg) { document.querySelectorAll("[data-thanks]").forEach(function (m) { m.hidden = true; }); msg.hidden = false; }
    }
  }

  /* ---------------- Our Homes filters ---------------- */
  var filterBar = document.querySelector("[data-filters]");
  if (filterBar) {
    var cards = document.querySelectorAll("[data-cats]");
    var empty = document.querySelector("[data-empty]");
    filterBar.addEventListener("click", function (e) {
      var b = e.target.closest("[data-filter]");
      if (!b) return;
      var cat = b.getAttribute("data-filter");
      filterBar.querySelectorAll("[data-filter]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var shown = 0;
      cards.forEach(function (c) {
        var match = cat === "all" || c.getAttribute("data-cats").split(" ").indexOf(cat) > -1;
        c.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      var status = document.querySelector("[data-filter-status]");
      if (status) status.textContent = shown + (shown === 1 ? " home" : " homes") + " shown";
      track("homes_filter", { filter: cat });
    });
  }
})();
