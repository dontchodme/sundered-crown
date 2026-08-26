#!/usr/bin/env python3
"""HEALTH v4 -- the gauge (A), the lifeline (D) and the stages (F).

    python3 health_build.py --src ../02-chain/sc-cardspin.html \
                            --out ../02-chain/sc-health.html

WHY. Rick, 2026-08-17: "its really hard to tell how much health the balls have
left even after the rebuild ... now that weve moved to a more content driven
goal." Measured on the chain tip and on frames pulled out of a delivered short:

    ring stroke   1.7 sim -> 3.45 canvas px -> 0.208 mm on a phone
                                            -> 2.0 arcmin at 350 mm
    the eye's resolution limit is about 1 arcmin, so the entire health
    readout for one relic is a line at the threshold of being resolved

    full 300 HP   347 canvas px of arc = 20.9 mm of curve
    the ball      8.3 mm across, 1.4 degrees of visual angle

and three failures that are about the ENCODING rather than the size:

    1. hpFrac 1.0 and hpFrac 0.04 put the ember within 14 degrees of each
       other, because the sweep is a full turn. The brightest element of the
       readout is nearly co-located at full health and at one hit from death.
    2. An arc with no track drawn is an ANGLE judgement. Angle reads less
       accurately than length, which reads less accurately than position on a
       common scale -- and this one is on a subject moving at up to 2500 px/s.
    3. Both relics' rings are the same red in two different places, so "who is
       winning" costs two saccades and an angle subtraction. That is the one
       question the content goal cares about most and it is the most expensive
       thing on the screen to read.

WHAT THIS BUILDER DOES. Three edits, all presentation:

  A  GAUGE     stroke 1.7 -> 6.0, sweep 360 -> 270 with the gap at the foot,
               and the empty track is DRAWN. Fixes all three faults above:
               12.2 canvas px clears the acuity limit by 3.5x, the two ends of
               the scale end up 90 degrees apart, and a visible track turns an
               angle into a length against a reference.
  D  LIFELINE  one object in the band above the hall, two heads meeting at a
               marked centre, each head's distance from its own end being that
               relic's life on the 300 scale. ~1000 px of scale against the
               gauge's 347 px of arc. Drawn LAST, in screen space.
  F  STAGES    three pips on the gauge track at 0.66, CONFIG.desperation.at
               and 0.10. The live arc steps in VALUE and BEHAVIOUR, never in
               hue, because every hue in this game is already an affinity. A
               passed pip is drawn dead, so the track carries a permanent
               record. The crossing flash HOLDS NO STATE -- see below.

NO SIMULATION STATE, NO NEW FIELDS, NO RNG. The crossing flash is derived from
`hpGhost` vs `hp`: the ghost still being above a threshold the real value has
already fallen below IS the crossing window. No timer, no animation field,
nothing for a heal to leave stranded, and identical in the live page and in the
offline render. Same trick the fractures use. engine_ab.py is the proof.

THE MIDDLE ONE IS A JUDGEMENT CALL AND IT IS STATED. Rule 5 of RESUME-HERE --
put the information where the eye already is -- retired the HUD health bar in
v3 and was right to. But it answers "how badly is this relic hurt", which is
asked at the instant of impact with the eye on the ball. "Who is winning" is a
different question, asked between exchanges, and it cannot be answered at
either ball because it needs both. Splitting it across two objects moving at
2500 px/s is not putting it where the eye is; it is putting it in two places
at once. The lifeline is one object answering one question no ball can answer
alone. If that argument does not land, `TUG.on = false` removes it and the
other two edits stand on their own.
"""
from __future__ import annotations
import argparse, base64, hashlib, pathlib, re, sys

PROTECTED = {"sundered-crown.html", "sc-playable.html"}


# --------------------------------------------------------------------------
def cut(src: str, start: str, end: str, what: str) -> tuple[str, str]:
    """Replace the span [start, end) exactly once. Both markers must be unique
    or the edit is refused -- an anchored edit that matches twice is how a
    builder silently patches the wrong block."""
    for m, nm in ((start, "start"), (end, "end")):
        n = src.count(m)
        if n != 1:
            sys.exit(f"! {what}: {nm} anchor matches {n} times, expected 1")
    i = src.index(start)
    j = src.index(end)
    if j <= i:
        sys.exit(f"! {what}: end anchor precedes start anchor")
    return src[i:j], src[i:j]


def replace_span(src: str, start: str, end: str, new: str, what: str) -> str:
    old, _ = cut(src, start, end, what)
    print(f"  {what:<10} replaced {len(old):>5} chars "
          f"({hashlib.sha256(old.encode()).hexdigest()[:12]}) -> {len(new):>5}")
    return src.replace(old, new, 1)


def insert_before(src: str, anchor: str, new: str, what: str) -> str:
    n = src.count(anchor)
    if n != 1:
        sys.exit(f"! {what}: anchor matches {n} times, expected 1")
    print(f"  {what:<10} inserted {len(new):>5} chars")
    return src.replace(anchor, new + anchor, 1)


# ----------------------------------------------------------------- config --
CONFIG_JS = r"""/* ---------------------------------------------------------------- HEALTH ---
   QUARTERS. The scale is four chunks of 75 HP with real gaps between them, on
   the shell and on the lifeline both, because a count is the most robust thing
   a viewer can be asked for at phone size: "two chunks left" needs no scale,
   no reference and no estimate, and it survives motion blur, a thumbnail and
   peripheral vision. It also turns a continuous trend into EVENTS -- three per
   relic per fight, each one a beat -- which is a retention instrument as much
   as a legibility one. The last boundary is 0.25, which is
   CONFIG.desperation.at: the third chunk breaking is the frame the simulation
   actually changes gear, so the countable thing and the real thing coincide.

   Indexed by the chunk the head is IN, 0 = last quarter. Stages step in VALUE
   and BEHAVIOUR, never in hue -- every hue in this game already means an
   affinity (gold is the ult charge, green verdant, purple umbral, rose vigil),
   so a health scale that changed colour would claim to say something it does
   not. A value ramp is legible in monochrome, at thumbnail scale and to a
   colour-blind viewer, which is three properties a hue ramp does not have.

   `puls` is rad/s of an alpha wobble, and it is zero for the three healthy
   chunks on purpose: a readout that is always moving has no way to say now. */
const HEALTH_CHUNKS = [
  { lo: "#C4300C", hi: "#FFA24A", puls: 6.5 },   // last quarter = desperation
  { lo: "#9E1410", hi: "#FF6A34", puls: 0   },
  { lo: "#7E1012", hi: "#E0341E", puls: 0   },
  { lo: "#6E0C10", hi: "#C8221A", puls: 0   },   // full
];
/* Below this the last chunk is a sliver and "one hit from dead" deserves its
   own read, so BRINK overrides the chunk colour and doubles the pulse rate.
   A behaviour overlay rather than a fifth chunk -- the count stays four. */
const BRINK = { at: 0.10, lo: "#FF9A5A", hi: "#FFF4D0", puls: 13.0 };

/* The lifeline. `mode` is "mirror" -- two heads meeting at a marked centre,
   each head's distance from its own end being that relic's ABSOLUTE life --
   or "ratio", a single divider whose position is the share of the remaining
   life each relic holds. Mirror is the default because ratio cannot tell
   300v300 from 6v6, and "how close is the end" is the retention question.
   `pct` prints the percentage; `num` prints raw HP and stays off, because
   whether the build should state the score in HP is still an open decision. */
/* The ult block. `tip` is the `ult.tip` reminder in the last five seconds --
   the only text this HUD carries, and it is the same single source the intro
   card teaches from, so the two can never drift. */
const ULTBAR = { tip: true };

/* WHERE THE BAND LIVES. "top" or "bottom", and it is a live flag rather than a
   build option so the two can be A/B'd in one artifact.

   The argument for the top is not aesthetic: a Short is played inside platform
   chrome that occupies the BOTTOM of the screen -- caption, channel handle,
   the like/comment/share column on the right, and the scrub bar. Anything put
   down there is competing for pixels the app will draw over. The top strip is
   the one part of a vertical video the platform mostly leaves alone. */
const BAND = { pos: "top" };

const TUG = { on: true, mode: "mirror", pct: true, num: false, h: 56 };

"""


