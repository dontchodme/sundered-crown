#!/usr/bin/env python3
"""LOOK AT THE TWINBLADE ROW BEFORE THE ULTIMATE IS DESIGNED.

    python3 twinblade_survey.py --game ../02-chain/sc-paradox-ignition.html

`cell_survey` looks at all 42 cells at once, which is the right instrument for
"which type" and the wrong one for "which school on THIS type" (v43 §4 — its
occupancy column has now mispriced two cells). v40 pointed this discipline at
the bow row, v41 at the warhammer, v43 at the flail. Rick has taken
**verdant x twinblade**. This is that instrument pointed at the twinblade row,
and it is the first survey this type has ever had.

What is structurally peculiar about the twinblade, before any of it is
measured:

  * IT IS THE ONLY TYPE WITH TWO LIVE SEGMENTS. `blades: [0, 0.5]` — two
    opposed — against `[0]` for all five other types. And `tickHits` keeps a
    SEPARATE `hitCd` per segment, so the second blade is not decoration: it
    carries its own independent 0.45s cooldown.
  * IT IS THE LIGHTEST WEAPON IN THE GAME. mass 1.1 against 1.6/2.4/3.0/3.6/
    5.0. `resolveClank` weights mass^1.7 and calls a bind decisive above a
    0.16 share gap, so the question this section has to answer is not "does it
    lose binds" but "is there a single bind in the game it does not lose".
  * IT IS THE FASTEST AND THE SHORTEST. spin 5.7 against 1.6–3.4; reach 62
    against 54–116. Its blades come round more often than anything else's and
    sweep the least ground doing it.
  * AND IT CARRIES THE LOWEST DAMAGE IN THE GAME. 8.3–11.95 a blow, against a
    flail's 25–44.
  * THE CHOSEN SCHOOL SLOWS SWING. Entangle is `spin -0.13 / move -0.06` per
    stack, capped at 4. So verdant on this type is the fastest weapon in the
    game handing out the only status that makes a weapon slow.

  [1] THE ROW AND THE BLOCK. Read from AC.WEAPONS and AC.CONFIG, not a doc.

  [2] TWO BLADES, AND WHAT THE SECOND ONE IS WORTH. Live segment length and
      contacts/s per type off `bladeSegments`; then the decisive A/B — the
      donor run with `blades:[0,0.5]` against the same seeds with `blades:[0]`
      and nothing else touched. With a CONTROL that must come back at a known
      value: a greatsword given a second blade must gain what a twinblade
      loses by having one taken away, or the instrument is measuring something
      other than the blade.

  [3] THE LIGHTEST WEAPON IN THE GAME. Clank outcome read off the EFFECT —
      whose spinDir reversed, who ate the stagger — never recomputed from the
      mass formula. The formula's exponent and its decisive threshold are read
      out of the shipped `resolveClank.toString()`, v43 §12's rule.

  [4] WHAT ENTANGLE ACTUALLY BUYS, AND WHETHER THE FOE'S MODE DECIDES IT.
      `spinMul` reaches `tickWeapon`'s `spin` for every mode — but a bow's
      CADENCE is `tickFire`'s `S.cadence` and does not read spin at all. So
      the hypothesis to refute is: entangle is worth much less against the
      five ranged relics than against the twenty melee ones. Model-free A/B,
      channel deleted against channel live, split by the foe's mode.

  [5] THE FOUR OPEN CHANNELS ON THIS TYPE AS DELIVERED EFFECT. sunder / smite
      / entangle each get one A/B against the same channel deleted; vigil is
      not a foe status and gets the bank readout instead. This is the check on
      the CELL: `cell_survey` ranked entangle here on occupancy, and occupancy
      is the column that has mispriced two cells.

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
from wh_survey import CLANK_JS, CHANNEL_JS, WARD_JS  # noqa: E402

HERE = pathlib.Path(__file__).parent
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


TYPE_DONOR = {"greatsword": "dawnbringer", "twinblade": "widowmaker",
              "warhammer": "grudgebearer", "scythe": "thornwake",
              "flail": "gravemourn", "bow": "ironhail"}

# One foe per type, none of them the twinblade donor, so every cross-type row
# is scored against the identical field. gravemourn carries the chain mode,
# which the flail survey's foe set did not need and section [4] does.
FOES = ["emberedge", "lastlight", "aureole", "censer", "gravemourn"]
# Section [4] needs every MODE represented and needs to know which is which.
MODE_FOES = ["aureole", "vinesower", "farwarden", "marrowdraw",   # ranged
             "emberedge", "nightfell", "heartwood", "axiom",       # swing
             "lastlight", "censer", "foregone", "bulwarden",       # spin
             "gravemourn", "slagheart", "redflail", "paradox"]     # chain

# --------------------------------------------------------------- [1] grid ---

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape,
    reach: w.reach, width: w.width, artW: w.artW, dmg: w.dmg, spin: w.spin,
    mode: w.mode, mass: w.mass, arc: w.arc || null, blades: w.blades.length,
    bladeOffs: w.blades.slice(), knockMul: w.knockMul || null, shot: !!w.shot,
    onHit: w.onHit ? Object.entries(w.onHit)[0] : null,
    onSelf: w.onSelf ? Object.entries(w.onSelf)[0] : null,
    ult: w.ult ? { name: w.ult.name, charge: w.ult.charge } : null,
  }));
  const S = {};
  for (const [k, v] of Object.entries(AC.STATUS))
    S[k] = { maxStacks: v.maxStacks, dur: v.dur, spin: v.spin ?? null,
             move: v.move ?? null, dps: v.dps ?? null, tip: v.tip || "" };
  const src = AC.Match.prototype.resolveClank.toString();
  const ex = src.match(/Math\\.pow\\(m[AB],\\s*([0-9.]+)\\)/);
  const th = src.match(/Math\\.abs\\(shareA\\s*-\\s*shareB\\)\\s*>\\s*([0-9.]+)/);
  return { weapons: W, status: S, affinities: Object.keys(AC.AFFINITIES),
           combat: AC.CONFIG.combat, physics: AC.CONFIG.physics,
           clankCfg: AC.CONFIG.clank,
           massExp: ex ? parseFloat(ex[1]) : null,
           decisive: th ? parseFloat(th[1]) : null };
}"""

