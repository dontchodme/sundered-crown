#!/usr/bin/env python3
"""WHERE THE STAR SITS IN THE RING -- four seats, off one real frame. v66.

    python corona_star_sheet.py --game ../02-chain/sc-corona-fx.html

Rick, 2026-09-03: *"the star should live within the ring. not the ball."*
His section 1 always said so -- "an elliptical ring of neon light WITH A SMALL
GAP LEFT FOR a large star in the middle" -- and where in the ring the break
goes is his, not this session's (rule 2, and the ult animations are one of the
seven).

SHAPE QUESTIONS GO TO A SHEET; SCALE QUESTIONS NEED THE VIDEO. v53 spent three
rounds guessing a hand's size off still frames and settled it in one round trip
once Rick had a video -- and settled every SHAPE question in one round trip off
a sheet. This is a placement question, so it is a sheet.

FOUR SEATS, and the fourth is a control that should read WORSE:

    0        the end of the major axis -- 108 units out, and the only one of
             the four that cannot be confused with the ball
    pi/2     the front of the minor axis -- 42 out against a ball radius of 34,
             so it overlaps the shell
    pi       the far end of the major axis, the mirror of the first
    -pi/2    the BACK of the minor axis, where the star is drawn behind the
             ball. If this one reads fine the sheet is not measuring anything.

ONE FRAME, FOUR DRAWS. Every panel is the same match at the same instant with
one number changed, so what differs between them is the seat and nothing else.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "starwarden"

SHEET_JS = r"""([rid, foe, seed, secs, seats, labels]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid);
  const saved = { at: W.ult.starAt, r: W.ult.starR };
  /* THE FRAME IS A REAL ONE. A posed fighter at the centre of an empty hall
     would flatter every seat equally -- what has to be judged is the star
     against the arena, the health ring, the other fighter and whatever the
     bloom does to all of it. */
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    if (me.ultCorona && !me.ultCorona.popped && me.ultCorona.t > 0.6) break;
  }
  if (!me.ultCorona) return { ok: false };
  const R = AC.renderer, savedCtx = R.ctx;
  const PW = 420, PH = 620, COLS = seats.length;
  const cv = document.createElement("canvas");
  cv.width = PW * COLS; cv.height = PH + 34;
  const g = cv.getContext("2d");
  g.fillStyle = "#07050B";
  g.fillRect(0, 0, cv.width, cv.height);
  const panel = document.createElement("canvas");
  panel.width = 540; panel.height = 960;
  const pc = panel.getContext("2d");
  for (let i = 0; i < seats.length; i++){
    W.ult.starAt = seats[i];
    pc.save();
    pc.fillStyle = "#0B0710";
    pc.fillRect(0, 0, panel.width, panel.height);
    pc.restore();
    R.ctx = pc;
    R.drawArena(m);
    R.drawCorona(m, false);
    R.drawFighter(m, m.b);
    R.drawFighter(m, m.a);
    R.drawCorona(m, true);
    R.ctx = savedCtx;
    /* CROPPED ON THE CASTER, because the question is about an object 26px
       across and a whole 540x960 arena shrunk into a panel would answer a
       different one. */
    const cw = 420, ch = 620;
    const sx = Math.max(0, Math.min(panel.width - cw, me.x - cw / 2));
    const sy = Math.max(0, Math.min(panel.height - ch, me.y - ch / 2));
    g.drawImage(panel, sx, sy, cw, ch, i * PW, 34, PW, PH);
    g.save();
    g.fillStyle = "#EDE3D0";
    g.font = "600 17px monospace";
    g.fillText(labels[i], i * PW + 12, 23);
    g.strokeStyle = "#2A2233"; g.lineWidth = 1;
    g.strokeRect(i * PW + 0.5, 34.5, PW - 1, PH - 1);
    g.restore();
  }
  W.ult.starAt = saved.at; W.ult.starR = saved.r;
  R.ctx = savedCtx;
  return { ok: true, png: cv.toDataURL("image/png"),
           t: me.ultCorona.t, x: me.x, y: me.y };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--a", default=RID)
    ap.add_argument("--b", default="gravemourn")
    ap.add_argument("--seed", type=int, default=33138)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../05-reference/v66/corona-star-seats.png")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    import math
    seats = [0.0, math.pi / 2, math.pi, -math.pi / 2]
    labels = ["A  starAt 0      major axis, 108 out",
              "B  starAt pi/2   minor axis, 42 out",
              "C  starAt pi     major axis, far side",
              "D  starAt -pi/2  BEHIND the ball"]
    out = (pathlib.Path(__file__).parent / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nWHERE THE STAR SITS - four seats off one frame of "
          f"{a.a} vs {a.b}, seed {a.seed}\n")
    with game(game_path=gp) as (page, errors):
        r = page.evaluate(SHEET_JS, [a.a, a.b, a.seed, a.secs, seats, labels])
        assert not errors, errors[:3]
        if not r.get("ok"):
            print("  no window reached in this fight -- try another seed")
            return 1
        png = base64.b64decode(r["png"].split(",", 1)[1])
        out.write_bytes(png)
        print(f"  frame at t={r['t']:.2f}s into the window, "
              f"caster at ({r['x']:.0f}, {r['y']:.0f})")
        for lab in labels:
            print(f"    {lab}")
        print(f"\n  wrote {out}  {len(png) / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
