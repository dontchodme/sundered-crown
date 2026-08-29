# THE TWO MISSING FEATURES — brief for Claude Code

Phase 1 is done and its gate passes. The renderer arc shipped bloom. What is
left of Rick's original four is **the announcer text box** and **the Create
Short button** — `swb:speak` and `swb:createShort` still return
`{ ok: false }` in `app/main.js`.

Read `CLAUDE.md`, then `docs/BUILD-CHAIN.md`, then this.

---

## 0. THE DEBTS, FIRST, BECAUSE THEY ARE SMALL AND THEY ROT

1. **`post_build.py`'s defaults do not rebuild the tip.** `--src` still points
   at `sc-paradox-readouts.html` and `--out` at `sc-paradox-post.html`, from
   before `ultcarry_build.py` existed. A bare run silently skips the ult art
   fixes. Two strings, then `chain_audit.py` and `engine_ab.py`.
   `docs/BUILD-CHAIN.md` §3.
2. **`tools/README.md` is stale.** It says "62 files" over ~200, its BUILD
   section is missing `cineexport_build.py`, `readouts_build.py` and
   `post_build.py` — three of the four newest chain links — and it files four
   probes under "the shipping chain, in order".
3. **The contact sheets render a tofu box** where an em-dash belongs
   (`harrow-before-after.png`, `daybreak-ball-ab.png`). The sheet font lacks
   the glyph. Cosmetic, but this project reviews by photograph.

---

## 1. THE ANNOUNCER IS NOT A WIRING JOB. ITS HOME WAS DEMOLISHED.

**Check this before writing any code, because it changes the whole shape.**

`cinema_vo.py` speaks arbitrary text today — `--text` already does exactly what
Rick asked for. The problem is *where the line goes*.

The voiceover was designed to sit inside the **4.0 s intro card**:

- `cinema_vo.py`'s line is written to fit "inside the 4.0s intro card with air
  on both sides"
- `shorts_build.py`'s mix graph opens with `adelay 300`, commented **"the line
  starts after the card is up, not under the cut to it"**

**And the card is dead.** Rule 1. `cinema_clip --intro` and `--cold-open`
refuse to run without `--legacy-card`. The reason is measured, and it is brutal:

> `08-analytics`: **card-first videos lose 71–75% of the audience present when
> it appears.**

So the announcer's home was removed for killing retention, and every timing
decision in the VO path still assumes it. Wiring the text box to
`cinema_vo.py` as it stands would put Rick's typed line over a card that does
not ship.

### What actually has to be decided

**ANSWERED 2026-08-28. THE ANNOUNCER GOES AT THE START OF THE FIGHT.** Rick,
off three rendered files rather than a description: *"the announcer has to be at
the start of the fight. it doesnt make sense anywhere else."* `--vo-at` now
defaults to 0.0 in `shorts_build.py`.

The spread was paradox v heartwood seed 55957, `--lead 18`, one line and one
voice with only the placement moving:

```
1  audio-first     23.0s   line at 0.00-2.99s     CHOSEN
2  cold open       23.0s   line at 0.30-3.29s     the inherited 300ms
3  verdict panel   24.2s   line at 19.90-22.89s   rejected
```

The 300ms of arm 2 was never a decision -- it was chosen so the line began
after the 4.0s intro card was up, and with the card retired it waited for
nothing. Arm 3 needed `--verdict-hold 3.6` to exist at all, because the line is
2.99s against a 2.40s hold; that flag stays, and so does the audio-tail fix it
forced (below), but the placement is dead.

Kept for the record, because the rejected options are the reason the answer is
trustworthy. Where the line lives now. Real candidates:

| placement | the argument |
|---|---|
| **over the cold open** | the fight is already moving; audio carries the setup while the picture does the hooking. No frozen frames, no cliff. |
| **audio-first hook** | line starts at 0.0 s over the first frames of live fight, no lead-in at all. Shortest time-to-action of the three. |
| **over the verdict panel** | every capture already holds 2.40 s of verdict tail — a home that exists, is already timed, and is at the end where a drop costs nothing. |

**This is Rick's call under Rule 2, and it gets a SPREAD, not a
recommendation.** Render one fight three ways with the same line, hand him the
three files, ask. v43 landed its sound in one round trip that way; v42 took
four. Do not put this to him in prose — he is choosing a *register*, and a
description cannot carry one.

