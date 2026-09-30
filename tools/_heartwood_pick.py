#!/usr/bin/env python3
"""A ROOTFAST WINDOW, TO FILM. v112.

    python _heartwood_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape, by way of `_spellbreaker_pick.py` (its exclusions,
its voice count and its clip rules). What has to be ON SCREEN (and in the ear)
is the whole of v85 §4 as built at stage 6 (v112 §6): the cast -- the green
creak, and the blade greening hilt to tip with its leaf scale sprouting; the
leaf motes shed off it for the window; the root on every blow -- its short
creak-and-crack, the held ball marked for the shoots (Tendril's picture: drawn
on a tip that carries it; on a link built on sc-tendril-t3 the held ball shows
Paradox's hexagon, v112 §6), a NEW hold and a RE-ROOT of a ball already held,
and the ENTANGLE tag counting on the rooted foe; and THE CLOSE, so the window
must close BY ITS CLOCK with both alive (the wither, tip to hilt, its leaves
falling; the kill's close is the verdict's moment).

A window qualifies (`all`) only if it shows every one of those, and nothing on
screen takes them over: no cast of the foe's and no other banner anywhere in the
clip (lead to tail, from 2.4 s before the clip: a banner's life), not the
scrunch card (it opens at the match's first clank for `scrunch.ease x 2 +
intro` seconds and shrinks the arena under it), and the match must not end
inside the clip (`kill`). The qualifying windows are scored on the roots (their
voices), the new holds, the counted tags, the share of window frames with the
foe held, and the blows landed; the tool prints the `--at` and `--window` to
hand `cinema_clip` (lead 1.2 s, tail 1.8 s, `--end-at-window`), with `dur` the
window's length in MATCH time: the window clock stops in the freezes, so 8 + 3
would end the clip before the close. RICK WATCHES THE ULT'S WINDOW AND NOT THE
WHOLE FIGHT. Heartwood plays side A, as the clip does.

Left out of the pool by default: Twinshade (`--exclude`), whose shades are a
second body taking blows; and every foe of Heartwood's own affinity
(`--keep-aff` puts them back): a verdant foe wears the same green, roots and
entangles with its own school, and the clip has to show WHOSE green and whose
roots these are.

The voices are counted through `AC.SFX.play`, which is a no-op headless: the
call is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "heartwood"
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro, R = AC.CONFIG.physics.ballR;
  if (typeof AC.Match.prototype.tickGrove !== "function" || !/heartwood-root/.test(AC.SFX.play.toString()))
    return { err: "not a stage-6 Rootfast link (no tickGrove, no root voice)" };
  let V = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (V && kind === "ult" && q && /^heartwood(-root)?$/.test(q.w)) V.push(q.w);
    return oPlay.call(this, kind, q);
  };
  const out = [];
  try {
    for (const foe of foes) for (const sd of seeds){
      const m = new AC.Match(rid, foe, sd);
      const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
      let step = 0, win = null, best = null, clank1 = null;
      const wins = [], foeCastT = [];
      while (!m.over && step < secs / DT){
        const Z0 = me.ultRoot, T0 = me.rootTally;
        const rd0 = T0 ? T0.rooted : 0, rs0 = T0 ? T0.roots : 0, bl0 = T0 ? T0.blows : 0;
        const u0 = th.ultsFired || 0, bn0 = m.banner, c0 = m.clankCount || 0, nt0 = m.tags.length;
        V = [];
        m.step(DT); step++;
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== bn0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        const Z = me.ultRoot, T = me.rootTally;
        if (Z && !win) win = { t: m.t, cast: 0, rootV: 0, rooted: 0, holds: 0, blows: 0, frames: 0, held: 0,
                               tags: 0, clock: 0, end: m.t };
        if (win){
          for (const w of V){ if (w === "heartwood") win.cast++; else win.rootV++; }
          if (T){ win.rooted += T.rooted - rd0; win.holds += T.roots - rs0; win.blows += T.blows - bl0; }
          if (T && T.rooted > rd0 && th.alive){
            /* the root's count on the blow's own ENTANGLE tag (not the first-ever, the teaching panel) */
            const g = m.tags.slice(0).reverse().find(g2 => g2.key === "entangle" && g2.max - g2.life <= 0.1
                                                         && Math.hypot(g2.x - th.x, g2.y - th.y) < R * 3);
            if (g && !g.first && g.val > 0) win.tags++;
          }
          if (Z){ win.frames++; if (th.pin > 0 && !th.pinFree) win.held++; }
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
      for (const w of wins){
        const c0 = w.t - lead, c1 = w.end + tail;
        w.foeCasts = foeCastT.filter(t => t >= c0 - 2.4 && t <= c1).length;   // a banner lives 2.1-2.4 s
        w.card = clank1 !== null && clank1 < c1 && clank1 + CARD > c0 ? 1 : 0;
        w.kill = killT !== null && killT <= c1 ? 1 : 0;
        w.heldPct = w.frames ? 100 * w.held / w.frames : 0;
        w.reroots = w.rooted - w.holds;
        w.all = w.cast === 1 && w.clock && w.rootV === w.rooted && w.holds >= 1 && w.reroots >= 1 && w.tags >= 1
                && !w.foeCasts && !w.card && !w.kill ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0)
                + Math.min(w.rooted, 10) * 0.5 + Math.min(w.holds, 5) * 0.6 + Math.min(w.tags, 6) * 0.3
                + Math.min(w.heldPct, 60) / 15 + Math.min(w.blows, 12) * 0.1
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
    ap.add_argument("--seed0", type=int, default=112201)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of Heartwood's own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="07-shorts/v112/rootfast-window.mp4")
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
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'all':>4}{'roots':>6}{'holds':>6}"
          f"{'voiced':>7}{'tags':>5}{'held%':>7}{'blows':>6}{'other':>6}{'card':>5}{'kill':>5}{'score':>7}")
    for r in rows:
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['all']:>4}"
              f"{r['rooted']:>6}{r['holds']:>6}{r['rootV']:>7}{r['tags']:>5}{r['heldPct']:>7.1f}{r['blows']:>6}"
              f"{r['foeCasts']:>6}{r['card']:>5}{r['kill']:>5}{r['score']:>7.2f}")
    if rows:
        b = rows[0]
        print(f"\n  FILM THE WINDOW AND NOT THE FIGHT{'' if b['all'] else ' (NO WINDOW SHOWS EVERYTHING -- widen the search)'}:\n")
        print(f"    python tools/cinema_clip.py --game {a.game} "
              f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
        print(f"      --at {max(0, b['t'] - LEAD):.2f} "
              f"--window {b['dur'] + LEAD + TAIL:.2f} --end-at-window "
              f"--fps 60 --w 540 --out {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
