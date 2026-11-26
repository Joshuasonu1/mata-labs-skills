---
name: polcomms-reels
description: Edit political-communications reels (press-conference cut-downs and cinematic mass reels) for MATA Labs PolComms clients such as Viresh Sir and Dasoju Sravan (DSk), using the brand files in the video toolkit.
---

# PolComms reels

Follow `reel-production-core` for setup, pipeline, SFX rules, QC and truth/rights rules. This skill adds the PolComms formats and the per-politician brand layers. Brand geometry in `brands/*.json` was MEASURED from the team's reference reels; use those numbers rather than guessing.

## Pick the format
- **Press reel**: speaker footage cut into hook-led reels from timestamps the user gives (or moments proposed from a transcript).
- **Cinematic**: mass reel of convoy, crowd, walking, campaigning footage, beat-synced to trending audio.

## Brand layers
**Viresh Sir** (`viresh.json`). Reference reel: continuous speech, almost no cuts, about -14 LUFS.
- 1080x1920 black canvas; rounded press footage frame (x20 y332 w1040 h1250 radius 52, source cover-cropped); yellow (#FFD51E) rounded Telugu caption pill with bold dark (#151515) text INSIDE the frame near its bottom (about y 1235), one short phrase replaced when the spoken idea changes; approved circular party badge inside the frame, bottom-centre, below the pill (about y 1370, 110px); fine white dot-screen halftone strongest in the top ~40% (`halftone {mode:"overlay",cell:12,strength:0.9}`), faces and glyphs must stay clear.
- Clean cuts by default, restrained zoom (<= 1.08), optional soft whoosh only on real shot changes, text_pop low on key captions, impact at most once, no invented crowd audio, no glitch intro, no DSk pink.
- The press-conference DOCX look (red outlined text, whip-pan heavy b-roll, anthem BGM, crowd roar) is NOT what the reference reel shows. Offer it only as a clearly labelled variant if asked; any crowd roar must be real recorded event audio.

**Dasoju Sravan / DSk** (`dsk.json`), two sanctioned layouts seen in references (confirm which is current if unclear):
- **A, paper-white** (1080x1920): Telangana-map paper header, BRS car logo, name 'Dr Sravan Dasoju' in condensed bold navy, designation line, white rounded footage frame (x30 y668 w1000 h570), torn-top pink (#E90878) claim strip with white condensed bold English text that BUILDS word by word as spoken, document/crowd collage footer. Reference loudness is -17.4 LUFS; normalise to about -14 unless told otherwise.
- **B, pink full** ('PRESS MEET - 01' series): full pink background, tag top-left, BRS logo and name, white framed footage, large white Telugu serif headline with a pale rounded sub-pill (figures such as rupee amounts), full-width topical b-roll cutaways with red-circle callouts. Opponent cut-out portraits need approved assets.
- Brief glitch opening with glitch SFX is the team's convention (keep under about 1 s); paper_tear for document reveals; keyboard_typing for document text; riser into a factual reveal.
- DCC-Ash (names) and a Telugu font must be supplied. The layout artwork (header, claim strip, footer collage) must be supplied as a PNG plate (use `bg_image`).

**New politician**: copy a brand file, fill every field from their guide and reference reel (measure the layout from a frame), mark unverified values; ask for approved badge/logo, fonts, one gold-standard reel, caption language.

## Press reel recipe
1. Input: source video, HH:MM:SS ranges, optional hook line, verified caption text. No timestamps: ask, or propose ranges labelled as suggestions (from a transcript).
2. Hook: strongest complete statement first (first 1-2 s). Never cut a word or end a line before the speaker finishes the sentence: follow "Speech cuts" in `reel-production-core` (measure the pause at every in/out; extend to the real pause even if the reel gets longer).
3. Use the brand layout; captions change only when the idea changes; badge/logo via `persistent`.
4. Energy tools with restraint per brand: zoom on emphasis, halftone, whip + whoosh only on real shot changes, shutter on a camera-flash moment.
5. Music: licensed bed from the team, ducked. The team chooses trending audio; never claim to know what is trending.
6. Length 20-45 s unless told otherwise. Halftone here is full-frame; speaker-only isolation needs a matte (offer as optional).

## Cinematic recipe
1. Inputs: real clip folder, licensed trending track, verified text lines.
2. `beat_grid.py track.mp3 --out beats.json`; spot-check tempo by ear.
3. `plan_cinematic.py --brand <b> --clips clips/ --beats beats.json --music track.mp3 --out edl.json --duration N --every 2 --accelerate --slowmo-every K --speed-every M --text "A|B|C"`.
4. Review the draft EDL against what the clips show: vary convoy/crowd/walking, put the strongest shot on the drop, slo-mo (`speed:0.5`) on emotional moments, speed-up (`speed:2.0`) on transit.
5. Render text PNGs from `text_requests`, build, QC. Heavier kinetic type needs the motion-graphics renderer or an editor.
6. Real footage only; no fabricated crowds, events or applause.

## Debate / interview / rally reels: the @ktrtrs grammar
For interview cut-downs, rebuttal reels and rally speeches, read `ktr-edit-grammar.md` (in this skill folder) first. Short version:
- Frame 0 and the last 2-3 s are the same designed poster (grid thumbnail); about 0.5 s silence, then the hook in the leader's voice.
- Speech is the spine; cut on sentences, not beats. After every named number, year, document or rival, cut to a proof visual, then back to A-roll.
- Rival/archive clips in B&W (rounded card on black for openers, RGB glitch out); the leader stays in colour.
- Graphic kit: verdict stamps, red brush X slams, year/number ladders, giant red number, polaroid evidence card, newspaper strip with typing line, article push-ins, page-curl documents, typing quote box, kinetic type, map/data viz.
- Transitions: hard cuts; radial zoom-blur into crowd wides; glitch out of archive; rare dissolve.
- Sound: -14 LUFS, LRA about 3 LU, true peak <= -1 dBTP; low continuous bed; SFX only on graphics (glitch hit, riser into the reveal, pop per number/stamp, shutter on documents, one impact per reel).
- Style reference only: never copy another account's posters or wording, and every on-screen claim needs a client-supplied source.

## Always
Speech in ANY format (press reel or mass reel with speech elevations): never cut a word, never end a line before the sentence is finished; check every in/out against the audio, not just the transcript (see `reel-production-core` > Speech cuts).
Verify speaker name, designation and Telugu spelling with the user. MATA Labs stays non-partisan in tone: add no claims, attacks or statistics that were not supplied.
