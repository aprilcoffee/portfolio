> Source: Ting-Chun Liu, "On the Materiality of AI", in *un/learn ai – integrating AI in aesthetic practices*, vol. 3, eds. Grund, Wallenborn, Scherffig and Jenett, Mainz: KITeGG, 2025 (pp. 218–223). Online: https://unlearn.gestaltung.ai/de/article/gpm91yc8?chunks=gpm91yc8. Transcribed from page images of the PDF supplied by the artist, October 2026 (the body text is not machine-readable; "Chunk n" markers of the layout are left out). The supplied PDF shows only footnote 1 of the notes.

# On the Materiality of AI

Ting-Chun Liu

(Layout label: "gpm91yc8 ● Dieser Artikel ist nur auf Englisch verfügbar")

## Introduction

"we have re-enabled chatgpt plus subscriptions! thanks for your patience while we found more gpus"[1]

Sam Altman's tweet revealed how complex networks expose themselves only when certain nodes malfunction. The artificial intelligence (AI) industry relies on centralized semiconductor production, intensive energy consumption, and supply chains contributing to global environmental and political tensions. As Langdon Winner noted, societal conflicts and alliances are determined not just through political institutions but also through the physical arrangements of infrastructure: steel, concrete, wires, and semiconductors.[2]

This piece examines how Taiwan's semiconductor industry, particularly Taiwan Semiconductor Manufacturing Company (TSMC), creates both technological dependency and geopolitical vulnerability in the global AI infrastructure. Taiwan's strategy for maintaining its sovereignty through the *Silicon Shield* paradoxically requires accelerating technological systems that potentially undermine sovereignty elsewhere.

While writing the piece, there is a slight hum from the laptop, barely noticeable yet constants. This hidden noise from the fan, quietly cooling down trillions of transistors that were once grains of sand. This gentle hum signifies the countless layers of technology working beneath the surface, a constellation of silicon, metal, and code in operation.

## Main Part

Technology is a complex, shifting, recursive landscape, engaging with it as an artist reveals a double-edged reality. As Simon Penny observed, artists working with technology inevitably become entangled in consumer commodity economics.[3] This feedback loop became evident when OpenAI's published its first text-to-image model DALL·E.

It produced strange compositions that felt uncanny and raw, qualities that today's polished outputs have eliminated.

I was eager to work with these effects, yet as the model became outdated access was removed.

I found myself unable to run alternatives locally due to lacking computational hardware.

