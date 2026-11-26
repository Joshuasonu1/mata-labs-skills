# House rules and project notes (from Claude Code memory, 2026-11-26)

## Rule: speech cuts must finish sentences (applies to every reel with speech)
Every speech piece must start after the previous sentence ends and end only where the speaker finishes the sentence and pauses. Never clip a word or stop mid-thought to hit a target length. Whisper word timestamps can be 0.3-0.6 s off: measure RMS energy (20-50 ms windows) at every voice in/out; the out point must sit in a real pause with no speech resuming within ~0.3 s, otherwise extend to the next pause even if the reel gets longer. Move picture and subtitles with each change, re-check, and report the check.

## Project note: who is who in the 2026-11-25 DSk Swaeroes footage
- RS Praveen Kumar = the man in the white shirt, glasses, bald, wristwatch, hands clasped, standing centre in felicitation clip c16 (user-identified; pick-sheet shots 7-12).
- The police-uniform portrait on the event banner is NOT confirmed as him: do not use it as his image.
- DSk (Dr Sravan Dasoju) is the podium speaker in clips c01 and c02 (user-confirmed).
- Claude cannot identify people by face; only use identifications the user gives.
