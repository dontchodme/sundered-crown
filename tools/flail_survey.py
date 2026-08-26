#!/usr/bin/env python3
"""LOOK AT THE FLAIL ROW BEFORE THE ULTIMATE IS DESIGNED.

    python3 flail_survey.py --game ../02-chain/sc-marrowdraw-frame.html

`cell_survey` looks at all 42 cells at once, which is the right instrument for
"which type" and the wrong one for "which school on THIS type". v40 pointed the
same discipline at the bow row and found 82% of every arrow ends on a wall;
v41 pointed it at the warhammer and found the type throws its quarry out of its
own reach. Rick has taken **runic x flail**. This is that instrument pointed at
the flail row.

The flail is the only weapon in the game that is not attached to the ball.
`mode:"chain"` has exactly one member, `CONFIG.chain` is read by nothing else,
and `bladeSegments` returns something structurally different for it than for
the other five types. What is measurably peculiar about it:

  * THE HEAD IS THE WEAPON. Every other type's live segment runs from the shell
    to the tip of the blade -- 58 to 120 units of edge. A chain's segment is a
    stub around the head. Measured off `bladeSegments`, not off the formula.
  * THE HEAD IS NOT WHERE THE WEAPON POINTS. `headAng` is pulled toward
    `theta` by a spring and pushed by gravity, damping and centrifugal
    extension. It is the only contact point in the game that is not a function
    of the facing a viewer can see.
  * A STUN DOES NOT LOCK THIS WEAPON, IT DROPS IT. `tickWeapon`'s chain branch
    runs during a stun with `drive = 0`: the head coasts, sags toward the floor
    and pulls in on a slack chain. Every other type has `else if (f.stun > 0){
    /* weapon locked */ }` and resumes exactly where it stopped.
  * AND ITS OWN SCHOOL-TO-BE HANDS OUT STUNS. Hex is a 0.20s weapon stun. The
    chosen cell puts the stun-dealing school on the stun-sensitive type.

  [1] THE ROW AND THE BLOCK. Read from AC.WEAPONS and AC.CONFIG, not a doc.

  [2] THE HEAD IS THE WEAPON. Live segment length per type off `bladeSegments`,
      contacts per second at pinned damage, and where the head actually is:
      extension, reach from the shell, and lag behind the facing.

  [3] WHAT A STUN COSTS THIS TYPE. A synthetic 0.20s hex stun, one per fight,
      A/B'd against the identical seed with no stun, measured as contacts lost
      in the two seconds after it lands. Every type, same schedule, same pin.

  [4] THE CLANK LADDER. Outcome read off the EFFECT -- whose spinDir reversed,
      who ate the stagger -- never recomputed from the mass formula.

  [5] THE FOUR OPEN CHANNELS AS DELIVERED EFFECT. hex/smite/entangle each get
      one model-free A/B against the same channel deleted. Vigil is not a foe
      status and gets the bank readout instead, with the multiplier sweep that
      answers vigil od 1 from the MIDDLE of the type axis.

  [6] HEX ON THE FLAIL. The chosen cell, deep. Occupancy is a proxy twice
      removed (v39 5.2) -- hex is a RATE. Measured on the lock, on the ladder,
      and on what the cap would be worth if an ultimate could reach it.

  [7] THE TRAPS. Asserted, not assumed.

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


TYPE_DONOR = {"greatsword": "dawnbringer", "twinblade": "widowmaker",
              "warhammer": "grudgebearer", "scythe": "thornwake",
              "flail": "gravemourn", "bow": "ironhail"}
# One foe per type, none of them a donor, so every cross-type row is scored
# against the identical field.
FOES = ["emberedge", "spellbreaker", "lastlight", "aureole", "censer"]

# --------------------------------------------------------------- [1] grid ---

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape,
    reach: w.reach, width: w.width, artW: w.artW, dmg: w.dmg, spin: w.spin,
    mode: w.mode, mass: w.mass, arc: w.arc || null, blades: w.blades.length,
    knockMul: w.knockMul || null, shot: !!w.shot,
    onHit: w.onHit ? Object.entries(w.onHit)[0] : null,
    onSelf: w.onSelf ? Object.entries(w.onSelf)[0] : null,
    ult: w.ult ? { name: w.ult.name, charge: w.ult.charge,
                   dur: w.ult.dur || null } : null,
  }));
  const S = {};
  for (const [k, v] of Object.entries(AC.STATUS)) S[k] = Object.assign({}, v);
  return { weapons: W, status: S, affinities: Object.keys(AC.AFFINITIES),
           dt: AC.CONFIG.physics.dt, ballR: AC.CONFIG.physics.ballR,
           gravity: AC.CONFIG.physics.gravity,
           combat: AC.CONFIG.combat, clank: AC.CONFIG.clank,
           chain: AC.CONFIG.chain, impact: AC.CONFIG.impact };
}"""


# ---------------------------------------------------------- [2] geometry ---
# The live segment is read off `bladeSegments` -- the function the hit test
# actually calls -- and not from `reach`, because for a chain those are two
# different numbers and the whole point of this section is that they are.
#
# The head samples are taken every frame of a real fight, so extension and lag
# are what the fight sees, not what the constructor sets.

