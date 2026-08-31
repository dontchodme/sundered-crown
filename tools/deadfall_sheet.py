#!/usr/bin/env python3
"""THE SIGIL, AS A SHEET -- arming against armed against coming apart.

    python deadfall_sheet.py --out ../05-reference/v54/deadfall-states.png

SHAPE QUESTIONS GO TO A SHEET; SCALE QUESTIONS NEED THE VIDEO (CLAUDE.md §0,
the hand art). This answers exactly one shape question and does not pretend to
answer the other:

    CAN A VIEWER TELL AN ARMED SIGIL FROM A CRACKLING ONE?

That is §8.4's tenth check and the one thing in stage 3 no probe can run. With
a fuse the crackle was a COUNTDOWN and the tension was time; with a mine it is
an ARMING animation and the tension is space, so a viewer who cannot separate
the two states cannot see the mechanic at all.

It drives a REAL match -- no posed objects -- to the frames where each state
exists, and photographs the canvas the game draws. Whether the difference
survives motion, a phone screen and two balls moving over it is the video's
question and Rick's.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

# DRIVE TO A STATE, THEN DRAW. Every panel is a real match stepped to the
# first frame that satisfies its own predicate, so nothing here is posed.
SEEK_JS = r"""([foe, sd, want, secs]) => {
  /* THE LIVE PAGE STANDS DOWN, or the rAF loop redraws its OWN match over
     this one between the draw and the shutter -- the first cut of this tool
     photographed the intro card of a Dawnbringer/Grudgebearer fight nobody
     asked for. `cinema_clip`'s harness sets the same flag for the same
     reason, and the demo panel is a DOM overlay, so hiding it is separate. */
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match("nightfell", foe, sd);
  const me = m.a.w.id === "nightfell" ? m.a : m.b;
  window.__m = m;
  const live = () => m.sigils.reduce((s,g)=>s+g.ch.filter(c=>!c.dead).length,0);
  let step = 0, prevLive = 0;
  while (!m.over && step < secs / DT){
    const before = live();
    m.step(DT); step++;
    const after = live();
    const arming = m.sigils.filter(g => g.t <  g.arm).length;
    const armed  = m.sigils.filter(g => g.t >= g.arm).length;
    let ok = false;
    if (want === "arming") ok = arming > 0 && armed === 0 && m.sigils.length > 0
                                && m.sigils[0].t > 0.5 && m.sigils[0].t < 1.2;
    if (want === "snap")   ok = armed > 0 && m.sigils.some(g =>
                                 g.t >= g.arm && g.t < g.arm + 0.10);
    if (want === "armed")  ok = armed > 0 && arming === 0 && after === before
                                && m.sigils.some(g => g.t > g.arm + 1.0);
    if (want === "both")   ok = arming > 0 && armed > 0;
    if (want === "chain")  ok = after < before && after > 0
                                && m.sigils.some(g => g.ch.some(c => c.dead)
                                                   && g.ch.some(c => !c.dead));
    if (ok){
      AC.__draw(m);
      /* THE PIXELS COME BACK IN THIS SAME JS TURN, and that is not tidiness.
         The composited frame lives in a drawing buffer that is gone by the
         time an out-of-process screenshot asks for it -- the first cut of
         this tool used `locator("#cv").screenshot()` and got a near-black
         canvas with ghosts of the balls in it. `cinema_clip` reads
         `toDataURL` one line after `__draw` for exactly this reason. */
      return { t: +m.t.toFixed(2), figures: m.sigils.length, live: after,
               arming: m.sigils.filter(g => g.t < g.arm).length,
               armed: m.sigils.filter(g => g.t >= g.arm).length,
               png: document.getElementById("cv").toDataURL("image/png") };
    }
  }
  return null;
}"""

PANELS = [
    ("arming", "ARMING — incomplete, flickering, dim, and the crackle is"
               " unattached"),
    ("snap",   "THE SNAP — the frame it goes live"),
    ("armed",  "ARMED — complete, still, and every live charge carries a lamp"
               " at its own trigger radius"),
    ("both",   "BOTH AT ONCE — which is the state the hall is usually in"),
    ("chain",  "COMING APART — a spent point takes its two lines with it, so"
               " what is left on the floor is what is left to walk into"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--foe", default="bulwarden")
    ap.add_argument("--seed", type=int, default=3358)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="../05-reference/v54/deadfall-states")
    A = ap.parse_args()

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    path = resolve_game(A.game)
    print(f"\nDEADFALL — the two states, off a real match\n  game {path.name}")
    print(f"  nightfell vs {A.foe}, seed {A.seed}")

    with game(game_path=path) as (page, errors):
        for want, caption in PANELS:
            r = page.evaluate(SEEK_JS, [A.foe, A.seed, want, A.secs])
            if not r:
                print(f"  --    {want:<7} NOT REACHED in {A.secs:g}s")
                continue
            p = out.parent / f"{out.name}-{want}.png"
            p.write_bytes(base64.b64decode(r.pop("png").split(",", 1)[1]))
            print(f"  ok    {want:<7} t={r['t']:>6}s  "
                  f"{r['arming']} arming / {r['armed']} armed, "
                  f"{r['live']} charges live   -> {p.name}")
            print(f"        {caption}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
