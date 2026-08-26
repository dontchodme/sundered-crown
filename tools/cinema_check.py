#!/usr/bin/env python3
"""Try to break the CINEMA director's one promise: it cannot change the fight.

Three independent attacks, in increasing order of how much they would hurt:

  1. ENGINE A/B -- the same seeds through the unpatched build and the patched
     one. Every field of every summary must match. This catches a stray
     `this.rng()` draw introduced by the beat() calls, which is the realistic
     way this kind of patch corrupts a sim.

  2. TIME-SCALE INVARIANCE -- the same match, driven through the real frame
     loop, at wall rates from 1.0 down to 0.05, including a hard freeze. If
     feeding the fixed-step accumulator less wall time changed anything, this
     is where it shows. This is the claim the whole feature rests on.

  3. PRESCAN FIDELITY -- the beat list from the headless prescan must equal the
     beat list the live match actually produces, beat for beat, to the
     millisecond. If it does not, the director is cutting to moments that never
     happen.

  python3 cinema_check.py --a sc-sil.html --b sc-cinema.html --n 40
  python3 cinema_check.py --selftest      # prove attack 1 can actually fail
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).parent

IDS = ("dawnbringer,widowmaker,grudgebearer,thornwake,gravemourn,"
       "spellbreaker,ironhail,lightkeeper,farwarden")

# Seeds are generated inside the page by an LCG so the two builds cannot drift
# through Python-side ordering or float formatting.
SWEEP_JS = r"""
([ids, n, seed0]) => {
  const have = new Set(AC.WEAPONS.map(w => w.id));
  const missing = ids.filter(i => !have.has(i));
  if (missing.length) return { missing };
  const out = [];
  let s = seed0 >>> 0;
  for (let i = 0; i < ids.length; i++)
    for (let j = i + 1; j < ids.length; j++)
      for (let k = 0; k < n; k++) {
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        out.push(AC.simulate(ids[i], ids[j], s));
      }
  return { rows: out };
}
"""

# Drive the REAL frame loop by hand at a stated wall rate, rather than calling
# simulate(). simulate() bypasses the accumulator entirely, so it could not
# possibly detect a time-scale bug -- the bug would live in the loop it skips.
RATE_JS = r"""
([idA, idB, seed, rate, freezeAt]) => {
  const m = new AC.Match(idA, idB, seed);
  const dt = AC.CONFIG.physics.dt;
  let acc = 0, guard = 0, wall = 0;
  const RAW = 1 / 60;                       // a fixed 60fps frame
  while (!m.over && guard++ < 400000) {
    wall += RAW;
    // a hard freeze in the middle of the fight, exactly as the director does it
    // gate the freeze on WALL time -- m.t does not advance while frozen, so a
    // sim-time gate would never open again.
    const ts = (freezeAt > 0 && wall > freezeAt && wall < freezeAt + 0.5) ? 0 : rate;
    acc += RAW * ts;
    let steps = 0;
    while (acc >= dt && steps < 4000) { m.step(dt); acc -= dt; steps++; }
  }
  const s = m.summary();
  return { summary: s, beats: m.beats.map(b => [ +b.t.toFixed(4), b.kind,
             b.dmg | 0, b.crit ? 1 : 0, b.fatal ? 1 : 0 ]) };
}
"""

# Drive the LIVE path end to end: CINE.pump for stepping and CINE.drawLerped
# for the frame. The interpolator overwrites geometry on the fighters and the
# particle arrays, draws, and writes the saved numbers back -- so if the
# restore is not exact, or if the sim ever observes an interpolated value, the
# match that comes out will not be the one simulate() produces.
LIVE_JS = r"""
([idA, idB, seed, fps]) => {
  const plan = window.cinePlan(idA, idB, seed);
  CINE.on = true; CINE.interp = true; CINE.reset();
  CINE.plan = plan.cuts; CINE.acc = 0;
  const m = new AC.Match(idA, idB, seed); m.introT = 0;
  AC.__inject(m);
  const raw = 1 / fps;
  let guard = 0, cuts = 0;
  while (!m.over && guard++ < 400000) {
    const alpha = CINE.pump(raw, m, 1);
    if (CINE.phase === "whip") cuts++;
    if (alpha > 0) CINE.drawLerped(AC.renderer, m, alpha);
    else AC.renderer.draw(m);
  }
  return { summary: m.summary(), lerpedFrames: cuts };
}
"""

PRESCAN_JS = r"""
([idA, idB, seed]) => {
  // what the director sees before the match
  const plan = window.cinePlan(idA, idB, seed);
  // what the match actually produces
  const m = new AC.Match(idA, idB, seed);
  const dt = AC.CONFIG.physics.dt;
  let g = 0;
  while (!m.over && g++ < 200000) m.step(dt);
  const key = b => [ +b.t.toFixed(4), b.kind, b.dmg | 0, b.fatal ? 1 : 0 ].join("|");
  return {
    planned: plan.scored.map(key),
    actual:  m.beats.map(key),
    cuts:    plan.cuts.map(c => ({ t: +c.t.toFixed(2), tier: c.tier,
                                   score: +c.score.toFixed(3), fatal: !!c.fatal,
                                   why: c.why })),
    err: plan.err,
  };
}
"""


def sweep(path: pathlib.Path, ids: list[str], n: int, seed0: int):
    with game(game_path=path) as (page, errors):
        r = page.evaluate(SWEEP_JS, [ids, n, seed0])
        if errors:
            raise SystemExit(f"page errors in {path.name}: {errors[:3]}")
    if "missing" in r:
        raise SystemExit(f"{path.name} is missing relics: {r['missing']}")
    return r["rows"]


def attack_1(a: pathlib.Path, b: pathlib.Path, ids: list[str], n: int,
             sabotage: bool = False) -> bool:
    print(f"\n[1] ENGINE A/B  {a.name} vs {b.name}  ({len(ids)} relics x {n} seeds)")
    ra = sweep(a, ids, n, 0xC17E5A)
    rb = sweep(b, ids, n, 0xC17E5A)
    if sabotage:
        # Prove the comparison can fail: corrupt one field of one row.
        rb = json.loads(json.dumps(rb))
        rb[len(rb) // 2]["duration"] = rb[len(rb) // 2]["duration"] + 0.01
    if len(ra) != len(rb):
        print(f"    FAIL: {len(ra)} rows vs {len(rb)}")
        return False
    bad = [i for i, (x, y) in enumerate(zip(ra, rb)) if x != y]
    print(f"    matched {len(ra) - len(bad)}/{len(ra)} summaries, field for field")
    if bad:
        i = bad[0]
        print(f"    FAIL: first divergence at row {i}")
        for k in ra[i]:
            if ra[i][k] != rb[i].get(k):
                print(f"      {k}: {ra[i][k]!r} -> {rb[i].get(k)!r}")
    print("    RESULT:", "FAIL" if bad else "PASS")
    return not bad


RATES = [1.0, 0.5, 0.13, 0.05]


def attack_2(b: pathlib.Path, pairs, n: int) -> bool:
    print(f"\n[2] TIME-SCALE INVARIANCE  rates {RATES} + a 0.5s hard freeze")
    ok = True
    with game(game_path=b) as (page, errors):
        for (idA, idB) in pairs:
            for k in range(n):
                seed = (0x5EED * (k + 1) + 7919) & 0xFFFFFFFF
                ref = page.evaluate(RATE_JS, [idA, idB, seed, 1.0, 0])
                for rate in RATES[1:]:
                    got = page.evaluate(RATE_JS, [idA, idB, seed, rate, 0])
                    if got != ref:
                        ok = False
                        print(f"    FAIL {idA} v {idB} seed {seed} at rate {rate}")
                        print(f"      {ref['summary']}")
                        print(f"      {got['summary']}")
                frz = page.evaluate(RATE_JS, [idA, idB, seed, 1.0, 6.0])
                if frz != ref:
                    ok = False
                    print(f"    FAIL {idA} v {idB} seed {seed} with a mid-fight freeze")
        if errors:
            print(f"    page errors: {errors[:3]}")
            ok = False
    tot = len(pairs) * n * (len(RATES) - 1 + 1)
    print(f"    {tot} slowed/frozen runs compared against their 1.0x reference")
    print("    RESULT:", "PASS" if ok else "FAIL")
    return ok


def attack_3(b: pathlib.Path, pairs, n: int) -> bool:
    print(f"\n[3] PRESCAN FIDELITY  the plan vs what actually happens")
    ok = True
    shown = 0
    with game(game_path=b) as (page, errors):
        for (idA, idB) in pairs:
            for k in range(n):
                seed = (0xBEE5 * (k + 3) + 104729) & 0xFFFFFFFF
                r = page.evaluate(PRESCAN_JS, [idA, idB, seed])
                if r["err"]:
                    print(f"    prescan error: {r['err']}")
                    ok = False
                    continue
                if r["planned"] != r["actual"]:
                    ok = False
                    print(f"    FAIL {idA} v {idB} seed {seed}: "
                          f"{len(r['planned'])} planned vs {len(r['actual'])} actual")
                    for i, (x, y) in enumerate(zip(r["planned"], r["actual"])):
                        if x != y:
                            print(f"      first divergence at beat {i}: {x} -> {y}")
                            break
                elif shown < 2:
                    shown += 1
                    print(f"    {idA} v {idB} seed {seed}: "
                          f"{len(r['actual'])} beats, cut list:")
                    for c in r["cuts"]:
                        tag = "KILL" if c["fatal"] else f"T{c['tier']}"
                        print(f"      {c['t']:6.2f}s  {tag:4}  {c['score']:5.2f}  "
                              f"{', '.join(c['why'])}")
        if errors:
            print(f"    page errors: {errors[:3]}")
            ok = False
    print("    RESULT:", "PASS" if ok else "FAIL")
    return ok


def attack_4(b: pathlib.Path, pairs, n: int) -> bool:
    print(f"\n[4] INTERPOLATED RENDER  the live path, drawing between fixed steps")
    ok = True
    with game(game_path=b) as (page, errors):
        page.evaluate("AC.setResolution(360, 640)")
        for (idA, idB) in pairs:
            for k in range(n):
                seed = (0x1EA7 * (k + 5) + 7717) & 0xFFFFFFFF
                got = page.evaluate(LIVE_JS, [idA, idB, seed, 60])
                ref = page.evaluate("([a,b,s]) => AC.simulate(a,b,s)", [idA, idB, seed])
                if got["summary"] != ref:
                    ok = False
                    print(f"    FAIL {idA} v {idB} seed {seed}")
                    for key in ref:
                        if ref[key] != got["summary"].get(key):
                            print(f"      {key}: {ref[key]!r} -> {got['summary'].get(key)!r}")
        if errors:
            print(f"    page errors: {errors[:3]}")
            ok = False
    print(f"    {len(pairs) * n} matches rendered through the interpolator, "
          f"compared against simulate()")
    print("    RESULT:", "PASS" if ok else "FAIL")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="sc-sil.html")
    ap.add_argument("--b", default="sc-cinema.html")
    ap.add_argument("--ids", default=IDS)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    a, b = HERE / args.a, HERE / args.b
    if not a.exists():
        a = pathlib.Path(args.a)
    if not b.exists():
        b = pathlib.Path(args.b)
    ids = args.ids.split(",")
    pairs = [(ids[0], ids[1]), (ids[2], ids[3]), (ids[6], ids[7])]

    if args.selftest:
        print("SELFTEST: attack 1 is run against a deliberately corrupted result.")
        good = attack_1(a, b, ids[:3], 4, sabotage=True)
        print("\nSELFTEST", "FAILED (the check cannot detect a change!)" if good
              else "PASS (the check detects a one-field change)")
        return 0 if not good else 1

    r1 = attack_1(a, b, ids, args.n)
    r2 = attack_2(b, pairs, 4)
    r3 = attack_3(b, pairs, 4)
    r4 = attack_4(b, pairs, 2)
    print("\n" + "=" * 62)
    ok = r1 and r2 and r3 and r4
    print("CINEMA IS PRESENTATION-ONLY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