GEOM_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const R  = AC.CONFIG.physics.ballR;
  const C  = AC.CONFIG.chain;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }
  const angDiff = (a, b) => { let d = (a - b) % (Math.PI*2);
    if (d >  Math.PI) d -= Math.PI*2; if (d < -Math.PI) d += Math.PI*2; return d; };

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const chain = me.w.mode === "chain";
      const chainLen = me.w.reach * (1 - C.hilt);

      let step = 0, hits = 0;
      let segSum = 0, segN = 0, segMin = 1e9, segMax = 0;
      let extSum = 0, reachSum = 0, lagSum = 0, lagAbsMax = 0;
      let taut = 0, slack = 0;
      let reachMin = 1e9, reachMax = 0;

      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        if (self === me && mul === undefined) hits++;
        return r;
      };

      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const segs = m.bladeSegments(me);
        for (const s of segs){
          const L = Math.hypot(s.bx - s.ax, s.by - s.ay);
          segSum += L; segN++;
          if (L < segMin) segMin = L;
          if (L > segMax) segMax = L;
        }
        if (chain){
          const ext = me.headR / chainLen;
          extSum += ext;
          if (ext >= 0.98) taut++;
          if (ext <= 0.45) slack++;
          const d = Math.hypot(me.headX - me.x, me.headY - me.y);
          reachSum += d;
          if (d < reachMin) reachMin = d;
          if (d > reachMax) reachMax = d;
          const lag = angDiff(me.headAng, me.theta);
          lagSum += Math.abs(lag);
          if (Math.abs(lag) > lagAbsMax) lagAbsMax = Math.abs(lag);
        } else {
          /* the same two questions asked of a rigid weapon, so the flail row
             has a control rather than a solo number */
          const segs2 = segs[0];
          reachSum += Math.hypot(segs2.bx - me.x, segs2.by - me.y);
          lagSum += 0; extSum += 1; taut++;
        }
      }
      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT, chain,
                  hits, seg: segN ? segSum / segN : 0, segMin, segMax,
                  ext: step ? extSum / step : 0,
                  taut: step ? taut / step : 0, slack: step ? slack / step : 0,
                  reach: step ? reachSum / step : 0,
                  reachMin: reachMin === 1e9 ? 0 : reachMin, reachMax,
                  lag: step ? lagSum / step : 0, lagMax: lagAbsMax,
                  chainLen });
    }
  }
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


# ------------------------------------------------------------- [3] stun ---
# ONE forced 0.20s stun per fight -- a hex stun, exactly -- against the
# identical seed with none. The readout is contacts in the WINDOW after it,
# because a whole-fight difference would be chaos rather than the stun.
#
# The stun is written the way STATUS.hex writes it (`f.stun = Math.max(...)`)
# and at a time chosen from the seed, so the schedule is identical between the
# two arms and identical across types.

