"""FIND FIGHTS WHOSE STATIC WINDOW IS WORTH FILMING.

`cinema_clip` has `--at T --window N`, so a clip of JUST the ultimate needs the
match time a cast opens at. This prints them, biggest swarm first, because gate
2's question is "does the arena read as full of pink lightning by the fourth
second" and a cast that grew nothing cannot answer it.

    python _storm_pick.py --game ../02-chain/sc-storm.html --n 12

`open` is the cast, `close` is the detonation. Film `--at open-1 --window 10.5`.
"""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(rid, f, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    let open0 = -1, peak = 0, i = 0;
    while (!m.over && i < secs / DT){
      const had = !!m.storm;
      const S = m.storm;
      const was = S ? { peak: S.peak, blows: S.blows, eaten: S.eaten,
                        alive: S.bolts.length, ins: m.inset } : null;
      m.step(DT); i++;
      if (m.storm && !had) open0 = m.t;
      if (m.storm) peak = Math.max(peak, m.storm.bolts.length);
      if (!m.storm && had && open0 >= 0){
        out.push({ foe: f, seed: sd, open: +open0.toFixed(2),
                   close: +m.t.toFixed(2), peak: was.peak, blows: was.blows,
                   eaten: was.eaten, alive: was.alive,
                   ins: +was.ins.toFixed(0),
                   dur: +m.t.toFixed(1), over: m.over });
        open0 = -1; peak = 0;
      }
    }
  }
  return out;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-storm.html")
ap.add_argument("--relic", default="arclight")
ap.add_argument("--foes", default="ironhail,axiom,lastlight,grudgebearer,"
                                  "twinshade,vesper,thornshear,duskreave")
ap.add_argument("--n", type=int, default=8)
ap.add_argument("--seed0", type=int, default=11961)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--open-hall", type=float, default=1e9,
                help="only casts that opened at an inset below this. The swarm "
                     "the design priced is the one in the OPEN hall.")
A = ap.parse_args()
HERE = pathlib.Path(__file__).parent
seeds = [A.seed0 + 977 * i for i in range(A.n)]

with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
    rows = pg.evaluate(JS, [A.relic, A.foes.split(","), seeds, A.secs])

rows = [r for r in rows if r["ins"] < A.open_hall]
rows.sort(key=lambda r: -r["peak"])
print(f"\n{len(rows)} casts, biggest swarm first\n")
print(f"  {'foe':<14} {'seed':>7}  {'open':>6} {'close':>6}  {'inset':>5}  "
      f"{'blows':>5} {'peak':>5} {'eaten':>5} {'alive':>5}   film")
for r in rows[:20]:
    print(f"  {r['foe']:<14} {r['seed']:>7}  {r['open']:>6.2f} "
          f"{r['close']:>6.2f}  {r['ins']:>5}  {r['blows']:>5} {r['peak']:>5} "
          f"{r['eaten']:>5} {r['alive']:>5}   "
          f"--at {max(0, r['open']-1):.1f} --window 10.5")
