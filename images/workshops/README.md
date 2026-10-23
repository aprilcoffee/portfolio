# Workshop images

Put photos and material for the **Workshops** page here (one folder per workshop is fine,
e.g. `images/workshops/2026-weimar-local-ai/01.jpg`).

1. Add the files (or a folder), then shrink them: `python3 scripts/compress-images.py`
   (long side 2400 px, JPEG quality 82, EXIF/GPS removed; PNG/HEIC photos become `.jpg`).
2. Describe the workshop in `data/site.json` under `"workshops"` (see below), `git pull` first.
3. `python3 scripts/build.py`, commit and push.

```json
{
  "title": "Local AI in the moving-image studio",
  "year": "2026",
  "place": "Weimar", "host": "Bauhaus-Universität Weimar",
  "text": "English description.\n\nSecond paragraph.",
  "text_de": "…", "text_zh": "…",
  "images": ["images/workshops/2026-weimar-local-ai/01.jpg",
             {"src": "images/workshops/2026-weimar-local-ai/02.jpg", "alt": "Participants at the screens"}]
}
```

`title`, `year`, `place`, `host` and `text` all accept `_de` / `_zh` variants except `year`
(`title_zh`, `place_de`, …); anything empty falls back to English. Add `"hidden": true` to keep an entry offline.
