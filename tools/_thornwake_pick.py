#!/usr/bin/env python3
"""A BRAMBLESNARE WINDOW, TO FILM. v113.

    python _thornwake_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape, by way of `_spellbreaker_pick.py` (its exclusions,
its voice count and its clip rules). What has to be ON SCREEN (and in the ear)
is the whole of v84 §4 as built at stage 6 (v113 §5): the cast -- the rustle
and creak, and the scythe's blade greening; blows landing in the window, each
one opening a bramble where it landed (a dry crackle, the tangle growing out of
the hit point); the foe stepping into one -- SNARED, the creak-and-crack and
the thorn shoots clenching its rim; the foe BITTEN inside a bramble -- the soft
snap, the thorn flash on its rim, the ENTANGLE tag counting; and THE CLOSE, so
the window must close BY ITS CLOCK with both alive (the green fading off the
blade; a death's close or a kill is the death voice's moment and the
verdict's). The brambles outlive the window, so bites in the clip's tail after
the close are scored too.

A window qualifies (`all`) only if it shows every one of those -- one cast
voice, a clock close, at least two brambles, a snare and three bites -- and
nothing on screen takes them over: no cast of the foe's and no other banner
anywhere in the clip (lead to tail, from 2.4 s before the clip: a banner's
life), not the scrunch card (it opens at the match's first clank for
`scrunch.ease x 2 + intro` seconds and shrinks the arena under it), and the
match must not end inside the clip (`kill`). The qualifying windows are scored
on the brambles, the snares, the bites (and the bites after the close), and the
share of window frames with the foe held; the tool prints the `--at` and
`--window` to hand `cinema_clip` (lead 1.2 s, tail 1.8 s, `--end-at-window`),
with `dur` the window's length in MATCH time: the window clock stops in the
freezes, so 8 + 3 would end the clip before the close. RICK WATCHES THE ULT'S
WINDOW AND NOT THE WHOLE FIGHT. Thornwake plays side A, as the clip does.

Left out of the pool by default: Twinshade (`--exclude`), whose shades are a
second body the brambles do not test; and every foe of Thornwake's own
affinity (`--keep-aff` puts them back): a verdant foe wears the same green,
entangles with its own school and plants its own vines, and the clip has to
show WHOSE brambles snare it.

The voices are counted through `AC.SFX.play`, which is a no-op headless: the
call is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "thornwake"
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro;
  if (typeof AC.Match.prototype.tickBrier !== "function" || !/thornwake-crackle/.test(AC.SFX.play.toString()))
    return { err: "not a stage-6 Bramblesnare link (no tickBrier, no crackle voice)" };
  let V = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (V && kind === "ult" && q && /^thornwake(-crackle|-snare|-bite)?$/.test(q.w)) V.push(q.w);
    return oPlay.call(this, kind, q);
  };
  const out = [];
  try {
    for (const foe of foes) for (const sd of seeds){
      const m = new AC.Match(rid, foe, sd);
      const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
      let step = 0, win = null, best = null, clank1 = null;
      const wins = [], foeCastT = [], biteT = [];
      while (!m.over && step < secs / DT){
        const Z0 = me.ultBramble;
        const u0 = th.ultsFired || 0, bn0 = m.banner, c0 = m.clankCount || 0;
        V = [];
        m.step(DT); step++;
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== bn0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        for (const w of V) if (w === "thornwake-bite") biteT.push(m.t);
        const Z = me.ultBramble;
        if (Z && !win) win = { t: m.t, cast: 0, crackle: 0, snareV: 0, biteV: 0, frames: 0, held: 0, green: 0,
                               stops: 0, clock: 0, end: m.t };
        if (win){
          for (const w of V){
            if (w === "thornwake") win.cast++;
            else if (w === "thornwake-crackle") win.crackle++;
            else if (w === "thornwake-snare") win.snareV++;
            else if (w === "thornwake-bite") win.biteV++;
          }
          if (Z){ win.frames++; if (th.brierHeld > 0) win.held++; if (me.brierGreen >= 1) win.green++; if (m.hitStop > 0) win.stops++; }
          win.end = m.t;
          if (!Z){
            win.clock = Z0 && Z0.t + DT >= Z0.dur - 1e-9 && me.alive && th.alive && !m.over ? 1 : 0;
            wins.push(win);
            win = null;
          }
        }
      }
      if (win){ win.end = m.t; wins.push(win); }          // open at the kill: no close to film
      const killT = m.over ? m.t : null;
      /* scored once the fight is run: the foe's casts anywhere in the CLIP, the scrunch card, and the bites
         in the clip's tail (the brambles outlive the window) */
      for (const w of wins){
        const c0 = w.t - lead, c1 = w.end + tail;
        w.foeCasts = foeCastT.filter(t => t >= c0 - 2.4 && t <= c1).length;   // a banner lives 2.1-2.4 s
        w.card = clank1 !== null && clank1 < c1 && clank1 + CARD > c0 ? 1 : 0;
        w.kill = killT !== null && killT <= c1 ? 1 : 0;                     // the match ends inside the clip
        w.tailBites = biteT.filter(t => t > w.end && t <= c1).length;
        w.heldPct = w.frames ? 100 * w.held / w.frames : 0;
        w.all = w.cast === 1 && w.clock && w.crackle >= 2 && w.snareV >= 1 && w.biteV >= 3
                && !w.foeCasts && !w.card && !w.kill ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0)
                + Math.min(w.crackle, 4) * 0.8 + Math.min(w.snareV, 4) * 0.8 + Math.min(w.biteV, 12) * 0.25
                + Math.min(w.tailBites, 3) * 0.5 + Math.min(w.heldPct, 30) / 10
                - 2 * w.foeCasts - 2 * w.card - 3 * w.kill;
        w.foe = foe; w.seed = sd; w.dur = w.end - w.t;
        if (!best || w.score > best.score) best = w;
      }
      if (best) out.push(best);
    }
  } finally { V = null; if (own) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  out.sort((p, q) => q.score - p.score);
  return { rows: out.slice(0, 12), n: out.length, all: out.filter(r => r.all).length };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=113001)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of Thornwake's own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v113/bramblesnare-window.mp4")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        affs = dict(page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff])"))
        ids = list(affs)
        skip = {x for x in a.exclude.split(",") if x}
        if not a.keep_aff:
            skip |= {i for i in ids if affs[i] == affs[RID] and i != RID}
        pool = [i for i in ids if i != RID and i not in skip]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        R = page.evaluate(JS, [RID, foes, seeds, a.secs, LEAD, TAIL])
        assert not errors, errors[:3]
    if "err" in R:
        raise SystemExit(R["err"])
    rows = R["rows"]
    print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds (left out: {', '.join(sorted(skip)) or 'none'})  ·  "
          f"the best window of each fight: {R['n']}, of which {R['all']} show everything\n")
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'all':>4}{'crk':>4}{'snr':>4}{'bite':>5}"
          f"{'tail':>5}{'held%':>7}{'stops':>6}{'other':>6}{'card':>5}{'kill':>5}{'score':>7}")
    for r in rows:
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['all']:>4}"
              f"{r['crackle']:>4}{r['snareV']:>4}{r['biteV']:>5}{r['tailBites']:>5}{r['heldPct']:>7.1f}{r['stops']:>6}"
              f"{r['foeCasts']:>6}{r['card']:>5}{r['kill']:>5}{r['score']:>7.2f}")
    if rows:
        b = rows[0]
        print(f"\n  FILM THE WINDOW AND NOT THE FIGHT{'' if b['all'] else ' (NO WINDOW SHOWS EVERYTHING -- widen the search)'}:\n")
        print(f"    python cinema_clip.py --game {a.game} "
              f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
        print(f"      --at {max(0, b['t'] - LEAD):.2f} "
              f"--window {b['dur'] + LEAD + TAIL:.2f} --end-at-window "
              f"--fps 60 --w 540 --out {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
