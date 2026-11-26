# Typography guide: Telugu, Hindi/Marathi (Devanagari), English

## Copy integrity
- Use the client's exact words. Never rewrite, translate, abbreviate or correct silently. Ask.
- Feed Indic strings to Photoshop via a **UTF-8 JSON file** (ExtendScript mis-reads UTF-8 in `.jsx`).
- After rendering, zoom to 200% and compare every word with the source: conjuncts, vowel signs, ZWNJ (U+200C) joins. If Photoshop breaks a ZWNJ word, show the user the alternative rendering and get sign-off.
- Leading 1.3–1.45× for Telugu and Devanagari (marks above and below). Never letter-space Indic text. Don't fake bold by stroking thin fonts.

## Font palette (installed = ✓)
| Role | Telugu | Devanagari | English |
|---|---|---|---|
| Hero | Ramabhadra ✓, Noto Serif Telugu Black ✓, Mandali, Suranna, NTR | Rozha One, Yatra One, Khand Bold, Teko, Hind Bold | Bebas Neue ✓, Anton, Oswald, Montserrat Black |
| Supporting | Noto Serif Telugu Bold ✓, Nirmala UI Bold ✓ | Hind SemiBold, Mukta Bold, Nirmala UI ✓ | Poppins SemiBold ✓ |
| Small info | Nirmala UI ✓, Noto Sans Telugu | Nirmala UI ✓, Mukta | Poppins ✓ |
| Accent word | Gurajada, Dhurjati | Kalam | brush script |
Install Google Fonts (OFL) when needed. **Two families max** per design.

## Hierarchy (on 1080 wide)
| Level | Size | Example |
|---|---|---|
| Hero word or number | 160–320px | మోదీ, 370, అఖండ, 5 |
| Headline line | 90–140px | the main slogan |
| Supporting line | 50–80px | on a label bar or brush |
| Name / designation | 40–56px | name strip, credentials |
| Info (date, place, handle) | 26–34px | corners, bottom strip |

## Treatments (choose 1–2)
- **Interlocked lockup:** huge plus small words fitted together (R1).
- **Solid extrusion:** Drop Shadow, Normal 100%, distance 8–14, size 0, darker shade (R1, ktrtrs).
- **Texture fill:** grunge or stone clipped to the text (R3, R6).
- **Gradient fill:** two stops, same hue family (R4, R5).
- **Outline:** 6–10px stroke for type over photos.
- **Label bar / brush slash:** measure the bar, centre the text on it, same tilt (2–5°).
- **Wordmark behind the head:** type layer below the cut-out (R2).
- **Watermark word:** 5–8% opacity giant name (R4).
- **Name strip:** small dark bar plus brand accent tick, top-left, **not** over the head.

## Section guidelines
- **Main headline:** ≤ 6 words visible at thumbnail size; the strongest word biggest.
- **Supporting headline:** one line, on a bar or in a contrasting weight.
- **Small information:** never below 26px; group in one block.
- **Date and location:** a corner badge or bottom strip; consistent across a series.
- **Campaign branding:** logo, symbol and ballot number from client files; same corner every time.
