#!/usr/bin/env python
"""CROZIER, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v95.

    python crozier_probe.py --game ../02-chain/sc-radiance.html [--seeds 2]
    python crozier_probe.py --game ../02-chain/sc-radiance.html --lab [--labtag] [--set ult.charge=15]

Counts EVENTS, both sides, every foe. `--lab` is side A on the lab's seeds and
field (the 33 the row was priced against), printing the design's table.
`--labtag` is THE LAB'S LANCE, emulated on the build: tagged one step late
(`fresh()`), shown to the engine as an armed shot of r 1 (so no engine test
reaches it, and its walls are at r 1), and landed by its own ball test at the
true radius after the step -- `overlays/staff_sanct.js` line for line. That is
the reproduction arm.

STAGE 2 -- LANCE:
  [1] every lance leaves with the spell's numbers and its pierce
  [2] the cadence is 0.34 exactly
  [3] NO LANCE IS EVER CLANKED -- and the check can fail: it counts the frames
      on which a lance stood inside a foe blade's parry reach (the
      opportunities), and a lance that vanished with life left, off the wall
      and unlanded (a clank)
  [4] lance blows a fight (the brief's ~7.6)
STAGE 3 -- RADIANCE:
  [5] a grown lance is EXACTLY on the ramp at every step: r = r0 + (r1-r0) k,
      dmgMul = m0 (1 + (mul-1) k), k = min(1, (t - born) / T)
  [6] a lance grows if and only if it was loosed in the window
  [7] grown a cast (~12), lance blows a cast (~3.2)
  [8] a grown landing of 20 or more files a crit beat (the director films it)
  [9] an ult beat a cast
  [P] the render path is CALLED: needle, shaft
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets, labTag, labP]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena, R = AC.CONFIG.physics.ballR, PAD = AC.CONFIG.shot.pad;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const undo = [];
  for (const [path, v] of sets){ const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++) o = o[ks[i]]; const k = ks[ks.length - 1];
    if (!(k in o)) return { err: 'no field ' + path }; undo.push([o, k, o[k]]); o[k] = v; }
  const U = w.ult, live = U.charge < 1e8;
  /* THE LAB'S LANCE (--labtag): spawned as an ordinary arrow, tagged after its
     first step -- armed, r 1 to the engine, the true radius kept -- and landed
     by the probe after each step, as the overlay's onFrame did. The build's
     own pierce and growth are switched off for it. */
  const oSpawn = AC.Match.prototype.spawnShot;
  if (labTag) AC.Match.prototype.spawnShot = function(f, angle, quiet){
    const r = oSpawn.call(this, f, angle, quiet), s = this.shots[this.shots.length - 1];
    if (s && s.spell === 'lance'){ delete s.pierce; delete s.grow; s.untagged = true; }
    return r;
  };
  const T = { fights: 0, wins: 0, dur: 0, looses: 0, badCad: [], lances: 0, badLance: [], blows: 0, lanceBlows: 0,
              opps: 0, clanks: 0, casts: 0, ultBeats: 0, rampChecked: 0, rampDev: 0, badRamp: [], badGrow: 0,
              grown: 0, winLanceBlows: 0, bigGrown: 0, bigCrit: 0, tally: 0, labCasts: 0, lostWhy: [], badBeat: [], eaten: 0 };
  try {
    for (const [a, b, sd] of pairs){
      const m = new AC.Match(a, b, sd); m.slLive = false;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a, own = me === m.a ? 'a' : 'b';
      let landedNow = null;
      const oRH = m.resolveHit;
      m.resolveHit = function(self, tgt, x, y, seg, mul, over){
        const cs = this._cineShot;
        if (self === me && cs && cs.spell === 'lance'){ T.lanceBlows++; landedNow = cs; if (me.ultRadiance) T.winLanceBlows++; }
        return oRH.call(this, self, tgt, x, y, seg, mul, over);
      };
      const oB = m.beat; m.beat = function(o){
        if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++;
        const cs = this._cineShot;
        /* the CASTER's beat only: a reflect resolving inside the lance's own
           resolveHit files the FOE's beat with the lance still handed over */
        if (o && o.kind === 'hit' && cs && cs.spell === 'lance' && cs.grow && o.dmg >= 20 && o.side === (me === this.a ? 0 : 1)){ T.bigGrown++; if (o.crit) T.bigCrit++;
          else if (T.badBeat.length < 4) T.badBeat.push({ side: o.side, mine: me === this.a ? 0 : 1, fatal: o.fatal, dmg: o.dmg, foe: foe.w.id }); }
        return oB.call(this, o);
      };
      const landed = new WeakSet();
      let step = 0;
      while (!m.over && step < secs / DT){
        const before = new Map(); for (const s of m.shots) if (s.own === own && s.spell === 'lance') before.set(s, { x: s.x, y: s.y, life: s.life, r: s.r });
        const fc0 = me.fireCd, f0 = me.shotsFired, open0 = !!me.ultRadiance, frozen = m.hitStop > 0, nShots0 = m.shots.length, tor0 = m.tornado, eaten0 = tor0 ? tor0.eaten : 0;
        landedNow = null;
        const oRH2 = m.resolveHit;
        m.step(DT); step++;
        const open1 = !!me.ultRadiance;
        if (!open0 && open1) T.casts++;
        if (me.shotsFired > f0){
          T.looses++;
          if (Math.abs((me.fireCd - fc0) - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push(me.fireCd - fc0);
        }
        const alive = new Set(m.shots);
        for (const s of m.shots){
          if (s.own !== own || s.spell !== 'lance') continue;
          if (!before.has(s)){
            T.lances++;
            const ok = (labTag || s.pierce === true) && Math.abs(Math.hypot(s.vx, s.vy) - S.speed) < 1e-9 && (s.grow ? true : s.r === S.r);
            if (!ok && T.badLance.length < 5) T.badLance.push({ r: s.r, pierce: s.pierce });
            if (!labTag){
              if (s.grow) T.grown++;
              if ((s.grow && !open0 && !open1) || (!s.grow && open0 && open1)) T.badGrow++;
            }
          }
          if (!labTag && s.grow && !frozen){
            const G = s.grow, k = Math.min(1, (m.t - G.born) / G.T);
            const wantR = G.r0 + (G.r1 - G.r0) * G.k, wantM = G.m0 * (1 + (G.mul - 1) * G.k);
            const dev = Math.max(Math.abs(s.r - wantR), Math.abs(s.dmgMul - wantM), Math.abs(G.k - k) > DT / G.T + 1e-9 ? Math.abs(G.k - k) : 0);
            T.rampChecked++; T.rampDev = Math.max(T.rampDev, dev);
            if (dev > 1e-9 && T.badRamp.length < 5) T.badRamp.push({ r: s.r, wantR, k: G.k, kNow: k });
          }
          /* the opportunity: a lance inside a foe blade's parry reach */
          if (!labTag && foe.alive && foe.stun <= 0){
            for (const q of m.bladeSegments(foe)){
              if (segDist(q.ax, q.ay, q.bx, q.by, s.x, s.y).d < s.r + foe.w.width * 0.5 + PAD){ T.opps++; break; }
            }
          }
        }
        /* DUSKREAVE'S SCOUR EATS ENEMY SHOTS (`scourEat`, before tickShots): a
           lance gone on a step the tornado's own count moved is eaten, not
           clanked. */
        let eatenNow = tor0 ? tor0.eaten - eaten0 : 0;
        if (!labTag) for (const [s, was] of before){
          if (alive.has(s) || s === landedNow) continue;
          const n = m.inset;
          const atWall = s.x < n + s.r + 8 || s.x > A.w - n - s.r - 8 || s.y < n + s.r + 8 || s.y > A.h - n - s.r - 8;
          const expired = s.life <= 1e-9;
          const hitFoe = Math.hypot(s.x - foe.x, s.y - foe.y) < R + s.r + 12;
          if (!atWall && !expired && !hitFoe && eatenNow > 0){ eatenNow--; T.eaten++; continue; }
          if (!atWall && !expired && !hitFoe){ T.clanks++; if (T.lostWhy.length < 8) T.lostWhy.push({ foe: foe.w.id, shots: nShots0, full: nShots0 >= AC.CONFIG.shot.maxLive - 1, scour: !!foe.ultScour, x: Math.round(s.x), y: Math.round(s.y), life: +s.life.toFixed(2) }); }
        }
        if (labTag){
          /* the overlay's onFrame, on the build: tag, grow, land */
          const t = m.t, open = !!me.ultRadiance;
          for (const s of m.shots){
            if (s.own === own && s.untagged){ s.untagged = false; s.arm = 99; s.lance = true; s.lr = s.r; s.r = 1;
              if (open){ s.lgrow = true; s.born = t; T.grown++; } }
          }
          for (let i = m.shots.length - 1; i >= 0; i--){
            const s = m.shots[i];
            if (s.own !== own || !s.lance) continue;
            if (s.lgrow){ const k = Math.min(1, (t - s.born) / labP.gT); s.lr = 16 + (labP.gR1 - 16) * k; s.dmgMul = 1 + (labP.gMul - 1) * k; }
            if (foe.alive && me.alive && Math.hypot(s.x - foe.x, s.y - foe.y) < R + s.lr){
              const bl = Math.hypot(s.vx, s.vy) || 1;
              const seg = { ax: s.x - s.vx / bl * 10, ay: s.y - s.vy / bl * 10, bx: s.x + s.vx / bl * 10, by: s.y + s.vy / bl * 10, a: s.a };
              m.shotHits++; m._cineShot = s; m.resolveHit(me, foe, s.x, s.y, seg, s.dmgMul, s.over); m._cineShot = null;
              m.shots.splice(i, 1);
            }
          }
        }
      }
      if (me.radianceTally) T.tally += me.radianceTally.casts;
      T.fights++; T.dur += m.t; T.blows += me.hits; if (m.winner === me) T.wins++;
      T.labCasts += Math.floor(step * DT / 16 + 1e-9);
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; AC.Match.prototype.spawnShot = oSpawn; }
  T.live = live;
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d'); const R = AC.renderer, saved = R.ctx;
  const seen = { needle: 0, shaft: 0 }; let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed); const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const L = m.shots.filter(s => s.spell === 'lance');
        if (!(step % 7 === 0 || L.some(s => s.grow))) continue;
        R.ctx = ctx; R.drawShots(m); R.drawWeapon(m, me); R.ctx = saved; frames++;
        if (L.some(s => !s.grow)) seen.needle++;
        if (L.some(s => s.grow && s.grow.k > 0.5)) seen.shaft++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="crozier")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true")
    ap.add_argument("--labtag", action="store_true", help="the lab's lance, emulated: one step late, r 1 to the engine, its own ball test")
    ap.add_argument("--labseed0", type=int, default=2207)
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--secs", type=float, default=200.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    sets = [(kv.split("=", 1)[0], json.loads(kv.split("=", 1)[1])) for kv in a.set]
    t0 = time.time()
    STAVES = ("ironhail", "culverin", "briarwand", "cipher", "watchlight", "crozier", "bloodwick", "nightglass")
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != a.relic]
        if a.lab:
            lab_foes = [f for f in foes if f not in STAVES]
            pairs = [[a.relic, f, a.labseed0 + 11 * i] for f in lab_foes for i in range(20)]
        else:
            seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
            pairs = [p for f in foes for s in seeds for p in ([a.relic, f, s], [f, a.relic, s])]
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets, a.labtag, {"gT": 0.4, "gR1": 70, "gMul": 3}])
        D = None if a.lab else page.evaluate(DRAW_JS, [a.relic, 7331, a.secs])
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]; casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F, lanceF=T["lanceBlows"] / F, grownC=T["grown"] / casts if casts else 0,
               winLanceC=T["winLanceBlows"] / casts if casts else 0, blowsF=T["blows"] / F, dur=T["dur"] / F)
    tag = ("--lab (side A, the lab's seeds and field)" if a.lab else "every foe, both sides") + ("  --labtag" if a.labtag else "")
    print(f"CROZIER PROBE -- {a.game}   {F} fights, {tag}" + (f"   set {' '.join(a.set)}" if a.set else "") + f"   {time.time()-t0:.0f}s")
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f}   lance blows {row['lanceF']:.2f} a fight   grown {row['grownC']:.2f} a cast   "
          f"lance blows {row['winLanceC']:.2f} a cast (in the window)   blows {row['blowsF']:.1f} a fight   mean {row['dur']:.1f}s")
    if a.lab:
        print("  against stage 0 on 151 (runs/build/stage0_*.txt): lanceHits is per cast")
        if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row), indent=1))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["lances"] > 20 * F and not T["badLance"], "[1] every lance leaves with the spell's numbers and its pierce",
          f"{T['lances']} lances" + (f"  BAD {T['badLance']}" if T["badLance"] else ""))
    check(not T["badCad"] and T["looses"] > 0, "[2] the cadence is exact", f"{T['looses']} looses" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["opps"] > 100 and T["clanks"] == 0, "[3] no lance is ever clanked -- over the frames it stood in a blade's reach",
          f"{T['opps']} lance-frames inside a foe blade's parry reach; {T['eaten']} eaten by Duskreave's Scour; {T['clanks']} otherwise lost off the wall and unlanded" + (f"  WHY {T['lostWhy']}" if T["lostWhy"] else ""))
    check(4 <= row["lanceF"] <= 16, "[4] lance blows a fight (the brief's ~7.6)", f"{row['lanceF']:.2f}")
    if T["live"]:
        check(T["rampChecked"] > 0 and not T["badRamp"], "[5] a grown lance is exactly on the ramp at every step",
              f"{T['rampChecked']} lance-steps, worst deviation {T['rampDev']:.2e}" + (f"  BAD {T['badRamp']}" if T["badRamp"] else ""))
        check(T["grown"] > 0 and T["badGrow"] == 0, "[6] a lance grows iff it was loosed in the window", f"{T['grown']} grown, {T['badGrow']} wrong")
        check(7 <= row["grownC"] <= 16 and 1.5 <= row["winLanceC"] <= 6, "[7] grown ~12 a cast, lance blows ~3.2 a cast",
              f"{row['grownC']:.2f}, {row['winLanceC']:.2f}")
        check(T["bigGrown"] > 0 and T["bigCrit"] == T["bigGrown"], "[8] a grown landing of 20 or more files a crit beat",
              f"{T['bigCrit']} of {T['bigGrown']}" + (f"  BAD {T['badBeat']}" if T["badBeat"] else ""))
        check(T["ultBeats"] == T["tally"], "[9] an ult beat a cast", f"{T['ultBeats']} beats for {T['tally']} casts")
    check(D["threw"] is None and D["seen"]["needle"] > 0 and (not T["live"] or D["seen"]["shaft"] > 0),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row, D=D), indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
