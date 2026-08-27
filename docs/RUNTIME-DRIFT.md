# RUNTIME DRIFT — the seed names a fight *on a given V8*

**Measured 2026-08-26, before any renderer work.** This was found by running
Phase 1's own falsification test, which had never been run to completion.

---

## THE SENTENCE THAT HAS AN UNWRITTEN CLAUSE

`CLAUDE.md` §1:

> `(build, relic A, relic B, seed)` → the same fight, always.

The clause is **…on the same V8 build.** It is not a caveat; it is load-bearing,
and nothing in the repo recorded it or pinned it.

---

## WHAT WAS RUN, AND WHAT CAME BACK

`tools/shell_identity.py`, 192 fights, the app's Electron against Playwright's
headless Chromium:

```
FAIL  80/192 identical
  app      Chromium 128.0.6613.186   (Electron 32.3.3)
  headless Chromium 151.0.7922.34    (playwright 1.62.0, unpinned)
```

**The shell is innocent.** Three checks say so, and they were run in this order
because the first two are what stop an innocent file being read for a day:

| probe | result |
|---|---|
| headless, same rows twice, same page | **identical** — deterministic within a runtime |
| headless, rows reversed | **192/192** — order-independent, no shared state between fights |
| `tools/math_fingerprint.py` | **9 of 20 Math functions differ in the last bit** |

```
identical : sin cos asin acos log sqrt sinh log1p log2 log10 hypot
DIFFERENT : tan atan exp cbrt cosh tanh expm1 atan2 pow
  Math.pow    electron=4004cdbd35066fbc  headless=4004cdbd35066fbd
  Math.exp    electron=400ba518ac162efa  headless=400ba518ac162ef9
  Math.atan2  electron=3fd16ec9a368d12b  headless=3fd16ec9a368d12a
```

V8 implements these in `ieee754.cc`. **Nothing in the language specifies their
last bit** and that file changes between Chromium releases.

### Why one bit is enough

`Math.pow` and `Math.exp` are not decoration in this engine. They are in the
per-step integrator:

```
6302:  f.vy += P.gravity * Math.pow((f.w.mass + f.burden * f.burdenMass) ...   gravity, every fighter, every step
6354:  const k = 1 - Math.exp(-P.relax * dt);                                  relax
6407:  f.headAngVel *= Math.pow(C.damp, dt * 120);                             head damping
6416:  f.headR += (target - f.headR) * (1 - Math.exp(-C.extend * dt));         head extension
7034:  const wA = Math.pow(mA, 1.7), wB = Math.pow(mB, 1.7);                   collision mass split
```

At `dt = 1/120` a 40-second fight is ~4,800 steps. A last-bit difference in the
gravity term compounds.

### The sensitivity, priced against a control

One ULP was added to a *single* function's result inside **one** runtime, then
the same 192 fights re-run against that runtime's own unmodified output:

```
headless(151) vs Electron(128)      : 80/192 identical
headless vs headless, +1 ULP on pow : 68/192
headless vs headless, +1 ULP on exp : 61/192
headless vs headless, +1 ULP on sin : 78/192      <- control: sin is IDENTICAL
headless vs headless, +1 ULP on atan2: 68/192        across the two runtimes,
                                                     so this arm measures the
                                                     sensitivity, not the drift
```

A one-ULP nudge to any one function reproduces the entire cross-runtime gap.
**The 112 differing fights are not a shell defect being amplified — they are
arithmetic chaos on a last bit, which is the only thing that actually differs.**

---

## THE PART THAT IS NOT ABOUT THE APP

The flagship v43 clip is `07-shorts/v43/stasis-v-heartwood.mp4`, recorded
everywhere in the docs as **"seed 25064, 23.0s, three holds"**, and mp4s are
gitignored on the stated grounds that **the seed rebuilds them.**

```
seed 25064  paradox v heartwood
  Chromium 128 : winner Paradox, hp 17, duration 44.52, clanks 16
  Chromium 151 : winner Paradox, hp 17, duration 46.41, clanks 17
```

