"""SCRUNCH — the hall makes room, the fight never stops.

Rick, on the name plate: *"the nameplate drops down and covers the top of the
screen just to show the same information that was always there... what if we
scrunch up the arena and show the fight cards at the bottom?"*

He was right and the plate is abandoned. The HUD already carries both names, so
a banner repeating them is decoration. The STATS are what the HUD does not
carry, and a panel is worth its pixels only if it says something new.

WHAT THIS DOES
  * the hall scales down to `k` (0.65) over `ease`, holds, and scales back
  * a purpose-built panel occupies the freed space at the bottom
  * the simulation is never gated -- `scrunchT` is a presentation clock and
    step() has no early return for it, unlike `introT`
  * at the kill the hall scrunches again and the panel shows the VERDICT, and
    the full-screen result card is suppressed so the loser's shatter is NOT
    played out behind a 60% scrim -- verdict and payoff share the frame

THE CONSTRAINT: the hall is 520x800 sim units and the renderer is width-bound
(`scale = aw / CONFIG.arena.w`), so cutting height cuts width by the same
factor. Changing CONFIG.arena is a simulation change and would force a retune,
so it is not on the table. At k=0.65 the hall is 686 wide in a 1080 frame and
197px of margin appears on each side. That is the real, visible price and it is
paid deliberately.

NOTHING HERE TOUCHES THE SIMULATION. `CONFIG.arena`, `hud`, `arenaTop` and the
un-scrunched `scale`/`aw`/`ah` are all unchanged -- the layout fields are
mutated for the duration of one draw and handed straight back.
"""
import argparse, hashlib, pathlib, sys

A_CFG = "intro: { dur: 4.0, clash: 0.46, reveal: 0.50 }"
B_CFG = A_CFG + """,
  /* THE SCRUNCH. `k` 0.65 was chosen from a sheet at three levels: 0.75 leaves
     only 396px of panel and forces the stats to 0.61 scale (cramped), 0.55
     gives the panel everything but the relics get small. 0.65 is 558px of
     panel with the stats near full size and a hall that is still easy to
     follow. `bottom` is the last row clear of the platform's caption zone --
     the delivered frame maps game y to output y*0.7875 + 96, and TikTok's
     furniture starts around output 1530. */
  scrunch: { on: true, k: 0.65, ease: 0.42, intro: 3.0,
             resultDelay: 1.05, gap: 22, bottom: 1812 }"""

A_FLD = "this.introT = 0;"
B_FLD = A_FLD + """
    /* Presentation clocks. Like introT in that simulate() never arms them --
       `scrunchAuto` is set by __inject and newMatch, which only presentation
       and capture layers call -- and UNLIKE introT in that step() has no early
       return for them. The hall makes room; it does not stop. */
    this.scrunchT = 0; this.scrunchMode = null; this.scrunchAuto = false;"""

A_STEP = "  step(dt){"
B_STEP = """  step(dt){
    /* THE SCRUNCH CLOCK, and the two moments it arms on. Deliberately ahead of
       every early return in step(), including `over`, because the verdict beat
       has to arm after the match has ended. */
    if (this.scrunchT > 0) this.scrunchT -= dt;
    if (this.scrunchAuto && CONFIG.scrunch.on){
      const S = CONFIG.scrunch;
      /* The first clank is the anchor, exactly as it is for the intro card --
         firstbeat.py made that a measured quantity rather than a taste call. */
      if (!this.scrunchMode && this.clankCount > 0){
        this.scrunchMode = "tape";
        this.scrunchT = S.ease * 2 + S.intro;
      }
      /* The verdict waits for the shatter. drawResult already learned this the
         hard way (its own note: the card used to fade in on the killing blow
         and put the most legible moment in the match behind 60% black), so the
         same 1.05s hold is reused rather than reinvented. */
      if (this.over && this.scrunchMode !== "result" &&
          (this.resultT || 0) >= S.resultDelay){
        this.scrunchMode = "result";
        this.scrunchT = S.ease * 2 + 999;      // holds to the end of the clip
      }
    }"""

