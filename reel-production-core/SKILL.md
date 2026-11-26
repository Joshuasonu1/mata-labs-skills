---
name: reel-production-core
description: Shared workflow, EDL format, SFX rules and QC checklist for building vertical reels with the MATA Labs video toolkit (used by the PolComms and SDOT video skills).
---

# Reel production core

The common engine behind every MATA Labs video skill. Brand-specific looks live in the brand files; this skill is the *how*.

## Setup (every session)
1. Find `video-toolkit.zip` (or the unzipped `video-toolkit/` folder, or `toolkit/` inside dsk-studio) among the user's files. If missing, ask for it. Unzip into its own new folder.
2. Inputs the editor/user must supply: source footage, caption text (Telugu included, already verified), licensed music, approved logos/party badges, fonts in `fonts/`. The cloud workspace has NO speech-to-text and NO Telugu font; never invent a transcript. If Telugu text renders as boxes, stop and ask for the font. (On the user's own machine, `scripts/transcribe.py` runs Whisper.)
3. Read the brand file in `brands/` for the project (`viresh.json`, `dsk.json`, `sdot.json`). Surface any `OPEN_CONFLICT` or `NEEDS INPUT` entries before building; do not silently pick a side.

## Pipeline
1. Analyse the footage (ffprobe, extract a few frames and look at them). Say what you see.
2. Write captions/overlays as PNGs: `python3 scripts/render_card.py spec.json out.png` (spec: `{"type":"caption","brand":"viresh","text":"..."}`; types: caption, lower_third, stat_card, polaroid_credit).
3. Write the EDL JSON (see `examples/`). Times are seconds or HH:MM:SS. SFX `"at":"seg:N"` lands on the start of segment N.
4. Build: `python3 scripts/build_reel.py edl.json` -> `out.mp4` + `out.timeline.json`.
5. QC: `python3 scripts/qc_check.py out.mp4 --sheet sheet.png`. LOOK at the contact sheet and at 3+ individual frames (open, hook, a caption, last frame). Fix and rebuild; do not deliver a first render unseen.
6. Deliver the MP4 plus the EDL JSON (so editors can tweak and re-run) and a 3-5 line note: what was made, open assumptions, items for human check.

## EDL essentials
Top level: `brand`, `out`, `segments[]`, optional `persistent[]` (logo/badge PNGs on every segment), `bg_image`, `audio{vo, music{file,gain_db,duck}, sfx[]}`.
Segment: `src,in,out,layout(frame|full|polaroid),zoom{from,to},speed,halftone{mode,cell,strength},whip_in,whip_out,audio(keep|mute),captions[{t0,t1,png,y,x,anim}]`; polaroid adds `tilt,credit_png`. Caption times are relative to the segment. Segment lengths snap to whole frames so beat-locked cuts stay locked. Halftone: prefer `mode:"overlay"` (fast); `mode:"screen"` is slow.

## Speech cuts: never cut a word or an unfinished sentence (user rule, 2026-11-25)
Every speech piece must START after the previous sentence has ended and END only where the speaker finishes the sentence and actually pauses. A line that sounds clipped is a failed render, even if the transcript looked right.
- Whisper word timestamps are often 0.3-0.6 s late or early; never trust them alone for in/out points.
- Before rendering, measure the audio around every in and out (RMS in 20-50 ms windows, e.g. ffmpeg -> numpy): the out point must sit in a real pause (about 20 dB or more below the line's peak, or below about -30 dBFS) and speech must NOT resume within the next ~0.3 s. If it resumes, the sentence is not finished: extend the out point to the next real pause, even if that adds a few seconds.
- The in point must also be in a pause: no tail of the previous word at the start.
- If the speaker runs one sentence straight into the next with no pause, keep the whole thought or pick a different line. Do not chop mid-thought to hit a target length; length targets are soft.
- Lists ("three things: A, B, C") must include the lead-in and every item, through to the pause after the last one.
- Move the matching picture segment and subtitle with every voice edge change (lip sync), then re-run the edge check on the final config and report it (each line: pause follows, OK).

## Colour grading (learned from Enam Alamin, "Pro Color Grading Workflow in Premiere", youtube QTEN6MUMCPI)
Grade in separate, named layers in this order (Premiere: stacked Lumetri effects; ffmpeg: chained filters). Check with scopes, not eyes.
1. **Input**: log footage -> apply the log-to-Rec709 LUT first (`lut3d=file.cube`). Phone/press footage is usually already Rec709: skip.
2. **Exposure + white balance**: luma waveform; highlights at or below ~90 IRE unless a real light source; whites white and blacks black; fix with temperature/tint until skin looks clean.
3. **Contrast with curves** (3 points): shadows down but not crushed (~5 IRE), mids slightly up for skin, highlights under 90-95 IRE. Filmic trick: lift the black point slightly for "milky" blacks.
4. **Masks for problem areas** (blown sky: feathered mask, lower exposure/mids). The mask layer must sit ABOVE the contrast layer or the detail does not come back.
5. **Skin tone**: tracked ellipse mask or HSL key on skin; check the vectorscope skin line; correct green/magenta with tint, then a touch of saturation and lift.
6. **Colour separation** (orange-teal or any complementary pair that fits the story): RGB curves (red down in shadows, up in highlights; blue down in highlights) and desaturate pure blacks (luma vs saturation).
7. **Background-only tweaks** with an inverted face mask: hue-vs-sat / hue-vs-hue (shift blues to teal, yellows to orange).
8. **Glow + grain**: duplicate layer, gaussian blur ~30, luma key the highlights, blend Lighten at low opacity; then a film-grain overlay.
Tested ffmpeg chain (adjust per clip; keep brand colours and party colours accurate, do not shift pink/saffron/green party colours):
`curves=master='0/0.04 0.25/0.22 0.5/0.52 0.92/0.9 1/0.94',colorbalance=rs=-0.08:bs=0.08:rh=0.06:bh=-0.06:rm=0.03,eq=saturation=1.08,split[a][b];[b]lutyuv=y='if(gt(val,200),val,0)',gblur=sigma=30[gl];[a][gl]blend=all_mode=lighten:all_opacity=0.35,noise=alls=6:allf=t+u`
Grade footage to match before adding graphics; keep one look per reel, and keep skin natural on politicians (no orange faces).

## SFX rules
- Library and intended uses: `sfx/catalog.json`. Fire an SFX only when something visibly happens (cut, caption appear, reveal). Silence beats noise.
- Dialogue/VO always wins: music about -24 to -28 dB under speech with ducking, SFX about -14 to -20 dB.
- Synthetic SFX (text_pop, tick, shutter, impact_low, scroll_swish) are placeholders; say so when delivering.
- Never add fabricated crowd applause/reactions or any audio that implies events that did not occur; use only real recorded event audio.

## Truth and rights (non-negotiable)
- Never invent quotes, statistics, rankings, names, party assets, crowd reactions or footage. Every number on screen needs a supplied source.
- Do not misrepresent footage with edits or captions; keep context.
- Social-media b-roll and trending audio are supplied by the team: remind them to confirm reuse rights and credit handles.
- Use only approved logos/badges as supplied; never rebuild or recolour them.

## Final checklist (state each as done / not done)
Resolution 1080x1920 H.264 AAC 48k; loudness about -14 LUFS; every speech line starts and ends in a measured pause with the sentence finished (no clipped words); hook in first 1-2 s; captions inside safe zone (top ~180px and bottom ~280px clear); text readable at phone size; spelling and Telugu glyphs (human check); facts match the source; logo/badge correct; SFX motivated; music quieter than speech; no black first/last frames unless intended; handle credits present for borrowed clips.

## When output is off
Fix the cause in the brand file or EDL, not just the single video, and tell the user which file changed.
