# Photoshop techniques for campaign posters (Photoshop 2027, Windows)

Working habits and feature verdicts distilled from PiXimperfect's beginner course (Lessons 1–3) and the "Photoshop 2027: Top 21 New Features" review (Nov 2026). Credit costs are as reported in that review and may change.

## Setup (once per machine)
- **Crop tool:** untick **Delete Cropped Pixels**. If it stays on, recropping or re-framing for another format later is impossible.
- **Move tool:** untick Auto-Select (when you need it for one click, hold `Ctrl` and click) and untick Show Transform Controls. Set **Align To = Canvas**. With a selection active, alignment then uses the selection; without one, it uses the canvas.
- **Preferences → Tools:** untick *Enable Flick Panning*; tick *Show Reference Point when using Transform*.
- **Preferences → Image Processing:** set Select Subject / Remove Background to **Cloud**. It's more accurate on hair and doesn't use credits.
- **Preferences → Type:** set the placeholder text to a Telugu line (the review showed Hindi working) to see Indic shaping as soon as you click with the Type tool.
- A tool behaving oddly (most often a brush whose blend mode was left non-Normal): click the arrow next to the tool in the Options bar → gear → **Reset Tool**.

## Non-destructive habits
- Put paint, removal and retouch work on a **new empty layer**. With the Remove/Healing tools, tick **Sample All Layers**.
- The **Patch tool won't work on an empty layer**. Copy the layer with `Ctrl+J` and patch the copy.
- Use adjustments as **adjustment layers**. With a selection active, the new adjustment layer gets a mask that limits it to that area.
- `Alt`-click a layer's eye icon to solo it and check what a removal layer actually contains.
- Save the layered master with `Ctrl+S` (PSD). Make the deliverables with **File → Export As** (PNG/JPEG); Save As won't offer social formats while the file has layers.

## Cut-outs and backgrounds
- **Select Subject (Cloud)** or **Remove Background** (Contextual Task Bar) on the original portrait. Check hair at 200% over a **solid-colour fill layer** (black, then white) before compositing.
- **Object Selection → Select People** can isolate parts of a person: clothes, hair, skin. Use it to mask Hue/Sat on **clothes only** (never skin, see `portrait-preservation.md`).
- Add to or subtract from a selection with the Lasso: `Shift` adds, `Alt` subtracts, `Ctrl+Shift+I` inverts.
- **Clean up event and rally backgrounds** with **Remove tool → Find Distractions**:
  - **People** selects background people and lets you edit the selection before you apply.
  - **Wires & Cables** applies immediately, so run it on a new layer.
  - **Atmospheric effects** (fog, haze, smoke) and **Shadows** (2027) kept detail very well in the review. About 10 credits each.
  - **Turn Generative AI off** for small removals the surrounding texture can cover: it's faster and keeps the real texture. Turn it **On** (not Auto) for big or complex areas.
  - Never let a Find Distractions selection touch the leader. Subtract them with `Alt` before applying.
- **Patch tool (Source, Normal)** often gives a more natural result than Remove on texture such as walls, stage backdrops and sky, because you choose the source patch yourself.
- **Content-Aware Fill without AI, at full resolution:** select the area, Edit → Content-Aware Fill → Output to **New Layer**.
- `Shift`-click with Remove or Healing draws a straight stroke. Use it for poles, railings and banner ropes.

## Re-framing for 4:5 / 1:1 / 9:16
- Crop tool with **Fill: Generative Expand** keeps the original pixels and invents only the new border. Use it on **background plates and scenery only**, and check the seam.
- **Do not use Generative Recompose** (Edit menu). In the review it changed the person's face and clothing patterns.
- Crop **reference point**: drag the point onto the leader's eye, then `Alt`-drag a corner so the crop scales around it. This keeps the face on a thirds line and leaves room for the headline. Press `O` to cycle overlays.
- To centre a headline in the empty space: draw a Rectangular Marquee over that space, then use the Move tool's align buttons. `Ctrl+D` deselects.

## Grading, texture and lighting
- **Camera Raw Denoise now works on JPEGs:** Filter → Convert for Smart Filters → Camera Raw Filter → Details → Denoise. Use it on phone-shot crowd and event photos. It isn't generative, so it's also safe on the portrait (check at 100%).
- **Camera Raw → Color Grading → Apply LUT:** up to 3 LUTs, global or masked, and you can load your own .cube files. Useful for a consistent series grade.
- **Camera Raw → Effects → Glow:** Bloom for stage lights, **Streak / Motion** for kinetic rally highlights. Apply it to the plate, not the face.
- **Blend If** (double-click the layer): drag the *Underlying Layer* white slider left so a texture or graphic shows only on darker areas. `Alt`-drag to split the slider for a soft edge.
- Graphics on curved objects (banners, flags, bottles): Smart Object → `Ctrl+T` → right-click Warp → Cylinder, then the Screen or Multiply blend mode. *Layer → Convert to Mockup* (beta) follows fabric folds but broke on curved objects in the review.
- **Don't use the Overlay eye-catchlight trick on the leader.** It paints over face pixels, which breaks the portrait rules.

## Flat client artwork
- **Type → Convert to Text Layers** (beta, about 10 credits) rebuilds a flat JPEG poster into editable text with matched fonts. Untested on Telugu, so check every glyph against the original, and remember the rule that client copy is used verbatim.

