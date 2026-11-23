#!/usr/bin/env python3
"""Google Analytics viewer: pick a country (or city) and see which pages people there read
and what they did (videos, chat, outbound links, scrolling, where they came from).

Runs on your own computer only (http://localhost:8791) and reads GA4 through the Google
Analytics Data API. Python 3 and the `openssl` command (built into macOS); no packages.

    GA_PROPERTY=123456789 GA_KEY=~/.config/liutingchun/ga-key.json python3 scripts/ga-viewer.py

GA_PROPERTY: the numeric property id (GA -> Admin -> Property details; not the G-... id).
GA_KEY: a service-account key (JSON) with read access to the property. Setup, once:
  1. console.cloud.google.com -> new project -> APIs & Services -> Library ->
     "Google Analytics Data API" -> Enable.
  2. IAM & Admin -> Service accounts -> Create (no roles needed) -> Keys -> Add key -> JSON.
     Keep the file outside the repo, e.g. ~/.config/liutingchun/ga-key.json.
  3. GA -> Admin -> Property access management -> + -> the service account's e-mail
     (...@...iam.gserviceaccount.com) as Viewer.
  4. Optional: GA -> Admin -> Custom definitions -> Create custom dimension "video_title"
     (event scope) so video titles show up (counts start from that day).

    python3 scripts/ga-viewer.py --demo    made-up numbers, to look at the page without GA
"""
import base64, json, os, random, subprocess, sys, tempfile, threading, time, urllib.parse, urllib.request, webbrowser
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8791
API = "https://analyticsdata.googleapis.com/v1beta/properties/"
SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
CACHE_SECONDS = 600


# ---------- access token: service-account JWT signed with openssl ----------
def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


class Auth:
    def __init__(self, key_path):
        with open(os.path.expanduser(key_path)) as f:
            self.info = json.load(f)
        self.token, self.expires = None, 0
        self.lock = threading.Lock()

    def get(self):
        with self.lock:
            if self.token and time.time() < self.expires - 60:
                return self.token
            now = int(time.time())
            uri = self.info.get("token_uri", "https://oauth2.googleapis.com/token")
            head = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
            claim = b64(json.dumps({"iss": self.info["client_email"], "scope": SCOPE, "aud": uri,
                                    "iat": now, "exp": now + 3600}).encode())
            unsigned = (head + "." + claim).encode()
            fd, path = tempfile.mkstemp(suffix=".pem")
            try:
                with os.fdopen(fd, "w") as f:
                    f.write(self.info["private_key"])
                sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", path], input=unsigned,
                                     capture_output=True, check=True).stdout
            finally:
                os.remove(path)
            body = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                           "assertion": unsigned.decode() + "." + b64(sig)}).encode()
            try:
                with urllib.request.urlopen(urllib.request.Request(uri, data=body)) as r:
                    res = json.load(r)
            except urllib.error.HTTPError as e:
                sys.exit("Google sign-in failed %s: %s" % (e.code, e.read().decode()[:400]))
            self.token, self.expires = res["access_token"], now + int(res.get("expires_in", 3600))
            return self.token


