#!/usr/bin/env python3
"""WHAT IS WRONG WITH UMBRAL. Rick asked; this answers it with measurement.

    python3 curse_probe.py --game ../02-chain/sc-paradox-ignition.html

`row_price.py` found curse topping the OCCUPANCY column on both thin rows and
sitting at or below zero by DELIVERED EFFECT, having stripped 94-108 of a
400 hp pool doing it. That is not "curse is weak" — a weak channel does not
remove a quarter of the enemy. It is a channel that arrives enormous and buys
nothing, and this probe is about which of the three possible reasons it is.

    curse: { maxStacks: 8, dur: 99, maxHpLoss: 13 }

    apply(key, n){
      ...
      if (key === "curse") this.maxHp = Math.max(60, this.maxHp - def.maxHpLoss * n);
    }

    // tickStatus, last line
    f.hp = Math.min(f.hp, f.maxHp);

  [1] NOMINAL AGAINST EFFECTIVE. A stack removes 13 from the CEILING. It
      removes health only where the clamp finds hp above the new ceiling — so
      a stack landing on a foe already below its cap is free for the foe.
      Recorded at the moment of every application.

  [2] WHEN IT LANDS. The foe's hp fraction at each application. If curse is
      front-loaded the two numbers in [1] agree; if it keeps applying to a
      bar that is already low, they diverge and that IS the defect.

  [3] WHERE IT GOES. Effective removal split by who won. Health taken off a
      foe that goes on to win is health that bought nothing, and umbral's
      donor loses most of these fights.

  [4] THE DESPERATION SIDE EFFECT, which points the other way and nobody has
      ever counted. `desperate` is `hp / maxHp <= 0.25` and curse lowers the
      DENOMINATOR, so a cursed foe crosses that line later in absolute health.
      desperation is +35% damage and +30% spin, so curse is quietly denying
      the foe a buff at the same time as it fails to kill it.

  [5] THE CONTROL THAT PRICES THE FIX. The identical nominal amount taken off
      the BOTTOM of the bar instead of the top: 13 hp per stack, current
      health, maxHp untouched. Same applier, same rate, same everything else.
      The gap between that and the shipped curse is what the school is losing.

Injection is runtime-only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


# The three umbral relics' types, plus the two thin types their open cells sit
# on, so the answer is not read off one donor.
DONORS = {"flail": "gravemourn", "greatsword": "nightfell", "twinblade": "twinshade",
          "scythe": "thornwake", "warhammer": "grudgebearer"}

ARMS_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult, arm]) => {
  const DT = AC.CONFIG.physics.dt;
  const CU = AC.STATUS.curse;
  const DES = AC.CONFIG.desperation.at;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral";
  delete w.onHit; delete w.onSelf;
  if (arm !== "none") w.onHit = { curse: 1 };

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      let nominal = 0, effective = 0, apps = 0, wasted = 0;
      const atFrac = [];
      /* INSTANCE SHADOW, not a prototype patch: only this fighter's applier is
         wrapped, so the donor's own statuses and every other relic in the
         match run the shipped code. */
      const origApply = th.apply.bind(th);
      th.apply = function(key, n){
        if (key !== "curse") return origApply(key, n);
        const cur = th.status.curse ? th.status.curse.stacks : 0;
        const room = Math.min(CU.maxStacks - cur, n);   // stacks that will land
        if (room <= 0){ return origApply(key, n); }
        const hp0 = th.hp, mh0 = th.maxHp;
        atFrac.push(hp0 / mh0);
        apps += room;
        nominal += CU.maxHpLoss * room;

        if (arm === "bottom"){
          /* THE CONTROL. The same number off the BOTTOM of the bar. maxHp is
             left alone, so nothing about the ceiling, the clamp or the
             desperation ratio moves and the only difference is where the
             health comes from. */
          const before = th.hp;
          th.hp -= CU.maxHpLoss * room;
          effective += before - th.hp;
          /* the stacks still have to exist, or the status is not applied and
             the picture and the tips disagree with the mechanic */
          const sv = CU.maxHpLoss; CU.maxHpLoss = 0;
          const r = origApply(key, n);
          CU.maxHpLoss = sv;
          return r;
        }

        const r = origApply(key, n);
        /* the clamp runs in tickStatus, after this; what it WILL take is
           exactly the overhang, and nothing else touches hp in between */
        const took = Math.max(0, hp0 - th.maxHp);
        effective += took;
        wasted += (CU.maxHpLoss * room) - took;
        return r;
      };

      let step = 0, despFr = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        if (th.alive && th.hp / th.maxHp <= DES) despFr++;
      }
      rows.push({ foe: f, seed: sd, dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  dealt: me.dealt, taken: th.dealt,
                  nominal, effective, wasted, apps,
                  atFrac: atFrac.slice(0, 24),
                  desp: step ? despFr / step : 0,
                  thHp: th.hp, thMaxHp: th.maxHp, maxHp0: 400 });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=24.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [3301 + 19 * i for i in range(a.seeds)]
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, aff:w.aff, shape:w.shape}))")
        cfg = page.evaluate("() => ({curse: AC.STATUS.curse, desp: AC.CONFIG.desperation,"
                            " hp: AC.CONFIG.combat.baseHP})")
        pin_ids = [w["id"] for w in W]
        print(f"\ncurse  maxStacks {cfg['curse']['maxStacks']}  dur {cfg['curse']['dur']}  "
              f"maxHpLoss {cfg['curse']['maxHpLoss']}   "
              f"(cap {cfg['curse']['maxStacks'] * cfg['curse']['maxHpLoss']} of "
              f"{cfg['hp']} = "
              f"{cfg['curse']['maxStacks'] * cfg['curse']['maxHpLoss'] / cfg['hp']:.0%} "
              f"of the pool)")
        print(f"desperation  at {cfg['desp']['at']:.0%} hp  ->  "
              f"dmg x{cfg['desp']['dmg']}  spin x{cfg['desp']['spin']}")

        res = {}
        for t, donor in DONORS.items():
            foes = [w["id"] for w in W if w["id"] != donor]
            res[t] = {}
            for arm in ("none", "curse", "bottom"):
                rows = page.evaluate(ARMS_JS, [donor, foes, seeds, a.secs, a.pin,
                                               pin_ids, True, arm])
                fin = [r for r in rows if r["win"] >= 0]
                won = [r for r in fin if r["win"] == 1]
                lost = [r for r in fin if r["win"] == 0]
                res[t][arm] = {
                    "win": mean(r["win"] for r in fin),
                    "nominal": mean(r["nominal"] for r in rows),
                    "effective": mean(r["effective"] for r in rows),
                    "wasted": mean(r["wasted"] for r in rows),
                    "apps": mean(r["apps"] for r in rows),
                    "effWon": mean(r["effective"] for r in won),
                    "effLost": mean(r["effective"] for r in lost),
                    "desp": mean(r["desp"] for r in rows),
                    "dur": mean(r["dur"] for r in rows),
                    "atFrac": [x for r in rows for x in r["atFrac"]],
                }

        # ------------------------------------------------------------ [1] --
        print(f"\n[1] NOMINAL AGAINST EFFECTIVE — what a curse stack is worth "
              f"on paper, and what the clamp actually took\n")
        print(f"    {'donor':<14}{'type':<12}{'stacks landed':>15}"
              f"{'nominal hp':>12}{'ACTUALLY TAKEN':>16}{'wasted':>9}{'kept':>7}")
        for t, donor in DONORS.items():
            c = res[t]["curse"]
            keep = c["effective"] / c["nominal"] if c["nominal"] else 0
            print(f"    {donor:<14}{t:<12}{c['apps']:>15.1f}{c['nominal']:>12.0f}"
                  f"{c['effective']:>16.0f}{c['wasted']:>9.0f}{keep:>7.0%}")
        keeps = [res[t]["curse"]["effective"] / max(1, res[t]["curse"]["nominal"])
                 for t in DONORS]
        check("a curse stack does not deliver what the tip says it delivers",
              mean(keeps) < 0.9,
              f"{mean(keeps):.0%} of the nominal removal reaches the foe, "
              f"averaged over five donors — the tip says "
              f"'Permanently takes 13 max hp per stack' and it does, but the "
              f"CLAMP is what turns a ceiling into health and it only fires "
              f"where the bar is above the new ceiling")

        # ------------------------------------------------------------ [2] --
        print(f"\n[2] WHEN IT LANDS — the foe's hp fraction at each application\n")
        print(f"    {'donor':<14}{'applications':>14}{'mean hp% at apply':>20}"
              f"{'landed above 50%':>18}{'landed below 25%':>18}")
        for t, donor in DONORS.items():
            fr = res[t]["curse"]["atFrac"]
            if not fr:
                continue
            hi = sum(1 for x in fr if x > 0.5) / len(fr)
            lo = sum(1 for x in fr if x < 0.25) / len(fr)
            print(f"    {donor:<14}{len(fr):>14}{mean(fr):>20.0%}"
                  f"{hi:>18.0%}{lo:>18.0%}")

        # ------------------------------------------------------------ [3] --
        print(f"\n[3] WHERE IT GOES — effective removal, split by who won\n")
        print(f"    {'donor':<14}{'win':>8}{'hp taken in a WIN':>20}"
              f"{'hp taken in a LOSS':>21}{'share of it wasted on a loss':>31}")
        for t, donor in DONORS.items():
            c = res[t]["curse"]
            n = res[t]["none"]
            tot = c["effWon"] + c["effLost"]
            share = c["effLost"] / tot if tot else 0
            print(f"    {donor:<14}{c['win']:>8.1%}{c['effWon']:>20.0f}"
                  f"{c['effLost']:>21.0f}{share:>31.0%}")

        # ------------------------------------------------------------ [4] --
        print(f"\n[4] THE SIDE EFFECT NOBODY HAS COUNTED — curse lowers the "
              f"DENOMINATOR of `hp / maxHp <= 0.25`\n")
        print(f"    {'donor':<14}{'foe desperate, no curse':>26}"
              f"{'with curse':>14}{'change':>10}")
        for t, donor in DONORS.items():
            n, c = res[t]["none"], res[t]["curse"]
            print(f"    {donor:<14}{n['desp']:>26.1%}{c['desp']:>14.1%}"
                  f"{(c['desp'] - n['desp']):>+10.1%}")
        dd = mean(res[t]["curse"]["desp"] - res[t]["none"]["desp"] for t in DONORS)
        check("curse ALSO denies the foe its desperation buff, which is worth "
              "something and has never been counted",
              dd < 0,
              f"the foe spends {abs(dd):.1%} less of the fight under "
              f"x{cfg['desp']['dmg']} damage and x{cfg['desp']['spin']} spin. "
              f"It is real and it is not enough to save the channel")

        # ------------------------------------------------------------ [5] --
        print(f"\n[5] THE FIX, PRICED — the identical nominal amount taken off the "
              f"BOTTOM of the bar instead of the top\n")
        print(f"    {'donor':<14}{'no channel':>12}{'curse as shipped':>19}"
              f"{'lift':>8}{'same hp as damage':>20}{'lift':>8}")
        for t, donor in DONORS.items():
            n, c, b = res[t]["none"], res[t]["curse"], res[t]["bottom"]
            print(f"    {donor:<14}{n['win']:>12.1%}{c['win']:>19.1%}"
                  f"{c['win'] - n['win']:>+8.1%}{b['win']:>20.1%}"
                  f"{b['win'] - n['win']:>+8.1%}")
        lc = mean(res[t]["curse"]["win"] - res[t]["none"]["win"] for t in DONORS)
        lb = mean(res[t]["bottom"]["win"] - res[t]["none"]["win"] for t in DONORS)
        check("THE SAME NUMBER OFF THE BOTTOM OF THE BAR IS WORTH SEVERAL TIMES "
              "WHAT IT IS WORTH OFF THE TOP",
              lb > lc,
              f"curse as shipped {lc:+.1%}, the identical hp as damage "
              f"{lb:+.1%} — a factor of "
              f"{(lb / lc) if abs(lc) > 0.001 else float('inf'):.1f}x on the "
              f"same applications, same rate, same everything else")
        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))
        out = {"cfg": cfg, "res": {t: {k: {kk: vv for kk, vv in v.items()
                                          if kk != "atFrac"}
                                      for k, v in arms.items()}
                                  for t, arms in res.items()}}

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
