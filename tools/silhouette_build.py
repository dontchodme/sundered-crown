#!/usr/bin/env python3
"""SCHOOL GRAMMARS — a per-school branch that changes the OUTLINE, not the paint.

    python3 silhouette_build.py --src sc-audit.html --out sc-sil.html --runic

THE MEASUREMENT THAT ASKED FOR THIS
------------------------------------
`silhouette_probe.py`, colour stripped out entirely, intersection-over-union
between the seven schools of each type on the shipped build:

    greatsword   1 outline   IoU 1.000        <-- pixel identical
    warhammer    1 outline   IoU 1.000        <-- pixel identical
    scythe       1 outline   IoU 1.000        <-- pixel identical
    flailHead    1 outline   IoU 1.000        <-- pixel identical
    twinblade    2 outlines  IoU 0.347
    bow          3 outlines  IoU 0.622

Rick: *"what i really ment was unique models/silhouettes for each weapon ...
whats important is that they are visually distinct."* Four of six types have one
outline for every school. At N=48 that is eight silhouettes wearing 48 names.

AND THE CALIBRATION IS THE INTERESTING PART
--------------------------------------------
For scale, the same metric BETWEEN types, which is as different as two weapons
in this game ever get:

    greatsword / twinblade  0.280      greatsword / warhammer  0.179
    twinblade  / bow        0.152      greatsword / bow        0.128

The runic twinblade — the one per-school branch Rick has seen and kept — scores
**0.347 against its own type-mates.** That is nearly as far apart as two
different weapon TYPES. So the approved bar is not "add a detail": it is
**a branch should approach the distance between two types.** Anything around
0.9 is a sticker.

THE PROPOSAL THIS TESTS
------------------------
Not 48 bespoke silhouettes. **Seven school GRAMMARS, each of which deforms any
type it is applied to.** Three already exist and are each applied to exactly one
shape, which is why they have never looked like a system:

    runic       in pieces, held by nothing, daylight between   (twinblade)
    vigil       discrete countable plates                      (bow)
    dwarven     riveted, bolted, built rather than forged      (bow)
    sanctified  --
    bloodsworn  --
    verdant     --
    umbral      --

Seven inventions applied 8 times each is a very different project from 56
inventions. **This build tests whether a grammar TRANSFERS**: it takes runic's,
the most extreme and the only one Rick has approved, and puts it on the
greatsword — the worst cell on the matrix sheet, "almost pure silhouette-plus-
glow", and the longest, most solid shape in the game. If the grammar survives
that trip, it will survive the other six.

  --runic   `SHAPES.greatsword` gains a runic branch: no grip, no crossguard,
            the blade in six shards with real daylight between them, and a
            sigil turning backwards where a hand would be.

WHAT IS DELIBERATELY NOT DONE
------------------------------
`_twinConjured` is left alone. The new `_conjure` helper duplicates its logic
rather than replacing it, because folding the twinblade into a shared routine is
a change to a SHIPPED, APPROVED silhouette and `engine_ab.py` cannot see a
render change. Merge them once the pattern is agreed, and only behind a
pixel-identity check on the twinblade — `silhouette_probe.py --types twinblade`
must still read 0.347.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from _wh_patch import (WARHAMMER_ANCHOR, WARHAMMER_BODY, WARHAMMER_GRAMMARS)
from _sf_patch import (SCYTHE_ANCHOR, SCYTHE_BODY, SCYTHE_GRAMMARS,
                       FLAIL_ANCHOR, FLAIL_BODY, FLAIL_GRAMMARS)
from _gs_patch import GS_ANCHOR, GS_BODY, GS_GRAMMARS
from _tb_patch import (TB_ANCHOR, TB_BODY, TB_GRAMMARS,
                       BOW_ANCHOR, BOW_BODY)

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

CONJURE_FN = r"""
  /* THE RUNIC GRAMMAR, EXTRACTED SO IT CAN TRAVEL.

     `_twinConjured` proved the idea on one shape: there is no solid blade at
     all, only hard crystalline shards hanging in a blade-shaped line with real
     daylight between them, light bleeding through the gaps, and a sigil turning
     backwards in the space where a hand would be. "Held by nothing" twice over.
     `silhouette_probe.py` scores that branch at IoU 0.347 against its own
     type-mates -- nearly as far apart as two different weapon TYPES.

     This is the same grammar with the profile handed in, so any shape can wear
     it. `prof(c)` traces the blade outline the type wants; everything else --
     the fracture, the drift, the beam, the sigil -- is the school.

     NOTE: `_twinConjured` deliberately still has its own copy. Folding it into
     this would change a shipped, approved silhouette, and no automated check in
     this project can see a render regression. Merge later, behind a
     pixel-identity test.

     Deterministic in SHAPES._t. No rng. bladeSegments derives the hit segment
     from f.theta, so none of this can move a hitbox. */
  _conjure(c, L, W, p, o){
    const t = SHAPES._t || 0;
    const N = o.n, gap = o.gap, bw = o.bw, prof = o.prof;
    /* The slice window is where the shards are CUT, which is not always the
       whole weapon. A blade runs from the gap to the point, but a hammer's ink
       is all out at the head, and slicing an empty stretch of haft would spend
       two of three shards on nothing. Defaults to the blade case. */
    const sf = o.sliceFrom === undefined ? gap : o.sliceFrom;
    const st = o.sliceTo   === undefined ? L   : o.sliceTo;
    const span = st - sf;

    c.save();                                    // the light through the gaps
    c.globalCompositeOperation = "lighter";
    const beam = c.createLinearGradient(gap, 0, L, 0);
    beam.addColorStop(0,    p.core + "00");
    beam.addColorStop(0.30, p.core + "CC");
    beam.addColorStop(1,    p.glow);
    c.strokeStyle = beam; c.lineCap = "round";
    c.lineWidth = W * o.beam;
    c.beginPath(); c.moveTo(gap, 0); c.lineTo(L, 0); c.stroke();
    c.restore();

    c.lineJoin = "miter"; c.lineCap = "butt";
    for (let i = 0; i < N; i++){
      const u0 = i / N, u1 = (i + (o.frac || 0.87)) / N;   // the daylight
      const x0 = sf + span * u0, x1 = sf + span * u1;
      const cx = (x0 + x1) / 2;
      const drift = Math.sin(t * 2.1 + i * 2.3) * W * o.drift;
      const cant  = Math.sin(t * 1.6 + i * 1.4) * o.cant;

      c.save();
      c.translate(cx, drift); c.rotate(cant); c.translate(-cx, -drift);
      c.beginPath();
      c.rect(x0, drift - bw * 2.2, x1 - x0, bw * 4.4);
      c.clip();

      /* p.dark, not a near-black literal -- see _sf_patch. The mask probe
         flattens every colour to one white and therefore cannot see a
         black bar; the colour matrix showed it immediately. */
      prof(c); c.fillStyle = p.dark; c.fill();               // silhouette
      const g = c.createLinearGradient(cx, -bw, cx, bw);     // lit from above
      g.addColorStop(0,    p.steel);
      g.addColorStop(0.52, p.core);
      g.addColorStop(1,    p.dark);
      prof(c); c.fillStyle = g; c.globalAlpha = 0.94; c.fill(); c.globalAlpha = 1;

      c.save();                                              // the cut faces
      prof(c); c.clip();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.055);
      c.beginPath();
      c.moveTo(x0, drift - bw * 2); c.lineTo(x0, drift + bw * 2);
      c.moveTo(x1, drift - bw * 2); c.lineTo(x1, drift + bw * 2);
      c.stroke();
      c.restore();

      prof(c);
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.045); c.stroke();
      c.restore();
    }

    c.save();                                    // the point is light, not steel
    c.globalCompositeOperation = "lighter";
    c.fillStyle = "#FFFFFF"; c.shadowColor = p.core; c.shadowBlur = 18;
    c.beginPath(); c.arc(L * 1.02, 0, W * 0.075, 0, TAU); c.fill();
    c.restore();

    c.save();                                    // the sigil, turning backwards
    c.translate(gap * 0.50, 0);
    c.rotate(-t * 2.4);
    c.globalCompositeOperation = "lighter";
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.030);
    c.shadowColor = p.core; c.shadowBlur = 14;
    const rr = W * o.sigil;
    c.beginPath(); c.arc(0, 0, rr, 0, TAU); c.stroke();
    c.beginPath();
    for (let i = 0; i < 3; i++){
      const a = i * TAU / 3;
      const x = Math.cos(a) * rr * 0.60, y = Math.sin(a) * rr * 0.60;
      if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
    }
    c.closePath(); c.stroke();
    c.lineWidth = Math.max(1, W * 0.020);
    for (let i = 0; i < 3; i++){
      const a = i * TAU / 3 + Math.PI / 3;
      c.beginPath();
      c.moveTo(Math.cos(a) * rr * 1.15, Math.sin(a) * rr * 1.15);
      c.lineTo(Math.cos(a) * rr * 1.55, Math.sin(a) * rr * 1.55);
      c.stroke();
    }
    c.restore();
  },

  /* RUNIC GREATSWORD. The grammar's first trip to another type, and the
     hostile case on purpose: the greatsword is the longest, most solid shape
     in the game and the matrix sheet's worst cell.

     What the school takes away is as important as what it adds. There is no
     grip, no wrapped leather, no crossguard and no pommel -- the crossguard in
     particular is the single largest horizontal element on the shipped
     greatsword, and deleting it is most of why the outline stops being the
     same outline. Six shards instead of the twinblade's five, because the
     blade is nearly twice as long and five would read as chunks. */
  _gsConjured(c, L, W, p){
    const gap = L * 0.20, bw = W * 0.34, span = L - gap;
    const prof = (cc) => {
      cc.beginPath();
      cc.moveTo(gap,               -bw * 0.52);
      cc.lineTo(gap + span * 0.10, -bw);
      cc.lineTo(L * 0.86,          -bw * 0.80);
      cc.lineTo(L * 1.01,           0);
      cc.lineTo(L * 0.86,           bw * 0.80);
      cc.lineTo(gap + span * 0.10,  bw);
      cc.lineTo(gap,                bw * 0.52);
      cc.closePath();
    };
    /* `frac` 0.74, not the twinblade's 0.87. MEASURED: at 0.87 the runic
       greatsword scored IoU 0.519 against its type-mates, against the runic
       twinblade's 0.403 on the same build -- the grammar had travelled but
       arrived weaker, because six narrow gaps in a blade nearly twice as long
       remove proportionally less of it. Wider daylight is the knob, and it is
       the school's own thesis turned up rather than a new idea. */
    SHAPES._conjure(c, L, W, p, { n:6, gap, bw, prof, frac:0.74,
                                  beam:0.050, drift:0.055, cant:0.060,
                                  sigil:0.30 });
  },
