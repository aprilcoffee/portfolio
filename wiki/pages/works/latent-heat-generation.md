---
title: "Latent Heat Generation"
type: work
tags: [artistic-research, material-infrastructure-of-ai, recursion-and-feedback]
sources:
  - ../../../data/site.json (works → latent-heat-generation)
  - https://liutingchun.com/works/latent-heat-generation/
  - https://liutingchun.com/zh/works/latent-heat-generation/
  - https://aprilcoffee.github.io/heat_as_image/index.html
  - https://github.com/aprilcoffee/heat_as_image
  - https://ars.electronica.art/panic/en/view/cybernetic-subjects-21338ddb450c817ab718ce48a0a628f5/
updated: 2026-11-22
---
# Latent Heat Generation

An artistic research project that makes the material side of AI visible. Thermal images of working GPUs become the base images of Stable Diffusion’s image-to-image process (not prompts), so the waste heat of computation becomes the material of the images, a recursive loop in which graphics cards look at their own physical conditions.

## Facts

- **Year:** 2025
- **Type:** Artistic Research, Video Installation
- **Type (de):** Künstlerische Forschung, Videoinstallation
- **Type (zh):** 藝術研究、影像裝置
- **Materials:** Computer, Graphics Cards, UV Wafer, Website
- **Link:** [Research notes](https://aprilcoffee.github.io/heat_as_image/index.html)
- **Clips:** 1 video file(s) on the work page
- **Page:** [https://liutingchun.com/works/latent-heat-generation/](https://liutingchun.com/works/latent-heat-generation/) · [zh](https://liutingchun.com/zh/works/latent-heat-generation/)

## Key ideas

- 'Generation' in several senses: heat, images, chip generations and the generational politics of technological dependency.
- Written from the position of a Taiwanese artist: limited in computing power, yet tied to the infrastructure (semiconductors) that AI depends on.
- Related research is published as 'Heat as Image' and the essay 'Heat as (Generative) Image Making' (Weizenbaum-Studienpreis 2025).

## Beyond this website

- **Thesis:** the writing behind the work is [Heat as (Generative) Image Making](../texts/heat-as-generative-image-making.md), at https://aprilcoffee.github.io/heat_as_image/index.html
- **How the installation works:** A thermal camera films the working graphics card (an NVIDIA RTX 4090); a phone with the thermal camera app and screen capture sends the live thermal image by NDI to the computer, where an NDI virtual camera feeds it into StreamDiffusion in TouchDesigner as the base image for image-to-image generation. The GPU temperature is not read as a prompt or other input: a Python script handles temperature control (nvidia-smi), so the card regulates itself, as well as scene control and a Parler TTS voice for the speaker; Processing composes the output for an LED panel over HDMI (from the artist's system diagram, November 2026). Code and instructions (MIT licence): https://github.com/aprilcoffee/heat_as_image
- **Exhibited:** one of the works in *Cybernetic Subjects* (Bauhaus-Universität Weimar, shown at the University of Arts Linz during the Ars Electronica Festival 2025), described there as investigating "the hidden material infrastructures of AI systems through thermal imaging feedback loops, creating real-time feedback where computational waste heat becomes generative material for AI imagery": https://ars.electronica.art/panic/en/view/cybernetic-subjects-21338ddb450c817ab718ce48a0a628f5/
- **Essay:** *Heat as (Generative) Image Making*, FIfF-Kommunikation 1/26, p. 64: https://www.fiff.de/fiff-kommunikation/2026/1/

## Related

- [The material infrastructure of AI](../topics/material-infrastructure-of-ai.md)
- [Recursion and feedback](../topics/recursion-and-feedback.md)
- [Heat as (Generative) Image Making](../texts/heat-as-generative-image-making.md)
- [External links](../external-links.md)
- [Sun](sun.md)
- [Steering Through the Inner Residue](steering-through-the-inner-residue.md)

## Sources

- ../../../data/site.json (works → latent-heat-generation)
- https://liutingchun.com/works/latent-heat-generation/
- https://liutingchun.com/zh/works/latent-heat-generation/
- https://aprilcoffee.github.io/heat_as_image/index.html
- https://github.com/aprilcoffee/heat_as_image
- https://ars.electronica.art/panic/en/view/cybernetic-subjects-21338ddb450c817ab718ce48a0a628f5/
