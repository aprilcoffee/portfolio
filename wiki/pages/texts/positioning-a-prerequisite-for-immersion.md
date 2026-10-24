---
title: "Positioning – A Prerequisite for Immersion (定位—沉浸的先決條件) (text)"
type: text
tags: [text, immersion, virtual-reality, locative-media, positioning, game-engine, mandarin]
sources:
  - ../../../data/site.json (about.sections, Publications & Writing 2024)
  - https://www.digiarts.org.tw/DigiArts/DataBasePage/4_236170297334000/Chi
  - ../../raw/texts/positioning-a-prerequisite-for-immersion.md
updated: 2026-10-24
---
# Positioning – A Prerequisite for Immersion (定位—沉浸的先決條件) (text)

A Mandarin essay by Ting-Chun Liu (劉庭均), published in 2024 on Digiarts, the online platform of the National Taiwan Museum of Fine Arts. Its thesis is in the title: before we can feel "presence" in any medium, real or virtual, we have to be *positioned* in it. Liu moves from navigation (stars, GPS, tuning forks, aircraft warning lights) through locative media and Huizinga's "magic circle", to how virtual space is built inside a computer (ray casting in *Wolfenstein 3D*, VRML, the octree data structure), and finally to how the body is placed in virtual reality (hand tracking, outside-in and inside-out tracking, SLAM). Artworks by Jeremy Hight and collaborators, Gilbertto Prado, Marshmallow Laser Feast and Shehani Fernando serve as examples. It ends with the body, the interface, the virtual camera and the objects forming one "magic circle" system in which each part finds its position relative to the others, and immersion arises from that.

## Facts

