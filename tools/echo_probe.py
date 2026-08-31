#!/usr/bin/env python3
"""RICK'S IMPALE-SHAPED CURSE, MEASURED BEFORE IT IS BUILT.

Rick's design: a curse stack REMEMBERS the damage of the hit that applied it.
Every later hit deals a share of the sum of everything remembered. Stacks cap
at K; a new stack displaces the WEAKEST one, so the pool converges on the
wielder's K biggest hits.

Injection is runtime-only. NOTHING is written to any build.

WHAT THE INJECTION IS NOT
-------------------------
The echo is paid as a SEPARATE hurt() immediately after the blow, not folded
into the blow's own damage number. So in this instrument the echo does not
scale hit-stop, knockback or hitstun, is not blocked by an Aegis wall, and
does not roll its own crit. A real build would fold it in before hurt() and
those four would follow. Every number below is therefore a floor on the
mechanic's spectacle and a fair reading of its DAMAGE.

Ult-applied curse (Dirge's 3, Eclipse's 3) remembers NOTHING here -- an
ultimate has no per-stack hit damage to remember. Arms run with ults
suppressed so this never fires; it is an open design question, not a bug.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
UMBRAL = ["gravemourn", "nightfell", "twinshade"]

ARM_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult, arm, K, RATE]) => {
  const DT = AC.CONFIG.physics.dt;
  const CU = AC.STATUS.curse;
  const origLoss = CU.maxHpLoss, origCap = CU.maxStacks;
  const origResolve = AC.Match.prototype.resolveHit;
  const BOTTOM = origLoss;                       // 13, the v47 control's size

  if (arm !== "shipped") CU.maxHpLoss = 0;
  if (arm === "echo") CU.maxStacks = K;          // chip and pool agree

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }
  const dw = AC.WEAPONS.find(x => x.id === donor);
  const ULTD = (dw.ult && dw.ult.dmg) || 0;      // what an ult-applied stack remembers

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      let echoDealt = 0, baseDealt = 0, hits = 0, capAt = -1, poolSum = 0, poolN = 0;
      let bottomDealt = 0, ultStacks = 0;
      const pool = [];
      let inResolve = false, hitD0 = 0;

      /* INSTANCE SHADOW on the foe's applier: catches EVERY curse application,
         the blow's own onHit and the ultimate's alike. Inside a blow the
         remembered value is that blow's damage, which `resolveHit` has already
         added to `me.dealt` by the time onHit runs. Outside one -- Dirge,
         Eclipse -- there is no per-stack blow to remember, so the ULT's own
         damage number stands in. That choice is a design decision, not a
         measurement, and it is flagged as such. */
      const origApply = th.apply.bind(th);
      th.apply = function(key, n){
        if (key === "curse"){
          if (arm === "echo"){
            const v = inResolve ? (me.dealt - hitD0) : ULTD;
            if (!inResolve) ultStacks += n;
            if (v > 0){
              for (let i = 0; i < n; i++) pool.push(v);
              pool.sort((x, y) => y - x);
              while (pool.length > K) pool.pop();
              if (pool.length >= K && capAt < 0) capAt = hits;
            }
          } else if (arm === "bottom"){
            const b = th.hp; th.hp -= BOTTOM * n; bottomDealt += b - th.hp;
          }
        }
        return origApply(key, n);
      };

      if (arm === "echo"){
        m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
          if (!(self === me && foe === th))
            return origResolve.call(this, self, foe, hx, hy, seg, mul, over);
          const d0 = self.dealt, h0 = self.hits;
          let s = 0; for (const v of pool) s += v;
          const echo = Math.round(s * RATE);
          inResolve = true; hitD0 = d0;
          origResolve.call(this, self, foe, hx, hy, seg, mul, over);
          inResolve = false;
          if (self.hits === h0) return;
          hits++; baseDealt += self.dealt - d0; poolSum += s; poolN++;
          if (echo > 0 && foe.alive){ this.hurt(foe, echo, self); echoDealt += echo; }
        };
      }

      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      let s = 0; for (const v of pool) s += v;
      rows.push({ foe: f, seed: sd, dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  dealt: me.dealt, taken: th.dealt, myHits: me.hits, foeHits: th.hits,
                  echoDealt, baseDealt, hits, capAt, ultStacks, bottomDealt,
                  capped: capAt > 0 ? 1 : 0,
                  poolEnd: s, poolMean: poolN ? poolSum / poolN : 0,
                  thHp: th.hp, thMaxHp: th.maxHp });
    }
  }

  CU.maxHpLoss = origLoss; CU.maxStacks = origCap;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""

HITS_JS = r"""([ids, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = {};
  for (const id of ids){
    const hs = [], ds = [], durs = [];
    for (const f of ids){
      if (f === id) continue;
      for (const sd of seeds){
        const m = new AC.Match(id, f, sd);
        const me = m.a.w.id === id ? m.a : m.b;
        let step = 0;
        while (!m.over && step < secs / DT){ m.step(DT); step++; }
        hs.push(me.hits); ds.push(me.dealt); durs.push(step * DT);
      }
    }
    hs.sort((a,b)=>a-b);
    out[id] = { mean: hs.reduce((a,b)=>a+b,0)/hs.length,
                p10: hs[Math.floor(hs.length*0.10)], med: hs[Math.floor(hs.length*0.5)],
                p90: hs[Math.floor(hs.length*0.90)],
                dur: durs.reduce((a,b)=>a+b,0)/durs.length,
                dmgPerHit: ds.reduce((a,b)=>a+b,0)/Math.max(1,hs.reduce((a,b)=>a+b,0)) };
  }
  return out;
}"""


def wr(rows):
    fin = [r for r in rows if r["win"] >= 0]
    return (sum(r["win"] for r in fin) / len(fin) if fin else float("nan")), len(fin), len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=24.0)
    ap.add_argument("--stage", default="hits")
    ap.add_argument("--ults", action="store_true")
    ap.add_argument("--grid", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = pathlib.Path(a.game)
    gp = gp if gp.is_absolute() else (HERE / gp).resolve()
    seeds = [3301 + 19 * i for i in range(a.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, aff:w.aff, shape:w.shape, dmg:w.dmg}))")
        ids = [w["id"] for w in W]
        byid = {w["id"]: w for w in W}

        if a.stage == "hits":
            print("\n[1] THE HIT BUDGET — how many blows a relic lands in a whole fight")
            print("    shipped damage, ultimates ON, whole roster, "
                  f"{a.seeds} seeds = {(len(ids)-1)*a.seeds} fights a relic\n")
            h = page.evaluate(HITS_JS, [ids, seeds, a.secs])
            out["hits"] = h
            print(f"    {'relic':14}{'shape':12}{'dmg':>7}{'hits/fight':>11}"
                  f"{'p10':>6}{'med':>6}{'p90':>6}{'dur':>7}{'dmg/hit':>9}")
            for k in sorted(h, key=lambda x: -h[x]["mean"]):
                w = byid[k]
                print(f"    {k:14}{w['shape']:12}{w['dmg']:>7.1f}{h[k]['mean']:>11.1f}"
                      f"{h[k]['p10']:>6}{h[k]['med']:>6}{h[k]['p90']:>6}"
                      f"{h[k]['dur']:>7.1f}{h[k]['dmgPerHit']:>9.1f}")

        if a.stage in ("arms", "ship"):
            pin = a.pin if a.stage == "arms" else 0
            grid = [tuple(float(y) if "." in y else int(y) for y in x.split(":"))
                    for x in a.grid.split(",")] if a.grid else [(3, 0.25), (5, 0.25)]
            u = "ults ON" if a.ults else "ults suppressed"
            label = (("damage PINNED at %.0f, " % pin) + u + " — the v47 column"
                     if pin else "SHIPPED damage, " + u + " — the real roster")
            print(f"\n[2] THE ARMS — {label}")
            print(f"    {a.seeds} seeds x 25 foes = {25*a.seeds} fights an arm\n")
            arms = [("none", 0, 0.0), ("shipped", 0, 0.0), ("bottom", 0, 0.0)] + [("echo", k, r) for k, r in grid]
            res = {}
            hdr = f"    {'donor':14}" + "".join(
                f"{(nm if nm!='echo' else 'K%d r%.0f%%'%(k, r*100)):>12}" for nm, k, r in arms)
            print(hdr)
            for donor in UMBRAL:
                foes = [i for i in ids if i != donor]
                cells, det = [], {}
                for nm, k, r in arms:
                    rows = page.evaluate(ARM_JS, [donor, foes, seeds, a.secs, pin,
                                                  ids, not a.ults, nm, k, r])
                    w, n, tot = wr(rows)
                    cells.append(f"{w:.1%}")
                    key = nm if nm != "echo" else f"echo{k}_{r}"
                    det[key] = {"win": w, "fin": n, "tot": tot,
                                "echo": statistics.mean([x["echoDealt"] for x in rows]),
                                "base": statistics.mean([x["baseDealt"] for x in rows]),
                                "hits": statistics.mean([x["hits"] for x in rows]),
                                "capAt": statistics.mean([x["capAt"] for x in rows if x["capAt"] > 0] or [0]),
                                "poolMean": statistics.mean([x["poolMean"] for x in rows]),
                                "dur": statistics.mean([x["dur"] for x in rows]),
                                "capped": statistics.mean([x["capped"] for x in rows]),
                                "ultStk": statistics.mean([x["ultStacks"] for x in rows]),
                                "bottom": statistics.mean([x["bottomDealt"] for x in rows])}
                res[donor] = det
                print(f"    {donor:14}" + "".join(f"{c:>12}" for c in cells))
            out["arms" if pin else "ship"] = res

            print(f"\n    ECHO CHANNEL — what the mechanic actually delivered")
            print(f"    {'donor':14}{'arm':>10}{'hits':>7}{'cap@':>7}{'pool':>8}"
                  f"{'base dmg':>10}{'echo dmg':>10}{'uplift':>9}{'capped':>8}{'ultStk':>8}")
            for donor in UMBRAL:
                for key, d in res[donor].items():
                    if not key.startswith("echo"): continue
                    up = d["echo"] / d["base"] if d["base"] else 0
                    print(f"    {donor:14}{key.replace('echo','K').replace('_',' r'):>10}"
                          f"{d['hits']:>7.1f}{d['capAt']:>7.1f}{d['poolMean']:>8.1f}"
                          f"{d['base']:>10.0f}{d['echo']:>10.0f}{up:>8.0%}"
                          f"{d['capped']:>7.0%}{d['ultStk']:>8.1f}")

        assert not errors, errors[:3]

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print("\nwrote", a.json)


main()
