---
title: "Stereotype Encoding: How AI Images Learn Cultural Bias (text)"
type: text
tags: [text, clip, bias, latent-space, collaboration]
sources:
  - https://www.academia.edu/165438573/Stereotype_Encoding_How_AI_Images_Learn_Cultural_Bias
  - https://www.filmwerkstatt-duesseldorf.de/latent-space-symposium/
  - https://aprilcoffee.github.io/heat_as_image/loss-function/statistical-index.html
updated: 2026-10-01
---
# Stereotype Encoding: How AI Images Learn Cultural Bias (text)

A 20-page text by Ting Chun Liu and Leon-Etienne Kühr, published in 2025 in *LATENT SPACE – LATENZ*, a project of the Filmwerkstatt Düsseldorf. It argues that image models such as CLIP link pictures and words through statistical closeness, not cause, and that this turns cultural assumptions into mathematics that looks neutral: "stereotype encoding". The argument is carried by small artistic experiments with faces, food, aesthetic scores and a map of 650,000 images.

## Facts

- **Authors:** Ting Chun Liu and Leon-Etienne Kühr
- **Where:** *LATENT SPACE – LATENZ*, Filmwerkstatt Düsseldorf, 2025, 20 pages. Read online: https://www.academia.edu/165438573/Stereotype_Encoding_How_AI_Images_Learn_Cultural_Bias
- **Talk with the same title:** Latent Space Symposium, Filmwerkstatt Düsseldorf, Saturday 29 November 2025 (afternoon session with Ludovica Schaerf and Hedda Roman). See [Filmwerkstatt Düsseldorf](../institutions/filmwerkstatt-duesseldorf.md).
- **Listed in the CV** as a 2025 publication and as a 2026 talk (see Open questions).

## Argument, section by section

1. **Material presence and statistical correlation.** Starts from medium specificity (Greenberg; Sol LeWitt shifting attention from representation to material) and photographic indexicality (Peirce's physical causation, Barthes' "certificate of presence"). Digital images already loosened the link to a material substrate (Mary Ann Doane). AI images bring "statistical indexicality": reference by "learned correlations rather than causal connections", "probabilistic pattern matching" instead of a light trace.
2. **Geometry of meaning.** CLIP (OpenAI, 2021) is trained on 400 million image-caption pairs with two encoders, a vision transformer and a text transformer, and compares them by cosine similarity in a shared embedding space. It does not generate images; its similarity scores guide diffusion models. Zero-shot classification and contrastive learning explained. ZeroCap's vector arithmetic ("German flag + Obama − America = Angela Merkel") gives "algorithmic semiosis": meaning that looks sound but is computed purely statistically.
3. **Exposing bias through artistic research.** Technical benchmarks are not enough; artistic practice works "not as an illustration of technical insights but as a research methodology". Cites Buolamwini and Gebru (face recognition near 99% accuracy for white men, failing about half the time for Black women) and the "coded gaze".
4. **The happiest person.** Hundreds of random faces from ThisPersonDoesNotExist are picked again and again by their CLIP score for "happy". The result is not a happy face but "the statistical average of visual patterns". The same method with "nurse" and "art" shows gender and racial bias as mathematical relationships.
5. **Food-face correlations.** Scoring synthetic faces against cuisines, Caucasian-looking faces lean to "schnitzel", others to "dumpling" and "kimchi". CLIP learned this only from closeness in its data. Definition: stereotype encoding turns cultural assumptions into "computational infrastructure that appears mathematically neutral while reproducing ideological content".
6. **Visualizing cultural clusters.** About 650,000 images encoded with CLIP and projected with UMAP.
   - *Aesthetic scoring:* Stable Diffusion 1.x was trained on LAION-Aesthetics, which cut about 5.8 billion web images to those scoring above roughly 5 to 6 out of 10; the predictor itself was trained on AVA, ratings of competitive photography, so a mostly Western professional taste became "foundational".
   - *NSFW filtering:* safety filters rest on "exactly 17 predetermined unsafe concepts". Coloured by NSFW score, the highest regions were "almost exclusively" images of female-presenting people, much of it harmless, reflecting how much pornography is on the web.
   - *Copyright islands:* clusters of branded and franchise imagery, sometimes bridged oddly (Star Wars to the chef Paul Bocuse via Disney's acquisitions and theme parks), because "semantic association is driven by co-occurrence".
7. **The algorithmic trace.** Photography records a moment of contact; these systems "accumulate approximations rather than singular moments of contact". They are "cultural artifacts that reproduce and amplify the power structures embedded in their data and algorithms", and biased output can re-enter visual culture and training data, creating feedback loops.

## Key terms

- **Statistical indexicality:** reference through learned correlation, not causal contact.
- **Stereotype encoding:** cultural assumptions turned into computation that looks neutral.
- **Algorithmic semiosis:** meaning made by operations that only look semantically sound.
- **Copyright islands:** clusters of repeated advertising and pop-culture images in the embedding map.
- **Coded gaze:** bias built into systems (Buolamwini).

## Models, datasets, sources named

CLIP, ZeroCap, Stable Diffusion 1.2–1.5, LAION-Aesthetics, AVA, ThisPersonDoesNotExist, UMAP; Greenberg, LeWitt, Peirce, Barthes, Doane, Buolamwini and Gebru, Levi and Gilboa (2024), Rando et al. (2022).

## Key ideas for the chat

- The same experiments (happiest face, food and faces, vector arithmetic) also appear in Liu's thesis, [Heat as (Generative) Image Making](heat-as-generative-image-making.md), where the author's own face is among those scored.
- It extends the talks on aesthetic scoring and NSFW filters in [Self-cannibalizing AI](../works/self-cannibalizing-ai.md).
- The argument runs against "neutral" AI: a model's idea of beauty, safety and a "typical" person comes from filtered data and a few chosen words.

## Open questions

- The CV lists the text under 2025 publications, and lists the symposium talk under 2026; the organiser's page dates the symposium 29 November 2025.

## Related

- [Critical AI and image models](../topics/critical-ai-and-image-models.md)
- [Leon-Etienne Kühr](../people/leon-etienne-kuehr.md)
- [Heat as (Generative) Image Making](heat-as-generative-image-making.md)
- [External links](../external-links.md)

## Sources

- https://www.academia.edu/165438573/Stereotype_Encoding_How_AI_Images_Learn_Cultural_Bias
- https://www.filmwerkstatt-duesseldorf.de/latent-space-symposium/
- https://aprilcoffee.github.io/heat_as_image/loss-function/statistical-index.html
