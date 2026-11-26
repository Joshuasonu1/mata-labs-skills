# Portrait preservation (mandatory)

The people in these covers are real public figures. Their face is their identity and political capital. A wrong nose, smoothed skin or altered smile is a factual error, and can be a reputational or legal problem.

## Never
- Generate, redraw, upscale-with-AI-hallucination, "enhance", beautify, slim, de-age, or face-swap the person.
- Ask an image model (ChatGPT, Firefly, Midjourney…) to produce an image **containing the person**, even "for reference" in the final file.
- Use liquify, skin smoothing, eye or teeth whitening, or "portrait" filters.
- Recolour skin, change hair or hairline, add or remove beard, glasses, tilak or jewellery.
- Flip a portrait horizontally if it shows text, a party symbol, a watch hand or a parting. Mirroring changes how familiar faces read. Ask first.
- Use a photo of a look-alike, or a generated "similar" person, as a stand-in.

## Always
- Work from the original supplied file (highest resolution). Keep it untouched in `assets/originals/`.
- Cut out with Photoshop **Remove Background** or **Select Subject**, then refine the edge (hair) only through mask edits. Pixels of the face are never painted.
- Keep scale reasonable: don't upscale a face more than about 1.5× its native size (soft faces look fake). If too small, choose a tighter layout or ask for a better photo.
- After compositing, compare the cover face side-by-side with the original at 100%: features, proportions, skin tone and expression must match.

## Allowed integration adjustments (non-destructive, on clipped adjustment layers)
| Adjustment | Purpose | Limit |
|---|---|---|
| Curves / Levels | match exposure to the scene | global only, no local face reshaping |
| Colour Balance / Photo Filter | match colour temperature (warm stage, cool dusk) | keep skin hue natural; check on a neutral grey |
| Hue/Sat on clothes or background only | harmonise brand colours | masked away from skin |
| Rim / edge light | a light-wrap from the background's brightest side | soft, ≤ 30% opacity, follows the real light direction |
| Contact / cast shadow | ground the subject | soft, offset away from the light; **never** a dark halo around hair |
| Atmospheric haze | depth where the body meets the background | at the lower body only |
| Grain | match noise between photo and plate | same grain layer over everything |

## Hair and edges checklist
- Zoom to 200% on the hair against the background: no grey fringe, no leftover studio colour, no dark glow.
- Bright skies are the hardest case. Use a faint offset contact shadow, not a dark outer glow.
- Watch background objects reading as part of the subject (e.g. flowers behind the head look like flowers in the hair). Move or blur the plate.

## When the photo isn't good enough
Say so and ask for another photo, or choose a layout that uses it smaller (collage card, inset circle). Never "fix" it with generation.
