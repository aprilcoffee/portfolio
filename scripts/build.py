#!/usr/bin/env python3
"""Generate the static site from data/site.json and posts/*.md.

Every page gets its own folder (works/<slug>/index.html, blog/<slug>/index.html, ...)
with full SEO tags, plus sitemap.xml and robots.txt. English is at the root, German
under de/ and Traditional Chinese under zh/ (the blog posts are not translated).

    pip install markdown
    python3 scripts/build.py
"""
import base64
import datetime
import hashlib
import html
import json
import os
import re
import runpy
import shutil
from urllib.parse import urlparse, urlsplit

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root
REPO = os.path.dirname(ROOT)
D = json.load(open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8"))
S = D["site"]
BASE = S["base_url"].rstrip("/")
PREFIX = urlparse(BASE).path.rstrip("/") + "/"  # "/" at liutingchun.com
NAV = ["works", "workshops", "about"]  # main menu
FOOT = ["blog", "friends"]  # small links at the bottom of the sidebar
SECTIONS = NAV + FOOT + ["performance", "press"]  # performance/ and press/ are now redirects

esc = lambda s: html.escape(str(s or ""), quote=True)
works = [w for w in D["works"] if not w.get("hidden")]
posts = [p for p in D.get("writing", []) if not p.get("hidden")]
post_slugs = {p["slug"] for p in posts}


# ---------- urls ----------
def url(path=""):
    return PREFIX + path


def abs_url(path=""):
    return BASE + "/" + path


def asset(u):
    return u if re.match(r"^(https?:)?//", u or "") else url((u or "").lstrip("/"))


def asset_abs(u):
    return u if re.match(r"^https?://", u or "") else abs_url((u or "").lstrip("/"))


# old liutingchun.com (Wix) paths -> new pages
OLD = {"": "", "/": "", "/cv": "about/", "/video-records": "works/#performances", "/friends": "friends/",
       "/blog": "blog/", "/works": "works/", "/blog/categories/works": "blog/",
       "/blog/categories/technique": "blog/"}
for w in D["works"]:
    for a in w.get("aliases", []):  # hidden works have no page: send their old URLs to the list
        OLD[a.rstrip("/")] = "works/" if w.get("hidden") else "works/%s/" % w["slug"]


def fix_link(href):
    """Point old Wix links at the new pages and drop tracking parameters."""
    try:
        p = urlsplit(href)
    except ValueError:
        return href
    if p.netloc.endswith("liutingchun.com"):
        path = p.path.rstrip("/")
        m = re.match(r"^/post/([^/]+)$", path)
        if m and m.group(1) in post_slugs:
            return url("blog/%s/" % m.group(1))
        if path in OLD:
            return url(LP[CUR[0]] + OLD[path])
    if "fbclid=" in (p.query or ""):
        q = "&".join(x for x in p.query.split("&") if not x.startswith("fbclid="))
        return p._replace(query=q).geturl()
    return href


TITLES = {}  # new page path -> title, filled in below


def a(href, text, cls=""):
    orig, href = href, fix_link(href)
    if href != orig and html.unescape(text) == orig and href in TITLES:
        text = esc(TITLES[href])  # a bare old URL as link text -> the page title
    ext = re.match(r"^https?://", href) and not href.startswith(BASE)
    return '<a href="%s"%s%s>%s</a>' % (esc(href), ' class="%s"' % cls if cls else "",
                                         ' target="_blank" rel="noopener"' if ext else "", text)


# ---------- media ----------
def img_src(u, w):
    m = re.match(r"^https://static\.wixstatic\.com/media/([^/?#]+)$", u or "")
    if not m or m.group(1).lower().endswith(".gif"):
        return asset(u)
    return "%s/v1/fit/w_%d,h_%d,q_85,enc_auto/%s" % (u, w, w, m.group(1))


# smaller copies of local photos (images/_w/<width>/…webp), made once with Pillow and kept in the repo,
# so phones and grids load an image of about the size they show; without Pillow the page uses the original only
RESP_W = (480, 960)
try:
    from PIL import Image as _PIL
except ImportError:
    _PIL = None
_sizes = {}


def srcset(u):
    rel = (u or "").lstrip("/")
    if _PIL is None or not re.match(r"^images/(?!_w/).+\.(jpe?g|png|webp)$", rel, re.I):
        return ""
    src = os.path.join(ROOT, rel)
    if rel not in _sizes:
        try:
            with _PIL.open(src) as im:
                _sizes[rel] = im.size[0]
        except OSError:
            _sizes[rel] = 0
    full = _sizes[rel]
    out = []
    for vw in RESP_W:
        if vw >= full * 0.85:
            break
        vrel = "images/_w/%d/%s.webp" % (vw, os.path.splitext(rel[len("images/"):])[0])
        vpath = os.path.join(ROOT, vrel)
        # a fresh checkout (GitHub Actions) gives every file a new date, so there only missing copies are made
        if not os.path.exists(vpath) or (os.path.getmtime(vpath) < os.path.getmtime(src) and not os.environ.get("GITHUB_ACTIONS")):
            try:
                with _PIL.open(src) as im:
                    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
                    im.thumbnail((vw, vw * 4), _PIL.LANCZOS)
                    os.makedirs(os.path.dirname(vpath), exist_ok=True)
                    im.save(vpath, "WEBP", quality=78, method=6)
            except OSError:
                break
        if os.path.getsize(vpath) > os.path.getsize(src) * 0.7:  # the original is already small: no gain
            continue
        out.append("%s %dw" % (url(vrel), vw))
    return ", ".join(out + ["%s %dw" % (url(rel), full)]) if out else ""


def img(u, w, alt="", cls="", lazy=True, sizes=None):
    fb = asset(u)
    ss = srcset(u)
    if ss and not sizes:  # how wide the image is shown: grid cards, half the plates, or a full plate
        sizes = ("(max-width: 800px) 100vw, 55vw" if w >= 1400 else "(max-width: 800px) 100vw, 30vw" if w >= 1000
                 else "(max-width: 800px) 100vw, (max-width: 1024px) 45vw, 30vw")
    return ('<img src="%s"%s alt="%s" loading="%s" decoding="async"%s '
            'onerror="if(this.src!==\'%s\')this.src=\'%s\'">') % (
        esc(img_src(u, w)), ' srcset="%s" sizes="%s"' % (esc(ss), sizes) if ss else "", esc(alt), "lazy" if lazy else "eager",
        ' class="%s"' % cls if cls else "", esc(fb), esc(fb))


def video_id(u):
    u = u or ""
    m = re.search(r"vimeo\.com/(?:video/)?(\d+)", u)
    if m:
        return "vimeo", m.group(1)
    m = re.search(r"(?:youtu\.be/|v=|embed/)([\w-]{11})", u)
    if m:
        return "youtube", m.group(1)
    if re.search(r"\.(mp4|mov|webm)(\?|$)", u):
        return "file", u
    return None


# real thumbnails recorded in site.json (works: video_thumb, performances: thumb), by video id
VIDEO_THUMBS = dict(S.get("video_thumbs", {}))  # extra ones, e.g. for videos in blog posts
for _it in D["works"] + D.get("performances", []):
    _v = video_id(_it.get("video"))
    _t = _it.get("video_thumb") or _it.get("thumb")
    if _v and _t:
        VIDEO_THUMBS.setdefault(_v[1], _t)


def embed(u, thumb="", title=""):
    v = video_id(u)
    if not v:
        return ""
    kind, vid = v
    if kind == "file":
        return '<div class="embed"><video controls preload="none" playsinline src="%s"></video></div>' % esc(asset(vid))
    src = ("https://player.vimeo.com/video/%s?dnt=1&autoplay=1" % vid if kind == "vimeo"
           else "https://www.youtube-nocookie.com/embed/%s?autoplay=1" % vid)
    thumb = thumb or VIDEO_THUMBS.get(vid)
    if not thumb:
        thumb = ("https://vumbnail.com/%s.jpg" % vid if kind == "vimeo"
                 else "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid)
    # A thumbnail that swaps itself for the player on click keeps pages light.
    return ('<button class="embed lite" type="button" data-src="%s" aria-label="Play video%s">'
            '%s<span class="play" aria-hidden="true"></span></button>') % (
        esc(src), esc(": " + title) if title else "", img(thumb, 1280, title))


def clip(c, title=""):
    """A video file kept in this repository (images/video/). Silent loops play by themselves,
    muted; anything with sound waits for the play button."""
    attrs = ('autoplay muted loop playsinline preload="auto"' if c.get("loop")
             else 'controls playsinline preload="none"')
    return '<figure class="clip"><video %s src="%s"%s aria-label="%s"></video></figure>' % (
        attrs, esc(asset(c["src"])), ' poster="%s"' % esc(asset(c["poster"])) if c.get("poster") else "", esc(title))


def cover_of(w):
    if w.get("cover"):
        return w["cover"]
    if w.get("images"):
        return w["images"][0]
    if w.get("video_thumb"):
        return w["video_thumb"]
    v = video_id(w.get("video"))
    if v and v[0] == "vimeo":
        return "https://vumbnail.com/%s.jpg" % v[1]
    if v and v[0] == "youtube":
        return "https://i.ytimg.com/vi/%s/hqdefault.jpg" % v[1]
    return ""


# ---------- text ----------
URL_RE = re.compile(r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+")


MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def linkify(text):
    """Bare URLs and Markdown links [label](url) in running text become links."""
    if MD_LINK.search(text or ""):
        out, last = [], 0
        for m in MD_LINK.finditer(text):
            out.append(linkify(text[last:m.start()]))
            out.append(a(m.group(2), esc(m.group(1))))
            last = m.end()
        out.append(linkify(text[last:]))
        return "".join(out)
    out, last = [], 0
    for m in URL_RE.finditer(text):
        u = m.group(0).rstrip(".,;:!?)")
        out.append(esc(text[last:m.start()]))
        out.append(a(u, esc(u)))
        last = m.start() + len(u)
    out.append(esc(text[last:]))
    return "".join(out)


def prose(text):
    """Work descriptions: blank line = paragraph, '# ' = heading, lines starting with '· ' = list."""
    parts = []
    for p in re.split(r"\n\s*\n", text or ""):
        p = p.strip()
        if not p:
            continue
        lines = p.split("\n")
        items = [l[2:].strip() for l in lines if l.startswith("· ")]
        if p.startswith("# "):
            parts.append("<h3>%s</h3>" % esc(p[2:]))
        elif items and len(items) == len([l for l in lines if l.startswith("· ")]) and lines[-1].startswith("· "):
            # lines starting with "· " are a list; a term before the first colon is set in bold
            intro = "\n".join(l for l in lines if not l.startswith("· "))
            lis = "".join("<li>%s</li>" % (re.sub(r"^([^:：]{1,24}[:：])", r"<strong>\1</strong>", linkify(i))) for i in items)
            parts.append(("<p>%s</p>" % linkify(intro).replace("\n", "<br>") if intro else "") + '<ul class="dots">%s</ul>' % lis)
        else:
            parts.append("<p>%s</p>" % linkify(p).replace("\n", "<br>"))
    return "".join(parts)


# a URL in running text that isn't already inside Markdown link syntax
BARE_URL_RE = re.compile(r"(?<![(<\"'\[])" + URL_RE.pattern)


def autolink(m):
    u = m.group(0)
    core = u.rstrip(".,;:!?)")
    return "<%s>%s" % (core, u[len(core):])


def post_html(src):
    """Blog posts are Markdown; bare video URLs on their own line become players."""
    lines, fenced = [], False
    for line in src.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced:
            s = line.strip()
            if URL_RE.fullmatch(s) or re.fullmatch(r"\S+\.(mp4|mov|webm)", s):
                line = ("\n" + embed(s) + "\n") if video_id(s) else "<%s>" % s
            else:
                line = BARE_URL_RE.sub(autolink, line)
        lines.append(line)
    h = markdown.markdown("\n".join(lines), extensions=["fenced_code", "nl2br", "sane_lists"])
    # images -> figures (alt text is the caption)
    h = re.sub(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"\s*/?>\s*</p>',
               lambda m: "<figure>%s%s</figure>" % (
                   img(html.unescape(m.group(2)), 1600, html.unescape(m.group(1))),
                   "<figcaption>%s</figcaption>" % m.group(1) if m.group(1) else ""), h)
    h = re.sub(r'<img alt="([^"]*)" src="([^"]+)"\s*/?>',
               lambda m: img(html.unescape(m.group(2)), 1600, html.unescape(m.group(1))), h)
    # links: old site -> new pages, external -> new tab
    h = re.sub(r'<a href="([^"]+)">(.*?)</a>', lambda m: a(html.unescape(m.group(1)), m.group(2)), h)
    return h


def read_post(slug):
    p = os.path.join(ROOT, "posts", slug + ".md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def summary(text, n=160, words=False):
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)|```.*?```", " ", text or "", flags=re.S)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"https?://\S+|[#>*_`]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= n:
        return t
    cut = t[:n - 1]
    if words and " " in cut:  # do not end in the middle of a word
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "…"


# ---------- languages ----------
# English at the site root, German under de/, Traditional Chinese under zh/.
# The blog posts themselves are not translated: they live once under blog/<slug>/.
LANGS = ["en", "de", "zh"]
# languages that are built but not shown: every page of theirs forwards to the English one, and they are left out of
# the language switch, hreflang and the sitemap (German is hidden until its translation has been reviewed)
HIDDEN_LANGS = {"de"}
SHOWN_LANGS = [l for l in LANGS if l not in HIDDEN_LANGS]
LP = {"en": "", "de": "de/", "zh": "zh/"}
HREFLANG = {"en": "en", "de": "de", "zh": "zh-Hant"}
LOCALE = {"en": "en_US", "de": "de_DE", "zh": "zh_TW"}
LANG_NAME = {"en": "EN", "de": "DE", "zh": "中文"}

UI = {
    "en": {
        "nav": {"works": "Works", "workshops": "Talks & Workshops", "about": "About", "blog": "Blog (archived)", "friends": "Friends"},
        "menu": "Menu", "more": "More", "language": "Language", "privacy": "Privacy",
        "selected": "Selected works", "all_works": "All works (%d) →",
        "works_lead": "Installations, performances, internet art and artistic research, %s–%s.",
        "works_desc": "Selected works by %s, %s–%s: installations, performances, internet art and artistic research on AI.",
        "Topics": "Topics", "Email": "Email", "contact_note": "I host workshops about local AI usage, embedding practice, and understanding biases in AI models. Workshop and lecture requests: please get in touch by email.", "work_by": "%s by %s, %s.",
        "tags": {"works": "Critical AI, generative art, artistic research, cybernetics, internet art, audio-visual performance",
                 "about": "Critical AI, generative art, artistic research, cybernetics, internet art, audio-visual performance",
                 "workshops": "local AI, embedding practice, AI bias, workshops, talks, talk recordings"},
        "sitemap": "Site map", "sitemap_lead": "Every page of this website.",
        "sitemap_desc": "Site map of the website of %s: works and performances, talks and workshops, about, blog.",
        "Year": "Year", "Status": "Status", "Type": "Type", "Materials": "Materials", "With": "With", "Link": "Link",
        "work_desc": "%s (%s), %s by %s.", "work": "work", "work_with": "with %s", "show_all": "Show all (%d)", "event": "Event page", "held": "Sessions", "workshop": "Workshop",
        "perf_title": "Performance archive",
        "watch": "Watch on %s ↗",
        "about": "About",
        "blog_title": "Blog Archive",
        "blog_lead": "Notes on works, and technical write-ups on Raspberry Pi, Processing and Python. The posts are written in Mandarin.",
        "blog_desc": "Blog archive of %s: notes on artworks and technical write-ups on Raspberry Pi, Processing and Python.",
        "friends_desc": "Friends and fellow artists of %s.",
        "workshops_lead": "Workshops I offer: using AI locally on your own computer, working hands-on with embeddings, and seeing the biases inside AI models. They work for anyone, from people who have never written code to artists, companies and scholars. Talk recordings below.",
        "workshops_desc": "Workshops and talks by %s on local AI usage, embedding practice and biases in AI models, with talk recordings.",
        "workshops_ask": "Workshop and lecture requests: please get in touch by email.",
        "press_groups": {"watch": "Talk recordings", "read": "Cited and discussed"},
        "Date": "Date", "Category": "Category",
        "ask": "Ask about my work", "ask_ph": "Ask me anything", "ask_btn": "Ask",
        "ask_ex": ["What is Latent Heat Generation about?", "Why can “giraffe” be spelled in 51 ways?", "Which of your works deal with AI?", "What are you working on now?"],
        "ask_note": "caution: AI may create random correlations",
        "ask_more": "Privacy",
        "ask_err": "Sorry, that didn’t work. Please try again in a moment, or write to %s.",
        "ask_busy": "Too many questions right now. Please wait a minute.",
        "ask_refusal": "I can’t answer that here, but ask me anything about my work.",
    },
    "de": {
        "nav": {"works": "Arbeiten", "workshops": "Vorträge & Workshops", "about": "Über mich", "blog": "Blog (archiviert)", "friends": "Freunde"},
        "menu": "Menü", "more": "Mehr", "language": "Sprache", "privacy": "Datenschutz",
        "selected": "Ausgewählte Arbeiten", "all_works": "Alle Arbeiten (%d) →",
        "works_lead": "Installationen, Performances, Netzkunst und künstlerische Forschung, %s–%s.",
        "works_desc": "Ausgewählte Arbeiten von %s, %s–%s: Installationen, Performances, Netzkunst und künstlerische Forschung zu KI.",
        "Topics": "Themen", "Email": "E-Mail", "contact_note": "Ich gebe Workshops zu lokaler KI-Nutzung, Embedding-Praxis und zum Verständnis von Biases in KI-Modellen. Anfragen für Workshops und Vorträge bitte per E-Mail.", "work_by": "%s von %s, %s.",
        "tags": {"works": "Kritische KI, generative Kunst, künstlerische Forschung, Kybernetik, Netzkunst, audiovisuelle Performance",
                 "about": "Kritische KI, generative Kunst, künstlerische Forschung, Kybernetik, Netzkunst, audiovisuelle Performance",
                 "workshops": "lokale KI, Embedding-Praxis, KI-Bias, Workshops, Vorträge, Vortragsaufzeichnungen"},
        "sitemap": "Seitenübersicht", "sitemap_lead": "Alle Seiten dieser Website.",
        "sitemap_desc": "Seitenübersicht der Website von %s: Arbeiten und Performances, Vorträge und Workshops, Über mich, Blog.",
        "Year": "Jahr", "Status": "Status", "Type": "Art", "Materials": "Material", "With": "Mit", "Link": "Link",
        "work_desc": "%s (%s), %s von %s.", "work": "Arbeit", "work_with": "mit %s", "show_all": "Alle anzeigen (%d)", "event": "Veranstaltung", "held": "Termine", "workshop": "Workshop",
        "perf_title": "Performance-Archiv",
        "watch": "Auf %s ansehen ↗",
        "about": "Über mich",
        "blog_title": "Blog-Archiv",
        "blog_lead": "Notizen zu Arbeiten und technische Anleitungen zu Raspberry Pi, Processing und Python. Die Beiträge sind auf Chinesisch (Mandarin) verfasst.",
        "blog_desc": "Blog-Archiv von %s: Notizen zu Arbeiten und technische Anleitungen zu Raspberry Pi, Processing und Python.",
        "friends_desc": "Freund*innen und befreundete Künstler*innen von %s.",
        "workshops_lead": "Workshops, die ich anbiete: KI lokal auf dem eigenen Rechner nutzen, praktisch mit Embeddings arbeiten und die Biases in KI-Modellen sichtbar machen. Sie eignen sich für alle, von Menschen ohne Programmiererfahrung bis zu Künstler*innen, Unternehmen und Wissenschaftler*innen. Darunter Aufzeichnungen von Vorträgen.",
        "workshops_desc": "Workshops und Vorträge von %s zu lokaler KI-Anwendung, Embedding-Praxis und Biases in KI-Modellen, mit Vortragsaufzeichnungen.",
        "workshops_ask": "Anfragen für Workshops und Vorträge richten Sie bitte per E-Mail an mich.",
        "press_groups": {"watch": "Vortragsaufzeichnungen", "read": "Zitiert und besprochen"},
        "Date": "Datum", "Category": "Kategorie",
        "ask": "Fragen Sie zu meiner Arbeit", "ask_ph": "Fragen Sie mich alles", "ask_btn": "Fragen",
        "ask_ex": ["Worum geht es in Latent Heat Generation?", "Warum lässt sich „giraffe“ auf 51 Arten schreiben?", "Welche Ihrer Arbeiten beschäftigen sich mit KI?", "Woran arbeiten Sie gerade?"],
        "ask_note": "Achtung: KI kann zufällige Zusammenhänge erzeugen · %s",
        "ask_more": "Datenschutz",
        "ask_err": "Das hat leider nicht geklappt. Bitte gleich noch einmal versuchen oder an %s schreiben.",
        "ask_busy": "Gerade kommen zu viele Fragen. Bitte eine Minute warten.",
        "ask_refusal": "Darauf kann ich hier nicht antworten. Fragen Sie mich gern zu meiner Arbeit.",
    },
    "zh": {
        "nav": {"works": "創作計畫", "workshops": "講座與工作坊", "about": "關於", "blog": "部落格（封存）", "friends": "朋友"},
        "menu": "選單", "more": "更多", "language": "語言", "privacy": "隱私權",
        "selected": "精選作品", "all_works": "全部作品（%d）→",
        "works_lead": "裝置、表演、網路藝術與藝術研究，%s–%s。",
        "works_desc": "%s的精選作品，%s–%s：裝置、表演、網路藝術，以及關於人工智慧的藝術研究。",
        "Topics": "主題", "Email": "信箱", "contact_note": "工作坊主題包含：在自己的電腦上使用人工智慧、嵌入向量實作，以及辨識人工智慧模型中的偏見。工作坊與講座邀約，歡迎來信。", "work_by": "%s，%s，%s。",
        "tags": {"works": "批判性人工智慧、生成藝術、藝術研究、模控論、網路藝術、音像演出",
                 "about": "批判性人工智慧、生成藝術、藝術研究、模控論、網路藝術、音像演出",
                 "workshops": "本地端人工智慧、嵌入向量實作、人工智慧偏見、工作坊、講座、講座錄影"},
        "sitemap": "網站地圖", "sitemap_lead": "這個網站的所有頁面。",
        "sitemap_desc": "%s網站的網站地圖：創作計畫與表演、講座與工作坊、關於、部落格。",
        "Year": "年份", "Status": "狀態", "Type": "類型", "Materials": "媒材", "With": "合作", "Link": "連結",
        "work_desc": "%s（%s），%s，%s。", "work": "作品", "work_with": "與 %s 合作", "show_all": "顯示全部（%d）", "event": "活動頁面", "held": "場次", "workshop": "工作坊",
        "perf_title": "表演紀錄",
        "watch": "在 %s 觀看 ↗",
        "about": "關於",
        "blog_title": "部落格封存",
        "blog_lead": "作品筆記，以及 Raspberry Pi、Processing 與 Python 的技術文章。",
        "blog_desc": "%s的部落格文章彙整：作品筆記，以及 Raspberry Pi、Processing 與 Python 技術文章。",
        "friends_desc": "%s的朋友、合作夥伴與藝術家夥伴，以及他們的作品網站連結。",
        "workshops_lead": "工作坊內容包含：在自己的電腦上使用人工智慧、動手操作嵌入向量，以及辨識人工智慧模型中的偏見。沒有寫程式經驗的人、藝術家、企業與研究者皆可參加。頁面下方為講座錄影。",
        "workshops_desc": "%s的講座與工作坊：講座錄影，以及在自己的電腦上使用人工智慧、嵌入向量實作與人工智慧模型偏見的工作坊。",
        "workshops_ask": "工作坊與講座邀約，歡迎來信。",
        "press_groups": {"watch": "講座錄影", "read": "引用與討論"},
        "Date": "日期", "Category": "分類",
        "ask": "關於我的作品，問問我", "ask_ph": "問我任何事", "ask_btn": "提問",
        "ask_ex": ["《Latent Heat Generation》在談什麼？", "為什麼「giraffe」可以有 51 種拼法？", "你有哪些作品跟人工智慧有關？", "你現在在做什麼？"],
        "ask_note": "注意：人工智慧可能產生隨機的關聯性",
        "ask_more": "隱私權",
        "ask_err": "抱歉，暫時無法回答。請稍後再試，或寫信至 %s。",
        "ask_busy": "目前提問太多，請稍候一分鐘。",
        "ask_refusal": "這個問題我沒辦法在這裡回答，歡迎問我作品相關的問題。",
    },
}
CUR = ["en"]  # language of the page being built; fix_link keeps visitors in it


def tr(obj, key, lang):
    """obj[key + '_de'] / obj[key + '_zh'] with the English field as fallback."""
    return (obj.get("%s_%s" % (key, lang)) if lang != "en" else None) or obj.get(key)


def lname(lang):
    return S.get("name_zh") if lang == "zh" and S.get("name_zh") else S["name"]


# ---------- layout ----------
_versions = {}


def versioned(path):
    """URL of a file in assets/ with ?v=<content hash>, so browsers fetch it again when it changes."""
    if path not in _versions:
        import hashlib
        try:
            with open(os.path.join(ROOT, path), "rb") as f:
                _versions[path] = hashlib.md5(f.read()).hexdigest()[:8]
        except OSError:  # e.g. the admin's in-browser preview, which has no assets/ folder
            _versions[path] = ""
    return "%s?v=%s" % (url(path), _versions[path]) if _versions[path] else url(path)


def idx(n):
    return ""  # numbering removed from the design; kept as a hook


def breadcrumbs(path, title, lang):
    """schema.org BreadcrumbList for a page: Home > section > page (none for the home page)."""
    parts = [x for x in path.strip("/").split("/") if x]
    if parts and parts[0] in ("de", "zh"):
        parts = parts[1:]
    if not parts:
        return None
    items = [(S["name"], abs_url(LP[lang]))]
    for i, seg in enumerate(parts):
        name = title if i == len(parts) - 1 else UI[lang]["nav"].get(seg, seg)
        items.append((name, abs_url(LP[lang] + "/".join(parts[:i + 1]) + "/")))
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": n + 1, "name": nm, "item": it}
                                for n, (nm, it) in enumerate(items)]}


def layout(path, title, desc, body, image=None, og_type="website", lang="en", ld=None, full=False, section="",
           alts=None, content_lang=None):
    """lang: language of the interface; content_lang: of the page text (a Chinese post in the English frame);
    alts: {lang: path} of the same page in the other languages (hreflang + language switch)."""
    u = UI[lang]
    page_title = "%s — %s" % (title, S["name"]) if title else "%s %s" % (S["name"], S.get("name_zh", ""))
    canonical = abs_url(path)
    image = asset_abs(image or S.get("og_image") or "")
    nav = "".join('<a href="%s"%s><span>%s</span></a>' % (
        url(LP[lang] + s + "/"), ' class="on" aria-current="page"' if s == section else "", esc(u["nav"][s]))
        for s in NAV)
    foot_nav = "".join('<a href="%s"%s>%s</a>' % (
        url(LP[lang] + s + "/"), ' class="on" aria-current="page"' if s == section else "", esc(u["nav"][s])) for s in FOOT)
    switch = "".join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
        url(alts[l] if alts else LP[l] + (section + "/" if section else "")), HREFLANG[l], HREFLANG[l],
        ' class="on" aria-current="true"' if l == lang else "", LANG_NAME[l]) for l in SHOWN_LANGS)
    hreflang = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (HREFLANG[l], esc(abs_url(p)))
                       for l, p in (alts or {}).items())
    if alts:
        hreflang += '<link rel="alternate" hreflang="x-default" href="%s">\n' % esc(abs_url(alts["en"]))
    links = "".join(a(l["url"], esc(l["label"])) for l in S.get("links", []))
    lds = ([ld] if isinstance(ld, dict) else list(ld or [])) + [b for b in [breadcrumbs(path, title, lang)] if b]
    ld_tag = ('<script type="application/ld+json">%s</script>' % json.dumps(lds[0] if len(lds) == 1 else lds, ensure_ascii=False)) if lds else ""
    ga = ('<script async src="%s" data-ga="%s"></script>' % (versioned("assets/analytics.js"), esc(S["ga_id"]))
          if S.get("ga_id") else "")
    cl = content_lang or HREFLANG[lang]
    return """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="author" content="{name}">
<link rel="canonical" href="{c}">
{hreflang}<meta property="og:site_name" content="{name}">
<meta property="og:locale" content="{locale}">
<meta property="og:type" content="{ogt}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{c}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{icon}" sizes="32x32" type="image/png">
<link rel="icon" href="{ico}" sizes="any">
<link rel="apple-touch-icon" href="{touch}">
<link rel="manifest" href="{manifest}">
<link rel="alternate" type="application/rss+xml" title="{name} — Blog" href="{feed}">
{ga}
<link rel="preload" href="{font_r}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{font_b}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{fonts}" media="print" onload="this.media='all'"><noscript><link rel="stylesheet" href="{fonts}"></noscript>
<link rel="stylesheet" href="{fonts_g}" media="print" onload="this.media='all'"><noscript><link rel="stylesheet" href="{fonts_g}"></noscript>
<link rel="stylesheet" href="{css}">
{ld}
</head>
<body>
<aside class="side" id="side"{side_lang}>
  <div class="side-head">
    <a class="brand" href="{home}"><span class="brand-en">{name}</span><span class="brand-zh" lang="zh-Hant">{zh}</span></a>
    <button class="menu-btn" id="menuBtn" aria-label="{menu}" aria-expanded="false">{menu}</button>
  </div>
  <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
  <nav class="langs" aria-label="{language}">{switch}</nav>
  <div class="side-foot">
    <div class="signal" data-effect="signal" aria-hidden="true"></div>
    <nav class="foot-nav" aria-label="{more}">{foot_nav}</nav>
    <div><a href="mailto:{email}">{email}</a></div>
    <div class="links">{links}</div>
    <div>© {year} {name}</div>
    <div class="legal"><a href="{imp}" lang="de">Impressum</a><a href="{dsg}">{privacy}</a></div>
  </div>
</aside>
<main class="main{full}" id="main">
{body}
</main>
<script src="{js}" data-p5="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.4/p5.min.js" data-effects="{fx}" defer></script>
</body>
</html>
""".format(lang=cl, side_lang=' lang="%s"' % HREFLANG[lang] if cl != HREFLANG[lang] else "",
           locale=LOCALE[lang] if not content_lang else ("zh_TW" if content_lang.startswith("zh") else LOCALE[lang]),
           t=esc(page_title), d=esc(desc or tr(S, "description", lang)), name=esc(S["name"]), zh=esc(S.get("name_zh", "")),
           c=esc(canonical), hreflang=hreflang, ogt=og_type, img=esc(image), icon=url("assets/favicon-32.png"), ico=url("favicon.ico"), touch=url("assets/apple-touch-icon.png"), manifest=url("site.webmanifest"),
           css=versioned("assets/style.css"), fonts=versioned("assets/fonts/fonts.css"), fonts_g=versioned("assets/fonts/fonts-google.css"), font_r=url("assets/fonts/Minipax-Regular.woff2"), font_b=url("assets/fonts/Minipax-Bold.woff2"), js=versioned("assets/site.js"), fx=versioned("assets/effects.js"), feed=url("blog/feed.xml"),
           ga=ga, ld=ld_tag, home=url(LP[lang]), imp=url("impressum/"), dsg=url("datenschutz/"), nav=nav, foot_nav=foot_nav, more=u["more"], switch=switch,
           menu=u["menu"], language=u["language"], privacy=u["privacy"], email=esc(S["email"]), links=links,
           year=datetime.date.today().year, full=" full" if full else "", body=body)


