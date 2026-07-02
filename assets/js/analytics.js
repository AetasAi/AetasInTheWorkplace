/* =====================================================================
   Aetas in the Workplace — Analytics
   --------------------------------------------------------------------
   Defers GA4 load until first user interaction (click, scroll, keypress).
   This eliminates unused JS on initial page load, improving mobile LCP.

   GA4 is initialised immediately on interaction so no sessions are missed.
   anonymize_ip: true applied for GDPR best practice.

   ID: G-HNH05BKNFX (ITW-specific)
   ===================================================================== */
(function () {
  'use strict';

  var GA4_ID = 'G-HNH05BKNFX';
  var loaded = false;

  function loadGA4() {
    if (loaded) return;
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

  // Load on first interaction — covers scroll, click, keypress, touch
  ['scroll', 'click', 'keydown', 'touchstart'].forEach(function (evt) {
    window.addEventListener(evt, loadGA4, { once: true, passive: true });
  });

  // Fallback: load after 5 seconds regardless (captures non-interacting visitors)
  setTimeout(loadGA4, 5000);
})();
