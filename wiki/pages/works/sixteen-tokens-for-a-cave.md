---
title: "Sixteen Tokens for a Cave"
type: work
tags: [multimodal-poetry, critical-ai-and-image-models, tokens, genetic-algorithm]
sources:
  - ../../../data/site.json (works → sixteen-tokens-for-a-cave)
  - https://liutingchun.com/works/sixteen-tokens-for-a-cave/
  - https://liutingchun.com/de/works/sixteen-tokens-for-a-cave/
  - https://liutingchun.com/zh/works/sixteen-tokens-for-a-cave/
  - https://media.ccc.de/v/39c3-51-ways-to-spell-the-image-giraffe-the-hidden-politics-of-token-languages-in-generative-ai
updated: 2026-10-07
---
# Sixteen Tokens for a Cave

Multimodal poetry in token language, with Leon-Etienne Kühr, in development. Starting from a stock photograph of a sea cave, a genetic algorithm bred sixteen tokens of CLIP's dictionary over two hundred generations. Image models that took no part in the search draw a cave from them. The work reads such token sequences as poetry written for a machine: we are not the addressee, we only overhear.

## Facts

- **Year:** 2025
- **Status:** In development (de: In Entwicklung; zh: 開發中)
- **Type:** Multimodal Poetry
- **Type (de):** Multimodale Poesie
- **Type (zh):** 多模態詩
- **Materials:** Genetic algorithm, CLIP ViT-L/14, image models
- **With:** Leon-Etienne Kühr
- **Link:** [Preliminary work in the 39C3 talk, 28:37–32:20 (media.ccc.de)](https://media.ccc.de/v/39c3-51-ways-to-spell-the-image-giraffe-the-hidden-politics-of-token-languages-in-generative-ai)
- **Page:** [https://liutingchun.com/works/sixteen-tokens-for-a-cave/](https://liutingchun.com/works/sixteen-tokens-for-a-cave/) · [de](https://liutingchun.com/de/works/sixteen-tokens-for-a-cave/) · [zh](https://liutingchun.com/zh/works/sixteen-tokens-for-a-cave/)

## Key ideas

- **The sixteen tokens:** email, defeats, wallart, cave, impacting, pi, peoplesvote, blames, mcclure, 👣, croati, desk, zazzle, numerous, mediter, eleng. Fragments like *croati* and *mediter* never finish their words.
- **Method:** 16 tokens, 200 generations, population 2048; CLIP ViT-L/14 similarity to the target photograph was the fitness. The token IDs are passed to each image model directly, skipping the step where a written prompt would be cut into tokens.
- **Four models, same tokens:** FLUX.1-dev, Stable Diffusion 3.5 medium, Stable Diffusion XL and Stable Diffusion 1.5 each draw a cave, though none took part in the search.
- **CLIP similarity to the target photograph:** the sixteen tokens 0.433; a (lazy) human description, "a photo of a cave and the ocean", 0.272; ChatGPT 0.258; JoyCaption Beta One 0.271; Gemini 0.273. Because this score is what the algorithm maximised, the transfer to other models is the part that counts.
- **Reading:** poetry for a machine reader, overheard by humans; a way of writing that grows out of the token dictionary described in [51 Ways to Spell the Image Giraffe](51-ways-to-spell-the-image-giraffe.md). This is a reading of the work, not the artist's statement.
- Target photograph: Stefan Kunze / Unsplash. First shown as "Prompt Reconstruction" in the 39C3 talk, 2025.

## Related

- [51 Ways to Spell the Image Giraffe](51-ways-to-spell-the-image-giraffe.md)
- [Critical AI and image models](../topics/critical-ai-and-image-models.md)
- [Chaos Communication Congress](../institutions/chaos-communication-congress.md)
- [Leon-Etienne Kühr](../people/leon-etienne-kuehr.md)

## Sources

- ../../../data/site.json (works → sixteen-tokens-for-a-cave)
- https://liutingchun.com/works/sixteen-tokens-for-a-cave/
- https://liutingchun.com/de/works/sixteen-tokens-for-a-cave/
- https://liutingchun.com/zh/works/sixteen-tokens-for-a-cave/
- https://media.ccc.de/v/39c3-51-ways-to-spell-the-image-giraffe-the-hidden-politics-of-token-languages-in-generative-ai
