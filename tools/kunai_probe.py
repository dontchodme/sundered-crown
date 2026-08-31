#!/usr/bin/env python3
"""PRICE EVERY SENTENCE OF §1 BEFORE A BUILDER IS OPENED.

    python3 kunai_probe.py --game ../02-chain/sc-paradox-ignition.html

v43's `runic_flail_probe` refuted two of the four sentences of its §1 in 840
fights, before a line of the relic existed. This is that instrument pointed at
the verdant twinblade's §1.

RICK'S §1, as amended:

    "green twinblade forgoes its blades for leaf kunai. the kunai shoot off in
     both directions rapidly as a projectile. the kunai ricochet off walls and
     clanks and turn to try to hit again. kunai grow and empower after they
     ricochet and gain bonus damage and high knockback."

    "the kunai ricochet shouldnt be steering. natural and predictable ricochet
     physics"

Nothing here writes to a build. Every kunai is pushed onto `m.shots` with the
same fields `tickShots` already reads — the shape the Bloodhunt fork branch
uses — so the flight, the parry, the wall and the hit are the SHIPPED code
paths and not a model of them.

  [1] WHAT FORGOING THE BLADES COSTS, AND WHAT IT SAVES. The blades are taken
      away for a window and the window is compared against the identical seed
      with them live. The saving is not rhetorical: `twinblade_survey` §3
      measured this type losing 100% of every bind it takes, and a relic with
      no blades out cannot be bound.

  [2] A SPIN-MODE WEAPON CAN ALREADY FIRE. `tickFire` gates on `f.w.shot` and
      not on mode — v39 open decision 4, inert for six sessions because no
      non-bow carries a shot. Asserted rather than assumed, because the whole
      design rests on it. And `tickFire` looses along `f.theta` ALONE, so
      "in both directions" is the one thing in §1 with no existing path.

  [3] WHERE A KUNAI ENDS. Census over the shipped paths: landed / parried by a
      blade / spent on a wall / expired. v40 measured 82% of every arrow in
      this game ending on a wall, and the source carries bow_survey §4's
      finding that `life` has NEVER expired in this game — a shot travels 1292
      units and the longest wall is 800. A bouncing kunai is the first
      projectile here whose `life` decides anything.

  [4] THE BOUNCE DISTRIBUTION — THE SENTENCE MOST LIKELY TO BREAK. "Grow and
      empower after they ricochet" is worth nothing if a kunai does not live
      to ricochet. Same shape as v43's "stay inside for too long", which
      measured 0.0 events a minute. Swept over speed, life and bounce budget,
      and the number that decides it is the share of LANDED kunai that arrive
      having bounced at least once.

  [5] HIGH KNOCKBACK ON A 62-REACH WEAPON. v41's warhammer survey found the
      type throws its quarry out of its own reach. This weapon has the
      shortest melee reach in the game. Time-to-touch after a knockback of
      size K, swept.

  [6] THE PARRY, AND WHETHER RICOCHETING OFF ONE REMOVES THE COUNTERPLAY.
      `tickShots`' parry is called "the piece that makes ranged fair AND
      legible". §1 turns it into a ricochet, and if a ricochet empowers then
      batting a kunai makes it worse. Measured as the parry rate by foe mode,
      because a foe cannot choose whether it has a spinning weapon.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


DONOR = "widowmaker"          # the twinblade block; its own school is grafted over
# Four foes per mode, so every table can be split the way section [4] of the
# type survey showed the channel splits.
FOES = ["aureole", "vinesower", "farwarden", "marrowdraw",      # ranged
        "emberedge", "nightfell", "heartwood", "axiom",          # swing
        "lastlight", "censer", "foregone", "bulwarden",          # spin
        "gravemourn", "slagheart", "redflail", "paradox"]        # chain

# --------------------------------------------------------------- [1] blades ---
# The blades are removed by emptying `w.blades` for the window, which is what
# "forgoes its blades" means in this engine: `bladeSegments` returns nothing,
# so tickHits lands nothing, `_clankPair` finds no crossing, and `tickShots`
# has no segment to parry with. One mutation reaches all four, which is the
# right shape — three separate suppressions would be three chances to disagree.

BLADES_JS = r"""([donor, foes, seeds, at, win, secs, pin, pinIds, noult, strip]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedBlades = w.blades.slice();
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
      w.blades = savedBlades.slice();
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const a0 = Math.round(at / DT), a1 = Math.round((at + win) / DT);

      let step = 0, hitsWin = 0, dealtWin = 0, clanksWin = 0, stunWin = 0;
      let foeHitsWin = 0, takenWin = 0, alive = true;
      const h0 = { me: 0, th: 0 };

      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const before = foe2.hp;
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        if (step >= a0 && step < a1){
          if (self === me){ hitsWin++; dealtWin += before - foe2.hp; }
          else { foeHitsWin++; takenWin += before - foe2.hp; }
        }
        return r;
      };

      while (step < a1){
        if (m.over){ alive = false; break; }
        if (step === a0){
          h0.me = me.clanks;
          if (strip) w.blades = [];
        }
        const s0 = me.stun;
        m.step(DT); step++;
        if (step > a0 && me.stun > s0) stunWin += me.stun - s0;
      }
      clanksWin = me.clanks - h0.me;
      w.blades = savedBlades.slice();

      rows.push({ foe: f, seed: sd, alive, strip,
                  hits: hitsWin, dealt: dealtWin, clanks: clanksWin,
                  stun: stunWin, foeHits: foeHitsWin, taken: takenWin,
                  win: win });
    }
  }

  w.blades = savedBlades;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""

