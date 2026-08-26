# SHORTS — how to make them. Handoff, 2026-08-14.

Vertical fight videos for TikTok / YouTube Shorts: fight card, voiceover,
cinema set-pieces, 1080x1920, under a minute. Three were shipped this session
off `01-live/sundered-crown.html` (`ba423d8e…`).

Everything here was run against the shipped v21 artifact. The tools are already
in `tools/`; nothing new needs building.

---

## 0. THE LAW FOR THIS PIPELINE

**Watch the output before you hand it over.** Every failure this pipeline has
produced was invisible to the automated checks and obvious in a single frame:
relics halved by the bottom edge, a beige-washed kill, a voiceover naming a
relic the card does not call by that name. Pull four frames. Look at them.

And **never re-render only the audio to "fix" a mix.** The mix is baked at the
last ffmpeg stage from a wav that the capture stage deletes. If the voiceover
is wrong, re-capture. Patching around it silently ships the wrong file.

---

## 1. WHAT YOU NEED

```
tools/kokoro-v1.0.onnx     325MB   NOT in the repo — restore per session
tools/voices-v1.0.bin       28MB   NOT in the repo — restore per session
python3 -c "import kokoro_onnx, soundfile"     must import
ffmpeg                                          must be on PATH
playwright + chromium                           the capture stage drives it
```

Restore the two model files into `tools/` (they resolve beside
`cinema_vo.py`):

```bash
curl -sL -o tools/kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sL -o tools/voices-v1.0.bin \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

---

## 2. THE PIPELINE, THREE STAGES

It is split on purpose. A full 45s fight at 60fps is ~2,800 frames and takes
**3-4 minutes of wall time to capture**, then another 1-2 to encode. That is
over a single tool window. Each stage below fits comfortably; the whole thing
in one command does not.

### Stage 1 — pick the fight

```bash
cd tools
python3 cinema_pick.py            # scans pairings, prints cut lists
```

At the shipped bar (`CINE.floor = 1.90`) **41% of matches contain no set-piece
at all**. That is correct and deliberate — do not lower the bar to find a
fight, scan for one. A fight worth filming has at least one cut; two or three
with different `why` strings is better television.

To inspect one specific seed, ask `cinePlan` directly through `scpage`:

```python
from scpage import game
JS = "([a,b,s]) => window.cinePlan(a,b,s)"
with game(game_path=pathlib.Path("sundered-crown.html").resolve()) as (page, err):
    print(page.evaluate(JS, ["nightfell", "emberedge", 695213480]))
```

Read the `why` on each cut. `blows traded` is a volley, `closing at` is a
speed cut, `of flight` is a long bolt. **Aim for variety across the set** — a
reel of three volleys sells one third of what the director does.

### Stage 2 — the voiceover

```bash
python3 cinema_vo.py --a Nightfell --b Emberedge --out vo-nf-ee.wav
```

Voice is `am_onyx`, picked on a measured five-voice sweep (median f0 86 Hz
against 120-150 for the rest — a clean third below the field, and unhurried).
Do not swap it on taste; the sweep table is in the file's docstring.

Lines land at ~3.1s and sit inside the 4.0s fight card with air on both sides.

> **GOTCHA — id is not the display name.** `--a/--b` on `cinema_clip.py` take
> **ids**; `cinema_vo.py` takes **spoken names**. For the four greatswords they
> differ, and a voiceover naming a relic the card does not is a shipped defect:
>
> As of v21 there is **exactly one** mismatch in the sixteen, and it is the one
> that bit:
>
> ```
> id oathwound  -> name "Goreshard"     <-- the only one
> ```
>
> Every other id equals its name case-insensitively. Do not trust that to hold
> after the next roster change — re-run the check below when relics are added.
>
> Resolve before writing the line:
> ```bash
> python3 -c "
> import re; src=open('sundered-crown.html').read()
> print(dict(re.findall(r'id:\"([a-z]+)\",\s*name:\"([^\"]+)\"', src)))"
> ```

### Stage 3a — capture

```bash
python3 cinema_clip.py --game sundered-crown.html \
  --full --intro --capture-only \
  --a nightfell --b emberedge --seed 695213480 \
  --fps 60 --w 540 --q 0.80 --out s2.mp4
```

* `--game` **explicitly, always.** It defaults to `sc-cinema.html`, which is
  not the live build. Same class of trap as `pick.py`.
* `--full` films from t=0; `--intro` includes the 4.0s fight card.
* `--w 540` is the capture width; stage 3b upscales to 1080. Capturing at 1080
  is far slower for no visible gain at Shorts bitrates.
* Leaves `_clip_frames/on_%05d.jpg` and `_clip_frames/on.wav`.

Expect ~2,500-3,300 frames and 130-230s. If the tool window dies mid-capture,
**the frames survive** — check `ls _clip_frames | wc -l` and, if the wav is
there too, skip straight to 3b.

### Stage 3b — encode to 1080x1920

```bash
ffmpeg -y -hide_banner -loglevel error \
  -framerate 60 -i _clip_frames/on_%05d.jpg -i _clip_frames/on.wav \
  -vf "scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ac 2 -shortest _raw.mp4
```

### Stage 3c — mix the voiceover and normalise

```bash
ffmpeg -y -hide_banner -loglevel error -i _raw.mp4 -i vo-nf-ee.wav \
  -filter_complex "[1:a]aresample=48000,adelay=300|300,volume=1.5,apad[v1];\
[0:a][v1]amix=inputs=2:duration=first:normalize=0[m];\
[m]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart short-2-nightfell-v-emberedge.mp4

