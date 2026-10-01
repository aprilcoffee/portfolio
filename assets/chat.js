/* "Ask about the work": sends the question (with the previous exchange as context) to the
   Cloudflare Worker (worker/) and shows the streamed answer, followed by suggested links
   that grow in. Only the latest exchange is shown; nothing is kept after a reload.
   Only text is rendered; https links become links. */
(function () {
  'use strict';
  var box = document.getElementById('ask');
  if (!box || !window.fetch || !window.TextDecoder) return;
  // The endpoint is stored reversed and base64-encoded so it is not sitting in the page
  // as a plain URL for scrapers. (The Worker itself checks origin, rate and Turnstile.)
  var endpoint;
  try { endpoint = atob(box.getAttribute('data-e').split('').reverse().join('')); } catch (e) { return; }
  var msgs = JSON.parse(box.getAttribute('data-msgs') || '{}');
  var log = box.querySelector('.ask-log');
  var form = box.querySelector('.ask-form');
  var input = form.querySelector('input');
  var btn = form.querySelector('button');
  var last = null;   // the previous exchange, sent along as context: [question, answer]
  var busy = false;

  // The ASCII GPU above the box: its blades alternate "+" and "x" (slowly at rest, fast
  // while an answer is written); the temperature climbs and the drawing's colour moves
  // from blue to red with it, then everything cools down.
  var gpu = box.querySelector('.ask-gpu'), temp = box.querySelector('.ask-gpu i');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var frame = 0, heat = 41, target = 41, spin = null;
  var COOL = [22, 140, 190], HOT = [228, 3, 46];
  function paint() {
    var t = Math.max(0, Math.min(1, (heat - 41) / (87 - 41)));
    var c = COOL.map(function (v, k) { return Math.round(v + (HOT[k] - v) * t); });
    if (gpu) gpu.style.color = 'rgb(' + c.join(',') + ')';
    if (temp) temp.textContent = Math.round(heat);
  }
  function tick() {
    frame = 1 - frame;
    if (gpu) gpu.className = 'ask-gpu f' + (frame + 1);
    heat += (target - heat) * (busy ? 0.05 : 0.03);
    paint();
  }
  function fanSpeed(ms) {
    clearInterval(spin);
    spin = (still && !busy) ? null : setInterval(tick, ms);
  }
  fanSpeed(520);

  // ---- optional Cloudflare Turnstile (invisible check), when a site key is configured ----
  var siteKey = box.getAttribute('data-turnstile');
  var widget = null, pendingToken = null;
  if (siteKey) {
    window.askTurnstileReady = function () {
      var holder = document.createElement('div');
      holder.className = 'ask-check';
      box.appendChild(holder);
      widget = window.turnstile.render(holder, {
        sitekey: siteKey, execution: 'execute', appearance: 'interaction-only',
        callback: function (t) { if (pendingToken) { var cb = pendingToken; pendingToken = null; cb(t); } },
        'error-callback': function () { if (pendingToken) { var cb = pendingToken; pendingToken = null; cb(''); } }
      });
    };
    var s = document.createElement('script');
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=askTurnstileReady';
    s.async = true;
    document.head.appendChild(s);
  }
  function token(cb) {
    if (!siteKey) return cb('');
    if (widget === null) return setTimeout(function () { token(cb); }, 200);
    pendingToken = cb;
    window.turnstile.reset(widget);
    window.turnstile.execute(widget);
  }

  // No dashes as punctuation in answers (the Worker asks for none; this catches the rest).
  // Number ranges such as 2016–2024 stay.
  function undash(text) {
    return text.replace(/\s*(?:—+|\s–\s)\s*/g, function (m, at) {
      if (!at) return '';
      return /[\u3000-\u9fff\uff00-\uffef]/.test(text.charAt(at - 1)) ? '，' : ', ';
    });
  }

  // Plain text only. Links come as checked buttons (suggest_links), so any URL the model
  // writes into the text is dropped: it may point to a page that does not exist.
  function render(el, text) {
    el.textContent = undash(text)
      .replace(/[ \t]*[(（]?\s*https?:\/\/[^\s<>()（）"'“”「」]*[)）]?/g, '')
      .replace(/[ \t]+([.,;:!?。，、；：！？])/g, '$1')
      .replace(/[:：]([.。])/g, '$1');
  }

  function link(href, label) {
    var a = document.createElement('a');
    a.href = href;
    a.textContent = label;
    if (a.protocol === 'https:' && a.hostname !== location.hostname) { a.target = '_blank'; a.rel = 'noopener'; }
    return a;
  }

  function line(cls, text) {
    var p = document.createElement('p');
    p.className = cls;
    p.textContent = text || '';
    log.appendChild(p);
    return p;
  }

  // Suggested links grow in one after another.
  function showLinks(links) {
    var wrap = document.createElement('div');
    wrap.className = 'ask-links';
    links.forEach(function (l, i) {
      var a = link(l.url, l.title);
      a.className = 'ask-link' + (a.target ? ' ext' : '');
      a.style.animationDelay = (0.12 + i * 0.14) + 's';
      wrap.appendChild(a);
    });
    log.appendChild(wrap);
  }

  function ask(q) {
    q = q.trim();
    if (!q || busy) return;
    busy = true;
    btn.disabled = true;
    // keep the box at least as tall as before, so hiding the example questions doesn't make it jump
    if (!box.classList.contains('open')) box.style.minHeight = box.offsetHeight + 'px';
    target = 87; fanSpeed(80);
    box.classList.add('open');
    log.textContent = '';                       // one exchange at a time
    line('ask-q', q);
    var out = line('ask-a pending');
    var text = '', links = null, problem = null;
    var history = (last ? [{ role: 'user', content: last[0] }, { role: 'assistant', content: last[1] }] : [])
      .concat([{ role: 'user', content: q }]);

    function finish(p) {
      problem = problem || p;
      if (typing) { clearInterval(typing); typing = null; }
      out.classList.remove('pending');
      if (problem) {
        out.classList.add('err');
        render(out, (problem === 'ask_refusal' || !text ? '' : text + '\n\n') + (msgs[problem] || msgs.ask_err));
      } else {
        last = [q, text];
      }
      if (links && links.length && problem !== 'ask_refusal') showLinks(links);
      busy = false;
      btn.disabled = false;
      target = 41; fanSpeed(still ? 160 : 520);
      if (still) setTimeout(function () { clearInterval(spin); if (gpu) gpu.className = 'ask-gpu'; }, 6000);
    }

    // Streamed text is revealed at a calm, typewriter pace (faster when a lot is waiting).
    var shown = '', typing = null, ended = null;
    function type() {
      if (shown.length < text.length) {
        var backlog = text.length - shown.length;
        shown = text.slice(0, shown.length + (backlog > 200 ? 4 : backlog > 60 ? 2 : 1));
        out.classList.remove('pending');
        render(out, shown);
        log.scrollTop = log.scrollHeight;
      } else if (ended) {
        clearInterval(typing); typing = null;
        var e = ended; ended = null; e();
      }
    }
    function startTyping() { if (!typing) typing = setInterval(type, 28); }

    function handle(lineText) {
      if (!lineText.trim()) return;
      var ev;
      try { ev = JSON.parse(lineText); } catch (e) { return; }
      if (typeof ev.t === 'string') {
        text += ev.t;
        startTyping();
      } else if (Array.isArray(ev.links)) {
        links = ev.links.filter(function (l) { return l && /^(https:|mailto:)/.test(l.url); });
      } else if (ev.error) {
        problem = ev.error === 'refusal' ? 'ask_refusal' : 'ask_err';
      }
    }

    token(function (t) {
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history, token: t, lang: document.documentElement.lang })
      }).then(function (res) {
        if (res.status === 429) return finish('ask_busy');
        if (!res.ok || !res.body) return finish('ask_err');
        var reader = res.body.getReader(), dec = new TextDecoder(), buf = '';
        function pump() {
          return reader.read().then(function (r) {
            if (r.done) {
              handle(buf);
              ended = function () { finish(text.trim() ? null : 'ask_err'); };
              startTyping();
              return;
            }
            buf += dec.decode(r.value, { stream: true });
            var parts = buf.split('\n');
            buf = parts.pop();
            parts.forEach(handle);
            return pump();
          });
        }
        return pump();
      }).catch(function () { finish('ask_err'); });
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = input.value;
    input.value = '';
    ask(q);
  });
  box.querySelector('.ask-chips').addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (b) ask(b.textContent);
  });
})();
