#!/usr/bin/env python3
"""A CONSECRATION WINDOW, TO FILM. v109.

    python _censer_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape, by way of `_angelus_pick.py` (its exclusions, its
voice count and its clip rules). What has to be ON SCREEN (and in the ear) is
the whole of v78 §4 as built at stage 6 (v109 §5): the cast -- the thurible
swing and the hammer head lighting; blows in the window, each a disc blooming
out of the struck ball with its bell, and more than one disc standing, so the
bell is heard at more than one pitch (it climbs one step a disc standing); the
foe on the ground, wearing the gold rim, a smite tick flashing the disc under it
and the SMITE tag; Censer on the ground, the up-drift, the heal chime and the
BLESSING tag -- and THE CLOSE, so the window must close BY ITS CLOCK with both
alive (the head cooling over 0.3 s; a death's close or a kill is the death
voice's moment and the verdict's), with a disc still standing at the close, so
the tail shows the ground going from live to inert (it stays drawn, dimmer,
until its 8 s are up: reading 14).

A window qualifies (`all`) only if it shows every one of those, and nothing on
screen takes them over: no cast of the foe's and no other banner anywhere in the
clip (lead to tail, from 2.4 s before the clip: a banner's life; a cast is read
off the foe's cast count OR any banner that is not Censer's), not the scrunch
card (it opens at the match's first clank for `scrunch.ease x 2 + intro`
seconds and shrinks the arena under it), and the match must not end inside the
clip (`kill`). The qualifying windows are scored on the discs, the distinct bell
pitches, the smite ticks, the heals, the frames with the foe on the ground, the
discs standing at the close and the hit stops while the head is lit; the tool
prints the `--at` and `--window` to hand `cinema_clip` (lead 1.2 s, tail 1.8 s,
`--end-at-window`), with `dur` the window's length in MATCH time: the window
clock stops in the freezes, so 8 + 3 would end the clip before the close. RICK
WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT. Censer plays side A, as the
clip does.

Left out of the pool by default: Twinshade (`--exclude`), whose shades take
blows and so take discs (reading 1) -- a disc at a second body, in a clip that
is about where the hammer lands; and every foe of Censer's own affinity
(`--keep-aff` puts them back): a sanctified foe wears the same white and gold
shell, and the clip has to show WHICH ball is on the ground and which is healed.

The voices are counted through `AC.SFX.play`, which is a no-op headless: the
call is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "censer"
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro;
  if (typeof AC.Match.prototype.tickConsecration !== "function" || !/censer-disc/.test(AC.SFX.play.toString()))
    return { err: "not a stage-6 Consecration link (no tickConsecration, no disc bell)" };
  let V = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (V && kind === "ult" && q && (q.w === "censer" || q.w === "censer-disc")) V.push([q.w, q.n]);
    else if (V && kind === "spark" && q && q.collect === true) V.push(["chime", q.n]);
    return oPlay.call(this, kind, q);
  };
  const out = [];
  try {
    for (const foe of foes) for (const sd of seeds){
      const m = new AC.Match(rid, foe, sd);
      const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a, side = me === m.a ? "a" : "b";
      let step = 0, win = null, best = null, clank1 = null;
      const wins = [], foeCastT = [];
      while (!m.over && step < secs / DT){
        const Z0 = me.ultHoly, T0 = me.holyTally;
        const k0 = T0 ? T0.ticks : 0, b0 = T0 ? T0.bless : 0, d0 = T0 ? T0.discs : 0, o0 = T0 ? T0.foeOn : 0, s0 = T0 ? T0.selfOn : 0;
        const u0 = th.ultsFired || 0, bn0 = m.banner, c0 = m.clankCount || 0;
        V = [];
        m.step(DT); step++;
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== bn0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        const Z = me.ultHoly, T = me.holyTally;
        if (Z && !win) win = { t: m.t, cast: 0, discs: 0, bells: [], ticks: 0, heals: 0, chimes: 0, foeOn: 0, selfOn: 0,
                               frames: 0, stops: 0, clock: 0, standing: 0, end: m.t };
        if (win){
          for (const [w, n] of V){
            if (w === "censer") win.cast++;
            else if (w === "censer-disc") win.bells.push(n);
            else if (w === "chime") win.chimes++;
          }
          if (T){ win.discs += T.discs - d0; win.ticks += T.ticks - k0; win.heals += T.bless - b0;
                  win.foeOn += T.foeOn - o0; win.selfOn += T.selfOn - s0; }
          if (Z){ win.frames++; if (m.hitStop > 0) win.stops++; }
          win.end = m.t;
          if (!Z){
            win.clock = Z0 && Z0.t + DT >= Z0.dur - 1e-9 && me.alive && th.alive && !m.over ? 1 : 0;
            win.standing = m.holyGround.filter(d => d.side === side).length;
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
        w.pitches = [...new Set(w.bells.map(n => Math.max(1, Math.min(5, n))))].sort().join("");
        w.onPct = w.frames ? 100 * w.foeOn / w.frames : 0;
        w.all = w.cast === 1 && w.clock && w.discs >= 2 && w.bells.length === w.discs && w.pitches.length >= 2
                && w.ticks >= 1 && w.heals >= 1 && w.chimes === w.heals && w.standing >= 1
                && !w.foeCasts && !w.card && !w.kill ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0)
                + Math.min(w.discs, 6) * 0.5 + w.pitches.length * 0.4 + Math.min(w.ticks, 8) * 0.3
                + Math.min(w.heals, 6) * 0.4 + Math.min(w.standing, 3) * 0.5 + Math.min(w.onPct, 50) / 25
                + Math.min(w.stops, 60) / 60
                - 2 * w.foeCasts - 2 * w.card - 3 * w.kill;
        w.foe = foe; w.seed = sd; w.dur = w.end - w.t;
        if (!best || w.score > best.score) best = w;
      }
      if (best){ delete best.bells; out.push(best); }
    }
  } finally { V = null; if (own) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  out.sort((p, q) => q.score - p.score);
  return { rows: out.slice(0, 12), n: out.length, all: out.filter(r => r.all).length };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=109001)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of Censer's own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v109/consecration-window.mp4")
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
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'all':>4}{'discs':>6}{'pitch':>6}"
          f"{'ticks':>6}{'heals':>6}{'on%':>6}{'stand':>6}{'stops':>6}{'other':>6}{'card':>5}{'kill':>5}{'score':>7}")
    for r in rows:
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['all']:>4}"
              f"{r['discs']:>6}{r['pitches']:>6}{r['ticks']:>6}{r['heals']:>6}{r['onPct']:>6.1f}{r['standing']:>6}"
              f"{r['stops']:>6}{r['foeCasts']:>6}{r['card']:>5}{r['kill']:>5}{r['score']:>7.2f}")
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
