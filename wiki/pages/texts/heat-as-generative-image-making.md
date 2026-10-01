---
title: "Heat as (Generative) Image Making (diploma thesis)"
type: text
tags: [thesis, diploma, material-infrastructure-of-ai, cybernetics, taiwan, weizenbaum]
sources:
  - https://aprilcoffee.github.io/heat_as_image/index.html
  - https://aprilcoffee.github.io/heat_as_image/prologue.html
  - https://aprilcoffee.github.io/heat_as_image/introduction/index.html
  - https://aprilcoffee.github.io/heat_as_image/loss-function/index.html
  - https://aprilcoffee.github.io/heat_as_image/optimized-noise/index.html
  - https://aprilcoffee.github.io/heat_as_image/materiality/index.html
  - https://aprilcoffee.github.io/heat_as_image/outlook.html
  - https://aprilcoffee.github.io/heat_as_image/bibliography.html
  - https://github.com/aprilcoffee/heat_as_image
  - https://www.fiff.de/fiff-kommunikation/2026/1/
updated: 2026-10-01
---
# Heat as (Generative) Image Making (diploma thesis)

Liu's diploma thesis at the Academy of Media Arts Cologne (KHM) is a web-based text that asks how heat, physical and metaphorical, shapes our understanding of AI-generated images: "from the warmth of GPUs to the geopolitical heat of semiconductor manufacturing". It walks from the code that makes an image, through the mathematics of diffusion models, down to the sand, cleanrooms and Taiwanese factories behind the chips, and ends in a position "somewhere between fascination and critique, between participation and resistance". It received the Weizenbaum-Studienpreis 2025 ([FIfF](../institutions/fiff.md)). The artwork that grew out of it is [Latent Heat Generation](../works/latent-heat-generation.md).

## Facts

- **Author:** Ting-Chun Liu, Academy of Media Arts Cologne. Written in the first person.
- **Form:** a website with chapters and sections, read page by page: https://aprilcoffee.github.io/heat_as_image/index.html
- **Code:** https://github.com/aprilcoffee/heat_as_image (MIT licence). GPU temperature is read, sent over OSC to StreamDiffusion in TouchDesigner, the image goes by NDI to a Processing visualisation, and Parler TTS adds a voice that speaks back. Needs an NVIDIA RTX card, Windows 10/11, Python 3.8+, TouchDesigner 2023+, Processing 4, CUDA 12.1.
- **Essay version:** *Heat as (Generative) Image Making*, FIfF-Kommunikation 1/26, p. 64 (essay for the Weizenbaum-Studienpreis).
- **Bibliography:** 43 entries, from Wiener and Turing to *Chip War* and *Atlas of AI*.
- **Date:** the site's title block shows "2024-03-27"; see Open questions.

## What the thesis says, chapter by chapter

### Prologue
Seven lines of Python with the Hugging Face Diffusers library and Stable Diffusion v1-5 produce "a photorealistic image of a functioning NVIDIA graphic card". The model is small enough to run locally on modest hardware, and those seven lines have been "integral" to Liu's practice. The text sets a gap against everyday life: the same person struggles to connect a computer to a wireless printer. The prologue also names the hardware layers (CUDA for NVIDIA, ROCm for AMD, MPS for Apple, OpenCL) and explains latent diffusion with a Variational Autoencoder in plain words.

### Introduction
- **Position.** AI "imitates human thought through computational means, but its capabilities are often mistakenly trusted"; it is "neither genuinely artificial nor truly intelligent" but pattern recognition built on mathematical prediction. It is profoundly material, inseparable from semiconductors, and tied to geopolitics.
- **A (possibly) cybernetic approach.** Cybernetics, from Greek *kybernētēs* (steersman), is used as a way of studying feedback loops and regulation. Sources: Wiener, Shannon's joke that the word is useful because nobody knows what it means, Margaret Mead's "Cybernetics of Cybernetics", Yuk Hui, Beatrice Fazi (*Contingent Computation*, "aesthetic as an ontological novelty"), Andrew Pickering, Matthew Fuller's lecture "Art as Metadiscipline" (KHM, 9 May 2023), Rosa Menkman. AI is treated as "open-ended inquiry" rather than a black box. A recurring tension is recursion: how deep to follow a technology's infrastructure without losing the practice, told through cooking and heat.
- **The unexpected imagery.** The path from generative art, to visualising computational heat in [Sun](../works/sun.md) (p5.js, orange gradient particles), to AI images as raw material in [Imaginary Landscape](../works/imaginary-landscape.md) (interpolation and shaders in Processing). Heat is "the invisible yet tangible byproduct of computation", produced by electrical resistance in chips.
- **Because my computer can't run.** Running out of memory with Stable Diffusion during the pandemic chip shortage showed that AI "is not merely code; it relies heavily on silicon, electricity, water, and human labor". Names NVIDIA's hold on CUDA, TSMC, Morris Chang, Taiwan's "Silicon Shield" and the EU Chips Act.
- **Note for the future self.** Written as a student turning teacher: technology is layered abstraction nobody grasps alone, yet inseparable from society; teaching it means presenting "every algorithm as also a proposition"; technology is tool, subject, medium and message at once. Footnote to Georg Trogemann, "The 18th Camel and The Habitats of Thought".

