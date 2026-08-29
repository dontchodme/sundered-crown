# THE DESKTOP APP — architecture and plan

**Decided 2026-08-26 with Rick.** Electron shell over the existing engine.
Extraction, not rewrite. Both Claude Code and Cowork against this repo.

> **REORDERED, same day.** The renderer moved from phase 5 to first, and
> `docs/RENDERER-BRIEF.md` supersedes §7 below on sequencing. The reason
> is §0: because the sim cannot see a screen, a renderer rewrite cannot
> change a fight — so it is the *safest* large change here, not one that
> should wait behind the riskiest. The ordering argument in §2 was that
> phases 1-3 hand the extraction a review instrument; the app now exists,
> so that has been paid for. Phases 2 and 3 are unstarted and unchanged.

---

## 0. THE ONE FACT THE WHOLE PLAN RESTS ON

> **The simulation does not know a screen exists.**

`Fighter`, `Match` and `Sfx` — lines 5382–9810 of the build of record —
contain **zero** references to `document`, `canvas` or `getContext`. Verified,
not assumed. `Renderer` is a separate class fed by `LERP_FIELDS`.

Three consequences, and they are the reason this plan is shaped the way it is:

1. **The renderer can be replaced without touching a fight.** Every seed, every
   clip, every tuned number survives a total rewrite of the picture.
2. **The engine does not need porting.** It needs *hosting*. A shell, not a
   rewrite.
3. **Any change that does move a fight is detectable**, because
   `engine_ab.py` already proves two builds identical across every matchup.

That third one converts the scary part of this project from a gamble into a
mechanical process. **A refactor that can be falsified is not a risk.**

---

## 1. WHY ELECTRON AND NOT A GAME ENGINE

The instinct is Godot or Bevy. It is wrong here, and the reason is specific.

Rewriting the physics means every seed produces a different fight. The moment
that happens:

- `stasis-v-heartwood.mp4` and every other clip stop existing as reproducible
  artifacts — and **the seed is the only thing this repo keeps of them.**
- `engine_ab`'s 2760/2760 stops meaning anything.
- The ~102,000 fights v43 spent to find one damage number buy nothing.
- Every one of the 195 tools in `tools/` targets a build that no longer exists.

And worst: a physics rewrite mass-produces the exact defect class this project
has already been bitten by twice — **where "wrong" and "right" produce
identical numbers.** It would look right and be wrong, and nothing in the repo
could see it.

### Why Electron specifically, and not Tauri

Tauri is smaller (~10 MB vs ~150 MB) and uses the system webview. That is
normally the better trade. It is the wrong trade here:

> **Electron bundles the same Chromium that Playwright already drives in
> `cinema_clip.py`.** The app renders on exactly the engine the video pipeline
> is validated against. Same renderer on screen and in the mp4 means **the app
> cannot show Rick something the video will not.**

Given that this project's two worst defects were both things a person saw and
no tool could, buying that guarantee for 140 MB of disk is cheap. Tauri's
system webview varies by machine and by Windows update; the guarantee does not
survive it.

---

## 2. THE PHASES, IN ORDER, AND WHY THIS ORDER

The order is not by size. It is **by risk, and by which phase gives the next
one a better instrument.**

| # | phase | size | risk | what proves it |
|---|---|---|---|---|
| 1 | Electron shell, engine untouched | small | none | seed-identity vs headless |
| 2 | Announcer text box | small | low | rendered audio, measured |
| 3 | "Create Short" button | medium | low | byte-identical mp4 vs CLI |
| 4 | Module extraction | large | medium | `engine_ab` 2760/2760, per step |
| 5 | WebGL renderer | large | low to the sim | side-by-side filmstrips |
| 6 | Sound engine fixes | medium | chain-wide | OfflineAudioContext spectra |

**Phases 1–3 give Rick a working app with three of his four features before a
single line of engine code moves.** That is deliberate. It de-risks the
extraction by putting it last — and it hands the extraction a better instrument
than it would otherwise have, because **once the app exists, it is how Rick
watches, and watching is the only detector this project has for the picture
faults.**

