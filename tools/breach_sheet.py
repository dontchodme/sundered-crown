#!/usr/bin/env python3
"""THE FOUR STATES, AS A SHEET — the cut, the tear, the dormant hole, the jet.

    python breach_sheet.py --out ../05-reference/v59/breach-states

SHAPE QUESTIONS GO TO A SHEET; SCALE QUESTIONS NEED THE VIDEO (CLAUDE.md §0,
the hand art, three rounds of guessing settled by one reference clip). This
answers the shape questions and does not pretend to answer the other one.

Design §5c names four states and says one of them is the mechanic:

    THE CUT      the blade sweeps through the stone. This is where the SIZE is
                 decided and the frame has to show the depth
    THE TEAR     the wall opens BEHIND the blade as it leaves. Sized
    THE HOLE     dormant between firings, glowing, aimed. Most of its nine
                 seconds
    THE JET      the front crosses the hall in 0.9s

and then a fifth thing the art has to carry, which is the count:

    A VIEWER SHOULD BE ABLE TO TELL THE FOURTH TEAR FROM THE FIFTH **BEFORE**
    THE FIFTH LANDS, or the ultimate ends without having promised it.

That is Grasp's four-knuckles problem one relic on, and it is open decision 1.
The `remaining` panels are it: the same shell at five chips and at one.

It drives a REAL match — nothing is posed — to the first frame that satisfies
each predicate, and photographs the canvas the game draws. v54 §2c is why this
exists at all: Deadfall's ARMING state was drawn at alpha 0.16 against a hall
that already had a gold pentagram on its floor, it did not read at all, and no
probe in this repo could have said so.

A SMALL AND A LARGE HOLE ARE THEIR OWN PANELS, because Rick's size mechanic is
the one thing here that can be measured green and still be invisible: `k` runs
0.5 to 1.5 and the built distribution reproduces the lab's, but a 7px hole and
a 21px hole on a 540-wide frame is a question for eyes.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

SEEK_JS = r"""([rid, foe, sd, want, secs]) => {
  /* THE LIVE PAGE STANDS DOWN, or the rAF loop redraws its OWN match over
     this one between the draw and the shutter. `cinema_clip`'s harness sets
     the same flag for the same reason, and the demo panel is a DOM overlay so
     hiding it is separate. */
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a;
  window.__m = m;
  const orig = m.tearVent;
  let tearAt = -9, tearK = 0;
  m.tearVent = function (f, P){
    const b = f.ultBreach ? f.ultBreach.tears : -1;
    orig.call(m, f, P);
    const a2 = f.ultBreach ? f.ultBreach.tears : -1;
    if (a2 > b){ tearAt = m.t; tearK = m.vents[m.vents.length - 1].k; }
  };
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    const V = me.ultBreach;
    const vs = m.vents;
    const live = vs.filter(v => v.own === "a");
    const jets = live.filter(v => v.front !== null && v.front !== undefined
                                  && v.front > 240 && v.front < 700);
    let ok = false;
    /* THE CUT. The blade is IN the stone and no tear has resolved yet, which
       is the frame the size is being decided on. */
    if (want === "cut") ok = !!(V && V.pass && V.pass.dwell > 0.05
                                && V.pass.maxPen > 70 && m.t - tearAt > 0.5);
    /* THE TEAR, on the frame after it resolved */
    if (want === "tear") ok = m.t - tearAt >= 0 && m.t - tearAt < 0.06
                              && live.length > 0;
    /* A SMALL ONE AND A LARGE ONE, dormant. `k` is the whole size mechanic. */
    /* A DORMANT FRAME IS RARE AND THAT IS THE MECHANIC, not the predicate:
       `warm` is 0.35 and `period` 1.1 against a front that takes 0.9s to cross
       the hall, so a hole is between firings for about a fifth of its life.
       The first cut of these two panels asked for a dormant frame AND a size
       and reached neither in 120 seconds. */
    if (want === "graze") ok = live.some(v => v.k < 0.80 && v.t > 0.4);
    if (want === "slash") ok = live.some(v => v.k > 1.35 && v.t > 0.4);
    /* THE JET, mid-flight and clear of the wall */
    if (want === "jet") ok = jets.length > 0;
    /* THE HALL, with several holes open at once */
    if (want === "hall") ok = live.length >= 4;
    /* THE COUNT — the fifth chip and the first. Open decision 1. */
    if (want === "five") ok = !!(V && V.tears === 0 && V.t > 0.25);
    if (want === "one")  ok = !!(V && V.n - V.tears === 1);
    if (ok){
      AC.__draw(m);
      /* THE PIXELS COME BACK IN THIS SAME JS TURN. The composited frame lives
         in a drawing buffer that is gone by the time an out-of-process
         screenshot asks for it. */
      return { t: +m.t.toFixed(2), holes: live.length,
               left: V ? V.n - V.tears : -1,
               ks: live.map(v => +v.k.toFixed(2)),
               halves: live.map(v => +v.half.toFixed(1)),
               png: document.getElementById("cv").toDataURL("image/png") };
    }
  }
  return null;
}"""

PANELS = [
    ("cut",   "THE CUT — the blade is inside the stone and nothing has torn "
              "yet. This is the frame the SIZE is decided on"),
    ("tear",  "THE TEAR — the wall opens behind the blade as it leaves"),
    ("graze", "A GRAZE — k under 0.75. Rick's size mechanic at its small end"),
    ("slash", "A SLASH — k over 1.35, and it is the same object three times "
              "the width"),
    ("jet",   "THE JET — the front crossing the hall, tapering from the wall, "
              "white only at the head"),
    ("hall",  "FOUR HOLES AT ONCE — the separator from Benediction and the "
              "Sentinel is MULTIPLICITY: those are one line owned by a "
              "wielder, this is the HALL firing"),
    ("five",  "FIVE CHIPS — the licence just opened. Open decision 1"),
    ("one",   "ONE CHIP — the next tear is the last, and a viewer should be "
              "able to see it coming"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-breach.html")
    ap.add_argument("--relic", default="cindercleave")
    ap.add_argument("--foe", default="emberedge")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="../05-reference/v59/breach-states")
    A = ap.parse_args()

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    path = resolve_game(A.game)
    print(f"\nBREACH — the four states, off a real match\n  game {path.name}")
    print(f"  {A.relic} vs {A.foe}, seed {A.seed}")

    with game(game_path=path) as (page, errors):
        for want, caption in PANELS:
            r = page.evaluate(SEEK_JS, [A.relic, A.foe, A.seed, want, A.secs])
            if not r:
                print(f"  --    {want:<6} NOT REACHED in {A.secs:g}s")
                continue
            p = out.parent / f"{out.name}-{want}.png"
            p.write_bytes(base64.b64decode(r.pop("png").split(",", 1)[1]))
            print(f"  ok    {want:<6} t={r['t']:>6}s  {r['holes']} holes, "
                  f"{r['left']} chips left, k {r['ks']}  -> {p.name}")
            print(f"        {caption}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
