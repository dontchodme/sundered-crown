#!/usr/bin/env python
"""THE STAFF'S PAINT GATE (v89 art doc, "What Code does with the pick", item 2).

    python staff_paint_gate.py --game ../02-chain/sc-culverin.html [--spin out.png]

v63's gate for a pasted silhouette: the build's own `SHAPES.staff` must draw
every candidate PIXEL-IDENTICAL to Cowork's spec (`06-docs/v89/staff_spec.js`)
injected over the same page, through the engine's own `litWeapon`, on the
engine's own frame -- the frame `staff_art_lab.py` draws the concept sheet on.
Same page, same rasteriser, so a difference can only be the paste. All 21
candidates are compared, not just the picked ones, because the losers stay in
the build until Rick's letters land.

It also measures the thing the concept sheet could not show: `drawWeapon`
draws a pre-blurred GLOW sprite under every weapon (`weaponGlow`), sized at
1.15 L, and the staff draws to ~1.9 L. It reports how much of the staff's glow
a 1.15 sprite loses against the build's own, per school -- the control is the
bow, which must lose nothing either way.

`--spin` writes a sheet of the staff as `drawWeapon` draws it in play (glow
sprite + `litWeapon`, the ball over it) at eight facings, one row a school at
Rick's current pick: the engine lights a weapon by its WORLD orientation, so
the one tilt the concept sheet was drawn at is not the whole picture.
"""
from __future__ import annotations
import argparse, base64, io, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
SPEC = HERE.parent / "06-docs" / "v89" / "staff_spec.js"
SCHOOLS = ["bloodsworn", "umbral", "vigil", "verdant", "runic", "sanctified", "dwarven"]

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--zoom", type=float, default=4.5)
ap.add_argument("--rot", type=float, default=-0.35)
ap.add_argument("--spin", default=None, help="write the in-play spin sheet here")
a = ap.parse_args()

JS = r"""([spec, schools, zoom, rot]) => {
  if (typeof STAFF === 'undefined' || !SHAPES.staff) return { err: 'this build has no SHAPES.staff' };
  const SPECSTAFF = eval('(() => { ' + spec + '; return STAFF; })()');
  const buildStaff = SHAPES.staff;
  const L = 60, W = 44, R = CONFIG.physics.ballR;
  const cv = document.createElement('canvas'), c = cv.getContext('2d');
  cv.width = Math.ceil((4 + R*2 + L*2.2) * zoom) + 24;
  cv.height = Math.ceil((W*2.4 + L*1.2*Math.abs(Math.sin(rot))) * zoom) + 24;
  function draw(key){
    c.setTransform(1,0,0,1,0,0); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
    c.fillStyle = '#0B0B12'; c.fillRect(0, 0, cv.width, cv.height);
    const p = Object.assign({}, AFFINITIES[key]);
    c.save(); c.translate(12 + (4 + R)*zoom, cv.height/2); c.scale(zoom, zoom); c.rotate(rot); c.translate(R - 6, 0);
    if (!litWeapon(c, 'staff', L, W, p, 0.5, rot)) SHAPES.staff(c, L, W, p, 0.5);
    c.restore();
    return c.getImageData(0, 0, cv.width, cv.height).data;
  }
  const out = { cells: [], pick: Object.assign({}, STAFF.pick) };
  const keep = Object.assign({}, STAFF.pick), keepS = Object.assign({}, SPECSTAFF.pick);
  for (const key of schools) for (const v of ['A','B','C']){
    STAFF.pick[key] = v; SPECSTAFF.pick[key] = v;
    SHAPES.staff = buildStaff;             const b = draw(key);
    SHAPES.staff = SPECSTAFF.staff;        const s = draw(key);
    SHAPES.staff = buildStaff;
    let diff = 0, maxd = 0, ink = 0;
    for (let i = 0; i < b.length; i++){
      const d = Math.abs(b[i] - s[i]); if (d){ diff++; if (d > maxd) maxd = d; }
    }
    for (let i = 0; i < b.length; i += 4) if (b[i] !== 11 || b[i+1] !== 11 || b[i+2] !== 18) ink++;
    out.cells.push({ key, v, diff, maxd, ink });
  }
  Object.assign(STAFF.pick, keep); Object.assign(SPECSTAFF.pick, keepS);

  // THE GLOW. The build's sprite against the same sprite cut at the old 1.15 L.
  // Alpha summed over the sprite: what a 1.15 sprite cannot hold is lost.
  function glowMass(shape, key, ext){
    const pal = AFFINITIES[key], blur = 20, PAD = Math.ceil(blur * 1.5) + 4;
    const w = Math.ceil(L * ext) + PAD * 2, h = Math.ceil(W * 3) + PAD * 2;
    const g = document.createElement('canvas'); g.width = w; g.height = h;
    const x = g.getContext('2d'); const OFF = w + 1000;
    x.translate(PAD, h / 2); x.shadowColor = pal.core; x.shadowBlur = blur; x.shadowOffsetX = OFF; x.translate(-OFF, 0);
    SHAPES[shape](x, L, W, pal, 0.5);
    const d = x.getImageData(0, 0, w, h).data; let m = 0, edge = 0;
    for (let i = 3; i < d.length; i += 4) m += d[i];
    for (let yy = 0; yy < h; yy++) edge += d[(yy * w + (w - 1)) * 4 + 3];
    return { m, edge, w };
  }
  out.glow = [];
  for (const key of schools){
    const full = glowMass('staff', key, 2.6), old = glowMass('staff', key, 1.15), now = glowMass('staff', key, GLOW_EXT.staff);
    out.glow.push({ key, lostOld: 1 - old.m / full.m, lostNow: 1 - now.m / full.m, edgeOld: old.edge, edgeNow: now.edge });
  }
  const bf = glowMass('bow', 'dwarven', 2.6), bo = glowMass('bow', 'dwarven', 1.15);
  out.bow = { lost: 1 - bo.m / bf.m, edge: bo.edge };
  out.ext = GLOW_EXT.staff;
  return out;
}"""