- **Title:** 「定位—沉浸的先決條件」, *Positioning – A Prerequisite for Immersion*. (The CV's Mandarin line gives 「定位——沉浸的前提」; the supplied PDF is titled 「定位—沉浸的先決條件」.)
- **Author:** Ting-Chun Liu (劉庭均), single author.
- **Where:** Digiarts, National Taiwan Museum of Fine Arts, 2024 (year from the CV). Online: https://www.digiarts.org.tw/DigiArts/DataBasePage/4_236170297334000/Chi
- **Language:** Mandarin (Traditional Chinese). Four pages, ten footnotes, seven figures.
- **Structure:** introduction; 技術輔助下的現實定位 (Positioning in reality with technical help); 空間如何存在於虛擬 (How space exists in the virtual); 身體於虛擬空間的定位 (Positioning the body in virtual space); 結語 (Conclusion).

## Argument, section by section

### Introduction: presence needs a position
Epigraph from Sybille Krämer's "Does the Body Disappear? A Comment on Computer Generated Spaces", citing Jay David Bolter: hardly any sensation claims more insistently than vertigo that we have a body, and that this body is defined by its position in space. Liu's opening image: lying in bed at night, looking at the open door, you imagine getting up, walking across the room and closing it; you are operating a cognitive model and moving your subjective viewpoint to the door. "Presence" in immersive media is, after Matthew Lombard and Theresa Ditton, the "illusion of nonmediation": the medium becomes transparent, "like an open window". Liu's claim: 「沉浸的先驗條件，在於將認知定位於所處無論現實或虛擬的空間中」 ("the a priori condition of immersion is locating cognition in the space one is in, whether real or virtual"). AR, VR, MR, alternate reality games and computer games all use technical means to place the viewer's bodily cognition inside an illusion.

### Positioning in reality with technical help
Epigraph from Jeremy Wood (2011): the more he studies maps and mapping, the more convinced he is that we do not really know where we are. Our ancestors read the stars; since the 1990s GPS uses 24 active satellites and trilateration from three or more of them. Positioning is an ancient problem: we need a reference to move at all. A musician strikes a 440 Hz tuning fork before playing; aircraft over cities locate themselves by the red lights on rooftops. Tuning fork, light, astrolabe or satellite: each is a relative referent that lets us "convince ourselves we are in space".

Example: *Project 34 North 118 West* (2003) by Jeff Knowlton, Naomi Spellman and Jeremy Hight, described as the first work to use satellite positioning to trigger narrative. Visitors walk Los Angeles streets with a GPS tablet, headphones and an interactive map; audio about the history of the buildings plays according to their movement. Hight calls this a "conversation" between place, infrastructure, freely chosen movement and digitally augmented space. Walking a four-block site, the visitor's presence exceeds the dimension of time; different times overlap with technical help. Sound is not the only cause of immersion: the interaction with a bounded physical area matters, which Johan Huizinga called the "magic circle" (chessboard, pitch, stage, game screen). The map both draws the circle and marks the visitor's position; the dot on the map is "the projection of the visitor's consciousness onto the device". Walking becomes a synchronised immersion between the virtual (map and sound) and the real (body and buildings), and the gamified search for sites lets visitors imagine themselves inside the map.

### How space exists in the virtual
Virtual space depends on technical development, and technical limits give it its own rules. Bolter and Grusin (*Remediation*): the logic of immediacy demands that the medium disappear, so we feel only what it represents, sitting in a racing car or standing on a mountain; an "immediate relationship" with the content. Game engines are today's main platform for AR and VR. In the early 1990s personal computers could not render real-time 3D with a virtual camera, so game programmers used **ray casting**: measuring 2D distances from a first-person viewpoint to the walls and texturing them with different brightness. The camera stays at the origin; only the scene moves, yet keyboard and mouse input create the illusion of moving through space. Liu calls this the earliest 3D game engine (figure: *Wolfenstein 3D*, 1992). Later MIT's Alice and VRML (Virtual Reality Modeling Language) were explored by early VR artists, for example Gilbertto Prado's *Desertesejo* (2000), a VRML flight over geological landscapes that keep being rebuilt.

Digital media come from the computation of data, and abstract data structures let physical circuits open up space. Liu explains the **tree** (root, nodes, branches, one parent per node, exactly one path to any node), the binary tree and the **octree**, which divides 3D Cartesian space into eight octants. Because a tree can recurse without end, a coordinate is found by searching "octants within octants": the whole space at the root, then 1/8, 1/64, 1/512 of it. The octree gives virtual space a hierarchy, and that hierarchy *is* its resolution; game-engine collision is computed from the relations between volumes in the nodes. Only because of this structure can we point to a specific place in virtual space, and only so can objects exist in it.

### Positioning the body in virtual space
Figure: Oskar Schlemmer, *Figure in Space with Plane Geometry and Spatial Delineations* (1924). Without a referent for the self, immersion breaks. The point-of-view film *Hardcore Henry* is immersive because the hero's arms and legs swing with the camera; look down in VR and see no limbs, and the gap between sight and body sense breaks the illusion. Leap Motion (2010), an infrared camera that tracks the hand skeleton by computer vision and was later mounted on VR headsets, makes VR more convincing by showing your own hands.

Registration and tracking are essential: in standard VR a physical movement must reach the image within 30 ms; hands, torso, head and eyes are measured by gyroscopes, accelerometers and magnetometers. Liu distinguishes **outside-in tracking** (emitters or cameras in the room, trackers on the body; the HTC Vive) from **inside-out tracking** (the headset scans its surroundings; Oculus Go at start-up), which needs SLAM (simultaneous localisation and mapping) so the user does not hit obstacles. Quoting Peter Anders: movement is the key to experiencing real or virtual space; without positioning and interaction our autonomy shrinks and we cannot experience it. Liu then asks: when the headset's sensors change the image, what is actually moving, the avatar's gaze in the game engine or the virtual space itself?

Examples: Marshmallow Laser Feast's *Treehugger: Wawona* (2016), a VR work around a giant sequoia modelled on a real tree in Sequoia National Park (*Wawona* is said to mean the call of the owl in the Miwok language); the view floats up the trunk into a point-cloud canopy, and flowing particles, standing for energy in the tree's vessels, react to the visitor's hand controllers. In game theory the "rabbit hole" from *Alice in Wonderland* is the first lure into an experience; in VR, Liu argues, it is not the moment of putting on the headset but the first interaction or audiovisual shock inside it. In *Treehugger* the feeling of leaving the ground pulls the visitor out of their real-world position. Shehani Fernando's *Limbo: a virtual experience of waiting for asylum* (2017) also uses point clouds but only lets the viewpoint turn; real scenes rendered as point clouds, with narration and street sound, position the viewer in reality and virtuality at once, inside a refugee's wait for asylum.

### Conclusion
We relate to the world by locating consciousness in the body and meeting the world through the senses. In first-person VR we place ourselves at the origin of a virtual Cartesian coordinate system; sensors pass on the movements of limbs and head, and the image or sound changes, so that moving the scene or the virtual camera makes the illusion that we moved. 「身體、互動媒介、虛擬鏡頭與物件共同組成一套『魔法圈』的系統，系統內各個主體透過定位，尋找與彼此相對位置的變化從而改變自身狀態，我們的自我認知也得以在系統中達成沉浸。」 ("Body, interactive medium, virtual camera and objects together form a 'magic circle' system; each subject in it, through positioning, finds changes in its position relative to the others and changes its own state, and so our self-awareness can reach immersion within the system.")

## Works, authors and technologies cited

- **Artworks:** Jeff Knowlton, Naomi Spellman and Jeremy Hight, *Project 34 North 118 West* (2003); Gilbertto Prado, *Desertesejo* (2000); Marshmallow Laser Feast, *Treehugger: Wawona* (2016); Shehani Fernando, *Limbo: a virtual experience of waiting for asylum* (2017); Oskar Schlemmer, *Figure in Space with Plane Geometry and Spatial Delineations* (1924); the film *Hardcore Henry*; the game *Wolfenstein 3D* (1992).
- **Authors:** Sybille Krämer; Jay David Bolter and Richard Grusin, *Remediation* (1999); Matthew Lombard and Theresa Ditton, "At the Heart of It All: The Concept of Presence" (1997); Jeremy Wood; Jeremy Hight in Buschauer and Willis (eds.), *Locative Media* (2014); Johan Huizinga, *Homo Ludens*; Samuel Greengard, *Virtual Reality* (2019); Peter Anders, *Envisioning Cyberspace* (1998).
- **Technologies:** GPS and trilateration, ray casting, Alice (MIT), VRML, trees and octrees, collision detection, Leap Motion, gyroscope/accelerometer/magnetometer, outside-in and inside-out tracking, HTC Vive, Oculus Go, SLAM, point clouds.

## Key ideas for the chat

- **Medium specificity from the inside.** As in Liu's later AI texts, the argument goes down into how the medium is built: immersion is explained by ray casting, octrees and tracking latency, not by content. The illusion of moving is, technically, the scene moving around a fixed camera.
- **Recursion as structure.** The octree's "octants within octants" is an early appearance of recursion in Liu's writing: the resolution of a virtual world is the depth of a recursive data structure. Compare [Recursion and feedback](../topics/recursion-and-feedback.md).
- **Feedback before cybernetics.** Immersion is described as a loop: body moves, sensors measure, image changes, self-perception updates. The later texts name this kind of loop in cybernetic terms ([Hello, Human!](hello-human.md)).
- **Positioning as reference.** Every position needs a referent (tuning fork, warning light, satellite, the dot on the map, one's own hands). Being "in" a space is always relative, technical and constructed.
- **The body stays central.** The essay connects to Liu's earlier body-based performance work: immersion breaks when the body has no place in the image. See [Body and action](../topics/body-and-action.md).

## Open questions

- The CV's Mandarin title (「定位——沉浸的前提」) differs from the PDF title (「定位—沉浸的先決條件」). Which wording does the artist prefer?
- Exact publication date on Digiarts is not given in the supplied text (the CV says 2024).

## Related

- [Recursion and feedback](../topics/recursion-and-feedback.md)
- [Body and action](../topics/body-and-action.md)
- [Hello, Human! catalogue text](hello-human.md)
- [Talks and writing](../talks-and-writing.md)
- [External links](../external-links.md)

## Sources

- data/site.json, about.sections: Publications & Writing (2024)
- https://www.digiarts.org.tw/DigiArts/DataBasePage/4_236170297334000/Chi
- Text supplied by the artist, October 2026 (PDF; extract in [raw/texts/positioning-a-prerequisite-for-immersion.md](../../raw/texts/positioning-a-prerequisite-for-immersion.md))
