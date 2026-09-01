#!/usr/bin/env python3
"""THE HAND, AS A SHEET -- reaching against holding against the crush.

    python grasp_sheet.py --out ../05-reference/v56/grasp-states

SHAPE QUESTIONS GO TO A SHEET; SCALE QUESTIONS NEED THE VIDEO (CLAUDE.md §0,
the hand art -- and v53 spent three rounds on Revenant's size because a sheet
shows the object STILL and every size complaint was about it in motion among
two others). This answers the shape questions and does not pretend to answer
the other:

    CAN A VIEWER TELL A REACH FROM A HOLD, AND A HOLD FROM THE CRUSH?
    AND CAN THEY SEE THE FIFTH GRAB COMING BEFORE IT LANDS?

Those are §7b of `06-docs/v56/SHROUDMAUL-BUILD-BRIEF.md`, and they are the
whole ultimate: **it deals no damage, so if the hand does not read, nothing
happened.** There is no number over the ball, no health bar moving and no
hit-stop scaled to a blow.

v54 §2c is the precedent and it nearly shipped broken. Deadfall's ARMING and
ARMED states were separated by alpha alone at 0.16, against a hall that ALREADY
had a gold pentagram on its floor, and photographed off a real match they did
not separate at all -- so sigils appeared already live and the arming beat did
not exist on screen. No probe in this repo could have said so.

It drives a REAL match -- no posed objects -- to the first frame that satisfies
each panel's own predicate, and photographs the canvas the game draws.
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
     this one between the draw and the shutter -- `deadfall_sheet` photographed
     a fight nobody asked for before this flag was set. The demo panel is a DOM
     overlay, so hiding it is separate. */
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  window.__m = m;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    const G = me.ultGrasp, C = me.graspCrush, u = me.w.ult;
    const d = Math.hypot(th.x - me.x, th.y - me.y);
    let ok = false;
    /* REACHING, DRAWN BACK -- AND IT IS A 0.1s STATE, WHICH IS A FINDING.
       `grabStun` is 0.5 and `cadence` is 0.6, so once the quarry is inside
       `radius` the hand is HOLDING for 83% of the time and the gap between
       one hold ending and the next grab is a tenth of a second. The first cut
       of this predicate asked for a drawn-back hand two thirds of the way
       through the cadence and NEVER FOUND ONE: it is asking for `hold <= 0`
       and `cd > 0.43` at the same time, and those cannot both be true.

       So "reaching" is really two different pictures -- the hand casting
       about while the quarry is OUT of reach (the `reach` panel), and this
       one-tenth-of-a-second flinch between grabs. Both are drawn; only one of
       them is on screen long enough to read. */
    if (want === "drawn")  ok = !!G && G.hold <= 0 && G.grabs > 0
                                && d <= u.radius;
    /* REACHING, EXTENDED. The cadence is nearly up and the hand is at full
       stretch -- the WIND-UP, which is the only warning a grab is coming. */
    if (want === "reach")  ok = !!G && G.hold <= 0 && G.cd < u.cadence * 0.18
                                && d > u.radius * 0.55;
    /* HOLDING. An ordinary grab, mid-hold, with the tether taut. */
    if (want === "hold")   ok = !!G && G.hold > 0 && !C
                                && G.grabs >= 2 && G.grabs <= u.n - 2
                                && G.hold < u.grabStun * 0.72;
    /* THE FOURTH, AND IT IS §7b'S QUESTION. n-1 pips are burning and the next
       grab is the crush. If a viewer cannot see this frame differently from
       the one above, the payoff arrives without having been promised. */
    if (want === "fourth") ok = !!G && G.hold > 0 && !C && G.grabs === u.n - 1;
    /* THE CRUSH. The window is already gone -- `ultGrasp` is nulled on the
       frame the fifth grab lands, which is "then dissipates" -- so this state
       lives entirely on `graspCrush`, the presentation clock. A build drawn
       off `ultGrasp` alone has NO FRAME HERE AT ALL, which is exactly what
       `grasp_relic_probe [P]` found on the first cut. */
    if (want === "crush")  ok = !!C && C.t > 0.5 && C.t < C.life * 0.6;
    /* AND THE LET-GO. */
    if (want === "fade")   ok = !G && !C && me.graspFade > 0.25
                                && me.graspFade < 0.7;
    if (ok){
      AC.__draw(m);
      /* THE PIXELS COME BACK IN THIS SAME JS TURN. The composited frame lives
         in a drawing buffer that is gone by the time an out-of-process
         screenshot asks for it -- `deadfall_sheet` got a near-black canvas
         with ghosts of the balls in it before this was moved inline. */
      return { t: +m.t.toFixed(2), grabs: G ? G.grabs : u.n,
               windowT: G ? +G.t.toFixed(2) : null,
               crushT: C ? +C.t.toFixed(2) : null,
               fade: +me.graspFade.toFixed(2),
               d: Math.round(d), radius: u.radius,
               png: document.getElementById("cv").toDataURL("image/png") };
    }
  }
  return null;
}"""

PANELS = [
    ("drawn",  "THE FLINCH — the 0.1s between one hold ending and the next"
               " grab. grabStun 0.5 against cadence 0.6 means the hand is"
               " CLOSED 83% of the time once the quarry is in reach"),
    ("reach",  "REACHING, EXTENDED — the cadence is nearly up. This is the only"
               " warning a grab is coming"),
    ("hold",   "HOLDING — closed on the WEAPON, tether taut, ball still"
               " drifting. That is `f.stun` and not `f.pin`, and it is what"
               " the frame has to say"),
    ("fourth", "THE FOURTH — four pips burning, one grab from the crush."
               " §7b: can a viewer see it coming?"),
    ("crush",  "THE CRUSH — the fifth. Bigger, harder shut, and it outlives the"
               " window it ended"),
    ("fade",   "AND IT DISSIPATES"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-grasp.html")
    ap.add_argument("--relic", default="shroudmaul")
    ap.add_argument("--foe", default="emberedge")
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="../05-reference/v56/grasp-states")
    A = ap.parse_args()

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    path = resolve_game(A.game)
    print(f"\nGRASP — the three states, off a real match\n  game {path.name}")
    print(f"  {A.relic} vs {A.foe}, seed {A.seed}\n")

    missed = 0
    with game(game_path=path) as (page, errors):
        for want, caption in PANELS:
            r = page.evaluate(SEEK_JS, [A.relic, A.foe, A.seed, want, A.secs])
            if not r:
                print(f"  --    {want:<7} NOT REACHED in {A.secs:g}s")
                missed += 1
                continue
            p = out.parent / f"{out.name}-{want}.png"
            p.write_bytes(base64.b64decode(r.pop("png").split(",", 1)[1]))
            print(f"  ok    {want:<7} t={r['t']:>6}s  grabs {r['grabs']}  "
                  f"sep {r['d']}/{r['radius']:g}  fade {r['fade']}   -> {p.name}")
            print(f"        {caption}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))
    if missed:
        print(f"\n  {missed} panel(s) never happened in this fight. That is a "
              f"finding if it is\n  the CRUSH — try another seed before "
              f"believing it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
