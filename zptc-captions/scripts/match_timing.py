"""Retime an existing captions file to a new cut of the same reel by matching the audio.

Use this before any speech-to-text whenever the new video re-uses the voiceover of a cut that
already has a captions file (same speaker, lines nudged, pauses trimmed, an intro added).
It takes seconds; Whisper on a music-heavy Telugu mix takes minutes and can fail.

usage: py -3.12 match_timing.py OLD.mp4 OLD_captions.json NEW.mp4 OUT_captions.json [--search 4]

For every caption it finds the shift (within +-search seconds) where the loudness pattern of
that line in OLD best matches NEW. Low-confidence shifts (corr < 0.6), and shifts that would
put a line before the previous one, take their neighbours' shift instead. Lines are kept in
order and never overlap. Text and any per-entry style are copied unchanged.
Prints one row per caption: old time, new time, shift, confidence, and a flag to check.
"""
import json, subprocess, sys
import numpy as np

RATE = 16000
HOP = 160            # 10 ms analysis frames


def envelope(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(RATE),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    e = np.sqrt(np.convolve(x * x, np.ones(400) / 400, "valid")[::HOP])
    return e


def best_shift(A, B, a, b, search):
    i0, i1 = int(max(0, a - 0.3) * 100), int((b + 0.3) * 100)
    seg = A[i0:i1]
    if len(seg) < 10:
        return 0.0, 0.0
    seg = (seg - seg.mean()) / (seg.std() + 1e-6)
    best = (-9.0, 0)
    for lag in range(-search * 100, search * 100 + 1, 2):
        j0 = i0 + lag
        if j0 < 0 or j0 + len(seg) > len(B):
            continue
        s2 = B[j0:j0 + len(seg)]
        c = float((seg * ((s2 - s2.mean()) / (s2.std() + 1e-6))).mean())
        if c > best[0]:
            best = (c, lag)
    return best[1] / 100.0, best[0]


def main():
    old_v, old_c, new_v, out_c = sys.argv[1:5]
    search = int(sys.argv[sys.argv.index("--search") + 1]) if "--search" in sys.argv else 4
    A, B = envelope(old_v), envelope(new_v)
    caps = json.load(open(old_c, encoding="utf8"))
    shifts = [best_shift(A, B, c[0], c[1], search) for c in caps]
    good = [abs(s) < 1e-9 or q >= 0.6 for s, q in shifts]
    # low-confidence lines: use the nearest confident neighbour's shift (prefer the earlier one)
    fixed = []
    for i, (s, q) in enumerate(shifts):
        if good[i]:
            fixed.append(s); continue
        prev = next((shifts[j][0] for j in range(i - 1, -1, -1) if good[j]), None)
        nxt = next((shifts[j][0] for j in range(i + 1, len(shifts)) if good[j]), None)
        fixed.append(prev if prev is not None else (nxt if nxt is not None else 0.0))
    rows = [[c[0] + f, c[1] + f, ok, ""] for c, f, ok in zip(caps, fixed, good)]
    # resolve overlaps: a confident line keeps its time; a low-confidence one gives way
    for i in range(1, len(rows)):
        p, r = rows[i - 1], rows[i]
        if r[0] >= p[1] - 1e-6:
            continue
        if r[2] and not p[2]:                 # shorten / pull back the uncertain previous line
            dur = max(0.4, min(p[1] - p[0], r[0] - 0.02 - p[0]))
            p[1] = r[0] - 0.02
            p[0] = min(p[0], p[1] - dur)
            p[3] = p[3] or "  <- shortened before a confident line"
        else:                                 # start this line after the previous one; keep its end
            r[0] = p[1] + 0.02
            r[1] = max(r[1], r[0] + 0.4)
            if p[1] - (r[0] - 0.02) > 0.15 or r[1] - r[0] < 0.5:
                r[3] = "  <- nudged after previous line"
    out = []
    print(f"{'old':>13}  {'new':>13}  shift   conf  text")
    for c, (s, q), f, r in zip(caps, shifts, fixed, rows):
        a, b = round(r[0], 2), round(r[1], 2)
        flag = r[3] or ("" if r[2] else "  <- low confidence, check")
        out.append([a, b, *c[2:]])
        print(f"{c[0]:6.2f}-{c[1]:6.2f}  {a:6.2f}-{b:6.2f}  {f:+.2f}  {q:4.2f}  {c[2]}{flag}")
    json.dump(out, open(out_c, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(f"wrote {out_c}: {len(out)} captions")


if __name__ == "__main__":
    main()
