#!/usr/bin/env python3
"""THE PIXEL-IDENTITY TEST `_twinConjured` HAS BEEN WAITING FOR.

    python3 twin_identity.py              # shipped vs the merged candidate
    python3 twin_identity.py --selftest   # prove the test can see a change
    python3 twin_identity.py --diff       # the source difference, normalised
    python3 twin_identity.py --apply      # merge, but ONLY if 0 px differ

WHY
---
`SHAPES._conjure` is the runic grammar, extracted so it can travel.
`SHAPES._twinConjured` is the shape it was extracted FROM, and it still keeps
its own private copy. The in-file note says why:

  > Folding this into `_conjure` would change a shipped, approved silhouette,
  > and no automated check in this project can see a render regression. Merge
  > later, behind a pixel-identity test.

This is that test. It is the deliverable whether or not the merge lands.

WHAT COUNTS AS SUCCESS -- stated before the numbers
---------------------------------------------------
**Zero differing pixels, at every sampled `_t`, at every sampled size.** Not
"visually identical", not "max delta 2". The shape is approved as drawn; a
merge that moves it by one channel on one pixel is a merge that changed the
art, and the whole point of the note is that the art must not move.

The same bar applies to `_gsConjured` and `_whConjured`: the merge touches
shared code, so the two shapes ALREADY riding `_conjure` are rendered before
and after too, and they must not move either. A merge that fixes the twinblade
by moving the greatsword has not passed.

HOW `_t` IS SAMPLED
--------------------
The shape animates on three phases -- `sin(t*2.1)`, `sin(t*1.6)` and the
sigil's `rotate(-t*2.4)`. Their common period is 20*pi, so a single frame
proves nothing: it could agree at t=0 and disagree everywhere else. Default is
16 values evenly spaced over the full common period, plus 4 off-grid values
that no evenly-spaced grid would visit.

THE INSTRUMENT IS VALIDATED FIRST
----------------------------------
Two separate page loads of the SAME file are rendered and compared before any
verdict is reported. If that is not 0 differing pixels, the harness itself is
noisy and every other number here is meaningless -- so the tool refuses to
report rather than blaming the merge for its own noise.
"""
from __future__ import annotations

import argparse
import base64
import io
import math
import pathlib
import re
import sys
import tempfile

import numpy as np
from PIL import Image

from scpage import game

HERE = pathlib.Path(__file__).parent
GAME = "sundered-crown.html"
# The build the twinblade silhouette was approved on, kept so this stays a
# regression test after the merge lands rather than a one-shot.
REFERENCE = "reference/sc-premerge-twin.html"


def resolve(name: str) -> pathlib.Path:
    for cand in (pathlib.Path(name), HERE / name, HERE.parent / name):
        if cand.exists():
            return cand.resolve()
    raise SystemExit(f"cannot find {name}")


# 20*pi is the common period of 2.1, 1.6 and 2.4 (all n/10, gcd 1 over 2*pi).
PERIOD = 20 * math.pi
TS = [PERIOD * k / 16 for k in range(16)] + [0.37, 1.234, 7.5, 41.9]

# (shape, affinity, L, W, scale). The shipped size first -- that is the size
# the art was approved at -- then a 6x blow-up, where a sub-pixel disagreement
# that rounds away at 62x30 becomes several pixels wide.
CONFIGS = [
    ("_twinConjured", "runic", 62, 30, 1.742),
    ("_twinConjured", "runic", 372, 180, 1.0),
    ("_gsConjured", "runic", 116, 40, 1.742),
    ("_whConjured", "runic", 76, 54, 1.742),
]

RENDER_JS = r"""(cfg) => {
  const S = AC.SHAPES;
  const p = AC.AFFINITIES[cfg.aff];
  const cv = document.createElement('canvas');
  cv.width = cfg.cw; cv.height = cfg.ch;
  const c = cv.getContext('2d');
  const out = [];
  for (const t of cfg.ts){
    S._t = t;
    c.setTransform(1,0,0,1,0,0);
    c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
    c.shadowBlur = 0; c.shadowColor = 'transparent';
    c.fillStyle = '#000000'; c.fillRect(0,0,cfg.cw,cfg.ch);
    c.save();
    c.translate(cfg.ox, cfg.oy); c.scale(cfg.s, cfg.s);
    S[cfg.shape](c, cfg.L, cfg.W, p);
    c.restore();
    out.push(cv.toDataURL('image/png').slice(22));
  }
  S._t = 0;
  return out;
}"""


