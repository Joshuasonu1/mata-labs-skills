---
name: social-media-cover-designer
description: Design premium cover images and profile banners for Facebook Pages, X (Twitter) headers, LinkedIn personal backgrounds and LinkedIn company Pages, built in Photoshop around the client's ORIGINAL portrait (never an AI face). Six design systems (cinematic, editorial, premium portrait, minimalist, documentary collage, political leadership), platform safe zones, Telugu/Hindi/English typography, AI-generated or stock background plates, and a scored QC pass. Use when the user asks for a cover photo, profile banner, header image, LinkedIn background, Facebook cover or X header for a person, leader, campaign or organisation. NOT for Instagram reel covers or ordinary feed posts.
---

# Social media cover designer

Builds wide-format profile covers (Facebook Page, X, LinkedIn personal, LinkedIn company) that look art-directed in Photoshop: real portrait cut-out, a background plate chosen for the concept, layered typography, textures, colour grade, then one export per platform with its own safe-zone layout.

**Scope:** covers and banners only. Instagram reel covers, feed posts and stories are out of scope (use `polcomms-reels` / `ig-*` skills).

## Inputs to collect (ask only for what's missing)
1. **Original portrait(s)**: highest resolution available. Studio shots on plain backgrounds cut out best.
2. **Name and designation**, exactly as they should appear (spelling verified by the user).
3. **Organisation / campaign / party**, plus approved logo files (never recreate a logo).
4. **Headline or tagline**, exact wording and language (Telugu / Hindi / English). Never rewrite it.
5. **Design direction**: one of the six systems, or "you choose".
6. **Platforms**: any of Facebook, X, LinkedIn personal, LinkedIn company.
Optional: brand colours, fonts, real event photos for collage, dates or locations.

## The non-negotiable rule
**Never generate, redraw, beautify, retouch or replace the person's face.** Use the supplied photo as a cut-out. Allowed: exposure, curves, colour balance, edge/rim light, natural shadow, atmospheric blending. Read `references/portrait-preservation.md` before every job.

## Pick a design system
| System | Use when | File |
|---|---|---|
| Cinematic dramatic | big statement, decision, milestone, fiery tone | `styles/cinematic.md` |
| Modern editorial | issue-led message, magazine feel, giant wordmark | `styles/editorial.md` |
| Premium portrait | personal brand, warm and trustworthy, face is the hero | `styles/premium-portrait.md` |
| Minimalist professional | LinkedIn, corporate, women leaders, clean white | `styles/minimalist.md` |
| Documentary collage | track record: works done, schemes, events (real photos) | `styles/documentary-collage.md` |
| Political leadership | rally energy, mass support, party colours, crowds | `styles/political-leadership.md` |

Rules of thumb: LinkedIn defaults to **minimalist** or **premium portrait**; X and Facebook for politicians default to **political leadership** or **cinematic**; anything with "works / development / achievements" plus real photos goes to **documentary collage**. Never use the same system twice in a row for one client unless asked.

## Workflow (follow in order)
1. **Brief**: confirm inputs, platform list, exact text. Write a 3-line concept: the story, the mood, one hero image idea.
2. **Platform specs**: open each `platforms/*.md`. Note canvas, safe zone and avatar/logo overlap. Design a master at the largest size, then one layout per platform (never just crop one image).
3. **Assets**: `workflows/research-assets.md`, then `workflows/background-generation.md`. Real photos first; generated plates only for scenery, light and texture. Log every asset in `assets_log.md` with source and licence.
4. **Portrait integration**: `workflows/portrait-integration.md`: Photoshop Remove Background, edge cleanup, colour match, light wrap, shadows.
5. **Typography**: `references/typography-guide.md`. Exact copy only; check Telugu/Devanagari shaping by zooming the render.
6. **Grade and finish**: `references/colour-grading.md` and `references/texture-library.md`.
7. **Exports**: one layered PSD per platform plus PNG/JPG at spec size (and @2x where noted).
8. **QC**: `workflows/final-quality-control.md`. Score /10 per criterion, preview desktop and mobile crops with the avatar mask overlaid, fix anything under 8, then present.

## Combined ChatGPT + Photoshop production (default pipeline)
**ChatGPT** makes the creative raw material: cinematic scenes, light elements, textures, atmosphere, abstract graphics, all generated **separately from the portrait**. **Photoshop** does the production: extraction and masking of the original portrait, compositing, colour matching, grading, shadows and highlights, torn paper, typography and effects, collage, final export. The result must read as a Photoshop composition, never as a raw AI image.

Order: analyse brief and references, then concept, then generate plates in ChatGPT, then import into Photoshop, then the original portrait cut-out, then composition, then type, textures and graphics, then review at desktop and mobile sizes, then per-platform exports.

**Honesty rule:** at the start of each job, check which tools actually work (`workflows/research-assets.md` §0). If Photoshop automation or ChatGPT is unavailable, say so and use the fallback (PIL-built layers, exported asset packs, ready-to-paste prompts, a Photoshop handoff note). Never describe a step in an app as done unless you actually ran it and saw the result.

## Tooling on this machine (tested)
- **Photoshop 2027** scripted via `"C:\Program Files\Adobe\Adobe Photoshop 2027\Photoshop.exe" <file.jsx>`. The first external script may raise "You are about to run the script…" (click Yes). If Photoshop isn't running, start it first and wait for the Home screen, because a cold-start launch drops the script. Keep the PC unlocked (scripts stall on the lock screen). Write progress to a file from the JSX and poll it.
- Helpers in `scripts/`: `ps_cutout.jsx` (batch Remove Background to PNG), `ps_helpers.jsx` (place PNG, fit text, layer FX, rounded and polygon fills, save PSD/PNG), `safe_zone_preview.py` (overlays avatar circles and crop lines on an export).
- **Fonts installed:** Noto Serif Telugu (Thin to Black), Ramabhadra (Telugu display), Nirmala UI (Telugu, Devanagari, Latin), Poppins, Bebas Neue. Others must be installed first (see typography guide).
- **ChatGPT desktop app** (computer use) generates background plates: start a new chat; prompt "vertical/horizontal photoreal…, NO people, NO text, NO logos, keep <zone> simple"; right-click the image, choose **Download a copy**, and type a full path in the Save As dialog. Adobe connector (if connected) offers Firefly / Remove Background / generative expand.
- **Known pitfalls:** ExtendScript reads `.jsx` as non-UTF-8, so pass Telugu/Hindi strings via a UTF-8 JSON file. Zero-width joiners (U+200C) can drop letters in Photoshop text (e.g. చైర్మన్‌గా rendered చైర్మనా), so render, zoom and compare. Don't name an ExtendScript global `path`. A dark drop shadow behind a cut-out shows as a halo on bright skies, so use a faint, offset contact shadow instead.

## Output layout
`<project>/covers/<client>_<platform>_<system>.psd|png`, `<project>/covers/previews/*_safezone.png`, `<project>/covers/assets_log.md`, `<project>/covers/qc_report.md`.

## References
`references/visual-analysis.md` (six reference posters decoded), `composition-guide.md`, `typography-guide.md`, `colour-grading.md`, `portrait-preservation.md`, `texture-library.md`, `asset-sources.md`.
