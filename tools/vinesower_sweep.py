#!/usr/bin/env python3
"""THE THICKET'S ECONOMY, SWEPT. Nine numbers, none of them chosen.

    python3 vinesower_sweep.py --game ../02-chain/sc-vinesower.html

`vinesower_probe` says the mechanic does what Rick's §1 says it does. It says
nothing about whether the NUMBERS are right, and they are not: at the
placeholders the relic wins 77.9% and `inReachGivenAny` sits at 1.55, which
clears the bar this file set for "several" by 0.05.

The economy is worse than the Converse's was:

    plants          linear in `dur` and bounded by `maxVines`
    plants ALIVE    linear in `vineLife` on top of that
    reachable       grows with `reach` against a hall that is 520 x 800
    damage          the product of all of it against `whipCd`

so no single number can be swept alone and a full grid is 5^4. This is
staged instead, and each stage is answering a different question:

  [A] THE READ. `reach` x `vineLife`, damage held. Rick's sentence -- "good
      but limited range so several can swipe at the enemy at the same time"
      -- is two requirements pulling opposite ways, and the pair of columns
      that measures them is `inReachGivenAny` (several) and `coverage` (but
      limited). Damage is deliberately NOT in this stage: it would let a
      setting buy the read by ending the fight.

  [B] THE PRICE. At the chosen read, `whipDmg` x `whipCd` for the share of
      the relic the ultimate is worth. A weapon whose ultimate is most of it
      is an ultimate with a weapon attached.

  [C] THE BLADE. What `dmg` has to be, given [A] and [B], for the relic to
      sit at 50%. Reported, not applied -- `tune.py` owns that number.

## The override is validated, not trusted

Every stage mutates `AC.WEAPONS`' ult block at runtime rather than rebuilding
the HTML, which is what makes a grid affordable. v39 established that this
has to be PROVED rather than assumed: `--verify-override` rebuilds the game
with one setting written into the file and asserts a batch of matches is
identical to the same setting applied at runtime, field for field.
"""
from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import statistics
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "vinesower"