def geom(L, W, s):
    """Canvas big enough for the shape, its glow and its 18px shadow blur."""
    cw = int(L * 1.25 * s + 120)
    ch = int(W * 3.2 * s + 120)
    return cw, ch, 60, ch // 2


def frames(path, cfg, ts):
    shape, aff, L, W, s = cfg
    cw, ch, ox, oy = geom(L, W, s)
    with game(game_path=path) as (pg, errors):
        pngs = pg.evaluate(RENDER_JS, {"shape": shape, "aff": aff, "L": L,
                                       "W": W, "s": s, "cw": cw, "ch": ch,
                                       "ox": ox, "oy": oy, "ts": ts})
        if errors:
            raise SystemExit(f"page errors in {path.name}: " + "; ".join(errors))
    return [np.asarray(Image.open(io.BytesIO(base64.b64decode(x))).convert("RGB"),
                       dtype=np.int16) for x in pngs]


def compare(a_path, b_path, ts, configs, label, *, quiet=False):
    """Return (total_diff_px, worst_channel_delta, rows)."""
    rows, tot, worst = [], 0, 0
    for cfg in configs:
        A = frames(a_path, cfg, ts)
        B = frames(b_path, cfg, ts)
        for t, fa, fb in zip(ts, A, B):
            d = np.abs(fa - fb)
            n = int((d.max(axis=2) > 0).sum())
            m = int(d.max())
            rows.append((cfg[0], cfg[2], cfg[3], t, n, m, fa.shape))
            tot += n
            worst = max(worst, m)
    if not quiet:
        print(f"  {label}")
        print(f"    {'shape':<15}{'size':>10}{'_t':>10}{'px differ':>11}"
              f"{'max delta':>11}")
        for shape, L, W, t, n, m, shp in rows:
            flag = "" if n == 0 else "   <--"
            print(f"    {shape:<15}{f'{L}x{W}':>10}{t:>10.3f}{n:>11d}"
                  f"{m:>11d}{flag}")
        px = sum(r[6][0] * r[6][1] for r in rows)
        print(f"    TOTAL {tot} differing pixels of {px} compared, "
              f"worst channel delta {worst}")
    return tot, worst, rows


# ------------------------------------------------------------------ THE MERGE --
# Three edits. The first two make `_conjure` able to express what
# `_twinConjured` actually draws; both are defaulted to the values `_conjure`
# hardcodes today, so `_gsConjured` and `_whConjured` cannot move.
E_DARK = ('prof(c); c.fillStyle = p.dark; c.fill();               // silhouette',
          'prof(c); c.fillStyle = o.dark || p.dark; c.fill();     // silhouette')
E_TIP = ('c.beginPath(); c.arc(L * 1.02, 0, W * 0.075, 0, TAU); c.fill();',
         'c.beginPath(); c.arc(L * (o.tipX || 1.02), 0, '
         'W * (o.tipR || 0.075), 0, TAU); c.fill();')

MERGED_BODY = '''  _twinConjured(c, L, W, p){
    const gap = L * 0.28, span = L - gap, bw = W * 0.52;
    const prof = (cc) => {
      cc.beginPath();
      cc.moveTo(gap,               -bw * 0.46);
      cc.lineTo(gap + span * 0.16, -bw);
      cc.lineTo(L * 0.97,          -bw * 0.13);
      cc.lineTo(L * 1.03,           0);
      cc.lineTo(L * 0.97,           bw * 0.11);
      cc.lineTo(gap + span * 0.16,  bw * 0.80);
      cc.lineTo(gap,                bw * 0.34);
      cc.closePath();
    };
    SHAPES._conjure(c, L, W, p, { n:5, gap, bw, prof, frac:0.87,
                                  beam:0.055, drift:0.065, cant:0.075,
                                  sigil:0.26, tipX:1.04, tipR:0.085,
                                  dark:"#040814" });
  },'''