def person(lang):
    p = {"@context": "https://schema.org", "@type": "Person", "name": S["name"],
         "alternateName": [n for n in dict.fromkeys([S.get("name_zh", ""), "Liu Ting-Chun", "Ting Chun Liu", "劉庭均"]) if n], "url": abs_url(LP[lang]),
         "email": "mailto:" + S["email"], "jobTitle": tr(S, "job_title", lang) or "Critical AI Artist",
         "description": tr(S, "statement", lang) or tr(S, "description", lang),
         "knowsAbout": S.get("knows_about", []),
         "hasOccupation": [{"@type": "Occupation", "name": o} for o in S.get("occupations", [])],
         "sameAs": [l["url"] for l in S.get("links", [])] + (["https://orcid.org/" + S["orcid"]] if S.get("orcid") else [])}
    p.update(S.get("person_extra", {}))
    return p


def pager(items, i, base, label, noun):
    prev = items[i - 1] if i > 0 else None
    nxt = items[i + 1] if i < len(items) - 1 else None
    one = lambda it, n, arrow: ('<a href="%s"><span class="mono">%s</span><span class="t">%s</span></a>' % (
        url(base % it["slug"]), arrow, esc(it[label])))
    return '<nav class="pager" aria-label="%s">%s%s</nav>' % (
        noun, one(prev, i, "←") if prev else "<span></span>", one(nxt, i + 2, "→") if nxt else "<span></span>")


