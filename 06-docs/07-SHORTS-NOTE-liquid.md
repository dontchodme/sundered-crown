# 07-shorts is NOT in this zip

The full tree exceeds the 30 MiB handoff cap, so `07-shorts/` — the v27 sample
slate and every rendered clip — is left out. Everything else is here and
complete: the chain, every builder, every probe, the docs, and `01-live`
untouched.

Restore it by copying `07-shorts/` across from your `sc-seed-v27` tree.

## Delivered separately in conversation

```
07-shorts/lastlight/lastlight-v-gravemourn.mp4      Lastlight (blade 17.5) on the
                                                    lastlight-only build, 36.0s
07-shorts/lastlight/lastlight-v-axiom-v30.mp4       the v30 composed tip, seed
                                                    88489753, 51.1s
07-shorts/liquid/liquid-wm-v-axiom.mp4              THE VESSEL. Widowmaker v Axiom,
                                                    seed 3946016107, 47.4s.
                                                    Axiom ends on 2%, Widowmaker
                                                    wins on 17% -- picked so BOTH
                                                    vessels visibly drain
07-shorts/liquid/liquid-lastlight-v-grudgebearer.mp4  THE SUBSTANCE. Lastlight
                                                    (thinnest liquid) v Grudgebearer
                                                    (thickest), seed 2976898105,
                                                    38.5s
```

## How the two liquid clips were picked, because it is not the usual criterion

A short made to SELL the game wants a close finish. A short made to JUDGE THE
INSTRUMENT wants both vessels near empty, because a fight the winner finishes
at 80% says nothing about whether a falling level reads. The seed sweep scored
on `|winner_hp - 55|` first and duration second, over 260 seeds per pairing.

Both are rendered `--no-intro`, no VO, no cold open: all fight, because the
thing being judged is on the balls and the card is four seconds that are not.

```
python3 render.py --game ../02-chain/sc-liquid.html \
    --a widowmaker --b axiom --seed 3946016107 --no-intro \
    --out ../07-shorts/liquid/liquid-wm-v-axiom.mp4
```

Nothing in the build depends on `07-shorts/` existing.