STUN_JS = r"""([donor, foes, seeds, ats, win, rwin, dur, secs, pin, pinIds, noult, armed]) => {
  const DT = AC.CONFIG.physics.dt;
  const C  = AC.CONFIG.chain;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
  }
  const angDiff = (a, b) => { let d = (a - b) % (Math.PI*2);
    if (d >  Math.PI) d -= Math.PI*2; if (d < -Math.PI) d += Math.PI*2; return d; };

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      for (const at of ats){
        const m  = new AC.Match(donor, f, sd);
        const me = m.a.w.id === donor ? m.a : m.b;
        const chain = me.w.mode === "chain";
        const chainLen = me.w.reach * (1 - C.hilt);
        const atStep  = Math.round(at / DT);
        /* The ARC window is short on purpose. The two arms are identical up to
           the stun and diverge after it, so a long window measures chaos
           rather than the stun -- run this at --stun-win 2 and the calibration
           row below stops holding. The EXTENSION horizon is longer because
           recovery is a slower process than the thing that caused it, and it
           is read off one arm only, so divergence cannot reach it. */
        const endStep = Math.round((at + win) / DT);
        const horizon = Math.round((at + Math.max(win, rwin)) / DT);
        const ang = () => chain ? me.headAng : me.theta;

        let step = 0, alive = true, hitsWin = 0;
        /* THE ARC, not the contacts. A 2s window holds 0.15 expected contacts
           for this type, so a Bernoulli count is noise; the angle the weapon
           actually turns through is a smooth quantity with the same meaning.
           Normalised by the unstunned arm's own rate, it reads in SECONDS OF
           SWING, and a rigid weapon must return the stun's own duration --
           which is the calibration this table lives or dies by. */
        let arc = 0, path = 0, prev = 0, recov = -1;
        let ext0 = 0, extEnd = 0, extMin = 1e9, vel0 = 0;

        const origHit = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
          const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
          if (self === me && mul === undefined && step >= atStep && step < endStep)
            hitsWin++;
          return r;
        };

        while (step < horizon){
          if (m.over){ alive = false; break; }
          if (step === atStep){
            prev = ang();
            if (chain){ ext0 = me.headR / chainLen; vel0 = Math.abs(me.headAngVel); }
            if (armed) me.stun = Math.max(me.stun, dur);
          }
          m.step(DT); step++;
          if (step > atStep){
            const a2 = ang();
            if (step <= endStep){
              const d = Math.abs(angDiff(a2, prev));
              arc  += d;
              path += d * (chain ? me.headR : me.w.reach);
            }
            prev = a2;
            if (chain){
              const e = me.headR / chainLen;
              if (e < extMin) extMin = e;
              /* the head is back when it reaches the extension it had when the
                 stun landed, and only after it has actually dipped -- so a
                 stun that happened to land on a head already swinging in does
                 not score an instant recovery */
              if (recov < 0 && extMin < ext0 - 0.01 && e >= ext0)
                recov = (step - atStep) * DT;
            }
          }
        }
        if (chain && alive) extEnd = me.headR / chainLen;
        if (!alive){ arc = -1; }       // a fight that ended is not a window
        rows.push({ foe: f, seed: sd, at, armed, alive, chain,
                    arc, path, hitsWin, recov,
                    ext0, extEnd, extMin: extMin === 1e9 ? 0 : extMin, vel0 });
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


# ------------------------------------------------- [4][5] shared with v41 ---
# The clank ladder, the channel A/B and the ward readout are the SAME
# instruments v41 pointed at the warhammer row, imported rather than
# transcribed, so the two rows are comparable line for line and a future fix
# to one of them fixes both.
from wh_survey import CLANK_JS, CHANNEL_JS, WARD_JS  # noqa: E402


# --------------------------------------------------------------- [6] hex ---
# v39 5.2: hex is not a quantity, it is a RATE. `hexClock += dt * stacks` and
# a stun fires at 1.15, so five stacks do not lock harder, they lock five times
# as often -- and `Math.max` means two overlapping locks are one lock.
# Occupancy is a proxy twice removed. This measures the lock itself.
#
# `hold` forces the quarry's hex to a fixed stack count every frame, which is
# the ceiling an ultimate could aim at. hold=0 is the shipped ladder.

HEX_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult, hold, chan]) => {
  const DT = AC.CONFIG.physics.dt;
  const H  = AC.STATUS.hex;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "runic";
  delete w.onHit; delete w.onSelf;
  if (chan > 0) w.onHit = { hex: chan };

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
      const th0 = th.maxHp;

      let step = 0, hits = 0, fires = 0, lock = 0, frozen = 0;
      let stackSum = 0, ge2 = 0, atCap = 0, any = 0;
      let apps = 0, appsCold = 0, appsCap = 0;   // where each application lands
      let lastHit = -1, gapSum = 0, gapN = 0, gapCold = 0;
      let prevClock = 0;

      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        if (self === me && mul === undefined){
          const st = foe2.status && foe2.status.hex;
          const n = st ? st.stacks : 0;
          apps++;
          if (n === 0) appsCold++;
          if (n >= H.maxStacks) appsCap++;
          if (lastHit >= 0){
            const g = (step - lastHit) * DT;
            gapSum += g; gapN++;
            if (g > H.dur) gapCold++;
          }
          lastHit = step;
          hits++;
        }
        return origHit.call(m, self, foe2, hx, hy, seg, mul, over);
      };

      while (!m.over && step < secs / DT){
        /* PINNED, not applied. `apply` ADDS n and clamps, so applying k every
           frame walks to the cap whatever k is; this holds the ladder at
           exactly k, which is the ceiling an ultimate could aim at. */
        if (hold > 0 && th.alive) th.status.hex = { stacks: hold, t: H.dur };
        const wasFrozen = m.hitStop > 0;
        m.step(DT); step++;
        if (wasFrozen) frozen++;
        const st = th.status && th.status.hex;
        const n = st ? st.stacks : 0;
        stackSum += n;
        if (n >= 1) any++;
        if (n >= 2) ge2++;
        if (n >= H.maxStacks) atCap++;
        /* a fire is the clock resetting -- read off the effect, not recomputed */
        const c = th.hexClock || 0;
        if (c < prevClock - 1e-9) fires++;
        prevClock = c;
        if (th.stun > 0) lock++;
      }
      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits, foeHits: th.hits, fires, lock, frozen,
                  stackSum, ge2, atCap, any,
                  apps, appsCold, appsCap,
                  gapSum, gapN, gapCold,
                  dealt: me.dealt, taken: th.dealt,
                  destroyed: th0 - th.hp, meHp: me.hp, thHp: th.hp });
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


# ------------------------------------------------------------- [7] traps ---

TRAP_JS = r"""() => {
  const src = AC.Match.prototype.tickWeapon.toString();
  const seg = AC.Match.prototype.bladeSegments.toString();
  const hit = AC.Match.prototype.tickHits.toString();
  const fire = AC.Match.prototype.tickFire.toString();
  return {
    chainModes: AC.WEAPONS.filter(w => w.mode === "chain").map(w => w.id),
    modes: [...new Set(AC.WEAPONS.map(w => w.mode))],
    /* the chain branch runs before the stun guard; every other mode is behind
       it. Read off the source rather than asserted in prose. */
    chainBeforeStunGuard:
      seg.indexOf('mode === "chain"') >= 0 &&
      src.indexOf('mode === "chain"') < src.indexOf("weapon locked"),
    stunGuardText: /else if \(f\.stun > 0\)\{ \/\* weapon locked \*\/ \}/.test(src),
    hitsSkipOnStun: /self\.stun > 0/.test(hit),
    fireSkipsOnStun: /f\.stun > 0/.test(fire),
    flailHasShot: AC.WEAPONS.filter(w => w.shape === "flail" && !!w.shot).map(w => w.id),
    chainCfg: Object.assign({}, AC.CONFIG.chain),
    hexIsTrueStun: AC.STATUS.hex.stunFor,
  };
}"""

# The bind's decisive threshold is a literal inside `resolveClank`, not a
# CONFIG knob, so it is READ OFF THE SHIPPED SOURCE rather than copied here. A
# change to the engine moves this tool with it; a change to this tool cannot
# move the engine.
DECISIVE_JS = r"""() => {
  const src = AC.Match.prototype.resolveClank.toString();
  const m = src.match(/Math\.abs\(shareA - shareB\)\s*>\s*([0-9.]+)/);
  const e = src.match(/Math\.pow\(mA,\s*([0-9.]+)\)/);
  return { decisive: m ? parseFloat(m[1]) : null,
           exponent: e ? parseFloat(e[1]) : null };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw-frame.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--sep-at", type=float, default=0.25)
    ap.add_argument("--stun-win", type=float, default=1.0)
    ap.add_argument("--recov-win", type=float, default=4.0)
    ap.add_argument("--only", default="", help="comma list of section numbers")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"1", "2", "3", "4", "5", "6", "7"}
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
        flails = [w for w in W if w["shape"] == "flail"]
        open_fl = [s for s in schools if (s, "flail") not in filled]
        pin_ids = [w["id"] for w in W]
        donor = TYPE_DONOR["flail"]
        CH = g["chain"]

        # ---------------------------------------------------------- [1] --
        if "1" in want:
            print(f"\n[1] THE FLAIL ROW — {len(flails)} of {len(schools)} filled, "
                  f"{len(open_fl)} open\n")
            print(f"    {'':<12}" + "".join(f"{s[:11]:>12}" for s in schools))
            print(f"    {'flail':<12}"
                  + "".join(f"{filled.get((s,'flail'),'·')[:11]:>12}" for s in schools))
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
            print(f"\n    CONFIG.chain  " + "  ".join(f"{k} {v:g}" for k, v in CH.items()))

            fields = ("reach", "width", "artW", "spin", "mode", "mass",
                      "knockMul", "blades")
            same = all(len({w[f] for w in flails}) == 1 for f in fields)
            check("all three flails share one physics block, field for field",
                  same, ", ".join(f"{f}={flails[0][f]}" for f in fields))

            modes = {}
            for w in W:
                modes.setdefault(w["mode"], set()).add(w["shape"])
            check("`chain` is a mode of one — no other type shares a line of it",
                  modes.get("chain") == {"flail"},
                  "  ".join(f"{k}: {','.join(sorted(v))}" for k, v in sorted(modes.items())))

            hardest = max(W, key=lambda w: w["dmg"])
            check("the flail carries the hardest blow in the game",
                  hardest["shape"] == "flail",
                  f"{hardest['name']} {hardest['dmg']:g}, next type is "
                  + max((t for t in shapes if t != 'flail'),
                        key=lambda t: max(w['dmg'] for w in W if w['shape'] == t))
                  + f" at {max(w['dmg'] for w in W if w['shape'] != 'flail'):g}")

            heavier = sorted({w["mass"] for w in W}, reverse=True)
            check("mass 3.6 is second on the ladder, behind the warhammer alone",
                  heavier[1] == flails[0]["mass"],
                  f"ladder {', '.join(f'{m:g}' for m in heavier)}")
            out["block"] = {f: flails[0][f] for f in fields}
            out["chain"] = CH

        # ---------------------------------------------------------- [2] --
        geom = {}
        if "2" in want:
            print(f"\n[2] THE HEAD IS THE WEAPON — live segment read off "
                  f"`bladeSegments`, dmg pinned {a.pin:g}, ultimates suppressed\n")
            print(f"    {'type':<12}{'live blade':>12}{'contacts/s':>12}"
                  f"{'tip / head':>12}{'reach':>7}{'extension':>11}{'taut':>8}"
                  f"{'slack':>8}{'lag rad':>9}{'lag max':>9}")
            for t in shapes:
                d = TYPE_DONOR[t]
                rows = page.evaluate(GEOM_JS, [d, FOES, seeds, a.secs, a.pin,
                                               pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                hits = sum(r["hits"] for r in rows)
                geom[t] = {
                    "seg": mean(r["seg"] for r in rows),
                    "segMin": min(r["segMin"] for r in rows),
                    "segMax": max(r["segMax"] for r in rows),
                    "hps": hits / dur if dur else 0, "hits": hits, "dur": dur,
                    "reach": mean(r["reach"] for r in rows),
                    "reachMax": max(r["reachMax"] for r in rows),
                    "ext": mean(r["ext"] for r in rows),
                    "taut": mean(r["taut"] for r in rows),
                    "slack": mean(r["slack"] for r in rows),
                    "lag": mean(r["lag"] for r in rows),
                    "lagMax": max(r["lagMax"] for r in rows),
                    "chain": rows[0]["chain"], "donor": d,
                    "nominal": by_id[d]["reach"] + 4,
                }
                q = geom[t]
                print(f"    {t:<12}{q['seg']:>12.1f}{q['hps']:>12.3f}"
                      f"{q['reach']:>12.1f}{by_id[d]['reach']:>7}"
                      f"{q['ext']:>11.2f}{q['taut']:>8.0%}{q['slack']:>8.0%}"
                      f"{q['lag']:>9.2f}{q['lagMax']:>9.2f}")

            fl = geom["flail"]
            others = {t: q for t, q in geom.items() if t != "flail"}
            check("the flail's live blade is the shortest in the game by a "
                  "long way",
                  all(fl["seg"] < q["seg"] * 0.5 for q in others.values()),
                  f"{fl['seg']:.1f} units against "
                  + ", ".join(f"{t} {q['seg']:.0f}" for t, q in
                              sorted(others.items(), key=lambda kv: kv[1]['seg'])))
            wid = by_id[donor]["width"]
            check("the flail's segment is 0.6 x its WIDTH and has nothing to do "
                  "with its reach",
                  abs(fl["seg"] - wid * 0.6) < 0.05,
                  f"{fl['seg']:.2f} against width {wid} x 0.6 = {wid * 0.6:.1f}; "
                  f"reach {by_id[donor]['reach']} does not appear in it")
            check("and every rigid weapon's segment IS its reach, shell to tip, "
                  "which is what makes the flail's number mean something",
                  all(q["nominal"] - 4 < q["seg"] < (q["nominal"] - 4) * 1.2
                      for q in others.values()),
                  ", ".join(f"{t} {q['seg']:.0f} on a reach of {q['nominal'] - 4:g}"
                            for t, q in sorted(others.items()))
                  + "  (act reach modifiers are the excess)")
            print(f"\n    the head's reachable band, which is the thing the "
                  f"segment above sits somewhere inside:\n"
                  f"    {fl['reach']:.1f} mean, {geom['flail']['reachMax']:.1f} "
                  f"furthest, on a chain of {by_id[donor]['reach'] * (1 - CH['hilt']):.1f} "
                  f"hung off a haft of {by_id[donor]['reach'] * CH['hilt']:.1f}")
            check("the chain lags its own facing and nothing else does",
                  fl["lag"] > 0.2 and all(q["lag"] < 1e-9 for q in others.values()),
                  f"mean |headAng-theta| {fl['lag']:.2f} rad, "
                  f"max {fl['lagMax']:.2f} rad")
            out["geom"] = geom

        # ---------------------------------------------------------- [3] --
        if "3" in want:
            ats = [6.0, 10.0, 14.0, 18.0, 22.0, 26.0]
            sdur = ST["hex"]["stunFor"]
            print(f"\n[3] WHAT A {sdur:g}s STUN COSTS EACH TYPE — one stun per "
                  f"fight, A/B'd against the identical seed with none.\n"
                  f"    Read as SWING LOST, not as contacts: a {a.stun_win:g}s "
                  f"window holds a fifth of a flail contact, so a count is\n"
                  f"    noise. The angle the weapon turns through is the same "
                  f"question with a usable variance, and\n    the distance the "
                  f"live edge travels is that question again with the radius "
                  f"left in.\n")
            print(f"    {'type':<12}{'mode':<8}{'arc/s':>8}{'swing lost':>12}"
                  f"{'x stun':>8}{'path lost':>11}{'x stun':>8}"
                  f"{'ext at t0':>11}{'floor':>8}"
                  f"{('at +' + format(a.stun_win, 'g') + 's'):>9}")
            stun = {}
            for t in shapes:
                d = TYPE_DONOR[t]
                args = [d, FOES, seeds, ats, a.stun_win, a.recov_win, sdur,
                        a.secs, a.pin, pin_ids, True]
                off = page.evaluate(STUN_JS, args + [False])
                on = page.evaluate(STUN_JS, args + [True])
                key = lambda r: (r["foe"], r["seed"], r["at"])
                onm = {key(r): r for r in on if r["alive"]}
                pairs = [(r, onm[key(r)]) for r in off
                         if r["alive"] and key(r) in onm]
                a0 = mean(x[0]["arc"] for x in pairs)
                a1 = mean(x[1]["arc"] for x in pairs)
                p0 = mean(x[0]["path"] for x in pairs)
                p1 = mean(x[1]["path"] for x in pairs)
                lost = a.stun_win * (1 - a1 / a0) if a0 else 0
                plost = a.stun_win * (1 - p1 / p0) if p0 else 0
                stun[t] = {"n": len(pairs), "a0": a0, "a1": a1,
                           "p0": p0, "p1": p1,
                           "lost": lost, "ratio": lost / sdur if sdur else 0,
                           "plost": plost, "pratio": plost / sdur if sdur else 0,
                           "mode": by_id[d]["mode"],
                           "ext0": mean(x[1]["ext0"] for x in pairs),
                           "extMin": mean(x[1]["extMin"] for x in pairs),
                           "extEnd": mean(x[1]["extEnd"] for x in pairs),
                           "recov": mean(x[1]["recov"] for x in pairs
                                         if x[1]["recov"] >= 0),
                           "nRecov": sum(1 for x in pairs if x[1]["recov"] >= 0),
                           "nDip": sum(1 for x in pairs
                                       if x[1]["extMin"] < x[1]["ext0"] - 0.01),
                           "chain": pairs[0][1]["chain"] if pairs else False}
                q = stun[t]
                ext = (f"{q['ext0']:>11.2f}{q['extMin']:>8.2f}{q['extEnd']:>9.2f}"
                       if q["chain"] else f"{'—':>11}{'—':>8}{'—':>9}")
                print(f"    {t:<12}{q['mode']:<8}{q['a0'] / a.stun_win:>8.2f}"
                      f"{q['lost']:>12.3f}{q['ratio']:>7.2f}x"
                      f"{q['plost']:>11.3f}{q['pratio']:>7.2f}x{ext}")

            fl = stun["flail"]
            rigid = {t: q for t, q in stun.items()
                     if t != "flail" and q["mode"] != "swing"}
            gs = stun["greatsword"]
            check("the instrument is calibrated — a weapon whose facing is its "
                  "own clock loses exactly the stun and not a millisecond more",
                  all(abs(q["ratio"] - 1.0) < 0.15 for q in rigid.values()),
                  ", ".join(f"{t} {q['ratio']:.2f}x" for t, q in sorted(rigid.items())))
            check("and the greatsword is the exception for a reason the source "
                  "states — `mode:\"swing\"` recomputes theta from the AIM every "
                  "frame, so a stunned greatsword's blade keeps tracking",
                  gs["ratio"] < 0.6,
                  f"{gs['ratio']:.2f}x — it is the only type in the game whose "
                  f"facing is not an integral of its own spin")
            check("THE HYPOTHESIS IS REFUTED: a stun costs the flail the same "
                  "swing it costs everything else. The head coasts through it, "
                  "and the coast pays for the respin",
                  abs(fl["ratio"] - 1.0) < 0.15,
                  f"{fl['lost']:.3f}s of swing for a {sdur:g}s stun — "
                  f"{fl['ratio']:.2f}x, inside the rigid band "
                  f"{min(q['ratio'] for q in rigid.values()):.2f}–"
                  f"{max(q['ratio'] for q in rigid.values()):.2f}")
            check("what it costs instead is REACH — the head pulls in and the "
                  "live edge travels a shorter circle for it",
                  fl["pratio"] > fl["ratio"] + 0.12
                  and all(abs(q["pratio"] - q["ratio"]) < 1e-6
                          for q in rigid.values()),
                  f"path {fl['pratio']:.2f}x against swing {fl['ratio']:.2f}x; "
                  f"extension {fl['ext0']:.2f} at the stun, floor "
                  f"{fl['extMin']:.2f}. For a rigid weapon the radius is a "
                  f"constant and the two columns are the same number by "
                  f"construction, which is what makes the flail's gap readable")
            check("and the reach comes back slower than the stun goes away, "
                  "which is the whole of what this type pays extra",
                  fl["recov"] > sdur and fl["nRecov"] > 0.5 * fl["nDip"],
                  f"{fl['recov']:.2f}s to climb back to the extension it had, "
                  f"against the {sdur:g}s stun itself — so the event is about "
                  f"{sdur + fl['recov']:.2f}s of shortened reach, roughly "
                  f"{(sdur + fl['recov']) / sdur:.0f}x the stun. Recovered "
                  f"inside the window in {fl['nRecov']} of {fl['nDip']} dips; "
                  f"the {fl['nDip'] - fl['nRecov']} that did not are censored "
                  f"OUT of that mean, so it is a floor")
            out["stun"] = stun

        # ---------------------------------------------------------- [4] --
        if "4" in want:
            dz = page.evaluate(DECISIVE_JS)
            thr, expo = dz["decisive"], dz["exponent"]
            clank_foes = FOES + ["slagheart"]
            print(f"\n[4] THE CLANK LADDER — measured off the effect, dmg "
                  f"pinned {a.pin:g}, ultimates suppressed.\n    Outcome is read "
                  f"from whose spinDir reversed and who ate the stagger, never "
                  f"recomputed from the mass\n    formula the game owns — and "
                  f"then checked AGAINST it. `margin` is |shareA-shareB| out of "
                  f"mass^{expo:g},\n    and a bind is decisive above "
                  f"{thr:g}.\n")
            print(f"    {'foe':<14}{'type':<11}{'mass':>6}{'margin':>8}"
                  f"{'clanks/min':>11}{'won':>7}{'deadlock':>10}{'lost':>7}"
                  f"{'stun taken':>12}{'stun dealt':>12}{'bind→hit':>10}")
            cl_rows = {}
            mf = flails[0]["mass"] ** expo
            for f in clank_foes:
                rows = page.evaluate(CLANK_JS, [donor, [f], seeds, a.secs,
                                                a.pin, pin_ids, True])
                cl = sum(r["clanks"] for r in rows)
                dr = sum(r["dur"] for r in rows)
                nAll = sum(r["nWon"] + r["nLost"] + r["nDead"] for r in rows)
                gAll = sum(r["gapWon"] + r["gapLost"] + r["gapDead"] for r in rows)
                mo = by_id[f]["mass"] ** expo
                cl_rows[f] = {"mass": by_id[f]["mass"], "shape": by_id[f]["shape"],
                              "margin": abs(mo - mf) / (mo + mf),
                              "heavier": mo > mf,
                              "clanks": cl, "dur": dr,
                              "won": sum(r["won"] for r in rows),
                              "lost": sum(r["lost"] for r in rows),
                              "dead": sum(r["dead"] for r in rows),
                              "stunMe": sum(r["stunMe"] for r in rows),
                              "stunTh": sum(r["stunTh"] for r in rows),
                              "gap": gAll / nAll if nAll else 0, "nGap": nAll}
                c = cl_rows[f]
                print(f"    {f:<14}{c['shape']:<11}{c['mass']:>6.1f}"
                      f"{c['margin']:>8.3f}{cl / c['dur'] * 60:>11.1f}"
                      f"{(c['won'] / cl if cl else 0):>7.0%}"
                      f"{(c['dead'] / cl if cl else 0):>10.0%}"
                      f"{(c['lost'] / cl if cl else 0):>7.0%}"
                      f"{c['stunMe']:>12.1f}{c['stunTh']:>12.1f}{c['gap']:>10.2f}")

            def outcome(c):
                if c["margin"] <= thr:
                    return "dead"
                return "lost" if c["heavier"] else "won"
            agree = all(
                (c[outcome(c)] / c["clanks"]) > 0.98
                for c in cl_rows.values() if c["clanks"])
            check("the effect and the mass model agree on every foe — which is "
                  "what makes the margin column a prediction rather than a "
                  "restatement",
                  agree,
                  ", ".join(f"{f} {outcome(c)} "
                            f"{c[outcome(c)] / max(1, c['clanks']):.0%}"
                            for f, c in cl_rows.items()))
            gsm = cl_rows["emberedge"]
            check("THE FLAIL IS HEAVIER THAN THE GREATSWORD AND CANNOT CASH IT "
                  "— the second-heaviest weapon in the game deadlocks with a "
                  "3.0, by six thousandths",
                  gsm["margin"] < thr and gsm["margin"] > thr * 0.9
                  and gsm["dead"] > gsm["won"],
                  f"margin {gsm['margin']:.4f} against a {thr:g} threshold — "
                  f"{thr - gsm['margin']:.4f} short, on {gsm['clanks']} binds, "
                  f"{gsm['dead'] / max(1, gsm['clanks']):.0%} of them deadlocks")
            lost_to = [f for f, c in cl_rows.items() if c["lost"] > c["won"]]
            check("and it loses binds to exactly one weapon in the game",
                  lost_to == ["censer"],
                  f"the 5.0 warhammer, {cl_rows['censer']['lost']} of "
                  f"{cl_rows['censer']['clanks']}, at "
                  f"{cl_rows['censer']['stunMe']:.0f}s of stagger taken "
                  f"against {cl_rows['censer']['stunTh']:.0f}s dealt")
            print(f"\n    `bind→hit` is the seconds from a bind to this "
                  f"relic's next landed blow. It is the recovery [3] priced\n"
                  f"    on the weapon, priced again on the fight: "
                  + ", ".join(f"{by_id[f]['shape']} {c['gap']:.2f}s"
                              for f, c in sorted(cl_rows.items(),
                                                 key=lambda kv: kv[1]["gap"]))
                  + ".")
            out["clank"] = cl_rows
            out["decisive"] = dz

        # ---------------------------------------------------------- [5] --
        if "5" in want:
            print(f"\n[5] THE FOUR OPEN CHANNELS AS DELIVERED EFFECT — SHIPPED "
                  f"damage, ultimates suppressed, same seeds on and off.\n    "
                  f"Sections 2-4 pin damage because they compare TYPES; this "
                  f"one compares schools on one type, where the\n    pin would "
                  f"only take the compensation this type is paid for its "
                  f"contact rate away from it.\n")
            print("    the readout is the FOE'S OWN HEALTH, ceiling captured "
                  "before curse could move it:\n    `self.dealt` counts what "
                  "resolveHit paid out and is blind to every DoT.\n")
            chans = [(None, None, 0), ("runic", "hex", 1),
                     ("sanctified", "smite", 1), ("verdant", "entangle", 2)]
            print(f"    {'cell':<24}{'status':<11}{'hp/s':>8}{'vs control':>12}"
                  f"{'win':>7}{'hits/min':>10}{'taken/s':>9}")
            base = None
            ch_rows = {}
            for aff, key, per in chans:
                rows = page.evaluate(CHANNEL_JS,
                                     [donor, aff or by_id[donor]["aff"], key, per,
                                      FOES, seeds, a.secs, 0, pin_ids, True,
                                      bool(key)])
                dr = sum(r["dur"] for r in rows)
                hp = sum(r["destroyed"] for r in rows) / dr
                wins = [r["win"] for r in rows if r["win"] >= 0]
                q = {"hp": hp, "win": mean(wins),
                     "hits": sum(r["hits"] for r in rows) / dr * 60,
                     "taken": sum(r["taken"] for r in rows) / dr, "n": len(rows)}
                if base is None:
                    base = hp
                    label, st = "— no channel —", ""
                    delta = ""
                else:
                    ch_rows[f"{aff} x flail"] = q
                    label, st = f"{aff} x flail", key
                    delta = f"{(hp / base - 1):>+11.1%}"
                print(f"    {label:<24}{st:<11}{hp:>8.2f}{delta:>12}"
                      f"{q['win']:>7.0%}{q['hits']:>10.1f}{q['taken']:>9.2f}")
                q["delta"] = hp / base - 1
            out["channels"] = ch_rows

            print(f"\n    vigil is not a foe status. `onSelf.ward`'s value is a "
                  f"per-relic BANK MULTIPLIER —\n    Lightkeeper 1.0 on a "
                  f"greatsword, Farwarden 2.5 on a bow, and v41 measured the "
                  f"warhammer\n    at 1.0. This is the middle of that axis.\n")
            mults = [1.0, 1.6, 2.3, 3.0]
            rows = page.evaluate(WARD_JS, [donor, mults, FOES, seeds, a.secs,
                                           0, pin_ids, True, a.sep_at])
            print(f"    {'mult':>6}{'banked/s':>10}{'absorbed/s':>12}"
                  f"{'mean pool':>11}{'held':>7}{'at cap':>8}"
                  f"{'breaks/fight':>14}{'burst':>8}{'win':>7}")
            ward_rows = {}
            for mu in mults:
                rs = [r for r in rows if abs(r["mult"] - mu) < 1e-9]
                dr = sum(r["dur"] for r in rs)
                wins = [r["win"] for r in rs if r["win"] >= 0]
                nb = sum(r["breaks"] for r in rs)
                q = {"banked": sum(r["banked"] for r in rs) / dr,
                     "absorbed": sum(r["absorbed"] for r in rs) / dr,
                     "pool": mean(r["pool"] for r in rs),
                     "held": mean(r["held"] for r in rs),
                     "cap": mean(r["atCap"] for r in rs),
                     "breaks": nb / len(rs),
                     "burst": (sum(r["burst"] for r in rs) / nb) if nb else 0,
                     "win": mean(wins)}
                ward_rows[mu] = q
                print(f"    {mu:>6.1f}{q['banked']:>10.2f}{q['absorbed']:>12.2f}"
                      f"{q['pool']:>11.1f}{q['held']:>7.0%}{q['cap']:>8.1%}"
                      f"{q['breaks']:>14.2f}{q['burst']:>8.1f}{q['win']:>7.0%}")
            out["ward"] = ward_rows

        # ---------------------------------------------------------- [6] --
        if "6" in want:
            H = ST["hex"]
            print(f"\n[6] HEX ON THE FLAIL — the chosen cell. hex is a RATE: "
                  f"one stack fires a {H['stunFor']:g}s weapon stun every "
                  f"{H['stunEvery']:g}s,\n    and k stacks fire k times as "
                  f"often. Cap {H['maxStacks']}, duration {H['dur']:g}s.\n")
            arms = [("no channel", 0, 0), ("shipped hex:1", 1, 0)] + \
                   [(f"pinned at {k}", 1, k) for k in range(1, H["maxStacks"] + 1)]
            print(f"    {'arm':<16}{'hits/s':>8}{'gap':>7}{'mean':>7}{'>=2':>6}"
                  f"{'cap':>6}{'fires/s':>9}{'lock':>7}{'foe hits/s':>12}"
                  f"{'taken/s':>9}{'hp/s':>7}{'net':>8}{'win':>7}")
            hx_rows = {}
            base = None
            for label, chan, hold in arms:
                rows = page.evaluate(HEX_JS, [donor, FOES, seeds, a.secs, 0,
                                              pin_ids, True, hold, chan])
                dr = sum(r["dur"] for r in rows)
                steps = sum(r["steps"] for r in rows)
                wins = [r["win"] for r in rows if r["win"] >= 0]
                gN = sum(r["gapN"] for r in rows)
                q = {"hps": sum(r["hits"] for r in rows) / dr,
                     "gap": sum(r["gapSum"] for r in rows) / gN if gN else 0,
                     "mean": sum(r["stackSum"] for r in rows) / steps,
                     "ge2": sum(r["ge2"] for r in rows) / steps,
                     "cap": sum(r["atCap"] for r in rows) / steps,
                     "fires": sum(r["fires"] for r in rows) / dr,
                     "lock": sum(r["lock"] for r in rows) / steps,
                     "hp": sum(r["destroyed"] for r in rows) / dr,
                     "foeHps": sum(r["foeHits"] for r in rows) / dr,
                     "taken": sum(r["taken"] for r in rows) / dr,
                     "win": mean(wins), "n": len(rows),
                     "apps": sum(r["apps"] for r in rows),
                     "cold": sum(r["appsCold"] for r in rows),
                     "appsCap": sum(r["appsCap"] for r in rows),
                     "gapCold": sum(r["gapCold"] for r in rows), "gapN": gN}
                if base is None:
                    base = q["hp"]; baseTaken = q["taken"]
                    net = ""; q["net"] = 0.0; q["netTaken"] = 0.0
                else:
                    net = f"{(q['hp'] / base - 1):>+7.1%}"
                    q["net"] = q["hp"] / base - 1
                    q["netTaken"] = q["taken"] / baseTaken - 1
                hx_rows[label] = q
                print(f"    {label:<16}{q['hps']:>8.3f}{q['gap']:>7.2f}"
                      f"{q['mean']:>7.2f}{q['ge2']:>6.0%}{q['cap']:>6.0%}"
                      f"{q['fires']:>9.3f}{q['lock']:>7.1%}{q['foeHps']:>12.3f}"
                      f"{q['taken']:>9.2f}{q['hp']:>7.2f}"
                      f"{net:>8}{q['win']:>7.0%}")

            sh = hx_rows["shipped hex:1"]
            print(f"\n    THE LADDER CANNOT START. The flail lands a blow every "
                  f"{sh['gap']:.2f}s and hex\n    expires in {H['dur']:g}s, so "
                  f"{sh['cold'] / sh['apps']:.0%} of every hex this cell applies "
                  f"lands on a foe with NO stacks\n    and {sh['gapCold'] / max(1, sh['gapN']):.0%} "
                  f"of the gaps between its own blows are longer than the status "
                  f"it carries.\n")
            check("the flail's own contact interval is longer than hex's "
                  "duration — the cell cannot build a ladder",
                  sh["gap"] > H["dur"],
                  f"{sh['gap']:.2f}s between blows against a {H['dur']:g}s status")
            check("a fire is read off the clock resetting, and the rate agrees "
                  "with stacks/stunEvery over unfrozen time",
                  abs(sh["fires"] - sh["mean"] / H["stunEvery"]) <
                  0.25 * max(1e-9, sh["mean"] / H["stunEvery"]),
                  f"observed {sh['fires']:.3f}/s against "
                  f"{sh['mean'] / H['stunEvery']:.3f}/s predicted")
            top = hx_rows[f"pinned at {H['maxStacks']}"]
            one = hx_rows["pinned at 1"]
            ctl = hx_rows["no channel"]
            check("the ladder does what the model says — k stacks lock k times "
                  "as often, all the way to the cap",
                  top["lock"] > sh["lock"] * 3
                  and top["fires"] > one["fires"] * 4,
                  f"lock {ctl['lock']:.1%} with no channel → {sh['lock']:.1%} "
                  f"shipped → {one['lock']:.1%} at one stack → "
                  f"{top['lock']:.1%} at {H['maxStacks']}; fires "
                  f"{one['fires']:.2f}/s → {top['fires']:.2f}/s")
            check("HEX IS A DEFENSIVE CHANNEL ON THIS TYPE — the lock is worth "
                  "more in blows the foe does not land than in blows this "
                  "relic does",
                  abs(sh["netTaken"]) > abs(sh["net"]),
                  f"shipped hex takes damage taken {baseTaken:.2f} → "
                  f"{sh['taken']:.2f}/s ({sh['netTaken']:+.1%}) while moving "
                  f"damage dealt {sh['net']:+.1%}; the foe lands "
                  f"{ctl['foeHps']:.3f}/s against {sh['foeHps']:.3f}/s")
            rungs = [hx_rows[f"pinned at {k}"] for k in range(1, H["maxStacks"] + 1)]
            monoF = all(rungs[i + 1]["foeHps"] < rungs[i]["foeHps"]
                        for i in range(len(rungs) - 1))
            monoT = all(rungs[i + 1]["taken"] < rungs[i]["taken"]
                        for i in range(len(rungs) - 1))
            # The bottom two rungs are one lock every 1.28s against one every
            # 0.64s and they are not separable at this sample size; the top
            # three are. The claim is made where the evidence is.
            topBot = all(r["foeHps"] < min(rungs[0]["foeHps"], rungs[1]["foeHps"])
                         for r in rungs[2:]) and \
                     all(r["foeHps"] < ctl["foeHps"] for r in rungs)
            check("AND IT PAYS ALL THE WAY TO THE CAP — but in the defensive "
                  "column, which is the one that is monotone rung by rung",
                  topBot and rungs[-1]["taken"] < rungs[0]["taken"] * 0.75,
                  "foe blows " + " → ".join(f"{r['foeHps']:.3f}" for r in rungs)
                  + f" (from {ctl['foeHps']:.3f} with no channel), taken "
                  + " → ".join(f"{r['taken']:.2f}" for r in rungs)
                  + (" — monotone" if monoT else " — with one inversion, left "
                     "visible rather than smoothed: rungs 1 and 2 are not "
                     "separable at this sample size and the claim is made on "
                     "3-5, which are")
                  + f" (from {ctl['taken']:.2f}). Damage DEALT does not order "
                  "itself: " + " ".join(f"{r['net']:+.0%}" for r in rungs) + " — "
                  f"the lock does not make this weapon swing faster, it stops "
                  f"the other one")
            check("so the cell's ultimate has a measured target and it is not "
                  "the one the cell was chosen on",
                  top["foeHps"] < ctl["foeHps"] * 0.5,
                  f"at the cap the foe lands {top['foeHps'] / ctl['foeHps'] - 1:+.0%} "
                  f"of the blows it lands against no channel at all and deals "
                  f"{top['taken'] / ctl['taken'] - 1:+.0%} of the damage. "
                  f"`5x the lock` is real — 86% against 29% — and what it buys "
                  f"is the foe not swinging, not this relic swinging more")
            out["hex"] = hx_rows

        # ---------------------------------------------------------- [7] --
        if "7" in want:
            t = page.evaluate(TRAP_JS)
            print(f"\n[7] THE TRAPS\n")
            check("`chain` is the only mode whose branch runs during a stun",
                  t["chainBeforeStunGuard"] and t["stunGuardText"],
                  "every other mode is behind `else if (f.stun > 0){ /* weapon "
                  "locked */ }`")
            check("a stunned fighter still lands no blows — the head moves, it "
                  "does not hit", t["hitsSkipOnStun"],
                  "tickHits skips on self.stun > 0")
            check("no flail carries a `shot` field — v39 od 4 is still live",
                  not t["flailHasShot"],
                  "tickFire gates on the FIELD, not on the mode: a shot left on "
                  "a melee weapon fires a bow at cadence forever")
            check("hex is one of the three TRUE stuns that break a wind-up",
                  t["hexIsTrueStun"] == ST["hex"]["stunFor"],
                  f"{t['hexIsTrueStun']:g}s, and Bloodmill lives on this type")
            out["traps"] = t

    if errors:
        print("\n!! page errors:")
        for e in errors[:10]:
            print("   ", e)

    bad = [n for n, ok in PASS if not ok]
    print(f"\n{len(PASS) - len(bad)}/{len(PASS)} checks passed")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad and not errors else 1


if __name__ == "__main__":
    sys.exit(main())
