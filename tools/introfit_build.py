#!/usr/bin/env python3
"""THE FIGHT CARD v3 — the legibility pass.  Rick, 2026-08-15:

    "They're pretty hard to read especially on mobile.  All of the info is
     scrunched at the bottom and a lot of leftover space is being unused.
     Make the text more legible and use more of its available space.  Also
     separate the status effect text from the ult text a bit."

Three changes, and every one of them is about the phone.  The canvas is
1080 wide and a phone renders it about 390pt across, so the card is drawn
at roughly 0.36x: v2's 25px tip is a 9pt glyph in the hand, and the two
longest ult tips were not even 25px — the shrink-to-fit guard quietly took
them to 19px, which is 7pt.  The smallest type on the card was attached to
its most important fact.

  1. THE CARD IS FILLED.  v2 bottom-anchored the facts (`yy = y0 + CH - 22
     - sum(heights)`), so a 560px card carried its content in the bottom
     ~240 and left the rest empty.  The facts now start under a header rule
     and the slack is SPENT: panels stretch (capped at +46 so a two-fact
     card does not turn into two slabs) and whatever is left widens the
     gaps.  Card height 560 -> 574 by moving the frame margin 118 -> 104,
     which is free: the tape between the cards keeps its exact 678..1242
     band, so nothing in _introTape moves.

  2. THE TYPE IS BIGGER, AND IT WRAPS.  Tips 25 -> 30px, names 31 -> 36,
     tags 19 -> 20, school 24 -> 25, tape labels 23 -> 27, HP line 22 -> 26.
     Tips now WRAP to a second line instead of shrinking; shrink survives
     only as the last resort for a string no break can fit (a 20px floor).
     The ultimate's "· 16s cooldown" tail is gone from the sentence and is
     now a right-aligned chip on the name row — it was stealing the width
     that forced the shrink in the first place.

  3. STATUS AND ULTIMATE ARE DIFFERENT OBJECTS.  v2 printed them as four
     identical left-aligned rows and the eye could not tell where one fact
     ended.  Each is now a panel with its own tinted ground and accent rail:
     the status in the fighter's school colour, the ultimate in gold with a
     lit border and the cooldown chip.  The gap above the ultimate (28) is
     twice the gap above the status (14), so the grouping is spatial as well
     as chromatic.  TRUESTRIKE drops to a one-line strip — it is a class
     property, not a headline, and the hierarchy should say so.

Layout is factored so it can be falsified without pixels: `_introFacts(f)`
builds the descriptors and wraps the tips, `_introLayout(facts, top, bot)`
assigns y/h and reports whether it fits.  introfit_probe.py calls both for
all 16 relics rather than trusting three screenshots.

    python3 introfit_build.py --src sc-daybreak.html --out sc-introfit.html

Anchored string edits, each anchor must hit exactly once.  Refuses to write
sundered-crown.html; stamps its output GENERATED.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent

# --------------------------------------------------------------------------
# the new card, verbatim
# --------------------------------------------------------------------------

CARD = r'''  /* One fighter's card, v3 (2026-08-15): identity, silhouette, and its facts
     laid out to FILL the card instead of pooling at its foot.  See
     introfit_build.py for the full rationale; the short version is that the
     phone draws this at ~0.36x, so v2's 25px tip was a 9pt glyph and its two
     longest ult tips were shrink-to-fit 19px — 7pt — on the most important
     line of the card.

     Facts are descriptors from `_introFacts` and positions from
     `_introLayout`; this function only draws them, which is what lets
     introfit_probe.py check every relic's layout without a screenshot.
     All values still read live from WEAPONS/STATUS/CONFIG at draw time, and
     relicStatus/relicShot remain the single source verify.py's legibility
     contract calls. */
  _introCard(f, y0, CH, imp, fade){
    if (y0 < -CH - 20 || y0 > this.H + 20) return;
    const c = this.ctx, pal = f.aff, x = 40, w = this.W - 80;
    c.save();
    c.globalAlpha = fade;
    c.fillStyle = "#0C0914F4";
    this.roundRect(x, y0, w, CH, 12); c.fill();
    c.strokeStyle = pal.core + "55"; c.lineWidth = 2;
    this.roundRect(x, y0, w, CH, 12); c.stroke();
    c.fillStyle = pal.core;
    this.roundRect(x, y0, 9, CH, 5); c.fill();

    c.textAlign = "left";
    c.font = "700 64px ui-serif,Georgia,serif";
    c.fillStyle = "#EDE3D0";
    c.fillText(f.w.name.toUpperCase(), IC.tx, y0 + 88);
    c.font = "700 25px ui-sans-serif,system-ui,sans-serif";
    c.fillStyle = pal.core;
    c.fillText(f.aff.name.toUpperCase(), IC.tx + 2, y0 + 128);

    /* the weapon, fitted to the header band's art box.  v2 drew every
       silhouette at a single scale:2.2, which made the greatswords overrun
       the band and the twinblades a speck.  The box is fixed, the scale is
       whatever makes THIS weapon fill it (_artBox measures the shape rather
       than trusting its `reach`), so the art can no longer leave the card. */
    const box = this._artBox(f.w);
    const as = Math.min(IC.artMaxS, IC.artW / box.w, IC.artH / box.h);
    c.save();
    c.translate(IC.artCX - as * (box.x + box.w / 2),
                y0 + IC.artCY - as * (box.y + box.h / 2));
    c.scale(as, as);
    c.rotate(-0.38);
    c.shadowColor = pal.core; c.shadowBlur = 26;
    this._artShape(c, f.w, pal);
    c.restore();

    /* the rule that closes the header and opens the facts */
    c.globalAlpha = fade * 0.5;
    c.fillStyle = "#6E6378";
    c.fillRect(IC.px, y0 + IC.ruleY, IC.pw, 1);
    c.globalAlpha = fade;

    const facts = this._introFacts(f);
    this._introLayout(facts, y0 + IC.top, y0 + CH - IC.bot);

    facts.forEach((r, i) => {
      /* cascade: each fact lands a beat after the last, after the impact */
      const a = clamp((imp - 0.20 - i * 0.09) / 0.22, 0, 1);
      if (a <= 0) return;
      const py = r.y + (1 - a) * 12;
      c.save();
      c.globalAlpha = fade * a;

      if (r.kind === "strip"){
        c.font = "800 25px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = r.col;
        c.fillText(r.name, IC.tx, py + 34);
        const tw = c.measureText(r.name).width + 16;
        c.font = "500 " + r.wrap.size + "px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = "#9C9384";
        c.fillText(r.wrap.lines[0], IC.tx + tw, py + 34);
        c.restore();
        return;
      }

      /* the ground: a tint of the fact's own colour, so the status reads as
         the fighter's and the ultimate reads as gold before a word is read */
      c.globalAlpha = fade * a * r.tintA;
      c.fillStyle = r.tint;
      this.roundRect(IC.px, py, IC.pw, r.h, 10); c.fill();
      c.globalAlpha = fade * a;
      if (r.edge){
        c.strokeStyle = r.edge; c.lineWidth = 1.5;
        this.roundRect(IC.px, py, IC.pw, r.h, 10); c.stroke();
      }
      c.fillStyle = r.rail;
      this.roundRect(IC.px, py + 9, 5, r.h - 18, 2.5); c.fill();

      const t0 = py + (r.h - r.contentH) / 2;
      c.font = "700 20px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = r.tagCol;
      c.fillText(r.tag, IC.tx, t0 + 30);
      const tw = c.measureText(r.tag).width + 16;
      c.font = "800 36px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = r.col;
      c.fillText(r.name, IC.tx + tw, t0 + 30);
      if (r.chip){
        c.textAlign = "right";
        c.font = "700 22px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = "#8A7F70";
        c.fillText(r.chip, IC.txr, t0 + 28);
        c.textAlign = "left";
      }
      c.font = "500 " + r.wrap.size + "px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = r.ink;
      for (let j = 0; j < r.wrap.lines.length; j++)
        c.fillText(r.wrap.lines[j], IC.tx, t0 + 70 + j * 38);
      c.restore();
    });
    c.restore();
  }

  /* The silhouette, drawn identically for the card and for the measurement
     below — one function, so a bbox can never disagree with what is drawn. */
  _artShape(c, w, pal){
    if (w.shape === "flail"){
      /* the same bowed chain it has in the arena, so the card shows the
         viewer the thing they are about to watch */
      const L = w.reach * 0.50;
      c.strokeStyle = "#6B6270"; c.lineWidth = w.width * 0.20; c.lineCap = "round";
      c.beginPath(); c.moveTo(-26, 0); c.quadraticCurveTo(L*0.5, 17, L, 0); c.stroke();
      c.fillStyle = "#9A93A4";
      for (let i = 1; i <= 8; i++){
        const t = i / 9, u = 1 - t;
        c.beginPath();
        c.arc(u*u*-26 + 2*u*t*(L*0.5) + t*t*L, 2*u*t*17, w.width * 0.13, 0, TAU);
        c.fill();
      }
      c.translate(L, 0);
      SHAPES.flailHead(c, w.artW, pal, 0.5);
    } else {
      const fn = SHAPES[w.shape];
      if (fn) fn(c, w.reach * 0.86, w.artW, pal);
    }
  }

  /* A shape's true extent, in the card's rotated frame, measured once per
     weapon and cached.  The shapes are drawing code, not geometry — reach
     and artW predict a greatsword's box and lie about a bow's — so the only
     honest way to fit one to a box is to rasterise it and look.  One 200px
     offscreen pass per weapon per page (~0.5ms), never during the fight. */
  _artBox(w){
    let b = ART_BOX.get(w.id);
    if (b) return b;
    /* Scanned every 2nd pixel and then padded by the step, so the box can
       only ever be too GENEROUS — an under-report would let art out of the
       card, which is the bug this whole function exists to prevent.  If the
       ink reaches the scratch canvas edge the shape outgrew the scratch and
       the box would be a lie, so the canvas doubles and it measures again
       rather than returning a clipped answer. */
    const STEP = 2;
    for (let N = 200; N <= 800; N *= 2){
      const OX = N * 0.26, OY = N * 0.59;   // room for the -0.38 rotation
      const cv = document.createElement("canvas");
      cv.width = N; cv.height = N;
      const c = cv.getContext("2d");
      c.translate(OX, OY); c.rotate(-0.38);
      this._artShape(c, w, AFFINITIES[w.aff] || w.aff);
      const d = c.getImageData(0, 0, N, N).data;
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      for (let y = 0; y < N; y += STEP)
        for (let x = 0; x < N; x += STEP)
          if (d[(y * N + x) * 4 + 3] > 12){
            if (x < x0) x0 = x;
            if (x > x1) x1 = x;
            if (y < y0) y0 = y;
            if (y > y1) y1 = y;
          }
      if (x1 < x0){ b = { x: -1, y: -1, w: 2, h: 2 }; break; }
      x0 -= STEP; y0 -= STEP; x1 += STEP; y1 += STEP;
      if (x0 > 0 && y0 > 0 && x1 < N - 1 && y1 < N - 1){
        b = { x: x0 - OX, y: y0 - OY, w: x1 - x0, h: y1 - y0 };
        break;
      }
    }
    if (!b) b = { x: -1, y: -1, w: 2, h: 2 };
    ART_BOX.set(w.id, b);
    return b;
  }

  /* The facts, as data.  Rick 08-14: no SHOOTS line (the silhouette and the
     ANY reach already say it); swing relics say they TRACK; the ultimate
     reads ULTIMATE > name > what it does with numbers > cooldown.  v3 moves
     the cooldown off the sentence and onto its own chip, and drops
     TRUESTRIKE to a strip — it is a class property, not a headline. */
  _introFacts(f){
    const pal = f.aff, out = [];
    const tipw = IC.txr - IC.tx;
    if (f.w.mode === "swing")
      out.push({ kind: "strip", name: "TRUESTRIKE",
                 tip: "Swords track their target instead of rotating",
                 col: pal.glow, gapBefore: 0, h: 52 });
    const rs = relicStatus(f.w);
    if (rs.def){
      /* ON HIT for self-statuses too — ward is banked by landing hits.  The
         +n is suppressed when the status cannot stack (ward maxStacks:1 —
         its onSelf value is a banking-rate multiplier, not a stack count). */
      const n = (f.w.onHit && f.w.onHit[rs.key]) ||
                (f.w.onSelf && f.w.onSelf[rs.key]) || 1;
      const cnt = rs.def.maxStacks > 1 ? "+" + n + " " : "";
      out.push({ kind: "panel", tag: "ON HIT",
                 name: (rs.self ? "GAIN " : "") + cnt + rs.def.name.toUpperCase(),
                 tip: rs.def.tip, col: pal.core, tagCol: "#7E7263",
                 ink: "#C6BBA6", rail: pal.core, tint: pal.core, tintA: 0.10,
                 edge: null, chip: null, gapBefore: 14 });
    }
    out.push({ kind: "panel", tag: "ULTIMATE",
               name: f.w.ult.name.toUpperCase(), tip: f.w.ult.tip || "",
               col: "#FFF4D0", tagCol: "#9C8654", ink: "#CFC2A4",
               rail: "#C9A227", tint: "#C9A227", tintA: 0.075,
               edge: "#C9A22740", chip: f.w.ult.charge + "s COOLDOWN",
               gapBefore: 28 });
    for (const r of out){
      r.wrap = this._introWrap(r.tip, r.kind === "strip"
                               ? tipw - 190 : tipw, r.kind === "strip" ? 26 : 30,
                               r.kind === "strip" ? 1 : 2);
      if (r.kind !== "strip"){
        r.contentH = 30 + 8 + 38 * r.wrap.lines.length;
        r.h = r.contentH + 28;
      }
    }
    return out;
  }

  /* Spend the card's spare height on the facts.  Panels stretch first, up to
     IC.stretch each so a two-fact card does not become two slabs, and the
     remainder widens the gaps.  Returns false if the facts do not fit at all
     — introfit_probe.py asserts that never happens on any relic, which is
     the check v2 had no way to write because its layout was inline. */
  _introLayout(facts, top, bot){
    let nat = 0;
    for (let i = 0; i < facts.length; i++)
      nat += facts[i].h + (i ? facts[i].gapBefore : 0);
    let slack = (bot - top) - nat;
    const natSlack = slack;            // headroom BEFORE stretching: the
    const pans = facts.filter(r => r.kind === "panel");   // one that can go
                                                          // negative
    if (slack > 0 && pans.length){
      const per = Math.min(IC.stretch, slack / pans.length);
      for (const r of pans) r.h += per;
      slack -= per * pans.length;
    }
    const nGap = facts.length - 1;
    const extra = slack > 0 && nGap > 0 ? slack / nGap : 0;
    const squash = slack < 0 ? Math.max(0, 1 + slack /
      Math.max(1, facts.slice(1).reduce((s, r) => s + r.gapBefore, 0))) : 1;
    let y = top;
    for (let i = 0; i < facts.length; i++){
      if (i) y += facts[i].gapBefore * squash + extra;
      facts[i].y = y;
      y += facts[i].h;
    }
    return { fits: y <= bot + 0.5, bottom: y, slack: bot - y, natSlack };
  }

  /* Word-wrap for the card's tips.  v2 shrank the face until the string fit
     one line, which made the longest and most important lines the smallest
     type on the card.  This keeps the face and spends a second line; the
     shrink survives only for a string no break can fit, with a 20px floor. */
  _introWrap(text, maxW, size, maxLines){
    const c = this.ctx;
    const words = String(text || "").split(" ");
    for (;;){
      c.font = "500 " + size + "px ui-sans-serif,system-ui,sans-serif";
      const lines = [];
      let cur = "";
      for (const wd of words){
        const t = cur ? cur + " " + wd : wd;
        if (!cur || c.measureText(t).width <= maxW) cur = t;
        else { lines.push(cur); cur = wd; }
      }
      lines.push(cur);
      const over = lines.some(l => c.measureText(l).width > maxW);
      if ((!over && lines.length <= maxLines) || size <= 20)
        return { lines, size, over };
      size -= 1;
    }
  }

'''

# --------------------------------------------------------------------------
# anchors
# --------------------------------------------------------------------------

CARD_START = "  /* One fighter's card: identity, silhouette, and its facts — each fact one"
CARD_END = "  /* The tale of the tape. Pairwise, not roster-normalised: each row scales"

# the card metric block, hung off CONFIG-adjacent module scope so every number
# the layout uses is named in one place rather than sprinkled through draws
IC_CONST = '''/* Fight-card metrics, v3.  One place for every number the card layout uses;
   the frame margin is 104 (was 118) and the card is 574 tall (was 560), which
   is free — the tape between the cards keeps its exact 678..1242 band.
   art* is a BOX, not a scale: every weapon is fitted to it (see _artBox), so
   a twinblade is not a speck next to a greatsword. */
const IC = { margin: 104, ch: 574,
             px: 76, pw: 934, tx: 98, txr: 994,
             ruleY: 176, top: 196, bot: 22, stretch: 46,
             artCX: 866, artCY: 92, artW: 250, artH: 148, artMaxS: 2.4 };
const ART_BOX = new Map();

'''

EDITS = [
    # ---- 1. the card metric block, in front of the renderer class ---------
    ("class Renderer",
     IC_CONST + "class Renderer"),

    # ---- 2. the frame geometry -------------------------------------------
    ("    const CH = 560, restA = 118, restB = this.H - CH - 118;",
     "    const CH = IC.ch, restA = IC.margin, restB = this.H - CH - IC.margin;"),

    # ---- 3. the title, one size up ---------------------------------------
    ('    c.font = "700 26px ui-serif,Georgia,serif";\n'
     '    c.fillStyle = "#5E5140";\n'
     '    c.fillText("SUPER WEAPON BALL: THE SUNDERED CROWN", this.W/2, 66);',
     '    c.font = "700 28px ui-serif,Georgia,serif";\n'
     '    c.fillStyle = "#6B5C48";\n'
     '    c.fillText("SUPER WEAPON BALL: THE SUNDERED CROWN", this.W/2, 62);'),

    # ---- 4. the countdown, clear of the taller card ----------------------
    ("    const bw = 420, bx = (this.W - bw)/2, by = this.H - 86;",
     "    const bw = 420, bx = (this.W - bw)/2, by = this.H - 74;"),

    # ---- 5. IC on the export surface, so the layout can be falsified -----
    ("              newMatch, __inject, SFX, renderer,",
     "              newMatch, __inject, SFX, renderer, IC,"),

    # ---- 6. tape row labels ----------------------------------------------
    ('      c.font = "700 23px ui-sans-serif,system-ui,sans-serif";\n'
     '      c.fillStyle = "#8A7F70";\n'
     '      c.fillText(label, W2, yy + 8);',
     '      c.font = "700 27px ui-sans-serif,system-ui,sans-serif";\n'
     '      c.fillStyle = "#9C8F7E";\n'
     '      c.fillText(label, W2, yy + 8);'),

    # ---- 7. the HP line --------------------------------------------------
    ('      c.font = "500 22px ui-sans-serif,system-ui,sans-serif";\n'
     '      c.fillStyle = "#5E5140";\n'
     '      c.fillText(CONFIG.combat.baseHP + " HP EACH", W2, yy + 4);',
     '      c.font = "600 26px ui-sans-serif,system-ui,sans-serif";\n'
     '      c.fillStyle = "#7E7263";\n'
     '      c.fillText(CONFIG.combat.baseHP + " HP EACH", W2, yy + 4);'),
]

STAMP = ("<!-- GENERATED by introfit_build.py — the fight card v3, the "
         "legibility pass. Edit the builder, not this file. -->\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sc-daybreak.html")
    ap.add_argument("--out", default="sc-introfit.html")
    a = ap.parse_args()
    src, out = HERE / a.src, HERE / a.out
    if out.name in ("sundered-crown.html", "sc-base.html"):
        sys.exit("refusing to write the live line / the chain root")

    t = src.read_text()
    print(f"src {a.src}  {hashlib.sha256(t.encode()).hexdigest()[:16]}")

    # the card body: a span between two unique markers
    for mk in (CARD_START, CARD_END):
        n = t.count(mk)
        if n != 1:
            sys.exit(f"anchor x{n}: {mk[:60]!r}")
    i, j = t.index(CARD_START), t.index(CARD_END)
    if not i < j:
        sys.exit("card markers out of order")
    t = t[:i] + CARD + t[j:]
    print(f"  span   _introCard -> v3           ({j - i} -> {len(CARD)} chars)")

    for old, new in EDITS:
        n = t.count(old)
        if n != 1:
            sys.exit(f"anchor x{n}: {old.splitlines()[0][:70]!r}")
        t = t.replace(old, new, 1)
        print(f"  anchor {old.splitlines()[0].strip()[:64]}")

    if not t.startswith("<!--"):
        t = STAMP + t
    out.write_text(t)
    print(f"out {a.out}  {hashlib.sha256(t.encode()).hexdigest()[:16]}  "
          f"{len(t)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