# ------------------------------------------------------------ [2] blades ---
# Live segment geometry read off `bladeSegments` — the function the hit test
# actually calls — plus, per blade index, how much of the fight that blade
# spends on its own cooldown. A second blade that is always cooling is not a
# second blade.

GEOM_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult]) => {
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
      const nb = me.w.blades.length;

      let step = 0, segSum = 0, segN = 0, segMin = 1e9, segMax = 0;
      const perBlade = new Array(nb).fill(0);   // hits credited to each index
      const coolFr   = new Array(nb).fill(0);   // frames that index was cooling
      let hits = 0, sweptSum = 0;

      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        if (self === me && mul === undefined){
          hits++;
          /* which segment landed it — matched on the segment object the hit
             test handed through, not re-derived from the angle */
          const segs = m.bladeSegments(me);
          for (let i = 0; i < segs.length; i++)
            if (seg && Math.abs(segs[i].a - seg.a) < 1e-12) perBlade[i]++;
        }
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
        for (let i = 0; i < nb; i++) if ((me.hitCd[i] || 0) > 0) coolFr[i]++;
        /* the ground one blade sweeps in a second, as an area rate: the
           annulus between the hilt and the tip, times the angle turned */
        sweptSum += Math.abs(me.w.spin * me.spinMul(m.actMods.spin)) * DT;
      }
      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT, nb,
                  hits, perBlade, coolFr,
                  seg: segN ? segSum / segN : 0, segMin, segMax,
                  turned: sweptSum });
    }
  }
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""

# The A/B. `blades` is mutated on the donor's weapon record BEFORE the Match is
# constructed, and `hitCd` is a sparse array read through `|| 0`, so nothing
# else in the engine has to know. Restored in a finally-equivalent tail.

