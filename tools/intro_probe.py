#!/usr/bin/env python3
"""Falsify the fight card v2, then film it.

    python3 intro_probe.py --src sundered-crown.html --out sc-intro.html

Four checks, each aimed at a specific way this change could lie:

  [1] ENGINE A/B. introT is presentation-only by contract; prove it anyway.
      AC.simulate over pinned seeds on both files must match field for field.

  [2] REVEAL CONTINUITY. The whole point of the reveal is that there is no
      cut: the last frame of the intro must BE the first frame of the fight.
      Asserted as pixels — mean |diff| between the frame at introT=epsilon
      and the frame at introT=0, same match, must be ~0.

  [3] NO BLACK RECTANGLE — and the check must fail on the build it replaces.
      At the first card frame the hall must already be visible behind the
      scrim. Measured as the fraction of lit pixels mid-frame; the same
      measurement is taken on the LAST BUILD WITHOUT A CARD, where the old
      solid fill must score near zero. A probe that cannot fail is comparing
      nothing — and once the card is in the baseline, --src IS a card build
      and the differential is structurally unfailable, which is exactly the
      state this check was written to prevent. Pass --pre with the last
      pre-card build (sc-c2.html) on any hop that only re-lays-out the card;
      it defaults to --src for the hop that first introduced it.

  [4] THE TAPE EXISTS. Mid-hold, the tape band must differ hard from the
      bare scene — numbers and bars are ink, and ink is measurable.

  [5] NOTHING CLIPS THE FRAME. The first edge-pairs sheet shipped "ANY"
      cut off at the frame edge, so now it is a measurement: at rebound,
      hold and late-hold phases (cards at rest — entrance/exit legitimately
      cross the top and bottom borders), no bright ink may sit within 6px
      of any frame edge, across melee, ranged and self-status pairings.

Then the part no assert can do: a filmstrip and a GIF at phone size, because
the law is WATCH IT and a still passes checks that motion fails.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).parent

PAIRINGS = [("dawnbringer", "grudgebearer"),
            ("gravemourn", "thornwake"),
            ("ironhail", "spellbreaker")]
N_SEEDS = 40
SEED0 = 20260814

SIM_JS = """([pairs, n, seed0]) => {
  const out = [];
  for (const [a, b] of pairs)
    for (let i = 0; i < n; i++)
      out.push(AC.simulate(a, b, (seed0 + i * 7919) >>> 0));
  return JSON.stringify(out);
}"""

# Draw the card at a given elapsed time on a pinned match and return coarse
# pixel stats plus (optionally) the PNG. Sampling every 3rd pixel keeps the
# transfer sane; the stats are computed in-page.
FRAME_JS = """([a, b, seed, e, wantPng]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject(m);
  m.introT = e === null ? 0 : Math.max(0, AC.CONFIG.intro.dur - e);
  AC.__draw(m);
  const cv = document.getElementById('cv');
  const d = cv.getContext('2d').getImageData(0, 0, 1080, 1920).data;
  let lit = 0, n = 0;
  for (let i = 0; i < d.length; i += 12){        // every 3rd pixel
    const l = 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
    if (l > 18) lit++;
    n++;
  }
  return { lit: lit / n,
           png: wantPng ? cv.toDataURL('image/png').slice(22) : null };
}"""

# Bright ink within `pad` px of the frame edge, at a given elapsed time.
# The scene behind the 80% scrim cannot exceed ~lum 55, so lum > 60 is card
# ink by construction.
EDGE_JS = """([a, b, seed, e, pad]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject(m);
  m.introT = Math.max(0, AC.CONFIG.intro.dur - e);
  AC.__draw(m);
  const cx = document.getElementById('cv').getContext('2d');
  let hits = 0;
  const scan = (x, y, w, h) => {
    const d = cx.getImageData(x, y, w, h).data;
    for (let i = 0; i < d.length; i += 4){
      const l = 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
      if (l > 60) hits++;
    }
  };
  scan(0, 0, 1080, pad); scan(0, 1920 - pad, 1080, pad);
  /* the seam band (y 860-1060) is excluded on the sides: the impact flash
     is a deliberate full-bleed beam along the collision line */
  scan(0, 0, pad, 860); scan(0, 1060, pad, 860);
  scan(1080 - pad, 0, pad, 860); scan(1080 - pad, 1060, pad, 860);
  return hits;
}"""

# Mean |diff| between two draws of the same pinned match, computed in-page.
DIFF_JS = """([a, b, seed, e1, e2, y0, y1]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const cv = document.getElementById('cv'), cx = cv.getContext('2d');
  const grab = (e) => {
    const m = new AC.Match(a, b, seed);
    AC.__inject(m);
    m.introT = e === null ? 0 : Math.max(0, AC.CONFIG.intro.dur - e);
    AC.__draw(m);
    return cx.getImageData(0, y0, 1080, y1 - y0).data;
  };
  const d1 = grab(e1), d2 = grab(e2);
  let s = 0, n = 0;
  for (let i = 0; i < d1.length; i += 8){
    s += Math.abs(d1[i] - d2[i]); n++;
  }
  return s / n;
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sundered-crown.html")
    ap.add_argument("--out", default="sc-intro.html")
    ap.add_argument("--pre", default=None,
                    help="the last build with NO fight card, for [3]'s "
                         "differential arm; defaults to --src")
    ap.add_argument("--no-film", action="store_true")
    a = ap.parse_args()
    src, out = HERE / a.src, HERE / a.out
    fails = 0

    def check(ok, name, detail=""):
        nonlocal fails
        if not ok:
            fails += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" +
              (f"  — {detail}" if detail else ""))

    # ---- [1] engine A/B -----------------------------------------------------
    sims = {}
    for path in (src, out):
        with game(game_path=path.resolve()) as (pg, errs):
            sims[path.name] = pg.evaluate(SIM_JS, [PAIRINGS, N_SEEDS, SEED0])
            assert not errs, (path.name, errs)
    n_total = len(PAIRINGS) * N_SEEDS
    check(sims[src.name] == sims[out.name],
          f"[1] engine A/B — {n_total} matches identical field for field")

    # ---- [2][3][4] pixels, on the patched build -----------------------------
    with game(game_path=out.resolve()) as (pg, errs):
        # [2] reveal continuity: introT=epsilon vs introT=0, whole frame
        d = pg.evaluate(DIFF_JS, ["dawnbringer", "grudgebearer", 4242,
                                  3.9999, None, 0, 1920])
        check(d < 0.5, "[2] reveal continuity — last intro frame IS the fight",
              f"mean |diff| {d:.3f} (limit 0.5)")

        # [3] the hall is visible behind the scrim on the FIRST card frame
        lit_out = pg.evaluate(FRAME_JS, ["dawnbringer", "grudgebearer", 4242,
                                         0.02, False])["lit"]
        # [4] the tape band mid-hold vs the bare scene
        d_tape = pg.evaluate(DIFF_JS, ["dawnbringer", "grudgebearer", 4242,
                                       2.2, None, 800, 1300])
        check(d_tape > 8.0, "[4] the tape exists — mid-hold band differs from "
              "the bare scene", f"mean |diff| {d_tape:.1f} (floor 8.0)")

        # [6] the in-battle popup reminders fit the new language: the
        # first-landing explainer panel prints "NAME — tip" at 25px inside a
        # 596-wide card (30px pads), so every STATUS tip must measure ≤536.
        bad_tips = pg.evaluate("""() => {
          const c2 = document.createElement('canvas').getContext('2d');
          c2.font = "500 25px ui-sans-serif,system-ui,sans-serif";
          const bad = [];
          for (const [k, s] of Object.entries(AC.STATUS))
            if (s.tip && c2.measureText(s.tip).width > 536)
              bad.push(k + ": " + Math.round(c2.measureText(s.tip).width) + "px");
          return bad;
        }""")
        check(not bad_tips, "[6] every tip fits the in-arena explainer panel",
              ", ".join(bad_tips) if bad_tips else "8 tips ≤ 536px at 25px")

        # [5] frame-edge clip audit, cards at rest
        clip = 0
        for pa, pb in [("dawnbringer", "grudgebearer"), ("ironhail", "lightkeeper"),
                       ("gravemourn", "thornwake"), ("farwarden", "widowmaker")]:
            for e in (0.55, 1.2, 2.2, 3.3):
                clip += pg.evaluate(EDGE_JS, [pa, pb, 4242, e, 6])
        check(clip == 0, "[5] nothing clips the frame — 4 pairings x 4 phases",
              f"{clip} bright edge pixels")
        assert not errs, errs

    # [3] continued: the same measurement must FAIL on a build with no card
    pre = (HERE / a.pre) if a.pre else src
    with game(game_path=pre.resolve()) as (pg, errs):
        lit_src = pg.evaluate(FRAME_JS, ["dawnbringer", "grudgebearer", 4242,
                                         0.02, False])["lit"]
        assert not errs, errs
    check(lit_out > 0.02 and lit_out > 4 * lit_src,
          "[3] no black rectangle — hall visible at first card frame, and the "
          "no-card build fails this same check",
          f"lit: out {lit_out:.4f} vs {pre.name} {lit_src:.4f}")

    if a.no_film:
        return 1 if fails else 0

    # ---- the filmstrip and the GIF, at phone size ---------------------------
    from PIL import Image
    frames_e = [0.06, 0.22, 0.38, 0.46, 0.55, 0.75, 1.20, 2.20,
                3.30, 3.60, 3.80, 3.97]
    stills = []
    with game(game_path=out.resolve()) as (pg, errs):
        for e in frames_e:
            r = pg.evaluate(FRAME_JS, ["gravemourn", "thornwake", 4242, e, True])
            stills.append((e, Image.open(io.BytesIO(
                base64.b64decode(r["png"]))).convert("RGB")))
        # GIF: the whole card at 12.5 fps, then a second of the real fight,
        # so the reveal is judged as a TRANSITION rather than a still
        gif = []
        e = 0.0
        while e < 4.0:
            r = pg.evaluate(FRAME_JS, ["gravemourn", "thornwake", 4242, e, True])
            gif.append(Image.open(io.BytesIO(
                base64.b64decode(r["png"]))).convert("RGB"))
            e += 0.08
        png = pg.evaluate("""() => {
          const frames = [];
          const m = new AC.Match('gravemourn', 'thornwake', 4242);
          AC.__inject(m); m.introT = 0;
          for (let f = 0; f < 14; f++){
            for (let s = 0; s < 10; s++) m.step(AC.CONFIG.physics.dt);
            AC.__draw(m);
            frames.push(document.getElementById('cv')
                        .toDataURL('image/png').slice(22));
          }
          return frames;
        }""")
        for p in png:
            gif.append(Image.open(io.BytesIO(base64.b64decode(p))).convert("RGB"))
        assert not errs, errs

    W = 340  # phone-ish width per cell
    cols, rows = 4, 3
    cell = (W, W * 16 // 9)
    sheet = Image.new("RGB", (cols * cell[0], rows * cell[1]), (10, 8, 16))
    for i, (e, im) in enumerate(stills):
        sheet.paste(im.resize(cell), ((i % cols) * cell[0], (i // cols) * cell[1]))
    sheet.save(HERE / "intro-filmstrip.png")
    gif = [im.resize((324, 576)) for im in gif]
    gif[0].save(HERE / "intro-preview.gif", save_all=True,
                append_images=gif[1:], duration=80, loop=0)
    print(f"  intro-filmstrip.png ({len(stills)} stills) · intro-preview.gif "
          f"({len(gif)} frames)")

    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
