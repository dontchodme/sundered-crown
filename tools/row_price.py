#!/usr/bin/env python3
"""PRICE A WHOLE ROW BY DELIVERED EFFECT, NOT BY OCCUPANCY.

    python3 row_price.py --type scythe --game ../02-chain/sc-paradox-ignition.html

`cell_survey` [4] ranks a cell on time-weighted STACK OCCUPANCY. That column
has now mispriced three cells: the umbral row (v40 §4.1), runic x flail
(v43 §4) and verdant x twinblade (v47). The failure is the same every time —
occupancy is a proxy twice removed for a status that is a RATE (v39 5.2), and
worse for one whose worth depends on the FOE'S MODE (v47 twinblade survey §4,
where entangle is -33% against a swinging foe and +3% against a bow).

**And cell_survey does not say so in its own output**, which is v47's open
decision 1. This is that column: one model-free A/B per open cell, the
school's channel live against the same weapon with the channel deleted,
against the WHOLE ROSTER rather than a five-relic field — because a foe field
that misweights the modes decides the table by itself.

It designs nothing and proposes nothing. It ranks the row twice and prints the
disagreement.

  [1] THE ROW. Which cells are open, read from AC.WEAPONS.
  [2] OCCUPANCY, as cell_survey computes it — imported, not transcribed, so the
      two tools cannot drift.
  [3] DELIVERED EFFECT. Channel live against channel deleted. Vigil has no foe
      channel and gets an onSelf arm instead, which is the only way its cell
      can appear in the same table at all.
  [4] THE DISAGREEMENT. Spearman-style rank comparison, printed whether or not
      it is large, because a session that only reports the column when it
      disagrees is a session that has stopped testing it.

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
from cell_survey import CLOCK_JS  # noqa: E402

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

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape, mode: w.mode,
    dmg: w.dmg, mass: w.mass, spin: w.spin, reach: w.reach,
    onHit: w.onHit ? Object.entries(w.onHit)[0] : null,
    onSelf: w.onSelf ? Object.entries(w.onSelf)[0] : null,
  }));
  const S = {};
  for (const [k, v] of Object.entries(AC.STATUS))
    S[k] = { maxStacks: v.maxStacks, dur: v.dur, dps: v.dps ?? null,
             spin: v.spin ?? null, move: v.move ?? null,
             taken: v.taken ?? null, tip: v.tip || "" };
  return { weapons: W, status: S, affinities: Object.keys(AC.AFFINITIES) };
}"""

# THE ARM. One slot, one key, one A/B. `slot` is "onHit" or "onSelf" so vigil's
# ward can be priced on the same axis as the six foe channels rather than being
# left out of the table with a dash, which is what cell_survey does today and
# is why no vigil cell has ever been ranked against its own row.

