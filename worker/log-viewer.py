#!/usr/bin/env python3
"""Chat log viewer: shows what visitors asked the homepage chat and what it answered.

Runs on your own computer only (http://localhost:8790) and reads the Cloudflare D1
database "liutingchun-chat-log" through the Cloudflare API. Python 3, no packages needed.

    CLOUDFLARE_API_TOKEN=... python3 worker/log-viewer.py

The token: Cloudflare dashboard -> My Profile -> API Tokens -> Create Token ->
Custom token -> Permissions: Account / D1 / Read. Keep it on your computer only.
(Without the variable the script asks for it.)

    python3 worker/log-viewer.py --local    reads the local test database of `wrangler dev`
"""
import getpass, glob, json, os, sqlite3, sys, threading, urllib.parse, urllib.request, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_NAME = "liutingchun-chat-log"
PORT = 8790
API = "https://api.cloudflare.com/client/v4"
COLS = "id, ts, lang, country, topic, status, question, answer, links, context, tokens_in, tokens_out"


# ---------- database access: Cloudflare D1 over the API, or the local wrangler copy ----------
class Remote:
    def __init__(self, token):
        self.token = token
        acc = self.call("GET", "/accounts")[0]["id"]
        dbs = self.call("GET", "/accounts/%s/d1/database?name=%s" % (acc, DB_NAME))
        if not dbs:
            sys.exit("No D1 database named %s yet (it is created by the first chat deploy)." % DB_NAME)
        self.url = "/accounts/%s/d1/database/%s/query" % (acc, dbs[0]["uuid"])

    def call(self, method, path, body=None):
        req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                     headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)["result"]
        except urllib.error.HTTPError as e:
            sys.exit("Cloudflare API error %s: %s" % (e.code, e.read().decode()[:400]))

    def query(self, sql, params=()):
        return self.call("POST", self.url, {"sql": sql, "params": list(params)})[0]["results"]


class Local:
    def __init__(self):
        here = os.path.dirname(os.path.abspath(__file__))
        files = [f for f in glob.glob(os.path.join(here, ".wrangler/state/v3/d1/*/*.sqlite"))
                 if not f.endswith("metadata.sqlite")]
        if not files:
            sys.exit("No local database; run `npx wrangler dev` in worker/ and ask a question first.")
        self.path = files[0]

    def query(self, sql, params=()):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        try:
            return [dict(r) for r in con.execute(sql, params)]
        finally:
            con.close()


def rows(db, f):
    where, params = [], []
    for key in ("topic", "lang", "status", "country"):
        if f.get(key):
            where.append("COALESCE(%s, '') = ?" % key)
            params.append("" if f[key] == "(none)" else f[key])
    if f.get("q"):
        where.append("(question LIKE ? OR answer LIKE ?)")
        params += ["%" + f["q"] + "%"] * 2
    if f.get("from"):
        where.append("ts >= ?"); params.append(f["from"])
    if f.get("to"):
        where.append("ts < ?"); params.append(f["to"] + "T99")
    sql = "SELECT %s FROM chats%s ORDER BY id DESC LIMIT 100 OFFSET ?" % (
        COLS, " WHERE " + " AND ".join(where) if where else "")
    return db.query(sql, params + [int(f.get("offset") or 0)])


def stats(db):
    out = {"total": db.query("SELECT COUNT(*) n FROM chats")[0]["n"]}
    for key in ("topic", "lang", "status", "country"):
        out[key] = db.query("SELECT COALESCE(%s, '(none)') v, COUNT(*) n FROM chats GROUP BY v ORDER BY n DESC" % key)
    out["days"] = db.query("SELECT substr(ts, 1, 10) d, COUNT(*) n FROM chats GROUP BY d ORDER BY d DESC LIMIT 30")
    return out


