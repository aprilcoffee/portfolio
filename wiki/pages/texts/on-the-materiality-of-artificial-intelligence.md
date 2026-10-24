---
title: "On the Materiality of Artificial Intelligence (text and talk)"
type: text
tags: [text, talk, materiality, gpu, semiconductors, taiwan, kitegg]
sources:
  - ../../../data/site.json (about.sections, Publications & Writing 2025; Talks 2024)
  - https://unlearn.gestaltung.ai/de/article/gpm91yc8?chunks=gpm91yc8
  - https://openscience.ub.uni-mainz.de/items/7d8cb85f-0e1a-409e-b9a1-a9dac96e48a0
  - https://ground-zero.khm.de/correlations/
  - https://aprilcoffee.github.io/heat_as_image/
  - ../../raw/texts/on-the-materiality-of-ai.md
updated: 2026-10-24
---
# On the Materiality of Artificial Intelligence (text and talk)

A short English essay by Ting-Chun Liu, printed as "On the Materiality of AI" in volume 3 of *un/learn ai – integrating AI in aesthetic practices* (KITeGG research project, 2025, pp. 218–223) and readable online on the project's website. It follows AI image generation down from the screen to the hardware: NVIDIA GPUs and CUDA, quartz from Spruce Pine, wafers, ASML's EUV lithography and finally TSMC in Taiwan. Its central claim is the "Taiwan dilemma": to protect its own sovereignty through the *Silicon Shield*, Taiwan must help accelerate a computing system that undermines sovereignty elsewhere, so "silicon is not neutral". The text frames itself as part of the artistic research documented in [Heat as (Generative) Image Making](heat-as-generative-image-making.md); the same title was Liu's lecture at the Correlations forum in Offenbach in December 2024.

## Facts

- **Text:** "On the Materiality of AI" (CV title: *On the Materiality of Artificial Intelligence*), single author, in: *un/learn ai – integrating AI in aesthetic practices*, vol. 3, pp. 218–223, Forschungsprojekt KITeGG, Mainz 2025. English only (the German site marks it "Dieser Artikel ist nur auf Englisch verfügbar"). Online article: https://unlearn.gestaltung.ai/de/article/gpm91yc8?chunks=gpm91yc8
- **Volume:** edited by Matthias Grund, Johanna Teresa Wallenborn, Lasse Scherffig and Florian Jenett; open access, CC BY 4.0; DOI 10.25358/openscience-13020; repository page https://openscience.ub.uni-mainz.de/items/7d8cb85f-0e1a-409e-b9a1-a9dac96e48a0
- **Talk:** *On the Materiality of Artificial Intelligence*, Correlations – Forum für KI in Kunst und Design, HfG Offenbach, 11–13 December 2024. https://ground-zero.khm.de/correlations/ The essay itself mentions this talk: Liu passed wafer pieces round the audience there.
- **Figure:** one full-page map by Liu, *The Making of Graphic Cards (Nvidia RTX 4090)*, a world map of the supply chain from raw quartz to the finished card.
- **Research context:** the essay ends "This writing is part of an artistic research documented at: https://aprilcoffee.github.io/heat_as_image/".
- **Project behind the book:** KITeGG, five German design schools; see [KITeGG and un/learn ai](../institutions/kitegg-unlearn-ai.md).

## Argument, section by section

### Introduction: a tweet, a hum
The essay opens with Sam Altman's 2023 post: "we have re-enabled chatgpt plus subscriptions! thanks for your patience while we found more gpus". For Liu this shows how "complex networks expose themselves only when certain nodes malfunction": the AI industry depends on centralised chip production, heavy energy use and supply chains that create environmental and political tension. Langdon Winner is cited for the idea that conflicts and alliances are settled not only in political institutions but in physical infrastructure, "steel, concrete, wires, and semiconductors". The stated subject is how Taiwan's chip industry, especially TSMC, creates both technological dependency and geopolitical vulnerability, and how the *Silicon Shield* "paradoxically requires accelerating technological systems that potentially undermine sovereignty elsewhere". The personal frame is the laptop fan humming while he writes, "quietly cooling down trillions of transistors that were once grains of sand", a sign of "a constellation of silicon, metal, and code in operation".

