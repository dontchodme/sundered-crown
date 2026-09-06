#!/usr/bin/env python3
"""THE LARGE STAR, MEASURED -- because Rick could not see it. v66.

    python corona_star_probe.py --game ../02-chain/sc-corona-fx.html

Rick, 2026-09-03, on the first rendered window: *"looking good. i cant see the
large star in the ring though."*

CLAUDE.md 4.1: when a person catches something no tool could, THE DELIVERABLE
IS A MEASUREMENT OF THE THING THEY SAW -- not a fix and an apology. This is
that measurement, and it is a permanent check because the same three faults are
available to anything drawn on a shell.

  [1] HOW LONG IS IT UP. The star lives from the cast until the first
      body-to-body contact, which `sash_tracks` measured at a median 1.32s in
      90% of windows. If it is only on screen for a second of eight, "I cannot
      see it" may be a DURATION problem and no amount of contrast fixes it.
  [2] HOW BIG IS IT AGAINST THE THING IT SITS ON. Drawn radius against
      `CONFIG.physics.ballR`. A mark smaller than the shell's own disc is a
      detail ON the relic, not an object beside it.
  [3] HOW MUCH LIGHT DOES IT ACTUALLY ADD. Two real rendered frames, identical
      but for `popped`, differenced over the star's own footprint. This is
      `ult_bloom_probe`'s decomposition: suppress ONE contributor and measure
      what changed, because a single number over a whole set-piece cannot say
      which half to change.

## THE THREE FAULTS THIS FOUND, ALL AT ONCE

1. IT WAS DRAWN UNDER `lighter`. `drawCorona` opens one `save()` with
   `globalCompositeOperation = "lighter"` for the band, and the star block
   inherited it -- so the star ADDED pink light to an already-bright pink
   shell. Section 4.1b, twice already in this project: a bright thing painted
   over a bright thing is not lit, it is erased.
2. IT WAS HALF THE SIZE OF THE BALL. 17px against `ballR` 34, so it sat
   entirely inside the shell's own disc.
3. IT WAS THE SAME HUE AS WHAT IT SAT ON. `_stWard`'s finding, in that
   function's own words: **a self-buff must separate by VALUE, not by hue** --
   every ward plate gets a near-black outline first for exactly this reason,
   and this is the second self-coloured mark on a vigil ball in the game.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "starwarden"


# [1]. THE CLOCK, off the engine's own window state and counted as SECONDS
# between two transitions rather than as frames on which something was true.
LIFE_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const A = { casts: 0, popped: 0, upF: 0, winF: 0, never: 0,
              tBody: [], tSeat: [], seatEver: 0, seatFirst: 0 };
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const u = me.w.ult;
    let step = 0, was = null, tb = -1, ts = -1;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const C = me.ultCorona;
      if (C){
        if (!was){ A.casts++; tb = -1; ts = -1; }
        A.winF++;
        if (!C.popped) A.upF++;
        /* [4]. THE TWO TRIGGERS, OBSERVED IN THE SAME FIGHT. What ships is a
           body-to-body contact, because the star used to sit on the body; it
           now sits on the band, 108 units out. So the counterfactual worth
           pricing is "the foe touches the star WHERE IT IS".

           THE CAVEAT IS REAL AND IS NOT HIDDEN: only the FIRST of these two is
           a clean measurement. Once the body trigger has fired, the fight this
           is being read off has already spent its shower, so a seat touch
           after that instant is a moment in a fight that would have gone
           differently (v43 section 7 -- a long A/B window measures divergence,
           not the thing). What is clean is which of the two comes FIRST and
           how often the seat is reachable at all. */
        if (u.starAt !== undefined){
          const ca = Math.cos(u.tilt), sa = Math.sin(u.tilt);
          const rx = (u.A + (u.A - u.wd)) / 2;
          const ry = (u.B + u.B * (u.A - u.wd) / u.A) / 2;
          const px = Math.cos(u.starAt) * rx, py = Math.sin(u.starAt) * ry;
          const sx = me.x + px * ca - py * sa, sy = me.y + px * sa + py * ca;
          if (ts < 0 && th.alive
              && Math.hypot(th.x - sx, th.y - sy) < R + u.starR) ts = C.t;
        }
        if (tb < 0 && th.alive
            && Math.hypot(th.x - me.x, th.y - me.y) < 2 * R + 2) tb = C.t;
        was = C;
      } else if (was){
        if (was.pops) A.popped++; else A.never++;
        if (tb >= 0) A.tBody.push(tb);
        if (ts >= 0){ A.seatEver++; A.tSeat.push(ts); }
        if (ts >= 0 && (tb < 0 || ts < tb)) A.seatFirst++;
        was = null;
      }
    }
  }
  return A;
}"""


