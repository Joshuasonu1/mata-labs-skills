# Composition guide for wide covers

Wide banners (2.6:1 to 5.9:1) behave differently from posters. The eye scans left to right, the avatar or logo covers a corner, and mobile crops the sides.

## The three zones
```
| AVATAR ZONE (keep clear) | MESSAGE ZONE (headline, name) | HERO ZONE (portrait) |
```
- **Avatar zone**: bottom-left on every platform (see `platforms/`). Put only background there (sky, blur, texture). Never text or faces.
- **Message zone**: the centre band. It survives mobile cropping best, so the headline goes here.
- **Hero zone**: the right third, where the portrait faces **into** the frame (toward the text). If the photo faces right, put it on the left of the message zone, still clear of the avatar, or choose another photo. Don't mirror (see portrait-preservation).

Variants: centred hero with the wordmark behind (editorial, X/FB only, because LinkedIn's avatar sits under the centre on mobile); portrait left plus text right (only if the avatar is not on the left, which is rare).

## Hierarchy (max 4 levels)
1. Hero line (one or two words huge), or the name for personal-brand covers.
2. Supporting line (0.45–0.6× the hero size).
3. Name and designation (if not level 1).
4. Small info: constituency, date, handle (≥ 22px at 1500 wide; LinkedIn company ≥ 16px).

## Scale and balance
- Portrait height: 85–110% of the canvas height (head near the top third line; crop at chest or waist by the canvas edge, never at the neck or knees).
- Headline cap height: 18–30% of the canvas height for FB/X; 22–35% for LinkedIn company (very short canvas).
- Negative space: at least 25% of the canvas should be calm (sky, blur, flat colour).
- One diagonal or curve (road, mic stand, brush slash, flag line) to lead from the text to the face.

## Depth stack (back to front)
1. Base plate (sky, city, landscape, gradient)
2. Symbolic or ghost layer (low-opacity double exposure, sketch skyline, giant watermark word)
3. Mid props (photo cards, flags, crowd strip, torn paper panel)
4. Portrait cut-out (+ rim light, contact shadow)
5. Foreground overlap (flags, crowd heads, mic, haze) crossing the bottom of the portrait
6. Typography (+ effects)
7. Finishing: grade, grain, vignette

Overlap between layers (wordmark behind the head, flags across the torso) creates the "designed in Photoshop" look. Flat side-by-side placement looks templated.

## Multi-platform layouts
Design a **master** at 3000×1000 (3:1) or larger, then re-layout per platform:
- Move the text block to each platform's safe zone instead of cropping it.
- LinkedIn company (5.9:1) needs its own layout: a smaller portrait or no portrait, a one-line message.
- Check every export with `scripts/safe_zone_preview.py`.
