# Workflow: final quality control

Run on **every platform export** before showing the user. Write the results to `covers/qc_report.md`.

## 1. Mechanical checks
- [ ] Exact export size per `platforms/*.md`; sRGB; file size under the limit.
- [ ] `python scripts/safe_zone_preview.py <file> <platform>` shows no text or face inside the avatar/logo mask or the crop bands (desktop and mobile).
- [ ] Text ≥ the minimum size for the platform (mobile legibility). View at 640px wide.
- [ ] Every Telugu/Devanagari word compared glyph-by-glyph with the supplied copy at 200% (watch ZWNJ, conjuncts, vowel signs).
- [ ] Face compared with the original at 100%: unchanged.
- [ ] Hair and edge check at 200%: no fringe, no halo, no background objects reading as part of the person.
- [ ] No generated people or crowds; all crowd or works photos are the client's real ones; logos from supplied files.
- [ ] Assets logged with licences.

## 2. Score (each /10, be honest)
| Criterion | What 9–10 looks like |
|---|---|
| Composition | clear hierarchy, avatar-aware, intentional negative space, depth through overlap |
| Typography | designed lockup, ≤ 2 families, readable on mobile, correct script |
| Portrait integration | matched light and colour, rim light, natural shadow, clean edges |
| Background quality | fits the concept, no AI artefacts, supports rather than competes |
| Colour grading | unified cast, brand colours accurate, luminance separation of the face |
| Professional finishing | textures convincing (fibrous torn edges), grain unifies, no cheap glow |
| Platform compatibility | all crops pass, separate layouts per platform |
| Visual impact | reads in under 1 second at thumbnail size |
**Overall = average.** Anything < 8 gets fixed before delivery; list what was fixed. Report the scores and the remaining weaknesses honestly to the user.

## 3. Distinctness
If the client already has covers, place the new one beside them: it should not look like a recolour of an earlier design.

## 4. Deliver
Per platform: `.psd` (layered, live text) plus `.png`/`.jpg` export plus a `_safezone.png` preview. Tell the user where they are and how to upload (Facebook: Page, then Edit cover; X: Edit profile, then the header camera icon; LinkedIn: profile pencil, then background photo).
