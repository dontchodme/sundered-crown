#!/usr/bin/env python
"""BRIARWAND, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v93.

    python briarwand_probe.py --game ../02-chain/sc-bloom.html [--seeds 2]
    python briarwand_probe.py --game ../02-chain/sc-bloom.html --lab [--set ult.charge=15]

Plays Briarwand against every relic in the build, from BOTH sides, stepping
the engine, and counts EVENTS (never frames on which an event was possible).
`--lab` is side A on the lab's seeds and field, printing the design's table.

STAGE 2 -- THORNBURST:
  [1] every thorn leaves with the spell's numbers
  [2] every loose is exactly three thorns, at theta, theta-0.28, theta+0.28
  [3] the cadence is 0.42 exactly (fireCd moves by cadence - dt, once)
  [4] thorns are clankable, and a thorn that reaches its range simply ends
  [5] blows a fight, the brief's ~27
STAGE 3 -- BLOOM:
  [6] the cloud moves toward the foe by exactly min(dist, 90 dt) a step,
      clamped to the inset
  [7] the foe inside the cloud, the brief's ~57% of window frames
  [8] bites a cast, the brief's ~12, never closer than 0.4s on the cloud's clock
  [9] the foe's entangle on a window frame, the brief's ~3.7
  [10] every cast files an ult beat; the first bite of a cast files one hit
       beat; a bite that kills files a fatal one
  [11] the window never outlives dur, and closes on a death
  [P]  the render path is CALLED: the thorns and the cloud
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const undo = [];
  for (const [path, v] of sets){
    const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++) o = o[ks[i]];
    const k = ks[ks.length - 1];
    if (!(k in o)) return { err: 'no field ' + path };
    undo.push([o, k, o[k]]); o[k] = v;
  }
  const U = w.ult, live = U.charge < 1e8;
  const T = { fights: 0, wins: 0, dur: 0, looses: 0, badLoose: [], badCad: [], thorns: 0, badThorn: [],
              thornHits: 0, blows: 0, batted: 0, expired: 0, walled: 0,
              casts: 0, ultBeats: 0, hitBeats: 0, castsBitten: 0, fatalBites: 0, fatalBeats: 0,
              cloudSteps: 0, badCloud: [], outside: 0, winFrames: 0, inFrames: 0, foeStk: 0,
              bites: 0, badGap: [], maxWinT: 0, winClock: 0, winDeath: 0 };
  try {
    for (const [a, b, sd] of pairs){
      const m = new AC.Match(a, b, sd);
      m.slLive = false;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a, own = me === m.a ? 'a' : 'b';
      const landed = new Set();
      const oRH = m.resolveHit;
      m.resolveHit = function(self, tgt, x, y, seg, mul, over){
        if (self === me && this._cineShot && this._cineShot.spell === 'thornburst'){ T.thornHits++; landed.add(this._cineShot); }
        return oRH.call(this, self, tgt, x, y, seg, mul, over);
      };
      let cloudPre = null, lastBiteT = null, bittenThisCast = false;
      if (m.tickPollen){
        const oTP = m.tickPollen;
        m.tickPollen = function(dt){
          const P = me.ultPollen;
          cloudPre = P ? { x: P.x, y: P.y, fx: foe.x, fy: foe.y, t: P.t, inset: this.inset, bites: me.pollenTally.bites } : null;
          const hpIn = foe.hp;
          const r = oTP.call(this, dt);
          if (hpIn > 0 && foe.hp <= 0) T.fatalBites++;   // only a death INSIDE tickPollen is a killing bite
          const Q = me.ultPollen;
          if (cloudPre && Q){
            const dx = cloudPre.fx - cloudPre.x, dy = cloudPre.fy - cloudPre.y, l = Math.hypot(dx, dy) || 1;
            const st = Math.min(l, U.drift * dt), n = cloudPre.inset;
            const ex = Math.max(n, Math.min(A.w - n, cloudPre.x + dx / l * st));
            const ey = Math.max(n, Math.min(A.h - n, cloudPre.y + dy / l * st));
            T.cloudSteps++;
            if ((Math.abs(Q.x - ex) > 1e-9 || Math.abs(Q.y - ey) > 1e-9) && T.badCloud.length < 5) T.badCloud.push({ qx: Q.x, ex, qy: Q.y, ey });
            if (Q.x < n - 1e-9 || Q.x > A.w - n + 1e-9 || Q.y < n - 1e-9 || Q.y > A.h - n + 1e-9) T.outside++;
            if (cloudPre.t === 0) lastBiteT = null;          // a new cast: its own clock
            if (me.pollenTally.bites > cloudPre.bites){
              if (lastBiteT !== null && Q.t - lastBiteT < U.every - 1e-9 && T.badGap.length < 5) T.badGap.push(Q.t - lastBiteT);
              lastBiteT = Q.t;
            }
          }
          return r;
        };
      }
      const oB = m.beat;
      m.beat = function(o){
        if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++;
        if (o && o.kind === 'hit' && o.bloom){ if (o.fatal) T.fatalBeats++; else T.hitBeats++; }
        return oB.call(this, o);
      };
      let step = 0, lastP = null;
      while (!m.over && step < secs / DT){
        const mine = new Set(); for (const s of m.shots) if (s.own === own) mine.add(s);
        const fc0 = me.fireCd, f0 = me.shotsFired, open0 = !!me.ultPollen, hp0 = foe.hp;
        const bites0 = me.pollenTally ? me.pollenTally.bites : 0;
        m.step(DT); step++;
        if (me.shotsFired > f0){
          T.looses++;
          const d = me.fireCd - fc0, nfired = me.shotsFired - f0;
          if ((Math.abs(d - (S.cadence - DT)) > 1e-9) && T.badCad.length < 5) T.badCad.push(d);
          const nw = m.shots.filter(s => s.own === own && !mine.has(s) && s.spell === 'thornburst');
          if (nfired !== S.fan && T.badLoose.length < 5) T.badLoose.push({ nfired });
          if (nw.length === S.fan){
            const as = nw.map(s => s.a), c0 = nw[0].a;
            const offs = as.map(x => x - c0).sort((p, q) => p - q);
            const want = [-S.spread, 0, S.spread];
            if (offs.some((v, i) => Math.abs(v - want[i]) > 1e-9) && T.badLoose.length < 5) T.badLoose.push({ offs });
          }
          for (const s of nw){
            T.thorns++;
            const sp = Math.hypot(s.vx, s.vy);
            const ok = s.r === S.r && s.grav === 0 && s.dmgMul === S.dmgMul && Math.abs(sp - S.speed) < 1e-6 && s.life === S.life - DT;
            if (!ok && T.badThorn.length < 5) T.badThorn.push({ r: s.r, sp, life: s.life, dmgMul: s.dmgMul });
          }
        }
        const alive = new Set(m.shots);
        for (const s of mine){
          if (alive.has(s) || s.spell !== 'thornburst') continue;
          if (landed.has(s)) continue;
          const n = m.inset;
          if (s.life <= 1e-9) T.expired++;
          else if (s.x < n + s.r + 1 || s.x > A.w - n - s.r - 1 || s.y < n + s.r + 1 || s.y > A.h - n - s.r - 1) T.walled++;
          else T.batted++;
        }
        const P = me.ultPollen;
        if (P){
          if (!open0){ T.casts++; bittenThisCast = false; lastBiteT = null; }
          T.winFrames++; T.foeStk += foe.stacks('entangle');
          if (Math.hypot(foe.x - P.x, foe.y - P.y) < U.cloudR + R) T.inFrames++;
          if (P.t > T.maxWinT) T.maxWinT = P.t;
          lastP = P;
        } else if (open0){
          if (lastP && lastP.t + DT >= lastP.dur - 1e-9) T.winClock++; else T.winDeath++;
          lastP = null;
        }
        if (me.pollenTally && me.pollenTally.bites > bites0){
          T.bites += me.pollenTally.bites - bites0;
          if (!bittenThisCast){ T.castsBitten++; bittenThisCast = true; }
        }
      }
      T.fights++; T.dur += m.t; T.blows += me.hits; if (m.winner === me) T.wins++;
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; }
  T.live = live;
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d'); const R = AC.renderer, saved = R.ctx;
  const seen = { thorn: 0, cloud: 0 }; let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed); const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const th = m.shots.some(s => s.spell === 'thornburst'), cl = !!me.ultPollen;
        if (!(step % 7 === 0 || cl)) continue;
        R.ctx = ctx; R.drawShots(m); if (R.drawPollen) R.drawPollen(m); R.drawWeapon(m, me); R.ctx = saved;
        frames++; if (th) seen.thorn++; if (cl) seen.cloud++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="briarwand")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true")
    ap.add_argument("--labseed0", type=int, default=2207)
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--secs", type=float, default=200.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    sets = [(kv.split("=", 1)[0], json.loads(kv.split("=", 1)[1])) for kv in a.set]
    t0 = time.time()
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != a.relic]
        if a.lab:
            lab_foes = [f for f in foes if f not in ("ironhail", "culverin", "cipher", "watchlight",
                                                   "crozier", "bloodwick", "nightglass")]
            seeds = [a.labseed0 + 11 * i for i in range(20)]
            pairs = [[a.relic, f, s] for f in lab_foes for s in seeds]
        else:
            seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
            pairs = [p for f in foes for s in seeds for p in ([a.relic, f, s], [f, a.relic, s])]
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets])
        D = None if a.lab else page.evaluate(DRAW_JS, [a.relic, 7331, a.secs])
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]; casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F, bitesC=T["bites"] / casts if casts else 0,
               inShare=T["inFrames"] / T["winFrames"] if T["winFrames"] else 0,
               stk=T["foeStk"] / T["winFrames"] if T["winFrames"] else 0, blowsF=T["blows"] / F,
               thornHitsF=T["thornHits"] / F, dur=T["dur"] / F)
    tag = "--lab (side A, the lab's seeds and field)" if a.lab else "every foe, both sides"
    print(f"BRIARWAND PROBE -- {a.game}   {F} fights, {tag}" + (f"   set {' '.join(a.set)}" if a.set else "")
          + f"   {time.time()-t0:.0f}s")
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f} a fight   bites {row['bitesC']:.2f} a cast   "
          f"inside {row['inShare']:.0%} of the window   foe entangle {row['stk']:.2f} on a window frame   "
          f"blows {row['blowsF']:.2f} a fight ({row['thornHitsF']:.2f} thorns)   mean {row['dur']:.1f}s")
    if a.lab:
        print("  the lab's arm U on Chromium 151 (stage 0, block 2207): win 54.7%, casts 3.10, bites 12.47,"
              " inside 57%, entangle 3.66")
        if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row), indent=1))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["thorns"] > 20 * F and not T["badThorn"], "[1] every thorn leaves with the spell's numbers",
          f"{T['thorns']} thorns seen after their first step" + (f"  BAD {T['badThorn']}" if T["badThorn"] else ""))
    check(T["looses"] > 0 and not T["badLoose"], "[2] every loose is three thorns at theta and +/-0.28",
          f"{T['looses']} looses" + (f"  BAD {T['badLoose']}" if T["badLoose"] else ""))
    check(not T["badCad"], "[3] the cadence is exact", f"fireCd moved by cadence - dt on all {T['looses']}"
          + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["batted"] > 0 and T["expired"] > 0, "[4] clanked, and a thorn at its range simply ends",
          f"batted/eaten {T['batted']}, expired {T['expired']}, on a wall {T['walled']}")
    check(20 <= row["blowsF"] <= 34, "[5] blows a fight, the brief's ~27",
          f"{row['blowsF']:.2f} a fight, {row['thornHitsF']:.2f} of them thorns")
    if T["live"]:
        check(T["cloudSteps"] > 1000 and not T["badCloud"] and T["outside"] == 0,
              "[6] the cloud moves by exactly min(dist, 90 dt), inside the inset",
              f"{T['cloudSteps']} steps" + (f"  BAD {T['badCloud']}" if T["badCloud"] else "") + f"; outside {T['outside']}")
        check(0.45 <= row["inShare"] <= 0.70, "[7] the foe inside the cloud, the brief's ~57%", f"{row['inShare']:.1%}")
        check(8.5 <= row["bitesC"] <= 15 and not T["badGap"], "[8] bites a cast, the brief's ~12, never under 0.4s apart",
              f"{row['bitesC']:.2f}" + (f"  BAD gaps {T['badGap']}" if T["badGap"] else ""))
        check(3.0 <= row["stk"] <= 4.0, "[9] the foe's entangle on a window frame, the brief's ~3.7", f"{row['stk']:.2f}")
        check(T["ultBeats"] == casts and T["hitBeats"] + T["fatalBeats"] >= T["castsBitten"] and T["fatalBeats"] == T["fatalBites"],
              "[10] ult beat a cast; a hit beat at a cast's first bite; a fatal one for a killing bite",
              f"{T['ultBeats']} ult beats for {casts} casts; {T['hitBeats']} first-bite beats for {T['castsBitten']} bitten casts; "
              f"{T['fatalBites']} killing bites, {T['fatalBeats']} fatal beats")
        check(T["maxWinT"] <= 8 + 1e-9 and T["winClock"] > 0 and T["winDeath"] > 0,
              "[11] the window never outlives dur, and closes on a death",
              f"longest {T['maxWinT']:.3f}s; by the clock {T['winClock']}, by a death or the end {T['winDeath']}")
    check(D["threw"] is None and D["frames"] > 0 and D["seen"]["thorn"] > 0 and (not T["live"] or D["seen"]["cloud"] > 0),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row, D=D), indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
