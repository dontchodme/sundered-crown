#!/usr/bin/env python3
"""A REBUTTAL WINDOW, TO FILM. v102.

    python _lodestone_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape (by way of `_ironhail_pick.py`). What has to be ON
SCREEN (and in the ear) is the whole of v70 §6.1-6.2: the cast (the rising
four-note chime; the rune chain lighting along the four walls from the
caster's nearest one), the walls lit with their motes and the head's rune,
TOUCHES -- each a wall's flare, the bar snapping into the ball, the rune-streak
off the hurled ball, the HEX tag with its count, and in the ear the snap
pitched by that count with the hex-snap under it -- and the close BY ITS
CLOCK: the reversed chime and the walls going dark from the far wall inward.
A window that a death ends (or the match's end) plays no close voice and
shows no clock go-dark, so it scores nothing. The counts the snaps are pitched
at are scored a point a count heard, so a window that climbs 1-2-3-4-5 beats
one that starts at the cap; a corner touch (two walls flare) and a touch in a
closed-in hall (the runes on the seals' line) add a little. The fight must
also run on for the clip's tail (1.8s past the close), or the kill takes the
picture.

The voices are READ, not inferred: `SFX.play` is wrapped (it is a no-op
headless, and the wrapper only records) so the counts are the `n` each touch's
snap was played with and the close is the `lodestone-close` voice itself. The
touches' walls are the picture's own records (`lodeFx`).

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
Lodestone plays side A, as `cinema_clip --a lodestone` films it.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "lodestone"
TAIL = 1.8

JS = r"""([rid, foes, seeds, secs, tail]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  if (!/lodestone-touch/.test(AC.SFX.play.toString())) throw new Error("no Lodestone voices: not the stage-6 link");
  let heard = [];
  const oPlay = AC.SFX.play;
  AC.SFX.play = function(kind, q){ heard.push([kind, q && q.w, q && q.n]); return oPlay.call(this, kind, q); };
  try {
    for (const foe of foes) for (const sd of seeds){
      const m = new AC.Match(rid, foe, sd);
      const me = m.a, th = m.b;
      let step = 0, win = null, best = null, pend = null;
      while (!m.over && step < secs / DT){
        const Z0 = me.ultRunes, h0 = me.hits, k0 = me.runeTally ? me.runeTally.touches : 0;
        const r0 = me.lodeFx ? me.lodeFx.slice() : [];
        heard = [];
        m.step(DT); step++;
        /* a clock-closed window waits for its tail: the fight must run on */
        if (pend && m.t >= pend.end + tail){ pend.tailOk = 1; pend.score += 3; if (!best || pend.score > best.score) best = pend; pend = null; }
        const Z = me.ultRunes, T = me.runeTally;
        const lv = heard.filter(x => x[0] === "ult" && /^lodestone/.test(x[1] || ""));
        if (Z && !win) win = { t: m.t, touches: 0, snaps: 0, hexSnaps: 0, ns: {}, seq: [], start: th.stacks("hex"),
                               castVoice: 0, closeVoice: 0, corner: 0, inset: 0, blows: 0, clock: 0, end: m.t, tailOk: 0 };
        if (!win) continue;
        for (const x of lv){
          if (x[1] === "lodestone") win.castVoice++;
          else if (x[1] === "lodestone-touch"){ win.snaps++; win.ns[x[2]] = (win.ns[x[2]] || 0) + 1; win.seq.push(x[2]); }
          else if (x[1] === "lodestone-close") win.closeVoice++;
        }
        win.hexSnaps += heard.filter(x => x[0] === "hex-snap").length;
        if (T && T.touches > k0){
          win.touches += T.touches - k0;
          for (const q of (me.lodeFx || [])) if (!r0.includes(q)){ if (q.walls.length > 1) win.corner++; }
          if (m.inset > 0) win.inset++;
        }
        if (Z){ win.blows += me.hits - h0; win.end = m.t; continue; }
        /* THE CLOSE: the close voice itself says it was the clock's, with both alive */
        win.end = m.t;
        win.clock = win.closeVoice === 1 && !m.over ? 1 : 0;
        const kinds = Object.keys(win.ns).length;
        win.score = win.clock && win.castVoice === 1 && win.snaps >= 2
          ? (4 + Math.min(win.snaps, 8) * 0.5 + Math.min(kinds, 5) * 1.0 + Math.min(win.blows, 8) * 0.2
             + (win.start <= 1 ? 0.5 : 0) + (win.corner ? 0.5 : 0) + (win.inset ? 0.5 : 0))
          : 0;
        win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
        win.nList = Object.keys(win.ns).map(Number).sort((p, q) => p - q).join(" ");
        if (win.score > 0) pend = win;
        win = null;
      }
      if (best) out.push(best);
    }
  } finally {
    if (Object.prototype.hasOwnProperty.call(AC.SFX, "play")) delete AC.SFX.play;
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=102201)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--also", default="aureole:102602,widowmaker:102007",
                    help="foe:seed pairs scored besides the grid (the voice lab's real window, the picture lab's watched fight)")
    ap.add_argument("--out", default="../07-shorts/v102/rebuttal-window.mp4")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs, TAIL])
        for pair in [x for x in a.also.split(",") if x]:
            f, sd = pair.split(":")
            rows += page.evaluate(JS, [RID, [f], [int(sd)], a.secs, TAIL])
        rows.sort(key=lambda r: -r["score"])
        assert not errors, errors[:3]
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds (+ {a.also})  ·  Lodestone side A\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'touch':>6}{'snaps':>6}"
              f"{'counts heard':>14}{'start':>6}{'corner':>7}{'inset':>6}{'blows':>6}{'score':>7}")
        for r in rows[:14]:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['touches']:>6}"
                  f"{r['snaps']:>6}{r['nList']:>14}{r['start']:>6}{r['corner']:>7}{r['inset']:>6}{r['blows']:>6}"
                  f"{r['score']:>7.2f}")
        if rows:
            b = rows[0]
            lead = 1.2
            print(f"\n  the pick's snaps, in order: {' '.join(map(str, b['seq']))}   (hex-snaps {b['hexSnaps']}, "
                  f"cast voice {b['castVoice']}, close voice {b['closeVoice']})")
            print(f"\n  FILM THE WINDOW AND NOT THE FIGHT:\n")
            print(f"    python cinema_clip.py --game {a.game} "
                  f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
            print(f"      --at {max(0, b['t'] - lead):.2f} "
                  f"--window {b['dur'] + lead + TAIL:.2f} --end-at-window "
                  f"--fps 60 --w 540 --out {a.out}")
        if a.json:
            pathlib.Path(a.json).write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
