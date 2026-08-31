#!/usr/bin/env python3
"""RICK'S §1 FOR THE PURPLE FLAIL, PRICED.

    "when the ult fires for a duration the flails chain gains length and then
     each time it lands a hit an etheral purple hand flys off the hit. the hand
     soars around the arena briefly and then clenches into a fist as it dive
     bombs into the enemy fighter. on contact it applies curse and deals
     massive knockback."

THE LOAD-BEARING QUESTION IS NOT THE HAND, IT IS THE CHAIN. This is a WINDOW
mechanic on the relic with the fewest blows in the game -- 5.6 a fight, 0.134
a second. A plain 8-second window contains ONE blow, and v50 §4 measured every
window shape on this relic at +3%. What makes the design survivable is the
half nobody would have thought to add: `wh_survey` established that contact
rate in this sim is REACH-dominated, so a longer chain is not decoration, it
is the thing that manufactures the hands. [1] measures whether it does.

  [1] THE CHAIN. Blows inside the window per cast, against chain multiplier
      and duration. No payload at all, so the column prices CONTACT.
  [2] THE HAND. What it pays, at the chain and duration [1] supports.
  [3] THE KNOCKBACK EATING ITS OWN WINDOW. v41 measured Grudgebearer's
      knockMul 2.3 costing 12% of its contacts. A hand that flings the quarry
      away mid-window is spawning fewer hands, and that loop is the design's
      one self-inflicted wound. Swept.

Base curse in every arm is v49's recommendation: K=3, echo 8%, permanent,
displacement kept, priced on the target. `apply:{curse:3}` is stripped from
Dirge in every arm -- it is what this replaces.

The hand is modelled as a DELAYED, CERTAIN hit: it always finds the foe after
its flight. A real build's hand can miss, be blocked by an Aegis wall, or
arrive after the fight ends; the last of those IS modelled (a hand in flight
when the match ends never lands). Runtime injection only; nothing is written.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent
DONOR = "gravemourn"

JS = r"""([donor, foes, seeds, secs, K, RATE, CHAIN, DUR, FLY, KNOCK, PAY, P1, HPB]) => {
  const DT = AC.CONFIG.physics.dt, CU = AC.STATUS.curse;
  const oL = CU.maxHpLoss, oC = CU.maxStacks;
  const origResolve = AC.Match.prototype.resolveHit;
  const origFire = AC.Match.prototype.fireUlt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const baseReach = w.reach, savedApply = w.ult.apply;
  delete w.ult.apply;
  CU.maxHpLoss = 0; CU.maxStacks = K;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    w.reach = baseReach;                       // never inherit a window
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const pool = [], hands = [];
    let inR = false, hitSrc = null, hitD0 = 0;
    let winUntil = -1, casts = 0, winBlows = 0, spawned = 0, landed = 0;
    let handDmg = 0, echoDealt = 0, baseDealt = 0, blows = 0, winOpen = 0;

    const trim = () => { pool.sort((a,b)=>b-a); while (pool.length > K) pool.pop(); };
    const origApply = th.apply.bind(th);
    th.apply = function(key, n){
      if (key === "curse"){
        const v = inR ? (hitSrc.dealt - hitD0) : 0;
        if (v > 0){ for (let i=0;i<n;i++) pool.push(v); trim(); }
      }
      return origApply(key, n);
    };

    m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      if (foe !== th) return origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      const d0 = self.dealt, h0 = self.hits;
      let s = 0; for (const v of pool) s += v;
      const echo = Math.round(s * RATE);
      inR = true; hitSrc = self; hitD0 = d0;
      origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      inR = false;
      if (self.hits === h0) return;
      const d = self.dealt - d0;
      blows++; baseDealt += d;
      if (echo > 0 && foe.alive){ this.hurt(foe, echo, self); echoDealt += echo; }
      /* THE HAND COMES OFF THE BLOW, so it carries that blow's own number. */
      if (self === me && winUntil > this.t){
        winBlows++;
        /* ONE HAND PER REMEMBERED BLOW. The hand TAKES the memory with it at
           the moment it peels off, so the pool empties on the blow and each
           hand carries exactly one stack -- the count on screen IS the chip. */
        if (PAY === "poolhands" || PAY === "carrykeep"){
          const n = pool.length;
          for (let i = 0; i < n; i++){
            const v = pool.shift();
            spawned++;
            hands.push({ at: this.t + FLY * (1 + i * 0.45), mem: v, carried: true });
          }
          return;
        }
        /* HANDS PER BLOW. The picture wants a flock; the relic lands 1.3
           blows a cast. Staggered so they arrive as a sequence, not a lump. */
        for (let i = 0; i < HPB; i++){
          spawned++;
          hands.push({ at: this.t + FLY * (1 + i * 0.45), mem: d / HPB });
        }
      }
    };

    m.fireUlt = function(fr, foe){
      const r = origFire.call(this, fr, foe);
      if (fr === me && foe === th){
        casts++; winUntil = this.t + DUR; w.reach = baseReach * CHAIN;
      }
      return r;
    };

    let step = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      if (winUntil > 0 && m.t > winUntil){
        winUntil = -1; w.reach = baseReach;
      } else if (winUntil > 0) winOpen += DT;
      while (hands.length && hands[0].at <= m.t){
        const h = hands.shift();
        if (!th.alive || !me.alive) continue;
        landed++;
        const dx = th.x - me.x, dy = th.y - me.y, dl = Math.hypot(dx,dy) || 1;
        th.vx += (dx/dl) * KNOCK; th.vy += (dy/dl) * KNOCK;
        if (PAY === "apply"){                  // the hand deepens the memory
          if (h.mem > 0){ pool.push(h.mem); trim(); }
        } else if (PAY === "spend"){           // the hand cashes the largest
          if (pool.length){
            const v = pool.shift();
            const d2 = Math.round(v * P1);
            if (d2 > 0){ m.hurt(th, d2, me); me.dealt += d2; handDmg += d2; }
          }
        } else if (PAY === "flat"){
          const d2 = Math.round(P1);
          m.hurt(th, d2, me); me.dealt += d2; handDmg += d2;
        } else if (PAY === "hit" || PAY === "hitcurse"){
          /* RICK'S HAND, READ STRAIGHT: it deals its OWN damage, and under the
             reworked curse the stack it applies remembers THAT damage -- so
             the hand is a blow, not a hollow stack. This is the arm the first
             pass never ran; its `apply` arm gave the hand zero damage and had
             it duplicate a value the blade had already parked, which is a
             different design and a strawman of this one. */
          const d2 = Math.round(P1 * th.dmgTakenMul());
          if (d2 > 0){ m.hurt(th, d2, me); me.dealt += d2; handDmg += d2; }
          if (PAY === "hitcurse" && d2 > 0 && th.alive){ pool.push(d2); trim(); }
        } else if (PAY === "carrykeep"){
          /* ALL FOUR OF RICK'S CLAUSES AT ONCE: the hand carries a remembered
             blow, DEALS it, and -- because a hand that lands is a hit --
             APPLIES curse remembering what it just dealt. The memory is spent
             and re-parked in the same instant, so the pool is refreshed
             rather than emptied. */
          const d2 = Math.round(h.mem * P1);
          if (d2 > 0){
            m.hurt(th, d2, me); me.dealt += d2; handDmg += d2;
            if (th.alive){ pool.push(d2); trim(); }
          }
        } else if (PAY === "poolhands"){       // the hand carries one memory
          const d2 = Math.round(h.mem * P1);
          if (d2 > 0){ m.hurt(th, d2, me); me.dealt += d2; handDmg += d2; }
        } else if (PAY === "memory"){          // the hand IS the blow, again
          const d2 = Math.round(h.mem * P1);
          if (d2 > 0){ m.hurt(th, d2, me); me.dealt += d2; handDmg += d2; }
        }
        th.flash = 1;
      }
    }
    w.reach = baseReach;
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                casts, winBlows, spawned, landed, handDmg, echoDealt, baseDealt,
                blows, winOpen, dur: step * DT,
                taken: th.dealt, foeHits: th.hits, myHp: me.hp,
                perCast: casts ? winBlows / casts : 0 });
  }
  w.reach = baseReach;
  CU.maxHpLoss = oL; CU.maxStacks = oC;
  if (savedApply) w.ult.apply = savedApply;
  return rows;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--K", type=int, default=3)
