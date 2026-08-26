#!/usr/bin/env python3
"""Falsify the fight card v3 — the legibility pass.

    python3 introfit_probe.py --src sc-daybreak.html --out sc-introfit.html

intro_probe.py already guards the four seconds (engine purity, reveal
continuity, the hall behind the scrim, the tape, the frame edges).  This one
guards the CLAIMS THIS CHANGE MAKES, and every check is written so it can
fail on the build it replaces:

  [A] EVERY RELIC FITS.  v2's layout was inline arithmetic inside a draw
      call, so the only way to know a card fit was to look at one.  v3
      factors it into _introFacts/_introLayout, so all 16 relics can be laid
      out and asked.  Fails if any card's facts run past its bottom edge.

  [B] THE TYPE IS ACTUALLY BIGGER.  The point of wrapping was to stop the
      shrink-to-fit guard from taking the longest ult tips to 19px.  Assert
      the smallest tip face rendered across the whole roster, and assert the
      same measurement on --src is SMALLER — a legibility claim that cannot
      distinguish the two builds is not a measurement.

  [C] NOTHING RUNS OUT OF ITS CARD.  Bright ink in the 26px band under the
      top card and the 20px band under the bottom card, over every relic
      paired against a long-tip opponent.  This is the check that caught the
      scythe hanging out of the header band on the first cut.

  [D] THE SPACE IS USED.  Ink coverage in the band y 290-430 — dead air on
      v2 (its facts began at y 434) and the status panel on v3.  Measured on
      BOTH builds; v3 must beat v2 by a wide margin or the change did not do
      the thing it was made to do.

  [E] STATUS AND ULTIMATE ARE SEPARATED.  The gap above the ultimate panel
      must exceed the gap above the status panel, on every relic — the
      spatial half of "make them distinguishable".  (The chromatic half is
      the gold rail and ground, which [F] renders for the eye.)

  [F] THE SHEET.  Every one of the 16 relics as it will actually be seen,
      at phone width, because none of the above can tell you it looks right.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).parent

# Lay out every relic's card and report the numbers the design rests on.
# Runs against the renderer the page actually draws with, not a copy.
LAYOUT_JS = """(hasIC) => {
  AC.setResolution(1080, 1920);
  const R = AC.renderer, out = [];
  for (const w of AC.WEAPONS){
    const other = AC.WEAPONS.find(o => o.id !== w.id).id;
    const m = new AC.Match(w.id, other, 7);
    const f = m.a;
    let rec = { id: w.id, mode: w.mode };
    if (hasIC){
      const IC = AC.IC, y0 = IC.margin;
      const facts = R._introFacts(f);
      const lay = R._introLayout(facts, y0 + IC.top, y0 + IC.ch - IC.bot);
      const box = R._artBox(w);
      const s = Math.min(IC.artMaxS, IC.artW / box.w, IC.artH / box.h);
      const ax0 = IC.artCX - s * box.w / 2, ax1 = IC.artCX + s * box.w / 2;
      const ay0 = IC.artCY - s * box.h / 2, ay1 = IC.artCY + s * box.h / 2;
      const c = R.ctx;
      c.font = "700 64px ui-serif,Georgia,serif";
      const nameW = c.measureText(w.name.toUpperCase()).width;
      rec.fits = lay.fits;
      rec.slack = Math.round(lay.natSlack * 10) / 10;
      rec.tipSizes = facts.map(r => r.wrap.size);
      rec.over = facts.some(r => r.wrap.over);
      rec.gapStatus = facts.length > 1 ? facts[facts.length-2].gapBefore : null;
      rec.gapUlt = facts[facts.length-1].gapBefore;
      rec.nFacts = facts.length;
      rec.art = [Math.round(ax0), Math.round(ax1),
                 Math.round(ay0), Math.round(ay1)];
      rec.artInCard = ax0 > 56 && ax1 < 1024 && ay0 > 6 && ay1 < IC.ruleY - 6;
      rec.nameClear = IC.tx + nameW + 30 < ax0;
    } else {
      /* v2 has no IC and no _introWrap: reproduce its shrink-to-fit so the
         two builds' tip faces are comparable at all. */
      const c = R.ctx;
      const tips = [];
      const rs = AC.relicStatus(w);
      if (w.mode === "swing")
        tips.push("Swords track their target instead of rotating");
      if (rs.def) tips.push(rs.def.tip);
      tips.push((w.ult.tip || "") + " · " + w.ult.charge + "s cooldown");
      rec.tipSizes = tips.map(t => {
        let fs = 25;
        for (;;){
          c.font = "500 " + fs + "px ui-sans-serif,system-ui,sans-serif";
          if (86 + c.measureText(t).width <= 1022 || fs <= 19) break;
          fs -= 1;
        }
        return fs;
      });
    }
    return_stub: out.push(rec);
  }
  return out;
}"""

# Ink (lum > 60 — the scene under the 80% scrim cannot exceed ~55) inside a
# rect, at a pinned elapsed time.  Used for both the overflow bands and the
# dead-air band.
INK_JS = """([a, b, seed, e, rect]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject(m);
  m.introT = Math.max(0.0001, AC.CONFIG.intro.dur - e);
  m.shake = 0;
  AC.__draw(m);
  const cx = document.getElementById('cv').getContext('2d');
  const d = cx.getImageData(rect[0], rect[1], rect[2], rect[3]).data;
  let hit = 0, n = 0;
  for (let i = 0; i < d.length; i += 4){
    const l = 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
    if (l > 60) hit++;
    n++;
  }
  return hit / n;
}"""

CARD_JS = """([a, b, e]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, 4242);
  AC.__inject(m);
  m.introT = Math.max(0.0001, AC.CONFIG.intro.dur - e);
  m.shake = 0;
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png').slice(22);
}"""

# The text column of the top card, on BOTH builds: x stops at 700 because
# v2 parked its silhouette from x716 and that ink is not a fact.  y 280-430
# is dead air on v2 (its first fact line landed at y462) and the status
# panel on v3.
DEAD_BAND = [76, 280, 624, 150]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sc-daybreak.html")
    ap.add_argument("--out", default="sc-introfit.html")
    ap.add_argument("--no-sheet", action="store_true")
    a = ap.parse_args()
    src, out = HERE / a.src, HERE / a.out
    fails = 0

    def check(ok, name, detail=""):
        nonlocal fails
        if not ok:
            fails += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))

    with game(game_path=out.resolve()) as (pg, errs):
        lay = pg.evaluate(LAYOUT_JS, True)

        bad = [r["id"] for r in lay if not r["fits"]]
        check(not bad, "[A] every relic's facts fit inside its card",
              ", ".join(bad) if bad else
              f"{len(lay)}/{len(lay)}, tightest headroom before stretch "
              f"{min(r['slack'] for r in lay):.1f}px")

        over = [r["id"] for r in lay if r["over"]]
        check(not over, "[A] no tip overruns its measured column",
              ", ".join(over) if over else f"{len(lay)}/{len(lay)} wrapped clean")

        art_bad = [r["id"] for r in lay if not r["artInCard"]]
        check(not art_bad, "[A] every silhouette sits inside the header band",
              ", ".join(art_bad) if art_bad else f"{len(lay)}/{len(lay)} fitted")

        name_bad = [r["id"] for r in lay if not r["nameClear"]]
        check(not name_bad, "[A] no name reaches the silhouette",
              ", ".join(name_bad) if name_bad else f"{len(lay)}/{len(lay)} clear by >30px")

        min_out = min(min(r["tipSizes"]) for r in lay)

        gap_bad = [r["id"] for r in lay
                   if r["nFacts"] > 1 and not (r["gapUlt"] > r["gapStatus"])]
        check(not gap_bad, "[E] the ultimate is set apart from the status",
              ", ".join(gap_bad) if gap_bad else
              f"gap above ULTIMATE {lay[0]['gapUlt']} > above ON HIT "
              f"{lay[0]['gapStatus']} on {len(lay)}/{len(lay)}")

        dead_out = pg.evaluate(INK_JS, ["gravemourn", "thornwake", 4242, 2.2,
                                        DEAD_BAND])

        # [C] overflow bands, every relic against a long-tip opponent
        spill = 0
        worst = None
        for r in lay:
            # the opponent carries the longest tip in the game (Reprisal, 70
            # chars) so the OTHER card is always the worst case too
            foil = "farwarden" if r["id"] != "farwarden" else "grudgebearer"
            for band, slot in (([40, 682, 1000, 26], "top"),
                               ([40, 1820, 1000, 20], "bot")):
                pa, pb = (r["id"], foil) if slot == "top" else (foil, r["id"])
                v = pg.evaluate(INK_JS, [pa, pb, 4242, 2.2, band])
                if v > 0:
                    spill += 1
                    worst = f"{r['id']} ({slot}) {v:.4f}"
        check(spill == 0, f"[C] nothing runs out of its card — {len(lay)} relics x 2 slots",
              f"{spill} bands with ink, worst {worst}" if spill else
              f"{2*len(lay)}/{2*len(lay)} bands clean")
        assert not errs, errs

    with game(game_path=src.resolve()) as (pg, errs):
        lay_src = pg.evaluate(LAYOUT_JS, False)
        min_src = min(min(r["tipSizes"]) for r in lay_src)
        dead_src = pg.evaluate(INK_JS, ["gravemourn", "thornwake", 4242, 2.2,
                                        DEAD_BAND])
        assert not errs, errs

    check(min_out >= 26 and min_out > min_src,
          "[B] the smallest tip on the card got bigger",
          f"v3 floor {min_out}px vs v2 floor {min_src}px "
          f"(v2 shrank {sum(1 for r in lay_src for s in r['tipSizes'] if s < 25)}"
          f" tips below 25px)")

    check(dead_out > 6 * dead_src and dead_out > 0.02,
          "[D] the card's dead band is now carrying facts",
          f"ink in the text column y280-430: v3 {dead_out:.4f} vs v2 {dead_src:.4f}")

    if a.no_sheet:
        return 1 if fails else 0

    # ---- [F] look at all sixteen -------------------------------------------
    from PIL import Image
    ids = [r["id"] for r in lay]
    pairs = [(ids[i], ids[(i + 1) % len(ids)]) for i in range(0, len(ids), 2)]
    shots = []
    with game(game_path=out.resolve()) as (pg, errs):
        for pa, pb in pairs:
            shots.append(Image.open(io.BytesIO(base64.b64decode(
                pg.evaluate(CARD_JS, [pa, pb, 2.2])))).convert("RGB"))
        assert not errs, errs
    W = 390
    cell = (W, W * 1920 // 1080)
    sheet = Image.new("RGB", (len(shots) * cell[0], cell[1]), (10, 8, 16))
    for i, im in enumerate(shots):
        sheet.paste(im.resize(cell, Image.LANCZOS), (i * cell[0], 0))
    sheet.save(HERE / "introfit-roster.png")
    print(f"  introfit-roster.png — {len(ids)} relics at phone width")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
