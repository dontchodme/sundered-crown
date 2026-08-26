#!/usr/bin/env python3
"""CAN THE WIND-UP EVER FINISH? -- before the ultimate is designed around it.

    python3 windup_probe.py --game ../02-chain/sc-twinshade-scrunch.html

Rick chose "can be broken -- the cast is lost" for the spin-up. That is the
option with real counterplay and it is also the one the Harrowing already
taught this project to check, because the Harrowing shipped with an 11.5% dud
rate nobody had measured.

**THE PROBLEM IS NOT HEX. IT IS EVERY HIT.** `takeHitstun` runs on every blow
landed, from anything, and sets `f.stun`. The chain drive reads

    const drive = f.stun > 0 ? 0 : spin * f.spinDir;

so ANY hit taken already stops the head being driven -- that behaviour exists
today and costs nothing. If "the cast is lost" is wired to the same condition,
the first blow the caster takes during the wind-up cancels the ultimate, and
"broken by a hex" quietly becomes "broken by anything at all".

So the design needs a THRESHOLD, and a threshold needs this number: how long a
stun-free window does this relic actually get?

Measures, on the provisional flail against a field:
  [1] hitstun events a second taken by the caster, and the share of time it
      spends stunned at all
  [2] the distribution of GAPS between stuns -- the honest answer to "would a
      1.2s wind-up ever complete"
  [3] the completion rate of a wind-up of length T, for several T, counted
      directly by walking the timeline rather than modelled from a rate

Writes nothing.
"""
from __future__ import annotations

import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

PROVISIONAL = {
    "id": "axiom", "name": "Provisional", "aff": "bloodsworn", "shape": "flail",
    "blades": [0], "reach": 96, "width": 22, "artW": 52, "dmg": 43.3,
    "spin": 2.2, "mode": "chain", "mass": 3.6, "onHit": {"hemorrhage": 2},
    "ult": {"name": "Placeholder", "charge": 16, "kind": "nova", "radius": 240,
            "dmg": 12, "apply": {"hemorrhage": 3}, "knock": 200,
            "tip": "PLACEHOLDER"},
    "blurb": "Provisional.",
}
FOES = ["thornwake", "censer", "ironhail", "heartwood", "lightkeeper",
        "spellbreaker", "dawnbringer", "grudgebearer"]

INJECT_JS = """(r) => { const w = AC.WEAPONS.find(x => x.id === r.id);
  for (const k of Object.keys(w)) delete w[k]; Object.assign(w, r); return "ok"; }"""

# The timeline is recorded per frame and the windows are counted afterwards in
# python, so "would a wind-up of length T complete" is answered by walking the
# real stun trace rather than by assuming stuns are Poisson. They are not --
# hitstun has diminishing returns (`stunDR`) and hits cluster into volleys.
TRACE_JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      let steps = 0, prevStun = 0;
      const stunStarts = [];
      let stunnedFrames = 0;
      while (!m.over && steps < 120 / DT){
        m.step(DT); steps++;
        const st = me.stun;
        if (st > prevStun + 1e-9) stunStarts.push(steps * DT);  // a fresh stun
        if (st > 0) stunnedFrames++;
        prevStun = st;
      }
      out.push({ foe: f, seed: s, dur: steps * DT, starts: stunStarts,
                 stunnedFrac: steps ? stunnedFrames / steps : 0 });
    }
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--seeds", type=int, default=10)
    A = ap.parse_args()
    g = (HERE / A.game).resolve()
    seeds = [7001 + i * 3571 for i in range(A.seeds)]

    with game(game_path=g) as (page, errors):
        page.evaluate(INJECT_JS, PROVISIONAL)
        rows = page.evaluate(TRACE_JS, ["axiom", FOES, seeds])
        if errors:
            print("PAGE ERRORS:", errors[:3])

    tot_dur = sum(r["dur"] for r in rows)
    tot_stun = sum(len(r["starts"]) for r in rows)
    print(f"\nWIND-UP PROBE -- {len(rows)} matches, {tot_dur:.0f}s of fight\n")
    print(f"[1] the caster takes {tot_stun/tot_dur:.3f} hitstun events a second "
          f"({tot_stun/len(rows):.1f} a match)")
    print(f"    and is stunned for "
          f"{100*statistics.mean(r['stunnedFrac'] for r in rows):.1f}% of all frames\n")

    gaps = []
    for r in rows:
        marks = [0.0] + r["starts"] + [r["dur"]]
        gaps += [b - a for a, b in zip(marks, marks[1:])]
    gaps.sort()
    q = lambda p: gaps[min(len(gaps) - 1, int(p * len(gaps)))]
    print(f"[2] gaps between stuns, {len(gaps)} of them")
    print(f"    median {statistics.median(gaps):.2f}s   mean {statistics.mean(gaps):.2f}s")
    print(f"    p25 {q(.25):.2f}s   p75 {q(.75):.2f}s   p90 {q(.90):.2f}s   max {gaps[-1]:.2f}s\n")

    print(f"[3] a wind-up starting at a UNIFORMLY RANDOM moment of the fight:")
    print(f"    {'wind-up':>9}{'completes':>11}{'attempts':>10}")
    for T in (0.4, 0.6, 0.8, 1.0, 1.2, 1.6, 2.0):
        ok = tries = 0
        for r in rows:
            st = r["starts"]
            # every 0.1s of the fight is a candidate start; the window survives
            # if no stun begins inside it
            t = 0.0
            while t + T <= r["dur"]:
                tries += 1
                if not any(t < s <= t + T for s in st): ok += 1
                t += 0.1
        print(f"    {T:>8.1f}s{100*ok/max(1,tries):>10.0f}%{tries:>10}")
    print("\n    This is the ceiling, not the answer: it assumes the bar fills at a")
    print("    moment unrelated to the fighting, and in practice a bar fills BECAUSE")
    print("    of an exchange, so real casts start in busier weather than these.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
