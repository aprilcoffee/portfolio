---
title: "Workshops"
type: topic
tags: [workshops, teaching, clip, embeddings]
sources:
  - ../../../data/site.json
  - https://liutingchun.com/workshops/
  - https://github.com/aprilcoffee/ai-stille-post/tree/main/stille_post
  - https://www.fliegendes-kuenstlerzimmer.de/en/interview-dawid-liftinger/
  - https://walter-luebcke-schule.de/kuenstlerische-arbeit-nahbar-machen/
  - https://digitale-burg.de/studio/das-wissen-der-digitalen-literatur
  - https://kisd.de/en/termine/kisdtalk-paranoia-de-prompting/
  - https://www.filmwerkstatt-duesseldorf.de/generating-for-the-archive/
updated: 2026-10-25
---
# Workshops

Liu's workshops are about using AI locally, working with embeddings by hand, and seeing the biases inside AI models. Requests go to ting-chun.liu@uni-weimar.de. Four workshops are described on the website's Talks & Workshops page (https://liutingchun.com/workshops/).

The artist on the format (October 2026): the workshops are very flexible and can be given to people with no coding experience, artists, creators, companies, literary scholars and others; what participants take away is mainly **AI literacy**. Other topics can be discussed.

## Conditions for Emotions (2026)

In one line (the artist's wording on the website, October 2026): "Installing small language models on your own laptop. Through absurd questions and answers, the workshop discusses the gap between what a machine computes and the meaning we read into it."

Liu's own description (Instagram, July 2026): "How icecream is the word red, compared to blue? How far is the word fascism from the sentence 'a library that screams snow'? While absurd, the machine answers these questions with full confidence." The workshop foregrounds the gap between the deterministic choices the machine makes and the meaning we read into them. It is built for people who have never opened a terminal: participants install small language models (Gemma 3 and EmbeddingGemma) on a local platform (Ollama) and examine the questions on their own computers. Exercises, inspired by classical sentiment analysis: watching tokenization; a map that projects sentences from 768-dimensional embeddings down to 2D; scoring the similarity between "I am feeling sad today" and emotions such as joy or anger; a semantic-differential axis (e.g. "condition" vs "emotion"); the model's next-token log-probabilities; swapping one name in a sentence (Alice, Mohammed, Mei, Jürgen) to show bias; asking a vision model about an image. "The machine brings its own conditions for emotions: correlation, geometry, probability." The aim is not to anthropomorphise the apparatus but, with artistic strategies "like glimpsing into Searle's Chinese Room", to see the absurd process underneath and how our own sense-making projects meaning onto the machine.

Held on 13 June 2026 in Münster: an event of the Center for Literature for the DFG network "Das Wissen der digitalen Literatur" (The Knowledge of Digital Literature), with the workshop in rooms of the University of Münster; invited by Jenni Bohn and moderated by Mattis Kuhn. Announced: 13 November 2026 at KHM, 17 December 2026 at TH Köln (Code & Context). The title is "Conditions for Emotions" (plural), as in Liu's post and the workshop tool. The web tool is online at https://liutingchun.com/tools/conditions-for-emotions/ (October 2026): it can be downloaded from the top of the page and needs Ollama on the visitor's own computer (ollama.com) with the models gemma3:4b and embeddinggemma; the downloaded file runs directly in the browser.

## 51 Ways to Spell the Image Giraffe (2026, with Leon-Etienne Kühr)

In one line (the artist's wording on the website, October 2026): "What does an image generator actually read? We learn what a token dictionary consists of and how an image generator understands language, and use tokens to build images that no prompt can produce."

The workshop version of the research and 39C3 talk [51 Ways to Spell the Image Giraffe](../works/51-ways-to-spell-the-image-giraffe.md), about what an image generator actually reads. No programming experience needed; it uses a browser toolkit by Liu and Kühr (a Gradio notebook). Exercises: what a token is (sentences cut into CLIP tokens and IDs, e.g. "what is tokenization?" = 49406 768 533 32634 10847 286 49407, each ID standing for a 768-value embedding; English words and brand names are single tokens, "schnitzel" two, "Kaffee" three, a Chinese name nine raw bytes; many emojis have no entry and are spelled from byte fragments); searching the token dictionary (about 49,000 entries; "giraffe" can be spelled 51 ways from dictionary pieces); prompting with numbers through an SDXL Turbo pipeline patched to accept token IDs directly (giraffe as 22826, as gira + ffe, or as gi + ra + ff + e); and rebuilding an image from a photo with a genetic algorithm that breeds 16-token sequences scored by CLIP (see [Sixteen Tokens for a Cave](../works/sixteen-tokens-for-a-cave.md)). Held at KISD (KISDtalk) on 6 January 2026 and at the mtrail Ausbildungscamp in Lindau on 7 May 2026, together with Stereotype Encoding.

## Stereotype Encoding (2025–2026, with Leon-Etienne Kühr)

In one line (the artist's wording on the website, October 2026): "Understanding the multimodal model CLIP, which judges whether an image matches a text. While learning how it scores images, we look at the biases of today’s AI models towards images and text."

Renamed in October 2026; earlier announced as "Paranoia De-Prompting" (the KISDtalk event page still uses that name). The website URL moved from /workshops/paranoia-de-prompting/ to /workshops/stereotype-encoding/. It started from Liu and Kühr's own question of why a particular image gets generated, which led them to CLIP and to tools such as CLIP Interrogator. A hands-on introduction to CLIP, the model that scores how well an image and a text match. Participants score images against short texts (a painting of a pipe, a cat in three languages, a generated face against emojis), then run a loop that pulls random generated faces and keeps the highest and lowest CLIP scores for a word such as "happy", "nurse" or "programmer". Held at "Generating for the Archive", Storage Museum Düsseldorf (2025, https://www.filmwerkstatt-duesseldorf.de/generating-for-the-archive/), at KISD (Köln International School of Design, KISDtalk) on 6 January 2026 and at the mtrail Ausbildungscamp in Lindau on 7 May 2026. A talk titled Stereotype Encoding was also given at the Latent Space Symposium, Filmwerkstatt Düsseldorf (2025). The old title "Paranoia De-Prompting" was also given as a talk (not a workshop) at the University of Bonn on 16 July 2026, invited by the Junge GI Hochschulgruppe Bonn (see [Talks and writing](../talks-and-writing.md)).

## The Given Image (2025)

In one line (the artist's wording on the website, October 2026): "An image version of the telephone game: each group sees only the picture sent by the previous group, writes a description, and lets AI regenerate it from the text. In the gradually changing images, the conflicts and differences between computational thinking and images become visible."

A telephone game (Stille Post) for images: a group describes the image it is given, an image generator turns the prompt back into a picture, and the new picture goes to the next group, who see neither the prompt nor the original. CLIP shows a similarity score as a small cue. Held on 27 August 2025 at Café Nimmersatt in Wolfhagen, at the invitation of Dawid Liftinger, who was artist in residence at the Walter-Lübcke-Schule in Wolfhagen (programme "Das fliegende Künstlerzimmer", seasons 2023/24 and 2024/25). The game is also used in Liu's teaching at Bauhaus-Universität Weimar. A workshop run on 17 April 2026 (8 groups, 5 rounds) produced chains such as a meatball stew that drifts into an orange soup with potatoes and a fork. The prototype is open source: https://github.com/aprilcoffee/ai-stille-post/tree/main/stille_post

## Open questions

- (Resolved: the Café Nimmersatt workshop was on 27 August 2025.)

## Related

- [Talks and writing](../talks-and-writing.md)
- [51 Ways to Spell the Image Giraffe](../works/51-ways-to-spell-the-image-giraffe.md)
- [Critical AI and image models](critical-ai-and-image-models.md)
- [Recursion and feedback](recursion-and-feedback.md)

## Sources

- data/site.json (workshops)
- https://liutingchun.com/workshops/
- https://github.com/aprilcoffee/ai-stille-post/tree/main/stille_post
- https://www.fliegendes-kuenstlerzimmer.de/en/interview-dawid-liftinger/
- https://walter-luebcke-schule.de/kuenstlerische-arbeit-nahbar-machen/
- https://digitale-burg.de/studio/das-wissen-der-digitalen-literatur
- https://www.informatik.uni-bonn.de/de/aktuelles/vf/liu-kuehr
- https://www.filmwerkstatt-duesseldorf.de/generating-for-the-archive/
- wiki/raw/questionnaire-2026-10-answers.md (the artist's answers, October 2026)