It does not rebuild them. Same winner, same hp, same hit counts — **1.9 seconds
and one clank different**, which is a different film. This is the project's own
defect class again: wrong and right produce numbers that look right.

Nothing in the repo records which Chromium rendered any historical
measurement, and `playwright` is unpinned — there is no `requirements.txt`.

---

## WHAT THIS DOES AND DOES NOT BLOCK

**Does not block the renderer.** Gate 2 of `RENDERER-BRIEF.md` is a side-by-side
filmstrip, old renderer against new. That comparison is valid at any pin **so
long as both strips come out of the same runtime.** Generate the pair together
or the drift lands inside the review artifact.

**Does block:** treating the app as showing Rick the fight the mp4 will contain.
That is the single guarantee Electron was chosen for
(`docs/ARCHITECTURE.md` §1) and it is void until the pair is pinned.

---

## THE PIN — DECIDED AND PROVEN, 2026-08-26

Rick's call was **pin up, then prove.**

Version equality was never on offer. No Electron ships Chromium 151:

```
electron 32.3 -> chromium 128     <- was installed
electron 43.4 -> chromium 150
electron 44.0 -> chromium 152     <- now pinned
playwright 1.62.0 -> chromium 151 <- now pinned
```

**But version equality was never the property that mattered.** Bit equality
was, and it is measurable. Both candidates were fingerprinted against the
installed headless Chromium 151 before anything in `app/` was touched:

```
electron 43.4.1  Chromium 150.0.7871.224  vs headless 151  ->  PASS, all 20 functions
electron 44.0.0  Chromium 152.0.7977.54   vs headless 151  ->  PASS, all 20 functions
```

`ieee754.cc` did not move between 150 and 152. Electron 44.0.0 is pinned as
the newest of the two; **43.4.1 is a measured fallback**, not a guess, if a
fresh major turns out to misbehave in the shell.

### The gate, run end to end

```
electron 44.0.0, app/main.js --identity-check   192 fights in 3.3s
python shell_identity.py

  [identity] app      Chromium 152.0.7977.54  192 fights
  [identity] headless Chromium 151.0.7922.34
  PASS  192/192 identical.
```

**That is the first time Phase 1's falsification test has been carried to a
verdict, and the first time it has passed.** `docs/ARCHITECTURE.md` §1's
guarantee — that the app cannot show Rick something the video will not — is
now a measured fact on this machine rather than an argument about webviews.

### Where the pin is written down

| | |
|---|---|
| `requirements.txt` | `playwright==1.62.0`, with why |
| `app/package.json` + `package-lock.json` | `electron` exactly `44.0.0` |
| `tools/math_fingerprint.py` | the check that says whether the pair still holds |
| `app/main.js --identity-check` | the gate, now runnable without a person clicking |

`npm run identity` had advertised that flag since the shell was written and
nothing in `main.js` read it, so the script silently started the app instead.
**That is why a gate written in the same session as the app went four sessions
without a verdict.** It now runs hidden and exits on the result.

### What is re-baselined, and what is not

The build is untouched — no file in `02-chain/` was opened. What changed is
the runtime under it, so:

- **Anything re-derived from a seed from here on is on Chromium 151/152.** That
  includes every clip. `07-shorts/v43/stasis-v-heartwood.mp4` will rebuild as
  the 46.41s fight, not the 44.52s one that was filmed. The mp4 on disk, if it
  still exists, is the only copy of the fight Rick actually watched.
- **Numbers quoted in `06-docs/` were measured on an unrecorded Chromium** and
  none of them can be attributed now. They are records of a decision, not
  values to trust to the digit.
- **Nothing needs retuning on this account.** The tuned values are inputs, not
  outputs; a fight moving by one clank does not make a damage number wrong. If
  a specific measurement is about to carry a decision, re-run it — that is the
  ordinary cost of the pin, paid once.

### The rule that follows

**Never build a side-by-side filmstrip from two runtimes.** It is the review
artifact for the renderer work and it is exactly the shape of thing this drift
would hide inside.
