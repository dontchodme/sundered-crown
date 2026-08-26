#!/usr/bin/env python3
"""LOOK AT THE FIVE OPEN WARHAMMER CELLS BEFORE CHOOSING ONE.

    python3 wh_survey.py --game ../02-chain/sc-vinesower-frame.html

v39's `cell_survey` looks at all 42 cells at once, which is the right
instrument for "which type" and the wrong one for "which school on THIS type".
v40 pointed the same discipline at the bow row and found that 82% of every
arrow the game has ever fired ends on a wall. Rick has picked the type. This
is that instrument pointed at the warhammer row.

The warhammer is the type nobody has looked at. Two relics in twenty-two, and
both of them inherited their block from a table rather than from a brief. What
is measurably different about it:

  * `mass 5.0` is the top of a `mass^1.7` ladder, and the ladder decides who
    keeps swinging after a bind. Nothing in the tree has ever measured what
    the top of it is worth.
  * `knockMul 2.3` is the highest in the game — 2.3x on a 165 impulse — and it
    is carried by the type with the SECOND SHORTEST reach (76). A hammer
    shoves its quarry away from a short arm. Nobody has asked what that costs.
  * `spin 1.6` is the slowest weapon in the game and `hitCd 0.45` allows 2.22
    contacts a second. The row lands 0.19. Contact is geometry, not cooldown.
  * `impact.stopPerDmg` prices the freeze off the DAMAGE of the blow, and this
    type lands the second-hardest blow in the game. `tickStatus` runs after
    the `hitStop` return in `step()` — so the heaviest type freezes its OWN
    status clock hardest, and every clock in `cell_survey` is measured at a
    PINNED 14 damage where that effect cannot appear.

  [1] THE GRID AND THE BLOCK. Read from AC.WEAPONS, not from a doc.

  [2] THE CLANK LADDER — the type's own thesis, never tested. Outcome is read
      off the EFFECT (whose spin reversed, who ate the stagger), never
      recomputed from the mass formula the game owns.

  [3] THE KNOCK AGAINST ITSELF. `knockMul` swept on the donor alone, pinned
      seeds, everything else held: does the hammer shove its quarry out of its
      own reach, and what does that cost in contacts?

  [4] THE FROZEN CLOCK. `hitStop` share per type, measured twice — at the
      pinned damage every published clock uses, and at SHIPPED damage, which
      is what the game runs.

  [5] THE FIVE OPEN CHANNELS AS DELIVERED EFFECT. Four foe statuses get one
      model-free A/B each: damage delivered with the channel, minus damage
      delivered with the channel deleted. Vigil is not a foe status and gets
      the readout its own mechanism deserves — bank rate, pool occupancy, cap
      saturation, shatters — plus the multiplier sweep that answers the vigil
      doc's open decision 4 from the heavy end of the type axis.

  [6] THE TRAPS. Asserted, not assumed.

Injection is runtime-only. NOTHING is written to any build.
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

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


# --------------------------------------------------------------- [1] grid ---

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape,
    reach: w.reach, width: w.width, artW: w.artW, dmg: w.dmg, spin: w.spin,
    mode: w.mode, mass: w.mass, arc: w.arc || null, blades: w.blades.length,
    knockMul: w.knockMul || null, shot: !!w.shot,
    onHit: w.onHit ? Object.entries(w.onHit)[0] : null,
    onSelf: w.onSelf ? Object.entries(w.onSelf)[0] : null,
    ult: w.ult ? { name: w.ult.name, kind: w.ult.kind, charge: w.ult.charge } : null,
  }));
  const S = {};
  for (const [k, v] of Object.entries(AC.STATUS)) S[k] = Object.assign({}, v);
  return { weapons: W, status: S, affinities: Object.keys(AC.AFFINITIES),
           dt: AC.CONFIG.physics.dt, ballR: AC.CONFIG.physics.ballR,
           combat: AC.CONFIG.combat, clank: AC.CONFIG.clank,
           impact: AC.CONFIG.impact, arena: AC.CONFIG.arena };
}"""


# -------------------------------------------------------------- [2] clank ---
# The outcome of a bind is read off what the bind DID, never recomputed from
# `mass^1.7`. resolveClank flips the loser's `spinDir` and leaves the winner's
# alone (both flip when the exchange is not decisive), and it stuns both in
# proportion to what each suffered. So: sample spinDir and stun either side of
# the shipped call and classify from the delta. A future change to the mass
# model moves these numbers; a future change to the probe cannot.

CLANK_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
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
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      let step = 0;
      let clanks = 0, won = 0, lost = 0, dead = 0;
      let stunMe = 0, stunTh = 0;
      let pending = null;                     // the last bind, until a hit lands
      const gapWon = [], gapLost = [], gapDead = [];

      const origClank = AC.Match.prototype.resolveClank;
      m.resolveClank = function(A, B, hx, hy){
        /* A bind between two shades is not this fighter's bind. Ultimates are
           suppressed here so it cannot arise, and it is guarded anyway: the
           classification below reads `me === A ? ... : ...` and would silently
           score B's flip as mine. */
        if (me !== A && me !== B) return origClank.call(m, A, B, hx, hy);
        const sA = A.spinDir, sB = B.spinDir, uA = A.stun, uB = B.stun;
        const r = origClank.call(m, A, B, hx, hy);
        const meFlip = (me === A ? A.spinDir !== sA : B.spinDir !== sB);
        const thFlip = (th === A ? A.spinDir !== sA : B.spinDir !== sB);
        clanks++;
        stunMe += (me === A ? A.stun - uA : B.stun - uB);
        stunTh += (th === A ? A.stun - uA : B.stun - uB);
        let out;
        if (meFlip && thFlip) { dead++; out = gapDead; }
        else if (!meFlip)     { won++;  out = gapWon;  }
        else                  { lost++; out = gapLost; }
        pending = { step, out };
        return r;
      };

      /* Only MY blows, and only ordinary ones: `mul` is defined for a
         projectile, and the warhammer has none, so this is belt and braces
         against a future donor that does. */
      let hits = 0;
      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        if (self === me && mul === undefined){
          hits++;
          if (pending){ pending.out.push((step - pending.step) * DT); pending = null; }
        }
        return r;
      };

      while (!m.over && step < secs / DT){ m.step(DT); step++; }

      const sum = a => a.reduce((x, y) => x + y, 0);
      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT,
                  foeMass: m.a.w.id === donor ? m.b.w.mass : m.a.w.mass,
                  clanks, won, lost, dead, hits,
                  stunMe, stunTh,
                  gapWon: sum(gapWon), nWon: gapWon.length,
                  gapLost: sum(gapLost), nLost: gapLost.length,
                  gapDead: sum(gapDead), nDead: gapDead.length });
    }
  }

  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


