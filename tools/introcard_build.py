#!/usr/bin/env python3
"""THE FIGHT CARD, v2 — the clash. Replaces the fade-from-black intro.

    python3 introcard_build.py --src sundered-crown.html --out sc-intro.html

WHAT CHANGES, AND WHY EACH THING
--------------------------------
Rick, 08-14: kill the fade from black and slide the cards in instead; and the
card should carry real numbers, not roster-normalised abstractions.

1. NOTHING SITS ON BLACK. A Match at t=0 already has everything needed to
   draw — fighters at their spawns, the sigil, the heraldic washes — so the
   card is now drawn over the REAL hall under an 80% scrim, and the exit is
   the scrim lifting off the room the viewer has been looking at all along.
   The phone build has run a fight behind its title card since v8 for exactly
   this reason. The hard cut is gone: the last frame of the intro IS the first
   frame of the fight, and intro_probe.py asserts that as pixels, not vibes.

2. THE CARDS ARRIVE THE WAY THE GAME TALKS. They fly in from the top and
   bottom of the frame, MEET at the centreline with a clank — sparks thrown
   sideways out of the seam, a ring, a damped shake, the clank sound — and
   rebound to their rest positions. A bind is already how this game says "two
   weapons met"; the intro now speaks the game's own language instead of
   alpha-fading like a slideshow. The clank/bell cues fire from Match.step on
   clock CROSSINGS, so a 4x-speed dt cannot double-fire them, and simulate()
   never sets introT so no sweep ever hears them.

3. THE TAPE: REAL NUMBERS, PAIRWISE. The roster-normalised bars said "more
   than him" but never HOW MUCH, and comparing them cost four saccades and a
   memory task per stat. The band between the cards is a tale of the tape:
   real value left, real value right, mirrored bars growing OUT OF THE IMPACT
   POINT, the winning side lit in its school colour and the losing side
   dimmed. Every number is read from WEAPONS/STATUS/CONFIG at draw time — the
   card has no numbers of its own to drift. relicStatus()/relicShot() remain
   the single source they became when Lightkeeper shipped a blank status line,
   the ranged REACH lie keeps its fix (RANGED prints "ANY", bar full), and the
   ultimate finally states its charge time — a real number the card has never
   shown.

WHAT DOES NOT CHANGE
--------------------
`Match.introT` still defaults to 0 and is still only ever set by presentation
layers, so simulate(), batch(), the tuner and every sweep are untouched — the
probe re-proves this with a src-vs-out A/B anyway. `CONFIG.intro.dur` stays
4.0s: the clash costs 0.46s and the reveal 0.50s, but the tape reads faster
than two separate stat blocks, so the hold is a wash and the total stays
where retention was already priced.

Anchors are cut around structure (the intro region boundaries, the step()
card clock, the draw() dispatch) — the same discipline that let the cinema
patch cross five builders untouched. Every anchor must hit exactly once or
the build refuses.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# --------------------------------------------------------------- anchors ---

CONFIG_OLD = "  intro: { dur: 4.0 },"
CONFIG_NEW = "  intro: { dur: 4.0, clash: 0.46, reveal: 0.50 },"

CONFIG_DOC_OLD = """     far too rich to infer from watching. 4s is long enough to read two stat
     blocks and short enough not to cost retention."""
CONFIG_DOC_NEW = """     far too rich to infer from watching. 4s total: the cards clash at
     `clash`, the tape reads in the hold, and the last `reveal` seconds lift
     the scrim off the hall instead of cutting."""

DISPATCH_OLD = "    if (m.introT > 0){ this.drawIntro(m); return; }"
DISPATCH_NEW = ("    if (m.introT > 0 && !this._introScene){ "
                "this.drawIntro(m); return; }")

STEP_OLD = """    if (this.introT > 0){
      this.introT -= dt;
      if (this.introT <= 0) SFX.play("seal");   // the bell, on the cut
      return;
    }"""

# During the intro the scene is the HALL, not the broadcast package: the HUD
# and footer text would double-print against the cards through the scrim
# (name up top, name on the card; seed in the footer, seed under the
# countdown). They are skipped in the scene pass and faded back in WITH the
# reveal, so the frame at the bell still equals the first fight frame exactly
# — intro_probe [2] holds to mean |diff| < 0.5 over the whole frame.
HUD_OLD = "    this.drawHud(m);"
HUD_NEW = "    if (!this._introScene) this.drawHud(m);"
FOOTER_OLD = "    this.drawFooter(m);"
FOOTER_NEW = "    if (!this._introScene) this.drawFooter(m);"

STEP_NEW = """    if (this.introT > 0){
      /* Presentation clock only — simulate() never sets introT, so no sweep
         ever runs this branch. The clank is the cards meeting at the
         centreline; the bell stays on the cut. Both fire on clock CROSSINGS
         so a 4x-speed dt cannot fire either twice. */
      const el0 = CONFIG.intro.dur - this.introT;
      this.introT -= dt;
      if (el0 < CONFIG.intro.clash &&
          CONFIG.intro.dur - this.introT >= CONFIG.intro.clash)
        SFX.play("clank", { mass: Math.max(this.a.w.mass, this.b.w.mass) });
      if (this.introT <= 0) SFX.play("seal");   // the bell, on the reveal
      return;
    }"""

# The whole intro region — drawIntro + _introPanel — is replaced between
# these two boundary lines. Cutting at the region boundary rather than inside
# the functions means any edit the region has picked up since v8 (the SHOOTS
# line, the IT GAINS direction fix) is consciously re-authored below rather
# than silently half-kept.
# Tip language — Rick's full wording pass, 08-14 (sc-wording-notes.json).
# Status tips read as an EFFECT CLAUSE because two surfaces print them: the
# card (under an "ON HIT +n NAME" line that already names the status) and the
# in-arena first-landing explainer ("NAME — tip"). A tip that repeats "apply
# N X stacks" would double-say both places, so his sentence forms live in the
# card's tag+name line and the tip carries only what the status DOES. Blanks
# in his notes are filled from the code, not guessed: hex stuns for
# STATUS.hex.stunFor (0.2s) on a timer that runs `stacks` times faster; ward
# blasts shatter:0.40 of the pool at its breaker. Curse keeps "permanently" —
# it is the only status that never expires, and dropping that would teach it
# as just another DoT. All ≤40 chars (the status contract).
TIP_EDITS = [
    ('tip:"Sears for 1.5/s a stack"',
     'tip:"Deals 1.5 damage per second per stack"'),
    ('tip:"Bleeds for 1.5/s a stack"',
     'tip:"Deals 1.5 damage per second per stack"'),
    ('tip:"Slows the swing 13% a stack"',
     'tip:"Slows swing 13%, move 6%, per stack"'),
    ('tip:"Jams the weapon shut, on a timer"',
     'tip:"0.2s weapon stun, more often per stack"'),
    ('tip:"Eats maximum life, for good"',
     'tip:"Permanently takes 13 max hp per stack"'),
    ('tip:"+11% damage taken a stack"',
     'tip:"Increases damage taken by 11% per stack"'),
    ('tip:"Shields, then shatters when broken"',
     'tip:"Hits bank a shield; 40% blast on a break"'),
    # Ult tips take his sentence forms verbatim where they were complete, with
    # numbers filled from the data where he left blanks. Widowmaker's
    # knockback (knock:200) is dropped because his note dropped it. Reprisal:
    # he asked for "___ bonus damage" — the code adds the banked ward pool as
    # FLAT damage on dmg:34, so the line spends "the ward", not a number that
    # does not exist. ≤72 chars (the v2 ult contract; was 44 for the one-line
    # card — verify.py moves with this patch).
    ('tip:"Pillar of light: 18 damage, heals 34"',
     'tip:"Pillar of light: deals 18 damage, heals 34"'),
    ('tip:"Nova: 16 damage, 3 Hemorrhage, knockback"',
     'tip:"Nova: deals 16 damage and applies 3 Hemorrhage stacks"'),
    ('tip:"Nova: 14 damage, 3 Sunder, huge knockback"',
     'tip:"Nova: deals 14 damage and applies 3 Sunder stacks — extra knockback"'),
    ('tip:"Roots them 1.6s, 10 damage, 3 Entangle"',
     'tip:"Roots for 1.6 seconds, deals 10 damage and applies 3 Entangle stacks"'),
    ('tip:"Drags them in: 14 damage, 3 Curse"',
     'tip:"Pulls target in, dealing 14 damage and applying 3 Curse stacks"'),
    ('tip:"Bolt: 20 damage, 3 Hex"',
     'tip:"Fires a bolt which deals 20 damage and applies 3 Hex stacks"'),
    ('tip:"A ring of bolts, in every direction at once"',
     'tip:"Fires a nova of arrows"'),
    ('tip:"Nova: 12 damage, wide knockback"',
     'tip:"Nova: deals 12 damage — extra knockback"'),
    ('tip:"Spends the ward as one aimed shot"',
     'tip:"Gains rotation speed, then spends the ward as bonus damage on one shot"'),
]

# The notes' language, codified across every surface it appears on — not just
# the card. The brand line lands on the page <title>, the <h1>, and the
# in-fight footer; the STATUS comment becomes the writing convention future
# relics follow, so the style Rick set today outlives this patch. The
# in-battle popup reminders (the first-landing explainer panel and the quick
# tags) read STATUS tips and names directly, so they pick the new language up
# from the same single source — probe [6] proves the longer tips still fit
# the panel.
BRAND_EDITS = [
    ("<title>The Sundered Crown</title>",
     "<title>Super Weapon Ball: The Sundered Crown</title>"),
    ("<h1>The Sundered Crown<small>six relics · one arena · no survivors"
     "</small></h1>",
     "<h1>Super Weapon Ball<small>The Sundered Crown · one arena · no "
     "survivors</small></h1>"),
    ('    const title = "T H E   S U N D E R E D   C R O W N";',
     '    const title = "SUPER WEAPON BALL: THE SUNDERED CROWN";'),
    ("""  /* `tip` is the one line a first-time viewer gets. It appears on the intro
     card, and again in the arena the first time the status actually lands, so
     someone who skipped the card still learns what the colour means. Keep them
     under ~34 characters or they will not read at phone size. */""",
     """  /* `tip` is the one line a first-time viewer gets. It appears on the fight
     card under an "ON HIT +n NAME" line, and again in the arena explainer
     panel ("NAME — tip") the first time the status lands — so a tip is an
     EFFECT CLAUSE: what the status does, verb first, numbers real, "per
     stack" for stacking effects. Never restate the name or the stack count;
     both surfaces already print them. ≤40 chars (verify.py enforces it; the
     arena panel fits ~42 at its 25px). Ult tips are full sentences — the
     card composes name > effect with numbers > cooldown — and get ≤72. */"""),
]

REGION_START = ("  /* ---------------------------------------------------"
                "---------- intro --- */")
REGION_END = "  /* One line, not two."

REGION_NEW = r'''  /* ------------------------------------------------------------- intro --- */
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
    c.font = "700 26px ui-serif,Georgia,serif";
    c.fillStyle = "#5E5140";
    c.fillText("SUPER WEAPON BALL: THE SUNDERED CROWN", this.W/2, 66);
    c.restore();

    /* The cards. Approach accelerates INTO the hit (ease-in), the rebound
       eases out of it, and the tape appears in the gap they leave behind —
       drawn first, so the parting cards physically uncover it. */
    const CH = 560, restA = 118, restB = this.H - CH - 118;
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
    const bw = 420, bx = (this.W - bw)/2, by = this.H - 86;
    c.fillStyle = "#191424"; this.roundRect(bx, by, bw, 7, 4); c.fill();
    c.fillStyle = "#C9A227"; this.roundRect(bx, by, bw * p, 7, 4); c.fill();
    c.restore();
    c.restore();
  }

  /* One fighter's card: identity, silhouette, and its facts — each fact one
     line, verb + number, cascading in after the impact. All values read live
     from the data the sim runs on; relicStatus/relicShot are the same single
     source verify.py's legibility contract calls. */
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
    c.fillText(f.w.name.toUpperCase(), 84, y0 + 96);
    c.font = "700 24px ui-sans-serif,system-ui,sans-serif";
    c.fillStyle = pal.core;
    c.fillText(f.aff.name.toUpperCase(), 86, y0 + 136);

    /* the weapon, big enough to read the silhouette */
    c.save();
    c.translate(776, y0 + 210);
    c.rotate(-0.38);
    c.scale(2.2, 2.2);
    c.shadowColor = pal.core; c.shadowBlur = 26;
    if (f.w.shape === "flail"){
      /* the same bowed chain it has in the arena, so the card shows the
         viewer the thing they are about to watch */
      const L = f.w.reach * 0.50;
      c.strokeStyle = "#6B6270"; c.lineWidth = f.w.width * 0.20; c.lineCap = "round";
      c.beginPath(); c.moveTo(-26, 0); c.quadraticCurveTo(L*0.5, 17, L, 0); c.stroke();
      c.fillStyle = "#9A93A4";
      for (let i = 1; i <= 8; i++){
        const t = i / 9, u = 1 - t;
        c.beginPath();
        c.arc(u*u*-26 + 2*u*t*(L*0.5) + t*t*L, 2*u*t*17, f.w.width * 0.13, 0, TAU);
        c.fill();
      }
      c.translate(L, 0);
      SHAPES.flailHead(c, f.w.artW, pal, 0.5);
    } else {
      const fn = SHAPES[f.w.shape];
      if (fn) fn(c, f.w.reach * 0.86, f.w.artW, pal);
    }
    c.restore();

    /* The facts. Rick 08-14: the SHOOTS line is gone (the silhouette and
       the ANY reach already say it); swing-mode relics say they TRACK (the
       one motion rule a first-time viewer cannot guess: this weapon aims
       while every other weapon spins); the ultimate reads ULTIMATE > name >
       what it does with numbers > cooldown.

       Two lines per named fact — the tag and name announce, the tip explains
       at full width. The one-line version squeezed tips to 19px and the
       longest ultimate still clipped the frame (probe [5] audits the edges
       now); 25px on its own line is the size the old card already proved at
       phone scale. */
    const facts = [];
    if (f.w.mode === "swing")
      facts.push({ tag: "", name: "TRUESTRIKE",
                   tip: "Swords track their target instead of rotating",
                   col: pal.glow });
    const rs = relicStatus(f.w);
    if (rs.def){
      /* ON HIT for self-statuses too — ward is banked by landing hits, so
         Rick's "ON HIT — gain" is what the code does. The +n is suppressed
         when the status cannot stack (ward maxStacks:1 — its onSelf value
         is a banking-rate multiplier, not a stack count, and printing
         "+2.5 WARD" taught a mechanic that does not exist). */
      const n = (f.w.onHit && f.w.onHit[rs.key]) ||
                (f.w.onSelf && f.w.onSelf[rs.key]) || 1;
      const cnt = rs.def.maxStacks > 1 ? "+" + n + " " : "";
      facts.push({ tag: "ON HIT",
                   name: (rs.self ? "GAIN " : "") + cnt +
                         rs.def.name.toUpperCase(),
                   tip: rs.def.tip, col: pal.core });
    }
    facts.push({ tag: "ULTIMATE", name: f.w.ult.name.toUpperCase(),
                 tip: (f.w.ult.tip || "") + " · " + f.w.ult.charge + "s cooldown",
                 col: "#FFF4D0" });

    let yy = y0 + CH - 22 - facts.reduce((s, r) => s + (r.name ? 74 : 44), 0);
    facts.forEach((r, i) => {
      /* cascade: each fact lands a beat after the last, after the impact */
      const a = clamp((imp - 0.20 - i * 0.09) / 0.22, 0, 1);
      const step = r.name ? 74 : 44;
      if (a <= 0){ yy += step; return; }
      c.save();
      c.globalAlpha = fade * a;
      const ry = yy + (1 - a) * 12;
      c.font = "700 19px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = "#5E5140";
      if (r.tag) c.fillText(r.tag, 86, ry + 28);
      const tw = r.tag ? c.measureText(r.tag).width + 18 : 0;
      if (r.name){
        c.font = "800 31px ui-sans-serif,system-ui,sans-serif";
        c.fillStyle = r.col;
        c.fillText(r.name, 86 + tw, ry + 28);
      }
      const tipText = r.name ? r.tip : "— " + r.tip;
      const tx = r.name ? 86 : 86 + tw;
      const ty = r.name ? ry + 62 : ry + 28;
      c.fillStyle = "#B4A996";
      let fs = 25;                       // shrink-to-fit stays as a guard
      for (;;){
        c.font = "500 " + fs + "px ui-sans-serif,system-ui,sans-serif";
        if (tx + c.measureText(tipText).width <= 1022 || fs <= 19) break;
        fs -= 1;
      }
      c.fillText(tipText, tx, ty);
      c.restore();
      yy += step;
    });
    c.restore();
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
      c.font = "800 80px ui-serif,Georgia,serif";
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
      c.font = "700 23px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = "#8A7F70";
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
        c.font = isNum ? "800 46px ui-sans-serif,system-ui,sans-serif"
                       : "800 34px ui-sans-serif,system-ui,sans-serif";
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
      c.font = "500 22px ui-sans-serif,system-ui,sans-serif";
      c.fillStyle = "#5E5140";
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

'''


def apply(text: str, old: str, new: str, name: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"! anchor for {name} appears {n} times, expected 1.\n"
                         f"  The source has moved under this builder. Diff "
                         f"before re-anchoring — do not loosen the anchor.")
    print(f"  [introcard] {name}")
    return text.replace(old, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sundered-crown.html")
    ap.add_argument("--out", default="sc-intro.html")
    ap.add_argument("--no-check", action="store_true",
                    help="skip loading the output in a browser (do not)")
    a = ap.parse_args()

    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    src = HERE / a.src
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr)
        return 2
    text = src.read_text(encoding="utf-8")
    before = len(text)

    # The one-line anchors go FIRST: the new intro region itself calls
    # drawHud/drawFooter (the reveal fade-in), so patching them after the
    # region lands would find two occurrences and correctly refuse.
    text = apply(text, HUD_OLD, HUD_NEW, "scene pass skips the HUD")
    text = apply(text, FOOTER_OLD, FOOTER_NEW, "scene pass skips the footer")

    # the intro region, replaced between its structural boundaries
    for name, anc in (("region start", REGION_START), ("region end", REGION_END)):
        if text.count(anc) != 1:
            raise SystemExit(f"! anchor for {name} appears {text.count(anc)} "
                             f"times, expected 1")
    i0 = text.index(REGION_START)
    i1 = text.index(REGION_END)
    if i1 <= i0:
        raise SystemExit("! intro region boundaries are out of order")
    text = text[:i0] + REGION_NEW + text[i1:]
    print("  [introcard] drawIntro/_introPanel region replaced "
          "(clash + tape + reveal)")

    text = apply(text, CONFIG_OLD, CONFIG_NEW, "CONFIG.intro gains clash/reveal")
    for old, new in TIP_EDITS:
        text = apply(text, old, new, f"tip: {new.split(':', 1)[1]}")
    for i, (old, new) in enumerate(BRAND_EDITS):
        text = apply(text, old, new,
                     ["page <title>", "page <h1>", "in-fight footer",
                      "the tip-writing convention, codified"][i])
    text = apply(text, CONFIG_DOC_OLD, CONFIG_DOC_NEW, "CONFIG.intro comment")
    text = apply(text, DISPATCH_OLD, DISPATCH_NEW,
                 "draw() reentry guard (the scene behind the scrim)")
    text = apply(text, STEP_OLD, STEP_NEW, "step(): clank on the clash crossing")

    stamp = "<!-- GENERATED by introcard_build.py — edit the builder, not this file -->\n"
    if not text.startswith("<!-- GENERATED"):
        text = stamp + text

    out = HERE / a.out
    out.write_text(text, encoding="utf-8")
    print(f"{a.src} -> {a.out}   {before} -> {len(text)} bytes")

    if a.no_check:
        return 0

    # v12 rule: a patcher must open its own output.
    from scpage import game
    with game(game_path=out.resolve()) as (pg, errs):
        bad = pg.evaluate("""() => {
          const out = [];
          AC.setResolution(1080, 1920);
          AC.SFX.play = function(){}; AC.SFX.resume = function(){};
          const ids = AC.WEAPONS.map(w => w.id);
          /* draw every phase of the card for a melee pair, a ranged pair and
             a self-status pair — the three card layouts that exist */
          const pairs = [[ids[0], ids[2]]];
          const ranged = AC.WEAPONS.find(w => w.mode === "ranged");
          const self2  = AC.WEAPONS.find(w => w.onSelf);
          if (ranged) pairs.push([ranged.id, ids[4] || ids[1]]);
          if (self2)  pairs.push([self2.id, ids[1]]);
          for (const [ia, ib] of pairs){
            try {
              const m = new AC.Match(ia, ib, 4242);
              AC.__inject(m);
              for (const e of [0.001, 0.2, 0.45, 0.47, 0.6, 0.9, 1.6, 2.8,
                               3.55, 3.8, 3.99]){
                m.introT = AC.CONFIG.intro.dur - e;
                AC.__draw(m);
              }
              m.introT = 0; AC.__draw(m);
            } catch (err){ out.push(ia + " vs " + ib + ": " + err.message); }
          }
          return out;
        }""")
        if errs or bad:
            print("! PAGE ERRORS:\n  " + "\n  ".join(errs + bad), file=sys.stderr)
            return 1
    print("  check: every card phase drawn for melee / ranged / self-status "
          "pairs, no exceptions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
