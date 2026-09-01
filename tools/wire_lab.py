#!/usr/bin/env python3
"""THE BARBED WIRE RING ON THE BLOODSWORN WARHAMMER — Rick's §1, priced.

§1: "the hammer gains massive rotational speed. It also gets a barbed wire ring
around it that matches its hit range. enemies caught in the barbed wire are
stunned, gain a bleed stack, and are held until the hammer comes around and
connects. the connection deals massive knockback and causes the barbed wire ring
to explode and expire, applying bleed again."

THREE THINGS IN ONE WINDOW, and the point of this lab is to find out which of
them the value is actually in:

  SPIN     the head turns faster, so it lands more blows. `mode:"spin"` is what
           a warhammer already is, so this is a rate change and nothing else.
           Crucible (3.4x), Reprisal (6.0x) and Bloodmill (6.9x) all do it.
  RING     a catch at hit range: stun + a bleed stack, held.
  CONNECT  the head comes around, hits, throws the foe, and the ring goes off.

The hold is NOT a free parameter — it is however long the head takes to come
round, so it falls out of the spin. Faster spin = shorter hold and a sooner
payoff. grab_lab's law was +2.6 win points per second held; if that law governs
here too the hold is worth almost nothing and the value has to be in the other
two. That is the registered prediction.

Grudgebearer stands in as a bloodsworn warhammer with its own Crucible
suppressed, exactly as grab_lab used it for the umbral one, so the two sets of
numbers are comparable. Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations
import argparse, json, math, pathlib, statistics, sys

WIRE_JS = r"""([cfg, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === cfg.donor);
  const saved = { aff:w.aff, dmg:w.dmg, spin:w.spin, charge:w.ult.charge,
                  onHit:w.onHit?JSON.parse(JSON.stringify(w.onHit)):null,
                  onSelf:w.onSelf?JSON.parse(JSON.stringify(w.onSelf)):null };
  w.aff = cfg.aff; delete w.onHit; delete w.onSelf;
  if (cfg.chan) { w.onHit = {}; w.onHit[cfg.chan] = cfg.chanPer; }
  if (cfg.dmg !== null) w.dmg = cfg.dmg;
  w.ult.charge = 1e9;                       // the donor's own ultimate never fires
  const BASE_SPIN = saved.spin;
  const KNOCK = AC.CONFIG.combat.knock * (w.knockMul || 1);
  const BASE_CAP = AC.STATUS[cfg.chan].maxStacks;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m  = new AC.Match(cfg.donor, f, sd);
    const me = m.a.w.id === cfg.donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;

    let steps=0, clock=0, winT=null, casts=0, catches=0, connects=0;
    let heldT=0, spunT=0, caught=false, expired=0;
    w.spin = BASE_SPIN;

    while (!m.over && steps < secs/DT){
      m.step(DT); steps++;
      if (m.hitStop > 0) continue;             // sim frozen; so is the window
      if (!cfg.on){ continue; }

      if (winT === null){
        clock += DT;
        if (clock >= cfg.charge && me.hp > 0){
          winT = 0; clock = 0; casts++; caught = false;
          if (cfg.spin) w.spin = BASE_SPIN * cfg.spinMul;
          if (cfg.ceiling) AC.STATUS[cfg.chan].maxStacks = cfg.ceiling;
        }
      } else {
        winT += DT; spunT += DT;
        const dx = th.x - me.x, dy = th.y - me.y;
        const d  = Math.hypot(dx, dy);

        if (cfg.ring && !caught && d <= cfg.radius && th.hp > 0){
          caught = true; catches++;
          th.apply(cfg.chan, cfg.bleedCatch);
        }
        if (caught && th.hp > 0){
          heldT += DT;
          /* "held until the hammer comes around" -- refreshed every frame, so
             the hold's LENGTH is not a knob: it is however long the head takes.
             Cleared below if the window ends first, or the foe would keep a
             stun the ultimate never paid for. */
          if (cfg.stun) th.stun = Math.max(th.stun, DT * 2);
          if (cfg.pin){ th.pin = Math.max(th.pin, DT * 2);
                        th.pinMax = Math.max(th.pinMax, DT * 2);
                        if (!th.pinV) th.pinV = [th.vx, th.vy]; }
          // the head comes around: theta within `eps` of the bearing to the foe
          const bearing = Math.atan2(dy, dx);
          let da = Math.abs(((me.theta - bearing + Math.PI) % (2*Math.PI)
                             + 2*Math.PI) % (2*Math.PI) - Math.PI);
          if (da <= cfg.eps && d <= cfg.radius + 20){
            connects++;
            if (cfg.connect){
              let bonus = 0;
              if (cfg.consume){
                /* THE RING EXPLODES THE BLEED. Crucible's verb, which bloodsworn
                   has never used: the payoff scales with what the hammer put on
                   rather than adding a stack to a bar that is already full. */
                const st = th.stacks(cfg.chan);
                bonus = st * cfg.consumePer;
                delete th.status[cfg.chan];
              }
              m.hurt(th, w.dmg * cfg.connectMul + bonus, me);
              if (!cfg.consume) th.apply(cfg.chan, cfg.bleedBlow);
              const kl = d || 1, p = KNOCK * cfg.knockMul;
              th.vx += (dx/kl)*p; th.vy += (dy/kl)*p;
              if (cfg.stun) th.stun = 0; if (cfg.pin) th.pin = 0;
            }
            caught = false;
            if (cfg.endOnConnect){ winT = null; w.spin = BASE_SPIN;
                                   if (cfg.ceiling) AC.STATUS[cfg.chan].maxStacks = BASE_CAP; }
          }
        }
        if (winT !== null && winT >= cfg.dur){
          winT = null; w.spin = BASE_SPIN;
          if (cfg.ceiling) AC.STATUS[cfg.chan].maxStacks = BASE_CAP;
          if (caught){ expired++; if (cfg.stun) th.stun = 0; if (cfg.pin) th.pin = 0; }
          caught = false;
        }
      }
    }
    w.spin = BASE_SPIN; AC.STATUS[cfg.chan].maxStacks = BASE_CAP;
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1, dur: steps*DT,
                hits: me.hits, dealt: me.dealt, foeHits: th.hits,
                casts, catches, connects, heldT, spunT, expired });
  }
  w.aff=saved.aff; w.dmg=saved.dmg; w.spin=saved.spin; w.ult.charge=saved.charge;
  delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return rows;
}"""

BASE = dict(donor="grudgebearer", aff="bloodsworn", chan="hemorrhage", chanPer=2,
            dmg=None, charge=16.0, dur=8.0, radius=110.0, spinMul=6.0,
            eps=0.25, pin=False, connectMul=1.0, knockMul=3.0,
            bleedCatch=1, bleedBlow=2, spin=True, ring=True, connect=True,
            endOnConnect=True, on=True, consume=False, consumePer=8.0, ceiling=0,
            stun=True)

def summarise(rows):
    ok=[r for r in rows if r["win"]>=0]
    g=lambda k: statistics.mean([r[k] for r in rows])
    return dict(n=len(ok), win=statistics.mean([r["win"] for r in ok]) if ok else 0,
                casts=g("casts"), catch=g("catches"), conn=g("connects"),
                held=g("heldT"), spun=g("spunT"), hits=g("hits"),
                dealt=g("dealt"), foe=g("foeHits"), dur=g("dur"), exp=g("expired"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=12); ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="/tmp/wire_lab.json")
    ap.add_argument("--arms", default="")
    a=ap.parse_args()
    sys.path.insert(0, str(pathlib.Path(a.repo)/"tools"))
    from scpage import game
    seeds=[3301+19*i for i in range(a.seeds)]
    out={}
    def run(page, foes, **kw):
        cfg=dict(BASE); cfg.update(kw)
        return summarise(page.evaluate(WIRE_JS, [cfg, foes, seeds, a.secs]))
    with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
        ids=page.evaluate("() => AC.WEAPONS.map(w=>w.id)")
        foes=[i for i in ids if i!="grudgebearer"]
        n=len(foes)*a.seeds
        print(f"\nGRUDGEBEARER AS A BLOODSWORN WARHAMMER, its own Crucible suppressed, "
              f"{len(foes)} foes x {a.seeds} seeds = {n} fights an arm\n")
        off=run(page, foes, on=False); out["floor"]=off
        HDR=(f"    {'arm':<30}{'win':>7}{'casts':>7}{'catch':>7}{'conn':>6}"
             f"{'held':>7}{'blows':>7}{'foe':>6}{'lift':>8}")
        def show(label, s):
            print(f"    {label:<30}{s['win']:>7.1%}{s['casts']:>7.2f}{s['catch']:>7.2f}"
                  f"{s['conn']:>6.2f}{s['held']:>7.1f}{s['hits']:>7.1f}{s['foe']:>6.1f}"
                  f"{(s['win']-off['win'])*100:>+7.1f}%", flush=True)
        ARMS=[("[1] THE DECOMPOSITION", None),
              ("§1 as written", {}),
              ("spin only, no ring", dict(ring=False, connect=False)),
              ("ring only, no spin boost", dict(spin=False)),
              ("ring + spin, no connect", dict(connect=False)),
              ("§1 but the ball is PINNED too", dict(pin=True)),
              ("[2] ROTATIONAL SPEED", None),
              ("spin x2.0", dict(spinMul=2.0)), ("spin x3.4 (Crucible)", dict(spinMul=3.4)),
              ("spin x9.0", dict(spinMul=9.0)), ("spin x12.0", dict(spinMul=12.0)),
              ("[3] THE RING", None),
              ("radius 76 (reach)", dict(radius=76.0)),
              ("radius 150", dict(radius=150.0)), ("radius 220", dict(radius=220.0)),
              ("[4] THE CONNECT", None),
              ("knock x1 (a normal blow)", dict(knockMul=1.0)),
              ("knock x2", dict(knockMul=2.0)), ("knock x5", dict(knockMul=5.0)),
              ("connect dmg x2", dict(connectMul=2.0)),
              ("[5] THE BLEED", None),
              ("no bleed on catch", dict(bleedCatch=0)),
              ("explosion bleed 1", dict(bleedBlow=1)),
              ("explosion bleed 4", dict(bleedBlow=4)),
              ("[8] THE SNAG — Rick's ruling: the ball is HELD, the weapon is NOT", None),
              ("SNAG, no consume", dict(stun=False, pin=True, radius=110.0)),
              ("SNAG + consume 8/stack", dict(stun=False, pin=True, radius=110.0, consume=True, consumePer=8.0)),
              ("SNAG + consume 14/stack", dict(stun=False, pin=True, radius=110.0, consume=True, consumePer=14.0)),
              ("SNAG + consume 20/stack", dict(stun=False, pin=True, radius=110.0, consume=True, consumePer=20.0)),
              ("SNAG, no pin either (ring only)", dict(stun=False, pin=False, radius=110.0)),
              ("SNAG + consume 14, spin x9", dict(stun=False, pin=True, radius=110.0, consume=True, consumePer=14.0, spinMul=9.0)),
              ("[7] THE BLEED IS INERT — TWO REPAIRS", None),
              ("explosion CONSUMES bleed, 8/stack", dict(consume=True, consumePer=8.0)),
              ("explosion CONSUMES bleed, 14/stack", dict(consume=True, consumePer=14.0)),
              ("ceiling 4->8 while ring stands", dict(ceiling=8)),
              ("ceiling 8 AND consume", dict(ceiling=8, consume=True, consumePer=8.0)),
              ("[6] DOES THE WINDOW END?", None),
              ("runs on after the connect", dict(endOnConnect=False)),
              ("window 4s", dict(dur=4.0)), ("window 12s", dict(dur=12.0))]
        want = set(a.arms.split(",")) if a.arms else None
        sect = None
        for label, kw in ARMS:
            if kw is None:
                sect = label[1]
                if want is None or sect in want:
                    print(f"\n  {label}"); print(HDR)
                continue
            if want is not None and sect not in want: continue
            s=run(page, foes, **kw); out[label]=s; show(label, s)
        print(f"\n    {'FLOOR — no ultimate':<30}{off['win']:>7.1%}"
              f"{'':>7}{'':>7}{'':>6}{'':>7}{off['hits']:>7.1f}{off['foe']:>6.1f}")
        print(f"\n  errors: {errors}")
    pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
main()
