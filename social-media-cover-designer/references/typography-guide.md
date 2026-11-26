# Typography guide (Telugu, Hindi/Marathi/Nepali Devanagari, English)

## Copy rules
- Use the **exact text supplied** by the user. Never translate, shorten, re-spell or "improve" it. If something looks misspelt, ask.
- Pass non-Latin strings to Photoshop through a UTF-8 JSON file (ExtendScript mis-reads UTF-8 inside `.jsx`).
- **ZWNJ (U+200C) warning:** Photoshop's engine can drop or mis-join glyphs around it (seen: చైర్మన్‌గా rendered చైర్మనా). After rendering, zoom to 200% and compare every word with the source. If a word breaks, try the string without ZWNJ (renders the standard conjunct) and **show the user both** for sign-off.
- Check conjuncts, vowel signs (ై ొ ీ / ि ी ै) and the half-letters at the top and bottom. They extend beyond the cap height, so give lines 30–40% leading.

## Typeface palette
| Role | Telugu | Devanagari (Hindi/Marathi/Nepali) | English |
|---|---|---|---|
| Hero / display | **Ramabhadra** (installed), Noto Serif Telugu Black (installed), Mandali, Suranna, NTR | Rozha One, Yatra One, Khand Bold, Teko Bold, Hind Bold | Bebas Neue (installed), Anton, Oswald Bold, Montserrat Black |
| Supporting | Noto Serif Telugu SemiBold/Bold, Nirmala UI Bold (installed) | Hind SemiBold, Mukta Bold, Nirmala UI Bold | Poppins SemiBold (installed), Inter |
| Small info | Nirmala UI, Noto Sans Telugu | Nirmala UI, Mukta | Poppins Medium/Regular |
| Script accent (one word max) | Gurajada, Dhurjati | Kalam, Tiro Devanagari | Montserrat Italic, a brush script |

Install missing Google Fonts (OFL, free for commercial use) from fonts.google.com before use: Ramabhadra, Mandali, Suranna, NTR, Gurajada, Noto Sans Telugu, Rozha One, Yatra One, Khand, Teko, Hind, Mukta, Kalam, Anton, Oswald, Montserrat. **Max two families per cover** (one display, one text).

## Hierarchy recipe
| Level | Size at 1500×500 | Weight | Colour |
|---|---|---|---|
| Hero word / name | 110–170px | display / black | brand accent or white |
| Supporting line | 52–80px | bold | white, dark ink or accent |
| Designation / org | 30–40px | semibold | 70–85% contrast |
| Info / date / handle | 22–28px | medium | muted |
Scale by width for other platforms (LinkedIn company: ×0.75, and drop to 2 levels).

## Effects menu (pick 1–2 per cover)
- **Solid extrusion (2.5D):** Drop Shadow, Normal blend, 100%, distance 8–14px, size 0, colour = darker shade of the text. R1 style.
- **Subtle 3D:** Bevel & Emboss (Inner Bevel, depth 100, size 3–5, soft) plus a faint drop shadow. For gold or metallic heroes.
- **Outline:** Stroke 6–10px outside, contrasting colour, for text over busy photos.
- **Texture fill:** clip a grunge, stone or paper texture to the text (Overlay/Multiply 40–70%). R3 and R6 style.
- **Gradient fill:** 2 stops in the same hue family (gold to orange, orange to red). R4 and R5 style.
- **Label bar:** text on a solid or brush-stroke bar, tilted 2–5°. Measure the bar's real position and centre the text on it.
- **Interlocked lockup:** small connector words tucked beside the big ones (R1). Align baselines and cap heights deliberately.
- **Giant wordmark behind the subject:** the name 1.5–2× the canvas width, behind the cut-out (R2) or as a 6–10% opacity watermark (R4).

## Don'ts
Thin fonts on photos; more than one script font; all-caps Telugu or Devanagari (no such thing, so don't fake it with scaling); letter-spacing Indic scripts (it breaks shaping); centring long multi-line text over a face.