def body_span(text, name):
    """Byte range of `  <name>(...){ ... \\n  },` by brace matching."""
    m = re.search(r"^  " + re.escape(name) + r"\(", text, re.M)
    if not m:
        raise SystemExit(f"cannot find {name}")
    i = text.index("{", m.end())
    depth, j = 0, i
    while True:
        ch = text[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    end = text.index(",", j) + 1
    return m.start(), end


def merged_text(text, *, naive=False, keep_comment=True):
    """`naive`: parameters only -- no new options, so the literal and the tip
    silently take `_conjure`'s values. That is the merge someone would write
    without this test, and measuring it is the point."""
    if not naive:
        for old, new in (E_DARK, E_TIP):
            if text.count(old) != 1:
                raise SystemExit(f"anchor found {text.count(old)}x: {old[:48]}")
            text = text.replace(old, new)
    s, e = body_span(text, "_twinConjured")
    body = MERGED_BODY
    if naive:
        body = re.sub(r",\s*\n\s*tipX:1\.04, tipR:0\.085,\s*\n\s*dark:\"#040814\"",
                      "", body).replace("sigil:0.26 })", "sigil:0.26 })")
        body = body.replace("sigil:0.26, tipX:1.04, tipR:0.085,\n"
                            "                                  dark:\"#040814\" });",
                            "sigil:0.26 });")
    head = ""
    if keep_comment:
        head = ("  /* MERGED INTO `_conjure`, 2026-08-14, behind "
                "`tools/twin_identity.py`.\n"
                "     The private copy is gone; the options below are what it "
                "differed by.\n"
                "     `dark`, `tipX` and `tipR` exist so this shape can keep the "
                "exact ink\n"
                "     it shipped with -- they default to what `_conjure` "
                "hardcoded, so\n"
                "     `_gsConjured` and `_whConjured` do not move. 0 differing "
                "pixels at 20\n"
                "     values of `_t` over the full 20*pi common period, at both "
                "sizes. */\n")
    return text[:s] + head + body + text[e:]


PERTURB_ANCHOR = 'blade(); c.fillStyle = "#040814"; c.fill();'


def perturbed(text, kind):
    """Deliberate damage, to show the test is not stuck at 0."""
    if kind == "subpixel":
        old = "c.beginPath(); c.arc(L * 1.04, 0, W * 0.085, 0, TAU); c.fill();"
        new = "c.beginPath(); c.arc(L * 1.0401, 0, W * 0.085, 0, TAU); c.fill();"
    elif kind == "onelsb":
        old = 'blade(); c.fillStyle = "#040814"; c.fill();'
        new = 'blade(); c.fillStyle = "#040815"; c.fill();'
    elif kind == "drift":
        old = "const drift = Math.sin(t * 2.1 + i * 2.3) * W * 0.065;"
        new = "const drift = Math.sin(t * 2.1 + i * 2.3) * W * 0.0651;"
    else:
        raise SystemExit(kind)
    if text.count(old) != 1:
        raise SystemExit(f"perturbation anchor found {text.count(old)}x")
    return text.replace(old, new)


def tmpfile(text, name="sundered-crown.html"):
    out = pathlib.Path(tempfile.mkdtemp()) / name
    out.write_text(text)
    return out


def normalised(text, name):
    """Function body with comments and whitespace stripped, for --diff."""
    s, e = body_span(text, name)
    body = text[s:e]
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    body = re.sub(r"//[^\n]*", "", body)
    return [ln.strip() for ln in body.splitlines() if ln.strip()]


def do_diff(src):
    import difflib
    text = src.read_text()
    a = normalised(text, "_conjure")
    b = normalised(text, "_twinConjured")
    print("== `_conjure` (a) vs `_twinConjured` (b), comments stripped ==")
    for ln in difflib.unified_diff(a, b, "_conjure", "_twinConjured", lineterm="", n=1):
        print("  " + ln)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default=GAME, help="reference build")
    ap.add_argument("--b", default=None,
                    help="candidate build (default: the merge, built here)")
    ap.add_argument("--nt", type=int, default=len(TS),
                    help="how many _t values (>= 8 required)")
    ap.add_argument("--naive", action="store_true",
                    help="merge with parameters only, no new `_conjure` options")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--diff", action="store_true")
    ap.add_argument("--apply", action="store_true",
                    help="write the merge into --a, but only if 0 px differ")
    a = ap.parse_args()

    src = resolve(a.a)
    if a.diff:
        do_diff(src)
        return 0
    if a.nt < 8:
        raise SystemExit("--nt must be >= 8: one frame of an animated shape "
                         "proves nothing")
    ts = TS[:a.nt]
    text = src.read_text()

    # ---- the harness must be silent before it is allowed to accuse anything --
    print("== INSTRUMENT: same file, two page loads ==")
    n, m, _ = compare(src, src, ts[:4], CONFIGS[:2], "shipped vs shipped")
    if n:
        raise SystemExit("the harness is not deterministic across page loads; "
                         "every number below would be noise. Refusing to report.")
    print("  0 differing pixels -- the render is reproducible.\n")

    if a.selftest:
        print("== SELFTEST: can this test see a change? ==")
        # The perturbations name lines from the pre-merge private copy, so once
        # the merge has landed they are applied to the reference build instead.
        base = src if PERTURB_ANCHOR in text else resolve(REFERENCE)
        base_text = base.read_text()
        if base is not src:
            print(f"  (perturbing {REFERENCE}; the merged build no longer "
                  "contains the private copy)")
        ok = True
        for kind, why in [("subpixel", "point moved 0.01% of L"),
                          ("onelsb", "silhouette literal +1 on blue"),
                          ("drift", "drift amplitude +0.15%")]:
            p = tmpfile(perturbed(base_text, kind))
            n, m, _ = compare(base, p, ts, CONFIGS[:2], f"{kind} ({why})",
                              quiet=True)
            seen = n > 0
            ok &= seen
            print(f"  {kind:<10} {why:<34} {n:>7d} px, max delta {m:>3d}"
                  f"   {'SEEN' if seen else '<-- INVISIBLE'}")
        if not ok:
            print("  SELFTEST FAILED: a change the test cannot see means a "
                  "0 from this test means nothing.")
            return 2
        print("  selftest OK: the test is sensitive to sub-pixel geometry and "
              "to 1 LSB of colour.\n")

    if a.b:
        cand = resolve(a.b)
        label = cand.name
    elif E_DARK[0] in text:
        # not merged yet: build the candidate and measure it
        cand = tmpfile(merged_text(text, naive=a.naive))
        label = "MERGED (naive: parameters only)" if a.naive else "MERGED"
    else:
        # already merged: this is now a REGRESSION test against the build the
        # silhouette was approved on. Same bar, opposite direction.
        cand, src = src, resolve(REFERENCE)
        label = "already merged -- vs the pre-merge reference " + REFERENCE
        print(f"   (--a is already merged; comparing against {REFERENCE})")

    print(f"== IDENTITY: shipped vs {label} ==")
    print(f"   {len(ts)} values of _t over the 20*pi common period, "
          f"{len(CONFIGS)} shape/size configs")
    n, m, rows = compare(src, cand, ts, CONFIGS, label)
    print()
    if n == 0:
        print("  VERDICT: BIT-IDENTICAL. 0 differing pixels. The merge may land.")
    else:
        moved = sorted({r[0] for r in rows if r[4]})
        print(f"  VERDICT: NOT IDENTICAL -- {n} differing pixels, max channel "
              f"delta {m}.")
        print(f"           shapes that moved: {', '.join(moved)}")
        print("           The merge must be ABANDONED. A near-identical merge "
              "is a failure here.")

    if a.apply:
        if n:
            print("\n  --apply REFUSED: not bit-identical.")
            return 1
        src.write_text(merged_text(text, naive=a.naive))
        print(f"\n  applied to {src}")
    return 0 if n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
