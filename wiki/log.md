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

## [2026-10-07] add | works 51 Ways to Spell the Image Giraffe, Sixteen Tokens for a Cave
- New work pages (both "In development", 2025, with Leon-Etienne Kühr), written from the artist's portfolio deck and the 39C3 recording page; site.json gained the works plus a `status` field.
- Touched: institutions/chaos-communication-congress, topics/critical-ai-and-image-models, people/leon-etienne-kuehr, external-links (pointer to the website's new Press & Media page, /press/).

## [2026-10-08] add | external mentions of Self-cannibalizing AI
- Cacini (APRJA 2024) and Unthinking Photography (Image Exhaust, 2025) added to external-links and works/self-cannibalizing-ai. Both found by web search; the pages themselves could not be opened from this environment.

## [2026-10-08] add | Expanded Conference 2026 paper
- DOI 10.1145/3840416.3840463 (given by the artist) added to the CV Publications on the website, to the work links of Steering Through the Inner Residue, and to external-links and works/steering-through-the-inner-residue. The ACM page could not be opened; the paper title is assumed to match the Art Track presentation.

## [2026-10-19] update | Expanded 2026 paper, WIP Festival
- Steering Through the Inner Residue paper: title, authors and venue checked against the artist's camera-ready PDF; it is forthcoming (DOI does not resolve yet), so the DOI link was removed from the website and no URL is given in the wiki. Only bibliographic facts are recorded; the paper's content is not summarised before publication.
- CV: WIP Arts & Technology Festival 2026 (Flows, CYENS, Nicosia, 16-25 October 2026) added under Exhibitions with Kühr, from the artist's word; role and shown work still unknown.

## [2026-10-20] update | positioning, workshops, Expanded talk, WIP, Artist Magazine
- overview: first sentence now "research-based media artist working with critical AI" (the website's new wording); workshops bullet (local AI usage, embedding practice, understanding biases in AI models).
- faq and teaching-education-awards: workshops and how to invite Liu (email; the chat keeps giving the public gmail address).
- talks-and-writing, timeline: Expanded 2026 (Art Track, Linz) added as a talk, with the speaker page; the paper is forthcoming and has no link yet.
- exhibitions-and-performances: WIP Festival 2026 is an exhibition (work shown still unknown).
- works/steering-through-the-inner-residue: materials, where it was developed, funding (hessian.AI, KITeGG/BMBF), taken from the artist's camera-ready paper PDF (credits only; the paper is not summarised).
- external-links: Artist Magazine article (page not opened, title and date unknown).

## [2026-10-21] update | Artist Magazine article
- external-links: title, author, issue and the mention of Liu (LTG, Noise Flow Practice vol.1, C-LAB) filled in from the PDF the artist supplied.

## [2026-10-21] remove | Artist Magazine article
- external-links: the 2019 Artist Magazine article (only a photo of Liu performing) taken out again at the artist's request; it is no longer on the website's Press & Media page either.

## [2026-10-24] ingest | Workshops page, Bonn talk
- topics/workshops: new page (Condition for Emotions, Paranoia De-Prompting, The Given Image); Walter-Lübcke-Schule and Dawid Liftinger checked against the programme's website.
- talks-and-writing: added the 16 July 2026 talk at the University of Bonn (Junge GI Hochschulgruppe Bonn), checked on the organiser's pages.

## [2026-10-25] update | Site restructure
- Performance page merged into Works ("Performance archive"); Press & Media split: talk recordings on "Workshops & Talks", texts by others in the About CV. faq and topics/audio-visual-performance point to the new URLs; site-map regenerated.

## [2026-10-25] update | Workshop texts
- Workshop pages rewritten to describe the exercises concretely (from the workshop screenshots): local models such as Gemma 3 / EmbeddingGemma, the distance/axis/token/next-token/name-swap/image exercises, Magritte pipe, face search scores. Chinese texts rewritten for clarity.
