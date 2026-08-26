#!/usr/bin/env python3
"""MATERIALS — lit face / shadowed face / honed edge on the four base shapes.

    python3 depth_build.py --src sc-sil.html --out sc-mat.html \
            --greatsword --warhammer --scythe --twinblade --literals

NEXT-SESSION.md §3.1: *"`_whBase`, `_gsBase`, `_scBase` and `_twinDagger` all
have a lit face / shadowed face / honed edge structure that sells them as
objects. Most of the new grammar geometry is a single fill with an outline."*
The silhouettes are correct; the materials are thin.

THE ONE RULE THIS BUILD IS WRITTEN AROUND
------------------------------------------
**A facet is INTERIOR. It must not change the outline and it must not cast
glow.**

`drawWeapon` sets `shadowBlur = 20` before calling a shape, so every fill in
here emits a shadow. The base fill already casts the weapon's halo; a facet
drawn on top of it would cast a SECOND halo from an interior edge -- brighter
where they overlap, and one more shadowed draw a frame on the exact budget
`sundered-crown-performance.md` is watching. So every facet pass is wrapped in
`save(); shadowBlur = 0; ... restore()`.

That rule is also what makes this build falsifiable. Since nothing here moves a
path, `silhouette_probe.py` must return the SAME six numbers it returned on the
source -- with one deliberate exception, `--literals`, below. A number that
moves means a facet leaked into the outline.

    greatsword 0.364   warhammer 0.322   scythe 0.443
    twinblade  0.359   bow       0.350   flailHead 0.365

WHY THE CONTRAST RUNS DOWNWARD ONLY
------------------------------------
resume-here-v13 §6: every school's `steel` is light -- sanctified's is literally
`#FFFFFF` -- and every `dark` is near-black. There is no headroom above `steel`,
so a "highlight" pass is not available. Depth here is made entirely by taking
light AWAY on the faces that face away, which is the same finding that killed
the greatsword animation's first two versions.

  --greatsword  blade: ridge down the axis, lower facet shaded, fuller becomes
                a groove in the upper facet instead of a glowing bar
  --warhammer   head: one smooth top-to-bottom gradient becomes three hard
                facets -- chamfer, cheek, underside. A machined block has
                edges; a gradient is a cylinder.
  --scythe      crescent: the back half shaded, so the existing lit inner curve
                reads as the honed edge of a wedge rather than as a rim light
  --twinblade   the shadowed flat is `#00000055` -- black at 33%, which is the
                same black in all 48 cells. Palette-owned shade instead.
  --literals    the near-black literals: `#12100C` (grip wrap, ricasso) and
                `_twinConjured`'s `#040814`.

`--literals` IS THE ONE FLAG THAT MOVES A NUMBER, and it is the interesting one.
NEXT-SESSION.md §2 says every `#040814` became `p.dark` in v13. One did not:
`_twinConjured` keeps its own copy of the runic logic (§4 warns about exactly
this) and still fills its shards with the literal. Consequences, both real:

  * in COLOUR it paints near-black where runic's `dark` is `#08264F`, a navy
  * in the MASK the probe flattens palette fields to white and cannot flatten a
    literal, so the runic twinblade's shards currently register as EMPTY --
    only their rims are measured

So `--literals` is predicted to change `twinblade` and nothing else. It is a
separate flag because it edits a silhouette Rick has already approved.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# ------------------------------------------------------------- greatsword --
GS_ANCHOR = """    c.beginPath();                                             // blade
    c.moveTo(L*0.225, -bh);
    c.lineTo(L*0.795, -bh*0.90);
    c.lineTo(L,        0);
    c.lineTo(L*0.795,  bh*0.90);
    c.lineTo(L*0.225,  bh);
    c.closePath();
    c.fillStyle = p.steel; c.fill();
    c.fillStyle = p.core + "77";                               // fuller
    c.fillRect(L*0.27, -bh*0.28, L*0.46, bh*0.56);