def page_head(title, lead="", tags=""):
    return '<header class="page-head"><h1 class="page-title">%s</h1>%s%s</header>' % (
        esc(title), '<p class="lead">%s</p>' % esc(lead) if lead else "",
        '<p class="topics"><span class="mono">%s</span> %s</p>' % (esc(UI[CUR[0]]["Topics"]), esc(tags)) if tags else "")


def webpage_ld(kind, path, name, desc, lang, tags):
    """A schema.org page of the given kind (CollectionPage, AboutPage...) with the page's topic tags as keywords."""
    return {"@context": "https://schema.org", "@type": kind, "name": name, "description": desc, "url": abs_url(path),
            "inLanguage": HREFLANG[lang], "keywords": tags,
            "isPartOf": {"@type": "WebSite", "name": S["name"], "url": abs_url()},
            "about": {"@type": "Person", "name": S["name"], "url": abs_url(LP[lang])}}


def work_alt(w, lang, k=0, n=0):
    """Alt text of a work's image: what it is and who made it, plus its place among the work's images."""
    u = UI[lang]
    t = (u["work_desc"] % (w["title"], w.get("year"), tr(w, "type", lang) or u["work"], lname(lang))).rstrip(".。")
    return "%s (%d/%d)" % (t, k, n) if n > 1 else t


