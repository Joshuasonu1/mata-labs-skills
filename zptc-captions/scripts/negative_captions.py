"""Burn 'negative text' captions onto a video, centred inside the footage frame.

Caption letters show an inverted (negative) version of the footage under them, lifted
toward white so they stay readable, with a soft dark halo. Text never leaves the
footage frame (it does not touch the black canvas).

usage: py -3.12 negative_captions.py input.mp4 captions.json output.mp4
           [--style zptc] [--top-band-until SECONDS] [--preview SECONDS]
captions.json: [[start, end, "text"], ...]  or  [start, end, "text", "<style name>"] per entry
Style presets live in caption_styles/<name>.json (default: zptc).
--top-band-until S: captions that start before S use the "zptc_top_band" preset (black space
above a title collage), everything else uses --style. One render pass for the whole reel.
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 30000 / 1001
PAD = 40
STYLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "caption_styles")


def apply_style(name="zptc"):
    """Load caption_styles/<name>.json into the module settings."""
    global STYLE, FX0, FX1, FY0, FY1, MARGIN, MAXW, CX, CY, BAND, GREY, MIN_LUM, LIFT, HALO
    global BIG_SIZE, BIG_MIN, LABEL_SIZE, MAX_WORDS, FONT, BIG_VAR, LABEL_VAR, LABEL_SHARE
    global FADE_IN, FADE_OUT, SLIDE, UPPER, ADAPTIVE
    s = json.load(open(os.path.join(STYLE_DIR, name + ".json"), encoding="utf8"))
    STYLE = s
    f = s["default_frame"]
    FX0, FX1, FY0, FY1 = f["x0"], f["x1"], f["y0"], f["y1"]
    MARGIN = s["frame_margin"]
    MAXW = (FX1 - FX0) - 2 * MARGIN
    BAND = s["band_position"]
    CX = (FX0 + FX1) // 2
    CY = FY0 + int(BAND * (FY1 - FY0))
    GREY, MIN_LUM = s["negative_grey"], s["negative_min_brightness"]
    LIFT, HALO = s["negative_lift_to_white"], s["halo_darkness"]
    BIG_SIZE, BIG_MIN, LABEL_SIZE = s["big_size"], s["big_min_size"], s["label_size"]
    MAX_WORDS, LABEL_SHARE = s["max_words_per_card"], s["label_share_of_text"]
    FONT, BIG_VAR, LABEL_VAR = s["font_file"], s["big_font_variation"], s["label_font_variation"]
    FADE_IN, FADE_OUT, SLIDE = s["fade_in_s"], s["fade_out_s"], s["slide_up_px"]
    UPPER, ADAPTIVE = s["uppercase"], s["adaptive_frame"]


apply_style(sys.argv[sys.argv.index("--style") + 1] if "--style" in sys.argv else "zptc")


def chunks(t0, t1, text):
    words = text.split()
    if len(words) <= MAX_WORDS:
        return [(t0, t1, text)]
    parts = [p.strip() for p in re.split(r"(?<=\.\.\.)|(?<=,)", text) if p.strip()]
    out = []
    for p in parts:
        w = p.split()
        n = -(-len(w) // MAX_WORDS)
        size = -(-len(w) // n)
        out += [" ".join(w[i:i + size]) for i in range(0, len(w), size)]
    total = sum(len(p) for p in out)
    res, t = [], t0
    for p in out:
        d = (t1 - t0) * len(p) / total
        res.append((t, t + d, p))
        t += d
    return res


def clean(text):
    text = text.strip()
    text = re.sub(r"[.,]+$", "", text)          # drop trailing . , ...
    return text


def wrap(words, f):
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= MAXW or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def font(size, condensed):
    f = ImageFont.truetype(FONT, size)
    names = [n.decode() if isinstance(n, bytes) else n for n in f.get_variation_names()]
    want = BIG_VAR if condensed else LABEL_VAR   # names from the style preset
    if want in names:
        f.set_variation_by_name(want)
    return f


_ROWS = {}   # src -> per-frame list of (top, bottom) or None, from one low-res pass


def _analyse(src):
    """Footage extent per frame: first to last run of non-black rows taller than 150 px
    (ignores thin overlay strips; a split screen counts as one tall frame).
    Decodes once at 1/4 size (W/4 x H/4 gray)."""
    if src in _ROWS:
        return _ROWS[src]
    w, h = W // 4, H // 4
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    out = []
    while True:
        buf = p.stdout.read(w * h)
        if len(buf) < w * h:
            break
        a = np.frombuffer(buf, np.uint8).reshape(h, w)
        on = list(a[:, 75:195].max(1) > 8) + [False]   # canvas is pure black; dark shots still count
        runs, start = [], None
        for y, v in enumerate(on):
            if v and start is None:
                start = y
            elif not v and start is not None:
                if y - start > 150 // 4:
                    runs.append((start * 4, y * 4 - 1))
                start = None
        out.append((runs[0][0], runs[-1][1]) if runs else None)
    p.wait()
    _ROWS[src] = out
    return out


def _box_at(src, t):
    rows = _analyse(src)
    i = min(len(rows) - 1, max(0, int(t * FPS)))
    return rows[i]


def frame_box(src, t0, t1=None):
    """Typical footage frame during the caption: median over every frame, so brief zoom-ins,
    fades and dark shots don't move the caption. Near-standard frames snap to the standard."""
    t1 = t0 if t1 is None else t1
    n = max(1, int((t1 - t0) * FPS))
    boxes = [b for b in (_box_at(src, t0 + k / FPS) for k in range(n)) if b]
    if not boxes:
        return FY0, FY1
    top = int(np.median([b[0] for b in boxes]))
    bottom = int(np.median([b[1] for b in boxes]))
    if abs(top - FY0) < 40 and abs(bottom - FY1) < 40 or bottom - top < 300:
        return FY0, FY1
    return top, bottom