# ---------- GA4 Data API ----------
class GA:
    def __init__(self, prop, auth):
        self.prop, self.auth = prop, auth
        self.cache = {}

    def call(self, method, body):
        key = method + json.dumps(body, sort_keys=True)
        hit = self.cache.get(key)
        if hit and time.time() - hit[0] < CACHE_SECONDS:
            return hit[1]
        req = urllib.request.Request(API + self.prop + ":" + method, data=json.dumps(body).encode(),
                                     headers={"Authorization": "Bearer " + self.auth.get(),
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                res = json.load(r)
        except urllib.error.HTTPError as e:
            raise RuntimeError("GA %s: %s" % (e.code, e.read().decode()[:300]))
        self.cache[key] = (time.time(), res)
        return res

    def report(self, dims, mets, start, end, filt=None, order=None, limit=200, realtime=False):
        body = {"dimensions": [{"name": d} for d in dims], "metrics": [{"name": m} for m in mets], "limit": limit}
        if not realtime:
            body["dateRanges"] = [{"startDate": start, "endDate": end}]
        if filt:
            body["dimensionFilter"] = filt
        if order:
            body["orderBys"] = [{"metric": {"metricName": order}, "desc": True}]
        res = self.call("runRealtimeReport" if realtime else "runReport", body)
        out = []
        for r in res.get("rows", []):
            row = {d: v["value"] for d, v in zip(dims, r.get("dimensionValues", []))}
            for m, v in zip(mets, r.get("metricValues", [])):
                row[m] = float(v["value"]) if "." in v["value"] else int(v["value"])
            out.append(row)
        return out


def exact(field, value):
    return {"filter": {"fieldName": field, "stringFilter": {"value": value, "matchType": "EXACT"}}}


def all_of(*parts):
    parts = [p for p in parts if p]
    return None if not parts else parts[0] if len(parts) == 1 else {"andGroup": {"expressions": parts}}


def events_in(names):
    return {"filter": {"fieldName": "eventName", "inListFilter": {"values": names}}}


QUIET = ["page_view", "session_start", "first_visit", "user_engagement"]


def region(ga, f):
    """Everything about one place (or the whole world when no country is given)."""
    s, e = f.get("start") or "28daysAgo", f.get("end") or "today"
    place = all_of(exact("country", f["country"]) if f.get("country") else None,
                   exact("city", f["city"]) if f.get("city") else None)
    jobs = {
        "totals": (["country"] if f.get("country") else [], ["activeUsers", "newUsers", "sessions", "screenPageViews",
                   "userEngagementDuration", "engagementRate"], place, None, 1),
        "days": (["date"], ["activeUsers", "screenPageViews"], place, None, 400),
        "cities": (["city"], ["activeUsers", "screenPageViews"], place, "activeUsers", 30),
        "pages": (["pagePath", "pageTitle"], ["screenPageViews", "activeUsers", "userEngagementDuration"],
                  place, "screenPageViews", 100),
        "page_events": (["pagePath", "eventName"], ["eventCount"],
                        all_of(place, {"notExpression": events_in(QUIET)}), "eventCount", 500),
        "events": (["eventName"], ["eventCount", "totalUsers"], place, "eventCount", 50),
        "links": (["eventName", "linkUrl"], ["eventCount"],
                  all_of(place, events_in(["click", "chat_link", "file_download"])), "eventCount", 50),
        "sources": (["sessionSourceMedium"], ["sessions", "activeUsers"], place, "sessions", 20),
        "landing": (["landingPagePlusQueryString"], ["sessions"], place, "sessions", 20),
        "devices": (["deviceCategory"], ["activeUsers"], place, "activeUsers", 10),
        "langs": (["contentGroup"], ["screenPageViews"], place, "screenPageViews", 10),
        "videos": (["customEvent:video_title", "customEvent:video_section"], ["eventCount"],
                   all_of(place, exact("eventName", "video_open")), "eventCount", 50),
    }

    def run(item):
        name, (dims, mets, filt, order, limit) = item
        try:
            return name, ga.report(dims, mets, s, e, filt, order, limit)
        except RuntimeError as err:
            if name == "videos":  # custom dimensions not registered yet: fall back to the link
                try:
                    return name, [{"customEvent:video_title": r["linkUrl"], "customEvent:video_section": "",
                                   "eventCount": r["eventCount"], "unregistered": 1}
                                  for r in ga.report(["linkUrl"], ["eventCount"], s, e,
                                                     all_of(place, exact("eventName", "video_open")), "eventCount", 50)]
                except RuntimeError:
                    pass
            return name, {"error": str(err)}

    with ThreadPoolExecutor(6) as pool:
        return dict(pool.map(run, jobs.items()))


def countries(ga, f):
    s, e = f.get("start") or "28daysAgo", f.get("end") or "today"
    return ga.report(["country"], ["activeUsers", "screenPageViews", "userEngagementDuration"], s, e,
                     order="activeUsers", limit=250)


def live(ga, f):
    return ga.report(["country", "unifiedScreenName"], ["activeUsers"], None, None, order="activeUsers",
                     limit=50, realtime=True)


# ---------- --demo: made-up numbers in the same shape ----------
class Demo:
    PAGES = [("/", "Ting-Chun Liu"), ("/works/", "Works – Ting-Chun Liu"),
             ("/works/latent-heat-generation/", "Latent Heat Generation – Ting-Chun Liu"),
             ("/zh/works/sixteen-tokens-for-a-cave/", "Sixteen Tokens for a Cave – 劉庭均"),
             ("/de/workshops/", "Vorträge, Workshops & Texte – Ting-Chun Liu"),
             ("/about/", "About – Ting-Chun Liu"), ("/blog/", "Blog – Ting-Chun Liu")]
    COUNTRIES = {"Germany": ["Berlin", "Weimar", "Cologne"], "Taiwan": ["Taipei", "Tainan"],
                 "United States": ["New York", "(not set)"], "Netherlands": ["Amsterdam"]}

    def __init__(self):
        random.seed(3)

    def report(self, dims, mets, start, end, filt=None, order=None, limit=200, realtime=False):
        r = random.Random(json.dumps([dims, filt]))
        pools = {"country": list(self.COUNTRIES), "city": ["Berlin", "Weimar", "Taipei", "Cologne", "(not set)"],
                 "pagePath": [p for p, _ in self.PAGES], "eventName": ["page_view", "scroll", "click", "video_open",
                 "chat_question", "chat_link", "user_engagement", "session_start", "first_visit"],
                 "linkUrl": ["https://vimeo.com/12345", "https://www.instagram.com/", "https://youtu.be/abc"],
                 "sessionSourceMedium": ["google / organic", "(direct) / (none)", "l.instagram.com / referral",
                                         "facebook.com / referral"],
                 "landingPagePlusQueryString": [p for p, _ in self.PAGES[:4]], "deviceCategory": ["desktop", "mobile"],
                 "contentGroup": ["en", "de", "zh-Hant"], "customEvent:video_title": ["Imaginary Landscape", "39C3 talk"],
                 "customEvent:video_section": ["talks", "work"], "unifiedScreenName": [t for _, t in self.PAGES]}
        if not dims:
            combos = [()]
        elif dims == ["date"]:
            combos = [(time.strftime("%Y%m%d", time.localtime(time.time() - 86400 * i)),) for i in range(28)]
        else:
            combos = {tuple(r.choice(pools.get(d, [""])) for d in dims) for _ in range(12)}
        out = []
        for c in combos:
            row = dict(zip(dims, c))
            if "pageTitle" in row:
                row["pageTitle"] = dict(self.PAGES).get(row.get("pagePath"), "")
            for m in mets:
                row[m] = round(r.random(), 2) if m == "engagementRate" else r.randint(1, 300) * (40 if m == "userEngagementDuration" else 1)
            out.append(row)
        return sorted(out, key=lambda x: -x.get(order, 0)) if order else out


# ---------- the page ----------
PAGE = r"""<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>網站訪客 · GA</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{font:14px/1.5 -apple-system,"PingFang TC","Noto Sans TC",system-ui,sans-serif;margin:0;color:#111;background:#fff}
.mono,.n{font-family:ui-monospace,Menlo,monospace} .n{text-align:right;white-space:nowrap}
.muted{color:#888} a{color:#E4032E;text-decoration:none} a:hover{text-decoration:underline}
header{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;padding:12px 20px;border-bottom:1px solid #eee;position:sticky;top:0;background:#fff;z-index:2}
header h1{font-size:15px;margin:0}
button.chip{font:inherit;font-size:13px;border:1px solid #ccc;background:#fff;padding:1px 8px;cursor:pointer;border-radius:2px}
button.chip.on{background:#111;color:#fff;border-color:#111}
input{font:inherit;font-size:13px;padding:2px 5px;border:1px solid #ccc}
main{display:grid;grid-template-columns:270px 1fr;min-height:calc(100vh - 50px)}
nav{border-right:1px solid #eee;padding:10px 0;overflow:auto;max-height:calc(100vh - 50px);position:sticky;top:50px}
nav .c{display:grid;grid-template-columns:1fr auto;gap:0 8px;padding:4px 16px;cursor:pointer;position:relative}
nav .c:hover{background:#f6f6f6} nav .c.on{background:#111;color:#fff} nav .c.on .muted{color:#bbb}
nav .c .bar{position:absolute;left:0;bottom:0;height:2px;background:#E4032E}
nav .c small{grid-column:1/3;font-size:11px}
#live{padding:8px 16px 12px;border-bottom:1px solid #eee;font-size:12px}
#live b{color:#E4032E}
section#view{padding:16px 24px 60px;min-width:0}
h2{font-size:20px;margin:0 0 2px} h3{font-size:14px;margin:28px 0 6px;padding-bottom:4px;border-bottom:1px solid #111}
h3 .muted{font-weight:normal;font-size:12px}
.kpis{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.kpi{border:1px solid #eee;padding:8px 12px;min-width:120px} .kpi b{display:block;font-size:20px;font-family:ui-monospace,Menlo,monospace}
.kpi span{font-size:12px;color:#888}
.cities{display:flex;flex-wrap:wrap;gap:4px;margin:6px 0}
table{border-collapse:collapse;width:100%} td,th{padding:5px 8px;border-bottom:1px solid #f0f0f0;vertical-align:top;font-size:13px}
th{text-align:left;font-weight:normal;color:#888;font-size:12px}
td.t{width:100%} .path{font-size:11px;color:#888;font-family:ui-monospace,Menlo,monospace;word-break:break-all}
.tags{margin-top:3px} .tag{display:inline-block;font-size:11px;background:#f3f3f3;padding:0 6px;margin:2px 4px 0 0;border-radius:2px}
.tag.hot{background:#fde6ea;color:#a0001c}
.meter{height:6px;background:#E4032E;display:block;margin-top:3px;min-width:1px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:0 32px}
svg{display:block;width:100%;height:110px} .err{color:#E4032E;font-size:12px}
.lang{display:inline-block;font-size:10px;border:1px solid #ccc;padding:0 4px;margin-right:4px;color:#666}
@media(max-width:900px){main{grid-template-columns:1fr} nav{position:static;max-height:260px;border-right:0;border-bottom:1px solid #eee} .grid2{grid-template-columns:1fr}}
</style>
<header>
  <h1>網站訪客</h1>
  <span id="ranges"></span>
  <span class="muted">或</span><input id="from" type="date"><span class="muted">–</span><input id="to" type="date">
  <span class="muted" id="status"></span>
</header>
<main>
  <nav><div id="live"></div><div id="countries"></div></nav>
  <section id="view"></section>
</main>
<script>
var S = {start:'28daysAgo', end:'today', country:'', city:''};
var RANGES = [['7daysAgo','7 天'],['28daysAgo','28 天'],['90daysAgo','90 天'],['365daysAgo','一年']];
var EV = {page_view:'看頁面', scroll:'捲到頁底（90%）', click:'點外部連結', user_engagement:'停留在頁面上',
  session_start:'開始一次造訪', first_visit:'第一次來', video_open:'開影片', chat_question:'在問答框提問',
  chat_link:'點問答框推薦的連結', file_download:'下載檔案', view_search_results:'站內搜尋',
  video_start:'開始播放嵌入影片', video_progress:'嵌入影片看到一半', video_complete:'嵌入影片看完',
  form_start:'開始填表單', form_submit:'送出表單'};
var HOT = {video_open:1, chat_question:1, chat_link:1, click:1, file_download:1, video_start:1, video_complete:1};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function qs(o){return Object.keys(o).filter(function(k){return o[k]}).map(function(k){return k+'='+encodeURIComponent(o[k])}).join('&')}
function get(u){return fetch(u).then(function(r){return r.json()})}
function num(n){return Number(n||0).toLocaleString('de-DE')}
function dur(sec){sec=Math.round(sec||0); return sec<60 ? sec+' 秒' : Math.floor(sec/60)+' 分 '+(sec%60)+' 秒'}
function ev(n){return EV[n] ? EV[n]+' <span class="muted mono" style="font-size:11px">'+esc(n)+'</span>' : '<span class="mono">'+esc(n)+'</span>'}
function langOf(p){return /^\/de\//.test(p)?'DE':/^\/zh\//.test(p)?'中':'EN'}
function status(t){document.getElementById('status').textContent=t||''}

function header(){
  document.getElementById('ranges').innerHTML = RANGES.map(function(r){
    return '<button class="chip'+(S.start===r[0]&&S.end==='today'?' on':'')+'" data-s="'+r[0]+'">'+r[1]+'</button>'}).join(' ');
}
document.getElementById('ranges').onclick = function(e){
  var b = e.target.closest('button'); if(!b) return;
  S.start = b.dataset.s; S.end = 'today'; document.getElementById('from').value = document.getElementById('to').value = '';
  header(); loadCountries(); loadView();
};
['from','to'].forEach(function(id){ document.getElementById(id).onchange = function(){
  var f = document.getElementById('from').value, t = document.getElementById('to').value;
  if(f && t){ S.start = f; S.end = t; header(); loadCountries(); loadView(); }
}});

function loadLive(){
  get('/api/live').then(function(rs){
    if(rs.error){ document.getElementById('live').innerHTML = '<span class="err">即時：'+esc(rs.error)+'</span>'; return; }
    var by = {}, total = 0;
    rs.forEach(function(r){ by[r.country] = (by[r.country]||0) + r.activeUsers; total += r.activeUsers; });
    document.getElementById('live').innerHTML = '<b>●</b> 過去 30 分鐘 <b>'+total+'</b> 人' +
      (total ? '<br>' + Object.keys(by).map(function(c){return esc(c)+' '+by[c]}).join(' · ') +
      '<br><span class="muted">' + rs.slice(0,5).map(function(r){return esc(r.unifiedScreenName)}).join('<br>') + '</span>' : '');
  });
}

function loadCountries(){
  get('/api/countries?'+qs({start:S.start,end:S.end})).then(function(rs){
    if(rs.error){ document.getElementById('countries').innerHTML = '<p class="err" style="padding:0 16px">'+esc(rs.error)+'</p>'; return; }
    var max = Math.max.apply(null, rs.map(function(r){return r.activeUsers}).concat([1]));
    var all = rs.reduce(function(a,r){return a+r.activeUsers},0);
    document.getElementById('countries').innerHTML =
      '<div class="c'+(S.country?'':' on')+'" data-c=""><span>全部地區</span><span class="n">'+num(all)+'</span></div>' +
      rs.map(function(r){
        return '<div class="c'+(S.country===r.country?' on':'')+'" data-c="'+esc(r.country)+'"><span>'+esc(r.country)+'</span>' +
          '<span class="n">'+num(r.activeUsers)+'</span><small class="muted">'+num(r.screenPageViews)+' 次瀏覽 · 平均 '+
          dur(r.userEngagementDuration/Math.max(r.activeUsers,1))+'</small><span class="bar" style="width:'+(100*r.activeUsers/max)+'%"></span></div>';
      }).join('');
  });
}
document.getElementById('countries').onclick = function(e){
  var c = e.target.closest('.c'); if(!c) return;
  S.country = c.dataset.c; S.city = '';
  document.querySelectorAll('nav .c').forEach(function(x){x.classList.toggle('on', x===c)});
  loadView(); window.scrollTo(0,0);
};

function bars(days){
  if(!days || !days.length) return '';
  days = days.slice().sort(function(a,b){return a.date<b.date?-1:1});
  var max = Math.max.apply(null, days.map(function(d){return d.activeUsers}).concat([1])), w = 100/days.length;
  return '<svg viewBox="0 0 100 40" preserveAspectRatio="none">' + days.map(function(d,i){
    var h = 36*d.activeUsers/max;
    return '<rect x="'+(i*w+w*0.1)+'" y="'+(38-h)+'" width="'+(w*0.8)+'" height="'+h+'" fill="#111"><title>'+
      d.date.slice(0,4)+'-'+d.date.slice(4,6)+'-'+d.date.slice(6)+'：'+d.activeUsers+' 人、'+d.screenPageViews+' 次瀏覽</title></rect>';
  }).join('') + '<line x1="0" x2="100" y1="38.2" y2="38.2" stroke="#ccc" stroke-width=".3"/></svg>' +
  '<div class="muted" style="display:flex;justify-content:space-between;font-size:11px"><span>'+days[0].date.slice(4,6)+'/'+days[0].date.slice(6)+
  '</span><span>每天的訪客數（游標移到長條上看數字）</span><span>'+days[days.length-1].date.slice(4,6)+'/'+days[days.length-1].date.slice(6)+'</span></div>';
}
function table(rows, cols, empty){
  if(rows && rows.error) return '<p class="err">'+esc(rows.error)+'</p>';
  if(!rows || !rows.length) return '<p class="muted">'+(empty||'沒有資料')+'</p>';
  return '<table><tr>'+cols.map(function(c){return '<th'+(c.n?' class="n"':'')+'>'+c.h+'</th>'}).join('')+'</tr>' +
    rows.map(function(r){return '<tr>'+cols.map(function(c){return '<td class="'+(c.n?'n':'t')+'">'+c.f(r)+'</td>'}).join('')+'</tr>'}).join('') + '</table>';
}
function share(rows, key){
  if(!rows || rows.error) return function(){return ''};
  var max = Math.max.apply(null, rows.map(function(r){return r[key]}).concat([1]));
  return function(r){return '<span class="meter" style="width:'+(100*r[key]/max)+'%"></span>'};
}

function loadView(){
  var v = document.getElementById('view');
  v.style.opacity = .4; status('讀取中…');
  get('/api/region?'+qs(S)).then(function(d){
    v.style.opacity = 1; status('');
    if(d.error){ v.innerHTML = '<p class="err">'+esc(d.error)+'</p>'; return; }
    var t = (d.totals && d.totals[0]) || {};
    var evc = {}; (d.events.error?[]:d.events).forEach(function(r){evc[r.eventName]=r.eventCount});
    var pe = {}; (d.page_events.error?[]:d.page_events).forEach(function(r){(pe[r.pagePath]=pe[r.pagePath]||[]).push(r)});
    var h = '<h2>'+esc(S.country||'全部地區')+(S.city?' · '+esc(S.city):'')+'</h2>';
    h += '<div class="kpis">' + [
      [num(t.activeUsers),'位訪客'], [num(t.newUsers),'位第一次來'], [num(t.screenPageViews),'次看頁面'],
      [dur(t.userEngagementDuration/Math.max(t.activeUsers||0,1)),'平均每人停留'],
      [Math.round((t.engagementRate||0)*100)+'%','的造訪有互動'],
      [num(evc.video_open),'次開影片'], [num(evc.chat_question),'個問答框提問'], [num(evc.click),'次點外部連結']
    ].map(function(k){return '<div class="kpi"><b>'+k[0]+'</b><span>'+k[1]+'</span></div>'}).join('') + '</div>';
    if(S.country && !d.cities.error && d.cities.length){
      h += '<div class="cities"><span class="muted" style="font-size:12px;margin-right:4px">城市</span><button class="chip'+(S.city?'':' on')+'" data-city="">全部</button>' +
        d.cities.map(function(c){return '<button class="chip'+(S.city===c.city?' on':'')+'" data-city="'+esc(c.city)+'">'+esc(c.city==='(not set)'?'不明':c.city)+' '+c.activeUsers+'</button>'}).join('') + '</div>';
    }
    h += bars(d.days.error?[]:d.days);

    h += '<h3>看了哪些頁面 <span class="muted">· 標籤是在那一頁做的事</span></h3>';
    var pm = share(d.pages, 'screenPageViews');
    h += table(d.pages, [
      {h:'頁面', f:function(r){ var tags = (pe[r.pagePath]||[]).map(function(x){
          return '<span class="tag'+(HOT[x.eventName]?' hot':'')+'">'+esc((EV[x.eventName]||x.eventName))+' '+x.eventCount+'</span>'}).join('');
        return '<span class="lang">'+langOf(r.pagePath)+'</span>'+esc(r.pageTitle.replace(/ [–-] (Ting-Chun Liu|劉庭均)$/,''))+
          '<div class="path"><a href="https://liutingchun.com'+esc(r.pagePath)+'" target="_blank">'+esc(r.pagePath)+'</a></div>'+pm(r)+
          (tags?'<div class="tags">'+tags+'</div>':'')}},
      {h:'瀏覽', n:1, f:function(r){return num(r.screenPageViews)}},
      {h:'人數', n:1, f:function(r){return num(r.activeUsers)}},
      {h:'平均停留', n:1, f:function(r){return dur(r.userEngagementDuration/Math.max(r.activeUsers,1))}}
    ]);

    h += '<div class="grid2"><div><h3>做了什麼 <span class="muted">· 所有互動</span></h3>';
    h += table(d.events, [
      {h:'動作', f:function(r){return ev(r.eventName)}},
      {h:'次數', n:1, f:function(r){return num(r.eventCount)}},
      {h:'人數', n:1, f:function(r){return num(r.totalUsers)}}
    ]);
    h += '</div><div><h3>開了哪些影片</h3>';
    var unreg = d.videos && d.videos[0] && d.videos[0].unregistered;
    h += table(d.videos, [
      {h:'影片', f:function(r){var t = r['customEvent:video_title']; return (/^https?:/.test(t)?'<a href="'+esc(t)+'" target="_blank">'+esc(t)+'</a>':esc(t||'(沒有標題)'))+
        (r['customEvent:video_section']?' <span class="muted">'+esc({talks:'講座',performances:'表演',work:'作品頁'}[r['customEvent:video_section']]||r['customEvent:video_section'])+'</span>':'')}},
      {h:'次數', n:1, f:function(r){return num(r.eventCount)}}
    ], '沒有人開影片');
    if(unreg) h += '<p class="muted" style="font-size:12px">在 GA 後台註冊自訂維度 video_title、video_section 後，這裡會顯示影片標題。</p>';
    h += '<h3>點出去的連結</h3>';
    h += table(d.links, [
      {h:'連結', f:function(r){return '<a href="'+esc(r.linkUrl)+'" target="_blank" class="mono" style="font-size:12px;word-break:break-all">'+esc(r.linkUrl||'(不明)')+'</a> <span class="muted">'+(r.eventName==='chat_link'?'問答框':r.eventName==='file_download'?'下載':'')+'</span>'}},
      {h:'次數', n:1, f:function(r){return num(r.eventCount)}}
    ], '沒有');
    h += '</div></div>';

    h += '<div class="grid2"><div><h3>從哪裡來</h3>';
    h += table(d.sources, [
      {h:'來源 / 媒介', f:function(r){return '<span class="mono" style="font-size:12px">'+esc(r.sessionSourceMedium)+'</span>'}},
      {h:'造訪', n:1, f:function(r){return num(r.sessions)}}
    ]);
    h += '<h3>第一頁落在哪裡</h3>';
    h += table(d.landing, [
      {h:'著陸頁', f:function(r){return '<span class="path" style="font-size:12px">'+esc(r.landingPagePlusQueryString)+'</span>'}},
      {h:'造訪', n:1, f:function(r){return num(r.sessions)}}
    ]);
    h += '</div><div><h3>裝置</h3>';
    h += table(d.devices, [
      {h:'裝置', f:function(r){return {desktop:'電腦',mobile:'手機',tablet:'平板'}[r.deviceCategory]||esc(r.deviceCategory)}},
      {h:'人數', n:1, f:function(r){return num(r.activeUsers)}}
    ]);
    h += '<h3>看哪個語言版本</h3>';
    h += table(d.langs, [
      {h:'語言', f:function(r){return {en:'英文',de:'德文','zh-Hant':'中文'}[r.contentGroup]||esc(r.contentGroup)}},
      {h:'瀏覽', n:1, f:function(r){return num(r.screenPageViews)}}
    ]);
    h += '</div></div>';
    v.innerHTML = h;
  }).catch(function(err){ v.style.opacity = 1; status(''); v.innerHTML = '<p class="err">'+esc(err)+'</p>'; });
}
document.getElementById('view').onclick = function(e){
  var b = e.target.closest('button[data-city]'); if(!b) return;
  S.city = b.dataset.city; loadView();
};
header(); loadLive(); loadCountries(); loadView(); setInterval(loadLive, 60000);
</script>"""


def main():
    if "--demo" in sys.argv:
        ga = Demo()
    else:
        prop = os.environ.get("GA_PROPERTY") or input("GA property id (numbers only, GA -> Admin -> Property details): ").strip()
        key = os.environ.get("GA_KEY") or input("Path to the service-account key (JSON): ").strip()
        ga = GA(prop.replace("properties/", ""), Auth(key))
        ga.auth.get()  # fail early on a bad key

    class Handler(BaseHTTPRequestHandler):
        def send(self, obj, kind="application/json"):
            data = (obj if isinstance(obj, str) else json.dumps(obj)).encode()
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            f = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
            fn = {"/api/region": region, "/api/countries": countries, "/api/live": live}.get(u.path)
            if not fn:
                return self.send(PAGE, "text/html; charset=utf-8")
            try:
                self.send(fn(ga, f))
            except Exception as e:  # show it in the page instead of a blank screen
                self.send({"error": str(e)})

        def log_message(self, *a):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)  # this computer only
    url = "http://localhost:%d/" % PORT
    print("GA viewer: %s   (Ctrl+C to stop)" % url)
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