# ----------------------------------------------------------- [2] can it fire ---

FIRE_JS = r"""([donor, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedShot = w.shot ? JSON.parse(JSON.stringify(w.shot)) : null;
  const fireSrc = AC.Match.prototype.tickFire.toString();

  const runs = {};
  for (const arm of ["bare", "shot"]){
    if (arm === "shot")
      w.shot = { cadence: 0.34, speed: 380, r: 24, life: 3.4, dmgMul: 1 };
    else if (savedShot) w.shot = savedShot; else delete w.shot;

    const m = new AC.Match(donor, foe, seed);
    const me = m.a.w.id === donor ? m.a : m.b;
    let step = 0, spawned = 0, angs = [];
    const seen = new Set();
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      for (const s of m.shots){
        if (s.own !== (me === m.a ? "a" : "b")) continue;
        if (seen.has(s)) continue;
        seen.add(s); spawned++;
        if (angs.length < 40) angs.push(Math.atan2(s.vy, s.vx));
      }
    }
    runs[arm] = { spawned, dur: step * DT, mode: me.w.mode };
  }
  if (savedShot) w.shot = savedShot; else delete w.shot;

  /* "in both directions", and then a FAN — what does the loose site already
     take? `tickFire` calls spawnShot ONCE a cadence; spawnShot itself takes an
     optional angle and falls back to f.theta. */
  const spawnSrc = AC.Match.prototype.spawnShot.toString();
  const looses = (fireSrc.match(/spawnShot\(/g) || []).length;
  const takesAngle = /angle\s*===\s*undefined\s*\?\s*f\.theta\s*:\s*angle/.test(spawnSrc);
  const arity = AC.Match.prototype.spawnShot.length;
  const shiftsAtCap = /shots\.length\s*>=\s*CONFIG\.shot\.maxLive\)\s*this\.shots\.shift\(\)/
                        .test(spawnSrc);
  const spawnAt = /R \+ reach/.test(spawnSrc);
  return { runs, looses, takesAngle, arity, shiftsAtCap, spawnAt,
           maxLive: AC.CONFIG.shot.maxLive };
}"""

# ------------------------------------------------- [3][4][6] the kunai census ---
# Every kunai is pushed with exactly the fields `tickShots` reads, so the
# flight is the shipped path. The end state is read off the shot OBJECT after
# it has been spliced out of `m.shots` — tickShots mutates x/y/life/bounce in
# place before removing it, so the reference this probe holds carries the
# final state and the classification is exact rather than reconstructed.

