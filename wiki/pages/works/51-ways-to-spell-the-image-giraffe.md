---
title: "51 Ways to Spell the Image Giraffe"
type: work
tags: [artistic-research, talk, critical-ai-and-image-models, tokens]
sources:
  - ../../../data/site.json (works → 51-ways-to-spell-the-image-giraffe)
  - https://liutingchun.com/works/51-ways-to-spell-the-image-giraffe/
  - https://liutingchun.com/de/works/51-ways-to-spell-the-image-giraffe/
  - https://liutingchun.com/zh/works/51-ways-to-spell-the-image-giraffe/
  - https://media.ccc.de/v/39c3-51-ways-to-spell-the-image-giraffe-the-hidden-politics-of-token-languages-in-generative-ai
updated: 2026-10-07
---
# 51 Ways to Spell the Image Giraffe

An artistic research project and talk with Leon-Etienne Kühr, in development, on the token dictionary of image models. Image models do not read words but tokens, fragments from a fixed dictionary; CLIP's dictionary has about 49,000 of them, and "giraffe" can be spelled from it in 51 ways. The work was presented at the 39th Chaos Communication Congress (39C3, Hamburg, December 2025).

## Facts

- **Year:** 2025
- **Status:** In development (de: In Entwicklung; zh: 開發中)
- **Type:** Artistic Research, Talk
- **Type (de):** Künstlerische Forschung, Vortrag
- **Type (zh):** 藝術研究、講演
- **Materials:** CLIP tokenizer, Stable Diffusion
- **With:** Leon-Etienne Kühr
- **Link:** [Talk recording, 39C3 (media.ccc.de)](https://media.ccc.de/v/39c3-51-ways-to-spell-the-image-giraffe-the-hidden-politics-of-token-languages-in-generative-ai) (38 min, English with German translation, CC BY 4.0)
- **Page:** [https://liutingchun.com/works/51-ways-to-spell-the-image-giraffe/](https://liutingchun.com/works/51-ways-to-spell-the-image-giraffe/) · [de](https://liutingchun.com/de/works/51-ways-to-spell-the-image-giraffe/) · [zh](https://liutingchun.com/zh/works/51-ways-to-spell-the-image-giraffe/)

## Key ideas

- Before any training, the token dictionary already decides what can be pictured. Fed straight into the model, most of the 51 spellings of "giraffe" still draw a giraffe, some drift to an elephant or a horse, from the single token *giraffe* to *g|i|r|a|f|f|e*.
- Some images cannot be prompted at all because the dictionary has been sanitised (from the talk's description on media.ccc.de).
- The dictionary is built by Byte Pair Encoding: the most frequent character pairs in scraped text are merged again and again. Brand names, platform slang and hashtags become single tokens, while less common or non-English words break into long chains. The result is a hidden politics of language in image models.
- The research turns this layer into material, and in [Sixteen Tokens for a Cave](sixteen-tokens-for-a-cave.md) into a way of writing. That work was first shown as "Prompt Reconstruction" in this talk (recording 28:37–32:20).

## Related

- [Sixteen Tokens for a Cave](sixteen-tokens-for-a-cave.md)
- [Self-cannibalizing AI](self-cannibalizing-ai.md): the 37C3 talk, earlier in the same line
- [Critical AI and image models](../topics/critical-ai-and-image-models.md)
- [Chaos Communication Congress](../institutions/chaos-communication-congress.md)
- [Leon-Etienne Kühr](../people/leon-etienne-kuehr.md)
- [External links](../external-links.md)

## Sources

- ../../../data/site.json (works → 51-ways-to-spell-the-image-giraffe)
- https://liutingchun.com/works/51-ways-to-spell-the-image-giraffe/
- https://liutingchun.com/de/works/51-ways-to-spell-the-image-giraffe/
- https://liutingchun.com/zh/works/51-ways-to-spell-the-image-giraffe/
- https://media.ccc.de/v/39c3-51-ways-to-spell-the-image-giraffe-the-hidden-politics-of-token-languages-in-generative-ai
