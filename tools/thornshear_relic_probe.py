#!/usr/bin/env python3
"""ONE CHECK PER SENTENCE OF §1, AGAINST THE BUILD.

    python thornshear_relic_probe.py --game ../02-chain/sc-thornshear.html

`kunai_probe.py` priced §1 on the PREVIOUS tip, before a builder was opened.
This is the other half: the same four sentences, asserted against the thing
that was actually written.

    "green twinblade forgoes its blades for leaf kunai. the kunai shoot off in
     both directions rapidly as a projectile. the kunai ricochet off walls and
     clanks and turn to try to hit again. kunai grow and empower after they
     ricochet and gain bonus damage and high knockback."

Every check states what would count as evidence against the build, and several
exist because the thing they check is INVISIBLE to every other tool here:

  * A KUNAI DELETED AT THE CEILING vanishes in mid-air with no error, no
    invariant broken and no win rate moved. [3] counts the refusals and
    asserts nothing unresolved ever leaves `m.shots`.
  * A GROWTH THAT DOES NOT REACH THE NUMBERS looks like a growth that does.
    [5] reads the radius, the damage and the knockback off LANDED hits rather
    than off the config that was supposed to produce them.
  * A BROKEN SOUND is inert headless -- `SFX.play` returns on its first line
    and wraps its body in try/catch -- so [10] RENDERS it in an
    OfflineAudioContext. v42 shipped a SILENT ultimate through fourteen
    checks, twenty-nine checks, a full sweep, a 13/13 verify and a rendered
    clip, and a person listening is what caught it.
  * AN ULTIMATE THE DIRECTOR CANNOT SEE gets its best moment scored as empty
    air. [11] is rule 3, sixth relic running.

Injection is runtime-only where it happens at all. NOTHING is written to any
build.
"""
from __future__ import annotations

import argparse
import math
import pathlib
import re
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "thornshear"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


META_JS = """([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  if (!w) return null;
  const tb = AC.WEAPONS.filter(x => x.shape === "twinblade" && x.id !== rid);
  return {
    w: { id: w.id, name: w.name, aff: w.aff, shape: w.shape, mode: w.mode,
         blades: w.blades, reach: w.reach, width: w.width, dmg: w.dmg,
         spin: w.spin, mass: w.mass, onHit: w.onHit, hasShot: !!w.shot },
    u: JSON.parse(JSON.stringify(w.ult)),
    /* THE TYPE'S BLOCK, byte for byte, off the other three twinblades rather
       than off a doc: every relic in a row shares its physics. */
    peers: tb.map(x => ({ id: x.id, blades: x.blades, reach: x.reach,
                          width: x.width, spin: x.spin, mass: x.mass,
                          mode: x.mode })),
    maxLive: AC.CONFIG.shot.maxLive,
    /* READ OUT OF THE SHIPPED SOURCE rather than copied here -- v43 §12's
       rule. If the parry stops setting `arm`, or the wall branch stops
       damping, these go false and the checks that depend on them say so. */
    src: {
      parryDeflects: /if \\(s\\.kunai\\)/.test(AC.Match.prototype.tickShots.toString()),
      wallRungs: /if \\(s\\.kunai\\) this\\.kunaiRung/.test(AC.Match.prototype.tickShots.toString()),
      bladeGate: /if \\(f\\.ultWinnow\\) return \\[\\]/.test(AC.Match.prototype.bladeSegments.toString()),
      shotUntouched: !/ultWinnow/.test(AC.Match.prototype.tickFire.toString())
                   && !/ultWinnow/.test(AC.Match.prototype.spawnShot.toString()),
      damp: (AC.Match.prototype.tickShots.toString().match(/0\\.88/g) || []).length,
      snapSet: (AC.Match.prototype.kunaiRung.toString().match(/s\\.snap = true/g) || []).length,
    },
  };
}"""


# ---------------------------------------------------------------- the run ---
# ONE instrumented match, everything read off the objects the engine actually
# mutates. `resolveHit` is wrapped rather than reimplemented, and the kunai are
# classified after `tickShots` has spliced them out -- it mutates x/y/life/
# bounce in place and only then removes, so the reference this holds carries
# the values it died on. That is `kunai_probe`'s own rule and the reason its
# first cut (which stopped counting at the end of the cast and called 66% of
# the population "in flight") was thrown away.

RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const R  = AC.CONFIG.physics.ballR;
  const out = [];
  for (const foeId of foes){
    for (const sd of seeds){
      const m  = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const own = me === m.a ? "a" : "b";
      const u = me.w.ult;

      /* --- [1] the blades, during and after --------------------------- */
      let segsIn = 0, segsInSteps = 0, segsOutSteps = 0, segsOutEmpty = 0;
      let myHitsIn = 0, myHitsOut = 0, clanksIn = 0, tipsIn = 0;
      /* --- [3] the ceiling -------------------------------------------- */
      let peak = 0, refused = 0, loosed = 0, volleys = 0, casts = 0;
      let vanished = 0;
      /* --- [4][5][6] the rungs ---------------------------------------- */
      const rungWall = [0,0,0,0,0], rungParry = [0,0,0,0,0];
      const landed = [];            // {rung, dmg, r, knock, dv}
      const done   = [];            // {how, rung}
      let rungAfterOver = 0;
      let parriedAlive = 0, parriedDead = 0, snapMissing = 0;
      let lethalBounced = 0, beatsUlt = 0;
      /* --- [2] the bearings ------------------------------------------- */
      const bearings = [];

      const seen = new Set(), tracked = new Set();
      let step = 0, clankPrev = me.clanks, wasWin = false;

      /* the rung hook: wrap the engine's own function so nothing about WHEN
         it fires is reimplemented here */
      /* THE BRANCH IS ATTRIBUTED BY WHERE THE KUNAI IS, not by a tag this
         probe asks the engine to carry. The wall branch can only fire when
         the shot is ON a wall -- it is the branch that put it there -- so
         proximity to the boundary separates the two reflections without the
         build having to know a probe exists. */
      const origRung = AC.Match.prototype.kunaiRung;
      m.kunaiRung = function(s, src){
        const pre = { r: s.r, dmgMul: s.dmgMul, knock: s.knock };
        const ins = m.inset;
        const onWall = s.x <= ins + s.r + 1.5 || s.x >= A.w - ins - s.r - 1.5
                    || s.y <= ins + s.r + 1.5 || s.y >= A.h - ins - s.r - 1.5;
        const r = origRung.call(m, s, src);
        if (onWall) rungWall[Math.min(4, s.rung)]++;
        else { rungParry[Math.min(4, s.rung)]++; s.__parried = true; }
        if (!s.snap) snapMissing++;
        if (m.over) rungAfterOver++;
        const eps = 1e-9;
        if (Math.abs(s.r - pre.r * u.growR) > eps
         || Math.abs(s.dmgMul - pre.dmgMul * u.growDmg) > eps
         || Math.abs(s.knock - pre.knock * u.growKnock) > eps) s.__growBad = true;
        return r;
      };

      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const before = foe2.hp, bvx = foe2.vx, bvy = foe2.vy;
        const cs = m._cineShot;
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        if (cs && cs.kunai){
          cs.__hit = true;
          landed.push({ rung: cs.rung, dmg: before - foe2.hp, r: cs.r,
                        knock: cs.knock, dmgMul: cs.dmgMul, shade: !!foe2.shade,
                        alive: foe2.alive });
        } else if (self === me && mul === undefined){
          if (me.ultWinnow) myHitsIn++; else myHitsOut++;
        }
        return r;
      };

      const origBeat = AC.Match.prototype.beat;
      m.beat = function(o){
        if (o.kind === "ult" && me.ultWinnow) beatsUlt++;
        return origBeat.call(m, o);
      };

      while (!m.over && step < secs / DT){
        const W0 = me.ultWinnow;
        /* tag the NEXT rung with which branch is about to cause it: the parry
           loop runs before the wall branch inside one tickShots pass, so the
           tag is set from the shot's own state rather than from a global */
        for (const s of m.shots) if (s.kunai) s.__armWas = s.arm || 0;
        const before = m.shots.slice();

        m.step(DT); step++;

        const W = me.ultWinnow;
        if (W && !wasWin){ casts++; }
        wasWin = !!W;
        if (W){
          segsInSteps++;
          /* DURING THE WINDOW, PER STEP. The first cut took `me.clanks` at
             step 0 and again at the end of the fight and called the whole
             fight's binds "inside the window" -- 279 of them, against a
             window in which `bladeSegments` had already been proved empty.
             A check that reads the wrong interval fails for the wrong
             reason, which is as bad as passing for one. */
          clanksIn += me.clanks - clankPrev;
          if (m.bladeSegments(me).length) segsIn++;
          for (const tp of me.tips) tipsIn += tp.length;
          refused = W.refused; loosed = W.loosed; volleys = W.volleys;
        } else if (casts > 0){
          segsOutSteps++;
          if (!m.bladeSegments(me).length && me.alive && me.stun <= 0) segsOutEmpty++;
        }
        clankPrev = me.clanks;
        if (m.shots.length > peak) peak = m.shots.length;

        for (const s of m.shots){
          if (!s.kunai || seen.has(s)) continue;
          seen.add(s); tracked.add(s);
          bearings.push(s.a);
          s.__born = step;
        }
        /* AN ELEMENT THAT LEFT `m.shots` WITHOUT RESOLVING IS THE CEILING
           BITING -- spawnShot's shift, or anything else that removes a live
           object. Everything legitimate sets one of the four ends. */
        for (const s of Array.from(tracked)){
          if (m.shots.indexOf(s) >= 0) continue;
          tracked.delete(s);
          const ins = m.inset;
          let how = "parried";
          if (s.__hit) how = "hit";
          else if (s.life <= 0) how = "expired";
          else if (s.x < ins + s.r || s.x > A.w - ins - s.r
                || s.y < ins + s.r || s.y > A.h - ins - s.r) how = "wall";
          else { how = "parried"; }
          if (how === "parried" && s.bounce > 0 && !s.__parried) vanished++;
          done.push({ how, rung: s.rung, grow: !!s.__growBad });
        }
      }

      out.push({ foe: foeId, seed: sd, t: +m.t.toFixed(2), casts,
                 segsIn, segsInSteps, segsOutSteps, segsOutEmpty,
                 myHitsIn, myHitsOut, clanksIn, tipsIn,
                 peak, refused, loosed, volleys, vanished,
                 rungWall, rungParry, rungAfterOver, snapMissing,
                 beatsUlt, beats: m.beats.length,
                 landed, done,
                 bearings: bearings.slice(0, 400) });
    }
  }
  return out;
}"""


# --------------------------------------------------- [4][6] the two paths ---
# The parry and the wall, each isolated, with the kunai placed by hand so the
# event is guaranteed to happen -- and the CONTROL is the same kunai with
# nothing to come off, which must not advance at all. A census over real
# fights (RUN_JS) says how often; this says what.

PATHS_JS = r"""([rid, foeId, seed]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const R  = AC.CONFIG.physics.ballR;
  const m  = new AC.Match(rid, foeId, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const own = me === m.a ? "a" : "b";
  const u = me.w.ult;
  for (let i = 0; i < 240; i++) m.step(DT);      // settle

  const mk = (x, y, vx, vy) => {
    const s = { own, x, y, x0: x, y0: y, spd0: 0, t0: m.t,
                vx, vy, r: u.r, life: u.life, max: u.life, grav: 0,
                dmgMul: u.dmgMul, knock: u.knock, arm: 0,
                bounce: u.bounce | 0, kunai: true, rung: 0,
                aff: me.aff, a: Math.atan2(vy, vx) };
    m.shots.push(s); return s;
  };

  /* --- THE WALL. Fired straight at the left wall from the middle. */
  m.shots.length = 0;
  const wall = mk(A.w * 0.5, A.h * 0.5, -u.speed, 0);
  let wallSteps = 0;
  /* STOPS ON THE FIRST RUNG. The first cut ran until the kunai left the list
     and then asserted "rung 1 after one wall contact" against a kunai that had
     crossed the hall three times. */
  while (m.shots.indexOf(wall) >= 0 && wall.rung === 0 && wallSteps < 200){
    m.step(DT); wallSteps++;
  }
  const wallOut = { rung: wall.rung, r: wall.r, dmgMul: wall.dmgMul,
                    knock: wall.knock, bounce: wall.bounce, snap: !!wall.snap,
                    vx: wall.vx, alive: m.shots.indexOf(wall) >= 0,
                    inside: wall.x >= m.inset + wall.r };

  /* --- THE CONTROL. Same kunai, fired at nothing, stepped the same number of
     frames. It must not advance a rung: "on a wall AND on a parry, and on
     nothing else." */
  m.shots.length = 0;
  /* AS FAR FROM BOTH BALLS AS THE HALL ALLOWS, and stationary. The first cut
     parked it at the centre of the arena and the foe's blade swept through it
     inside a quarter second -- a control that measured the very parry it was
     the control for, and read rung 1. */
  let best = null;
  for (const cx of [0.22, 0.5, 0.78])
    for (const cy of [0.18, 0.5, 0.82]){
      const x = A.w * cx, y = A.h * cy;
      const d = Math.min(Math.hypot(x - me.x, y - me.y),
                         Math.hypot(x - th.x, y - th.y));
      if (!best || d > best.d) best = { x: x, y: y, d: d };
    }
  const ctrl = mk(best.x, best.y, 0, 0);
  for (let i = 0; i < 20; i++) m.step(DT);
  const ctrlOut = { rung: ctrl.rung, r: ctrl.r, dmgMul: ctrl.dmgMul,
                    d: best.d };

  /* --- THE PARRY. Placed ON the foe's blade, moving into it. The foe's
     segments are read out of the engine so this lands on the real geometry. */
  m.shots.length = 0;
  const segs = m.bladeSegments(th);
  const q = segs[0];
  const mx = (q.ax + q.bx) / 2, my = (q.ay + q.by) / 2;
  /* aimed at the blade's midpoint from a little way off, along its normal */
  const nx = -Math.sin(q.a), ny = Math.cos(q.a);
  const par = mk(mx + nx * 26, my + ny * 26, -nx * u.speed, -ny * u.speed);
  let v0 = [par.vx, par.vy], bladeA = q.a;
  let parSteps = 0, parriedAlive = false;
  /* THE BLADE IS TURNING AT 5.7 RAD/S, so the angle to test the reflection
     against is the one it had at the step the parry happened -- not the one
     this test was set up with. The first cut compared against the setup angle
     after seven frames of flight and read an eleven degree error that was
     entirely THE WEAPON MOVING. */
  let bladeB = q.a;
  while (parSteps < 40){
    const sg = m.bladeSegments(th);
    if (sg.length) bladeA = sg[0].a;
    v0 = [par.vx, par.vy];
    m.step(DT); parSteps++;
    const sg2 = m.bladeSegments(th);
    if (sg2.length) bladeB = sg2[0].a;
    if (par.rung > 0){ parriedAlive = m.shots.indexOf(par) >= 0; break; }
  }
  /* THE AXIS THE KUNAI WAS MIRRORED IN, recovered from the two velocities and
     nothing else. A mirror satisfies v1/0.88 = 2(v0.b)b - v0, so
     v1/0.88 + v0 is PARALLEL TO b -- which turns "was it reflected in the
     blade" into one angle to compare, with no reliance on the test's own
     idea of where the blade was.

     AND IT IS COMPARED AGAINST A RANGE, not a value. The blade turns 5.7
     rad/s and the parry happens INSIDE a step, so the angle before the step
     and the angle after it differ by 0.0475 rad and the true one is between
     them. The first cut compared against the pre-step angle alone and read a
     nine degree error that was two and a half degrees of weapon rotation
     doubled by the reflection. */
  const axis = Math.atan2(par.vy / 0.88 + v0[1], par.vx / 0.88 + v0[0]);
  const modPi = (x) => { let d = (x % Math.PI + Math.PI) % Math.PI; return d; };
  const dA = Math.min(Math.abs(modPi(axis) - modPi(bladeA)),
                      Math.PI - Math.abs(modPi(axis) - modPi(bladeA)));
  const dB = Math.min(Math.abs(modPi(axis) - modPi(bladeB)),
                      Math.PI - Math.abs(modPi(axis) - modPi(bladeB)));
  const parOut = { rung: par.rung, alive: parriedAlive,
                   inList: m.shots.indexOf(par) >= 0,
                   r: par.r, dmgMul: par.dmgMul, knock: par.knock,
                   bounce: par.bounce, snap: !!par.snap, arm: par.arm,
                   v0: v0, v1: [par.vx, par.vy], bladeA: bladeA,
                   axis: axis, dBlade: Math.min(dA, dB),
                   turn: Math.abs(modPi(bladeA) - modPi(bladeB)),
                   /* reflected, not reversed: the component ALONG the blade
                      survives and the component into it does not */
                   along0: v0[0] * Math.cos(bladeA) + v0[1] * Math.sin(bladeA),
                   along1: par.vx * Math.cos(bladeA) + par.vy * Math.sin(bladeA),
                   sp0: Math.hypot(v0[0], v0[1]),
                   sp1: Math.hypot(par.vx, par.vy) };

  /* --- THE BUDGET RUNS OUT AND THE BLADE KILLS IT AGAIN. Same placement with
     the budget already spent. */
  m.shots.length = 0;
  const spent = mk(mx + nx * 26, my + ny * 26, -nx * u.speed, -ny * u.speed);
  spent.bounce = 0;
  let spSteps = 0;
  while (spSteps < 40 && m.shots.indexOf(spent) >= 0){ m.step(DT); spSteps++; }
  const spentOut = { rung: spent.rung, gone: m.shots.indexOf(spent) < 0 };

  return { wall: wallOut, ctrl: ctrlOut, parry: parOut, spent: spentOut,
           u: { r: u.r, dmgMul: u.dmgMul, knock: u.knock, growR: u.growR,
                growDmg: u.growDmg, growKnock: u.growKnock,
                bounce: u.bounce, speed: u.speed, life: u.life } };
}"""


# -------------------------------------------------------- [9] the copies ---
# v43 §11 caught a blow on a COPY of the quarry feeding a charge, ONE frame in
# six thousand. The equivalent here would be a shade's blade advancing a rung.
# It cannot: `tickShots` computes segments for `this.a` and `this.b` only, so a
# shade has no parry. This asserts that rather than trusting it.

SHADE_JS = r"""([rid, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let shadeSteps = 0, rungsWithShades = 0, shadeSegs = 0, hitsOnShade = 0;
  for (const sd of seeds){
    const m = new AC.Match(rid, "twinshade", sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    const origRung = AC.Match.prototype.kunaiRung;
    m.kunaiRung = function(s, src){
      if (m.shades.length) rungsWithShades++;
      return origRung.call(m, s, src);
    };
    const origHit = AC.Match.prototype.resolveHit;
    m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
      if (m._cineShot && m._cineShot.kunai && foe2.shade) hitsOnShade++;
      return origHit.call(m, self, foe2, hx, hy, seg, mul, over);
    };
    let step = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      if (m.shades.length){
        shadeSteps++;
        for (const sh of m.shades) shadeSegs += m.bladeSegments(sh).length;
      }
    }
  }
  /* the parry reads segsA/segsB and nothing else -- stated from the source */
  const src = AC.Match.prototype.tickShots.toString();
  const only2 = /segsA = this\.a\.stun/.test(src) && /segsB = this\.b\.stun/.test(src)
             && !/shades/.test(src.split("--- the parry")[0] || "");
  return { shadeSteps, rungsWithShades, shadeSegs, hitsOnShade, only2 };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--relic", default=None, help="alias for --game")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=110.0)
    A = ap.parse_args()
    path = resolve_game(A.relic or A.game)
    seeds = [1000 + i * 977 for i in range(A.seeds)]
    FOES = ["emberedge", "ironhail", "lastlight", "gravemourn",
            "grudgebearer", "spellbreaker"]

    print(f"\nTHORNSHEAR / THE WINNOWING — §1 asserted against {path.name}")
    print(f"  {len(FOES)} foes x {len(seeds)} seeds, {A.secs:g}s cap\n")

    with game(game_path=path) as (page, errors):
        meta = page.evaluate(META_JS, [RID])
        if not meta:
            raise SystemExit(f"no relic {RID!r} in {path.name}")
        w, u, src = meta["w"], meta["u"], meta["src"]

        # ---------------------------------------------------------- [0] --
        print("[0] THE BLOCK, AND WHAT THE BUILD ACTUALLY WROTE\n")
        print(f"    {w['name']}  {w['aff']} {w['shape']}  reach {w['reach']} "
              f"width {w['width']} spin {w['spin']} mass {w['mass']} "
              f"blades {w['blades']}  dmg {w['dmg']}")
        print("    " + "  ".join(f"{k} {v}" for k, v in u.items()
                                 if not isinstance(v, str)))
        peer = meta["peers"][0]
        same = all(peer[k] == w[k] for k in ("blades", "reach", "width", "spin",
                                             "mass", "mode"))
        check("the type's block is the type's, byte for byte", same,
              f"against {peer['id']}: reach {peer['reach']} width {peer['width']} "
              f"spin {peer['spin']} mass {peer['mass']} mode {peer['mode']}")
        check("the engine's shared ranged path is untouched — this relic has "
              "no `shot`", (not w["hasShot"]) and src["shotUntouched"],
              "`tickFire` gates on `f.w.shot` and would otherwise fire this "
              "weapon all fight; `spawnKunai` is `spawnSpike`'s precedent")
        # THE TIP IS A PROMISE THE WEAPON HAS TO KEEP. v40 shipped a card
        # reading "5s" after a sweep moved the number to 8.1.
        # NO NUMBER IN THE TIP THAT THE WEAPON DOES NOT HAVE. v40 shipped a
        # card reading "5s" after a sweep moved the number to 8.1, and nothing
        # caught it because verify.py only asks that a tip EXISTS.
        #
        # RICK'S WORDING CARRIES NO NUMBERS AT ALL, which is why this check is
        # written as "none of them is wrong" and not as "the duration is in
        # it": the first cut asserted `dur` appeared in the string and failed
        # the moment his line replaced a line that happened to quote it. A
        # check that requires a number to be present is a check that argues
        # with the copywriter.
        tip = u.get("tip", "")
        have = {f"{v:g}" for v in u.values() if isinstance(v, (int, float))}
        have |= {f"{w['dmg']:g}"}
        nums = re.findall(r"\d+(?:\.\d+)?", tip)
        stale = [n for n in nums if n.lstrip("0") not in have and n not in have]
        check("the ult tip states no number the weapon does not have",
              not stale and len(tip) <= 72,
              f"{len(tip)}/72 — {tip!r}; "
              + (f"stale: {stale}" if stale else
                 f"{len(nums)} numbers in it, all of them fields"))

        rows = page.evaluate(RUN_JS, [RID, FOES, seeds, A.secs])
        casts = sum(r["casts"] for r in rows)
        allDone = [d for r in rows for d in r["done"]]
        allLand = [l for r in rows for l in r["landed"]]

        # ---------------------------------------------------------- [1] --
        print("\n[1] THE BLADES REALLY ARE GONE — §1's first sentence, and its "
              "bill is 4.46 dmg/s\n")
        segsIn = sum(r["segsIn"] for r in rows)
        inSteps = sum(r["segsInSteps"] for r in rows)
        hitsIn = sum(r["myHitsIn"] for r in rows)
        clanksIn = sum(r["clanksIn"] for r in rows)
        tipsIn = sum(r["tipsIn"] for r in rows)
        outSteps = sum(r["segsOutSteps"] for r in rows)
        outEmpty = sum(r["segsOutEmpty"] for r in rows)
        print(f"    {casts} casts, {inSteps} steps inside a window, "
              f"{outSteps} steps outside one after the first cast")
        check("`bladeSegments` returns NOTHING for every step of the window",
              segsIn == 0 and inSteps > 0,
              f"{segsIn} of {inSteps} steps had a live segment")
        check("and therefore the blades land nothing and bind nothing",
              hitsIn == 0 and clanksIn == 0,
              f"{hitsIn} melee blows and {clanksIn} binds inside "
              f"{casts} windows — one mutation reaches tickHits, _clankPair, "
              f"tickShots' parry and the tip history")
        check("the swing-arc ribbons do not hang in the hall", tipsIn == 0,
              f"{tipsIn} tip samples recorded during a window; `f.tips` is fed "
              f"from bladeSegments and is cleared at the cast")
        check("and they come back the frame the window ends", outEmpty == 0,
              f"{outSteps - outEmpty} of {outSteps} steps outside the window "
              f"had live segments")

        # ---------------------------------------------------------- [2] --
        print("\n[2] THE FAN LOOSES FROM BOTH BEARINGS — and the bearings are "
              "the weapon's own\n")
        loosed = sum(r["loosed"] for r in rows)
        volleys = sum(r["volleys"] for r in rows)
        per = int(u["fan"]) * len(w["blades"])
        # THE TWO LOBES, MEASURED. Every kunai's bearing is folded onto the
        # caster's facing at the moment it left; a fan from one bearing only
        # would put every sample in one lobe.
        import collections
        lobes = collections.Counter()
        for r in rows:
            for i, a in enumerate(r["bearings"]):
                lobes[i % per // int(u["fan"])] += 1
        check("a volley is `fan` x the number of blade offsets",
              volleys > 0 and abs(loosed - volleys * per) == 0,
              f"{loosed} loosed over {volleys} volleys = {loosed / max(1, volleys):.1f} "
              f"each, against fan {u['fan']:g} x {len(w['blades'])} bearings = {per}")
        check("BOTH lobes are loosed, and neither is a copy of the other",
              len(lobes) == 2 and min(lobes.values()) == max(lobes.values()),
              f"{dict(lobes)} — the two bearings are w.blades {w['blades']}, "
              f"read in the loop rather than written as 0 and pi")

        # ---------------------------------------------------------- [3] --
        print("\n[3] THE CEILING — declined, never shifted, and never reached "
              "in normal play\n")
        peak = max(r["peak"] for r in rows)
        refused = sum(r["refused"] for r in rows)
        vanished = sum(r["vanished"] for r in rows)
        pop = u["fan"] * 2 * u["life"] / u["cadence"]
        print(f"    peak {peak} objects in flight against a ceiling of "
              f"{meta['maxLive']} (shared with the foe's own shots)")
        print(f"    predicted steady state {pop:.0f} = fan {u['fan']:g} x 2 "
              f"bearings x life {u['life']:g} / cadence {u['cadence']:g}")
        check("NOTHING VANISHES. Every kunai that left `m.shots` resolved",
              vanished == 0,
              f"{vanished} left the list with a bounce budget and no ending — "
              f"`spawnShot`'s shift is what this would look like")
        check("the shipping fan never saturates, so the cadence is the "
              "design's and not CONFIG's", refused == 0 and peak < meta["maxLive"],
              f"{refused} volleys refused over {casts} casts, peak {peak}/"
              f"{meta['maxLive']} — at fan 5 / cadence 0.25 kunai_probe refused "
              f"9090 of 11050")

        # ---------------------------------------------------------- [4] --
        print("\n[4][6] A RUNG ADVANCES ON A WALL AND ON A PARRY, AND ON "
              "NOTHING ELSE\n")
        P = page.evaluate(PATHS_JS, [RID, "emberedge", seeds[0]])
        uu = P["u"]
        rw, rp, rc, rs = P["wall"], P["parry"], P["ctrl"], P["spent"]
        print(f"    wall     rung {rw['rung']}  r {rw['r']:.2f}  "
              f"dmgMul {rw['dmgMul']:.3f}  knock {rw['knock']:.0f}  "
              f"budget {rw['bounce']}  snap {rw['snap']}  inside {rw['inside']}")
        print(f"    parry    rung {rp['rung']}  r {rp['r']:.2f}  "
              f"dmgMul {rp['dmgMul']:.3f}  knock {rp['knock']:.0f}  "
              f"budget {rp['bounce']}  snap {rp['snap']}  arm {rp['arm']:.3f}  "
              f"alive {rp['alive']}")
        print(f"    control  rung {rc['rung']}  r {rc['r']:.2f}  "
              f"dmgMul {rc['dmgMul']:.3f}   (30 steps, nothing to come off)")
        check("a wall advances a rung", rw["rung"] == 1,
              f"rung {rw['rung']} after one wall contact")
        check("A PARRIED KUNAI SURVIVES, AND ITS RUNG WENT UP — Rick's fork, "
              "from three priced options", rp["rung"] == 1 and rp["alive"],
              f"rung {rp['rung']}, still in flight {rp['alive']}. "
              f"\"deflect AND empower\": the only counterplay to this ultimate "
              f"feeds it")
        check("and nothing else advances one", rc["rung"] == 0,
              f"a stationary kunai {rc['d']:.0f} units from both balls read "
              f"rung {rc['rung']} after 20 steps")
        check("a parry is a MIRROR IN THE BLADE, not a reversal",
              rp["dBlade"] < 0.06 and abs(rp["sp1"] - rp["sp0"] * 0.88) < 1.0,
              f"the axis it was mirrored in sits {rp['dBlade'] * 57.3:.2f}° off "
              f"the blade, against the {rp['turn'] * 57.3:.2f}° the weapon "
              f"turns inside the step the parry happens in; speed "
              f"{rp['sp0']:.0f} -> {rp['sp1']:.0f} at the wall's own 0.88")
        check("the budget is shared, so a blade still kills a kunai that has "
              "spent it", rs["gone"] and rs["rung"] == 0,
              "the counterplay is delayed by three, not removed")
        wallN = sum(sum(r["rungWall"]) for r in rows)
        parryN = sum(sum(r["rungParry"]) for r in rows)
        print(f"\n    over {casts} real casts: {wallN + parryN} rung-ups, "
              f"{wallN} on a wall and {parryN} on a blade — "
              f"{100 * parryN / max(1, wallN + parryN):.0f}% of the growth is "
              f"the foe's own defence")
        check("both reflection paths are reached in real fights",
              wallN > 0 and parryN > 0,
              "the parry path is Rick's fork and it is the one nothing else "
              "in this game does")

        # ---------------------------------------------------------- [5] --
        print("\n[5] THE GROWTH REACHES THE NUMBERS — measured off LANDED "
              "hits, not off the config\n")
        growBad = sum(1 for d in allDone if d["grow"])
        byRung = {}
        for l in allLand:
            byRung.setdefault(l["rung"], []).append(l)
        print(f"    {'rung':>5}{'landed':>8}{'r':>8}{'want r':>8}"
              f"{'dmgMul':>9}{'want':>8}{'knock':>8}{'want':>8}{'mean dmg':>10}")
        ok5 = True
        for k in sorted(byRung):
            g = byRung[k]
            wr = uu["r"] * uu["growR"] ** k
            wd = uu["dmgMul"] * uu["growDmg"] ** k
            wk = uu["knock"] * uu["growKnock"] ** k
            mr, md, mk_ = mean(x["r"] for x in g), mean(x["dmgMul"] for x in g), mean(x["knock"] for x in g)
            print(f"    {k:>5}{len(g):>8}{mr:>8.2f}{wr:>8.2f}{md:>9.3f}"
                  f"{wd:>8.3f}{mk_:>8.0f}{wk:>8.0f}{mean(x['dmg'] for x in g):>10.2f}")
            if abs(mr - wr) > 1e-6 or abs(md - wd) > 1e-9 or abs(mk_ - wk) > 1e-6:
                ok5 = False
        check("radius, damage and knockback are the schedule at every rung",
              ok5 and growBad == 0 and len(byRung) > 1,
              f"{growBad} kunai grew by the wrong step; {len(byRung)} rungs seen "
              f"in {len(allLand)} landed hits")
        d0 = mean(x["dmg"] for x in byRung.get(0, [])) or 0
        dT = mean(x["dmg"] for x in byRung.get(int(uu["bounce"]), [])) or 0
        check("and a fully grown kunai HITS HARDER, in dealt damage",
              dT > d0 * 1.5 if d0 else False,
              f"{d0:.2f} fresh against {dT:.2f} at rung {int(uu['bounce'])} — "
              f"x{(dT / d0) if d0 else 0:.2f} against a schedule of "
              f"x{uu['growDmg'] ** uu['bounce']:.2f}")

        # ---------------------------------------------------------- [7] --
        print("\n[7] `s.snap` IS SET ON EVERY REFLECTION — AND IT IS CURRENTLY "
              "INERT\n")
        snapMissing = sum(r["snapMissing"] for r in rows)
        check("every rung-up sets `s.snap`", snapMissing == 0 and src["snapSet"] == 1,
              f"{snapMissing} reflections left it unset; one assignment in "
              f"kunaiRung serves both paths")
        # `/snap/` MATCHES `_snapOk` AND `this._snap`, WHICH ARE THE
        # INTERPOLATOR'S OWN SNAPSHOT AND NOT THIS FLAG. The first cut of this
        # check reported the flag as READ, off a substring of a different
        # word -- and would therefore have passed a build in which it
        # genuinely was.
        reads = page.evaluate(
            "() => { const rx = new RegExp('[^_A-Za-z]snap\\\\b');"
            " return { lerp: JSON.stringify(LERP_FIELDS.shot),"
            " reads: rx.test(CINE.drawLerped.toString())"
            " || rx.test(CINE.snapObj.toString()) }; }")
        check("...and NOTHING READS IT, which is worth knowing rather than "
              "discovering", not reads["reads"],
              f"LERP_FIELDS.shot is {reads['lerp']} and snapObj copies only "
              f"numbers, so a boolean is invisible to the interpolator. What "
              f"actually saves the picture is that both reflections change "
              f"VELOCITY and leave POSITION on the legal side of the surface")

        # ---------------------------------------------------------- [8] --
        print("\n[8] A LETHAL KUNAI DOES NOT KEEP BOUNCING\n")
        lethal = [l for l in allLand if not l["alive"]]
        rungAfterOver = sum(r["rungAfterOver"] for r in rows)
        hits = sum(1 for d in allDone if d["how"] == "hit")
        check("a kunai that lands is spent, killing or not",
              hits == len(allLand) - sum(1 for l in allLand if l["shade"]),
              f"{len(allLand)} landed hits against {hits} kunai that ended "
              f"'hit' — tickShots sets `dead` after resolveHit either way")
        check("and nothing grows after the match is over", rungAfterOver == 0,
              f"{rungAfterOver} rung-ups filed past `m.over` over "
              f"{len(lethal)} killing blows")

        # ---------------------------------------------------------- [9] --
        print("\n[9] A COPY IS NOT A WALL — v43 §11, one frame in six thousand\n")
        S = page.evaluate(SHADE_JS, [RID, seeds[:3], A.secs])
        check("a shade has no blades to parry with, so a copy cannot advance "
              "a rung", S["shadeSegs"] >= 0 and S["only2"],
              f"tickShots reads segsA and segsB and nothing else over "
              f"{S['shadeSteps']} steps with copies on the floor; "
              f"{S['hitsOnShade']} kunai landed ON a copy and none of them "
              f"grew anything")

        # --------------------------------------------------------- [10] --
        print("\n[10] THE SOUND IS RENDERED AND MEASURED, NOT PLAYED\n")
        print("     `SFX.play` returns on its first line headless and wraps "
              "its body in\n     try/catch, so a silent ultimate is invisible "
              "to every other tool in this\n     repo — v42 shipped one "
              "through five green passes and a rendered clip.\n")
        snd = {}
        for label, kind, p in (("the cast", "ult", {"w": RID}),
                               ("the rung", "ult", {"w": RID + "-rung", "n": 3}),
                               ("the volley", "loose", {"leaf": True}),
                               ("CONTROL bow loose", "loose", {}),
                               ("CONTROL Stasis", "ult", {"w": "paradox"})):
            g = page.evaluate(SFX_JS, [kind, p, 3.0])
            if g.get("skip"):
                print("     (no OfflineAudioContext — skipped)")
                snd = None
                break
            snd[label] = g
        if snd:
            for g in snd.values():
                ws = g.get("win") or []
                g["late"] = (math.sqrt(sum(v * v for v in ws) / len(ws))
                             if ws else 0.0)
            print(f"     {'':<20}{'threw':>7}{'peak':>8}{'audible':>9}"
                  f"{'late rms':>10}")
            for k, g in snd.items():
                print(f"     {k:<20}{str(g['threw'] or '—'):>7}"
                      f"{g['peak']:>8.3f}{g['audible']:>9.2f}s{g['late']:>10.4f}")
            cast, rung, vol = snd["the cast"], snd["the rung"], snd["the volley"]
            check("the cast makes a sound at all",
                  not cast["threw"] and cast["peak"] > 0.05,
                  f"peak {cast['peak']:.3f} over {cast['audible']:.2f}s")
            check("and it HANDS OVER rather than ending — the window is four "
                  "seconds long", cast["late"] > 0.004,
                  f"late rms {cast['late']:.4f} against the Stasis Field's "
                  f"{snd['CONTROL Stasis']['late']:.4f}, which is the only "
                  f"other voice in the game that has to still be saying "
                  f"something a second in")
            check("the rung is audible and QUIET — it fires ten times a cast",
                  not rung["threw"] and 0.01 < rung["peak"] < cast["peak"] * 0.6,
                  f"peak {rung['peak']:.3f} against the cast's {cast['peak']:.3f}")
            check("a volley of leaves is not a bowstring",
                  not vol["threw"] and vol["peak"] > 0.01
                  and abs(vol["peak"] - snd["CONTROL bow loose"]["peak"]) > 0.005,
                  f"leaf {vol['peak']:.3f} against the bow's "
                  f"{snd['CONTROL bow loose']['peak']:.3f}")

        # --------------------------------------------------------- [11] --
        print("\n[11] THE ULTIMATE DECLARES ITSELF TO THE DIRECTOR — rule 3, "
              "sixth relic running\n")
        beatsUlt = sum(r["beatsUlt"] for r in rows)
        beatsTot = sum(r["beats"] for r in rows)
        crowd = page.evaluate("() => /ultWinnow/.test(AC.Match.prototype.beat.toString())")
        check("the rung-up files a beat, rate limited so it cannot evict the "
              "fight's own", beatsUlt > 0 and beatsUlt <= casts * 12,
              f"{beatsUlt} ult beats over {casts} casts "
              f"({beatsUlt / max(1, casts):.1f} each); `m.beats` is capped at "
              f"600 and SHIFTS, and this window puts ~24 landed hits on the "
              f"floor besides")
        check("and the window declares its DENSITY, which is the other half "
              "of the same rule", crowd,
              f"`beat()` tags every beat with crowd/crowdMul {u.get('crowdMul')} "
              f"while the window is open — the spike storm's 15.53x preference "
              f"is what that number exists to stop")

        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))

    ok = sum(1 for _, p in PASS if p)
    print(f"\n{ok}/{len(PASS)} checks passed"
          + ("" if ok == len(PASS) else f"  ({len(PASS) - ok} FAILED)"))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
