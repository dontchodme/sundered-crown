#!/usr/bin/env python3
"""THE CONVERSE, FALSIFIED.

    python3 foregone_probe.py --game ../02-chain/sc-foregone.html

Every check is written so that it CAN fail, and the ones that matter carry a
negative control -- a build where the thing does not happen must not pass.

  [1]  LAID BY DISTANCE, NOT BY TIME. Rick's answer. Positive: a moving caster
       lays sigils `gap` apart, measured on the real spacing. NEGATIVE CONTROL:
       a caster held in place lays exactly the one dropped at the cast site and
       no more. A time-gated implementation fails that and only that.

  [2]  THE REVERSAL VISITS EVERY SIGIL, NEWEST TO OLDEST, AND ENDS AT THE
       OLDEST. Asserted on the visit ORDER and the end POSITION, not on a
       count -- a reversal that fired every bloom in the wrong order would
       pass a count.

  [3]  NOTHING STOPS IT. Rick's fourth answer, and unfalsifiable without a
       harness. A 0.5s stun, five stacks of hex and a `breakSpin` are applied
       every single frame of the reversal. It must still complete, still bloom
       every sigil, and still end at the oldest.

  [4]  ON RAILS. An impulse larger than Grudgebearer's fatal launch is applied
       mid-reversal and must not move it off the line. This is what separates
       rails from a very strong shove.

  [5]  ZERO BURDEN. `ultTrace` is null on every frame of every match among the
       twenty pre-existing relics.

  [6]  A PULSE IS NOT A SWING. `f.hits` must not move on a pulse or a bloom.
       v38 §7 found the contact-rate table counting ultimates as contact; this
       relic fires up to sixty rings a cast and would be the largest such
       error in the game by a factor of four.

  [7]  THE PULSE ECONOMY, measured rather than modelled.

  [8]  DOES IT FIGHT -- every foe, pinned seeds, no timeouts.

  [9]  WHAT THE CELL WAS FOR. Hex occupancy and delivered lock with the
       ultimate ON and OFF on identical seeds. The design exists because hex
       holds two stacks 18% of a fight here and caps 1% of the time. If the
       Converse does not move those, it is good for some other reason and the
       write-up has to say so -- which is v38 §4b, caught one relic too late.
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
ID = "foregone"
FOES = ["thornwake", "lastlight", "grudgebearer", "dawnbringer", "gravemourn",
        "ironhail", "nightfell", "widowmaker"]

# One instrumented run, several questions. `mode` selects the harness:
#   ""        natural
#   "pinned"  the caster is forced back to its position every frame
#   "stun"    every stun the engine has, every frame of the reversal
#   "knock"   one impulse over Grudgebearer's launchFatal, mid-reversal
TRACE_JS = """([id, foe, seed, mode, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  const me = m.a.w.id === id ? m.a : m.b;
  const u = me.w.ult;

  const segDist = (px, py, ax, ay, bx, by) => {
    const vx = bx - ax, vy = by - ay, L2 = vx*vx + vy*vy;
    let t = L2 ? ((px-ax)*vx + (py-ay)*vy) / L2 : 0;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(px - (ax + vx*t), py - (ay + vy*t));
  };

  /* THE BLOOMS ARE COUNTED AT THE SITE, NOT INFERRED FROM THE STATE.
     `_traceBurst` is the single firing site, so wrapping it is exact -- and
     it is the only way to see the LAST bloom at all: `f.ultTrace` is nulled
     in the same frame the final sigil is reached, so anything that reads the
     counters after `step()` is permanently one bloom short. The first cut of
     this probe was, and reported 11 of 12 as a failure of the build. */
  const bursts = [];
  const orig = AC.Match.prototype._traceBurst;
  AC.Match.prototype._traceBurst = function(f, fo, o, R, dmg, hexN, big){
    if (f === me) bursts.push({ big: !!big, x: o.x, y: o.y, t: m.t });
    return orig.call(this, f, fo, o, R, dmg, hexN, big);
  };

  let steps = 0, castStep = -1, laidBase = 0;
  const laid = [], offLine = [], travel = [];
  let hitsAtCast = null, hitsAtEnd = null, dealtAtCast = null;
  let prevLaid = 0, prevPhase = null, path = 0, pathAtDrop = 0;
  let endPos = null, oldest = null, stuns = 0, kicked = false;
  let pulses = 0, hits = 0, done = false, frozen = 0, traceFrames = 0;

  while (steps < secs / DT && !done){
    if (castStep < 0 && steps === Math.round(1.2 / DT)) me.charge = u.charge;

    const S0 = me.ultTrace;
    const tgt = (S0 && S0.phase === "trace" && S0.i >= 0) ? S0.orbs[S0.i] : null;
    const px = me.x, py = me.y;
    const wasFrozen = m.hitStop > 0;

    m.step(DT); steps++;
    if (mode === "pinned"){ me.x = px; me.y = py; me.vx = 0; me.vy = 0; }

    const S = me.ultTrace;
    if (S && castStep < 0){
      castStep = steps;
      hitsAtCast = me.hits; dealtAtCast = me.dealt;
      /* The sigil dropped AT the cast site is not "laid by travelling" and is
         deliberately excluded from [1] -- counting it made the negative
         control report 1 where the answer is 0. */
      prevLaid = S.orbs.length; laidBase = S.orbs.length;
      path = 0; pathAtDrop = 0;
    }
    if (S){
      pulses = S.pulses; hits = S.hits;
      if (S.phase === "lay"){
        path += Math.hypot(me.x - px, me.y - py);
        if (S.orbs.length > prevLaid){
          const o = S.orbs[S.orbs.length - 1];
          /* PATH LENGTH since the last drop, which is the quantity the rule
             is written against. The straight-line distance between two
             sigils is the CHORD of an arc the ball actually flew and is a
             lower bound on it, so measuring chords cannot test the rule. */
          laid.push({ x: o.x, y: o.y, t: S.t, path: path - pathAtDrop });
          pathAtDrop = path;
          prevLaid = S.orbs.length;
        }
        oldest = S.orbs.length ? { x: S.orbs[0].x, y: S.orbs[0].y } : null;
      } else if (S.phase === "trace"){
        traceFrames++;
        if (wasFrozen) frozen++;
        else travel.push(Math.hypot(me.x - px, me.y - py));
        if (tgt) offLine.push(segDist(me.x, me.y, px, py, tgt.x, tgt.y));
        if (mode === "stun"){
          me.stun = Math.max(me.stun, 0.5);
          me.apply("hex", 5);
          m.breakSpin(me, "harness");
          stuns++;
        }
        if (mode === "knock" && !kicked && bursts.filter(b => b.big).length >= 2){
          kicked = true; me.vx += 2600; me.vy -= 2600;
        }
      }
      if (S.released && endPos === null){
        hitsAtEnd = me.hits;
        endPos = { x: me.x, y: me.y };
      }
      prevPhase = S.phase;
    } else if (prevPhase === "trace" || prevPhase === "spent"){
      if (endPos === null){ hitsAtEnd = me.hits; endPos = { x: me.x, y: me.y }; }
      done = true;
    }
    if (m.over) break;
  }
  AC.Match.prototype._traceBurst = orig;
  const big = bursts.filter(b => b.big);
  return { steps, castStep, laid, offLine, travel, endPos, oldest,
           hitsAtCast, hitsAtEnd, dealtAtCast, dealt: me.dealt,
           pulses, blooms: big.length, bloomAt: big.map(b => [b.x, b.y]),
           hits, stuns, kicked, over: m.over, frozen, traceFrames,
           uSpeed: u.speed, gap: u.gap, maxOrbs: u.maxOrbs, lay: u.lay };
}"""

# [5] The zero-burden claim, asserted directly rather than argued.
BURDEN_JS = """([ids, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let frames = 0, seen = 0, matches = 0;
  for (const id of ids){
    for (const f of foes){
      if (f === id) continue;
      for (const s of seeds){
        const m = new AC.Match(id, f, s);
        matches++;
        let n = 0;
        while (!m.over && n < secs / DT){
          m.step(DT); n++; frames++;
          if (m.a.ultTrace || m.b.ultTrace) seen++;
        }
      }
    }
  }
  return { frames, seen, matches };
}"""

# [8][9] The fight, and the thing the cell was for. `noult` runs the same
# seeds with the charge unreachable, so the ultimate's contribution to hex is
# a difference on identical matches rather than a comparison across two
# different populations.
FIGHT_JS = """([id, foes, seeds, secs, noult, pin, pinIds]) => {
  const DT = AC.CONFIG.physics.dt;
  const saved = {};
  if (pin) for (const p of pinIds){
    const x = AC.WEAPONS.find(y => y.id === p);
    if (x){ saved[p] = x.dmg; x.dmg = pin; }
  }
  const w = AC.WEAPONS.find(x => x.id === id);
  const sv = w.ult.charge;
  if (noult) w.ult.charge = 1e9;
  const rows = [];
  for (const f of foes) for (const s of seeds){
    const m = new AC.Match(id, f, s);
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let n = 0, ge2 = 0, cap = 0, sum = 0, fires = 0, locked = 0, prev = 0;
    while (!m.over && n < secs / DT){
      m.step(DT); n++;
      const st = th.status.hex, k = st ? st.stacks : 0;
      sum += k; if (k >= 2) ge2++; if (k >= 5) cap++;
      const c = th.hexClock || 0;
      if (c < prev - 1e-9) fires++;
      prev = c;
      if (th.stun > 0) locked++;
    }
    rows.push({ foe: f, seed: s, dur: n * DT, over: m.over, hits: me.hits,
                ults: me.ultsFired, dealt: me.dealt,
                mean: n ? sum / n : 0, p2: n ? ge2 / n : 0,
                pCap: n ? cap / n : 0, firesPerS: fires / (n * DT),
                lock: n ? locked / n : 0,
                won: !!(m.winner && m.winner.w.id === id) });
  }
  w.ult.charge = sv;
  for (const p of Object.keys(saved)){
    AC.WEAPONS.find(y => y.id === p).dmg = saved[p];
  }
  return rows;
}"""

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-foregone.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--pin", type=float, default=0.0)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [101 + 7 * i for i in range(a.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        u = page.evaluate(
            "() => { const w = AC.WEAPONS.find(x => x.id === '%s'); "
            "return { ult: w.ult, dmg: w.dmg, aff: w.aff, shape: w.shape }; }" % ID)
        U = u["ult"]
        print(f"\n{ID} — {u['aff']} {u['shape']} dmg {u['dmg']}  ·  {U['name']} "
              f"charge {U['charge']}  lay {U['lay']}s  gap {U['gap']}  "
              f"speed {U['speed']}\n")

        nat = page.evaluate(TRACE_JS, [ID, "thornwake", 337, "", 40.0])
        assert nat["castStep"] > 0, "no cast in the natural run"

        # ----------------------------------------------------------- [1] --
        print("[1] LAID BY DISTANCE, NOT BY TIME\n")
        paths = [o["path"] for o in nat["laid"]]
        dts = [nat["laid"][i]["t"] - nat["laid"][i - 1]["t"]
               for i in range(1, len(nat["laid"]))]
        cvp = statistics.pstdev(paths) / statistics.mean(paths)
        cvt = statistics.pstdev(dts) / statistics.mean(dts)
        print(f"    natural: {len(nat['laid'])} laid by travelling")
        print(f"      PATH between drops   mean {statistics.mean(paths):6.2f}"
              f"   sd {statistics.pstdev(paths):5.2f}   cv {cvp:.4f}"
              f"   (the rule: {U['gap']})")
        print(f"      TIME between drops   mean {statistics.mean(dts):6.2f}s"
              f"   sd {statistics.pstdev(dts):5.2f}   cv {cvt:.4f}")
        pin = page.evaluate(TRACE_JS, [ID, "thornwake", 337, "pinned", 40.0])
        print(f"    pinned : {len(pin['laid'])} laid while held in place "
              f"(the control)")
        # A distance-gated drop happens on the first FRAME past the threshold,
        # so the path at a drop is `gap` plus at most one frame of travel --
        # 1600/120 = 13 units at the very worst, and ~3 at cruise.
        check("a sigil is dropped at a fixed PATH LENGTH, within one frame "
              "of travel",
              all(U["gap"] <= v <= U["gap"] + 14 for v in paths),
              f"every drop in [{min(paths):.2f}, {max(paths):.2f}] "
              f"against a gap of {U['gap']}")
        check("...and NOT at a fixed interval — the clock is the loose one",
              cvt > cvp * 8,
              f"cv(time) {cvt:.4f} is {cvt / cvp:.0f}x cv(path) {cvp:.4f}")
        check("NEGATIVE CONTROL — a caster that does not move lays nothing",
              len(pin["laid"]) == 0,
              f"{len(pin['laid'])} laid while held in place "
              f"(a time-gated build lays ~{U['lay'] / 0.32:.0f})")

        # ----------------------------------------------------------- [2] --
        print("\n[2] NEWEST TO OLDEST, ENDING AT THE OLDEST\n")
        sig = [[nat["oldest"]["x"], nat["oldest"]["y"]]] if nat["oldest"] else []
        sig = None
        # The sigils, in the order they were laid: the cast-site one first,
        # then `laid`. The cast-site position is the caster's at the cast, and
        # `oldest` is read off the live array, so they are the same object.
        order = [[o["x"], o["y"]] for o in nat["laid"]]
        order = [[nat["oldest"]["x"], nat["oldest"]["y"]]] + order
        print(f"    sigils laid {len(order)}   blooms fired {nat['blooms']}")
        seq_ok = (len(nat["bloomAt"]) == len(order)
                  and all(abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6
                          for a, b in zip(nat["bloomAt"], order[::-1])))
        endd = (math.hypot(nat["endPos"]["x"] - nat["oldest"]["x"],
                           nat["endPos"]["y"] - nat["oldest"]["y"])
                if nat["endPos"] and nat["oldest"] else None)
        print(f"    bloom sequence == the laid sequence reversed: {seq_ok}")
        print(f"    ends {endd:.3f}px from the oldest sigil")
        check("every sigil blooms exactly once",
              nat["blooms"] == len(order),
              f"{nat['blooms']} blooms for {len(order)} sigils")
        check("in reverse order — the bloom positions ARE the laid positions, "
              "backwards",
              seq_ok, "matched position for position")
        check("and it ends AT the oldest sigil",
              endd is not None and endd < 0.5,
              f"{endd:.3f}px" if endd is not None else "no end recorded")

        # ----------------------------------------------------------- [3] --
        print("\n[3] NOTHING STOPS IT — the harness\n")
        st = page.evaluate(TRACE_JS, [ID, "thornwake", 337, "stun", 40.0])
        print(f"    a 0.5s stun + 5 hex + a breakSpin applied on EVERY one of "
              f"{st['stuns']} frames of the reversal")
        sendd = (math.hypot(st["endPos"]["x"] - st["oldest"]["x"],
                            st["endPos"]["y"] - st["oldest"]["y"])
                 if st["endPos"] and st["oldest"] else None)
        print(f"    blooms {st['blooms']} against {nat['blooms']} natural"
              + (f", ends {sendd:.3f}px from the oldest" if sendd is not None
                 else ", REVERSAL NEVER COMPLETED"))
        check("the reversal completes under continuous hard stun",
              st["endPos"] is not None and sendd < 0.5,
              f"{st['stuns']} stun applications, still ended on the sigil")
        check("and blooms every sigil anyway",
              st["blooms"] == nat["blooms"],
              f"{st['blooms']} vs {nat['blooms']} natural")

        # ----------------------------------------------------------- [4] --
        print("\n[4] ON RAILS\n")
        kn = page.evaluate(TRACE_JS, [ID, "thornwake", 337, "knock", 40.0])
        off = max(nat["offLine"]) if nat["offLine"] else None
        koff = max(kn["offLine"]) if kn["offLine"] else None
        # TRAVEL PER UNFROZEN FRAME, not `Math.hypot(vx, vy)`. The build sets
        # vx/vy during the reversal for the ART -- the trail, the blur and the
        # weapon's lean all read velocity -- and the position is what moves.
        # Reading the velocity field measures the decoration.
        want = U["speed"] / 120.0
        tr = [v for v in nat["travel"] if v > 1e-9]
        print(f"    travel per unfrozen frame: mean {statistics.mean(tr):.3f}px"
              f"   against u.speed/120 = {want:.3f}")
        print(f"    {nat['frozen']} of {nat['traceFrames']} reversal frames "
              f"were hitStop ({nat['frozen'] / nat['traceFrames']:.0%})")
        print(f"    max distance off the segment: natural {off:.2f}px, "
              f"after a 3677-unit impulse {koff:.2f}px")
        check("it moves at the reversal speed, measured on POSITION",
              abs(statistics.mean(tr) - want) < want * 0.02,
              f"{statistics.mean(tr):.3f} vs {want:.3f} px/frame "
              f"= {statistics.mean(tr) * 120:.0f} u/s")
        check("an impulse over Grudgebearer's launchFatal cannot pull it "
              "off the line",
              kn["kicked"] and koff is not None and koff < 40
              and kn["blooms"] == nat["blooms"],
              f"max {koff:.2f}px off, and it still blooms "
              f"{kn['blooms']}/{nat['blooms']}")

        # ----------------------------------------------------------- [6] --
        print("\n[6] A PULSE IS NOT A SWING\n")
        dh = nat["hitsAtEnd"] - nat["hitsAtCast"]
        print(f"    {nat['pulses']} pulses and {nat['blooms']} blooms across "
              f"one cast; f.hits moved by {dh} over the same window")
        print(f"    of those, {nat['hits']} rings actually reached the foe")
        check("no pulse or bloom increments f.hits",
              dh <= 3,
              f"+{dh} across a cast that fired "
              f"{nat['pulses'] + nat['blooms']} rings — melee only")

        # ----------------------------------------------------------- [5] --
        print("\n[5] ZERO BURDEN\n")
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        others = [i for i in ids if i != ID]
        b = page.evaluate(BURDEN_JS, [others[:20], others[:6], seeds[:3], 60.0])
        print(f"    {b['matches']} matches among the other {len(others)}, "
              f"{b['frames']} frames, ultTrace non-null on {b['seen']}")
        check("ultTrace is null on every frame of every match without it",
              b["seen"] == 0, f"0 of {b['frames']} frames")

        # ----------------------------------------------------------- [7] --
        print("\n[7] THE PULSE ECONOMY, one natural cast\n")
        print(f"    sigils {nat['blooms']}   small pulses "
              f"{nat['pulses']}   blooms {nat['blooms']}   "
              f"rings that reached the foe {nat['hits']}"
              f"   ({nat['hits'] / max(1, nat['pulses'] + nat['blooms']):.0%})")
        print(f"    damage dealt across the cast: "
              f"{nat['dealt'] - nat['dealtAtCast']:.0f}")

        # ----------------------------------------------------------- [8] --
        print(f"\n[8] DOES IT FIGHT — {len(FOES)} foes x {len(seeds)} seeds\n")
        on = page.evaluate(FIGHT_JS, [ID, FOES, seeds, a.secs, False,
                                      a.pin, ids])
        durs = [r["dur"] for r in on]
        print(f"    {len(on)} matches   mean {statistics.mean(durs):.1f}s   "
              f"min {min(durs):.1f}   max {max(durs):.1f}   "
              f"timeouts {sum(1 for r in on if not r['over'])}   "
              f"win {statistics.mean(1 if r['won'] else 0 for r in on):.0%}   "
              f"casts/match {statistics.mean(r['ults'] for r in on):.2f}")
        check("no timeouts", all(r["over"] for r in on),
              f"{sum(1 for r in on if not r['over'])}/{len(on)}")
        check("it casts in every matchup",
              all(sum(r["ults"] for r in on if r["foe"] == f) > 0 for f in FOES),
              "min per-foe total "
              f"{min(sum(r['ults'] for r in on if r['foe'] == f) for f in FOES)}")

        # ----------------------------------------------------------- [9] --
        print(f"\n[9] WHAT THE CELL WAS FOR — hex, ult ON vs OFF, same seeds\n")
        off_ = page.evaluate(FIGHT_JS, [ID, FOES, seeds, a.secs, True,
                                        a.pin, ids])
        rows = []
        for lab, rs in (("ult OFF", off_), ("ult ON", on)):
            rows.append((lab,
                         statistics.mean(r["mean"] for r in rs),
                         statistics.mean(r["p2"] for r in rs),
                         statistics.mean(r["pCap"] for r in rs),
                         statistics.mean(r["firesPerS"] for r in rs),
                         statistics.mean(r["lock"] for r in rs)))
        print(f"    {'':<10}{'mean':>7}{'>=2':>7}{'at cap':>8}"
              f"{'fires/s':>9}{'lock':>7}")
        for lab, m_, p2, pc, fp, lk in rows:
            print(f"    {lab:<10}{m_:>7.2f}{p2:>7.0%}{pc:>8.1%}"
                  f"{fp:>9.3f}{lk:>7.1%}")
        d = {k: rows[1][i] - rows[0][i] for i, k in
             enumerate(["", "mean", "p2", "pCap", "fps", "lock"]) if k}
        print(f"    {'delta':<10}{d['mean']:>+7.2f}{d['p2']:>+7.1%}"
              f"{d['pCap']:>+8.1%}{d['fps']:>+9.3f}{d['lock']:>+7.1%}")
        out["hex"] = {"off": rows[0][1:], "on": rows[1][1:]}
        check("the Converse moves the number it was designed to move — "
              "hex at its CAP",
              d["pCap"] > 0.005,
              f"{rows[0][3]:.1%} -> {rows[1][3]:.1%} of the fight at 5 stacks")
        check("and the delivered lock with it",
              d["lock"] > 0.01,
              f"{rows[0][5]:.1%} -> {rows[1][5]:.1%}")

        assert not errors, errors[:4]

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED)" if bad else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1, default=str))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