"""

GS_BODY = """    c.beginPath();                                             // blade
    c.moveTo(L*0.225, -bh);
    c.lineTo(L*0.795, -bh*0.90);
    c.lineTo(L,        0);
    c.lineTo(L*0.795,  bh*0.90);
    c.lineTo(L*0.225,  bh);
    c.closePath();
    c.fillStyle = p.steel; c.fill();

    /* DEPTH, and it is INTERIOR: shadowBlur is zeroed so the halo stays the
       one the fill above already cast. A diamond section -- ridge down the
       axis, the lower facet turned away from the light. */
    c.save(); c.shadowBlur = 0;
    c.beginPath();                                             // shadowed face
    c.moveTo(L*0.225, 0);
    c.lineTo(L,       0);
    c.lineTo(L*0.795, bh*0.90);
    c.lineTo(L*0.225, bh);
    c.closePath();
    c.fillStyle = SHAPES._shade(p.steel, 0.50, 0.34); c.fill();
    /* The fuller was `p.core + "77"` across the whole width -- a lit bar over
       both facets, which is a groove that glows and crosses its own ridge. A
       groove is dark, and it lives on one face. */
    c.fillStyle = SHAPES._shade(p.dark, 1.30, 0.16);
    c.fillRect(L*0.27, -bh*0.72, L*0.46, bh*0.40);
    c.fillStyle = p.core + "55";                               // its lit lower lip
    c.fillRect(L*0.27, -bh*0.34, L*0.46, bh*0.10);
    c.restore();
"""

# -------------------------------------------------------------- warhammer --
WH_ANCHOR = """    c.beginPath();                                             // head
    c.moveTo(L*0.64, -hh);
    c.lineTo(L*0.93, -hh);
    c.lineTo(L,      -hh*0.66);
    c.lineTo(L,       hh*0.66);
    c.lineTo(L*0.93,  hh);
    c.lineTo(L*0.64,  hh);
    c.closePath();
    const g = c.createLinearGradient(0, -hh, 0, hh);
    g.addColorStop(0, p.steel);
    g.addColorStop(0.5, SHAPES._shade(p.steel, 0.62, 0.50));
    g.addColorStop(1,   SHAPES._shade(p.steel, 0.34, 0.50));
    c.fillStyle = g; c.fill();
    c.strokeStyle = SHAPES._shade(p.steel, 0.18, 0.62);
    c.lineWidth = Math.max(1, W*0.05); c.stroke();
"""

WH_BODY = """    const head = (cc) => {                                     // head
      cc.beginPath();
      cc.moveTo(L*0.64, -hh);
      cc.lineTo(L*0.93, -hh);
      cc.lineTo(L,      -hh*0.66);
      cc.lineTo(L,       hh*0.66);
      cc.lineTo(L*0.93,  hh);
      cc.lineTo(L*0.64,  hh);
      cc.closePath();
    };
    head(c);
    c.fillStyle = p.steel; c.fill();
    /* THREE HARD FACETS, not one gradient. A gradient from steel to near-black
       down the head is a cylinder; a hammer head is a machined block and the
       thing that says so is the EDGE between two flat values. Chamfer, cheek,
       underside -- and interior, so shadowBlur is off. */
    c.save(); c.shadowBlur = 0;
    head(c); c.clip();
    c.fillStyle = SHAPES._shade(p.steel, 0.70, 0.26);          // cheek
    c.fillRect(L*0.60, -hh*0.58, L*0.45, hh*0.92);
    c.fillStyle = SHAPES._shade(p.steel, 0.38, 0.46);          // underside
    c.fillRect(L*0.60,  hh*0.34, L*0.45, hh*0.70);
    c.restore();
    head(c);
    c.strokeStyle = SHAPES._shade(p.steel, 0.18, 0.62);
    c.lineWidth = Math.max(1, W*0.05); c.stroke();
"""

# ----------------------------------------------------------------- scythe --
SC_ANCHOR = """    c.beginPath();                                              // crescent
    c.moveTo(L*0.70, W*0.20);
    c.bezierCurveTo(L*1.02, -W*0.20, L*0.98, -W*0.95, L*0.56, -W*1.32);
    c.bezierCurveTo(L*0.88, -W*0.72, L*0.86, -W*0.10, L*0.66, W*0.30);
    c.closePath();
    const g = c.createLinearGradient(L*0.55, -W, L*0.95, W*0.2);
"""

SC_BODY = """    const cres = (cc) => {                                      // crescent
      cc.beginPath();
      cc.moveTo(L*0.70, W*0.20);
      cc.bezierCurveTo(L*1.02, -W*0.20, L*0.98, -W*0.95, L*0.56, -W*1.32);
      cc.bezierCurveTo(L*0.88, -W*0.72, L*0.86, -W*0.10, L*0.66, W*0.30);
      cc.closePath();
    };
    cres(c);
    const g = c.createLinearGradient(L*0.55, -W, L*0.95, W*0.2);