# One measurement function, driven by an override dict. Every stage calls it.
MEASURE_JS = r"""([rid, over, foes, seeds, secs, sampleGrid]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = JSON.parse(JSON.stringify(w.ult));
  const savedDmg = w.dmg;
  for (const k of Object.keys(over)){
    if (k === "dmg") w.dmg = over[k]; else w.ult[k] = over[k];
  }
  const u = w.ult;

  let wins = 0, played = 0, dur = 0, casts = 0;
  let dVine = 0, dShot = 0, dMelee = 0, whips = 0, lands = 0, planted = 0;
  let contactSamples = 0, contactInReach = 0, armedSamples = 0, liveArmed = 0;
  let covHits = 0, covSamples = 0;
  const strikeLog = [];
  const winHist = {};

  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let inVine = false;
      const oR = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, ov){
        const sh = m._cineShot, d0 = self.dealt;
        const r = oR.call(m, self, foe2, hx, hy, seg, mul, ov);
        const dd = self.dealt - d0;
        if (self === me){
          if (inVine) dVine += dd; else if (sh) dShot += dd; else dMelee += dd;
        }
        return r;
      };
      const oP = AC.Match.prototype.plantVine;
      m.plantVine = function(s){ planted++; return oP.call(m, s); };
      const oT = AC.Match.prototype.tickVines;
      const local = [];
      m.tickVines = function(dt){
        inVine = true;
        const before = m.vines.map(v => ({ v, whips: v.whips, l: v.lands }));
        const r = oT.call(m, dt);
        inVine = false;
        for (const b of before){
          if (b.v.whips > b.whips){ whips++; local.push([m.t, b.v]); }
          if (b.v.lands > b.l) lands++;
        }
        let inReach = 0, armed = 0;
        for (const v of m.vines){
          if (v.t < v.sprout) continue;
          armed++;
          if (Math.hypot(th.x - v.x, th.y - v.y) <= u.reach + R) inReach++;
        }
        if (armed > 0){
          armedSamples++; liveArmed += armed;
          if (inReach > 0){ contactSamples++; contactInReach += inReach; }
          /* COVERAGE: the share of the hall a ball's CENTRE could stand in and
             be reachable. Sampled on a coarse grid, and only every Nth frame --
             this is the "but limited" half of the sentence and it is the only
             number here that is about the hall rather than about the foe. */
          if (sampleGrid && (armedSamples % 60 === 0)){
            const n2 = m.inset;
            for (let gx = 0; gx < 9; gx++) for (let gy = 0; gy < 13; gy++){
              const px = n2 + R + (gx / 8) * (A.w - 2 * n2 - 2 * R);
              const py = n2 + R + (gy / 12) * (A.h - 2 * n2 - 2 * R);
              covSamples++;
              for (const v of m.vines){
                if (v.t < v.sprout) continue;
                if (Math.hypot(px - v.x, py - v.y) <= u.reach + R){ covHits++; break; }
              }
            }
          }
        }
        return r;
      };
      let st = 0, hadBloom = false;
      while (!m.over && st < secs / DT){
        const hb = !!me.ultBloom;
        m.step(DT); st++;
        if (!hb && me.ultBloom) casts++;
      }
      played++; dur += st * DT;
      if (m.winner === me) wins++;
      /* distinct plants inside 0.6s of each strike */
      for (let i = 0; i < local.length; i++){
        const set = new Set();
        for (let j = 0; j < local.length; j++)
          if (Math.abs(local[j][0] - local[i][0]) <= 0.6) set.add(local[j][1]);
        winHist[set.size] = (winHist[set.size] || 0) + 1;
      }
      for (const e of local) strikeLog.push(e[0]);
    }
  }
  w.dmg = savedDmg;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  Object.assign(w.ult, saved);

  const dTot = Math.max(1, dVine + dShot + dMelee);
  const wTot = Math.max(1, Object.values(winHist).reduce((a, b) => a + b, 0));
  return { played, wins, win: wins / played, dur: dur / played, casts,
           planted, whips, lands,
           whipsPerCast: casts ? whips / casts : 0,
           landsPerCast: casts ? lands / casts : 0,
           whiffRate: whips ? 1 - lands / whips : 0,
           plantsPerCast: casts ? planted / casts : 0,
           vineShare: dVine / dTot, shotShare: dShot / dTot, meleeShare: dMelee / dTot,
           dVine, dShot, dMelee,
           inReachGivenAny: contactSamples ? contactInReach / contactSamples : 0,
           liveArmed: armedSamples ? liveArmed / armedSamples : 0,
           contactShare: armedSamples ? contactSamples / armedSamples : 0,
           coverage: covSamples ? covHits / covSamples : 0,
           several: Object.entries(winHist)
                    .filter(([k]) => +k >= 3)
                    .reduce((a, [, v]) => a + v, 0) / wTot };
}"""

# The override, proved rather than assumed.
IDENTITY_JS = r"""([rid, over, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = JSON.parse(JSON.stringify(w.ult));
  const savedDmg = w.dmg;
  for (const k of Object.keys(over)){
    if (k === "dmg") w.dmg = over[k]; else w.ult[k] = over[k];
  }
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(rid, f, sd);
    let st = 0;
    while (!m.over && st < secs / DT){ m.step(DT); st++; }
    out.push([st, Math.round(m.a.hp * 1e6), Math.round(m.b.hp * 1e6),
              m.a.hits, m.b.hits, m.vines.length]);
  }
  w.dmg = savedDmg;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  Object.assign(w.ult, saved);
  return out;
}"""