CH2_JS = r"""([donor, aff, slot, key, per, foes, seeds, secs, pin, pinIds, noult, on]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = aff;
  delete w.onHit; delete w.onSelf;
  if (on && key){ const o = {}; o[key] = per; w[slot] = o; }

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
      const mh0 = th.maxHp;
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      rows.push({ foe: f, foeMode: th.w.mode, seed: sd,
                  hpCut: mh0 - th.maxHp, maxHp0: mh0,
                  dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, foeHits: th.hits,
                  dealt: me.dealt, taken: th.dealt,
                  meHp: me.hp, thHp: th.hp });
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
    ap.add_argument("--type", default="scythe")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--taken", default="", help="extra cells to price, aff x type")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [2207 + 11 * i for i in range(a.seeds)]
    T = a.type
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        g = page.evaluate(GRID_JS)
        W, ST = g["weapons"], g["status"]
        by_id = {w["id"]: w for w in W}
        schools = sorted(set({w["aff"] for w in W}) | set(g["affinities"]))
        filled = {(w["aff"], w["shape"]): w["name"] for w in W}
        chan = {}
        for s in schools:
            rel = [w for w in W if w["aff"] == s]
            if not rel:
                continue
            r0 = rel[0]
            chan[s] = {"onHit": r0["onHit"], "onSelf": r0["onSelf"]}
        donor = TYPE_DONOR[T]
        allfoes = [w["id"] for w in W if w["id"] != donor]
        pin_ids = [w["id"] for w in W]
        openc = [s for s in schools if (s, T) not in filled]

        print(f"\n[1] THE {T.upper()} ROW — donor {donor}, "
              f"{len(openc)} of {len(schools)} cells open\n")
        print(f"    {'':<12}" + "".join(f"{s[:11]:>12}" for s in schools))
        print(f"    {T:<12}"
              + "".join(f"{filled.get((s, T), '·')[:11]:>12}" for s in schools))
        print(f"\n    open: " + ", ".join(f"{s} x {T}" for s in openc))

        # ------------------------------------------------------------ [2] --
        print(f"\n[2] OCCUPANCY — cell_survey's own column, imported\n")
        print(f"    {'cell':<24}{'status':<12}{'hits/s':>8}{'mean':>7}{'>=2':>7}"
              f"{'cap':>7}{'appl':>7}{'refr':>7}")
        occ = {}
        occ_foes = [w["id"] for w in W if w["id"] != donor][:4]
        for s in openc:
            ch = chan[s]["onHit"]
            if not ch:
                print(f"    {s + ' x ' + T:<24}{'— no onHit channel —':<12}")
                continue
            k, per = ch
            rows = page.evaluate(CLOCK_JS, [donor, s, k, per, occ_foes, seeds,
                                            a.pin, pin_ids, a.secs])
            dur = sum(r["dur"] for r in rows)
            occ[s] = {"status": k, "hps": sum(r["hits"] for r in rows) / dur,
                      "mean": mean(r["meanStacks"] for r in rows),
                      "p2": mean(r["p2"] for r in rows),
                      "cap": mean(r["pMax"] for r in rows),
                      "apps": mean(r["apps"] for r in rows),
                      "refr": sum(r["refresh"] for r in rows)
                              / max(1, sum(r["apps"] for r in rows))}
            o = occ[s]
            print(f"    {s + ' x ' + T:<24}{k:<12}{o['hps']:>8.3f}{o['mean']:>7.2f}"
                  f"{o['p2']:>7.0%}{o['cap']:>7.0%}{o['apps']:>7.1f}{o['refr']:>7.0%}")

        # ------------------------------------------------------------ [3] --
        print(f"\n[3] DELIVERED EFFECT — channel live against channel deleted, "
              f"against all {len(allfoes)} other relics, "
              f"{len(allfoes) * len(seeds)} fights an arm\n")
        print(f"    {'cell':<24}{'slot':<8}{'status':<12}{'dealt/s':>9}"
              f"{'taken/s':>9}{'foe blows/s':>13}{'win':>8}{'lift':>8}")
        eff = {}
        for s in openc:
            ch, slot = chan[s]["onHit"], "onHit"
            if not ch:
                ch, slot = chan[s]["onSelf"], "onSelf"
            if not ch:
                continue
            k, per = ch
            on = page.evaluate(CH2_JS, [donor, s, slot, k, per, allfoes, seeds,
                                        a.secs, a.pin, pin_ids, True, True])
            off = page.evaluate(CH2_JS, [donor, s, slot, k, per, allfoes, seeds,
                                         a.secs, a.pin, pin_ids, True, False])
            dOn = sum(r["dur"] for r in on)
            dOff = sum(r["dur"] for r in off)
            fOn = [r for r in on if r["win"] >= 0]
            fOff = [r for r in off if r["win"] >= 0]
            rec = {"slot": slot, "status": k, "per": per,
                   "dps": sum(r["dealt"] for r in on) / dOn,
                   "tps": sum(r["taken"] for r in on) / dOn,
                   "fbps": sum(r["foeHits"] for r in on) / dOn,
                   "win": mean(r["win"] for r in fOn),
                   "winOff": mean(r["win"] for r in fOff),
                   "dpsOff": sum(r["dealt"] for r in off) / dOff,
                   "tpsOff": sum(r["taken"] for r in off) / dOff,
                   "hpCut": mean(r["hpCut"] for r in on),
                   "maxHp0": mean(r["maxHp0"] for r in on),
                   "totalDealt": sum(r["dealt"] for r in on) / len(on),
                   "totalDealtOff": sum(r["dealt"] for r in off) / len(off),
                   "byMode": {}}
            for md in ("ranged", "swing", "spin", "chain"):
                a2 = [r for r in fOn if r["foeMode"] == md]
                b2 = [r for r in fOff if r["foeMode"] == md]
                if a2 and b2:
                    rec["byMode"][md] = mean(r["win"] for r in a2) - mean(r["win"] for r in b2)
            eff[s] = rec
            print(f"    {s + ' x ' + T:<24}{slot:<8}{k:<12}{rec['dps']:>9.2f}"
                  f"{rec['tps']:>9.2f}{rec['fbps']:>13.3f}{rec['win']:>8.1%}"
                  f"{rec['win'] - rec['winOff']:>+8.1%}")

        # WHAT THE CHANNEL ACTUALLY DELIVERED INTO THE FOE, so a channel that
        # is weak can be told apart from a channel that never arrived. Curse
        # is the case this column exists for: `apply` lowers maxHp and the
        # per-frame `f.hp = Math.min(f.hp, f.maxHp)` turns that into real
        # health removed, so "it did nothing" and "it did a lot and it did not
        # matter" are two different findings.
        print(f"\n    what each channel put INTO the foe over a whole fight\n")
        print(f"    {'cell':<24}{'blade damage':>14}{'no-channel blade':>18}"
              f"{'channel delta':>15}{'max hp removed':>16}")
        for s, rec in eff.items():
            print(f"    {s + ' x ' + T:<24}{rec['totalDealt']:>14.0f}"
                  f"{rec['totalDealtOff']:>18.0f}"
                  f"{rec['totalDealt'] - rec['totalDealtOff']:>+15.0f}"
                  f"{rec['hpCut']:>13.0f} of {rec['maxHp0']:.0f}")

        print(f"\n    the lift, split by the FOE'S MODE — v47's finding was that a "
              f"channel's worth is decided here\n")
        print(f"    {'cell':<24}" + "".join(f"{m:>10}" for m in
                                            ("ranged", "swing", "spin", "chain")))
        for s, rec in eff.items():
            print(f"    {s + ' x ' + T:<24}"
                  + "".join(f"{rec['byMode'].get(m, 0):>+10.1%}"
                            for m in ("ranged", "swing", "spin", "chain")))

        # ------------------------------------------------------------ [4] --
        print(f"\n[4] DO THE TWO COLUMNS AGREE?\n")
        shared = [s for s in eff if s in occ]
        if len(shared) >= 2:
            occ_rank = sorted(shared, key=lambda s: -occ[s]["p2"])
            eff_rank = sorted(shared, key=lambda s: -(eff[s]["win"] - eff[s]["winOff"]))
            print(f"    by occupancy (>=2 stacks):  "
                  + " > ".join(f"{s} {occ[s]['p2']:.0%}" for s in occ_rank))
            print(f"    by delivered effect:        "
                  + " > ".join(f"{s} {eff[s]['win']-eff[s]['winOff']:+.1%}"
                               for s in eff_rank))
            agree = occ_rank[0] == eff_rank[0]
            check("the two columns pick the same top cell on this row",
                  agree,
                  ("they agree on " + occ_rank[0]) if agree else
                  f"occupancy says {occ_rank[0]}, delivered effect says "
                  f"{eff_rank[0]} — a FOURTH row where the occupancy column "
                  f"does not rank what it is read as ranking")
        vig = [s for s in openc if not chan[s]["onHit"]]
        check("a school with no foe channel is priced on the same axis as the "
              "others rather than printed as a dash",
              all(s in eff for s in vig),
              f"{', '.join(vig) or 'none on this row'} — cell_survey prints "
              f"'— vigil has no onHit channel —' and ranks it nowhere")
        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))
        out = {"type": T, "open": openc, "occupancy": occ, "delivered": eff}

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