### Main part: the artist as consumer
"Technology is a complex, shifting, recursive landscape." Following Simon Penny, artists who work with technology are inevitably entangled in consumer commodity economics, and Liu calls this a "feedback loop". His example is his own: OpenAI's first DALL·E produced "strange compositions that felt uncanny and raw, qualities that today's polished outputs have eliminated"; he wanted to work with them, but access was removed when the model became outdated, and he could not run alternatives locally for lack of hardware. The essay prints the line of PyTorch code that decides this, `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")`.

### GPUs and CUDA as gatekeeping
Midjourney, DALL·E, Stable Diffusion and ChatGPT were all trained on NVIDIA data-centre GPUs, notably the A100; ChatGPT alone is estimated to have needed 20,000 to 30,000 A100s to train. GPU cores built for 3D games suit the massive, simple, repetitive arithmetic of neural networks; the turning point was AlexNet (2012). Liu writes that one of its researchers, Alex Krizhevsky, then went to NVIDIA to develop CUDA, the proprietary parallel computing framework (stated as in the text). A printed CUDA `RuntimeError` ("Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False...") stands for the dependency: most models expect CUDA, which runs only on NVIDIA hardware, so the hardware is "not just a technical choice but a gatekeeping mechanism".

### From sand to wafer
Chips begin as quartz (silicon dioxide), common as sand, but production needs "unnatural purity at 99.9999999%". Only two companies control extraction and refinement, both in Spruce Pine, North Carolina; the silicon then goes to companies in Japan to become wafers. At the Correlations forum Liu passed wafer pieces round: the audience is always struck by their delicacy, since even slight touches leave grease marks, which is why manufacturers need ultra-clean environments.

### Lithography as chokepoint
The critical bottleneck is lithography. Only the Dutch company ASML makes the EUV machines needed for advanced chips, with 100% market share and machines costing over $150 million each, a monopoly with "profound political leverage", as US export bans on sales to China show. The figure maps the wider chain: quartz from Covia and American Elements (US) and Universal Quartz (India); silicon and wafers from Shin-Etsu (Japan); ZEISS optics (Germany) and Oxford Instruments etching systems (UK) feeding ASML (Netherlands); Synopsys EDA software and NVIDIA design (US); SK Hynix memory (Korea); fabrication at TSMC, packaging at ASE (Taiwan) and assembly at Foxconn (Taiwan/China), ending in an RTX 4090.

### TSMC as a political artefact
All of this converges at TSMC, which made about 90% of advanced semiconductors in 2022; there NVIDIA's layouts are etched with ASML machines. TSMC's dominance is historical, not natural: founded in 1987, at the end of forty years of martial law, it filled the gap left when US pressure (the 1986 US–Japan Semiconductor Agreement) pushed Japan out of chip dominance. A Taiwan moving from authoritarian rule to democracy recruited Morris Chang, a Taiwanese-American engineer, to found the world's first dedicated foundry, building Taiwan into "a geopolitical hinge" where "sand from North Carolina becomes the foundation of our digital world".

### The Taiwan dilemma
In 2021 Taiwan had its worst drought in a century; the high-tech industry was kept going with government support, "often at the expense of the general populace", while chip shortages brought the industry under scrutiny. President Tsai Ing-wen restated the *Silicon Shield*: chip dominance as economic leverage and deterrent against Chinese aggression. So "Semiconductor is not just a technical asset—it's a geopolitical instrument of sovereignty", and the dilemma follows (italic in the original): "*protect its sovereignty, Taiwan must help accelerate a system that undermines sovereignty elsewhere and generates new crises*. What protects this one island may destabilize others. Silicon is not neutral." Silicon underpins generative AI and militarised computing: fighter jets with TSMC-made chips were deployed by the Israeli government in Gaza; US and European Chip Acts restricting China make Taiwan "the pivot point in an emerging techno-political order". TSMC's origins show that advanced computation "was never the result of free markets alone". The chips now run generative AI, predictive policing, algorithmic governance and "synthetic culture", yet "There is no guarantee that Taiwan itself will not be made expendable."

### Conclusion
"AI is more than the symbol of clouds or the tireless server room at work; its material foundations are inseparable from its geopolitical nature." The question is "not simply who is responsible for these systems, but how we choose to engage with the collective systems we are all, to some degree, complicit in." The essay closes on the fan again: to work with AI is "to work with these contradictions, to remain close not only to the surface of the output, but also the condition that shaped it—the layers beneath, the labor behind, the heat in circuits, the extracted nature within networks, the intangible infrastructure, and the silent hum behind the interface."

## People, companies and sources named

Sam Altman (tweet, 2023), Langdon Winner, Simon Penny, Alex Krizhevsky and AlexNet (2012), Morris Chang, Tsai Ing-wen; NVIDIA (A100, RTX 4090, CUDA), OpenAI (DALL·E, ChatGPT), Midjourney, Stable Diffusion, ASML, ZEISS, Oxford Instruments, Shin-Etsu, SK Hynix, Synopsys, TSMC, ASE, Foxconn, Covia, American Elements, Universal Quartz; the 1986 US–Japan Semiconductor Agreement; US and European Chip Acts. The supplied copy shows only note 1 (Altman); the other notes (2–14) were not legible.

## Key ideas for the chat

- **Materiality against the cloud.** The essay is the compact version of the thesis chapter "Materiality of Artificial Intelligence" in [Heat as (Generative) Image Making](heat-as-generative-image-making.md): the same chain of GPU, quartz, wafer, EUV, TSMC and Taiwan, shortened to six pages and one map.
- **The hum as method.** It begins and ends with the laptop fan. Heat and noise, the by-products, are where the material system becomes perceptible; the same idea drives [Latent Heat Generation](../works/latent-heat-generation.md), where waste heat becomes the image.
- **Feedback beyond the machine.** "Feedback loop" here is economic: the artist's tools depend on a consumer market, and losing access to old DALL·E is a loss of an aesthetic. This links the cybernetic language of [Recursion and feedback](../topics/recursion-and-feedback.md) to political economy.
- **Error messages as evidence.** Code and a CUDA error are quoted as material documents of dependency, not as decoration.
- **A situated, complicit position.** Written by a Taiwanese artist about the infrastructure his own country supplies, it refuses neutrality ("Silicon is not neutral") and also refuses easy blame: everyone is "to some degree, complicit".

## Open questions

- The essay says Alex Krizhevsky was employed by NVIDIA to develop CUDA after AlexNet (2012). General histories date CUDA to 2006–2007 and place Krizhevsky at Google after 2012; ask the artist whether this sentence should be read differently (the chat should repeat it only as the essay's wording).
- Notes 2–14 are not legible in the supplied PDF; the full references are in the printed volume and on the online article.
- Title: the printed article is headed "On the Materiality of AI"; the CV and talk use "On the Materiality of Artificial Intelligence". Same text.

## Related

- [The material infrastructure of AI](../topics/material-infrastructure-of-ai.md)
- [Heat as (Generative) Image Making](heat-as-generative-image-making.md)
- [Latent Heat Generation](../works/latent-heat-generation.md)
- [KITeGG and un/learn ai](../institutions/kitegg-unlearn-ai.md)
- [Chaos Communication Congress](../institutions/chaos-communication-congress.md) (the 38C3 talk *arafed futures* covers related ground)
- [Talks and writing](../talks-and-writing.md)
- [External links](../external-links.md)

## Sources

- https://gestaltung.ai/en#publications (KITeGG publications, where the un/learn ai volumes are listed)

- data/site.json, about.sections: Publications & Writing (2025) and Talks (2024)
- https://unlearn.gestaltung.ai/de/article/gpm91yc8?chunks=gpm91yc8
- https://openscience.ub.uni-mainz.de/items/7d8cb85f-0e1a-409e-b9a1-a9dac96e48a0
- https://ground-zero.khm.de/correlations/
- https://aprilcoffee.github.io/heat_as_image/
- Text supplied by the artist, October 2026 (PDF of the printed pages; transcript in [raw/texts/on-the-materiality-of-ai.md](../../raw/texts/on-the-materiality-of-ai.md))