# ---------- the page ----------
PAGE = r"""<!doctype html><html lang="en"><meta charset="utf-8"><title>Chat log</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font:14px/1.5 ui-monospace,Menlo,monospace;margin:0;padding:20px 24px;color:#111;background:#fff}
h1{font-size:16px;margin:0 0 4px} .muted{color:#888}
.bar{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin:12px 0}
.group{display:flex;flex-wrap:wrap;gap:4px;align-items:center} .group b{font-weight:normal;color:#888;margin-right:2px}
button.chip{font:inherit;border:1px solid #ccc;background:#fff;padding:1px 7px;cursor:pointer}
button.chip.on{background:#111;color:#fff;border-color:#111}
input{font:inherit;padding:3px 6px;border:1px solid #ccc}
.row{border-top:1px solid #eee;padding:10px 0;display:grid;grid-template-columns:150px 1fr;gap:4px 16px}
.meta{color:#888;font-size:12px} .q{font-weight:bold;white-space:pre-wrap}
.a{white-space:pre-wrap;color:#333;max-height:4.5em;overflow:hidden;cursor:pointer} .a.open{max-height:none}
.ctx{color:#888;font-size:12px} .links a{margin-right:10px;font-size:12px;color:#E4032E}
.err{color:#E4032E} #more{margin:14px 0}
@media(max-width:700px){.row{grid-template-columns:1fr}}
</style>
<h1>Chat log <span class="muted" id="total"></span></h1>
<div class="bar">
  <input id="q" placeholder="search question / answer" size="28">
  <span class="muted">from</span><input id="from" type="date"><span class="muted">to</span><input id="to" type="date">
</div>
<div class="bar" id="filters"></div>
<div id="list"></div>
<button id="more" class="chip">more</button>
<script>
var F = {}, offset = 0;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function qs(o){return Object.keys(o).filter(function(k){return o[k]}).map(function(k){return k+'='+encodeURIComponent(o[k])}).join('&')}
function get(u){return fetch(u).then(function(r){return r.json()})}
function filters(s){
  document.getElementById('total').textContent = s.total + ' questions';
  var h = '';
  ['topic','lang','status','country'].forEach(function(k){
    h += '<span class="group"><b>'+k+'</b>' + s[k].map(function(x){
      return '<button class="chip'+(F[k]===x.v?' on':'')+'" data-k="'+k+'" data-v="'+esc(x.v)+'">'+esc(x.v)+' '+x.n+'</button>'}).join('') + '</span>';
  });
  h += '<span class="group"><b>days</b>' + s.days.map(function(d){return '<span class="muted">'+d.d.slice(5)+':'+d.n+'</span>'}).join(' ') + '</span>';
  document.getElementById('filters').innerHTML = h;
}
function row(r){
  var links = []; try { links = JSON.parse(r.links || '[]') } catch (e) {}
  return '<div class="row"><div class="meta">'+esc(r.ts.replace('T',' ').slice(0,16))+'<br>'+esc(r.lang||'')+' · '+esc(r.country||'')+
    '<br>'+esc(r.topic||'—')+(r.status!=='ok'?' · <span class="err">'+esc(r.status)+'</span>':'')+
    '<br>'+(r.tokens_in||0)+' / '+(r.tokens_out||0)+' tok</div><div>'+
    (r.context?'<div class="ctx">after: '+esc(r.context)+'</div>':'')+
    '<div class="q">'+esc(r.question)+'</div><div class="a" title="click to expand">'+esc(r.answer)+'</div>'+
    '<div class="links">'+links.map(function(l){return '<a href="'+esc(l.url)+'" target="_blank">'+esc(l.title)+'</a>'}).join('')+'</div></div></div>';
}
function load(add){
  if(!add) offset = 0;
  get('/api/rows?'+qs(Object.assign({offset:offset},F))).then(function(rs){
    var list = document.getElementById('list');
    list.innerHTML = (add?list.innerHTML:'') + (rs.length||add ? rs.map(row).join('') : '<p class="muted">nothing yet</p>');
    document.getElementById('more').style.display = rs.length===100 ? '' : 'none';
    offset += rs.length;
  });
}
function refresh(){ get('/api/stats').then(filters); load(false); }
document.getElementById('filters').onclick = function(e){
  var b = e.target.closest('button'); if(!b) return;
  F[b.dataset.k] = F[b.dataset.k]===b.dataset.v ? '' : b.dataset.v; refresh();
};
document.getElementById('list').onclick = function(e){ if(e.target.classList.contains('a')) e.target.classList.toggle('open'); };
document.getElementById('more').onclick = function(){ load(true); };
var t; ['q','from','to'].forEach(function(id){
  document.getElementById(id).oninput = function(){ clearTimeout(t); t = setTimeout(function(){ F[id] = document.getElementById(id).value; load(false); }, 300); };
});
refresh();
</script>"""


def main():
    if "--local" in sys.argv:
        db = Local()
    else:
        token = os.environ.get("CLOUDFLARE_API_TOKEN") or getpass.getpass("Cloudflare API token (D1 Read): ").strip()
        db = Remote(token)

    class Handler(BaseHTTPRequestHandler):
        def send(self, body, kind):
            data = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            f = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
            if u.path == "/api/rows":
                self.send(json.dumps(rows(db, f)), "application/json")
            elif u.path == "/api/stats":
                self.send(json.dumps(stats(db)), "application/json")
            else:
                self.send(PAGE, "text/html; charset=utf-8")

        def log_message(self, *a):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)  # this computer only
    url = "http://localhost:%d/" % PORT
    print("Chat log: %s   (Ctrl+C to stop)" % url)
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
