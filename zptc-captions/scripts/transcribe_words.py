"""Word-level timestamps for a video's voiceover (for timing caption lines).

usage: py -3.12 transcribe_words.py input.mp4
Prints one line per phrase: [start]word [start]word ...
Telugu voiceovers come out as an English translation; match lines by meaning and pauses.
"""
import os, subprocess, sys, tempfile
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
from faster_whisper import WhisperModel

src = sys.argv[1]
wav = os.path.join(tempfile.mkdtemp(), "vo.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(wav, language="en", word_timestamps=True, vad_filter=True)
for s in segs:
    print(" ".join(f"[{w.start:.2f}]{w.word.strip()}" for w in s.words))
