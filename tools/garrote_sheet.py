#!/usr/bin/env python3
"""THE WIRE, AS A SHEET -- the ring standing, the catch, the hold, the throw.

    python garrote_sheet.py --out ../05-reference/v60/garrote-states

SHAPE QUESTIONS GO TO A SHEET; SCALE QUESTIONS NEED THE VIDEO (CLAUDE.md §0,
and v53 spent three rounds on Revenant's hand size because a sheet shows the
object STILL and every size complaint was about it in motion among two others).
This answers the shape questions and does not pretend to answer the other.

    THE ONE THAT MATTERS IS `hold`. Brief §9: "THE SNAG — the foe stops moving
    AND KEEPS SWINGING. If this does not read, the ultimate looks like a stun
    and the whole separation in §3 is invisible."

**A held ball with a moving weapon is a picture this game has never drawn.**
Every other hold in the roster locks the weapon too, so there has never been a
frame in which one fighter is anchored and still swinging. If it reads as a
frozen fighter, the design is not on screen -- and no probe in this repo can
say which of those a viewer sees. `garrote_relic_probe [4]` proves the weapon
is TURNING; it cannot prove anybody can tell.

`hold` is photographed at the moment the caught fighter's own blade is furthest
from where the wire has anchored it, which is the frame where "held but
swinging" is most visible if it is visible at all.

v54 §2c is the precedent and it nearly shipped broken: Deadfall's ARMING and
ARMED states were separated by alpha alone, and photographed off a real match
they did not separate at all.

It drives a REAL match -- no posed objects -- to the first frame that satisfies
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
  /* THE LIVE PAGE STANDS DOWN, or the rAF loop redraws its OWN match over
     this one between the draw and the shutter -- `deadfall_sheet` photographed
     a fight nobody asked for before this flag was set. The demo panel is a DOM
     overlay, so hiding it is separate. */
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  window.__m = m;
  const R = AC.CONFIG.physics.ballR;
  let step = 0, wasCaught = false, sinceCatch = 0, bestSwing = -1;
  while (!m.over && step < secs / DT){
    const caughtBefore = !!(me.ultWire && me.ultWire.caught);
    m.step(DT); step++;
    const W = me.ultWire, u = me.w.ult;
    const d = Math.hypot(th.x - me.x, th.y - me.y);
    const caught = !!(W && W.caught);
    if (caught && !caughtBefore) sinceCatch = 0;
    if (caught) sinceCatch += DT;
    let ok = false;

    /* THE RING, STANDING AND EMPTY. The wind-up and the telegraph: the first
       object in this game whose area IS the weapon's own hit range, drawn. A
       viewer who sees it should know where it is unsafe to be -- and the
       quarry is deliberately OUTSIDE it here, so the ring is read on its own
       rather than as a thing wrapped round a catch. */
    if (want === "ring")  ok = !!W && !caught && W.t > 0.4
                               && d > u.radius * 1.35;

    /* THE MOMENT BEFORE. The quarry is inside the ring's own radius and has
       not been taken yet -- one frame of jeopardy, and the only frame in which
       the ring's boundary and the thing it is about to catch are both on
       screen. */
    /* AND THE BOUNDARY IS `radius + ballR`, NOT `radius`. The ring is drawn
       at the hammer's reach and the catch fires when the quarry's SHELL
       touches it, which is 34px further out between centres. The first cut of
       this predicate used `radius` and could never be satisfied -- the catch
       had always already happened. Not a bug: a ball caught when its edge
       meets the wire is what "caught in the wire" means. */
    if (want === "verge") ok = !!W && !caught && d < (u.radius + R) * 1.18
                               && d > (u.radius + R) * 1.02;

    /* THE CATCH. */
    if (want === "catch") ok = caught && sinceCatch > 0.05 && sinceCatch < 0.30;

    /* THE HOLD, AND IT IS THE PANEL THE WHOLE DESIGN RESTS ON. Photographed
       where the caught fighter's own blade is furthest from the wire that is
       holding it -- the frame in which "the ball is held and the weapon is
       not" is most visible if it is visible at all. `th.stun <= 0` because a
       fighter that happens to be in ordinary hitstun is not swinging either,
       and that frame would say the opposite of the sentence. */
    if (want === "hold"){
      if (caught && sinceCatch > 0.35 && th.stun <= 0 && m.hitStop <= 0){
        /* how far the blade has come round from the wielder's own bearing */
        const bx = Math.cos(th.theta), by = Math.sin(th.theta);
        const ax = (me.x - th.x), ay = (me.y - th.y);
        const al = Math.hypot(ax, ay) || 1;
        const swing = 1 - (bx * ax + by * ay) / al;   // 0 aimed at, 2 away
        /* NO FLOOR, AND THE ACHIEVED ANGLE IS REPORTED INSTEAD. The first cut
           demanded swing > 1.4 and produced NO PANEL against Axiom -- which
           looked like the hold never happening and was actually the foe's
           WEAPON TYPE. A greatsword is `mode:"swing"` and recomputes `theta`
           from the AIM every frame (open item 10), so its blade points at the
           thing holding it and can never come round. A missing panel says
           "this did not happen"; a panel with a number on it says which
           weapons can show the sentence and which cannot. */
        if (swing > bestSwing){ bestSwing = swing; ok = true; }
      }
    }

    /* THE TAIL, AND IT IS THE PICTURE COST OF `expire:"ring"`. The ring has
       blown apart, the payoff has visibly happened, and the window is STILL
       OPEN with the hammer turning at 6x for the rest of its 8 seconds. That
       is the arm Rick took on 2026-09-01 and it is worth +14.7 points over
       ending the window on the connect -- and it is the one frame in this
       sheet that could say the picture is contradicting the mechanic.

       Nothing is drawn for it today. If this panel reads as "the ultimate is
       over and the hammer is just fast", that is the finding. */
    if (want === "tail") ok = !!W && W.spent && W.t > u.dur * 0.6
                              && m.hitStop <= 0;

    /* THE THROW. The ring is gone, the quarry is leaving, and the wire is
       still fading behind it -- this is the payoff for an eight-second
       window and it is ONE frame. */
    if (want === "throw") ok = !W && me.wireFade > 0.45 && me.wireFade < 0.85
                               && wasCaught;
    if (caught) wasCaught = true;
    if (!W && me.wireFade <= 0.1) wasCaught = false;

    if (ok){
      AC.__draw(m);
      /* THE PIXELS COME BACK IN THIS SAME JS TURN. The composited frame lives
         in a drawing buffer that is gone by the time an out-of-process
         screenshot asks for it -- `deadfall_sheet` got a near-black canvas
         with ghosts of the balls in it before this was moved inline. */
      const shot = { t: +m.t.toFixed(2),
                     caught: caught, held: W ? +W.held.toFixed(2) : null,
                     fade: +me.wireFade.toFixed(2),
                     foeStun: +th.stun.toFixed(3),
                     d: Math.round(d), radius: u.radius,
                     swing: +bestSwing.toFixed(2), foeMode: th.w.mode,
                     png: document.getElementById("cv").toDataURL("image/png") };
      /* `hold` keeps looking for a better frame; everything else takes the
         first one that satisfies its predicate. */
      if (want !== "hold") return shot;
      window.__best = shot;
    }
  }
  return (want === "hold") ? (window.__best || null) : null;
}"""

