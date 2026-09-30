#!/usr/bin/env python3
"""A BLOODPRICE WINDOW, TO FILM. v114.

    python _goreshard_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape, by way of `_spellbreaker_pick.py` (its exclusions,
its voice count and its clip rules). What has to be ON SCREEN (and in the ear)
is the whole of v81 §4 as built at stage 6 (v114 §5): the cast -- the wet
drawn-blade hiss, and the red running down the blade from the guard to the
point; the blade's glow climbing and sinking with the foe's Hemorrhage (so the
window's frames must see the foe at 0, 2 and 4 stacks); blows she lands priced
on 2 and on 4 stacks -- the strike pitched down a semitone a stack, the float
drawn larger; the blood motes off the barbs for the window; and THE CLOSE, so
the window must close BY ITS CLOCK with both alive (the red draining back into
the guard over 0.35 s, and no voice: v81's "close -- nothing"; a death's close
or a kill is the death voice's moment and the verdict's).

A window qualifies (`all`) only if it shows every one of those, and nothing on
screen takes them over: no cast of the foe's and no other banner anywhere in the
clip (lead to tail, from 2.4 s before the clip: a banner's life; a cast is read
off the foe's cast count OR any banner that is not Bloodprice's), not the
scrunch card (it opens at the match's first clank for `scrunch.ease x 2 +
intro` seconds and shrinks the arena under it), and the match must not end
inside the clip (`kill`). The qualifying windows are scored on the blows priced
on 4 and on 2 (their voices and floats), the stack levels the glow shows, and
the blows she lands; the tool prints the `--at` and `--window` to hand
`cinema_clip` (lead 1.2 s, tail 1.8 s, `--end-at-window`), with `dur` the
window's length in MATCH time: the window clock stops in the freezes, so 8 + 3
would end the clip before the close. RICK WATCHES THE ULT'S WINDOW AND NOT THE
WHOLE FIGHT. Goreshard (`oathwound`) plays side A, as the clip does.

Left out of the pool by default: Twinshade (`--exclude`), whose shades are a
second body taking blows and bleeding; and every foe of Goreshard's own
affinity (`--keep-aff` puts them back): a bloodsworn foe wears the same red,
bleeds HER with its own Hemorrhage, and the clip has to show WHOSE blade the
price reddens.

The voices are counted through `AC.SFX.play`, which is a no-op headless: the
call is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "oathwound"              # Goreshard (the roster's one id / name mismatch)
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro;
  const src = AC.SFX.play.toString();
  if (typeof AC.Match.prototype.tickGore !== "function" || !/w === "oathwound"/.test(src) || !/kind === "hit" && p\.price/.test(src))
    return { err: "not a stage-6 Bloodprice link (no tickGore, no cast arm or priced-blow branch)" };
  let V = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (V){
      if (kind === "ult" && q && q.w === rid) V.push(["cast", 0]);
      else if (kind === "hit" && q && Object.prototype.hasOwnProperty.call(q, "price")) V.push(["priced", q.price]);
    }
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
        const Z0 = me.ultPrice, T0 = me.priceTally;
        const bl0 = T0 ? T0.blows : 0;
        const u0 = th.ultsFired || 0, bn0 = m.banner, c0 = m.clankCount || 0;
        V = [];
        m.step(DT); step++;
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== bn0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        const Z = me.ultPrice, T = me.priceTally;
        if (Z && !win) win = { t: m.t, cast: 0, p2: 0, p4: 0, pOther: 0, blows: 0, frames: 0, lv: [0, 0, 0, 0, 0],
                               stops: 0, clock: 0, end: m.t };
        if (win){
          for (const [k, n] of V){
            if (k === "cast") win.cast++;
            else if (n === 2) win.p2++; else if (n === 4) win.p4++; else win.pOther++;
          }
          if (T) win.blows += T.blows - bl0;
          if (Z){ win.frames++; win.lv[Math.min(4, th.stacks("hemorrhage"))]++; if (m.hitStop > 0) win.stops++; }
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
      /* scored once the fight is run: the foe's casts anywhere in the CLIP and the scrunch card */
      for (const w of wins){
        const c0 = w.t - lead, c1 = w.end + tail;
        w.foeCasts = foeCastT.filter(t => t >= c0 - 2.4 && t <= c1).length;   // a banner lives 2.1-2.4 s
        w.card = clank1 !== null && clank1 < c1 && clank1 + CARD > c0 ? 1 : 0;
        w.kill = killT !== null && killT <= c1 ? 1 : 0;                     // the match ends inside the clip
        w.levels = [0, 2, 4].filter(k => w.lv[k] > 0).length;               // the glow's ladder, as seen
        w.all = w.cast === 1 && w.clock && w.p4 >= 1 && w.p2 >= 1 && w.levels === 3
                && !w.foeCasts && !w.card && !w.kill ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0)
                + Math.min(w.p4, 6) * 0.8 + Math.min(w.p2, 4) * 0.6 + w.levels * 0.5
                + Math.min(w.blows, 10) * 0.1
                - 2 * w.foeCasts - 2 * w.card - 3 * w.kill;
        w.foe = foe; w.seed = sd; w.dur = w.end - w.t;
        w.lvPct = w.frames ? w.lv.map(x => Math.round(100 * x / w.frames)) : [0, 0, 0, 0, 0];
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
    ap.add_argument("--seed0", type=int, default=114001)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of Goreshard's own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v114/bloodprice-window.mp4")
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
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'all':>4}{'@4':>4}{'@2':>4}"
          f"{'  stacks 0/2/4 %':>17}{'blows':>6}{'stops':>6}{'other':>6}{'card':>5}{'kill':>5}{'score':>7}")
    for r in rows:
        lv = "/".join(str(r['lvPct'][k]) for k in (0, 2, 4))
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['all']:>4}"
              f"{r['p4']:>4}{r['p2']:>4}{lv:>17}{r['blows']:>6}{r['stops']:>6}"
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
