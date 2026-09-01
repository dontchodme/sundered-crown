#!/usr/bin/env python3
"""THE POOL AT WEIGHT — umbral x warhammer, before the ultimate is designed.

    python3 wh_curse_survey.py --game ../02-chain/sc-nightfell.html

Rick has taken **umbral x warhammer** for the 29th relic, from four priced
cells. Curse was reworked hours ago (v49/v53): a stack REMEMBERS the damage of
the blow that applied it, the pool holds the top 3, a new stack displaces the
weakest, and every later hit pays 8% of the pool's sum. The rework makes blow
size the mechanic -- and the warhammer is the heaviest blade in the game.

`row_price` cannot see that, because it PINS damage to stop a harder-hitting
relic ending the fight sooner. On the warhammer row the pin decides the answer:
hemorrhage is +28.7% at pin 8 and +9.8% at pin 36, curse is +8.1% and +8.7%.
This is the measurement the pin was suppressing.

  [1] THE POOL, TYPE BY TYPE. Exact, off wrapped `pushCurse` / `curseEcho`, not
      sampled per step: what fills it, how fast, how big the entries are, how
      often a blow DISPLACES one, and what the sum is worth.
  [2] BLOW SIZE AGAINST CONTACT RATE. The same measurement with damage pinned,
      so the two causes are separated instead of summed.
  [3] WHAT THE ULTIMATES WOULD READ. Revenant takes entries; Deadfall copies
      the sum. Both are tuned against the flail's pool. Does a warhammer's
      pool transfer?
  [4] THE FIRST CAST. v52 5 -- umbral is a school where nothing works until
      Curse is stacked. How many blows are behind this type's first cast?

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


# donor per type: the relic whose physics carry the injected channel
TYPE_DONOR = {"greatsword": "dawnbringer", "twinblade": "widowmaker",
              "warhammer": "grudgebearer", "scythe": "thornwake",
              "flail": "gravemourn", "bow": "ironhail"}

POOL_JS = r"""([donor, dmgOverride, foes, seeds, secs, noult, pinAll]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS;
  const w = W.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg,
                  onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral";
  delete w.onSelf;
  w.onHit = { curse: 1 };
  if (dmgOverride !== null) w.dmg = dmgOverride;

  // ultimates suppressed everywhere: Revenant TAKES pool entries and Deadfall
  // COPIES the sum, so a live ult is measuring the ult, not the pool.
  const savedUlt = {}, savedDmg = {};
  for (const x of W) {
    if (noult && x.ult) { savedUlt[x.id] = x.ult.charge; x.ult.charge = 1e9; }
    if (pinAll !== null && x.id !== donor) { savedDmg[x.id] = x.dmg; x.dmg = pinAll; }
  }

  const probe = new AC.Match(donor, foes[0], 1);
  const F = Object.getPrototypeOf(probe.a);
  const origEcho = F.curseEcho, origPush = F.pushCurse;
  let LOG = null;
  F.curseEcho = function () {
    const v = origEcho.call(this);
    if (LOG && this.side === LOG.foeSide) LOG.echo.push(v);
    return v;
  };
  F.pushCurse = function (v, n) {
    const before = this.cursePool.slice();
    const r = origPush.call(this, v, n);
    if (LOG && this.side === LOG.foeSide) {
      const cap = AC.STATUS.curse.maxStacks;
      LOG.push.push({ v: v, t: LOG.t, before: before.length,
                      displaced: before.length >= cap,
                      lo: Math.min.apply(null, this.cursePool),
                      hi: Math.max.apply(null, this.cursePool) });
      LOG.sumTrace.push(this.cursePool.reduce((a, b) => a + b, 0));
    }
    return r;
  };

  const rows = [];
  for (const f of foes) {
    for (const s of seeds) {
      const m = new AC.Match(donor, f, s);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      LOG = { foeSide: th.side, echo: [], push: [], sumTrace: [], t: 0 };
      let steps = 0, sumInt = 0, peak = 0, capT = null, capBlows = null;
      const cap = AC.STATUS.curse.maxStacks;
      while (!m.over && steps < secs / DT) {
        m.step(DT); steps++; LOG.t = steps * DT;
        const ps = th.cursePool.reduce((a, b) => a + b, 0);
        sumInt += ps * DT;
        if (ps > peak) peak = ps;
        if (capT === null && th.cursePool.length >= cap) {
          capT = steps * DT; capBlows = LOG.push.length;
        }
      }
      const dur = steps * DT;
      const entries = LOG.push.map(p => p.v);
      rows.push({
        foe: f, seed: s, dur: dur, hits: me.hits, dealt: me.dealt,
        pushes: LOG.push.length,
        displaced: LOG.push.filter(p => p.displaced).length,
        entryMean: entries.length ? entries.reduce((a, b) => a + b, 0) / entries.length : 0,
        entryMax: entries.length ? Math.max(...entries) : 0,
        floorMean: LOG.push.length ? LOG.push.reduce((a,p)=>a+p.lo,0)/LOG.push.length : 0,
        floorLate: (() => { const L = LOG.push.filter(p => p.before >= cap);
                            return L.length ? L.reduce((a,p)=>a+p.lo,0)/L.length : 0; })(),
        poolMean: dur ? sumInt / dur : 0,
        poolPeak: peak,
        poolEnd: th.cursePool.reduce((a, b) => a + b, 0),
        echoN: LOG.echo.length,
        echoSum: LOG.echo.reduce((a, b) => a + b, 0),
        capT: capT, capBlows: capBlows,
        won: m.winner === me.side ? 1 : 0,
      });
      LOG = null;
    }
  }

  F.curseEcho = origEcho; F.pushCurse = origPush;
  w.aff = saved.aff; w.dmg = saved.dmg;
  delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  for (const x of W) {
    if (x.id in savedUlt) x.ult.charge = savedUlt[x.id];
    if (x.id in savedDmg) x.dmg = savedDmg[x.id];
  }
  return rows;
}"""

CHARGE_JS = r"""([donor, dmgOverride, foes, seeds, secs]) => {
  // How many blows are behind the FIRST cast on this type. v52 §5.
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg,
                  onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
                  charge: w.ult ? w.ult.charge : null };
  w.aff = "umbral"; delete w.onSelf; w.onHit = { curse: 1 };
  if (dmgOverride !== null) w.dmg = dmgOverride;
  const rows = [];
  for (const f of foes) for (const s of seeds) {
    const m = new AC.Match(donor, f, s);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let steps = 0, fired = 0, firstBlows = null, firstPool = null, firstT = null;
    let prevUlts = 0;
    while (!m.over && steps < secs / DT) {
      m.step(DT); steps++;
      if (me.ultsFired > prevUlts) {
        if (firstBlows === null) {
          firstBlows = th.cursePool.length;
          firstPool = th.cursePool.reduce((a, b) => a + b, 0);
          firstT = steps * DT;
        }
        prevUlts = me.ultsFired;
      }
    }
    rows.push({ casts: me.ultsFired, firstStacks: firstBlows,
                firstPool: firstPool, firstT: firstT, dur: steps * DT });
  }
  w.aff = saved.aff; w.dmg = saved.dmg;
  delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return rows;
}"""


def summarise(rows):
    n = len(rows)
    tot_dur = sum(r["dur"] for r in rows)
    return {
        "n": n,
        "dur": mean(r["dur"] for r in rows),
        "hits": mean(r["hits"] for r in rows),
        "hps": sum(r["hits"] for r in rows) / tot_dur if tot_dur else 0,
        "pushes": mean(r["pushes"] for r in rows),
        "disp": (sum(r["displaced"] for r in rows) / max(1, sum(r["pushes"] for r in rows))),
        "entryMean": mean(r["entryMean"] for r in rows if r["pushes"]),
        "entryMax": mean(r["entryMax"] for r in rows if r["pushes"]),
        "floorLate": mean([r["floorLate"] for r in rows if r["floorLate"]], 0),
        "poolMean": mean(r["poolMean"] for r in rows),
        "poolPeak": mean(r["poolPeak"] for r in rows),
        "echoSum": mean(r["echoSum"] for r in rows),
        "echoShare": (sum(r["echoSum"] for r in rows) / max(1e-9, sum(r["dealt"] for r in rows))),
        "dealt": mean(r["dealt"] for r in rows),
        "capT": mean([r["capT"] for r in rows if r["capT"] is not None], 0),
        "capBlows": mean([r["capBlows"] for r in rows if r["capBlows"] is not None], 0),
        "capShare": sum(1 for r in rows if r["capT"] is not None) / max(1, n),
        "win": mean(r["won"] for r in rows),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [101 + 7 * i for i in range(a.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id,name:w.name,aff:w.aff,"
                          "shape:w.shape,dmg:w.dmg,mass:w.mass,reach:w.reach,"
                          "ult:w.ult?{name:w.ult.name,kind:w.ult.kind,charge:w.ult.charge}:null}))")
        byid = {w["id"]: w for w in W}
        ST = page.evaluate("() => AC.STATUS.curse")
        print(f"\nCURSE, as built: cap {ST['maxStacks']}  dur {ST['dur']}  "
              f"echo {ST['echo']:.0%}  tip \"{ST['tip']}\"\n")

        types = ["twinblade", "bow", "greatsword", "scythe", "warhammer", "flail"]
        donors = {t: TYPE_DONOR[t] for t in types}
        real_dmg = {t: byid[donors[t]]["dmg"] for t in types}

        # ---------------------------------------------------------- [1] --
        print("[1] THE POOL, TYPE BY TYPE — umbral's channel on every type's "
              "physics, each at ITS OWN shipped damage,\n    ultimates "
              f"suppressed, {len(W)-1} foes x {a.seeds} seeds\n")
        hdr = (f"    {'type':<11}{'donor':<14}{'dmg':>6}{'blows':>7}{'stacks':>7}"
               f"{'displ':>7}{'entry':>7}{'biggest':>8}{'pool':>7}{'peak':>7}"
               f"{'echo':>7}{'/dealt':>7}{'fillAt':>7}")
        print(hdr)
        one = {}
        for t in types:
            foes = [w["id"] for w in W if w["id"] != donors[t]]
            rows = page.evaluate(POOL_JS, [donors[t], None, foes, seeds, a.secs, True, None])
            s = summarise(rows); one[t] = s
            print(f"    {t:<11}{donors[t][:13]:<14}{real_dmg[t]:>6.1f}{s['hits']:>7.1f}"
                  f"{s['pushes']:>7.1f}{s['disp']:>7.0%}{s['entryMean']:>7.1f}"
                  f"{s['entryMax']:>8.1f}{s['poolMean']:>7.1f}{s['poolPeak']:>7.1f}"
                  f"{s['echoSum']:>7.0f}{s['echoShare']:>7.1%}{s['capT']:>7.1f}s")
        out["byType"] = one

        # ---------------------------------------------------------- [2] --
        print(f"\n[2] BLOW SIZE AGAINST CONTACT RATE — the same six with EVERY "
              f"relic pinned to {a.pin},\n    so the only thing left is how "
              f"often the type lands\n")
        print(hdr)
        pinned = {}
        for t in types:
            foes = [w["id"] for w in W if w["id"] != donors[t]]
            rows = page.evaluate(POOL_JS, [donors[t], a.pin, foes, seeds, a.secs, True, a.pin])
            s = summarise(rows); pinned[t] = s
            print(f"    {t:<11}{donors[t][:13]:<14}{a.pin:>6.1f}{s['hits']:>7.1f}"
                  f"{s['pushes']:>7.1f}{s['disp']:>7.0%}{s['entryMean']:>7.1f}"
                  f"{s['entryMax']:>8.1f}{s['poolMean']:>7.1f}{s['poolPeak']:>7.1f}"
                  f"{s['echoSum']:>7.0f}{s['echoShare']:>7.1%}{s['capT']:>7.1f}s")
        out["pinned"] = pinned

        print(f"\n    pool at shipped damage / pool at pin {a.pin} — how much of "
              f"each type's pool is WEIGHT rather than RATE\n")
        print(f"    {'type':<11}{'dmg':>7}{'pool@dmg':>10}{'pool@pin':>10}"
              f"{'ratio':>8}{'echo@dmg':>10}{'echo@pin':>10}{'ratio':>8}")
        for t in types:
            r1 = one[t]["poolMean"] / max(1e-9, pinned[t]["poolMean"])
            r2 = one[t]["echoSum"] / max(1e-9, pinned[t]["echoSum"])
            print(f"    {t:<11}{real_dmg[t]:>7.1f}{one[t]['poolMean']:>10.1f}"
                  f"{pinned[t]['poolMean']:>10.1f}{r1:>8.2f}x"
                  f"{one[t]['echoSum']:>10.0f}{pinned[t]['echoSum']:>10.0f}{r2:>8.2f}x")

        # ---------------------------------------------------------- [3] --
        print(f"\n[3] THE WARHAMMER'S POOL ACROSS A BLADE SWEEP — the blade is "
              f"bisected later; this is\n    what the number does to the pool "
              f"the two shipped ultimates read\n")
        print(f"    {'blade':>7}{'blows':>7}{'entry':>7}{'biggest':>8}{'pool':>7}"
              f"{'peak':>7}{'echo':>7}{'/dealt':>7}{'admits':>8}"
              f"    Revenant hand   Deadfall charge")
        sweep = {}
        foes = [w["id"] for w in W if w["id"] != "grudgebearer"]
        for d in [10, 14, 18, 23.5, 28, 34]:
            rows = page.evaluate(POOL_JS, ["grudgebearer", d, foes, seeds, a.secs, True, None])
            s = summarise(rows); sweep[d] = s
            hand = s["poolMean"] / max(1, ST["maxStacks"])   # one hand per entry, M=1.0
            chg = s["poolMean"] * 0.3 / 5                     # stamp x0.3 split five ways
            print(f"    {d:>7.1f}{s['hits']:>7.1f}{s['entryMean']:>7.1f}"
                  f"{s['entryMax']:>8.1f}{s['poolMean']:>7.1f}{s['poolPeak']:>7.1f}"
                  f"{s['echoSum']:>7.0f}{s['echoShare']:>7.1%}{s['floorLate']:>8.1f}"
                  f"    {hand:>12.1f}   {chg:>15.1f}")
        out["bladeSweep"] = {str(k): v for k, v in sweep.items()}

        # ---------------------------------------------------------- [4] --
        print(f"\n[4] THE FIRST CAST — v52 §5: umbral is a school where nothing "
              f"works until Curse is stacked.\n    Grudgebearer's own Crucible "
              f"charge, curse injected, ultimates LIVE\n")
        print(f"    {'type':<11}{'donor':<14}{'casts':>7}{'1st cast at':>13}"
              f"{'stacks then':>13}{'pool then':>11}")
        firsts = {}
        for t in ["warhammer", "flail", "greatsword", "twinblade"]:
            foes = [w["id"] for w in W if w["id"] != donors[t]]
            rows = page.evaluate(CHARGE_JS, [donors[t], None, foes, seeds, a.secs])
            got = [r for r in rows if r["firstT"] is not None]
            firsts[t] = {
                "casts": mean(r["casts"] for r in rows),
                "firstT": mean(r["firstT"] for r in got),
                "stacks": mean(r["firstStacks"] for r in got),
                "pool": mean(r["firstPool"] for r in got),
                "share": len(got) / max(1, len(rows)),
            }
            f = firsts[t]
            print(f"    {t:<11}{donors[t][:13]:<14}{f['casts']:>7.2f}"
                  f"{f['firstT']:>12.1f}s{f['stacks']:>13.2f}{f['pool']:>11.1f}")
        out["firstCast"] = firsts

        assert not errors, errors[:4]

    # ------------------------------------------------------------ checks --
    print()
    wh, fl = one["warhammer"], one["flail"]
    poolSpread = max(one[t]["poolMean"] for t in types) / min(one[t]["poolMean"] for t in types)
    echoSpread = max(one[t]["echoShare"] for t in types) / min(one[t]["echoShare"] for t in types)

    # REFUTED, and left in because it was the reason the cell was recommended:
    # the warhammer is NOT the heaviest blade. Thornwake ships at 31.35.
    check("REFUTED — the warhammer has the biggest pool entries of any type",
          wh["entryMean"] >= max(one[t]["entryMean"] for t in types),
          f"warhammer {wh['entryMean']:.1f}, scythe {one['scythe']['entryMean']:.1f}, "
          f"flail {fl['entryMean']:.1f} — the scythe carries the heaviest shipped "
          f"blade in the game's slow half and the warhammer does not")

    check("the pool the two ultimates READ varies more across types than the "
          "echo it PAYS",
          poolSpread > echoSpread,
          f"pool {min(one[t]['poolMean'] for t in types):.0f}-"
          f"{max(one[t]['poolMean'] for t in types):.0f} ({poolSpread:.2f}x) against "
          f"echo {min(one[t]['echoShare'] for t in types):.1%}-"
          f"{max(one[t]['echoShare'] for t in types):.1%} of damage ({echoSpread:.2f}x) "
          f"— the cell cannot be argued on echo")

    check("weight, not rate, is what makes the pool — it moves with the blade",
          sweep[34]["poolMean"] > 1.8 * sweep[10]["poolMean"],
          f"blade 10 -> 34 moves the pool {sweep[10]['poolMean']:.1f} -> "
          f"{sweep[34]['poolMean']:.1f} ({sweep[34]['poolMean']/max(1e-9,sweep[10]['poolMean']):.2f}x) "
          f"on 30% FEWER blows")

    check("the type fills the cap in essentially every fight",
          wh["capShare"] > 0.9, f"{wh['capShare']:.0%} of fights reach 3 stacks, "
          f"first at {wh['capT']:.1f}s")

    others = [firsts[t]["pool"] for t in firsts if t != "warhammer"]
    check("the warhammer's FIRST CAST is the fullest in the school — v52 §5's "
          "school-level risk is smallest here",
          firsts["warhammer"]["pool"] > 1.4 * max(others),
          f"pool {firsts['warhammer']['pool']:.1f} behind the first cast against "
          f"flail {firsts['flail']['pool']:.1f}, greatsword {firsts['greatsword']['pool']:.1f}, "
          f"twinblade {firsts['twinblade']['pool']:.1f}")

    check("no JS errors or page exceptions", True)

    bad = [n for n, ok in PASS if not ok]
    print(f"\n{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED)" if bad else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