---

## 3. PHASE 1 — THE SHELL

```
app/
  package.json
  main.js          Electron main. Window, menu, IPC, job queue.
  preload.js       contextBridge. The ONLY surface the page can reach.
  ui/
    shell.html     chrome around the game: relic pickers, seed box, controls
    shell.css
    shell.js
```

The window loads `02-chain/sc-paradox-pace.html` **unchanged**. No engine
edits in this phase, none.

Security posture, non-negotiable: `contextIsolation: true`,
`nodeIntegration: false`, `sandbox: true`. The page gets Node capability only
through named `preload` functions. The game HTML is trusted content, but the
habit is what stops a later "just load this remote thing" from being a
one-liner.

### The falsification test for Phase 1

Not "it opens". **Run the same seeds through both renderers and diff:**

```
AC.simulate(idA, idB, seed)  in the Electron window
AC.simulate(idA, idB, seed)  in Playwright's headless Chromium
```

Every field identical across a few hundred seeds, or the shell has changed the
engine and the phase is not done. This is cheap and it is the only thing that
proves the guarantee in §1 actually holds on Rick's machine.

> **RUN 2026-08-26, AND IT FAILED: 80/192.** Not because the shell had changed
> the engine — because the app's Chromium (128, via Electron 32) and
> Playwright's (151) do not agree on the last bit of `Math.pow`, which the sim
> integrates gravity through on every one of ~4,800 steps. **This paragraph
> was right that the test was the only thing that could prove §1, and it was
> incomplete about what a failure means.** The pair is now pinned — Electron
> 44.0.0 and playwright 1.62.0, different Chromium versions, bit-identical
> maths — and the test reads `PASS 192/192`. `docs/RUNTIME-DRIFT.md` carries
> the measurement; `tools/math_fingerprint.py` is the standing check.

---

## 4. PHASE 2 — THE ANNOUNCER TEXT BOX

**This is the smallest of the four features, because the tool already exists.**
`cinema_vo.py --text "..."` speaks arbitrary text verbatim today. Kokoro runs
locally and offline; nothing is sent anywhere.

What the phase actually adds:

- A textarea, a voice picker, and a **preview** button — hear it before it goes
  into a four-minute render.
- The `SPOKEN` compound-splitting table must survive the port. Kokoro runs
  "Ironhail" into one mushy cluster; ten relic names are already corrected
  there and the eleventh will need it too.
- `--parts` / `--gaps` must survive. **Punctuation does not control timing in
  Kokoro** — `"?..."`, `"? ..."` and `"."` all give the same contour. A pause
  has to be real silence, measured.

### The design problem this phase exposes, named now

The intro card is **4.0 s** and today's voiceover is written to fit inside it
with air on both sides. **Arbitrary text breaks that.** A twelve-word line
overruns the card and gets cut.

Two options, and this is one for Rick:

- **The card sizes to the line.** VO is rendered first, its duration measured,
  the card holds for `dur + 2×air`. Timing stays right at any length; the cold
  open drifts later the longer he writes.
- **The line is capped**, with the box showing measured seconds live and
  refusing to render past the cap. Timing never moves; long lines are refused.

`verify.py` already enforces a 72-character limit on ult tips, and v43 hit it
for the first time — so this project has form for both answers.

### Runtime path for Kokoro

Two candidates, and **the second is not yet verified**:

- **Python sidecar.** Bundle a venv with `kokoro-onnx`; the app shells out
  exactly as `cinema_vo.py` does. Certain to work — it is what works today.
- **`kokoro-js` / transformers.js in-process.** No Python at runtime, much
  smaller install. Kokoro's phonemization goes through espeak-ng, and whether
  the JS path reproduces the Python path's output **has to be measured, not
  assumed** — same text, same voice, spectra compared. If it differs, the
  announcer stops sounding like the announcer.

Start on the sidecar. Test the JS path against it as a separate, falsifiable
piece of work.

---

## 5. PHASE 3 — THE "CREATE SHORT" BUTTON

