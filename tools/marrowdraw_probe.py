#!/usr/bin/env python3
"""§1 PRICED BEFORE IT IS BUILT — the bloodsworn bow's ballista window.

    python3 marrowdraw_probe.py --game ../02-chain/sc-bulwarden-frame.html

Rick's §1, verbatim, and every sentence of it is a claim this file has to put
a number on BEFORE a builder writes it into a chain:

  "red bow slows down its shots drastically for a duration and begins shooting
   larger balista shots. The shots gain a homing effect that will seek out its
   opponent. when the shots hit they pierce the enemy ball fly through and fork
   into 2 shots which turn around and try to home in and hit again. the forks
   apply bleed
   the balista shot can be clanked nullifying the fork and destroying the bolt"

v41 built §1 literally and the probe refuted it inside an hour: the shield was
posted on the one side the hammer already guarded, and 67 casts blocked six
blows. That cost a build. The three numbers that could do the same thing here
are known in advance, so they are measured first:

  [2] WHAT HOMING BUYS. `bow_survey` §2: a bow lands 8.3% of what it fires and
      81% of it ends on a wall. Homing is aimed at exactly that 81%, which is
      the type's real constraint -- but nobody has ever steered a shot in this
      engine, and "seeks the opponent" could be worth 3 points or 40.

  [3] WHAT A BIGGER BOLT COSTS. `r` is on BOTH sides of the ledger: the hit
      test is `dist < R + s.r` and the parry test is
      `dist < s.r + width/2 + pad`. A ballista bolt is easier to hit WITH and
      easier to bat out of the air, and §1's counterplay clause depends on
      which of the two grows faster. If the parry wins, the ultimate is a
      present to the foe.

  [4] WHAT SLOWING COSTS. A slower bolt spends longer in the air, which is
      more time for a blade to find it AND more time for homing to work.
      Opposite signs, same knob.

  [5] THE COUNTERPLAY IS THE FOE'S PROPERTY, and it is not flat: `bow_survey`
      §3 measured the parry from 5.9% (warhammer) to 12.0% (twinblade) at
      today's bolt. v40 open decision 5 says that spread has never been priced.
      Under a bolt twice the size it is the difference between an ultimate and
      a formality.

  [6] CAN A FORK TURN AROUND AT ALL? A fork leaves at the bolt's heading with
      the ball behind it. At speed v and turn rate w it cannot come back
      inside a radius of v/w. This is geometry, and if the radius is bigger
      than the hall the sentence cannot be built as written.

  [1] "CLANKED NULLIFIES THE FORK" IS ALREADY THE ENGINE'S RULE, free, because
      `tickShots` resolves the parry BEFORE the hit and a parried shot never
      reaches the branch a fork would hang off. Asserted, not assumed.

Everything below is a WRAPPER on the shipped method, installed on the MATCH
INSTANCE. Nothing re-implements a predicate the game owns. The one thing that
is re-implemented is the classification of a REMOVED shot, which reads the
shot's own final state after the engine has finished mutating it -- and the
parry is TAGGED at its own effect call rather than inferred, `bow_survey`'s
rule, so a sink added to `tickShots` later cannot be silently absorbed.

INJECTION IS RUNTIME-ONLY. Nothing is written to any build.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent

SUBJECT = "ironhail"     # the body. Bloodsworn's channel is carried on it, so
                         # the row is comparable with bow_survey [5].

# The one place §1's numbers live. Everything the sweeps vary is a key here, so
# a control that means "off" can be written as 0 and be read as 0 --  v41's
# `u.feed || 1` bug is one `||` away in every one of these.
BASE = dict(r=24, speed=380, life=3.4, dmgMul=1.0, cadMul=1.0, home=0.0,
            fork=0, forkSpread=0.9, forkSpeedMul=1.0, forkRMul=0.6,
            forkHome=0.0, forkLife=2.2, forkArm=0.18, forkDmgMul=0.5)

RUN_JS = r"""([shooter, foes, seeds, secs, pin, pinIds, noult, aff, chan, B]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const R  = AC.CONFIG.physics.ballR;

  /* The roster is a SHARED object. Everything touched here is saved by value
     and put back at the end, and the caller checks that it was. */
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null, aff: x.aff,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null,
                   onSelf: x.onSelf ? JSON.parse(JSON.stringify(x.onSelf)) : null,
                   cad: x.shot ? x.shot.cadence : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }
  const sub = AC.WEAPONS.find(y => y.id === shooter);
  if (aff){                                   /* carry bloodsworn's channel */
    sub.aff = aff;
    delete sub.onSelf; sub.onHit = {}; sub.onHit[chan[0]] = chan[1];
  }
  if (B.cadMul !== 1) sub.shot.cadence = saved[shooter].cad * B.cadMul;

  const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
  const angDiff = (a, b) => { let d = b - a;
    while (d >  Math.PI) d -= 2 * Math.PI;
    while (d < -Math.PI) d += 2 * Math.PI; return d; };

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      /* ---- the ballista upgrade. A shot the subject loosed, and only that,
         is rewritten in place the frame it is born. Every other shot in the
         match -- including the foe's, if the foe is a bow -- is untouched. */
      let fired = 0, evicted = 0;
      const oSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, ang){
        if (m.shots.length >= AC.CONFIG.shot.maxLive) evicted++;
        const r0 = oSpawn.call(m, fg, ang);
        if (fg === me){
          fired++;
          const s = m.shots[m.shots.length - 1];
          if (s && !s.ult){
            const sp = Math.hypot(s.vx, s.vy) || 1;
            const k  = B.speed / sp;
            s.vx *= k; s.vy *= k;
            s.r = B.r; s.life = B.life; s.max = B.life;
            s.dmgMul = (s.dmgMul === undefined ? 1 : s.dmgMul) * B.dmgMul;
            s.bal = true; s.home = B.home;
          }
        }
        return r0;
      };

      /* ---- the fork. Queued in resolveHit -- which is the only place that
         knows a shot LANDED, and which the engine hands the shot on
         `_cineShot` -- and spawned after tickShots has finished, so nothing
         is inserted into the array the engine is iterating backwards. */
      let landedBal = 0, landedFork = 0, forks = 0, balForked = 0;
      const oRes = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const s = m._cineShot;
        const r = oRes.call(m, self, foe2, hx, hy, seg, mul, over);
        if (s && self === me){
          if (s.fork) landedFork++;
          else if (s.bal){
            landedBal++;
            /* A bolt that KILLED does not fork. Counted apart from
               `landedBal` so the check below is an identity and not an
               approximation -- the first cut asserted forks == 2 x landed and
               failed on exactly the five lethal bolts in the run. */
            if (B.fork > 0 && foe2.alive){
              balForked++;
              m.__q.push({ x: s.x, y: s.y, vx: s.vx, vy: s.vy });
            }
          }
        }
        return r;
      };

      /* ---- the parry tag. bow_survey's rule: the parry is the only
         spawnFx("#FFF4D0", 9, 240) in the file and it fires at the shot's
         exact position. Collected only while inside tickShots. */
      let inShots = false;
      const parryFx = [];
      const oFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n, spd, life, size, dx, dy){
        if (inShots && col === "#FFF4D0" && n === 9 && spd === 240)
          parryFx.push(x + "," + y);
        return oFx.call(m, x, y, col, n, spd, life, size, dx, dy);
      };

      const T = { hit:0, parried:0, walled:0, expired:0, unknown:0, ambig:0,
                  fHit:0, fParried:0, fWalled:0, fExpired:0,
                  balParried:0, forkedFromParried:0 };
      let steerSum = 0, steerN = 0, flightSum = 0, flightN = 0;

      m.__q = [];
      const oTick = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        /* ---- HOMING. Rate limited, so "seeks" is a TRY: a quarry that can
           out-turn the bolt gets round it, exactly as Aegis's `turn` makes
           "tries to face them" a sentence with a failure mode in it. The
           speed is never changed -- only the heading -- so a slower bolt is
           slower because §1 said so and not because steering bled it. */
        for (const s of m.shots){
          if (!s.home) continue;
          const tgt = s.own === "a" ? m.b : m.a;
          if (!tgt.alive) continue;
          const cur  = Math.atan2(s.vy, s.vx);
          const want = Math.atan2(tgt.y - s.y, tgt.x - s.x);
          const d    = angDiff(cur, want);
          const step = clamp(d, -s.home * dt, s.home * dt);
          const na   = cur + step;
          const sp   = Math.hypot(s.vx, s.vy);
          s.vx = Math.cos(na) * sp; s.vy = Math.sin(na) * sp;
          s.a  = na;                       /* the art points where it goes */
          steerSum += Math.abs(step); steerN++;
        }

        const pre = m.shots.slice();
        parryFx.length = 0;
        m.__q.length = 0;
        inShots = true;
        const r = oTick.call(m, dt);
        inShots = false;

        if (pre.length){
          const live = new Set(m.shots);
          const n = m.inset, P = new Set(parryFx);
          for (const s of pre){
            if (live.has(s)) continue;
            if (s.own !== (me === m.a ? "a" : "b")) continue;
            const spent = s.life <= 0 || s.x < n + s.r || s.x > A.w - n - s.r
                                      || s.y < n + s.r || s.y > A.h - n - s.r;
            const parried = P.has(s.x + "," + s.y);
            if (s.fork){
              if (parried) T.fParried++;
              else if (s._ph) T.fHit++;
              else if (s.life <= 0) T.fExpired++;
              else if (spent) T.fWalled++;
              else T.unknown++;
              continue;
            }
            if (parried){ T.parried++; T.balParried++; if (spent) T.ambig++; continue; }
            if (s._ph){ T.hit++; flightSum += (s.max - s.life); flightN++; continue; }
            if (s.life <= 0){ T.expired++; continue; }
            if (spent){ T.walled++; continue; }
            T.unknown++;
          }
        }

        /* ---- the forks are born. Two, diverging by `forkSpread` about the
           bolt's own heading, `forkArm` seconds before they may hit anything
           -- which IS "pierce the enemy ball fly through": the arm window is
           the pass-through, and it is expressed in the engine's own `arm`
           field rather than in a new one. */
        for (const q of m.__q){
          const base = Math.atan2(q.vy, q.vx);
          const sp = Math.hypot(q.vx, q.vy) * B.forkSpeedMul;
          for (let k = 0; k < B.fork; k++){
            const off = B.fork === 1 ? 0
                      : (-B.forkSpread / 2 + B.forkSpread * (k / (B.fork - 1)));
            const a = base + off;
            m.shots.push({
              own: me === m.a ? "a" : "b",
              x: q.x, y: q.y, x0: q.x, y0: q.y, spd0: 0, t0: m.t,
              vx: Math.cos(a) * sp, vy: Math.sin(a) * sp,
              r: Math.max(4, B.r * B.forkRMul),
              life: B.forkLife, max: B.forkLife, grav: 0,
              dmgMul: B.forkDmgMul, arm: B.forkArm,
              home: B.forkHome, fork: true, aff: me.aff, a,
            });
            forks++;
          }
        }
        return r;
      };

      let steps = 0, sepSum = 0, hstop = 0, meStun = 0, thStun = 0;
      while (!m.over && steps < secs / DT){
        const hs = m.hitStop;
        m.step(DT); steps++;
        if (hs > 0) hstop++;
        if (me.stun > 0) meStun++;
        if (th.stun > 0) thStun++;
        sepSum += Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;
      }

      rows.push({ foe: f, seed: sd, steps, dur: steps * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, dealt: me.dealt, taken: th.dealt,
                  thHp: th.hp, thMaxHp: th.maxHp,
                  fired, evicted, forks, landedBal, landedFork, balForked,
                  live: m.shots.filter(s => s.own === (me === m.a ? "a" : "b")).length,
                  sep: steps ? sepSum / steps : 0,
                  hstop: steps ? hstop / steps : 0,
                  thStun: steps ? thStun / steps : 0,
                  meanSteer: steerN ? steerSum / steerN : 0,
                  meanFlight: flightN ? flightSum / flightN : 0,
                  ...T });
    }
  }

  /* ---- put the roster back, by value. */
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid), s = saved[pid];
    x.dmg = s.dmg; x.aff = s.aff;
    if (s.ch !== null) x.ult.charge = s.ch;
    delete x.onHit; delete x.onSelf;
    if (s.onHit) x.onHit = s.onHit;
    if (s.onSelf) x.onSelf = s.onSelf;
    if (s.cad !== null) x.shot.cadence = s.cad;
  }
  return rows;
}"""

# `resolveHit` is where a landed shot is known, and the engine hands it over on
# `_cineShot`. The flag has to be set on the SHOT so the classifier can read it
# one frame later, and `bow_survey` sets `_pHit` for the same reason. `_ph`
# here, set inside the same wrapper.
RUN_JS = RUN_JS.replace(
    "        if (s && self === me){",
    "        if (s) s._ph = true;\n        if (s && self === me){")


ROSTER_JS = """() => JSON.stringify(AC.WEAPONS.map(w => ({
  id: w.id, aff: w.aff, dmg: w.dmg, onHit: w.onHit || null, onSelf: w.onSelf || null,
  shot: w.shot || null, charge: w.ult ? w.ult.charge : null })))"""

PASS = FAILN = 0


def check(name, ok, detail=""):
    global PASS, FAILN
    if ok:
        PASS += 1
    else:
        FAILN += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def agg(rows):
    f = sum(r["fired"] for r in rows) or 1
    fk = sum(r["forks"] for r in rows)
    return dict(
        fired=sum(r["fired"] for r in rows),
        landed=sum(r["hit"] for r in rows) / f,
        parried=sum(r["parried"] for r in rows) / f,
        wall=sum(r["walled"] for r in rows) / f,
        expired=sum(r["expired"] for r in rows) / f,
        unknown=sum(r["unknown"] for r in rows),
        forks=fk,
        forkHit=(sum(r["fHit"] for r in rows) / fk) if fk else 0.0,
        forkParried=(sum(r["fParried"] for r in rows) / fk) if fk else 0.0,
        forkWall=(sum(r["fWalled"] for r in rows) / fk) if fk else 0.0,
        forkExp=(sum(r["fExpired"] for r in rows) / fk) if fk else 0.0,
        hitsPerS=sum(r["hits"] for r in rows) / max(1e-9, sum(r["dur"] for r in rows)),
        dealtPerS=sum(r["dealt"] for r in rows) / max(1e-9, sum(r["dur"] for r in rows)),
        dur=statistics.mean(r["dur"] for r in rows),
        win=statistics.mean(r["win"] for r in rows),
        flight=statistics.mean([r["meanFlight"] for r in rows if r["meanFlight"]] or [0]),
        sep=statistics.mean(r["sep"] for r in rows),
    )


def run(page, cfg, foes, seeds, secs, pin, pin_ids, aff, chan):
    B = dict(BASE); B.update(cfg)
    return page.evaluate(RUN_JS, [SUBJECT, foes, seeds, secs, pin, pin_ids,
                                  True, aff, chan, B])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bulwarden-frame.html")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--secs", type=float, default=90.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--json", default="")
    ap.add_argument("--only", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [4101 + i * 977 for i in range(a.seeds)]
    out = {}
    only = set(a.only.split(",")) if a.only else None

    def want(k):
        return only is None or k in only

    src = gp.read_text()

    with game(game_path=gp) as (page, errors):
        # Taken before anything runs, so "the roster was put back" is a
        # comparison against the shipped state and not against whatever the
        # first sweep happened to leave.
        before = json.loads(page.evaluate(ROSTER_JS))
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, shape:w.shape, aff:w.aff}))")
        pin_ids = [w["id"] for w in W]
        # One foe per SHAPE plus every bow excluded: a bow foe fires back and
        # its shots would land in the same array this probe is classifying.
        by_shape = {}
        for w in W:
            if w["shape"] == "bow":
                continue
            by_shape.setdefault(w["shape"], []).append(w["id"])
        foes = [ids[0] for ids in by_shape.values()]
        chan = ["hemorrhage", 2]

        print(f"\n§1 PRICED — bloodsworn's channel on {SUBJECT}'s body, damage pinned "
              f"{a.pin}, ultimates suppressed\n    foes {', '.join(foes)}   "
              f"{len(seeds)} seeds   {a.secs:.0f}s cap")

        # ------------------------------------------------------------ [0] --
        print("\n[0] CONTROL — does the instrument move the simulation?\n")
        base = run(page, {}, foes, seeds, a.secs, a.pin, pin_ids, "bloodsworn", chan)
        clean = page.evaluate(
            """([sh, foes, seeds, secs, pin, ids]) => {
              const DT = AC.CONFIG.physics.dt, saved = {};
              for (const pid of ids){ const x = AC.WEAPONS.find(y=>y.id===pid); if(!x) continue;
                saved[pid] = {dmg:x.dmg, ch:x.ult?x.ult.charge:null, aff:x.aff,
                              onHit:x.onHit?JSON.parse(JSON.stringify(x.onHit)):null,
                              onSelf:x.onSelf?JSON.parse(JSON.stringify(x.onSelf)):null};
                x.dmg = pin; if (x.ult) x.ult.charge = 1e9; }
              const sub = AC.WEAPONS.find(y=>y.id===sh);
              sub.aff = "bloodsworn"; delete sub.onSelf; sub.onHit = {hemorrhage:2};
              const rows = [];
              for (const f of foes) for (const sd of seeds){
                const m = new AC.Match(sh, f, sd);
                const me = m.a.w.id===sh ? m.a : m.b, th = me===m.a?m.b:m.a;
                let steps = 0;
                while (!m.over && steps < secs/DT){ m.step(DT); steps++; }
                rows.push({steps, hits:me.hits, dealt:me.dealt, thHp:th.hp,
                           fired:me.shotsFired});
              }
              for (const pid of Object.keys(saved)){
                const x = AC.WEAPONS.find(y=>y.id===pid), s = saved[pid];
                x.dmg = s.dmg; x.aff = s.aff; if (s.ch!==null) x.ult.charge = s.ch;
                delete x.onHit; delete x.onSelf;
                if (s.onHit) x.onHit = s.onHit; if (s.onSelf) x.onSelf = s.onSelf; }
              return rows;
            }""", [SUBJECT, foes, seeds, a.secs, a.pin, pin_ids])
        same = all(
            b["steps"] == c["steps"] and abs(b["dealt"] - c["dealt"]) < 1e-9
            and b["hits"] == c["hits"] and abs(b["thHp"] - c["thHp"]) < 1e-9
            and b["fired"] == c["fired"]
            for b, c in zip(base, clean))
        check("wrapping spawnShot/resolveHit/spawnFx/tickShots changes nothing",
              same, f"{len(base)} runs, steps+hits+dealt+foe hp+fired field for field")
        A0 = agg(base)
        check("the baseline reproduces bow_survey §2 — a bow lands ~8% and walls ~81%",
              0.06 <= A0["landed"] <= 0.11 and 0.76 <= A0["wall"] <= 0.86,
              f"landed {A0['landed']:.1%}  parried {A0['parried']:.1%}  "
              f"wall {A0['wall']:.1%}  of {A0['fired']} fired")
        check("every subject arrow is classified — no sink this probe does not know",
              sum(r["unknown"] for r in base) == 0,
              f"{sum(r['unknown'] for r in base)} unknown, "
              f"{sum(r['ambig'] for r in base)} parries also past the wall line")

        # ------------------------------------------------------------ [2] --
        print("\n[2] WHAT HOMING BUYS — turn rate on today's bolt, everything else held\n")
        print(f"    {'turn rad/s':<12}{'fired':>7}{'landed':>9}{'parried':>9}{'wall':>8}"
              f"{'flight s':>10}{'hits/s':>8}{'dmg/s':>8}{'ttk':>7}")
        HOME = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 12.0]
        home_rows = {}
        for w in HOME:
            rs = base if w == 0.0 else run(page, {"home": w}, foes, seeds, a.secs,
                                           a.pin, pin_ids, "bloodsworn", chan)
            g = agg(rs); home_rows[w] = g
            print(f"    {w:<12.2f}{g['fired']:>7}{g['landed']:>9.1%}{g['parried']:>9.1%}"
                  f"{g['wall']:>8.1%}{g['flight']:>10.2f}{g['hitsPerS']:>8.3f}"
                  f"{g['dealtPerS']:>8.2f}{g['dur']:>7.1f}")
        out["home"] = {str(k): v for k, v in home_rows.items()}
        lo, hi = home_rows[0.0]["landed"], home_rows[12.0]["landed"]
        check("homing is worth measuring at all — the landed rate moves by more "
              "than the arm on the baseline", hi > lo * 1.5,
              f"{lo:.1%} at 0 rad/s -> {hi:.1%} at 12 rad/s  ({hi/max(lo,1e-9):.1f}x)")
        check("the wall is what homing eats — v40's 81% is the number it attacks",
              home_rows[12.0]["wall"] < home_rows[0.0]["wall"] - 0.10,
              f"wall {home_rows[0.0]['wall']:.1%} -> {home_rows[12.0]['wall']:.1%}")

        # ------------------------------------------------------------ [3] --
        print("\n[3] WHAT A BIGGER BOLT COSTS — `r` is on both sides of the ledger\n")
        print(f"    {'r':<8}{'fired':>7}{'landed':>9}{'parried':>9}{'wall':>8}"
              f"{'par/land':>10}{'hits/s':>8}{'dmg/s':>8}")
        SZ = [24, 32, 40, 48, 60]
        size_rows = {}
        for r in SZ:
            rs = base if r == 24 else run(page, {"r": r}, foes, seeds, a.secs,
                                          a.pin, pin_ids, "bloodsworn", chan)
            g = agg(rs); size_rows[r] = g
            print(f"    {r:<8}{g['fired']:>7}{g['landed']:>9.1%}{g['parried']:>9.1%}"
                  f"{g['wall']:>8.1%}{g['parried']/max(g['landed'],1e-9):>10.2f}"
                  f"{g['hitsPerS']:>8.3f}{g['dealtPerS']:>8.2f}")
        out["size"] = {str(k): v for k, v in size_rows.items()}
        r0 = size_rows[24]["parried"] / max(size_rows[24]["landed"], 1e-9)
        r1 = size_rows[60]["parried"] / max(size_rows[60]["landed"], 1e-9)
        print(f"\n    parried per landed: {r0:.2f} at r=24  ->  {r1:.2f} at r=60")
        check("§1's counterplay clause has teeth OR it does not — the ratio is "
              "measured either way", True,
              "the bolt gets " + ("MORE" if r1 > r0 else "LESS")
              + f" clankable per hit as it grows ({r0:.2f} -> {r1:.2f})")

        # ------------------------------------------------------------ [4] --
        print("\n[4] WHAT SLOWING COSTS — longer in the air is more parry AND more steering\n")
        print(f"    {'speed':<8}{'home':>6}{'fired':>7}{'landed':>9}{'parried':>9}"
              f"{'wall':>8}{'flight s':>10}{'hits/s':>8}")
        spd_rows = {}
        for sp in [380, 300, 220, 150]:
            for hm in [0.0, 2.0]:
                rs = run(page, {"speed": sp, "home": hm}, foes, seeds, a.secs,
                         a.pin, pin_ids, "bloodsworn", chan)
                g = agg(rs); spd_rows[f"{sp}|{hm}"] = g
                print(f"    {sp:<8}{hm:>6.1f}{g['fired']:>7}{g['landed']:>9.1%}"
                      f"{g['parried']:>9.1%}{g['wall']:>8.1%}{g['flight']:>10.2f}"
                      f"{g['hitsPerS']:>8.3f}")
        out["speed"] = spd_rows

        # ------------------------------------------------------------ [6] --
        print("\n[6] CAN A FORK TURN AROUND — and what happens to the two that are born\n")
        print(f"    {'fork turn':<11}{'r ratio':>9}{'forks':>7}{'hit':>8}{'parried':>9}"
              f"{'wall':>8}{'expired':>9}{'hits/s':>8}{'dmg/s':>8}")
        fork_rows = {}
        PROP = {"r": 44, "speed": 220, "home": 2.0, "cadMul": 3.0,
                "dmgMul": 2.2, "fork": 2}
        for ft in [0.0, 1.0, 2.0, 4.0, 8.0]:
            cfg = dict(PROP); cfg["forkHome"] = ft
            rs = run(page, cfg, foes, seeds, a.secs, a.pin, pin_ids, "bloodsworn", chan)
            g = agg(rs); fork_rows[ft] = g
            v = 220 * BASE["forkSpeedMul"]
            rad = v / ft if ft else float("inf")
            print(f"    {ft:<11.1f}{rad:>9.0f}{g['forks']:>7}{g['forkHit']:>8.1%}"
                  f"{g['forkParried']:>9.1%}{g['forkWall']:>8.1%}{g['forkExp']:>9.1%}"
                  f"{g['hitsPerS']:>8.3f}{g['dealtPerS']:>8.2f}")
        out["fork"] = {str(k): v for k, v in fork_rows.items()}
        best = max(fork_rows.values(), key=lambda g: g["forkHit"])
        check("a fork CAN come back and connect — the sentence is buildable",
              best["forkHit"] > 0.05,
              f"best return rate {best['forkHit']:.1%} of forks; "
              f"turn radius at 220 u/s is v/w — 220 at 1 rad/s, 55 at 4")
        acct = {}
        for ft, g in fork_rows.items():
            acct[ft] = g["forkHit"] + g["forkParried"] + g["forkWall"] + g["forkExp"]
        check("every fork is accounted for — hit, batted, wall or run out, with "
              "the remainder still in flight at the whistle",
              all(0.9 <= v <= 1.0001 for v in acct.values()),
              "  ".join(f"{k:g}:{v:.1%}" for k, v in acct.items()))
        check("a HARD-homing fork stops ending on walls entirely — the wall is "
              "what the whole ultimate is aimed at",
              fork_rows[8.0]["forkWall"] < 0.02 < fork_rows[0.0]["forkWall"],
              f"wall {fork_rows[0.0]['forkWall']:.1%} at turn 0 -> "
              f"{fork_rows[8.0]['forkWall']:.1%} at turn 8")

        # ------------------------------------------------------------ [1] --
        print("\n[1] \"CLANKED NULLIFIES THE FORK\" — already the engine's rule\n")
        pro = run(page, PROP | {"forkHome": 4.0}, foes, seeds, a.secs, a.pin,
                  pin_ids, "bloodsworn", chan)
        gp_ = agg(pro)
        nbal = sum(r["balForked"] for r in pro)
        nkill = sum(r["landedBal"] for r in pro) - nbal
        nfork = sum(r["forks"] for r in pro)
        npar = sum(r["balParried"] for r in pro)
        parry_i = src.index("--- the parry")
        hit_i = src.index("--- the hit.")
        check("in tickShots the parry branch is resolved BEFORE the hit branch, "
              "so a batted bolt never reaches the branch a fork hangs off",
              parry_i < hit_i, f"parry at char {parry_i}, hit at {hit_i}")
        check("and behaviourally: forks == 2 x bolts that landed on a foe that "
              "SURVIVED, with batted bolts producing none",
              nfork == 2 * nbal and npar > 0,
              f"{nbal} bolts landed on a live foe -> {nfork} forks; {npar} were "
              f"batted out of the air and {nkill} were lethal, and neither "
              f"forked")

        # ------------------------------------------------------------ [5] --
        print("\n[5] THE COUNTERPLAY IS THE FOE'S — the parry spread, today's bolt "
              "against the ballista\n")
        print(f"    {'foe':<14}{'shape':<12}{'today par':>11}{'today land':>12}"
              f"{'bal par':>10}{'bal land':>10}{'fork/hit':>10}")
        shp = {w["id"]: w["shape"] for w in W}
        spread = {}
        for fo in foes:
            b1 = run(page, {}, [fo], seeds, a.secs, a.pin, pin_ids, "bloodsworn", chan)
            b2 = run(page, PROP | {"forkHome": 4.0}, [fo], seeds, a.secs, a.pin,
                     pin_ids, "bloodsworn", chan)
            g1, g2 = agg(b1), agg(b2)
            spread[fo] = (g1, g2)
            fh = sum(r["forks"] for r in b2) / max(1, sum(r["landedBal"] for r in b2))
            print(f"    {fo:<14}{shp[fo]:<12}{g1['parried']:>11.1%}{g1['landed']:>12.1%}"
                  f"{g2['parried']:>10.1%}{g2['landed']:>10.1%}{fh:>10.2f}")
        out["spread"] = {k: {"today": v[0], "bal": v[1]} for k, v in spread.items()}
        pv = [v[1]["parried"] for v in spread.values()]
        pv0 = [v[0]["parried"] for v in spread.values()]
        check("the ballista does not flatten the foe's counterplay into a constant",
              max(pv) / max(min(pv), 1e-9) > 1.4,
              f"today {min(pv0):.1%}-{max(pv0):.1%} ({max(pv0)/max(min(pv0),1e-9):.1f}x), "
              f"ballista {min(pv):.1%}-{max(pv):.1%} "
              f"({max(pv)/max(min(pv),1e-9):.1f}x)")

        # ------------------------------------------------------------ [7] --
        print("\n[7] THE TRAPS\n")
        after = json.loads(page.evaluate(ROSTER_JS))
        check("the roster is put back — dmg, aff, channels, cadence and charge, "
              "by value", after == before,
              "23 relics identical field for field"
              if after == before else "THE ROSTER WAS LEFT MUTATED")
        gated = page.evaluate(
            "() => { const s = AC.WEAPONS.find(w=>w.shape!=='bow'); "
            "return { hasShot: !!s.shot, mode: s.mode }; }")
        check("v39 od 4 / v40 §6.1 — `tickFire` still gates on `f.w.shot` and not "
              "on mode, so a `shot` field on a melee relic would fire a bow",
              not gated["hasShot"],
              "inert today because no melee relic carries one — the exact "
              "condition an ult that swaps the shot block must not break")
        assert not errors, errors[:3]

    print(f"\n{PASS}/{PASS + FAILN} checks passed"
          + (f"  ({FAILN} FAILED)" if FAILN else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 1 if FAILN else 0


if __name__ == "__main__":
    sys.exit(main())
