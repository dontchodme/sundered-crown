#!/usr/bin/env python
"""THE UMBRAL SCYTHE, PHOTOGRAPHED IN COLOUR, BEFORE STAGE 2.

    python duskreave_sheet.py --game ../02-chain/sc-duskreave.html

Brief stage 1: "Art: the umbral scythe silhouette. Film it and show Rick a strip
before stage 2 -- v58's `_whEaten` was rejected on sight after it was built and
tuned, and CLAUDE.md 4.0 exists because of it."

DUSKREAVE IS THE FIRST RELIC THAT WILL EVER DRAW `_scEaten`. `SHAPES.scythe` has
routed `umbral` to it since before this cell had anything in it, so the grammar
has shipped in the file for many versions and has never been on screen.

AND `silhouette_probe` CANNOT SEE IT, WHICH IS WHY THIS TOOL DRAWS IN COLOUR.
That probe forces every colour the shape asks for to white so it can compare
OUTLINES -- and `_scEaten` takes its bites with `destination-out` and then
strokes a RIM around each one. Flatten the palette and the rims are white, the
weapon is white, and the bite is a white hole in a white shape: the whole
grammar disappears and the row's IoU table describes a plain crescent. The same
is true of `_gsEaten` and `_tbEaten`, which have been shipping for far longer.
That is open item 35's two-instruments problem with a mechanism attached, and it
is a finding rather than a defect in this relic.

Two sheets, and each answers a different question:

    --row     all seven scythes at zoom, in their own palettes, on one strip.
              THE QUESTION: does umbral read as its own weapon on this row, and
              do the bites read as bites?

    --arena   the relic in a real fight at the delivery resolution.
              THE QUESTION: does any of it survive at the size it ships at? A
              grammar that only works at zoom is a grammar nobody will see --
              v56's hand shipped at ~40px and read as a white scribble.

Nothing is written to any build.
"""
from __future__ import annotations
import argparse, base64, io, pathlib, sys

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game, resolve_game  # noqa: E402

SCHOOLS = ["sanctified", "bloodsworn", "dwarven", "verdant", "umbral",
           "runic", "vigil"]

# The scythe's own dimensions, off the type. Asserted by the builder against
# all six shipped scythes; repeated here only because this tool draws a weapon
# with no relic behind it.
L, W = 104, 46

ROW_JS = r"""(cfg)=>{
  AC.setResolution(1080, 1920);
  const cv = document.getElementById('cv'), c = cv.getContext('2d');
  const s = AC.renderer.scale * cfg.zoom;
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  c.shadowBlur = 0; c.shadowColor = 'transparent';
  /* THE BACKGROUND IS THE HALL'S, NOT BLACK. `_scEaten` bites with
     destination-out, and on this page that reaches the weapon's own scratch
     buffer and nothing else -- but a bite drawn over pure black and a bite
     drawn over the arena floor are different pictures to a person, and the
     arena is what ships. */
  c.fillStyle = cfg.bg; c.fillRect(0, 0, 1080, 1920);
  const p = Object.assign({}, AC.AFFINITIES[cfg.aff]);
  AC.SHAPES._t = 0;
  c.save();
  c.translate(cfg.ox, cfg.oy); c.rotate(cfg.rot); c.scale(s, s);
  /* VIA `litWeapon`, WHICH IS THE PATH THE GAME USES. It bakes the weapon onto
     its own TRANSPARENT scratch first, which is the only reason an eaten
     grammar is safe at all (v58: painted straight onto an opaque background
     these punch thousands of pixels through it). Drawing the raw SHAPES
     function here would photograph a picture the game never shows. */
  if (AC.litWeapon) AC.litWeapon(c, 'scythe', cfg.L, cfg.W, p, 0.5, cfg.rot);
  else AC.SHAPES.scythe(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  return cv.toDataURL('image/png').slice(22);
}"""

ARENA_JS = r"""([rid, foe, sd, secs, wantT])=>{
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a.w.id === rid ? m.a : m.b;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    /* THE BLADE AT FULL EXTENSION AND NOT FROZEN. A scythe photographed mid
       hit-stop is a scythe in a still frame of somebody else's impact, and the
       grammar is on the CUTTING EDGE, so the frame wanted is the one where the
       edge is broadside to the camera. */
    if (m.t < wantT || m.hitStop > 0) continue;
    const th = Math.abs(Math.sin(me.theta));
    if (th < 0.86) continue;
    AC.__draw(m);
    /* WHERE THE RELIC IS, IN DEVICE PIXELS, so the zoom crop follows the
       weapon instead of the hall. The first cut cropped a fixed box and
       photographed the arena's own pentagram with both fighters in the
       corners. */
    const sc = AC.renderer.scale, ov = AC.renderer.ox || 0, oy2 = AC.renderer.oy || 0;
    return { t: +m.t.toFixed(2), theta: +me.theta.toFixed(2),
             sx: me.x * sc + ov, sy: me.y * sc + oy2, sc: sc,
             png: document.getElementById("cv").toDataURL("image/png") };
  }
  return null;
}"""

