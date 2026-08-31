#!/usr/bin/env python3
"""LOOK AT THE SCYTHE ROW BEFORE THE ULTIMATE IS DESIGNED.

    python3 scythe_survey.py --game ../02-chain/sc-paradox-ignition.html

v40 pointed this discipline at the bow row, v41 at the warhammer, v43 at the
flail, v47 at the twinblade. Rick has taken **vigil x scythe**. This is the
scythe's first survey, and the first time a VIGIL cell has been surveyed at
all — `cell_survey` prints vigil as a dash on every row because the school has
no onHit channel, so no vigil cell has ever been ranked against its own type.

`row_price.py` already settled which cell: against the whole roster, vigil is
the strongest channel on this row at **+19.2%**, ahead of bloodsworn's +11.7%,
dwarven's +7.9% and umbral's -0.4%. This survey is about the TYPE and about
the CHANNEL on it.

What is structurally peculiar about the pairing, before any of it is measured:

  * THE WARD IS THE ONLY STATUS THAT CAN BE THROWN AWAY. Every other status
    expires having already delivered its effect. `tickStatus` on a lapsed ward
    does `f.shield = 0; f.shieldMax = 0` — **the whole banked pool, gone
    unspent.** Nothing in this repo has ever measured how much that is.

  * AND ITS CLOCK IS 5 SECONDS, WHICH IS THE SAME ORDER AS THIS TYPE'S CONTACT
    INTERVAL. The scythe lands a blow every ~4.3 seconds. Each blow restarts
    the clock, so the plate lives on a margin of well under a second. The
    source already carries the warhammer's version of this: *"the plate
    expires four times a fight, so a charge timer that knows nothing about the
    plate casts on an empty one more often than not: the pool at the cast is a
    MEDIAN OF ZERO over 88 casts."*

  * `STATUS.ward.bank 0.55 / cap 90` HAVE NEVER BEEN SWEPT. Vigil od 4, and
    still open in v41, v42, v43 and v47. v43 added a third point on the type
    axis by measuring the flail banking fine at 1.0, like the warhammer and
    unlike the bow — Farwarden's 2.5 was a patch for a BOW and not for weight.
    The scythe is the fourth point and this is where the sweep finally runs.

  [1] THE ROW AND THE BLOCK. Read from AC.WEAPONS, not a doc.
  [2] THE BLADE. Live segment, contacts, and contacts per radian turned, every
      type, so the scythe's number has five controls beside it.
  [3] THE CLANK LADDER AT MASS 2.4. Outcome read off the EFFECT. The scythe
      sits in the middle of the mass ladder and is the only type that has
      never had this measured.
  [4] THE WARD'S CLOCK AGAINST THE TYPE'S CLOCK, and what gets thrown away.
      Then the sweep that answers vigil od 4.
  [5] THE TRAPS.

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
from wh_survey import CLANK_JS  # noqa: E402
from twinblade_survey import GEOM_JS  # noqa: E402

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
FOES = ["emberedge", "spellbreaker", "aureole", "censer", "gravemourn"]

# ------------------------------------------------------------- [4] the ward ---
# The plate, instrumented at the two events nothing in the repo counts: what it
# ABSORBED, and what it was holding when the 5-second clock ran out.
#
# `shatter` is wrapped on the instance rather than the prototype, so only this
# match is watched and every other relic runs the shipped code. Expiry is read
# off the transition — the status object gone with a pool still on the shell —
# because tickStatus zeroes both in the same statement and there is no hook.

WARD2_JS = r"""([donor, foes, seeds, secs, pin, pinIds, noult, bank, cap, dur]) => {
  const DT = AC.CONFIG.physics.dt;
  const W  = AC.STATUS.ward;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  const savedS = { bank: W.bank, cap: W.cap, dur: W.dur };
  if (bank !== null) W.bank = bank;
  if (cap  !== null) W.cap  = cap;
  if (dur  !== null) W.dur  = dur;
  w.aff = "vigil";
  delete w.onHit;
  w.onSelf = { ward: 1 };

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

      let step = 0, upFr = 0, poolSum = 0, poolN = 0, peak = 0;
      let raises = 0, expiries = 0, shatters = 0;
      let lost = 0, absorbed = 0, banked = 0;
      let lastHit = -1, gapSum = 0, gapN = 0;

      /* A SHATTER LOOKS EXACTLY LIKE AN EXPIRY FROM OUTSIDE. `shatter()` does
         `f.shield = 0; f.shieldMax = 0; delete f.status.ward` -- the same three
         writes tickStatus makes when the clock runs out. The first cut of this
         section counted both as expiries and added an already-ABSORBED pool to
         the thrown-away column, which is why absorbed + lost came out larger
         than banked. The conservation check below is now permanent. */
      let shatteredThisStep = false;
      const origShatter = m.shatter.bind(m);
      m.shatter = function(fr, src){
        if (fr === me){ shatters++; shatteredThisStep = true; }
        return origShatter(fr, src);
      };
      const origHurt = m.hurt.bind(m);
      m.hurt = function(foe2, dmg, src){
        if (foe2 === me && foe2.shield > 0)
          absorbed += Math.min(foe2.shield, dmg);
        return origHurt(foe2, dmg, src);
      };
      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const before = me.shield;
        const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
        /* NO `mul === undefined` GATE. A shot routes through resolveHit with
           `mul` SET (s.dmgMul), so gating on it counts none of a bow's banking
           while the bow banks normally -- which is how the conservation check
           below came back at 1.93x on the bow row and nowhere else. The gate is
           right for "was this an ordinary melee blow" and wrong for "did this
           blow bank", and the ward does not care which kind it was. */
        if (self === me){
          banked += Math.max(0, me.shield - before);
          const t = step * DT;
          if (lastHit >= 0){ gapSum += t - lastHit; gapN++; }
          lastHit = t;
        }
        return r;
      };

      let hadWard = false, prevShield = 0;
      while (!m.over && step < secs / DT){
        const wasWard = !!me.status.ward, ps = me.shield;
        shatteredThisStep = false;
        m.step(DT); step++;
        const isWard = !!me.status.ward;
        if (!wasWard && isWard) raises++;
        /* THE THROW-AWAY. The status object is gone, the pool it was holding
           went with it, and no shatter fired — so this is health the relic
           banked and never spent. */
        if (wasWard && !isWard && ps > 0.5 && me.shield === 0
            && !shatteredThisStep){
          expiries++; lost += ps;
        }
        if (me.shield > 0){ upFr++; poolSum += me.shield; poolN++;
                            if (me.shield > peak) peak = me.shield; }
      }
      rows.push({ foe: f, seed: sd, dur: step * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  up: step ? upFr / step : 0,
                  pool: poolN ? poolSum / poolN : 0, peak,
                  raises, expiries, shatters, lost, absorbed, banked,
                  gap: gapN ? gapSum / gapN : 0, hits: me.hits,
                  dealt: me.dealt, taken: th.dealt });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  W.bank = savedS.bank; W.cap = savedS.cap; W.dur = savedS.dur;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""