"""

SC_TAIL_ANCHOR = """    c.fillStyle = g; c.fill();
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.05);  // inner edge
"""

SC_TAIL_BODY = """    c.fillStyle = g; c.fill();
    /* THE BACK OF THE WEDGE. The crescent is a blade seen edge-on: the inner
       curve is honed and already carries a lit stroke, so the outer half has
       to fall away or that stroke reads as a rim light on a flat sticker.
       Clip to the crescent, flood it dark, then lay the gradient back down
       shifted TOWARD the honed edge -- what stays uncovered is a band along
       the back, exactly where the metal turns away. Interior: no glow. */
    c.save(); c.shadowBlur = 0;
    cres(c); c.clip();
    c.fillStyle = SHAPES._shade(p.steel, 0.42, 0.40);
    c.fillRect(L*0.40, -W*1.50, L*0.80, W*2.00);
    c.translate(-W*0.10, W*0.115);
    cres(c); c.fillStyle = g; c.fill();
    c.restore();
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.05);  // inner edge
"""

# -------------------------------------------------------------- twinblade --
TB_ANCHOR = """    c.fillStyle = "#00000055";                                 // shadowed flat
"""
TB_BODY = """    c.save(); c.shadowBlur = 0;                                // interior facet
    /* WAS "#00000055" -- one black at 33% for all 48 cells, which is a
       shadow the palette cannot reach. `_shade` off the school's own steel
       instead, so a bloodsworn dagger's dark side is a bloodsworn dark. */
    c.fillStyle = SHAPES._shade(p.steel, 0.50, 0.34);          // shadowed flat
"""
TB_TAIL_ANCHOR = """    c.closePath(); c.fill();
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.05);  // one honed edge
"""
TB_TAIL_BODY = """    c.closePath(); c.fill();
    c.restore();
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.05);  // one honed edge
"""

# --------------------------------------------------------------- literals --
LITERALS = [
    ('    c.strokeStyle = "#12100C"; c.lineWidth = Math.max(1, W*0.035);\n',
     '    c.strokeStyle = SHAPES._shade(p.dark, 0.42, 0.10);'
     ' c.lineWidth = Math.max(1, W*0.035);\n',
     "greatsword grip wrap"),
    ('    c.strokeStyle = "#12100C"; c.lineWidth = Math.max(1, W*0.045);\n',
     '    c.strokeStyle = SHAPES._shade(p.dark, 0.42, 0.10);'
     ' c.lineWidth = Math.max(1, W*0.045);\n',
     "twinblade grip wrap"),
    ('    c.fillStyle = "#12100C";\n',
     '    c.fillStyle = SHAPES._shade(p.dark, 0.42, 0.10);\n',
     "twinblade ricasso"),
    ('      blade(); c.fillStyle = "#040814"; c.fill();              // silhouette\n',
     '      blade(); c.fillStyle = p.dark; c.fill();                 // silhouette\n',
     "_twinConjured shard silhouette  <-- MOVES THE twinblade NUMBER"),
]


# ----------------------------------------------------------------- bowlit --
# THE BOW'S PRIVATE NEAR-BLACK VOCABULARY. Measured 2026-08-13
# (`sundered-crown-blind-ink.md`): `palette_probe --no-glow` puts the bow at
# UNOWNED 60.6% against 0.0-0.1% for every other shape, and the ink is not a
# detail -- `limb(W*0.30, "#0D0907")` is the DOMINANT pass, the widest of the
# three strokes that build the recurve. 60% of a bow is byte-identical in all
# seven cells.
#
# The obvious objection, and it was wrong: near-black has no chroma headroom,
# so this is a metric win and a visual nothing. Each school's `dark` scaled to
# the literal's own luminance, pairwise CIEDE2000:
#
#   literal   lum     min     med     max      (JND ~2.3)
#   #0D0907   9.71   1.97   11.88   19.59
#   #0F0A08  10.92   2.35   13.47   22.71
#   #140E0A  14.99   3.94   17.60   30.93
#   #1A0512  10.40   2.18   12.80   21.37
#
# For scale: the game's worst school pair after the v13 palette fix, measured
# over the whole weapon, is 21.19. There is real room down there.
#
# `_ink` is `_facet`'s discipline for a different job. `_facet` blends steel
# toward dark and holds the luminance `_shade` produced; `_ink` takes `dark`
# itself and SCALES it to a literal's luminance. Value is held to within 0.73
# of 255 across all seven schools (quantisation only) -- so the reason the
# comment in SHAPES.bow gives for the near-black existing at all, "DARK
# separates by VALUE on any school palette", is untouched. Only the hue returns.
#
# NOT CONVERTED, deliberately: `#CFC6B4`, the string highlight. It is a light
# value, it is cord rather than metal or wood, and it is the whole of the
# "empty string means it just fired" tell. Scaling a school `steel` UP to its
# luminance clips and desaturates (dwarven steel is #6A6E74, lum 110 against
# the string's 199). Left alone on purpose, like sanctified's khaki facet --
# so `palette_probe` will show a small residue and not a clean 0.0%.
INK_JS = """  /* A NEAR-BLACK THE PALETTE OWNS. A literal near-black is invisible to every
     instrument in this project at once: no palette field moves it, and the
     silhouette mask flattens palette fields and thresholds greyscale at 40, so
     ink below 40 that is not a field cannot be seen either. It reads as a
     plausible number for a smaller object. depth_build.py --bowlit.

     Scale the school's own `dark` to the literal's luminance. The VALUE is what
     the near-black was for; the hue is what it was throwing away. */
  _ink(hex, lum){
    const cache = SHAPES._inkCache || (SHAPES._inkCache = {});
    const id = hex + "|" + lum;
    const hit = cache[id];
    if (hit) return hit;
    const n = parseInt(hex.slice(1), 16);
    const r0 = (n >> 16) & 255, g0 = (n >> 8) & 255, b0 = n & 255;
    const l0 = 0.2126 * r0 + 0.7152 * g0 + 0.0722 * b0;
    const k = l0 > 0.5 ? lum / l0 : 0;
    const q = (v) => Math.max(0, Math.min(255, Math.round(v * k)));
    const r = q(r0), g = q(g0), b = q(b0);
    return (cache[id] = "#" + ((1 << 24) | (r << 16) | (g << 8) | b)
                              .toString(16).slice(1));
  },