# ------------------------------------------------------------------- fonts --
# Atkinson Hyperlegible Next and Atkinson Hyperlegible Mono, from the Braille
# Institute -- typefaces designed so that characters which normally collapse
# into each other (I l 1, O 0, rn/m) stay distinguishable at low acuity. That
# is the exact failure mode this whole pass is about, and it is a stronger
# argument for them than taste is.
#
# EMBEDDED, not linked. The artifact is one self-contained file: render.py,
# verify.py and every sheet tool open it over file://, where a webfont URL
# would silently fall back and every measurement taken afterwards would be of
# the wrong typeface. Base64 costs 69 KB and removes the failure entirely.
#
# SIL Open Font License 1.1 (OFL-1.1), which permits embedding. The copyright
# and license notice ships inside the artifact with the fonts, as OFL requires.
FONT_PKGS = {
    "Atkinson Hyperlegible Next": "atkinson-hyperlegible-next",
    "Atkinson Hyperlegible Mono": "atkinson-hyperlegible-mono",
}

def font_css(root: pathlib.Path) -> str:
    faces = []
    for family, pkg in FONT_PKGS.items():
        # vendored next to the builder first, so the patch is self-contained and
        # a rebuild needs no network; the npm layout second, for a fresh checkout
        cands = [root / f"{pkg}.woff2",
                 root / f"node_modules/@fontsource-variable/{pkg}/files/{pkg}-latin-wght-normal.woff2"]
        f = next((c for c in cands if c.exists()), None)
        if f is None:
            sys.exit(f"! missing font: looked for\n    " + "\n    ".join(map(str, cands))
                     + f"\n  npm install @fontsource-variable/{pkg}")
        b64 = base64.b64encode(f.read_bytes()).decode()
        faces.append(
            "@font-face{font-family:'%s';font-style:normal;font-display:block;"
            "font-weight:100 900;src:url(data:font/woff2;base64,%s) format('woff2-variations')}"
            % (family, b64))
        print(f"  font       {family:<28} {f.stat().st_size/1024:5.1f} KB")
    return ("<style>\n/* Atkinson Hyperlegible Next & Mono -- Copyright the Atkinson\n"
            "   Hyperlegible Project Authors. SIL Open Font License 1.1. */\n"
            + "\n".join(faces) + "\n</style>\n")

# One family per role, everywhere: display/UI text is Next, anything that is a
# NUMBER READ AS A QUANTITY is Mono, because a monospace digit does not change
# width as it counts and a countdown that reflows is a countdown that twitches.
FONT_MAP = [
    ('ui-serif,Georgia,serif',                        "'Atkinson Hyperlegible Next',sans-serif"),
    ('ui-serif,Georgia,"Times New Roman",serif',      "'Atkinson Hyperlegible Next',sans-serif"),
    ('ui-sans-serif,system-ui,sans-serif',            "'Atkinson Hyperlegible Next',sans-serif"),
    ('ui-monospace,SFMono-Regular,Menlo,monospace',   "'Atkinson Hyperlegible Mono',monospace"),
    ('ui-monospace,Menlo,monospace',                  "'Atkinson Hyperlegible Mono',monospace"),
    ('ui-monospace,monospace',                        "'Atkinson Hyperlegible Mono',monospace"),
    ('system-ui,-apple-system,sans-serif',            "'Atkinson Hyperlegible Next',sans-serif"),
    ('600 12px system-ui',      "600 12px 'Atkinson Hyperlegible Next',sans-serif"),
    ('600 11px system-ui',      "600 11px 'Atkinson Hyperlegible Next',sans-serif"),
    ('11px ui-monospace',       "11px 'Atkinson Hyperlegible Mono',monospace"),
    ('700 48px ui-monospace,monospace', "700 48px 'Atkinson Hyperlegible Mono',monospace"),
]

# Canvas does not queue text against a font that has not loaded -- it draws the
# fallback and returns the fallback's metrics, so a headless capture taken one
# frame too early is silently in the wrong typeface with the wrong widths. The
# page therefore does not announce itself until the faces are in. Every harness
# already waits on `window.AC`, so gating the flag next to it costs no tool a
# single line except scpage, which now also waits for __fontsReady.
FONT_GATE = """
/* The capture path must never photograph a fallback face. `document.fonts`
   resolves once both variable fonts are parsed; until then __fontsReady is
   false and scpage.game() holds. The live page just redraws on the next rAF. */
window.__fontsReady = false;
(function(){
  const want = ["700 33px 'Atkinson Hyperlegible Next'",
                "800 30px 'Atkinson Hyperlegible Next'",
                "500 18px 'Atkinson Hyperlegible Next'",
                "800 40px 'Atkinson Hyperlegible Mono'"];
  const done = () => { window.__fontsReady = true; };
  if (!document.fonts){ done(); return; }
  Promise.all(want.map(f => document.fonts.load(f)))
    .then(() => document.fonts.ready).then(done).catch(done);
})();
"""


