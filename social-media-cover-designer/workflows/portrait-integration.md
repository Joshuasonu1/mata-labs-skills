# Workflow: portrait integration (Photoshop)

Read `references/portrait-preservation.md` first. The face pixels are never painted or generated.

## 1. Extract
- Downscale huge originals to ≤ 2100px tall for speed, keeping the original archived.
- Photoshop **Remove Background** (scripted: `scripts/ps_cutout.jsx`), or Select Subject, then Select and Mask for hair (Refine Hair, Decontaminate Colors 50–70%).
- Inspect at 200%: hair edges, between the arms, glasses, earrings. Busy backgrounds (rallies) often keep extra people or logos, so crop tighter around the subject **before** Remove Background and re-run. If it still fails, use a cleaner photo.

## 2. Place
- Scale per `references/composition-guide.md`; crop by the canvas edge (chest or waist), never mid-neck.
- The face looks into the frame toward the text.
- Hide anything that would extend into the avatar zone.

## 3. Match (clipped adjustment layers)
1. **Curves**: match black and white points to the plate.
2. **Colour Balance / Photo Filter** 10–25% toward the plate's light colour.
3. **Brightness**: the face stays 0.5–1 stop brighter than the background right behind it.

## 4. Light
- **Rim / light wrap:** a new layer clipped to the subject, soft brush in the plate's brightest colour along the edge facing the light source, Screen 20–35%. Or Outer Glow ≤ 25%, size 20–40 px, in the light colour (not white).
- **Contact shadow:** a soft, low-opacity (15–25%) shadow offset **away from the light**, under the arms or where the body meets panels. **No dark halo** around the head, which shows as a dirty edge on bright skies.

## 5. Atmosphere
Haze or smoke over the lower body (where it meets the crowd or road) at 20–40%; foreground elements (flags, mic, crowd heads) crossing the torso create depth.

## 6. Verify identity
Put the original next to the composite at 100%. Same features, proportions, skin tone, expression. If any adjustment shifted skin hue noticeably, reduce it.

## Scripting notes (Photoshop 2027, ExtendScript)
- Launch: `Photoshop.exe <run.jsx>` with Photoshop already open; click **Yes** on the run-script prompt the first time.
- Pass data as UTF-8 JSON; write progress to a text file; don't rely on COM (`Photoshop.Application` may not be registered).
- Layer FX via ActionManager (`setd` on `Lefx`): see `scripts/ps_helpers.jsx`.
