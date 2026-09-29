#!/usr/bin/env python3
"""AN ASCENSION WINDOW, TO FILM. v104.

    python _angelus_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape (and `_widowmaker_pick.py`'s exclusions). What has
to be ON SCREEN (and in the ear) is the whole of v74 §6 as built at stage 6:
the cast's chord, the column and the halo as the ball rises; the arrival, where
the shafts light; shaft blows, each a gold thread running up its shaft, and
each heal a flare of the halo, BLESSING n on the caster and the glass tap (its
pitch one step per blessing count, so more than one count is heard); a hit stop
freezing the shafts -- and THE CLOSE, so the window must close BY ITS CLOCK with
both alive (the only close with the chord, the shafts shortening to blades and
the ball's drop; a death close or a kill is the death voice's moment and the
verdict's, readings 10 and 15), and the ball must LAND inside the clip's tail
(the thud, heard on the first floor contact after the close: median 1.17 s
after it, and a knocked drop lands later), so the tail is where the landing is
scored.

A window qualifies (`all`) only if it shows every one of those, and nothing on
screen takes them over: no cast of the foe's and no other banner anywhere in the
clip (lead to tail, from 2.4 s before the clip: a banner's life; a cast is read
off the foe's cast count OR any banner that is not Angelus's), and not the
scrunch card, which opens at the match's first clank for `scrunch.ease x 2 +
intro` seconds and shrinks the arena under it; and the match must not end
inside the clip (`kill`): the first pick, Farwarden 104001, closed by its clock
and landed 0.73 s later, and Angelus killed Farwarden 0.14 s after the landing,
so the thud sat under the kill's voices and the clip ran on into the verdict.
The qualifying windows are
scored on the heals, the distinct tap counts, the threads, the hit stops while
lit, the foe's blows landing on the hung ball, and how soon the ball lands; the
tool prints the `--at` and `--window` to hand `cinema_clip` (lead 1.2 s, tail
1.8 s, `--end-at-window`). RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE
FIGHT. Angelus plays side A, as the clip does.

Left out of the pool by default: Twinshade (`--exclude`), whose shades take
shaft blows and heal (reading 11) -- threads starting at a second body, in a
clip that is about which ball the light runs to; and every foe of Angelus's own
affinity (`--keep-aff` puts them back): a sanctified foe wears the same white
and gold shell, and the clip has to show WHICH ball is healed.

The voices are counted through `AC.SFX.play`, which is a no-op headless: the
call is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "angelus"
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro;
  if (typeof AC.Match.prototype.tickAscend !== "function" || !/angelus-shaft/.test(AC.SFX.play.toString()))
    return { err: "not a stage-6 Ascension link (no tickAscend, no tap voice)" };
  let V = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (V && kind === "ult" && q && typeof q.w === "string" && q.w.startsWith("angelus")) V.push([q.w, q.n]);
    return oPlay.call(this, kind, q);
  };
  const out = [];
  try {
    for (const foe of foes) for (const sd of seeds){
      const m = new AC.Match(rid, foe, sd);
      const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
      let step = 0, win = null, best = null, clank1 = null, falling = null;
      const seenThr = new WeakSet();          // tickAscend can run twice a step: a thread is new when first seen
      const wins = [], foeCastT = [];
      while (!m.over && step < secs / DT){
        const Z0 = me.ultRise, h0 = me.hits, th0 = th.hits, T0 = me.riseTally;
        const b0 = T0 ? T0.bless : 0, a0 = T0 ? T0.arrivals : 0, u0 = th.ultsFired || 0, bn0 = m.banner;
        const c0 = m.clankCount || 0;
        V = [];
        m.step(DT); step++;
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== bn0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        const Z = me.ultRise, T = me.riseTally;
        /* the landing thud belongs to the window that closed before it */
        for (const [w] of V) if (w === "angelus-land" && falling){ falling.landT = m.t; falling = null; }
        if (Z && !win) win = { t: m.t, arrive: 0, litBlows: 0, heals: 0, taps: [], threads: 0, stops: 0,
                               foeOn: 0, cast: 0, chord: 0, clock: 0, landT: null, end: m.t };
        if (win){
          for (const [w, n] of V){
            if (w === "angelus") win.cast++;
            else if (w === "angelus-shaft") win.taps.push(n);
            else if (w === "angelus-close") win.chord++;
          }
          if (T){ win.arrive += T.arrivals - a0; win.heals += T.bless - b0; }
          if (Z0 && Z0.lit) win.litBlows += me.hits - h0;
          if (Z && Z.lit){
            for (const q of me.ascendFx) if (!seenThr.has(q)){ seenThr.add(q); win.threads++; }
            if (m.hitStop > 0) win.stops++;
            win.foeOn += th.hits - th0;
          }
          win.end = m.t;
          if (!Z){
            win.clock = win.chord === 1 && me.alive && th.alive && !m.over ? 1 : 0;
            wins.push(win);
            if (win.clock) falling = win;
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
        w.fall = w.landT === null ? null : w.landT - w.end;
        w.land = w.fall !== null && w.fall <= tail - 0.3 ? 1 : 0;           // the thud inside the tail, heard
        w.counts = [...new Set(w.taps)].sort().join("");
        w.all = w.cast === 1 && w.arrive === 1 && w.clock && w.land && w.heals >= 2 && w.taps.length === w.heals
                && w.threads > 0 && w.stops > 0 && !w.foeCasts && !w.card && !w.kill ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0) + (w.land ? 3 : 0)
                + Math.min(w.heals, 8) * 0.5 + w.counts.length * 0.4 + Math.min(w.threads, 8) * 0.2
                + Math.min(w.stops, 60) / 30 + Math.min(w.foeOn, 3) * 0.3
                + (w.land ? (tail - w.fall) : 0)
                - 2 * w.foeCasts - 2 * w.card - 3 * w.kill;
        w.foe = foe; w.seed = sd; w.dur = w.end - w.t;
        if (!best || w.score > best.score) best = w;
      }
      if (best){ delete best.taps; out.push(best); }
    }
  } finally { V = null; if (own) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  out.sort((p, q) => q.score - p.score);
  return { rows: out.slice(0, 12), n: out.length, all: out.filter(r => r.all).length };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=104001)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of Angelus's own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v104/ascension-window.mp4")
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
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'land':>5}{'fall':>6}{'all':>4}"
          f"{'blows':>6}{'heals':>6}{'taps n':>8}{'thr':>5}{'stops':>6}{'foeOn':>6}{'other':>6}{'card':>5}{'kill':>5}{'score':>7}")
    for r in rows:
        fall = f"{r['fall']:.2f}" if r["fall"] is not None else "-"
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['land']:>5}{fall:>6}"
              f"{r['all']:>4}{r['litBlows']:>6}{r['heals']:>6}{r['counts']:>8}{r['threads']:>5}{r['stops']:>6}"
              f"{r['foeOn']:>6}{r['foeCasts']:>6}{r['card']:>5}{r['kill']:>5}{r['score']:>7.2f}")
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
