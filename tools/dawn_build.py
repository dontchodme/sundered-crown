#!/usr/bin/env python
"""DAWNBRINGER / DAYBREAK, REDESIGNED -- the sun rises up the hall. v97.

Built from `06-docs/v86/dawnbringer-daybreak-redesign-v86.md` §5 (Cowork,
2026-09-26) and its §7 rulings, which are the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the dawn, sparks out     sc-corollary-c14 -> sc-dawn.html
    stage 2   the blade                confirm 10.4 wide on 151 (no link unless it moves)
    stage 3   picture, voice, field    sc-dawn -> sc-daybreak-fx.html

§1: "For a duration the sun rises. A line of light climbs the hall from the
floor to the top over the whole duration, and everything below the line is in
the dawn: an enemy standing in it is smitten and burned for as long as it
stays there."

§4, declared: `lineY = H - k*H`, `k = (t - t0) / dur` (floor at cast, ceiling
at close). Lit = `foe.y > lineY`. Every 0.5s while lit: `foe.apply("smite", 1,
f)` and `hurt(foe, 2, f)` (ward first, nothing else, no beat). The caster gets
nothing (arm B).

THE WINDOW AND CHARGE. Window 8 (§1/§4). CHARGE 14 IN THE GAME'S CLOCK: Rick
ruled "what Cowork tested" (v86 §7), which was 16 seconds of the LAB's step
clock -- freezes included -- and then, for the whole batch (2026-09-27), "use
the game's equivalent". The engine charges only in unfrozen time; its 14 gives
the casts the lab's 16 did. The shipped Daybreak was charge 14, dur 5. §6's heal and line-speed flags are
built as written: no heal, the full floor-to-ceiling rise.

THE READINGS, where the build has to choose and the doc or the engine decides:
  1. THE TICK'S CADENCE is the lab's (`overlays/dawn.js`): a 0.5s cooldown
     that runs through the whole window and fires on the first lit frame it
     is clear -- "every 0.5s while lit", priced that way.
  2. `apply`'s SOURCE IS A SIDE LETTER. §4 and the lab pass the Fighter; the
     engine's contract (Fighter.apply's own comment) is "a" or "b", and smite
     DOES tick damage, so its fatal-tick beat is attributed by that letter.
  3. "NO BEAT" FOR A TICK -- except a tick that KILLS, which files its own
     `fatal: true` hit beat. That is this engine's standing rule for every
     side-channel kill (the Aegis return, Scour's ticks: "ticks file nothing,
     the fatal one does"), and without it a fight won on the dawn has no
     killing blow (open item 3's class). Every other tick files nothing.
  4. H is `CONFIG.arena.h`, the full hall, as the lab reads it. After the hall
     starts closing (t > 27) the visible floor sits above H, so the line
     starts below it for up to ~1.4s; the lab priced exactly that.

THE CLOCK. The window and the tick cooldown run on the window tickers' clock,
which stops through a hit stop (tickWinnow's and tickCharge's convention). The
lab counted every step, freezes included.

SPARKS OUT. The ultimate's kind is no longer "radiant", so nothing sets
`ultRadiant` and the spark spawn in `resolveHit` is unreachable for this
relic. The spark MACHINERY stays: Lastlight's Harrowing throws the same sparks.
The corona art and the sparks' field spec are stage 3's.

THE BASE is the chain tip, `sc-corollary-c14.html` (sc-leaf + Axiom /
Corollary stages 1-6), named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "dawnbringer"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v86 and Rick's §7.
ULT = {
    # Rick, v86 §7: "what Cowork tested" -- 16 on the LAB's clock, which counts
    # hit-stop freezes; Rick, 2026-09-27, for the batch: "use the game's
    # equivalent". The engine charges only in unfrozen time, and its 14 gives
    # the casts the lab's 16 did (v97 §3: 52.5% at 14 against the lab's 53.5%).
    "charge": 14,
    "dur": 8,         # §1/§4 "over 8s"
    "tick": 0.5,      # §4 "every 0.5s while lit"
    "tickDmg": 2,     # §4 `hurt(foe, 2, f)`
    "smite": 1,       # §4 `foe.apply("smite", 1, f)`
}
TIP = "The sun rises up the hall: foes below the dawn line are smitten and burn"

SHIPPED_ULT = '''    ult:{ name:"Daybreak", charge:14, kind:"radiant", dur:5.0,
         sparks:6, sparkDmg:5, sparkKnock:260, sparkLife:8.0, sparkGrace:0.7,
         tip:"For 5s its hits spray sparks — 5 dmg to foes, healing when collected" },'''


def ult_block() -> str:
    return (f'''    ult:{{ name:"Daybreak", charge:{ULT["charge"]}, kind:"dawn", dur:{ULT["dur"]},
         tick:{ULT["tick"]}, tickDmg:{ULT["tickDmg"]}, smite:{ULT["smite"]},
         tip:"{TIP}" }},''')


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

("dawnbringer's ultimate is the dawn",
 SHIPPED_ULT,
 ult_block()),

("the fighter carries the dawn's window",
 '''    this.ultRadiant = null;   // {t, dur} while Daybreak burns
''',
 '''    this.ultRadiant = null;   // {t, dur} while Daybreak burns
    /* {t, dur, cd} while DAYBREAK's dawn is rising (v86). null on every other
       relic and on this one outside its window: `tickDawn` returns after a
       two-iteration loop that does nothing. `dawnTally` is the probe's count,
       cumulative over the fight; nothing in the simulation reads it. */
    this.ultDawn = null;
    this.dawnTally = null;
'''),

("the cast opens the dawn and resolves nothing",
 '''    if (u.kind === "radiant"){
      f.ultRadiant = { t: 0, dur: u.dur || 5.0 };''',
 '''    if (u.kind === "dawn"){
      /* DAYBREAK (v86). NOTHING RESOLVES HERE: the cast starts the sun
         rising, and `tickDawn` does everything the window does. The sparks
         are gone for this relic -- nothing sets `ultRadiant` any more -- and
         the spark machinery stays for Lastlight's Harrowing. `cd` starts at
         zero, so a foe already in the dawn is struck on the first frame. */
      f.ultDawn = { t: 0, dur: u.dur, cd: 0 };
      if (!f.dawnTally)
        f.dawnTally = { casts: 0, ticks: 0, dealt: 0, litFrames: 0,
                        frames: 0 };
      f.dawnTally.casts++;
      return;
    }
    if (u.kind === "radiant"){
      f.ultRadiant = { t: 0, dur: u.dur || 5.0 };'''),

("the dawn ticks with the window tickers",
 '''    this.tickEcho(dt);                  // COROLLARY (v80)
''',
 '''    this.tickEcho(dt);                  // COROLLARY (v80)
    this.tickDawn(dt);                  // DAYBREAK (v86)
'''),

("tickDawn raises the sun",
 '''  tickWinnow(dt){
''',
 '''  /* =================================================== THE DAWN =======
     v86 §4: the line `lineY = H - k*H`, `k = t / dur` -- the floor at the
     cast, the ceiling at the close. A foe whose centre is below it
     (`foe.y > lineY`; y grows downward) is lit, and every `tick` seconds
     while lit it is smitten +`smite` and takes `tickDmg` through `hurt`:
     ward first and NOTHING ELSE -- no crit, no knock, no hit stop, no
     hitstun -- and no beat, except the tick that KILLS, which files its
     own (this engine's rule for a side-channel kill; see the builder's
     reading 3). The caster gets nothing.

     THE COOLDOWN RUNS THROUGH THE WHOLE WINDOW, lit or not, and a tick fires
     on the first lit frame it is clear: the lab's cadence, and what was
     priced. On the window tickers' clock, so it freezes through a hit stop.

     THE SOURCE IS A SIDE LETTER (Fighter.apply's contract): smite ticks
     damage, and a fatal smite tick is attributed by it. */
  tickDawn(dt){
    for (const f of [this.a, this.b]){
      const D = f.ultDawn;
      if (!D) continue;
      D.t += dt;
      if (D.t >= D.dur || !f.alive){ f.ultDawn = null; continue; }
      const u = f.w.ult, T = f.dawnTally;
      const foe = f === this.a ? this.b : this.a;
      const H = CONFIG.arena.h;
      const lineY = H - Math.min(1, D.t / D.dur) * H;
      D.cd -= dt;
      T.frames++;
      if (!foe.alive || !(foe.y > lineY)) continue;
      T.litFrames++;
      if (D.cd > 0) continue;
      D.cd = u.tick;
      T.ticks++;
      foe.apply("smite", u.smite, f === this.a ? "a" : "b");
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      this.hurt(foe, u.tickDmg, f);
      T.dealt += before - (foe.hp + foe.shield);
      if (wasUp && foe.hp <= 0)
        this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                    x: foe.x, y: foe.y, dmg: u.tickDmg, crit: false,
                    fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                    selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                    close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                    ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                    shotSpd0: 0, dawn: true });
    }
  }

  tickWinnow(dt){
'''),

]



# ---------------------------------------------------------------- stage 3 --
# PICTURE, VOICE, THE SPARKS' FIELD OUT. v86 §4 and §5 stage 3, every open
# choice picked on measurements under Rick's "you pick i overrule" (v97 §4).
# Presentation only: engine_ab WITH Dawnbringer in the roster is the proof.
FX_OLD = '''    /* DAYBREAK RISES, IT DOES NOT DETONATE, and it stays sparse in the middle
       ON PURPOSE. CLAUDE.md §4.1b is the record of this relic's art blowing
       out over a body already at 0.892 luma -- "the ball was not lit, it was
       erased". Piling embers onto that centre would recreate exactly the
       fault that section exists to prevent. */
    dawnbringer: { mode: 'burst', n: 1350, sp: [120, 470], grav: -90,
                   drag: 1.8, life: [0.45, 1.15], heavy: 0.0,
                   size: [0.7, 2.1], spawn: 0.10, up: 110 },
'''
S3 = [

('''Sfx ult branch: Daybreak’s voices (step 0-7 + close) replace the chord and bell''',
 '''        if (w === "dawnbringer"){                       // a chord and a bell
          [0, 7, 12, 16].forEach((st, i) =>
            this._tone(t + i * 0.03, { freq: 220 * Math.pow(2, st/12), gain: 0.13,
                                       dur: 1.5, type:"triangle" }));
          this._burst(t + 0.14, { freq: 5200, q: 0.9, gain: 0.20, dur: 0.5, type:"highpass" });''',
 '''        if (w === "dawnbringer" || w === "dawnbringer-step"){   // the sun rises
          /* DAYBREAK -- v86 §4 SOUND: "a slow swell rising over the whole 8s
             (re-struck tones stepping up a scale, one per second -- the only
             voice in the roster tied to the window's clock)". HANDOFF, of five,
             picked on the numbers by `dawn_voice_lab.py` under Rick's "you
             pick i overrule" (v97).

             ONE STEP A CALL. The bare id is the cast (`fireUlt` plays it for
             every relic) and is step 0; `tickDawn` plays steps 1-7 as the
             window's OWN clock crosses each second, and the close when it
             runs out -- so a hit stop, which freezes that clock, holds the
             note, and a caster who dies mid-window stops the rise. The eight
             steps are one octave of C major, C5 -> C6 (diatonic to the
             score's A minor), each 1.631 dB over the last going in: +9 dB
             over the eight coming out of the chain, which compresses it.

             A HELD NOTE DOES NOT EXIST IN THIS TOOLKIT (CLAUDE.md 4.5), so a
             step is RE-STRUCK every 12-23 whole cycles (~22 ms), in phase, for
             up to 1.75 s -- a window-second runs 1.16 s of match time at the
             median and 1.62 s at p99, because every hit stop freezes the
             window's clock -- and the NEXT step stops each strike that has
             not sounded yet. The old note releases over its own 0.5 s decay
             while the new one fills in: one line, handed from degree to
             degree however long the second runs. The first strike carries
             0.6 of the plateau, so a degree re-strikes softly. `dawnHeld` keeps
             each step's strikes for the hand-off: presentation state on the
             synth, never read by the simulation.

             `.frequency.value = f` AFTER `_tone` IS LOAD-BEARING. `_tone`
             sets its pitch with an event AT the strike, and Chromium starts
             the oscillator's phase off the param's 440 Hz default: measured,
             a strike at 1046 Hz lands up to 180 degrees off, so re-strikes
             above ~600 Hz cancel instead of summing (the lab's RAW control:
             the top step 10 dB down and the swell gone). Setting the value
             puts every strike within one sample. */
          const n = w === "dawnbringer" ? 0 : Math.max(0, Math.min(7, p.n | 0));
          const f = 440 * Math.pow(2, (3 + [0, 2, 4, 5, 7, 9, 11, 12][n]) / 12);
          const g = 0.002212 * Math.pow(10, 1.631 * n / 20);
          const dt = Math.max(1, Math.round(f * 0.022)) / f;
          const q = Math.pow(0.0001 / g, dt / 0.5);
          const H = this.dawnHeld || (this.dawnHeld = []), P = n > 0 ? H[n - 1] : null;
          if (P){ for (const [o, at] of P.os) if (at >= t) try { o.stop(t); } catch(e){}
                  H[n - 1] = null; }
          const os = [];
          for (let k = 0; k * dt < 1.75; k++){
            const o = this._tone(t + k * dt, { freq: f, dur: 0.5, type:"triangle",
                                               gain: k ? g : Math.max(g, g * 0.6 / (1 - q)) });
            o.frequency.value = f;
            os.push([o, t + k * dt]);
          }
          H[n] = { t0: t, dt, f, g, os };
        } else if (w === "dawnbringer-close"){          // held, and released
          /* "close -- the top note held and released" (v86 §4). STOP, of five
             (`dawn_voice_lab.py`). It picks up step 7's strike grid IN PHASE
             -- the same start, the same spacing -- and stops step 7's strikes
             that have not sounded, so the hold carries on without a seam. It
             holds 0.5 s (the picture's wash fades over 0.5 s), then stops
             re-striking and the note releases on its own 0.5 s decay, -34 dB
             380 ms later.
             `tickDawn` plays it only when the window closes by its clock,
             never on a death. */
          const H = this.dawnHeld || (this.dawnHeld = []), P = H[7];
          const f = P ? P.f : 440 * Math.pow(2, 15 / 12);
          const g = P ? P.g : 0.002212 * Math.pow(10, 1.631 * 7 / 20);
          const dt = P ? P.dt : Math.max(1, Math.round(f * 0.022)) / f, t0 = P ? P.t0 : t;
          let k = Math.ceil((t - t0) / dt - 1e-9);
          if (P){ for (const [o, at] of P.os) if (at >= t0 + (k - 0.5) * dt) try { o.stop(t); } catch(e){}
                  H[7] = null; }
          for (; t0 + k * dt < t + 0.5; k++)
            this._tone(t0 + k * dt, { freq: f, gain: g, dur: 0.5,
                                      type:"triangle" }).frequency.value = f;'''),

('''tickDawn: steps 1-7 and the close ride the window’s clock''',
 '''      const D = f.ultDawn;
      if (!D) continue;
      D.t += dt;
      if (D.t >= D.dur || !f.alive){ f.ultDawn = null; continue; }''',
 '''      const D = f.ultDawn;
      if (!D) continue;
      const sec = Math.floor(D.t);
      D.t += dt;
      /* DAYBREAK'S VOICE RIDES THIS CLOCK (v86 §4: "the only voice in the
         roster tied to the window's clock"). A step each time `D.t` crosses
         a whole second (`sec` is the second before this frame's add; the
         cast already played step 0), and the close when the window runs out
         with its caster alive: never on a death, and never once the fight
         is over, because step() stops calling this. Presentation only:
         SFX.play draws nothing, is a no-op headless, and nothing here is
         read back (dawn_voice_lab: fights identical with and without it). */
      if (f.alive && D.t >= D.dur) SFX.play("ult", { w: "dawnbringer-close" });
      else if (f.alive && Math.floor(D.t) > sec)
        SFX.play("ult", { w: "dawnbringer-step", n: Math.floor(D.t) });
      if (D.t >= D.dur || !f.alive){ f.ultDawn = null; continue; }'''),

('''dawn picture: fighter fields''',
 '''    this.ultDawn = null;
    this.dawnTally = null;
''',
 '''    this.ultDawn = null;
    this.dawnTally = null;
    /* DAYBREAK'S PICTURE (v86 §4), and none of it is the window: the dawn
       outlives `ultDawn` by the half second its wash takes to fade, so the
       picture keeps its own state. On the FIGHTER and never on `m.ultFx`
       (one slot, and the opponent's cast takes it: open item 25). Driven in
       `tickPresentation`, except `dawnTagged`, which `tickDawn` re-arms;
       nothing in the simulation reads any of it.
         dawnFade     1 while the dawn is up; eased to 0 over 0.5s after the
                      window closes, the caster falls, or the match ends
         dawnK        the line's height, 0 at the floor, 1 at the ceiling --
                      the last the window showed, so a fading wash stays
                      where the line stood
         dawnAge      the presentation clock since the cast (the brightening)
         dawnLitFade  the lit foe's motes, up while it is in the dawn
         dawnTagged   this lit stretch has had its SMITE tag */
    this.dawnFade = 0;
    this.dawnK = 0;
    this.dawnAge = 0;
    this.dawnLitFade = 0;
    this.dawnTagged = false;
'''),

('''dawn picture: its clocks in tickPresentation''',
 '''                 : Math.max(0, f.echoFade - dt / 0.45);
''',
 '''                 : Math.max(0, f.echoFade - dt / 0.45);
      /* AND THE DAWN'S. Every `life` in this method is in HALF-SECONDS (it
         runs twice a normal step): 0.6 is the cast's 0.3s brightening and
         1.0 the close's 0.5s fade. The line is read off the window with
         `tickDawn`'s own formula, so the picture is where the test is; it
         holds still through a hit stop because the window does, and this
         clock keeps playing. Not after the match: `tickDawn` never runs
         again once `over` is set, so a window open at the kill would
         otherwise hold the dawn lit through the whole verdict. */
      { const D = this.over ? null : f.ultDawn;
        if (D){
          if (!(f.dawnFade > 0)) f.dawnAge = 0;              // a new dawn
          f.dawnFade = 1;
          f.dawnAge += dt;
          f.dawnK = Math.min(1, D.t / D.dur);
          const foe = f === this.a ? this.b : this.a, H = CONFIG.arena.h;
          const lit = foe.alive && foe.y > H - f.dawnK * H;
          f.dawnLitFade = lit ? Math.min(1, f.dawnLitFade + dt / 0.2)
                              : Math.max(0, f.dawnLitFade - dt / 0.7);
        } else if (f.dawnFade > 0 || f.dawnLitFade > 0){
          f.dawnFade = Math.max(0, f.dawnFade - dt / 1.0);
          f.dawnLitFade = Math.max(0, f.dawnLitFade - dt / 0.7);
          f.dawnAge += dt;
        }
      }
'''),

('''dawn picture: the tag re-arms out of the dawn''',
 '''      if (!foe.alive || !(foe.y > lineY)) continue;
''',
 '''      /* out of the dawn: the next tick that lands tags again (`dawnShown`) */
      if (!foe.alive || !(foe.y > lineY)){ f.dawnTagged = false; continue; }
'''),

('''dawn picture: the tick calls dawnShown''',
 '''      T.dealt += before - (foe.hp + foe.shield);
''',
 '''      T.dealt += before - (foe.hp + foe.shield);
      if (!f.dawnTagged) this.dawnShown(f, foe);          // the picture's
'''),

('''dawn picture: dawnShown''',
 '''  /* =================================================== THE DAWN =======''',
 '''  /* DAYBREAK'S SMITE TAG -- ON A CROSSING, NEVER ON A TICK. Corona's rule
     (`burnFoe`): at two ticks a second, a tag a tick would print SMITE a
     dozen times over one foe in one window. So the FIRST tick of each lit
     stretch tags, and `tickDawn` re-arms the flag on the first frame the foe
     is out of the dawn: a foe that stays lit is tagged once, one that
     bounces out and back is tagged again as it re-enters. No count on it --
     the ball draws its own smite (`_stSmite`), and the blade's smite tag
     prints the name alone too.

     PRESENTATION ONLY. The flag, `tags` and `taught` are read by nothing in
     the simulation; this runs after the tick has resolved and changes none
     of it. */
  dawnShown(f, foe){
    f.dawnTagged = true;
    if (!(foe.hp > 0)) return;                 // the killing tick: the shatter says it
    const first = !this.taught.smite && !!STATUS.smite.tip;
    if (first) this.taught.smite = true;
    this.statusTag(foe.x, foe.y, "smite", first);
  }

  /* =================================================== THE DAWN ======='''),

('''dawn picture: the draw call''',
 '''    if (__world) this.drawArena(m);
    c.scale(this.scale, this.scale);
''',
 '''    if (__world) this.drawArena(m);
    c.scale(this.scale, this.scale);
    /* DAYBREAK'S DAWN, ON THE FLOOR: over the hall's own paint and under
       everything that stands in it. The WORLD pass and never the emissive
       one -- v86 §4, "a WASH, not a light source", and CLAUDE.md §4.1c: the
       bloom reads the emissive layer's colour whatever its alpha, so a wash
       there would be a full-arena bloom source, the Harrowing's fog. */
    if (__world) this.drawDawn(m);
'''),

('''dawn picture: drawDawn''',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------------------ THE DAWN ---
     Daybreak (v86 §4). Everything below the line is in the dawn: a WASH of
     the caster's glow at alpha 0.10, source-over; the line a 4-unit band
     at 0.60 with a 12-unit gradient above it, the horizon. It hangs off the
     CASTER (`dawnFade`, `dawnK`, `dawnAge`), never `m.ultFx`. At the cast
     it appears at the floor and brightens over 0.3s; at the close it is at
     the ceiling and the whole hall's wash fades over 0.5s.

     NOTHING HERE TOUCHES A BALL. It is drawn before every relic body, so
     each is painted over it -- the old Daybreak drew a white corona under
     `lighter` over a 0.89-luma body and ERASED it (CLAUDE.md §4.1b). The lit
     foe's motes are drawn here too, so its own shell hides them: they rise
     off it, never across it. No `lighter` anywhere in it.

     THE LIVE HALL ONLY. Once the walls start closing the line begins below
     the visible floor (v97 reading 4); this clips to the inset, so the line
     rises into view out of the floor instead of being drawn on the wall.

     PRESENTATION ONLY: no rng, no spawnFx, no Math.random -- the motes are
     shellHash on their index against the match clock (and the death clock
     after the kill, so they keep drifting while they fade) -- and nothing
     here writes a field the simulation reads. */
  drawDawn(m){
    const a = m.a, b = m.b;
    if (!(a.dawnFade > 0) && !(b.dawnFade > 0)) return;      // <- zero burden
    const c = this.ctx, A = CONFIG.arena, R = CONFIG.physics.ballR;
    const n = m.inset || 0, x0 = n, w = A.w - 2 * n, yF = A.h - n;
    const T = m.t + (m.deathAge || 0);
    c.save();
    c.beginPath(); c.rect(x0, n, w, yF - n); c.clip();
    for (const f of [a, b]){
      const fade = f.dawnFade;
      if (!(fade > 0)) continue;
      const P = f.aff, y = A.h - f.dawnK * A.h, hb = 2;
      const s = Math.min(1, f.dawnAge / 0.6);             // half-seconds
      const on = fade * (1 - (1 - s) * (1 - s));
      if (y + hb < yF){                                      // the wash
        c.globalAlpha = 0.10 * on;
        c.fillStyle = P.glow;
        c.fillRect(x0, y + hb, w, yF - y - hb);
      }
      if (y - hb - 12 < yF){                             // the horizon, then the line
        const g = c.createLinearGradient(0, y - hb, 0, y - hb - 12);
        g.addColorStop(0, P.core); g.addColorStop(1, P.core + "00");
        c.globalAlpha = 0.60 * on;
        c.fillStyle = g;
        c.fillRect(x0, y - hb - 12, w, 12);
        c.globalAlpha = 0.60 * on;
        c.fillStyle = P.core;
        c.fillRect(x0, y - hb, w, 4);
      }
      /* THE LIT FOE'S MOTES: a faint drift up off its shell while it is in
         the dawn. Born inside the disc on its upper side, so its own body
         covers them until they clear the rim. */
      const foe = f === a ? b : a, L = f.dawnLitFade * fade;
      if (L > 0.01 && foe.alive){
        c.fillStyle = P.glow;
        for (let i = 0; i < 12; i++){
          const ph = (T * (0.50 + 0.30 * shellHash(9101, i)) + shellHash(9103, i)) % 1;
          const ang = -Math.PI / 2 + (shellHash(9107, i) - 0.5) * 2.4;
          const r0 = R * (0.50 + 0.45 * shellHash(9109, i));
          const mx = foe.x + Math.cos(ang) * r0 + Math.sin(T * 1.9 + i * 2.3) * 2.5;
          const my = foe.y + Math.sin(ang) * r0 - ph * 44;
          c.globalAlpha = L * 0.70 * Math.sin(ph * Math.PI);
          c.beginPath();
          c.arc(mx, my, 1.6 * (0.7 + 0.6 * shellHash(9113, i)), 0, TAU);
          c.fill();
        }
      }
    }
    c.restore();
  }

  drawMotes(m){
'''),

('''retire the sparks-era pool (drawUltUnder)''',
 '''    else if (u.w === "dawnbringer"){
      /* Daybreak on the floor: a breathing pool of dawn under the LIVE
         caster — this piece runs five seconds and the caster keeps moving.
         The old target rings left with Judgement; nothing falls anymore. */
      const rise = clamp(u.t / 0.35, 0, 1);
      const fade = 1 - clamp((u.t - (u.life - 0.5)) / 0.5, 0, 1);
      const pulse = 0.88 + 0.12 * Math.sin(u.t * 7);
      const g = c.createRadialGradient(src.x, src.y, 5, src.x, src.y, 105 * pulse);
      g.addColorStop(0, "#FFF6E255"); g.addColorStop(1, "#FFF6E200");
      c.globalAlpha = 0.8 * rise * fade;
      c.fillStyle = g;
      c.beginPath(); c.arc(src.x, src.y, 105 * pulse, 0, TAU); c.fill();
    }

''',
 ''''''),

('''retire the sparks-era corona (drawUltOver)''',
 '''    /* ---- Daybreak: white heat radiating off the whole relic ------------- */
    else if (u.w === "dawnbringer"){
      const R = CONFIG.physics.ballR;
      const rise = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - (u.life - 0.5)) / 0.5, 0, 1);
      const k2 = rise * fade;
      /* THE CORONA IS A RING, NOT A DISC, AND THE HOLE IS THE POINT.
       *
       * It was a disc from stop 0 = #FFFFFF at the centre, drawn with
       * `lighter` straight over a relic body already sitting at 0.892 luma.
       * The ball was not lit by Daybreak, it was ERASED by it: measured on
       * the caster's disc, 0.499 bare -> 0.905 at the peak with 58% of the
       * disc past 0.98, and only +0.041 of that came from the bloom. Rick
       * watched it and said the white balls were washed out; the bloom got
       * the blame and the bloom was a bystander.
       *
       * The gradient's own numbers are UNCHANGED -- same stops, same reach,
       * same alpha -- so the light around the ball is exactly as bright as it
       * was. All that changed is that nothing is painted over the body.
       *
       * THE HOLE HAS TO BE CUT IN THE PATH. A radial gradient with an inner
       * radius still fills its inner circle with colorStop(0), so moving the
       * inner radius out to R alone would have left the white centre exactly
       * where it was and looked like the fix had done nothing. The second arc
       * is wound backwards to subtract it. */
      c.globalCompositeOperation = "lighter";
      const pulse = 0.92 + 0.08 * Math.sin(u.t * 13);
      const g = c.createRadialGradient(src.x, src.y, R * 0.94, src.x, src.y, R * 2.3 * pulse);
      g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.4, "#FFF6E288");
      g.addColorStop(1, "#FFD98A00");
      c.globalAlpha = 0.8 * k2;
      c.fillStyle = g;
      c.beginPath(); c.arc(src.x, src.y, R * 2.3 * pulse, 0, TAU);
      c.arc(src.x, src.y, R * 0.94, TAU, 0, true); c.fill();
      /* flame tongues: deterministic flicker, licking upward off the shell */
      for (let i = 0; i < 9; i++){
        const a0 = (i / 9) * TAU + Math.sin(u.t * (2.1 + shellHash(19, i)) + i) * 0.25;
        const flick = 0.55 + 0.45 * Math.sin(u.t * (9 + shellHash(29, i) * 5) + i * 2.1);
        const len = (R * 0.9 + shellHash(39, i) * R * 0.8) * flick;
        const bx = src.x + Math.cos(a0) * (R + 2), by = src.y + Math.sin(a0) * (R + 2);
        const tx2 = src.x + Math.cos(a0) * (R + 2 + len * 0.4) - 0 ;
        const ty2 = by - len;                       // heat goes UP
        c.globalAlpha = k2 * 0.55 * flick;
        c.strokeStyle = i % 3 ? "#FFF6E2" : "#FFFFFF";
        c.lineWidth = 3.2 - (i % 3);
        c.beginPath();
        c.moveTo(bx, by);
        c.quadraticCurveTo(bx + Math.cos(a0) * len * 0.3, by - len * 0.5, tx2, ty2);
        c.stroke();
      }
      /* the ignition ring, once, at the cast */
      const ring = clamp(u.t / 0.4, 0, 1);
      if (ring < 1){
        c.globalAlpha = (1 - ring) * 0.9;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 4 * (1 - ring * 0.5);
        c.shadowColor = "#FFFFFF"; c.shadowBlur = 16;
        c.beginPath(); c.arc(src.x, src.y, R + 130 * ring, 0, TAU); c.stroke();
        c.shadowBlur = 0;
      }
      c.globalCompositeOperation = "source-over";
    }

''',
 ''''''),

('''restyle the HUD sigil (shards out)''',
 '''  /* DAYBREAK -- the sun comes up. Rays turn, the disc rises with the charge,
     and four shards orbit because a spark field IS the mechanic. */
  dawnbringer(c, t, cf, P){
    const rise = 0.42 - cf * 0.46;
    SG.spokes(c, 12, 0.52, 0.96 + Math.sin(t * 2) * 0.04, t * 0.34, P.glow, 0.07, 0.34 + cf * 0.5);
    c.save(); c.beginPath(); c.rect(-1.1, -1.1, 2.2, 1.1 + rise); c.clip();
    SG.disc(c, 0, rise, 0.44, P.core, 0.55 + cf * 0.45);
    c.restore();
    SG.path(c, [[-0.86, rise], [0.86, rise]], P.glow, 0.075, 0.9);
    for (let i = 0; i < 4; i++){
      const a = t * 1.5 + i * TAU / 4;
      SG.shard(c, Math.cos(a) * 0.74, rise - 0.34 + Math.sin(a) * 0.26,
               0.1 * (0.35 + cf), t * 2 + i, P.glow, 0.35 + cf * 0.6);
    }
  },
''',
 '''  /* DAYBREAK -- the sun comes up. Rays turn, and the horizon RISES with the
     charge carrying the half-sun on it, which is now the ultimate itself: a
     line of light climbing the hall. The four orbiting shards are gone with
     the sparks they stood for (v86: "sparks out"). */
  dawnbringer(c, t, cf, P){
    const rise = 0.42 - cf * 0.46;
    SG.spokes(c, 12, 0.52, 0.96 + Math.sin(t * 2) * 0.04, t * 0.34, P.glow, 0.07, 0.34 + cf * 0.5);
    c.save(); c.beginPath(); c.rect(-1.1, -1.1, 2.2, 1.1 + rise); c.clip();
    SG.disc(c, 0, rise, 0.44, P.core, 0.55 + cf * 0.45);
    c.restore();
    SG.path(c, [[-0.86, rise], [0.86, rise]], P.glow, 0.075, 0.9);
  },
'''),

('''retire the banner’s horizon''',
 '''    if (b.w === "dawnbringer"){
      fn = (i) => ({ dy: -(1 - ease(clamp((age - i * 0.012) / 0.13, 0, 1))) * 230 * k });
      if (age > 0.09 && age < 0.55){
        const k2 = (age - 0.09) / 0.46;
        c.save();
        c.globalCompositeOperation = "lighter";
        c.shadowBlur = 0;
        c.globalAlpha = (1 - k2) * 0.5;
        c.fillStyle = "#FFE7A8";
        c.fillRect(cx - A.w * 0.5 * k2, y + 12 * k, A.w * k2, (3 + 9 * (1 - k2)) * k);
        c.restore();
      }
    }
''',
 '''    if (b.w === "dawnbringer"){
      /* THE LETTERS RISE -- a sunrise -- AND THE HORIZON THAT SWEPT OUT UNDER
         THEM IS GONE. The dawn line is now the ultimate: it appears at the
         floor on the same frames, and a second full-width line of light at
         the CASTER's height, brighter than the real one while it brightens,
         would teach the viewer the wrong line. */
      fn = (i) => ({ dy: -(1 - ease(clamp((age - i * 0.012) / 0.13, 0, 1))) * 230 * k });
    }
'''),

('''the ultFx life map: say what dawnbringer’s entry is now''',
 '''      life: { dawnbringer: 1.6, widowmaker: 1.3, grudgebearer: 1.7,
''',
 '''      /* DAYBREAK (v97) IS NO LONGER A SET-PIECE ON THIS SLOT. Its dawn is an
         8s window drawn off the fighter (`drawDawn`), where the one ultFx
         slot cannot erase it; the pool and the corona that read this record
         are retired and its field spec is out, so this entry carries the
         CAST's record and nothing draws from it -- as for Corollary. */
      life: { dawnbringer: 1.6, widowmaker: 1.3, grudgebearer: 1.7,
'''),

]


SYNC_FX_WRITE: list = []


def sync_fx_remove(s: str) -> str:
    """The sparks' field spec out of BOTH copies (v86 §5), cindercleave's and
    corollary's `sync_fx` shape: the whole inlined module compared to
    src/render/fx.js before and after, both stamps re-cut. No replacement:
    the dawn's mote drift rides a moving foe for 8s, which the one-slot field
    cannot carry, so it is drawn (v97 §4)."""
    fx_js = HERE.parent / "src" / "render" / "fx.js"
    mod = fx_js.read_text(encoding="utf-8")
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    if s[head.end():tm.start()].rstrip("\n") != mod.rstrip():
        if FX_OLD not in mod and FX_OLD in s:
            raise SystemExit("src/render/fx.js already lacks the spec but the page "
                             "still has it -- a rebuild: restore fx.js first "
                             "(git checkout -- src/render/fx.js)")
        raise SystemExit("src/render/fx.js and the inlined copy have DIVERGED "
                         "before this builder wrote anything")
    if mod.count(FX_OLD) != 1 or s.count(FX_OLD) != 1:
        raise SystemExit("the sparks' fx spec is not exactly once in both copies")
    mod2 = mod.replace(FX_OLD, "", 1)
    s = s.replace(FX_OLD, "", 1)
    old_sha = head.group(1)
    new_sha = hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    s = s.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
    head2 = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                      r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    tm2 = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head2.end())
    if s[head2.end():tm2.start()].rstrip("\n") != mod2.rstrip():
        raise SystemExit("the inlined copy and src/render/fx.js DIVERGED across "
                         "this builder's own write")
    SYNC_FX_WRITE.append((fx_js, mod2))
    print(f"  fx    the sparks' spec out of both copies; stamp "
          f"{old_sha[:16]} -> {new_sha[:16]}")
    return s

def relic_ult(code: str) -> str:
    """The ult block of Dawnbringer's weapon entry, comments stripped."""
    i = code.find('id:"dawnbringer"')
    if i < 0:
        raise SystemExit("no Dawnbringer in this source -- wrong build")
    j = code.find("ult:{", i)
    k = code.find("},", j)
    return code[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "3"], required=True)
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
    print(f"\nDAWNBRINGER / DAYBREAK -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")

    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Corollary
    # through its apply-contract fix (stage 5) on top of sc-leaf.
    for need, why in (("s.over.stop = 0.02 * s.rung;", "no Winnowing rung stop"),
                      ("echoShown", "no Corollary stage 4 -- not the chain tip"),
                      ('tgt.apply("hex", u.hex, f === this.a ? "a" : "b")',
                       "no Corollary stage 5"),
                      ('name:"Corollary", charge:14, kind:"echo"',
                       "no Corollary stage 6 (charge 14) -- build on sc-corollary-c14")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    print("  base  sc-leaf's line + Axiom / Corollary stages 1-6 -- the chain tip")

    if A.stage == "1":
        if "ultDawn" in code:
            raise SystemExit("this source already carries stage 1 -- built")
        if strip_comments(SHIPPED_ULT) not in code:
            raise SystemExit("Dawnbringer's shipped Daybreak is not in this source "
                             "as shipped -- the base has moved under the builder")
        edits = S1
    else:
        if "ultDawn" not in code:
            raise SystemExit("stage 3 needs stage 1 under it -- no dawn here")
        if "dawnShown" in code:
            raise SystemExit("this source already carries stage 3 -- built")
        edits = S3
    for label, old, new in edits:
        s = one(s, old, new, label)
    if A.stage == "3":
        s = sync_fx_remove(s)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if strip_comments(ult_block()).strip() != blk.strip():
        raise SystemExit(f"REFUSING TO WRITE -- Dawnbringer's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the doc's: {tip!r}")
    print(f"  ok    ult   {blk.splitlines()[0].strip()} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S3:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws "
                             "the match RNG")
    kinds = re.findall(r'kind:"dawn"', out_code)
    if len(kinds) != 1:
        raise SystemExit(f"REFUSING TO WRITE -- {len(kinds)} dawn ultimates, "
                         "expected exactly Dawnbringer's")
    if re.search(r'kind:"radiant"', out_code):
        raise SystemExit("REFUSING TO WRITE -- a relic still carries "
                         "kind:\"radiant\"; the sparks are not out")
    print("  ok    one dawn ultimate, Dawnbringer's; no relic is radiant; no "
          "insert draws the RNG")
    if A.stage == "3":
        # THE SPARKS-ERA ART IS GONE: no ult renderer keys on Dawnbringer's
        # ultFx any more, and the sparks' field is out of both copies.
        if 'u.w === "dawnbringer"' in out_code:
            raise SystemExit('REFUSING TO WRITE -- art still keyed on u.w === "dawnbringer"')
        if FX_OLD in s or re.search(r"\bdawnbringer: \{ mode:", strip_comments(s)):
            raise SystemExit("REFUSING TO WRITE -- the sparks' field spec is still in the page")
        print('  ok    sparks-era art retired (no u.w === "dawnbringer"), the '
              "sparks' field spec out")

    syntax_check(s, out_p.name)
    for fx_js, mod2 in SYNC_FX_WRITE:        # tracked src/render/fx.js, last
        fx_js.write_text(mod2, encoding="utf-8", newline="\n")
        print(f"  wrote {fx_js.relative_to(HERE.parent)}")
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    print(f"  charge {ULT['charge']}  window {ULT['dur']}  tick {ULT['tick']}s  "
          f"{ULT['tickDmg']} dmg + smite {ULT['smite']}   blade 10.4 "
          "(the doc's and Rick's; not bisected)")
    print("\n  GATE -- in this order, and each can fail:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids <the 33 others> --n 8")
    print(f"    python dawn_probe.py --game {A.out}")
    print("    relic at 10.4 against stage 0's arm B on 151 (the lab)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