def work_card(n, w, lang, kw=False):
    c = cover_of(w)
    line = tr(w, "kw", lang) if kw else ""
    return ('<a class="card" href="%s"><div class="thumb">%s</div><div class="cap">%s<span class="t">%s%s</span>'
            '<span class="mono">%s</span>%s</div></a>') % (
        url(LP[lang] + "works/%s/" % w["slug"]), img(c, 900, work_alt(w, lang)) if c else '<span class="ph">%s</span>' % esc(w["title"]),
        idx(n), esc(w["title"]), '<span class="zh" lang="zh-Hant">%s</span>' % esc(w["title_zh"]) if w.get("title_zh") else "",
        esc(w.get("year")) + (" · " + esc(tr(w, "status", lang)) if w.get("status") else ""),
        '<span class="kw">%s</span>' % esc(line) if line else "")


def meta(rows):
    return '<dl class="meta">%s</dl>' % "".join("<dt>%s</dt><dd>%s</dd>" % r for r in rows if r[1])


# ---------- pages ----------
pages = {}  # path -> html
noindex = set()  # redirect stubs: kept out of the sitemap
for l in LANGS:
    TITLES.update({url(LP[l] + "works/%s/" % w["slug"]): w["title"] for w in works})
    TITLES.update({url(LP[l] + s + "/"): UI[l]["nav"][s] for s in NAV + FOOT})
TITLES.update({url("blog/%s/" % p["slug"]): p["title"] for p in posts})


def hidden_to_en(path):
    """de/works/x/ -> works/x/ while German is hidden; other paths stay as they are."""
    for l in HIDDEN_LANGS:
        if LP[l] and path.startswith(LP[l]):
            return path[len(LP[l]):]
    return path


def page(path, *args, **kw):
    if hidden_to_en(path) != path:
        redirect(path, hidden_to_en(path))
        return
    if path in ("impressum/", "datenschutz/"):  # German by law; framed in German, or in English while German is hidden
        kw.update(lang="en", content_lang="de") if "de" in HIDDEN_LANGS else kw.update(lang="de")
    pages[path] = layout(path, *args, **kw)


def each(path):
    """The same page in every language."""
    return {l: LP[l] + path for l in SHOWN_LANGS}


# The chat's header: the GPU from "This is also a GPU", drawn in text. chat.js spins the
# fans (the <b> glyphs) and raises the temperature while an answer is being written.
def _ask_gpu():
    art = r"""      .------------------------------------------------------------.
   ___|  .-----------.      .-----------.      .-----------.       |
  |   | /  \   |   /  \    /  \   |   /  \    /  \   |   /  \      |
  |   ||    \  |  /    |  |    \  |  /    |  |    \  |  /    |     |
  |   ||-----( o )-----|  |-----( o )-----|  |-----( o )-----|  =  |
  |   ||    /  |  \    |  |    /  |  \    |  |    /  |  \    |  =  |
  |   | \  /   |   \  /    \  /   |   \  /    \  /   |   \  /   =  |
  |___|  '-----------'      '-----------'      '-----------'       |
      '----------.---------------------.---------------------------'
                 |  |||||||||||||||||  |          \       {T}
                 '---------------------'           '---."""
    # spokes of the first fan (row, column); the other two fans sit 19 and 38 columns further.
    # v = vertical, d = diagonal, h = horizontal. chat.js alternates "+" (v, h) and "x" (d).
    spokes = {(r, 15): "v" for r in (2, 3, 5, 6)}
    spokes.update({rc: "d" for rc in ((2, 11), (3, 12), (5, 12), (6, 11), (2, 19), (3, 18), (5, 18), (6, 19))})
    spokes.update({(4, c): "h" for c in list(range(8, 13)) + list(range(18, 23))})
    for (r, c), k in list(spokes.items()):
        spokes[(r, c + 19)] = spokes[(r, c + 38)] = k
    rows = []
    for r, line in enumerate(art.split("\n")):
        rows.append("".join('<b class="%s">%s</b>' % (spokes[(r, c)], ch) if (r, c) in spokes else esc(ch)
                            for c, ch in enumerate(line)))
    return "\n".join(rows).replace("{T}", "<i>41</i>°C")


ASK_GPU = _ask_gpu()


def home_text(lang):
    """The big text at the bottom of the homepage (site.home_text / _de / _zh). Empty: the
    space stays, so the layout does not move when text is added later."""
    t = tr(S, "home_text", lang)
    if not t:
        return '<p class="home-statement empty" aria-hidden="true"></p>'
    # a blank line in the text starts a new paragraph
    parts = [esc(x.strip()) for x in t.split("\n\n") if x.strip()]
    return '<p class="home-statement">%s</p>' % "<br><br>".join("<span>%s</span>" % x for x in parts)


