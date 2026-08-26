# HEALTH — the patch.  `sc-health.html` `d0bb4890b19edc47`

Built from chain tip `02-chain/sc-cardspin.html` `ec9b8d753235385d` by
`tools/health_build.py`. The artifact is **generated, never hand-edited** — if
you need to change anything in here, change the builder and rebuild, or the
engine drifts out of the file that was tuned.

Four things, all presentation. `engine_ab` proves the simulation is untouched.

```
A  GAUGE      health on the shell: stroke 1.7 -> 6.0, sweep 360 -> 270 with the
              gap at the foot, the empty track DRAWN, and four countable chunks
              of 75 HP. Cream bevel on each lit chunk so the red scale still
              reads on the six relics that wear red or amber themselves.
D  LIFELINE   one panel above the hall: both relic names, both percentages,
              both lives in the same four chunks, two heads meeting at a marked
              centre. Drawn LAST in screen space, so a cinema cut cannot slice
              it (v26 HUD spill).
F  STAGES     the chunk boundaries are the stages; the third one IS
              CONFIG.desperation.at. The crossing flash holds no state -- it is
              derived from hpGhost lagging hp.
U  ULT BLOCK  a bespoke sigil per relic (17/17, keyed on weapon id, enforced by
              the builder), a quartered charge bar, a countdown in the last five
              seconds, and the relic's own `ult.tip` while it is imminent.
+  TYPE       Atkinson Hyperlegible Next + Mono, embedded as base64 WOFF2,
              48 stacks rewritten. SIL OFL 1.1; notice ships in the artifact.
```

---

## 1. Restore

```
tools/*.py            -> your tools/          (scpage.py IS MODIFIED, see §4)
tools/fonts/          -> your tools/fonts/    (needed to rebuild)
02-chain/sc-health.html -> your 02-chain/
```

## 2. Prove it before you trust it

```bash
cd tools
python3 engine_ab.py --a ../02-chain/sc-cardspin.html \
                     --b ../02-chain/sc-health.html \
  --ids dawnbringer,widowmaker,grudgebearer,thornwake,gravemourn,slagheart,\
spellbreaker,ironhail,lightkeeper,farwarden,aureole,censer,emberedge,\
oathwound,heartwood,nightfell,axiom --n 8
python3 verify.py --game ../02-chain/sc-health.html --n 40
```

Expect **1088/1088 identical** and **13/13**. Anything else, stop.

Rebuild from source to check the artifact is what the builder makes:

```bash
python3 health_build.py --src ../02-chain/sc-cardspin.html --out /tmp/x.html
sha256sum /tmp/x.html            # must start d0bb4890b19edc47
```

## 3. Ship

`health_build.py` refuses to write `sundered-crown.html` or `sc-playable.html`,
so shipping is deliberate and manual:

```bash
cp ../02-chain/sc-health.html ../02-chain/<new tip name>   # promote the tip
# then, only on your word:
cp ../02-chain/sc-health.html ../01-live/sundered-crown.html
# and update SEED.md with the hash
```

## 4. The one thing that will bite you if you skip it

**`scpage.py` is modified and must go back with the rest.** The artifact embeds
its fonts; Canvas draws the FALLBACK face — and returns the fallback's metrics —
for any text measured before those faces parse. A capture taken one frame early
is silently in the wrong typeface with the wrong widths and looks entirely
plausible. The page now withholds `window.AC` until `document.fonts.ready`, and
`scpage.game()` waits on it. Every capture in the repo goes through that one
function. With the old `scpage.py`, sheets and renders may photograph the
fallback.

## 5. Flags, live in the console

```js
BAND.pos = "bottom"    // move the whole band under the hall and redraw
TUG.mode = "ratio"     // one divider instead of two mirrored halves
TUG.num  = true        // raw HP instead of the percentage
ULTBAR.tip = false     // drop the ult tip line
TUG.on = false         // remove the lifeline entirely; gauge + stages stand alone
```

`BAND.pos` defaults to **top**. Bottom composes better on its own, and it was
built and looked at — but on Shorts the bottom strip is where the caption, the
channel handle, the like/comment/share column and the scrub bar go, so the B
fighter's block lands under platform chrome. Top is the strip the platform
mostly leaves alone.

## 6. Cost

`tools/hud_cost.py` — same harness, both builds, back to back:

```
ironhail/oathwound     +2.4%
dawnbringer/censer     +1.9%
MEAN                   +2.2%   draw cost vs the shipped build
```

Ratio only. This container has no GPU and its rasteriser disagrees with real
hardware by ~10x, so the absolute milliseconds are meaningless — but the two
builds were measured in one session through one instrument, which is the only
question the patch has to answer. **It has not been measured on your machine
or on a handset**, and the standing budget is ~6 ms at 165 Hz.

## 7. New tools

```
health_build.py   the builder. Fails if any relic has no sigil.
health_sheet.py   the gauge at chosen HP values, two builds, 1:1 + acuity
roster_sheet.py   all 17 relics x 5 HP values -- this is what caught the red-on-red
ult_sheet.py      all 17 ult blocks x 3 charge levels, with a sigil preflight
ult_frame.py      both ult blocks hot at once -- the only state that proves they
                  do not collide, and it found that they did
stage_shot.py     the four chunk crossings, by writing hp and hpGhost by hand
hudpos_shot.py    top vs bottom, one artifact, one frame
hud_cost.py       relative draw cost, forced raster, N draws in one rAF
```

## 8. Open decisions

1. **Same-affinity pairs still read as one object.** Dawnbringer/Censer are both
   sanctified cream across names, chunks and charge bars. The centre axis is a
   2 px grey line and wants to be a hard bright divider. One small change.
2. **The ult name has no owner in the band** now that the relic names moved into
   the lifeline — bound only by side and by the charge bar's affinity colour.
3. **Is the ult tip a caption?** It is rule 4's *remind during*, transient by
   construction, and it is also the only prose this HUD has ever carried.
4. **The `near` window is five SECONDS, not a fraction**, so a 13 s ult shows its
   countdown from 62% charge and an 18 s one from 72%.
5. **The sigils are first-pass** — one round of eyes. Rootfast and Corollary are
   the densest, Bramblesnare the faintest.
6. **Perf on real hardware.** §6 is a ratio in a GPU-less box. The 165 Hz budget
   has still never been measured against any of this.
7. **Promote to the chain tip of record?** `sc-cardspin.html` is still it.
