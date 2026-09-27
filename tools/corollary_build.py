#!/usr/bin/env python
"""AXIOM / COROLLARY, REDESIGNED -- every blow is followed by its corollary. v88.

Built from `06-docs/v80/axiom-corollary-redesign-v80.md` §5 (Cowork,
2026-09-26) and its §7 rulings, which are the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision. Every number below is
the doc's or Rick's, and where the doc says it in words the words win over the
lab (`overlays/corollary.js`) -- see THE READINGS below.

    stage 1   the echo, no hex       sc-leaf -> sc-echo.html
    stage 2   the hex                sc-echo -> sc-corollary.html
    stage 3   the blade              7.42 KEPT -- Rick, 2026-09-26 (no link)
    stage 4   picture, voice, beat   (not written yet)

§1: "For a duration every blow Axiom lands is followed by its corollary: half
a second later a rune-echo of the same blow strikes the enemy again, for the
same damage, wherever it has got to -- as long as it is still within reach of
the sword -- and the echo hexes."

THE WINDOW. Charge 16, window 8 -- Rick, 2026-09-26 (v80 §7). The doc stated
neither, and those are the numbers every run in `06-docs/v80/runs/` was priced
at. The shipped bolt was charge 13.

THE BLADE. 7.42, unchanged -- Rick, 2026-09-26, after stage 3 measured that it
does not hold parity with the bolt on 151 (34.1 against 40.2 at 1320 a side).
He kept the blade over the parity.

THE READINGS, where the lab and the prose part and the prose is built:
  1. "A queued echo past the window still lands (it was earned)" -- §4. The lab
     clears its queue at window close. Here the queue outlives the window.
  2. "no crit" -- §4 -- and "Whether the echo should carry the blow's crit (it
     does not)" -- §6.3. The lab copies `me.dealt`, crit included. Here a crit
     blow's echo is its damage as dealt with EXACTLY the crit's extra taken
     out: `dmg - (dmgBase - dmgNoCrit)`, where `dmgNoCrit` is the same blow
     rounded before the multiply. (The first build divided by critMul, which
     is off by one on about one crit echo in eight -- found in review.)
  3. THE TARGET IS THE FOE. §4 writes `hurt(foe, dmg, f)` and "the foe within
     200 + R of Axiom", and the lab resolves every echo on the real opponent.
     A blow Axiom lands on one of Twinshade's shades therefore echoes onto
     Twinshade. (The first build sent it to the shade it hit, which the doc
     does not say, and which let an echo land on a shade that had already
     rejoined -- found in review. Two sources agree on the foe; that is built.)

THE CLOCK. The window, the half second and the charge all run on the window
tickers' clock, which stops through a hit stop exactly as `tickWinnow`'s and
`tickCharge`'s do. The lab counted wall steps, freezes included. That is the
engine's convention and not a reading of the doc: the built relic casts ~3.6
times a fight where the lab's fixed schedule gave ~4.2, and an echo lands 0.5s
of FIGHT after its blow -- a median 0.675s on the match clock, because the
blow's own hit stop always falls inside the half second.

THE BASE IS `sc-leaf.html`, named and asserted: the build of record since
Rick passed its gate 4 on 2026-09-26 ("I approve the Thornshear fix"). 34
relics, the minute pace, Starwarden, Crossweave's nova, and the Winnowing's
rung stop.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "axiom"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v80 §1/§4 and
# Rick's §7. None of them is bisected here.
ULT = {
    "charge": 16,     # Rick, v80 §7 -- the number it was priced at
    "dur": 8,         # Rick, v80 §7 -- the number it was priced at
    "delay": 0.5,     # §1 "half a second later"
    "reach": 200,     # §1/§4 "within 200 + R of Axiom"; §6.2 kept as written
    "hex": 1,         # §1 "and the echo hexes"; §4 `apply("hex", 1, f)` -- stage 2
}
TIP = "Every blow is followed by its corollary: the same blow again, hexing"

SHIPPED_ULT = '''    ult:{ name:"Corollary", charge:13, kind:"bolt", dmg:18, apply:{hex:3},
          tip:"Deals 18 damage and applies 3 Hex stacks" },'''


def ult_block(hex_: int) -> str:
    return (f'''    ult:{{ name:"Corollary", charge:{ULT["charge"]}, kind:"echo", dur:{ULT["dur"]},
          delay:{ULT["delay"]}, reach:{ULT["reach"]}, hex:{hex_},
          tip:"{TIP}" }},''')


def ult_mid(hex_: int) -> str:
    """The one line stage 2 changes -- its own row, so chain_audit's marker for
    stage 2 is the line that carries the hex and not a line both stages share."""
    return f'''          delay:{ULT["delay"]}, reach:{ULT["reach"]}, hex:{hex_},\n'''


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse."""
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def strip_comments(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will (CLAUDE.md 4.11)."""
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        print("  WARN  no `node` on PATH -- output NOT syntax checked.")
        return
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not "
                                 "parse.\n  "
                                 + "\n  ".join((r.stderr or "").strip()
                                               .splitlines()[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


# ---------------------------------------------------------------- stage 1 --
S1 = [

("axiom's ultimate is the echo",
 SHIPPED_ULT,
 ult_block(0)),

("the fighter carries the echo's window",
 '''    this.ultWinnow = null;
    /* {t, dur, blows, figures, refused, sprung} while DEADFALL''',
 '''    this.ultWinnow = null;
    /* {t, dur, q} while COROLLARY's window is open, AND AFTER IT CLOSES UNTIL
       THE LAST QUEUED ECHO HAS RESOLVED -- v80 §4, "a queued echo past the
       window still lands (it was earned)". null on every other relic and on
       this one outside that span, which is the zero-burden argument:
       `tickEcho` returns after a two-iteration loop that does nothing, and the
       one line in `resolveHit` is a truthiness test on a field no other relic
       carries. `echoTally` is the probe's count, cumulative over the fight;
       nothing in the simulation reads it. */
    this.ultEcho = null;
    this.echoTally = null;
    /* {t, dur, blows, figures, refused, sprung} while DEADFALL'''),

("the cast opens the window and resolves nothing",
 '''    /* An aimed shot does not resolve in this frame -- it starts a DRAW, and''',
 '''    if (u.kind === "echo"){
      /* COROLLARY. NOTHING RESOLVES HERE: the cast changes what a landed blow
         IS for `u.dur` seconds, the same shape as the Winnowing and the
         Thicket. Every blow Axiom lands while the window is open queues its
         corollary in `resolveHit`, and `tickEcho` pays it `u.delay` later.

         THE BOLT IS GONE, and with it the cast's own damage and its three
         hex: v80's "bolt out". Spellbreaker's Unmaking still uses `kind:
         "bolt"`, so none of that code moves.

         A CAST CANNOT LAND ON A RUNNING QUEUE AT THE SHIPPED NUMBERS -- charge
         16 against a window of 8 and a delay of 0.5 -- and if those numbers
         ever move, the unresolved echoes are carried onto the new clock
         rather than dropped, because they were earned. */
      const prev = f.ultEcho;
      f.ultEcho = { t: 0, dur: u.dur, q: [] };
      if (prev) for (const q of prev.q)
        f.ultEcho.q.push(Object.assign({}, q, { at: q.at - prev.t }));
      if (!f.echoTally)
        f.echoTally = { casts: 0, blows: 0, echoes: 0, landed: 0, dealt: 0,
                        hex: 0, crits: 0 };
      f.echoTally.casts++;
      return;
    }

    /* An aimed shot does not resolve in this frame -- it starts a DRAW, and'''),

("the blow is also priced with no crit",
 '''    if (crit){ dmg *= forge ? C.critMul + self.w.ult.critMulPer * forge.n : C.critMul; self.crits++; }
''',
 '''    /* THE SAME BLOW WITH NO CRIT, rounded the way the blow is rounded on the
       next line but one. Corollary's echo is "the blow's damage as dealt"
       with "no crit" (v80 §4, §6.3), and this is the only line in the engine
       that still knows what the blow was before the multiply. A const with
       no side effect: every other relic's blow is byte-identical, and
       `engine_ab` over the other 33 is the proof. */
    const dmgNoCrit = Math.round(dmg);
    if (crit){ dmg *= forge ? C.critMul + self.w.ult.critMulPer * forge.n : C.critMul; self.crits++; }
'''),

("a blow landed in the window queues its corollary",
 '''    this.hurt(foe, dmg, self);
    foe.flash = 1;
    foe.ringFlash = 1;
    self.hits++; self.dealt += dmg;
''',
 '''    this.hurt(foe, dmg, self);
    foe.flash = 1;
    foe.ringFlash = 1;
    self.hits++; self.dealt += dmg;
    /* COROLLARY'S QUEUE. HERE, BESIDE `self.hits++`, BECAUSE THIS LINE IS WHAT
       "A BLOW LANDED" MEANS IN THIS ENGINE -- verify's six-hit floor counts it
       and the lab counted it. Only while the window is OPEN; the queue itself
       outlives the window (see `tickEcho`).

       THE ECHO IS "THE BLOW'S DAMAGE AS DEALT" (v80 §4) -- this `dmg`, the
       number `hurt` was just handed, after the wall and before the ward --
       WITH NO CRIT: §4 says "no crit" and §6.3 says the echo does not carry
       the blow's. So a crit blow's echo has exactly the crit's extra taken
       out, `dmgBase - dmgNoCrit`, and never goes below zero. The lab copied
       the crit; the prose is built.

       THE TARGET IS THE FOE -- Axiom's opponent, as §4 writes it and the lab
       priced it -- and not whatever body the blow landed on. A blow on one of
       Twinshade's shades echoes onto Twinshade.

       `ox, oy` is where on the struck body the blow landed and `bear` the
       bearing it came from -- stage 4's rune and ghost sweep, stored now
       because this is the only frame that knows them. Nothing in the
       simulation reads them. */
    if (self.ultEcho && self.ultEcho.t < self.ultEcho.dur){
      self.ultEcho.q.push({ at: self.ultEcho.t + self.w.ult.delay,
                            dmg: crit ? Math.max(0, dmg - (dmgBase - dmgNoCrit)) : dmg,
                            tgt: self === this.a ? this.b : this.a,
                            ox: hx - foe.x, oy: hy - foe.y,
                            bear: Math.atan2(self.y - foe.y, self.x - foe.x) });
      self.echoTally.blows++;
      if (crit) self.echoTally.crits++;
    }
'''),

("the echo ticks with the window tickers",
 '''    this.tickAegis(dt);
    for (const [self, foe] of [[this.a, this.b], [this.b, this.a]])
      this.tickHits(self, foe, dt);''',
 '''    this.tickAegis(dt);
    /* WITH THE OTHER WINDOW TICKERS, on the normal step path, so it freezes
       through a hit stop exactly as they do -- the half second is half a
       second of FIGHT. Before `tickHits`, for the reason `tickWinnow` gives:
       a corollary resolved against last frame's positions would be testing
       where the foe used to be. */
    this.tickEcho(dt);                  // COROLLARY (v80)
    for (const [self, foe] of [[this.a, this.b], [this.b, this.a]])
      this.tickHits(self, foe, dt);'''),

("tickEcho pays the corollary",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE COROLLARY ==
     v80 §4: at `at`, if both alive and the foe within `reach` + R of Axiom,
     `hurt(foe, dmg, f)` -- ward first; NO crit, NO sunder multiplier, NO
     knock, NO hit stop: "the echo is a rune, not a swing" -- and
     `foe.apply("hex", hex, f)`.

     `hurt` IS THE WHOLE OF IT, AND THAT IS WHAT MAKES THOSE FOUR NOs TRUE.
     Crit, sunder, knock, hit stop and hitstun all live in `resolveHit`; an
     echo that went through it would be a second swing. What `hurt` does
     carry is the WARD'S own rule: an echo that empties a ward shatters it,
     and the shatter bursts, knocks the attacker, sets its 0.10 stop and
     throws 40 sparks off the match stream -- exactly as it does for any
     other damage that breaks a ward.

     THE QUEUE OUTLIVES THE WINDOW. §4: "A queued echo past the window still
     lands (it was earned)" -- so the state is dropped only when the clock is
     past `dur` AND the queue is empty. The lab dropped it at the close.

     THE TARGET IS THE FOE, Axiom's opponent, always -- set at the queue. */
  tickEcho(dt){
    for (const f of [this.a, this.b]){
      const E = f.ultEcho;
      if (!E) continue;
      E.t += dt;
      const u = f.w.ult, T = f.echoTally;
      while (E.q.length && E.q[0].at <= E.t){
        const q = E.q.shift(), tgt = q.tgt;
        T.echoes++;
        if (!f.alive || !tgt.alive) continue;
        if (Math.hypot(tgt.x - f.x, tgt.y - f.y)
            >= u.reach + CONFIG.physics.ballR) continue;
        T.landed++;
        const before = tgt.hp + tgt.shield;
        this.hurt(tgt, q.dmg, f);
        T.dealt += before - (tgt.hp + tgt.shield);
        if (u.hex > 0){ tgt.apply("hex", u.hex, f); T.hex += u.hex; }
        /* THE NUMBER, in the runic glow (§4 picture). `float` pushes to a
           list and draws no random number, so it moves no fight. */
        if (q.dmg >= 1)
          this.float(tgt.x, tgt.y - 50, q.dmg, f.aff.glow, 22 + q.dmg * 0.5);
      }
      if (E.t >= E.dur && !E.q.length) f.ultEcho = null;
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the echo hexes",
 ult_mid(0),
 ult_mid(ULT["hex"])),

]


# ---------------------------------------------------------------- stage 4 --
# PICTURE, VOICE, THE ECHO BEAT, THE FIELD. v80 §4 PICTURE/SOUND and §5 stage 4.
# Rick, 2026-09-26: "you pick i overrule" -- every open choice below is Code's,
# made on a measurement recorded in v88 §6, and Rick overrules from one clip.
#
# NOTHING HERE MAY MOVE A FIGHT. `echoShown` is called from `tickEcho`, which is
# on the sim path, so everything it does is write-only presentation: SFX.play
# (a no-op headless, plain-number opts), beat() (write-only), `finisher`
# (decays with the sim, read only by the renderer), `m.ultFx` (read only by
# presentation) and the picture's own record list. `engine_ab` WITH AXIOM IN
# THE ROSTER is the proof, and the builder refuses any insert that draws the
# match RNG.

# THE BOLT'S FIELD OUT, THE ECHO'S IN -- one edit, both copies (`sync_fx`).
FX_OLD = '''    axiom: { mode: 'beam', n: 1200, sp: [40, 190], grav: -40, drag: 1.6,
             life: [0.28, 0.72], heavy: 0.0, size: [0.6, 1.8],
             spawn: 0.35, up: 0 },
'''
# The rune motes (v80 §4 "Field: rune motes on each echo, both copies"). The
# row is the picture's pick (v88 §6); the key is not a relic id because the
# field is armed at an ECHO, not at the cast -- the cast arms `w:"axiom"`,
# which now has no spec and so no field, which is "the bolt's field spec out".
FX_ECHO = '''    /* COROLLARY'S RUNE MOTES -- ON EACH LANDED ECHO, NOT AT THE CAST (the
       bolt's beam field is out). A small burst at the rune's seat, drawn at
       [u.tx, u.ty] because it is a burst without `atSelf`. Its births are
       SPREAD OVER THE FLARE (spawn 0.50 = 0.25s), so the field peaks after the
       ghost blade has gone rather than on its frames: that is what keeps the
       echo's peak frame inside the app's 4.77 ms of headroom. */
    'axiom-echo': { mode: 'burst', n: 200, sp: [20, 120], grav: -60, drag: 1.8,
                    life: [0.50, 1.30], heavy: 0.0, size: [0.6, 1.7],
                    spawn: 0.50, up: 25 },
'''
# m.ultFx.life for an echo's motes, in the presentation clock's half-seconds:
# at least the spec's spawn 0.50 + longest life 1.30 (v88 §6c).
ECHO_FX_LIFE = 1.9

# THE VOICES -- corollary_voice_lab.py's picks (v88 §6b): BAR, MIRROR, SNAP.
VOICE_CAST_ARM = '''        } else if (w === "axiom"){                      // the edge lights
          /* COROLLARY -- A RUNE-CHIME, 0.3s (v80 §4 SOUND), picked on the
             numbers under Rick's "you pick i overrule" by
             `corollary_voice_lab.py` (BAR, of four). Axiom had no arm and
             fell through to rune-crack, the fallback ten other relics still
             use -- so this ADDS an arm and leaves that one alone.

             ONE STRUCK BAR. The partials are a free bar's modes (1 : 2.76 :
             5.40 on 1319 Hz), which is what makes it a CHIME and not a note;
             the 20 ms tick at 5.2 kHz is the mallet and the sine an octave
             under is the body. Audible 300 ms by the lab's declared
             definition (5 ms RMS above 2% of its own loudest window), peak
             0.364 at 7 ms, register against rune-crack 0.35 -- the crack and
             the falling square are both gone. */
          this._burst(t, { freq: 5200, q: 2.0, gain: 0.09, dur: 0.020,
                           type:"bandpass" });
          [[1319, 1.00], [3640, 0.42], [7123, 0.16]].forEach(([fq, k]) =>
            this._tone(t, { freq: fq, to: fq * 0.996, gain: 0.15 * k,
                            dur: 0.51, type:"triangle" }));
          this._tone(t, { freq: 659, to: 656, gain: 0.07, dur: 0.40,
                          type:"sine" });
        } else if (w === "axiom-echo"){                 // the corollary lands
          /* THE ECHO -- "the sword's own strike voice, reversed (a rising
             'whoom'), quieter" (v80 §4). MIRROR, of five, from
             `corollary_voice_lab.py`.

             THE STRIKE VOICE IS `hit`, and these are its own numbers at the
             echo's own damage (`hw` and not `w`: here `w` is the relic id).
             Run backwards, its sine RISES 46 Hz -> tf while it SWELLS, and its
             noise band swells in over its burst length, both topping out td
             after the echo lands -- 0.13-0.17 s across the echo's damage,
             which is the drawn 0.15 s ghost sweep.

             NOT A LITERAL REVERSAL, AND IT CANNOT BE: reversing samples needs
             an async render, and `cinema_clip` / `render.py` rebuild this synth
             synchronously with `Object.create`, so a cached buffer would be
             SILENT in every clip. It is built from `_tone` instead -- and
             `_tone` only decays (CLAUDE.md 4.5), so the swell is struck again
             at every one of the chirp's own CYCLE STARTS: each strike begins at
             phase 0 where the chirp is at phase 0 and rides the same pitch
             curve, so they sum into ONE rising sine, not a flutter. Measured
             against the literal reversal: register 0.98 against the hit
             (literal 1.00), energy centre late (0.60 of its span), one swell,
             -6 dB under the hit in short-term level on every noise draw
             (0.50-0.53) -- quieter, and the same distance quieter at every
             damage it lands at, because it scales as the hit does.

             Deterministic: no random draw, and the noise band is wide (q 1.1,
             the hit's own) so its level barely moves between sessions. */
          const hw = clamp((p.dmg || 10) / 45, 0.12, 1);
          const tf = 190 - 90 * hw, tg = 0.22 + 0.26 * hw, td = 0.11 + 0.13 * hw;
          const nf = 2600 - 1500 * hw, ng = 0.16 + 0.20 * hw, nd = 0.06 + 0.06 * hw;
          const r = tf / 46, L = Math.log(r);
          const c0 = Math.ceil(46 * td / L * (Math.pow(r, 0.45) - 1));
          const c1 = Math.floor(46 * td / L * (r - 1));
          for (let c = c0; c <= c1; c++){
            const s = td / L * Math.log(1 + c * L / (46 * td));
            this._tone(t + s, { freq: 46 * Math.pow(r, s / td),
                                to: 46 * Math.pow(r, (s + 0.05) / td),
                                gain: tg * 0.30 * Math.pow(10, -34 * (1 - s / td) / 20),
                                dur: 0.05, type:"sine" });
          }
          this._sweep(t + td - nd, { f0: nf * 0.6, f1: nf * 1.25, q: 1.1,
                                     gain: ng * 0.45, dur: nd / 0.6, atk: nd,
                                     type:"bandpass" });
'''
VOICE_CALLS = '''      SFX.play("ult", { w: "axiom-echo", dmg: q.dmg });   // the strike, reversed
      if (f.w.ult.hex > 0) SFX.play("hex-snap");            // the hex -- its snap
'''

# THE PICTURE -- the picture lab's picks (v88 §6c). One statement in echoShown
# for every shown echo (landed or missed), and its own edits.
PICTURE_PUSH = '''    { const X = this.echoFx; X.push({ src: f, tgt, ox: q.ox, oy: q.oy, bear: q.bear, sw: q.sw, dd: q.dd, landed, t: 0, life: landed ? 0.5 : 0.8 }); if (X.length > 24) X.shift(); }
'''
PICTURE_ROWS = [

('''picture: the ghost needs the blow’s swing and distance''',
 '''                            bear: Math.atan2(self.y - foe.y, self.x - foe.x) });
''',
 '''                            bear: Math.atan2(self.y - foe.y, self.x - foe.x),
                            sw: (self.w.mode === "swing" ? Math.cos(self.swingPhase) : 1) * self.spinDir < 0 ? -1 : 1,
                            dd: Math.hypot(self.x - foe.x, self.y - foe.y) });
'''),

('''picture: Fighter: echoFade''',
 '''    this.ultEcho = null;
    this.echoTally = null;
''',
 '''    this.ultEcho = null;
    this.echoTally = null;
    /* COROLLARY'S RUNE LINE, the fade of it: 1 while the window is open,
       eased to 0 over 0.45s after it closes. On the FIGHTER and not on
       `m.ultFx` for v54 section 2a's measured reason (one slot; the opponent's
       cast takes it). Presentation only -- nothing in the simulation reads it,
       and it is driven in `tickPresentation`. */
    this.echoFade = 0;
'''),

('''picture: Match: echoFx''',
 '''    this.sigilFlash = [];
''',
 '''    this.sigilFlash = [];
    /* AND COROLLARY'S RESOLVED ECHOES: the flare and the ghost of the blade
       for a landed one, the broken rune for a miss. A RECORD, NOT A PARTICLE
       FIELD, pushed in `tickEcho`, aged in `tickPresentation`, drawn by
       `drawEcho` and `drawEchoGhost`, emptied at the end of the match in
       `decay`. It exists because `tickEcho` shift()s the queue and nulls
       `f.ultEcho` on the tick the last echo resolves, so a picture read off the
       queue alone would lose every flare. Nothing in the simulation reads it. */
    this.echoFx = [];
'''),

('''picture: tickPresentation: echoFade''',
 '''      f.coronaFade = f.ultCorona ? 1
                   : Math.max(0, f.coronaFade - dt / 0.4);
''',
 '''      f.coronaFade = f.ultCorona ? 1
                   : Math.max(0, f.coronaFade - dt / 0.4);
      /* AND THE RUNE LINE'S. Up instantly, down over 0.45s -- the Breach
         licence's own numbers. The WINDOW is `E.t < E.dur`: the state itself
         outlives the window while late echoes are still queued, and the line,
         which is the window's tell, does not. Nor does it outlive the match:
         `tickEcho` never runs again once `over` is set, so a window open at the
         kill would otherwise hold the line lit through the whole verdict. */
      f.echoFade = (!this.over && f.ultEcho && f.ultEcho.t < f.ultEcho.dur) ? 1
                 : Math.max(0, f.echoFade - dt / 0.45);
'''),

('''picture: tickPresentation: echoFx''',
 '''      if (b.t >= b.life) this.sigilFlash.splice(i, 1);
    }
''',
 '''      if (b.t >= b.life) this.sigilFlash.splice(i, 1);
    }
    /* COROLLARY'S RESOLVED ECHOES. `life` IS IN HALF-SECONDS like every
       other clock in this method: the flare is 0.5 (0.25s), the ghost's sweep
       0.30 (v80's 0.15s), a miss 0.8 (0.4s). On THIS clock and not the sim's,
       so an echo that shatters a ward -- the one echo that sets a stop -- still
       plays its flare through the freeze. */
    for (let i = this.echoFx.length - 1; i >= 0; i--){
      const e = this.echoFx[i];
      e.t += dt;
      if (e.t >= e.life) this.echoFx.splice(i, 1);
    }
'''),

('''picture: decay: echoFx at match end''',
 '''    if (this.over && this.tornado) this.tornado = null;
''',
 '''    /* AND COROLLARY'S RECORDS END WITH THE MATCH. They age on the
       presentation clock, which keeps running under the verdict, so a KILLING
       echo's flare and ghost still play out (0.25s at most) -- three of seven
       Axiom wins in the stage-3 sample ended on an echo. This empties the list
       before the panel. The PENDING runes need nothing here: `drawEcho` stops
       drawing them the frame `over` is set, because `tickEcho` never runs again
       and they would otherwise sit frozen on the foe through the whole 2.4s. */
    if (this.over && this.echoFx.length && (this.resultT || 0) > 0.5)
      this.echoFx.length = 0;
    if (this.over && this.tornado) this.tornado = null;
'''),

('''picture: draw: ghost, world pass over the fighters''',
 '''    this.drawFighter(m, m.a);
''',
 '''    this.drawFighter(m, m.a);
    /* COROLLARY'S GHOST BLADE, OVER BOTH FIGHTERS: it sweeps THROUGH the foe,
       and a blade drawn with the fighters is swallowed by the very shell it is
       crossing (the weapon is clipped by the other relic's shell). World pass,
       like `drawSpectre`: a solid greatsword stays out of the bloom. */
    this.drawEchoGhost(m);
'''),

('''picture: draw: runes + line, emissive pass over the fighters''',
 '''    this.drawCrackle(m, true);
''',
 '''    /* COROLLARY'S RUNES, THEIR FLARE, AND THE RUNE LINE: on the shell and on
       the blade, so over both balls; light, so in this pass. */
    this.drawEcho(m);
    this.drawCrackle(m, true);
'''),

('''picture: Renderer: the Corollary methods''',
 '''  drawSigils(m){
''',
 '''  /* ==== COROLLARY, DRAWN (v80 §4) =========================================
     "On a landed blow a rune is stamped on the foe at the hit point (runic
     core, r 12); at +0.5s it FLARES and a ghost of Axiom's blade sweeps
     through the foe from the same bearing the blow came from (drawn, 0.15s,
     alpha 0.5) ... Cast: the blade's edge lights with a rune line."

     THE RUNE is the charge sigil's inner figure -- "what follows", a triangle
     in a ring -- and not `_glyph`, which is Unmaking's rune: a Spellbreaker v
     Axiom fight would otherwise stamp one mark for two ultimates (ULT SIGILS'
     rule 9). Its apex points the way the blow travelled.
     IT IS SEPARATED BY VALUE, NOT HUE: runic core on a runic foe is the same
     colour, so the stroke carries the school's dark as an outline (Starwarden's
     lesson, v66 §3b). `lighter` measured a quarter of the legibility on a
     white sanctified shell (v88 §6).
     SEATED ON THE SHELL: the hit point sits on the rim (a median 39 from
     the centre over 24 blows, against ballR 34), so a rune centred there
     hangs half off the ball; it is pulled in along the same direction to 20,
     where its outline meets the rim.
     WHILE PENDING a clock runs round it, so the half second is visible and the
     flare arrives as the ring closes. AT RESOLUTION it flares -- expands,
     whitens and goes -- and the ghost sweeps. A MISS (out of reach) loses its
     inner figure at once and the ring breaks into three arcs that part and
     drop: the rune failing, not the picture failing, with no flare, no ghost
     and no number.

     TWO PASSES. `drawEchoGhost` is the WORLD pass (a solid greatsword; see
     `drawSpectre`), drawn over both fighters because a blade drawn with them
     is clipped by the shell it is going through. `drawEcho` is the EMISSIVE
     pass, over both fighters. Neither reads `m.ultFx`.

     PRESENTATION ONLY: no rng, no spawnFx, no Math.random, and nothing here
     writes a field the simulation reads. */
  _echoSeat(tgt, ox, oy){
    const d = Math.hypot(ox, oy), s = d > 20 ? 20 / d : 1;
    return [tgt.x + ox * s, tgt.y + oy * s];
  }

  _echoPath(c, r){
    c.beginPath();
    c.arc(0, 0, r, 0, TAU);
    for (let i = 0; i < 3; i++){
      const a = i * TAU / 3, px = Math.cos(a) * r * 0.62, py = Math.sin(a) * r * 0.62;
      if (i) c.lineTo(px, py); else c.moveTo(px, py);
    }
    c.closePath();
  }

  _echoRune(c, x, y, rot, r, col, dark){
    c.save();
    c.translate(x, y); c.rotate(rot);
    c.globalAlpha = 1;
    c.lineCap = "round"; c.lineJoin = "round";
    c.strokeStyle = dark; c.lineWidth = 5.2;
    this._echoPath(c, r); c.stroke();
    c.strokeStyle = col; c.lineWidth = 2.0;
    this._echoPath(c, r); c.stroke();
    c.restore();
  }

  drawEchoGhost(m){
    const F = m.echoFx;
    if (!F || !F.length) return;                               // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const e of F){
      if (!e.landed || e.t >= 0.30) continue;                  // 0.15s, half-seconds
      const k = e.t / 0.30, f = e.src, tgt = e.tgt;
      const L = f.w.reach * m.actMods.reach * f.reachMul + 6;
      /* A VIRTUAL AXIOM on the bearing the blow came from, at the blow's own
         distance -- held so the foe's centre falls in the blade's body (40-75%
         of its length), and swept in the blow's own direction through a
         half-arc that starts and ends clear of the shell. */
      const D = clamp(e.dd, R - 6 + L * 0.40, R - 6 + L * 0.75);
      const ang = e.bear + Math.PI + e.sw * 0.75 * (2 * k - 1);
      c.save();
      c.globalAlpha = 0.5 * Math.min(1, (1 - k) / 0.25);
      c.translate(tgt.x + Math.cos(e.bear) * D, tgt.y + Math.sin(e.bear) * D);
      c.rotate(ang);
      c.translate(R - 6, 0);
      if (!litWeapon(c, f.w.shape, L, f.w.artW, f.aff, f.drawK, ang)){
        const fn = SHAPES[f.w.shape];
        if (fn) fn(c, L, f.w.artW, f.aff, f.drawK);
      }
      c.restore();
    }
  }

  _echoLine(m, f){
    const fade = f.echoFade * (f.stun > 0 ? 0.42 : 1);
    if (fade < 0.02) return;
    const c = this.ctx, R = CONFIG.physics.ballR, A = f.aff, E = f.ultEcho;
    const run = E && E.t < 0.25 ? E.t / 0.25 : 1;       // it lights hilt to tip
    const L = f.w.reach * m.actMods.reach * f.reachMul + 6;
    const bw = f.w.artW * 0.34;
    /* ONE EDGE OF `_gsConjured`, inset: from the first shard to the point.
       Not the axis -- `_shatter` already runs a hairline down the axis, and a
       rune line that could not be told from it would be no tell at all. */
    const P = [[R - 6 + L * 0.30, -bw * 0.80], [R - 6 + L * 0.86, -bw * 0.64],
               [R - 6 + L * 0.99, -bw * 0.06]];
    const foe = f === m.a ? m.b : m.a;
    c.save();
    if (foe.alive){                    // occluded by the foe's shell, as the blade is
      c.beginPath();
      c.rect(-4000, -4000, 8000, 8000);
      c.arc(foe.x, foe.y, R * 0.98, 0, TAU, true);
      c.clip();
    }
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round"; c.lineJoin = "round";
    for (const s of m.bladeSegments(f)){
      c.save();
      c.translate(f.x, f.y); c.rotate(s.a);
      const x1 = P[0][0] + (P[2][0] - P[0][0]) * run;
      c.save();
      c.beginPath(); c.rect(0, -60, x1, 120); c.clip();
      c.globalAlpha = 0.85 * fade;
      c.strokeStyle = A.core; c.lineWidth = 1.82;
      c.beginPath(); c.moveTo(P[0][0], P[0][1]);
      c.lineTo(P[1][0], P[1][1]); c.lineTo(P[2][0], P[2][1]); c.stroke();
      /* THE RUNE MARKS, cut across the line and fixed to the blade: the kind of
         each is shellHash on its index, so they are the same marks every frame
         and every fight. */
      c.strokeStyle = A.glow; c.lineWidth = 1.54; c.globalAlpha = fade;
      c.beginPath();
      const x0 = P[0][0] + 3, n = Math.floor((P[1][0] - 2 - x0) / 6.5);
      for (let i = 0; i <= n; i++){
        const x = x0 + i * 6.5;
        const y = P[0][1] + (P[1][1] - P[0][1]) * (x - P[0][0]) / (P[1][0] - P[0][0]);
        const kind = (shellHash(881, i) * 4) | 0;
        if (kind === 0){ c.moveTo(x, y - 2.6); c.lineTo(x, y + 2.6); }
        else if (kind === 1){ c.moveTo(x - 1.6, y + 2.4); c.lineTo(x + 1.6, y - 2.4); }
        else if (kind === 2){ c.moveTo(x + 1.6, y - 2.4); c.lineTo(x - 1.2, y);
                              c.lineTo(x + 1.6, y + 2.4); }
        else { c.moveTo(x - 1.4, y - 2.4); c.lineTo(x - 1.4, y + 2.4);
               c.moveTo(x + 1.4, y - 2.4); c.lineTo(x + 1.4, y + 2.4); }
      }
      c.stroke();
      c.restore();
      if (run < 1){                                  // the point of light that lights it
        const y1 = P[0][1] + (P[1][1] - P[0][1]) * Math.min(1, (x1 - P[0][0]) / (P[1][0] - P[0][0]));
        c.globalAlpha = fade; c.fillStyle = "#FFFFFF";
        c.beginPath(); c.arc(x1, y1, 2.2, 0, TAU); c.fill();
      }
      c.restore();
    }
    c.restore();
  }

  drawEcho(m){
    const a = m.a, b = m.b, F = m.echoFx;
    if (!(F && F.length) && !a.ultEcho && !b.ultEcho &&
        !(a.echoFade > 0) && !(b.echoFade > 0)) return;       // <- zero burden
    const c = this.ctx;
    for (const f of [a, b]){
      if (f.alive) this._echoLine(m, f);
      const E = f.ultEcho;
      if (!E || m.over) continue;
      const A = f.aff, d = f.w.ult.delay;
      for (const q of E.q){
        if (!q.tgt.alive) continue;
        /* the echo's age on the WINDOW clock, which is the clock it is paid on */
        const p = clamp((E.t - (q.at - d)) / d, 0, 1);
        const [x, y] = this._echoSeat(q.tgt, q.ox, q.oy);
        const r = 12 * (1 + 0.35 * Math.max(0, 1 - p / 0.16));   // the stamp lands
        this._echoRune(c, x, y, q.bear + Math.PI, r, A.core, A.dark);
        if (p > 0){
          /* THE HALF SECOND, run round the rune as a clock: when it closes,
             the echo comes */
          c.save();
          c.globalCompositeOperation = "lighter";
          c.strokeStyle = A.glow; c.lineWidth = 2.2; c.lineCap = "round";
          c.beginPath(); c.arc(x, y, r, -Math.PI / 2, -Math.PI / 2 + p * TAU); c.stroke();
          c.restore();
        }
      }
    }
    if (!F) return;
    for (const e of F){
      const A = e.src.aff, [x, y] = this._echoSeat(e.tgt, e.ox, e.oy);
      const rot = e.bear + Math.PI;
      if (e.landed){
        /* IT LEAVES BY BECOMING THE FLARE -- expands, thickens, whitens, goes --
           which is how Deadfall's figure leaves (`drawSigils`) */
        const k = clamp(e.t / 0.5, 0, 1), ez = 1 - Math.pow(1 - k, 3);
        c.save();
        c.globalCompositeOperation = "lighter";
        if (k < 0.3){
          c.globalAlpha = (1 - k / 0.3) * 0.75; c.fillStyle = A.glow;
          c.beginPath(); c.arc(x, y, 12 * (1 + 0.6 * ez), 0, TAU); c.fill();
        }
        c.translate(x, y); c.rotate(rot);
        c.globalAlpha = Math.pow(1 - k, 1.2);
        c.strokeStyle = k < 0.35 ? "#FFFFFF" : A.glow;
        c.lineWidth = 2.0 + 3.0 * (1 - k);
        c.lineCap = "round"; c.lineJoin = "round";
        this._echoPath(c, 12 * (1 + 1.3 * ez)); c.stroke();
        c.restore();
      } else {
        /* THE COROLLARY MISSED. The inner figure is gone at once -- what
           follows did not follow -- and the ring breaks into its three arcs,
           which part and DROP, drawn as the pending rune was so they read on a
           white shell and a dark one alike. */
        const k = clamp(e.t / 0.8, 0, 1), ez = 1 - (1 - k) * (1 - k);
        c.save();
        c.translate(x, y);
        c.lineCap = "round";
        c.globalAlpha = 1 - k * k;
        for (let i = 0; i < 3; i++){
          const a0 = rot + i * TAU / 3 + 0.22, a1 = a0 + TAU / 3 - 0.44;
          const mid = (a0 + a1) / 2, tw = (i - 1) * 0.6 * ez;
          const ox = Math.cos(mid) * 7 * ez, oy = Math.sin(mid) * 7 * ez + 14 * k * k;
          c.strokeStyle = A.dark; c.lineWidth = 5.2;
          c.beginPath(); c.arc(ox, oy, 12, a0 + tw, a1 + tw); c.stroke();
          c.strokeStyle = A.core; c.lineWidth = 2.0;
          c.beginPath(); c.arc(ox, oy, 12, a0 + tw, a1 + tw); c.stroke();
        }
        c.restore();
      }
    }
  }

  drawSigils(m){
'''),

]

ECHO_SHOWN = ('''  /* ============================================ THE COROLLARY, SHOWN ==
     Everything an echo does that is NOT the simulation: the voice, the
     director's beat, the kill's flash, the rune motes and the picture's
     record. Called from `tickEcho` for a LANDED echo and for one that found
     the foe out of reach (a dead party shows nothing -- the fight is over).
     Every line here is write-only: nothing in the simulation reads a beat,
     `finisher`, `ultFx`, the picture's records or a sound.

     THE BEAT (rule 3; v80 §4 "The echo files a `hit` beat"). Every landed
     echo files one, carrying the number `hurt` was handed -- "a second strike
     on the same number". A FATAL echo files its own `fatal: true`, the rule
     every side-channel kill in this engine follows (the Aegis return, the
     jets, the Bloodletting ticks): `hurt` files no beat, so without this a
     fight Axiom wins on an echo has no killing blow for the director to cut
     to. `echo: true` lets a picker tell the two apart; cineScore ignores it.

     THE KILL'S FLASH, NOT ITS WEIGHT. A fatal echo arms `finisher`, the wall
     flash every fatal side-channel hit arms, and NOT `killStop`: v80 §4 says
     "no hit stop" and the echo is a rune, not a swing.

     THE MOTES ARE A FIELD ON `m.ultFx`, AND `m.ultFx` IS ONE SLOT (open item
     25). So an echo arms it ONLY when the slot is free or already Axiom's --
     it never erases the opponent's running set-piece. When the slot is taken
     the echo simply has no motes; its drawn picture does not live on ultFx. */
  echoShown(f, tgt, q, landed){
    if (landed){
''' + VOICE_CALLS + '''      this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                  x: tgt.x, y: tgt.y, dmg: q.dmg, crit: false,
                  fatal: !tgt.alive, hpAfter: Math.max(0, tgt.hp),
                  hpFrac: Math.max(0, tgt.hp) / tgt.maxHp, maxHp: tgt.maxHp,
                  selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: tgt.speed,
                  close: Math.hypot(f.vx - tgt.vx, f.vy - tgt.vy),
                  ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                  shotSpd0: 0, echo: true });
      if (!tgt.alive) this.finisher = 1.0;
      const side = f === this.a ? "a" : "b", U = this.ultFx;
      if (!U || ((U.w === "axiom" || U.w === "axiom-echo") && U.src === side)){
        /* at the RUNE's seat, where the picture stamps it: the hit point pulled
           in to 20 from the foe's centre (v88 §6c) */
        const d0 = Math.hypot(q.ox, q.oy) || 1, s0 = Math.min(d0, 20) / d0;
        const rx = tgt.x + q.ox * s0, ry = tgt.y + q.oy * s0;
        this.ultFx = { w: "axiom-echo", kind: "echo", phase: "echo",
                       src: side, tgt: side === "a" ? "b" : "a",
                       x: rx, y: ry, tx: rx, ty: ry, hit: true, radius: 60,
                       aff: f.aff, t: 0, life: ''' + f"{ECHO_FX_LIFE}" + ''' };
      }
    }
''' + PICTURE_PUSH + '''  }

  tickWinnow(dt){
''')

S4 = [

("a missed echo is shown",
 '''        if (Math.hypot(tgt.x - f.x, tgt.y - f.y)
            >= u.reach + CONFIG.physics.ballR) continue;
''',
 '''        if (Math.hypot(tgt.x - f.x, tgt.y - f.y)
            >= u.reach + CONFIG.physics.ballR){
          this.echoShown(f, tgt, q, false);        // v88 stage 4: the miss, shown
          continue;
        }
'''),

("a landed echo is shown",
 '''          this.float(tgt.x, tgt.y - 50, q.dmg, f.aff.glow, 22 + q.dmg * 0.5);
      }
      if (E.t >= E.dur && !E.q.length) f.ultEcho = null;
''',
 '''          this.float(tgt.x, tgt.y - 50, q.dmg, f.aff.glow, 22 + q.dmg * 0.5);
        this.echoShown(f, tgt, q, true);           // v88 stage 4: voice, beat, motes, picture
      }
      if (E.t >= E.dur && !E.q.length) f.ultEcho = null;
'''),

("echoShown: the echo's voice, beat, flash, motes and picture",
 '''  tickWinnow(dt){
''',
 ECHO_SHOWN),

("the cast's life entry says what it carries now",
 '''                 same reason. The other three are strikes and end. */
              oathwound: 1.5, heartwood: 2.2, nightfell: 1.4,
              axiom: 1.5,
''',
 '''                 same reason. The other two are strikes and end.
                 COROLLARY (v88) IS NO LONGER A STRIKE: it is an 8s window
                 whose picture hangs off the fighter and the match, where
                 the one ultFx slot cannot erase it. This entry carries the
                 CAST's record only, and the cast has no art and no field of
                 its own on ultFx -- the bolt's were retired. */
              oathwound: 1.5, heartwood: 2.2, nightfell: 1.4,
              axiom: 1.5,
'''),

]

# THE BOLT'S ART, RETIRED -- two whole renderer branches, removed as spans in
# main() (a removal has no line of its own to audit; the builder asserts the
# absence instead: no `u.w === "axiom"` anywhere in the output).
RETIRE = [
    ("the bolt's construction lines (drawUltUnder)",
     "    /* ---- Corollary: the construction lines, ruled on the floor ------------- */\n",
     "    /* ---- Quarrelstorm: the dust the release blows off the floor ------------ */\n",
     "    /* ---- Corollary's construction lines were the BOLT's; retired in v88 stage 4.\n"
     "       The echo's picture is drawn off the fighter, not off ultFx. */\n\n"),
    ("the bolt's proof (drawUltOver)",
     "    /* ---- Corollary: the proof, stepped out and then concluded -------------- */\n",
     "    /* ---- Quarrelstorm: the RELEASE. Not arrows — drawShots draws those ----- */\n",
     "    /* ---- Corollary's proof was the BOLT's; retired in v88 stage 4. */\n\n"),
]


RUNECRACK = "        } else {                                        // rune-crack\n"


def voice_rows() -> list:
    """The three voices as edits -- only once the lab's picks are in."""
    rows = []
    if VOICE_CAST_ARM:
        rows.append(("axiom's cast voice, before the shared rune-crack",
                     RUNECRACK, VOICE_CAST_ARM + RUNECRACK))
    return rows + VOICE_ARM_ROWS


VOICE_ARM_ROWS: list = [

('''the runic school’s hex snap, its own kind''',
 '''      else if (kind === "seal"){
''',
 '''      else if (kind === "hex-snap"){
        /* THE HEX'S SNAP -- v80 §4 "the hex -- its snap", and v79 ("hex's own
           snap") and v75 ("a hex snap") name the same sound, so it is the
           RUNIC SCHOOL's voice and its own `kind`, not an Axiom sub-voice.
           SNAP, of five, from `corollary_voice_lab.py`.

           A finger snap's band (2.6 kHz, 22 ms) on a short 1.3 kHz body, and a
           ping held nearly level on top: audible 25 ms, peak at 6 ms, rise
           under 1 ms. Placed where a fight cannot mistake it: centroid 3.35
           kHz, nearly two octaves under the wall tick's 12.3 kHz (the
           commonest sound in a fight); register 0.20 against the echo it
           lands on top of, 0.41 against rune-crack. Level between 3x the
           wall tick and the hit on every noise draw -- the bands are WIDE so
           a session's noise buffer cannot push it out of that window. */
        this._burst(t, { freq: 2600, q: 1.2, gain: 0.38, dur: 0.022, type:"bandpass" });
        this._burst(t, { freq: 1300, q: 1.0, gain: 0.15, dur: 0.030, type:"bandpass" });
        this._tone (t, { freq: 3100, to: 2500, gain: 0.138, dur: 0.045, type:"triangle" });
      }
      else if (kind === "seal"){
'''),

]


def retire_span(s: str, label: str, start: str, end: str, repl: str) -> str:
    """Remove [start, end) -- both anchors exactly once, end after start."""
    if s.count(start) != 1 or s.count(end) != 1:
        raise SystemExit(f"ANCHOR {label}: start x{s.count(start)}, "
                         f"end x{s.count(end)} -- expected exactly 1 each")
    i, j = s.index(start), s.index(end)
    if j <= i:
        raise SystemExit(f"ANCHOR {label}: the end anchor is before the start")
    print(f"  ok    retired {label}  ({s.count(chr(10), i, j)} lines)")
    return s[:i] + repl + s[j:]


def sync_fx(s: str) -> str:
    """The inlined copy and src/render/fx.js stay one object (cindercleave's
    `sync_fx`, one relic along): the bolt's spec out and the echo's in, in BOTH
    copies, the whole module compared before and after, both stamps re-cut.
    A spec written only into the page is dropped by the next fx_build, and
    `ULTFX.sync` returns silently on a missing spec (open item 46)."""
    fx_js = HERE.parent / "src" / "render" / "fx.js"
    mod = fx_js.read_text(encoding="utf-8")
    if FX_ECHO in mod and FX_OLD not in mod:
        mod = mod.replace(FX_ECHO, FX_OLD, 1)
        print("  fx    src/render/fx.js already carries this build's edit -- "
              "reverted in memory first (a rebuild)")
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    if not tm:
        raise SystemExit("no ULT FIELDS glue after the inlined fx.js")
    if s[head.end():tm.start()].rstrip("\n") != mod.rstrip():
        raise SystemExit("src/render/fx.js and the inlined copy have DIVERGED "
                         "before this builder wrote anything. Fix that first.")
    if mod.count(FX_OLD) != 1 or s.count(FX_OLD) != 1:
        raise SystemExit("the bolt's fx spec is not exactly once in both copies")
    mod2 = mod.replace(FX_OLD, FX_ECHO, 1)
    s = s.replace(FX_OLD, FX_ECHO, 1)
    old_sha = head.group(1)
    new_sha = hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    s = s.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
    head2 = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                      r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    tm2 = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head2.end())
    if s[head2.end():tm2.start()].rstrip("\n") != mod2.rstrip():
        raise SystemExit("the inlined copy and src/render/fx.js DIVERGED "
                         "across this builder's own write")
    SYNC_FX_WRITE.append((fx_js, mod2))
    print(f"  fx    bolt's spec out, 'axiom-echo' in, both copies identical; "
          f"stamp {old_sha[:16]} -> {new_sha[:16]}")
    return s