"""

RUNIC_EDIT = [(
    "  greatsword(c, L, W, p){\n"
    "    const bh = W * 0.19;                                       "
    "// blade half-height",
    "  greatsword(c, L, W, p, k, aff){\n"
    "    /* THE SCHOOL BRANCH. Same dispatch as SHAPES.twinblade -- a school\n"
    "       with a grammar of its own gets a different OUTLINE here, not a\n"
    "       different colour. See silhouette_build.py for why, and\n"
    "       silhouette_probe.py for whether it worked. */\n"
    "    if ((p.key || aff) === \"runic\") return SHAPES._gsConjured(c, L, W, p);\n"
    "    const bh = W * 0.19;                                       "
    "// blade half-height",
    "greatsword gains a runic branch")]


CHECK_JS = r"""() => {
  AC.setResolution(1080, 1920);
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const shapes = ['greatsword','warhammer','scythe','twinblade','bow','flailHead'];
  const out = [];
  for (const t of [0, 0.13, 0.4, 0.77, 1.9]){
    AC.SHAPES._t = t;
    for (const sk of Object.keys(AC.AFFINITIES)){
      const p = AC.AFFINITIES[sk];
      for (const s of shapes){
        c.setTransform(1,0,0,1,0,0);
        c.fillStyle = "#0B0910"; c.fillRect(0,0,300,300);
        c.save(); c.translate(150,150);
        try {
          if (s === 'flailHead') AC.SHAPES[s](c, 52, p, 0.5);
          else AC.SHAPES[s](c, 100, 44, p, 0.5, sk);
        } catch (e){ out.push(`t=${t} ${sk}/${s}: ${e.message}`); }
        c.restore();
      }
    }
  }
  /* `_conjure` uses globalCompositeOperation = "lighter". v12: forcing lighter
     on a shadow summed glows that used to occlude and hung a bright bar across
     a banner. Every use here is scoped -- prove it. */
  c.save(); c.translate(150,150);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1; c.shadowBlur = 20;
  AC.SHAPES.greatsword(c, 100, 44, AC.AFFINITIES.runic, 0.5, 'runic');
  if (c.globalCompositeOperation !== 'source-over')
    out.push('runic greatsword leaked composite ' + c.globalCompositeOperation);
  if (c.globalAlpha !== 1) out.push('leaked globalAlpha ' + c.globalAlpha);
  if (c.shadowBlur !== 20) out.push('leaked shadowBlur ' + c.shadowBlur);
  c.restore();
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sc-audit.html")
    ap.add_argument("--out", default="sc-sil.html")
    ap.add_argument("--runic", action="store_true")
    ap.add_argument("--warhammer", action="store_true",
                    help="seven school grammars on the flattest row in the game")
    ap.add_argument("--scythe", action="store_true")
    ap.add_argument("--flail", action="store_true")
    ap.add_argument("--greatsword", action="store_true",
                    help="the six schools the --runic branch left flat")
    ap.add_argument("--twinblade", action="store_true")
    ap.add_argument("--bow", action="store_true")
    a = ap.parse_args()

    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    if a.greatsword and not a.runic:
        print('! --greatsword extends the runic branch; pass --runic too',
              file=sys.stderr)
        return 2
    if not (a.runic or a.warhammer or a.scythe or a.flail or a.greatsword
            or a.twinblade or a.bow):
        print("! nothing to do; pass --runic/--warhammer/--scythe/--flail/--greatsword",
              file=sys.stderr)
        return 2

    text = (HERE / a.src).read_text(encoding="utf-8")
    anchor = "const SHAPES = {\n"
    if text.count(anchor) != 1:
        print("! could not find the SHAPES object exactly once", file=sys.stderr)
        return 1
    text = text.replace(anchor, anchor + CONJURE_FN, 1)
    edits = list(RUNIC_EDIT) if a.runic else []
    if a.warhammer:
        edits.append((WARHAMMER_ANCHOR, WARHAMMER_BODY,
                      "warhammer: 7 school grammars + _whBase"))
    if a.scythe:
        edits.append((SCYTHE_ANCHOR, SCYTHE_BODY,
                      "scythe: 7 school grammars + _scBase"))
    if a.flail:
        edits.append((FLAIL_ANCHOR, FLAIL_BODY,
                      "flailHead: 7 school grammars + _fhBase"))
    if a.greatsword:
        edits.append((GS_ANCHOR, GS_BODY,
                      "greatsword: 7 school grammars + _gsBase"))
    if a.twinblade:
        edits.append((TB_ANCHOR, TB_BODY, "twinblade: 7 school grammars"))
    if a.bow:
        edits.append((BOW_ANCHOR, BOW_BODY, "bow: +5 school branches"))
    for anc, repl, name in edits:
        n = text.count(anc)
        if n != 1:
            print(f"! anchor for '{name}' appears {n} times, expected 1",
                  file=sys.stderr)
            return 1
        text = text.replace(anc, repl, 1)
        print(f"  [silhouette] {name}")
    if a.warhammer:
        # the four grammars go in right after the (now renamed) _whBase closes
        tail = "    for (const rx of [0.685, 0.895]) for (const ry of [-0.72, 0.72]){\n      c.beginPath(); c.arc(L*rx, hh*ry, W*0.055, 0, TAU); c.fill();\n    }\n  },\n"
        if text.count(tail) != 1:
            print("! could not find the end of _whBase exactly once", file=sys.stderr)
            return 1
        text = text.replace(tail, tail + WARHAMMER_GRAMMARS, 1)
        print("  [silhouette] warhammer grammars x7")
    if a.scythe:
        tail = ("    c.moveTo(L*0.70, W*0.20);\n"
                "    c.bezierCurveTo(L*1.02, -W*0.20, L*0.98, -W*0.95, L*0.56, -W*1.32);\n"
                "    c.stroke();\n  },\n")
        if text.count(tail) != 1:
            print("! could not find the end of _scBase exactly once", file=sys.stderr)
            return 1
        text = text.replace(tail, tail + SCYTHE_GRAMMARS, 1)
        print("  [silhouette] scythe grammars x7")
    if a.flail:
        tail = ("    c.beginPath(); c.arc(0, 0, r*0.52, 1.1, 2.4); "
                "c.lineWidth = Math.max(1, D*0.05); c.stroke();\n    c.restore();\n  },\n")
        if text.count(tail) != 1:
            print("! could not find the end of _fhBase exactly once", file=sys.stderr)
            return 1
        text = text.replace(tail, tail + FLAIL_GRAMMARS, 1)
        print("  [silhouette] flailHead grammars x7")
    if a.greatsword:
        tail = ("    c.moveTo(L*0.225, -bh); c.lineTo(L*0.795, -bh*0.90); "
                "c.lineTo(L, 0);\n    c.stroke();\n  },\n")
        if text.count(tail) != 1:
            print("! could not find the end of _gsBase exactly once", file=sys.stderr)
            return 1
        text = text.replace(tail, tail + GS_GRAMMARS, 1)
        print("  [silhouette] greatsword grammars x7")
    if a.twinblade:
        tail = ("    c.moveTo(L*0.385, -bh); c.lineTo(L*0.50, -bh*1.34);\n"
                "    c.lineTo(L*0.565, -bh*0.86); c.lineTo(L, 0);\n"
                "    c.stroke();\n  },\n")
        if text.count(tail) != 1:
            print("! could not find the end of _twinDagger exactly once",
                  file=sys.stderr)
            return 1
        text = text.replace(tail, tail + TB_GRAMMARS, 1)
        print("  [silhouette] twinblade grammars x7")

    out = HERE / a.out
    out.write_text(text, encoding="utf-8")
    print(f"{a.src} -> {a.out}")

    from scpage import game
    with game(game_path=out.resolve()) as (pg, errs):
        bad = pg.evaluate(CHECK_JS)
        if errs:
            print("! PAGE ERRORS:\n  " + "\n  ".join(errs), file=sys.stderr)
            return 1
        if bad:
            print("! SHAPE ERRORS:\n  " + "\n  ".join(bad), file=sys.stderr)
            return 1
    print("  check: 5 clock values x 7 schools x 6 shapes, no exceptions, "
          "no leaked composite/alpha/shadow")
    print(f"\n  python3 silhouette_probe.py --game {a.out} --types greatsword")
    print("  Target: approach 0.347, the runic twinblade's score. 0.9 is a sticker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
