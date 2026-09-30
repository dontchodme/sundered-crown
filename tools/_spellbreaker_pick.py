#!/usr/bin/env python3
"""AN UNMAKING WINDOW, TO FILM. v111.

    python _spellbreaker_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape, by way of `_aureole_pick.py` (its exclusions, its
voice count and its clip rules). What has to be ON SCREEN (and in the ear) is
the whole of v79 §4 as built at stage 6 (v111 §5): the cast -- the glass crack
into a hum, and the script written along both her blades; the rune motes shed
off them for the window; her blows landing their second hex -- the HEX +2 tag
at the impact; a hex proc the window doubles on the foe -- the snap lengthened
to match, and the foe's weapon greyed for the stun's own 0.4 s; and THE CLOSE,
so the window must close BY ITS CLOCK with both alive (the hum cutting out,
the script unwritten tip to hilt over 0.2 s; a death's close or a kill is the
death voice's moment and the verdict's).

A window qualifies (`all`) only if it shows every one of those, and nothing on
screen takes them over: no cast of the foe's and no other banner anywhere in the
clip (lead to tail, from 2.4 s before the clip: a banner's life; a cast is read
off the foe's cast count OR any banner that is not the Unmaking's), not the
scrunch card (it opens at the match's first clank for `scrunch.ease x 2 +
intro` seconds and shrinks the arena under it), and the match must not end
inside the clip (`kill`). The qualifying windows are scored on the second hexes
(the +2 tags), the doubled stuns (their voice and grey), the share of window
frames with the foe's weapon grey, and the blows she lands; the tool prints the
`--at` and `--window` to hand `cinema_clip` (lead 1.2 s, tail 1.8 s,
`--end-at-window`), with `dur` the window's length in MATCH time: the window
clock stops in the freezes, so 8 + 3 would end the clip before the close. RICK
WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT. Spellbreaker plays side A, as
the clip does.

Left out of the pool by default: Twinshade (`--exclude`), whose shades are a
second body taking hexes and greys; and every foe of Spellbreaker's own
affinity (`--keep-aff` puts them back): a runic foe wears the same blue, hexes
HER weapon with its own school (a plain stun, not the grey) and casts in the
same runes, and the clip has to show WHOSE weapon the Unmaking greys.

The voices are counted through `AC.SFX.play`, which is a no-op headless: the
call is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "spellbreaker"
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro;
  if (typeof AC.Match.prototype.tickUnmaking !== "function" || !/spellbreaker-stun/.test(AC.SFX.play.toString()))
    return { err: "not a stage-6 Unmaking link (no tickUnmaking, no stun voice)" };
  let V = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (V && kind === "ult" && q && /^spellbreaker(-stun|-close)?$/.test(q.w)) V.push(q.w);
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
        const Z0 = me.ultUnmake, T0 = me.unmakeTally;
        const x0 = T0 ? T0.extra : 0, bl0 = T0 ? T0.blows : 0;
        const u0 = th.ultsFired || 0, bn0 = m.banner, c0 = m.clankCount || 0;
        V = [];
        m.step(DT); step++;
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== bn0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        const Z = me.ultUnmake, T = me.unmakeTally;
        if (Z && !win) win = { t: m.t, cast: 0, stunV: 0, closeVoice: 0, extra: 0, blows: 0, frames: 0, grey: 0,
                               stops: 0, clock: 0, end: m.t };
        if (win){
          for (const w of V){
            if (w === "spellbreaker") win.cast++;
            else if (w === "spellbreaker-stun") win.stunV++;
            else if (w === "spellbreaker-close") win.closeVoice++;
          }
          if (T){ win.extra += T.extra - x0; win.blows += T.blows - bl0; }
          if (Z){ win.frames++; if (th.unmkGrey > 0) win.grey++; if (m.hitStop > 0) win.stops++; }
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
        w.greyPct = w.frames ? 100 * w.grey / w.frames : 0;
        w.all = w.cast === 1 && w.clock && w.closeVoice === 1 && w.extra >= 1 && w.stunV >= 1
                && !w.foeCasts && !w.card && !w.kill ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0)
                + Math.min(w.extra, 8) * 0.5 + Math.min(w.stunV, 8) * 0.6 + Math.min(w.greyPct, 40) / 10
                + Math.min(w.blows, 10) * 0.1
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
    ap.add_argument("--seed0", type=int, default=111001)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of Spellbreaker's own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v111/unmaking-window.mp4")
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
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'all':>4}{'+2':>4}{'stunV':>6}"
          f"{'grey%':>7}{'blows':>6}{'stops':>6}{'other':>6}{'card':>5}{'kill':>5}{'score':>7}")
    for r in rows:
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['all']:>4}"
              f"{r['extra']:>4}{r['stunV']:>6}{r['greyPct']:>7.1f}{r['blows']:>6}{r['stops']:>6}"
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