rm -f _raw.mp4 && rm -rf _clip_frames
```

Why each part:

* `adelay=300|300` — 300ms in, so the line starts after the card appears.
* `volume=1.5` — the VO sits over a full music bed; unlifted it is mush.
* `normalize=0` on `amix` — without it ffmpeg halves both inputs and the whole
  video comes out quiet.
* `apad` — the VO is 3s against a 45s video; without padding `amix` can end the
  stream early.
* `loudnorm I=-14` — the TikTok/YouTube norm. Lands ~-14.7 to -15.4 LUFS in
  one pass. **This is the answer to the old "renders are 6 dB under platform
  norm" note** — that only applied to the bare `render.py` path.
* `+faststart` — moov atom first, so the platforms can stream it.

---

## 3. VERIFY BEFORE HANDING OVER

```bash
ffprobe -v error -show_entries format=duration \
        -show_entries stream=width,height,codec_name -of csv=p=0 FILE
ffmpeg -hide_banner -i FILE -af loudnorm=I=-14:TP=-1.5:print_format=summary \
       -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
```

Pass marks: `1080,1920`, `h264` + `aac`, **duration under 60s**, integrated
between -16 and -13 LUFS, true peak at or under -0.3 dBTP.

Then look at four frames — the card, a cut, the finish, and one moment where
the action is near the bottom wall:

```bash
for t in 1.8 34.0 36.5 40.0; do
  ffmpeg -y -loglevel error -ss $t -i FILE -frames:v 1 /tmp/f_$t.jpg
done
```

Checking: both relic names on the card match the voiceover; no relic clipped by
the frame edge; the impact is not a white/beige wash.

---

## 4. LENGTH

Shorts must be **under 60 seconds**. Screen time is longer than match time —
the director spends roughly +1s per set-piece, and the 4.0s card is on top:

```
match 46.8s + card + cuts -> 54.8s     (comfortable)
match 38.1s + card + cuts -> 48.6s
match 31.5s + card + cuts -> 40.9s     (ideal)
```

A match over ~50s of sim risks breaching 60s. `cinema_pick.py` filters to
24-50s; prefer the short end. If a fight is worth it but too long, drop
`--intro` (saves 4s) or film a window instead of `--full`:

```bash
python3 cinema_clip.py --game sundered-crown.html --lead 12 ...
```

which starts 12s of match time before the finish.

---

## 5. WHAT SHIPPED THIS SESSION, FOR COMPARISON

```
short-1-farwarden-v-nightfell     seed 2072567088   54.8s   1 cut  (4-blow volley)
short-2-nightfell-v-emberedge     seed  695213480   48.6s   1 cut  (8-blow volley
                                                             that IS the kill, 2.91)
short-3-widowmaker-v-goreshard    seed 2723075806   40.9s   3 cuts (pace + volley
                                                             + brink finish, 3.24)
```

All three: `--full --intro`, `--fps 60 --w 540 --q 0.80`, crf 23, `am_onyx`.

---

## 6. KNOWN RESIDUALS

* **Status tags at the side walls** (`Bramblesnare` and friends) can clip the
  frame edge. That is the tag renderer, not the camera, and it predates the
  director. Unfixed.
* **The ranged whoosh does not pitch-bend with the tape-slow** — it is
  scheduled at real rate while the score drops. Audible only if listened for.
* **`render.py` still schedules audio against MATCH time**, so it cannot
  express cinematic dilation. `cinema_clip.py` is the wall-time path and is the
  one to use for anything with the director on. Porting that into `render.py`
  remains the one real integration cost.
* **Single-pass `loudnorm` lands ~1 dB shy of target.** Two-pass would nail it
  if a platform ever complains; it has not been needed.

---

## 7. OPEN DECISIONS

1. **No end card.** The videos stop on the verdict, ~2.2s after the finish.
   A 1-2s outro with the relic names or a handle is the obvious next addition
   and nobody has decided what it should say.
2. **The voiceover only ever names the fighters.** A second line over the
   finish ("Nightfell takes the crown") is one more `cinema_vo.py` call and a
   second `adelay`, but it needs the winner, which means reading the plan
   before rendering rather than after.
3. **Capture width is 540 upscaled to 1080.** Fine at Shorts bitrates, but
   nobody has A/B'd it against a true 1080 capture on a phone screen — and the
   project's standing rule is that phone-size judgements happen on a phone.
4. **Fights are picked by cut score, not by shape.** A fight whose only cut
   lands at 8s is worse television than one that builds, and nothing currently
   scores that.

---

## 8. ADDENDUM, v22 (2026-08-15) — the Crucible broke stage 3c

The Grudgebearer short (`short-4-grudgebearer-v-thornwake`, seed 1476297217)
measured **+0.5 dBTP** out of the §2 stage-3c mix — the Crucible's implosion
SFX stacked on the kill hit spikes past what single-pass loudnorm holds.
§6's "~1 dB shy" note undersold it for this content.

The fix that shipped, replacing the loudnorm tail of the filter graph:

```
[m]loudnorm=I=-14:TP=-2.0:LRA=11,aresample=48000,\
alimiter=attack=5:release=60:limit=0.79:level=false[a]
```

**`level=false` is mandatory.** alimiter defaults to auto-leveling the
limited signal back to full scale, which made TP *worse* (+0.6). With
level=false: −15.6 LUFS / −1.1 dBTP, inside the §3 pass band.
