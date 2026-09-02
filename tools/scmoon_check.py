#!/usr/bin/env python
"""THE SPEC IS THE THING THAT SHIPS, SO CHECK THE SPEC AND NOT THE LAB.

    python scmoon_check.py --game ../02-chain/sc-duskreave.html

`scmoon_spec.js` is the standalone `_scMoon` written for the builder. The lab
drew arm A from shared helpers; this injects the SPEC as `SHAPES._scEaten`,
renders it through `litWeapon`, and diffs it pixel for pixel against the lab's
arm A. A spec that drifted from the sheet Rick chose from would show here as
a non-zero diff. Then it films a real arena frame with the spec in place and a
strip of the weapon at three world angles, so the lit-face flip (`_litN`) is
seen and not assumed.
"""
from __future__ import annotations
import argparse, base64, io, math, pathlib, sys

from PIL import Image, ImageChops, ImageDraw

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402
import umbral_scythe_moon_lab as lab  # noqa: E402

SPEC = (HERE / "scmoon_spec.js").read_text(encoding="utf-8")


def spec_fn_source() -> str:
    """The method body as an installable function expression."""
    i = SPEC.index("_scMoon(c, L, W, p){")
    body = SPEC[i + len("_scMoon"):].rstrip()
    assert body.endswith("},"), body[-20:]
    body = body[:-1]                       # drop the trailing comma
    return "(function" + body + ")"


def render(pg, arm_js, res, zoom, rot):
    ox, oy = res // 2, int(res * 16 / 9) // 2
    got = pg.evaluate(lab.DRAW_JS if arm_js == "A" else lab.DRAW_JS.replace(
        'S._scEaten = (cfg.arm === "E") ? U.SHIPPED : U.ARMS[cfg.arm];', ''),
        {"arm": arm_js, "L": lab.L, "W": lab.W, "zoom": zoom, "res": res,
         "ox": ox, "oy": oy, "rot": rot, "bg": "#0B0710"})
    return Image.open(io.BytesIO(base64.b64decode(got["png"]))).convert("RGB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-duskreave.html")
    ap.add_argument("--out", default="../05-reference/v63")
    A = ap.parse_args()
    out = HERE / A.out
    out.mkdir(parents=True, exist_ok=True)

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        pg.evaluate(lab.PRELUDE)
        ref = render(pg, "A", 1080, 3.2, lab.ROT)
        n_spec = pg.evaluate("(src)=>{ const S = AC.SHAPES; S._scMoon = eval(src); "
                             "S._scEaten = S._scMoon; if (S._litCache) S._litCache = {}; "
                             "return typeof S._scMoon; }", spec_fn_source())
        print(f"  spec installed as SHAPES._scMoon ({n_spec}), routed over _scEaten")
        got = render(pg, "SPEC", 1080, 3.2, lab.ROT)
        diff = ImageChops.difference(ref, got).convert("L")
        bbox = diff.point(lambda v: 255 if v > 8 else 0).getbbox()
        nz = sum(1 for v in diff.getdata() if v > 8)
        print(f"  spec vs lab arm A at zoom 3.2: {nz} pixels differ by >8/255  "
              f"{'PASS' if nz == 0 else 'FAIL'}  bbox {bbox}")
        # A CONTROL THAT CAN FAIL: the spec against the SHIPPED grammar must
        # differ, or the diff above is measuring nothing.
        shipped = render(pg, "E", 1080, 3.2, lab.ROT) if False else None
        pg.evaluate("()=>{ AC.SHAPES._scEaten = window.__UMB.SHIPPED; }")
        shipped = render(pg, "SPEC", 1080, 3.2, lab.ROT)
        nz2 = sum(1 for v in ImageChops.difference(ref, shipped).convert("L").getdata() if v > 8)
        print(f"  control, lab arm A vs shipped _scEaten: {nz2} pixels differ  "
              f"{'PASS (the diff can see)' if nz2 > 10000 else 'FAIL (instrument blind)'}")
        pg.evaluate("()=>{ AC.SHAPES._scEaten = AC.SHAPES._scMoon; if (AC.SHAPES._litCache) AC.SHAPES._litCache = {}; }")

        # three world angles, so the lit-face mirror is seen
        cells = []
        for rot in (-0.55, 0.9, 2.4):
            im = render(pg, "SPEC", 1080, 2.4, rot)
            bg = Image.new("RGB", im.size, (0x0B, 0x07, 0x10))
            x0, y0, x1, y1 = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 6 else 0).getbbox()
            side = max(x1 - x0, y1 - y0) + 60
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
            cells.append(im.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)).resize((300, 300)))
        # and a real fight frame
        shot = pg.evaluate(lab.ARENA_JS.replace(
            'S._scEaten = (arm === "E") ? U.SHIPPED : U.ARMS[arm];', ''),
            ["SPEC", "duskreave", "lastlight", 33581, 60.0, 6.0])
        fr = Image.open(io.BytesIO(base64.b64decode(shot["png"]))).convert("RGB")
        fr.save(out / "duskreave-moon-arena.png")
        r = int(130 * shot["sc"])
        w, h = fr.size
        fx = min(max(int(shot["sx"]), r), w - r); fy = min(max(int(shot["sy"]), r), h - r)
        zoomed = fr.crop((fx - r, fy - r, fx + r, fy + r))
        zoomed = zoomed.resize((zoomed.width * 2, zoomed.height * 2), Image.NEAREST)

        sh = Image.new("RGB", (300 * 3 + 40 + zoomed.width, max(330, zoomed.height + 30)), (8, 6, 12))
        d = ImageDraw.Draw(sh)
        d.text((8, 6), "_scMoon, THE SPEC, through litWeapon: three world angles at zoom, and a real fight frame at ship size (2x pixels).", fill=(210, 200, 230))
        for i, im in enumerate(cells):
            sh.paste(im, (8 + 300 * i, 26))
        sh.paste(zoomed, (8 + 300 * 3 + 24, 26))
        p = out / "duskreave-moon-spec-check.png"
        sh.save(p)
        print(f"  {p}  {sh.size}   arena frame t={shot['t']}s  ->  duskreave-moon-arena.png")

    if errs:
        print("\n  PAGE ERRORS:", *errs[:6], sep="\n    ")
        return 1
    return 0 if nz == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