# ------------------------------------------------------------------ sigils --
SIG_JS = r"""/* ------------------------------------------------------------- ULT SIGILS ---
   RULE 9: one generic thing for N relics is a mistake this build has already
   made three times -- one ultimate burst, one ultimate sound, and nearly one
   banner animation. So this is a table keyed on the WEAPON ID, not on
   `ult.kind`: Eclipse, Exsanguinate, Bulwark and Consecration are all
   `kind:"nova"` and a viewer must never be shown the same picture for them.

   Each routine draws in UNIT SPACE -- the caller has already translated to the
   sigil centre and scaled so 1 = the sigil radius -- and is handed (t, cf, P):
   the presentation clock, the charge fraction 0..1, and the relic's palette.
   Charge is pure wall time (`f.charge += dt`, fires at `ult.charge`), so cf is
   a clock and every sigil uses it as one: the glyph ASSEMBLES as the ultimate
   approaches and is complete at the moment it goes off. That is the anticipation
   beat -- the viewer can see it coming, which is worth more to a fight than
   anything the glyph could say after the fact. */
const SG = {
  a(c, v){ c.globalAlpha = Math.max(0, Math.min(1, v)); },
  ring(c, x, y, r, col, w, al){ SG.a(c, al ?? 1); c.strokeStyle = col;
    c.lineWidth = w; c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke(); SG.a(c, 1); },
  arc(c, x, y, r, a0, a1, col, w, al){ SG.a(c, al ?? 1); c.strokeStyle = col;
    c.lineWidth = w; c.beginPath(); c.arc(x, y, r, a0, a1); c.stroke(); SG.a(c, 1); },
  disc(c, x, y, r, col, al){ SG.a(c, al ?? 1); c.fillStyle = col;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); SG.a(c, 1); },
  poly(c, pts, col, al, close){ SG.a(c, al ?? 1); c.fillStyle = col;
    c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
    if (close !== false) c.closePath(); c.fill(); SG.a(c, 1); },
  path(c, pts, col, w, al){ SG.a(c, al ?? 1); c.strokeStyle = col; c.lineWidth = w;
    c.lineJoin = "round"; c.lineCap = "round";
    c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
    c.stroke(); SG.a(c, 1); },
  /* a four-point shard, the shape the Daybreak sparks already use in the hall */
  shard(c, x, y, r, rot, col, al){
    SG.a(c, al ?? 1); c.fillStyle = col;
    c.save(); c.translate(x, y); c.rotate(rot);
    for (const k of [0, Math.PI / 2]){
      c.save(); c.rotate(k); c.beginPath();
      c.moveTo(0, -r); c.lineTo(r * 0.34, 0); c.lineTo(0, r); c.lineTo(-r * 0.34, 0);
      c.closePath(); c.fill(); c.restore();
    }
    c.restore(); SG.a(c, 1);
  },
  spokes(c, n, r0, r1, phase, col, w, al){
    SG.a(c, al ?? 1); c.strokeStyle = col; c.lineWidth = w; c.lineCap = "round";
    for (let i = 0; i < n; i++){
      const a = phase + i * TAU / n;
      c.beginPath();
      c.moveTo(Math.cos(a) * r0, Math.sin(a) * r0);
      c.lineTo(Math.cos(a) * r1, Math.sin(a) * r1); c.stroke();
    }
    SG.a(c, 1);
  },
};

const ULTSIG = {
  /* DAYBREAK -- the sun comes up. Rays turn, the disc rises with the charge,
     and four shards orbit because a spark field IS the mechanic. */
  dawnbringer(c, t, cf, P){
    const rise = 0.42 - cf * 0.46;
    SG.spokes(c, 12, 0.52, 0.96 + Math.sin(t * 2) * 0.04, t * 0.34, P.glow, 0.07, 0.34 + cf * 0.5);
    c.save(); c.beginPath(); c.rect(-1.1, -1.1, 2.2, 1.1 + rise); c.clip();
    SG.disc(c, 0, rise, 0.44, P.core, 0.55 + cf * 0.45);
    c.restore();
    SG.path(c, [[-0.86, rise], [0.86, rise]], P.glow, 0.075, 0.9);
    for (let i = 0; i < 4; i++){
      const a = t * 1.5 + i * TAU / 4;
      SG.shard(c, Math.cos(a) * 0.74, rise - 0.34 + Math.sin(a) * 0.26,
               0.1 * (0.35 + cf), t * 2 + i, P.glow, 0.35 + cf * 0.6);
    }
  },
  /* EXSANGUINATE -- a drop, and a ring drawn INTO it. The twinblade's two
     strokes cross behind. */
  widowmaker(c, t, cf, P){
    SG.path(c, [[-0.78, -0.78], [0.78, 0.78]], P.steel, 0.06, 0.3);
    SG.path(c, [[0.78, -0.78], [-0.78, 0.78]], P.steel, 0.06, 0.3);
    SG.ring(c, 0, 0, 0.92 - cf * 0.42, P.core, 0.06 + cf * 0.05, 0.35 + cf * 0.55);
    const s = 0.5 + cf * 0.22;
    SG.poly(c, [[0, -0.92 * s / 0.5 * 0.5], [0.44 * s / 0.5 * 0.5, 0.18],
                [0, 0.5 * s / 0.5 * 0.5], [-0.44 * s / 0.5 * 0.5, 0.18]],
            P.core, 0.55 + cf * 0.45);
    SG.disc(c, -0.1 * s, 0.06, 0.09 * s, P.glow, 0.5 + cf * 0.4);
  },
  /* CRUCIBLE -- the bowl, the heat, and four chevrons pointing IN, because
     the ultimate's first act is a pull. */
  grudgebearer(c, t, cf, P){
    SG.path(c, [[-0.6, -0.34], [-0.42, 0.5], [0.42, 0.5], [0.6, -0.34]], P.core, 0.1, 0.85);
    SG.path(c, [[-0.7, -0.34], [0.7, -0.34]], P.glow, 0.09, 0.9);
    for (let i = 0; i < 3; i++){
      const x = -0.32 + i * 0.32, w = Math.sin(t * 3 + i) * 0.09;
      SG.path(c, [[x, -0.44], [x + w, -0.62], [x - w, -0.8]], P.glow, 0.06, 0.3 + cf * 0.6);
    }
    for (let i = 0; i < 4; i++){
      const a = i * TAU / 4 + Math.PI / 4, d = 1.02 - cf * 0.34;
      c.save(); c.translate(Math.cos(a) * d, Math.sin(a) * d); c.rotate(a);
      SG.path(c, [[0.14, -0.16], [-0.06, 0], [0.14, 0.16]], P.glow, 0.07, 0.3 + cf * 0.6);
      c.restore();
    }
  },
  /* BRAMBLESNARE -- a thorn ring that CLOSES as the charge fills. */
  thornwake(c, t, cf, P){
    const r = 0.92 - cf * 0.3;
    SG.ring(c, 0, 0, r, P.core, 0.07, 0.85);
    for (let i = 0; i < 9; i++){
      const a = i * TAU / 9 + t * 0.22;
      const ix = Math.cos(a) * r, iy = Math.sin(a) * r;
      const l = 0.2 + cf * 0.12;
      SG.poly(c, [[ix, iy],
                  [ix - Math.cos(a - 0.34) * l, iy - Math.sin(a - 0.34) * l],
                  [ix - Math.cos(a + 0.16) * l * 0.5, iy - Math.sin(a + 0.16) * l * 0.5]],
              P.glow, 0.55 + cf * 0.4);
    }
    SG.disc(c, 0, 0, 0.1 + cf * 0.1, P.glow, 0.4 + cf * 0.5);
  },

  /* THE HARROWING -- twelve blades, held, then thrown. Added by
     lastlight_build.py's relic; the sigil table is keyed on weapon id and this
     builder EXITS if any relic lacks one, which is how the eighteenth relic
     announced itself here rather than shipping a blank ult block.

     The glyph is the cast frozen one instant before it happens: twelve little
     scythes on a ring, hafts pointing back at the centre they came from,
     sliding OUT and brightening as the charge fills, and the core emptying as
     they go. THE COUNT IS THE COUNT -- `u.scythes` is 12 and so is this, so a
     viewer who counts the glyph and then counts the spray gets the same
     number. Same discipline as Slagburst's cracks equalling its shards. */
  lastlight(c, t, cf, P){
    const N = 12;
    const d = 0.30 + cf * 0.56;                  // how far out they have got
    SG.ring(c, 0, 0, 0.96, P.core, 0.05, 0.14 + cf * 0.26);
    for (let i = 0; i < N; i++){
      const a = i * TAU / N + t * 0.18;
      c.save();
      c.translate(Math.cos(a) * d, Math.sin(a) * d);
      c.rotate(a);
      SG.path(c, [[-0.21, 0.02], [0.01, 0.0]], P.core, 0.045, 0.30 + cf * 0.55);
      SG.arc(c, 0.05, -0.055, 0.105, -1.15, 1.85, P.glow, 0.048, 0.42 + cf * 0.58);
      c.restore();
    }
    SG.disc(c, 0, 0, 0.17 - cf * 0.11, P.glow, 0.32 + cf * 0.4);
  },
  /* DIRGE -- a spiral wound inward, and the bell it is sung from. */
  gravemourn(c, t, cf, P){
    const pts = [];
    for (let i = 0; i <= 68; i++){
      const u = i / 68, a = t * 0.7 + u * TAU * 2.1, r = 0.96 * (1 - u * (0.55 + cf * 0.4));
      pts.push([Math.cos(a) * r, Math.sin(a) * r]);
    }
    SG.path(c, pts, P.core, 0.065, 0.4 + cf * 0.5);
    SG.path(c, [[-0.3, 0.34], [-0.22, -0.2], [0.22, -0.2], [0.3, 0.34]], P.glow, 0.08, 0.85);
    SG.disc(c, 0, 0.44, 0.09, P.glow, 0.6 + cf * 0.4);
  },
  /* IRONBLOOM -- a bud clamped shut that OPENS with the charge, shrapnel
     already loose around it. */
  slagheart(c, t, cf, P){
    for (let i = 0; i < 3; i++){
      const a = -Math.PI / 2 + i * TAU / 3;
      c.save(); c.rotate(a + cf * 0.5);
      SG.poly(c, [[0, 0.1], [0.34 + cf * 0.16, -0.3 - cf * 0.3], [0, -0.66 - cf * 0.3],
                  [-0.34 - cf * 0.16, -0.3 - cf * 0.3]], P.core, 0.7 + cf * 0.3);
      c.restore();
    }
    SG.disc(c, 0, 0, 0.17, P.glow, 0.6 + cf * 0.4);
    for (let i = 0; i < 6; i++){
      const a = t * 1.1 + i * TAU / 6, d = 0.8 + Math.sin(t * 2.4 + i) * 0.12;
      SG.disc(c, Math.cos(a) * d, Math.sin(a) * d, 0.055, P.glow, 0.25 + cf * 0.6);
    }
  },
  /* UNMAKING -- a rune that comes APART. The four quarters drift out as the
     charge fills, which is the mechanic stated backwards and on purpose. */
  spellbreaker(c, t, cf, P){
    const d = 0.06 + cf * 0.2;
    for (let i = 0; i < 4; i++){
      const a = i * TAU / 4 + Math.PI / 4;
      c.save(); c.translate(Math.cos(a) * d, Math.sin(a) * d); c.rotate(cf * 0.4 * (i % 2 ? 1 : -1));
      SG.poly(c, [[0.04, 0.04], [0.52, 0.04], [0.52, 0.52], [0.04, 0.52]], P.core, 0.8);
      c.restore();
    }
    SG.ring(c, 0, 0, 0.95, P.glow, 0.05, 0.25 + cf * 0.5);
    SG.path(c, [[-0.16, 0], [0.16, 0]], P.glow, 0.07, 0.4 + cf * 0.5);
  },
  /* QUARRELSTORM -- eight heads going out. The nova of arrows, counted. */
  ironhail(c, t, cf, P){
    for (let i = 0; i < 8; i++){
      const a = i * TAU / 8 + t * 0.3, d = 0.3 + cf * 0.56;
      c.save(); c.translate(Math.cos(a) * d, Math.sin(a) * d); c.rotate(a + Math.PI / 2);
      SG.poly(c, [[0, -0.24], [0.15, 0.1], [0, 0.02], [-0.15, 0.1]], P.core, 0.5 + cf * 0.5);
      c.restore();
    }
    SG.ring(c, 0, 0, 0.2, P.glow, 0.07, 0.6);
  },
  /* BULWARK -- the shield, and the shove that comes off it. */
  lightkeeper(c, t, cf, P){
    SG.ring(c, 0, 0, 0.55 + cf * 0.42, P.glow, 0.07, 0.2 + cf * 0.6);
    SG.poly(c, [[0, -0.72], [0.56, -0.42], [0.56, 0.2], [0, 0.76], [-0.56, 0.2], [-0.56, -0.42]],
            P.core, 0.85);
    SG.path(c, [[0, -0.5], [0, 0.5]], P.glow, 0.07, 0.5 + cf * 0.4);
    SG.path(c, [[-0.34, -0.1], [0.34, -0.1]], P.glow, 0.07, 0.5 + cf * 0.4);
  },
  /* REPRISAL -- a reticle that TIGHTENS, because the ult is one aimed shot
     paid for with the ward. */
  farwarden(c, t, cf, P){
    const r = 0.92 - cf * 0.36;
    SG.ring(c, 0, 0, r, P.core, 0.06, 0.85);
    SG.spokes(c, 4, r * 0.42, r * 1.24, t * 0.2, P.glow, 0.06, 0.4 + cf * 0.5);
    SG.disc(c, 0, 0, 0.09 + cf * 0.06, P.glow, 0.5 + cf * 0.5);
    c.save(); c.rotate(-Math.PI / 4);
    SG.path(c, [[-0.95, 0], [0.2 + cf * 0.6, 0]], P.steel, 0.05, 0.25 + cf * 0.6);
    c.restore();
  },
  /* BENEDICTION -- the halo, and the shaft through it. Heals, so the shaft
     grows DOWN into the frame rather than out of it. */
  aureole(c, t, cf, P){
    const g = c.createLinearGradient(0, -1, 0, 1);
    g.addColorStop(0, P.glow + "00"); g.addColorStop(0.5, P.glow);
    g.addColorStop(1, P.glow + "00");
    SG.a(c, 0.3 + cf * 0.55); c.fillStyle = g;
    c.fillRect(-0.17 - cf * 0.08, -1, 0.34 + cf * 0.16, 2); SG.a(c, 1);
    c.save(); c.scale(1, 0.36);
    SG.ring(c, 0, -1.5, 0.62, P.core, 0.16, 0.9);
    c.restore();
    for (let i = 0; i < 3; i++){
      const y = 0.9 - ((t * 0.5 + i / 3) % 1) * 1.7;
      SG.disc(c, 0, y, 0.06, P.glow, 0.5 * cf);
    }
  },
  /* CONSECRATION -- the censer swings, and the rings go out from where it is,
     not from the middle. */
  censer(c, t, cf, P){
    const sw = Math.sin(t * 1.7) * (0.16 + cf * 0.2);
    SG.path(c, [[0, -0.95], [Math.sin(sw) * 0.85, -0.95 + Math.cos(sw) * 0.72]], P.steel, 0.045, 0.7);
    const bx = Math.sin(sw) * 0.85, by = -0.95 + Math.cos(sw) * 0.72;
    SG.poly(c, [[bx - 0.26, by], [bx + 0.26, by], [bx + 0.17, by + 0.4], [bx - 0.17, by + 0.4]],
            P.core, 0.9);
    for (let i = 0; i < 3; i++){
      const u = (t * 0.6 + i / 3) % 1;
      SG.ring(c, bx, by + 0.2, 0.12 + u * 0.72, P.glow, 0.05, (1 - u) * (0.25 + cf * 0.6));
    }
  },
  /* SLAGBURST -- the shell splits, and NINE shards come off it, because nine
     is the measured ceiling the week-one note records as countable in frame. */
  emberedge(c, t, cf, P){
    SG.disc(c, 0, 0, 0.3, P.core, 0.9);
    SG.path(c, [[-0.2, -0.2], [0.05, 0], [-0.1, 0.22]], P.dark, 0.06, 0.9);
    for (let i = 0; i < 9; i++){
      const a = i * TAU / 9 + t * 0.24, d = 0.4 + cf * 0.5;
      SG.shard(c, Math.cos(a) * d, Math.sin(a) * d, 0.1, a, P.glow, 0.3 + cf * 0.65);
    }
  },
  /* BLOODPRICE -- a beam, and the toll paid under it. */
  oathwound(c, t, cf, P){
    const g = c.createLinearGradient(-1, 0, 1, 0);
    g.addColorStop(0, P.core + "00"); g.addColorStop(0.55, P.core); g.addColorStop(1, P.glow);
    SG.a(c, 0.35 + cf * 0.6); c.fillStyle = g;
    c.fillRect(-1, -0.16 - cf * 0.06, 2, 0.32 + cf * 0.12); SG.a(c, 1);
    SG.poly(c, [[0, 0.3], [0.24, 0.66], [0, 0.92], [-0.24, 0.66]], P.core, 0.55 + cf * 0.4);
    SG.disc(c, 0.86, 0, 0.11 + cf * 0.06, P.glow, 0.6 + cf * 0.4);
  },
  /* ROOTFAST -- roots going down and GRIPPING. Anchored, not thrown. */
  heartwood(c, t, cf, P){
    SG.path(c, [[0, -0.9], [0, 0.2]], P.core, 0.1, 0.9);
    for (const s of [-1, 1]) for (let i = 0; i < 2; i++){
      const y = 0.2 - i * 0.34, l = (0.34 + cf * 0.3) * (1 - i * 0.2);
      SG.path(c, [[0, y], [s * l * 0.6, y + 0.22], [s * l, y + 0.6 - i * 0.1]],
              P.core, 0.075, 0.55 + cf * 0.4);
    }
    for (let i = 0; i < 4; i++){
      const a = -Math.PI / 2 + (i - 1.5) * 0.44;
      SG.disc(c, Math.cos(a) * 0.55, -0.62 + Math.sin(a) * 0.16 + 0.16, 0.09,
              P.glow, 0.35 + cf * 0.5);
    }
  },
  /* ECLIPSE -- one disc slides over the other and the corona is what is left.
     Four relics share kind:"nova"; not one of them may share this picture. */
  nightfell(c, t, cf, P){
    SG.spokes(c, 16, 0.62, 0.62 + 0.3 * (0.3 + cf * 0.7), t * 0.2, P.glow, 0.045, 0.25 + cf * 0.55);
    SG.disc(c, 0, 0, 0.58, P.glow, 0.75);
    SG.disc(c, 0.5 - cf * 0.5, -0.14 + cf * 0.14, 0.58, "#07050C", 1);
    SG.ring(c, 0, 0, 0.58, P.core, 0.05, 0.4 + cf * 0.5);
  },
  /* COROLLARY -- a proof. The outer figure is given; the inner one is what
     follows from it, and it draws itself in as the charge fills. */
  axiom(c, t, cf, P){
    c.save(); c.rotate(t * 0.16);
    SG.path(c, [0, 1, 2, 0].map(i => [Math.cos(-Math.PI / 2 + i * TAU / 3) * 0.9,
                                      Math.sin(-Math.PI / 2 + i * TAU / 3) * 0.9]),
            P.core, 0.07, 0.85);
    SG.path(c, [0, 1, 2, 0].map(i => [Math.cos(Math.PI / 2 + i * TAU / 3) * 0.5 * cf,
                                      Math.sin(Math.PI / 2 + i * TAU / 3) * 0.5 * cf]),
            P.glow, 0.06, 0.3 + cf * 0.6);
    c.restore();
    SG.poly(c, [[-0.13, 0.68], [0.13, 0.68], [0.13, 0.94], [-0.13, 0.94]],
            P.glow, 0.3 + cf * 0.6);   // the tombstone: QED
  },
};

"""