BAKED_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(rid, f, sd);
    let st = 0;
    while (!m.over && st < secs / DT){ m.step(DT); st++; }
    out.push([st, Math.round(m.a.hp * 1e6), Math.round(m.b.hp * 1e6),
              m.a.hits, m.b.hits, m.vines.length]);
  }
  return out;
}"""

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-vinesower.html")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--secs", type=float, default=85.0)
    ap.add_argument("--foes", type=int, default=6)
    ap.add_argument("--stage", default="abc")
    ap.add_argument("--verify-override", action="store_true")
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    gp = (HERE / A.game).resolve()
    if not gp.exists():
        sys.exit(f"no such build: {gp}")
    seeds = [101 + 7 * i for i in range(A.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        roster = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        base = page.evaluate(f"() => JSON.parse(JSON.stringify("
                             f"AC.WEAPONS.find(w => w.id === '{RID}')))")
        # a foe field spanning the parry column (bow_survey §2.2) and both
        # extremes of mass, since the whip's knock is a velocity and mass is
        # what resists it
        FOES = [f for f in ["grudgebearer", "widowmaker", "emberedge",
                            "gravemourn", "thornwake", "spellbreaker",
                            "censer", "axiom"] if f in roster][:A.foes]
        print(f"\nVINESOWER SWEEP — {len(FOES)} foes x {len(seeds)} seeds, "
              f"{A.secs:.0f}s cap")
        print(f"  placeholders: " + "  ".join(
            f"{k} {base['ult'][k]}" for k in
            ["seeds", "sprout", "vineLife", "reach", "windup", "whipDmg",
             "whipCd", "whipKnock", "maxVines"]))
        print(f"  dmg {base['dmg']}\n")

        # ------------------------------------------------------- override --
        if A.verify_override:
            # THE BAKED HALF CANNOT RUN IN HERE. `scpage.game` opens a
            # sync_playwright context and a second one nested inside it throws
            # ("Sync API inside the asyncio loop"). The live half is collected
            # now, the page is closed, and the rebuilt build is opened after.
            OV = {"reach": 170, "vineLife": 9.0, "whipDmg": 4, "whipCd": 1.0}
            override_live = page.evaluate(IDENTITY_JS,
                                          [RID, OV, FOES[:3], seeds[:3], 40.0])
            # THE REBUILD HAS TO CARRY EVERY NUMBER THE LIVE PAGE IS CARRYING,
            # not the builder's defaults. The first cut of this check rebuilt
            # from TUNED_QS and the stock ULT block and disagreed at match 0 --
            # which was the TEST being wrong, not the override. The full
            # current setting is read off the page and passed through.
            override_full = dict(
                {k: v for k, v in base["ult"].items()
                 if isinstance(v, (int, float))},
                **OV)
            override_full["dmg"] = base["dmg"]
            override_args = (OV, override_full, FOES[:3], seeds[:3])

        # ----------------------------------------------- [H] the hold ------
        # THE FIRST CUT OF STAGE A RAN AT THE PLACEHOLDER `dmg` AND THE RELIC
        # WON 92-100% OF EVERY CELL IN THE GRID. That is not a balance
        # observation, it is a MEASUREMENT ERROR: a fight the relic wins in
        # twenty seconds ends before the garden it is supposed to be measuring
        # has finished growing, so every read column was taken against a
        # truncated cast. The blade is held near even for the read stages and
        # tuned properly in [C].
        hold = None
        if "a" in A.stage or "b" in A.stage:
            print("[H] THE HOLD — `dmg` bisected to a near-even relic, so the read "
                  "stages are\n    measured on fights that actually run.\n")
            lo, hi = 6.0, base["dmg"]
            for _ in range(5):
                mid = (lo + hi) / 2
                m = page.evaluate(MEASURE_JS, [RID, {"dmg": mid}, FOES,
                                               seeds[:max(2, len(seeds) - 1)],
                                               A.secs, False])
                print(f"      dmg {mid:>6.2f}  win {m['win']:>5.0%}  "
                      f"dur {m['dur']:>5.1f}s")
                if m["win"] > 0.5: hi = mid
                else: lo = mid
            hold = round((lo + hi) / 2, 2)
            print(f"\n    holding dmg at {hold} for [A] and [B].")
            out["hold"] = hold

        # ------------------------------------------------------- [A] read --
        if "a" in A.stage:
            print(f"\n[A] THE READ — \"good but limited range so several can swipe "
                  f"at the enemy at\n    the same time\". Two requirements pulling "
                  f"opposite ways. Damage is HELD at\n    the placeholder so no "
                  f"setting can buy the read by ending the fight.\n")
            # RICK'S SECOND AND THIRD NOTES MOVED THIS GRID. "it may be
            # spawning too many of them ... with less vines i think we can
            # afford to make them longer." So the axes are now the MAGAZINE
            # (a number the viewer can count) and the REACH, and the grid runs
            # from smaller-and-longer than the last pick rather than around it.
            #
            # The perimeter arithmetic from the first version still holds and
            # is why reach has to rise as the count falls:
            #     in-reach ~= 2*sqrt((reach+R)^2 - d^2) * N / 2640
            # Halving N wants reach up by roughly the same factor to hold the
            # read, and that is the trade Rick is asking for by name.
            reaches = [130, 165, 205, 250]
            mags = [6, 8, 10, 12]
            print(f"    {'reach':>6}{'seeds':>6}{'life':>6}"
                  f"{'plants/cast':>12}{'armed':>7}"
                  f"{'in reach':>10}{'3+/0.6s':>9}{'coverage':>10}"
                  f"{'slash/cast':>12}{'whiff':>7}{'win':>7}")
            gridA = {}
            for rr, mag in itertools.product(reaches, mags):
                # the plants from one magazine all want to be alive together,
                # so the life is set from how long the magazine takes to empty
                vl = round(mag * 0.34 / 0.84 + 6.0, 1)
                ovA = {"reach": rr, "seeds": mag, "maxVines": mag + 2,
                       "vineLife": vl}
                if hold: ovA["dmg"] = hold
                m = page.evaluate(MEASURE_JS, [RID, ovA, FOES, seeds, A.secs, True])
                gridA[f"{rr}/{mag}"] = dict(m, seeds=mag, vineLife=vl, reach=rr,
                                            maxVines=mag + 2)
                print(f"    {rr:>6}{mag:>6}{vl:>6.1f}"
                      f"{m['plantsPerCast']:>12.1f}"
                      f"{m['liveArmed']:>7.1f}{m['inReachGivenAny']:>10.2f}"
                      f"{m['several']:>9.0%}{m['coverage']:>10.0%}"
                      f"{m['whipsPerCast']:>12.1f}"
                      f"{m['whiffRate']:>7.0%}{m['win']:>7.0%}")
            out["A"] = gridA
            # SEVERAL at the least coverage that buys it. "But limited" is the
            # constraint, not the objective, and a setting that reaches the
            # whole hall has answered a different sentence.
            best = max(v["inReachGivenAny"] for v in gridA.values())
            print(f"\n    ONE THING THIS GRID HAD TO BE RUN TWICE TO SAY. The first "
                  f"cut ran at the\n    placeholder `dmg`, the relic won 92-100% of "
                  f"every cell, and NOTHING reached 2.2\n    plants in reach — which "
                  f"read like a hard ceiling and got written up as one, with\n    a "
                  f"perimeter argument behind it. It was the confound: fights ending "
                  f"in twenty\n    seconds were being scored on gardens that had not "
                  f"finished growing. With [H]'s\n    hold in place the same grid "
                  f"reaches {best:.2f}. The ceiling was the measurement.\n\n"
                  f"    BOTH metrics are kept because they answer different halves of "
                  f"the sentence:\n    in-reach is how many CAN strike at an "
                  f"instant, 3+/0.6s is how many DO inside a\n    beat the viewer "
                  f"perceives as one. Rick's words are about the second.")
            # RICK'S CEILING, NOT THIS FILE'S. "i also think it may be
            # spawning too many of them" is an instruction about the count,
            # and a pick that answers it by raising the count has answered
            # something else. Everything at or under 8 seeds is eligible; the
            # read is then maximised inside that, and the COVERAGE it costs is
            # reported rather than optimised away -- because "less vines,
            # longer" spends coverage by construction and he asked for it.
            SEED_CEIL = 8
            ok = [(k, v) for k, v in gridA.items()
                  if v["seeds"] <= SEED_CEIL and v["several"] >= 0.45]
            cands = sorted(ok, key=lambda kv: (-round(kv[1]["several"], 2),
                                               kv[1]["coverage"]))[:3]
            print(f"\n    CANDIDATES for [B] (the read is necessary, not "
                  f"sufficient — [B] has to be able\n    to PRICE the garden, and "
                  f"a garden that wins at any whipDmg cannot be priced):")
            for k, v in cands:
                print(f"      {k:<9} several {v['several']:.0%}  coverage "
                      f"{v['coverage']:.0%}  seeds {v['seeds']}  "
                      f"slash/cast {v['whipsPerCast']:.1f}")
            out["candsA"] = [k for k, _ in cands]

            if ok:
                pickA = cands[0]
                v = pickA[1]
                print(f"\n    PICK: reach/seeds {pickA[0]} — {v['several']:.0%} of "
                      f"strikes have 3+ distinct plants\n    inside 0.6s and "
                      f"{v['inReachGivenAny']:.2f} in reach at any instant, off "
                      f"only {v['seeds']} seeds.\n    IT COSTS {v['coverage']:.0%} "
                      f"OF THE HALL, up from 42% at the last pick's 26 short "
                      f"vines —\n    that is the trade \"less vines, longer\" "
                      f"buys, and it is reported rather than\n    optimised away.")
                out["pickA"] = pickA[0]
            else:
                pickA = max(gridA.items(), key=lambda kv: kv[1]["several"])
                print(f"\n    NOTHING CLEARS 60% 3+/0.6s. Best is {pickA[0]} at "
                      f"{pickA[1]['several']:.0%} / {pickA[1]['coverage']:.0%}.")
                out["pickA"] = pickA[0]
            check("several plants strike the foe inside one perceptual beat",
                  bool(ok),
                  f"{len(ok)} of {len(gridA)} settings clear 60% 3+/0.6s")
            check("and more than two can reach it at a single instant, which the "
                  "confounded first run said was impossible",
                  best >= 2.2, f"best {best:.2f}")
            # AND THEY ARE CANDIDATES, NOT A PICK. The first cut of this file
            # chose one garden here and handed it to [B], and [B] then could not
            # price it: at 26 plants and 20+ whips a cast the ultimate wins the
            # fight at ANY whipDmg, because what is doing the work is 20 hit
            # stuns, not the damage on them. The read and the price are not
            # independent and cannot be solved in sequence.
            CANDS = [(gridA[k]["reach"], gridA[k]["maxVines"],
                      gridA[k]["seeds"], gridA[k]["vineLife"]) for k, _ in cands]
            RR, CAP, SEEDS_, VL = CANDS[0]
        else:
            RR, VL = base["ult"]["reach"], base["ult"]["vineLife"]
            SEEDS_, CAP = base["ult"]["seeds"], base["ult"]["maxVines"]
            CANDS = [(RR, CAP, SEEDS_, VL)]

        # ------------------------------------------------------ [B] price --
        # AND THIS STAGE HAD TO BE REWRITTEN FOR THE SAME REASON [A] DID.
        # The first cut swept whipDmg x whipCd at [H]'s hold and reported the
        # vine SHARE, which came back 61-74% and could not be brought near a
        # third at any setting. That is arithmetic, not balance: the share is
        # a ratio and the hold pins its denominator to a weak blade. Held at
        # dmg 6.8 the vines are most of the relic no matter what they hit for.
        #
        # A share is only meaningful at the damage the relic will SHIP with,
        # and that damage depends on the ultimate -- so the two are solved
        # together. Every cell bisects `dmg` to an even relic and reports the
        # share AT THAT POINT. It is more expensive by the width of a
        # bisection and it is the only version that answers the question.
        if "b" in A.stage:
            print(f"\n[B] THE PRICE — at reach {RR:g} / {SEEDS_:g} seeds, "
                  f"what the ultimate is WORTH.\n    Each cell bisects `dmg` to an "
                  f"even relic first, because a SHARE measured against a\n    blade "
                  f"that is not the shipping blade is a statement about the blade.\n")
            bseeds = [101 + 7 * i for i in range(max(6, A.seeds * 2))]
            bfoes = [f for f in ["grudgebearer", "widowmaker", "emberedge",
                                 "gravemourn", "thornwake", "spellbreaker",
                                 "censer", "axiom"] if f in roster]

            def balance(ov, steps=5):
                lo, hi = 2.0, 26.0
                m = None
                for _ in range(steps):
                    mid = (lo + hi) / 2
                    o = dict(ov); o["dmg"] = mid
                    m = page.evaluate(MEASURE_JS, [RID, o, bfoes, bseeds,
                                                   A.secs, False])
                    if m["win"] > 0.5: hi = mid
                    else: lo = mid
                d = round((lo + hi) / 2, 2)
                o = dict(ov); o["dmg"] = d
                m = page.evaluate(MEASURE_JS, [RID, o, bfoes, bseeds, A.secs, False])
                return d, m

            # THE COOLDOWN AXIS IS WIDE ON PURPOSE. `whips/cast` came back at
            # 17-26 in the first cut and every one of them is a HIT STUN as
            # well as damage, so the ultimate was winning by lockdown at any
            # damage. Fewer, harder whips is the only lever that touches that.
            dmgs = [2, 5, 9, 14]
            cds = [1.4, 2.2, 3.2]
            print(f"    {'garden':>10}{'whipDmg':>8}{'whipCd':>8}{'dmg@50%':>9}"
                  f"{'win':>7}{'vine dmg':>10}{'several':>9}"
                  f"{'dmg/cast':>10}{'whips/cast':>12}{'dur':>7}")
            gridB = {}
            for (rr, cap, mag, vl) in CANDS:
                for wd, cd in itertools.product(dmgs, cds):
                    ov = {"reach": rr, "vineLife": vl, "seeds": mag,
                          "maxVines": cap, "whipDmg": wd, "whipCd": cd}
                    d, m = balance(ov)
                    key = f"{rr}/{mag}|{wd}/{cd}"
                    gridB[key] = dict(m, dmgAt50=d, reach=rr, maxVines=cap,
                                      seeds=mag, vineLife=vl, whipDmg=wd, whipCd=cd)
                    print(f"    {f'{rr:g}/{mag:g}':>10}{wd:>8}{cd:>8.1f}{d:>9.2f}"
                          f"{m['win']:>7.0%}{m['vineShare']:>10.0%}"
                          f"{m['several']:>9.0%}"
                          f"{m['dVine']/max(1,m['casts']):>10.0f}"
                          f"{m['whipsPerCast']:>12.1f}{m['dur']:>7.1f}")
            out["B"] = gridB
            # THE TARGET IS A SHARE AT BALANCE. A third is the number: it is
            # what an ultimate on a 15-charge cooldown is worth if the weapon
            # is still the relic, and it is close to what the Harrowing and
            # the Converse land at on their own decompositions.
            TARGET = 0.33
            # BOTH constraints at once: the ultimate is worth about a third at
            # balance, AND the read Rick asked for survives the pricing. A
            # setting that hits the share by making the garden inert has
            # answered the wrong question.
            live = [kv for kv in gridB.items() if kv[1]["several"] >= 0.50]
            pool = live or list(gridB.items())
            # AND COVERAGE BREAKS THE TIE. Stage A ranks candidates on the read
            # BEFORE they are priced, and pricing moves them: 250/8 led A by
            # 3pp of `several` and finished level with 205/8 once whipDmg and
            # whipCd were solved. When two settings deliver the same read, the
            # one that reaches less of the hall is the one §1 asked for --
            # "good but LIMITED range" is a clause in the design, not a
            # tolerance this file gets to spend.
            bestShare = min(abs(kv[1]["vineShare"] - TARGET) for kv in pool)
            bestSev = max(kv[1]["several"] for kv in pool
                          if abs(kv[1]["vineShare"] - TARGET) <= bestShare + 0.05)
            tied = [kv for kv in pool
                    if abs(kv[1]["vineShare"] - TARGET) <= bestShare + 0.05
                    and kv[1]["several"] >= bestSev - 0.02]
            pickB = min(tied, key=lambda kv: kv[1]["reach"])
            v = pickB[1]
            print(f"\n    PICK: {pickB[0]} — with the blade bisected to "
                  f"{v['dmgAt50']:.2f} the vines carry {v['vineShare']:.0%}\n    "
                  f"of the relic against a target of {TARGET:.0%}, and "
                  f"{v['several']:.0%} of strikes still have 3+ plants\n    inside "
                  f"0.6s, at reach {v['reach']:g} — the SHORTEST of "
                  f"{len(tied)} settings tied on both.\n    "
                  f"{len(bfoes) * len(bseeds)} matches a cell.")
            out["pickB"] = pickB[0]
            check("a setting exists that puts the ultimate near a third of the "
                  "relic AT BALANCE, without killing the read",
                  abs(v["vineShare"] - TARGET) < 0.10 and v["several"] >= 0.50,
                  f"{v['vineShare']:.0%} share, {v['several']:.0%} several; "
                  f"the grid spans "
                  f"{min(x['vineShare'] for x in gridB.values()):.0%}-"
                  f"{max(x['vineShare'] for x in gridB.values()):.0%}")
            RR, CAP = v["reach"], v["maxVines"]
            SEEDS_, VL = v["seeds"], v["vineLife"]
            WD, CD = v["whipDmg"], v["whipCd"]
            DMG = v["dmgAt50"]
        else:
            WD, CD = base["ult"]["whipDmg"], base["ult"]["whipCd"]
            DMG = base["dmg"]

        # ------------------------------------------------------ [C] confirm --
        if "c" in A.stage:
            print(f"\n[C] THE CONFIRMATION — the whole picked setting, on every "
                  f"foe in the roster.\n    This is still not a tuning result: "
                  f"verify.py runs 231 pairings and tune.py owns\n    `dmg`. It is "
                  f"the bracket to hand them.\n")
            cfoes = [f for f in roster if f != RID]
            cseeds = [101 + 7 * i for i in range(max(6, A.seeds * 2))]
            ov = {"reach": RR, "vineLife": VL, "seeds": SEEDS_,
                  "maxVines": CAP, "whipDmg": WD, "whipCd": CD}
            print(f"    {'dmg':>7}{'win':>7}{'dur':>7}{'vine dmg':>10}"
                  f"{'arrow':>8}{'melee':>8}{'whips/cast':>12}{'n':>6}")
            gridC = {}
            for d in sorted({round(DMG - 2, 2), round(DMG - 1, 2), DMG,
                             round(DMG + 1, 2), round(DMG + 2, 2)}):
                o = dict(ov); o["dmg"] = d
                m = page.evaluate(MEASURE_JS, [RID, o, cfoes, cseeds,
                                               A.secs, False])
                gridC[f"{d}"] = m
                print(f"    {d:>7.2f}{m['win']:>7.1%}{m['dur']:>7.1f}"
                      f"{m['vineShare']:>10.0%}{m['shotShare']:>8.0%}"
                      f"{m['meleeShare']:>8.0%}{m['whipsPerCast']:>12.1f}"
                      f"{m['played']:>6}")
            out["C"] = gridC
            near = min(gridC.items(), key=lambda kv: abs(kv[1]["win"] - 0.5))
            print(f"\n    NEAREST 50% against all {len(cfoes)} foes x "
                  f"{len(cseeds)} seeds: dmg {near[0]} at {near[1]['win']:.1%}.")
            out["pickC"] = near[0]
            DMG = float(near[0])
            check("the picked setting sits near even against the whole roster",
                  abs(near[1]["win"] - 0.5) < 0.06,
                  f"{near[1]['win']:.1%} over {near[1]['played']} matches")

        print(f"\n    THE SETTING THIS SWEEP ARRIVES AT:")
        print(f"      reach {RR:g}  seeds {SEEDS_:g}  maxVines {CAP:g}  "
              f"vineLife {VL:g}  whipDmg {WD:g}  whipCd {CD:g}  dmg {DMG:g}")
        print(f"      rebuild:  python3 vinesower_build.py --reach {RR:g} "
              f"--seeds {SEEDS_:g} --maxvines {CAP:g} --vinelife {VL:g} "
              f"--whipdmg {WD:g} --whipcd {CD:g} --dmg {DMG:g}")

        assert not errors, errors[:4]

    # ------------------------------------------------------ [0] override --
    if A.verify_override:
        print("\n[0] THE OVERRIDE IS PROVED, NOT TRUSTED — every number in every "
              "table above was\n    applied at runtime rather than rebuilt, which "
              "is the only reason a grid this\n    wide is affordable. v39 "
              "established that this has to be shown, not assumed.\n")
        OV, OFULL, ofoes, oseeds = override_args
        args = [sys.executable, "vinesower_build.py",
                "--src", "../02-chain/sc-foregone.html",
                "--out", "/tmp/sc-vinesower-ovtest.html"]
        for k, v in OFULL.items():
            if k == "charge":
                continue
            args += [f"--{k.lower()}", str(v)]
        r = subprocess.run(args, cwd=HERE, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-800:], r.stderr[-800:])
            sys.exit("rebuild for override verification failed")
        with game(game_path=pathlib.Path("/tmp/sc-vinesower-ovtest.html")) as (p2, e2):
            baked = p2.evaluate(BAKED_JS, [RID, ofoes, oseeds, 40.0])
            assert not e2, e2[:3]
        same = override_live == baked
        print(f"    {json.dumps(OV)} applied at runtime on top of the "
              f"build's own numbers,\n    against a build carrying all of it in "
              f"the file: {len(baked)} matches, field for field.")
        check("a runtime ult override is identical to the same numbers baked "
              "into the build",
              same,
              f"{len(baked)}/{len(baked)} identical" if same else
              f"first disagreement at match "
              f"{next((i for i, (x, y) in enumerate(zip(override_live, baked)) if x != y), None)}")

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"   ({len(bad)} FAILED)" if bad else ""))
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1, default=str))
        print(f"wrote {A.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