"""

_D = 'SHAPES._ink(p.dark, '
BOWLIT = [
    ('\n    limb(W*0.30, "#0D0907");                                 // silhouette, dominant\n',
     '\n    limb(W*0.30, ' + _D + '9.71));                     // silhouette, dominant\n',
     "bow limb: the dominant pass  <-- 35-59% of the weapon"),
    ('\n      c.strokeStyle = "#0D0907"; c.lineWidth = Math.max(1, W*0.022);\n',
     '\n      c.strokeStyle = ' + _D + '9.71); c.lineWidth = Math.max(1, W*0.022);\n',
     "bow bloodsworn: barb outline"),
    ('\n          c.fillStyle = "#1A0512";\n          c.fillRect(-W*0.30, -W*0.155, W*0.60, W*0.31);\n',
     '\n          c.fillStyle = ' + _D + '10.40);\n          c.fillRect(-W*0.30, -W*0.155, W*0.60, W*0.31);\n',
     "bow vigil: plate base"),
    ('\n      c.fillStyle = "#0D0907"; c.fillRect(-L*0.055, -lh*0.34, L*0.11, lh*0.68);\n',
     '\n      c.fillStyle = ' + _D + '9.71); c.fillRect(-L*0.055, -lh*0.34, L*0.11, lh*0.68);\n',
     "bow dwarven: riser plate"),
    ('\n      c.fillStyle = "#0D0907";\n      for (const sy of [-1, 1]){\n',
     '\n      c.fillStyle = ' + _D + '9.71);\n      for (const sy of [-1, 1]){\n',
     "bow dwarven: riser rivets"),
    ('\n          c.fillStyle = "#0D0907";\n          c.beginPath(); c.arc(q.x, q.y, W*0.10, 0, TAU); c.fill();\n',
     '\n          c.fillStyle = ' + _D + '9.71);\n          c.beginPath(); c.arc(q.x, q.y, W*0.10, 0, TAU); c.fill();\n',
     "bow dwarven: limb bolt rings"),
    # ALPHA IS PRESERVED. A destination-out site takes its strength from the
    # source alpha, and this "99" is the only alpha-suffixed literal in the bow.
    ('\n          c.fillStyle = "#0D090799";\n',
     '\n          c.fillStyle = ' + _D + '9.71) + "99";\n',
     "bow dwarven: bolt slot (alpha 99 preserved)"),
    ('\n    c.strokeStyle = "#0F0A08"; c.lineWidth = Math.max(1.4, W*0.055);\n',
     '\n    c.strokeStyle = ' + _D + '10.92); c.lineWidth = Math.max(1.4, W*0.055);\n',
     "bow string: the dark under-stroke"),
    ('\n    c.fillStyle = "#140E0A";                                 // riser, dark\n',
     '\n    c.fillStyle = ' + _D + '14.99);                    // riser, dark\n',
     "bow riser: dark base"),
    ('\n      c.strokeStyle = "#140E0A"; c.lineWidth = Math.max(1.4, W*0.075);\n',
     '\n      c.strokeStyle = ' + _D + '14.99); c.lineWidth = Math.max(1.4, W*0.075);\n',
     "bow bolt: dark shaft"),
]
INK_ANCHOR = "  _shade(hex, k, mix){"   # same insertion point as FACET_JS

ERASE_ANCHOR = 'c.globalCompositeOperation = "destination-out";'
ERASE_NOTE = ('{ind}/* AN ERASE TAKES ITS STRENGTH FROM THE SOURCE ALPHA, and this site never\n'
              '{ind}   set one -- it inherited whatever fill the base shape happened to finish\n'
              '{ind}   on, so the depth of every bite in the game was decided by the last line\n'
              '{ind}   of a function that knows nothing about biting. depth_build.py --erase. */\n')

# The alphas the shipped build reaches these sites with, measured by calling
# each base shape in the browser and reading `c.fillStyle` back:
#
#   _gsBase     rgba(255,255,255,0.467)   the fuller, `p.core + "77"`
#   _twinDagger "#00000055"               the shadowed flat, 0.333
#   _whBase     opaque                    the rivets
#   _scBase     opaque                    the crescent's gradient
#
# So a greatsword is bitten at 47%, a dagger at 33%, and a hammer and a scythe
# all the way through -- four different weapons under one word. `pin` writes
# each of those numbers down where it is used, changing nothing on screen;
# `full` makes every bite a real hole, which is what the umbral grammar says it
# is and which BREAKS TWO CELLS -- see the note in main().
PINS = {
    "_gsRadiant": '"#00000077"',
    "_gsEaten":   '"#00000077"',
    "_tbRadiant": '"#00000055"',
    "_tbEaten":   '"#00000055"',
}

# The builder's own check, widened: every shape, every school, five clock
# values, and the context handed back exactly as it was found. A facet pass
# that forgets its `restore()` would otherwise leave shadowBlur at 0 for
# everything drawn after it in the frame.
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
        c.globalCompositeOperation = 'source-over';
        c.globalAlpha = 1; c.shadowBlur = 20; c.shadowColor = p.core;
        try {
          if (s === 'flailHead') AC.SHAPES[s](c, 52, p, 0.5);
          else AC.SHAPES[s](c, 100, 44, p, 0.5, sk);
        } catch (e){ out.push(`t=${t} ${sk}/${s}: ${e.message}`); }
        if (c.shadowBlur !== 20)
          out.push(`${sk}/${s} leaked shadowBlur ${c.shadowBlur}`);
        if (c.globalAlpha !== 1)
          out.push(`${sk}/${s} leaked globalAlpha ${c.globalAlpha}`);
        if (c.globalCompositeOperation !== 'source-over')
          out.push(`${sk}/${s} leaked composite ${c.globalCompositeOperation}`);
        c.restore();
      }
    }
  }
  return out;
}"""