def ask_box(lang):
    """The chat box on the homepage; only rendered once site.chat_endpoint is set."""
    if not S.get("chat_endpoint"):
        return ""
    u = UI[lang]
    msgs = {k: u[k] % (S.get("email_alt") or S["email"],) if k == "ask_err" else u[k] for k in ("ask_err", "ask_busy", "ask_refusal")}
    # the endpoint is written reversed + base64 so it is not a plain URL in the page source
    enc = base64.b64encode(S["chat_endpoint"].encode()).decode()[::-1]
    ts = ' data-turnstile="%s"' % esc(S["turnstile_sitekey"]) if S.get("turnstile_sitekey") else ""
    return ('<section class="ask" id="ask" aria-labelledby="ask-h" data-e="%s"%s data-msgs="%s">'
            '<pre class="ask-gpu" aria-hidden="true">' + ASK_GPU + '</pre>'
            '<h2 id="ask-h" class="ask-h">%s</h2>'
            '<div class="ask-log" aria-live="polite"></div>'
            '<form class="ask-form"><span class="ask-prompt" aria-hidden="true">&gt;</span>'
            '<input name="q" type="text" maxlength="600" autocomplete="off" required '
            'placeholder="%s" aria-label="%s" data-ex="%s"><button type="submit">%s</button></form>'
            '<p class="ask-note">%s</p>'
            '<script src="%s" defer></script></section>') % (
        enc, ts, esc(json.dumps(msgs, ensure_ascii=False)), esc(u["ask"]),
        esc(u["ask_ph"]), esc(u["ask_ph"]), esc(json.dumps(u["ask_ex"], ensure_ascii=False)), esc(u["ask_btn"]),
        esc(u["ask_note"]).replace("%s", '<a href="%s">%s</a>' % (url("datenschutz/#chat"), esc(u["ask_more"]))),
        versioned("assets/chat.js"))


years = sorted(w["year"][:4] for w in works if w.get("year"))
y0, y1 = (years[0], years[-1]) if years else ("", "")
platforms = sorted({"Vimeo" if "vimeo" in (p.get("video") or "") else "YouTube"
                    for p in D.get("performances", []) if not p.get("hidden")})

def redirect(old, new):
    """A tiny page that forwards an old URL (e.g. writing/ -> blog/)."""
    new = hidden_to_en(new)
    pages[old] = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Moved</title>'
                  '<link rel="canonical" href="%s"><meta name="robots" content="noindex">'
                  '<meta http-equiv="refresh" content="0; url=%s"><a href="%s">%s</a></html>\n' % (
                      esc(abs_url(new.split("#")[0])), esc(url(new)), esc(url(new)), esc(abs_url(new))))
    noindex.add(old)


