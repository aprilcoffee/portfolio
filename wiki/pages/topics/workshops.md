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
updated: 2026-10-24
---
# Workshops

Liu's workshops are about using AI locally, working with embeddings by hand, and seeing the biases inside AI models. Requests go to ting-chun.liu@uni-weimar.de. Three workshops are described on the website's Talks & Workshops page (https://liutingchun.com/workshops/).

The artist on the format (October 2026): the workshops are very flexible and can be given to people with no coding experience, artists, creators, companies, literary scholars and others; what participants take away is mainly **AI literacy**. Other topics can be discussed, for example anything related to tokens (see [51 Ways to Spell the Image Giraffe](../works/51-ways-to-spell-the-image-giraffe.md)).

## Conditions for Emotions (2026)

Liu's own description (Instagram, July 2026): "How icecream is the word red, compared to blue? How far is the word fascism from the sentence 'a library that screams snow'? While absurd, the machine answers these questions with full confidence." The workshop foregrounds the gap between the deterministic choices the machine makes and the meaning we read into them. It is built for people who have never opened a terminal: participants install small language models (Gemma 3 and EmbeddingGemma) on a local platform (Ollama) and examine the questions on their own computers. Exercises, inspired by classical sentiment analysis: watching tokenization; a map that projects sentences from 768-dimensional embeddings down to 2D; scoring the similarity between "I am feeling sad today" and emotions such as joy or anger; a semantic-differential axis (e.g. "condition" vs "emotion"); the model's next-token log-probabilities; swapping one name in a sentence (Alice, Mohammed, Mei, Jürgen) to show bias; asking a vision model about an image. "The machine brings its own conditions for emotions: correlation, geometry, probability." The aim is not to anthropomorphise the apparatus but, with artistic strategies "like glimpsing into Searle's Chinese Room", to see the absurd process underneath and how our own sense-making projects meaning onto the machine.

Held on 13 June 2026 in Münster: an event of the Center for Literature for the DFG network "Das Wissen der digitalen Literatur" (The Knowledge of Digital Literature), with the workshop in rooms of the University of Münster; invited by Jenni Bohn and moderated by Mattis Kuhn. Announced: 13 November 2026 at KHM, 17 December 2026 at TH Köln (Code & Context). The title is "Conditions for Emotions" (plural), as in Liu's post and the workshop tool.

## Paranoia De-Prompting (2026, with Leon-Etienne Kühr)

It started from Liu and Kühr's own question of why a particular image gets generated, which led them to CLIP and to tools such as CLIP Interrogator. A hands-on introduction to CLIP, the model that scores how well an image and a text match. Participants score images against short texts (a painting of a pipe, a cat in three languages, a generated face against emojis), then run a loop that pulls random generated faces and keeps the highest and lowest CLIP scores for a word such as "happy", "nurse" or "programmer". Held at KISD (Köln International School of Design, KISDtalk) on 6 January 2026 and at the mtrail Ausbildungscamp in Lindau on 7 May 2026. The same title was also given as a talk (not a workshop) at the University of Bonn on 16 July 2026, invited by the Junge GI Hochschulgruppe Bonn (see [Talks and writing](../talks-and-writing.md)).

## The Given Image (2025)

A telephone game (Stille Post) for images: a group describes the image it is given, an image generator turns the prompt back into a picture, and the new picture goes to the next group, who see neither the prompt nor the original. CLIP shows a similarity score as a small cue. Held on 27 August 2025 at Café Nimmersatt in Wolfhagen, at the invitation of Dawid Liftinger, who was artist in residence at the Walter-Lübcke-Schule in Wolfhagen (programme "Das fliegende Künstlerzimmer", seasons 2023/24 and 2024/25). The game is also used in Liu's teaching at Bauhaus-Universität Weimar. A workshop run on 17 April 2026 (8 groups, 5 rounds) produced chains such as a meatball stew that drifts into an orange soup with potatoes and a fork. The prototype is open source: https://github.com/aprilcoffee/ai-stille-post/tree/main/stille_post

## Open questions

- (Resolved: the Café Nimmersatt workshop was on 27 August 2025.)

## Related

- [Talks and writing](../talks-and-writing.md)
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
- wiki/raw/questionnaire-2026-10-answers.md (the artist's answers, October 2026)