# ------------------------------------------------------------------ tint --
# MEASURED, not assumed. `_shade(hex, k, mix)` pulls a colour toward its own
# LUMINANCE by `mix` and then scales it by `k`, so every facet above lands on
# the same grey no matter whose weapon it is:
#
#   school      steel     sat     _shade(steel,0.50,0.34)   sat
#   sanctified  #FFFFFF   0.00    #808080                   0.00
#   bloodsworn  #EBD3D3   0.37    #726A6A                   0.04
#   runic       #D4E4FF   1.00    #6C727B                   0.06
#   umbral      #B6A5C9   0.25    #59545F                   0.06
#
# The TB_BODY comment claims the facet makes "a bloodsworn dagger's dark side a
# bloodsworn dark". It does not: all seven land at saturation <= 0.06. The one
# surface with room to carry a school's colour throws it away.
#
# `_facet` blends steel toward the school's OWN `dark` instead. `t` per site is
# chosen to land within ~13 luminance of the grey it replaces, so the VALUE
# structure Rick approved does not move — only the hue comes back.
FACET_JS = """  /* A SHADOWED FACE, IN THE SCHOOL'S OWN COLOUR. `_shade` desaturates toward
     luminance, which is right for a highlight and wrong for a shadow: it sends
     all seven schools to the same grey (sanctified #808080, runic #6C727B).
     A turned-away face is lit by less of the same light, not by grey light, so
     blend toward the school's `dark`. `t` is picked per site to hold the
     luminance `_shade` produced. depth_build.py --tint. */
  _facet(steel, dark, t){
    const cache = SHAPES._facetCache || (SHAPES._facetCache = {});
    const id = steel + "|" + dark + "|" + t;
    const hit = cache[id];
    if (hit) return hit;
    const s = parseInt(steel.slice(1), 16), d = parseInt(dark.slice(1), 16);
    const mix = (sh) => Math.round((((s >> sh) & 255)
                 + ((((d >> sh) & 255)) - ((s >> sh) & 255)) * t));
    const r = mix(16), g = mix(8), b = mix(0);
    return (cache[id] = "#" + ((1 << 24) | (r << 16) | (g << 8) | b)
                              .toString(16).slice(1));
  },

"""
FACET_ANCHOR = "  _shade(hex, k, mix){"