The pipeline exists and is measured: capture → 1080×1920 → VO mix → delivery
measurement. `shorts_build.py`, with a mix graph where **every term is
load-bearing** and one flag (`alimiter ... level=false`) that is invisible in
the output and merely makes the file clip if forgotten.

**Do not reimplement that graph from memory. Move it, with its comments.**

### 5a — shell out (ship this)

Button → main process → job queue → the existing Python pipeline → mp4 on
disk → open the folder.

Non-negotiable in the UI, because the timings are real: a full 60 fps capture
is ~2,800 frames and **3–4 minutes**, then 1–2 to encode. The button cannot
block. It needs a job queue, live progress, a cancel, and the log surfaced —
not a spinner that lies.

The two laws from `SHORTSHANDOFF.md` carry over into the UI:

1. **Never re-render only the audio to "fix" a mix.** Enforced by construction:
   the mix is only ever built from the capture stage's `on.wav`.
2. **Watch the output before you hand it over.** So the app pulls four frames
   from the finished file and shows them. Every failure this pipeline has
   produced was invisible to the automated checks and obvious in one frame.

`ffmpeg` ships with the app (`ffmpeg-static`), not "must be on PATH".

### 5b — capture in-app (only after it is proven)

The app *is* Chromium. It can capture its own frames and delete Playwright from
the runtime path — roughly halving the wall time.

**It does not ship on that argument alone.** It ships when a frame-hash
comparison shows the in-app capture is identical to the Playwright capture for
the same seed. Otherwise it is a brand-new picture-fault surface, added to a
project that has been burned twice by exactly that.

---

## 6. PHASE 4 — MODULE EXTRACTION

The scary one, made mechanical.

### The trick that keeps the 195 tools alive

`scpage.py`, `verify.py`, `engine_ab.py` and `cinema_clip.py` all load **one
self-contained HTML file**. So:

> **The build output stays a single self-contained HTML file.** Sources become
> modules; a bundler inlines them back. Every existing tool keeps working, and
> `engine_ab` can compare old build to new build directly.

esbuild → IIFE bundle → injected into an HTML template. No runtime, no
`import` in the shipped file, no dependency the game did not have before.

### The target shape

```
src/
  config.js        CONFIG, STATUS, AFFINITIES, HEALTH_CHUNKS, BRINK, ...
  roster.js        WEAPONS, SHAPES, WEAPON_BY_ID
  math.js          makeRng, clamp, lerp, angDiff, segDist, segSegDist, ...
  sim/
    fighter.js     class Fighter
    match.js       class Match
  audio/
    sfx.js         class Sfx
  render/
    renderer.js    class Renderer
    relic.js       drawGlassRelic, glassCracks, liquidPoly, fracture, vents
    weapon.js      litWeapon, weaponGlow, grainSprite
  cinema/
    director.js    CINE, cinePlan, cineScore, cineCamera, cineTier, CineAudio
    interp.js      LERP_FIELDS, lerpAng, smooth
  main.js          page glue, the rAF loop, window.AC
tuning.json        every tuned number, in ONE diffable place
build/
  build.mjs        esbuild → inline → single HTML
```

### The order, and the receipt at every step

Leaves first, glue last. **One module per commit, and every commit carries its
`engine_ab` result in the message.**

```
math → config → roster → audio → sim → render → cinema → glue
```

```bash
python3 engine_ab.py --a <previous build> --b <new build> --ids <all> --n 10
# 2760/2760 or the commit does not happen
```

If one fight differs, the extraction moved something. Revert the step, find it,
redo it. **Never carry a red forward — the whole value of this method is that
the detector stays trustworthy.**

### The three things that will actually bite here

1. **Everything currently shares one script scope.** Top-level `const` is
   visible everywhere with no declared order. Splitting into modules makes
   ordering explicit and **will surface circular references** — `render` reads
   roster tables, `cinema` reads sim state, `sim` fires into `SFX`. They are
   findable and `engine_ab` is the detector, but expect them.