SCOUR_JS = r"""([rid, foe, sd, secs, want, need]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    const T = m.tornado;
    if (!T) continue;
    /* `want` IS A FRACTION OF THE WINDOW, on the window's OWN clock. Sampling
       against `m.t` would drift by up to 2.4s of hit stop across a ten-second
       window (`scour_probe`), so "a third of the way in" would not mean the
       same thing on two seeds. */
    if (T.t < want * T.dur) continue;
    if (need){
      const th2 = me === m.a ? m.b : m.a;
      const inside = (th2.y + 34 >= T.top &&
                      Math.abs(th2.x - T.cx) <= T.w/2 + 34);
      if (!inside || m.hitStop > 0) continue;
    }
    AC.__draw(m);
    const A = AC.CONFIG.arena;
    return { t:+m.t.toFixed(2), wt:+T.t.toFixed(2), cx:Math.round(T.cx),
             dir:T.dir, w:T.w, top:T.top, inset:Math.round(m.inset),
             bandH: Math.round(A.h - m.inset - T.top),
             hallW: A.w - 2*m.inset, hallH: A.h - 2*m.inset,
             foeIn: (th.y + 34 >= T.top &&
                     Math.abs(th.x - T.cx) <= T.w/2 + 34) ? 1 : 0,
             png: document.getElementById("cv").toDataURL("image/png") };
  }
  return null;
}"""