# the scrunch factor and both panels, inserted before drawFooter
A_DRAW = "  drawFooter(m){"
B_DRAW = """  /* How far the hall is scaled right now. 1 = untouched. */
  scrunchK(m){
    const S = CONFIG.scrunch;
    if (!S.on || !m || !(m.scrunchT > 0)) return 1;
    const hold = m.scrunchMode === "result" ? 999 : S.intro;
    const total = S.ease * 2 + hold;
    const e = total - m.scrunchT;
    const eo = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3);
    if (e < S.ease)        return lerp(1, S.k, eo(e / S.ease));
    if (e < S.ease + hold) return S.k;
    return lerp(S.k, 1, eo((e - S.ease - hold) / S.ease));
  }

  /* The panel. Laid out FOR this strip rather than borrowed from the middle of
     a full-screen card -- `_introTape` is 546px tall and centred for a 1920
     frame, and reusing it meant scaling it to 0.9 and hoping. Every position
     below is derived from the box it is actually given, so the panel adapts if
     `k` moves instead of being re-tuned by hand. */
  drawScrunchPanel(m, k){
    const S = CONFIG.scrunch, c = this.ctx;
    const y = this.arenaTop + this.ah * k + S.gap;
    const h = S.bottom - y, x = 24, w = this.W - 48;
    if (h < 60) return;
    /* the panel arrives as the hall retreats, on the same curve */
    const a = clamp((1 - k) / (1 - S.k), 0, 1);
    c.save();
    c.globalAlpha = a;
    c.fillStyle = "#0C0914";
    this.roundRect(x, y, w, h, 14); c.fill();
    c.strokeStyle = "#C9A22755"; c.lineWidth = 2;
    this.roundRect(x, y, w, h, 14); c.stroke();
    if (m.scrunchMode === "result") this._panelResult(m, x, y, w, h);
    else                            this._panelFacts(m, x, y, w, h);
    c.restore();
  }

  /* WHAT THE STATUSES AND ULTS DO -- not a stat comparison.

     Rick: *"i dont think stats are what the scrunch should show. it should
     show what the status effects and ults do"*. He is right and the tape is
     out. Damage/hit and weight are inert trivia a viewer cannot act on; SUNDER
     and HEMORRHAGE and QUARRELSTORM are the things that are about to happen on
     screen, and the panel is a legend for them. When "+2 HEMORRHAGE" flashes
     over a relic ten seconds later, this is what makes the red numbers mean
     something.

     Every string comes from `_introFacts` and `STATUS[].tip`, which the intro
     card already uses -- so the panel and the card cannot drift, and the
     ">=40 char" tip discipline verify.py enforces still governs the copy. */
  /* SELF-CONTAINED fact composition and wrapping.

     Earlier cuts called `_introFacts` / `_introWrap` so the panel and the intro
     card could not drift. That is the right instinct and the wrong dependency:
     those helpers were extracted late in the chain, and `01-live` composes the
     same facts INLINE inside `_introCard`. A patch that only applies to builds
     newer than the extraction is not a patch for the live session.

     So the panel composes its own, from the same single source of truth the
     card reads -- `STATUS[].tip`, `relicStatus()`, `w.ult.tip` and
     `w.ult.charge`. The STRINGS cannot drift because there is only one copy of
     them; only the composition is duplicated, and the panel is its own surface
     with its own layout anyway. The cooldown goes on a chip rather than being
     concatenated into the tip, which is where the newer card puts it too. */
  _scrunchWrap(text, maxW, size, maxLines){
    const c = this.ctx;
    const words = String(text || "").split(" ");
    for (;;){
      c.font = "500 " + size + "px ui-sans-serif,system-ui,sans-serif";
      const lines = []; let cur = "";
      for (const wd of words){
        const t = cur ? cur + " " + wd : wd;
        if (!cur || c.measureText(t).width <= maxW) cur = t;
        else { lines.push(cur); cur = wd; }
      }
      lines.push(cur);
      const over = lines.some(l => c.measureText(l).width > maxW);
      if ((!over && lines.length <= maxLines) || size <= 15) return { lines, size };
      size -= 1;
    }
  }

  _scrunchFacts(f){
    const pal = f.aff, out = [];
    if (f.w.mode === "swing")
      out.push({ kind: "strip", name: "TRUESTRIKE",
                 tip: "Swords track their target instead of rotating",
                 col: pal.glow });
    const rs = relicStatus(f.w);
    if (rs && rs.def){
      /* ON HIT for self-statuses too -- ward is banked by landing hits. The
         +n is suppressed when the status cannot stack. */
      const n = (f.w.onHit && f.w.onHit[rs.key]) ||
                (f.w.onSelf && f.w.onSelf[rs.key]) || 1;
      const cnt = rs.def.maxStacks > 1 ? "+" + n + " " : "";
      out.push({ kind: "panel", tag: "ON HIT",
                 name: (rs.self ? "GAIN " : "") + cnt + rs.def.name.toUpperCase(),
                 tip: rs.def.tip, col: pal.core, tagCol: "#7E7263",
                 ink: "#C6BBA6", rail: pal.core });
    }
    out.push({ kind: "panel", tag: "ULTIMATE",
               name: f.w.ult.name.toUpperCase(), tip: f.w.ult.tip || "",
               col: "#FFF4D0", tagCol: "#9C8654", ink: "#CFC2A4",
               rail: "#C9A227", chip: f.w.ult.charge + "s COOLDOWN" });
    return out;
  }

  _panelFacts(m, x, y, w, h){
    const c = this.ctx;
    const pad = 22, nameH = 74, gut = 26;
    const colW = (w - pad * 2 - gut) / 2;
    const cols = [
      { f: m.a, x: x + pad,                    align: "left" },
      { f: m.b, x: x + pad + colW + gut,       align: "left" },
    ];

    /* names, outboard, each beside its own colour rail -- the two columns are
       identified by colour and position and nothing else would say which is
       which */
    [[m.a, x + pad, 1], [m.b, x + w - pad, -1]].forEach(([f, tx, dir]) => {
      c.fillStyle = f.aff.core;
      this.roundRect(dir > 0 ? tx : tx - 9, y + pad + 2, 9, 52, 5); c.fill();
      c.textAlign = dir > 0 ? "left" : "right";
      c.font = "700 38px ui-serif,Georgia,serif";
      c.fillStyle = "#EDE3D0";
      c.fillText(f.w.name.toUpperCase(), tx + dir * 20, y + pad + 36);
      c.font = "700 19px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = f.aff.core;
      c.fillText(f.aff.name.toUpperCase(), tx + dir * 22, y + pad + 60);
    });
    c.strokeStyle = "#C9A22733"; c.lineWidth = 1;
    c.beginPath(); c.moveTo(x + pad, y + pad + nameH);
    c.lineTo(x + w - pad, y + pad + nameH); c.stroke();
    /* the column divider, so two independent lists do not read as one */
    c.strokeStyle = "#C9A22722";
    c.beginPath(); c.moveTo(x + pad + colW + gut / 2, y + pad + nameH + 10);
    c.lineTo(x + pad + colW + gut / 2, y + h - pad); c.stroke();

    const facts = cols.map(cc => this._scrunchFacts(cc.f));
    /* a class trait (TRUESTRIKE) is one line and only some relics have one.
       Reserve the same height in BOTH columns so the ON HIT blocks start level
       -- a comparison whose two halves are offset stops being a comparison. */
    const hasStrip = facts.some(fs => fs.some(r => r.kind === "strip"));
    const stripH = hasStrip ? 40 : 0;
    const top = y + pad + nameH + 16;

    const block = (r, cx, by, wid, bottom) => {
      const wrap = this._scrunchWrap(r.tip, wid - 14, 21, 3);
      const bodyH = 20 + 30 + wrap.lines.length * (wrap.size + 6);
      const yy = bottom ? by - bodyH : by;
      c.fillStyle = r.rail || "#C9A227";
      this.roundRect(cx, yy + 2, 5, bodyH - 8, 3); c.fill();
      c.textAlign = "left";
      c.font = "700 16px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = r.tagCol || "#7E7263";
      c.fillText(r.tag || "", cx + 16, yy + 16);
      if (r.chip){
        c.textAlign = "right";
        c.fillStyle = "#7E7263";
        c.fillText(r.chip, cx + wid - 6, yy + 16);
        c.textAlign = "left";
      }
      c.font = "700 27px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = r.col || "#EDE3D0";
      c.fillText(r.name, cx + 16, yy + 46);
      c.font = "500 " + wrap.size + "px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = r.ink || "#C6BBA6";
      wrap.lines.forEach((ln, i) =>
        c.fillText(ln, cx + 16, yy + 46 + 26 + i * (wrap.size + 6)));
      return bodyH;
    };

    cols.forEach((cc, i) => {
      const fs = facts[i];
      const strip = fs.find(r => r.kind === "strip");
      if (strip){
        c.textAlign = "left";
        c.font = "700 17px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = strip.col;
        c.fillText(strip.name, cc.x, top + 14);
        const wr = this._scrunchWrap(strip.tip, colW, 19, 1);
        c.font = "500 " + wr.size + "px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = "#8B8071";
        c.fillText(wr.lines[0], cc.x, top + 34);
      }
      const onHit = fs.find(r => r.tag === "ON HIT");
      if (onHit) block(onHit, cc.x, top + stripH, colW, false);
      const ult = fs.find(r => r.tag === "ULTIMATE");
      if (ult) block(ult, cc.x, y + h - pad, colW, true);
    });
  }

  /* The verdict, in the same strip. The point of putting it here instead of
     over the hall is that the loser is coming apart at exactly this moment and
     the full-screen card used to bury that behind a scrim. */
  _panelResult(m, x, y, w, h){
    const c = this.ctx, W2 = x + w / 2;
    const wn = m.winner, ls = m.loser;
    if (!wn){ return; }
    c.textAlign = "center";
    c.font = "700 22px ui-sans-serif,system-ui,sans-serif";
    c.fillStyle = "#6E6378";
    c.fillText(m.reason === "timeout" ? "THE SEALS HOLD" : "THE CROWN PASSES TO", W2, y + 40);

    c.font = "700 58px ui-serif,Georgia,serif";
    c.fillStyle = wn.aff.core;
    c.shadowColor = wn.aff.core; c.shadowBlur = 40;
    c.fillText(wn.w.name.toUpperCase(), W2, y + 104);
    c.shadowBlur = 0;

    /* THE NUMBER THE VIDEO NEVER STATED. Every week-1 note is written around
       it -- 2 HP of 300, won on 12 HP, Ironhail on 8 HP -- and it has never
       been on screen at a size anyone reads on a phone. */
    const hp = Math.ceil(wn.hp);
    c.font = "800 92px ui-sans-serif,system-ui,sans-serif";
    c.fillStyle = "#EDE3D0";
    c.fillText(hp + " HP", W2, y + h - 92);
    c.font = "700 22px ui-sans-serif,system-ui,sans-serif";
    c.fillStyle = "#7E7263";
    c.fillText("OF " + CONFIG.combat.baseHP + " REMAINING", W2, y + h - 58);

    c.font = "400 21px ui-sans-serif,system-ui,sans-serif";
    c.fillStyle = "#5E5568";
    c.fillText(`over ${ls.w.name}  ·  ${m.t.toFixed(1)}s  ·  ${m.clankCount} clanks`,
               W2, y + h - 20);
  }

  drawFooter(m){
    /* The panel is the framing while the hall is scrunched, and the footer
       would otherwise sit just above it -- visible through the panel while it
       is still fading in. Suppressed for the whole scrunch rather than only
       where it overlaps, so it never half-appears. */
    if (CONFIG.scrunch.on && this.scrunchK(m) < 0.999) return;
    return this._drawFooterReal(m);
  }

  _drawFooterReal(m){"""