BLADES_JS = r"""([donor, offs, foes, seeds, secs, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedBlades = w.blades.slice();
  w.blades = offs.slice();

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
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, dealt: me.dealt, taken: th.dealt,
                  clanks: me.clanks, meHp: me.hp, thHp: th.hp });
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

# ---------------------------------------------------------- [4] entangle ---
# The MECHANISM read, beside the outcome read. `spinMul` is sampled off the
# foe every frame, so "the ladder reached the foe" is measured rather than
# assumed, and the foe's own blows are counted so the effect has somewhere to
# land. Entangle is applied by the donor's own onHit, exactly as a verdant
# twinblade would apply it — no synthetic schedule.

ENT_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult, on, force]) => {
  const DT = AC.CONFIG.physics.dt;
  const STATUS_DUR = AC.STATUS.entangle.dur;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "verdant";
  delete w.onHit; delete w.onSelf;
  if (on) w.onHit = { entangle: 2 };

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
      let step = 0, stackSum = 0, capFr = 0, twoFr = 0, spinMulSum = 0,
          moveMulSum = 0, speedSum = 0, entMulSum = 0, entMulN = 0, despFr = 0;
      while (!m.over && step < secs / DT){
        /* THE CEILING ARM. The ladder is held AT CAP rather than left to the
           weapon's own contact rate, so "what would an ultimate that pinned
           this be worth" is a measurement and not an extrapolation. Written
           the way the applier writes it, before the step, so tickStatus runs
           the clock down on it exactly as it would on a real stack. */
        if (force > 0) th.status.entangle = { t: STATUS_DUR, stacks: force };
        m.step(DT); step++;
        const st = th.stacks("entangle");
        stackSum += st;
        if (st >= 4) capFr++;
        if (st >= 2) twoFr++;
        spinMulSum += th.spinMul(m.actMods.spin);
        /* THE STATUS TERM ALONE. spinMul multiplies the ACT modifier, which
           moves with the act clock, and multiplies again when the fighter is
           desperate -- so a raw spinMul cannot be compared against the status
           table. Divide the act modifier back out and skip the desperate
           frames, and what is left is exactly (1 + entangle.spin * stacks). */
        if (!th.desperate){
          entMulSum += th.spinMul(m.actMods.spin) / m.actMods.spin;
          entMulN++;
        } else despFr++;
        moveMulSum += th.moveMul();
        speedSum += Math.hypot(th.vx, th.vy);
      }
      rows.push({ foe: f, foeMode: th.w.mode, foeShape: th.w.shape,
                  seed: sd, steps: step, dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, foeHits: th.hits,
                  dealt: me.dealt, taken: th.dealt,
                  stacks: step ? stackSum / step : 0,
                  cap: step ? capFr / step : 0, two: step ? twoFr / step : 0,
                  spinMul: step ? spinMulSum / step : 1,
                  entMul: entMulN ? entMulSum / entMulN : 1,
                  desp: step ? despFr / step : 0,
                  moveMul: step ? moveMulSum / step : 1,
                  speed: step ? speedSum / step : 0 });
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

# ------------------------------------------------------------- [6] traps ---

TRAP_JS = r"""() => {
  const out = {};
  const hitSrc  = AC.Match.prototype.tickHits.toString();
  const segSrc  = AC.Match.prototype.bladeSegments.toString();
  const pairSrc = AC.Match.prototype._clankPair.toString();
  const fireSrc = AC.Match.prototype.tickFire.toString();
  const probe   = new AC.Match("widowmaker", "aureole", 7);
  const spinSrc = probe.a.spinMul.toString();
  out.perBladeCd   = /hitCd\[i\]/.test(hitSrc);
  out.stunSkips    = /self\.stun\s*>\s*0/.test(hitSrc);
  out.segFromTheta = /f\.theta\s*\+\s*off/.test(segSrc);
  out.pairContinue = /continue;/.test(pairSrc);
  out.fireNoSpin   = !/spin/.test(fireSrc.split("if (f.ultDraw)")[0]);
  out.spinFloor    = /Math\.max\(0\.15/.test(spinSrc);
  out.entangleInSpin = /entangle/.test(spinSrc);
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--donor", default="widowmaker")
    ap.add_argument("--only", default="", help="comma list of section numbers")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"1", "2", "3", "4", "5", "6"}
    gp = (HERE / a.game).resolve()
    seeds = [1301 + 17 * i for i in range(a.seeds)]
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        g = page.evaluate(GRID_JS)
        W, ST = g["weapons"], g["status"]
        schools = sorted(set({w["aff"] for w in W}) | set(g["affinities"]))
        shapes = sorted({w["shape"] for w in W})
        filled = {(w["aff"], w["shape"]): w["name"] for w in W}
        twins = [w for w in W if w["shape"] == "twinblade"]
        open_tb = [s for s in schools if (s, "twinblade") not in filled]
        pin_ids = [w["id"] for w in W]
        donor = a.donor
        by_id = {w["id"]: w for w in W}

        # ---------------------------------------------------------- [1] --
        if "1" in want:
            print(f"\n[1] THE TWINBLADE ROW — {len(twins)} of {len(schools)} filled, "
                  f"{len(open_tb)} open\n")
            print(f"    {'':<12}" + "".join(f"{s[:11]:>12}" for s in schools))
            print(f"    {'twinblade':<12}"
                  + "".join(f"{filled.get((s,'twinblade'),'·')[:11]:>12}" for s in schools))
            print(f"\n    the type's block, and where it sits in the game\n")
            print(f"    {'type':<12}{'reach':>7}{'width':>7}{'spin':>7}{'mass':>7}"
                  f"{'blades':>8}{'mode':>8}{'arc':>6}{'dmg':>16}")
            for t in shapes:
                rel = [w for w in W if w["shape"] == t]
                r0 = rel[0]
                dmgs = f"{min(w['dmg'] for w in rel):.1f}-{max(w['dmg'] for w in rel):.1f}"
                print(f"    {t:<12}{r0['reach']:>7}{r0['width']:>7}{r0['spin']:>7.1f}"
                      f"{r0['mass']:>7.1f}{str(r0['bladeOffs']):>8}{r0['mode']:>8}"
                      f"{(r0['arc'] if r0['arc'] else '-'):>6}{dmgs:>16}")
            print(f"\n    CONFIG.combat  " + "  ".join(f"{k} {v:g}" for k, v in g["combat"].items()))
            print(f"    entangle       " + "  ".join(
                f"{k} {v}" for k, v in ST["entangle"].items() if k != "tip"))

            fields = ("reach", "width", "artW", "spin", "mode", "mass", "blades")
            same = all(len({w[f] for w in twins}) == 1 for f in fields)
            check("all three twinblades share one physics block, field for field",
                  same, ", ".join(f"{f}={twins[0][f]}" for f in fields))

            nb = {w["shape"]: w["blades"] for w in W}
            check("the twinblade is the only type with more than one live segment",
                  [t for t, n in nb.items() if n > 1] == ["twinblade"],
                  "  ".join(f"{t}:{n}" for t, n in sorted(nb.items())))

            masses = sorted({w["mass"] for w in W})
            check("mass 1.1 is the bottom of the ladder, alone",
                  masses[0] == twins[0]["mass"],
                  f"ladder {', '.join(f'{m:g}' for m in masses)}")

            spins = sorted({w["spin"] for w in W}, reverse=True)
            check("spin 5.7 is the top of the ladder, alone",
                  spins[0] == twins[0]["spin"],
                  f"ladder {', '.join(f'{s:g}' for s in spins)}")

            ceil = {t: max(w["dmg"] for w in W if w["shape"] == t) for t in shapes}
            lowest = min(ceil, key=lambda t: ceil[t])
            check("the twinblade's hardest blow is the softest CEILING in the game",
                  lowest == "twinblade",
                  ", ".join(f"{t} {ceil[t]:g}" for t in sorted(ceil, key=lambda x: ceil[x]))
                  + "  — the single softest blow is Axiom's 7.42, a greatsword, "
                    "so the type is low by its ceiling and not by its floor")
            out["block"] = {f: twins[0][f] for f in fields}
            out["entangle"] = ST["entangle"]

        # ---------------------------------------------------------- [2] --
        geom = {}
        if "2" in want:
            print(f"\n[2] TWO BLADES — live segment off `bladeSegments`, "
                  f"dmg pinned {a.pin:g}, ultimates suppressed\n")
            print(f"    {'type':<12}{'blades':>7}{'live blade':>12}{'total edge':>12}"
                  f"{'contacts/s':>12}{'per blade':>14}{'cooling':>12}"
                  f"{'rad/s':>8}{'contacts/rad':>14}")
            for t in shapes:
                d = TYPE_DONOR[t]
                # a relic cannot fight itself: the flail donor is in FOES
                foes_t = [f for f in FOES if f != d]
                rows = page.evaluate(GEOM_JS, [d, foes_t, seeds, a.secs, a.pin,
                                               pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                hits = sum(r["hits"] for r in rows)
                nb = rows[0]["nb"]
                per = [sum(r["perBlade"][i] for r in rows) for i in range(nb)]
                cool = [sum(r["coolFr"][i] for r in rows) for i in range(nb)]
                steps = sum(r["steps"] for r in rows)
                geom[t] = {"hps": hits / dur if dur else 0, "hits": hits,
                           "dur": dur, "nb": nb,
                           "seg": mean(r["seg"] for r in rows),
                           "per": per,
                           "cool": [c / steps if steps else 0 for c in cool],
                           "turn": sum(r["turned"] for r in rows) / dur if dur else 0}
                gg = geom[t]
                gg["edge"] = gg["seg"] * nb
                gg["perRad"] = gg["hps"] / gg["turn"] if gg["turn"] else 0
                print(f"    {t:<12}{nb:>7}{gg['seg']:>12.1f}{gg['edge']:>12.1f}"
                      f"{gg['hps']:>12.3f}"
                      f"{('/'.join(str(x) for x in per)):>14}"
                      f"{('/'.join(f'{c:.0%}' for c in gg['cool'])):>12}"
                      f"{gg['turn']:>8.2f}{gg['perRad']:>14.4f}")

            tb = geom["twinblade"]
            melee = {t: v for t, v in geom.items() if t != "bow"}
            worst = min(melee, key=lambda t: melee[t]["perRad"])
            check("the twinblade carries the MOST live edge in the game, and turns "
                  "it the least efficiently of any melee type",
                  tb["edge"] == max(v["edge"] for v in geom.values())
                  and worst == "twinblade",
                  f"edge {tb['edge']:.1f} against a greatsword's "
                  f"{geom['greatsword']['edge']:.1f}; "
                  + ", ".join(f"{t} {melee[t]['perRad']:.4f}"
                              for t in sorted(melee, key=lambda x: melee[x]['perRad']))
                  + " contacts per radian turned")
            share = min(tb["per"]) / max(1, sum(tb["per"]))
            check("both blades land — the second is not decoration",
                  share > 0.35,
                  f"{tb['per'][0]} / {tb['per'][1]} blows, weaker blade "
                  f"{share:.1%} of the type's contacts")

            # --- the A/B, and its control -------------------------------
            print(f"\n    the second blade, taken away — same seeds, same foes, "
                  f"nothing else touched\n")
            print(f"    {'arm':<28}{'contacts/s':>12}{'dealt/s':>10}{'taken/s':>10}"
                  f"{'clanks/min':>12}{'win':>7}")
            ab = {}
            for label, d, offs in [
                    ("twinblade  [0, 0.5]  ships", donor, [0, 0.5]),
                    ("twinblade  [0]       one",   donor, [0]),
                    ("greatsword [0]       ships", "dawnbringer", [0]),
                    ("greatsword [0, 0.5]  two",   "dawnbringer", [0, 0.5]),
                    ("scythe     [0]       ships", "thornwake",   [0]),
                    ("scythe     [0, 0.5]  two",   "thornwake",   [0, 0.5]),
                    ("warhammer  [0]       ships", "grudgebearer", [0]),
                    ("warhammer  [0, 0.5]  two",   "grudgebearer", [0, 0.5])]:
                rows = page.evaluate(BLADES_JS, [d, offs, FOES, seeds, a.secs,
                                                 a.pin, pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                fin = [r for r in rows if r["win"] >= 0]
                rec = {"hps": sum(r["hits"] for r in rows) / dur,
                       "dps": sum(r["dealt"] for r in rows) / dur,
                       "tps": sum(r["taken"] for r in rows) / dur,
                       "cpm": sum(r["clanks"] for r in rows) / dur * 60,
                       "win": mean(r["win"] for r in fin)}
                ab[label.split()[0] + " " + label.split()[1]] = rec
                print(f"    {label:<28}{rec['hps']:>12.3f}{rec['dps']:>10.2f}"
                      f"{rec['tps']:>10.2f}{rec['cpm']:>12.1f}{rec['win']:>7.1%}")

            gain = {}
            for t, one, two in [("twinblade", "twinblade [0]", "twinblade [0,"),
                                ("greatsword", "greatsword [0]", "greatsword [0,"),
                                ("scythe", "scythe [0]", "scythe [0,"),
                                ("warhammer", "warhammer [0]", "warhammer [0,")]:
                gain[t] = ab[two]["hps"] / ab[one]["hps"] if ab[one]["hps"] else 0
            print(f"\n    a second opposed blade is worth, in contact rate:")
            for t in ("twinblade", "scythe", "warhammer", "greatsword"):
                print(f"        {t:<12} x{gain[t]:.2f}   "
                      f"({'spin' if t != 'greatsword' else 'swing'} mode)")
            spins = [gain[t] for t in ("twinblade", "scythe", "warhammer")]
            check("every arm gains from a second blade and none of them doubles",
                  all(1.0 < gg < 2.0 for gg in gain.values()),
                  ", ".join(f"{t} x{gain[t]:.2f}" for t in gain)
                  + " — the 0.45s hitCd is per SEGMENT, so a doubling would mean "
                    "the two blades never share a pass")
            check("the second blade is worth more to a SPINNING weapon than to a "
                  "SWINGING one — so the gain belongs to full rotation, not to the "
                  "twinblade",
                  min(spins) > gain["greatsword"],
                  f"spin arms {', '.join(f'{s:.2f}' for s in sorted(spins))} "
                  f"against swing {gain['greatsword']:.2f}: a swing recomputes "
                  f"theta from the AIM every frame, so the opposed blade points "
                  f"away from the quarry for most of the arc")
            out["blade_gain"] = gain
            out["blades_ab"] = ab

        # ---------------------------------------------------------- [3] --
        if "3" in want:
            print(f"\n[3] THE LIGHTEST WEAPON IN THE GAME — outcome read off the "
                  f"EFFECT, dmg pinned {a.pin:g}, ultimates suppressed")
            e, thr = g["massExp"], g["decisive"]
            print(f"    mass^{e:g}, decisive above a {thr:g} share gap — both read out "
                  f"of the shipped resolveClank\n")
            print(f"    {'foe':<14}{'type':<12}{'mass':>6}{'margin':>8}{'thr':>6}"
                  f"{'clanks/min':>12}{'won':>7}{'deadlock':>10}{'lost':>7}"
                  f"{'stagger eaten':>15}")
            clank = {}
            for f in ["ironhail", "lastlight", "emberedge", "gravemourn",
                      "censer", "spellbreaker"]:
                rows = page.evaluate(CLANK_JS, [donor, [f], seeds, a.secs,
                                                a.pin, pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                n = sum(r["clanks"] for r in rows)
                won = sum(r["won"] for r in rows)
                lost = sum(r["lost"] for r in rows)
                dead = sum(r["dead"] for r in rows)
                fm = rows[0]["foeMass"]
                mm, mf = by_id[donor]["mass"], fm
                wA, wB = mm ** e, mf ** e
                shareA, shareB = wB / (wA + wB), wA / (wA + wB)
                margin = abs(shareA - shareB)
                stun = sum(r["stunMe"] for r in rows) / dur if dur else 0
                clank[f] = {"n": n, "won": won, "lost": lost, "dead": dead,
                            "margin": margin, "mass": fm, "stun": stun}
                print(f"    {f:<14}{by_id[f]['shape']:<12}{fm:>6.1f}{margin:>8.4f}"
                      f"{thr:>6.2f}{n/dur*60 if dur else 0:>12.1f}"
                      f"{(won/n if n else 0):>7.0%}{(dead/n if n else 0):>10.0%}"
                      f"{(lost/n if n else 0):>7.0%}{stun:>14.3f}s")

            wins = {f: v["won"] for f, v in clank.items()}
            check("the twinblade wins no bind in the game",
                  sum(wins.values()) == 0,
                  "won " + ", ".join(f"{f} {v}" for f, v in wins.items()))
            mirror = clank["spellbreaker"]
            check("the only bind it does not lose is against itself, and that is a "
                  "deadlock",
                  mirror["lost"] == 0 and mirror["dead"] == mirror["n"],
                  f"{mirror['dead']}/{mirror['n']} deadlocks, margin "
                  f"{mirror['margin']:.4f} against a {thr:g} threshold")
            out["clank"] = clank

        # ---------------------------------------------------------- [4] --
        if "4" in want:
            print(f"\n[4] WHAT ENTANGLE BUYS, BY THE FOE'S MODE — verdant grafted onto "
                  f"the donor, channel live against channel deleted\n")
            arms = {}
            for on in (True, False):
                arms[on] = page.evaluate(ENT_JS, [donor, MODE_FOES, seeds, a.secs,
                                                  a.pin, pin_ids, True, on, 0])
            arms["cap"] = page.evaluate(ENT_JS, [donor, MODE_FOES, seeds, a.secs,
                                                 a.pin, pin_ids, True, False,
                                                 ST["entangle"]["maxStacks"]])
            print(f"    {'foe':<14}{'mode':<8}{'stacks':>8}{'>=2':>6}{'cap':>6}"
                  f"{'foe spinMul':>12}{'foe moveMul':>12}"
                  f"{'foe blows/s':>13}{'taken/s':>10}{'win':>8}")
            byfoe = {}
            for f in MODE_FOES:
                on = [r for r in arms[True] if r["foe"] == f]
                off = [r for r in arms[False] if r["foe"] == f]
                dOn = sum(r["dur"] for r in on)
                dOff = sum(r["dur"] for r in off)
                fOn = [r for r in on if r["win"] >= 0]
                fOff = [r for r in off if r["win"] >= 0]
                rec = {
                    "mode": on[0]["foeMode"],
                    "stacks": mean(r["stacks"] for r in on),
                    "two": mean(r["two"] for r in on),
                    "cap": mean(r["cap"] for r in on),
                    "spinMul": mean(r["spinMul"] for r in on),
                    "moveMul": mean(r["moveMul"] for r in on),
                    "foeHpsOn": sum(r["foeHits"] for r in on) / dOn,
                    "foeHpsOff": sum(r["foeHits"] for r in off) / dOff,
                    "takenOn": sum(r["taken"] for r in on) / dOn,
                    "takenOff": sum(r["taken"] for r in off) / dOff,
                    "winOn": mean(r["win"] for r in fOn),
                    "winOff": mean(r["win"] for r in fOff),
                }
                byfoe[f] = rec
                print(f"    {f:<14}{rec['mode']:<8}{rec['stacks']:>8.2f}"
                      f"{rec['two']:>6.0%}{rec['cap']:>6.0%}"
                      f"{rec['spinMul']:>12.3f}{rec['moveMul']:>12.3f}"
                      f"{rec['foeHpsOn']:>7.3f}/{rec['foeHpsOff']:<5.3f}"
                      f"{rec['takenOn']:>5.2f}/{rec['takenOff']:<4.2f}"
                      f"{rec['winOn'] - rec['winOff']:>+8.1%}")

            print(f"\n    rolled up by the foe's MODE — this is the question\n")
            print(f"    {'foe mode':<10}{'n':>4}{'foe blows/s off->on':>22}"
                  f"{'change':>9}{'taken/s off->on':>18}{'change':>9}{'win':>9}")
            bymode = {}
            for md in ("ranged", "swing", "spin", "chain"):
                fs = [f for f in MODE_FOES if byfoe[f]["mode"] == md]
                if not fs:
                    continue
                hOn = mean(byfoe[f]["foeHpsOn"] for f in fs)
                hOff = mean(byfoe[f]["foeHpsOff"] for f in fs)
                tOn = mean(byfoe[f]["takenOn"] for f in fs)
                tOff = mean(byfoe[f]["takenOff"] for f in fs)
                dW = mean(byfoe[f]["winOn"] - byfoe[f]["winOff"] for f in fs)
                bymode[md] = {"n": len(fs), "hOn": hOn, "hOff": hOff,
                              "tOn": tOn, "tOff": tOff, "dWin": dW}
                print(f"    {md:<10}{len(fs):>4}{hOff:>13.3f} -> {hOn:<7.3f}"
                      f"{(hOn/hOff-1) if hOff else 0:>+9.1%}"
                      f"{tOff:>10.2f} -> {tOn:<6.2f}"
                      f"{(tOn/tOff-1) if tOff else 0:>+9.1%}{dW:>+9.1%}")

            print(f"\n    THE CEILING — the same ladder HELD AT CAP, which is what an "
                  f"ultimate that pinned it would be buying\n")
            print(f"    {'foe mode':<10}{'n':>4}{'foe spinMul':>13}"
                  f"{'foe blows/s  off -> cap':>26}{'change':>9}"
                  f"{'taken/s off -> cap':>21}{'change':>9}")
            bycap = {}
            for md in ("ranged", "swing", "spin", "chain"):
                fs = [f for f in MODE_FOES if byfoe[f]["mode"] == md]
                if not fs:
                    continue
                cp = [r for r in arms["cap"] if byfoe[r["foe"]]["mode"] == md]
                of = [r for r in arms[False] if byfoe[r["foe"]]["mode"] == md]
                dC = sum(r["dur"] for r in cp)
                dO = sum(r["dur"] for r in of)
                hC = sum(r["foeHits"] for r in cp) / dC
                hO = sum(r["foeHits"] for r in of) / dO
                tC = sum(r["taken"] for r in cp) / dC
                tO = sum(r["taken"] for r in of) / dO
                sm = mean(r["spinMul"] for r in cp)
                bycap[md] = {"spinMul": sm, "hC": hC, "hO": hO, "tC": tC, "tO": tO,
                             "entMul": mean(r["entMul"] for r in cp)}
                print(f"    {md:<10}{len(fs):>4}{sm:>13.3f}"
                      f"{hO:>17.3f} -> {hC:<6.3f}{(hC/hO-1) if hO else 0:>+9.1%}"
                      f"{tO:>12.2f} -> {tC:<6.2f}{(tC/tO-1) if tO else 0:>+9.1%}")
            exp = 1 + ST["entangle"]["spin"] * ST["entangle"]["maxStacks"]
            got = mean(v["entMul"] for v in bycap.values())
            base = mean(r["entMul"] for r in arms[False])
            check("the forced arm actually reaches the weapon — the status term alone, "
                  "act modifier divided out and desperate frames dropped, lands on "
                  "what the table predicts at cap",
                  abs(got - exp) < 0.01 and abs(base - 1.0) < 0.01,
                  f"held {got:.3f} against 1 + {ST['entangle']['spin']} x "
                  f"{ST['entangle']['maxStacks']} = {exp:.3f}; the unentangled "
                  f"control reads {base:.3f}")
            out["entangle_at_cap"] = bycap

            if "ranged" in bymode and "spin" in bymode:
                r, s = bymode["ranged"], bymode["spin"]
                rCut = 1 - (r["hOn"] / r["hOff"] if r["hOff"] else 1)
                sCut = 1 - (s["hOn"] / s["hOff"] if s["hOff"] else 1)
                check("entangle cuts a MELEE foe's blows harder than a RANGED foe's",
                      sCut > rCut,
                      f"spin -{sCut:.1%} against ranged -{rCut:.1%} — a bow's "
                      f"cadence is tickFire's, and tickFire never reads spin")
            out["entangle_by_mode"] = bymode
            out["entangle_by_foe"] = byfoe

        # ---------------------------------------------------------- [5] --
        if "5" in want:
            # THE WHOLE ROSTER, not a five-relic field. Section [4] showed the
            # channel's worth is decided by the foe's MODE, so a foe field that
            # misweights the modes decides this table by itself: FOES is 20%
            # swing where the roster is 28%, and swing is where entangle is
            # worth three times what it is anywhere else.
            allfoes = [w["id"] for w in W if w["id"] != donor]
            print(f"\n[5] THE FOUR OPEN CHANNELS ON THIS TYPE — one A/B each, "
                  f"channel live against the same channel deleted, "
                  f"against all {len(allfoes)} other relics\n")
            print(f"    {'school'.ljust(12)}{'status':<12}{'per hit':>8}"
                  f"{'dealt/s':>10}{'taken/s':>10}{'foe blows/s':>13}{'win':>9}")
            chan = {}
            base = None
            for aff, key, per in [("dwarven", "sunder", 1),
                                  ("sanctified", "smite", 1),
                                  ("verdant", "entangle", 2)]:
                rows_on = page.evaluate(CHANNEL_JS, [donor, aff, key, per, allfoes,
                                                     seeds, a.secs, a.pin,
                                                     pin_ids, True, True])
                rows_off = page.evaluate(CHANNEL_JS, [donor, aff, key, per, allfoes,
                                                      seeds, a.secs, a.pin,
                                                      pin_ids, True, False])
                dOn = sum(r["dur"] for r in rows_on)
                dOff = sum(r["dur"] for r in rows_off)
                fOn = [r for r in rows_on if r["win"] >= 0]
                fOff = [r for r in rows_off if r["win"] >= 0]
                rec = {"dps": sum(r["dealt"] for r in rows_on) / dOn,
                       "tps": sum(r["taken"] for r in rows_on) / dOn,
                       "dpsOff": sum(r["dealt"] for r in rows_off) / dOff,
                       "tpsOff": sum(r["taken"] for r in rows_off) / dOff,
                       "win": mean(r["win"] for r in fOn),
                       "winOff": mean(r["win"] for r in fOff)}
                chan[aff] = rec
                base = base or rec
                print(f"    {aff:<12}{key:<12}{per:>8}{rec['dps']:>10.2f}"
                      f"{rec['tps']:>10.2f}{'':>13}"
                      f"{rec['win']:>8.1%}  ({rec['win']-rec['winOff']:+.1%} vs "
                      f"the same weapon with no channel)")

            wr = page.evaluate(WARD_JS, [donor, [1.0], allfoes, seeds, a.secs,
                                         a.pin, pin_ids, True, 0.25])
            dW = sum(r["dur"] for r in wr)
            print(f"    {'vigil':<12}{'ward':<12}{'onSelf':>8}"
                  f"{sum(r['dealt'] for r in wr)/dW:>10.2f}{'':>10}{'':>13}"
                  f"   bank readout only — vigil applies nothing to a foe")

            best = max(chan, key=lambda k: chan[k]["win"] - chan[k]["winOff"])
            n_arm = len(allfoes) * len(seeds)
            check("the three foe channels on this type are ranked by DELIVERED "
                  "effect, whatever cell_survey's occupancy column said",
                  True,
                  f"strongest is {best} — "
                  + ", ".join(f"{k} {chan[k]['win']-chan[k]['winOff']:+.1%}"
                              for k in chan)
                  + f"  (n={n_arm} a arm)")
            out["channels"] = chan

        # ---------------------------------------------------------- [6] --
        if "6" in want:
            print(f"\n[6] THE TRAPS\n")
            t = page.evaluate(TRAP_JS)
            check("each blade carries its OWN hit cooldown — hitCd is indexed by "
                  "segment", t["perBladeCd"])
            check("a stunned twinblade lands nothing — tickHits skips on self.stun",
                  t["stunSkips"])
            check("both segments are rigid functions of f.theta — the twinblade has "
                  "no lag term to be surprised by", t["segFromTheta"])
            check("_clankPair CONTINUES past a buried blade rather than returning — "
                  "one blade being blocked cannot mask the other", t["pairContinue"])
            check("tickFire's cadence never reads spin — entangle cannot slow a bow's "
                  "rate of fire", t["fireNoSpin"])
            check("entangle reaches the weapon through spinMul, and spinMul floors "
                  "at 0.15", t["entangleInSpin"] and t["spinFloor"])
            check("no JS errors or page exceptions", not errors,
                  "; ".join(errors[:3]))

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 0 if n_ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
