#!/usr/bin/env python3
"""IS THE `_twinConjured` MERGE INVISIBLE IN A WHOLE FRAME, NOT JUST A SHAPE?

    python3 merge_frame_check.py --a _pristine.html --b sundered-crown.html

`twin_identity.py` proved `_twinConjured`/`_gsConjured`/`_whConjured` render
identically in ISOLATION, on their own offscreen canvases. That is not the same
claim as "the artifact renders identically", and v17's SEED.md makes the second
one. This closes the gap.

WHY IT IS BEING ASKED NOW
-------------------------
The fight-card patch's probe [3] measures the lit fraction of the first card
frame. The patch reports **0.0298** built from the pristine `f78e0253`; the same
builder on our merged `95d34e6c` line reports **0.0304**. Both report 0.0049 for
their unpatched source. A 2% difference in a number that should be bit-equal is
either a real render change or something the probe is sampling that is not the
render — and "close enough" is not an answer available here.

WHAT WOULD COUNT AS FAILURE
---------------------------
Any non-zero differing pixel count on a pinned match, over several pairings
chosen to include a twinblade (the shape that moved) and several that cannot
contain one (the control). A twinblade-free pairing that differs would mean the
merge damaged shared code; a twinblade pairing that differs would mean the
isolation test was measuring the wrong thing.
"""
from __future__ import annotations
import argparse, base64, io, pathlib, sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

FRAME = r"""
([a, b, seed, steps, w, h]) => {
  AC.setResolution(w, h);
  const m = new AC.Match(a, b, seed);
  for (let i = 0; i < steps; i++) m.step(1 / 60);
  AC.__draw(m);
  return document.querySelector("canvas").toDataURL("image/png");
}
"""

# widowmaker and spellbreaker are the two twinblades — the shape the merge
# touched. The last two pairings contain neither and are the control: if they
# differ, the damage is in shared code, not in the merged shape.
PAIRS = [("widowmaker", "grudgebearer", 111),
         ("spellbreaker", "dawnbringer", 222),
         ("widowmaker", "spellbreaker", 333),
         ("dawnbringer", "grudgebearer", 444),
         ("thornwake", "gravemourn", 555)]
STEPS = [0, 40, 200]


def shots(path, w, h):
    out = {}
    with game(game_path=path) as (page, errors):
        for (a, b, seed) in PAIRS:
            for st in STEPS:
                d = page.evaluate(FRAME, [a, b, seed, st, w, h])
                im = Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1])))
                out[(a, b, seed, st)] = np.asarray(im.convert("RGB")).astype(np.int16)
        if errors:
            sys.exit(f"{path.name}: {errors[:3]}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", required=True, help="the build the silhouette was approved on")
    ap.add_argument("--b", required=True, help="the merged build")
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--h", type=int, default=960)
    A = ap.parse_args()

    sa = shots(HERE / A.a, A.w, A.h)
    sb = shots(HERE / A.b, A.w, A.h)

    print(f"{A.a}  vs  {A.b}     {A.w}x{A.h}\n")
    print(f"{'pairing':<30}{'step':>6}{'diff px':>10}{'maxDelta':>10}")
    print("-" * 56)
    total = 0
    for k in sa:
        d = np.abs(sa[k] - sb[k])
        npx = int((d.max(axis=2) > 0).sum())
        total += npx
        twin = "twin" if k[0] in ("widowmaker", "spellbreaker") \
                      or k[1] in ("widowmaker", "spellbreaker") else "ctrl"
        print(f"{k[0]+' v '+k[1]+' ('+twin+')':<30}{k[3]:>6}{npx:>10}{int(d.max()):>10}")
    print()
    ok = total == 0
    print(f"  TOTAL {total} differing pixels over {len(sa)} frames — "
          f"{'IDENTICAL' if ok else 'THE MERGE MOVED THE RENDER'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
