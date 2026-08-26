# v38 — HANDOFF. Where this is and what to pick up.

**2026-08-20.** Two relics added to the chain this session; the twentieth was
designed, built, tuned, filmed and posted-cut in one sitting.

```
02-chain/sc-redbarb.html    428860147c4570da   razor tips, presentation only
02-chain/sc-redflail.html   07d4c845732cfe72   <-- THE BUILD OF RECORD CANDIDATE
built off 02-chain/sc-twinshade-scrunch.html 859692484ce77e0f
01-live UNTOUCHED, still on sixteen

flail_relic_probe   17/17
engine_ab           1710/1710 IDENTICAL on the other nineteen, twice
verify.py --n 40    13/13 . 0/7600 timeouts . spread 14.7pp . mean 38.1s
director_diag       Bloodmill 15.53x -> 2.16x ex-kill; Triplicate 1.69x unmoved
flail_sweep's runtime override vs a real rebuild: 380/380 identical
```

## Read in this order

| doc | the headline |
|---|---|
| `look.md` | The cell measured BEFORE any design work. Hemorrhage holds ≥2 stacks 41% of a fight against 52% and 59% for the school's other two — and the cause is the status CLOCK, not the chain. Also: the published contact-rate table counted ULTIMATES as contact. |
| `design.md` | §1 in Rick's words, and nothing started before it existed. |
| **`README.md`** | **The build. §4 is the one to read: a third of the ultimate is a mechanic nobody designed, and the hemorrhage uptime that justified the whole cell is worth −0.5pp.** |

## Three things that outlive the relic

1. **`contact_rate_probe.py` counted ultimates as contact.** Restored to the
   tree with `--noult`. The flail is the LOWEST-contact type in the game, not
   the fifth, and v36's reach-dominance finding is a tie.
2. **Six instruments stepped 1/60 where `CONFIG.physics.dt` is 1/120.** v37
   found this; it recurred here and was fixed before any number was quoted.
3. **The director's crowd exception is per-relic now.** v37 open decision 3,
   come due. `crowd` is a boolean the volley rule reads; `crowdMul` is a
   strength each ultimate declares. Triplicate declares none and is untouched.

## What is NOT in this repo

`.gitignore` at the root explains each. In short: the mp4s and wavs (the seed IS
the fight — commands in `sc/WHATS-NOT-IN-THIS-ZIP.md`), `05-reference/**/*.png`
(every one is a probe's output), the 338 MB kokoro models (`FETCH-KOKORO.md`,
two curls), and frame caches.

**Restoring the voice** is required to re-render a short with VO:

```bash
cd sc/tools && bash -c 'curl -sL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx && curl -sL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin'
pip install kokoro-onnx soundfile --break-system-packages
```

## The posting cut, and how to rebuild it exactly

```bash
cd sc/tools
python3 cinema_vo.py --a Threshmaw --b Twinshade \
  --parts "The Sundered Crown.|Threshmaw...|versus Twinshade." --gaps "0.22,0.16" \
  --out ../07-shorts/v38/vo-threshmaw-twinshade.wav
python3 cinema_clip.py --game ../02-chain/sc-redflail.html \
  --a redflail --b twinshade --seed 18392971 --full \
  --vo ../07-shorts/v38/vo-threshmaw-twinshade.wav --vo-at 0.3 \
  --shorts --fps 60 --w 540 --q 0.80 \
  --out ../07-shorts/v38/threshmaw-v-twinshade-open.mp4
```

**NO `--intro` and NO `--cold-open`.** That is the change: the card is gone and
the scrunch does the introduction without freezing the hall. README §10.

## The first four things to pick up

1. **`01-live` is FOUR relics behind** — Lastlight, Slagheart, Triplicate and
   Threshmaw all exist and nobody outside this tree can play them. v27 open
   decision 1, and by a distance the oldest open thing in the project.
2. **Pull the analytics on the card removal.** The prediction is registered in
   README §10 and it is v32's, unaltered: r(6) ~0.28 → ~0.45+ with the
   post-0:05 tail unchanged at 0.43. If the tail moves too, find out why before
   crediting the card.
3. **Bloodmill has no set-piece art.** Every other ultimate in the game has a
   `drawUltUnder`/`drawUltOver` branch; this one has a sound and spikes and the
   generic banner.
4. **The design's stated rationale is falsified and nothing has replaced it.**
   README §4b.