**Price it from the data first.** `08-analytics/` has per-second retention
curves and the code that fetched them. The 71–75% number came from there. Look
at what the curves say about the first three seconds before offering the
spread — the same folder that killed the card can rank these.

### Then the mechanism, which is the easy half

- textarea → `cinema_vo.py --text`, a **preview** button that plays it without
  a four-minute render, and a voice picker. Voice of record is `bm_lewis`.
- **Keep the `SPOKEN` compound-splitting table.** Kokoro runs "Ironhail" into
  one mushy cluster; ten relic names are corrected there and the eleventh will
  need it.
- **Keep `--parts` / `--gaps`.** Punctuation does not control timing in
  Kokoro — `"?..."`, `"? ..."` and `"."` give the same contour. A pause has to
  be real, measured silence.
- **Length is now unbounded and something must give.** With the card gone the
  4.0 s ceiling is gone with it, but whatever placement wins has its own
  budget. Measure the rendered line and either fit the placement to it or show
  the duration live in the box and refuse past the cap. `verify.py` already
  caps ult tips at 72 characters, so the project has form for the second.
- **Kokoro runs local and offline.** Nothing about Rick's text leaves his PC.
  Say so in the UI; it is a feature.

---

## 2. CREATE SHORT — the pipeline exists, the button does not

`shorts_build.py` does capture → 1080×1920 → VO mix → delivery measurement,
with a mix graph where **every term is load-bearing** and one flag
(`alimiter ... level=false`) that is invisible in the output and merely makes
the file clip if forgotten. **Move that graph with its comments. Do not
reimplement it from memory.**

### The post chain already reaches the capture — verified

`post_build.py` hooks `POSTFX.frame()` inside the method that the live rAF
loop, `AC.__draw` and `CINE.drawLerped` all go through. So a captured frame
gets the same bloom the app shows. **That is the Electron guarantee actually
holding**, and it means Phase 3 does not have to solve it. Do not move that
hook to the rAF loop for convenience; that is precisely how the app and the
video start to diverge.

### What the button needs

- **A job queue, and progress that is true.** A full 60 fps capture is ~2,800
  frames and **3–4 minutes**, then 1–2 to encode. A spinner is a lie. Surface
  the log, give it a cancel.
- **Never re-render only the audio to "fix" a mix** — enforced by construction:
  the mix is only ever built from the capture stage's `on.wav`.
- **Pull four frames from the finished file and show them.** Every failure this
  pipeline has produced was invisible to the automated checks and obvious in
  one frame: relics halved by the bottom edge, a beige-washed kill, a voiceover
  naming a relic the card does not call by that name.
- **Ship ffmpeg with the app** (`ffmpeg-static`), not "must be on PATH".
- Write the mp4 where Rick chooses and open the folder.

### Do not build in-app capture yet

The app is Chromium and could capture its own frames, roughly halving the wall
time. It ships when a **frame-hash comparison** proves it identical to the
Playwright capture for the same seed — not on the argument that it should be.
Otherwise it is a new picture-fault surface on a project that has been burned
twice by exactly that.

---

## 3. WHAT RICK HAS TO INSTALL FIRST

Neither feature can be tested without these, and neither is on the machine yet:

```powershell
winget install Gyan.FFmpeg          # the encode. Phase 3 blocks on it.

cd C:\dev\sundered-crown\tools       # the voice. 353 MB. Phase 2 blocks on it.
curl.exe -L -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl.exe -L -o voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

`kokoro-onnx`, `soundfile` and `playwright` are already installed. Both files
are gitignored on purpose — 353 MB in history is 353 MB nobody can delete, and
it is byte-identical on every machine that downloads it.

---

## 4. THE GATES

1. **`engine_ab` stays 192/192** against the current tip. Neither feature
   should touch a fight; run it anyway, because "it cannot have" is what
   somebody says right before finding out.
2. **`shell_identity.py` still passes** after any Electron or Playwright move.
   The pin is bit-equality, not version-equality — `math_fingerprint.py` is the
   check that says whether the pair still holds.
3. **The announcer spread goes to Rick as audio**, not as a description.
4. **Four frames off every finished mp4, looked at**, before it is called done.
