---
name: zptc-captions
description: Add the "ZPTC style" negative-text captions to a reel - small white uppercase label over a big condensed uppercase line whose letters show the footage's inverted colours, in the lower band of the rounded footage frame - timed to the voiceover, as a burned-in MP4 and an editable Premiere Pro XML, with optional SFX. Use when the user says "ZPTC captions", "ZPTC style", "add captions like previous", "same captions as the election reels", or gives a Viresh Sir election reel plus a script to caption.
---

# ZPTC captions

The saved caption look from the Viresh Sir Kurupam ZPTC election reels (Nov 2026). Everything needed is in this skill folder: `scripts/` (Python) and `scripts/caption_styles/zptc.json` (all style settings). Follow `reel-production-core` truth rules: caption only words that are in the supplied script and actually spoken.

## The look (do not change unless asked)
- Big line: Bahnschrift Bold Condensed, uppercase, 150 px (shrinks to 96 to fit). Letters = negative of the footage under them (difference vs grey 225, brightness floor 175), soft dark glow behind.
- Label: Bahnschrift Bold, white, 54 px, the first ~third of the words, above the big line, left edges aligned.
- Position: centred, 82% down the footage frame, 60 px inside its edges. Never on the black canvas, never on faces. Placement adapts per caption to shots with a smaller or zooming frame (median frame size over the caption).
- Max 5 words per card (long lines split at "..." / "," then evenly, time shared by character count). Trailing . , dropped; ? ! kept. 0.25 s slide-up fade-in, 0.12 s fade-out.

## Workflow
Work in the user's project folder (e.g. `Desktop\files tdp`). Run the scripts from this skill's `scripts/` folder by full path. Needs Python 3.12 (`py -3.12`) with numpy, Pillow, faster-whisper, and ffmpeg on PATH.

1. **Probe**: `ffprobe` duration/frames; grab a frame and confirm the rounded footage frame (default x114-965, y405-1597 on a 1080x1920 black canvas). Make a contact sheet and look at it.
2. **Timing - fast path first.** If an earlier cut of this reel already has a captions file (same voiceover, new edit), retime it by audio matching - seconds, not minutes:
   `py -3.12 <skill>/scripts/match_timing.py "<old video>" captions_<old>.json "<new video>" captions_<name>.json`
   Read its table: lines flagged "low confidence" or "nudged" get a look in QC. Then apply any text changes the user made to the script (e.g. "YISU" -> "Young India Skills University"; a longer phrase may need its end moved to the next line's start).
   **Only for genuinely new voiceover**: `py -3.12 <skill>/scripts/transcribe_words.py "<video>"` (CPU Whisper; slow, and unreliable under loud music - run it on short sections, never the whole reel in one go). Telugu VO prints as an English translation; map each script line to its phrase by meaning and pauses. Use the start of each phrase, end just before the next. Write `captions_<name>.json` = `[[start, end, "text"], ...]` (see `examples/captions_example.json`). Split a long line into explicit entries when its parts are spoken at uneven pace.
3. **Render - one pass**: `py -3.12 <skill>/scripts/negative_captions.py "<video>" captions_<name>.json <name>_captioned.mp4 --style zptc` (`--preview 12` for a quick test). Check the frame rate is read from the video (it is; never assume 29.97). If the reel opens with a title collage covered in its own text (the DSK protest reels: collage until ~17.6 s), add `--top-band-until 17.6` so those captions go in the black space above the collage - same pass, no second render. A single caption can also name its own preset as a 4th entry: `[start, end, "text", "zptc_top_band"]`. Never render twice to combine placements (it drops frames at the end).
   Progress prints every 240 frames with a percentage; tell the user the estimate (about 1.5-2 min for a 110 s reel).
4. **QC (always)**: extract 12-16 frames at caption midpoints, tile them, LOOK: caption on its spoken line, inside the footage, lower band, off faces, readable. Check any shot with a different/animated frame up close. Fix and re-render before delivering.
5. **Premiere**: `py -3.12 <skill>/scripts/make_premiere.py "<video>" captions_<name>.json Premiere_<name> "<Title>" [sfx.json]`. Then verify every `<pathurl>` exists. Tracks: V1 video, V2 glow, V3 negative text (Difference blend), V4 label + 35% white lift, A1/A2 source audio, A3/A4 SFX.
6. **SFX (only if asked)**: plan in a JSON like `examples/sfx_example.json` - soft whooshes (-20 dB) only on real shot cuts (`ffmpeg select='gt(scene,0.25)'`), at most one `impact_low` (-16 dB), optional quiet `text_pop`; library at `C:/Users/hello/Documents/dsk-studio/toolkit/sfx`. Mix: `py -3.12 <skill>/scripts/sfx_mix.py "<video>" sfx.json <captioned>.mp4 <out>.mp4` (normalises to -14 LUFS). Synthetic SFX are placeholders - say so. No crowd/applause sounds.
7. **Deliver**: send the MP4 (SendUserFile) and give the Premiere XML path; 3-5 lines on what was made and what to check.

## Always flag
- Script lines not present in the voiceover (leave them out, list them).
- Numbers the speech recogniser hears differently from the script (e.g. the Kurupam majority: script 3,656, ASR heard 3,646) - keep the script's text and ask the user to confirm.
- Spelling of names (Viresh Chandra Dev, Kutami, Kurupam) is the user's to verify.

## Tuning
To change the look, copy `scripts/caption_styles/zptc.json` to a new name and pass `--style <name>`. Keep `zptc.json` as the approved reference.
