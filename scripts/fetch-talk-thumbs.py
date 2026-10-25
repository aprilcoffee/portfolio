#!/usr/bin/env python3
"""Give every talk recording (site.json "press", group "watch") and every own text (CV "Publications & Writing") a preview image.

For each entry without "thumb", reads the preview image the host page offers (og:image; on
media.ccc.de that is a frame of the recording), saves it as images/talks/<name>.jpg
(long side 1280 px) and writes the path into site.json. Runs in .github/workflows/build.yml
before the build; never fails it. To use your own screenshot instead, put it in images/talks/
and set "thumb" by hand (or in the admin)."""
import html, io, json, os, re, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "data", "site.json")
UA = {"User-Agent": "Mozilla/5.0 (liutingchun.com thumbnail fetcher)"}


def get(url):
    url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%")  # addresses with Chinese characters
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def og_image(url):
    page = get(url).decode("utf-8", "replace")
    for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']'):
        m = re.search(pat, page, re.I)
        if m:
            return urllib.request.urljoin(url, html.unescape(m.group(1)))


def main():
    from PIL import Image
    d = json.load(open(SITE, encoding="utf-8"))
    changed = False
    pubs = next((s for s in d.get("about", {}).get("sections", []) if s["title"].startswith("Publications")), {"items": []})["items"]
    todo = [it for it in d.get("press", []) if it.get("group") == "watch"] + pubs  # talk recordings and own texts
    for it in todo:
        if it.get("thumb") or not it.get("url"):
            continue
        try:
            src = og_image(it["url"])
            if not src:
                print("no preview image:", it["url"])
                continue
            im = Image.open(io.BytesIO(get(src))).convert("RGB")
            im.thumbnail((1280, 1280), Image.LANCZOS)
            name = re.sub(r"[^a-z0-9]+", "-", (it.get("title") or it.get("text", "")).lower()).strip("-")[:60] + ".jpg"
            rel = "images/talks/" + name
            os.makedirs(os.path.join(ROOT, "images", "talks"), exist_ok=True)
            im.save(os.path.join(ROOT, rel), "JPEG", quality=82, optimize=True, progressive=True)
            it["thumb"] = rel
            changed = True
            print("saved", rel, "from", src)
        except Exception as e:  # a host that is down must not stop the build
            print("skip %s: %s" % (it["url"], e), file=sys.stderr)
    if changed:
        with open(SITE, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