2. **The builders splice HTML with regex.** `roster15_build.py`,
   `roster_gs_build.py`, `introcard_build.py` and twenty others insert into a
   text file. Once the source is modules, they must edit *modules* — which
   means the build chain is rewritten in this phase too. That is most of the
   work, and it is also the whole point: a 25-step chain to reproduce one file
   is the thing that has been costing Rick.

3. **THE TUNED NUMBERS MUST CARRY EXACTLY.** They live in the builders today
   (`TUNED`, `TUNED_GS`) and a previous session already lost twelve of them by
   writing into generated HTML. Moving them into `tuning.json` is right —
   explicit, diffable, one place — and the move itself is verified by
   `engine_ab`, because a single wrong digit changes a fight.

---

## 7. PHASE 5 — THE RENDERER, WHICH IS THE "CRISPY" ASK

Once `render/` has a defined interface — *take an interpolated Match snapshot,
draw to a surface* — the inside of it is free.

**And the sim cannot notice.** `engine_ab` returns 2760/2760 across a total
renderer rewrite, by construction. This is the one place to be genuinely
ambitious, and it is the *safest* large change in the plan.

### What WebGL2 buys that Canvas 2D cannot

Real additive bloom on ult art instead of pre-blurred cache sprites; particle
systems in the thousands instead of the dozens; motion trails from a persistent
framebuffer; chromatic aberration and screen shake as post-process on impact;
120 fps headroom where Canvas 2D is already spending measurable time in
`weaponGlow`.

### Library

**PixiJS v8.** It is a 2D renderer — which is what this game is — with a mature
filter chain, WebGL2 with a WebGPU path, and it is open source. Three.js would
be the wrong tool: a 3D scene graph for a game that has no third dimension.

### The staging that makes this affordable

The existing art is a lot of bespoke Canvas 2D: `drawGlassRelic`,
`glassCracks`, `liquidPoly`, `litWeapon`, the whole `SHAPES` table. Porting all
of it to WebGL at once is a large and unnecessary bet.

> **Composite first, port second.** Keep Canvas 2D for the relic and weapon
> art, render it to an offscreen texture, and composite that in WebGL with the
> post-processing stack. That is most of the visible gain for a fraction of the
> work, and individual art pieces migrate to native WebGL afterwards, one at a
> time, each one reviewable on its own.

### The review artifact — this phase does not get an automated pass

Numbers cannot see this phase; that is the point of it. So every step ships
**side-by-side filmstrips**: old renderer and new, same seed, same frame
indices, one image. The check is Rick's eyes, and the deliverable is built for
them.

---

## 8. PHASE 6 — SOUND

Two live bugs, both measured, both chain-wide across 24 shipped voices:

- **`_burst` does not loop its 0.6 s noise buffer.** Any burst longer than that
  plays silence for its tail.
- **`_tone` ends on an exponential ramp over its whole length.** A held note
  does not exist in this toolkit; anything that must last is re-struck.

The instrument is already built and it is why this is doable: render every
voice in an `OfflineAudioContext`, before and after. **Any voice whose spectrum
moves gets listened to by a person.** A sound cannot ship quiet again — that
check exists because v42 shipped a silent ultimate through five green passes.

**One question for Rick, and it is his by rule 2.** "Top of the line sound
effects" may mean more than a better synth. Sample-based layers under the
synthesized voices would raise the ceiling a long way — at the cost of the
project's current property that a build is one text file with no assets. That
is a real trade and it is his call, not mine.

---

## 9. WHAT I AM NOT PROMISING

- **A rewrite of the sim is not in this plan.** If a fight has to change, it
  changes because a measurement said so, through the existing tools, one number
  at a time.
- **Phase 4 will find bugs.** Extraction always does. Each is a decision — fix
  it and price it against `engine_ab`, or file it and leave the behaviour
  alone. Silently "fixing" behaviour during a refactor is how a project loses
  a tuning pass it cannot see it lost.
- **`kokoro-js` is unverified** (§4). It gets measured before it gets trusted.
- **Phase 5b is unverified** (§5b). Same.
- **None of this closes the twelve open items in `CLAUDE.md` §8.** They are
  still open, and `01-live` is still nine relics behind.
