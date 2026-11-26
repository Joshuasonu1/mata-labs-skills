# Workflow: research and asset selection

## 0. Check which tools are actually available (every job)
Before planning, check and **state honestly** in the brief which of these you can use:
| Tool | How to check | If missing |
|---|---|---|
| Photoshop desktop (scriptable) | `Photoshop.exe` exists under `C:\Program Files\Adobe\Adobe Photoshop*`; a test JSX writes a log file | build plates in Python/PIL, deliver PSD-ready layers plus a manual Photoshop handoff note |
| ChatGPT desktop app (image gen) | computer-use `request_access` for "ChatGPT" is granted and the app opens | write ready-to-paste prompts in `prompts.md` for the user; or use the Adobe connector or stock |
| Adobe connector (Firefly / Remove BG / Stock) | `adobe_mandatory_init` succeeds | skip |
| Browser (built-in / Chrome) | browser tools load | use WebSearch summaries only |
Never claim a tool was used if it wasn't. Say "handoff" where the user must do a step.

## 1. Concept first
Write: **story** (what the cover says), **mood** (cinematic, calm…), **hero image** (portrait pose), **one symbol** (landmark, road, flags, works), **system** (from SKILL.md).

## 2. Inspiration pass (look, don't take)
Browse 10–20 references on Behance, Pinterest and Dribbble for the chosen system plus "facebook cover / twitter header / linkedin banner". Note 3 concrete techniques to use (e.g. "wordmark behind head", "torn scroll with curl shadow"). Don't save or copy artworks.

## 3. Collect real assets from the client
Portraits (several poses), event and works photos, logos, brand colours, fonts. Prefer photos where the subject faces the side where the text will go.

## 4. Fill gaps
Order of preference: **client's real photo**, then **free stock (Unsplash/Pexels/Pixabay)** for scenery and texture, then **generated plate** (ChatGPT/Firefly) for mood, light and texture, then premium stock (Envato/Adobe/Freepik) with the licence logged.
Selection criteria: matches the concept; light direction compatible with the portrait; empty space where the text and avatar go; resolution ≥ 2× the export; no people, text or logos (unless the client's own).

## 5. Log
Append to `covers/assets_log.md` (file, source URL or "ChatGPT prompt: …", licence, usage).