ap.add_argument("--rate", type=float, default=0.08)
ap.add_argument("--stage", default="chain")
ap.add_argument("--chain", type=float, default=1.6)
ap.add_argument("--dur", type=float, default=8.0)
ap.add_argument("--fly", type=float, default=1.2)
ap.add_argument("--knock", type=float, default=400.0)
ap.add_argument("--hpb", type=int, default=1)
a = ap.parse_args()
seeds = [3301 + 19 * i for i in range(a.seeds)]

def run(page, foes, chain, dur, fly, knock, pay, p1, hpb=1):
    return page.evaluate(JS, [DONOR, foes, seeds, a.secs, a.K, a.rate,
                              chain, dur, fly, knock, pay, p1, hpb])

with game(game_path=(HERE / a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != DONOR]
    base_reach = page.evaluate(f"() => AC.WEAPONS.find(w=>w.id==='{DONOR}').reach")
    mm = lambda rows, k: statistics.mean([r[k] for r in rows])
    wr = lambda rows: (lambda f: sum(r["win"] for r in f)/len(f))([r for r in rows if r["win"] >= 0])
    print(f"\nGRAVEMOURN, base reach {base_reach}. curse K={a.K}, echo {a.rate:.0%}. "
          f"{a.seeds} seeds x 25 foes = {25*a.seeds} fights an arm")

    if a.stage == "chain":
        print(f"\n[1] THE CHAIN — does length manufacture the hands? "
              f"(no payload, knock 0)\n")
        print(f"    {'chain':>7}{'reach':>7}{'blows':>7}{'in win':>8}{'dealt':>8}"
              f"{'TAKEN':>8}{'foe blows':>11}{'fight len':>11}{'win':>8}")
        for chain in (1.0, 1.15, 1.3, 1.45, 1.6, 2.0):
            for dur in (a.dur,):
                r = run(page, foes, chain, dur, a.fly, 0.0, "none", 0)
                print(f"    {chain:>7.2f}{base_reach*chain:>7.0f}"
                      f"{mm(r,'blows'):>7.1f}{mm(r,'winBlows'):>8.2f}"
                      f"{mm(r,'baseDealt')+mm(r,'echoDealt'):>8.0f}{mm(r,'taken'):>8.0f}"
                      f"{mm(r,'foeHits'):>11.1f}{mm(r,'dur'):>10.1f}s{wr(r):>8.1%}")
        print(f"\n    duration sweep at chain {a.chain}:")
        print(f"    {'dur':>7}{'blows in window':>17}{'per cast':>10}{'hands/fight':>13}{'win':>8}")
        for dur in (5.0, 8.0, 12.0, 16.0):
            r = run(page, foes, a.chain, dur, a.fly, 0.0, "none", 0)
            print(f"    {dur:>7.0f}{mm(r,'winBlows'):>17.2f}{mm(r,'perCast'):>10.2f}"
                  f"{mm(r,'spawned'):>13.2f}{wr(r):>8.1%}")

    if a.stage == "hit":
        print(f"\n[4] THE HAND AS A BLOW — chain {a.chain}, {a.dur:.0f}s, "
              f"{a.hpb} hand(s) a blow, knock {a.knock:.0f}\n")
        print(f"    {'hand dmg':>9}{'no curse':>11}{'+ curse':>10}{'curse adds':>12}"
              f"{'hands':>8}{'landed':>8}{'hand dmg/fight':>16}")
        base = None
        for d in (0, 15, 30, 45, 60):
            a_ = run(page, foes, a.chain, a.dur, a.fly, a.knock, "hit", d, a.hpb)
            b_ = run(page, foes, a.chain, a.dur, a.fly, a.knock, "hitcurse", d, a.hpb)
            print(f"    {d:>9}{wr(a_):>11.1%}{wr(b_):>10.1%}{wr(b_)-wr(a_):>+12.1%}"
                  f"{mm(b_,'spawned'):>8.2f}{mm(b_,'landed'):>8.2f}{mm(b_,'handDmg'):>16.0f}")
        print(f"\n    {'variant':34}{'win':>8}{'hands':>8}{'landed':>8}{'hand dmg':>10}{'echo':>7}")
        for pay, p1, lab in [("poolhands", 1.0, "carries a memory, SPENDS it"),
                             ("carrykeep", 1.0, "carries it, deals it, RE-APPLIES it"),
                             ("carrykeep", 0.7, "same, x0.7"),
                             ("carrykeep", 1.4, "same, x1.4")]:
            r = run(page, foes, a.chain, a.dur, a.fly, a.knock, pay, p1, a.hpb)
            print(f"    {lab:34}{wr(r):>8.1%}{mm(r,'spawned'):>8.2f}"
                  f"{mm(r,'landed'):>8.2f}{mm(r,'handDmg'):>10.0f}{mm(r,'echoDealt'):>7.0f}")

    if a.stage == "pay":
        print(f"\n[2] THE HAND — chain {a.chain}, {a.dur:.0f}s window, "
              f"{a.fly:.1f}s flight, knock {a.knock:.0f}\n")
        print(f"    {'payload':16}{'win':>8}{'worth':>8}{'hands':>8}{'landed':>8}"
              f"{'hand dmg':>10}{'echo':>7}{'blade':>8}")
        arms = [("none", 0), ("apply", 0), ("spend", 1.0),
                ("poolhands", 0.7), ("poolhands", 1.0), ("poolhands", 1.4),
                ("poolhands", 2.0)]
        base = None
        for pay, p1 in arms:
            r = run(page, foes, a.chain, a.dur, a.fly, a.knock, pay, p1, a.hpb)
            w_ = wr(r)
            if base is None: base = w_
            lab = pay if pay in ("none","apply") else f"{pay} x{p1:g}"
            print(f"    {lab:16}{w_:>8.1%}{w_-base:>+8.1%}{mm(r,'spawned'):>8.2f}"
                  f"{mm(r,'landed'):>8.2f}{mm(r,'handDmg'):>10.0f}"
                  f"{mm(r,'echoDealt'):>7.0f}{mm(r,'baseDealt'):>8.0f}")

    if a.stage == "knock":
        print(f"\n[3] DOES THE KNOCKBACK EAT ITS OWN WINDOW? "
              f"chain {a.chain}, {a.dur:.0f}s, memory x1.0\n")
        print(f"    {'knock':>7}{'blows in window':>17}{'hands':>8}{'hand dmg':>10}"
              f"{'blows/fight':>13}{'win':>8}")
        for kn in (0, 200, 400, 700, 1000):
            r = run(page, foes, a.chain, a.dur, a.fly, kn, "memory", 1.0, a.hpb)
            print(f"    {kn:>7.0f}{mm(r,'winBlows'):>17.2f}{mm(r,'spawned'):>8.2f}"
                  f"{mm(r,'handDmg'):>10.0f}{mm(r,'blows'):>13.1f}{wr(r):>8.1%}")

    assert not errors, errors[:3]