SPIN = r"""([schools, zoom]) => {
  const L = 60, W = 44, R = CONFIG.physics.ballR, N = 8, cell = Math.ceil((R + L*2.1) * 2 * zoom / 1.6);
  const cv = document.createElement('canvas'); cv.width = cell * N; cv.height = cell * schools.length;
  const c = cv.getContext('2d'); c.fillStyle = '#0B0B12'; c.fillRect(0, 0, cv.width, cv.height);
  schools.forEach((key, r) => {
    const pal = AFFINITIES[key];
    for (let i = 0; i < N; i++){
      const ang = i * Math.PI * 2 / N - Math.PI / 2;
      c.save(); c.translate(i * cell + cell / 2, r * cell + cell / 2); c.scale(zoom / 1.6, zoom / 1.6);
      // drawWeapon's non-chain branch, as written: rotate, out to the ball's edge, glow sprite, then litWeapon
      c.save(); c.rotate(ang); c.translate(R - 6, 0);
      const g = weaponGlow('staff', L, W, pal, 0.5, 20); c.drawImage(g.cv, g.ox, g.oy);
      if (!litWeapon(c, 'staff', L, W, pal, 0.5, ang)) SHAPES.staff(c, L, W, pal, 0.5);
      c.restore();
      const gr = c.createRadialGradient(-R*0.3, -R*0.3, R*0.1, 0, 0, R);
      gr.addColorStop(0, SHAPES._shade(pal.dark, 1.9, 0.2)); gr.addColorStop(1, SHAPES._ink(pal.dark, 6));
      c.fillStyle = gr; c.beginPath(); c.arc(0, 0, R, 0, Math.PI * 2); c.fill();
      c.strokeStyle = pal.core + '99'; c.lineWidth = 1.6; c.beginPath(); c.arc(0, 0, R - 1, 0, Math.PI * 2); c.stroke();
      c.restore();
    }
  });
  return cv.toDataURL('image/png').slice(22);
}"""

with game(game_path=(HERE / a.game).resolve()) as (page, errors):
    r = page.evaluate(JS, [SPEC.read_text(encoding="utf-8"), SCHOOLS, a.zoom, a.rot])
    if "err" in r:
        raise SystemExit(r["err"])
    spin = page.evaluate(SPIN, [SCHOOLS, a.zoom]) if a.spin else None
    assert not errors, errors

print(f"THE PAINT GATE -- {a.game}   pick {r['pick']}")
bad = 0
for c in r["cells"]:
    ok = c["diff"] == 0 and c["ink"] > 1000
    bad += not ok
    print(f"  {'ok  ' if ok else 'FAIL'}  {c['key']:<11} {c['v']}  {c['diff']:>7} px differ"
          f"  (max {c['maxd']})   ink {c['ink']}")
print(f"\n  {21 - bad}/21 candidates pixel-identical to the spec"
      f"{'' if not bad else '  <-- THE PASTE IS NOT THE SPEC'}")

print(f"\nTHE GLOW -- share of the staff's glow a sprite of the given length loses "
      f"(against one sized at 2.6 L)")
print(f"  {'school':<11} {'at 1.15 L':>10} {'at ' + str(r['ext']) + ' L':>10}   alpha on the sprite's far edge (1.15 / now)")
for g in r["glow"]:
    print(f"  {g['key']:<11} {g['lostOld']:>9.1%} {g['lostNow']:>10.1%}   {g['edgeOld']:>7} / {g['edgeNow']}")
print(f"  control: the bow at 1.15 L loses {r['bow']['lost']:.2%}, far-edge alpha {r['bow']['edge']}")
glow_ok = all(g["lostNow"] < 0.001 and g["edgeNow"] == 0 for g in r["glow"]) and r["bow"]["edge"] == 0
print(f"  {'ok  ' if glow_ok else 'FAIL'}  the build's sprite holds all of every staff's glow, and the bow's never lost any")

if spin:
    p = pathlib.Path(a.spin); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(base64.b64decode(spin)); print(f"\n  wrote {p}")
sys.exit(0 if (bad == 0 and glow_ok) else 1)
