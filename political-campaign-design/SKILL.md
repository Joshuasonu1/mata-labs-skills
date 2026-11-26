---
name: political-campaign-design
description: Design professional political campaign graphics in vertical formats (Instagram feed posters 1080x1350, stories and reel covers/thumbnails 1080x1920, WhatsApp status, square posts) for real leaders, built in Photoshop around their ORIGINAL photos (never an AI face). Six design systems (cinematic dramatic, modern editorial typography, premium portrait, minimalist white editorial, documentary photo collage, mass rally campaign), Telugu/Hindi/English typography with exact client copy, ChatGPT-generated background plates, real crowd footage only, and a scored QC pass. Use when the user asks for a campaign poster, election poster, leader poster, reel cover, reel thumbnail, story design or "make it like this poster" for a politician or campaign. For Facebook/X/LinkedIn banners use social-media-cover-designer; for editing reels use polcomms-reels.
---

# Political campaign design (posters, stories, reel covers)

Professional, Photoshop-composited campaign graphics for real political leaders. Real portraits, real crowds, exact copy, and art direction that looks designed by an agency, not generated.

## Inputs (ask only for what's missing)
1. **Original photos** of the leader (several poses; the highest resolution available).
2. **Exact copy**: headline, supporting line, name, designation, constituency, date and location. Telugu/Hindi copy is used **verbatim**.
3. **Party or campaign identity**: approved logo and symbol files, colours.
4. **Purpose and format(s)**: feed poster, story, reel cover (which reel?), WhatsApp status.
5. **Real event or works photos** if the story needs proof (crowds, schemes, development).
6. **Direction**: one of the six systems, a reference image, or "you choose".

## Non-negotiable rules
1. **Portrait preservation:** never generate, redraw, beautify or alter the leader's face. Cut-outs of the original photo only (`references/portrait-preservation.md`).
2. **Exact copy:** never rewrite, translate or "fix" supplied text; ask if in doubt. Verify the Indic shaping glyph by glyph after rendering.
3. **Truth:** no generated crowds, rallies, events or "works" presented as real; no statistics or claims that weren't supplied; no rival-party symbols or colours; logos only from supplied files.
4. Generated images are for **scenery, light, texture and symbols only**.

## Formats and safe zones
| Format | Canvas | Keep key content inside |
|---|---|---|
| Feed poster | 1080×1350 (4:5) | 60px margin all round |
| Square post | 1080×1080 | 60px margin |
| Story / WhatsApp status | 1080×1920 | y 250–1580 (top bar and reply box cover the edges) |
| Reel cover / thumbnail | 1080×1920 | **y 285–1635** (fits both the 3:4 profile-grid crop 240–1680 and the 4:5 feed crop) and avoid the right 140px (reel buttons) and the bottom 320px when shown in the reel UI |
Always export the full 9:16 and also check a 3:4 and a 4:5 centre crop preview.

## Pick a design system
| # | System | Use for | Workflow |
|---|---|---|---|
| 1 | Dramatic cinematic | decisions, victories, historic moments, attacks on issues | `workflows/cinematic-poster.md` |
| 2 | Modern editorial typography | slogans, "vote for", youth messaging, giant wordmark | `workflows/editorial-poster.md` |
| 3 | Premium portrait | introductions, greetings, personal brand, trust | `workflows/portrait-poster.md` |
| 4 | Minimalist white editorial | quotes, women leaders, policy, calm statements | `workflows/minimalist-poster.md` |
| 5 | Documentary photo collage | works done, schemes, track record, events (real photos) | `workflows/documentary-collage.md` |
| 6 | Mass rally campaign | rallies, roadshows, nominations, poll-day mobilisation | `workflows/mass-campaign-poster.md` |
For a **series** (e.g. 15 reel covers), rotate systems and vary crop, pose and layout so the grid doesn't repeat. Keep one or two constants (brand colour, name strip) for identity.

## Production pipeline (ChatGPT + Photoshop)
1. **Brief:** concept in 3 lines (story, mood, hero image), system choice, formats.
2. **Tool check** (be honest): Photoshop scriptable? ChatGPT app reachable via computer use? Adobe connector? If not, use the fallbacks in `../social-media-cover-designer/workflows/research-assets.md` §0 and say so.
3. **Assets:** client photos first, then free stock, then ChatGPT plates (prompt rules in `references/asset-sources.md`). Log everything.
4. **Photoshop:** Remove Background on the original portrait, composite, colour match, rim light, contact shadow (never a dark halo), textures, typography, grade, grain. Follow the setup, non-destructive habits and the list of banned 2027 AI features in `references/photoshop-techniques.md` (no Relight, Recompose or Generative Upscale on the leader; re-frame with Generative Expand on plates only).
5. **QC** (below), then deliver layered PSD plus PNG per format.

Shared tested scripts live in `../social-media-cover-designer/scripts/`: `ps_cutout.jsx` (batch Remove Background), `ps_helpers.jsx` (place, fit text, FX, shapes, save). Launch with `"C:\Program Files\Adobe\Adobe Photoshop 2027\Photoshop.exe" runner.jsx` while Photoshop is open; click Yes on the first run-script prompt; keep the PC unlocked.

## Quality control (score each /10; fix anything < 8 before showing)
1. Professionally art-directed composition (hierarchy, depth via overlap, negative space)?
2. Portrait authentic and unchanged (compare with the original at 100%)?
3. Background complements the subject (no objects growing out of the head, luminance separation)?
4. Typography readable at phone size; copy exact; Indic shaping correct?
5. Textures realistic (fibrous torn edges, scanned paper, not plain polygons)?
6. Lighting consistent (one light direction, rim on the correct side)?
7. Looks like a finished Photoshop composition, not raw AI?
8. Visually distinct from previous designs in the series?
Report the average and the remaining weaknesses honestly.

## References
`references/design-analysis.md` (six reference posters decoded plus the @ktrtrs reel-cover grammar plus lessons from past jobs) · `typography-guide.md` · `colour-palettes.md` · `portrait-preservation.md` · `asset-sources.md` · `photoshop-techniques.md` (tool setup, cut-out and cleanup methods, re-framing, Camera Raw, shortcuts).