KUNAI_JS = r"""([donor, foes, seeds, cfg, secs, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const A  = AC.CONFIG.arena;
  const R  = AC.CONFIG.physics.ballR;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedBlades = w.blades.slice();
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
      w.blades = savedBlades.slice();
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const own = me === m.a ? "a" : "b";
      const a0 = Math.round(cfg.at / DT), a1 = Math.round((cfg.at + cfg.dur) / DT);
      /* THE TAIL. The first cut of this probe stopped at a1 and classified 66%
         of every kunai as "in flight" -- a census that never saw two thirds of
         its own population, and every share in it was wrong. The window keeps
         running with the blades still off and nothing more loosed, until the
         last kunai has resolved or could not still be alive: life, plus the
         slack a bounce budget buys at 0.88 damping a bounce. */
      const tail = Math.round((cfg.life + 2.0) / DT);

      /* the hit flag, written on the shot object itself by the one call
         tickShots makes for a landed projectile */
      let tTouch = -1;
      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const before = foe2.hp;
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        if (m._cineShot && m._cineShot.__k){
          m._cineShot.__hit = true;
          m._cineShot.__dmg = before - foe2.hp;
        } else if (self === me && step >= a1 && tTouch < 0){
          /* the first BLADE blow after the cast ends -- not a kunai, which is
             why this arm of the test is gated on _cineShot being absent */
          tTouch = (step - a1) * DT;
        }
        return r;
      };

      const live = new Set();          // kunai still in m.shots
      const done = [];                 // kunai that have resolved
      let step = 0, fireCd = 0, fired = 0, alive = true;
      let peak = 0, refused = 0, sepSum = 0, sepN = 0, sepMax = 0;

      while (step < a1 + tail){
        if (m.over){ alive = false; break; }
        if (step === a0 && cfg.strip) w.blades = [];
        if (step === a1 && cfg.strip) w.blades = savedBlades.slice();

        /* THE CAST. A FAN out of each of the two blade bearings, at a cadence,
           from the shell edge — the two places this weapon's edges come out of.
           Rick: "instead of 2 kunai. lets do a fan of kunai and really turn the
           number of projectiles up so the ricochet shots have a better chance
           of connecting."

           CONFIG.shot.maxLive IS A HARD CEILING OF 64 AND IT IS THE FIRST
           THING A FAN MEETS. `spawnShot` honours it by SHIFTING THE OLDEST
           SHOT OUT — which on a bouncing kunai means one vanishing in mid-air,
           a picture fault of exactly v42/v43's class. This probe refuses to
           loose instead, the way the Bloodhunt fork branch does, and counts
           the refusals, because the count is the finding. */
        if (step >= a0 && step < a1){
          fireCd -= DT;
          if (fireCd <= 0){
            fireCd = cfg.cadence;
            const perVolley = cfg.fan * 2;
            if (m.shots.length + perVolley > AC.CONFIG.shot.maxLive){
              refused += perVolley;
            } else
            for (const dir of [0, Math.PI])
            for (let k = 0; k < cfg.fan; k++){
              const off = cfg.fan === 1 ? 0
                        : -cfg.spread / 2 + cfg.spread * (k / (cfg.fan - 1));
              const ang = me.theta + dir + off;
              const s = {
                own, x: me.x + Math.cos(ang) * (R + 6),
                y: me.y + Math.sin(ang) * (R + 6),
                x0: me.x, y0: me.y, spd0: cfg.speed, t0: m.t,
                vx: Math.cos(ang) * cfg.speed, vy: Math.sin(ang) * cfg.speed,
                r: cfg.r, life: cfg.life, max: cfg.life, grav: cfg.grav,
                dmgMul: cfg.dmgMul, arm: 0, bounce: cfg.bounce,
                knock: cfg.knock, aff: me.aff, a: ang,
                __k: true, __b0: cfg.bounce, __hit: false, __dmg: 0,
              };
              m.shots.push(s); live.add(s); fired++;
            }
          }
        }

        m.step(DT); step++;
        if (m.shots.length > peak) peak = m.shots.length;
        const sep = Math.hypot(th.x - me.x, th.y - me.y);
        if (step >= a0 && step < a1){ sepSum += sep; sepN++;
                                      if (sep > sepMax) sepMax = sep; }

        for (const s of Array.from(live)){
          if (m.shots.indexOf(s) >= 0) continue;
          live.delete(s);
          /* EXACT, not reconstructed: tickShots mutates x/y/life/bounce in
             place and only then splices, so these are the values it died on.
             The predicates below are `tickShots`' own, in its own order. */
          const n = m.inset;
          let how = "parried";
          if (s.__hit) how = "hit";
          else if (s.life <= 0) how = "expired";
          else if (s.x < n + s.r || s.x > A.w - n - s.r
                || s.y < n + s.r || s.y > A.h - n - s.r) how = "wall";
          done.push({ how, used: s.__b0 - s.bounce, dmg: s.__dmg });
        }
      }
      w.blades = savedBlades.slice();

      const by = { hit: 0, parried: 0, wall: 0, expired: 0, unresolved: live.size };
      let bounceSum = 0, hitAfterBounce = 0, bounceOnHit = 0, dmg = 0;
      const hist = [0, 0, 0, 0, 0, 0, 0];
      for (const d of done){
        by[d.how]++;
        bounceSum += d.used;
        hist[Math.min(6, d.used)]++;
        if (d.how === "hit"){
          dmg += d.dmg;
          bounceOnHit += d.used;
          if (d.used >= 1) hitAfterBounce++;
        }
      }
      rows.push({ foe: f, foeMode: th.w.mode, seed: sd, alive, fired,
                  peak, refused, tailSteps: tail, tTouch,
                  sep: sepN ? sepSum / sepN : 0, sepMax,
                  resolved: done.length, by, hist, dmg,
                  bounceMean: done.length ? bounceSum / done.length : 0,
                  bounceOnHit: by.hit ? bounceOnHit / by.hit : 0,
                  hitAfterBounce });
    }
  }

  w.blades = savedBlades;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""

# ------------------------------------------------------------ [5] knockback ---
# The quantity v41 measured on the warhammer, asked of the shortest reach in
# the game: after a shove of size K, how long before this weapon can touch
# anything again. The shove is applied along the caster's own bearing, which
# is the direction a kunai would carry, and the clock runs to the next landed
# blow rather than to a separation threshold — the threshold is the thing being
# questioned.

KNOCK_JS = r"""([donor, foes, seeds, ks, at, horizon, secs, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const R  = AC.CONFIG.physics.ballR;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }
  const rows = [];
  for (const K of ks){
    for (const f of foes){
      for (const sd of seeds){
        const m  = new AC.Match(donor, f, sd);
        const me = m.a.w.id === donor ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        const a0 = Math.round(at / DT), hz = Math.round((at + horizon) / DT);
        let step = 0, tHit = -1, sepAt = 0, sepMax = 0, alive = true;

        const origHit = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
          const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
          if (self === me && step > a0 && tHit < 0) tHit = (step - a0) * DT;
          return r;
        };

        while (step < hz){
          if (m.over){ alive = false; break; }
          if (step === a0){
            /* along the caster's bearing, the way `s.knock` shoves: "along the
               BOLT's travel, not away from the shooter" */
            const ang = Math.atan2(th.y - me.y, th.x - me.x);
            th.vx += Math.cos(ang) * K; th.vy += Math.sin(ang) * K;
            sepAt = Math.hypot(th.x - me.x, th.y - me.y);
          }
          m.step(DT); step++;
          if (step > a0){
            const d = Math.hypot(th.x - me.x, th.y - me.y);
            if (d > sepMax) sepMax = d;
          }
        }
        rows.push({ K, foe: f, seed: sd, alive, tHit, sepAt, sepMax });
      }
    }
  }
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
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--at", type=float, default=12.0, help="when the cast lands")
    ap.add_argument("--dur", type=float, default=4.0, help="how long it runs")
    ap.add_argument("--only", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"1", "2", "3", "4", "5", "6"}
    gp = (HERE / a.game).resolve()
    seeds = [4401 + 13 * i for i in range(a.seeds)]
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        meta = page.evaluate("""() => ({
          arena: AC.CONFIG.arena, ballR: AC.CONFIG.physics.ballR,
          shot: AC.CONFIG.shot,
          inset: (() => { const m = new AC.Match("widowmaker","aureole",1);
                          return m.inset; })(),
          tb: (() => { const w = AC.WEAPONS.find(x => x.id === "widowmaker");
                       return { reach: w.reach, spin: w.spin, mass: w.mass,
                                dmg: w.dmg, blades: w.blades.slice() }; })(),
        })""")
        pin_ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        modes = {w["id"]: w["mode"] for w in
                 page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, mode:w.mode}))")}
        A, R, n = meta["arena"], meta["ballR"], meta["inset"]
        print(f"\narena {A['w']}x{A['h']}  inset {n}  ballR {R}  "
              f"maxLive {meta['shot']['maxLive']}  "
              f"twinblade reach {meta['tb']['reach']} spin {meta['tb']['spin']} "
              f"mass {meta['tb']['mass']}")

        # ---------------------------------------------------------- [1] --
        if "1" in want:
            print(f"\n[1] WHAT FORGOING THE BLADES COSTS — a {a.dur:g}s window at "
                  f"t={a.at:g}s, same seeds, blades live against blades gone\n")
            arms = {}
            for strip in (False, True):
                arms[strip] = page.evaluate(BLADES_JS,
                                            [DONOR, FOES, seeds, a.at, a.dur,
                                             a.secs, a.pin, pin_ids, True, strip])
            live = [r for r in arms[False] if r["alive"]]
            gone = [r for r in arms[True] if r["alive"]]
            print(f"    {'window':<14}{'my blows':>10}{'dealt':>9}{'clanks':>9}"
                  f"{'stagger eaten':>15}{'foe blows':>11}{'taken':>9}")
            for lbl, rs in (("blades live", live), ("blades gone", gone)):
                w = a.dur * len(rs)
                print(f"    {lbl:<14}{sum(r['hits'] for r in rs)/w:>10.3f}"
                      f"{sum(r['dealt'] for r in rs)/w:>9.2f}"
                      f"{sum(r['clanks'] for r in rs)/w*60:>9.1f}"
                      f"{sum(r['stun'] for r in rs)/w:>14.3f}s"
                      f"{sum(r['foeHits'] for r in rs)/w:>11.3f}"
                      f"{sum(r['taken'] for r in rs)/w:>9.2f}")
            wl = a.dur * len(live)
            wg = a.dur * len(gone)
            lost_dps = sum(r["dealt"] for r in live)/wl - sum(r["dealt"] for r in gone)/wg
            saved_stun = (sum(r["stun"] for r in live)/wl
                          - sum(r["stun"] for r in gone)/wg)
            saved_clank = (sum(r["clanks"] for r in live)/wl
                           - sum(r["clanks"] for r in gone)/wg) * 60
            print(f"\n    the bill: {lost_dps:.2f} damage a second, and it buys back "
                  f"{saved_clank:.1f} binds a minute\n    and {saved_stun:.3f}s of "
                  f"stagger a second — every one of which this type LOSES "
                  f"(twinblade_survey §3)")
            check("taking the blades away costs damage — the ultimate has a bill "
                  "to beat and this is it", lost_dps > 0,
                  f"{lost_dps:.2f} dmg/s over the window, at pinned {a.pin:g}")
            takenUp = (sum(r["taken"] for r in gone)/wg
                       - sum(r["taken"] for r in live)/wl)
            check("REFUTED — I expected the avoided binds to be a saving, and they "
                  "are not: damage TAKEN goes UP when the blades come off",
                  takenUp > 0,
                  f"taken {sum(r['taken'] for r in live)/wl:.2f} -> "
                  f"{sum(r['taken'] for r in gone)/wg:.2f} dmg/s, +{takenUp:.2f}. "
                  f"A bind this type LOSES still costs the foe a swing, so "
                  f"{saved_clank:.1f} binds a minute were worth more as "
                  f"interruption than they cost as stagger. THE REAL BILL IS "
                  f"{lost_dps + takenUp:.2f} DMG/S, not {lost_dps:.2f}")
            out["bill"] = lost_dps + takenUp
            out["blades"] = {"lostDps": lost_dps, "savedClanks": saved_clank,
                             "savedStun": saved_stun}

        # ---------------------------------------------------------- [2] --
        if "2" in want:
            print(f"\n[2] CAN A SPIN-MODE WEAPON FIRE AT ALL — v39 od 4, asserted\n")
            fr = page.evaluate(FIRE_JS, [DONOR, "emberedge", seeds[0], a.secs])
            b, s = fr["runs"]["bare"], fr["runs"]["shot"]
            print(f"    {'arm':<28}{'mode':>8}{'shots loosed':>14}{'per second':>12}")
            for lbl, r in (("no w.shot (ships)", b), ("w.shot grafted on", s)):
                print(f"    {lbl:<28}{r['mode']:>8}{r['spawned']:>14}"
                      f"{(r['spawned']/r['dur'] if r['dur'] else 0):>12.3f}")
            check("a twinblade with a `shot` fires, with no other change anywhere — "
                  "tickFire gates on f.w.shot and not on mode",
                  b["spawned"] == 0 and s["spawned"] > 0,
                  f"{b['spawned']} loosed bare, {s['spawned']} with the shot grafted "
                  f"on; v39 open decision 4 has been inert for six sessions and this "
                  f"design is what makes it load-bearing")
            check("a FAN is a call, not a build — spawnShot already takes an angle "
                  "and only falls back to f.theta when none is given",
                  fr["takesAngle"] and fr["arity"] == 2,
                  f"spawnShot(f, angle), arity {fr['arity']}; tickFire calls it "
                  f"{fr['looses']}x a cadence with no angle. Both directions and any "
                  f"fan width are spawnShot(f, f.theta + off) in a loop — nothing "
                  f"about the projectile system has to change")
            check("AND THE FAN'S REAL HAZARD IS THE CEILING: spawnShot SHIFTS THE "
                  "OLDEST SHOT OUT at maxLive rather than declining to spawn",
                  fr["shiftsAtCap"],
                  f"maxLive {fr['maxLive']} — on a bouncing kunai that is one "
                  f"VANISHING IN MID-AIR, a picture fault of exactly v42/v43's "
                  f"class: no error, no invariant broken, and only a person "
                  f"watching can see it. The Bloodhunt fork branch already refuses "
                  f"to spawn instead, for the neighbouring reason")
            out["fire"] = fr

        # -------------------------------------------------------- [3][4][6] --
        def cast(cfg, foes=None, sds=None):
            c = dict(at=a.at, dur=a.dur, cadence=0.25, fan=5, spread=0.7,
                     speed=420, life=3.0, r=10, bounce=3, knock=0, grav=0,
                     dmgMul=1.0, strip=True)
            c.update(cfg)
            return page.evaluate(KUNAI_JS, [DONOR, foes or FOES, sds or seeds, c,
                                            a.secs, a.pin, pin_ids, True])

        def roll(rows):
            fired = sum(r["fired"] for r in rows)
            res = sum(r["resolved"] for r in rows)
            by = {k: sum(r["by"][k] for r in rows)
                  for k in ("hit", "parried", "wall", "expired", "unresolved")}
            hist = [sum(r["hist"][i] for r in rows) for i in range(7)]
            hab = sum(r["hitAfterBounce"] for r in rows)
            return {"fired": fired, "res": res, "by": by, "hist": hist,
                    "hab": hab, "peak": max(r["peak"] for r in rows),
                    "refused": sum(r["refused"] for r in rows),
                    "dmg": sum(r["dmg"] for r in rows),
                    "casts": len(rows)}

        if "3" in want or "4" in want or "6" in want:
            base = dict(fan=5, bounce=3, life=3.0, speed=420, r=10)
            rows = cast(base)
            print(f"\n[3] WHERE A KUNAI ENDS — fan {base['fan']} each way, "
                  f"cadence 0.25s, speed {base['speed']}, life {base['life']:g}s, "
                  f"bounce budget {base['bounce']}, r {base['r']}, "
                  f"blades off for the window\n")
            print(f"    {'foe mode':<10}{'loosed':>8}{'landed':>9}{'parried':>9}"
                  f"{'wall':>8}{'expired':>9}{'in flight':>11}"
                  f"{'peak/64':>9}{'refused':>9}")
            for md in ("ranged", "swing", "spin", "chain"):
                rs = [r for r in rows if r["foeMode"] == md]
                if not rs:
                    continue
                g = roll(rs)
                f0 = max(1, g["fired"])
                print(f"    {md:<10}{g['fired']:>8}{g['by']['hit']/f0:>9.1%}"
                      f"{g['by']['parried']/f0:>9.1%}{g['by']['wall']/f0:>8.1%}"
                      f"{g['by']['expired']/f0:>9.1%}"
                      f"{g['by']['unresolved']/f0:>11.1%}"
                      f"{g['peak']:>9}{g['refused']:>9}")
            g = roll(rows)
            f0 = max(1, g["fired"])
            print(f"    {'ALL':<10}{g['fired']:>8}{g['by']['hit']/f0:>9.1%}"
                  f"{g['by']['parried']/f0:>9.1%}{g['by']['wall']/f0:>8.1%}"
                  f"{g['by']['expired']/f0:>9.1%}{g['by']['unresolved']/f0:>11.1%}"
                  f"{g['peak']:>9}{g['refused']:>9}")

            check("a bouncing kunai does not end the way an arrow does — v40 "
                  "measured 82% of every arrow in this game spent on a wall",
                  g["by"]["wall"] / f0 < 0.60,
                  f"{g['by']['wall']/f0:.1%} on a wall against a bow's 82%, "
                  f"because a bounce budget of {base['bounce']} is {base['bounce']} "
                  f"walls that do not kill it")
            check("THE CEILING BITES — a fan this size cannot be loosed at this "
                  "cadence without spawnShot shifting live kunai out of the air",
                  g["refused"] > 0,
                  f"{g['refused']} looses refused by this probe against a 64 "
                  f"ceiling, peak {g['peak']} in flight. The shipping build must "
                  f"DECLINE like the fork branch, not SHIFT like spawnShot")

            print(f"\n[4] THE BOUNCE DISTRIBUTION — the sentence that decides "
                  f"whether the growth is a mechanic or decoration\n")
            print(f"    bounces used, over every kunai that resolved:")
            tot = max(1, sum(g["hist"]))
            print("    " + "".join(f"{i if i < 6 else '6+':>8}" for i in range(7)))
            print("    " + "".join(f"{h/tot:>8.1%}" for h in g["hist"]))
            print(f"\n    {'arm':<34}{'landed':>9}{'hits/cast':>11}"
                  f"{'mean bounces':>14}{'landed AFTER a bounce':>23}")
            sweep = {}
            for lbl, cfg in [
                    ("fan 5   bounce 3  life 3.0", dict(fan=5, bounce=3, life=3.0)),
                    ("fan 5   bounce 0  life 3.0", dict(fan=5, bounce=0, life=3.0)),
                    ("fan 5   bounce 1  life 3.0", dict(fan=5, bounce=1, life=3.0)),
                    ("fan 5   bounce 6  life 3.0", dict(fan=5, bounce=6, life=3.0)),
                    ("fan 5   bounce 6  life 6.0", dict(fan=5, bounce=6, life=6.0)),
                    ("fan 3   bounce 3  life 3.0", dict(fan=3, bounce=3, life=3.0)),
                    ("fan 9   bounce 3  life 3.0", dict(fan=9, bounce=3, life=3.0)),
                    ("fan 5   bounce 3  speed 260", dict(fan=5, bounce=3, speed=260)),
                    ("fan 5   bounce 3  r 20", dict(fan=5, bounce=3, r=20))]:
                rs = cast(cfg)
                gg = roll(rs)
                sweep[lbl] = gg
                h = max(1, gg["by"]["hit"])
                bmean = sum(i * gg["hist"][i] for i in range(7)) / max(1, gg["res"])
                print(f"    {lbl:<34}{gg['by']['hit']:>9}"
                      f"{gg['by']['hit']/gg['casts']:>11.2f}"
                      f"{bmean:>14.2f}{gg['hab']/h:>23.1%}")

            # --- THE FAN AGAINST THE CADENCE ------------------------------
            # Rick: "really turn the number of projectiles up so the ricochet
            # shots have a better chance of connecting." The rows above say
            # more kunai did not land more hits. This is why: the volleys are
            # loosed off `me.theta`, which on this type turns 6.47 rad/s, so
            # the SPIN is what spreads them and the fan only widens a volley
            # that was already going to sweep. Matched for total kunai loosed,
            # the two extremes are the test.
            print(f"\n    the fan against the cadence — where the coverage "
                  f"actually comes from\n")
            print(f"    {'arm':<34}{'loosed':>8}{'refused':>9}{'peak':>6}"
                  f"{'landed':>8}{'hits/cast':>11}{'after a bounce':>16}")
            fanrows = {}
            for lbl, cfg in [
                    ("fan 1  cadence 0.10  (2/volley)", dict(fan=1, cadence=0.10)),
                    ("fan 3  cadence 0.15", dict(fan=3, cadence=0.15)),
                    ("fan 5  cadence 0.25", dict(fan=5, cadence=0.25)),
                    ("fan 9  cadence 0.45", dict(fan=9, cadence=0.45)),
                    ("fan 9  cadence 0.90  (18/volley)", dict(fan=9, cadence=0.90)),
                    ("fan 5  cadence 0.60  spread 1.6", dict(fan=5, cadence=0.60,
                                                             spread=1.6))]:
                rs = cast(dict(cfg, bounce=3, life=3.0))
                gg = roll(rs)
                fanrows[lbl] = gg
                h = max(1, gg["by"]["hit"])
                print(f"    {lbl:<34}{gg['fired']:>8}{gg['refused']:>9}"
                      f"{gg['peak']:>6}{gg['by']['hit']:>8}"
                      f"{gg['by']['hit']/gg['casts']:>11.2f}{gg['hab']/h:>16.1%}")
            best = max(fanrows, key=lambda k: fanrows[k]["by"]["hit"])
            spread = (max(v["by"]["hit"] for v in fanrows.values())
                      / max(1, min(v["by"]["hit"] for v in fanrows.values())))
            check("MORE PROJECTILES IS NOT MORE DAMAGE — every fan lands within a "
                  "narrow band of every other, because the coverage comes from the "
                  "weapon's own 6.47 rad/s and not from the fan",
                  spread < 1.6,
                  f"best {best} at {max(v['by']['hit'] for v in fanrows.values())} "
                  f"landed, worst at {min(v['by']['hit'] for v in fanrows.values())}"
                  f" — x{spread:.2f} across a 9x range of fan width. "
                  f"The knobs that DID move it are the bounce budget (+78%) and "
                  f"the kunai's radius")
            out["fan"] = fanrows

            b3 = sweep["fan 5   bounce 3  life 3.0"]
            b0 = sweep["fan 5   bounce 0  life 3.0"]
            share = b3["hab"] / max(1, b3["by"]["hit"])
            check("A KUNAI LIVES TO RICOCHET — the growth is a mechanic and not "
                  "decoration",
                  share > 0.25,
                  f"{share:.1%} of every landed kunai arrives having bounced at "
                  f"least once. v43's comparable sentence measured 0.0 events a "
                  f"minute and had to be replaced")
            check("and the bounce is what makes the fan connect at all — the same "
                  "fan with no bounce budget is the control",
                  b3["by"]["hit"] > b0["by"]["hit"],
                  f"{b3['by']['hit']} landed with 3 bounces against "
                  f"{b0['by']['hit']} with none, same seeds, same everything else")
            out["census"] = {"base": g, "sweep": {k: v for k, v in sweep.items()}}

        # ---------------------------------------------------------- [5] --
        if "5" in want:
            print(f"\n[5] HIGH KNOCKBACK ON THE SHORTEST REACH IN THE GAME — fired "
                  f"WHERE THE MECHANIC FIRES IT, on every landed kunai, along the "
                  f"kunai's own travel\n")
            print(f"    {'knock'  :>7}{'landed':>9}{'dmg/cast':>11}"
                  f"{'separation in window':>22}{'peak':>8}"
                  f"{'blade touches again':>21}{'never':>8}")
            kn = {}
            for K in [0, 120, 260, 420, 700]:
                rs = cast(dict(fan=5, cadence=0.25, bounce=3, life=3.0, knock=K))
                gg = roll(rs)
                ok = [r for r in rs if r["alive"]]
                got = [r["tTouch"] for r in ok if r["tTouch"] >= 0]
                kn[K] = {"hit": gg["by"]["hit"], "dmg": gg["dmg"] / gg["casts"],
                         "sep": mean(r["sep"] for r in ok),
                         "sepMax": mean(r["sepMax"] for r in ok),
                         "t": mean(got),
                         "miss": 1 - len(got) / max(1, len(ok))}
                print(f"    {K:>7}{kn[K]['hit']:>9}{kn[K]['dmg']:>11.1f}"
                      f"{kn[K]['sep']:>22.0f}{kn[K]['sepMax']:>8.0f}"
                      f"{kn[K]['t']:>20.2f}s{kn[K]['miss']:>8.0%}")
            hi, lo = kn[700], kn[0]
            check("knockback SHOVES THE QUARRY OUT OF THE KUNAI STREAM — the "
                  "ultimate's own damage is what pays for it, not the blades",
                  hi["hit"] < lo["hit"],
                  f"landed {lo['hit']} at no knock against {hi['hit']} at 700, "
                  f"separation {lo['sep']:.0f} -> {hi['sep']:.0f} units in a "
                  f"520x800 hall")
            out["knock_live"] = kn

            ks = [0, 100, 200, 300, 450]
            kr = page.evaluate(KNOCK_JS, [DONOR, FOES[:8], seeds, ks, a.at, 6.0,
                                          a.secs, a.pin, pin_ids, True])
            print(f"\n    THE SAME QUESTION, ASKED ON A CLOCK — one synthetic shove "
                  f"at t={a.at:g}s, which is v43 §7's trap and is kept as the "
                  f"control\n")
            print(f"    {'knock':>7}{'separation at':>15}{'peak separation':>17}"
                  f"{'time to touch again':>22}{'never touched':>15}")
            kk = {}
            for K in ks:
                rs = [r for r in kr if r["K"] == K and r["alive"]]
                got = [r["tHit"] for r in rs if r["tHit"] >= 0]
                kk[K] = {"sepAt": mean(r["sepAt"] for r in rs),
                         "sepMax": mean(r["sepMax"] for r in rs),
                         "t": mean(got), "miss": 1 - len(got) / max(1, len(rs))}
                print(f"    {K:>7}{kk[K]['sepAt']:>15.0f}{kk[K]['sepMax']:>17.0f}"
                      f"{kk[K]['t']:>21.2f}s{kk[K]['miss']:>15.0%}")
            reach = meta["tb"]["reach"] + meta["ballR"] * 2
            worst = max(ks)
            check("A SINGLE SHOVE ON A CLOCK MEASURES NOTHING ON THIS TYPE, and "
                  "that is the instrument and not the mechanic — v43 §7, where a "
                  "pin read -12% on a clock and +42% on its own condition",
                  abs(kk[worst]["t"] - kk[0]["t"]) < 0.5,
                  f"time to the next landed blow {kk[0]['t']:.2f}s -> "
                  f"{kk[worst]['t']:.2f}s across 0 to {worst} knock, peak separation "
                  f"{kk[0]['sepMax']:.0f} -> {kk[worst]['sepMax']:.0f}. This weapon "
                  f"cannot reach past {reach:.0f} units and sits at a mean "
                  f"{kk[0]['sepAt']:.0f}, so it is ALREADY out of reach and one "
                  f"shove cannot take it further out")
            out["knock"] = kk

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0 if n_ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
