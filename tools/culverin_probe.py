#!/usr/bin/env python
"""CULVERIN, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v96.

    python culverin_probe.py --game ../02-chain/sc-ironfall.html [--seeds 2]
    python culverin_probe.py --game ../02-chain/sc-ironfall.html --lab [--set ult.charge=15]

Plays Culverin against every relic in the build, from BOTH sides, stepping the
engine itself, and asserts what `CULVERIN-BUILD-BRIEF.md` §2 says each stage
must be true of. Every check is a count of EVENTS, not of frames on which an
event was possible (CLAUDE.md, five times over).

`--lab` is the other instrument: side A only, on the lab's own seeds
(`2207 + 11i`) and the lab's own field (every relic but Culverin and Ironhail,
the donor), printing the design's table -- win, casts a fight, shells a cast,
blows a window, the foe's sunder on a window frame -- so a built number is read
against the lab's on the same fights. `--set` moves a field of Culverin's
WEAPONS entry live and puts it back, which is how the charge is converted.

STAGE 2 -- THE SPELL:
  [1] every slug leaves with the slug's numbers (r, grav, dmgMul, speed, life)
  [2] the cadence is 0.55 EXACTLY: on every step that looses a slug, `fireCd`
      moves by `cadence - dt` and nothing else
  [3] every live slug's vy grows by exactly grav*dt on every step the world
      moves, and not at all on a frozen one; vx never changes
  [4] a slug that reaches a wall is spent -- no slug bounces
  [5] slugs are clankable: some are batted out of the air, over the run
  [6] blows a fight: the brief's ~14 (slugs and blade together)

STAGE 3 -- IRONFALL:
  [7] every shell leaves with life T, the shell's numbers and the SOLVED
      velocity for the foe's lead point at that instant
  [8] shells a cast, the brief's ~7.3
  [9] blows a window, the brief's ~2.8
  [10] the foe's sunder on a window frame, the brief's ~3.1
  [11] shells are clankable, walls kill them, and a shell that reaches its
       mark bursts -- and some bursts land
  [12] the window never outlives `dur` on its own clock, and closes on a death
  [13] every cast files an `ult` beat, and a shell or a burst that kills files
       a FATAL one
  [P]  the render path is CALLED against a real 2D context: the slug, the
       shell and its ring, and the staff, on frames where they exist
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
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
  const T = { fights: 0, wins: 0, dur: 0, spawned: 0, badSpawn: [], cadSteps: 0, badCad: [],
              gravSteps: 0, frozenSteps: 0, badGrav: [], bounced: 0,
              slugHits: 0, blows: 0, slugLanded: 0, slugWall: 0, slugOther: 0,
              casts: 0, ultBeats: 0, shells: 0, declined: 0, badShell: [],
              shellHit: 0, pops: 0, popHits: 0, shellWall: 0, shellOther: 0,
              winFrames: 0, foeStk: 0, winBlows: 0, maxWinT: 0, winDeath: 0, winClock: 0,
              kills: 0, killsByUlt: 0, fatalBeatOnUltKill: 0, overLive: 0 };
  try {
    for (const [a, b, sd] of pairs){
      const m = new AC.Match(a, b, sd);
      m.slLive = false;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a;
      const own = me === m.a ? 'a' : 'b';
      const landed = new Set();
      let inShots = false, lastKiller = null;
      const oRH = m.resolveHit;
      m.resolveHit = function(self, tgt, x, y, seg, mul, over){
        const hp0 = tgt.hp;
        if (self === me){
          const cs = this._cineShot;
          if (cs && !cs.shell){ T.slugHits++; landed.add(cs); }
          else if (cs && cs.shell){ T.shellHit++; landed.add(cs); }
          else if (inShots) T.popHits++;
        }
        const r = oRH.call(this, self, tgt, x, y, seg, mul, over);
        if (self === me && hp0 > 0 && tgt.hp <= 0)
          lastKiller = this._cineShot ? (this._cineShot.shell ? 'shell' : 'slug') : (inShots ? 'pop' : 'blade');
        return r;
      };
      const oTS = m.tickShots;
      m.tickShots = function(dt){ inShots = true; try { return oTS.call(this, dt); } finally { inShots = false; } };
      let snap = null;
      if (m.tickIronfall){
        const oTI = m.tickIronfall;
        m.tickIronfall = function(dt){ snap = { x: foe.x, y: foe.y, vx: foe.vx, vy: foe.vy, cx: me.x, cy: me.y }; return oTI.call(this, dt); };
      }
      const oB = m.beat;
      m.beat = function(o){ if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++; return oB.call(this, o); };
      let step = 0, winOpen = false, lastI = null;
      while (!m.over && step < secs / DT){
        const frozen = m.over || m.latch || m.splitHold || m.hitStop > 0;
        const mine = new Map();
        for (const s of m.shots) if (s.own === own) mine.set(s, [s.vx, s.vy, s.life]);
        const fc0 = me.fireCd, f0 = me.shotsFired, h0 = me.hits;
        const open0 = !!me.ultIronfall;
        m.step(DT); step++;
        if (m.shots.length > AC.CONFIG.shot.maxLive) T.overLive++;
        // the loose, the slug and the shell
        if (me.shotsFired > f0){
          const d = me.fireCd - fc0; T.cadSteps++;
          if (Math.abs(d - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push({ t: m.t, d });
        }
        for (const s of m.shots){
          if (s.own !== own || mine.has(s)) continue;
          if (s.shell){
            T.shells++;
            /* PUSHED AFTER tickShots, so the probe meets it exactly as it
               left: nothing has moved it yet. `snap` is the foe and the caster
               as tickIronfall saw them. */
            const Tt = U.T, g = U.g;
            const ltx = snap.x + snap.vx * Tt, lty = snap.y + snap.vy * Tt;
            const ok = s.life === Tt && s.max === Tt && s.r === U.shellR && s.grav === g
                    && s.dmgMul === U.shellMul && s.shard === true && s.pop === U.popDmg && s.popR === U.popR
                    && s.x === snap.cx && s.y === snap.cy
                    && Math.abs(s.tx - ltx) < 1e-9 && Math.abs(s.ty - lty) < 1e-9
                    && Math.abs(s.vx - (s.tx - s.x) / Tt) < 1e-9
                    && Math.abs(s.vy - ((s.ty - s.y) / Tt - 0.5 * g * Tt)) < 1e-9;
            if (!ok && T.badShell.length < 5) T.badShell.push({ life: s.life, r: s.r, vx: s.vx, vy: s.vy, tx: s.tx, ltx });
          } else if (me.shotsFired > f0){
            T.spawned++;
            const sp = Math.hypot(s.vx, s.vy - s.grav * DT);
            const ok = s.r === S.r && s.grav === S.grav && s.dmgMul === S.dmgMul
                    && Math.abs(sp - S.speed) < 1e-6 && s.life === S.life - DT && !(s.bounce > 0);
            if (!ok && T.badSpawn.length < 5) T.badSpawn.push({ r: s.r, grav: s.grav, dmgMul: s.dmgMul, sp, life: s.life });
          }
        }
        // the fall, and the fates
        const alive = new Set(m.shots);
        for (const [s, v0] of mine){
          if (!alive.has(s)){
            const A = AC.CONFIG.arena, n = m.inset;
            const atWall = s.x < n + s.r + 1 || s.x > A.w - n - s.r - 1 || s.y < n + s.r + 1 || s.y > A.h - n - s.r - 1;
            if (s.shell){
              if (landed.has(s)) {}
              else if (s.life <= 0) T.pops++;
              else if (atWall) T.shellWall++;
              else T.shellOther++;
            } else {
              if (landed.has(s)) T.slugLanded++;
              else if (atWall) T.slugWall++;
              else T.slugOther++;
            }
            continue;
          }
          if (s.shell) continue;
          if (frozen){
            T.frozenSteps++;
            if ((s.vy !== v0[1] || s.vx !== v0[0]) && T.badGrav.length < 5) T.badGrav.push({ frozen: true, dvy: s.vy - v0[1] });
          } else {
            T.gravSteps++;
            if (s.vx !== v0[0]){ T.bounced++; continue; }
            if (Math.abs((s.vy - v0[1]) - s.grav * DT) > 1e-9 && T.badGrav.length < 5)
              T.badGrav.push({ dvy: s.vy - v0[1], want: s.grav * DT });
          }
        }
        // the window
        const I = me.ultIronfall;
        if (I){
          if (!open0) T.casts++;
          T.winFrames++; T.foeStk += foe.stacks('sunder');
          if (I.t > T.maxWinT) T.maxWinT = I.t;
          lastI = I;
        } else if (open0){
          if (lastI && lastI.t + DT >= lastI.dur - 1e-9) T.winClock++; else T.winDeath++;
          lastI = null;
        }
        if (I || open0) T.winBlows += me.hits - h0;
      }
      T.fights++; T.dur += m.t; T.blows += me.hits;
      if (m.winner === me){
        T.wins++; T.kills++;
        if (lastKiller === 'shell' || lastKiller === 'pop'){
          T.killsByUlt++;
          if (m.beats.some(o => o.fatal)) T.fatalBeatOnUltKill++;
        }
      }
      if (me.ironTally) T.declined += me.ironTally.declined;
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; }
  T.live = live;
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d');
  const R = AC.renderer, saved = R.ctx;
  const seen = { slug: 0, shell: 0, staff: 0 };
  let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed);
      const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const hasSlug = m.shots.some(s => s.spell === 'slug'), hasShell = m.shots.some(s => s.shell);
        if (!(step % 7 === 0 || hasShell)) continue;
        R.ctx = ctx;
        R.drawShots(m); R.drawWeapon(m, me);
        R.ctx = saved;
        frames++; if (hasSlug) seen.slug++; if (hasShell) seen.shell++; seen.staff++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="culverin")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true", help="side A, the lab's seeds and field, the design's table")
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
            foes = [f for f in foes if f != "ironhail"]
            seeds = [2207 + 11 * i for i in range(20 if a.seeds == 2 else a.seeds)]
            pairs = [[a.relic, f, s] for f in foes for s in seeds]
        else:
            seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
            pairs = [p for f in foes for s in seeds for p in ([a.relic, f, s], [f, a.relic, s])]
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets])
        D = page.evaluate(DRAW_JS, [a.relic, 7331, a.secs]) if not a.lab else None
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]
    tag = f"--lab (side A, the lab's seeds, {len(foes)} foes)" if a.lab else "every foe, both sides"
    print(f"CULVERIN PROBE -- {a.game}   {F} fights, {tag}"
          + (f"   set {' '.join(a.set)}" if a.set else "") + f"   {time.time()-t0:.0f}s")
    casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F,
               shellsC=T["shells"] / casts if casts else 0,
               blowsW=T["winBlows"] / casts if casts else 0,
               stk=T["foeStk"] / T["winFrames"] if T["winFrames"] else 0,
               blowsF=T["blows"] / F, dur=T["dur"] / F)
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f} a fight   shells {row['shellsC']:.2f} a cast   "
          f"blows {row['blowsW']:.2f} a window   foe sunder {row['stk']:.2f} on a window frame   "
          f"blows {row['blowsF']:.2f} a fight   mean {row['dur']:.1f}s")
    if a.lab:
        print("  the lab's arm U on Chromium 151 (stage 0, block 2207): win 48.5%, casts 2.87, shells 7.33,"
              " blows 2.80, sunder 3.11")
        if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row), indent=1))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["spawned"] > 20 * F and not T["badSpawn"], "[1] every slug leaves with the slug's numbers",
          f"{T['spawned']} slugs seen alive after their first step, of {T['cadSteps']} loosed"
          + (f"  BAD {T['badSpawn']}" if T["badSpawn"] else ""))
    check(T["cadSteps"] > 0 and not T["badCad"], "[2] the cadence is exact",
          f"{T['cadSteps']} looses, fireCd moved by cadence - dt on every one" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["gravSteps"] > 1000 and T["frozenSteps"] > 0 and not T["badGrav"],
          "[3] vy grows by grav*dt on every moving step and not on a frozen one",
          f"{T['gravSteps']} moving slug-steps, {T['frozenSteps']} frozen" + (f"  BAD {T['badGrav']}" if T["badGrav"] else ""))
    check(T["bounced"] == 0 and T["slugWall"] > 0, "[4] no slug bounces; a slug at a wall is spent",
          f"{T['slugWall']} spent on a wall, {T['bounced']} changed vx in flight")
    check(T["slugOther"] > 0, "[5] slugs are clankable",
          f"{T['slugOther']} gone mid-hall without landing (batted, or eaten by Scour's band)")
    check(11 <= row["blowsF"] <= 17, "[6] blows a fight, the brief's ~14",
          f"{row['blowsF']:.2f} blows a fight, {T['slugHits']/F:.2f} of them slugs")
    if T["live"]:
        check(T["shells"] > 0 and not T["badShell"], "[7] every shell leaves as solved",
              f"{T['shells']} shells, every one life T, the shell's numbers, the lead point and its velocity"
              + (f"  BAD {T['badShell']}" if T["badShell"] else ""))
        check(6.3 <= row["shellsC"] <= 8.0, "[8] shells a cast, the brief's ~7.3",
              f"{row['shellsC']:.2f} over {casts} casts; {T['declined']} declined at the ceiling")
        check(2.0 <= row["blowsW"] <= 3.6, "[9] blows a window, the brief's ~2.8", f"{row['blowsW']:.2f}")
        check(2.3 <= row["stk"] <= 3.9, "[10] the foe's sunder on a window frame, the brief's ~3.1", f"{row['stk']:.2f}")
        check(T["shellOther"] > 0 and T["shellWall"] > 0 and T["pops"] > 0 and T["popHits"] > 0,
              "[11] clanked, walled, burst -- and bursts land",
              f"in flight {T['shellHit']}, burst {T['pops']} (landed {T['popHits']}), wall {T['shellWall']}, "
              f"batted/eaten {T['shellOther']}")
        check(T["maxWinT"] <= 8 + 1e-9 and T["winDeath"] > 0 and T["winClock"] > 0,
              "[12] the window never outlives dur, and closes on a death",
              f"longest {T['maxWinT']:.3f}s; closed by the clock {T['winClock']}, by a death or the end {T['winDeath']}")
        check(T["ultBeats"] == casts and T["fatalBeatOnUltKill"] == T["killsByUlt"],
              "[13] every cast files an ult beat; every kill by a shell or a burst files a fatal one",
              f"{T['ultBeats']} beats for {casts} casts; {T['killsByUlt']} kills by the ultimate, "
              f"{T['fatalBeatOnUltKill']} with a fatal beat")
        check(T["overLive"] == 0, "[·] the hall never holds more than maxLive", f"{T['overLive']} steps over")
    check(D["threw"] is None and D["frames"] > 0 and D["seen"]["slug"] > 0 and (not T["live"] or D["seen"]["shell"] > 0),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row, D=D), indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
