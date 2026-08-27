#!/usr/bin/env python3
"""THE BLOOM SPREAD. One seed, one runtime, four columns, for Rick's eyes.

    python post_spread.py
    python post_spread.py --a paradox --b heartwood --seed 25064 --moments 3

`docs/RENDERER-BRIEF.md` §7 gate 2: every step ships side-by-side filmstrips,
old and new, same seed, same frame indices, one image. And §8.5, which is
CLAUDE.md rule 2: offer a SPREAD, not a guess. v43 landed its sound in one
round trip that way and v42 took four, because a spread of one can never
reveal that the register is wrong.

BOTH STRIPS COME OUT OF ONE RUNTIME, and that is not a detail. Chromium 128
and 151 disagree on the last bit of Math.pow, which is 112 fights in 192
(docs/RUNTIME-DRIFT.md) -- so a sheet whose control was rendered anywhere but
here would be comparing two different fights and calling the difference bloom.
Every tile below is drawn from the same page, the same match object, the same
frame.

WHICH MOMENTS. Not chosen by eye, and not the first thing on screen: the frame
at t=0 has nothing above the lowest threshold in the spread, so a sheet built
from it would show four identical tiles and read as "bloom does nothing". The
scan pass runs the fight at low resolution and measures the emissive mass
inside the arena rect -- how many pixels are bright enough to bloom at all --
then takes the peaks, kept apart so three tiles are not three frames of one
blow.

Writes a PNG to 05-reference/post/ and prints what changed, per column, so the
picture arrives with a number beside it.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-frame.html"
POST_JS = REPO / "src" / "render" / "post.js"
OUTDIR = REPO / "05-reference" / "post"

SCAN_JS = r"""
(cfg) => {
  /* THE DIRECTOR HAS TO BE RUNNING, and for four sessions of sheets it was
     not. Stepping the sim by hand and calling AC.__draw is not what the mp4
     does: cinema_clip.py resets CINE, plans the cuts, and then drives every
     frame through CINE.pump and CINE.drawLerped -- the same loop the live
     page runs. Without that there are no cuts, no zoom, no bars, no wash and
     no time dilation, and the interpolated draw is missing too. A sheet built
     the other way is a picture the video will never contain, which is the one
     thing docs/ARCHITECTURE.md §1 exists to prevent.

     `CINE` and `cinePlan` are reachable by bare name here: this runs in the
     game's own realm, and a top-level const IS visible to other classic
     scripts in the same realm. It is only across realms -- the app shell
     reaching into the frame -- that it needs the AC export. */
  window.__frozen = true;
  AC.setResolution(cfg.sw, cfg.sh);
  CINE.on = true; CINE.interp = true; CINE.reset(); CINE.acc = 0;
  CINE.plan = cinePlan(cfg.a, cfg.b, cfg.seed >>> 0).cuts;

  const m = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
  m.introT = 0;
  AC.__inject(m);
  AC.SFX.play = function () {};
  AC.SFX.resume = function () {};

  const cv = document.getElementById('cv');
  const g = cv.getContext('2d');
  const R = AC.renderer, k = R.k;
  const x0 = Math.max(0, Math.round(R.pad * k)), y0 = Math.max(0, Math.round(R.arenaTop * k));
  const w = Math.min(cv.width - x0, Math.round(R.aw * k));
  const h = Math.min(cv.height - y0, Math.round(R.ah * k));

  const FPS = 60, raw = 1 / FPS;
  const every = Math.max(1, Math.round(cfg.every * FPS));
  const out = [];
  let frame = 0, wall = 0;
  while (!m.over && frame < cfg.maxFrames) {
    const alpha = CINE.pump(raw, m, 1);
    wall += raw;
    frame++;
    if (frame % every) continue;
    m.shake = 0;                       // Math.random() per draw -- see SHEET_JS
    if (alpha > 0) CINE.drawLerped(R, m, alpha); else AC.__draw(m);
    const d = g.getImageData(x0, y0, w, h).data;
    let mass = 0;
    for (let i = 0; i < d.length; i += 4) {
      const l = (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) / 255;
      if (l > cfg.thresh) mass += l - cfg.thresh;
    }
    out.push({ frame: frame, t: +wall.toFixed(3), simT: +m.t.toFixed(3),
               mass: +mass.toFixed(2), cut: !!CINE.cut,
               wash: +(CINE.wash || 0).toFixed(3),
               tier: CINE.cut ? (CINE.cut.fatal ? 'KILL' : 'T' + CINE.cut.tier) : null });
  }
  return { samples: out, wall: +wall.toFixed(2), frames: frame,
           cuts: CINE.plan.length, over: m.over };
}
"""

SHEET_JS = (HERE / "postspread_sheet.js").read_text(encoding="utf-8")


def pick(samples, n, apart):
    """Peaks of emissive mass, kept apart so three tiles are not three frames
    of one blow. Greedy by mass, which is enough here and is at least a
    stated rule rather than a taste."""
    chosen = []
    for s in sorted(samples, key=lambda r: -r["mass"]):
        if s["mass"] <= 0:
            break
        if all(abs(s["t"] - c["t"]) >= apart for c in chosen):
            chosen.append(s)
        if len(chosen) == n:
            break
    return sorted(chosen, key=lambda r: r["t"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--a", default="paradox")
    ap.add_argument("--b", default="heartwood")
    ap.add_argument("--seed", type=int, default=25064)
    ap.add_argument("--pairs", default=None,
                    help="a:b:seed,a:b:seed -- one sheet, several fights, so a "
                         "register can be judged against more than one kind of "
                         "art at once. Overrides --a/--b/--seed.")
    ap.add_argument("--per", type=int, default=None,
                    help="moments taken from each pairing")
    ap.add_argument("--cuts", action="store_true",
                    help="only consider moments where the director is IN a "
                         "cut. Required for --effect cut: outside a cut the "
                         "ramp is zero by design and every column is the same "
                         "picture.")
    ap.add_argument("--moments", type=int, default=3)
    ap.add_argument("--apart", type=float, default=2.0,
                    help="minimum seconds between chosen moments")
    ap.add_argument("--tile", type=int, default=380)
    ap.add_argument("--wide", type=int, default=620,
                    help="tile width for the two-column `chosen` sheet")
    ap.add_argument("--effect",
                    choices=("bloom", "trails", "chosen", "cut", "grade"),
                    default="bloom",
                    help="which spread. `trails` holds bloom at the chosen "
                         "default and varies only the tail length.")
    ap.add_argument("--warm", type=int, default=None,
                    help="frames run into the chain before the one captured. "
                         "Trails are history and a cold buffer shows none.")
    ap.add_argument("--every", type=float, default=0.1, help="scan interval")
    ap.add_argument("--out", default=None)
    A = ap.parse_args()

    path = pathlib.Path(A.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2

    post_src = POST_JS.read_text(encoding="utf-8")

    with game(game_path=path) as (page, errors):
        if not page.evaluate("() => !!document.createElement('canvas')"
                             ".getContext('webgl2')"):
            print("! no WebGL2 in this Chromium")
            return 2
        page.add_script_tag(content=post_src)

        if not page.evaluate("() => !!(window.AC && AC.CINE)"):
            print("! this build does not export CINE -- run cineexport_build.py")
            return 2

        if A.pairs:
            pairs = []
            for spec in A.pairs.split(","):
                x, y, sd = spec.split(":")
                pairs.append({"a": x, "b": y, "seed": int(sd)})
        else:
            pairs = [{"a": A.a, "b": A.b, "seed": A.seed}]
        per = A.per if A.per is not None else (
            A.moments if len(pairs) == 1 else 2)

        label = " + ".join(P["a"] + " v " + P["b"] for P in pairs)
        print("")
        print("POST SPREAD  " + label)
        moments = []
        for pi, P in enumerate(pairs):
            print(f"  scanning {P[chr(97)]} v {P[chr(98)]} seed {P[chr(115)+chr(101)+chr(101)+chr(100)]} at {A.every}s...")
            scan = page.evaluate(SCAN_JS, {
                "a": P["a"], "b": P["b"], "seed": P["seed"],
                "every": A.every, "sw": 270, "sh": 480,
                "thresh": 0.62, "maxFrames": 6000,
            })
            print(f"    {scan['frames']} frames, {scan['wall']}s of video, "
                  f"{scan['cuts']} cuts planned")
            pool = scan["samples"]
            if A.cuts or A.effect == "cut":
                pool = [r for r in pool if r["cut"]]
                print(f"    {len(pool)} of {len(scan['samples'])} samples are "
                      f"inside a cut")
            chosen = pick(pool, per, A.apart)
            if not chosen:
                print("! nothing in this pairing clears the threshold; a row")
                print("  from it would be identical tiles.")
                return 1
            for mm in chosen:
                print("    frame " + str(mm["frame"]).rjust(5)
                      + "  " + format(mm["t"], ">6.2f") + "s  mass "
                      + format(mm["mass"], ">9.1f")
                      + ("  " + mm["tier"] + " CUT" if mm["tier"] else ""))
                moments.append({"pair": pi, "t": mm["t"],
                                "frame": mm["frame"]})

        if A.effect == "grade":
            cols = ["off", "subtle", "mid", "strong"]
            warm = A.warm if A.warm is not None else 24
            title = "GRADE — " + label
            sub = ("one variable: how graded. vignette, grain and contrast "
                   "move together; bloom and trails are the chosen ones.")
        elif A.effect == "cut":
            cols = ["off", "gentle", "mid", "strong"]
            warm = A.warm if A.warm is not None else 24
            title = "CUT RAMP — " + label
            sub = ("one variable: how much brighter the director's own cut "
                   "makes the bloom. every column is the chosen look. "
                   + label + ", seed " + str(pairs[0]["seed"]))
        elif A.effect == "chosen":
            cols = ["off", "chosen"]
            warm = A.warm if A.warm is not None else 20
            title = "AS CHOSEN — " + label
            sub = ("does the register hold on art that is not Paradox's "
                   "lightning? bloom + trails at the chosen settings.")
        elif A.effect == "trails":
            cols = ["off", "short", "mid", "long"]
            warm = A.warm if A.warm is not None else 20
            title = "TRAIL SPREAD — " + label
            sub = ("one variable: tail length in SECONDS. bloom is held at "
                   "the chosen default in every column, the control included.")
        else:
            cols = ["off", "low", "mid", "high"]
            warm = A.warm if A.warm is not None else 1
            title = "BLOOM SPREAD — " + label
            sub = ("same seed, same frame, one runtime. OFF is the untouched "
                   "2D canvas.")
        print(f"  rendering the sheet at 1080x1920, {warm} warm frames…")
        sheet = page.evaluate(SHEET_JS, {
            "pairs": pairs,
            "moments": moments,
            "cols": cols,
            "tile": A.wide if A.effect == "chosen" else A.tile,
            "effect": A.effect, "warm": warm,
            "title": title, "sub": sub,
            "runtime": f"build {path.name}",
        })
        if errors:
            print("! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = pathlib.Path(A.out) if A.out else (
        OUTDIR / (A.effect + "-spread-"
                  + "-".join(P["a"] + "-" + P["b"] + "-" + str(P["seed"])
                             for P in pairs) + ".png"))
    out.write_bytes(base64.b64decode(sheet["png"]))

    print(f"\n  {sheet['renderer']}")
    print("")
    print("  " + "frame".rjust(7) + " " + "variant".rjust(8) + " "
          + "% px changed".rjust(13) + " " + "mean add".rjust(9) + "  tier")
    for r in sheet["report"]:
        print("  " + str(r["frame"]).rjust(7) + " " + r["variant"].rjust(8)
              + " " + format(r["pctChanged"], ">12.1f") + "% "
              + format(r["meanAdd"], ">9.2f") + "  "
              + (r.get("tier") or "-")
              + ("  wash " + format(r["wash"], ".3f")
                 if r.get("wash") is not None else ""))
    print(f"\n  wrote {out}  ({sheet['w']}x{sheet['h']}, "
          f"{out.stat().st_size // 1024} KB)")
    print("\n  THE CHECK IS RICK'S EYES. The numbers say the columns differ;")
    print("  they cannot say which one is right.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
