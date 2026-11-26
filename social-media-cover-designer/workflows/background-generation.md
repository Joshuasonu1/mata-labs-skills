# Workflow: background plate generation (ChatGPT, then Photoshop)

Generate **scenery, light and texture only**. Never a person, never a face, never a crowd or event presented as real.

## Prompt template
```
Create an image: <wide 3:1 | 4:1 | 16:9> photorealistic <scene>, <time of day / light>, <mood/colour>.
Leave <left third / right half / top band> simple and uncluttered for text and a portrait to be added later.
NO people, NO faces, NO text, NO letters, NO logos, NO watermarks, NO flags of any party.
High detail, natural colours, realistic photography.
```
Image models often return portrait or square images. Ask for the wide ratio explicitly; if it comes back narrow, extend it in Photoshop (Generative Expand / Content-Aware Fill) on **background-only** areas.

Useful plates per system: cinematic (fire glow, embers, smoke on black), editorial (sky, lake, hills), premium portrait (dusk skyline), minimalist (pencil skyline on white), documentary (soft sky with birds), leadership (golden gradient, sun flare, mandala). Light and texture plates are generated on **pure black** (blend Screen) or **pure white** (blend Multiply).

## ChatGPT desktop procedure (computer use)
1. `request_access` ["ChatGPT"]; open the app; click **New chat** (never post into the user's existing chats).
2. Paste the prompt, press Enter, and wait about 60–90 s ("Creating image…").
3. Right-click the image, choose **Download a copy**, and in the Save As dialog click the File name box, press Ctrl+A, then type the full path `<project>/covers/assets/<name>.png` and click Save. (If clicking the image opens the viewer, use its download icon instead.)
4. Verify the file exists and check its size with Python. Log the prompt in `assets_log.md`.
5. Look at it: wrong ratio, stray people or text, or "AI look" (melted details, over-saturation) means regenerate with a corrected prompt.

## Fallback (ChatGPT unavailable)
Write the prompts in `covers/prompts.md`, ask the user to generate and drop the files into `covers/assets/`, or use stock.

## Prepare the plate in Photoshop
- Place it as a Smart Object; scale to cover; extend or crop to the platform canvas.
- Blur slightly (Gaussian 3–8px or Lens Blur) to create depth behind the subject. It also hides AI micro-artefacts.
- Check that nothing behind the head reads as part of the person (flowers, poles, branches growing out of the head). Move or blur.
- Pre-grade toward the system palette before adding the portrait.
