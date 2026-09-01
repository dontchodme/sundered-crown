"""Pick a seed to FILM. Gate 2 item 4: a filmstrip before any tuning.

Not a probe and not a gate -- a search for one fight in which a viewer can
actually see what Crossweave is. Three things have to be on screen and the
first one is the one a bad seed loses:

  THE CAST HAS TO BE EARLY. The window is 4.1s of a ~45s fight and it fires
  about twice. A cast at 38s is a clip nobody watches to.

  THE FAN HAS TO BE SEEN AS A FAN. That means volleys loosed while the two
  fighters are far enough apart for three arrows to separate -- at 60 units
  the fan is a smear and at 400 it is three distinct lines.

  AND THE SHOVE HAS TO LAND. `lightOnly` volleys are the ones where a viewer
  sees the ball thrown sideways by nothing, which is the honest state of stage
  3 and the thing Rick is being asked to judge.

Runtime only. NOTHING is written to any build.
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RELIC = "gloamwire"

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const own = me === m.a ? "a" : "b";
      const R = AC.CONFIG.physics.ballR;

      let firstCast = -1, casts = 0, hadNet = false;
      let volleys = 0, both = 0, lightOnly = 0, arrowOnly = 0;
      let sepSum = 0, sepN = 0;
      const V = new Map(), spent = new Set(), born = new Set();

      let i = 0;
      while (!m.over && i < secs / DT){
        m.step(DT); i++;
        if (me.ultNet){
          if (!hadNet){ hadNet = true; casts++; if (firstCast < 0) firstCast = m.t; }
        } else hadNet = false;
        for (const s of m.shots){
          if (!s.net || s.own !== own) continue;
          if (!born.has(s)){
            born.add(s);
            if (!V.has(s.volley)){
              V.set(s.volley, { a: false, l: false });
              volleys++;
              /* the separation the volley was loosed at -- a fan needs room */
              sepSum += Math.hypot(me.x - th.x, me.y - th.y) - 2 * R; sepN++;
            }
          }
          if (s.strandSpent && !spent.has(s)){
            spent.add(s);
            const v = V.get(s.volley); if (v) v.l = true;
          }
          /* `_pHit` IS THE PROBE'S TAG AND THIS TOOL DOES NOT INSTALL IT, so
             the `both` and `arrowOnly` columns below are ALWAYS ZERO and mean
             nothing. Left in rather than deleted because the ranking does not
             use them and removing them would make the printed table look like
             it had measured something it had not. The real split is
             `gloamwire_relic_probe [3]`: both 16.2%, arrow-only 3.4%. */
          if (s._pHit){ const v = V.get(s.volley); if (v) v.a = true; }
        }
      }
      for (const v of V.values()){
        if (v.a && v.l) both++;
        else if (v.l) lightOnly++;
        else if (v.a) arrowOnly++;
      }
      out.push({ foe: foeId, seed: sd, t: +m.t.toFixed(1),
                 win: me.hp > th.hp, casts,
                 firstCast: +firstCast.toFixed(1),
                 volleys, both, lightOnly, arrowOnly,
                 sep: sepN ? +(sepSum / sepN).toFixed(0) : 0 });
    }
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
    ap.add_argument("--foes", default="thornwake,paradox,heartwood,slagheart")
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--secs", type=float, default=120.0)
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [30011 + 101 * i for i in range(a.n)]
    foes = a.foes.split(",")

    with game(game_path=gp) as (page, errors):
        rows = page.evaluate(JS, [RELIC, foes, seeds, a.secs])
        assert not errors, errors[:4]

    # AN EARLY CAST IS WORTH MORE THAN A GOOD ONE. Everything else is a
    # tie-break: a viewer who has stopped watching cannot judge anything.
    def score(r):
        if r["casts"] < 2 or r["firstCast"] < 0:
            return -1e9
        return (-3.0 * r["firstCast"]
                + 2.0 * r["both"] + 1.5 * r["lightOnly"]
                + 0.02 * r["sep"]
                + (6 if 32 <= r["t"] <= 55 else 0))

    rows.sort(key=score, reverse=True)
    print(f"\n{gp.name}   {len(foes)} foes x {len(seeds)} seeds\n")
    print("    (`both` and `arrow` are always 0 here -- this tool does not "
          "install the probe's hit tag. Rank on `light` and `1st`;")
    print("     the real split is in gloamwire_relic_probe [3].)")
    print("")
    print(f"    {'foe':<14}{'seed':>7}{'dur':>7}{'win':>6}{'casts':>7}"
          f"{'1st':>7}{'volleys':>9}{'both':>6}{'light':>7}{'sep':>6}")
    for r in rows[:12]:
        print(f"    {r['foe']:<14}{r['seed']:>7}{r['t']:>7.1f}"
              f"{'W' if r['win'] else 'L':>6}{r['casts']:>7}"
              f"{r['firstCast']:>7.1f}{r['volleys']:>9}{r['both']:>6}"
              f"{r['lightOnly']:>7}{r['sep']:>6}")
    b = rows[0]
    print(f"\n    PICK: --a {RELIC} --b {b['foe']} --seed {b['seed']}")
    print(f"          first cast at {b['firstCast']:.1f}s of a {b['t']:.1f}s "
          f"fight, {b['casts']} casts, mean separation {b['sep']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
