/* THE FIGHT CARD, RETIRED. Removed from the build by tools/cardstrip_build.py.
 *
 * Rick, 2026-08-31: "if we can afford to remove the fight card then do it.
 * theres no sense in keeping it as i dont intend to use it again. we can just
 * archive it."
 *
 * WHAT IT WAS. A four-second full-screen title card at the head of every
 * match: a relic plate sliding down from the top, another up from the bottom,
 * the two clashing at the centreline at `CONFIG.intro.clash`, a tape of
 * scrolling text between them, and a bell on the reveal. `drawIntro` drew the
 * real renderer's real match behind a scrim, which is what the `_introScene`
 * reentry guard was for.
 *
 * WHY IT WENT. It was retired as a DELIVERABLE long before it was removed as
 * CODE -- `08-analytics` measured it losing 71-75%% of the audience before the
 * fight began, and CLAUDE.md rule 1 has read "THE FIGHT CARD IS DEAD. Nothing
 * ships with one" for six versions. `cinema_clip --intro` and `--cold-open`
 * refused to run without `--legacy-card` for just as long. What finally
 * removed it is that a dead feature is not free: 545 lines of renderer that
 * every future renderer change has to not break, a `Match` field thirty tools
 * zeroed defensively, a draw-time reentry guard on four unrelated calls, and
 * `CONFIG.intro.dur` sitting inside the seal-time arithmetic of a build that
 * never showed a card.
 *
 * WHAT REPLACED IT. Nothing, on purpose. The teaching moved to the SCRUNCH
 * PANEL, which is drawn over the live fight at the first point of contact and
 * composes its own facts from `STATUS[].tip`, `relicStatus()`, `w.ult.tip`
 * and `w.ult.charge` -- so removing this cost the game no copy at all.
 *
 * THIS FILE IS A RECORD AND NOT A MODULE. It will not run as it stands: these
 * are `Renderer` methods lifted out of a class body, and they read `IC`,
 * `CONFIG.intro`, `shellHash`, `_artShape`, `_artBox` and `_introScene`, of
 * which the middle two no longer exist in the build. To revive it, take the
 * build it was cut from (sha below) rather than pasting this back.
 *
 * CUT FROM   sc-nightfell.html sha256:2632c08b2742c4fff8c56556319d759c4fbda297be485af802141a8c94db29fe
 * BY         tools/cardstrip_build.py
 * ON         the build that became sc-nocard.html
 */