def strip(pngs, labels, out, cell, title):
    """One row of panels with a caption over each."""
    n = len(pngs)
    sh = Image.new("RGB", (cell[0] * n, cell[1] + 26), (8, 6, 12))
    d = ImageDraw.Draw(sh)
    d.text((6, 4), title, fill=(190, 180, 210))
    for i, (im, lab) in enumerate(zip(pngs, labels)):
        sh.paste(im.resize(cell), (cell[0] * i, 26))
        d.text((cell[0] * i + 8, 30), lab, fill=(230, 220, 245))
    out.parent.mkdir(parents=True, exist_ok=True)
    sh.save(out)
    print(f"  {out}  {sh.size}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-duskreave.html")
    ap.add_argument("--relic", default="duskreave")
    ap.add_argument("--foe", default="lastlight")
    ap.add_argument("--seed", type=int, default=33581)
    ap.add_argument("--secs", type=float, default=60.0)
    ap.add_argument("--at", type=float, default=6.0,
                    help="earliest match time to take the arena frame at")
    ap.add_argument("--zoom", type=float, default=3.2)
    ap.add_argument("--seedlist", default="33581,11961,55196",
                    help="the three seeds gate 2 films")
    ap.add_argument("--caught", action="store_true",
                    help="GATE 3: only take a frame where the quarry is "
                         "actually inside the band")
    ap.add_argument("--scour", action="store_true",
                    help="GATE 2: three casts on three seeds, before any "
                         "tuning. Does the band read as a third of the hall?")
    ap.add_argument("--row", action="store_true")
    ap.add_argument("--arena", action="store_true")
    ap.add_argument("--out", default="../05-reference/v63")
    A = ap.parse_args()
    if not A.row and not A.arena and not A.scour:
        A.row = A.arena = True

    out = (HERE / A.out)
    gp = resolve_game(A.game) if callable(globals().get("resolve_game")) \
        else (HERE / A.game).resolve()

    with game(game_path=gp) as (pg, errs):
        if A.row:
            print("\nTHE SCYTHE ROW, IN COLOUR -- seven schools, one weapon")
            ims, labs = [], []
            for aff in SCHOOLS:
                png = pg.evaluate(ROW_JS, {
                    "aff": aff, "L": L, "W": W, "zoom": A.zoom,
                    "ox": 540, "oy": 900, "rot": -0.55, "bg": "#0B0710"})
                im = Image.open(io.BytesIO(base64.b64decode(png))).convert("RGB")
                r = int(L * A.zoom * 2.0)
                ims.append(im.crop((540 - r, 900 - r, 540 + r, 900 + r)))
                labs.append(aff.upper() + ("   <- DUSKREAVE" if aff == "umbral"
                                           else ""))
            strip(ims, labs, out / "duskreave-scythe-row-colour.png",
                  (360, 360),
                  "THE SCYTHE ROW IN COLOUR, drawn through litWeapon -- the "
                  "path the game uses. UMBRAL is _scEaten and has never been "
                  "on screen before: this relic is the first to wear it.")

        if A.arena:
            print("\nTHE RELIC IN A FIGHT, at the delivery resolution")
            shot = pg.evaluate(ARENA_JS,
                               [A.relic, A.foe, A.seed, A.secs, A.at])
            if not shot:
                print("  NO FRAME -- no un-frozen broadside blade in "
                      f"{A.secs:g}s of {A.relic} vs {A.foe} on seed {A.seed}.")
                print("  That is a finding about the seed, not about the art. "
                      "Try another.")
            else:
                im = Image.open(io.BytesIO(base64.b64decode(
                    shot["png"].split(",", 1)[1]))).convert("RGB")
                out.mkdir(parents=True, exist_ok=True)
                p = out / "duskreave-arena.png"
                im.save(p)
                print(f"  {p}  {im.size}  t={shot['t']}s  "
                      f"theta={shot['theta']}")
                # AND A ZOOM OF THE SAME FRAME, because "does it read at
                # delivery size" and "what is it" are two questions and one
                # picture cannot answer both. v53: shape questions go to a
                # sheet, scale questions need the frame it ships at.
                w, h = im.size
                r = int(160 * shot["sc"])
                cx = min(max(int(shot["sx"]), r), w - r)
                cy = min(max(int(shot["sy"]), r), h - r)
                q = im.crop((cx - r, cy - r, cx + r, cy + r))
                q = q.resize((q.width * 2, q.height * 2), Image.NEAREST)
                p2 = out / "duskreave-arena-zoom.png"
                q.save(p2)
                print(f"  {p2}  {q.size}  (2x nearest, same frame)")

        if A.scour:
            # THREE CASTS ON THREE SEEDS, and each is sampled at a DIFFERENT
            # point in its own window -- near the start, the middle and the
            # end. One instant repeated three times says nothing about a thing
            # whose whole job is to move.
            print("\nGATE 2 -- three casts, three seeds, before any tuning")
            shots, labs = [], []
            seeds = [int(x) for x in A.seedlist.split(",")]
            for i, sd in enumerate(seeds):
                want = [0.12, 0.50, 0.86][i % 3]
                got = pg.evaluate(SCOUR_JS,
                                  [A.relic, A.foe, sd, A.secs, want,
                                   1 if A.caught else 0])
                if not got:
                    print(f"  seed {sd}: NO CAST in {A.secs:g}s -- that is a "
                          f"finding about the seed, not the band")
                    continue
                im = Image.open(io.BytesIO(base64.b64decode(
                    got["png"].split(",", 1)[1]))).convert("RGB")
                shots.append(im)
                labs.append(f"seed {sd}  t={got['t']}s  window {got['wt']}s  "
                            f"cx={got['cx']} dir={got['dir']:+d}")
                print(f"  seed {sd}: window {got['wt']:.2f}s, cx {got['cx']}, "
                      f"dir {got['dir']:+d}, foe inside: "
                      f"{'YES' if got['foeIn'] else 'no'}")
                print(f"    band {got['w']:.0f} wide of a {got['hallW']:.0f} "
                      f"hall = {100*got['w']/got['hallW']:.0f}%   "
                      f"{got['bandH']} tall of {got['hallH']:.0f} = "
                      f"{100*got['bandH']/got['hallH']:.0f}%")
            if shots:
                out.mkdir(parents=True, exist_ok=True)
                W = sum(im.width for im in shots)
                sh = Image.new("RGB", (W, shots[0].height + 26), (8, 6, 12))
                d = ImageDraw.Draw(sh)
                d.text((6, 4), "SCOUR, GATE 2 - the band sweeping, three casts."
                               "  Does it read as a third of the hall?",
                       fill=(210, 200, 230))
                x = 0
                for im, lab in zip(shots, labs):
                    sh.paste(im, (x, 26))
                    d.text((x + 8, 32), lab, fill=(235, 220, 250))
                    x += im.width
                q = out / ("scour-gate3.png" if A.caught
                           else "scour-gate2.png")
                sh.save(q)
                print(f"  {q}  {sh.size}")

    if errs:
        print("\n  PAGE ERRORS:", *errs[:4], sep="\n    ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
