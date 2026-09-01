#!/usr/bin/env python3
"""net_lab.py — GLOAMWIRE / CROSSWEAVE, priced before it is built.

    python net_lab.py --game ../02-chain/sc-breach.html --stage 1

Rick's §1, verbatim:
    "purple bow gains a triple shot. each arrow connected by a string of purple
     lightning. Enemies hit by an arrow take extra damage. enemies hit by only
     the lightning take no damage but take extra knockback. Enemies hit by both
     take both"
    "can we also give the ult increased fire rate?"

Design: 06-docs/v61/gloamwire-design-v61.md.  Brief: 06-docs/v61/GLOAMWIRE-BUILD-BRIEF.md.

Every patch is a runtime prototype wrapper installed ONCE, and every knob is
read off `w.ult` at the moment of use -- so a sweep changes numbers and never
re-patches. INJECTION IS RUNTIME-ONLY. NOTHING IS WRITTEN TO ANY BUILD.

  [0] ASSERTIONS, before any number is read. The five bows share one `shot`
      block byte for byte; an arrow and a swing deal the same base damage;
      curse is the reworked pool mechanic.

  [1] THE POOL, across the whole umbral school. The design's central claim is
      that a bow fills the curse memory FROM RANGE and therefore FASTEST.
      *** THIS IS GATE 1 OF THE BUILD BRIEF. Run it on the pin. ***

  [2] THE CROSSOVER. An arrow reaches R + shot.r = 58; a strand reaches
      R + strandW. They are equal at strandW = shot.r = 24, and Rick's three
      outcomes can only all exist near that line. Below it "hit by the lightning
      alone" is unreachable BY CONSTRUCTION; above it "hit by the arrow alone"
      is. Two controls that must come back at known values.

  [3] FAN AGAINST PARALLEL. A fan's gap grows with range; a parallel net's does
      not. Rick took the fan.

  [4] THE FIRE RATE, and the ceiling that could make the sweep lie:
      CONFIG.shot.maxLive is 64 and spawnShot SHIFTS at the cap. Measured, not
      assumed.

  [5] CONTACTS AS EVENTS. The first range table binned a VOLLEY by its FIRST
      contact, so a volley shoved at 250 and then hit by an arrow at 90 was
      filed as "no damage" and its arrow was never counted -- it reported an
      8-14% damage share where the volley accounting says 21%. The volley was
      the wrong unit. This records arrow contacts and strand contacts
      separately, each with its own range, and reconciles the two.

  [6] THE COMPOSITION and the magazine ladder.

  [7] WHAT THE ULTIMATE IS WORTH, ult_price's way, and what it does to the pool.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"    [{'ok ' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


def mean(xs):
    xs = list(xs)
    return statistics.mean(xs) if xs else float("nan")


def m_(rows, k):
    return mean(r[k] for r in rows)


def wr(rows):
    d = [r for r in rows if r["win"] >= 0]
    return (sum(r["win"] for r in d) / len(d)) if d else float("nan")


def base_ult(**kw):
    """The settled sheet. Every caller overrides only what it is sweeping."""
    u = dict(name="Crossweave", kind="net", charge=15,
             volleys=24, n=3, mode="fan", spread=0.90, cadMul=0.5,
             dmgMul=1.4, strandW=90, strandKnock=260, dur=99.0, tip="x")
    u.update(kw)
    return u


INSTALL_JS = r"""() => {
  if (window.__netInstalled) return "already";
  window.__netInstalled = true;
  const M = AC.Match.prototype, R = AC.CONFIG.physics.ballR;
  const oFire = M.fireUlt, oSpawn = M.spawnShot,
        oTick = M.tickShots, oResolve = M.resolveHit;

  /* point-segment distance; AC does not export its own */
  function segD(ax, ay, bx, by, px, py){
    const vx = bx - ax, vy = by - ay;
    const L = vx * vx + vy * vy;
    let t = L ? ((px - ax) * vx + (py - ay) * vy) / L : 0;
    t = t < 0 ? 0 : t > 1 ? 1 : t;
    const dx = px - (ax + vx * t), dy = py - (ay + vy * t);
    return Math.hypot(dx, dy);
  }
  M.__netInit = function(){ this.__volleys = []; this.__volleyId = 0; };

  M.fireUlt = function(f, foe){
    const u = f.w.ult;
    if (!u || u.kind !== "net") return oFire.call(this, f, foe);
    f.ultNet = { t: 0, dur: u.dur, left: (u.volleys || 0) };
    if (f.__net) f.__net.casts++;
  };

  M.spawnShot = function(f, angle){
    const u = f.w.ult, N = f.ultNet;
    if (!N || angle !== undefined || !u || u.kind !== "net")
      return oSpawn.call(this, f, angle);
    const n = u.n || 3, id = ++this.__volleyId, made = [];
    for (let k = 0; k < n; k++){
      const off = n === 1 ? 0 : (k - (n - 1) / 2);
      const a = u.mode === "fan" ? f.theta + off * u.spread : f.theta;
      const before = this.shots.length;
      oSpawn.call(this, f, a);
      if (this.shots.length === before) continue;
      const s = this.shots[this.shots.length - 1];
      if (u.mode !== "fan"){
        const px = -Math.sin(f.theta), py = Math.cos(f.theta);
        s.x += px * off * u.spread; s.y += py * off * u.spread;
      }
      s.dmgMul = u.dmgMul;
      s.netVolley = id; s.netIdx = k;
      made.push(s);
    }
    if (made.length > 1){
      this.__volleys.push({ id, own: f === this.a ? "a" : "b",
                            arrowHit: false, strandHit: false, struck: {},
                            hadStrand: false,
                            gapSum: 0, gapN: 0, bandSum: 0 });
      if (f.__net) f.__net.volleys++;
    }
    if (u.volleys && N.left > 0){ N.left--; if (N.left <= 0) f.ultNet = null; }
  };

  M.resolveHit = function(self, foe, hx, hy, seg, mul, over){
    const s = this._cineShot;
    if (s && s.netVolley && this.__volleys){
      const v = this.__volleys.find(q => q.id === s.netVolley);
      if (v) v.arrowHit = true;
    }
    return oResolve.call(this, self, foe, hx, hy, seg, mul, over);
  };

  M.tickShots = function(dt){
    if (!this.__volleys) this.__netInit();
    for (const f of [this.a, this.b]){
      const N = f.ultNet; if (!N) continue;
      N.t += dt;
      if (!f.w.ult.volleys && N.t >= N.dur) f.ultNet = null;
      if (!f.alive || this.over) f.ultNet = null;
    }
    const byV = new Map();
    for (const s of this.shots){
      if (!s.netVolley) continue;
      let a = byV.get(s.netVolley); if (!a) byV.set(s.netVolley, a = []);
      a.push(s);
    }
    for (const v of this.__volleys){
      const arr = byV.get(v.id);
      if (!arr || arr.length < 2) continue;
      arr.sort((p, q) => p.netIdx - q.netIdx);
      const src = v.own === "a" ? this.a : this.b;
      const foe = v.own === "a" ? this.b : this.a;
      const u = src.w.ult;
      for (let i = 0; i + 1 < arr.length; i++){
        if (arr[i+1].netIdx - arr[i].netIdx !== 1) continue;
        /* [2] THE GAP, SAMPLED IN FLIGHT. The band where a strand can be hit
           alone is (gap - 2*(R + r)); negative means the arrow discs overlap
           and the outcome is unreachable no matter what the strand does. */
        v.hadStrand = true;
        const gap = Math.hypot(arr[i+1].x - arr[i].x, arr[i+1].y - arr[i].y);
        v.gapSum += gap; v.gapN++;
        v.bandSum += Math.max(0, gap - 2 * (R + arr[i].r));
        if (!foe.alive || !src.alive) continue;
        const key = arr[i].netIdx + "-" + arr[i+1].netIdx;
        if (v.struck[key]) continue;
        if (segD(arr[i].x, arr[i].y, arr[i+1].x, arr[i+1].y, foe.x, foe.y)
            > R + (u.strandW || 6)) continue;
        v.struck[key] = true; v.strandHit = true;
        const bl = Math.hypot(arr[i].vx, arr[i].vy) || 1;
        foe.vx += (arr[i].vx / bl) * u.strandKnock;
        foe.vy += (arr[i].vy / bl) * u.strandKnock;
      }
    }
    oTick.call(this, dt);
    for (let i = this.__volleys.length - 1; i >= 0; i--){
      const v = this.__volleys[i];
      if (this.shots.some(s => s.netVolley === v.id)) continue;
      const src = v.own === "a" ? this.a : this.b;
      const n = src.__net;
      if (n){
        if (v.arrowHit && v.strandHit) n.both++;
        else if (v.arrowHit) n.arrowOnly++;
        else if (v.strandHit) n.lightOnly++;
        else n.miss++;
        if (v.hadStrand) n.hadStrand++;
        if (v.gapN){ n.gapSum += v.gapSum / v.gapN; n.bandSum += v.bandSum / v.gapN; n.gapN++; }
      }
      this.__volleys.splice(i, 1);
    }
  };
  return "installed";
}"""

EV_JS = r"""() => {
  if (window.__evInstalled) return "already";
  window.__evInstalled = true;
  const M = AC.Match.prototype, R = AC.CONFIG.physics.ballR;
  const oResolve = M.resolveHit, oTick = M.tickShots;
  M.resolveHit = function(self, foe, hx, hy, seg, mul, over){
    const s = this._cineShot;
    if (s && s.netVolley && self.__net){
      self.__net.ev = self.__net.ev || [];
      self.__net.ev.push([Math.hypot(foe.x - self.x, foe.y - self.y), 1, 0]);
    }
    return oResolve.call(this, self, foe, hx, hy, seg, mul, over);
  };
  /* A strand contact is detected by watching `struck` grow across the parent
     call -- the strand code itself is not re-implemented here. */
  M.tickShots = function(dt){
    const pre = new Map();
    for (const v of (this.__volleys || [])) pre.set(v.id, Object.keys(v.struck).length);
    oTick.call(this, dt);
    for (const v of (this.__volleys || [])){
      const p = pre.get(v.id); if (p === undefined) continue;
      const now = Object.keys(v.struck).length;
      if (now > p){
        const src = v.own === "a" ? this.a : this.b;
        const foe = v.own === "a" ? this.b : this.a;
        if (src.__net){
          src.__net.ev = src.__net.ev || [];
          for (let i = 0; i < now - p; i++)
            src.__net.ev.push([Math.hypot(foe.x - src.x, foe.y - src.y), 0, 1]);
        }
      }
    }
  };
  return "installed";
}"""

CAD_JS = r"""() => {
  if (window.__cadInstalled) return "already";
  window.__cadInstalled = true;
  const M = AC.Match.prototype, oFire = M.tickFire, oSpawn = M.spawnShot;
  /* The engine gates cadMul on `f.ultBal`, which is the BALLISTA window. A net
     window has to open the same gate, and faking `ultBal` would start
     tickBallista's clock and Marrowdraw's bolt upgrades. So the multiplier is
     applied here instead, on the same field, without touching the engine's. */
  M.tickFire = function(f, foe, dt){
    const u = f.w.ult;
    if (!(f.ultNet && u && u.cadMul !== undefined && u.cadMul !== 1))
      return oFire.call(this, f, foe, dt);
    const S = f.w.shot, before = f.fireCd;
    const r = oFire.call(this, f, foe, dt);
    /* it fired: fireCd jumped forward by exactly S.cadence. Scale that step. */
    if (f.fireCd > before) f.fireCd -= S.cadence * (1 - u.cadMul);
    return r;
  };
  M.spawnShot = function(f, angle){
    if (this.shots.length >= AC.CONFIG.shot.maxLive){
      this.__evicted = (this.__evicted || 0) + 1;
    }
    return oSpawn.call(this, f, angle);
  };
  return "installed";
}"""

RUN_JS = r"""([donor, foes, seeds, secs, ult, onHit, sample]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === donor);
  const sv = { onHit: W.onHit, ult: W.ult, aff: W.aff };
  W.onHit = onHit; W.aff = "umbral";
  if (ult) W.ult = ult;
  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    m.__netInit();
    const me = m.a.w.id === donor ? m.a : m.b, th = me === m.a ? m.b : m.a;
    const n0 = me.__net = { casts:0, volleys:0, both:0, arrowOnly:0, lightOnly:0, miss:0, hadStrand:0,
                 gapSum:0, bandSum:0, gapN:0 };
    let step = 0, next = 0, sepSum = 0, sepN = 0, poolSum = 0;
    let poolPeak = 0, tFirst = -1, tFull = -1, atCap = 0;
    const K = AC.STATUS.curse.maxStacks;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (t >= next){ next += sample;
        sepSum += Math.hypot(th.x - me.x, th.y - me.y); sepN++;
        const p = th.cursePool || [];
        let s = 0; for (const v of p) s += v; poolSum += s;
        if (s > poolPeak) poolPeak = s;
        if (tFirst < 0 && p.length >= 1) tFirst = t;
        if (tFull  < 0 && p.length >= K) tFull  = t;
        if (p.length >= K) atCap++;
      }
    }
    /* THE TAIL. A volley whose arrows are still in the air when the match
       ends was never retired by tickShots, so the four outcomes did not sum
       to the volley count. Retire them here rather than dropping them: an
       in-flight volley that has already touched the foe is a real outcome. */
    for (const v of (m.__volleys || [])){
      if (v.arrowHit && v.strandHit) n0.both++;
      else if (v.arrowHit) n0.arrowOnly++;
      else if (v.strandHit) n0.lightOnly++;
      else n0.miss++;
      if (v.hadStrand) n0.hadStrand++;
    }
    const n = me.__net;
    rows.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                dur: step*DT, hits: me.hits, dealt: me.dealt,
                casts: n.casts, volleys: n.volleys,
                both: n.both, arrowOnly: n.arrowOnly,
                lightOnly: n.lightOnly, miss: n.miss, hadStrand: n.hadStrand,
                gap: n.gapN ? n.gapSum / n.gapN : 0,
                band: n.gapN ? n.bandSum / n.gapN : 0,
                sep: sepN ? sepSum / sepN : 0,
                poolMean: sepN ? poolSum / sepN : 0,
                poolPeak, tFirst, tFull,
                capFrac: sepN ? atCap / sepN : 0,
                pool: sepN ? poolSum / sepN : 0 });
  }
  W.onHit = sv.onHit; W.ult = sv.ult; W.aff = sv.aff;
  return rows;
}"""

RUN_EV_JS = (RUN_JS
             .replace("const sv = { onHit: W.onHit, ult: W.ult, aff: W.aff };",
                      "const sv = { onHit: W.onHit, ult: W.ult, aff: W.aff, dmg: W.dmg };\n"
                      "  if (ult && ult.__blade) W.dmg = ult.__blade;")
             .replace("W.onHit = sv.onHit; W.ult = sv.ult; W.aff = sv.aff;",
                      "W.onHit = sv.onHit; W.ult = sv.ult; W.aff = sv.aff; W.dmg = sv.dmg;")
             .replace("pool: sepN ? poolSum / sepN : 0 });",
                      "pool: sepN ? poolSum / sepN : 0, ev: n.ev || [], "
                      "evicted: m.__evicted || 0 });"))


# --------------------------------------------------------------------------- #

DONOR = "ironhail"          # the bow donor. Gloamwire's own id once it exists.
R, SHOT_R = 34, 24          # CONFIG.physics.ballR, shot.r -- asserted in [0]


def arms(page, donor, foes, seeds, secs, ult, onHit, sample=0.25):
    return page.evaluate(RUN_EV_JS, [donor, foes, seeds, secs, ult, onHit, sample])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-breach.html")
    ap.add_argument("--stage", default="all",
                    help="0..7 or 'all'. Stage 1 is the build brief's GATE 1.")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--donor", default=DONOR)
    ap.add_argument("--blade", type=float, default=9.2)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    want = (lambda s: a.stage in ("all", str(s)))
    seeds = [3301 + 19 * i for i in range(a.seeds)]
    gp = resolve_game(a.game)
    out = {}

    with game(game_path=gp) as (page, errors):
        got = page.evaluate(INSTALL_JS)
        page.evaluate(EV_JS)
        page.evaluate(CAD_JS)
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, aff:w.aff, "
                          "shape:w.shape, dmg:w.dmg}))")
        CU = page.evaluate("() => ({K:AC.STATUS.curse.maxStacks, "
                           "echo:AC.STATUS.curse.echo, dur:AC.STATUS.curse.dur})")
        PH = page.evaluate("() => ({R:AC.CONFIG.physics.ballR, "
                           "maxLive:AC.CONFIG.shot.maxLive, "
                           "arena:AC.CONFIG.arena})")
        byid = {w["id"]: w for w in W}
        ids = [w["id"] for w in W]
        donor = a.donor
        foes = [i for i in ids if i != donor]
        N = len(foes) * len(seeds)
        diag = math.hypot(PH["arena"]["w"], PH["arena"]["h"])
        print(f"\n{gp.name}   {len(ids)} relics   patch: {got}")
        print(f"curse K={CU['K']} echo={CU['echo']:.0%} dur={CU['dur']}   "
              f"ballR={PH['R']}  maxLive={PH['maxLive']}  "
              f"arena {PH['arena']['w']}x{PH['arena']['h']} (diagonal {diag:.0f})")
        print(f"donor {donor}   {len(foes)} foes x {len(seeds)} seeds = {N} fights "
              f"an arm   (binomial SE ~{100*(0.25/N)**0.5:.1f}pp)")

        # ---------------------------------------------------------------- [0]
        print("\n[0] ASSERTIONS, before any number is read")
        check("curse is the reworked pool mechanic",
              CU["K"] == 3 and abs(CU["echo"] - 0.08) < 1e-9,
              f"K={CU['K']} echo={CU['echo']}")
        shot = page.evaluate("() => AC.WEAPONS.filter(w=>w.shot)"
                             ".map(w=>[w.id, JSON.stringify(w.shot)])")
        check("every bow shares one shot block byte for byte",
              len({b for _, b in shot}) == 1,
              f"{len(shot)} relics, {len({b for _, b in shot})} distinct block")
        dm = page.evaluate(f"() => AC.WEAPONS.find(w=>w.id==='{donor}').shot.dmgMul")
        check("an arrow and a swing deal the same base damage", dm == 1.0,
              f"shot.dmgMul={dm}")
        r0 = page.evaluate(f"() => AC.WEAPONS.find(w=>w.id==='{donor}').shot.r")
        check("an arrow connects at R + shot.r = 58", PH["R"] + r0 == 58,
              f"{PH['R']} + {r0} = {PH['R']+r0}")

        # ---------------------------------------------------------------- [1]
        if want(1):
            print("\n[1] THE POOL ACROSS THE SCHOOL  *** BUILD BRIEF GATE 1 ***")
            print("    donor ults suppressed, foes' ults on, pool sampled every 0.25s")
            print(f"    {'body':14}{'shape':12}{'dmg':>7}{'blows':>7}{'pool':>7}"
                  f"{'peak':>7}{'1st':>7}{'3rd':>7}{'at cap':>8}")
            POOL_JS = RUN_EV_JS  # same runner; ult stubbed via charge
            rowsets = {}
            umb = [w["id"] for w in W if w["aff"] == "umbral"]
            for u_id in umb + [donor]:
                f2 = [i for i in ids if i != u_id]
                oh = {"curse": 1}
                ult = dict(kind="none", charge=1e9, name="-", tip="-")
                rs = page.evaluate(POOL_JS, [u_id, f2, seeds, a.secs, ult, oh, 0.25])
                rowsets[u_id] = rs
                lab = "GLOAMWIRE" if u_id == donor else u_id
                tF = mean(r["tFirst"] for r in rs if r.get("tFirst", -1) >= 0) \
                     if "tFirst" in rs[0] else float("nan")
                print(f"    {lab:14}{byid[u_id]['shape']:12}{byid[u_id]['dmg']:>7.2f}"
                      f"{m_(rs,'hits'):>7.1f}{m_(rs,'poolMean'):>7.1f}"
                      f"{m_(rs,'poolPeak'):>7.1f}"
                      f"{(tF if tF==tF else 0):>6.1f}s"
                      f"{mean(r['tFull'] for r in rs if r['tFull']>=0):>6.1f}s"
                      f"{m_(rs,'capFrac'):>8.0%}")
            out["pool"] = {k: v for k, v in rowsets.items()}
            g = rowsets[donor]
            check("GATE 1a — the bow's pool is within 6 of the design's 54.2",
                  abs(m_(g, "poolMean") - 54.2) < 6.0, f"{m_(g,'poolMean'):.1f}")
            t3 = mean(r["tFull"] for r in g if r["tFull"] >= 0)
            check("GATE 1b — three memories deep within 2s of the design's 13.1s",
                  abs(t3 - 13.1) < 2.0, f"{t3:.1f}s")

        # ---------------------------------------------------------------- [2]
        if want(2):
            print("\n[2] THE CROSSOVER — parallel 130 apart, dmgMul 1.0, KNOCK 0")
            print("    at knock 0 a strand records a classification and touches")
            print("    nothing, so every arm must be the SAME FIGHT. That is this")
            print("    section's control and it is the win column.")
            print(f"    {'strandW':>9}{'reach':>7}{'both':>7}{'arrow only':>12}"
                  f"{'light only':>12}{'miss':>7}{'sum':>7}{'win':>8}")
            C = {}
            for w in [0, 12, 18, 24, 30, 40, 60]:
                u = base_ult(mode="parallel", spread=130, dmgMul=1.0,
                             strandW=w, strandKnock=0, cadMul=1.0,
                             volleys=0, dur=8.0)
                rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                C[w] = rows
                v = m_(rows, "volleys") or 1
                tot = (m_(rows,'both') + m_(rows,'arrowOnly')
                       + m_(rows,'lightOnly') + m_(rows,'miss'))
                mark = "   <- arrow reach == strand reach" if w == SHOT_R else ""
                print(f"    {w:>9}{PH['R']+w:>7}{m_(rows,'both')/v:>6.0%}"
                      f"{m_(rows,'arrowOnly')/v:>12.0%}{m_(rows,'lightOnly')/v:>12.0%}"
                      f"{m_(rows,'miss')/v:>7.0%}{tot/v:>7.0%}{wr(rows):>8.1%}"
                      f"{mark}")
            out["cross"] = C
            wins = {round(wr(r), 6) for r in C.values()}
            check("the knock-0 control: every arm is the same fight",
                  len(wins) == 1, f"{len(wins)} distinct win rates")
            v0 = m_(C[0], "volleys") or 1
            check("a hairline strand is inside its own arrows",
                  m_(C[0], "lightOnly") / v0 < 0.03,
                  f"light-only {m_(C[0],'lightOnly')/v0:.1%}")
            v6 = m_(C[60], "volleys") or 1
            check("above the line lightning-only leads arrow-only",
                  m_(C[60],'lightOnly') > m_(C[60],'arrowOnly'),
                  f"{m_(C[60],'lightOnly')/v6:.0%} vs {m_(C[60],'arrowOnly')/v6:.0%}")
            for w in C:
                tot = (m_(C[w],'both') + m_(C[w],'arrowOnly')
                       + m_(C[w],'lightOnly') + m_(C[w],'miss'))
                if abs(tot / (m_(C[w],'volleys') or 1) - 1) > 0.02:
                    check(f"the four outcomes sum to the volley count at W{w}",
                          False, f"{tot/(m_(C[w],'volleys') or 1):.1%}")
                    break
            else:
                check("the four outcomes sum to the volley count at every width", True)
            # the reach control: past the arena diagonal, nothing may miss
            u = base_ult(mode="parallel", spread=130, dmgMul=1.0,
                         strandW=int(diag * 2), strandKnock=0, cadMul=1.0,
                         volleys=0, dur=8.0)
            rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
            v = m_(rows, "volleys") or 1
            check(f"a strand reaching past the arena diagonal ({diag:.0f}) "
                  f"catches every volley",
                  m_(rows, "miss") / v < 0.03, f"miss {m_(rows,'miss')/v:.1%}")

        # ---------------------------------------------------------------- [3]
        if want(3):
            print("\n[3] FAN AGAINST PARALLEL, both at strandW 30")
            print(f"    {'shape':>12}{'spread':>10}{'gap':>7}{'both':>7}"
                  f"{'arrow':>8}{'light':>8}{'miss':>7}{'win':>8}")
            for mode, sp, lab in [("parallel", 70, "70"), ("parallel", 130, "130"),
                                  ("parallel", 200, "200"),
                                  ("fan", 0.30, "17 deg"), ("fan", 0.60, "34 deg"),
                                  ("fan", 0.90, "52 deg")]:
                u = base_ult(mode=mode, spread=sp, dmgMul=1.0, strandW=30,
                             strandKnock=0, cadMul=1.0, volleys=0, dur=8.0)
                rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                v = m_(rows, "volleys") or 1
                print(f"    {mode:>12}{lab:>10}{m_(rows,'gap'):>7.0f}"
                      f"{m_(rows,'both')/v:>6.0%}{m_(rows,'arrowOnly')/v:>8.0%}"
                      f"{m_(rows,'lightOnly')/v:>8.0%}{m_(rows,'miss')/v:>7.0%}"
                      f"{wr(rows):>8.1%}")

        # ---------------------------------------------------------------- [4]
        if want(4):
            print("\n[4] THE FIRE RATE — and the cap that could make this lie")
            print(f"    CONFIG.shot.maxLive = {PH['maxLive']}; spawnShot SHIFTS at "
                  f"the cap.\n    READ `evicted` BEFORE `win`.")
            print(f"    {'window':>22}{'cadMul':>8}{'rate':>7}{'volleys':>9}"
                  f"{'arrow hits':>12}{'shoves':>9}{'evicted':>9}{'win':>7}")
            ev_bad = 0
            for lab, kw in [("8 SECONDS", dict(dur=8.0, volleys=0)),
                            ("MAGAZINE OF 24", dict(dur=99.0, volleys=24))]:
                for cm in [1.0, 0.5, 0.25]:
                    u = base_ult(dmgMul=1.0, cadMul=cm, **kw)
                    rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                    na = mean(sum(1 for e in r["ev"] if e[1]) for r in rows)
                    ns = mean(sum(1 for e in r["ev"] if e[2]) for r in rows)
                    ev_bad += m_(rows, "evicted")
                    print(f"    {lab:>22}{cm:>8.2f}{1/cm:>6.1f}x"
                          f"{m_(rows,'volleys'):>9.1f}{na:>12.1f}{ns:>9.1f}"
                          f"{m_(rows,'evicted'):>9.1f}{wr(rows):>7.0%}")
                print()
            check("GATE 2 — the projectile cap never evicts a shot",
                  ev_bad == 0, f"{ev_bad:.1f} evictions across the sweep")

        # ---------------------------------------------------------------- [5]
        if want(5):
            print("[5] CONTACTS AS EVENTS, each with its own range")
            print(f"    {'fan':>6}{'strandW':>9}{'arrows':>9}{'strands':>9}"
                  f"{'<100':>8}{'100-200':>10}{'>200':>8}{'win':>7}")
            for sp, w in [(0.60, 60), (0.60, 90), (0.90, 60), (0.90, 90),
                          (0.90, 120), (1.20, 60)]:
                u = base_ult(spread=sp, strandW=w, dmgMul=1.0, cadMul=1.0,
                             volleys=0, dur=8.0)
                rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                A = [0, 0, 0]
                na = ns = 0
                for r in rows:
                    for d, ar, st in r["ev"]:
                        if ar:
                            na += 1
                            A[0 if d < 100 else 1 if d < 200 else 2] += 1
                        else:
                            ns += 1
                n = len(rows)
                print(f"    {math.degrees(sp):>5.0f}d{w:>9}{na/n:>9.1f}{ns/n:>9.1f}"
                      + "".join(f"{A[i]/max(1,na):>8.0%}" if i != 1
                                else f"{A[i]/max(1,na):>10.0%}" for i in range(3))
                      + f"{wr(rows):>7.0%}")
            # the reconciliation the first pass of this section failed
            u = base_ult(spread=0.90, strandW=90, dmgMul=1.0, cadMul=1.0,
                         volleys=0, dur=8.0)
            rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
            na = mean(sum(1 for e in r["ev"] if e[1]) for r in rows)
            ns = mean(sum(1 for e in r["ev"] if e[2]) for r in rows)
            dmgV = m_(rows, 'both') + m_(rows, 'arrowOnly')
            shoV = m_(rows, 'both') + m_(rows, 'lightOnly')
            check("arrow contacts >= volleys that dealt damage",
                  na >= dmgV - 0.01, f"{na:.1f} >= {dmgV:.1f}")
            check("strand contacts between 1x and 2x volleys that shoved "
                  "(two strands a volley)",
                  shoV - 0.01 <= ns <= 2 * shoV + 0.01, f"{ns:.1f} vs {shoV:.1f}")

        # ---------------------------------------------------------------- [6]
        if want(6):
            print("\n[6] THE COMPOSITION, on the magazine shape")
            blades = [16.23, 13.0, 10.0, 7.0]
            print(f"    {'arrow damage':>22}"
                  + "".join(f"{'blade '+str(b):>13}" for b in blades))
            for lab, dmm in [("normal (1.0x)", 1.0), ("+40% (1.4x)", 1.4),
                             ("+80% (1.8x)", 1.8)]:
                cells = []
                for b in blades:
                    u = base_ult(dmgMul=dmm)
                    u["__blade"] = b
                    rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                    cells.append(f"{wr(rows):>12.0%}")
                print(f"    {lab:>22}" + "".join(cells))

            print(f"\n    THE MAGAZINE LADDER — blade {a.blade}, arrows x1.4")
            print(f"    {'volleys':>9}{'window':>9}{'arrow hits':>12}{'shoves':>9}"
                  f"{'pool':>7}{'win':>7}")
            for n in [12, 18, 24, 30, 36]:
                u = base_ult(volleys=n)
                u["__blade"] = a.blade
                rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                na = mean(sum(1 for e in r["ev"] if e[1]) for r in rows)
                ns = mean(sum(1 for e in r["ev"] if e[2]) for r in rows)
                print(f"    {n:>9}{n*0.34*0.5:>8.1f}s{na:>12.1f}{ns:>9.1f}"
                      f"{m_(rows,'pool'):>7.1f}{wr(rows):>7.0%}")

            print(f"\n    THE SHOVE — magazine 24. It is a COST and that is the")
            print(f"    finding: it buys back about a point of blade.")
            print(f"    {'knock':>9}{'shoves':>9}{'separation':>12}{'win':>7}")
            prev = None
            mono = True
            for k in [0, 130, 260, 400]:
                u = base_ult(strandKnock=k)
                u["__blade"] = a.blade
                rows = arms(page, donor, foes, seeds, a.secs, u, {"curse": 1})
                ns = mean(sum(1 for e in r["ev"] if e[2]) for r in rows)
                w = wr(rows)
                if prev is not None and w > prev + 0.02:
                    mono = False
                prev = w
                print(f"    {k:>9}{ns:>9.1f}{m_(rows,'sep'):>12.0f}{w:>7.0%}")
            check("the shove is monotone DOWN across the sweep", mono)

        # ---------------------------------------------------------------- [7]
        if want(7):
            print("\n[7] WHAT CROSSWEAVE IS WORTH, and what it does to the pool")
            u_on = base_ult(); u_on["__blade"] = a.blade
            u_off = base_ult(charge=1e9); u_off["__blade"] = a.blade
            on = arms(page, donor, foes, seeds, a.secs, u_on, {"curse": 1})
            off = arms(page, donor, foes, seeds, a.secs, u_off, {"curse": 1})
            print(f"    curse pool with Crossweave      {m_(on,'pool'):>6.1f}")
            print(f"    curse pool with it stubbed      {m_(off,'pool'):>6.1f}")
            print(f"    win with Crossweave             {wr(on):>6.0%}")
            print(f"    win with it stubbed             {wr(off):>6.0%}")
            print(f"    Crossweave is worth          {100*(wr(on)-wr(off)):>+7.1f}pp"
                  f"   (median ultimate +20.4pp)")
            check("Crossweave RAISES the curse pool — v49 §5b amended, not broken",
                  m_(on, 'pool') > m_(off, 'pool'),
                  f"{m_(on,'pool'):.1f} vs {m_(off,'pool'):.1f}")

        print("\n--- checks ---------------------------------------------------")
        bad = [c for c in CHECKS if not c[1]]
        print(f"    {len(CHECKS)-len(bad)}/{len(CHECKS)} passed")
        for n, _, d in bad:
            print(f"    FAILED: {n}  {d}")
        assert not errors, errors[:3]
        if a.json:
            pathlib.Path(a.json).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
