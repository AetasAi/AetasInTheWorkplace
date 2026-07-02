/* =====================================================================
   Aetas in the Workplace — Analytics
   --------------------------------------------------------------------
   Defers GA4 load until first user interaction (click, scroll, keypress).
   This eliminates unused JS on initial page load, improving mobile LCP.

   GDPR / PECR compliance: GA4 will only load if the visitor has
   accepted cookies via the cookie notice. Declining suppresses all
   analytics loading — including the 5-second fallback timer.

   GA4 is initialised immediately on interaction so no sessions are missed.
   anonymize_ip: true applied for GDPR best practice.

   ID: G-HNH05BKNFX (ITW-specific)
   ===================================================================== */
(function () {
  'use strict';

  var GA4_ID = 'G-HNH05BKNFX';
  var loaded = false;

  function hasConsent() {
    return localStorage.getItem('aetas-cookie-consent') === 'accepted';
  }

  function loadGA4() {
    if (loaded) return;
    if (!hasConsent()) return;   // ← GDPR gate: do nothing if not accepted
    loaded = true;

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA4_ID, { anonymize_ip: true });
  }

  // Only attach interaction listeners if consent already given (returning visitors)
  // or consent is not yet decided (first-time visitors — listeners fire but loadGA4
  // will check consent state at the moment of execution).
  // If consent is explicitly 'declined', we skip even attaching the listeners.
  if (localStorage.getItem('aetas-cookie-consent') !== 'declined') {
    ['scroll', 'click', 'keydown', 'touchstart'].forEach(function (evt) {
      window.addEventListener(evt, loadGA4, { once: true, passive: true });
    });

    // Fallback: load after 5 seconds — only fires if consent is accepted by then
    setTimeout(loadGA4, 5000);
  }
})();
