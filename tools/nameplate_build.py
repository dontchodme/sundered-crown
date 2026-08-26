"""NAME PLATE — the matchup, over a fight that never stops.

The 4.0s intro card costs 55-75% of the audience present when it appears
(v32 §6, measured on eight shipped videos). The expensive part is not the card,
it is the FREEZE: while `introT > 0`, `step()` returns early and the simulation
does not advance. Four seconds of stopped fight.

This builds the replacement. Same information -- both names, both affinities,
both palettes -- delivered as a band that rises out of the HUD, holds, and
retracts into it, while the fight runs underneath at full speed.

PLACEMENT IS MEASURED, NOT PICKED. `plate_occupancy.py` sampled 128 matches
across eight pairings inside the 3.0s window the plate would occupy:

    sim y   0-100   ->  screen y  176- 379    1.5% of relic-time   <- here
    sim y 600-700   ->  screen y 1394-1598   25.4% of relic-time   17x busier

The relics live in the BOTTOM of the hall during that window. A broadcast
"lower third" would land squarely on top of them. The top band, directly under
the HUD, is 17x quieter -- and it is where the names already live, so the plate
reads as the HUD briefly enlarged rather than as a new object. When it retracts
the HUD keeps carrying the names, which is what the card never did.

WHAT THIS DOES NOT TOUCH: `CONFIG.intro` and the whole card path are left
intact, so a card build and a plate build differ by one flag and can be
A/B'd. `plateT` is presentation-only -- `simulate()` never sets it, exactly as
`introT` is never set, so every headless sweep, the tuner and `engine_ab` are
bit-identical. No layout constant moves: `hud`, `arenaTop`, `ah` and `pad` are
all untouched, so nothing here can force a retune.
"""
import argparse, hashlib, pathlib, sys

# ---------------------------------------------------------------- 1. CONFIG
A_CFG = "intro: { dur: 4.0, clash: 0.46, reveal: 0.50 }"
B_CFG = A_CFG + """,
  /* THE NAME PLATE. It sits ON the HUD rather than below it, because the HUD
     ALREADY carries both names -- a second band underneath printed the same
     two words twice, 100px apart, which read as a bug rather than a design
     (caught at 1:1 on plate-zoom, invisible on a contact sheet). So the plate
     is the HUD enlarged in place: it covers y 0-236, of which the HUD already
     owned 0-152, so the genuinely new occlusion is 84px. That 84px lands in
     the band plate_occupancy.py measured as the quietest in the hall during
     this exact window -- 1.5% of relic-time against 25.4% for the busiest.

     `dur` is 3.0 against the card's 4.0 because nothing is being waited for:
     the fight is already running, so the plate only has to be READ. */
  plate: { on: true, dur: 3.0, rise: 0.34, fall: 0.40,
           x: 0, w: 1080, y: 0, h: 236, row: 92, pad: 26 }"""

# ------------------------------------------------------- 2. the Match field
A_FLD = "this.introT = 0;"
B_FLD = A_FLD + """
    /* Presentation clock, like introT -- but this one does NOT gate step().
       simulate() never sets it, so no sweep, tuner or A/B ever sees it. */
    this.plateT = 0;"""

# ------------------------------------------------------------- 3. the clock
A_STEP = "  step(dt){"
B_STEP = """  step(dt){
    /* THE PLATE CLOCK. Deliberately the first thing in step() and deliberately
       NOT a gate: it runs down while the world advances normally, which is the
       entire point of the plate. The bell fires on the clock CROSSING so a
       4x-speed dt cannot ring it twice -- same guard the intro card uses. */
    if (this.plateT > 0){
      this.plateT -= dt;
      if (this.plateT <= 0) SFX.play("seal");
    }"""

