#!/usr/bin/env python3
"""Photograph the health readout at chosen HP values, on two builds, at 1:1.

The readout is a function of `hp`, and a fight will not hand you the values you
want to look at -- so this parks a real match, writes hp and hpGhost by hand,
and photographs the shell. Nothing here is a statistic; it is the contact sheet
RESUME-HERE §5 asks for before anyone believes an effect works.

    python3 health_sheet.py --a ../02-chain/sc-cardspin.html \
                            --b ../02-chain/sc-health.html --out sheet.png

The ACUITY row is the honest part. A phone shows 1080 px across ~65 mm and is
held at ~350 mm, so the frame subtends ~638 arcmin; resampling to one sample
per arcmin is a conservative stand-in for the eye's resolution limit. It is a
model, not a measurement, and it is stated as one.
"""
from __future__ import annotations
import argparse, base64, math, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
from scpage import game

SHOT = r"""
([ida, idb, seed, hpa, hpb, t, statuses]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const m = window.__m || (window.__m = (() => {
    const mm = new AC.Match(ida, idb, seed);
    mm.introT = 0; AC.__inject(mm);
    AC.SFX.play = function(){}; AC.SFX.resume = function(){};
    const dt = AC.CONFIG.physics.dt;
    while (mm.t < t) mm.step(dt);
    return mm;
  })());
  m.shake = 0; m.hitStop = 0; m.banner = null;
  for (const [f, hp, x, y] of [[m.a, hpa, 150, 250], [m.b, hpb, 372, 566]]){
    f.hp = hp; f.hpGhost = hp; f.ringFlash = 0; f.mend = 0; f.stun = 0;
    f.flash = 0; f.x = x; f.y = y; f.vx = 0; f.vy = 0;
    if (!statuses) f.status = {};
  }
  AC.__draw(m);
  const cv = document.getElementById('cv'), r = AC.renderer;
  return { png: cv.toDataURL('image/png').slice(22),
           ax: Math.round(r.pad + m.a.x * r.scale),
           ay: Math.round(r.arenaTop + m.a.y * r.scale),
           R:  Math.round(AC.CONFIG.physics.ballR * r.scale) };
}
"""


def acuity(img: Image.Image, frame_w: int = 1080,
           phone_mm: float = 65.1, dist_mm: float = 350.0) -> Image.Image:
    arcmin = math.degrees(2 * math.atan((phone_mm / 2) / dist_mm)) * 60
    k = arcmin / frame_w
    w, h = img.size
    small = img.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    return small.resize((w, h), Image.LANCZOS)


def capture(path: pathlib.Path, hps, ida, idb, seed, t, statuses):
    out = []
    with game(game_path=path.resolve()) as (pg, errs):
        for hpa, hpb in hps:
            r = pg.evaluate(SHOT, [ida, idb, seed, hpa, hpb, t, statuses])
            im = Image.open(pathlib.Path("_hb.png"))if False else None
            raw = base64.b64decode(r["png"])
            pathlib.Path("_hb.png").write_bytes(raw)
            out.append((Image.open("_hb.png").convert("RGB"), r))
        if errs:
            print(f"! {path.name} page errors:", *errs[:5], sep="\n    ")
            sys.exit(1)
    return out


def font(sz, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
    try:    return ImageFont.truetype(p, sz)
    except Exception: return ImageFont.load_default()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="../02-chain/sc-cardspin.html", help="control")
    ap.add_argument("--b", default="../02-chain/sc-health.html", help="variant")
    ap.add_argument("--ids", default="axiom,nightfell")
    ap.add_argument("--seed", type=int, default=20260816)
    ap.add_argument("--t", type=float, default=7.0)
    ap.add_argument("--hp", default="300,198,114,45,12")
    ap.add_argument("--statuses", action="store_true")
    ap.add_argument("--out", default="health-sheet.png")
    ap.add_argument("--frame", default="", help="also write a full frame at this hp pair, e.g. 84,196")
    g = ap.parse_args()

    ida, idb = g.ids.split(",")
    vals = [float(v) for v in g.hp.split(",")]
    hps = [(v, 300.0) for v in vals]

    A = capture(pathlib.Path(g.a), hps, ida, idb, g.seed, g.t, g.statuses)
    B = capture(pathlib.Path(g.b), hps, ida, idb, g.seed, g.t, g.statuses)
    R = A[0][1]["R"]
    half = int(R * 1.75)
    ax, ay = A[0][1]["ax"], A[0][1]["ay"]
    box = (ax - half, ay - half, ax + half, ay + half)
    cell = half * 2
    MAG = 2

    rows = [("SHIPPED  sc-cardspin", [im for im, _ in A], False),
            ("SHIPPED  at ~1 arcmin", [im for im, _ in A], True),
            ("v4  sc-health", [im for im, _ in B], False),
            ("v4  at ~1 arcmin", [im for im, _ in B], True)]
    W = 96 + len(vals) * (cell * MAG + 12)
    H = 46 + len(rows) * (cell * MAG + 40)
    sheet = Image.new("RGB", (W, H), (8, 6, 12))
    d = ImageDraw.Draw(sheet)
    for j, v in enumerate(vals):
        d.text((96 + j * (cell * MAG + 12) + cell * MAG // 2, 16),
               f"{int(v)} HP", font=font(21, True), fill=(232, 222, 202), anchor="mm")
    for i, (name, ims, ac) in enumerate(rows):
        y = 46 + i * (cell * MAG + 40)
        for j, im in enumerate(ims):
            c = (acuity(im) if ac else im).crop(box)
            sheet.paste(c.resize((cell * MAG, cell * MAG), Image.NEAREST),
                        (96 + j * (cell * MAG + 12), y))
        d.text((10, y + cell * MAG // 2), name.replace("  ", "\n"),
               font=font(16, True), fill=(150, 142, 166), anchor="lm")
    sheet.save(g.out)
    print(f"{g.out}  {sheet.size}   ball {R*2}px at 1:1, shown at {MAG}x")

    if g.frame:
        hpa, hpb = [float(v) for v in g.frame.split(",")]
        for tag, p in (("shipped", g.a), ("v4", g.b)):
            fr = capture(pathlib.Path(p), [(hpa, hpb)], ida, idb, g.seed, g.t, True)[0][0]
            fr.save(f"frame-{tag}.png")
            acuity(fr).save(f"frame-{tag}-acuity.png")
        print("frame-shipped.png / frame-v4.png (+ -acuity)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