SYNC_FX_WRITE: list = []     # written only after every refusal has passed


def axiom_ult(code: str) -> str:
    """The ult block of Axiom's weapon entry, comments stripped."""
    i = code.find('id:"axiom"')
    if i < 0:
        raise SystemExit("no Axiom in this source -- wrong build")
    j = code.find("ult:{", i)
    k = code.find("},", j)
    return code[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "4"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nAXIOM / COROLLARY -- stage {A.stage}")
    # THE HASH IS OF THE LF TEXT, as every relic builder's printed hash is:
    # `read_text` folds a CRLF file (sc-leaf is one) to LF, and this builder
    # writes LF. The file's own bytes hash differently when it is CRLF.
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")

    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED, NOT GUESSED (BINDWEED brief :80-84, which
    # speaks for the batch): sc-leaf, which carries the Winnowing's rung stop.
    for need, why in (('id:"starwarden"', "no Starwarden -- not the settled trunk"),
                      ("novaDmg", "no Crossweave nova -- the short branch"),
                      ("s.over.stop = 0.02 * s.rung;",
                       "no Winnowing rung stop -- this is sc-trunk or older, "
                       "not sc-leaf. Rick passed sc-leaf's gate 4; build on it.")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    print("  base  34 relics, minute pace, Starwarden, Crossweave's nova AND "
          "the Winnowing's rung stop -- sc-leaf's line")

    ult0 = ult_block(0)
    ult1 = ult_block(ULT["hex"])
    if A.stage == "1":
        if "ultEcho" in code:
            raise SystemExit("this source already carries stage 1 -- built")
        if strip_comments(SHIPPED_ULT) not in code:
            raise SystemExit("Axiom's shipped bolt is not in this source as "
                             "shipped -- the base has moved under the builder")
        edits = S1
    elif A.stage == "2":
        if "ultEcho" not in code:
            raise SystemExit("stage 2 needs stage 1 under it -- no echo here")
        if strip_comments(ult1) in code:
            raise SystemExit("this source already carries stage 2 -- built")
        edits = S2
    else:
        if strip_comments(ult1) not in code:
            raise SystemExit("stage 4 needs stage 2 under it -- no hexing echo here")
        if "echoShown" in code:
            raise SystemExit("this source already carries stage 4 -- built")
        edits = S4 + PICTURE_ROWS + voice_rows()
        for label, start, end, repl in RETIRE:
            s = retire_span(s, label, start, end, repl)

    for label, old, new in edits:
        s = one(s, old, new, label)
    if A.stage == "4":
        s = sync_fx(s)

    # WHAT SHIPPED IS WHAT THIS RUN PRINTED (`ult_matches`, the v56 lesson).
    out_code = strip_comments(s)
    blk = axiom_ult(out_code)
    want = ult0 if A.stage == "1" else ult1
    if strip_comments(want).strip() != blk.strip():
        raise SystemExit(f"REFUSING TO WRITE -- Axiom's ult block is not what "
                         f"this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the doc's: {tip!r}")
    print(f"  ok    ult   {blk.splitlines()[0].strip()} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    # NO NEW `Math.random`. The base has twelve (audio noise, shake, the
    # random-matchup buttons -- none on the sim path); this build adds none.
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # NO INSERT DRAWS THE MATCH RNG ITSELF -- every sim-path insert, not only
    # tickEcho. What an echo DOES reach through `hurt` is the ward's shatter,
    # which throws 40 sparks off the stream when an echo breaks a ward; that
    # is the ward's rule for all damage and v80 §4 routes the echo through it
    # ("ward first"). It is deterministic, and it is not this code's own draw.
    for label, _old, new in S1 + S4 + PICTURE_ROWS + voice_rows():
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws "
                             "the match RNG")
    # AND NO OTHER RELIC CAN REACH IT: the only writer of `ultEcho` is the
    # `kind === "echo"` branch, and only Axiom carries that kind.
    kinds = re.findall(r'kind:"echo"', out_code)
    if len(kinds) != 1:
        raise SystemExit(f"REFUSING TO WRITE -- {len(kinds)} echo ultimates, "
                         "expected exactly Axiom's")
    print("  ok    one echo ultimate in the build, and it is Axiom's; no insert "
          "draws the RNG itself")
    if A.stage == "4":
        # THE BOLT'S ART IS GONE: nothing in the renderer keys on Axiom's
        # ultFx any more, and its field spec is out of both copies.
        if 'u.w === "axiom"' in out_code:
            raise SystemExit("REFUSING TO WRITE -- bolt art still keyed on "
                             'u.w === "axiom"')
        if FX_OLD in s or FX_ECHO not in s:
            raise SystemExit("REFUSING TO WRITE -- the fx spec swap is not in "
                             "the page")
        n_shown = out_code.count("echoShown(")
        if n_shown != 3:
            raise SystemExit(f"REFUSING TO WRITE -- echoShown appears {n_shown}x "
                             "(want the definition and its two calls)")
        print('  ok    bolt art retired (no u.w === "axiom"), bolt spec out, '
              "echo spec in, echoShown defined and called twice")

    syntax_check(s, out_p.name)
    for fx_js, mod2 in SYNC_FX_WRITE:        # tracked src/render/fx.js, last
        fx_js.write_text(mod2, encoding="utf-8", newline="\n")
        print(f"  wrote {fx_js.relative_to(HERE.parent)}")
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    print(f"  charge {ULT['charge']}  window {ULT['dur']}  delay {ULT['delay']}"
          f"  reach {ULT['reach']}+R  hex {0 if A.stage == '1' else ULT['hex']}"
          "   blade 7.42 (the doc's and Rick's; not bisected)")
    ids33 = "<the 33 others>"
    print("\n  GATE -- in this order, and each can fail:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids {ids33} --n 8")
    print("      IDENTICAL on the 33. Axiom's OWN pairings differ -- run them")
    print("      separately and say how many; that difference is the pass.")
    if A.stage == "1":
        print(f"    python corollary_probe.py --game {A.out}")
        print("    relic at 7.42 WITHOUT hex against the prose-reading lab's arm B")
    else:
        print(f"    python corollary_probe.py --game {A.out} --hex")
        print("    relic at 7.42 WITH hex against the prose-reading lab's arm C")
        print(f"    python verify.py --game {A.out} --n 40")
        print(f"    python tip_audit.py --game {A.out}")
    print(f"    python chain_audit.py --relic <stage-1 link> --tip <tip> "
          "--builder corollary_build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