for L in LANGS:
    CUR[0] = L
    u, P = UI[L], LP[L]

    # home: generative field + statement, then a few recent works
    page(P, "", tr(S, "description", L),
         '<section class="home-hero"><div class="field" data-effect="field" data-words="%s" aria-hidden="true"></div>'
         '<h1 class="sr-only">%s %s</h1>%s%s</section>'
         '<section class="home-selected" aria-label="%s"><div class="grid">%s</div>'
         '<a class="more" href="%s">%s</a></section>' % (
             esc(json.dumps(S.get("hidden_words", []), ensure_ascii=False)),
             esc(S["name"]), esc(S.get("name_zh", "")), ask_box(L), home_text(L),
             esc(u["selected"]),
             "".join(work_card(i + 1, w, L) for i, w in enumerate(works[:3])), url(P + "works/"), esc(u["all_works"] % len(works))),
         ld=person(L), full=True, lang=L, alts=each(""))

    SHORT_HOST = {"thephotographersgallery.org.uk": "The Photographers’ Gallery"}
    # each performance record and talk recording opens on Vimeo / YouTube / the host's site in a new tab
    def watch_card(href, thumb, title, sub, note, title_lang="", ph="", more=""):
        v = video_id(href)
        where = "YouTube" if v and v[0] == "youtube" else "Vimeo" if v else urlparse(href).netloc.replace("www.", "")
        where = SHORT_HOST.get(where, where)
        pic = img(thumb, 1100, title) if thumb else '<span class="ph">%s</span>' % esc(ph or title)
        return ('<div class="perf-item"><a class="perf-card" href="%s" target="_blank" rel="noopener"><div class="thumb">%s'
                '<span class="watch">%s</span></div><div class="cap"><h3%s>%s</h3>%s%s</div></a>') % (
            esc(href), pic, esc(u["watch"] % where), title_lang, esc(title),
            '<p class="by mono">%s</p>' % esc(sub) if sub else "", '<p>%s</p>' % esc(note) if note else "") + (
            # an event page next to the recording (a link can't sit inside the card's own link)
            '<a class="perf-more mono" href="%s" target="_blank" rel="noopener">%s ↗</a>' % (esc(more), esc(u["event"])) if more else "") + "</div>"

    perfs = [p for p in D.get("performances", []) if not p.get("hidden") and p.get("video")]
    perf_html = "".join(watch_card(p["video"], p.get("thumb") or cover_of({"video": p.get("video")}), tr(p, "title", L),
                                   p.get("year", ""), tr(p, "note", L), more=p.get("link", "")) for p in perfs)
    page(P + "works/", u["nav"]["works"], u["works_desc"] % (lname(L), y0, y1),
         '<header class="page-head"><h1 class="page-title">%s</h1>%s</header>' % (
             esc(u["nav"]["works"]), '<p class="lead jump"><a href="#performances">%s ↓</a></p>' % esc(u["perf_title"]) if perfs else "") +
         '<div class="grid">%s</div>' % "".join(work_card(i + 1, w, L, kw=True) for i, w in enumerate(works)) +
         ('<section class="sub-sec" id="performances"><header class="sub-head"><h2>%s</h2></header>'
          '<div class="perf">%s</div></section>' % (esc(u["perf_title"]), perf_html) if perfs else ""),
         ld=webpage_ld("CollectionPage", P + "works/", u["nav"]["works"], u["works_desc"] % (lname(L), y0, y1), L, u["tags"]["works"]),
         section="works", lang=L, alts=each("works/"))

    for i, w in enumerate(works):
        wtags = tr(w, "tags", L) or []
        rows = [(u["Year"], esc(w.get("year"))), (u["Status"], esc(tr(w, "status", L))), (u["Type"], esc(tr(w, "type", L))),
                (u["Materials"], esc(tr(w, "materials", L))), (u["Topics"], esc(", ".join(wtags))), (u["With"], esc(w.get("collaborators")))]
        rows += [(u["Link"], a(l["url"], esc(l.get("label") or l["url"]))) for l in w.get("links", []) if l.get("url")]
        ims = w.get("images", [])
        plates = embed(w.get("video"), w.get("video_thumb", ""), w["title"]) + "".join(clip(c, w["title"]) for c in w.get("clips", []))
        moving = w.get("video") or w.get("clips")
        # full-width lead (video, clips or the first photo), then the rest in two masonry
        # columns so photos of different proportions leave no gaps
        figs = ["<figure>%s</figure>" % img(im, 1600 if k == 0 else 1000, work_alt(w, L, k + 1, len(ims)))
                for k, im in enumerate(ims)]
        if not moving and figs:
            plates += figs.pop(0).replace("<figure>", '<figure class="hero">', 1)
        if len(figs) == 1:
            plates += figs[0].replace("<figure>", '<figure class="hero">', 1)
        elif figs:
            plates += '<div class="cols">%s</div>' % "".join(figs)
        text = tr(w, "text", L)
        # a translation may be missing: then the English text is shown, marked as English
        tl = HREFLANG[L] if L == "en" or w.get("text_" + L) else "en"
        body = ('<article class="work"><aside class="work-info">%s<h1>%s</h1>%s%s<div class="prose"%s>%s</div>%s</aside>'
                '<div class="plates">%s</div>%s</article>') % (
            idx(i + 1), esc(w["title"]), '<p class="zh" lang="zh-Hant">%s</p>' % esc(w["title_zh"]) if w.get("title_zh") else "",
            meta(rows), ' lang="%s"' % tl if tl != HREFLANG[L] else "", prose(text),
            '<p class="credits">%s</p>' % esc(w["credits"]) if w.get("credits") else "",
            plates, pager(works, i, P + "works/%s/", "title", u["nav"]["works"]))
        generic = u["work_desc"] % (w["title"], w.get("year"), tr(w, "type", L) or u["work"], lname(L))
        # the description names the artist in full, then the work's own text
        by = u["work_by"] % (tr(w, "type", L) or u["work"], lname(L), w.get("year"))
        # an optional "summary" (+ _de/_zh) replaces the opening of the text, e.g. when a work opens with a poem
        lead = tr(w, "summary", L) or text
        room = (100 if L == "zh" else 155) - len(by) - 1  # keep the whole description within what a result shows
        desc = (by + ("" if L == "zh" else " ") + summary(lead, max(room, 40), words=L != "zh")) if lead else generic
        ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": w["title"],
              "alternateName": w.get("title_zh") or None, "dateCreated": w.get("year", "")[:4],
              "genre": tr(w, "type", L) or None, "url": abs_url(P + "works/%s/" % w["slug"]), "inLanguage": HREFLANG[L],
              "image": asset_abs(cover_of(w)) if cover_of(w) else None, "description": desc,
              "keywords": ", ".join(wtags) or None,
              "creator": {"@type": "Person", "name": S["name"], "url": abs_url(P)}}
        lds = [{k: v for k, v in ld.items() if v}]
        vid = video_id(w.get("video"))
        if vid and vid[0] in ("vimeo", "youtube"):
            thumb = w.get("video_thumb") or cover_of(w)
            lds.append({k: v for k, v in {
                "@context": "https://schema.org", "@type": "VideoObject", "name": w["title"], "description": desc,
                "thumbnailUrl": asset_abs(thumb) if thumb else None, "uploadDate": ("%s-01-01T00:00:00+00:00" % w["year"][:4]) if (w.get("year") or "")[:4].isdigit() else None,
                "embedUrl": ("https://player.vimeo.com/video/%s" % vid[1] if vid[0] == "vimeo"
                             else "https://www.youtube-nocookie.com/embed/%s" % vid[1]),
                "inLanguage": HREFLANG[L], "creator": {"@type": "Person", "name": S["name"], "url": abs_url(P)}}.items() if v})
        page(P + "works/%s/" % w["slug"], w["title"] + (" " + w["title_zh"] if w.get("title_zh") else ""), desc, body,
             image=cover_of(w), og_type="article", ld=lds, section="works", lang=L,
             alts=each("works/%s/" % w["slug"]))

    def press_rows(group):
        rows = ""
        for it in D.get("press", []):
            if it.get("group") != group or not it.get("url"):
                continue
            note = tr(it, "note", L)
            same = L != "en" and bool(note) and not it.get("note_" + L)  # not translated: mark the row as English
            rows += ('<div class="cv-row press-row"%s><span class="mono">%s</span><span>%s<span class="press-by">%s</span>%s</span></div>' % (
                ' lang="en"' if same else "", esc((it.get("date") or "")[:4]), a(it["url"], esc(it["title"])),
                esc(it.get("outlet")), '<span class="press-note">%s</span>' % esc(note) if note else ""))
        return rows

    # CV: a jump list of the sections first; long sections show their latest rows and fold the rest away
    def cv_id(title):
        return "cv-" + re.sub(r"[^a-z]+", "-", title.lower()).strip("-")  # prefixed: #performances is the works page's band

    CV_SHOW = 8
    cv, jumps = "", []
    texts = press_rows("read")
    for sec in D["about"]["sections"]:
        rows = []
        for it in sec["items"]:
            text = tr(it, "text", L)
            same = L != "en" and not it.get("text_" + L)  # not translated: mark the row as English
            rows.append('<div class="cv-row"%s><span class="mono">%s</span><span>%s</span></div>' % (
                ' lang="en"' if same else "", esc(it.get("year")), a(it["url"], esc(text)) if it.get("url") else esc(text)))
        body = "".join(rows[:CV_SHOW]) + ('<details class="cv-more"><summary class="mono">%s</summary>%s</details>' % (
            esc(u["show_all"] % len(rows)), "".join(rows[CV_SHOW:])) if len(rows) > CV_SHOW + 2 else "".join(rows[CV_SHOW:]))
        sid = cv_id(sec["title"])
        jumps.append((sid, tr(sec, "title", L)))
        cv += '<section class="cv-sec" id="%s"><h2>%s</h2><div>%s</div></section>' % (sid, esc(tr(sec, "title", L)), body)
        if sec["title"] == "Publications & Writing" and texts:  # texts by others follow the own texts
            jumps.append(("texts", u["press_groups"]["read"]))
            cv += '<section class="cv-sec" id="texts"><h2>%s</h2><div>%s</div></section>' % (esc(u["press_groups"]["read"]), texts)
    cv_nav = '<nav class="cv-nav mono" aria-label="CV">%s</nav>' % "".join('<a href="#%s">%s</a>' % (i, esc(t)) for i, t in jumps)

    bio = tr(D["about"], "bio", L)
    more = tr(D["about"], "text", L)  # the longer text under the bio (the bio alone stays the page description)
    about_mail = S.get("email_alt") or S["email"]  # the address shown on the About page (the sidebar has site.email)
    page(P + "about/", u["about"], bio,
         '<div class="about-top"><h1 class="page-title">%s</h1><div><p class="bio">%s</p>%s'
         '<p class="contact"><span class="mono">%s</span><a href="mailto:%s">%s</a></p>'
         '<p class="contact-note">%s</p>'
         '<p class="topics"><span class="mono">%s</span> %s</p></div></div>%s%s' % (
             esc(u["about"]), esc(bio), '<div class="prose about-text"%s>%s</div>' % (
                 "" if L == "en" or D["about"].get("text_" + L) else ' lang="en"', prose(more)) if more else "",
             esc(u["Email"]), esc(about_mail), esc(about_mail), esc(u["contact_note"]),
             esc(u["Topics"]), esc(u["tags"]["about"]), cv_nav, cv),
         ld=dict(person(L), description=bio, keywords=u["tags"]["about"]), og_type="profile", section="about", lang=L, alts=each("about/"))

    # workshops: what a workshop can be, one page each (site.json "workshops", images in images/workshops/),
    # then the talk recordings (site.json "press", group "watch")
    shops = [x for x in D.get("workshops", []) if not x.get("hidden")]
    mail = S.get("email_alt") or S["email"]
    contact = '<p class="contact"><span class="mono">%s</span><a href="mailto:%s">%s</a></p><p class="contact-note">%s</p>' % (
        esc(u["Email"]), esc(mail), esc(mail), esc(u["workshops_ask"]))

    def shop_pics(x):
        return [i["src"] if isinstance(i, dict) else i for i in x.get("images", [])]

    def shop_card(x):
        pics = shop_pics(x)
        return ('<a class="card shop-card" href="%s"><div class="thumb">%s</div><div class="cap"><span class="t">%s</span>'
                '<span class="mono">%s</span><span class="kw">%s</span></div></a>') % (
            url(P + "workshops/%s/" % x["slug"]), img(pics[0], 900, tr(x, "title", L)) if pics else '<span class="ph">%s</span>' % esc(x["title"]),
            esc(tr(x, "title", L)), esc(x.get("with") and u["work_with"] % x["with"] or ""), esc(tr(x, "summary", L)))

    talks = [it for it in D.get("press", []) if it.get("group") == "watch" and it.get("url")]
    talk_html = "".join(watch_card(it["url"], it.get("thumb"), it["title"], " · ".join(x for x in (it.get("outlet"), (it.get("date") or "")[:4]) if x),
                                   tr(it, "note", L), ' lang="en"' if L != "en" else "", (it.get("outlet") or "").split(",")[0]) for it in talks)
    page(P + "workshops/", u["nav"]["workshops"], u["workshops_desc"] % lname(L),
         page_head(u["nav"]["workshops"], u["workshops_lead"]) +
         ('<div class="grid">%s</div>' % "".join(shop_card(x) for x in shops) if shops else "") +
         ('<section class="sub-sec" id="talks"><header class="sub-head"><h2>%s</h2></header><div class="perf talks">%s</div></section>' % (
             esc(u["press_groups"]["watch"]), talk_html) if talks else "") +
         '<div class="sub-sec">%s</div>' % contact,
         ld=webpage_ld("CollectionPage", P + "workshops/", u["nav"]["workshops"], u["workshops_desc"] % lname(L), L, u["tags"]["workshops"]),
         section="workshops", lang=L, alts=each("workshops/"))

    for i, x in enumerate(shops):
        pics = shop_pics(x)
        alts = [(i.get("alt_" + L) or i.get("alt")) if isinstance(i, dict) else None for i in x.get("images", [])]
        figs = ["<figure>%s</figure>" % img(im, 1600 if k == 0 else 1000, alts[k] or "%s (%d/%d)" % (tr(x, "title", L), k + 1, len(pics)))
                for k, im in enumerate(pics)]
        plates = "".join(f.replace("<figure>", '<figure class="hero">', 1) for f in figs)  # screenshots: each at full width
        text, held = tr(x, "text", L), tr(x, "held", L)
        tl = HREFLANG[L] if L == "en" or x.get("text_" + L) else "en"
        body = ('<article class="work"><aside class="work-info"><p class="kicker mono"><a href="%s">%s</a></p><h1>%s</h1>%s<p class="shop-sum">%s</p><div class="prose"%s>%s</div>'
                '%s%s</aside><div class="plates">%s</div>%s</article>') % (
            url(P + "workshops/"), esc(u["workshop"]), esc(tr(x, "title", L)), meta([(u["With"], esc(x.get("with")))]), esc(tr(x, "summary", L)),
            ' lang="%s"' % tl if tl != HREFLANG[L] else "", prose(text),
            '<div class="held"><h2 class="mono">%s</h2><p>%s</p></div>' % (esc(u["held"]), "<br>".join(linkify(h) for h in held.split("\n") if h.strip())) if held else "",
            contact, plates, pager(shops, i, P + "workshops/%s/", "title", u["nav"]["workshops"]))
        desc = summary(tr(x, "summary", L) or text, 100 if L == "zh" else 155, words=L != "zh")
        page(P + "workshops/%s/" % x["slug"], tr(x, "title", L), desc, body, image=pics[0] if pics else None, og_type="article",
             ld={k: v for k, v in {"@context": "https://schema.org", "@type": "CreativeWork", "genre": "Workshop", "name": tr(x, "title", L),
                 "description": desc, "url": abs_url(P + "workshops/%s/" % x["slug"]), "inLanguage": HREFLANG[L],
                 "image": asset_abs(pics[0]) if pics else None,
                 "creator": {"@type": "Person", "name": S["name"], "url": abs_url(P + "about/")}}.items() if v},
             section="workshops", lang=L, alts=each("workshops/%s/" % x["slug"]))

    # the former pages for performances and for press now live on the works, workshops and about pages
    redirect(P + "performance/", P + "works/#performances")
    redirect(P + "press/", P + "workshops/#talks")
    redirect(P + "workshops/condition-for-emotions/", P + "workshops/conditions-for-emotions/")  # renamed 2026-10

    groups, order = {}, []
    for p in posts:
        y = p["date"][:4]
        if y not in groups:
            groups[y] = []
            order.append(y)
        groups[y].append('<li><a href="%s" lang="%s"><span class="t">%s</span><span class="cat mono">%s</span>'
                         '<span class="ex">%s</span></a></li>' % (
                             url("blog/%s/" % p["slug"]), p.get("lang", "zh-Hant"), esc(p["title"]), esc(p.get("category")),
                             esc(p.get("excerpt"))))
    page(P + "blog/", u["blog_title"], u["blog_desc"] % lname(L),
         page_head(u["blog_title"], u["blog_lead"]) +
         "".join('<section class="year-group"><span class="mono">%s</span><ul>%s</ul></section>' % (y, "".join(groups[y]))
                 for y in order),
         section="blog", lang=L, alts=each("blog/"))

    def friend(f):
        thumb = img(f["image"], 600, f["name"]) if f.get("image") else '<span class="ph">%s</span>' % esc(f["name"])
        if not f.get("url"):  # site no longer online: keep the name, drop the link
            return '<div class="card"><div class="thumb">%s</div><div class="cap"><span class="t">%s</span></div></div>' % (
                thumb, esc(f["name"]))
        return ('<a class="card" href="%s" target="_blank" rel="noopener"><div class="thumb">%s</div>'
                '<div class="cap"><span class="t">%s</span><span class="mono">↗</span></div></a>') % (
            esc(f["url"]), thumb, esc(f["name"]))

    page(P + "friends/", u["nav"]["friends"], u["friends_desc"] % lname(L),
         page_head(u["nav"]["friends"]) +
         '<div class="grid friends">%s</div>' % "".join(friend(f) for f in D.get("friends", [])),
         ld=webpage_ld("CollectionPage", P + "friends/", u["nav"]["friends"], u["friends_desc"] % lname(L), L, ""),
         section="friends", lang=L, alts=each("friends/"))

    # HTML site map: every page in one list, for visitors and for crawlers
    def smap(head, href, items=(), lang_attr=""):
        lis = "".join('<li><a href="%s"%s>%s</a></li>' % (esc(h), lang_attr, esc(t)) for t, h in items)
        return '<section class="cv-sec"><h2><a href="%s">%s</a></h2><div>%s</div></section>' % (
            esc(href), esc(head), '<ul class="sitemap-list">%s</ul>' % lis if lis else "")
    page(P + "sitemap/", u["sitemap"], u["sitemap_desc"] % lname(L),
         page_head(u["sitemap"], u["sitemap_lead"]) +
         smap(S["name"], url(P)) +
         smap(u["nav"]["works"], url(P + "works/"), [(w["title"], url(P + "works/%s/" % w["slug"])) for w in works]) +
         smap(u["perf_title"], url(P + "works/#performances"), [(tr(p, "title", L), p["video"]) for p in perfs]) +
         smap(u["nav"]["workshops"], url(P + "workshops/"), [(tr(x, "title", L), url(P + "workshops/%s/" % x["slug"])) for x in shops] +
              [(u["press_groups"]["watch"], url(P + "workshops/#talks"))]) +
         smap(u["about"], url(P + "about/"), [(u["press_groups"]["read"], url(P + "about/#texts"))]) +
         smap(u["nav"]["blog"], url(P + "blog/"), [(p["title"], url("blog/%s/" % p["slug"])) for p in posts],
              ' lang="%s"' % "zh-Hant") +
         smap(u["nav"]["friends"], url(P + "friends/")) +
         smap("Impressum / " + u["privacy"], url("impressum/"), [("Impressum", url("impressum/")), (u["privacy"], url("datenschutz/"))]),
         lang=L, alts=each("sitemap/"))

