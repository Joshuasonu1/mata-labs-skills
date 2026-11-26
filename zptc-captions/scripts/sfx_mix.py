"""Mix SFX into a video's audio and remux.

usage: py -3.12 sfx_mix.py source_video.mp4 sfx.json video_with_captions.mp4 out.mp4
Audio = source audio + SFX (each placed so its peak lands on 'at'), normalised to target LUFS.
Video stream of video_with_captions.mp4 is copied untouched.
"""
import json, os, subprocess, sys, wave
import numpy as np


def peak_offset(path):
    w = wave.open(path)
    sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    a = np.frombuffer(w.readframes(w.getnframes()), {2: np.int16, 4: np.int32}[sw]).reshape(-1, ch)
    e = np.convolve(np.abs(a.astype(float)).mean(1), np.ones(max(1, sr // 50)), "same")
    return e.argmax() / sr


def main():
    src, plan_f, vid, out = sys.argv[1:5]
    plan = json.load(open(plan_f, encoding="utf8"))
    d = plan["sfx_dir"]
    args = ["ffmpeg", "-v", "error", "-y", "-i", src]
    filt, labels = [], []
    for i, ev in enumerate(plan["events"], 1):
        p = os.path.join(d, ev["name"] + ".wav")
        start = max(0.0, ev["at"] - peak_offset(p))
        args += ["-i", p]
        ms = int(round(start * 1000))
        filt.append(f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo,"
                    f"volume={ev['gain_db']}dB,adelay={ms}|{ms}[s{i}]")
        labels.append(f"[s{i}]")
    n = len(labels) + 1
    filt.append(f"[0:a]aformat=channel_layouts=stereo{''.join(['[a0]'])}")
    filt.append(f"[a0]{''.join(labels)}amix=inputs={n}:normalize=0:duration=first[mix]")
    filt.append(f"[mix]loudnorm=I={plan.get('target_lufs', -14)}:TP=-1.5:LRA=11[aout]")
    args += ["-i", vid, "-filter_complex", ";".join(filt), "-map", f"{n}:v", "-map", "[aout]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "44100", "-movflags", "+faststart",
             "-shortest", out]
    subprocess.run(args, check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