# site -> the t that reproduces its luminance. k=0.70 is a light facet and
# needs little dark in it; k=0.38 is an underside and needs a lot.
TINTS = [
    ('SHAPES._shade(p.steel, 0.50, 0.34)', 'SHAPES._facet(p.steel, p.dark, 0.60)'),
    ('SHAPES._shade(p.steel, 0.70, 0.26)', 'SHAPES._facet(p.steel, p.dark, 0.36)'),
    ('SHAPES._shade(p.steel, 0.38, 0.46)', 'SHAPES._facet(p.steel, p.dark, 0.74)'),
    ('SHAPES._shade(p.steel, 0.42, 0.40)', 'SHAPES._facet(p.steel, p.dark, 0.68)'),
]


# ------------------------------------------------------------ worldlight --
# Rick, watching judge-tint.mp4: "is the tint happening when the sword clanks?"
# It is not. Every facet above is painted INSIDE the weapon's own transform, so
# it marks the side of the blade called `+y`, not the side turned away from the
# light -- and it rides around with the sword. Measured on the umbral
# greatsword, upper-minus-lower screen luminance by facing:
#
#   facing     0     45     90    135    180    225    270    315
#   sc-tint  +31   +1.5   +6.3   +1.7   -31   +0.2   -8.6   -0.9
#
# A world-lit blade holds one sign at every facing. It flips, and it flips
# hardest at 0/180 -- which is where a clank puts it, because a clank sets
# hitStop and then multiplies spinDir by -1. The bake is older than the depth
# pass (sc-sil flips too, off the grip) but the depth pass put a big one on the
# blade and --tint made it chromatic instead of merely tonal.
#
# The light is world-up. `_lit` reads the live transform, mirrors the facet
# about the blade axis when the weapon has turned over, and returns |n| as the
# strength -- so the facet fades to nothing as the blade swings edge-on to the
# light and there is NO POP at the crossing, because there is nothing left to
# flip. Cost is one getTransform per facet per weapon per frame; measure it.
LIGHT_JS = """  /* WORLD LIGHT. `_lit` mirrors an interior facet about the blade axis when the
     weapon has turned over, so a shadowed face stays on the side away from the
     light instead of riding around with the object. Returns the strength: 1
     when the blade lies flat to the light, 0 when it swings edge-on, and the
     mirror happens exactly where the strength is 0. depth_build.py
     --worldlight. */
  _litN(c){
    const m = c.getTransform();
    return m.d / (Math.hypot(m.c, m.d) || 1);
  },
  _lit(c){
    const n = SHAPES._litN(c);
    if (n < 0) c.scale(1, -1);
    return Math.abs(n);
  },

"""