/* ---- 1 of 2 ---- */
  /* ------------------------------------------------------------- intro --- */
  /* The fight card, v2: the clash. See introcard_build.py for the full
     rationale. Shape of the 4 seconds:

       0.00-0.46  the cards fly in from top and bottom and MEET at centre
       0.46       clank: sparks out of the seam, ring, shake, the clank sound
       0.46-0.74  they rebound to rest; the tape bars grow out of the impact
       0.74-3.50  the hold: everything readable, everything a real number
       3.50-4.00  the reveal: cards leave the way they came, the scrim lifts,
                  the bell lands on the hall — already lit, already drawn —
                  and the first sim step happens on the same picture

     Everything below is a pure function of introT (through shellHash for
     scatter) — no RNG, no state, nothing the simulation can see. The scene
     behind the scrim is the real renderer drawing the real match at t=0, via
     the _introScene reentry guard in draw(). */
  drawIntro(m){
    const c = this.ctx, I = CONFIG.intro;
    const e = clamp(I.dur - m.introT, 0, I.dur);        // elapsed card time
    const p = e / I.dur;                                 // 0 -> 1 overall
    const imp = e - I.clash;                             // time since impact
    const r = clamp((e - (I.dur - I.reveal)) / I.reveal, 0, 1);
    const eo = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3);
    const fade = 1 - eo(r);

    /* the hall itself, held at t=0, under a scrim that the reveal lifts */
    this._introScene = true;
    this.draw(m);
    this._introScene = false;
    c.setTransform(this.k, 0, 0, this.k, 0, 0);
    c.save();
    c.globalAlpha = 0.80 * fade;
    c.fillStyle = "#05040A";
    c.fillRect(0, 0, this.W, this.H);
    c.restore();

    /* the broadcast package returns with the reveal — by the bell it is at
       full strength, so the cut frame is byte-identical to a fight frame */
    if (r > 0){
      c.save();
      c.globalAlpha = eo(r);
      this.drawHud(m);
      this.drawFooter(m);
      c.restore();
    }

    c.save();
    /* the impact shakes the whole card layer, and the shake dies out */
    const sh = imp > 0 ? 30 * Math.exp(-imp * 8) : 0;
    if (sh > 0.3)
      c.translate(Math.sin(imp * 91) * sh, Math.cos(imp * 77) * sh * 0.6);

    c.save();
    c.globalAlpha = fade;
    c.textAlign = "center";
    c.font = "700 28px 'Atkinson Hyperlegible Next',sans-serif";
    c.fillStyle = "#6B5C48";
    c.fillText("SUPER WEAPON BALL: THE SUNDERED CROWN", this.W/2, 62);
    c.restore();

    /* The cards. Approach accelerates INTO the hit (ease-in), the rebound
       eases out of it, and the tape appears in the gap they leave behind —
       drawn first, so the parting cards physically uncover it. */
    const CH = IC.ch, restA = IC.margin, restB = this.H - CH - IC.margin;
    const meetA = this.H/2 - CH + 8, meetB = this.H/2 - 8;
    let yA, yB;
    if (imp <= 0){
      const k0 = clamp(e / I.clash, 0, 1), kIn = k0 * k0;
      yA = lerp(-CH - 90, meetA, kIn);
      yB = lerp(this.H + 90, meetB, kIn);
    } else {
      const k1 = eo(imp / 0.28);
      yA = lerp(meetA, restA, k1);
      yB = lerp(meetB, restB, k1);
    }
    if (r > 0){
      const k2 = Math.pow(r, 3);
      yA = lerp(restA, -CH - 90, k2);
      yB = lerp(restB, this.H + 90, k2);
    }

    if (imp > 0 && r < 1) this._introTape(m, restA + CH, restB, imp, fade);
    this._introCard(m.a, yA, CH, imp, fade);
    this._introCard(m.b, yB, CH, imp, fade);
    if (imp > 0) this._introFx(m, imp, fade);

    /* the countdown, so the cut never feels arbitrary. The seed line is
       gone (Rick: delete) — the seed still lives in the footer and on the
       result card for anyone replaying a fight. */
    c.save();
    c.globalAlpha = fade;
    const bw = 420, bx = (this.W - bw)/2, by = this.H - 74;
    c.fillStyle = "#191424"; this.roundRect(bx, by, bw, 7, 4); c.fill();
    c.fillStyle = "#C9A227"; this.roundRect(bx, by, bw * p, 7, 4); c.fill();
    c.restore();
    c.restore();
  }

  /* One fighter's card, v3 (2026-08-15): identity, silhouette, and its facts
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
    c.font = "700 64px 'Atkinson Hyperlegible Next',sans-serif";
    c.fillStyle = "#EDE3D0";
    c.fillText(f.w.name.toUpperCase(), IC.tx, y0 + 88);
    c.font = "700 25px 'Atkinson Hyperlegible Next',sans-serif";
    c.fillStyle = pal.core;
    c.fillText(f.aff.name.toUpperCase(), IC.tx + 2, y0 + 128);

    /* the weapon, fitted to the header band's art box.  v2 drew every
       silhouette at a single scale:2.2, which made the greatswords overrun
       the band and the twinblades a speck.  The box is fixed, the scale is
       whatever makes THIS weapon fill it (_artBox measures the shape rather
       than trusting its `reach`), so the art can no longer leave the card. */
    /* v4: the art turns, at the relic's OWN `spin`. The card then shows the
       stat it prints two lines below -- a fast weapon visibly turns faster --
       which a fixed pose cannot do.

       The MOTION is bounded rather than the scale. A first version fitted the
       art to its circumscribed radius so any angle was safe, and it cost 48%
       of the size on the long relics -- because a 112-unit weapon turned
       toward vertical cannot fit a 148-tall band at all. But the same
       arithmetic shows v3 ALREADY extends past artH at its own -0.38 pose, so
       the band is a layout hint and not a clip, and fitting to it was
       inventing a constraint the shipped card does not honour. The scale is
       therefore v3's, unchanged, and the ANGLE is what is kept small:

         entry   REST - 0.52 rad, easing in, arrested exactly on REST at the
                 clash -- the impact stops it, the way it stops the cards
         hold    a +-0.15 rad sway at the relic's own rate, so a fast relic
                 visibly breathes faster than a slow one and the card is alive
                 while it is being read

       Bounded sway also beats a monotone drift geometrically: a free-running
       idle at spin 3.4 would travel 2.09 rad across the hold and put the art
       somewhere its scale was never fitted for. */
    const box = this._artBox(f.w);
    const as = Math.min(IC.artMaxS, IC.artW / box.w, IC.artH / box.h);
    const REST = -0.38, rate = f.w.spin || 1.2;
    const SWEEP = 1.30, SWAY = 0.45, SWAYRATE = 0.22;
    const TRAVEL = 0.60;
    /* imp < 0 is the approach: the angle runs BACK from rest at `rate*3.2` so
       it arrives on REST at imp = 0 by construction, not by tuning. After the
       impact it holds still for 0.30s -- the clash has to read as a stop --
       then drifts. */
    const ang = imp <= 0
      ? REST - SWEEP * Math.pow(clamp(-imp / CONFIG.intro.clash, 0, 1), 0.65)
      : REST + SWAY * Math.sin(Math.max(0, imp - 0.30) * rate * SWAYRATE);
    c.save();
    c.translate(IC.artCX - as * (box.x + box.w / 2),
                y0 + IC.artCY - as * (box.y + box.h / 2));
    c.scale(as, as);
    c.rotate(ang);
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
        c.font = "800 25px 'Atkinson Hyperlegible Next',sans-serif";
        c.fillStyle = r.col;
        c.fillText(r.name, IC.tx, py + 34);
        const tw = c.measureText(r.name).width + 16;
        c.font = "500 " + r.wrap.size + "px 'Atkinson Hyperlegible Next',sans-serif";
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
      c.font = "700 20px 'Atkinson Hyperlegible Next',sans-serif";
      c.fillStyle = r.tagCol;
      c.fillText(r.tag, IC.tx, t0 + 30);
      const tw = c.measureText(r.tag).width + 16;
      c.font = "800 36px 'Atkinson Hyperlegible Next',sans-serif";
      c.fillStyle = r.col;
      c.fillText(r.name, IC.tx + tw, t0 + 30);
      if (r.chip){
        c.textAlign = "right";
        c.font = "700 22px 'Atkinson Hyperlegible Next',sans-serif";
        c.fillStyle = "#8A7F70";
        c.fillText(r.chip, IC.txr, t0 + 28);
        c.textAlign = "left";
      }
      c.font = "500 " + r.wrap.size + "px 'Atkinson Hyperlegible Next',sans-serif";
      c.fillStyle = r.ink;
      for (let j = 0; j < r.wrap.lines.length; j++)
        c.fillText(r.wrap.lines[j], IC.tx, t0 + 70 + j * 38);
      c.restore();
    });
    c.restore();
  }