## Features banned on the leader's face or body (they regenerate pixels)
| Feature | Problem seen in review |
|---|---|
| Relight layer (Layer → New Relight Layer, 30 credits) | hair detail rebuilt, halos, fails on glass |
| Firefly Upscaler 2 (Image → Generative Upscale) | invents false detail (stripes, buttons) |
| Remove Related Elements | lowers resolution across the whole image. If you must use it on a background, crop to the area first, remove, then Image → Reveal All |
| Generative Recompose | changed the face and outfit |
| Generative Restyle / Camera Angles / AI Assistant | regenerated or unreliable |
These are allowed on background plates only, and must be checked at 100%.

## Advanced library (75 tutorials: text effects, texturing, cinematic posters)
Read these before designing: `C:\Users\hello\Downloads\dsk mass reel\photoshop-kb\` → `ADVANCED_PHOTOSHOP_WORKFLOWS.md` (W1 reference recreation, W3 campaign poster), `CINEMATIC_POSTER_DESIGN.md` §11 (cinematic → campaign guardrails), `TYPOGRAPHY_AND_TEXT_EFFECTS.md`, `IMAGE_TEXTURING_AND_EFFECTS.md`, `YOUTUBE_TUTORIAL_INDEX.md` (sources).
Key additions:
- **Key-light matching**: clipped Curves + Color Balance per element before any effect; nothing brighter than the key light.
- **Painted rim light**: Screen Solid Color, Blend If off the darks, textured brush on the lit side (≤30% on leaders).
- **Contact shadow**: darkest at the touch point.
- **Fire light**: Blend If Red.
- **Fog**: Screen + Colorize.
- **Beam brush**: leading lines.
- **Fringe**: Minimum about 7 on the mask.
- **Brutalist grit**: noise, then Threshold.
- **Print integration**: a displacement map at about 2 px.
- **Type**: gold/chrome via Bevel Depth 1000 + Gradient Map; spray via Fill 0 + Drop Shadow Cone + Noise + Blend If. Never split Telugu text into per-glyph shapes.

## Core compositing techniques (PiXimperfect beginner playlist, 13 lessons)
Full lesson notes with exercises: `C:\Users\hello\Downloads\dsk mass reel\photoshop-kb\` (README = index).
- **Blend modes:** Multiply hides white (birds or line-art on a sky made pure white with a clipped Curves; marble, shadow textures), Screen hides black (smoke, snow, sparks, light leaks), Overlay/Soft Light hide 50% grey (textures, grain, punch), Color fixes *lighting* casts only. To darken or brighten without duplicating the photo, use an **empty Curves layer set to Multiply or Screen** plus Blend If.
- **Blend If** (double-click the layer): *Underlying* sliders hide by the brightness beneath, *This Layer* by its own; always `Alt`-split. Blue-channel Blend If removes a bright sky behind trees and flags with no selection. Logo-painted-on-a-wall look = Multiply copy + Screen copy with Blend If + 1 px blur + a grunge mask.
- **Fill vs Opacity:** in Color/Linear Burn/Dodge, Vivid/Linear Light, Hard Mix and Difference, Fill changes how strongly the layer interacts with what's below. **Grade = warm Solid Color → Hard Mix → Fill 15–25% → Blend If split.** With layer styles, Fill 0% keeps only the effect (embossed slogan in a wall).
- **Fake sun:** soft dab → Color Dodge → untick *Transparency Shapes Layer* → Fill sets the strength, plus a radial gradient glare in Screen mode.
- **Masks:** select first, then add the adjustment (comes pre-masked); `Alt`+mask button = negative mask; feather/density in Properties; **one mask on a group** instead of copied masks; **double masking** (group mask + layer mask) to place a rim highlight only on the lit side.
- **Clipping and groups:** `Alt`+click the line = clip (separate grades for leader vs background). Groups default to Pass Through; set the **group to Normal** to keep its adjustments inside.
- **Halo-free cut-outs:** Select Subject (Cloud) → Select and Mask (Refine Hair, Refine Edge brush, On Black view) → `Ctrl`+click the mask → Contract 2 px → invert → fill black. **Before blurring the background, remove the subject from it:** load the mask → Expand 50 px → Content-Aware Fill, then blur.
- **Depth:** Blur Gallery Iris/Field/Tilt-Shift on a smart object; Noise tab about 10% so the grain matches. Light direction mismatch → flip the **plate**, not the leader.
- **Colour:** Hue/Sat advanced targeting (push to extremes to see the range, narrow it, soften the falloff, reset, then edit) to match flags and scarves to the brand hex while skin drops out of range; Prominent Colors preset; colour before texture.
- **Camera Raw:** RAW → `Shift`+Open Object (re-editable WB); 16-bit Adobe RGB working space; masks Background/Sky (subtract People to protect faces); presets per event; `P` before/after, `O`/`U` clipping.
- **Brushes:** Flow (builds up as you paint) vs Opacity (per stroke); `Shift`+number = flow; scatter-brush presets (dust, embers, petals) with *Include Tool Settings*; watercolor mask reveals keep face pixels original.
- **Delivery:** autosave recovery 5 min; Save As for versions, Save a Copy for previews; PSD up to 2 GB → PSB; Export As with sRGB + embed; PNG for text-heavy posters.

## Shortcut card
`V` Move · `C` Crop · `B` Brush · `L` Lasso · `J` Healing/Remove group (`Shift+J` cycles) · hold `~` to erase with the brush · `]`/`[` brush size · `Alt`+right-drag for on-canvas size/hardness · `X` swap colours · `Ctrl+J` duplicate layer · `Ctrl+T` transform · `Ctrl+D` deselect · `Ctrl+Shift+I` invert · `Space` pan · `Ctrl+Space`-drag zoom · hold `H` bird's-eye · `Ctrl+0` fit · hold a tool key to borrow that tool, release to return
