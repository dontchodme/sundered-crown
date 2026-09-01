#!/usr/bin/env python3
"""RICK'S §1 FOR THE 30th RELIC, PRICED BEFORE A BUILDER IS OPENED.

    "the scythe throws out a bloody spectral copy of itself. the copy flies a
     short duration and then sticks in place. rotating around its center axis
     and dealing damage to any enemy in its area. the spectral scythe deals
     reduced damage but hits rapidly applying bleed."

THE QUESTION THIS ULTIMATE HAS TO ANSWER IS NOT "IS IT STRONG". It is whether
the BLEED half of the sentence does anything at all, because Hemorrhage is a
flat 1.5 damage a second a stack and it CAPS AT FOUR. A spectre that hits every
0.2s saturates the cap in under a second and every application after that is
duration upkeep, not damage. If that is true then "hits rapidly applying bleed"
is a picture and the tick DAMAGE is the mechanic, which is worth knowing before
anybody tunes the wrong number for a week.

Thornwake stands in — same shape, same mass, same reach, same 5.24s contact
gap. Its entangle is replaced with bloodsworn's hemorrhage at the school's own
weight (2 a hit) and Bramblesnare is stripped to a bare cast, so the only thing
the ultimate does is Rick's §1. The 26 other relics keep their own ultimates:
this is the real field, NOT `row_price`'s ultimates-off world (v59 §4.1).

Runtime injection only. Nothing is written to any build.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from scpage import game  # noqa: E402

DONOR = "thornwake"

JS = r"""([donor, foes, seeds, secs, P]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const origFire = AC.Match.prototype.fireUlt;

  /* ---- the donor becomes the cell ------------------------------------ */
  const sv = { onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
               onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
               dmg: w.dmg, ult: JSON.parse(JSON.stringify(w.ult)) };
  delete w.onHit; delete w.onSelf;
  if (P.chan) w.onHit = { hemorrhage: P.per };
  if (P.blade > 0) w.dmg = P.blade;
  /* Bramblesnare stripped to a bare cast — no damage, no root, no entangle */
  w.ult.dmg = 0; w.ult.freeze = 0; delete w.ult.apply;
  if (P.noult) w.ult.charge = 1e9;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m  = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;

    let spectres = [], casts = 0, ticks = 0, spDmg = 0, selfTicks = 0;
    let inAreaSteps = 0, liveSteps = 0;

    m.fireUlt = function(fr, foe){
      const r = origFire.call(this, fr, foe);
      if (fr === me && foe === th && P.on){
        casts++;
        /* thrown at where the quarry is NOW. No homing — it is a thrown
           object, and Rick's ricochet ruling on Thornshear is the precedent:
           natural, predictable, no tracking. */
        const dx = th.x - me.x, dy = th.y - me.y, d = Math.hypot(dx, dy) || 1;
        for (let i = 0; i < P.n; i++){
          const sp = (i - (P.n - 1) / 2) * 0.35;          // fan, if n > 1
          const ca = Math.cos(sp), sa = Math.sin(sp);
          spectres.push({ x: me.x, y: me.y,
                          vx: (dx/d*ca - dy/d*sa) * P.speed,
                          vy: (dx/d*sa + dy/d*ca) * P.speed,
                          flyUntil: this.t + P.flight,
                          dieAt: this.t + P.flight + P.life,
                          next: this.t + P.tick });
        }
      }
      return r;
    };

    let step = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const A = AC.CONFIG.arena;
      for (let i = spectres.length - 1; i >= 0; i--){
        const s = spectres[i];
        if (m.t > s.dieAt){ spectres.splice(i, 1); continue; }
        const flying = m.t < s.flyUntil;
        if (flying){
          s.x += s.vx * DT; s.y += s.vy * DT;
          /* it stops at a wall rather than leaving the hall */
          if (s.x < 0 || s.x > A.w || s.y < 0 || s.y > A.h){
            s.x = Math.max(0, Math.min(A.w, s.x));
            s.y = Math.max(0, Math.min(A.h, s.y));
            s.flyUntil = m.t;
          }
        }
        liveSteps++;
        const df = Math.hypot(th.x - s.x, th.y - s.y);
        if (df <= P.rad) inAreaSteps++;
        if (m.hitStop > 0) continue;            // the sim is frozen; so is it
        if (m.t < s.next) continue;
        if (flying && !P.hitFly){ s.next = m.t + P.tick; continue; }
        s.next = m.t + P.tick;
        if (th.alive && df <= P.rad){
          ticks++;
          const dmg = Math.round(P.dmg * th.dmgTakenMul());
          if (dmg > 0){ m.hurt(th, dmg, me); spDmg += dmg; }
          if (P.bleed > 0) th.apply("hemorrhage", P.bleed);
          if (P.knock > 0){
            const dx2 = th.x - s.x, dy2 = th.y - s.y, dl = Math.hypot(dx2, dy2) || 1;
            th.vx += dx2/dl * P.knock; th.vy += dy2/dl * P.knock;
          }
        }
        if (P.selfHit && me.alive){
          const ds = Math.hypot(me.x - s.x, me.y - s.y);
          if (ds <= P.rad){
            selfTicks++;
            const sd = Math.round(P.dmg * me.dmgTakenMul());
            if (sd > 0) m.hurt(me, sd, th);
            if (P.bleed > 0) me.apply("hemorrhage", P.bleed);
          }
        }
      }
      /* THE WINDOW'S CEILING. Rick's fork: while the ultimate is standing,
         Hemorrhage stacks past its usual 4 — for the blade too, not only the
         spectre. maxStacks is GLOBAL in the engine, so this is the naive build
         and its scoping is an open question for Code. */
      if (P.capHi > 0) AC.STATUS.hemorrhage.maxStacks = spectres.length ? P.capHi : 4;
      if (m.over) spectres.length = 0;
    }

    AC.STATUS.hemorrhage.maxStacks = 4;
    rows.push({ foe: f, seed: sd, dur: step * DT,
                win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                casts, ticks, spDmg, selfTicks,
                dwell: liveSteps ? inAreaSteps / liveSteps : 0,
                hits: me.hits, dealt: me.dealt });
  }

  delete w.onHit; delete w.onSelf;
  if (sv.onHit) w.onHit = sv.onHit;
  if (sv.onSelf) w.onSelf = sv.onSelf;
  w.dmg = sv.dmg; w.ult = sv.ult;
  return rows;
}"""

CENTRE = dict(chan=True, per=2, blade=0, noult=False, on=True, n=1,
              speed=420.0, flight=0.55, life=6.0, rad=138.0, tick=0.22,
              dmg=4.0, bleed=1, knock=0.0, hitFly=True, selfHit=False, capHi=0)


def arms():
    A = []
    def add(name, **kw): A.append((name, {**CENTRE, **kw}))
    add("no ultimate at all",            noult=True, on=False)
    add("bare cast, no spectre",         on=False)
    add("THE CENTRE",                    )
    A.append(("--- does the bleed half do anything ---", None))
    add("spectre, NO bleed",             bleed=0)
    add("spectre, bleed 2 a tick",       bleed=2)
    add("bleed only, no tick damage",    dmg=0.0)
    A.append(("--- the tick rate ---", None))
    for t in (0.12, 0.35, 0.55, 0.90):
        add(f"tick {t:.2f}s",            tick=t)
    A.append(("--- damage a tick ---", None))
    for d in (2.0, 6.0, 9.0):
        add(f"dmg {d:.0f} a tick",       dmg=d)
    A.append(("--- the area ---", None))
    for r in (104.0, 172.0, 206.0):
        add(f"radius {r:.0f}",           rad=r)
    A.append(("--- how long it stands ---", None))
    for l in (3.0, 9.0, 13.0):
        add(f"life {l:.0f}s",            life=l)
    A.append(("--- the flight ---", None))
    add("flight 0.2s",                   flight=0.2)
    add("flight 1.1s",                   flight=1.1)
    add("inert while flying",            hitFly=False)
    A.append(("--- forks that are not knobs ---", None))
    add("it cuts the caster too",        selfHit=True)
    add("knockback 120",                 knock=120.0)
    add("two spectres, half life",       n=2, life=3.0)
    return A


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="spectre.json")
    a = ap.parse_args()
    seeds = [2207 + 11 * i for i in range(a.seeds)]
    gp = (TOOLS / a.game).resolve()
    t0 = time.time(); out = {}

    def wr(rs):
        d = [r for r in rs if r["win"] >= 0]
        return sum(r["win"] for r in d) / len(d) if d else float("nan")

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != DONOR]
        AR = arms()
        n = sum(1 for _, p in AR if p)
        print(f"\nRICK'S §1, PRICED — {DONOR} standing in, hemorrhage 2 a hit, "
              f"Bramblesnare stripped")
        print(f"{len(foes)} foes x {a.seeds} seeds = {len(foes)*a.seeds} fights an arm, "
              f"{n} arms, {n*len(foes)*a.seeds} fights\n")
        print(f"  {'arm':<30}{'win':>7}{'lift':>8}{'casts':>7}{'ticks':>7}"
              f"{'spDmg':>8}{'dwell':>7}{'self':>6}")
        base = None
        for name, P in AR:
            if P is None:
                print(f"  {name}")
                continue
            rs = page.evaluate(JS, [DONOR, foes, seeds, a.secs, P])
            assert not errors, errors
            w = wr(rs)
            if base is None:
                base = w
            rec = dict(win=w, lift=w - base,
                       casts=statistics.mean(r["casts"] for r in rs),
                       ticks=statistics.mean(r["ticks"] for r in rs),
                       spDmg=statistics.mean(r["spDmg"] for r in rs),
                       dwell=statistics.mean(r["dwell"] for r in rs),
                       selfT=statistics.mean(r["selfTicks"] for r in rs))
            out[name] = rec
            print(f"  {name:<30}{w:>7.1%}{w-base:>+8.1%}{rec['casts']:>7.2f}"
                  f"{rec['ticks']:>7.1f}{rec['spDmg']:>8.0f}{rec['dwell']:>7.1%}"
                  f"{rec['selfT']:>6.1f}", flush=True)
        print(f"\n  {n*len(foes)*a.seeds} fights in {time.time()-t0:.0f}s   "
              f"page errors: {errors}")
    pathlib.Path(TOOLS / a.out).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