```
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Whether Midjourney, DALL·E, Stable Diffusion, or ChatGPT, all generative models were trained on NVIDIA's data center graphic processing units (GPUs), notably the *NVIDIA A100*. ChatGPT alone required an estimated 20,000 to 30,000 A100s just to train.[4] Billions of tiny cores in GPUs, originally designed for rendering 3D games, turned out to be perfect for training neural networks, due to their ability to compute massive volumes of simple, repetitive mathematical operations. The turning point came in 2012 when AlexNet,[5] a deep convolutional neural network, leveraged GPUs' parallel processing capabilities that outperformed all other image classification approaches, making graphic cards the industry standard.

One of the researchers Alex Krizhevsky was then employed by NVIDIA to develop *CUDA* (Compute Unified Device Architecture), a proprietary framework for parallel computing.

```
RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running on a CPU-only machine, please use torch.load with map_location='cpu' to map your storages to the CPU.
```

This CUDA error message exposes a deeper dependency—most AI models expect CUDA-enabled environments that only work with NVIDIA GPUs. Their hardware is not just a technical choice but a gatekeeping mechanism.

The production of semiconductors that power modern GPUs reveals a complex global network spanning multiple continents and involving dozens of specialized companies (Figure 1).

A making of semiconductor begins as one of the most common materials: sand, specifically quartz or silicon dioxide. Despite its ubiquity, chip production demands unnatural purity at 99.9999999%.

Only two companies worldwide control the critical extraction and refinement process.

And both are based in Spruce Pine, North Carolina. They turn sand into silicon that then travels to companies in Japan to be formed into wafers. At a talk at the *Correlations Forum* in *hfg Offenbach*, I passed around wafer pieces to the audiences. What always strikes audience members is their delicacy, which even slight touches left grease marks and contamination, revealing why manufacturers must work in ultra-clean environments.

These wafers then face the most critical bottleneck in chip production: lithography. Only the Dutch company ASML (Advanced Semiconductor Materials Lithography) produces the Extreme Ultraviolet (EUV) machines needed for printing advanced semiconductors, holding 100% market share with machines costing over $150 million each. This monopoly creates profound political leverage, as recent U.S. export bans have prohibited these machines from being sold to China.[6]

[Figure 1: The Making of Graphic Cards (Nvidia RTX 4090) - Global supply chain visualization showing the journey from raw materials to final product. © Ting-Chun Liu. Contains materials courtesy of NVIDIA, TSMC, ASML, and other manufacturers.
Map labels, read from the image: Quartz: Covia (US), American Elements (US) → Purified Silicon → Shin-Etsu Group (JP) (Silicon) → TSMC (TW); Universal Quartz (India); Oxford Instruments (UK) (plasma etching and deposition systems) → ASML (NL) (Lithography Machine (EUV)); ZEISS (DE) (Optical System) → ASML; SK Hynix (Kr) (Random Access Memory); Synopsys (US) (electronic design automation (EDA) software) → NVIDIA (US) (Design) → TSMC (TW); ASE (TW) (Packaging); Foxconn (TW/CN) (Assembly); final product: RTX 4090.]

All these elements then converge at TSMC, the world's leading chip fabricator, which produced about 90% of advanced semiconductors as of 2022.[7] Here, NVIDIA's electronic layouts are etched onto silicon with ASML's EUV machines, transforming chip designs from mere drawings into functional processors.

TSMC's dominance emerged from specific historical circumstances when the company was founded in 1987. At the end of Taiwan's forty years under martial law, TSMC filled the gap created when U.S. pressure forced Japan to retreat from semiconductor dominance through the 1986 U.S.–Japan Semiconductor Agreement.[8] Taiwan, transitioning from authoritarian rule to democracy, recruited Morris Chang, a Taiwanese-American engineer who had never set foot on Taiwanese soil, to establish the world's first dedicated semiconductor foundry. TSMC's establishment actively constructing Taiwan as a geopolitical hinge in the global semiconductor supply chain where sand from North Carolina becomes the foundation of our digital world.

In 2021, Taiwan experienced its worst drought in a century. The high-tech industry, barely sustained itself with government support, often at the expense of the general populace. The drought coincided with sudden chip demand, leading to global chip shortages that brought Taiwan's semiconductor industry under scrutiny.[9] Taiwan's then-President Tsai Ing-wen reiterated the importance of the *Silicon Shield*,[10] describing how the country's chip dominance serves as both economic leverage and a deterrent against Chinese aggression.[11] Semiconductor is not just a technical asset—it's a geopolitical instrument of sovereignty. Taiwan must maintain semiconductor dominance if it is to remain independent. Taiwan is structurally entangled in AI's acceleration. Building the digital infrastructure also enables extractive computation and the consolidation of power through information. And here the dilemma comes arises: *protect its sovereignty, Taiwan must help accelerate a system that undermines sovereignty elsewhere and generates new crises*. What protects this one island may destabilize others. Silicon is not neutral.

It underpins the tools of generative AI and militarized computing. Fighter jets equipped with TSMC-manufactured chips,[12] were deployed by the Israeli government in Gaza.[13] With the U.S. and European Chip Acts restricting China's access to high-end processors[14] Taiwan has become the pivot point in an emerging techno-political order. The very infrastructure of AI is built on decades of political engineering. TSMC's origins makes clear that advanced computation was never the result of free markets alone. It was infrastructural, strategic, and deeply historical.

Today, that uncertainty hasn't disappeared. The chips Taiwan produces now operate in systems of generative AI, predictive policing, algorithmic governance, and synthetic culture. Despite all this, Taiwan itself remains one of the region's most at risk polities if this acceleration continues in this direction. There is no guarantee that Taiwan itself will not be made expendable.

## Conclusion

AI is more than the symbol of clouds or the tireless server room at work; its material foundations are inseparable from its geopolitical nature. Engaging with these systems means also engaging with the intangible structures that constitute and are constituted by our relation to the world.

The question then is not simply who is responsible for these systems, but how we choose to engage with the collective systems we are all, to some degree, complicit in. The gentle hum of the laptop fan continues, cooling transistors that were once grains of sand. To work with AI, is to work with these contradictions, to remain close not only to the surface of the output, but also the condition that shaped it—the layers beneath, the labor behind, the heat in circuits, the extracted nature within networks, the intangible infrastructure, and the silent hum behind the interface.

This writing is part of an artistic research documented at: https://aprilcoffee.github.io/heat_as_image/

Notes (only note 1 is legible in the supplied PDF):
1. Altman, S. (2023). *We have re-enabled ChatGPT Plus*