/* ---- 2 of 2 ---- */
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
      c.font = "500 " + size + "px 'Atkinson Hyperlegible Next',sans-serif";
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

  /* The tale of the tape. Pairwise, not roster-normalised: each row scales
     to the larger of the two values, so "who has the edge and by how much"
     is one glance, in real units. The winning side is lit in its school
     colour; a tie lights both. RANGED prints "ANY" with a full bar — the
     bow's reach:54 is the shortest number in the game on the relic that
     hits from anywhere, and the old card already learned that lesson. */
  _introTape(m, topY, botY, imp, fade){
    const c = this.ctx, W2 = this.W / 2;
    const eo = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3);
    const A = m.a.w, B = m.b.w;
    const rangedA = !!relicShot(A), rangedB = !!relicShot(B);
    const fmt = (v, d) => d ? (Math.round(v * 10) / 10).toFixed(d)
                            : String(Math.round(v));
    const rows = [
      ["DAMAGE / HIT", A.dmg, B.dmg, 0, null, null],
      ["REACH", rangedA ? Infinity : A.reach, rangedB ? Infinity : B.reach, 0,
       rangedA ? "ANY" : null, rangedB ? "ANY" : null],
      ["SWING SPEED", A.spin, B.spin, 1, null, null],
      ["WEIGHT", A.mass, B.mass, 1, null, null],
    ];

    c.save();
    /* VS, stamped on the impact */
    const vA = clamp(imp / 0.05, 0, 1);
    if (vA > 0){
      c.save();
      c.globalAlpha = fade * vA;
      c.textAlign = "center";
      c.translate(W2, topY + 64);
      const vs = lerp(2.3, 1, eo(imp / 0.14));
      c.scale(vs, vs);
      c.font = "800 80px 'Atkinson Hyperlegible Next',sans-serif";
      c.lineWidth = 9; c.strokeStyle = "#000000CC";
      c.strokeText("VS", 0, 28);
      c.fillStyle = "#C9A227";
      c.shadowColor = "#C9A227"; c.shadowBlur = 30;
      c.fillText("VS", 0, 28);
      c.restore();
    }

    let yy = topY + 180;
    for (let i = 0; i < rows.length; i++){
      const [label, va, vb, dec, ta, tb] = rows[i];
      const bk = eo((imp - 0.08 - i * 0.07) / 0.30);
      if (bk <= 0){ yy += 84; continue; }
      const fa = va === Infinity ? 1e9 : va, fb = vb === Infinity ? 1e9 : vb;
      const mx = Math.max(va === Infinity ? 0 : va, vb === Infinity ? 0 : vb) || 1;
      const sides = [
        [m.a, va === Infinity ? 1 : va / mx, fa >= fb, ta || fmt(va, dec), -1],
        [m.b, vb === Infinity ? 1 : vb / mx, fb >= fa, tb || fmt(vb, dec),  1],
      ];
      c.save();
      c.globalAlpha = fade * bk;
      c.textAlign = "center";
      c.font = "700 27px 'Atkinson Hyperlegible Next',sans-serif";
      c.fillStyle = "#9C8F7E";
      c.fillText(label, W2, yy + 8);
      for (const [f, frac, lit, s, dir] of sides){
        /* 280-long bars and numbers pulled in to ±430: the widest value
           ("104" at 46px, "ANY" at 34px) now keeps a ≥30px margin to the
           frame edge on both sides — the first edge-pairs sheet clipped */
        const x0 = W2 + dir * 122;
        const L = Math.max(6, 280 * clamp(frac, 0, 1) * bk);
        c.globalAlpha = fade * bk * 0.55;
        c.fillStyle = "#221C30";
        this.roundRect(dir < 0 ? x0 - 280 : x0, yy - 15, 280, 13, 6); c.fill();
        c.globalAlpha = fade * bk;
        c.fillStyle = lit ? f.aff.core : "#4A4356";
        this.roundRect(dir < 0 ? x0 - L : x0, yy - 15, L, 13, 6); c.fill();
        /* the numbers count up with the bars, so the impact literally knocks
           the values out of the fighters */
        c.textAlign = dir < 0 ? "right" : "left";
        /* "ANY" is wider than any numeral and was clipping the frame edge —
           words get a smaller face than numbers */
        const isNum = /^[0-9.]+$/.test(s);
        c.font = isNum ? "800 46px 'Atkinson Hyperlegible Next',sans-serif"
                       : "800 34px 'Atkinson Hyperlegible Next',sans-serif";
        c.fillStyle = lit ? "#EDE3D0" : "#6E6378";
        const shown = isNum ? fmt(parseFloat(s) * (0.4 + 0.6 * bk), dec) : s;
        c.fillText(shown, W2 + dir * 430, yy + (isNum ? 2 : 0));
      }
      c.restore();
      yy += 84;
    }

    const hpA = eo((imp - 0.5) / 0.3);
    if (hpA > 0){
      c.globalAlpha = fade * hpA;
      c.textAlign = "center";
      c.font = "600 26px 'Atkinson Hyperlegible Next',sans-serif";
      c.fillStyle = "#7E7263";
      c.fillText(CONFIG.combat.baseHP + " HP EACH", W2, yy + 4);
    }
    c.restore();
  }

  /* The impact itself: sparks thrown SIDEWAYS out of the seam (the cards
     collided vertically, so the metal leaves horizontally — the same rule
     the clank sparks follow), a ring, and a flash along the seam. Pure
     function of imp through shellHash; nothing here can touch the sim. */
  _introFx(m, imp, fade){
    if (imp > 0.95) return;
    const c = this.ctx, cx = this.W / 2, cy = this.H / 2;
    const eo = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3);
    const H = shellHash;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round";
    const cols = ["#FFF4D0", m.a.aff.glow, m.b.aff.glow];
    for (let i = 0; i < 30; i++){
      const t2 = clamp((imp - H(7311, i) * 0.05) / 0.55, 0, 1);
      if (t2 <= 0 || t2 >= 1) continue;
      const base = i % 2 ? 0 : Math.PI;
      const ang = base + (H(7313, i) - 0.5) * 0.9;
      const spd = 620 * (0.35 + H(7317, i));
      const d = spd * 0.55 * (1 - Math.pow(1 - t2, 2.4));
      const px = cx + Math.cos(ang) * d;
      const py = cy + Math.sin(ang) * d + 40 * t2 * t2;
      c.globalAlpha = fade * (1 - t2) * 0.9;
      c.strokeStyle = cols[i % 3];
      c.lineWidth = 4.5 * (1 - t2 * 0.6);
      c.beginPath();
      c.moveTo(px, py);
      c.lineTo(px - Math.cos(ang) * 30 * (1 - t2), py - Math.sin(ang) * 30 * (1 - t2));
      c.stroke();
    }
    const t3 = clamp(imp / 0.42, 0, 1);
    if (t3 < 1){
      c.globalAlpha = fade * (1 - t3) * 0.75;
      c.strokeStyle = "#FFF4D0"; c.lineWidth = 7 * (1 - t3 * 0.7);
      c.beginPath(); c.arc(cx, cy, 24 + eo(t3) * 430, 0, TAU); c.stroke();
      c.globalAlpha = fade * (1 - t3) * 0.45;
      c.strokeStyle = "#C9A227"; c.lineWidth = 4;
      c.beginPath(); c.arc(cx, cy, 12 + eo(t3 * 0.8) * 300, 0, TAU); c.stroke();
    }
    const t4 = clamp(imp / 0.16, 0, 1);
    if (t4 < 1){
      const g = c.createLinearGradient(0, cy - 60, 0, cy + 60);
      g.addColorStop(0, "#FFF4D000"); g.addColorStop(0.5, "#FFF4D0");
      g.addColorStop(1, "#FFF4D000");
      c.globalAlpha = fade * (1 - t4) * 0.8;
      c.fillStyle = g;
      c.fillRect(0, cy - 60, this.W, 120);
    }
    c.restore();
  }

