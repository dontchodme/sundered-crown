#!/usr/bin/env python3
"""THE AMPLIFIER AT WEIGHT — dwarven x scythe, before the ultimate is designed.

    python3 sunder_survey.py --game ../02-chain/sc-nightfell.html

Rick has taken **dwarven x scythe** for the 30th relic, from four priced cells
(v57). Sunder is the only status in the table that is a pure MULTIPLIER: it
deals nothing itself and adds 11% damage taken per stack, six stacks, 5.0s.

Every other channel in the game pays out on the blow that applies it or on a
clock. Sunder pays out on the NEXT blow — so its worth is contact rate twice
over: once to raise the stacks, and once to spend them before they decay. The
scythe has the second-fewest blows in the game.

REGISTERED PREDICTION, and this tool's job is to falsify it:

    sunder's delivered value rises with contact rate; the scythe's inter-blow
    interval is close to sunder's 5.0s duration, so a scythe should sit under
    two stacks, should land a large share of its blows at ZERO stacks, and
    should be near the bottom of the six types.

  [1] THE STACK AT WEIGHT. Every type's donor carrying dwarven's channel at its
      OWN shipped damage, ultimates suppressed. Read off a wrapped
      `dmgTakenMul` — the exact multiplier every blow was amplified by — not
      sampled per step.
  [2] THE SAME WITH DAMAGE PINNED. Blow RATE against blow SIZE, separated
      rather than summed. Sunder is the one channel whose payout does not
      depend on blow size at all, so the two tables should differ less here
      than they do for curse (v55 2b) — which is itself a check.
  [3] DECAY AGAINST CADENCE. The share of blows arriving at zero stacks, and
      the mean gap between blows against the status's own 5.0s.
  [4] WHAT THE THREE DWARVEN ULTIMATES WOULD READ. Crucible consumes the
      stacks, Slagburst detonates them, Ironbloom's shrapnel applies more. All
      three are tuned against a warhammer's, a greatsword's and a flail's
      stack count. Does a scythe's transfer?

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
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


TYPE_DONOR = {"greatsword": "dawnbringer", "twinblade": "widowmaker",
              "warhammer": "grudgebearer", "scythe": "thornwake",
              "flail": "gravemourn", "bow": "ironhail"}

# ---------------------------------------------------------------------------
# ON: the donor carries dwarven's onHit sunder. OFF: the donor carries no
# channel at all. Same seeds, same foes, same body — the only difference is the
# channel, so the pair is paired and the difference is the channel's.
#
# `dmgTakenMul` is wrapped rather than sampled: it is called once per damage
# event on the fighter it belongs to and it returns the exact number the blow
# was multiplied by. Sampling stacks per step would count the seconds a stack
# existed, which is what `cell_survey` [4] does and is the proxy v39 5.2 and
# v47 both caught being wrong.
# ---------------------------------------------------------------------------

SUNDER_JS = r"""([donor, foes, seeds, secs, on, pinAll]) => {
  const DT = AC.CONFIG.physics.dt;
  const W  = AC.WEAPONS;
  const w  = W.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg,
                  onHit:  w.onHit  ? JSON.parse(JSON.stringify(w.onHit))  : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "dwarven";
  delete w.onHit; delete w.onSelf;
  if (on) w.onHit = { sunder: 1 };

  const savedUlt = {}, savedDmg = {};
  for (const x of W) {
    if (x.ult) { savedUlt[x.id] = x.ult.charge; x.ult.charge = 1e9; }
    if (pinAll !== null) { savedDmg[x.id] = x.dmg; x.dmg = pinAll; }
  }

  const probe = new AC.Match(donor, foes[0], 1);
  const F = Object.getPrototypeOf(probe.a);
  const origMul = F.dmgTakenMul;
  let LOG = null;
  F.dmgTakenMul = function () {
    const v = origMul.call(this);
    if (LOG && this.side === LOG.foeSide) {
      LOG.mul.push(v);
      LOG.stk.push(this.stacks("sunder"));
      LOG.at.push(LOG.t);
    }
    return v;
  };

  const rows = [];
  try {
    for (const f of foes) {
      for (const s of seeds) {
        const m  = new AC.Match(donor, f, s);
        const me = m.a.w.id === donor ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        LOG = { foeSide: th.side, mul: [], stk: [], at: [], t: 0 };
        let steps = 0, stkInt = 0, capT = null;
        const cap = AC.STATUS.sunder.maxStacks;
        while (!m.over && steps < secs / DT) {
          m.step(DT); steps++; LOG.t = steps * DT;
          const k = th.stacks("sunder");
          stkInt += k * DT;
          if (capT === null && k >= cap) capT = steps * DT;
        }
        const dur = steps * DT;
        const gaps = [];
        for (let i = 1; i < LOG.at.length; i++) gaps.push(LOG.at[i] - LOG.at[i-1]);
        rows.push({
          foe: f, seed: s, dur: dur, over: m.over,
          win: m.winner ? (m.winner === me ? 1 : 0) : -1,
          hits: me.hits, dealt: me.dealt, taken: th.dealt,
          events: LOG.mul.length,
          meanMul: LOG.mul.length ? LOG.mul.reduce((a,b)=>a+b,0) / LOG.mul.length : 1,
          meanStkAtBlow: LOG.stk.length ? LOG.stk.reduce((a,b)=>a+b,0) / LOG.stk.length : 0,
          zeroShare: LOG.stk.length ? LOG.stk.filter(x=>x===0).length / LOG.stk.length : 0,
          capShare: LOG.stk.length ? LOG.stk.filter(x=>x>=cap).length / LOG.stk.length : 0,
          twStk: dur > 0 ? stkInt / dur : 0,
          capT: capT,
          gap: gaps.length ? gaps.reduce((a,b)=>a+b,0) / gaps.length : null,
        });
      }
    }
  } finally {
    F.dmgTakenMul = origMul;
    w.aff = saved.aff; w.dmg = saved.dmg;
    delete w.onHit; delete w.onSelf;
    if (saved.onHit)  w.onHit  = saved.onHit;
    if (saved.onSelf) w.onSelf = saved.onSelf;
    for (const x of W) {
      if (x.ult && savedUlt[x.id] !== undefined) x.ult.charge = savedUlt[x.id];
      if (savedDmg[x.id] !== undefined) x.dmg = savedDmg[x.id];
    }
  }
  return rows;
}"""

SHIPPED_JS = """() => Object.fromEntries(AC.WEAPONS.map(w => [w.id, w.dmg]))"""

DWARF_JS = """() => ({
  relics: AC.WEAPONS.filter(w => w.aff === "dwarven")
            .map(w => ({ id: w.id, shape: w.shape, dmg: w.dmg,
                         onHit: w.onHit, ult: w.ult })),
  sunder: AC.STATUS.sunder,
  scythes: AC.WEAPONS.filter(w => w.shape === "scythe")
             .map(w => ({ id: w.id, aff: w.aff, dmg: w.dmg,
                          ult: { name: w.ult.name, kind: w.ult.kind,
                                 charge: w.ult.charge, tip: w.ult.tip } })),
})"""


def arm(page, donor, foes, seeds, secs, on, pin):
    rows = page.evaluate(SUNDER_JS, [donor, foes, seeds, secs, on, pin])
    fin = [r for r in rows if r["win"] >= 0]
    dur = sum(r["dur"] for r in rows)
    return {
        "n": len(rows),
        "win": mean(r["win"] for r in fin),
        "blows": mean(r["events"] for r in rows),
        "hps": sum(r["events"] for r in rows) / dur,
        "meanMul": mean(r["meanMul"] for r in rows),
        "stkAtBlow": mean(r["meanStkAtBlow"] for r in rows),
        "zero": mean(r["zeroShare"] for r in rows),
        "capShare": mean(r["capShare"] for r in rows),
        "twStk": mean(r["twStk"] for r in rows),
        "gap": mean(r["gap"] for r in rows if r["gap"] is not None),
        "capT": mean(r["capT"] for r in rows if r["capT"] is not None),
        "capEver": sum(1 for r in rows if r["capT"] is not None) / max(1, len(rows)),
        "dealt": mean(r["dealt"] for r in rows),
        "dur": mean(r["dur"] for r in rows),
    }


def table(page, types, foes_all, seeds, secs, pin):
    out = {}
    for t in types:
        d = TYPE_DONOR[t]
        foes = [f for f in foes_all if f != d]
        on = arm(page, d, foes, seeds, secs, True, pin)
        off = arm(page, d, foes, seeds, secs, False, pin)
        on["lift"] = on["win"] - off["win"]
        on["winOff"] = off["win"]
        on["dealtOff"] = off["dealt"]
        on["donor"] = d
        out[t] = on
    return out


def show(name, tab, dmg):
    print(f"\n{name}\n")
    print(f"    {'type':<11}{'donor':<14}{'dmg':>6}{'blows':>7}{'gap':>7}"
          f"{'stk@blow':>10}{'0 stk':>7}{'6 stk':>7}{'meanMul':>9}"
          f"{'dealt':>8}{'no-ch':>8}{'lift':>8}")
    for t, r in sorted(tab.items(), key=lambda kv: -kv[1]["lift"]):
        print(f"    {t:<11}{r['donor']:<14}{dmg[r['donor']]:>6.1f}{r['blows']:>7.1f}"
              f"{r['gap']:>7.2f}{r['stkAtBlow']:>10.2f}{r['zero']:>7.0%}"
              f"{r['capShare']:>7.0%}{r['meanMul']:>9.3f}{r['dealt']:>8.0f}"
              f"{r['dealtOff']:>8.0f}{r['lift']:>+8.1%}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--types", default="")
    ap.add_argument("--skip-pin", action="store_true")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [2207 + 11 * i for i in range(a.seeds)]
    types = a.types.split(",") if a.types else list(TYPE_DONOR)
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        dmg = page.evaluate(SHIPPED_JS)
        info = page.evaluate(DWARF_JS)
        foes_all = list(dmg)

        print(f"\n[0] THE ROOM — sunder {info['sunder']['taken']:.0%} per stack, "
              f"{info['sunder']['maxStacks']} stacks, {info['sunder']['dur']}s\n")
        print(f"    dwarven ships {len(info['relics'])} relics:")
        for r in info["relics"]:
            k = list(r["onHit"].items())[0] if r["onHit"] else ("—", 0)
            print(f"      {r['id']:<14}{r['shape']:<12}dmg {r['dmg']:<7.2f}"
                  f"onHit {k[0]}:{k[1]:<4}{r['ult']['name']}")
        print(f"\n    the scythe row as shipped:")
        for r in info["scythes"]:
            print(f"      {r['id']:<14}{r['aff']:<12}dmg {r['dmg']:<7.2f}"
                  f"{r['ult']['name']:<14}{r['ult']['kind']:<10}"
                  f"charge {r['ult']['charge']}")

        ship = table(page, types, foes_all, seeds, a.secs, None)
        show(f"[1] THE STACK AT WEIGHT — each type's donor at its OWN shipped "
             f"damage,\n    ultimates suppressed, {len(foes_all)-1} foes x "
             f"{len(seeds)} seeds an arm", ship, dmg)
        out["shipped"] = ship

        if not a.skip_pin:
            pinned = table(page, types, foes_all, seeds, a.secs, a.pin)
            show(f"[2] THE SAME WITH EVERY RELIC PINNED TO {a.pin:g} — blow RATE "
                 f"with blow SIZE removed", pinned, {k: a.pin for k in dmg})
            out["pinned"] = pinned

            print(f"\n    what moved between the two tables\n")
            print(f"    {'type':<11}{'lift@ship':>11}{'lift@pin':>10}{'move':>9}"
                  f"{'stk@ship':>10}{'stk@pin':>9}")
            for t in sorted(ship, key=lambda t: -ship[t]["lift"]):
                s, p = ship[t], pinned[t]
                print(f"    {t:<11}{s['lift']:>+11.1%}{p['lift']:>+10.1%}"
                      f"{(s['lift']-p['lift'])*100:>+8.1f}pp"
                      f"{s['stkAtBlow']:>10.2f}{p['stkAtBlow']:>9.2f}")

        # ---------------------------------------------------------- [3] --
        print(f"\n[3] DECAY AGAINST CADENCE — sunder's own duration is "
              f"{info['sunder']['dur']}s\n")
        print(f"    {'type':<11}{'gap between blows':>19}{'gap / dur':>11}"
              f"{'blows at 0 stk':>16}{'ever reached 6':>16}{'first 6 at':>12}")
        for t, r in sorted(ship.items(), key=lambda kv: kv[1]["gap"]):
            capt = f"{r['capT']:.1f}s" if r["capEver"] else "never"
            print(f"    {t:<11}{r['gap']:>19.2f}"
                  f"{r['gap']/info['sunder']['dur']:>11.2f}"
                  f"{r['zero']:>16.0%}{r['capEver']:>16.0%}{capt:>12}")

        sc = ship.get("scythe")
        if sc:
            faster = [t for t, r in ship.items() if r["gap"] < sc["gap"]]
            rank = sorted(ship, key=lambda t: -ship[t]["lift"]).index("scythe") + 1
            check("the scythe holds under two stacks at the moment of a blow",
                  sc["stkAtBlow"] < 2.0,
                  f"{sc['stkAtBlow']:.2f} stacks, {sc['zero']:.0%} of blows at zero")
            check("sunder's delivered lift rises with contact rate",
                  all(ship[t]["lift"] >= sc["lift"] for t in faster),
                  "types with a shorter gap than the scythe: "
                  + ", ".join(f"{t} {ship[t]['lift']:+.1%}" for t in faster)
                  + f"  vs scythe {sc['lift']:+.1%}")
            check("the scythe is in the bottom half of the six on delivered lift",
                  rank > len(ship) / 2,
                  f"rank {rank} of {len(ship)}")

        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    print("\nA RED CHECK HERE IS THE FINDING, not a bug. Every one of them is a\n"
          "sentence this survey went in believing.")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
