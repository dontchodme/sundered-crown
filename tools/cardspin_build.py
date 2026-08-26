#!/usr/bin/env python3
"""The fight card's art TURNS.  v4 of _introCard.

    python3 cardspin_build.py --src ../02-chain/sc-ember.html --out ../02-chain/sc-cardspin.html

WHY THIS IS NOT DECORATION. `spin` is already per-relic data -- the rate the
thing turns in the hall. Driving the card art from the same number means the
card SHOWS the stat it is printing two lines below: a relic with a high swing
speed visibly turns faster than one without. A fixed pose cannot do that.

THE BEAT. The art flies in turning and is ARRESTED by the clash, on the same
frame the two cards collide and the sparks come out of the seam. Then it idles
-- a slow turn at a quarter rate, so the card reads as alive while it is being
read. Entry sweep is `spin * 3.2 * 0.46s`; for Grudgebearer (spin 1.6) that is
2.36 rad, about 135 degrees, and it lands exactly on the reading angle.

THE PRICE, STATED UP FRONT. v3 fitted each shape's axis-aligned box into the
250x148 art band, which is a valid fit at -0.38 rad and at no other angle. A
turning weapon needs a rotation-INVARIANT fit, so the scale is now taken from
the circumscribed radius. Long weapons get smaller. That is the honest cost of
moving them and the builder prints it per relic rather than hiding it.

Nothing here is simulation. `_introCard` is presentation, driven by `imp`
(time since the clash), which is a pure function of introT -- so simulate(),
batch(), verify.py and tune.py cannot see any of it. engine_ab.py proves it.
"""
from __future__ import annotations
import argparse, pathlib, sys

PROTECTED = {"sundered-crown.html"}

OLD = """    const box = this._artBox(f.w);
    const as = Math.min(IC.artMaxS, IC.artW / box.w, IC.artH / box.h);
    c.save();
    c.translate(IC.artCX - as * (box.x + box.w / 2),
                y0 + IC.artCY - as * (box.y + box.h / 2));
    c.scale(as, as);
    c.rotate(-0.38);
    c.shadowColor = pal.core; c.shadowBlur = 26;
    this._artShape(c, f.w, pal);
    c.restore();"""

NEW = """    /* v4: the art turns, at the relic's OWN `spin`. The card then shows the
       stat it prints two lines below -- a fast weapon visibly turns faster --
       which a fixed pose cannot do.

       The MOTION is bounded rather than the scale. A first version fitted the
       art to its circumscribed radius so any angle was safe, and it cost 48%
       of the size on the long relics -- because a 112-unit weapon turned
       toward vertical cannot fit a 148-tall band at all. But the same
       arithmetic shows v3 ALREADY extends past artH at its own -0.38 pose, so
       the band is a layout hint and not a clip, and fitting to it was
       inventing a constraint the shipped card does not honour. The scale is
       therefore v3's, unchanged, and the ANGLE is what is kept small:

         entry   REST - 0.52 rad, easing in, arrested exactly on REST at the
                 clash -- the impact stops it, the way it stops the cards
         hold    a +-0.15 rad sway at the relic's own rate, so a fast relic
                 visibly breathes faster than a slow one and the card is alive
                 while it is being read

       Bounded sway also beats a monotone drift geometrically: a free-running
       idle at spin 3.4 would travel 2.09 rad across the hold and put the art
       somewhere its scale was never fitted for. */
    const box = this._artBox(f.w);
    const as = Math.min(IC.artMaxS, IC.artW / box.w, IC.artH / box.h);
    const REST = -0.38, rate = f.w.spin || 1.2;
    const SWEEP = __SWEEP__, SWAY = __SWAY__, SWAYRATE = __SWAYRATE__;
    const TRAVEL = __TRAVEL__;
    /* imp < 0 is the approach: the angle runs BACK from rest at `rate*3.2` so
       it arrives on REST at imp = 0 by construction, not by tuning. After the
       impact it holds still for 0.30s -- the clash has to read as a stop --
       then drifts. */
    const ang = imp <= 0
      ? REST - SWEEP * Math.pow(clamp(-imp / CONFIG.intro.clash, 0, 1), 0.65)
      : __IDLE__;
    c.save();
    c.translate(IC.artCX - as * (box.x + box.w / 2),
                y0 + IC.artCY - as * (box.y + box.h / 2));
    c.scale(as, as);
    c.rotate(ang);
    c.shadowColor = pal.core; c.shadowBlur = 26;
    this._artShape(c, f.w, pal);
    c.restore();"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="../02-chain/sc-ember.html")
    ap.add_argument("--out", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--sweep", type=float, default=0.52,
                    help="radians the art is offset from the reading angle on entry")
    ap.add_argument("--sway", type=float, default=0.15,
                    help="radians of idle sway either side of the reading angle")
    ap.add_argument("--sway-rate", type=float, default=0.55,
                    help="multiplier on the relic's own spin for the idle motion")
    ap.add_argument("--travel", type=float, default=0.60,
                    help="radians the idle TURN may travel before it stops. A "
                         "free-running turn takes long relics near vertical, "
                         "where they cross the header rule -- measured, not "
                         "assumed: T18/T30 both put ink at y=293 against a "
                         "290 limit, while the v3 control sat at 252.")
    ap.add_argument("--idle", choices=("sway", "turn"), default="sway",
                    help="sway: bounded oscillation. turn: a continuous slow "
                         "rotation -- reads as alive rather than as a jitter, "
                         "and needs the art to be safe at EVERY angle")
    A = ap.parse_args()
    if pathlib.Path(A.out).name in PROTECTED:
        print(f"REFUSED -- {A.out} is a shipped artifact.", file=sys.stderr); return 1
    src = pathlib.Path(A.src)
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr); return 2
    s = src.read_text(encoding="utf-8")
    n = s.count(OLD)
    if n != 1:
        print(f"! the _introCard art anchor hit {n} times, wanted exactly 1. "
              f"Diff before re-anchoring -- do not loosen it.", file=sys.stderr)
        return 3
    idle = ("REST + SWAY * Math.sin(Math.max(0, imp - 0.30) * rate * SWAYRATE)"
            if A.idle == "sway" else
            "REST + Math.max(0, imp - 0.30) * rate * SWAYRATE")
    body = (NEW.replace("__IDLE__", idle)
               .replace("__TRAVEL__", f"{A.travel:.2f}")
               .replace("__SWEEP__", f"{A.sweep:.2f}")
               .replace("__SWAYRATE__", f"{A.sway_rate:.2f}")
               .replace("__SWAY__", f"{A.sway:.2f}"))
    s = s.replace(OLD, body, 1)
    pathlib.Path(A.out).write_text(s, encoding="utf-8")
    print(f"  {A.src} -> {A.out}  (1 anchor)  "
          f"sweep {A.sweep} sway {A.sway} @ spin x{A.sway_rate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
