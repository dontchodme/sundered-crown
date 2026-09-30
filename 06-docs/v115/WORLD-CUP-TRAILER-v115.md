# THE WORLD CUP TRAILER (trailer 1) — v115

Cowork, 2026-09-29. A 30-second hype trailer for the tournament series planned in
`CROWN-CUP-PLAN-v115.md` (as of this commit that plan, its app brief and `cup.py` are in the
claude.ai Project, not in this repo). Built and delivered; everything below is what was made,
how, and what was measured.

**Trailer 2 is a different thing from a different session**: the fully drawn anime trailer,
`06-docs/v116/ANIME-TRAILER-v116.md`. Nothing here touches it and nothing there touches this.

## Rick's rulings (2026-09-29)

| question | ruling |
|---|---|
| the name on screen | **SUPER WEAPON BALL WORLD CUP** — no number (over "World Cup 2" and "The Crown Cup"). This answers the plan's open decision §9.1. |
| when it starts | **no timing** — the end card says *Follow so you don't miss a match.* |
| the announcer | **yes** — the shorts' hook voice, Kokoro `bm_lewis`. |

## The file

`07-shorts/worldcup-trailer/worldcup-trailer.mp4` — 1080×1920, 60 fps, 30.000 s,
H.264 + AAC 48 kHz stereo. mp4s are gitignored; the commands at the end rebuild it.

## What is in it (bars of the score, 128 BPM, a bar is 1.875 s)

```
bars 0-1    0.00- 3.75  the wall: all 49 cells of the grid (7 schools x 7 weapons) ignite a row
                        per sixteenth -- "49 FIGHTERS"; then the crown slams in -- "ONE CROWN"
bars 2-3    3.75- 7.50  four named cuts: Duskreave/Scour, Cindercleave/Breach,
                        Thornshear/The Winnowing, Bloodmirror/Bloodletting
bars 4-5    7.50-11.25  "16 GROUPS" (sixteen cards A-P) and "ONE KNOCKOUT" (an empty bracket
                        converging on the crown), each over dimmed footage, a cut between
bars 6-7   11.25-15.00  "WIN OR GO HOME": Vesper, Starwarden, Ravelbone, Paradox, named
bars 8-9   15.00-18.75  seven one-beat cuts, then half a beat of black (the score's gap)
bar  10    18.75-20.63  a real kill, slowed further: Gloamwire over Emberedge -- "WHO TAKES THE CROWN?"
bars 11-12 20.63-24.38  the drop: six one-beat cuts, four half-beat cuts
bars 13-15 24.38-30.00  title: crown, SUPER WEAPON BALL / WORLD CUP, then FOLLOW
```

Voice lines, in order: *Forty-nine fighters. / One crown. / Sixteen groups. / One knockout. /
Win, or go home. / Who takes the crown? / The Super Weapon Ball World Cup. / Follow, so you
don't miss a match.* Each lands on its caption (`trailer_edit.VO` and `BANDS`).

Captions use the shorts' stakes band — dark band, gold rules, cream serif caps — so the
trailer reads as the same channel.

## Choices made, and why

- **Footage only from `GAME` (`sc-nightglass-fx`, Rick-passed, 41 relics).** The design
  batch's line is awaiting his eye, and its redesigns change seven relics' ultimates
  (Dawnbringer, Widowmaker, Ironhail, Lightkeeper, Aureole, Censer, Axiom). Foes were
  picked from relics whose ultimate is the same on both lines — except the first three
  clips, filmed before that rule was in (Widowmaker, Axiom as foes); in the frames the edit
  uses, the foe's ultimate is not on screen (cast times checked).
- **The eight relics only on the batch line are dark tiles with a "?"** on the wall
  (Morningstar, Ironwood, Portcullis, Bindweed, Coldiron, Lodestone, Oracle, Angelus). The
  wall still counts 49, it shows nothing Rick has not passed, and "?" is a reason to follow.
- **No tournament result appears.** The fights are ordinary seeds, not cup fixtures; the
  group cards show only school colours, the bracket slots are empty. Nothing is spent
  before the draw is published.
- **Fights were picked by measurement** (`trailer_scan.py`): per relic, the cast with the
  most damage in the 3 s after it, cast at 4-40 s, foe alive at +3 s; filmed from
  cast − 0.3 s. In-points were then chosen off contact sheets.
- **The game's music bed is muted in every clip** (`trailer_clip.py`, in-page; no file in
  `02-chain/` touched): fourteen tape-slowed beds cut together would clash on every cut.
  Each cut keeps its own fight audio from the game's synth, under the score.
- **The score is synthesized from nothing** (`trailer_music.py`: D minor, 128 BPM, braams,
  drums, supersaw ostinato, risers). No samples, no licence to read.

## Measured

| | value | how |
|---|---|---|
| integrated loudness | **−14.3 LUFS** | ebur128 on the delivered file |
| true peak | **−2.0 dBTP** | same; limiter set 1 dB under the target because the AAC encode overshoots (−1.7 with none, −1.9 at 0.5 dB) |
| speech to bed | **+7.5 LU** | voice stem vs ducked bed, LUFS, over the windows the voice speaks (the shorts' own bar was +7.3) |
| picture | 1800 frames, 1080×1920, 60/1 | ffprobe |

The ported scripts in `tools/` were checked against the scratch build that made the
delivered file: identical frames at 1.2, 12.5 and 25.9 s, identical score and mix samples.

## Not checked, said plainly

- **Nobody has listened to it yet.** The score, mix and voice were judged on spectrograms,
  waveforms and loudness numbers, not by ear. The voice lines' phonemes were read back from
  Kokoro and all eight say what they should.
- **The runtime was not the pin.** Filmed in a Cowork container on Playwright 1.56 /
  Chromium 141, not 1.62 / 151. That is fine for pictures; no number here is a fight
  measurement, and the fights would not reproduce bit-for-bit on the pinned runtime.
- Zooms up to 1.55× are upscales of 1080-wide capture, so the tightest cuts are a little soft.
- The Cipher and Nightglass one-beat cuts show more of the foe's ultimate (Heartwood's
  Rootfast, Emberedge's Slagburst) than their own.

## Rebuild (Windows: `python`, from `tools/`, one line at a time)

```
python trailer_clips.py
```
```
python trailer_portraits.py
```
```
python trailer_vo.py
```
```
python trailer_music.py
```
```
python trailer_cut.py --out ../07-shorts/worldcup-trailer/video.mp4
```
```
python trailer_mix.py
```
```
python trailer_deliver.py
```

`trailer_clips.py` is the slow step (≈5 min a clip, 17 clips, serial on purpose). The
edit — every cut, in-point, zoom, caption and voice onset — is one table,
`trailer_edit.py`; change it and re-run the last three steps. `trailer_sheet.py` makes a
timestamped contact sheet of any clip, for choosing in-points.

## Open decisions

1. **The eight "?" tiles** — keep them dark until those relics ship, or light them once
   Rick has passed the batch (re-run `trailer_portraits.py` with `MYSTERY` emptied).
2. **Post it before the draw, or with it** — the trailer promises the format, not a date.
3. **The seed string** — the plan's seed rule hashes `"crown-cup-1/..."`; with the name
   now *World Cup*, keep that string (it is only a label, and changing it changes every
   fight) or rename it before the draw is published.
