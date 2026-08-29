#!/usr/bin/env python3
"""EVERY ULTIMATE'S REAL ultFx, CAUGHT OUT OF A REAL FIGHT.

    python ult_fx_capture.py
    python ult_fx_capture.py --ids paradox,slagheart --out ../05-reference/post/ultfx.json

WHY THIS EXISTS
---------------
ult_filmstrip.py and ult_bloom_probe.py build a synthetic fx block:

    m.ultFx = { w:id, kind:w.ult.kind, ... t:t, life:life }

`kind` but NO `phase`. Eight ultimates branch on phase in the renderer with
`if (u.phase === ...) else if ...` and no fallback, so they draw NOTHING and
both tools reported that as a low score rather than as a blank:

    emberedge detonate    marrowdraw ballista   twinshade split
    slagheart latch       lastlight  harrow     redflail  spinstorm
    paradox   stasis      foregone   retrace

THE FIX IS NOT TO HAND-WRITE THE MISSING PHASES. That would put a picture on
the sheet that the engine never produces, and every number taken off it would
be a measurement of the guess -- the exact defect class CLAUDE.md 4.1 is about,
committed deliberately this time. So the blocks are CAPTURED: a real match is
stepped until `fireUlt` writes one, and every distinct phase it passes through
is copied out verbatim.

HOW THE ULT IS MADE TO FIRE. `f.charge` is set to `f.w.ult.charge`, which is
the same test step() applies (`if (f.charge >= f.w.ult.charge)`), so fireUlt
runs its own ordinary path and builds its own ordinary block. Nothing about
the ultimate is bypassed.

GEOMETRY IS THE ONE THING A REPLAY MUST OVERWRITE. A captured block carries
the positions the fighters were at when it fired; a filmstrip places them at
fixed points so every relic is judged on the same frame. So `x/y/tx/ty` are
recorded but a replayer is expected to substitute its own -- see `replay()`.
Everything else, including `phase` and every relic-specific field, is the
engine's.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
FOE, ALT_FOE = "grudgebearer", "dawnbringer"

CAPTURE_JS = """([id, foe, seed, maxT]) => {
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const w = AC.WEAPONS.find(x => x.id === id);
  const dt = AC.CONFIG.physics.dt;

  /* Placed the way the filmstrip places them, BEFORE the cast, so the block
     is born with a geometry a sheet can actually reproduce. */
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.26; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.74; m.b.y = A.h * 0.68;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;

  /* The same test step() applies. fireUlt then runs its ordinary path. */
  m.a.charge = w.ult.charge;

  const seen = {}, order = [];
  let steps = 0;
  const maxSteps = Math.ceil(maxT / dt);
  while (steps < maxSteps){
    m.step(dt); steps++;
    const u = m.ultFx;
    if (!u) continue;
    const key = u.phase === undefined ? "-" : String(u.phase);
    if (seen[key]) continue;
    /* Structured clone via JSON: the block is plain data apart from `aff`,
       which is a palette object and survives. A live reference would go on
       mutating after capture and the library would record the LAST state of
       every phase rather than its first. */
    let copy;
    try { copy = JSON.parse(JSON.stringify(u)); }
    catch (e) { continue; }
    copy.__capturedAt = steps * dt;
    seen[key] = copy; order.push(key);
  }
  return { kind: w.ult.kind, name: w.ult.name, phases: order, blocks: seen };
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-paradox-fx.html")
    ap.add_argument("--ids", default="")
    ap.add_argument("--seed", type=int, default=31337)
    ap.add_argument("--max-t", type=float, default=14.0,
                    help="seconds of match to step while waiting for phases")
    ap.add_argument("--out", default="../05-reference/post/ultfx-library.json")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")

    with game(game_path=g) as (page, errors):
        ids = [i.strip() for i in A.ids.split(",") if i.strip()] or \
              page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        lib, blank = {}, []
        for rid in ids:
            foe = ALT_FOE if rid == FOE else FOE
            r = page.evaluate(CAPTURE_JS, [rid, foe, A.seed, A.max_t])
            if not r["phases"]:
                blank.append(rid)
                continue
            lib[rid] = r
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(lib, indent=1), encoding="utf8")

    print(f"  {out.name}  --  {len(lib)} of {len(ids)} relics captured")
    print(f"  {'relic':<14}{'kind':<12}phases")
    for rid, r in lib.items():
        print(f"  {rid:<14}{r['kind']:<12}{', '.join(r['phases'])}")
    if blank:
        print(f"\n  NEVER FIRED in {A.max_t}s: {', '.join(blank)}")
        print("  -- not a capture failure to shrug at: the block a tool replays")
        print("     for these would still be a guess. Raise --max-t or pick a")
        print("     seed where the ult lands.")


if __name__ == "__main__":
    main()