# ------------------------------------------------------------------ gauge --
GAUGE_JS = r"""    /* --- the health gauge, wrapped inside the shell --------------------
       v5. FOUR CHUNKS OF 75 HP, with real gaps. The v3 ring was accurate and
       beautifully drawn at 1.7 sim units, which is 3.45 canvas px, which is
       0.21 mm on a phone at arm's length -- about 2 arcmin, at the threshold
       of what an eye resolves. Four faults were measured; each is answered.

       1. STROKE. 6.0 units is 12.2 canvas px, 0.73 mm, ~7 arcmin. Clears the
          acuity limit by three and a half times.
       2. THE EXTREMES COLLIDED. A full 360 sweep puts hpFrac 1.0 and hpFrac
          0.04 within 14 degrees of each other, so the ember -- the brightest
          element of the readout, and the one the v3 note calls "where it sits
          on the circle IS the health value" -- sat in nearly the same place at
          full health and at one hit from death. The sweep is 270 with the gap
          at the FOOT: the two ends are 90 degrees apart.
       3. NO REFERENCE. An arc with no track is an ANGLE judgement, and angle
          reads less accurately than length. The empty track is drawn.
       4. IT ASKED FOR AN ESTIMATE. Even fixed, a continuous arc asks the
          viewer to judge a proportion. Four chunks ask them to COUNT, which
          needs no scale and no reference, survives motion blur and thumbnail
          scale, and turns a trend into three events per relic per fight.

       The last boundary is 0.25 = CONFIG.desperation.at, so the frame the
       third chunk breaks is the frame the simulation changes gear. An emptied
       chunk stays on the track as dead groove -- a permanent record, readable
       in a frozen frame, which a pulse is not.

       THE CROSSING FLASH HOLDS NO STATE. `hpGhost` already lags `hp`, so "the
       ghost is still above a boundary the real value has fallen below" IS the
       crossing window -- no timer, no animation field, nothing a heal can
       leave stranded, and identical in the live page and the offline render.
       Same trick the fractures use.

       THE FLASH IS DELIBERATELY SMALL. The first cut turned the gauge white
       and bloomed it at shadowBlur 30 on the crossing frame, which obliterated
       the ball and the readout for a quarter of a second -- announcing a state
       change by destroying the instrument that states it. Rule 6. The ring-pop
       carries the event; the gauge keeps saying the value throughout. */
    const GA0 = Math.PI * 0.75, GSPAN = Math.PI * 1.5;   // 270deg, foot open
    const rr = R * 0.86, lw = 6.0, NCH = 4, CGAP = 0.075;
    const chunkOf = (v) => Math.min(NCH - 1, Math.floor(v * NCH));
    const ghostFrac = clamp((f.hpGhost ?? f.hp) / base, 0, 1);
    const brink = hpFrac > 0 && hpFrac <= BRINK.at;
    const SS = brink ? BRINK : HEALTH_CHUNKS[chunkOf(hpFrac)];

    /* the crossing window, derived rather than stored */
    let sf = 0;
    for (const T of [chunkOf(ghostFrac) / NCH, BRINK.at]){
      if (ghostFrac > T && hpFrac <= T)
        sf = Math.max(sf, clamp((ghostFrac - T) / 0.045, 0, 1));
    }
    const puls = SS.puls ? 0.72 + 0.28 * Math.sin(m.t * SS.puls) : 1;
    const rf = f.ringFlash || 0;
    const seg = GSPAN / NCH;

    c.save();
    c.lineCap = "butt";
    for (let i = 0; i < NCH; i++){
      const a0 = GA0 + seg * i + CGAP / 2, a1 = GA0 + seg * (i + 1) - CGAP / 2;
      const fill = clamp(hpFrac * NCH - i, 0, 1);
      /* The channel has to be dark enough to frame a chunk on a BRIGHT relic
         -- a red band on Dawnbringer's near-white shell is the worst-contrast
         case in the roster and it is invisible without this. */
      c.strokeStyle = "#04030A"; c.lineWidth = lw + 3.4;
      c.beginPath(); c.arc(f.x, f.y, rr, a0, a1); c.stroke();
      /* the empty groove: this is what makes it a count and not an estimate */
      c.strokeStyle = fill > 0 ? "#3A3048" : "#241D33";
      c.lineWidth = lw;
      c.beginPath(); c.arc(f.x, f.y, rr, a0, a1); c.stroke();
      if (fill <= 0.001) continue;
      /* Every lit chunk takes the CURRENT stage colour, not its own index.
         A fixed redline on the last chunk made a relic at 300 HP look like it
         was already hurt -- the colour was stating a position on the scale
         while the viewer read it as a state. */
      const CS = SS;
      const g2 = c.createConicGradient(a0, f.x, f.y);
      g2.addColorStop(0, CS.lo);
      g2.addColorStop(Math.min(0.999, (a1 - a0) * fill / TAU), CS.hi);
      g2.addColorStop(1, CS.hi);
      c.strokeStyle = (f.mend > 0 || rf > 0.55) ? "#FFF4D0" : g2;
      c.globalAlpha = puls;
      c.lineWidth = lw + (f.mend > 0 ? 1.4 : 0) + rf * 3.0 + sf * 1.8;
      c.shadowColor = f.mend > 0 ? "#FFF4D0" : CS.hi;
      c.shadowBlur = (SS.puls ? 16 : 9) + rf * 26 + sf * 10;
      c.beginPath(); c.arc(f.x, f.y, rr, a0, a0 + (a1 - a0) * fill); c.stroke();
      c.shadowBlur = 0; c.globalAlpha = 1;
      /* THE BEVEL, and it is not decoration. The roster sheet says the red
         scale is a weak read on a WARM shell -- Widowmaker and Goreshard are
         bloodsworn crimson, and Grudgebearer, Slagheart, Ironhail and
         Emberedge are dwarven amber, so six of seventeen relics wear the
         gauge's own hue. A dark channel alone does not separate them, because
         hue against hue is the one comparison that fails. A cream hairline on
         the lit edge separates by VALUE instead, which is the principle
         `_stWard` already records for a self-buff: contrast that does not
         depend on the colour underneath it. */
      c.strokeStyle = "#FFEFD8"; c.globalAlpha = 0.85 * puls;
      c.lineWidth = 1.3;
      c.beginPath();
      c.arc(f.x, f.y, rr + lw / 2 - 0.65, a0, a0 + (a1 - a0) * fill); c.stroke();
      c.globalAlpha = 1;
    }

    if (maxFrac < 1){                     // life permanently eaten by Curse
      c.strokeStyle = AFFINITIES.umbral.core; c.globalAlpha = 0.55;
      c.lineWidth = lw * 0.5;
      c.beginPath();
      c.arc(f.x, f.y, rr + lw * 0.72, GA0 + GSPAN * maxFrac, GA0 + GSPAN);
      c.stroke();
      c.globalAlpha = 1;
    }

    /* The drain tail. The ghost lags the real value by a few tenths, so the
       segment between them is exactly the bite that was just taken -- the size
       of a hit becomes something you watch happen rather than a number you
       have to read. Borrowed from fighting games, where it has been solving
       this same problem for thirty years. Six times wider than it was. */
    if (ghostFrac > hpFrac + 0.002){
      c.strokeStyle = "#FFE9C0"; c.globalAlpha = 0.9; c.lineWidth = lw;
      c.shadowColor = "#FF9A5A"; c.shadowBlur = 16;
      for (let i = 0; i < NCH; i++){
        const a0 = GA0 + seg * i + CGAP / 2, a1 = GA0 + seg * (i + 1) - CGAP / 2;
        const lo = clamp(hpFrac * NCH - i, 0, 1), hi = clamp(ghostFrac * NCH - i, 0, 1);
        if (hi - lo < 0.002) continue;
        c.beginPath();
        c.arc(f.x, f.y, rr, a0 + (a1 - a0) * lo, a0 + (a1 - a0) * hi); c.stroke();
      }
      c.shadowBlur = 0; c.globalAlpha = 1;
    }

    if (hpFrac > 0.001){
      /* The head. One bright moving point is worth more than any amount of
         extra ring: the eye locks onto it, and now that the scale has a foot,
         a groove and four chunks, where it sits is unambiguous. */
      const ha = GA0 + GSPAN * hpFrac;
      const hxp = f.x + Math.cos(ha) * rr, hyp = f.y + Math.sin(ha) * rr;
      c.save();
      c.globalCompositeOperation = "lighter";
      const er = 8 + rf * 8 + sf * 3;
      const eg = c.createRadialGradient(hxp, hyp, 0, hxp, hyp, er);
      eg.addColorStop(0, "#FFFFFF");
      eg.addColorStop(0.32, SS.puls ? "#FF5A3C" : "#FF9A5A");
      eg.addColorStop(1, "#FF3B2400");
      c.fillStyle = eg;
      c.beginPath(); c.arc(hxp, hyp, er, 0, TAU); c.fill();
      c.restore();
    }

    /* The crossing. One ring, out of the shell, on the frame a chunk breaks --
       so losing a quarter is an EVENT and not a colour you notice later. sf
       falls 1 -> 0 as the ghost catches up, which is both the fade and the
       expansion, from one derived number. */
    if (sf > 0){
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = sf * 0.5;
      c.strokeStyle = "#FFF4D0";
      c.lineWidth = 1.8 + sf * 2.2;
      c.shadowColor = "#FFD9A0"; c.shadowBlur = 11;
      c.beginPath();
      c.arc(f.x, f.y, R * (1.02 + (1 - sf) * 0.78), 0, TAU); c.stroke();
      c.restore();
    }
    c.restore();

"""


