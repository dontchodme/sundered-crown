#!/usr/bin/env python
"""BLOODWICK, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v90.

    python bloodwick_probe.py --game ../02-chain/sc-gyre.html [--seeds 2]
    python bloodwick_probe.py --game ../02-chain/sc-gyre.html --lab [--labtag] [--set ult.charge=15]

Counts EVENTS, both sides, every foe. `--lab` is side A on the lab's seeds and
field (the 33 the row was priced against), printing the design's table.
`--labtag` gives a globule its bend, and its slot in the orbit, one step late,
as the lab's `fresh()` did: the reproduction arm.

STAGE 2 -- BLOODSEEKER:
  [1] every globule leaves with the spell's numbers and its bend
  [2] the cadence is 0.34 exactly
  [3] no shot turns more than home*dt in a step (the bend is a curve)
  [4] blows a fight (the brief's ~22)
STAGE 3 -- THE ORBIT:
  [5] never more than maxOrb orbiters
  [6] an orbiter sits within 1px of the lane on every window step it is placed
  [7] orbiters are clanked (the counterplay) and land (a moat)
  [8] the close looses every orbiter at the foe at the spell's speed and bend
STAGE 4 -- THE LUNGE:
  [9] a lunge sends every orbiter at the foe at 520, homing 8, life 2.0, and
      empties the orbit, only with the foe inside 230
  [10] lunged a cast (~7), blows a window (~5.3), the foe's hemorrhage on a
       window frame (~3.2)
  [11] an ult beat a cast, and one a lunge
  [P]  the render path is CALLED: globule, lane
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets, labTag]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const undo = [];
  for (const [path, v] of sets){ const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++) o = o[ks[i]]; const k = ks[ks.length - 1];
    if (!(k in o)) return { err: 'no field ' + path }; undo.push([o, k, o[k]]); o[k] = v; }
  const U = w.ult, live = U.charge < 1e8;
  const oSpawn = AC.Match.prototype.spawnShot;
  if (labTag) AC.Match.prototype.spawnShot = function(f, angle, quiet){
    const r = oSpawn.call(this, f, angle, quiet), s = this.shots[this.shots.length - 1];
    if (s && s.spell === 'bloodseeker'){
      delete s.home; s.untagged = true;
      if (s.orb && f.ultGyre){ f.ultGyre.orb = f.ultGyre.orb.filter(q => q !== s); s.orb = false; f.gyreTally.orbited--; }
    }
    return r;
  };
  const T = { fights: 0, wins: 0, dur: 0, looses: 0, badCad: [], globs: 0, badGlob: [], blows: 0,
              turnChecked: 0, badTurn: [], maxOrb: 0, laneChecked: 0, badLane: [], orbClanked: 0, orbLanded: 0,
              loosedChecked: 0, badLoose: [], lungedChecked: 0, badLunge: [], lungeFar: 0, casts: 0, ultBeats: 0,
              lunges: 0, lunged: 0, orbited: 0, winFrames: 0, foeStk: 0, winBlows: 0, tally: 0, labCasts: 0 };
  try {
    for (const [a, b, sd] of pairs){
      const m = new AC.Match(a, b, sd); m.slLive = false;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a, own = me === m.a ? 'a' : 'b';
      let landedNow = new Set();
      const oRH = m.resolveHit;
      m.resolveHit = function(self, tgt, x, y, seg, mul, over){
        const cs = this._cineShot;
        if (self === me && cs && cs.spell === 'bloodseeker'){ landedNow.add(cs); if (cs.orb) T.orbLanded++; }
        return oRH.call(this, self, tgt, x, y, seg, mul, over);
      };
      const oB = m.beat; m.beat = function(o){ if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++; return oB.call(this, o); };
      let step = 0;
      while (!m.over && step < secs / DT){
        const before = new Map();
        for (const s of m.shots) if (s.own === own && s.spell === 'bloodseeker')
          before.set(s, { a: Math.atan2(s.vy, s.vx), orb: !!s.orb, home: s.home, x: s.x, y: s.y });
        const fc0 = me.fireCd, f0 = me.shotsFired, G0 = me.ultGyre, frozen = m.hitStop > 0, h0 = me.hits;
        const lunges0 = me.gyreTally ? me.gyreTally.lunges : 0;
        landedNow = new Set();
        m.step(DT); step++;
        if (labTag){
          const G = me.ultGyre;
          for (const s of m.shots) if (s.own === own && s.untagged){
            s.untagged = false; s.home = S.home;
            if (G && G.orb.length < U.maxOrb){ s.orb = true; s.home = 0; G.orb.push(s); me.gyreTally.orbited++; }
          }
        }
        const G = me.ultGyre;
        if (G && !G0) T.casts++;
        if (me.shotsFired > f0){
          T.looses++;
          if (Math.abs((me.fireCd - fc0) - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push(me.fireCd - fc0);
        }
        const lungedNow = me.gyreTally && me.gyreTally.lunges > lunges0;
        if (lungedNow && Math.hypot(foe.x - me.x, foe.y - me.y) >= U.lungeR + 1e-6) T.lungeFar++;
        const alive = new Set(m.shots);
        for (const s of m.shots){
          if (s.own !== own || s.spell !== 'bloodseeker') continue;
          const was = before.get(s);
          if (!was){
            T.globs++;
            /* a globule loosed with the foe already close joins the orbit and is
               LUNGED on its very first step: it arrives with the lunge's numbers */
            const sp0 = Math.hypot(s.vx, s.vy), lunged = s.home === U.lungeHome && Math.abs(sp0 - U.lungeV) < 1e-6;
            const ok = (labTag || s.orb || s.home === S.home || lunged) && s.r === S.r && (s.orb || lunged || Math.abs(sp0 - S.speed) < 1e-9);
            if (!ok && T.badGlob.length < 5) T.badGlob.push({ home: s.home, orb: s.orb, v: Math.hypot(s.vx, s.vy) });
            continue;
          }
          /* THE BEND: a free shot's heading moves at most home*dt a step */
          if (!frozen && !s.orb && !was.orb && was.home === s.home && s.home > 0){
            let d = Math.atan2(s.vy, s.vx) - was.a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
            T.turnChecked++;
            if (Math.abs(d) > s.home * DT + 1e-9 && T.badTurn.length < 5) T.badTurn.push({ d, lim: s.home * DT, home: s.home });
          }
          /* THE LANE: an orbiter placed this step sits at orbitR from the ball */
          if (s.orb && was.orb && !frozen){
            const r = Math.hypot(s.x - me.x, s.y - me.y);
            T.laneChecked++;
            if (Math.abs(r - U.orbitR) > 1 && T.badLane.length < 5) T.badLane.push({ r: +r.toFixed(2), meMoved: +Math.hypot(me.x - was.x, me.y - was.y).toFixed(1) });
          }
          /* LOOSED AT THE CLOSE, or LUNGED */
          if (was.orb && !s.orb){
            const sp = Math.hypot(s.vx, s.vy);
            if (lungedNow){
              T.lungedChecked++;
              const ok = Math.abs(sp - U.lungeV) < 1e-6 * U.lungeV + 1 && s.home === U.lungeHome;
              if (!ok && T.badLunge.length < 5) T.badLunge.push({ sp, home: s.home, life: s.life });
            } else {
              T.loosedChecked++;
              const ok = Math.abs(sp - S.speed) < 1 && s.home === S.home;
              if (!ok && T.badLoose.length < 5) T.badLoose.push({ sp, home: s.home });
            }
          }
        }
        for (const [s, was] of before){
          if (alive.has(s) || landedNow.has(s)) continue;
          if (was.orb){
            const n = m.inset;
            const atWall = s.x < n + s.r + 4 || s.x > A.w - n - s.r - 4 || s.y < n + s.r + 4 || s.y > A.h - n - s.r - 4;
            if (!atWall && s.life > 1e-9) T.orbClanked++;
          }
        }
        if (G){ T.maxOrb = Math.max(T.maxOrb, G.orb.length); T.winFrames++; T.foeStk += foe.stacks('hemorrhage'); T.winBlows += me.hits - h0; }
      }
      if (me.gyreTally){ T.lunges += me.gyreTally.lunges; T.lunged += me.gyreTally.lunged; T.orbited += me.gyreTally.orbited; T.tally += me.gyreTally.casts; }
      T.fights++; T.dur += m.t; T.blows += me.hits; if (m.winner === me) T.wins++;
      T.labCasts += Math.floor(step * DT / 16 + 1e-9);
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; AC.Match.prototype.spawnShot = oSpawn; }
  T.live = live; T.lungeLive = typeof AC.Match.prototype.tickGyre === 'function' && /gyreTally\.lunges\+\+/.test(AC.Match.prototype.tickGyre.toString());
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d'); const R = AC.renderer, saved = R.ctx;
  const seen = { glob: 0, orbit: 0 }; let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed); const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        if (!(step % 7 === 0 || me.ultGyre)) continue;
        R.ctx = ctx; R.drawShots(m); R.drawWeapon(m, me); if (R.drawGyre) R.drawGyre(m); R.ctx = saved; frames++;
        if (m.shots.some(s => s.spell === 'bloodseeker')) seen.glob++;
        if (me.ultGyre && me.ultGyre.orb.length) seen.orbit++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="bloodwick")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true")
    ap.add_argument("--labtag", action="store_true", help="the lab's tagging: the bend and the orbit slot one step late")
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
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets, a.labtag])
        D = None if a.lab else page.evaluate(DRAW_JS, [a.relic, 7331, a.secs])
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]; casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F, orbC=T["orbited"] / casts if casts else 0, lungedC=T["lunged"] / casts if casts else 0,
               winBlowC=T["winBlows"] / casts if casts else 0, stk=T["foeStk"] / T["winFrames"] if T["winFrames"] else 0,
               inF=T["winBlows"] / F, outF=(T["blows"] - T["winBlows"]) / F, blowsF=T["blows"] / F, dur=T["dur"] / F)
    tag = ("--lab (side A, the lab's seeds and field)" if a.lab else "every foe, both sides") + ("  --labtag" if a.labtag else "")
    print(f"BLOODWICK PROBE -- {a.game}   {F} fights, {tag}" + (f"   set {' '.join(a.set)}" if a.set else "") + f"   {time.time()-t0:.0f}s")
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f}   hits in/out {row['inF']:.2f}/{row['outF']:.2f}   orbited {row['orbC']:.2f} a cast   "
          f"lunged {row['lungedC']:.2f} a cast   blows {row['winBlowC']:.2f} a window   foe hemorrhage {row['stk']:.2f}   blows {row['blowsF']:.1f} a fight   mean {row['dur']:.1f}s")
    if a.lab:
        print("  against stage 0 on 151 (runs/build/stage0_*.txt)")
        if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row), indent=1))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["globs"] > 20 * F and not T["badGlob"], "[1] every globule leaves with the spell's numbers and its bend",
          f"{T['globs']} globules" + (f"  BAD {T['badGlob']}" if T["badGlob"] else ""))
    check(not T["badCad"] and T["looses"] > 0, "[2] the cadence is exact", f"{T['looses']} looses" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["turnChecked"] > 0 and not T["badTurn"], "[3] no shot turns more than home*dt a step",
          f"{T['turnChecked']} shot-steps" + (f"  BAD {T['badTurn']}" if T["badTurn"] else ""))
    check(14 <= row["blowsF"] <= 60, "[4] blows a fight (the brief's ~22 is the spell's)", f"{row['blowsF']:.1f}")
    if T["live"]:
        check(0 < T["maxOrb"] <= 6, "[5] never more than maxOrb orbiters", f"most at once {T['maxOrb']}")
        check(T["laneChecked"] > 0 and not T["badLane"], "[6] an orbiter sits within 1px of the lane on every window step",
              f"{T['laneChecked']} orbiter-steps" + (f"  BAD {T['badLane']}" if T["badLane"] else ""))
        check(T["orbClanked"] > 0 and T["orbLanded"] > 0, "[7] orbiters are clanked and land", f"clanked {T['orbClanked']}, landed {T['orbLanded']}")
        check(T["loosedChecked"] > 0 and not T["badLoose"], "[8] the close looses every orbiter at the spell's speed and bend",
              f"{T['loosedChecked']}" + (f"  BAD {T['badLoose']}" if T["badLoose"] else ""))
        if T["lungeLive"]:
            check(T["lungedChecked"] > 0 and not T["badLunge"] and T["lungeFar"] == 0,
                  "[9] a lunge sends every orbiter at 520, homing 8 -- only with the foe inside 230",
                  f"{T['lungedChecked']} lunged, {T['lungeFar']} lunges with the foe outside" + (f"  BAD {T['badLunge']}" if T["badLunge"] else ""))
            check(4 <= row["lungedC"] <= 11 and 3 <= row["winBlowC"] <= 9 and 2 <= row["stk"] <= 4.5,
                  "[10] lunged ~7 a cast, blows ~5.3 a window, hemorrhage ~3.2 on a window frame",
                  f"{row['lungedC']:.2f}, {row['winBlowC']:.2f}, {row['stk']:.2f}")
            check(T["ultBeats"] == T["tally"] + T["lunges"], "[11] an ult beat a cast and one a lunge",
                  f"{T['ultBeats']} beats for {T['tally']} casts and {T['lunges']} lunges")
    check(D["threw"] is None and D["seen"]["glob"] > 0 and (not T["live"] or D["seen"]["orbit"] > 0),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row, D=D), indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
