"""Export the negative-text captions as a Premiere Pro sequence (FCP7 XML + PNG layers).

Tracks:
  V1  source video
  V2  halo      (soft dark glow, normal blend, alpha baked in)
  V3  negative  (grey 225 text, blend mode DIFFERENCE -> inverts the footage under it)
  V4  label     (small white label + 35% white over the big line to keep it readable)
  A1/A2 source audio

usage: py -3.12 make_premiere.py input.mp4 captions.json OUT_FOLDER
"""
import json, os, sys, urllib.parse
import numpy as np
from PIL import Image
import negative_captions as nc

TB, NTSC = 30, "TRUE"          # 29.97 fps
FPS = 30000 / 1001
TOTAL_FRAMES = 3545
LIFT_OPACITY = 0.35
HALO_OPACITY = nc.HALO


def url(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "file://localhost/" + urllib.parse.quote(p, safe="/:")


def fr(t):
    return int(round(t * FPS))


def rate():
    return f"<rate><timebase>{TB}</timebase><ntsc>{NTSC}</ntsc></rate>"


def full(layer_rgba, top, left):
    img = np.zeros((nc.H, nc.W, 4), np.uint8)
    h, w = layer_rgba.shape[:2]
    img[top:top + h, left:left + w] = layer_rgba
    return Image.fromarray(img, "RGBA")


def rgba(rgb, alpha):
    a = (alpha.clip(0, 1) * 255).astype(np.uint8)
    out = np.zeros(alpha.shape + (4,), np.uint8)
    out[..., :3] = rgb
    out[..., 3] = a
    return out


def main():
    global TOTAL_FRAMES, FPS, TB, NTSC
    src, capf, outdir = sys.argv[1:4]
    title = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].endswith(".json") else "Kurupam ZPTC"
    import subprocess
    TOTAL_FRAMES = int(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=nb_frames",
         "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
    _, FPS = nc.probe_rate(src)             # real frame rate of this video (24, 25, 29.97, 30 ...)
    nc.FPS = FPS
    NTSC = "TRUE" if abs(FPS - round(FPS)) > 0.01 else "FALSE"
    TB = int(round(FPS))
    png_dir = os.path.join(outdir, "caption_layers")
    os.makedirs(png_dir, exist_ok=True)
    top_until = float(sys.argv[sys.argv.index("--top-band-until") + 1]) if "--top-band-until" in sys.argv else None
    caps = []
    for entry in json.load(open(capf, encoding="utf8")):
        t0, t1, txt = entry[:3]
        style = entry[3] if len(entry) > 3 and entry[3] else (
            "zptc_top_band" if top_until is not None and t0 < top_until else "zptc")
        caps += [(c0, c1, ct, style) for c0, c1, ct in nc.chunks(t0, t1, txt)]

    tracks = {2: [], 3: [], 4: []}
    for i, (t0, t1, txt, style) in enumerate(caps, 1):
        nc.apply_style(style)
        neg, lab, halo, top, left = nc.render(txt, nc.frame_box(src, t0, t1) if nc.ADAPTIVE else None)
        layers = {
            2: ("halo", rgba(0, halo * HALO_OPACITY)),
            3: ("neg", rgba(nc.GREY, neg)),
            4: ("label", rgba(255, np.maximum(lab, neg * LIFT_OPACITY))),
        }
        s, e = fr(t0), fr(t1)
        for tr, (kind, arr) in layers.items():
            name = f"{i:03d}_{kind}.png"
            full(arr, top, left).save(os.path.join(png_dir, name))
            tracks[tr].append((name, s, e, txt.upper(), kind))
    print(len(caps), "caption cards ->", png_dir)

    def still(idx, tr, name, s, e, label, kind):
        n = e - s
        mode = "difference" if kind == "neg" else "normal"
        path = os.path.join(png_dir, name)
        return f"""
        <clipitem id="c{tr}_{idx}">
          <name>{kind}: {label.replace('&', 'and')}</name>
          <enabled>TRUE</enabled>
          <duration>{n}</duration>{rate()}
          <start>{s}</start><end>{e}</end><in>0</in><out>{n}</out>
          <file id="f{tr}_{idx}">
            <name>{name}</name>
            <pathurl>{url(path)}</pathurl>{rate()}
            <duration>{n}</duration>
            <media><video><samplecharacteristics>{rate()}<width>{nc.W}</width><height>{nc.H}</height></samplecharacteristics></video></media>
          </file>
          <compositemode>{mode}</compositemode>
        </clipitem>"""

    vname = os.path.basename(src)
    src_file = f"""<file id="src">
            <name>{vname}</name>
            <pathurl>{url(src)}</pathurl>{rate()}
            <duration>{TOTAL_FRAMES}</duration>
            <media>
              <video><samplecharacteristics>{rate()}<width>{nc.W}</width><height>{nc.H}</height></samplecharacteristics></video>
              <audio><samplecharacteristics><depth>16</depth><samplerate>44100</samplerate></samplecharacteristics><channelcount>2</channelcount></audio>
            </media>
          </file>"""
    v1 = f"""
        <clipitem id="v1">
          <name>{vname}</name><enabled>TRUE</enabled>
          <duration>{TOTAL_FRAMES}</duration>{rate()}
          <start>0</start><end>{TOTAL_FRAMES}</end><in>0</in><out>{TOTAL_FRAMES}</out>
          {src_file}
          <link><linkclipref>v1</linkclipref><mediatype>video</mediatype><trackindex>1</trackindex><clipindex>1</clipindex></link>
          <link><linkclipref>a1</linkclipref><mediatype>audio</mediatype><trackindex>1</trackindex><clipindex>1</clipindex></link>
          <link><linkclipref>a2</linkclipref><mediatype>audio</mediatype><trackindex>2</trackindex><clipindex>1</clipindex></link>
        </clipitem>"""

    def aclip(cid, ch):
        return f"""
        <clipitem id="{cid}">
          <name>{vname}</name><enabled>TRUE</enabled>
          <duration>{TOTAL_FRAMES}</duration>{rate()}
          <start>0</start><end>{TOTAL_FRAMES}</end><in>0</in><out>{TOTAL_FRAMES}</out>
          <file id="src"/>
          <sourcetrack><mediatype>audio</mediatype><trackindex>{ch}</trackindex></sourcetrack>
          <link><linkclipref>v1</linkclipref><mediatype>video</mediatype><trackindex>1</trackindex><clipindex>1</clipindex></link>
          <link><linkclipref>a1</linkclipref><mediatype>audio</mediatype><trackindex>1</trackindex><clipindex>1</clipindex></link>
          <link><linkclipref>a2</linkclipref><mediatype>audio</mediatype><trackindex>2</trackindex><clipindex>1</clipindex></link>
        </clipitem>"""

    vtracks = f"<track>{v1}\n      </track>"
    for tr in (2, 3, 4):
        items = "".join(still(i, tr, *c) for i, c in enumerate(tracks[tr], 1))
        vtracks += f"\n      <track>{items}\n      </track>"

    # optional SFX on A3 (left) / A4 (right)
    sfx_tracks = ""
    if len(sys.argv) > 5 and sys.argv[5].endswith(".json"):
        import wave
        from sfx_mix import peak_offset
        plan = json.load(open(sys.argv[5], encoding="utf8"))
        per_ch = {1: "", 2: ""}
        for i, ev in enumerate(plan["events"], 1):
            p = os.path.join(plan["sfx_dir"], ev["name"] + ".wav")
            w = wave.open(p)
            n = max(1, int(round(w.getnframes() / w.getframerate() * FPS)))
            s = fr(max(0.0, ev["at"] - peak_offset(p)))
            lin = 10 ** (ev["gain_db"] / 20)
            for ch in (1, 2):
                fdef = (f"""<file id="sfx{i}"><name>{ev['name']}.wav</name><pathurl>{url(p)}</pathurl>{rate()}
            <duration>{n}</duration><media><audio><samplecharacteristics><depth>16</depth><samplerate>{w.getframerate()}</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media></file>"""
                        if ch == 1 else f'<file id="sfx{i}"/>')
                per_ch[ch] += f"""
        <clipitem id="sfx{i}_{ch}">
          <name>{ev['name']} ({ev.get('why', '')})</name><enabled>TRUE</enabled>
          <duration>{n}</duration>{rate()}
          <start>{s}</start><end>{s + n}</end><in>0</in><out>{n}</out>
          {fdef}
          <sourcetrack><mediatype>audio</mediatype><trackindex>{ch}</trackindex></sourcetrack>
          <filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory><effecttype>audiolevels</effecttype><mediatype>audio</mediatype>
            <parameter><parameterid>level</parameterid><name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax><value>{lin:.5f}</value></parameter></effect></filter>
        </clipitem>"""
        sfx_tracks = f"\n        <track>{per_ch[1]}\n        </track>\n        <track>{per_ch[2]}\n        </track>"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4">
  <sequence id="seq1">
    <name>{title} - negative captions</name>
    <duration>{TOTAL_FRAMES}</duration>{rate()}
    <timecode>{rate()}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>
    <media>
      <video>
        <format><samplecharacteristics>{rate()}<width>{nc.W}</width><height>{nc.H}</height>
          <pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>
      {vtracks}
      </video>
      <audio>
        <numOutputChannels>2</numOutputChannels>
        <format><samplecharacteristics><depth>16</depth><samplerate>44100</samplerate></samplecharacteristics></format>
        <track>{aclip('a1', 1)}
        </track>
        <track>{aclip('a2', 2)}
        </track>{sfx_tracks}
      </audio>
    </media>
  </sequence>
</xmeml>
"""
    xp = os.path.join(outdir, title.replace(" ", "_") + "_captions.xml")
    open(xp, "w", encoding="utf8").write(xml)
    print("wrote", xp)


if __name__ == "__main__":
    main()
