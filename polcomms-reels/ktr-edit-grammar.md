# Mass-edit grammar learned from @ktrtrs reels (studied 2026-11-26)

Source: 12 reels from instagram.com/ktrtrs (DgKfa83BJLE "Rated 10/10" studied frame by frame + audio; 11 more at 1 fps + loudness). Local copies: `dsk mass reel/reference_reels/ktrtrs/` (contact sheets in `sheets/`, notes in `notes.json`, board `board.html`).
Use this as the reference grammar for **debate / interview / rally-speech reels** ("explainer-attack" and "rally" formats). It is a style reference only: never copy their posters, wording or claims. Every number, quote, headline and document on screen must come from the client with a source.

## 1. Structure (60-80 s)
- **Frame 0 = the designed poster** (cover). The same poster closes the reel for the last 2-3 s. Instagram uses frame 0 as the grid thumbnail, so the grid reads as movie posters. Poster: cut-out of the leader, a huge brush or condensed title (Telugu or English), torn-paper/brush edges, one accent colour.
- **About 0.5 s of silence** after the poster frame, then the hook line in the leader's voice.
- **Speech is the spine.** Cuts follow sentences, not a beat grid (measured: no beat grid on any reel; cut-to-beat sync = chance). All "Speech cuts" rules in `reel-production-core` apply.
- **Proof after every claim**: the moment a number, year, scheme, document or rival is named, cut to a picture of it (graphic, news screenshot, document, archive clip, map, chart), then return to the A-roll.
- Opening variant for rebuttal reels: start on the **rival's archive clip in B&W in a small rounded card on black**, then an **RGB glitch** breaks into the leader's full-colour answer.

## 2. Graphic kit (build each as PNG/MOV overlay)
| Element | Look | When |
|---|---|---|
| Poster cover / end card | cut-out + brush title + torn edges, tilted event card + giant italic number with swoosh | frame 0 and last 2-3 s |
| Rating / verdict stamp | gold outline circle '10/10' popping in; or huge red '10/10' slamming over a blurred-bg cut-out with handwritten script line above | sarcastic verdicts |
| Red brush X slam | red brush X over a B&W photo, repeated per year/item | broken promises lists |
| Year + number ladder | year label top, white number + small word under, on black or B&W photo | data stories |
| Giant red number / '0' | huge red figure with white words above/below on black | punchline numbers |
| Down/up chevrons | stacked animated chevrons between two red numbers | change in a figure |
| Polaroid / cream card | footage inside a cream card, italic red label + big condensed red line | evidence clip |
| Newspaper strip | real headline cropped as a top strip, red grid tint, English line typing letter by letter | cited news |
| Article / document | full-screen screenshot with slow push; page-curl slide between pages; papers sliding onto white blurred bg | proof |
| Quote box | outlined rounded box on maroon/colour panel, serif text typing word by word | key sentence |
| Kinetic type | letters dropping in, arched word settling flat, word swaps, red hand-drawn X over a word | explainer lines |
| Data viz | dark grey map with region filling red, labels popping, dots flying into a hemicycle, light trails, rising bar chart into a big number | policy explainers |
| Cartoon cut-out | hand-drawn caricature sticker at bottom (needs client approval; avoid defamatory imagery) | satire beats |
| Handwritten captions | top third, marker font, white with keyword in yellow/green (red for negative) | motivational / caption-led reels |
| Notebook flatlay end | photo pinned on a notebook on a coffee table, handwritten title | soft / story reels |

## 3. Picture treatments
- **Rival / archive = B&W** (often in a rounded card on black); the leader stays in colour.
- **Duotone tint** (pink/red) on archive stills with a big gold year ('2015').
- **Speaker matte on new backgrounds** (skyline, bokeh, crowd, chalkboard, diagonal stripes): needs a person matte (`object-separation` skill or a supplied matte).
- **Colour isolation** (scene B&W, leader in colour) + heavy vignette: needs a person matte; ffmpeg `colorhold` alone is too weak on red/pink sets.
- **Burned-edge old-film frame** + warm grade for hardship b-roll (dry fields, farmers).
- **Rounded inset with soft shadow over a blurred copy of itself** for vertical-ised 16:9 clips.
- **2-up split stacks** (two photos stacked) and **speaker top / crowd bottom** splits.
- Punch-in crops between wide and tight on the same interview take to hide jump cuts.

## 4. Transitions
Mostly hard cuts. Accents only:
- **Radial zoom-blur whip** into crowd/drone wides (rally reels).
- **RGB-split pixel glitch** about 0.3 s out of an archive clip.
- **Zoom-blur punch-in** onto the speaker for emphasis.
- Rare **cross-dissolve / double exposure** from ground b-roll back to studio.
- Pink/white **flash wash** between b-roll shots.

## 5. Sound (measured)
- Every reel **-14.0 to -15.3 LUFS integrated**, LRA 2-3 LU (dense, even). Keep true peak <= -1 dBTP (two of theirs clip at +1.3/+1.5: do not copy that).
- Music bed low under speech (vocal-chop / trap / corporate pulse), continuous, not cut to picture.
- SFX sparse and tied to graphics: glitch hit (+ sub) on the glitch open; **riser into a big reveal**; **pop/tick on each number, stamp or dot build**; shutter/click on a document; **one punchy impact per reel** on the main punchline. Most cuts have no SFX at all.
- Raw "I was there" reels (protest visits) keep natural audio and get only the end poster.

## 6. ffmpeg recipes (tested on a 1080x1920 frame)
```
# B&W rounded card (radius 40) on black
[0:v]crop=900:900:90:300,scale=820:820,hue=s=0,format=rgba,geq=lum='p(X,Y)':cb='p(X,Y)':a='if(gt(hypot(max(0,abs(X-W/2)-(W/2-40)),max(0,abs(Y-H/2)-(H/2-40))),40),0,255)'[c];[bg][c]overlay=130:480
# RGB-split glitch frame (animate offsets per frame, 6-8 frames)
[0:v]rgbashift=rh=-28:bh=28:gv=6,crop=iw:ih/9:0:ih*0.4,scale=1080:213[s];[0:v]rgbashift=rh=-12:bh=12[b];[b][s]overlay=40:760,noise=alls=20:allf=t
# Radial zoom blur (blend of 4 scales; ramp scales over 4-6 frames for the whip)
[0:v]split=4[a][b][c][d];[b]scale=iw*1.06:-1,crop=1080:1920[b2];[c]scale=iw*1.12:-1,crop=1080:1920[c2];[d]scale=iw*1.2:-1,crop=1080:1920[d2];[a][b2]blend=all_expr='(A+B)/2'[ab];[c2][d2]blend=all_expr='(A+B)/2'[cd];[ab][cd]blend=all_expr='(A+B)/2'
# Pink duotone archive
hue=s=0,colorchannelmixer=rr=1.0:gg=0.62:bb=0.72,curves=master='0/0.12 1/0.95'
```
Colour grade chain: see `reel-production-core` > Colour grading.
