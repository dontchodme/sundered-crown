#!/usr/bin/env python3
"""DUSKREAVE / SCOUR, PRICED THE WAY EVERY OTHER RELIC IN THIS PROJECT IS PRICED.

v63 correction to `duskreave_config.py` (v62). That tool grafted umbral curse and
a 21 blade onto the scythe donor (Thornwake) and left the donor's own ultimate,
BRAMBLESNARE (a 1.6s root, 10 damage, 3 Entangle), LIVE IN EVERY ARM. So v62's
"no ultimate" arm was really "Bramblesnare", and its "SCOUR" arm was
"Bramblesnare AND Scour". Every other design lab in the repo -- spectre_lab,
wire_lab, quiver_lab, row_price, cell_ults_on -- sets the donor's charge to 1e9
so the cell has no ultimate but the one being designed. This one does too.

    --donor-ult off    (default) the donor's Bramblesnare never fires. The
                       number this produces is comparable to Crossweave's
                       +48.8 and to cell_ults_on's floors.
    --donor-ult live   v62's exact arms, for reproduction. Should print
                       26.6% / 82.4% / +55.8pp on Chromium 141.0.7390.37.

The tornado model is otherwise UNCHANGED from v62 -- `hurt` plus a hand-computed
echo, two 10s windows pinned at t=12 and t=30, 160 wide, top at y=600, 200 px/s
sweep. Its limitations are v62 HANDOFF s6 and they still hold: no crit, no
jitter, no Sunder, no Aegis, no hit-stop, no hit-stun, and the drag does not
move the ball.

CONTROLS THAT CAN FAIL
  1. `--donor-ult live` must reproduce v62's 26.6 / 82.4 / +55.8 exactly. The
     engine is deterministic and the Chromium is the same; anything else means
     the tool or the build has moved.
  2. With the donor's ultimate off, the no-ult floor must land within the
     ~4.3pp error bar of cell_ults_on's FIELD-ULTS-ON floor for umbral x scythe
     at blade 31.35 (39.0%) ADJUSTED for the lighter blade -- i.e. it must be
     LOWER than 39.0%, and lower than the live-Bramblesnare floor.

Runs from `tools/` with `python` or `py`. Paths are repo-relative.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from scpage import game, resolve_game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=34)
ap.add_argument("--donor-ult", choices=["off", "live"], default="off")
ap.add_argument("--blade", type=float, default=21.0)
ap.add_argument("--rate", type=float, default=7.0)
ap.add_argument("--base", type=float, default=5.0)
ap.add_argument("--width", type=float, default=160.0)
ap.add_argument("--curse-rule", choices=["top3", "fifo"], default="top3",
                help="top3 = shipped rule (keep the 3 biggest). fifo = the rolling window Rick proposed (keep the last 3), installed at runtime exactly as tornado_fifo.py installs it")
ap.add_argument("--out", default=None)
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, blade, base, on, apply_, windows, rate, width, top, speed, donorUltOff]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.CONFIG.arena.w, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg, charge: w.ult ? w.ult.charge : null,
                  onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral"; w.dmg = blade; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  if (donorUltOff && w.ult) w.ult.charge = 1e9;
  const span = W - width, period = 2 * span / speed;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    let step = 0, nextTick = 0, ticks = 0, baseSum = 0, echoSum = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (!on || !foe.alive || m.over) continue;
      if (!windows.some(([s, e]) => t >= s && t < e) || t < nextTick) continue;
      nextTick = t + 1 / rate;
      const ph = ((t - windows[0][0]) % period) * speed;
      const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
      if (!((foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R))) continue;
      const echo = Math.round(foe.curseEcho());
      const b = Math.round(base);
      m.hurt(foe, b + echo, me); me.dealt += b + echo; me.hits++;
      if (apply_){ foe.pushCurse(b, 1); foe.apply("curse", 1); }
      ticks++; baseSum += b; echoSum += echo;
    }
    out.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1, ticks,
               baseSum, echoSum, dur: step * DT, dealt: me.dealt, hits: me.hits,
               donorCasts: me.ultsFired || 0 });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  if (saved.charge !== null) w.ult.charge = saved.charge;
  return out;
}"""