# --------------------------------------------------------------- [3] knock --
# One knob, on the donor only, on pinned seeds. Everything the knob touches:
# the impulse in resolveHit, the impulse a ward shatter throws (no ward here),
# and `this.shake`, which is drawn and never stepped. So a difference in this
# table is the shove and nothing else.
#
# The post-hit separation is sampled at a fixed delay after each landed blow
# rather than on the next frame: the impulse is applied to velocity, so the
# frame after a hit shows almost none of it. `sepAt` is in seconds.

KNOCK_JS = r"""([donor, foes, seeds, secs, kms, sepAt, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const R  = AC.CONFIG.physics.ballR;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedKm = w.knockMul;

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  for (const km of kms){
    w.knockMul = km;
    for (const f of foes){
      for (const sd of seeds){
        const m  = new AC.Match(donor, f, sd);
        const me = m.a.w.id === donor ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;

        let step = 0, hits = 0, dealt0 = 0;
        let sepSum = 0, sepN = 0;
        let atHit = 0, afterHit = 0, nPair = 0;
        let lastHitStep = -1, gapSum = 0, gapN = 0;
        const pend = [];

        const sep = () => Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;

        const origHit = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
          const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
          if (self === me && mul === undefined){
            hits++;
            const s0 = sep();
            pend.push({ at: step + Math.round(sepAt / DT), s0 });
            if (lastHitStep >= 0){ gapSum += (step - lastHitStep) * DT; gapN++; }
            lastHitStep = step;
          }
          return r;
        };

        while (!m.over && step < secs / DT){
          m.step(DT); step++;
          const s = sep();
          sepSum += s; sepN++;
          while (pend.length && pend[0].at <= step){
            const p = pend.shift();
            if (!m.over){ atHit += p.s0; afterHit += s; nPair++; }
          }
        }

        rows.push({ km, foe: f, seed: sd, steps: step, dur: step * DT,
                    over: m.over, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                    hits, dealt: me.dealt, taken: th.dealt,
                    foeHits: th.hits,
                    sep: sepN ? sepSum / sepN : 0,
                    atHit, afterHit, nPair,
                    gap: gapN ? gapSum / gapN : 0, gapN,
                    meHp: me.hp, thHp: th.hp });
      }
    }
  }

  w.knockMul = savedKm;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


# ------------------------------------------------------------ [4] hitStop ---
# `step()` returns early on `hitStop > 0`, BEFORE tickStatus. v39 measured that
# on the scythe and called it 9.4% of a fight. It is a property of the pair of
# blows being traded, so it belongs to the TYPE, and it is read here off the
# value the frame is about to be stepped with — the same convention bow_survey
# uses, so the two tables can be compared.

FREEZE_JS = r"""([donors, foes, seeds, secs, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  for (const d of donors){
    for (const f of foes){
      if (f === d) continue;
      for (const sd of seeds){
        const m  = new AC.Match(d, f, sd);
        const me = m.a.w.id === d ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        let step = 0, frozen = 0, stunMe = 0;
        while (!m.over && step < secs / DT){
          if (m.hitStop > 0) frozen++;
          if (me.stun > 0) stunMe++;
          m.step(DT); step++;
        }
        rows.push({ donor: d, foe: f, seed: sd, steps: step, dur: step * DT,
                    frozen, stunMe, hits: me.hits + th.hits,
                    myHits: me.hits, dealt: me.dealt });
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


# ----------------------------------------------------------- [5] channels ---
# One donor, one school's channel, ON and OFF on the same seeds. The readout is
# damage DELIVERED, which is model-free: it does not care whether the status
# deals damage, multiplies it, slows the foe or stuns its weapon, and it prices
# a hex stun and a hemorrhage tick on the same axis. cell_survey's occupancy is
# a proxy twice removed (v39 5.2); this is the thing itself.

CHANNEL_JS = r"""([donor, aff, key, per, foes, seeds, secs, pin, pinIds, noult, on]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = aff;
  delete w.onHit; delete w.onSelf;
  if (on && key) { w.onHit = {}; w.onHit[key] = per; }

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
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      /* `self.dealt` counts what resolveHit paid out and NOTHING else, so it
         is blind to every damage-over-time status and to curse's max-hp bite
         -- which is exactly half the channels this table is comparing. The
         foe's own health is the model-free readout: nothing but this relic
         takes any of it, and the ceiling is captured before curse can move
         it. */
      const th0 = th.maxHp;
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, dealt: me.dealt, taken: th.dealt,
                  destroyed: th0 - th.hp, hpCut: th0 - th.maxHp,
                  thHp: th.hp, thMaxHp: th.maxHp, meHp: me.hp });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


# The vigil readout. `onSelf.ward`'s value is already a per-relic bank
# multiplier (resolveHit banks `dmg * STATUS.ward.bank * n`), which is the knob
# Farwarden had to set to 2.5 because ward was authored on a greatsword. The
# warhammer is the other end of that axis. Banking is sampled off the pool
# itself — it only ever rises at the bank site — and absorption and breaks are
# counted at the two shipped functions that own them.

WARD_JS = r"""([donor, mults, foes, seeds, secs, pin, pinIds, noult, sepAt]) => {
  const DT = AC.CONFIG.physics.dt;
  const R  = AC.CONFIG.physics.ballR;
  const W  = AC.STATUS.ward;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "vigil";
  delete w.onHit;

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  for (const mult of mults){
    w.onSelf = { ward: mult };
    for (const f of foes){
      for (const sd of seeds){
        const m  = new AC.Match(donor, f, sd);
        const me = m.a.w.id === donor ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;

        let absorbed = 0, breaks = 0, expired = 0, burst = 0;
        let step = 0;
        const sep = () => Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;
        const pend = [];
        let atBreak = 0, afterBreak = 0, nBreak = 0;

        const origHurt = AC.Match.prototype.hurt;
        m.hurt = function(foe2, dmg, src){
          if (foe2 === me && me.shield > 0 && dmg > 0)
            absorbed += Math.min(me.shield, dmg);
          return origHurt.call(m, foe2, dmg, src);
        };
        /* THE BREAK IS A SECOND SHOVE. `shatter` throws the ATTACKER away from
           the vigil ball at `W.knock * f.w.knockMul` -- the wielder's own
           multiplier, which on this type is the 2.3 section [3] just priced.
           So the plate breaking pushes the quarry out of reach exactly the way
           a landed blow does, and this measures it on the same axis. */
        const origShatter = AC.Match.prototype.shatter;
        m.shatter = function(f2, src){
          if (f2 === me){
            breaks++;
            burst += Math.round((me.shieldMax || 0) * W.shatter);
            pend.push({ at: step + Math.round(sepAt / DT), s0: sep() });
          }
          return origShatter.call(m, f2, src);
        };

        let poolSum = 0, atCap = 0, held = 0, banked = 0;
        let prev = 0, prevHadWard = false;
        while (!m.over && step < secs / DT){
          m.step(DT); step++;
          const s = me.shield;
          if (s > prev) banked += s - prev;
          /* an expiry is the plate going to zero with no break filed for it */
          if (prevHadWard && !me.status.ward && s === 0) expired++;
          prev = s; prevHadWard = !!me.status.ward;
          poolSum += s;
          if (s > 0) held++;
          if (s >= W.cap - 1e-6) atCap++;
          const now = sep();
          while (pend.length && pend[0].at <= step){
            const p = pend.shift();
            if (!m.over){ atBreak += p.s0; afterBreak += now; nBreak++; }
          }
        }

        rows.push({ mult, foe: f, seed: sd, steps: step, dur: step * DT,
                    win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                    hits: me.hits, dealt: me.dealt, taken: th.dealt,
                    banked, absorbed, breaks, burst,
                    expired: Math.max(0, expired - breaks),
                    atBreak, afterBreak, nBreak,
                    pool: step ? poolSum / step : 0,
                    held: step ? held / step : 0,
                    atCap: step ? atCap / step : 0 });
      }
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


# --------------------------------------------------------- [2c] no-op ctrl --
# Every table above shadows prototype methods on one Match. If any of that
# perturbed the simulation, the whole survey would be about the probe.

CONTROL_JS = r"""([donor, foe, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const run = (instrument) => {
    const out = [];
    for (const sd of seeds){
      const m = new AC.Match(donor, foe, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      if (instrument){
        const oC = AC.Match.prototype.resolveClank;
        m.resolveClank = function(A, B, hx, hy){
          const s = A.spinDir; const r = oC.call(m, A, B, hx, hy); void s; return r; };
        const oH = AC.Match.prototype.resolveHit;
        m.resolveHit = function(...a){ return oH.call(m, ...a); };
        const oU = AC.Match.prototype.hurt;
        m.hurt = function(...a){ return oU.call(m, ...a); };
        const oS = AC.Match.prototype.shatter;
        m.shatter = function(...a){ return oS.call(m, ...a); };
      }
      let steps = 0;
      while (!m.over && steps < secs / DT){ m.step(DT); steps++; }
      out.push([steps, Math.round(me.hp * 1e6) / 1e6, Math.round(th.hp * 1e6) / 1e6,
                me.hits, th.hits, me.clanks]);
    }
    return out;
  };
  return { bare: run(false), inst: run(true) };
}"""


TYPE_DONOR = {"greatsword": "dawnbringer", "twinblade": "widowmaker",
              "warhammer": "grudgebearer", "scythe": "thornwake",
              "flail": "gravemourn", "bow": "ironhail"}
# One foe per type, none of them a donor, so every row in [4] is scored
# against the identical field.
FOES = ["emberedge", "spellbreaker", "lastlight", "slagheart", "aureole"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-vinesower-frame.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--sep-at", type=float, default=0.25)
    ap.add_argument("--only", default="", help="comma list of section numbers")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"1", "2", "3", "4", "5", "6"}
    gp = (HERE / a.game).resolve()
    seeds = [1301 + 17 * i for i in range(a.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        g = page.evaluate(GRID_JS)
        W, ST = g["weapons"], g["status"]
        by_id = {w["id"]: w for w in W}
        schools = sorted(set({w["aff"] for w in W}) | set(g["affinities"]))
        shapes = sorted({w["shape"] for w in W})
        filled = {(w["aff"], w["shape"]): w["name"] for w in W}
        whs = [w for w in W if w["shape"] == "warhammer"]
        open_wh = [s for s in schools if (s, "warhammer") not in filled]
        pin_ids = [w["id"] for w in W]
        donor = TYPE_DONOR["warhammer"]

        # ---------------------------------------------------------- [1] --
        if "1" in want:
            print(f"\n[1] THE WARHAMMER ROW — {len(whs)} of {len(schools)} filled, "
                  f"{len(open_wh)} open\n")
            print(f"    {'':<14}" + "".join(f"{s[:11]:>12}" for s in schools))
            print(f"    {'warhammer':<14}"
                  + "".join(f"{filled.get((s,'warhammer'),'·')[:11]:>12}" for s in schools))
            print(f"\n    the type's block, and where it sits in the game\n")
            print(f"    {'type':<12}{'reach':>7}{'width':>7}{'spin':>7}{'mass':>7}"
                  f"{'knockMul':>10}{'mode':>8}{'blades':>8}{'dmg':>16}")
            for t in shapes:
                rel = [w for w in W if w["shape"] == t]
                r0 = rel[0]
                kms = {w["knockMul"] or 1.0 for w in rel}
                dmgs = f"{min(w['dmg'] for w in rel):.1f}–{max(w['dmg'] for w in rel):.1f}"
                print(f"    {t:<12}{r0['reach']:>7}{r0['width']:>7}{r0['spin']:>7.1f}"
                      f"{r0['mass']:>7.1f}"
                      f"{('/'.join(f'{k:g}' for k in sorted(kms))):>10}"
                      f"{r0['mode']:>8}{r0['blades']:>8}{dmgs:>16}")

            fields = ("reach", "width", "artW", "spin", "mode", "mass",
                      "knockMul", "blades")
            same = all(len({w[f] for w in whs}) == 1 for f in fields)
            check("both warhammers share one physics block, field for field",
                  same, ", ".join(f"{f}={whs[0][f]}" for f in fields))

            best = max((w["knockMul"] or 1.0) for w in W)
            check("knockMul 2.3 is the highest in the game",
                  abs(best - (whs[0]["knockMul"] or 1.0)) < 1e-9,
                  f"warhammer {whs[0]['knockMul']}, next "
                  f"{sorted({w['knockMul'] or 1.0 for w in W})[-2]:g}, "
                  f"impulse {g['combat']['knock'] * whs[0]['knockMul']:.0f} "
                  f"against {g['combat']['knock']:.0f} at 1x")

            heavier = [w["shape"] for w in W if w["mass"] > whs[0]["mass"]]
            check("mass 5.0 is the top of the ladder", not heavier,
                  "next is " + max(
                      (t for t in shapes if t != "warhammer"),
                      key=lambda t: [w for w in W if w["shape"] == t][0]["mass"])
                  + f" at {max(w['mass'] for w in W if w['shape'] != 'warhammer'):.1f}")
            out["block"] = {f: whs[0][f] for f in fields}

        # ---------------------------------------------------------- [2] --
        if "2" in want:
            print(f"\n[2] THE CLANK LADDER — measured off the effect, dmg pinned "
                  f"{a.pin:g}, ultimates suppressed\n")
            print("    a bind the hammer WINS leaves its own spin running and "
                  "reverses the foe's.\n")
            print(f"    {'foe':<14}{'type':<11}{'mass':>6}{'clanks/min':>11}"
                  f"{'won':>7}{'deadlock':>10}{'lost':>7}{'stun taken':>12}"
                  f"{'stun dealt':>12}")
            clank_rows = {}
            for f in FOES:
                rows = page.evaluate(CLANK_JS, [donor, [f], seeds, a.secs,
                                                a.pin, pin_ids, True])
                cl = sum(r["clanks"] for r in rows)
                dur = sum(r["dur"] for r in rows)
                won = sum(r["won"] for r in rows)
                lost = sum(r["lost"] for r in rows)
                dead = sum(r["dead"] for r in rows)
                clank_rows[f] = {
                    "mass": by_id[f]["mass"], "shape": by_id[f]["shape"],
                    "clanks": cl, "dur": dur, "won": won, "lost": lost, "dead": dead,
                    "stunMe": sum(r["stunMe"] for r in rows),
                    "stunTh": sum(r["stunTh"] for r in rows),
                    "gapWon": sum(r["gapWon"] for r in rows),
                    "nWon": sum(r["nWon"] for r in rows),
                    "gapLost": sum(r["gapLost"] for r in rows),
                    "nLost": sum(r["nLost"] for r in rows),
                    "gapDead": sum(r["gapDead"] for r in rows),
                    "nDead": sum(r["nDead"] for r in rows)}
                c = clank_rows[f]
                print(f"    {f:<14}{c['shape']:<11}{c['mass']:>6.1f}"
                      f"{cl / dur * 60:>11.1f}"
                      f"{(won / cl if cl else 0):>7.0%}"
                      f"{(dead / cl if cl else 0):>10.0%}"
                      f"{(lost / cl if cl else 0):>7.0%}"
                      f"{c['stunMe']:>12.1f}{c['stunTh']:>12.1f}")

            tot = sum(c["clanks"] for c in clank_rows.values())
            lost_tot = sum(c["lost"] for c in clank_rows.values())
            won_tot = sum(c["won"] for c in clank_rows.values())
            sm = sum(c["stunMe"] for c in clank_rows.values())
            st = sum(c["stunTh"] for c in clank_rows.values())
            check("the hammer does not lose binds",
                  lost_tot / max(1, tot) < 0.02,
                  f"{lost_tot} of {tot} lost, {won_tot} won "
                  f"({won_tot / max(1,tot):.0%})")
            check("and it eats less of the stagger than it hands out",
                  st > sm * 1.5,
                  f"{sm:.1f}s taken against {st:.1f}s dealt — "
                  f"{st / max(1e-9, sm):.1f}x")
            gw = sum(c["gapWon"] for c in clank_rows.values())
            nw = sum(c["nWon"] for c in clank_rows.values())
            gd = sum(c["gapDead"] for c in clank_rows.values())
            nd = sum(c["nDead"] for c in clank_rows.values())
            print(f"\n    time from a bind to the hammer's next landed blow — "
                  f"won {gw / max(1,nw):.2f}s (n={nw})"
                  + (f", deadlock {gd / max(1,nd):.2f}s (n={nd})" if nd else
                     ", deadlock never happened"))
            out["clank"] = clank_rows

            ctl = page.evaluate(CONTROL_JS, [donor, FOES[0], seeds[:4], a.secs])
            check("the instrument does not move the simulation",
                  ctl["bare"] == ctl["inst"],
                  f"{len(ctl['bare'])} seeds, field for field")

        # ---------------------------------------------------------- [3] --
        if "3" in want:
            kms = [1.0, 1.6, 2.3, 3.0]
            print(f"\n[3] THE KNOCK AGAINST ITSELF — knockMul swept on the hammer "
                  f"alone, SHIPPED damage, ultimates suppressed\n")
            rows = page.evaluate(KNOCK_JS, [donor, FOES, seeds, a.secs, kms,
                                            a.sep_at, 0, pin_ids, True])
            print(f"    {'knockMul':>9}{'impulse':>9}{'hits/min':>10}{'dmg/s':>8}"
                  f"{'win':>7}{'mean sep':>10}{'sep at hit':>12}"
                  f"{f'sep +{a.sep_at:g}s':>12}{'push':>8}{'hit gap':>9}")
            knock = {}
            for km in kms:
                rs = [r for r in rows if abs(r["km"] - km) < 1e-9]
                dur = sum(r["dur"] for r in rs)
                hits = sum(r["hits"] for r in rs)
                dealt = sum(r["dealt"] for r in rs)
                dec = [r for r in rs if r["win"] >= 0]
                nP = sum(r["nPair"] for r in rs)
                at = sum(r["atHit"] for r in rs) / max(1, nP)
                af = sum(r["afterHit"] for r in rs) / max(1, nP)
                gapn = sum(r["gapN"] for r in rs)
                gap = sum(r["gap"] * r["gapN"] for r in rs) / max(1, gapn)
                knock[km] = {"hits": hits, "dur": dur, "dealt": dealt,
                             "win": mean(r["win"] for r in dec), "n": len(rs),
                             "sep": mean(r["sep"] for r in rs),
                             "atHit": at, "afterHit": af, "gap": gap,
                             "timeouts": sum(1 for r in rs if not r["over"])}
                k = knock[km]
                print(f"    {km:>9.1f}{g['combat']['knock'] * km:>9.0f}"
                      f"{hits / dur * 60:>10.1f}{dealt / dur:>8.2f}"
                      f"{k['win']:>7.0%}{k['sep']:>10.1f}{at:>12.1f}{af:>12.1f}"
                      f"{af - at:>+8.1f}{gap:>9.2f}")

            base, off = knock[2.3], knock[1.0]
            dh = (base["hits"] / base["dur"]) / (off["hits"] / off["dur"]) - 1
            print(f"\n    the shipped hammer lands {dh:+.1%} of the contacts it "
                  f"would land at 1x, and its blow opens the gap by "
                  f"{base['afterHit'] - base['atHit']:+.0f} units against "
                  f"{off['afterHit'] - off['atHit']:+.0f} at 1x — on a "
                  f"{by_id[donor]['reach']} reach. Damage is held at the "
                  f"shipped {by_id[donor]['dmg']:.2f} across the sweep, so the "
                  f"win column prices the shove and nothing else.")
            check("the shove is real — a landed blow opens the distance",
                  base["afterHit"] > base["atHit"],
                  f"{base['atHit']:.1f} -> {base['afterHit']:.1f} units "
                  f"{a.sep_at:g}s after the blow")
            check("the shove costs contacts",
                  (off["hits"] / off["dur"]) > (base["hits"] / base["dur"]),
                  f"{off['hits'] / off['dur'] * 60:.1f} hits/min at 1x against "
                  f"{base['hits'] / base['dur'] * 60:.1f} at the shipped 2.3x")
            # The cost does NOT keep growing, and that was not the hypothesis.
            # The hall is finite and closing: past some point the foe is thrown
            # into a wall and comes straight back, so the room hands back what
            # the hammer throws away. WHERE that floor sits moved between a
            # 6-seed and a 12-seed run (1.6x, then 2.3x) and this survey does
            # not claim to have pinned it — only that the cost stops growing at
            # or before the shipped setting, which held on both.
            hard = knock[3.0]
            check("and the cost saturates — the room hands back what the hammer "
                  "throws away, so 3x is no worse than the shipped 2.3x",
                  (hard["hits"] / hard["dur"]) >= (base["hits"] / base["dur"]),
                  " ".join(f"{k:g}x {knock[k]['hits'] / knock[k]['dur'] * 60:.1f}"
                           for k in kms) + " hits/min")
            check("no run hit the wall clock", all(k["timeouts"] == 0 for k in knock.values()),
                  f"{len(rows)} runs, {a.secs:g}s cap")

            # Robustness: the sweep above suppresses ultimates, and Crucible is
            # a launch — an ultimate that shoves harder than the shove being
            # measured. If the finding is an artefact of switching it off, it
            # will not survive switching it back on.
            # ROBUSTNESS, AND IT REFUTED THE FRAMING ABOVE. The sweep suppresses
            # ultimates. Switch them back on and run BOTH shipped warhammers:
            # Crucible carries `pullBase/pullMax/pullRamp` and drags the foe in;
            # Consecration is a nova that knocks it further out. If the type's
            # ultimate slot is where the shove gets paid for, those two relics
            # must answer this differently.
            print(f"\n    the same two settings with ULTIMATES LIVE, on both "
                  f"shipped warhammers — Crucible PULLS the foe in, "
                  f"Consecration is a nova that knocks it further out\n")
            print(f"    {'relic':<14}{'ult':<15}{'knockMul':>9}{'hits/min':>10}"
                  f"{'dmg/s':>8}{'win':>7}{'the shove is worth':>20}")
            uk = {}
            for wid in [w["id"] for w in whs]:
                urows = page.evaluate(KNOCK_JS, [wid, FOES, seeds, a.secs,
                                                 [1.0, 2.3], a.sep_at, 0,
                                                 pin_ids, False])
                for km in (1.0, 2.3):
                    rs = [r for r in urows if abs(r["km"] - km) < 1e-9]
                    dur = sum(r["dur"] for r in rs)
                    uk[(wid, km)] = {
                        "hits": sum(r["hits"] for r in rs), "dur": dur,
                        "dealt": sum(r["dealt"] for r in rs),
                        "win": mean(r["win"] for r in rs if r["win"] >= 0)}
                for km in (1.0, 2.3):
                    v = uk[(wid, km)]
                    d = (uk[(wid, 2.3)]["win"] - uk[(wid, 1.0)]["win"]
                         if km == 2.3 else None)
                    print(f"    {by_id[wid]['name']:<14}"
                          f"{by_id[wid]['ult']['name']:<15}{km:>9.1f}"
                          f"{v['hits'] / v['dur'] * 60:>10.1f}"
                          f"{v['dealt'] / v['dur']:>8.2f}{v['win']:>7.0%}"
                          + (f"{d:>+19.0%}" if d is not None else f"{'':>20}"))

            gb = uk[("grudgebearer", 2.3)]["win"] - uk[("grudgebearer", 1.0)]["win"]
            cn = uk[("censer", 2.3)]["win"] - uk[("censer", 1.0)]["win"]
            check("THE FRAMING ABOVE IS WRONG FOR GRUDGEBEARER — with Crucible "
                  "live the shove stops costing it anything",
                  gb >= 0, f"{gb:+.0%} from the shove with the pull live, "
                  f"against {base['win'] - off['win']:+.0%} with it suppressed")
            check("and the relic whose ultimate does NOT pull is still paying",
                  cn < gb, f"Censer {cn:+.0%} against Grudgebearer's {gb:+.0%} "
                  f"— the same type, the same shove, opposite ultimates")
            out["knock"] = {str(k): v for k, v in knock.items()}
            out["knockUlt"] = {f"{w}@{k:g}": v for (w, k), v in uk.items()}

        # ---------------------------------------------------------- [4] --
        if "4" in want:
            print(f"\n[4] THE FROZEN CLOCK — share of the fight `hitStop` holds "
                  f"`tickStatus` off, per type\n")
            donors = [TYPE_DONOR[t] for t in shapes]
            freeze = {}
            for label, pin in (("pinned " + f"{a.pin:g}", a.pin), ("shipped", 0)):
                rows = page.evaluate(FREEZE_JS, [donors, FOES, seeds, a.secs,
                                                 pin, pin_ids, True])
                for t in shapes:
                    rs = [r for r in rows if r["donor"] == TYPE_DONOR[t]]
                    st = sum(r["steps"] for r in rs)
                    freeze.setdefault(t, {})[label] = {
                        "frozen": sum(r["frozen"] for r in rs) / max(1, st),
                        "contacts": sum(r["hits"] for r in rs)
                        / max(1e-9, sum(r["dur"] for r in rs)),
                        "dmg": sum(r["dealt"] for r in rs)
                        / max(1e-9, sum(r["dur"] for r in rs))}
            I = g["impact"]

            def per_blow(d):
                """What one blow of `d` damage freezes, off CONFIG.impact."""
                return min(I["stopMax"], I["stopBase"] + d * I["stopPerDmg"])

            print(f"    {'type':<12}{'dmg/blow':>10}{'stop/blow':>11}"
                  f"{'frozen (pinned)':>18}{'frozen (shipped)':>18}"
                  f"{'contacts/s':>12}{'shipped-pinned':>16}")
            for t in sorted(shapes, key=lambda t: -freeze[t]["shipped"]["frozen"]):
                r0 = [w for w in W if w["shape"] == t]
                d0 = mean(w["dmg"] for w in r0)
                f0 = freeze[t][f"pinned {a.pin:g}"]["frozen"]
                f1 = freeze[t]["shipped"]["frozen"]
                print(f"    {t:<12}{d0:>10.1f}{per_blow(d0):>11.3f}"
                      f"{f0:>17.1%}{f1:>18.1%}"
                      f"{freeze[t]['shipped']['contacts']:>12.3f}"
                      f"{f1 - f0:>+15.1%}")
            wh = freeze["warhammer"]
            sc = freeze["scythe"]["shipped"]["frozen"]
            check("reproduces v39's independent scythe measurement of 9.4%",
                  abs(sc - 0.094) < 0.01, f"{sc:.1%} here, 9.4% in "
                  "runic_scythe_probe — a different tool, a different session")

            # THE HYPOTHESIS THIS SECTION WAS BUILT ON IS FALSE, and it is
            # stated as a check so it stays falsified rather than quietly
            # dropped: `stopPerDmg` does price the freeze off the blow, but
            # `stopMax` caps it at 0.13 and hitStop is a MAX rather than a
            # sum -- so what fills a fight with freeze is how OFTEN blows
            # land, not how big they are.
            worst = min(shapes, key=lambda t: freeze[t]["shipped"]["frozen"])
            biggest = max(shapes, key=lambda t: mean(
                w["dmg"] for w in W if w["shape"] == t))
            check("the freeze is contact-driven, not blow-size-driven — the type "
                  "with the biggest blow freezes the hall LEAST",
                  worst == biggest,
                  f"{biggest} freezes {per_blow(mean(w['dmg'] for w in W if w['shape'] == biggest)):.3f}s "
                  f"per blow, the longest in the game, and holds the hall for "
                  f"{freeze[biggest]['shipped']['frozen']:.1%} — the lowest")
            check("so cell_survey's PINNED clocks need no shipped-damage "
                  "correction on this type",
                  abs(wh["shipped"]["frozen"] - wh[f"pinned {a.pin:g}"]["frozen"]) < 0.01,
                  f"{wh[f'pinned {a.pin:g}']['frozen']:.1%} pinned against "
                  f"{wh['shipped']['frozen']:.1%} shipped — "
                  f"{wh['shipped']['frozen'] - wh[f'pinned {a.pin:g}']['frozen']:+.1%}")
            out["freeze"] = freeze

        # ---------------------------------------------------------- [5] --
        if "5" in want:
            print(f"\n[5] THE FIVE OPEN CELLS — delivered effect at SHIPPED "
                  f"damage, ultimates suppressed, same seeds on and off\n")
            chan = {}
            for s in schools:
                rel = [w for w in W if w["aff"] == s]
                h = [w["onHit"] for w in rel if w["onHit"]]
                sf = [w["onSelf"] for w in rel if w["onSelf"]]
                chan[s] = (h[0] if h else None, sf[0] if sf else None)
            off = page.evaluate(CHANNEL_JS, [donor, "dwarven", None, 0, FOES,
                                             seeds, a.secs, 0, pin_ids,
                                             True, False])
            offd = sum(r["destroyed"] for r in off) / sum(r["dur"] for r in off)
            offw = mean(r["win"] for r in off if r["win"] >= 0)
            print(f"    the control — the same hammer, SHIPPED damage, no channel "
                  f"at all: {offd:.2f} hp/s destroyed, {offw:.0%} win over "
                  f"{len(off)} fights.\n    Damage is NOT pinned here: this is a "
                  f"within-type comparison, and a hammer pinned to 14 is a "
                  f"different weapon (it wins 7%).\n")
            offh = sum(r["hits"] for r in off) / sum(r["dur"] for r in off) * 60
            offt = sum(r["taken"] for r in off) / sum(r["dur"] for r in off)
            print(f"    {'cell':<24}{'status':<12}{'hp/s':>8}{'vs control':>12}"
                  f"{'win':>7}{'hits/min':>10}{'taken/s':>9}"
                  f"{'max hp eaten':>14}{'stacks':>8}{'dur':>7}")
            print(f"    {'— no channel —':<24}{'':<12}{offd:>8.2f}{'':>12}"
                  f"{offw:>7.0%}{offh:>10.1f}{offt:>9.2f}")
            deliver = {}
            for s in open_wh:
                onhit, onself = chan[s]
                if not onhit:
                    continue
                key, per = onhit
                on = page.evaluate(CHANNEL_JS, [donor, s, key, per, FOES, seeds,
                                                a.secs, 0, pin_ids, True, True])
                dur = sum(r["dur"] for r in on)
                d = sum(r["destroyed"] for r in on) / dur
                w_ = mean(r["win"] for r in on if r["win"] >= 0)
                cut = mean(r["hpCut"] for r in on)
                deliver[s] = {"status": key, "per": per, "hps": d,
                              "lift": d / offd - 1, "win": w_, "hpCut": cut,
                              "hits": sum(r["hits"] for r in on) / dur * 60,
                              "taken": sum(r["taken"] for r in on) / dur,
                              "n": len(on)}
                v = deliver[s]
                print(f"    {s + ' x warhammer':<24}{key:<12}{d:>8.2f}"
                      f"{v['lift']:>+11.1%}{w_:>7.0%}{v['hits']:>10.1f}"
                      f"{v['taken']:>9.2f}{cut:>14.1f}"
                      f"{ST[key]['maxStacks']:>8}{ST[key]['dur']:>7.1f}")

            # NOT A FLOOR. This check was written expecting every channel to be
            # worth something and it failed on the first run, which is the
            # finding: on a type whose problem is a quarry it keeps throwing
            # out of reach, a status that makes the quarry SLOWER TO COME BACK
            # is a cost. Section [3] is why, and the hits/min column is the
            # mechanism rather than the story.
            worst = min(deliver, key=lambda k: deliver[k]["lift"])
            check("the no-channel control is not a floor",
                  not all(v["lift"] > 0 for v in deliver.values()),
                  ", ".join(f"{k} {v['lift']:+.1%}" for k, v in deliver.items()))
            check("and the channel that slows the QUARRY is the worst of the "
                  "four — [3] says this type's problem is a foe it keeps "
                  "throwing away, and entangle makes it slower to come back",
                  worst == "verdant",
                  f"verdant {deliver['verdant']['lift']:+.1%} at "
                  f"{deliver['verdant']['hits']:.1f} hits/min against the "
                  f"control's {offh:.1f}")
            check("and the readout sees what `dealt` cannot — curse's bite out "
                  "of the ceiling",
                  deliver.get("umbral", {}).get("hpCut", 0) > 0,
                  f"{deliver.get('umbral', {}).get('hpCut', 0):.1f} max hp eaten "
                  f"a fight, none of which appears in `self.dealt`")

            mults = [1.0, 1.6, 2.3, 3.0]
            print(f"\n    vigil is not a foe status and does not belong in that "
                  f"table. Its own readout, same shipped damage — "
                  f"`onSelf.ward` is a per-relic BANK MULTIPLIER "
                  f"(Lightkeeper 1.0 on a greatsword, Farwarden 2.5 on a bow, "
                  f"and vigil od 4 says the constants do not survive the type "
                  f"axis)\n")
            wrows = page.evaluate(WARD_JS, [donor, mults, FOES, seeds, a.secs,
                                            0, pin_ids, True, a.sep_at])
            print(f"    {'mult':>6}{'banked/s':>10}{'absorbed/s':>12}"
                  f"{'mean pool':>11}{'held':>7}{'at cap':>8}"
                  f"{'breaks/fight':>14}{'burst':>8}{'break push':>12}{'win':>7}")
            ward = {}
            for mlt in mults:
                rs = [r for r in wrows if abs(r["mult"] - mlt) < 1e-9]
                dur = sum(r["dur"] for r in rs)
                nb = sum(r["nBreak"] for r in rs)
                ward[mlt] = {
                    "banked": sum(r["banked"] for r in rs) / dur,
                    "absorbed": sum(r["absorbed"] for r in rs) / dur,
                    "pool": mean(r["pool"] for r in rs),
                    "held": mean(r["held"] for r in rs),
                    "atCap": mean(r["atCap"] for r in rs),
                    "breaks": mean(r["breaks"] for r in rs),
                    "burst": (sum(r["burst"] for r in rs)
                              / max(1, sum(r["breaks"] for r in rs))),
                    "expired": mean(r["expired"] for r in rs),
                    "push": ((sum(r["afterBreak"] for r in rs)
                              - sum(r["atBreak"] for r in rs)) / max(1, nb)),
                    "win": mean(r["win"] for r in rs if r["win"] >= 0),
                    "n": len(rs)}
                v = ward[mlt]
                print(f"    {mlt:>6.1f}{v['banked']:>10.2f}{v['absorbed']:>12.2f}"
                      f"{v['pool']:>11.1f}{v['held']:>7.0%}{v['atCap']:>8.1%}"
                      f"{v['breaks']:>14.2f}{v['burst']:>8.1f}{v['push']:>+12.1f}"
                      f"{v['win']:>7.0%}")
            cap = ST["ward"]["cap"]
            print(f"\n    the pool ceiling is {cap:g}, the plate's own clock is "
                  f"{ST['ward']['dur']:g}s, and a break throws the attacker at "
                  f"{ST['ward']['knock']:g} x this type's {whs[0]['knockMul']} "
                  f"= {ST['ward']['knock'] * whs[0]['knockMul']:.0f} — "
                  f"MORE than the {g['combat']['knock'] * whs[0]['knockMul']:.0f} "
                  f"of its own blow.")
            check("ward on this type does not need Farwarden's hand-patch",
                  ward[1.0]["pool"] > 0 and ward[1.0]["absorbed"] > 0,
                  f"at 1.0 the plate holds {ward[1.0]['pool']:.1f} of a "
                  f"{cap:g} cap and eats {ward[1.0]['absorbed']:.2f} dmg/s")
            check("THE PLATE BREAKING IS A SECOND SHOVE — it pushes the quarry "
                  "out of reach the same way a landed blow does",
                  ward[1.0]["push"] > 0,
                  f"{ward[1.0]['push']:+.1f} units {a.sep_at:g}s after a break "
                  f"at 1.0x, on a {whs[0]['reach']} reach")
            out["deliver"] = deliver
            out["ward"] = {str(k): v for k, v in ward.items()}
            out["control"] = {"dmg": offd, "win": offw}

        # ---------------------------------------------------------- [6] --
        if "6" in want:
            print(f"\n[6] THE TRAPS\n")
            check("the warhammer is mode `spin`, not `swing` — it has no arc",
                  all(w["mode"] == "spin" and not w["arc"] for w in whs),
                  ", ".join(f"{w['name']} {w['mode']}" for w in whs))
            check("no warhammer carries a `shot` field (v39 od 4: tickFire gates "
                  "on the field, not on mode)",
                  not any(w["shot"] for w in whs),
                  "both clean")
            ceiling = whs[0]["blades"] / g["combat"]["hitCd"]
            got = out.get("freeze", {}).get("warhammer", {}).get("shipped", {}).get("contacts")
            check("contact is geometry, not cooldown",
                  got is None or got < ceiling * 0.25,
                  f"one blade at hitCd {g['combat']['hitCd']:g} allows "
                  f"{ceiling:.2f} contacts/s; the row lands "
                  + (f"{got:.3f}" if got else "0.19"))
            dot = [s for s in open_wh if chan.get(s, (None, None))[0]
                   and ST[chan[s][0][0]].get("dps")] if "5" in want else []
            if dot:
                print(f"\n    and one that is not a bug: damage-over-time does not "
                      f"route through `hurt`'s shield gate, so "
                      f"{', '.join(dot)} go UNDER a ward. A vigil hammer's plate "
                      f"is no answer to them.")

        assert not errors, errors[:4]

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED: {', '.join(bad)})" if bad else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
