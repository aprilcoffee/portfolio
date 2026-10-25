(function () {
  'use strict';

  var DRAFT_KEY = 'ltc-draft';
  var GH_KEY = 'ltc-github';
  var main = document.getElementById('main');
  var POST_KEY = 'ltc-post-';   // + slug: unpublished Markdown body
  var DIRTY_KEY = 'ltc-posts-dirty';
  var D = null;          // site data being edited
  var tab = 'works';
  var sel = 0;           // selected work index
  var psel = 0;          // selected post index
  var wsel = 0;          // selected workshop index

  // ---------- storage ----------
  function save() {
    try { localStorage.setItem(DRAFT_KEY, JSON.stringify(D)); } catch (e) {}
    document.getElementById('saved').textContent = '草稿已存 ' + new Date().toLocaleTimeString();
  }
  function gh() {
    var def = { owner: 'aprilcoffee', repo: 'portfolio', branch: 'main', dir: '', token: '' };
    try { return Object.assign(def, JSON.parse(localStorage.getItem(GH_KEY)) || {}); } catch (e) { return def; }
  }
  function setGh(c) { try { localStorage.setItem(GH_KEY, JSON.stringify(c)); } catch (e) {} }

  // Post bodies live in posts/<slug>.md; edits are kept locally until published.
  function dirtyPosts() {
    try { return JSON.parse(localStorage.getItem(DIRTY_KEY)) || []; } catch (e) { return []; }
  }
  function setPostBody(slug, text) {
    try {
      localStorage.setItem(POST_KEY + slug, text);
      var d = dirtyPosts();
      if (d.indexOf(slug) < 0) { d.push(slug); localStorage.setItem(DIRTY_KEY, JSON.stringify(d)); }
    } catch (e) {}
    document.getElementById('saved').textContent = '草稿已存 ' + new Date().toLocaleTimeString();
  }
  function getPostBody(slug) {
    var local = null;
    try { local = localStorage.getItem(POST_KEY + slug); } catch (e) {}
    if (local != null) return Promise.resolve(local);
    return fetch('../posts/' + encodeURIComponent(slug) + '.md', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.text() : ''; });
  }
  function clearPostDrafts() {
    try {
      dirtyPosts().forEach(function (s) { localStorage.removeItem(POST_KEY + s); });
      localStorage.removeItem(DIRTY_KEY);
    } catch (e) {}
  }

  // ---------- tiny DOM helpers ----------
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'on') Object.keys(attrs.on).forEach(function (ev) { el.addEventListener(ev, attrs.on[ev]); });
      else if (k === 'text') el.textContent = attrs[k];
      else if (k in el && k !== 'list') el[k] = attrs[k];
      else el.setAttribute(k, attrs[k]);
    });
    [].concat(kids || []).forEach(function (c) {
      if (c != null) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return el;
  }
  function btn(text, fn, cls) { return h('button', { className: 'btn ' + (cls || ''), text: text, type: 'button', on: { click: fn } }); }

  // text input bound to obj[key]
  function field(label, obj, key, opts) {
    opts = opts || {};
    var input = opts.area
      ? h('textarea', { className: opts.cls || '', value: obj[key] || '' })
      : h('input', { type: 'text', value: obj[key] || '', placeholder: opts.ph || '' });
    input.addEventListener('input', function () { obj[key] = input.value; save(); if (opts.after) opts.after(); });
    return h('label', {}, [label, input]);
  }

  // list of short words edited as "a, b, c"
  function tagsField(label, obj, key) {
    var input = h('input', { type: 'text', value: (obj[key] || []).join(', ') });
    input.addEventListener('input', function () {
      obj[key] = input.value.split(',').map(function (x) { return x.trim(); }).filter(Boolean); save();
    });
    return h('label', {}, [label, input]);
  }

  // list of objects edited as "a | b | c" lines
  function lines(label, owner, key, cols, hint, cls) {
    function ser(arr) {
      return (arr || []).map(function (o) {
        return cols.map(function (c) { return o[c] || ''; }).join(' | ').replace(/( \| )+$/, '');
      }).join('\n');
    }
    function parse(txt) {
      return txt.split('\n').map(function (l) { return l.trim(); }).filter(Boolean).map(function (l) {
        var parts = l.split(' | '), o = {};
        cols.forEach(function (c, i) {
          // the last column takes whatever remains
          o[c] = (i === cols.length - 1 ? parts.slice(i).join(' | ') : parts[i] || '').trim();
        });
        return o;
      });
    }
    var ta = h('textarea', { className: 'lines ' + (cls || ''), value: ser(owner[key]) });
    ta.addEventListener('input', function () { owner[key] = parse(ta.value); save(); });
    return h('div', { className: 'stack', style: 'gap:4px' }, [
      h('label', {}, [label, ta]),
      hint ? h('p', { className: 'hint', style: 'margin:0', text: hint }) : null
    ]);
  }

  function bar(title, right) {
    return h('div', { className: 'bar' }, [h('h2', { text: title })].concat(right || []));
  }

  function resolve(url) {
    if (!url) return '';
    return /^(https?:)?\/\//.test(url) ? url : '../' + url.replace(/^\//, '');
  }

  // ---------- tabs ----------
  var tabs = {};

  tabs.works = function () {
    var works = D.works;
    if (sel >= works.length) sel = works.length - 1;

    var list = h('div', { className: 'items' }, works.map(function (w, i) {
      return h('div', {
        className: 'item' + (i === sel ? ' on' : '') + (w.hidden ? ' off' : ''),
        on: { click: function () { sel = i; render(); } }
      }, [h('span', { text: w.title || '(untitled)' }), h('span', { className: 'y', text: w.year || '' })]);
    }));

    var w = works[sel];
    var editor = w ? workForm(w) : h('p', { text: '還沒有作品。' });

    main.append(
      bar('作品 Works', [
        btn('+ 新增作品', function () {
          works.unshift({ slug: 'new-work-' + Date.now().toString(36), title: 'New work', title_zh: '', year: String(new Date().getFullYear()),
            type: '', materials: '', collaborators: '', cover: '', images: [], video: '', links: [], credits: '', text: '', hidden: true });
          sel = 0; save(); render();
        }, 'primary')
      ]),
      h('div', { className: 'split' }, [list, editor])
    );
  };

  function workForm(w) {
    var thumbs = h('div', { className: 'thumbs' });
    function drawThumbs() {
      thumbs.innerHTML = '';
      [w.cover].concat(w.images || []).filter(Boolean).map(function (u) { return u.replace(/\s*\|\s*wide\s*$/, ''); }).forEach(function (u) {
        thumbs.appendChild(h('img', { src: resolve(u), loading: 'lazy' }));
      });
    }
    drawThumbs();

    var imagesTa = h('textarea', { className: 'lines', value: (w.images || []).join('\n') });
    imagesTa.addEventListener('input', function () {
      w.images = imagesTa.value.split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
      save(); drawThumbs();
    });

    var upload = h('input', { type: 'file', accept: 'image/*', multiple: true, style: 'display:none' });
    var upStatus = h('span', { className: 'status' });
    upload.addEventListener('change', function () {
      var files = Array.prototype.slice.call(upload.files);
      if (!files.length) return;
      var c = gh();
      if (!c.token) { alert('請先到「發佈」頁填入 GitHub token。'); return; }
      var done = 0;
      upStatus.textContent = '上傳中…';
      files.reduce(function (p, f) {
        return p.then(function () {
          var name = f.name.toLowerCase().replace(/[^a-z0-9._-]+/g, '-');
          var rel = 'images/' + (w.slug || 'misc') + '/' + name;
          return readB64(f).then(function (b64) {
            return putFile(c, repoPath(c, rel), b64, 'Upload image ' + rel);
          }).then(function () {
            w.images = (w.images || []).concat(rel);
            imagesTa.value = w.images.join('\n');
            done++; upStatus.textContent = '已上傳 ' + done + '/' + files.length;
            save(); drawThumbs();
          });
        });
      }, Promise.resolve()).catch(function (e) { upStatus.textContent = '上傳失敗：' + e.message; });
      upload.value = '';
    });

    var i = D.works.indexOf(w);
    function move(d) {
      var j = i + d;
      if (j < 0 || j >= D.works.length) return;
      D.works.splice(j, 0, D.works.splice(i, 1)[0]);
      sel = j; save(); render();
    }

    var hidden = h('input', { type: 'checkbox', checked: !!w.hidden });
    hidden.addEventListener('change', function () { w.hidden = hidden.checked; save(); render(); });

    return h('div', { className: 'form' }, [
      h('div', { className: 'actions' }, [
        btn('↑ 上移', function () { move(-1); }, 'sm'),
        btn('↓ 下移', function () { move(1); }, 'sm'),
        h('a', { className: 'btn sm', href: '../preview.html?preview#/works/' + encodeURIComponent(w.slug), target: 'ltc-preview', text: '預覽 ↗', style: 'text-decoration:none' }),
        btn('刪除', function () {
          if (confirm('刪除「' + w.title + '」？')) { D.works.splice(i, 1); save(); render(); }
        }, 'sm danger'),
        h('label', { className: 'check', style: 'margin-left:auto' }, [hidden, '隱藏（不顯示在網站）'])
      ]),
      h('div', { className: 'row' }, [
        field('標題 Title', w, 'title', { after: function () { document.querySelector('.item.on span').textContent = w.title; } }),
        field('中文標題', w, 'title_zh')
      ]),
      h('div', { className: 'row' }, [
        field('網址代稱 slug（只用英文小寫與 -）', w, 'slug'),
        field('年份 Year', w, 'year')
      ]),
      h('div', { className: 'row' }, [field('狀態 Status（例：In development；留空＝不顯示）', w, 'status'), field('狀態 DE', w, 'status_de'), field('狀態 中文', w, 'status_zh')]),
      h('div', { className: 'row' }, [field('形式 Type', w, 'type'), field('媒材 Materials', w, 'materials')]),
      h('div', { className: 'row' }, [field('形式（德文 DE）', w, 'type_de'), field('媒材（德文 DE）', w, 'materials_de')]),
      h('div', { className: 'row' }, [field('形式（中文）', w, 'type_zh'), field('媒材（中文）', w, 'materials_zh')]),
      h('div', { className: 'row' }, [field('合作 With', w, 'collaborators'), field('影片 Vimeo / YouTube 網址', w, 'video')]),
      h('div', { className: 'row' }, [field('關鍵字一行 Keywords（作品列表標題下的小字，例：AI video installation）', w, 'kw'), field('關鍵字 DE', w, 'kw_de'), field('關鍵字 中文', w, 'kw_zh')]),
      tagsField('主題標籤 Topics（逗號分隔；顯示在作品頁並給搜尋引擎）', w, 'tags'),
      h('div', { className: 'row' }, [tagsField('主題標籤 DE（留空＝德文頁顯示英文）', w, 'tags_de'), tagsField('主題標籤 中文（留空＝中文頁顯示英文）', w, 'tags_zh')]),
      field('分享預覽小字 Summary（貼到臉書、LINE 時的說明，也是搜尋結果的描述；留空＝用說明文字開頭）', w, 'summary', { area: true }),
      h('div', { className: 'row' }, [field('分享小字 DE', w, 'summary_de', { area: true }), field('分享小字 中文', w, 'summary_zh', { area: true })]),
      field('說明文字 English（空一行＝分段；以「# 」開頭＝小標題）', w, 'text', { area: true, cls: 'tall' }),
      field('說明文字 Deutsch（留空＝德文頁顯示英文）', w, 'text_de', { area: true, cls: 'tall' }),
      field('說明文字 中文（留空＝中文頁顯示英文）', w, 'text_zh', { area: true, cls: 'tall' }),
      field('Credits（每行一條）', w, 'credits', { area: true }),
      lines('連結（每行：名稱 | 網址）', w, 'links', ['label', 'url']),
      field('封面圖（留空＝用第一張圖）', w, 'cover', { after: drawThumbs }),
      field('分享縮圖（貼到臉書時的圖；會自動裁成 1200×630 並加上標題；留空＝用封面）', w, 'share_image'),
      h('label', {}, ['圖片（每行一個網址或 images/… 路徑；第一張放大顯示，其餘兩欄；行尾加「 | wide」＝這張佔滿整寬，適合圖表與投影片）', imagesTa]),
      h('div', { className: 'actions' }, [btn('上傳圖片到 GitHub…', function () { upload.click(); }, 'sm'), upStatus, upload]),
      thumbs
    ]);
  }

  // photos are scaled down (long side 2400 px) and saved as JPEG before they go to GitHub, like scripts/compress-images.py
  function shrinkImage(file) {
    var plain = readB64(file).then(function (b64) { return { b64: b64, name: file.name.toLowerCase().replace(/[^a-z0-9._-]+/g, '-') }; });
    if (!/^image\/(jpeg|png|webp)$/.test(file.type)) return plain;  // gif, svg, heic…: upload as they are
    return new Promise(function (res) {
      var url = URL.createObjectURL(file), im = new Image();
      im.onload = function () {
        var k = Math.min(1, 2400 / Math.max(im.naturalWidth, im.naturalHeight));
        var c = document.createElement('canvas');
        c.width = Math.round(im.naturalWidth * k); c.height = Math.round(im.naturalHeight * k);
        var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(im, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        c.toBlob(function (b) {
          if (!b || b.size >= file.size && k === 1) return res(plain);
          readB64(b).then(function (b64) {
            res({ b64: b64, name: file.name.toLowerCase().replace(/\.[^.]*$/, '').replace(/[^a-z0-9._-]+/g, '-') + '.jpg' });
          });
        }, 'image/jpeg', 0.82);
      };
      im.onerror = function () { URL.revokeObjectURL(url); res(plain); };
      im.src = url;
    }).then(function (r) { return r; }, function () { return plain; });
  }

  tabs.workshops = function () {
    var shops = D.workshops = D.workshops || [];
    if (wsel >= shops.length) wsel = shops.length - 1;
    var list = h('div', { className: 'items' }, shops.map(function (x, i) {
      return h('div', {
        className: 'item' + (i === wsel ? ' on' : '') + (x.hidden ? ' off' : ''),
        on: { click: function () { wsel = i; render(); } }
      }, [h('span', { text: x.title || '(untitled)' }), h('span', { className: 'y', text: x.year || '' })]);
    }));
    var x = shops[wsel];
    main.append(
      bar('工作坊 Workshops（講座錄影在「講座錄影／評論」分頁）', [
        btn('+ 新增工作坊', function () {
          shops.unshift({ slug: 'workshop-' + Date.now().toString(36), title: 'New workshop', year: String(new Date().getFullYear()), summary: '', text: '', held: '', images: [], hidden: true });
          wsel = 0; save(); render();
        }, 'primary')
      ]),
      h('div', { className: 'split' }, [list, x ? workshopForm(x) : h('p', { text: '還沒有工作坊。按「新增工作坊」。' })])
    );
  };

  function workshopForm(x) {
    var i = D.workshops.indexOf(x);
    var thumbs = h('div', { className: 'thumbs' });
    function drawThumbs() {
      thumbs.innerHTML = '';
      (x.images || []).map(function (m) { return typeof m === 'string' ? m : m.src; }).filter(Boolean).forEach(function (u) {
        thumbs.appendChild(h('img', { src: resolve(u), loading: 'lazy' }));
      });
    }
    drawThumbs();
    // one line per image: path | alt | alt DE | alt 中文 (a bare path keeps the image without a description)
    function imgLine(m) {
      if (typeof m === 'string') return m;
      return [m.src, m.alt || '', m.alt_de || '', m.alt_zh || ''].join(' | ').replace(/( \| )+$/, '');
    }
    function parseImg(t) {
      var p = t.split(' | ').map(function (v) { return v.trim(); });
      if (p.length === 1) return p[0];
      var o = { src: p[0] };
      if (p[1]) o.alt = p[1];
      if (p[2]) o.alt_de = p[2];
      if (p[3]) o.alt_zh = p[3];
      return o;
    }
    var imagesTa = h('textarea', { className: 'lines tall', value: (x.images || []).map(imgLine).join('\n') });
    imagesTa.addEventListener('input', function () {
      x.images = imagesTa.value.split('\n').map(function (t) { return t.trim(); }).filter(Boolean).map(parseImg); save(); drawThumbs();
    });
    var upload = h('input', { type: 'file', accept: 'image/*', multiple: true, style: 'display:none' });
    var upStatus = h('span', { className: 'status' });
    upload.addEventListener('change', function () {
      var files = Array.prototype.slice.call(upload.files);
      if (!files.length) return;
      var c = gh();
      if (!c.token) { alert('請先到「發佈」頁填入 GitHub token。'); return; }
      var done = 0;
      upStatus.textContent = '壓縮並上傳中…';
      files.reduce(function (p, f) {
        return p.then(function () {
          return shrinkImage(f).then(function (r) {
            var rel = 'images/workshops/' + (x.slug || 'misc') + '/' + r.name;
            return putFile(c, repoPath(c, rel), r.b64, 'Upload image ' + rel).then(function () {
              x.images = (x.images || []).concat(rel);
              imagesTa.value = x.images.map(imgLine).join('\n');
              done++; upStatus.textContent = '已上傳 ' + done + '/' + files.length;
              save(); drawThumbs();
            });
          });
        });
      }, Promise.resolve()).catch(function (e) { upStatus.textContent = '上傳失敗：' + e.message; });
      upload.value = '';
    });
    var hidden = h('input', { type: 'checkbox', checked: !!x.hidden });
    hidden.addEventListener('change', function () { x.hidden = hidden.checked; save(); render(); });
    function move(d) {
      var j = i + d;
      if (j < 0 || j >= D.workshops.length) return;
      D.workshops.splice(j, 0, D.workshops.splice(i, 1)[0]);
      wsel = j; save(); render();
    }
    return h('div', { className: 'form' }, [
      h('div', { className: 'actions' }, [
        btn('↑ 上移', function () { move(-1); }, 'sm'),
        btn('↓ 下移', function () { move(1); }, 'sm'),
        btn('刪除', function () {
          if (confirm('刪除「' + x.title + '」？')) { D.workshops.splice(i, 1); save(); render(); }
        }, 'sm danger'),
        h('label', { className: 'check', style: 'margin-left:auto' }, [hidden, '隱藏（不顯示在網站）'])
      ]),
      h('div', { className: 'row' }, [
        field('標題 Title', x, 'title', { after: function () { document.querySelector('.item.on span').textContent = x.title; } }),
        field('標題 DE', x, 'title_de'), field('標題 中文', x, 'title_zh')
      ]),
      h('div', { className: 'row' }, [field('資料夾代稱 slug（上傳的圖片放在 images/workshops/<slug>/；只用英文小寫與 -）', x, 'slug'), field('年份 Year', x, 'year')]),
      field('合作 With（例：Leon-Etienne Kühr；留空＝不顯示）', x, 'with'),
      h('div', { className: 'row' }, [field('一句話介紹 Summary（列表卡片與頁首大字）', x, 'summary', { area: true }), field('一句話 DE', x, 'summary_de', { area: true }), field('一句話 中文', x, 'summary_zh', { area: true })]),
      field('說明文字 English（空一行＝分段；以「# 」開頭＝小標題）', x, 'text', { area: true, cls: 'tall' }),
      field('說明文字 Deutsch（留空＝德文頁顯示英文）', x, 'text_de', { area: true, cls: 'tall' }),
      field('說明文字 中文（留空＝中文頁顯示英文）', x, 'text_zh', { area: true, cls: 'tall' }),
      h('div', { className: 'row' }, [field('場次 Sessions（每行一場：日期 · 地點／主辦；顯示在頁面最下方）', x, 'held', { area: true }), field('場次 DE', x, 'held_de', { area: true }), field('場次 中文', x, 'held_zh', { area: true })]),
      h('label', {}, ['圖片（每行一張：路徑 | 圖片說明 | 說明 DE | 說明 中文；第一張是封面。圖片說明給看不到圖的人與搜尋引擎，描述畫面上有什麼）', imagesTa]),
      h('div', { className: 'actions' }, [btn('上傳圖片到 GitHub…（自動縮到長邊 2400px、轉 JPEG）', function () { upload.click(); }, 'sm'), upStatus, upload]),
      thumbs
    ]);
  }

  tabs.performances = function () {
    main.append(
      bar('表演紀錄 Performance archive'),
      h('div', { className: 'form' }, [
        lines('每行一支：標題 | 說明 | Vimeo/YouTube 網址 | 縮圖（選填）| 說明 DE | 說明 中文 | 年份 | 標題 DE | 標題 中文', D, 'performances', ['title', 'note', 'video', 'thumb', 'note_de', 'note_zh', 'year', 'title_de', 'title_zh'], '顯示在「作品」頁最下方的深色區塊，順序即網站上的順序。點擊會在新分頁開啟 Vimeo / YouTube。沒有縮圖時自動用 Vimeo / YouTube 的縮圖。標題通常不翻譯；只有需要區分時才填（例：Imaginary Landscape（表演版））。', 'tall')
      ])
    );
  };

  tabs.press = function () {
    main.append(
      bar('講座錄影／評論 Talks & texts'),
      h('div', { className: 'form' }, [
        lines('每行一筆：分類 | 標題 | 來源 | 日期 | 網址 | 說明 | 說明 DE | 說明 中文 | 截圖', D, 'press', ['group', 'title', 'outlet', 'date', 'url', 'note', 'note_de', 'note_zh', 'thumb'], '分類：watch＝講座錄影（顯示在「工作坊與講座」頁），read＝他人寫的評論與研究（顯示在「關於」的 CV 裡）。順序即網站上的順序；日期寫 2026 或 2026-05。截圖留空時，發佈後 GitHub 會自動抓錄影頁的預覽圖存到 images/talks/；要用自己的截圖就填 images/… 路徑。', 'tall')
      ])
    );
  };

  tabs.about = function () {
    var a = D.about;
    var box = h('div', { className: 'form' }, [field('簡介 Bio (English；也是關於頁的分享預覽小字)', a, 'bio', { area: true }),
      field('簡介 Bio (Deutsch)', a, 'bio_de', { area: true }), field('簡介 Bio（中文）', a, 'bio_zh', { area: true }),
      field('較長的介紹 About text (English；空一行＝分段；顯示在簡介下方)', a, 'text', { area: true, cls: 'tall' }),
      field('較長的介紹 DE', a, 'text_de', { area: true, cls: 'tall' }), field('較長的介紹 中文', a, 'text_zh', { area: true, cls: 'tall' })]);
    a.sections.forEach(function (sec, i) {
      box.appendChild(h('div', { className: 'card stack', style: 'gap:12px' }, [
        h('div', { className: 'actions' }, [
          h('div', { style: 'flex:1' }, [field('段落標題', sec, 'title')]),
          h('div', { style: 'flex:1' }, [field('DE', sec, 'title_de')]),
          h('div', { style: 'flex:1' }, [field('中文', sec, 'title_zh')]),
          btn('↑', function () { if (i) { a.sections.splice(i - 1, 0, a.sections.splice(i, 1)[0]); save(); render(); } }, 'sm'),
          btn('刪除', function () { if (confirm('刪除段落「' + sec.title + '」？')) { a.sections.splice(i, 1); save(); render(); } }, 'sm danger')
        ]),
        lines('每行：年份 | 內容 | 連結 | 中文 | DE | 日期 | 類型 | 預覽圖 | 圖片來源（圖片來源會在書寫列表顯示成「圖：…」；類型寫 talk 或 workshop，會在近期場次標成「演講」「工作坊」；日期也可以寫 TBA＝日期待定；後面幾欄都可留空；日期寫 2026-12-17，日期還沒到的講座會出現在「講座與工作坊」頁的「即將舉行」；最後一欄是預覽圖路徑，出版與寫作留空會自動抓）', sec, 'items', ['year', 'text', 'url', 'text_zh', 'text_de', 'date', 'kind', 'thumb', 'credit'], null, sec.items.length > 8 ? 'tall' : '')
      ]));
    });
    box.appendChild(h('div', {}, [btn('+ 新增段落', function () { a.sections.push({ title: 'New section', items: [] }); save(); render(); })]));
    main.append(bar('關於 / CV'), box);
  };

  tabs.writing = function () {
    var posts = D.writing = D.writing || [];
    if (psel >= posts.length) psel = posts.length - 1;
    var list = h('div', { className: 'items' }, posts.map(function (p, i) {
      return h('div', {
        className: 'item' + (i === psel ? ' on' : '') + (p.hidden ? ' off' : ''),
        on: { click: function () { psel = i; render(); } }
      }, [h('span', { text: p.title || '(untitled)' }), h('span', { className: 'y', text: (p.date || '').slice(0, 4) })]);
    }));
    var p = posts[psel];
    main.append(
      bar('文章 Blog', [
        btn('+ 新增文章', function () {
          var slug = 'post-' + Date.now().toString(36);
          posts.unshift({ slug: slug, date: new Date().toISOString().slice(0, 10), title: 'New post', category: 'works',
            cover: '', excerpt: '', lang: 'zh-Hant', hidden: true });
          setPostBody(slug, '');
          psel = 0; save(); render();
        }, 'primary')
      ]),
      h('div', { className: 'split' }, [list, p ? postForm(p) : h('p', { text: '還沒有文章。' })])
    );
  };

  function postForm(p) {
    var i = D.writing.indexOf(p);
    var body = h('textarea', { className: 'tall', style: 'min-height:520px;font-family:ui-monospace,Menlo,monospace;font-size:13px', value: '載入中…', disabled: true });
    getPostBody(p.slug).then(function (t) { body.value = t; body.disabled = false; });
    body.addEventListener('input', function () { setPostBody(p.slug, body.value); });

    var hidden = h('input', { type: 'checkbox', checked: !!p.hidden });
    hidden.addEventListener('change', function () { p.hidden = hidden.checked; save(); render(); });

    var slugField = field('網址代稱 slug（改了會變成新網址）', p, 'slug');
    slugField.querySelector('input').addEventListener('change', function () {
      // keep the body attached to the new slug
      if (!body.disabled) setPostBody(p.slug, body.value);
    });

    return h('div', { className: 'form' }, [
      h('div', { className: 'actions' }, [
        btn('↑ 上移', function () { if (i > 0) { D.writing.splice(i - 1, 0, D.writing.splice(i, 1)[0]); psel = i - 1; save(); render(); } }, 'sm'),
        btn('↓ 下移', function () { if (i < D.writing.length - 1) { D.writing.splice(i + 1, 0, D.writing.splice(i, 1)[0]); psel = i + 1; save(); render(); } }, 'sm'),
        h('a', { className: 'btn sm', href: '../preview.html?preview#/writing/' + encodeURIComponent(p.slug), target: 'ltc-preview', text: '預覽 ↗', style: 'text-decoration:none' }),
        btn('刪除', function () {
          if (confirm('從列表刪除「' + p.title + '」？（GitHub 上的 .md 檔會保留）')) { D.writing.splice(i, 1); save(); render(); }
        }, 'sm danger'),
        h('label', { className: 'check', style: 'margin-left:auto' }, [hidden, '隱藏'])
      ]),
      field('標題', p, 'title', { after: function () { document.querySelector('.item.on span').textContent = p.title; } }),
      h('div', { className: 'row' }, [slugField, field('日期 YYYY-MM-DD', p, 'date')]),
      h('div', { className: 'row' }, [field('分類（works / technique）', p, 'category'), field('語言（zh-Hant / en）', p, 'lang')]),
      field('摘要（列表與搜尋引擎用，一兩句）', p, 'excerpt', { area: true }),
      field('封面圖（分享縮圖）', p, 'cover'),
      h('label', {}, ['內文（Markdown：空一行分段、### 小標、![說明](圖片網址)、```程式碼```；單獨一行的影片網址會變成播放器）', body])
    ]);
  }

  tabs.friends = function () {
    main.append(bar('朋友 Friends'), h('div', { className: 'form' }, [
      lines('每行一位：名字 | 網址 | 圖片', D, 'friends', ['name', 'url', 'image'], null, 'tall')
    ]));
  };

  tabs.site = function () {
    var s = D.site;
    main.append(bar('網站設定'), h('div', { className: 'form' }, [
      h('div', { className: 'row' }, [field('名字', s, 'name'), field('中文名字', s, 'name_zh')]),
      field('網站描述（首頁的分享預覽小字與搜尋結果描述）', s, 'description', { area: true }),
      h('div', { className: 'row' }, [field('網站描述 DE', s, 'description_de', { area: true }), field('網站描述 中文', s, 'description_zh', { area: true })]),
      h('div', { className: 'row' }, [field('Email（側欄、Impressum、About）', s, 'email'), field('About 頁顯示的 Email（留空＝用左邊那個）', s, 'email_alt')]),
      field('ORCID iD（只填 0000-0000-0000-0000；顯示在 About 頁，留空＝不顯示）', s, 'orcid'),
      field('首頁圖片', s, 'home_image'),
      field('首頁大字（首頁下方的大字；空一行＝分段；留空＝留白）', s, 'home_text', { area: true }),
      h('div', { className: 'row' }, [field('首頁大字 DE', s, 'home_text_de', { area: true }), field('首頁大字 中文', s, 'home_text_zh', { area: true })]),
      field('簡介 Statement（搜尋引擎、分享、llms.txt 用，不顯示在首頁）', s, 'statement', { area: true }),
      h('div', { className: 'row' }, [field('Statement DE', s, 'statement_de', { area: true }), field('Statement 中文', s, 'statement_zh', { area: true })]),
      (function () {
        var ta = h('textarea', { value: (s.address || []).join('\n'), placeholder: 'Musterstraße 1\n12345 Berlin\nDeutschland' });
        ta.addEventListener('input', function () {
          s.address = ta.value.split('\n').map(function (x) { return x.trim(); }).filter(Boolean); save();
        });
        return h('label', {}, ['Impressum 地址（德國法規要求，每行一段）', ta]);
      })(),
      field('Google Analytics ID（G-…）', s, 'ga_id'),
      field('網站網址（搜尋引擎、分享連結用；換網域時改這裡）', s, 'base_url'),
      field('預設分享縮圖（直式 800×1200：臉書會顯示小圖＋多行小字；換圖請用新檔名，臉書才會重新抓）', s, 'og_image'),
      field('Facebook App ID（選填；只為了消除臉書 Sharing Debugger 的 fb:app_id 警告）', s, 'fb_app_id'),
      h('h3', { text: '分享預覽小字（貼到臉書、LINE 時的說明；留空＝用網站內建的句子）' }),
      h('div', { className: 'row' }, [field('首頁與關於頁的分享標題（手機上一定會顯示；瀏覽器分頁的標題不變）', s, 'share_title'), field('分享標題 DE', s, 'share_title_de'), field('分享標題 中文', s, 'share_title_zh')]),
      h('div', { className: 'row' }, [field('首頁與關於頁（留空＝首頁用網站描述、關於頁用簡介 bio）', s, 'share_about', { area: true }), field('首頁與關於頁 DE', s, 'share_about_de', { area: true }), field('首頁與關於頁 中文', s, 'share_about_zh', { area: true })]),
      h('div', { className: 'row' }, [field('作品頁', s, 'share_works', { area: true }), field('作品頁 DE', s, 'share_works_de', { area: true }), field('作品頁 中文', s, 'share_works_zh', { area: true })]),
      h('div', { className: 'row' }, [field('講座、工作坊與書寫頁', s, 'share_workshops', { area: true }), field('講座與工作坊 DE', s, 'share_workshops_de', { area: true }), field('講座與工作坊 中文', s, 'share_workshops_zh', { area: true })]),
      h('div', { className: 'row' }, [field('部落格頁', s, 'share_blog', { area: true }), field('部落格 DE', s, 'share_blog_de', { area: true }), field('部落格 中文', s, 'share_blog_zh', { area: true })]),
      h('div', { className: 'row' }, [field('朋友頁', s, 'share_friends', { area: true }), field('朋友頁 DE', s, 'share_friends_de', { area: true }), field('朋友頁 中文', s, 'share_friends_zh', { area: true })]),
      lines('側欄連結（每行：名稱 | 網址）', s, 'links', ['label', 'url']),
      lines('首頁背景藏的標題（每行：文字 | 連結）', s, 'hidden_links', ['text', 'url'], '游標靠近時以藍色浮現，點一下就前往連結。站內頁面寫 works/作品slug/、workshops/工作坊slug/、workshops/#talks（會自動加上 /de/、/zh/）；文章可直接貼完整網址。英文即可，太長的標題在手機上可能放不下。')
    ]));
  };

  tabs.publish = function () {
    var c = gh();
    var log = h('div', { className: 'log' });
    function say(t) { log.textContent = t; }

    main.append(bar('發佈 Publish'), h('div', { className: 'stack' }, [
      h('div', { className: 'card' }, [
        h('h3', { text: '方法 A：直接存到 GitHub（推薦）' }),
        h('p', { text: '需要一個只開放這個 repo「Contents: Read and write」權限的 fine-grained token（GitHub → Settings → Developer settings → Fine-grained tokens）。Token 只存在這台電腦的瀏覽器。' }),
        h('div', { className: 'form' }, [
          h('div', { className: 'row' }, [field('Owner', c, 'owner', { after: function () { setGh(c); } }), field('Repo', c, 'repo', { after: function () { setGh(c); } })]),
          h('div', { className: 'row' }, [field('Branch', c, 'branch', { after: function () { setGh(c); } }), field('網站資料夾（留空＝repo 根目錄）', c, 'dir', { after: function () { setGh(c); } })]),
          (function () {
            var t = h('input', { type: 'password', value: c.token, placeholder: 'github_pat_…' });
            t.addEventListener('input', function () { c.token = t.value.trim(); setGh(c); });
            return h('label', {}, ['Token', t]);
          })(),
          h('div', { className: 'actions' }, [
            btn('發佈到 GitHub', function () {
              if (!c.token) return say('請先填 token。');
              say('發佈中…');
              var dirty = dirtyPosts();
              var steps = dirty.reduce(function (pr, slug) {
                return pr.then(function () {
                  return getPostBody(slug).then(function (t) {
                    say('發佈文章 ' + slug + '…');
                    return putFile(c, repoPath(c, 'posts/' + slug + '.md'), b64utf8(t), 'Update post ' + slug);
                  });
                });
              }, Promise.resolve());
              steps.then(function () {
                return putFile(c, repoPath(c, 'data/site.json'), b64utf8(JSON.stringify(D, null, 2) + '\n'), 'Update site content');
              }).then(function () {
                clearPostDrafts();
                say('✓ 已發佈' + (dirty.length ? '（含 ' + dirty.length + ' 篇文章）' : '') + '。GitHub 會自動重建頁面，約 1–2 分鐘後上線。');
              }).catch(function (e) { say('✗ 失敗：' + e.message); });
            }, 'primary'),
            btn('從 GitHub 重新載入', function () {
              if (!confirm('用 GitHub 上的版本覆蓋目前草稿？')) return;
              say('載入中…');
              api(c, 'GET', repoPath(c, 'data/site.json'), null, true)
                .then(function (txt) { D = JSON.parse(txt); save(); say('✓ 已載入。'); })
                .catch(function (e) { say('✗ 失敗：' + e.message); });
            })
          ])
        ])
      ]),
      h('div', { className: 'card' }, [
        h('h3', { text: '方法 B：下載檔案手動上傳' }),
        h('p', { text: '下載 site.json，放到 repo 的 ' + repoPath(c, 'data/site.json') + ' 並 commit。文章內文不包含在內，請用方法 A 或直接改 posts/ 裡的 .md 檔。' }),
        h('div', { className: 'actions' }, [
          btn('下載 site.json', function () {
            var a = h('a', { href: URL.createObjectURL(new Blob([JSON.stringify(D, null, 2) + '\n'], { type: 'application/json' })), download: 'site.json' });
            document.body.appendChild(a); a.click(); a.remove();
          }),
          btn('捨棄草稿（重新讀取網站上的版本）', function () {
            if (!confirm('捨棄所有未發佈的修改？')) return;
            try { localStorage.removeItem(DRAFT_KEY); } catch (e) {}
            clearPostDrafts();
            location.reload();
          }, 'danger')
        ])
      ]),
      log
    ]));
  };

  // ---------- GitHub API ----------
  // path of a file inside the repository ('' = the site lives at the repository root)
  function repoPath(c, rel) {
    var d = (c.dir || '').replace(/^\/+|\/+$/g, '');
    return d ? d + '/' + rel : rel;
  }

  function api(c, method, path, body, raw) {
    var url = 'https://api.github.com/repos/' + c.owner + '/' + c.repo + '/contents/' +
      path.split('/').map(encodeURIComponent).join('/') + (method === 'GET' ? '?ref=' + encodeURIComponent(c.branch) : '');
    return fetch(url, {
      method: method,
      cache: 'no-store',  // a cached "404" or old sha makes the next upload fail (422 / 409)
      headers: {
        Authorization: 'Bearer ' + c.token,
        Accept: raw ? 'application/vnd.github.raw' : 'application/vnd.github+json'
      },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      if (r.status === 404 && method === 'GET' && !raw) return null;
      if (!r.ok) return r.text().then(function (t) { throw new Error(r.status + ' ' + t.slice(0, 200)); });
      return raw ? r.text() : r.json();
    });
  }

  // Create or replace a file. GitHub needs the current sha to replace a file; if it changed
  // in between (or was missing), fetch it again and retry once.
  function putFile(c, path, b64, message) {
    function attempt() {
      return api(c, 'GET', path).then(function (cur) {
        var body = { message: message, content: b64, branch: c.branch };
        if (cur && cur.sha) body.sha = cur.sha;
        return api(c, 'PUT', path, body);
      });
    }
    return attempt().catch(function (e) {
      if (/^(409|422) /.test(e.message)) return attempt();
      throw e;
    });
  }

  function b64utf8(s) {
    var bytes = new TextEncoder().encode(s), bin = '';
    for (var i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }

  function readB64(file) {
    return new Promise(function (res, rej) {
      var r = new FileReader();
      r.onload = function () { res(String(r.result).split(',')[1]); };
      r.onerror = rej;
      r.readAsDataURL(file);
    });
  }

  // ---------- shell ----------
  function render() {
    main.innerHTML = '';
    Array.prototype.forEach.call(document.querySelectorAll('.side [data-tab]'), function (b) {
      b.classList.toggle('on', b.getAttribute('data-tab') === tab);
    });
    tabs[tab]();
  }

  Array.prototype.forEach.call(document.querySelectorAll('.side [data-tab]'), function (b) {
    b.addEventListener('click', function () { tab = b.getAttribute('data-tab'); render(); window.scrollTo(0, 0); });
  });

  var draft = null;
  try { draft = JSON.parse(localStorage.getItem(DRAFT_KEY)); } catch (e) {}
  if (draft) {
    D = draft;
    document.getElementById('saved').textContent = '載入本機草稿';
    render();
  } else {
    fetch('../data/site.json', { cache: 'no-cache' })
      .then(function (r) { return r.json(); })
      .then(function (d) { D = d; render(); })
      .catch(function () { main.textContent = '無法讀取 ../data/site.json'; });
  }
})();