# blog posts: one version each (not translated), in the English frame
CUR[0] = "en"
for i, p in enumerate(posts):
    src = read_post(p["slug"])
    desc = p.get("excerpt") or summary(src)
    body = ('<article class="post"><aside class="post-info" lang="en"><h1 lang="%s">%s</h1>%s<a class="back" href="%s">← Blog Archive</a></aside>'
            '<div class="prose post-body">%s</div>%s</article>') % (
        p.get("lang", "zh-Hant"), esc(p["title"]),
        meta([("Date", esc(p["date"])), ("Category", esc(p.get("category"))),
              ("Author", a(abs_url("about/"), esc("%s, media artist" % S["name"])))]),
        url("blog/"), post_html(src), pager(posts, i, "blog/%s/", "title", "Posts"))
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"],
          "inLanguage": p.get("lang", "zh-Hant"), "url": abs_url("blog/%s/" % p["slug"]),
          "image": asset_abs(p.get("cover") or S.get("og_image")), "description": desc,
          "author": {"@type": "Person", "name": S["name"], "url": abs_url(), "jobTitle": "Media artist"},
          "mainEntityOfPage": abs_url("blog/%s/" % p["slug"])}
    page("blog/%s/" % p["slug"], p["title"], desc, body, image=p.get("cover"), og_type="article",
         content_lang=p.get("lang", "zh-Hant"), ld=ld, section="blog")


redirect("writing/", "blog/")
for p in posts:
    redirect("writing/%s/" % p["slug"], "blog/%s/" % p["slug"])

addr = S.get("address") or []
addr_html = "<br>".join(esc(x) for x in addr) if addr else \
    '<span class="todo">[Postanschrift fehlt — in site.json → site.address eintragen]</span>'
page("impressum/", "Impressum", "Impressum / legal notice of %s." % S["name"], body="""
<div class="legal-page">
<h1 class="page-title">Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>{name}<br>{addr}</p>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:{email}">{email}</a></p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>{name}<br>{addr}</p>
<h2>Haftung für Links</h2>
<p>Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte ich keinen Einfluss habe. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich. Bei Bekanntwerden von Rechtsverletzungen werden derartige Links umgehend entfernt.</p>
<h2>Urheberrecht</h2>
<p>Texte, Bilder und Videos auf dieser Website unterliegen dem Urheberrecht von {name} bzw. der genannten Fotograf*innen und Kooperationspartner*innen. Eine Verwendung ist nur nach vorheriger Zustimmung erlaubt.</p>
<h2 id="schriften">Schriften / Typefaces</h2>
<p>Diese Website verwendet freie Schriften unter der <a href="https://openfontlicense.org/">SIL Open Font License 1.1</a>; die Schriftdateien liegen auf diesem Server, die Lizenztexte sind jeweils verlinkt. / This site uses open-source typefaces under the SIL Open Font License 1.1, served from this server.</p>
<ul class="font-credits">
<li><b>Minipax</b> von Raphaël Ronot (Text und Überschriften Latein / text and headings, Latin): <a href="https://github.com/ronotypo/Minipax">github.com/ronotypo/Minipax</a>, Lizenz: <a href="{fonts}LICENSES/Minipax-OFL.txt">OFL</a></li>
<li><b>仙人掌明體 Cactus Classical Serif</b> von Tian Haidong und Moonlit Owen (Fließtext Chinesisch / body text, Chinese): <a href="https://github.com/MoonlitOwen/CactusSerif">github.com/MoonlitOwen/CactusSerif</a>, Lizenz: <a href="{fonts}LICENSES/Cactus-Classical-Serif-OFL.txt">OFL</a>. Teilmengen von Google Fonts, auf diesem Server.</li>
<li><b>芫荽 Iansui</b> von ButTaiwan, auf Basis von Klee One (Fontworks) (Anmerkungen, Bildunterschriften und Chat, Chinesisch / notes, captions and chat, Chinese): <a href="https://github.com/ButTaiwan/iansui">github.com/ButTaiwan/iansui</a>, Lizenz: <a href="{fonts}LICENSES/Iansui-OFL.txt">OFL</a>. Teilmengen von Google Fonts, auf diesem Server.</li>
<li><b>jf open 粉圓 (jf open huninn)</b> von justfont (Überschriften Chinesisch / headings, Chinese): <a href="https://github.com/justfont/open-huninn-font">github.com/justfont/open-huninn-font</a>, Lizenz: <a href="{fonts}LICENSES/jf-open-huninn-OFL.txt">OFL</a>. Für das Web in Teilmengen zerlegt und daher umbenannt (LTC Round), wie es die Lizenz für den reservierten Namen verlangt.</li>
</ul>
<p class="en">Legal notice for this personal artist website. Contact: {email}.</p>
</div>""".format(name=esc(S["name"]), addr=addr_html, email=esc(S["email"]), fonts=url("assets/fonts/")))

CHAT_PRIVACY = """<h2 id="chat">7. Fragen zur Arbeit (KI-Chat)</h2>
<p>Auf der Startseite können Sie Fragen zu den Arbeiten stellen. Erst wenn Sie eine Frage absenden, wird sie zusammen mit den vorherigen Fragen und Antworten dieses Gesprächs an einen Cloudflare Worker (Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA) und von dort an die API von OpenAI (OpenAI Ireland Ltd., 1st Floor, The Liffey Trust Centre, 117–126 Sheriff Street Upper, Dublin 1, Irland; Konzernmutter OpenAI, L.L.C., USA) übertragen, die die Antwort erzeugt. Cloudflare verarbeitet dabei Ihre IP-Adresse, um Missbrauch zu begrenzen (höchstens einige Fragen pro Minute). Um die Funktion des Chats zu verbessern (z.&nbsp;B. unbeantwortete oder fehlerhafte Antworten zu erkennen und die Wissensbasis zu ergänzen), werden Ihre Frage, die erzeugte Antwort, die vorgeschlagenen Links, die Sprache der Seite, eine automatische Einordnung des Themas und das Land, aus dem die Anfrage kommt (von Cloudflare aus der IP-Adresse abgeleitet), in einer Datenbank bei Cloudflare (D1) gespeichert, ohne IP-Adresse und ohne Cookies. Diese Einträge werden nicht für Werbung verwendet, nicht weitergegeben und ohne feste Löschfrist aufbewahrt; auf Anfrage löschen wir einzelne Einträge (bitte mit Datum und Wortlaut der Frage). OpenAI verwendet Daten aus der API nicht zum Training seiner Modelle und speichert sie nur kurzzeitig (in der Regel bis zu 30 Tage) zur Missbrauchserkennung. Bitte geben Sie keine personenbezogenen Daten in das Feld ein.{turnstile} Rechtsgrundlage ist Art. 6 Abs. 1 lit. a und f DSGVO (Ihre Anfrage; berechtigtes Interesse an einem Auskunftsangebot über die Arbeiten und an dessen Verbesserung). Die Übermittlung in die USA erfolgt auf Grundlage der EU-Standardvertragsklauseln bzw. des EU-US Data Privacy Framework. Die Antworten werden automatisch erzeugt und können Fehler enthalten.</p>
"""

CHAT_PRIVACY = CHAT_PRIVACY.replace("{turnstile}", (
    " Zum Schutz vor automatisierten Anfragen wird beim Absenden Cloudflare Turnstile geladen, das ohne Cookies "
    "prüft, ob die Anfrage von einem Menschen stammt (Art. 6 Abs. 1 lit. f DSGVO)."
) if S.get("turnstile_sitekey") else "")

