#!/usr/bin/env python3
"""CURSE AS A ROLLING WINDOW OF THE LAST 3 HITS. Rick, 2026-09-01.

The shipped rule keeps the THREE BIGGEST blows ever landed, forever:

    pushCurse(v,n){ push; sort descending; length = maxStacks; }

The proposal keeps the THREE MOST RECENT, whatever their size:

    pushCurse(v,n){ push; while (length > maxStacks) shift(); }

That is not a relic change. It is a change to the school, and it reaches
Gravemourn, Nightfell, Twinshade, Shroudmaul, the Gloamwire build Code has
open right now, and the umbral scythe being designed in this document.

Three measurements, runtime injection only, nothing written to any build:

  [1] UNIT CHECK. Three big memories then three small ones must leave the pool
      SMALL under FIFO and BIG under top-3. A rule change that does not show up
      here is not installed.
  [2] IS CURSE STILL FLAT ACROSS WEAPONS? v49 chose a small cap to narrow the
      gap between a 5.6-blow flail and a 25.7-blow twinblade; v60 s4 measured
      the result at 82-117 total echo for every type in the game. FIFO should
      invert that -- a weapon that hits often flushes its own pool.
  [3] WHAT IT DOES TO THE FOUR BUILT UMBRAL RELICS, head to head.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, "/mnt/user-data/uploads/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="/mnt/user-data/uploads/sundered-crown/02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=30)
ap.add_argument("--out", default="/tmp/curse_fifo.json")
a = ap.parse_args()

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
  // [1] UNIT CHECK
  const f = m0.a;
  f.cursePool.length = 0;
  f.pushCurse(100, 3);
  const big = f.cursePool.slice();
  f.pushCurse(5, 3);
  const after = f.cursePool.slice();
  return { mode, big, after, sum: after.reduce((x,y)=>x+y,0) };
}"""

ECHO_JS = r"""([donor, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral"; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    let step = 0, echoTot = 0, samples = 0, sumAcc = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      if (step % 60 === 0){ sumAcc += foe.curseSum(); samples++; }
    }
    rows.push({ hits: me.hits, dealt: me.dealt, poolMean: sumAcc / Math.max(samples,1),
                win: m.winner ? (m.winner === me ? 1 : 0) : -1 });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return rows;
}"""

RELIC_JS = r"""([id, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    out.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1 });
  }
  return out;
}"""

TYPE_DONOR = {"greatsword":"dawnbringer","twinblade":"widowmaker","warhammer":"grudgebearer",
              "scythe":"thornwake","flail":"gravemourn","bow":"ironhail"}

with game(game_path=pathlib.Path(a.game)) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    seeds = [12101 + 47*i for i in range(a.seeds)]
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    t0 = time.time(); res = {}
    print("\n[1] UNIT CHECK — three memories of 100, then three of 5\n")
    for mode in ("top3", "fifo"):
        u = page.evaluate(INSTALL, mode)
        print(f"    {mode:<6} after 3x100: {u['big']}   after 3x5: {u['after']}   sum {u['sum']:.0f}")
        res[f"unit_{mode}"] = u
    ok = (res["unit_top3"]["sum"] == 300 and res["unit_fifo"]["sum"] == 15)
    print(f"    {'PASS — the rule change is installed' if ok else 'FAIL — injection not reaching pushCurse'}")

    print(f"\n[2] IS CURSE STILL FLAT ACROSS WEAPONS? "
          f"{len(panel)}x{a.seeds} fights a cell\n")
    print(f"    {'type':<12}{'blows':>8}{'POOL top3':>12}{'POOL fifo':>12}"
          f"{'echo/blow top3':>17}{'echo/blow fifo':>16}{'total echo top3':>18}{'fifo':>9}")
    flat = {}
    for typ, donor in TYPE_DONOR.items():
        foes = [p for p in panel if p != donor]
        row = {}
        for mode in ("top3", "fifo"):
            page.evaluate(INSTALL, mode)
            rs = page.evaluate(ECHO_JS, [donor, foes, seeds, 120.0])
            assert not errors, errors[:3]
            row[mode] = { "hits": statistics.mean([r["hits"] for r in rs]),
                          "pool": statistics.mean([r["poolMean"] for r in rs]) }
        h = row["top3"]["hits"]
        e3, ef = row["top3"]["pool"]*0.08, row["fifo"]["pool"]*0.08
        flat[typ] = {"hits": h, "pool3": row["top3"]["pool"], "poolf": row["fifo"]["pool"],
                     "tot3": e3*h, "totf": ef*row["fifo"]["hits"]}
        print(f"    {typ:<12}{h:>8.1f}{row['top3']['pool']:>12.1f}{row['fifo']['pool']:>12.1f}"
              f"{e3:>17.2f}{ef:>16.2f}{e3*h:>18.0f}{ef*row['fifo']['hits']:>9.0f}")
    t3 = [v["tot3"] for v in flat.values()]; tf = [v["totf"] for v in flat.values()]
    print(f"\n    spread across weapons — top3: {min(t3):.0f} to {max(t3):.0f} "
          f"({max(t3)/max(min(t3),1e-9):.1f}x)    fifo: {min(tf):.0f} to {max(tf):.0f} "
          f"({max(tf)/max(min(tf),1e-9):.1f}x)")

    print(f"\n[3] THE FOUR BUILT UMBRAL RELICS, top3 vs fifo, vs the whole field\n")
    print(f"    {'relic':<14}{'ultimate':<12}{'top3':>10}{'fifo':>10}{'move':>10}")
    relics = {}
    for id_ in ("gravemourn","nightfell","twinshade","shroudmaul"):
        foes = [i for i in ids if i != id_]
        r = {}
        for mode in ("top3","fifo"):
            page.evaluate(INSTALL, mode)
            rs = page.evaluate(RELIC_JS, [id_, foes, seeds[:12], 120.0])
            assert not errors, errors[:3]
            r[mode] = statistics.mean([x["win"] for x in rs if x["win"] >= 0])
        relics[id_] = r
        ult = {"gravemourn":"Revenant","nightfell":"Deadfall",
               "twinshade":"Triplicate","shroudmaul":"Grasp"}[id_]
        print(f"    {id_:<14}{ult:<12}{r['top3']:>10.1%}{r['fifo']:>10.1%}"
              f"{(r['fifo']-r['top3'])*100:>+9.1f}pp")
    page.evaluate(INSTALL, "top3")
    json.dump({"flat": flat, "relics": relics}, open(a.out, "w"), indent=1)
    print(f"\n    done in {time.time()-t0:.0f}s   errors: {errors}")