# draw(): apply the scrunched layout, and hand it back before the panel
A_HEAD = ('    if (m.introT > 0 && !this._introScene){ this.drawIntro(m); return; }\n'
          '    c.save();')
B_HEAD = ('    if (m.introT > 0 && !this._introScene){ this.drawIntro(m); return; }\n'
          '    /* THE SCRUNCH. Every draw below is written against pad/aw/ah/scale,\n'
          '       so shrinking those four is the whole mechanism -- the hall, the\n'
          '       clip rects, the relics and the arena frame all follow for free.\n'
          '       They are handed straight back before the panel is drawn, so no\n'
          '       layout constant is left mutated and nothing downstream can be\n'
          '       looking at a scrunched value on the next frame. */\n'
          '    let __sk = 1, __sv = null;\n'
          '    if (!this._introScene){\n'
          '      __sk = this.scrunchK(m);\n'
          '      if (__sk < 0.999){\n'
          '        __sv = { pad: this.pad, aw: this.aw, ah: this.ah, scale: this.scale };\n'
          '        this.aw = __sv.aw * __sk; this.ah = __sv.ah * __sk;\n'
          '        this.scale = __sv.scale * __sk; this.pad = (this.W - this.aw) / 2;\n'
          '      }\n'
          '    }\n'
          '    c.save();')