# --------------------------------------------------------------- lifeline --
HUD_JS = r"""  /* --------------------------------------------------------------- hud ---
     The two identity rows are GONE from here. A relic's name now lives inside
     its own half of the lifeline, next to its own percentage and its own four
     chunks, so identity and health are one object instead of two things the
     viewer has to associate across 120 px of empty band. What is left up here
     is the one thing that genuinely cannot go on a moving ball and does not
     belong to the health readout: the ultimate charge.

     One row, mirrored -- A's charge on the left, B's on the right -- so the
     band echoes the lifeline underneath it and the left half of the frame is
     A everywhere. `this.hud` does not move. */
  drawHud(m){
    /* Top: the ult row sits above the lifeline. Bottom: the lifeline stays
       against the hall and the ult row goes under it, so in both cases the
       readout nearest the fight is the one the fight changes. */
    const y = BAND.pos === "bottom"
      ? this.arenaTop + this.ah + 12 + TUG.h + 14
      : 6;
    this.drawBar(m, m.a, y, -1);
    this.drawBar(m, m.b, y,  1);
  }

  /* The ult block. The two identity rows are gone, so this has ~96px of band
     and half the frame width to itself, and it spends it on the three things
     an ultimate is: WHAT it is (a bespoke sigil), WHEN it lands (a quartered
     charge bar and, in the last five seconds, a countdown), and WHAT IT DOES
     (its own `ult.tip`, the same string the intro card teaches from -- shown
     only while it is imminent).

     That last one is rule 4 -- teach before, remind during -- finally getting
     its DURING. The tip has only ever existed on the intro card, which is 40
     seconds and one skip away from the moment it matters. It is transient by
     construction: it fades in when the ult is five seconds out and is gone the
     instant it fires, so it is a cue and not a caption sitting on the frame. */
  drawBar(m, f, y, side){
    const c = this.ctx, pad = 34;
    const U = f.w.ult;
    const cf = clamp(f.charge / U.charge, 0, 1);
    const secs = Math.max(0, U.charge - f.charge);
    const near = secs <= 5, hot = secs <= 1.6;
    const left = side < 0;
    const SR = 42, NCH = 4;
    const scx = left ? pad + SR : this.W - pad - SR, scy = y + 46;
    const tx = left ? pad + SR * 2 + 20 : this.W - pad - SR * 2 - 20;
    /* 340, not 430. At 430 the left bar ran to x=568 and its countdown sat at
       584 -- both past the frame's midpoint and into the other relic's block.
       Every width here is checked against `this.W / 2`, and 280 rather than
       340 so the bar stops clear of the countdown seated at the midline. */
    const bw = 280, bh = 15, bx = left ? tx : tx - bw;
    const half = this.W / 2;

    this._ultSigil(m, f, scx, scy, SR, cf, hot);

    c.save();
    c.textAlign = left ? "left" : "right";
    c.font = "700 33px ui-serif,Georgia,serif";
    c.fillStyle = hot ? "#FFF4D0" : (near ? "#C9BDD4" : "#877C96");
    if (hot){ c.shadowColor = "#FFF4D0"; c.shadowBlur = 18; }
    c.fillText(U.name.toUpperCase(), tx, y + 32);
    c.shadowBlur = 0;

    /* the charge, in the same four chunks as the health, so the frame has one
       counting language rather than two */
    const gap = 5, cw = (bw - gap * (NCH - 1)) / NCH;
    for (let i = 0; i < NCH; i++){
      const seg = left ? bx + i * (cw + gap) : bx + bw - cw - i * (cw + gap);
      const fill = clamp(cf * NCH - i, 0, 1);
      c.fillStyle = "#181125";
      this.roundRect(seg, y + 42, cw, bh, 4); c.fill();
      if (fill <= 0.001) continue;
      c.fillStyle = hot ? "#FFF4D0" : f.aff.glow;
      if (hot){ c.shadowColor = "#FFF4D0"; c.shadowBlur = 12; }
      this.roundRect(left ? seg : seg + cw * (1 - fill), y + 42, cw * fill, bh, 4);
      c.fill();
      c.shadowBlur = 0;
    }

    /* the countdown. Anticipation is the cheapest retention there is: a viewer
       who can see the ultimate coming waits for it. Only the last five. */
    if (near){
      const k = 1 - clamp(secs / 5, 0, 1);
      /* Seated against the midline and growing OUTWARD. Placed off the end of
         each bar instead, two relics both about to fire printed "NOW" on top
         of each other -- which is the state the countdown exists for. */
      c.textAlign = left ? "right" : "left";
      c.font = `800 ${26 + k * 14}px ui-monospace,SFMono-Regular,Menlo,monospace`;
      c.fillStyle = hot ? "#FFF4D0" : "#C9A227";
      c.shadowColor = "#FFF4D0"; c.shadowBlur = 8 + k * 16;
      c.fillText(hot ? "NOW" : secs.toFixed(1),
                 left ? half - 22 : half + 22, y + 58);
      c.shadowBlur = 0;
      /* the tip, wrapped, and only while it is about to matter */
      if (ULTBAR.tip && U.tip){
        /* the countdown above set textAlign to face the midline; the tip
           faces the other way, and forgetting that ran it off both edges */
        c.textAlign = left ? "left" : "right";
        c.globalAlpha = clamp((5 - secs) / 1.2, 0, 1) * 0.92;
        c.font = "500 18px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = "#C6BBA9";
        /* wraps inside this relic's own half and nowhere near the other's */
        const tw = Math.abs(left ? half - tx : tx - half) - 12;
        const words = U.tip.split(" "), lines = [];
        let ln = "";
        for (const w of words){
          const t2 = ln ? ln + " " + w : w;
          if (c.measureText(t2).width > tw && ln){ lines.push(ln); ln = w; }
          else ln = t2;
        }
        if (ln) lines.push(ln);
        for (let i = 0; i < Math.min(2, lines.length); i++)
          c.fillText(lines[i], tx, y + 74 + i * 22);
        c.globalAlpha = 1;
      }
    }
    c.restore();
  }

  /* One sigil per relic, keyed on the weapon id. Four relics share
     kind:"nova" and not one of them may share a picture -- see ULTSIG. The
     fallback is the relic's OWN weapon silhouette, never a generic mark,
     because a generic mark for seventeen relics is the mistake rule 9 exists
     to stop. */
  _ultSigil(m, f, x, y, r, cf, hot){
    const c = this.ctx, P = f.aff;
    c.save();
    c.fillStyle = "#0A0714";
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    c.strokeStyle = hot ? "#FFF4D0" : "#2A2238";
    c.lineWidth = hot ? 2.6 : 1.8;
    if (hot){ c.shadowColor = "#FFF4D0"; c.shadowBlur = 14; }
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke();
    c.shadowBlur = 0;
    c.save();
    c.beginPath(); c.arc(x, y, r - 1.5, 0, TAU); c.clip();
    c.translate(x, y);
    const k = r * 0.76; c.scale(k, k);
    c.lineWidth = 0.06;
    const fn = ULTSIG[f.w.id];
    if (fn) fn(c, m.t, cf, P);
    else { c.scale(1 / k * 0.55, 1 / k * 0.55); this._artShape(c, f.w, P); }
    c.restore();
    c.restore();
  }

  /* ------------------------------------------------------------ LIFELINE ---
     "How badly is this relic hurt" is asked at the instant of impact, with the
     eye already on the ball. That is why health lives on the shell and stays.

     "WHO IS WINNING" is a different question. It is asked BETWEEN exchanges,
     and it cannot be answered at either ball, because it needs both. Rule 5 --
     put the information where the eye already is -- retired the HUD health bar
     in v3 and was right to; but splitting a COMPARISON across two objects
     moving at 2500 px/s is not putting it where the eye is. It is putting it
     in two places at once and charging the viewer two saccades and an angle
     subtraction for the one fact the content goal cares about most.

     One object. Two halves growing inward from the frame edges to a marked
     centre, each half's fill being that relic's life on the 300 scale --
     position along a common scale, the most accurately read encoding there is,
     and about 1000 px of it against the gauge's 347 px of arc. A pure ratio
     divider (TUG.mode = "ratio") cannot tell 300v300 from 6v6, which is why
     mirror is the default: both halves retreat as the fight burns down, so a
     nearly empty bar is a nearly finished fight.

     FOUR CHUNKS, the same four the shell carries, so the two readouts are one
     language: count them on the bar, count them on the ball, they agree. The
     last boundary is CONFIG.desperation.at.

     NAME, PERCENTAGE AND CHUNKS IN ONE PANEL. The name sits at the outer edge
     in its own affinity colour; the percentage sits at the INNER edge, so the
     two numbers flank the centre line and are read as a pair rather than
     hunted for. Both are fixed seats -- the head moves, and a number riding it
     would collide with the centre at full life and run off the frame at low.
     30 px is 1.8 mm on a phone, about 18 arcmin, comfortably above the ~14
     where numerals stop being read and start being recognised as shapes.

     DRAWN LAST, IN SCREEN SPACE, ON PURPOSE. draw() paints the HUD before the
     arena, and a cinema cut lets the arena clip bleed 70 px up over the band;
     that is the v26 HUD spill, and anything that has to survive a cut belongs
     after drawArenaFrame rather than inside drawBar. The letterbox is clipped
     to the arena rect and cannot reach it either. */
  drawTug(m){
    if (!TUG.on || this._introScene) return;
    const c = this.ctx;
    const base = CONFIG.combat.baseHP;
    const x0 = this.pad + 8, x1 = this.W - this.pad - 8, w = x1 - x0;
    const h = TUG.h;
    const y = BAND.pos === "bottom" ? this.arenaTop + this.ah + 12
                                  : this.arenaTop - h - 8;
    const mid = (x0 + x1) / 2;
    const tier = 26, cy0 = y + tier + 3, ch = h - tier - 10;
    const frac = (o) => clamp(Math.max(0, o) / base, 0, 1);
    const NCH = 4;

    c.save();
    /* A plate across the whole band. Two jobs: it seats the panel against the
       hall, and it is the one thing in the frame a cinema cut's 70 px arena
       bleed must not be allowed to paint over. */
    c.fillStyle = "#07050C";
    c.fillRect(0, y - 8, this.W, h + 14);
    c.fillStyle = "#0B0812";
    this.roundRect(x0, y, w, h, 8); c.fill();
    c.strokeStyle = "#221B30"; c.lineWidth = 2;
    this.roundRect(x0, y, w, h, 8); c.stroke();

    if (TUG.mode === "ratio"){
      /* One divider. Kept because it is the purest answer to the single
         question, and one flag away if the mirror reads as two bars. */
      const fa = frac(m.a.hp), fb = frac(m.b.hp), tot = fa + fb;
      const sp = tot > 1e-6 ? x0 + w * (fa / tot) : mid;
      c.save();
      c.beginPath(); this.roundRect(x0, y, w, h, 8); c.clip();
      c.fillStyle = m.a.aff.core; c.fillRect(x0, y, sp - x0, h);
      c.fillStyle = m.b.aff.core; c.fillRect(sp, y, x1 - sp, h);
      c.restore();
      c.strokeStyle = "#FFF4D0"; c.lineWidth = 5;
      c.beginPath(); c.moveTo(sp, y - 9); c.lineTo(sp, y + h + 9); c.stroke();
      c.restore();
      return;
    }

    const GAPX = 5, half = w / 2 - 7;
    const cw = (half - GAPX * (NCH - 1)) / NCH;
    for (const [f, sign, ex] of [[m.a, 1, x0 + 3], [m.b, -1, x1 - 3]]){
      const fr = frac(f.hp), gh = frac(f.hpGhost ?? f.hp);
      const brink = fr > 0 && fr <= BRINK.at;
      const SS = brink ? BRINK : HEALTH_CHUNKS[Math.min(NCH - 1, Math.floor(fr * NCH))];
      const al = SS.puls ? 0.74 + 0.26 * Math.sin(m.t * SS.puls) : 1;

      for (let i = 0; i < NCH; i++){
        const cx0 = ex + sign * (i * (cw + GAPX));
        const fill = clamp(fr * NCH - i, 0, 1);
        const gfil = clamp(gh * NCH - i, 0, 1);
        const L = Math.min(cx0, cx0 + sign * cw);
        /* the empty slot: this is what makes it a COUNT and not an estimate */
        c.fillStyle = "#1B1428";
        c.fillRect(L, cy0, cw, ch);
        c.strokeStyle = "#33294A"; c.lineWidth = 1.4;
        c.strokeRect(L + 0.7, cy0 + 0.7, cw - 1.4, ch - 1.4);
        /* the drain tail, the same instrument as on the shell */
        if (gfil > fill + 0.002){
          c.fillStyle = "#FFE9C0"; c.globalAlpha = 0.85;
          const a = cx0 + sign * cw * fill, b = cx0 + sign * cw * gfil;
          c.fillRect(Math.min(a, b), cy0, Math.abs(b - a), ch);
          c.globalAlpha = 1;
        }
        if (fill <= 0.001) continue;
        /* Affinity colour, because the first job of this half is to say WHICH
           RELIC. The stage rides as VALUE, never hue -- as on the shell. */
        c.globalAlpha = al;
        const gx = c.createLinearGradient(cx0, cy0, cx0 + sign * cw, cy0 + ch);
        gx.addColorStop(0, f.aff.dark);
        gx.addColorStop(1, (brink || SS.puls) ? SS.hi : f.aff.core);
        c.fillStyle = gx;
        c.fillRect(Math.min(cx0, cx0 + sign * cw * fill), cy0, cw * fill, ch);
        c.globalAlpha = 1;
      }

      /* the head */
      if (fr > 0.001){
        const whole = Math.floor(Math.min(fr * NCH, NCH - 1e-6));
        const head = ex + sign * (whole * (cw + GAPX) + cw * (fr * NCH - whole));
        c.save();
        c.shadowColor = SS.puls ? SS.hi : f.aff.core; c.shadowBlur = 14;
        c.fillStyle = "#FFF4D0";
        c.fillRect(head - 2.5, cy0 - 4, 5, ch + 8);
        c.restore();
      }

      /* name at the outer edge, percentage at the inner one */
      c.save();
      c.textBaseline = "alphabetic";
      c.textAlign = sign > 0 ? "left" : "right";
      c.font = "700 27px ui-serif,Georgia,serif";
      c.fillStyle = "#07050C"; c.strokeStyle = "#07050C";
      c.lineWidth = 5; c.lineJoin = "round";
      c.strokeText(f.w.name.toUpperCase(), ex + sign * 8, y + 21);
      c.fillStyle = f.aff.core;
      c.fillText(f.w.name.toUpperCase(), ex + sign * 8, y + 21);
      if (TUG.pct || TUG.num){
        const txt = TUG.pct ? Math.round(fr * 100) + "%"
                            : String(Math.max(0, Math.round(f.hp)));
        c.textAlign = sign > 0 ? "right" : "left";
        c.font = "800 30px ui-sans-serif,system-ui,sans-serif";
        c.strokeText(txt, mid - sign * 14, y + 22);
        c.fillStyle = (brink || SS.puls) ? SS.hi : "#EDE3D0";
        c.fillText(txt, mid - sign * 14, y + 22);
      }
      c.restore();
    }
    /* the axis the two halves are compared about */
    c.strokeStyle = "#6E6378"; c.lineWidth = 2;
    c.beginPath(); c.moveTo(mid, y + 4); c.lineTo(mid, y + h - 4); c.stroke();
    c.restore();
  }

"""


