#!/usr/bin/env python3
"""ULT SET-PIECES FOR THE FOUR NEW GREATSWORDS.

    python3 ultart_build.py --src sc-gs7.html --out sc-gs7-ults.html

WHY THIS IS NEEDED AT ALL
-------------------------
Ultimate MECHANICS dispatch on `u.kind` — nova, beam, bolt, freeze all resolve
in `fireUlt` for any relic. Ultimate ART dispatches on `u.w === "<id>"`, per
relic, bespoke. So a new relic's ultimate works perfectly and **draws nothing**:
damage lands, statuses apply, the banner names it, and the screen is empty.

Ten of sixteen relics are in that state. This does the four new greatswords.
Lightkeeper, Farwarden, Aureole, Censer and Emberedge are still bare and are
NOT touched here — they are a separate decision, not a silent ride-along.

WHAT EACH ONE HAD TO AVOID
--------------------------
Every new ult shares a school with an existing one, and the school palette is
the same, so the risk is four set-pieces that read as recolours of what is
already there. Each is built against its school-mate:

  Bloodprice   vs Exsanguinate (Widowmaker)  — that is a NOVA of fangs thrown
               outward. This is a SEAM: a wound torn open in the air at the
               target, bleeding downward, with the oath drawn as a taut thread
               back to the caster. Outward-radial vs vertical-and-tethered.

  Rootfast     vs Bramblesnare (Thornwake)   — those roots TRAVEL, caster to
               quarry, along the floor. These GROW IN PLACE, erupting upward
               around the target and closing over it, then browning as the
               hold ends. Horizontal-reaching vs vertical-caging.

  Eclipse      vs Dirge (Gravemourn)         — that is a vortex pulling INWARD.
               This pushes a dark disc OUTWARD that subtracts light, with a
               bright corona at its edge. Inward-spiral vs outward-shadow.

  Corollary    vs Unmaking (Spellbreaker)    — that bolt is a JAG, chaotic,
               and it closes a cage. This is a STRAIGHT RULE drawn in discrete
               steps with a glyph stamped at each node, resolving into one
               sigil. Chaos vs construction — the same school arguing two ways.

FRAME COST
----------
Set-pieces are the frame's worst moment and this session measured what a single
full-canvas blur costs. Every `shadowBlur` here is on a small stroke, none
exceeds 20, and the per-branch counts are 3 / 2 / 2 / 4 — at or below the
existing branches (Spellbreaker's Unmaking uses 5, one of them at 26). Nothing
here draws a blurred shape whose bounding box is the canvas.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# --------------------------------------------------------------- UNDER ------
UNDER = r'''
    /* ---- Bloodprice: what runs out of the wound, on the floor -------------- */
    else if (u.w === "oathwound"){
      const open = clamp((u.t - 0.12) / 0.26, 0, 1);
      const fade = 1 - clamp((u.t - 0.6) / 0.85, 0, 1);
      c.globalAlpha = 0.8 * fade * open;
      const g = c.createRadialGradient(u.tx, u.ty + 14, 3, u.tx, u.ty + 14, 108 * open);
      g.addColorStop(0, "#5A0A18EE"); g.addColorStop(0.6, "#3A0610AA");
      g.addColorStop(1, "#3A061000");
      c.fillStyle = g;
      c.beginPath(); c.ellipse(u.tx, u.ty + 14, 108 * open, 46 * open, 0, 0, TAU); c.fill();
      /* rivulets: the pool does not stay a circle */
      for (let i = 0; i < 7; i++){
        const a = shellHash(31, i) * TAU;
        const len = 60 * open * (0.5 + shellHash(32, i));
        c.globalAlpha = 0.6 * fade * open;
        c.strokeStyle = "#5A0A18"; c.lineWidth = 4 - shellHash(33, i) * 2;
        this._jag(c, u.tx, u.ty + 14, u.tx + Math.cos(a) * len,
                  u.ty + 14 + Math.sin(a) * len * 0.42, 5, 7, 340 + i, open);
      }
    }

    /* ---- Rootfast: the root PLATE, spreading from the quarry outward ------- */
    else if (u.w === "heartwood"){
      const grow = clamp(u.t / 0.42, 0, 1);
      const brown = clamp((u.t - u.life * 0.62) / (u.life * 0.38), 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.80) / (u.life * 0.20), 0, 1);
      const N = 11;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + shellHash(71, i) * 0.5;
        const len = 132 * grow * (0.55 + shellHash(72, i) * 0.7);
        c.globalAlpha = 0.85 * fade;
        /* Roots run from the TARGET, not the caster — this is the whole
           difference from Bramblesnare and it has to be visible on the floor
           before the cage above it explains itself. */
        c.strokeStyle = brown > 0 ? "#4A3418" : "#0D3A1A";
        c.lineWidth = 6 - (i % 3);
        this._jag(c, tgt.x, tgt.y, tgt.x + Math.cos(a) * len,
                  tgt.y + Math.sin(a) * len * 0.5, 7, 15, 700 + i, grow);
        c.globalAlpha = 0.5 * fade * (1 - brown);
        c.strokeStyle = "#2E6B2C"; c.lineWidth = 2;
        this._jag(c, tgt.x, tgt.y, tgt.x + Math.cos(a) * len,
                  tgt.y + Math.sin(a) * len * 0.5, 7, 15, 700 + i, grow);
      }
    }

    /* ---- Eclipse: the floor goes out, in a ring running outward ------------ */
    else if (u.w === "nightfell"){
      const ex = clamp(u.t / 0.44, 0, 1);
      const fade = 1 - clamp((u.t - 0.55) / 0.9, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.4));
      c.globalAlpha = 0.9 * fade;
      const g = c.createRadialGradient(u.x, u.y, R * 0.05, u.x, u.y, Math.max(1, R));
      g.addColorStop(0, "#05010AEE"); g.addColorStop(0.72, "#12042099");
      g.addColorStop(0.94, "#2A0A4066"); g.addColorStop(1, "#2A0A4000");
      c.fillStyle = g;
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.fill();
    }

    /* ---- Corollary: the construction lines, ruled on the floor ------------- */
    else if (u.w === "axiom"){
      const draw = clamp(u.t / 0.22, 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 0.8, 0, 1);
      c.globalAlpha = 0.5 * fade;
      c.strokeStyle = "#2A5C9E"; c.lineWidth = 1.2;
      /* Straight, ruled, and extended PAST the target — a construction line,
         not a strike. Nothing here wobbles; that is the point of the school
         arguing against its own twinblade. */
      const dx = tgt.x - u.x, dy = tgt.y - u.y, L = Math.hypot(dx, dy) || 1;
      const ux = dx / L, uy = dy / L;
      c.beginPath();
      c.moveTo(u.x - ux * 40, u.y - uy * 40);
      c.lineTo(u.x + ux * (L + 90) * draw, u.y + uy * (L + 90) * draw);
      c.stroke();
      for (let i = 0; i < 3; i++){
        const rr = 34 + i * 26;
        c.globalAlpha = 0.28 * fade * draw;
        c.beginPath(); c.arc(tgt.x, tgt.y, rr, 0, TAU); c.stroke();
      }
    }
'''

# ---------------------------------------------------------------- OVER ------
OVER = r'''
    /* ---- Bloodprice: a seam torn open in the air, and the oath that holds -- */
    else if (u.w === "oathwound"){
      const open = clamp((u.t - 0.08) / 0.22, 0, 1);
      const shut = clamp((u.t - u.life * 0.55) / (u.life * 0.45), 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 1.0, 0, 1);
      const H = 120, w = 30 * open * (1 - shut);

      /* the wound: a vesica, dark inside, hot at the rim */
      c.save();
      c.translate(u.tx, u.ty);
      c.globalAlpha = Math.max(0, 1 - shut);
      c.beginPath();
      c.moveTo(0, -H);
      c.quadraticCurveTo(w, 0, 0, H);
      c.quadraticCurveTo(-w, 0, 0, -H);
      const wg = c.createLinearGradient(-w, 0, w, 0);
      wg.addColorStop(0, "#3A0610"); wg.addColorStop(0.5, "#120004");
      wg.addColorStop(1, "#3A0610");
      c.fillStyle = wg; c.fill();
      c.strokeStyle = "#FF97A2"; c.lineWidth = 2.6;
      c.shadowColor = "#E03A4E"; c.shadowBlur = 18;
      c.stroke();
      c.shadowBlur = 0;
      c.restore();

      /* it bleeds downward — drops leaving the seam, not thrown outward */
      c.globalCompositeOperation = "source-over";
      for (let i = 0; i < 9; i++){
        const ph = (u.t * 1.3 + shellHash(21, i)) % 1;
        c.globalAlpha = (1 - ph) * fade * 0.9 * open;
        c.fillStyle = "#E03A4E";
        const px = u.tx + (shellHash(22, i) - 0.5) * w * 1.6;
        const py = u.ty - H * 0.3 + ph * (H * 1.5);
        c.beginPath(); c.ellipse(px, py, 2.4, 4.2 + ph * 3, 0, 0, TAU); c.fill();
      }

      /* THE TETHER: a taut thread back to the caster. Straight, not jagged
         — a binding, and the thing Exsanguinate's flung fangs never had.
         (Was "THE OATH" when this relic was Oathwound. The picture did not
         change with the rename; the reason for it did.) */
      c.globalAlpha = 0.75 * fade;
      c.strokeStyle = "#8E1226"; c.lineWidth = 2.4;
      c.shadowColor = "#E03A4E"; c.shadowBlur = 10;
      c.beginPath(); c.moveTo(u.tx, u.ty); c.lineTo(src.x, src.y); c.stroke();
      c.shadowBlur = 0;
      for (let i = 0; i < 3; i++){            // beads running back down it
        const q = (u.t * 0.8 + i / 3) % 1;
        c.globalAlpha = (1 - q) * fade;
        c.fillStyle = "#FF97A2";
        c.beginPath();
        c.arc(lerp(u.tx, src.x, q), lerp(u.ty, src.y, q), 3.2, 0, TAU); c.fill();
      }
    }

    /* ---- Rootfast: a cage grown UP over the quarry, then browning ---------- */
    else if (u.w === "heartwood"){
      const grow = clamp(u.t / 0.40, 0, 1);
      const brown = clamp((u.t - u.life * 0.62) / (u.life * 0.30), 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.78) / (u.life * 0.22), 0, 1);
      const R = CONFIG.physics.ballR;
      const N = 9;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU;
        const h = (R + 78) * grow;
        const bx = tgt.x + Math.cos(a) * (R + 16);
        const by = tgt.y + Math.sin(a) * (R + 16);
        c.globalAlpha = fade * (0.9 - brown * 0.3);
        c.strokeStyle = brown > 0.5 ? "#5A4420" : "#2E6B2C";
        c.lineWidth = 5.2 - (i % 3) * 0.9;
        c.shadowColor = brown > 0.5 ? "#00000000" : "#4FD06B";
        c.shadowBlur = brown > 0.5 ? 0 : 12;
        /* Each stem rises and BENDS IN over the quarry — the cage closes.
           Bramblesnare's roots stay on the floor and never arch. */
        c.beginPath();
        c.moveTo(bx, by);
        c.quadraticCurveTo(bx, by - h * 0.8, tgt.x + Math.cos(a) * 6, by - h);
        c.stroke();
        c.shadowBlur = 0;
        if (grow > 0.5){                      // leaves unfurling on the stems
          for (let j = 1; j <= 2; j++){
            const t2 = j / 3;
            const lx = lerp(bx, tgt.x + Math.cos(a) * 6, t2);
            const ly = lerp(by, by - h, t2);
            c.globalAlpha = fade * (1 - brown) * 0.85 * clamp((grow - 0.5) * 2, 0, 1);
            c.fillStyle = "#BCF7C7";
            c.save(); c.translate(lx, ly); c.rotate(a + j * 1.1);
            c.beginPath(); c.ellipse(0, 0, 8, 3.4, 0, 0, TAU); c.fill();
            c.restore();
          }
        }
      }
    }

    /* ---- Eclipse: an OCCULTED BODY, and a shadow front that puts lights out -
       v1 was a dark disc expanding over the arena, and it did not read. You
       cannot subtract light from a hall that is already #100C16 — the "eaten
       light" was invisible by construction, and the corona ring ended up doing
       the entire job while growing off the top of the frame.
       So the reading is inverted. The eclipse is now an OBJECT that stays put
       and holds the eye: a black body over the caster with a hard bright rim,
       which is what an eclipse actually looks like. The expanding part is a
       thin shadow FRONT, and what makes it legible is not its own darkness but
       the motes it puts out as it passes them. Light going out is visible on a
       dark background; darkness is not. */
    else if (u.w === "nightfell"){
      const ex = clamp(u.t / 0.50, 0, 1);
      const fade = 1 - clamp((u.t - 0.62) / 0.75, 0, 1);
      const R = Math.max(1, u.radius * (1 - Math.pow(1 - ex, 2.2)));
      const BODY = 54;

      /* the shadow front — thin, and it is a WAVE, not a fill */
      c.globalAlpha = 0.55 * fade * (1 - ex * 0.5);
      const g = c.createRadialGradient(u.x, u.y, Math.max(1, R * 0.86), u.x, u.y, R);
      g.addColorStop(0, "#0A031600"); g.addColorStop(0.7, "#0A0316CC");
      g.addColorStop(1, "#00000000");
      c.fillStyle = g;
      c.beginPath(); c.arc(u.x, u.y, R, 0, TAU); c.fill();

      /* the motes the front has already passed, going out one by one. This is
         the whole effect: an absence you can only see by what it removes. */
      c.save();
      c.globalCompositeOperation = "lighter";
      for (let i = 0; i < 26; i++){
        const a = shellHash(83, i) * TAU;
        const rr = 70 + shellHash(84, i) * (u.radius * 1.15);
        const out = clamp((R - rr) / 46, 0, 1);          // 1 once swallowed
        if (out >= 1) continue;
        c.globalAlpha = (1 - out) * fade * 0.95;
        c.fillStyle = out > 0.35 ? "#DDB8FF" : "#F2E4FF";
        const s = (1 - out) * (1.8 + shellHash(85, i) * 2.4) + out * 5.5;
        c.beginPath();
        c.arc(u.x + Math.cos(a) * rr, u.y + Math.sin(a) * rr, s, 0, TAU);
        c.fill();
      }
      c.restore();

      /* THE BODY: black, hard-edged, and it does not move. An eclipse has a
         centre; v1 had only a rim leaving the frame. */
      c.globalAlpha = fade;
      c.fillStyle = "#05010A";
      c.beginPath(); c.arc(u.x, u.y, BODY, 0, TAU); c.fill();

      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = fade;
      c.strokeStyle = "#F2E4FF"; c.lineWidth = 2.6;
      c.shadowColor = "#A45CF0"; c.shadowBlur = 20;
      c.beginPath(); c.arc(u.x, u.y, BODY, 0, TAU); c.stroke();
      c.shadowBlur = 0;
      /* the corona proper — uneven, and it breathes */
      for (let i = 0; i < 22; i++){
        const a = (i / 22) * TAU + u.t * 0.35;
        const l = BODY * (0.22 + shellHash(81, i) * 0.55
                          * (0.7 + 0.3 * Math.sin(u.t * 6 + i)));
        c.globalAlpha = fade * 0.75;
        c.strokeStyle = "#DDB8FF"; c.lineWidth = 2.2;
        c.beginPath();
        c.moveTo(u.x + Math.cos(a) * BODY, u.y + Math.sin(a) * BODY);
        c.lineTo(u.x + Math.cos(a) * (BODY + l), u.y + Math.sin(a) * (BODY + l));
        c.stroke();
      }
      c.restore();
    }

    /* ---- Corollary: the proof, stepped out and then concluded -------------- */
    else if (u.w === "axiom"){
      const STEPS = 5;
      const step = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - 0.52) / 0.9, 0, 1);
      const done = clamp((u.t - 0.30) / 0.22, 0, 1);

      /* the rule: straight, and it ARRIVES IN STEPS rather than flickering.
         Unmaking is a jag redrawn every frame; this is the same school
         insisting the other way. */
      const n = Math.max(1, Math.ceil(STEPS * step));
      c.globalAlpha = fade;
      c.strokeStyle = "#BCDDFF"; c.lineWidth = 5;
      c.shadowColor = "#4A9EFF"; c.shadowBlur = 18;
      c.beginPath();
      c.moveTo(u.x, u.y);
      c.lineTo(lerp(u.x, tgt.x, n / STEPS), lerp(u.y, tgt.y, n / STEPS));
      c.stroke();
      c.strokeStyle = "#FFFFFF"; c.lineWidth = 1.8; c.shadowBlur = 0;
      c.beginPath();
      c.moveTo(u.x, u.y);
      c.lineTo(lerp(u.x, tgt.x, n / STEPS), lerp(u.y, tgt.y, n / STEPS));
      c.stroke();

      for (let i = 1; i <= n; i++){          // a glyph stamped at every node
        const t2 = i / STEPS;
        this._glyph(c, lerp(u.x, tgt.x, t2), lerp(u.y, tgt.y, t2),
                    7 + i * 1.6, u.t * 1.8 + i, "#BCDDFF", fade * 0.95);
      }

      /* the conclusion: one sigil, snapping to size and holding */
      if (u.hit && done > 0){
        const pop = 1 + (1 - done) * 0.7;
        this._glyph(c, tgt.x, tgt.y, 34 * pop, -u.t * 1.6, "#FFFFFF", fade * done);
        c.globalAlpha = fade * done * 0.7;
        c.strokeStyle = "#4A9EFF"; c.lineWidth = 2.2;
        c.shadowColor = "#4A9EFF"; c.shadowBlur = 16;
        c.beginPath(); c.arc(tgt.x, tgt.y, 34 * pop * 1.5, 0, TAU); c.stroke();
        c.shadowBlur = 0;
      }
    }
'''

LIFE_OLD = """      life: { dawnbringer: 1.6, widowmaker: 1.3, grudgebearer: 1.7,
              thornwake: 2.4, gravemourn: 1.6, spellbreaker: 1.4 }[f.w.id] || 1.5,"""
LIFE_NEW = """      life: { dawnbringer: 1.6, widowmaker: 1.3, grudgebearer: 1.7,
              thornwake: 2.4, gravemourn: 1.6, spellbreaker: 1.4,
              /* The four new greatswords. Rootfast is long because it is a
                 FREEZE and the art has to still be on screen while the hold
                 it is explaining is in force — Bramblesnare is 2.4 for the
                 same reason. The other three are strikes and end. */
              oathwound: 1.5, heartwood: 2.2, nightfell: 1.4,
              axiom: 1.5 }[f.w.id] || 1.5,"""

ANCHOR_UNDER = """    c.restore();
  }

  /* Above the fighters: light, blades, vines, bolts, dust. */
  drawUltOver(m){"""

ANCHOR_OVER = """    c.restore();
  }

  /* ----------------------------------------------------------- fighter --- */"""

CHECK_JS = r"""
(ids) => {
  const out = [];
  const R = document.createElement('canvas');
  for (const id of ids){
    const w = AC.WEAPONS.find(x => x.id === id);
    // Drive a real ultimate: build a match, force the fx block the way
    // fireUlt does, and draw at several points across its life. A branch that
    // throws, or that draws nothing, both fail here.
    const m = new AC.Match(id, id === "dawnbringer" ? "grudgebearer" : "dawnbringer",
                           0x9A11 + 7);
    AC.setResolution(1080, 1920);
    const f = m.a, foe = m.b;
    const rec = [];
    let threw = null;
    for (const t of [0.05, 0.25, 0.5, 0.9, 1.3]){
      m.ultFx = { w: id, kind: w.ult.kind, src: "a", tgt: "b",
                  x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: true,
                  radius: w.ult.radius || 300, aff: f.aff, t: t, life: 2.2 };
      const cv = document.getElementById('cv');
      const c = cv.getContext('2d');
      c.setTransform(1,0,0,1,0,0);
      c.fillStyle = "#000"; c.fillRect(0,0,1080,1920);
      try { AC.__draw(m); } catch (e) { threw = String(e); break; }
      // ink above a floor: how much of the frame the set-piece is responsible
      // for. Compared against the SAME frame with ultFx null.
      const a = c.getImageData(0,0,1080,1920).data;
      m.ultFx = null;
      c.setTransform(1,0,0,1,0,0);
      c.fillStyle = "#000"; c.fillRect(0,0,1080,1920);
      AC.__draw(m);
      const b = c.getImageData(0,0,1080,1920).data;
      let diff = 0;
      for (let i = 0; i < a.length; i += 16){
        if (Math.abs(a[i]-b[i]) + Math.abs(a[i+1]-b[i+1]) + Math.abs(a[i+2]-b[i+2]) > 12) diff++;
      }
      rec.push({ t, px: diff });
    }
    out.push({ id, threw, rec, peak: Math.max(...rec.map(r => r.px), 0) });
  }
  return out;
}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="sc-gs7.html")
    ap.add_argument("--out", default="sc-gs7-ults.html")
    ap.add_argument("--no-check", action="store_true")
    A = ap.parse_args()

    if pathlib.Path(A.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    src = HERE / A.src
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr)
        return 2
    s = src.read_text(encoding="utf-8")

    for name, anc in (("drawUltUnder tail", ANCHOR_UNDER),
                      ("drawUltOver tail", ANCHOR_OVER),
                      ("ultFx life table", LIFE_OLD)):
        n = s.count(anc)
        if n != 1:
            print(f"! anchor {name} appears {n} times, expected 1. Diff before "
                  f"re-anchoring — do not loosen it.", file=sys.stderr)
            return 3

    s = s.replace(ANCHOR_UNDER, UNDER + ANCHOR_UNDER, 1)
    s = s.replace(ANCHOR_OVER, OVER + ANCHOR_OVER, 1)
    s = s.replace(LIFE_OLD, LIFE_NEW, 1)
    print("  [ultart] drawUltUnder: 4 branches")
    print("  [ultart] drawUltOver:  4 branches")
    print("  [ultart] ultFx life table: 4 durations")

    doc = "<!DOCTYPE html>\n"
    i = s.find(doc)
    if i < 0:
        print("! no doctype", file=sys.stderr)
        return 4
    stamp = (f"<!-- GENERATED by ultart_build.py --src {A.src} — "
             f"do not hand-edit or tune in place -->")
    s = s[:i + len(doc)] + stamp + "\n" + s[i + len(doc):]

    out = HERE / A.out
    out.write_text(s, encoding="utf-8")
    print(f"{A.src} -> {A.out}   sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}")

    if A.no_check:
        print("  ! checks skipped")
        return 0

    sys.path.insert(0, str(HERE))
    from scpage import game
    ids = ["oathwound", "heartwood", "nightfell", "axiom"]
    with game(game_path=out) as (page, errors):
        rows = page.evaluate(CHECK_JS, ids)
        if errors:
            print(f"! page errors: {errors[:3]}", file=sys.stderr)
            out.unlink(); return 5

    bad = []
    print(f"\n  {'relic':<12}{'t=.05':>8}{'t=.25':>8}{'t=.5':>8}{'t=.9':>8}{'t=1.3':>8}")
    for r in rows:
        if r["threw"]:
            bad.append(f"{r['id']}: threw {r['threw'][:80]}")
            print(f"  {r['id']:<12}  THREW: {r['threw'][:60]}")
            continue
        cells = "".join(f"{x['px']:>8}" for x in r["rec"])
        print(f"  {r['id']:<12}{cells}")
        # A set-piece that draws nothing is the exact bug this build fixes.
        if r["peak"] < 200:
            bad.append(f"{r['id']}: peak {r['peak']} changed samples — draws (almost) nothing")
        if r["rec"][0]["px"] > r["peak"] * 0.9 and r["rec"][-1]["px"] > r["peak"] * 0.9:
            bad.append(f"{r['id']}: no arc — it does not start or end, it just sits")

    print()
    if bad:
        print("  ULT ART CHECK FAILED:")
        for b in bad: print("   ", b)
        out.unlink()
        print(f"\n  {A.out} deleted.")
        return 6
    print("  ult art check PASS — all four draw, none throws, each has an arc")
    print("  (sampled every 16th pixel; numbers are relative, not a budget)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
