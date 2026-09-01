#!/usr/bin/env python3
"""A ZERO-DAMAGE HOLD ON THE UMBRAL WARHAMMER — Rick's §1, priced.

    python3 grab_lab.py --game ../02-chain/sc-nightfell.html

§1: *"for a duration the artifact grows an etherial skeletal hand that reaches
out and grabs nearby enemies. the grab does no damage and doesn't apply curse
but it does apply massive hit stun. if it grabs several times in one trigger
(2-6 depending on balance) it true stuns for extra duration and then
dissipates."*

Nothing in this game has a zero-damage ultimate and nothing has a counter that
has to be EARNED inside one window. Both of those are measured here.

Two translations of "massive hit stun", because the engine already draws the
distinction Rick himself asked for:

  STUN   `f.stun` — the weapon is locked, tickHits skips, the head stops
         turning. The BALL keeps moving; `moveMul` floors at 0.45.
  PIN    `f.pin` — `move()` returns on it, so the ball is HELD. Written by
         exactly one relic (Paradox's Stasis Field) and by nothing else.

`takeHitstun` is NOT either of them and cannot be "massive": it caps at
`stunMax` 0.26s and each application shortens the next (`stunDR` 0.55).

  [1] IS A ZERO-DAMAGE HOLD WORTH ANYTHING AT ALL, against the same relic
      with the window deleted.
  [2] THE GRAB COUNT. 2 to 6, Rick's own range.
  [3] REACH, CADENCE, WINDOW. What the hand has to be able to do.
  [4] STUN AGAINST PIN — the Stasis Field's field, and what it costs to use it.
  [5] WHAT THE HOLD BUYS A CURSE RELIC. The claim the design rests on: an
      ultimate that touches the pool NOT AT ALL, and buys the blows that fill
      it. Measured against the same hold on a school that has no pool.

Injection is runtime-only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

GRAB_JS = r"""([cfg, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS;
  const w = W.find(x => x.id === cfg.donor);
  const saved = { aff: w.aff, dmg: w.dmg, charge: w.ult.charge,
                  onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = cfg.aff;
  delete w.onSelf; delete w.onHit;
  if (cfg.chan) { w.onHit = {}; w.onHit[cfg.chan] = cfg.chanPer; }
  if (cfg.dmg !== null) w.dmg = cfg.dmg;
  /* The relic's own ultimate never fires. The window below is driven off match
     time on the same clock the engine would have used, so `charge` still means
     what it means everywhere else. */
  w.ult.charge = 1e9;

  const rows = [];
  for (const f of foes) for (const sd of seeds) {
    const m = new AC.Match(cfg.donor, f, sd);
    const me = m.a.w.id === cfg.donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;

    let steps = 0, clock = 0, winT = null, grabs = 0;
    let casts = 0, totGrabs = 0, trues = 0, heldT = 0, reached = 0;
    let grabCd = 0, poolInt = 0;
    const perCast = [];

    while (!m.over && steps < secs / DT) {
      m.step(DT); steps++;
      if (m.hitStop > 0) continue;          // the sim is frozen; so is the hand
      poolInt += th.cursePool.reduce((a, b) => a + b, 0) * DT;
      if (!cfg.on) continue;

      if (winT === null) {
        clock += DT;
        if (clock >= cfg.charge && me.hp > 0) {
          winT = 0; grabs = 0; grabCd = 0; clock = 0; casts++;
        }
      }
      if (winT !== null) {
        winT += DT; grabCd -= DT;
        const d = Math.hypot(th.x - me.x, th.y - me.y);
        if (d <= cfg.radius) reached += DT;
        if (grabCd <= 0 && d <= cfg.radius && th.hp > 0) {
          grabs++; totGrabs++; grabCd = cfg.cadence;
          const last = grabs >= cfg.n;
          const hold = last ? cfg.trueStun : cfg.grabStun;
          th.stun = Math.max(th.stun, hold);
          if (cfg.pin) { th.pin = Math.max(th.pin, hold);
                         th.pinMax = Math.max(th.pinMax, hold);
                         if (!th.pinV) th.pinV = [th.vx, th.vy]; }
          heldT += hold;
          if (last) { trues++;
                      if (cfg.endOnTrue) { perCast.push(grabs); winT = null; }
                      else { grabs = 0; } }
        }
        if (winT !== null && winT >= cfg.dur) { perCast.push(grabs); winT = null; }
      }
    }
    const dur = steps * DT;
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1, dur: dur,
                hits: me.hits, dealt: me.dealt, foeHits: th.hits,
                casts: casts, grabs: totGrabs, trues: trues,
                heldT: heldT, reached: reached,
                grabsPerCast: perCast.length ? perCast.reduce((a,b)=>a+b,0)/perCast.length : 0,
                pool: dur ? poolInt / dur : 0 });
  }

  w.aff = saved.aff; w.dmg = saved.dmg; w.ult.charge = saved.charge;
  delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return rows;
}"""

BASE = dict(donor="grudgebearer", aff="umbral", chan="curse", chanPer=1, dmg=None,
            charge=16.0, dur=8.0, cadence=0.6, radius=140.0, grabStun=0.5,
            trueStun=2.0, n=4, pin=False, on=True, endOnTrue=True)


def summarise(rows):
    ok = [r for r in rows if r["win"] >= 0]
    return {
        "n": len(ok),
        "win": statistics.mean([r["win"] for r in ok]) if ok else 0,
        "casts": statistics.mean([r["casts"] for r in rows]),
        "grabs": statistics.mean([r["grabs"] for r in rows]),
        "gpc": statistics.mean([r["grabsPerCast"] for r in rows]),
        "trues": statistics.mean([r["trues"] for r in rows]),
        "held": statistics.mean([r["heldT"] for r in rows]),
        "hits": statistics.mean([r["hits"] for r in rows]),
        "foeHits": statistics.mean([r["foeHits"] for r in rows]),
        "dealt": statistics.mean([r["dealt"] for r in rows]),
        "pool": statistics.mean([r["pool"] for r in rows]),
        "dur": statistics.mean([r["dur"] for r in rows]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    seeds = [3301 + 19 * i for i in range(a.seeds)]
    out = {}
    want = set(a.only.split(",")) if a.only else None

    def run(page, foes, **kw):
        cfg = dict(BASE); cfg.update(kw)
        return summarise(page.evaluate(GRAB_JS, [cfg, foes, seeds, a.secs]))

    HDR = (f"    {'arm':<26}{'win':>7}{'casts':>7}{'grabs':>7}{'/cast':>7}"
           f"{'true':>6}{'held':>7}{'blows':>7}{'foe':>6}{'pool':>7}{'lift':>8}")

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w=>w.id)")
        foes = [i for i in ids if i != "grudgebearer"]
        n = len(foes) * a.seeds
        print(f"\nGRUDGEBEARER AS AN UMBRAL WARHAMMER, its own Crucible suppressed, "
              f"{len(foes)} foes x {a.seeds} seeds = {n} fights an arm\n")

        off = run(page, foes, on=False)
        print(f"[0] THE FLOOR — the relic with no ultimate at all\n")
        print(f"    win {off['win']:.1%}   blows {off['hits']:.1f}   "
              f"foe blows {off['foeHits']:.1f}   pool {off['pool']:.1f}   "
              f"fight {off['dur']:.1f}s")

        def row(lab, s):
            print(f"    {lab:<26}{s['win']:>7.1%}{s['casts']:>7.2f}{s['grabs']:>7.1f}"
                  f"{s['gpc']:>7.2f}{s['trues']:>6.2f}{s['held']:>7.1f}"
                  f"{s['hits']:>7.1f}{s['foeHits']:>6.1f}{s['pool']:>7.1f}"
                  f"{s['win']-off['win']:>+8.1%}")

        if not want or "1" in want:
            print(f"\n[1] IS A ZERO-DAMAGE HOLD WORTH ANYTHING — baseline: window 8s, "
                  f"cadence 0.6s, reach 140,\n    grab 0.5s, 4 grabs to true, "
                  f"true 2.0s, charge 16\n")
            print(HDR)
            base = run(page, foes)
            row("baseline", base)
            out["baseline"] = base

        if not want or "2" in want:
            print(f"\n[2] THE GRAB COUNT — Rick's 2 to 6\n")
            print(HDR)
            g2 = {}
            for nn in [2, 3, 4, 5, 6, 99]:
                s = run(page, foes, n=nn)
                row(f"n = {nn}" + ("  (never true)" if nn == 99 else ""), s)
                g2[nn] = s
            out["grabCount"] = {str(k): v for k, v in g2.items()}

        if not want or "3" in want:
            print(f"\n[3] REACH — how far the hand has to get. Ball r=34, "
                  f"warhammer reach 76, hall 520x800\n")
            print(HDR)
            for r in [70, 100, 140, 200, 280, 400]:
                row(f"radius {r}", run(page, foes, radius=float(r)))

            print(f"\n    CADENCE — how fast it can grab again\n")
            print(HDR)
            for c in [0.3, 0.45, 0.6, 0.9, 1.3]:
                row(f"cadence {c}s", run(page, foes, cadence=c))

            print(f"\n    THE WINDOW, and the hold lengths\n")
            print(HDR)
            for d in [4.0, 6.0, 8.0, 12.0]:
                row(f"window {d}s", run(page, foes, dur=d))
            for gs in [0.25, 0.5, 0.8, 1.2]:
                row(f"grab hold {gs}s", run(page, foes, grabStun=gs))
            for ts in [1.0, 2.0, 3.0, 4.0]:
                row(f"true stun {ts}s", run(page, foes, trueStun=ts))

        if not want or "4" in want:
            print(f"\n[4] STUN AGAINST PIN — `f.stun` locks the weapon; "
                  f"`f.pin` holds the BALL and is\n    the Stasis Field's, "
                  f"written by exactly one relic in the game\n")
            print(HDR)
            row("stun only", run(page, foes))
            row("stun + pin", run(page, foes, pin=True))
            for ts in [1.0, 2.0, 3.0]:
                row(f"pin, true {ts}s", run(page, foes, pin=True, trueStun=ts))
            print(f"\n    AND WITHOUT \"then dissipates\" — the window runs its "
                  f"full length and the counter\n    resets, so every nth grab "
                  f"is a true stun instead of the last one being\n")
            print(HDR)
            for nn in [2, 3, 4, 5]:
                row(f"n = {nn}, no dissipate", run(page, foes, n=nn, endOnTrue=False))

        if not want or "5" in want:
            print(f"\n[5] WHAT THE HOLD BUYS A CURSE RELIC — the same hold on "
                  f"schools with and without a pool,\n    damage pinned to "
                  f"grudgebearer's own so only the channel differs\n")
            print(HDR)
            for aff, chan, per in [("umbral", "curse", 1), ("dwarven", "sunder", 1),
                                   ("bloodsworn", "hemorrhage", 2),
                                   ("verdant", "entangle", 2), ("runic", "hex", 1),
                                   ("sanctified", "smite", 1)]:
                o = run(page, foes, on=False, aff=aff, chan=chan, chanPer=per)
                s = run(page, foes, aff=aff, chan=chan, chanPer=per)
                print(f"    {aff+' x '+chan:<26}{s['win']:>7.1%}{s['casts']:>7.2f}"
                      f"{s['grabs']:>7.1f}{s['gpc']:>7.2f}{s['trues']:>6.2f}"
                      f"{s['held']:>7.1f}{s['hits']:>7.1f}{s['foeHits']:>6.1f}"
                      f"{s['pool']:>7.1f}{s['win']-o['win']:>+8.1%}")

        assert not errors, errors[:4]

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"\nwrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