# --------------------------------------------------------------------- go --
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", default="../02-chain/sc-health.html")
    ap.add_argument("--mode", choices=("mirror", "ratio"), default="mirror")
    ap.add_argument("--hud", choices=("top", "bottom"), default="top")
    ap.add_argument("--fonts", default=str(pathlib.Path(__file__).parent / "fonts"),
                    help="dir holding the two .woff2 files (or a node_modules tree)")
    ap.add_argument("--num", action="store_true",
                    help="print the two HP values on the lifeline")
    ap.add_argument("--no-tug", action="store_true",
                    help="build A and F only, leaving the frame alone")
    a = ap.parse_args()

    src_p, out_p = pathlib.Path(a.src), pathlib.Path(a.out)
    if out_p.name in PROTECTED:
        sys.exit(f"! refusing to write {out_p.name}: that file is verified")
    if not src_p.exists():
        sys.exit(f"! missing {src_p}")
    s = src_p.read_text(encoding="utf-8")
    print(f"=== HEALTH v4  {src_p.name} "
          f"({hashlib.sha256(s.encode()).hexdigest()[:16]}) ===")

    cfg = (CONFIG_JS.replace('const BAND = { pos: "top" }', f'const BAND = {{ pos: "{a.hud}" }}')
                    .replace('mode: "mirror"', f'mode: "{a.mode}"')
                    .replace("num: false", f"num: {'true' if a.num else 'false'}")
                    .replace("on: true", f"on: {'false' if a.no_tug else 'true'}"))
    # fonts first: the @font-face block goes in before anything measures text
    s = insert_before(s, "<title>", font_css(pathlib.Path(a.fonts)), "fontface")
    s = insert_before(s, "window.AC = {", FONT_GATE, "fontgate")
    # `arenaTop` is computed once in the constructor, so a live flip of BAND.pos
    # would move the band and leave the hall where it was. Refresh it per frame
    # -- one comparison, and it makes the flag A/B-able in the console.
    s = s.replace("    SHAPES._t = m.t;",
                  "    SHAPES._t = m.t;\n"
                  "    this.arenaTop = BAND.pos === \"bottom\" ? 20 : this.hud + 24;")
    s = s.replace("    this.arenaTop = this.hud + 24;",
                  "    this.arenaTop = BAND.pos === \"bottom\" ? 20 : this.hud + 24;")
    s = s.replace("    const y = this.arenaTop + this.ah + 46;",
                  "    const y = BAND.pos === \"bottom\" ? this.H - 18\n"
                  "                                    : this.arenaTop + this.ah + 46;")
    s = insert_before(s, "const AFFINITIES = {", cfg, "config")
    s = insert_before(s, "const AFFINITIES = {", SIG_JS, "sigils")

    s = replace_span(
        s,
        "    /* --- the health ring, wrapped inside the shell ---------------------",
        "    if (f.stun > 0){                                   // staggered",
        GAUGE_JS, "gauge")

    # drawHud, drawBar and drawTug are replaced together: the relic names move
    # OUT of the two HUD rows and INTO the lifeline, which collapses the band to
    # one mirrored ult row and lets the bar be 56px tall. `this.hud` does not
    # move, so no layout constant changes and nothing can force a retune.
    s = replace_span(s, "  drawHud(m){", "  drawClock(m){", HUD_JS, "hud+bar+tug")
    s = insert_before(s, "    if (m.over) this.drawResult(m);",
                      "    this.drawTug(m);\n", "call")

    # The font rewrite runs LAST, after every insert above. Run against the
    # source first -- which is where it was, and it shipped one build that way
    # -- it cleans the file and then this builder pastes its own blocks in
    # still carrying `ui-serif,Georgia,serif`. Half the HUD came out in the
    # fallback face and the stale-token check passed, because at the moment it
    # ran the stale tokens genuinely were not there yet.
    n = 0
    for old, new in FONT_MAP:
        n += s.count(old); s = s.replace(old, new)
    print(f"  fonts      {n} font stacks rewritten to Atkinson")
    for stale in ("system-ui", "Georgia", "Menlo", "SFMono", "ui-serif", "ui-sans-serif"):
        if stale in s:
            sys.exit(f"! post-check: '{stale}' survived the font rewrite")

    # Post-checks. Presence and uniqueness of the things the edits DECLARE --
    # a builder that silently produced a file missing one of its own three
    # features would otherwise look identical to a successful run.
    must_be_unique = ["const HEALTH_CHUNKS", "const BRINK", "const TUG",
                      "const BAND = {",
                      "const ULTSIG", "const ULTBAR", "_ultSigil(m, f, x, y, r, cf, hot){",
                      "const rr = R * 0.86", "const GA0", "drawTug(m){",
                      "this.drawTug(m);", "drawBar(m, f, y, side){",
                      "drawHud(m){"]
    for name in must_be_unique:
        got = s.count(name)
        if got != 1:
            sys.exit(f"! post-check: '{name}' appears {got}x, expected 1")
    # and nothing may survive from the block that was replaced
    for gone in ["const rr = R * 0.80", "this.drawBar(m, m.b, 86)"]:
        if gone in s:
            sys.exit(f"! post-check: '{gone}' survived the replacement")
    # every relic must have its OWN sigil -- rule 9, enforced rather than hoped
            #
    ids = re.findall(r'\{ id:"([a-z]+)"', s)
    sig = s[s.index("const ULTSIG = {"):]
    sig = sig[:sig.index("\n};")]
    missing = [i for i in ids if f"\n  {i}(c, t, cf, P){{" not in sig]
    if missing:
        sys.exit(f"! post-check: {len(missing)} relics have no sigil: {missing}")
    print(f"  post-check  {len(must_be_unique)} unique declarations, 2 removals, "
          f"{len(ids)}/{len(ids)} relics have their own sigil")

    out_p.write_text(s, encoding="utf-8")
    print(f"\n  -> {out_p}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"  ({len(s)} chars, {len(s)-len(src_p.read_text(encoding='utf-8')):+d})")
    print(f"     TUG.mode={a.mode}  TUG.num={a.num}  TUG.on={not a.no_tug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