A_TAIL = "    if (m.over) this.drawResult(m);\n    c.restore();"
B_TAIL = ("    if (m.over) this.drawResult(m);\n"
          "    c.restore();\n"
          "    if (__sv){\n"
          "      Object.assign(this, __sv);\n"
          "      c.setTransform(this.k, 0, 0, this.k, 0, 0);\n"
          "      this.drawScrunchPanel(m, __sk);\n"
          "    }")

# the full-screen verdict card stands down when the panel is carrying it
A_RES = "  drawResult(m){\n    const c = this.ctx, w = m.winner, l = m.loser;"
B_RES = ("  drawResult(m){\n"
         "    /* The scrunch panel carries the verdict now. Both at once would put\n"
         "       a 60% scrim over the shatter, which is the exact defect the note\n"
         "       below was written about. */\n"
         "    if (CONFIG.scrunch.on && m.scrunchMode === \"result\") return;\n"
         "    const c = this.ctx, w = m.winner, l = m.loser;")

# arm the presentation clocks on both paths that build a match for viewing
A_INJ = "__inject(m){ match = m; window.__match = m;"
B_INJ = "__inject(m){ match = m; window.__match = m; m.scrunchAuto = CONFIG.scrunch.on;"
A_NEW = ("  match.introT = introOn ? CONFIG.intro.dur : 0;\n"
         "  window.__match = match;")   # the btnIntro handler has the same
                                        # first line, so anchor on both
