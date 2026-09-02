"""FIND A FIGHT WHOSE LAST CROSSWEAVE WINDOW ENDS JUST BEFORE THE KILL.

`cinema_clip` has `--lead N` (N seconds back from the killing blow) and no
start-at, so a short clip of JUST the ultimate needs a seed where the window
happens to sit at the end of the fight. This finds one.
"""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(rid, f, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let had = false, casts = [], open0 = -1;
    let i = 0;
    while (!m.over && i < secs / DT){
      m.step(DT); i++;
      if (me.ultNet && !had){ had = true; open0 = m.t; }
      if (!me.ultNet && had){ had = false; casts.push([open0, m.t]); }
    }
    if (had) casts.push([open0, m.t]);
    if (!casts.length) continue;
    const last = casts[casts.length - 1];
    out.push({ foe: f, seed: sd, t: +m.t.toFixed(2),
               win: me.hp > th.hp, casts: casts.length,
               open: +last[0].toFixed(2), close: +last[1].toFixed(2),
               gap: +(m.t - last[1]).toFixed(2) });
  }
  return out;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
ap.add_argument("--foes", default="thornwake,paradox,heartwood,slagheart,axiom,widowmaker")
ap.add_argument("--n", type=int, default=40)
a = ap.parse_args()
gp = resolve_game(a.game)
seeds = [30011 + 101 * i for i in range(a.n)]
with game(game_path=gp) as (page, errors):
    rows = page.evaluate(JS, ["gloamwire", a.foes.split(","), seeds, 120.0])
    assert not errors, errors[:4]

# the window must CLOSE close to the end, and OPEN late enough that a short
# lead reaches back past it -- so the whole ultimate is inside the clip.
ok = [r for r in rows if 0.2 <= r["gap"] <= 2.2 and r["win"]]
ok.sort(key=lambda r: (abs(r["gap"] - 1.0), -(r["close"] - r["open"])))
print(f"\n  {len(rows)} fights, {len(ok)} with the last window ending 0.2-2.2s "
      f"before the kill\n")
print(f"    {'foe':<14}{'seed':>7}{'fight':>8}{'opens':>8}{'closes':>8}"
      f"{'gap':>7}{'lead':>7}")
for r in ok[:10]:
    lead = r["t"] - r["open"] + 0.8
    print(f"    {r['foe']:<14}{r['seed']:>7}{r['t']:>8.1f}{r['open']:>8.1f}"
          f"{r['close']:>8.1f}{r['gap']:>7.1f}{lead:>7.1f}")
if ok:
    b = ok[0]
    print(f"\n    PICK: --a gloamwire --b {b['foe']} --seed {b['seed']} "
          f"--lead {b['t'] - b['open'] + 0.8:.1f}")