# The mirror is only valid where the facet's host shape is symmetric about
# y = 0 -- true of the greatsword blade, the hammer head and the dagger flat.
# The scythe's shade is CLIPPED to the crescent, which is not symmetric, so
# mirroring would shade a crescent that is not the one on screen. There the
# same physics is applied to the offset instead: the gradient is re-laid toward
# whichever side the light is actually on.
LIGHT_SAVE = "c.save(); c.shadowBlur = 0;"
LIGHT_WRAP = ("c.save(); c.shadowBlur = 0; c.globalAlpha = SHAPES._lit(c);"
              "  /* world light */")
LIGHT_SC_WRAP = ("c.save(); c.shadowBlur = 0;                                 "
                 "/* world light */\n"
                 "    const wl = SHAPES._litN(c); c.globalAlpha = Math.abs(wl);")
LIGHT_SC_OFFSET = ("c.translate(-W*0.10, W*0.115);",
                   "c.translate(-W*0.10, W*0.115 * (wl < 0 ? -1 : 1));")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sc-sil.html")
    ap.add_argument("--out", default="sc-mat.html")
    ap.add_argument("--greatsword", action="store_true")
    ap.add_argument("--warhammer", action="store_true")
    ap.add_argument("--scythe", action="store_true")
    ap.add_argument("--twinblade", action="store_true")
    ap.add_argument("--literals", action="store_true",
                    help="near-black literals -> palette; moves twinblade's IoU")
    ap.add_argument("--bowlit", action="store_true",
                    help="the BOW's near-black vocabulary -> palette, luminance "
                         "held. 10 sites, 5 literals, 35-59% of the weapon. Colour "
                         "only: BOTH silhouette masks must be unchanged.")
    ap.add_argument("--tint", action="store_true",
                    help="shadowed faces carry the school's own dark instead of "
                         "a shared grey; same luminance, requires the shape flags")
    ap.add_argument("--worldlight", action="store_true",
                    help="the light stays put while the weapon turns; fixes the "
                         "facet flip visible at clanks. Requires the shape flags")
    ap.add_argument("--erase", choices=["pin", "full"], default=None,
                    help="pin: write the shipped alphas down where they are used "
                         "(no visual change, and required by the shape edits above). "
                         "full: every bite a real hole — MOVES four cells")
    a = ap.parse_args()

    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    if not (a.greatsword or a.warhammer or a.scythe or a.twinblade
            or a.literals or a.bowlit or a.erase):
        print("! nothing to do; pass --greatsword/--warhammer/--scythe/"
              "--twinblade/--literals/--bowlit/--erase", file=sys.stderr)
        return 2

    text = (HERE / a.src).read_text(encoding="utf-8")

    edits: list[tuple[str, str, str]] = []
    if a.greatsword:
        edits.append((GS_ANCHOR, GS_BODY, "greatsword blade: ridge + shaded lower facet"))
    if a.warhammer:
        edits.append((WH_ANCHOR, WH_BODY, "warhammer head: three hard facets"))
    if a.scythe:
        edits.append((SC_ANCHOR, SC_BODY, "scythe crescent: path extracted"))
        edits.append((SC_TAIL_ANCHOR, SC_TAIL_BODY, "scythe crescent: shaded back"))
    if a.twinblade:
        edits.append((TB_ANCHOR, TB_BODY, "twinblade flat: palette-owned shade"))
        edits.append((TB_TAIL_ANCHOR, TB_TAIL_BODY, "twinblade flat: close the facet"))
    if a.literals:
        edits.extend(LITERALS)
    if a.bowlit:
        if text.count(INK_ANCHOR) != 1:
            print("! could not find _shade to insert _ink beside", file=sys.stderr)
            return 1
        text = text.replace(INK_ANCHOR, INK_JS + INK_ANCHOR, 1)
        edits.extend(BOWLIT)
        print(f"  [depth] bowlit: {len(BOWLIT)} bow sites -> _ink(p.dark, lum)")

    if a.tint:
        if not (a.greatsword or a.warhammer or a.scythe or a.twinblade):
            print("! --tint edits the facets, so it needs the shape flags that "
                  "create them", file=sys.stderr)
            return 1
        if text.count(FACET_ANCHOR) != 1:
            print("! could not find _shade to insert _facet beside",
                  file=sys.stderr)
            return 1
        text = text.replace(FACET_ANCHOR, FACET_JS + FACET_ANCHOR, 1)
        tinted, hit = [], 0
        for anc, repl, name in edits:
            for old, new in TINTS:
                if old in repl:
                    repl = repl.replace(old, new)
                    hit += 1
            tinted.append((anc, repl, name))
        edits = tinted
        want = (1 if a.greatsword else 0) + (2 if a.warhammer else 0) \
             + (1 if a.scythe else 0) + (1 if a.twinblade else 0)
        if hit != want:
            print(f"! --tint rewrote {hit} facet fills, expected {want} for the "
                  "flags given", file=sys.stderr)
            return 1
        print(f"  [depth] tint: {hit} facets moved off grey onto the school's dark")

    if a.worldlight:
        if not (a.greatsword or a.warhammer or a.scythe or a.twinblade):
            print("! --worldlight edits the facets, so it needs the shape flags "
                  "that create them", file=sys.stderr)
            return 1
        if text.count(FACET_ANCHOR) != 1:
            print("! could not find _shade to insert _lit beside", file=sys.stderr)
            return 1
        text = text.replace(FACET_ANCHOR, LIGHT_JS + FACET_ANCHOR, 1)
        lit, hit = [], 0
        for anc, repl, name in edits:
            if LIGHT_SAVE in repl:
                if "cres(c); c.clip();" in repl:              # the scythe
                    repl = repl.replace(LIGHT_SAVE, LIGHT_SC_WRAP, 1)
                    old, new = LIGHT_SC_OFFSET
                    if old not in repl:
                        print("! scythe offset not found", file=sys.stderr)
                        return 1
                    repl = repl.replace(old, new, 1)
                else:
                    repl = repl.replace(LIGHT_SAVE, LIGHT_WRAP, 1)
                hit += 1
            lit.append((anc, repl, name))
        edits = lit
        want = (1 if a.greatsword else 0) + (1 if a.warhammer else 0) \
             + (1 if a.scythe else 0) + (1 if a.twinblade else 0)
        if hit != want:
            print(f"! --worldlight wrapped {hit} facet blocks, expected {want}",
                  file=sys.stderr)
            return 1
        print(f"  [depth] worldlight: {hit} facet blocks follow the light, "
              "not the weapon")

    for anc, repl, name in edits:
        n = text.count(anc)
        if n != 1:
            print(f"! anchor for '{name}' appears {n} times, expected 1",
                  file=sys.stderr)
            return 1
        text = text.replace(anc, repl, 1)
        print(f"  [depth] {name}")

    if a.erase:
        i = text.find("const SHAPES = {")
        j = text.find("\n};", i)
        if i < 0 or j < 0:
            print("! could not bound the SHAPES object", file=sys.stderr)
            return 1

        def stamp(seg: str, style: str) -> tuple[str, int]:
            lines, n = seg.split("\n"), 0
            for k, line in enumerate(lines):
                if line.strip() == ERASE_ANCHOR:
                    ind = line[:len(line) - len(line.lstrip())]
                    lines[k] = (line + "\n" + ERASE_NOTE.format(ind=ind)
                                + ind + f"c.fillStyle = {style};")
                    n += 1
            return "\n".join(lines), n

        if a.erase == "full":
            block, n = stamp(text[i:j], '"#000000"')
            text = text[:i] + block + text[j:]
            print(f"  [depth] erase=full: {n} sites, every bite a real hole")
        else:
            total = 0
            for fn, style in PINS.items():
                s = text.find("\n  " + fn + "(c")
                if s < 0:
                    print(f"! {fn} not found", file=sys.stderr)
                    return 1
                e = text.find("\n  },", s)
                seg, n = stamp(text[s:e], style)
                if n != 1:
                    print(f"! {fn} has {n} erase sites, expected 1", file=sys.stderr)
                    return 1
                text = text[:s] + seg + text[e:]
                total += n
            print(f"  [depth] erase=pin: {total} sites pinned to the shipped alpha")

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
    print("  check: 5 clock values x 7 schools x 6 shapes, no exceptions,"
          " context handed back clean")
    print(f"\n  python3 silhouette_probe.py --game {a.out}")
    print("  Every number must match the source"
          + (" EXCEPT twinblade." if a.literals else ". No exceptions."))
    if a.bowlit:
        print("  --bowlit is COLOUR ONLY. Both masks must be unchanged, including\n  --footprint: _ink holds luminance, so it returns near-black from the\n  probe's white too. The instrument is a separate job from the art.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