B_NEW = ("  match.introT = introOn ? CONFIG.intro.dur : 0;\n"
         "  /* the live page gets the scrunch too, so this build can be WATCHED\n"
         "     rather than only rendered */\n"
         "  match.scrunchAuto = CONFIG.scrunch.on;\n"
         "  window.__match = match;")

# The live page keeps every feature A/B-able in two clicks; the scrunch gets the
# same treatment, beside the intro-card toggle it replaces. OPTIONAL -- the
# render-only chain builds have no button bar and must still build.
A_BTNH = '    <button id="btnIntro">Intro card</button>'
B_BTNH = ('    <button id="btnIntro">Intro card</button>\n'
          '    <button id="btnScrunch">Scrunch</button>')
A_BTNJ = 'const btnMute = document.getElementById("btnMute");'
B_BTNJ = ('const btnScrunch = document.getElementById("btnScrunch");\n'
          'if (btnScrunch){\n'
          '  btnScrunch.onclick = () => {\n'
          '    CONFIG.scrunch.on = !CONFIG.scrunch.on;\n'
          '    btnScrunch.textContent = CONFIG.scrunch.on ? "Scrunch" : "No scrunch";\n'
          '    btnScrunch.classList.toggle("off", !CONFIG.scrunch.on);\n'
          '    if (match) match.scrunchAuto = CONFIG.scrunch.on;\n'
          '  };\n'
          '}\n\n'
          'const btnMute = document.getElementById("btnMute");')
OPTIONAL = [("live toggle markup", A_BTNH, B_BTNH), ("live toggle handler", A_BTNJ, B_BTNJ)]

STEPS = [("CONFIG.intro", A_CFG, B_CFG), ("Match fields", A_FLD, B_FLD),
         ("step(dt)", A_STEP, B_STEP), ("panels", A_DRAW, B_DRAW),
         ("draw() head", A_HEAD, B_HEAD), ("draw() tail", A_TAIL, B_TAIL),
         ("drawResult", A_RES, B_RES), ("__inject", A_INJ, B_INJ),
         ("newMatch", A_NEW, B_NEW)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", default="../02-chain/sc-scrunch.html")
    ap.add_argument("--k", type=float, default=None, help="override CONFIG.scrunch.k")
    a = ap.parse_args()
    src = pathlib.Path(a.src).resolve()
    h0 = src.read_text(encoding="utf-8")
    h = h0
    print(f"  src {src.name}  {hashlib.sha256(h0.encode()).hexdigest()[:16]}")

    # Each anchor must appear EXACTLY ONCE. A builder whose anchor silently
    # matched zero times emits a file identical to its input and reports
    # success, which is the one failure mode nothing downstream can see.
    for name, anc, _ in STEPS:
        n = h.count(anc)
        if n != 1:
            print(f"  FAIL  anchor {name!r} matched {n} times, expected 1")
            return 1
    for name, anc, rep in STEPS:
        h = h.replace(anc, rep, 1)
        print(f"  ok    {name}")
    # Optional steps: applied where the anchor exists, REPORTED where it does
    # not. A render-only chain build has no button bar and that is not a fault.
    for name, anc, rep in OPTIONAL:
        n = h.count(anc)
        if n == 1:
            h = h.replace(anc, rep, 1); print(f"  ok    {name} (optional)")
        else:
            print(f"  skip  {name} (optional) — anchor matched {n} times")
    if a.k is not None:
        h = h.replace("scrunch: { on: true, k: 0.65,", f"scrunch: {{ on: true, k: {a.k},", 1)
        print(f"  ok    k overridden to {a.k}")

    out = pathlib.Path(a.out).resolve()
    out.write_text(h, encoding="utf-8", newline="\n")
    print(f"\n  wrote {out.name}  {hashlib.sha256(h.encode()).hexdigest()[:16]}"
          f"  (+{len(h) - len(h0)} bytes)")
    print("  01-live untouched; CONFIG.intro and the card path are intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
