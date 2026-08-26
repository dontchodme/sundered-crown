#!/usr/bin/env python3
"""Find fights worth filming: several qualifying cuts, and a finish that earns one.

A full-match video of a fight the director never fires on demonstrates nothing.
This scans seeds and reports the ones with a real cut list.
"""
from __future__ import annotations
import pathlib, sys
from scpage import game
HERE = pathlib.Path(__file__).parent
JS = r"""
([pairs, n, seed0]) => {
  let s = seed0 >>> 0; const out = [];
  for (const [a, b] of pairs) {
    for (let k = 0; k < n; k++) {
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const p = window.cinePlan(a, b, s); if (p.err) continue;
      const kill = p.cuts.find(c => c.fatal);
      out.push({ a, b, seed: s, dur: +p.dur.toFixed(1), cuts: p.cuts.length,
                 kill: !!kill,
                 list: p.cuts.map(c => ({ t: +c.t.toFixed(1),
                                          tier: c.fatal ? "KILL" : "T" + c.tier,
                                          score: +c.score.toFixed(2),
                                          kind: c.kind || "hit", n: c.n || 1,
                                          why: (c.why || []).join(", ") })) });
    }
  }
  return out;
}
"""
PAIRS = [["gravemourn","dawnbringer"],["grudgebearer","thornwake"],
         ["ironhail","widowmaker"],["spellbreaker","lightkeeper"],
         ["farwarden","gravemourn"],["dawnbringer","grudgebearer"],
         ["ironhail","thornwake"],["farwarden","spellbreaker"]]
def main():
    with game(game_path=(HERE/"sc-cinema.html").resolve()) as (page, err):
        rows = page.evaluate(JS, [PAIRS, 14, 0xF11E])
        if err: print("errors", err[:2])
    # Prefer fights that DEMONSTRATE the three criteria rather than merely
    # having cuts: a volley, a high-closing single, a long bolt.
    def flavour(r):
        k = {c["kind"] for c in r["list"]}
        w = " ".join(c["why"] for c in r["list"])
        return (("volley" in k), ("closing at" in w), ("px of flight" in w))
    good = [r for r in rows if r["cuts"] >= 2 and 26 <= r["dur"] <= 50]
    good.sort(key=lambda r: (-sum(flavour(r)), -r["cuts"], r["dur"]))
    seen=set(); out=[]
    for r in good:
        key=(r["a"],r["b"])
        if key in seen: continue
        seen.add(key); out.append(r)
    for r in out[:6]:
        print(f"{r['a']} v {r['b']}  seed {r['seed']}  {r['dur']}s  "
              f"{r['cuts']} cuts  "
              f"[{'+'.join(n for n, on in zip(('volley','pace','reach'), flavour(r)) if on) or 'plain'}]")
        for c in r["list"]:
            tag = f"{c['kind']}({c['n']})" if c["kind"] == "volley" else c["kind"]
            print(f"    {c['t']:6.1f}s  {c['tier']:4}  {c['score']:5.2f}  "
                  f"{tag:10} {c['why']}")
    return 0
if __name__ == "__main__":
    sys.exit(main())
