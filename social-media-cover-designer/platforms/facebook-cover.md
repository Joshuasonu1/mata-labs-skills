# Facebook Page cover

## Official specs (checked Nov 2026; re-verify each job, because Meta changes these)
Meta's own pages disagree, so design for the **strictest** combination:
- Help Center "Page profile picture and cover photo dimensions" ([facebook.com/help/125379114252045](https://www.facebook.com/help/125379114252045)): upload **851×315** (sRGB JPG, < 100 KB loads fastest), minimum 400×150. Mobile shows the cover at about 2.4:1, and the profile picture overlaps the cover by about 40px.
- Meta's "fb-answers" size guide ([facebook.com/fb-answers/facebook-cover-photo-size-guide](https://www.facebook.com/fb-answers/facebook-cover-photo-size-guide/)): displays at **820×312 desktop** and **640×360 mobile**. Safe zone about 820×360 (i.e. mobile shows the full height but crops the sides).

## Our export preset
| File | Size | Notes |
|---|---|---|
| `*_facebook.jpg` | **1640×624** (2× of 820×312) | sRGB JPG quality 90; Facebook downsamples, so 2× stays sharp |
| `*_facebook_851.jpg` | 851×315 | fallback at the Help Center size |
Master canvas for layout: 1640×624.

## Safe zones (on the 1640×624 canvas)
- **Mobile crop:** mobile is 16:9-ish (640×360), so only the **central ≈ 1110px** of width shows (x ≈ 265–1375). Headline and face must sit inside x 300–1340.
- **Profile picture:** a circle overlapping the **bottom-left** (desktop, new Pages layout), roughly x 40–400, y 420–624 at 2× scale. Keep it clear.
- **Top and bottom:** keep text 40px away from the top and 90px from the bottom (Page name and buttons sit below; a gradient may darken the bottom on some clients).
- Put the face in the right half of the safe width (x ≈ 820–1340) and the headline in x ≈ 420–900.

## Layout tips
- Facebook is the widest, story-friendly canvas for documentary collage strips and rally crowds.
- Avoid small body text: it shows at 640px wide on phones.
- Preview: `python scripts/safe_zone_preview.py <file> facebook`.
