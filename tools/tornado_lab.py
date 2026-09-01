#!/usr/bin/env python3
"""HOW LONG SHOULD A TORNADO CAST RUN? Measured, not guessed.

Rick chose a DURATION over a fixed count (2026-09-01), which makes delivered
damage variable: the cast is worth whatever the tornado happens to catch. The
budget is 100 damage at ~5 a tick, so the question "how many seconds" is really
"how many seconds buys 20 ticks of contact".

Vertical occupancy alone (v62 §1) says a fighter is below y=600 for 37.8% of a
fight. That is an OVERESTIMATE of contact, because the tornado is also narrow:
it has to be in the same PLACE, not just at the same height. This replays real
fights and sweeps a moving band through them.

WHAT THIS DOES NOT MODEL, declared: the tornado's own drag moves the fighter it
catches, and a caught fighter is held rather than free. So this measures the
rate at which a PASSIVE tornado would first make contact, which sets how often
a hold STARTS -- not how long one lasts. Contact once started is the hold, and
the hold is capped by the tick budget.

CONTROL THAT CAN FAIL: a band spanning the whole arena must return exactly the
vertical occupancy of the SAME tracks under the SAME edge rule. A sweep that
disagrees with a no-sweep measurement of its own data has broken geometry.

THE FIRST VERSION OF THIS CONTROL FAILED AND WAS RIGHT TO. It compared an
edge-rule sweep (ball touches the band when its RIM crosses y=600) against
v62 s1's centre-rule histogram (ball counted when its CENTRE crosses y=600).
Ball radius is 34, so the two rules differ by 34px of arena and the sweep came
back 51.5% against the histogram's 37.8%. Both numbers were right and the
comparison was not. Contact uses the edge rule -- a tornado catches a ball it
touches -- and the control now compares like with like.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=8)
ap.add_argument("--out", default="/tmp/tornado_lab.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, sample]) => {
  const DT = AC.CONFIG.physics.dt;
  const tracks = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    const xs = [], ys = [];
    let step = 0, acc = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++; acc += DT;
      if (acc >= sample){ acc = 0; xs.push(foe.x); ys.push(foe.y); }
    }
    tracks.push({ xs, ys, dur: step * DT });
  }
  return { tracks, arena: AC.CONFIG.arena, ballR: AC.CONFIG.physics.ballR };
}"""

HERE = pathlib.Path(__file__).parent
with game(game_path=(HERE / a.game).resolve() if not pathlib.Path(a.game).is_absolute()
          else pathlib.Path(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [8101 + 29*i for i in range(a.seeds)]
    SAMPLE = 0.05
    t0 = time.time()
    r = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, SAMPLE])
    assert not errors, errors[:3]
    tracks, W, H, R = r["tracks"], r["arena"]["w"], r["arena"]["h"], r["ballR"]

def contact(width, speed, top, tracks, sample=SAMPLE):
    """Band of `width` sweeping x at `speed` px/s, reversing at the walls,
    occupying y from `top` to the floor. Returns fraction of samples inside."""
    hit = tot = 0
    span = W - width
    for tr in tracks:
        for i, (x, y) in enumerate(zip(tr["xs"], tr["ys"])):
            t = i * sample
            if span <= 0:
                cx = W / 2
            else:
                # triangle wave: sweep across and back
                period = 2 * span / speed
                ph = (t % period) * speed
                cx = ph if ph <= span else 2 * span - ph
                cx += width / 2
            tot += 1
            if y + R >= top and abs(x - cx) <= width / 2 + R:
                hit += 1
    return hit / max(tot, 1)


def vertical_only(top, tracks, edge=True, sample=SAMPLE):
    """Occupancy of the height band alone, no sweep. The control's other half."""
    hit = tot = 0
    for tr in tracks:
        for y in tr["ys"]:
            tot += 1
            if (y + R >= top) if edge else (y >= top):
                hit += 1
    return hit / max(tot, 1)

print(f"\nTORNADO CONTACT — {len(tracks)} fights, foe position sampled every {SAMPLE}s")
print(f"arena {W}x{H}, ball r={R}, tornado top at y=600 (the 'third of the arena' height)\n")
ctl = contact(W, 200, 600, tracks)
vedge = vertical_only(600, tracks, edge=True)
vctr = vertical_only(600, tracks, edge=False)
print(f"    CONTROL — full-width sweep {ctl:.1%}  vs  no-sweep, same edge rule {vedge:.1%}")
print(f"    {'PASS — geometry agrees with itself' if abs(ctl - vedge) < 0.015 else 'FAIL — sweep geometry is wrong'}")
print(f"    for reference, the CENTRE rule on the same tracks: {vctr:.1%} "
      f"(v62 s1's histogram measured 37.8% this way, on both fighters)\n")
print(f"    {'width':>7}{'sweep px/s':>12}{'contact':>10}{'s of contact per 10s cast':>27}"
      f"{'ticks @4.5/s':>14}{'damage @5':>11}")
best = []
for width in (90, 120, 160, 200):
    for speed in (120, 200, 300):
        c = contact(width, speed, 600, tracks)
        secs10 = c * 10
        ticks = secs10 * 4.5
        print(f"    {width:>7}{speed:>12}{c:>9.1%}{secs10:>26.2f}{ticks:>14.1f}{ticks*5:>11.0f}")
        best.append((width, speed, c))
print()
print(f"    {'cast length needed for the full 20-tick / 100-damage budget':<62}")
print(f"    {'width':>7}{'sweep':>8}{'contact':>10}{'seconds to bank 20 ticks':>27}")
for width, speed, c in best:
    need = (20 / 4.5) / max(c, 1e-9)
    flag = "  <- longer than most fights allow" if need > 30 else ("  <- clean" if need <= 16 else "")
    print(f"    {width:>7}{speed:>8}{c:>9.1%}{need:>26.1f}{flag}")
json.dump({"control": ctl, "grid": best}, open(a.out, "w"), indent=1)
print(f"\n    {len(tracks)} fights in {time.time()-t0:.0f}s   errors: {errors}")
