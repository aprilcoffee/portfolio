# Log

Append-only. Newest entries at the bottom. Format: `## [YYYY-MM-DD] action | subject`.

## [2026-10-01] init | wiki created
- Schema written (CLAUDE.md), folders `raw/` and `pages/` set up.

## [2026-10-01] ingest | data/site.json (works, about, performances, site)
- 18 work pages in `pages/works/` (summary, facts, key ideas, related, sources).
- Lists generated from the CV: timeline, talks-and-writing, exhibitions-and-performances, teaching-education-awards.
- Written: overview, faq, 8 topic pages, 3 people pages, 6 institution pages.

## [2026-10-01] ingest | posts/*.md (titles and excerpts only)
- blog-archive page; blog links added to related works (Imaginary Landscape, Segmentary Moonlight, Light Segment, I kept repeating…, Take Off the Clothes, Message in a Bottle).
- Open: the full post texts (Mandarin) are not yet summarised page by page.

## [2026-10-01] add | site map and links
- pages/site-map.md: every page of the website (en/de/zh) and every external link, generated from data/site.json by scripts/wiki-sitemap.py (run on every site build and before every chat deploy). The chat recommends links only from the wiki.

## [2026-10-01] schema | chat voice
- CLAUDE.md: "The chat's voice" — facts strictly from the wiki; interpretation, connections, general context and playful answers allowed when marked as readings. The Worker's rules were loosened to match.

## [2026-10-01] add | external links
- Added: Stifterverband fellow page (teaching-education-awards, timeline, overview, institutions/bauhaus-university-weimar); Museum Angewandte Kunst AI-Worlding page (exhibitions-and-performances, timeline, works/steering-through-the-inner-residue, people/leon-etienne-kuehr); Synthiola page (works/just-jailbreak); Leon-Etienne Kühr's website (people/leon-etienne-kuehr).
- The first three URLs are also in data/site.json (CV `url`, work `links`). leon-etienne.com is wiki-only and was not fetched (robots check timed out).

## [2026-10-01] ingest | external pages, thesis, Stereotype Encoding
- Read in full: the thesis site (prologue, introduction, loss function, optimized noise, materiality, outlook, bibliography), the Academia text *Stereotype Encoding*, ground zero essay *Poetic Materialization*, and the pages of organisers (media.ccc.de 37C3/38C3/39C3, Screen Walks, Filmwerkstatt Düsseldorf, AI-Worlding, Staatstheater Darmstadt, Expanded Conference, Ars Electronica, KHM soft rotation, Correlations, FH Dortmund, TEDA poster).
- New pages: external-links; texts/heat-as-generative-image-making, texts/stereotype-encoding, texts/on-the-materiality-of-artificial-intelligence, texts/poetic-materialization-regarding-midjourney; institutions/filmwerkstatt-duesseldorf, institutions/kitegg-unlearn-ai.
- Touched: talks-and-writing, exhibitions-and-performances, overview, faq; works latent-heat-generation, self-cannibalizing-ai, steering-through-the-inner-residue, interpolation-of-the-invisible-color; topics material-infrastructure-of-ai, recursion-and-feedback, critical-ai-and-image-models; institutions chaos-communication-congress, bauhaus-university-weimar, storage-museum-duesseldorf, khm-cologne, fiff; people leon-etienne-kuehr.
- Schema: new page type `text` (CLAUDE.md, scripts/wiki-lint.py).
- Open (kept, not resolved): the CV dates *Generating for the Archive* and the *Stereotype Encoding* talk 2026 where the organiser says November 2025, and the Dortmund lecture 2024 where the page says 2025; the thesis site shows 2024-03-27 as date; the *un/learn ai* article text could not be read; leon-etienne.com could not be opened; FIfF's winners page showed no 2025 entry when checked.

## [2026-10-01] fix | Filmwerkstatt Düsseldorf dates
- CV (data/site.json) corrected to the organisers' dates: *Generating for the Archive* and the *Stereotype Encoding* symposium talk are 2025 (28 and 29 November 2025), not 2026.
- Touched: timeline, talks-and-writing, institutions/filmwerkstatt-duesseldorf, external-links, topics/archives-and-institutions. Still open: the Dortmund lecture (CV 2024, organiser 2025).

## [2026-10-01] ingest | Chaya Shen, Weimar staff page, chat style
- New page: people/chaya-shen (from chayashen.info about page, her CJD essay, KHM and ground zero pages; projects pages could not be read).
- Touched: external-links, teaching-education-awards (Weimar staff page link, now also the CV link in data/site.json).
- CLAUDE.md: the chat uses no dashes as punctuation.

## [2026-10-01] fix | chat links, Chaya Shen page trimmed
- people/chaya-shen cut to a short note: her topics (body, medicine) leaked into answers about Liu. Her site is listed with the friends (data/site.json, so in Site map and links).
- worker RULES: links from Site map and External links, URLs copied exactly, wiki paths are not web pages, people pages are not about Liu. chat.js drops URLs written in answer text.

## [2026-10-04] links | CV entries
- 29 CV entries in data/site.json got links to organisers', institutions' or publishers' pages (each opened and checked for Liu's name or the exact event); the Screen Walk entry now points to the event page.
- scripts/wiki-sitemap.py: site-map now lists every CV entry that has a link, so the chat can recommend them.
- Open: soundings Xtra (CV 2022, KHM page 19 October 2023).

## [2026-10-04] fix | CV from the artist
- soundings Xtra is 2023 (KHM page, 19 October 2023); linked. KISDtalk and NTHU talk linked (links from the artist). Vienna entry reworded: Erasmus+ Staff Mobility for Teaching (not a Lehrauftrag).
- Touched: exhibitions-and-performances, timeline, teaching-education-awards, faq.