# -------------------------------------------------------------- 4. the draw
A_DRAW = "  drawFooter(m){"
B_DRAW = """  /* The plate. Drawn LAST in draw(), in screen space, for the reason the
     health lifeline is: a cinema cut lets the arena clip bleed up over the
     band, and this placement is immune to it.

     The motion is HUD-anchored. It slides down out of the HUD, holds, and
     retracts back up into it, so the viewer is told once, loudly, where the
     names live -- and the HUD is still carrying them after the plate is gone.
     The card could not do that: it occupied the middle of the frame and left
     nothing behind. */
  drawPlate(m){
    const P = CONFIG.plate;
    if (!P.on || m.plateT <= 0) return;
    const c = this.ctx;
    const e = P.dur - m.plateT;
    const eo = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3);
    const ei = t => Math.pow(clamp(t, 0, 1), 3);
    const kIn  = eo(e / P.rise);
    const kOut = ei((e - (P.dur - P.fall)) / P.fall);

    /* PURE SLIDE, never a cross-fade. A fading plate is briefly translucent,
       and the HUD it is covering prints the same two names underneath it --
       so a fade shows every name twice for 0.4s. Sliding keeps the plate
       opaque for its whole life and reveals the HUD progressively as it
       leaves, which is also the read we want: the HUD did not appear, it was
       always there. */
    const travel = P.h + 20;
    const dy = -(1 - kIn) * travel - kOut * travel;
    if (dy <= -travel + 0.5) return;

    c.save();
    c.translate(0, dy);
    c.fillStyle = "#0C0914";
    this.roundRect(P.x, P.y - 24, P.w, P.h + 24, 16); c.fill();
    c.strokeStyle = "#C9A22766"; c.lineWidth = 2;
    this.roundRect(P.x - 2, P.y - 24, P.w + 4, P.h + 24, 16); c.stroke();

    [m.a, m.b].forEach((f, i) => {
      const y = P.y + P.pad + i * P.row, pal = f.aff;
      /* the colour rail is the intro card's own identity anchor, kept
         verbatim so the plate and the card teach the same association */
      c.fillStyle = pal.core;
      this.roundRect(40, y + 6, 9, P.row - 26, 5); c.fill();
      c.textAlign = "left";
      c.font = "700 56px ui-serif,Georgia,serif";
      c.fillStyle = "#EDE3D0";
      c.fillText(f.w.name.toUpperCase(), 68, y + 48);
      c.font = "700 22px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = pal.core;
      c.fillText(pal.name.toUpperCase(), 70, y + 78);
      /* the ultimate, right-aligned, because the HUD underneath is showing it
         and the plate must not lose information the thing it covers had */
      c.textAlign = "right";
      c.font = "700 20px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = "#6B5C48";
      c.fillText(f.w.ult.name.toUpperCase(), P.w - 40, y + 48);
    });
    c.restore();

    /* On the way OUT the plate is taller than the HUD it is covering, so for
       ~0.2s its lower row and the HUD's own row are both on screen and every
       name prints twice. Redrawing the HUD over the top makes the plate slide
       up BEHIND it, which is the read the motion is claiming anyway. Only on
       the fall -- on the rise the plate is supposed to cover the HUD. */
    if (kOut > 0) this.drawHud(m);
  }

  drawFooter(m){"""

# --------------------------------------------------------- 5. the draw call
A_CALL = "    if (m.over) this.drawResult(m);"
B_CALL = A_CALL + """
    this.drawPlate(m);"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", default="../02-chain/sc-nameplate.html")
    a = ap.parse_args()
    src = pathlib.Path(a.src).resolve()
    h = src.read_text()
    print(f"  src {src.name}  {hashlib.sha256(h.encode()).hexdigest()[:16]}")

    # Every anchor must appear EXACTLY ONCE. A builder that silently matched
    # zero times would emit a file identical to its input and report success,
    # which is the one failure mode nothing downstream could detect.
    for name, anchor in (("CONFIG.intro", A_CFG), ("Match.introT", A_FLD),
                         ("step(dt)", A_STEP), ("drawFooter", A_DRAW),
                         ("draw() tail", A_CALL)):
        n = h.count(anchor)
        if n != 1:
            print(f"  FAIL  anchor {name!r} matched {n} times, expected 1")
            return 1
        print(f"  ok    anchor {name}")

    for src_s, dst_s in ((A_CFG, B_CFG), (A_FLD, B_FLD), (A_STEP, B_STEP),
                         (A_DRAW, B_DRAW), (A_CALL, B_CALL)):
        h = h.replace(src_s, dst_s, 1)

    out = pathlib.Path(a.out).resolve()
    out.write_text(h)
    print(f"\n  wrote {out.name}  {hashlib.sha256(h.encode()).hexdigest()[:16]}"
          f"  ({len(h)} bytes, +{len(h) - len(src.read_text())})")
    print("  01-live untouched; the card path is intact and one flag away.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
