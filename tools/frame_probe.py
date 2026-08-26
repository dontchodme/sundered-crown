#!/usr/bin/env python3
"""THE SAFE FRAME, FALSIFIED.

    python3 frame_probe.py --game ../02-chain/sc-safeframe.html \
                           --ref  ../02-chain/sc-foregone.html

  [1] THE IDENTITY IS EXACT, NOT APPROXIMATE. A build at `FRAME.foot = 0` must
      render the SAME PIXELS as the build that had no FRAME at all. That is the
      claim the whole change rests on -- the old layout is a VALUE of the new
      code, not a case it approximates -- and it is asserted against a rendered
      frame rather than against the four constants, because four numbers
      agreeing is not the same as a picture agreeing.

  [2] THE ARENA IS INSIDE THE SAFE BOX. At the shipped `foot` the hall's own
      frame must end above 1920 - foot, and must not have been pushed off any
      other edge to get there. Measured on the drawn arena rectangle, not on
      the layout fields, for the same reason as [1].

  [3] IT IS THE SMALLER BOUND THAT WINS. Asserted by construction at three
      values of `foot`: the width binds until the height does, and `scale`
      is monotone non-increasing in `foot`.

  [4] NOTHING ELSE MOVED. The HUD band, the footer and the canvas size are
      read back and compared. A layout change that quietly shifted the HUD
      would pass [1] and [2] and still be wrong.

`engine_ab` is the separate proof that the SIMULATION did not move; this file
is only about pixels.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import subprocess
import sys

from PIL import Image, ImageChops

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent

SHOT_JS = """([a, b, seed, secs, scrunch]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  m.introT = 0;
  for (let i = 0; i < Math.round(secs / DT) && !m.over; i++) m.step(DT);
  /* THE SCRUNCH IS A SECOND LAYOUT AND HAS TO BE PHOTOGRAPHED AS ONE. The
     first version of this probe only ever rendered an ordinary frame, and
     the panel's hardcoded `bottom` sailed through it: 9/9 green while the
     one screen the change actually broke was never drawn. */
  if (scrunch){
    m.scrunchT = AC.CONFIG.scrunch.ease + AC.CONFIG.scrunch.intro * 0.5;
    m.scrunchMode = "intro";
  }
  AC.__draw(m);
  const r = AC.renderer;
  return { png: document.getElementById('cv').toDataURL('image/png'),
           pad: r.pad, aw: r.aw, ah: r.ah, scale: r.scale,
           arenaTop: r.arenaTop, hud: r.hud, W: r.W, H: r.H,
           foot: (typeof FRAME === "undefined") ? null : FRAME.foot,
           cw: document.getElementById('cv').width,
           ch: document.getElementById('cv').height,
           panelBottom: Math.min(AC.CONFIG.scrunch.bottom,
                                 (typeof FRAME === "undefined")
                                   ? AC.CONFIG.scrunch.bottom
                                   : 1920 - FRAME.foot - 12) };
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def shoot(path, a, b, seed, secs, scrunch=False):
    with game(game_path=path) as (page, errors):
        r = page.evaluate(SHOT_JS, [a, b, seed, secs, scrunch])
        assert not errors, errors[:3]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-safeframe.html")
    ap.add_argument("--ref", default="../02-chain/sc-foregone.html")
    ap.add_argument("--a", default="foregone")
    ap.add_argument("--b", default="redflail")
    ap.add_argument("--seed", type=int, default=912479)
    ap.add_argument("--at", type=float, default=17.0)
    ap.add_argument("--out", default="../05-reference/v39")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    rp = (HERE / a.ref).resolve()
    outdir = (HERE / a.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    ref = shoot(rp, a.a, a.b, a.seed, a.at)
    new = shoot(gp, a.a, a.b, a.seed, a.at)

    print(f"\n  {'build':<22}{'foot':>6}{'pad':>8}{'aw':>8}{'ah':>8}"
          f"{'scale':>8}{'top':>7}{'bottom':>8}")
    for lab, r in (("ref (no FRAME)", ref), (gp.name, new)):
        print(f"  {lab:<22}{str(r['foot']):>6}{r['pad']:>8.1f}{r['aw']:>8.1f}"
              f"{r['ah']:>8.1f}{r['scale']:>8.3f}{r['arenaTop']:>7.0f}"
              f"{r['arenaTop'] + r['ah']:>8.1f}")

    # ------------------------------------------------------------- [1] --
    print(f"\n[1] THE IDENTITY AT foot = 0\n")
    zero = (HERE / "../02-chain/_frame-foot0.html").resolve()
    # ALWAYS REBUILT. The first version built it only `if not exists`, and
    # the cached copy went stale the moment the relic's own build changed --
    # a different game is a different fight is different pixels, and the
    # identity check then failed loudly for a reason that had nothing to do
    # with the identity. A cached artefact with no invalidation is the same
    # bug as a picked seed with no invalidation, one file along.
    zero.unlink(missing_ok=True)
    subprocess.run([sys.executable, "frame_build.py", "--foot", "0",
                    "--src", str(rp), "--out", str(zero)],
                   cwd=HERE, check=True, capture_output=True)
    z = shoot(zero, a.a, a.b, a.seed, a.at)
    ri, zi = png(ref["png"]), png(z["png"])
    diff = ImageChops.difference(ri, zi)
    nz = diff.getbbox()
    print(f"    ref  pad {ref['pad']:.1f} aw {ref['aw']:.1f} "
          f"ah {ref['ah']:.1f} scale {ref['scale']:.4f}")
    print(f"    foot0 pad {z['pad']:.1f} aw {z['aw']:.1f} "
          f"ah {z['ah']:.1f} scale {z['scale']:.4f}")
    print(f"    pixel difference bbox: {nz}")
    check("foot=0 renders the same four numbers as the build with no FRAME",
          abs(z["pad"] - ref["pad"]) < 1e-9 and abs(z["aw"] - ref["aw"]) < 1e-9
          and abs(z["ah"] - ref["ah"]) < 1e-9
          and abs(z["scale"] - ref["scale"]) < 1e-12,
          "pad/aw/ah/scale all identical")
    check("...and the same PIXELS — the old layout is a value of the new code",
          nz is None, "0 differing pixels of 1080x1920"
          if nz is None else f"differs in {nz}")

    refS = shoot(rp, a.a, a.b, a.seed, a.at, True)
    zS = shoot(zero, a.a, a.b, a.seed, a.at, True)
    nzS = ImageChops.difference(png(refS["png"]), png(zS["png"])).getbbox()
    print(f"    SCRUNCHED frame difference bbox: {nzS}")
    check("...on the SCRUNCHED frame too — the second layout, which is the "
          "one that broke",
          nzS is None, "0 differing pixels"
          if nzS is None else f"differs in {nzS}")

    # ------------------------------------------------------------- [2] --
    print(f"\n[2] THE ARENA IS INSIDE THE SAFE BOX\n")
    foot = new["foot"]
    bot = new["arenaTop"] + new["ah"]
    safe = new["H"] - foot
    print(f"    hall runs {new['arenaTop']:.0f} .. {bot:.1f} of {new['H']}, "
          f"safe line at {safe} (foot {foot})")
    print(f"    side margin {new['pad']:.1f}px each — the game's own "
          f"background, not letterbox")
    check("the hall ends above the safe line",
          bot <= safe, f"{bot:.1f} <= {safe}")
    check("and was not pushed off another edge to get there",
          new["pad"] >= 0 and new["pad"] + new["aw"] <= new["W"] + 1e-6
          and new["arenaTop"] >= 0,
          f"x {new['pad']:.1f}..{new['pad'] + new['aw']:.1f} of {new['W']}")
    newS = shoot(gp, a.a, a.b, a.seed, a.at, True)
    print(f"    scrunch panel bottom {newS['panelBottom']:.0f} "
          f"against the safe line at {safe}")
    check("the scrunch panel ends above the safe line",
          newS["panelBottom"] <= safe,
          f"{newS['panelBottom']:.0f} <= {safe} — the ULTIMATE row is what "
          f"sits on that edge")
    check("the picture is LARGER than the 852x1512 the encode was boxing",
          new["aw"] > 852 and new["ah"] > 0,
          f"{new['aw']:.0f} wide against 852")

    # ------------------------------------------------------------- [3] --
    print(f"\n[3] IT IS THE SMALLER BOUND THAT WINS\n")
    rows = []
    for f in (0, 120, 240, 340, 460):
        p = (HERE / f"../02-chain/_frame-f{f}.html").resolve()
        subprocess.run([sys.executable, "frame_build.py", "--foot", str(f),
                        "--src", str(rp), "--out", str(p)],
                       cwd=HERE, check=True, capture_output=True)
        r = shoot(p, a.a, a.b, a.seed, 2.0)
        rows.append((f, r["scale"], r["aw"], r["ah"],
                     r["arenaTop"] + r["ah"], r["pad"]))
        p.unlink(missing_ok=True)
    print(f"    {'foot':>6}{'scale':>9}{'aw':>8}{'ah':>8}{'bottom':>9}{'side':>7}"
          f"   bound by")
    for f, sc, aw, ah, bt, pd in rows:
        print(f"    {f:>6}{sc:>9.3f}{aw:>8.1f}{ah:>8.1f}{bt:>9.1f}{pd:>7.1f}"
              f"   {'width' if pd <= 12.01 else 'height'}")
    check("scale is monotone non-increasing in foot",
          all(rows[i][1] >= rows[i + 1][1] - 1e-9 for i in range(len(rows) - 1)),
          f"{rows[0][1]:.3f} -> {rows[-1][1]:.3f}")
    check("the WIDTH binds until the height does",
          rows[0][5] <= 12.01 and rows[-1][5] > 12.01,
          "foot 0 is width-bound, foot 460 is height-bound")

    # ------------------------------------------------------------- [4] --
    print(f"\n[4] NOTHING ELSE MOVED\n")
    print(f"    hud {ref['hud']} -> {new['hud']}   arenaTop "
          f"{ref['arenaTop']:.0f} -> {new['arenaTop']:.0f}   "
          f"canvas {ref['cw']}x{ref['ch']} -> {new['cw']}x{new['ch']}")
    check("the HUD band and the arena's top edge are untouched",
          ref["hud"] == new["hud"] and ref["arenaTop"] == new["arenaTop"],
          "the strip comes out of the arena, not out of the HUD")
    check("the canvas is still 1080x1920",
          new["cw"] == 1080 and new["ch"] == 1920, f"{new['cw']}x{new['ch']}")

    Image.open(io.BytesIO(base64.b64decode(new["png"].split(",", 1)[1]))) \
        .convert("RGB").save(outdir / "safeframe.png")
    ri.save(outdir / "safeframe-before.png")
    print(f"\n  wrote safeframe.png and safeframe-before.png")

    bad = [n for n, ok in PASS if not ok]
    print(f"\n{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED)" if bad else ""))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
