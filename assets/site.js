(function () {
  'use strict';

  var me = document.currentScript;

  // Links from the first version of the site used #/works/slug style URLs.
  var m = location.hash.match(/^#\/(.*)$/);
  if (m) {
    var base = document.querySelector('.brand').getAttribute('href');
    location.replace(base + (m[1] ? m[1].replace(/\/?$/, '/') : ''));
    return;
  }

  var side = document.getElementById('side');
  var btn = document.getElementById('menuBtn');
  btn.addEventListener('click', function () {
    var open = side.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // German pages: the first time, say that parts of the German were translated with AI.
  var mt = document.getElementById('mtNote');
  if (mt) {
    var seen = false;
    try { seen = localStorage.getItem('mt-note') === 'seen'; } catch (e) {}
    if (!seen) {
      mt.hidden = false;
      mt.querySelector('button').addEventListener('click', function () {
        mt.hidden = true;
        try { localStorage.setItem('mt-note', 'seen'); } catch (e) {}
      });
    }
  }

  // Video thumbnails turn into the player on click.
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('.embed.lite');
    if (!el) return;
    var f = document.createElement('iframe');
    f.src = el.getAttribute('data-src');
    f.allow = 'autoplay; fullscreen; picture-in-picture';
    f.allowFullscreen = true;
    f.title = el.getAttribute('aria-label') || 'Video';
    var wrap = document.createElement('div');
    wrap.className = 'embed';
    wrap.appendChild(f);
    el.replaceWith(wrap);
  });

  // Images on work, workshop and blog pages open large on click; arrows / Esc to move and close.
  var pics = Array.prototype.filter.call(
    document.querySelectorAll('.plates figure img, .post-body figure img, .post-body p > img'),
    function (img) { return !img.closest('a'); });
  if (pics.length) {
    var box = document.createElement('div'), big = document.createElement('img'), at = 0, back = null;
    box.className = 'zoom';
    box.hidden = true;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.tabIndex = -1;
    box.innerHTML = '<button type="button" class="zoom-x" aria-label="Close">×</button>' +
      (pics.length > 1 ? '<button type="button" class="zoom-prev" aria-label="Previous">‹</button>' +
        '<button type="button" class="zoom-next" aria-label="Next">›</button>' : '');
    box.appendChild(big);
    document.body.appendChild(box);
    var show = function (i) {
      at = (i + pics.length) % pics.length;
      var img = pics[at];
      big.src = img.getAttribute('src');  // src is the full-size file; srcset only holds smaller copies
      big.alt = img.alt;
    };
    var close = function () {
      box.hidden = true;
      document.documentElement.classList.remove('zoomed');
      if (back) back.focus();
    };
    pics.forEach(function (img, i) {
      img.classList.add('zoomable');
      img.tabIndex = 0;
      var open = function () {
        back = img;
        show(i);
        box.hidden = false;
        document.documentElement.classList.add('zoomed');
        box.focus();
      };
      img.addEventListener('click', open);
      img.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
      });
    });
    box.addEventListener('click', function (e) {
      var t = e.target;
      if (t.classList.contains('zoom-prev')) show(at - 1);
      else if (t.classList.contains('zoom-next')) show(at + 1);
      else close();
    });
    document.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft' && pics.length > 1) show(at - 1);
      else if (e.key === 'ArrowRight' && pics.length > 1) show(at + 1);
    });
  }

  // p5.js effects: loaded only when a page has one, after everything else is done,
  // so they never compete with the content for bandwidth.
  if (!me || !document.querySelector('[data-effect]')) return;
  function load(src, cb) {
    var s = document.createElement('script');
    s.src = src;
    s.async = true;
    s.onload = cb;
    document.body.appendChild(s);
  }
  function start() {
    var idle = window.requestIdleCallback || function (f) { setTimeout(f, 200); };
    idle(function () {
      load(me.getAttribute('data-p5'), function () { load(me.getAttribute('data-effects')); });
    });
  }
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start);
})();
