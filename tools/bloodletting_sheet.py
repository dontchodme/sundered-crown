#!/usr/bin/env python3
"""BLOODLETTING, AS A SHEET — the throw, the stick, the mill, and the ceiling.

    python bloodletting_sheet.py --out ../05-reference/v59/bloodletting-states

SHAPE QUESTIONS GO TO A SHEET; SCALE QUESTIONS NEED THE VIDEO (CLAUDE.md §0,
and v53 spent three rounds on Revenant's hand size because a sheet shows the
object STILL and every size complaint was about it in motion among two others).
This answers the shape questions and does not pretend to answer the other.

## THE FOUR PANELS THAT MATTER ARE THE LAST FOUR

Design §7c, and it is the line the whole ultimate rests on:

> **THE CEILING** — while it stands, the quarry can carry more bleed than
> anything else in the game can put on it. §3 says this is the mechanic, SO IT
> HAS TO BE VISIBLE. The stack readout going past four is the only evidence on
> screen that the ceiling moved.
>
> **Photograph the stack readout at 5, 6, 7 and 8 off a real match before
> tuning anything.**

v54 §2c is the precedent and it nearly shipped a build: Deadfall's ARMING and
ARMED states were separated by alpha alone, and photographed off a real match
they did not separate at all. **A viewer cannot see a constant** — and until
this build, `_stBleed` drew `Math.min(4, n)` drips, so eight stacks looked
exactly like four and the +7.9pp mechanic had NO representation whatsoever.

Two things carry it now and both are in these frames: the drip count on the
shell is clamped to the fighter's own ceiling rather than to four, and the
status tag prints the count while — and only while — the ceiling is up.

## AND `stick` IS THE ONE THAT CAN BE MISSED

Design §7c again: "it stops. This is the frame that tells the viewer it is
staying, and if it does not read, the ultimate looks like a missed shot."

It drives a REAL match — no posed objects — to the first frame that satisfies
each panel's own predicate, and photographs the canvas the game draws.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

SEEK_JS = r"""([rid, foe, sd, want, secs]) => {
  /* THE LIVE PAGE STANDS DOWN, or the rAF loop redraws its OWN match over this
     one between the draw and the shutter -- `deadfall_sheet` photographed a
     fight nobody asked for before this flag was set. The demo panel is a DOM
     overlay, so hiding it is separate. */
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const u = me.w.ult, HEM = AC.STATUS.hemorrhage;
  let step = 0, bestDwell = -1;

  const stackWant = want.startsWith("stack") ? +want.slice(5) : 0;

  while (!m.over && step < secs / DT){
    /* THREE COPIES NOW, so every predicate below asks about the SET rather
       than about one object -- and `d` is the distance to the NEAREST live
       one, because "the quarry is inside the disc" is true of the set the
       moment it is true of any member. */
    const wasLanded = me.ultSpectres.some(S2 => !S2.dead && S2.landed);
    m.step(DT); step++;
    const live = me.ultSpectres.filter(S2 => !S2.dead);
    const S = live.find(S2 => S2.landed) || live[0] || null;
    let d = 1e9;
    for (const S2 of live) d = Math.min(d, Math.hypot(th.x - S2.x, th.y - S2.y));
    const dead = me.ultSpectres.filter(S2 => S2.dead);
    const fadeMax = dead.length ? Math.max.apply(null, dead.map(S2 => S2.fade))
                                : 0;
    let ok = false;

    /* THE THROW. The copy is in the air and has left the weapon far enough
       that both it and the caster are readable as two objects. */
    if (want === "throw") ok = live.length > 0 && live.every(S2 => !S2.landed)
                               && live[0].t > u.flight * 0.45;

    /* THE STICK, AND IT IS THE FRAME THAT SAYS IT IS STAYING. Design 7c: if
       this does not read, the ultimate looks like a missed shot. Taken on the
       first frame after landing, which is the frame the sound and the beat
       both fire on. */
    if (want === "stick") ok = live.some(S2 => S2.landed) && !wasLanded;

    /* THE MILL, WITH SOMETHING IN IT. Photographed at the deepest the quarry
       gets inside the disc, because a copy standing in an empty room is a
       picture of the object and not a picture of the mechanic. */
    if (want === "mill"){
      if (S && live.some(S2 => S2.landed) && m.hitStop <= 0 && d < u.disc){
        const dwell = 1 - d / u.disc;
        if (dwell > bestDwell){ bestDwell = dwell; ok = true; }
      }
    }

    /* THE COPY STANDING ALONE — the object in open space, which design 7b
       calls the strongest thing in Rick's section 1 and the first thing in
       this game the two balls have to navigate AROUND. */
    if (want === "alone") ok = live.length > 0
                               && live.every(S2 => S2.landed && S2.stand > 0.6)
                               && d > u.disc * 1.45 && m.hitStop <= 0;

    /* AND IT DISSOLVES. The window closing is not the same event as the
       picture of it ending. */
    if (want === "close") ok = !live.length && dead.length
                               && fadeMax > 0.35 && fadeMax < 0.8;

    /* THE CEILING, AT 5, 6, 7 AND 8 — design 7c's own instruction, and the
       only evidence on screen that the ceiling moved.

       THE TAG HAS TO BE UP TOO. The drip count on the shell is the persistent
       readout and the tag is the one that carries the NUMBER, so a frame with
       the stacks but no tag would show half of what was built. `life > 0.35`
       keeps it away from its own fade. */
    if (stackWant){
      const n = th.stacks("hemorrhage");
      const tag = m.tags.some(g => g.key === "hemorrhage" && g.life > 0.35);
      ok = n === stackWant && th.bleedCap > HEM.maxStacks && tag
           && m.hitStop <= 0;
    }

    if (ok){
      AC.__draw(m);
      /* THE PIXELS COME BACK IN THIS SAME JS TURN. The composited frame lives
         in a drawing buffer that is gone by the time an out-of-process
         screenshot asks for it. */
      const shot = { t: +m.t.toFixed(2),
                     live: live.length,
                     stand: S ? +S.stand.toFixed(2) : null,
                     ticks: me.ultSpectres.reduce((q, S2) => q + S2.ticks, 0),
                     d: Math.round(Math.min(d, 9999)), disc: u.disc,
                     hem: th.stacks("hemorrhage"), cap: th.bleedCap,
                     fade: +fadeMax.toFixed(2),
                     dwell: +bestDwell.toFixed(2),
                     png: document.getElementById("cv").toDataURL("image/png") };
      if (want !== "mill") return shot;
      window.__best = shot;
    }
  }
  return (want === "mill") ? (window.__best || null) : null;
}"""

PANELS = [
    ("throw",  "THE THROW — the copy has left the weapon. Same silhouette, red"
               " and ghosted"),
    ("stick",  "THE STICK — it stops. Design §7c: if this frame does not read,"
               " the ultimate looks like a MISSED SHOT"),
    ("alone",  "THE OBJECT IN OPEN SPACE — nothing in this game has ever"
               " occupied the middle of the floor. Design §7b calls this the"
               " strongest thing in the §1"),
    ("mill",   "THE MILL, WITH SOMETHING IN IT — photographed at the deepest"
               " the quarry gets inside the disc"),
    ("stack5", "THE CEILING AT 5 — one past what anything else in this game"
               " can put on a fighter"),
    ("stack6", "THE CEILING AT 6"),
    ("stack7", "THE CEILING AT 7"),
    ("stack8", "THE CEILING AT 8 — the top of the raised ceiling. Before this"
               " build `_stBleed` drew min(4, n) drips, so this frame was"
               " IDENTICAL to four"),
    ("close",  "AND IT DISSOLVES — the window closing is not the same event as"
               " the picture of it ending"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bloodletting.html")
    ap.add_argument("--relic", default="bloodmirror")
    ap.add_argument("--foe", default="thornwake")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="../05-reference/v59/bloodletting-states")
    A = ap.parse_args()

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    path = resolve_game(A.game)
    print(f"\nBLOODLETTING — the states, off a real match\n  game {path.name}")
    print(f"  {A.relic} vs {A.foe}, seed {A.seed}\n")

    missed = []
    with game(game_path=path) as (page, errors):
        for want, caption in PANELS:
            r = page.evaluate(SEEK_JS, [A.relic, A.foe, A.seed, want, A.secs])
            if not r:
                print(f"  --    {want:<7} NOT REACHED in {A.secs:g}s")
                missed.append(want)
                continue
            p = out.parent / f"{out.name}-{want}.png"
            p.write_bytes(base64.b64decode(r.pop("png").split(",", 1)[1]))
            print(f"  ok    {want:<7} t={r['t']:>6}s  live {r['live']}  "
                  f"stand {r['stand']}  "
                  f"ticks {r['ticks']}  sep {r['d']}/{r['disc']:g}  "
                  f"HEM {r['hem']}/{r['cap']}   -> {p.name}")
            print(f"        {caption}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))
    if missed:
        print(f"\n  {len(missed)} panel(s) never happened in this fight: "
              f"{', '.join(missed)}.")
        odd = [x for x in missed if x in ("stack5", "stack7")]
        if odd:
            print("\n  AND THE ODD NUMBERS DO NOT EXIST. Design 7c asks for "
                  "the readout at 5, 6,\n  7 AND 8 -- and 5 and 7 are "
                  "unreachable by arithmetic rather than by luck:\n  EVERY "
                  "application in this school is TWO. The spectre applies "
                  "`bleed` 2 a\n  tick and the blade applies "
                  "`onHit:{hemorrhage:2}`, so a quarry starting at 0\n  goes "
                  "2, 4, 6, 8 and can only ever be even. Not a defect and not "
                  "a seed\n  problem: the design asked to photograph a state "
                  "the numbers forbid.")
        if "stack8" in missed:
            print("\n  A MISSING `stack8` IS A FINDING AND NOT A SEED PROBLEM "
                  "if it survives two\n  more seeds -- it would mean the "
                  "ceiling is reachable in the probe's\n  counters and not in "
                  "a fight a person could watch.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