INSTALL = r"""(mode) => {
  const m0 = new AC.Match(AC.WEAPONS[0].id, AC.WEAPONS[1].id, 1);
  const P = Object.getPrototypeOf(m0.a);
  if (!P.__origPush) P.__origPush = P.pushCurse;
  const MAX = AC.STATUS.curse.maxStacks;
  if (mode === "fifo"){
    P.pushCurse = function(v, n){
      for (let i = 0; i < n; i++) this.cursePool.push(v);
      while (this.cursePool.length > MAX) this.cursePool.shift();
    };
  } else { P.pushCurse = P.__origPush; }
  return mode;
}"""

def wr(rs): return statistics.mean([r["win"] for r in rs if r["win"] >= 0])

with game(game_path=resolve_game(a.game)) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent")
    page.evaluate(INSTALL, a.curse_rule)
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != "thornwake"]
    seeds = [16001 + 67*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    off = a.donor_ult == "off"
    t0 = time.time()
    print(f"\nDUSKREAVE / SCOUR — blade {a.blade:g}, {a.rate:g} ticks/s, base {a.base:g}, "
          f"{a.width:g} wide, 10s casts")
    print(f"build {a.game}   {len(ids)} relics   {ver.split('Chrome/')[1].split(' ')[0] if 'Chrome/' in ver else ver}")
    print(f"CURSE RULE: {'shipped — keep the 3 BIGGEST' if a.curse_rule == 'top3' else 'ROLLING WINDOW — keep the LAST 3 (proposed, not shipped)'}")
    print(f"DONOR'S OWN ULTIMATE (Bramblesnare): {'OFF — charge 1e9 in every arm' if off else 'LIVE in every arm (v62 reproduction)'}")
    print(f"against all {len(foes)} other relics x {a.seeds} seeds = {len(foes)*a.seeds} fights an arm\n")
    res = {}
    for label, on, apply_ in (("no ultimate", False, False),
                              ("SCOUR, ticks apply curse", True, True),
                              ("SCOUR, ticks do not apply", True, False)):
        rs = page.evaluate(JS, ["thornwake", foes, seeds, 120.0, a.blade, a.base, on, apply_,
                                WIN, a.rate, a.width, 600.0, 200.0, off])
        assert not errors, errors[:3]
        res[label] = rs
        tk = statistics.mean([r["ticks"] for r in rs])
        bs = statistics.mean([r["baseSum"] for r in rs])
        es = statistics.mean([r["echoSum"] for r in rs])
        dc = statistics.mean([r["donorCasts"] for r in rs])
        print(f"    {label:<28}{wr(rs):>8.1%}   ticks {tk:>5.1f}   "
              f"base {bs:>6.1f}   echo {es:>6.1f}   total {bs+es:>6.1f}   "
              f"per cast {(bs+es)/2:>6.1f}   donor casts {dc:>4.2f}")
    o, A, B = res["no ultimate"], res["SCOUR, ticks apply curse"], res["SCOUR, ticks do not apply"]
    pair = {(r["foe"], r["seed"]): r for r in o}
    d = [(x, pair[(x["foe"], x["seed"])]) for x in A]
    d = [(x, y) for x, y in d if x["win"] >= 0 and y["win"] >= 0]
    flips = sum(1 for x, y in d if x["win"] != y["win"])
    print(f"\n    SCOUR IS WORTH {(wr(A)-wr(o))*100:+.1f}pp   "
          f"(apply clause {(wr(A)-wr(B))*100:+.1f}pp)   paired flips {flips}/{len(d)}   "
          f"paired SE ~{100*(flips**0.5)/len(d):.1f}pp")
    if not off:
        ok = abs(wr(o)-0.266) < 0.005 and abs(wr(A)-0.824) < 0.005
        print(f"    CONTROL 1 — v62 reproduction 26.6% / 82.4%: {'PASS' if ok else 'FAIL — tool or build has moved'}")
    else:
        print(f"    CONTROL 2 — no-ult floor {wr(o):.1%} must sit below cell_ults_on's 39.0% "
              f"(blade 31.35, no ult): {'PASS' if wr(o) < 0.39 else 'FAIL'}")
    print(f"    for scale: Crossweave +48.8pp (ult_price, own ult on vs off); "
          f"v60 s2 error bar ~4.3pp")
    print(f"\n    {3*len(foes)*a.seeds} fights in {time.time()-t0:.0f}s   errors: {errors}")
    if a.out:
        json.dump({"args": vars(a), "runtime": ver, "res": res}, open(a.out, "w"))
