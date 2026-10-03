/* Google Analytics 4, loaded on every page view (no consent banner).
   Advertising features stay off. A visitor can switch it off for their browser with an
   element carrying [data-ga-optout] (on the privacy page); the choice is kept in
   localStorage ('ga-consent' = 'denied', the same key the old banner used for "No").

   <script async src="/assets/analytics.js" data-ga="G-XXXX"></script> */
(function () {
  'use strict';
  var me = document.currentScript;
  var id = me && me.getAttribute('data-ga');
  if (!id || /[?&]preview\b/.test(location.search)) return;

  var KEY = 'ga-consent';
  var off = false;
  try { off = localStorage.getItem(KEY) === 'denied'; } catch (e) {}

  function label(b) {
    b.textContent = off ? b.getAttribute('data-on') : b.getAttribute('data-off');
  }
  function ready(fn) {
    if (document.body) fn(); else document.addEventListener('DOMContentLoaded', fn);
  }
  ready(function () {
    document.querySelectorAll('[data-ga-optout]').forEach(function (b) {
      label(b);
      b.addEventListener('click', function () {
        try { if (off) localStorage.removeItem(KEY); else localStorage.setItem(KEY, 'denied'); } catch (e) {}
        location.reload();
      });
    });
  });

  if (off) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'
  });
  window.gtag('js', new Date());
  window.gtag('config', id);
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
  document.head.appendChild(s);
})();