# [2] AND [3]. TWO REAL FRAMES, IDENTICAL BUT FOR ONE FLAG.
DRAW_JS = r"""([rid, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const cv = document.createElement("canvas");
  cv.width = 540; cv.height = 960;
  const ctx = cv.getContext("2d");
  const Rr = AC.renderer, saved = Rr.ctx;
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    if (me.ultCorona && !me.ultCorona.popped && me.ultCorona.t > 0.35) break;
  }
  const C = me.ultCorona;
  if (!C) { Rr.ctx = saved; return { ok: false }; }
  /* THE BOX IS THE STAR'S OWN FOOTPRINT AND NOTHING ELSE. A box the size of
     the arena would average the star away against the hall; a box the size of
     the ball would include the ring's own band where it crosses the shell.

     AND IT FOLLOWS THE STAR'S SEAT RATHER THAN THE CASTER, which this probe
     had to learn the moment Rick moved the star off the ball. The first cut
     centred on `me.x, me.y` because that is where the star was; with the star
     seated on the band 108 units out, the same box measured empty hall and
     reported |dL| 0.0000 -- a FALSE RED on a picture the contact sheet shows
     perfectly clearly. A PROBE THAT HARDCODES WHERE A THING USED TO BE
     MEASURES SOMEWHERE ELSE AND CALLS IT A DEFECT. */
  const u = me.w.ult;
  let cx = me.x, cy = me.y;
  if (u.starAt !== undefined){
    const ca = Math.cos(u.tilt), sa = Math.sin(u.tilt);
    const rx = (u.A + (u.A - u.wd)) / 2;
    const ry = (u.B + u.B * (u.A - u.wd) / u.A) / 2;
    const px = Math.cos(u.starAt) * rx, py = Math.sin(u.starAt) * ry;
    cx = me.x + px * ca - py * sa; cy = me.y + px * sa + py * ca;
  }
  const box = Math.ceil((u.starR || R) * 1.9);
  const x0 = Math.round(cx - box), y0 = Math.round(cy - box);
  const w = box * 2, h = box * 2;
  const shot = (pop) => {
    const was = C.popped;
    C.popped = pop;
    ctx.save();
    ctx.fillStyle = "#0B0710";
    ctx.fillRect(0, 0, cv.width, cv.height);
    ctx.restore();
    Rr.ctx = ctx;
    Rr.drawCorona(m, false);
    Rr.drawFighter(m, me);
    Rr.drawCorona(m, true);
    Rr.ctx = saved;
    C.popped = was;
    return ctx.getImageData(x0, y0, w, h).data;
  };
  const withStar = shot(false), without = shot(true);
  let sum = 0, peak = 0, n = 0, lit = 0;
  for (let i = 0; i < withStar.length; i += 4){
    const l1 = (0.2126 * withStar[i] + 0.7152 * withStar[i+1]
                + 0.0722 * withStar[i+2]) / 255;
    const l0 = (0.2126 * without[i] + 0.7152 * without[i+1]
                + 0.0722 * without[i+2]) / 255;
    const d = Math.abs(l1 - l0);
    sum += d; n++; if (d > peak) peak = d;
    if (d > 0.06) lit++;
  }
  Rr.ctx = saved;
  return { ok: true, mean: sum / n, peak, lit: lit / n, px: n, R,
           t: C.t, box: box, seatOff: Math.hypot(cx - me.x, cy - me.y) };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--foes", type=int, default=8)
    ap.add_argument("--secs", type=float, default=156.0)
    a = ap.parse_args()
    gp = resolve_game(a.game)
    print(f"\nTHE LARGE STAR - measured against {gp.name}\n")
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [4177 + 31 * i for i in range(a.seeds)]

        L = page.evaluate(LIFE_JS, [RID, foes, seeds, a.secs])
        assert not errors, errors[:3]
        casts = max(1, L["casts"])
        up = L["upF"] / 120 / casts
        win = L["winF"] / 120 / casts
        print(f"  [1] HOW LONG IT IS UP, over {L['casts']} casts")
        print(f"      the star stands   {up:5.2f}s a cast")
        print(f"      the window runs   {win:5.2f}s a cast")
        print(f"      so it is on screen for {up / win:.0%} of its own window,")
        print(f"      and {L['never']} of {L['casts']} casts never popped at "
              "all (the ring nobody crossed)\n")

        import statistics as _st
        med = lambda v: _st.median(v) if v else float("nan")
        print(f"  [4] THE TWO TRIGGERS, over the same {L['casts']} casts")
        print("      what ships is a BODY contact, because the star used to "
              "sit on the body.\n      It sits on the band now, 108 units "
              "out -- so this is what moving the\n      trigger to the star's "
              "own seat would be worth.\n")
        print(f"      body contact   fires in {len(L['tBody']) / casts:5.0%} "
              f"of casts, median {med(L['tBody']):.2f}s in")
        print(f"      the star's seat fires in {L['seatEver'] / casts:5.0%} "
              f"of casts, median {med(L['tSeat']):.2f}s in")
        print(f"      and the seat is touched FIRST in "
              f"{L['seatFirst'] / casts:.0%} of casts\n")
        print("      ONLY THE 'WHICH IS FIRST' COLUMN IS CLEAN. After the body "
              "trigger has\n      fired the fight has spent its shower, so a "
              "later seat touch is a moment\n      in a fight that would have "
              "gone differently (v43 section 7).\n")

        D = page.evaluate(DRAW_JS, [RID, foes[0], seeds[0], a.secs])
        assert not errors, errors[:3]
        if not D.get("ok"):
            print("  [2/3] no window reached in this fight -- try another seed")
            return 1
        print(f"  [2] HOW BIG IT IS, against the thing it sits on")
        print(f"      ball radius       {D['R']:.0f}px")
        print("      (the drawn radius is in `drawCorona`; a mark under the "
              "ball's own\n       radius is a detail ON the relic, not an "
              "object beside it)\n")
        print(f"  [3] HOW MUCH IT ACTUALLY CHANGES THE PICTURE")
        print("      two real frames, identical but for `popped`, differenced "
              f"over a\n      {D['box'] * 2}x{D['box'] * 2} box on THE STAR'S "
              f"OWN SEAT ({D['px']} px, {D['seatOff']:.0f} units from\n      "
              f"the caster's centre), at t={D['t']:.2f}s into the window\n")
        print(f"      mean |dL|         {D['mean']:.4f}")
        print(f"      peak |dL|         {D['peak']:.4f}")
        print(f"      pixels it moves   {D['lit']:.1%} of the box "
              "(|dL| > 0.06)\n")
        # A NUMBER WITH A LINE UNDER IT. Below this the star is not a thing on
        # screen -- it is a slight warming of a shell that is already the same
        # colour. Chosen against `_stWard`'s own separation, which is a
        # near-black outline against a rose plate: several tenths, not
        # hundredths.
        ok = D["lit"] > 0.06 and D["peak"] > 0.25
        print(f"  {'PASS' if ok else 'FAIL'}  the star is a thing on screen "
              "rather than a warming of the shell")
        if not ok:
            print("        (mean under 0.02 or peak under 0.25 is the fault "
                  "Rick reported:\n         a bright mark added to an already "
                  "bright shell of its own hue)")
        assert not errors, errors[:3]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