page("datenschutz/", "Datenschutz", "Privacy policy (Datenschutzerklärung) of %s." % S["name"], body="""
<div class="legal-page">
<h1 class="page-title">Datenschutz&shy;erklärung</h1>
<h2>1. Verantwortlicher</h2>
<p>{name}<br>{addr}<br>E-Mail: <a href="mailto:{email}">{email}</a></p>
<h2>2. Hosting</h2>
<p>Diese Website wird bei GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA) gehostet. Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie IP-Adresse, Zeitpunkt und aufgerufene Seite in Server-Logfiles, um die Website auszuliefern und abzusichern. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer sicheren und funktionsfähigen Website). Die Übermittlung in die USA erfolgt auf Grundlage des EU-US Data Privacy Framework.</p>
<h2>3. Google Analytics</h2>
<p>Diese Website verwendet Google Analytics 4 (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland), um die Nutzung statistisch auszuwerten. Beim Aufruf einer Seite setzt Google Analytics Cookies und erfasst pseudonymisierte Nutzungsdaten (z.&nbsp;B. aufgerufene Seiten, Sprache der Seite, Verweildauer, ungefährer Standort, Gerät, und ob im Fragefeld eine Frage gestellt oder ein vorgeschlagener Link angeklickt wurde – ohne den Text der Frage). IP-Adressen werden von Google Analytics 4 nicht gespeichert. Werbefunktionen sind deaktiviert. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer Reichweitenmessung dieser Website). Eine Übermittlung in die USA ist möglich; Google ist unter dem EU-US Data Privacy Framework zertifiziert.</p>
<p>Sie können der Erfassung jederzeit für diesen Browser widersprechen: <button type="button" data-ga-optout data-off="Google Analytics deaktivieren / Turn off analytics" data-on="Google Analytics wieder aktivieren / Turn analytics back on">Google Analytics deaktivieren / Turn off analytics</button> Alternativ können Sie Cookies in Ihrem Browser blockieren.</p>
<h2>4. Eingebettete Videos (Vimeo, YouTube)</h2>
<p>Videos werden erst geladen, wenn Sie auf das Vorschaubild klicken. Erst dann werden Daten (u.&nbsp;a. IP-Adresse) an Vimeo (Vimeo.com Inc., New York, USA) bzw. YouTube (Google Ireland Limited) übertragen; YouTube wird im erweiterten Datenschutzmodus (youtube-nocookie.com) eingebunden. Vorschaubilder einiger Vimeo-Videos werden über vumbnail.com geladen.</p>
<h2>5. Externe Bilder</h2>
<p>Einzelne ältere Bilder werden noch vom Server der früheren Website (static.wixstatic.com, Wix.com Ltd.) geladen. Dabei wird Ihre IP-Adresse an Wix übertragen. Diese Bilder werden nach und nach auf diese Website verlagert.</p>
<h2>6. Schriften und Skripte</h2>
<p>Es werden keine Google Fonts von Google-Servern geladen; alle Schriften werden von diesem Server ausgeliefert (siehe Impressum, Schriften). Die Bibliothek p5.js für die grafischen Animationen wird von cdnjs (Cloudflare, Inc.) geladen; dabei wird Ihre IP-Adresse an Cloudflare übertragen (Art. 6 Abs. 1 lit. f DSGVO).</p>
{chat}<h2>{n}. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit, Widerspruch sowie auf Widerruf erteilter Einwilligungen. Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren.</p>
<p class="en">In short: Google Analytics counts visits (you can turn it off with the button above); videos only load when you press play;{chat_en} nothing else tracks you.</p>
</div>""".format(name=esc(S["name"]), addr=addr_html, email=esc(S["email"]), n=8 if S.get("chat_endpoint") else 7,
               chat_en=" questions in the “Ask” box go to Cloudflare and OpenAI and are kept with the answers, without your IP address, to improve the chat;" if S.get("chat_endpoint") else "",
               chat=CHAT_PRIVACY if S.get("chat_endpoint") else ""))


# ---------- write ----------
def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


for s in SECTIONS + ["impressum", "datenschutz", "writing", "sitemap"] + [LP[l].strip("/") for l in LANGS if LP[l]]:  # start clean so removed works/posts disappear
    shutil.rmtree(os.path.join(ROOT, s), ignore_errors=True)
for path, text in pages.items():
    write(path + "index.html", text)

# RSS feed for the blog
feed_items = "".join(
    "<item><title>%s</title><link>%s</link><guid>%s</guid><pubDate>%s</pubDate><description>%s</description></item>" % (
        esc(p["title"]), abs_url("blog/%s/" % p["slug"]), abs_url("blog/%s/" % p["slug"]),
        datetime.datetime.strptime(p["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000"), esc(p.get("excerpt")))
    for p in posts)
feed = ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>%s — Blog</title>'
        "<link>%s</link><description>%s</description>%s</channel></rss>\n" % (esc(S["name"]), abs_url("blog/"), esc(S.get("description")), feed_items))
write("blog/feed.xml", feed)
write("writing/feed.xml", feed)  # old feed address, for existing subscribers

# llms.txt: a plain-language summary for AI assistants (llmstxt.org), linked from robots.txt
llms = ["# %s (%s)" % (S["name"], S.get("name_zh", "")), "",
        "> " + (S.get("statement") or S.get("description", "")), "",
        "Occupation: " + ", ".join(S.get("occupations", [])), "",
        "Areas: " + ", ".join(S.get("knows_about", [])), "",
        "## Main pages", "",
        "- [Works](%s): installations, performances, internet art and artistic research" % abs_url("works/"),
        "- [About / CV](%s): biography, teaching, exhibitions, talks, publications, texts by others" % abs_url("about/"),
        "- [Blog Archive](%s): texts and technical notes (in Mandarin)" % abs_url("blog/"),
        "- [Performances](%s): recordings of live audio-visual sets, 2016–2024 (on the works page)" % abs_url("works/#performances"),
        "- [Talks & Workshops](%s): talk recordings, and workshops on local AI, embeddings and AI bias" % abs_url("workshops/"),
        "- [Cited and discussed](%s): texts by others that cite or discuss the work, on the About page" % abs_url("about/#texts"), "",
        "The site is also available in Traditional Chinese (%s)." % abs_url("zh/"), "",
        "## Works", ""]
llms += ["- [%s](%s) (%s): %s" % (w["title"], abs_url("works/%s/" % w["slug"]), w.get("year"), w.get("type"))
         for w in works]
llms += ["", "## Contact", "", "- Email (talks, workshops, collaborations): " + (S.get("email_alt") or S["email"])] + ["- %s: %s" % (l["label"], l["url"]) for l in S.get("links", [])]
extra = os.path.join(ROOT, "data", "llms-extra.md")  # free text appended as is (edit it on GitHub)
if os.path.exists(extra):
    llms += ["", open(extra, encoding="utf-8").read().strip()]
llms_txt = "\n".join(llms) + "\n"
write("llms.txt", llms_txt)

# sitemap.xml and robots.txt only count at the domain root, so when the site lives
# in a subfolder they go to the repo root; the sitemap then also lists the other
# project sites on the domain (site.sitemap_extra).
# lastmod: a page's date moves only when its HTML changes (asset hashes ignored); kept in data/lastmod.json
LASTMOD_FILE = os.path.join(ROOT, "data", "lastmod.json")
try:
    _old = json.load(open(LASTMOD_FILE, encoding="utf-8"))
except (OSError, ValueError):
    _old = {}
_today = datetime.date.today().isoformat()
_new = {}
for _p, _html in pages.items():
    if _p in noindex:
        continue
    _h = hashlib.md5(re.sub(r"\?v=[0-9a-f]{8}", "", _html).encode()).hexdigest()[:12]
    _new[_p] = {"h": _h, "d": _old[_p]["d"] if _p in _old and _old[_p]["h"] == _h else _today}
if _new != _old:
    try:
        with open(LASTMOD_FILE, "w", encoding="utf-8") as f:
            f.write("{\n" + ",\n".join("%s: %s" % (json.dumps(k, ensure_ascii=False), json.dumps(_new[k])) for k in sorted(_new)) + "\n}\n")
    except OSError:
        pass
dates = {p: v["d"] for p, v in _new.items()}
dates.update({"blog/%s/" % p["slug"]: p["date"] for p in posts})
locs = ["  <url><loc>%s</loc>%s</url>\n" % (esc(abs_url(p)), "<lastmod>%s</lastmod>" % dates[p] if p in dates else "")
        for p in pages if p not in noindex]
locs += ["  <url><loc>%s</loc></url>\n" % esc(u) for u in S.get("sitemap_extra", [])]
top = REPO if PREFIX != "/" else ROOT
origin = "{0.scheme}://{0.netloc}/".format(urlparse(BASE))
open(os.path.join(top, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % "".join(locs))
open(os.path.join(top, "llms.txt"), "w", encoding="utf-8").write(llms_txt)
open(os.path.join(top, "robots.txt"), "w").write(
    "User-agent: *\nAllow: /\nDisallow: %sadmin/\nDisallow: %spreview.html\n\nSitemap: %ssitemap.xml\n"
    "# Summary for AI assistants: %sllms.txt\n" % (PREFIX, PREFIX, origin, origin))

# When the site lives at the domain root, keep old Wix URLs working.
if PREFIX == "/":
    old = dict(OLD, **{"/post/" + s: "blog/%s/" % s for s in post_slugs})
    for o, new in old.items():
        if o.strip("/") and o.strip("/") + "/" != new:
            write(o.strip("/") + "/index.html", '<!doctype html><meta charset="utf-8"><title>Moved</title>'
                  '<link rel="canonical" href="%s"><meta name="robots" content="noindex">'
                  '<meta http-equiv="refresh" content="0; url=%s"><a href="%s">%s</a>\n' % ((esc(abs_url(new)),) * 4))

# Keep the wiki's site map (what the homepage chat may link to) in step with the site.
runpy.run_path(os.path.join(ROOT, "scripts", "wiki-sitemap.py"))

print("built %d pages -> %s" % (len(pages), BASE))
