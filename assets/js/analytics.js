/* =====================================================================
   Aetas in the Workplace — Analytics
   --------------------------------------------------------------------
   Loads GA4 for site analytics.
   Cookiebot removed — site is B2B lead generation only.
   Review consent requirements before adding personal data collection.

   IDs:
     GA4: G-HNH05BKNFX (ITW-specific)
   ===================================================================== */
(function () {
  'use strict';

  var GA4_ID = 'G-HNH05BKNFX';

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA4_ID, { anonymize_ip: true });
})();
