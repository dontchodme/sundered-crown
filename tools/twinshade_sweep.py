#!/usr/bin/env python3
"""THE BLADE, NARROWED AGAINST THE FIELD ON PINNED SEEDS.

    python3 twinshade_sweep.py --blades 10.38,8,6,4.5,3

PINNED, because the engine's own `batch()` draws from `Math.random()`: two
candidates measured on two different populations differ by more than the thing
being measured, and a 2pp gap is unreadable. Every candidate here fights the
same eighteen foes on the same seed list.

DO NOT DERIVE THIS NUMBER. v36 registered a prediction from the factored model
on this exact cell — umbral's modifier should sit below 1.0 because curse
compounds — and it was falsified by nine points, because curse's value depends
on WHEN in the fight a hit lands and no `mod[school]` term can express that.
The model has now been wrong about this cell once. Measure it.

`dmg` is overridden AT RUNTIME rather than rebuilt per candidate, because
`w.dmg` is read in exactly one place in the simulation (`resolveHit`) and a
rebuild per candidate costs a minute each. `--check-rebuild` proves that is the
same measurement by running one candidate both ways — an instrument that has
not been checked against the thing it is standing in for is a guess with a
table around it.

REPORTED ALONGSIDE THE WINRATE, because the winrate is not the design axis:

    shadeShare   the fraction of this relic's landed blows struck by a COPY.
                 If it is small the ultimate is decoration; if it approaches
                 two thirds the relic is its cooldown and nothing else.
    killed/expired  how copies ended. The kill share is this ultimate's
                 equivalent of the Harrowing's dud rate — it is the foe's
                 counterplay, measured, and it is the number that says whether
                 "the copies can be killed" is a real sentence.
    healed       mean hp returned by lifesteal per match.
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
ID = "twinshade"

SWEEP_JS = """([id, foes, seeds, blade]) => {
  const W = AC.WEAPONS.find(x => x.id === id);
  const saved = W.dmg;
  if (blade !== null) W.dmg = blade;

  /* Instrumented on the PROTOTYPE, and reset per match. Counting shade blows
     by asking the engine is the only honest way: `owner.hits` deliberately
     INCLUDES them (verify.py's contact floor needs it to), so the two cannot
     be separated after the fact. */
  const P = AC.Match.prototype;
  let shadeHits = 0, healed = 0;
  const oh = P.resolveHit;
  P.resolveHit = function(self, foe){
    if (self.shade) shadeHits++;
    const before = self.hp;
    const r = oh.apply(this, arguments);
    if (self.hp > before) healed += self.hp - before;
    return r;
  };
  const ok = P.killShade;
  let killed = 0;
  P.killShade = function(i){ killed++; return ok.apply(this, arguments); };
  const oe = P.endSplit;
  let expired = 0;
  P.endSplit = function(f){
    if (f.ultSplit) expired += this.shades.filter(s => s.shade.owner === f).length;
    return oe.apply(this, arguments);
  };

  let wins = 0, total = 0, casts = 0, hits = 0;
  let K = 0, E = 0, H = 0, SH = 0, TO = 0, TOwin = 0;
  const durs = [], rows = [];
  for (const foe of foes){
    let w = 0;
    for (const s of seeds){
      shadeHits = 0; healed = 0; killed = 0; expired = 0;
      const m = new AC.Match(id, foe, s);
      const dt = AC.CONFIG.physics.dt;
      let g = 0;
      while (!m.over && g++ < 200000) m.step(dt);
      const me = m.a.w.id === id ? m.a : m.b;
      if (m.winner === me) w++;
      if (m.reason === "timeout"){ TO++; if (m.winner === me) TOwin++; }
      durs.push(m.t);
      casts += me.ultsFired;
      hits  += me.hits;
      SH += shadeHits; H += healed; K += killed; E += expired;
    }
    rows.push({ foe, w, n: seeds.length });
    wins += w; total += seeds.length;
  }
  P.resolveHit = oh; P.killShade = ok; P.endSplit = oe;
  W.dmg = saved;
  durs.sort((x, y) => x - y);
  return { blade: blade === null ? saved : blade,
           wins, total, rows, casts, hits, shadeHits: SH,
           killed: K, expired: E, healed: +H.toFixed(0),
           timeouts: TO, timeoutWins: TOwin,
           medDur: +durs[durs.length >> 1].toFixed(1) };
}"""


def run(page, foes, seeds, blade):
    return page.evaluate(SWEEP_JS, [ID, foes, seeds, blade])


def line(r):
    n = r["total"]
    win = 100 * r["wins"] / n
    share = 100 * r["shadeHits"] / max(1, r["hits"])
    ends = r["killed"] + r["expired"]
    killpct = 100 * r["killed"] / max(1, ends)
    to = 100 * r["timeouts"] / n
    return (f"  {r['blade']:>7.2f}  {win:>6.1f}%  {share:>7.0f}%  "
            f"{killpct:>7.0f}%  {r['healed']/n:>7.1f}  "
            f"{r['casts']/n:>6.2f}  {r['medDur']:>6.1f}s  {to:>6.0f}%")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-twinshade.html")
    ap.add_argument("--blades", default="10.38,8,6.5,5,4,3")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20260819)
    ap.add_argument("--check-rebuild", type=float, default=None,
                    help="rebuild at this blade and compare against the "
                         "runtime override on the same seeds")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    blades = [float(x) for x in A.blades.split(",")]
    seeds = [A.seed + i * 7919 for i in range(A.n)]

    with game(game_path=g) as (page, errs):
        foes = [w for w in page.evaluate(
            "() => AC.WEAPONS.map(w => w.id)") if w != ID]
        print(f"game   {g.name}")
        print(f"field  {len(foes)} foes x {len(seeds)} pinned seeds = "
              f"{len(foes)*len(seeds)} matches a candidate\n")
        print("    blade     win   shade%   killed%  healed   casts    dur")
        print("    " + "-" * 60)
        out = []
        for b in blades:
            r = run(page, foes, seeds, b)
            out.append(r)
            print(line(r))
        if errs:
            print("\nPAGE ERRORS:", errs[:3])

    print("\n  shade%   share of this relic's landed blows struck by a COPY")
    print("  killed%  share of copies that ENDED by being killed rather than "
          "expiring —\n           the foe's counterplay, measured")
    print("  healed   mean hp returned by lifesteal per match")
    print("  timeout  share of matches that hit CONFIG.timeout. A blade that "
          "raises this is\n           being scored by checkEnd's hp-FRACTION "
          "tiebreak and not by the relic.")

    if A.check_rebuild is not None:
        b = A.check_rebuild
        tmp = HERE / "../02-chain/_sweepcheck.html"
        print(f"\n=== INSTRUMENT CHECK — blade {b} two ways ===")
        subprocess.run([sys.executable, "twinshade_build.py",
                        "--src", "../02-chain/sc-health18.html",
                        "--out", "../02-chain/_sweepcheck.html",
                        "--blade", str(b)],
                       cwd=HERE, check=True, capture_output=True)
        with game(game_path=tmp.resolve()) as (page, errs):
            rb = run(page, foes, seeds, None)
        with game(game_path=g) as (page, errs):
            ro = run(page, foes, seeds, b)
        same = rb["wins"] == ro["wins"] and rb["hits"] == ro["hits"]
        print(f"  rebuilt at {b}:          {rb['wins']}/{rb['total']} wins, "
              f"{rb['hits']} hits, {rb['shadeHits']} by copies")
        print(f"  runtime override at {b}: {ro['wins']}/{ro['total']} wins, "
              f"{ro['hits']} hits, {ro['shadeHits']} by copies")
        print(f"  {'IDENTICAL — the override measures the same thing' if same else 'DIFFERENT — the sweep above is measuring something else'}")
        tmp.unlink(missing_ok=True)
        return 0 if same else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