PANELS = [
    ("ring",  "THE RING, STANDING AND EMPTY — the hammer's own hit range,"
              " drawn. The telegraph, and the only warning the other fighter"
              " gets"),
    ("verge", "THE MOMENT BEFORE — the quarry is inside the radius and has not"
              " been taken yet"),
    ("catch", "THE CATCH — the wire closes. It deals nothing and applies one"
              " Hemorrhage"),
    ("hold",  "THE HOLD, AND THIS IS THE ONE. The ball is anchored and the"
              " quarry's own blade is at full swing. If this reads as a FROZEN"
              " fighter, the design is not on screen — brief §9"),
    ("tail",  "THE TAIL — the ring is spent and the window is STILL OPEN, with"
              " the hammer turning at 6x and nothing at its reach. This is the"
              " picture cost of expire:\"ring\", and NOTHING IS DRAWN FOR IT"),
    ("throw", "THE THROW — the ring is gone, the wire is fading, and the quarry"
              " is leaving at over the speed ceiling"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-garrote.html")
    ap.add_argument("--relic", default="ravelbone")
    ap.add_argument("--foe", default="grudgebearer")
    ap.add_argument("--seed", type=int, default=11961)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="../05-reference/v60/garrote-states")
    A = ap.parse_args()

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    path = resolve_game(A.game)
    print(f"\nGARROTE — the five states, off a real match\n  game {path.name}")
    print(f"  {A.relic} vs {A.foe}, seed {A.seed}\n")

    missed = 0
    with game(game_path=path) as (page, errors):
        for want, caption in PANELS:
            r = page.evaluate(SEEK_JS, [A.relic, A.foe, A.seed, want, A.secs])
            if not r:
                print(f"  --    {want:<6} NOT REACHED in {A.secs:g}s")
                missed += 1
                continue
            p = out.parent / f"{out.name}-{want}.png"
            p.write_bytes(base64.b64decode(r.pop("png").split(",", 1)[1]))
            extra = ""
            if want == "hold":
                extra = (f"  swing {r.get('swing')} / 2.0 "
                         f"(foe mode {r.get('foeMode')})")
            print(f"  ok    {want:<6} t={r['t']:>6}s  sep {r['d']}/"
                  f"{r['radius']:g}  fade {r['fade']}  foe stun {r['foeStun']}"
                  f"{extra}   -> {p.name}")
            print(f"        {caption}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))
    if missed:
        print(f"\n  {missed} panel(s) never happened in this fight. That is a "
              f"FINDING if it is\n  `hold` — try another seed before believing "
              f"it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
