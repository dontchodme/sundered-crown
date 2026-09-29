#!/usr/bin/env python3
"""AN EXSANGUINATE WINDOW, TO FILM. v106.

    python _widowmaker_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape. What has to be ON SCREEN (and in the ear) is the
whole of v76 §4 as built at stage 6: the cast's inhale, her shell's dark-red
flush and the banner filling; the thread from the foe's bleed drips to her
shell, its beads running down it and a red "+n" on her per whole hp drained;
the reversed drip at BOTH counts the blade can make (it applies hemorrhage two
at a time, so only n 2 and n 4 are ever heard); the thread drawing back when
the foe stops bleeding; a hit stop freezing it -- and the SNAP, so the window
must close BY ITS CLOCK with the thread still up (a close with the thread
already drawn back, a death or the verdict is not the close the design names)
and the two shells well apart when it does -- at least 160 units centre to
centre, about 90 of open floor between the rims. The thread draws no line
between shells closer than 2 ballR + 10 (`_siphonPath`) and shortens its curve
under about 200, so the thread's share of the window (`up%`) counts only the
frames where it can be seen, and a snap at 89 units is a tear too small to read
(the third pick, Slagheart 106001, closed so, the balls touching a frame later).
A wider snap is a longer thread to tear, so the score adds the snap's distance
(to 300 units, +1 a hundred).

A window qualifies (`all`) only if it shows every one of those, and nothing on
screen takes them over: no cast of the foe's and no other banner anywhere in the
clip (lead to tail: a banner replaces hers -- one banner at a time -- and a
cast's set-piece and voice share the screen; a cast is read off the foe's cast
count OR any banner that is not hers, because some casts -- Grudgebearer's
Crucible, the fourth pick's -- raise their banner without that count; from 2.4 s
before the clip, a banner's life), and not the scrunch card, which opens at the
match's first clank for `scrunch.ease x 2 + intro` seconds and shrinks the arena
under it (a first cast often has it; the second pick, Aureole 106038, did, and
Aureole's Benediction fired 0.2 s after her cast). The qualifying windows are
scored on the drained hp, the thread's share of the window, the draw-backs and
her blows, and the tool prints the `--at` and `--window` to hand `cinema_clip`
(lead 1.2 s, tail 1.8 s, `--end-at-window`). RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE
FIGHT. Widowmaker plays side A, as the clip does. Left out of the pool by
default: Twinshade (`--exclude`), whose shades bleed and drip on screen and
drain nothing (reading 3) -- a second body with drips and no thread, in a clip
that is about the thread; and every foe of her own affinity (`--keep-aff` puts
them back): a bloodsworn foe wears the same red shell and blades, and the clip
has to show WHICH ball the blood goes to (the first pick, Goreshard, was one).

The drips are counted through `AC.SFX.play`, which is a no-op headless: the call
is recorded before its first line returns, and nothing here moves a fight.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "widowmaker"
LEAD, TAIL = 1.2, 1.8          # the clip: this much before the cast and after the close

JS = r"""([rid, foes, seeds, secs, lead, tail]) => {
  const DT = AC.CONFIG.physics.dt, SC = AC.CONFIG.scrunch, CARD = SC.ease * 2 + SC.intro;
  const GAP = 2 * AC.CONFIG.physics.ballR + 10;      // `_siphonPath` draws no line between shells closer than this
  const SNAPD = 160;                                   // the snap, filmed: this far apart, centre to centre
  if (typeof AC.Match.prototype.tickSiphon !== "function" || !/widowmaker-drain/.test(AC.SFX.play.toString()))
    return { err: "not a stage-6 Exsanguinate link (no tickSiphon, no drip voice)" };
  let drips = null;
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){
    if (drips && kind === "ult" && q && q.w === "widowmaker-drain") drips.push(q.n);
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
        const Z0 = me.ultDrain, h0 = me.hits, fade0 = me.siphonFade, hp0 = me.siphonHp, u0 = th.ultsFired || 0, b0 = m.banner;
        const c0 = m.clankCount || 0;
        drips = [];
        m.step(DT); step++;
        /* the foe's cast: its cast count, or ANY banner but hers (some casts raise their banner without
           passing through fireUlt's count -- Grudgebearer's Crucible does -- and an act's banner takes
           the one banner slot too) */
        if ((th.ultsFired || 0) > u0 || (m.banner && m.banner !== b0 && m.banner.text !== me.w.ult.name)) foeCastT.push(m.t);
        if (clank1 === null && (m.clankCount || 0) > c0) clank1 = m.t;
        const Z = me.ultDrain;
        if (Z && !win) win = { t: m.t, blows: 0, frames: 0, up: 0, back: 0, stops: 0, n2: 0, n4: 0, floats: 0,
                               drained0: me.drainTally ? me.drainTally.drained : 0, clock: 0, snap: 0, end: m.t };
        if (win){
          win.blows += me.hits - h0;
          win.floats += me.siphonHp - hp0;
          for (const n of drips){ if (n === 2) win.n2++; else if (n === 4) win.n4++; }
          if (Z){
            win.frames++;
            if (me.siphonFade > 0 && Math.hypot(me.x - th.x, me.y - th.y) >= GAP) win.up++;
            if (me.siphonFade < fade0 && me.siphonFade > 0 && fade0 === 1) win.back++;
            if (m.hitStop > 0 && me.siphonFade > 0) win.stops++;
          }
          win.end = m.t;
          if (!Z){
            win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive && th.alive && !m.over) ? 1 : 0;
            /* the snap is drawn where the thread hung when it snapped, so the shells must be apart then */
            win.snap = win.clock && me.siphonSnap && fade0 > 0
                       && Math.hypot(me.siphonSnap.sx - me.siphonSnap.fx, me.siphonSnap.sy - me.siphonSnap.fy) >= SNAPD ? 1 : 0;
            win.snapD = me.siphonSnap ? Math.hypot(me.siphonSnap.sx - me.siphonSnap.fx, me.siphonSnap.sy - me.siphonSnap.fy) : 0;
            win.drained = (me.drainTally ? me.drainTally.drained : 0) - win.drained0;
            wins.push(win);
            win = null;
          }
        }
      }
      /* scored once the fight is run: the foe's casts anywhere in the CLIP (lead to tail) and the
         scrunch card (it opens at the match's first clank for CARD seconds) are known only now */
      for (const w of wins){
        const c0 = w.t - lead, c1 = w.end + tail;
        w.foeCasts = foeCastT.filter(t => t >= c0 - 2.4 && t <= c1).length;   // a banner lives 2.1-2.4 s
        w.card = clank1 !== null && clank1 < c1 && clank1 + CARD > c0 ? 1 : 0;
        w.all = w.clock && w.snap && w.floats > 0 && w.n2 > 0 && w.n4 > 0 && w.up > 0
                && w.back > 0 && w.stops > 0 && !w.foeCasts && !w.card ? 1 : 0;
        w.score = (w.all ? 10 : 0) + (w.clock ? 4 : 0) + (w.snap ? 3 : 0)
                + Math.min(w.drained, 30) * 0.15 + (w.frames ? 3 * w.up / w.frames : 0)
                + Math.min(w.back, 3) * 0.4 + Math.min(w.blows, 8) * 0.2
                + (w.n2 ? 0.5 : 0) + (w.n4 ? 0.5 : 0) + Math.min(w.snapD, 300) / 100
                - 2 * w.foeCasts - 2 * w.card;
        w.foe = foe; w.seed = sd; w.dur = w.end - w.t;
        w.upPct = w.frames ? 100 * w.up / w.frames : 0;
        if (!best || w.score > best.score) best = w;
      }
      if (best) out.push(best);
    }
  } finally { drips = null; if (own) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  out.sort((p, q) => q.score - p.score);
  return { rows: out.slice(0, 12), n: out.length, all: out.filter(r => r.all).length };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=106001)
    ap.add_argument("--foes", type=int, default=99, help="how many foes, spread over the roster (default all)")
    ap.add_argument("--exclude", default="twinshade", help="foes left out of the pool (comma-separated; '' for none)")
    ap.add_argument("--keep-aff", action="store_true", help="keep the foes of her own affinity in the pool")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v106/exsanguinate-window.mp4")
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
          f"the best window of each fight: "
          f"{R['n']}, of which {R['all']} show everything\n")
    print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'snap':>5}{'all':>4}{'drained':>8}"
          f"{'+n':>5}{'n2':>4}{'n4':>4}{'up%':>6}{'back':>5}{'stops':>6}{'blows':>6}{'other':>6}{'card':>5}{'snap d':>7}{'score':>7}")
    for r in rows:
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['snap']:>5}{r['all']:>4}"
              f"{r['drained']:>8.1f}{r['floats']:>5}{r['n2']:>4}{r['n4']:>4}{r['upPct']:>6.1f}{r['back']:>5}"
              f"{r['stops']:>6}{r['blows']:>6}{r['foeCasts']:>6}{r['card']:>5}{r['snapD']:>7.0f}{r['score']:>7.2f}")
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
