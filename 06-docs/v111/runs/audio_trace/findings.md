# Spellbreaker's "-40 dB broadband" clip-audio difference: a render artefact

Traced 2026-09-30 by a Claude Code subagent. The orchestrator wrote this file from its report, because the
subagent could not write report files. Evidence: `readings.txt` and `renders.txt`, made by `readings.sh` /
`commands.sh` with the scripts here.

## Verdict

It is an artefact of rendering, not a change the build made to the game's sound. The whole gap is
`Math.random`:

- `Sfx._noiseBuffer()` fills its 0.6 s noise buffer with `Math.random()*2-1`, and every `_burst` plays
  from it.
- `renderAudio` in `tools/cinema_clip.py` builds a fresh buffer on every call. It does this for the synth's
  noise and again for the bed's.
- So each render gives every wall tick, hit and clank different noise, and two renders of one clip differ.

## Evidence (on the render's 16-bit PCM, before AAC)

**Null test.** One link (b7.5), rendered twice with `Math.random` as is:
- -37.7 dBFS over the whole track;
- before the cast, -43.3 / -34.2 dBFS in the first and second half-seconds;
- the stage-6 integrator's fx-vs-b7.5 pair read -43.6 / -36.4 there.

**The no-voice windows match the null.** At six windows away from any new voice:
- the integrator's difference reads -43.6 / -36.4 / -34.0 / -38.2 / -39.2 / -35.0 dBFS;
- the null test through AAC reads -44.0 / -36.3 / -34.5 / -38.8 / -39.0 / -35.3.

**Pinned** (`Math.random` replaced with mulberry32(1) for the render only):
- b7.5 against itself: about -124 dBFS rms, 1 LSB at most, within one page and across two page loads;
- fx against b7.5: -131 / -125 dBFS before the cast;
- the first difference over 1 LSB is at 79.1727, 6 ms after the cast (79.1667).

**Which source.** Freeing one noise source at a time on b7.5:

| Source | Level | Share |
|---|---|---|
| The synth's noise buffer | -35.5 dBFS | all of the effect |
| The bed's noise buffer | -64.7 | downbeat skins only |
| The hall's impulse response | -124 | none: the director's wet send is 0 |

**The band.** 62% of the difference's power is above 8 kHz and 27% at 3-8 kHz, where the burst voices
sit. That is why the C4-band controls stayed tight and the sizzle band scattered.

## No shared voice changed

- **Events.** The two event lists are identical apart from 26 added `spellbreaker-stun` and one
  `spellbreaker-close`. The same clanks, hits, wall ticks and cast appear on both, with the same options.
- **Shared voices.** Given the same 107 shared events, the two synths never differ by more than 1 LSB.
- **Code.** The `Sfx` diff from b7.5 to fx is 59 lines added and 0 removed: three new arms before the
  rune-crack fallback. `_burst`, `_tone`, `_noiseBuffer`, `buildChain`, the hex snap and `CineAudio` are
  byte-identical.
- **What does differ.** With the same events on both sides, the only differences are the designed stage-6
  voices:
  - the redesigned cast voice;
  - the stun's 1.0 s ring;
  - the close's tail and the bus compressor's recovery after it.

## What it changes in the v111 doc

The finding stands: 25 of 26 stun tails are heard, with the designed differences (hum +4.7 dB, close
+23.4, stun tails median +17.6). What changes is the yardstick. The 5.0 dB "no-voice spread" those tails
were counted against was noise-draw plus AAC scatter; on pinned PCM it is about 0.2 dB, so the tails
stand out further than the doc says.

## Optional fix (not applied)

- Pin `Math.random` with a fixed-seed generator inside `cinema_clip.py`'s `renderAudio`, around the hall
  and the two noise buffers, then restore it. `render_trace.py` shows how. Clips would then render
  identical audio every time.
- Seeding `Sfx._noiseBuffer` / `CineAudio.hall` in the game itself would make live noise identical on
  every load. That is a game change: it goes through the builders.
- A 1-LSB floor (about -124 dBFS) remains even when pinned. It is most likely the order Chromium sums
  the audio graph, and it was not traced.
