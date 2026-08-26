#!/usr/bin/env python3
"""How many DISTINCT images does the slow motion actually produce?

The sim runs on a fixed 1/120 step. Below about 0.25x, a 60fps frame feeds the
accumulator less than half a step, so most frames redraw an unchanged world.
The display is at 60 and the content is not. This counts it directly, with the
interpolator on and off, over the drop phase of a real set-piece.

  python3 cinema_smooth_probe.py
"""
from __future__ import annotations
import pathlib, sys
from scpage import game

HERE = pathlib.Path(__file__).parent
JS = r"""
([idA, idB, seed, fps, interp]) => {
  /* AUDIT: the probe used to assume its hardcoded seed had a cut; when the
     bar moved to 1.90 that stopped being true and it silently measured
     nothing. It now scans seeds until it finds one that clears the bar. */
  let plan = null, s2 = seed >>> 0;
  for (let k = 0; k < 40 && (!plan || !plan.cuts.length); k++) {
    s2 = (Math.imul(s2, 1103515245) + 12345) >>> 0;
    plan = window.cinePlan(idA, idB, s2);
  }
  if (!plan || !plan.cuts.length) return { err: "no cut found in 40 seeds" };
  seed = s2;
  CINE.on = true; CINE.interp = !!interp; CINE.reset();
  CINE.plan = plan.cuts.slice(); CINE.acc = 0;
  const m = new AC.Match(idA, idB, seed); m.introT = 0;
  const raw = 1 / fps, dt = AC.CONFIG.physics.dt;
  let frames = 0, distinct = 0, longest = 0, run = 0, phase = "";
  const seen = [];
  while (!m.over && frames < 400000) {
    const before = m.t;
    const alpha = CINE.pump(raw, m, 1);
    if (CINE.cut) {
      frames++;
      // a frame shows something new if the sim moved OR the interpolator did
      const moved = (m.t !== before) || (interp && alpha > 0);
      if (moved) { distinct++; longest = Math.max(longest, run); run = 1; }
      else run++;
      seen.push(CINE.phase);
    } else if (frames > 0) break;
  }
  longest = Math.max(longest, run);
  const dropFrames = seen.filter(p => p === "drop").length;
  return { frames, distinct, longest, dropFrames,
           pct: Math.round(distinct / Math.max(1, frames) * 100) };
}
"""

def main() -> int:
    with game(game_path=(HERE / "sc-cinema.html").resolve()) as (page, err):
        page.evaluate("AC.setResolution(360, 640)")
        print("one killing-blow set-piece, rendered at 60fps\n")
        print("  interp   frames  distinct   %   longest identical run")
        for interp in (False, True):
            r = page.evaluate(JS, ["gravemourn", "dawnbringer", 2901315739, 60, interp])
            if "err" in r: print("  ", r["err"]); continue
            print(f"  {'ON ' if interp else 'OFF'}      {r['frames']:5}   {r['distinct']:6}"
                  f"  {r['pct']:3}%        {r['longest']:3}")
        if err: print("page errors", err[:2])
    print("\n^ 'longest identical run' is the stutter, in frames. Anything above")
    print("  1 is the display showing the viewer the same image twice.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