def place_cy(top, bottom, block_h):
    """82% down the footage, but keep the block inside with a margin."""
    cy = top + int(BAND * (bottom - top))
    return min(cy, bottom - 45 - block_h // 2 + PAD)


def render(text, box=None):
    """Small white label above, big condensed negative line below; block centred in the footage.
    returns (neg_mask, label_mask, halo, top, left)"""
    words = (clean(text).upper() if UPPER else clean(text)).split()
    label, big = [], list(words)
    if len(words) >= 3:   # opening words (about a third of the text) go in the label
        total, acc = sum(len(w) for w in words), 0
        while len(big) > 1 and acc + len(big[0]) <= total * LABEL_SHARE:
            acc += len(big[0]); label.append(big.pop(0))
    size = BIG_SIZE
    while True:
        f = font(size, True)
        if f.getlength(" ".join(big)) <= MAXW:
            break
        if size > BIG_MIN:
            size -= 4
        elif len(big) > 1:                       # still too wide: move a word up to the label
            label.append(big.pop(0)); size = BIG_SIZE
        else:
            break
    big_s, label_s = " ".join(big), " ".join(label).rstrip(",")
    lsize = LABEL_SIZE
    lf = font(lsize, False)
    while label_s and lf.getlength(label_s) > MAXW and lsize > 30:   # keep label inside the frame
        lsize -= 2
        lf = font(lsize, False)
    bwid = int(f.getlength(big_s))
    lwid = int(lf.getlength(label_s)) if label_s else 0
    block_w = max(bwid, lwid)
    lab_h = int(LABEL_SIZE * 1.15) if label_s else 0
    big_h = int(size * 0.80)                     # cap height of the condensed caps
    bw = block_w + 2 * PAD
    bh = lab_h + big_h + 2 * PAD
    neg = Image.new("L", (bw, bh), 0)
    lab = Image.new("L", (bw, bh), 0)
    if label_s:
        ImageDraw.Draw(lab).text((PAD, PAD + lab_h - 8), label_s, font=lf, fill=255, anchor="ls")
    ImageDraw.Draw(neg).text((PAD, PAD + lab_h + big_h), big_s, font=f, fill=255, anchor="ls")
    both = Image.fromarray(np.maximum(np.asarray(neg), np.asarray(lab)))
    halo = both.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(16))
    halo = halo.point(lambda v: min(255, v * 2))
    cy = place_cy(*box, bh) if box else CY
    left, top = CX - bw // 2, cy - bh // 2
    as_f = lambda im: np.asarray(im, np.float32) / 255.0
    return as_f(neg), as_f(lab), as_f(halo), top, left


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def probe_rate(src):
    """Return the source video's frame rate as (string for ffmpeg, float)."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
    num, _, den = r.partition("/")
    return r, float(num) / float(den or 1)


def _arg(name, cast=str, default=None):
    return cast(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def main():
    global FPS
    src, capf, out = sys.argv[1:4]
    rate_str, FPS = probe_rate(src)
    preview = _arg("--preview", float)
    base = _arg("--style", str, "zptc")
    top_until = _arg("--top-band-until", float)
    rendered = []
    for entry in json.load(open(capf, encoding="utf8")):
        t0, t1, txt = entry[:3]
        style = entry[3] if len(entry) > 3 and entry[3] else (
            "zptc_top_band" if top_until is not None and t0 < top_until else base)
        apply_style(style)                     # per-caption placement / look, same single pass
        fx = (FADE_IN, FADE_OUT, SLIDE, HALO, GREY, MIN_LUM, LIFT)
        for c0, c1, ct in chunks(t0, t1, txt):
            rendered.append((c0, c1, *render(ct, frame_box(src, c0, c1) if ADAPTIVE else None), fx))
    apply_style(base)
    rendered.sort(key=lambda r: r[0])
    print(f"{len(rendered)} caption cards", flush=True)

    dec_args = ["ffmpeg", "-v", "error", "-i", src]
    if preview:
        dec_args += ["-t", str(preview)]
    dec = subprocess.Popen(dec_args + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", rate_str, "-i", "-", "-i", src,
                            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "copy",
                            "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    total = int(round((preview or float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
        capture_output=True, text=True).stdout.strip() or 0)) * FPS))
    n, fsz = 0, W * H * 3
    lum_w = np.array([0.3, 0.59, 0.11], np.float32)
    while True:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz:
            break
        t = n / FPS
        active = [r for r in rendered if r[0] <= t < r[1]]
        if active:   # only frames with a caption are touched, and only the caption's box
            fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
            for t0, t1, mask, lab, halo, top, left, (f_in, f_out, slide, halo_k, grey, min_lum, lift) in active:
                a_in = ease((t - t0) / f_in)
                a = a_in * min(1.0, (t1 - t) / f_out)
                y = top + int(round((1 - a_in) * slide))
                h, w = mask.shape
                orig = fr[y:y + h, left:left + w].astype(np.float32)
                hm = (halo * halo_k * a)[:, :, None]
                reg = orig * (1 - hm)
                # negative: invert the ORIGINAL footage (as in the reference), lightly lifted
                neg = np.abs(orig - grey)
                lum = neg @ lum_w
                boost = np.maximum(0, min_lum - lum)[:, :, None]   # keep the hue, never go dark
                letter = (neg + boost) * (1 - lift) + 255 * lift
                m = (mask * a)[:, :, None]
                reg = reg * (1 - m) + letter * m
                lm = (lab * a)[:, :, None]
                fr[y:y + h, left:left + w] = (reg * (1 - lm) + 255 * lm).clip(0, 255).astype(np.uint8)
            buf = fr.tobytes()
        enc.stdin.write(buf)
        n += 1
        if n % 240 == 0:
            pct = f" ({100 * n // total}%)" if total else ""
            print(f"{n} frames{pct}", flush=True)
    enc.stdin.close()
    enc.wait()
    print("done", n, "frames")


if __name__ == "__main__":
    main()
