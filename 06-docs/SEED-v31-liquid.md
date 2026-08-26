# SEED — v31, 2026-08-19. THE RELIC IS A VESSEL.

`02-chain/sc-liquid.html` is the chain tip candidate. One builder on top of the
v30 tip, replacing every on-ball health visual with a glass sphere full of
liquid whose level is its life.

```
02-chain/sc-health18.html                            b57041681d7ee45b   (v30 tip)
  liquid_build.py   GLASS + LIQUID + SLOSH           0277dc5fc464f8b0   sc-liquid   <-- TIP
  liquid_build.py --fracture on --leak spill         ff28ebcf0936776f   sc-liquid-frac
```

`01-live/sundered-crown.html` `51c9bf566f9eb679` **untouched.**

Full record: `06-docs/LIQUID-NOTES.md`. Everything below is the short version.

## The one command

```
cd tools
python3 liquid_build.py --src ../02-chain/sc-health18.html --out ../02-chain/sc-liquid.html
```

The shippable JS lives in `04-experiments/_liquid_core.js` and is shared with
`liquid_lab.py`, so the standalone lab and the game **cannot drift**. Edit the
core, re-run the builder.

## Checks

```
liquid_probe.py            14/14 on BOTH builds, and --selftest couples the liquid to the sim
                           by 1e-6 and requires check [1] to break (it breaks
                           35 of 36 matches)
engine_ab --n 6            918/918 IDENTICAL field for field on all 18 relics
verify.py --n 12           13/13 over 153 pairings, mean 38.0s, 0% timeouts
frame cost                 sc-liquid -1.0%, sc-liquid-frac +3.0% median vs the
                           v30 tip @1080x1920 in a GPU-less box. NOT a phone number.
sweep cost                 17.75 -> 18.48s / 612 matches, +4%
```

## The switches

```
MARKS.mode      "none" (shipped) | "desperation" | "ticks"
FRACTURE.on     false, and CUT FOR GOOD -- built properly, fixed twice,
                rendered as a frame-for-frame A/B on the same seed, and turned
                down. 06-docs/LIQUID-NOTES.md §4b is the record. Do not rebuild
                it to find out; read that first.
LEAK.on         false. A spill needs a hole and the holes were the crack arms.
```

`sc-liquid-frac.html` ff28ebcf0936776f is kept as the RECORD OF A DECISION,
not as a candidate. It costs +3.0% median frame where the shipped build costs
-1.0%.

## What the next session should do first

1. **Watch it at phone size, with sound.** With the fracture off, damage is
   carried by the level and nothing else on the ball, permanently. That is the
   one open question this build creates, and the obvious second channel is
   already spent.
2. **Measure a real handset.** Five sessions of visual work are now unmeasured.
3. **Decide the lifeline.** It was deliberately left alone and now speaks a
   different visual language from the balls.