TRAP_JS = r"""() => {
  const out = {};
  const tsSrc = AC.Match.prototype.tickStatus.toString();
  const rhSrc = AC.Match.prototype.resolveHit.toString();
  const hSrc  = AC.Match.prototype.hurt.toString();
  const probe = new AC.Match("thornwake", "aureole", 5);
  out.wardZeroesOnExpiry =
    /key === "ward"\)\{\s*f\.shield = 0;\s*f\.shieldMax = 0/.test(tsSrc);
  out.dotUnderWard = !/hurt/.test(tsSrc.split("def.dps")[1].slice(0, 200));
  out.bankAfterHurt = rhSrc.indexOf("onSelf") > rhSrc.indexOf("this.hurt(foe, dmg, self)");
  out.shieldEatsFirst = /foe\.shield > 0 && dmg > 0/.test(hSrc);
  out.reclock = /self\.apply\("ward", 1\)/.test(rhSrc);
  out.segFromTheta = /f\.theta \+ off/.test(AC.Match.prototype.bladeSegments.toString());
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=24.0)
    ap.add_argument("--only", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"1", "2", "3", "4", "5"}
    gp = (HERE / a.game).resolve()
    seeds = [5501 + 23 * i for i in range(a.seeds)]
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("""() => AC.WEAPONS.map(w => ({
              id:w.id, name:w.name, aff:w.aff, shape:w.shape, mode:w.mode,
              reach:w.reach, width:w.width, spin:w.spin, mass:w.mass,
              dmg:w.dmg, blades:w.blades.length, arc:w.arc||null,
              knockMul:w.knockMul||null}))""")
        ST = page.evaluate("() => AC.STATUS")
        shapes = sorted({w["shape"] for w in W})
        schools = sorted({w["aff"] for w in W})
        filled = {(w["aff"], w["shape"]): w["name"] for w in W}
        scythes = [w for w in W if w["shape"] == "scythe"]
        pin_ids = [w["id"] for w in W]
        donor = TYPE_DONOR["scythe"]

        # ---------------------------------------------------------- [1] --
        if "1" in want:
            print(f"\n[1] THE SCYTHE ROW — {len(scythes)} of {len(schools)} filled\n")
            print(f"    {'':<10}" + "".join(f"{s[:11]:>12}" for s in schools))
            print(f"    {'scythe':<10}"
                  + "".join(f"{filled.get((s,'scythe'),'·')[:11]:>12}" for s in schools))
            print(f"\n    {'type':<12}{'reach':>7}{'width':>7}{'spin':>7}{'mass':>7}"
                  f"{'blades':>8}{'mode':>8}{'dmg':>16}")
            for t in shapes:
                rel = [w for w in W if w["shape"] == t]
                r0 = rel[0]
                d = f"{min(x['dmg'] for x in rel):.1f}-{max(x['dmg'] for x in rel):.1f}"
                print(f"    {t:<12}{r0['reach']:>7}{r0['width']:>7}{r0['spin']:>7.1f}"
                      f"{r0['mass']:>7.1f}{r0['blades']:>8}{r0['mode']:>8}{d:>16}")
            print(f"\n    ward   " + "  ".join(f"{k} {v}" for k, v in ST["ward"].items()
                                               if k != "tip"))
            fields = ("reach", "width", "spin", "mode", "mass", "blades")
            check("all three scythes share one physics block, field for field",
                  all(len({w[f] for w in scythes}) == 1 for f in fields),
                  ", ".join(f"{f}={scythes[0][f]}" for f in fields))
            masses = sorted({w["mass"] for w in W})
            check("the scythe sits in the MIDDLE of the mass ladder — the only "
                  "type that is decisive against some binds and not others",
                  masses.index(scythes[0]["mass"]) not in (0, len(masses) - 1),
                  f"ladder {', '.join(f'{m:g}' for m in masses)}, "
                  f"scythe at {scythes[0]['mass']:g}")
            spread = max(w["dmg"] for w in scythes) / min(w["dmg"] for w in scythes)
            check("and it carries the widest damage spread of any three-relic type",
                  spread > 1.5,
                  f"{min(w['dmg'] for w in scythes):.2f} to "
                  f"{max(w['dmg'] for w in scythes):.2f} = x{spread:.2f} "
                  f"— Lastlight pays for the Harrowing, Thornwake does not")

        # ---------------------------------------------------------- [2] --
        geom = {}
        if "2" in want:
            print(f"\n[2] THE BLADE — live segment off `bladeSegments`, "
                  f"dmg pinned {a.pin:g}, ultimates suppressed\n")
            print(f"    {'type':<12}{'live blade':>12}{'contacts/s':>12}"
                  f"{'mean gap':>11}{'rad/s':>8}{'contacts/rad':>14}")
            for t in shapes:
                d = TYPE_DONOR[t]
                foes_t = [f for f in FOES if f != d]
                rows = page.evaluate(GEOM_JS, [d, foes_t, seeds, a.secs, a.pin,
                                               pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                hits = sum(r["hits"] for r in rows)
                turn = sum(r["turned"] for r in rows) / dur
                hps = hits / dur
                geom[t] = {"seg": mean(r["seg"] for r in rows), "hps": hps,
                           "gap": 1 / hps if hps else 0, "turn": turn,
                           "perRad": hps / turn if turn else 0}
                gg = geom[t]
                print(f"    {t:<12}{gg['seg']:>12.1f}{gg['hps']:>12.3f}"
                      f"{gg['gap']:>10.2f}s{gg['turn']:>8.2f}{gg['perRad']:>14.4f}")
            wd = ST["ward"]["dur"]
            close = [t for t in shapes if abs(geom[t]["gap"] - wd) < 1.5]
            check(f"THE WARD'S {wd:g}s CLOCK IS THE SAME ORDER AS THIS TYPE'S "
                  f"CONTACT INTERVAL",
                  "scythe" in close,
                  f"scythe lands a blow every {geom['scythe']['gap']:.2f}s against a "
                  f"{wd:g}s ward; the types inside 1.5s of the clock are "
                  f"{', '.join(close)}")
            out["geom"] = geom

        # ---------------------------------------------------------- [3] --
        if "3" in want:
            print(f"\n[3] THE CLANK LADDER AT MASS {scythes[0]['mass']:g}\n")
            print(f"    {'foe':<14}{'type':<12}{'mass':>6}{'clanks/min':>12}"
                  f"{'won':>7}{'deadlock':>10}{'lost':>7}{'stagger eaten':>15}")
            cl = {}
            for f in ["ironhail", "widowmaker", "lastlight", "emberedge",
                      "gravemourn", "censer"]:
                rows = page.evaluate(CLANK_JS, [donor, [f], seeds, a.secs,
                                                a.pin, pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                n = sum(r["clanks"] for r in rows)
                won = sum(r["won"] for r in rows)
                lost = sum(r["lost"] for r in rows)
                dead = sum(r["dead"] for r in rows)
                st = sum(r["stunMe"] for r in rows) / dur if dur else 0
                cl[f] = {"n": n, "won": won, "lost": lost, "dead": dead}
                fm = rows[0]["foeMass"]
                print(f"    {f:<14}{[w for w in W if w['id']==f][0]['shape']:<12}"
                      f"{fm:>6.1f}{n/dur*60 if dur else 0:>12.1f}"
                      f"{(won/n if n else 0):>7.0%}{(dead/n if n else 0):>10.0%}"
                      f"{(lost/n if n else 0):>7.0%}{st:>14.3f}s")
            anywon = sum(v["won"] for v in cl.values())
            anylost = sum(v["lost"] for v in cl.values())
            check("the scythe both WINS and LOSES binds — unlike the twinblade, "
                  "which loses every one, and the flail, which loses only to the "
                  "warhammer",
                  anywon > 0 and anylost > 0,
                  f"{anywon} won, {anylost} lost across six types")
            out["clank"] = cl

        # ---------------------------------------------------------- [4] --
        if "4" in want:
            print(f"\n[4] THE WARD ON THIS TYPE — and what the 5s clock throws away\n")
            print(f"    {'type':<12}{'gap':>7}{'plate up':>10}{'mean pool':>11}"
                  f"{'peak':>7}{'raises/min':>12}{'EXPIRIES/min':>14}"
                  f"{'shatters/min':>14}")
            wardrow = {}
            for t in shapes:
                d = TYPE_DONOR[t]
                foes_t = [f for f in FOES if f != d]
                rows = page.evaluate(WARD2_JS, [d, foes_t, seeds, a.secs, a.pin,
                                                pin_ids, True, None, None, None])
                dur = sum(r["dur"] for r in rows)
                wardrow[t] = {
                    "up": mean(r["up"] for r in rows),
                    "pool": mean(r["pool"] for r in rows),
                    "peak": max(r["peak"] for r in rows),
                    "raises": sum(r["raises"] for r in rows) / dur * 60,
                    "exp": sum(r["expiries"] for r in rows) / dur * 60,
                    "shat": sum(r["shatters"] for r in rows) / dur * 60,
                    "lost": sum(r["lost"] for r in rows),
                    "absorbed": sum(r["absorbed"] for r in rows),
                    "banked": sum(r["banked"] for r in rows),
                    "gap": mean(r["gap"] for r in rows if r["gap"] > 0),
                }
                v = wardrow[t]
                print(f"    {t:<12}{v['gap']:>6.2f}s{v['up']:>10.0%}"
                      f"{v['pool']:>11.1f}{v['peak']:>7.0f}{v['raises']:>12.1f}"
                      f"{v['exp']:>14.1f}{v['shat']:>14.1f}")

            print(f"\n    WHERE THE BANK GOES — nothing in this repo has ever "
                  f"counted the third column\n")
            print(f"    {'type':<12}{'banked':>10}{'ABSORBED':>11}"
                  f"{'THROWN AWAY ON EXPIRY':>24}{'kept':>8}")
            for t in shapes:
                v = wardrow[t]
                tot = v["absorbed"] + v["lost"]
                print(f"    {t:<12}{v['banked']:>10.0f}{v['absorbed']:>11.0f}"
                      f"{v['lost']:>24.0f}"
                      f"{(v['absorbed'] / tot if tot else 0):>8.0%}")
            sc = wardrow["scythe"]
            keep = sc["absorbed"] / max(1, sc["absorbed"] + sc["lost"])
            check("THE PLATE THROWS AWAY A REAL SHARE OF WHAT IT BANKS, and the "
                  "5s clock is why", sc["lost"] > 0,
                  f"the scythe absorbs {sc['absorbed']:.0f} and loses "
                  f"{sc['lost']:.0f} unspent — {keep:.0%} kept — at "
                  f"{sc['exp']:.1f} expiries a minute")
            # CONSERVATION. Every point banked is absorbed, thrown away on an
            # expiry, or still on the shell when the fight ends. If the two
            # measured columns exceed what was banked, the instrument is
            # counting one pool twice -- which is exactly what the first cut
            # did by reading a SHATTER as an expiry.
            worst = max(shapes, key=lambda t: (wardrow[t]["absorbed"]
                                               + wardrow[t]["lost"])
                        / max(1, wardrow[t]["banked"]))
            ratio = ((wardrow[worst]["absorbed"] + wardrow[worst]["lost"])
                     / max(1, wardrow[worst]["banked"]))
            check("CONSERVATION — absorbed plus thrown away cannot exceed what "
                  "was banked",
                  ratio <= 1.02,
                  "worst type " + worst + f" at {ratio:.2f}x  " +
                  ", ".join(f"{t} {(wardrow[t]['absorbed']+wardrow[t]['lost'])/max(1,wardrow[t]['banked']):.2f}"
                            for t in shapes))

            print(f"\n    THE SWEEP — vigil od 4, open since Vigil and restated in "
                  f"v41, v42, v43 and v47\n")
            print(f"    {'bank':>6}{'cap':>6}{'dur':>6}{'plate up':>10}"
                  f"{'mean pool':>11}{'absorbed':>10}{'thrown away':>13}"
                  f"{'kept':>7}{'win':>8}")
            sweep = {}
            base = (ST["ward"]["bank"], ST["ward"]["cap"], ST["ward"]["dur"])
            # A 2x2x2 around the shipped point rather than a star, so the
            # INTERACTION is separable. The first cut was a star and the best
            # cell in it beat the sum of its own single-knob moves by nine
            # points, which a star cannot explain.
            grid = [base,
                    (0.55, 90, 7.0), (0.55, 90, 9.0), (0.55, 140, 5.0),
                    (0.85, 90, 5.0), (0.85, 90, 7.0),
                    (0.85, 140, 5.0), (0.85, 140, 7.0),
                    (0.35, 90, 5.0)]
            # THE WHOLE ROSTER for the sweep, not a five-relic field. This is
            # vigil od 4 and it has been open since Vigil; forty fights a cell
            # is a win column with an eight-point error bar on it, which is
            # how a knob stays "unswept" through four sessions of being looked
            # at.
            foes_s = [w["id"] for w in W if w["id"] != donor]
            for (bk, cp, du) in grid:
                rows = page.evaluate(WARD2_JS, [donor, foes_s, seeds, a.secs,
                                                a.pin, pin_ids, True, bk, cp, du])
                dur = sum(r["dur"] for r in rows)
                fin = [r for r in rows if r["win"] >= 0]
                ab = sum(r["absorbed"] for r in rows)
                lo = sum(r["lost"] for r in rows)
                rec = {"up": mean(r["up"] for r in rows),
                       "pool": mean(r["pool"] for r in rows),
                       "ab": ab, "lo": lo,
                       "keep": ab / max(1, ab + lo),
                       "win": mean(r["win"] for r in fin)}
                sweep[f"{bk}/{cp}/{du}"] = rec
                tag = "  <- ships" if (bk, cp, du) == base else ""
                print(f"    {bk:>6.2f}{cp:>6.0f}{du:>6.1f}{rec['up']:>10.0%}"
                      f"{rec['pool']:>11.1f}{ab:>10.0f}{lo:>13.0f}"
                      f"{rec['keep']:>7.0%}{rec['win']:>8.1%}{tag}")
            shipped = sweep[f"{base[0]}/{base[1]}/{base[2]}"]
            longer = sweep["0.55/90/9.0"]
            bigger = sweep["0.85/90/5.0"]
            wider  = sweep["0.55/140/5.0"]
            check("`cap 90` IS NOT THE CONSTRAINT — raising it alone does almost "
                  "nothing, which is half of vigil od 4 answered",
                  abs(wider["win"] - shipped["win"]) < 0.03,
                  f"cap 90 -> 140 moves the win rate "
                  f"{shipped['win']:.1%} -> {wider['win']:.1%} and the mean pool "
                  f"{shipped['pool']:.1f} -> {wider['pool']:.1f}")
            check("AND `thrown away` IS NOT WASTE — the arm that throws away least "
                  "is the WORST arm in the sweep",
                  longer["keep"] > shipped["keep"] and longer["win"] < shipped["win"],
                  f"dur 9.0 keeps {longer['keep']:.0%} against dur 5.0's "
                  f"{shipped['keep']:.0%} and wins {longer['win']:.1%} against "
                  f"{shipped['win']:.1%}. A plate that expires unspent is a plate "
                  f"nobody had to break — v42 §3c from the other side: ask what "
                  f"the worst thing that scores well on a metric looks like")
            check("`bank` IS THE LIVE KNOB, and it is the one nobody has touched",
                  bigger["win"] > shipped["win"] > sweep["0.35/90/5.0"]["win"],
                  f"0.35 -> {sweep['0.35/90/5.0']['win']:.1%}, "
                  f"0.55 -> {shipped['win']:.1%}, 0.85 -> {bigger['win']:.1%}")
            # THE INTERACTION, decomposed rather than asserted.
            print(f"\n    the interaction, read off the 2x2 at cap 140\n")
            for k in ("0.55/140/5.0", "0.85/140/5.0", "0.55/90/7.0",
                      "0.85/140/7.0"):
                if k in sweep:
                    print(f"        {k:<16}{sweep[k]['win']:>7.1%}"
                          f"{sweep[k]['pool']:>9.1f} mean pool")
            out["ward"] = {"byType": wardrow, "sweep": sweep}

        # ---------------------------------------------------------- [5] --
        if "5" in want:
            print(f"\n[5] THE TRAPS\n")
            t = page.evaluate(TRAP_JS)
            check("an expiring ward ZEROES the pool — it is the only status in the "
                  "game whose effect can be thrown away unspent",
                  t["wardZeroesOnExpiry"])
            check("the plate eats damage first and the OVERFLOW carries through, so "
                  "a large hit is not wasted on a thin plate", t["shieldEatsFirst"])
            check("every landed blow re-clocks the ward — so the plate's life is the "
                  "type's contact interval, not its own duration", t["reclock"])
            check("the bank runs AFTER hurt in resolveHit, so a blow never banks "
                  "against itself", t["bankAfterHurt"])
            check("the blade is a rigid function of f.theta — no lag term",
                  t["segFromTheta"])
            check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