### The Loss Function in Our Practices
A loss function is the mathematical gap between a network's output and the desired outcome; with backpropagation and gradient descent it forms "a self-correcting feedback loop that is cybernetic in principle". The chapter asks whether an algorithm could work as a critique, "a mathematical sense of judgment of 'this is not what I want'", and concludes that a loss function is "a moving interplay between our guidance and the machine's iterative trial-and-error". Sections:

- **What you see is not inside the machine.** Working with a generative system is conversing, not observing. The appearance that a response is chosen at random makes it seem "already there inside the computer"; phrases like "the AI dreamed up an image" reinforce a false interior.
- **The purple coincidence.** Stable Diffusion's img2img run in a loop with no text prompt (`while True: image = m.run(img=image)`) drifts, whatever the start image, into "a purple, noisy texture". Following that led into the model's parts. Refers to Alvin Lucier's *I Am Sitting in a Room* and the 37C3 talk with Leon-Etienne Kühr ([Self-cannibalizing AI](../works/self-cannibalizing-ai.md)). Lesson: "AI image generation is not a single black box but a system of interconnected pipelines."
- **Eliza effect.** Turing's imitation game began as a test of telling a man from a woman by text; Weizenbaum's ELIZA (1966) moved people although they knew it was a script; Berry and Ciston's archive work shows inconsistencies in the accounts. ELIZA showed "how easily we assign meaning", exposing "our own human loss function".
- **Specificity in imaging.** Greenberg's medium specificity, Sol LeWitt ("a drawing of a line is a real line"), photography's indexicality (Barthes' "certificate of presence"), digital "ontological uncertainty" (Mary Ann Doane). Question: do AI images have a medium-specific trace?
- **Statistical index and embeddings.** CLIP, shared text-image space, cosine similarity, ZeroCap's vector arithmetic. Experiments: searching for the "happiest" generated face; pairing faces with food names, where Caucasian faces lean to "schnitzel" and Liu's own face to "dumpling" and "kimchi". The trace "no longer relies on light or contact, but on accumulated approximations and weighted distances in embedding space". The same experiments are developed in [Stereotype Encoding](stereotype-encoding.md).

### Optimized Noise Maker
Stable Diffusion as latent diffusion: a denoising model steered by text through cross-attention. Sections:

- **Measuring coffee.** A nine-step personal coffee routine as an algorithm; the 1991 Cambridge coffee-pot camera (128×128 greyscale, shared over a network); the Hyper Text Coffee Pot Control Protocol (RFC 2324); edge detection turning "is there coffee" into a maths problem.
- **Computer vision.** Convolutions work "like squinting your eye", pooling keeps the strongest features, layers go from edges to forms. The image becomes "a language of features and abstractions".
- **Self-critic machine.** GANs: a generator and a discriminator that criticises. *Portrait of Edmond de Belamy* (Obvious, trained on 15,000 portraits, $432,500 at Christie's, 2018); Philipp Schmitt's *Humans of AI* and *Declassifier* (YOLO, COCO) as ways of showing how machines segment the world.
- **A biochemical problem.** U-Net (Ronneberger, Fischer, Brox, 2015) came from biomedical segmentation: a contracting path that distils features, an expanding path that rebuilds the image, skip connections that keep detail. It reaches its limit when imagination is needed.
- **Attending to attention.** Queries, keys and values, softmax, cross-attention; "a tokenized sentence becomes a sequence of seeds". Machine attention resembles selection but lacks body and emotion.
- **Denoising.** DDPM forward and reverse diffusion, with U-Net, CLIP, latent diffusion and VAE. Rare features are treated as noise: if few training images show non-binary gender presentation the model may "wash out" ambiguity; each step averages towards popular internet imagery. Diffusion models "reflect the values of their users", and their look is "made possible by vast calculation on electronics".

### Materiality of Artificial Intelligence
Opens with Sam Altman's December 2023 post on re-enabling ChatGPT Plus after "finding more GPUs", and Langdon Winner's line that politics is settled in "steel and concrete, wires and semiconductors". Written from the position of a Taiwanese artist, treated as personal, not only academic. A laptop's fan noise stands for hidden layers; heat is electricity's by-product. Sections:

- **Art as commodity and commodity as art.** Simon Penny: artists using new technologies also engage consumer economics. Examples: Jeffrey Shaw's *The Legible City* (1989), ART+COM's TerraVision (1994), early DALL·E before polish. Liu's own ladder from Arduino to Raspberry Pi to GPUs, and Wirth's law (software slows faster than hardware speeds up). The irony of criticising a system from inside it.
- **Graphics Processing Units.** About 20,000–30,000 A100s estimated to train ChatGPT; A100 (2020, 54.2 billion transistors, TSMC 7 nm); RTX 4090 (76.3 billion, TSMC 4 nm, about 450 W); Stable Diffusion 1.5 needs about 10 GB VRAM. AlexNet (2012) set GPUs as the standard; CUDA makes NVIDIA the gatekeeper; market value above three trillion dollars in June 2024.
- **Sand, quartz and silicon.** Transistor-grade quartz comes from one place, Spruce Pine, North Carolina, at 99.9999999% purity, refined by two companies (The Quartz Corp, Covia).
- **All touches leave marks.** Liu bought wafers on eBay (about 5 EUR each) and passed them round at a presentation at hfg Offenbach; fingerprints show at once. Wafer supply: Shin-Etsu Handotai, SUMCO, Siltronic; Czochralski process, slicing, lapping, polishing, in cleanrooms.
- **Cleanrooms and chokepoints.** EUV lithography at 13.5 nm; ASML has the whole market for the most advanced machines (over $150 million each), with ZEISS mirrors. The suits protect "the machine from the contamination created by us". Export controls as leverage.
- **Fabrications.** TSMC makes about 90% of advanced chips (2022). Its founding in 1987 was a political act (1986 US–Japan agreement, Morris Chang recruited by Taiwan's state): "a political artifact". Source: Chris Miller, *Chip War*.
- **The Taiwan Dilemma.** The 2021 drought; the Silicon Shield; resource extraction across Nevada, Bolivia and Inner Mongolia; ChatGPT's estimated daily energy use (about 500,000 kWh). The paradox: Taiwan's chips enable generative AI, predictive policing and military computing, yet there is no guarantee Taiwan itself will not become expendable.

### Outlook and Reflection
Starts from the 2025 wave of Studio Ghibli-style image generation and Miyazaki's remark that AI images are "an insult to life itself". Artists see theft of style and labour, the public sees democratised tools, and Liu stands in a conflicted middle: "it is still people who shape the outcome". Points to artists who work with material infrastructure: Sam Ghantous (*How to Turn the Earth Inside Out*, *Your Golf Course Made My GPU*), Nadim Abbas (*Pilgrim in the Microworld*, Taipei Biennial 2023), Su Yu-Hsin (*Particular Waters*, 2023).

## Key ideas for the chat

- Heat is the thesis's thread: GPU warmth, the heat of image-making labour, and the geopolitical heat around Taiwan's chips. "Heat as image" means taking the waste product seriously as material.
- The method is practice-led: run the loop, watch where it drifts (purple), then open the pipeline part by part.
- The cybernetic frame links the thesis to [Recursion and feedback](../topics/recursion-and-feedback.md); the Taiwan chapters link to [The material infrastructure of AI](../topics/material-infrastructure-of-ai.md); the CLIP experiments link to [Critical AI and image models](../topics/critical-ai-and-image-models.md).
- It does not claim a neutral view: the author is a Taiwanese artist writing about the infrastructure his own country supplies.

## Open questions

- The site's title block gives 2024-03-27 as publication date, while the diploma is dated 2025 elsewhere on the wiki. Which is the date of the thesis, and which of the web version?
- Supervisors and acknowledgements are not named on the site.

## Related

- [Latent Heat Generation](../works/latent-heat-generation.md)
- [FIfF and the Weizenbaum-Studienpreis](../institutions/fiff.md)
- [Stereotype Encoding](stereotype-encoding.md)
- [External links](../external-links.md)

## Sources

- https://aprilcoffee.github.io/heat_as_image/ (all chapters: prologue, introduction, loss-function, optimized-noise, materiality, outlook, bibliography)
- https://github.com/aprilcoffee/heat_as_image
- https://www.fiff.de/fiff-kommunikation/2026/1/
