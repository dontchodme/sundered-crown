#!/usr/bin/env python
"""DAWNBRINGER / DAYBREAK, THE CIRCLE -- Rick's redesign. v99.

Built from `06-docs/v99/DAYBREAK-CIRCLE-BUILD-BRIEF.md` and
`dawnbringer-daybreak-circle-design-v99.md` (Cowork, 2026-09-27), which are
the input and the only input. CLAUDE.md §3 rule 0: nothing here is a design
decision.

    stage 1   the line out, the sun in     <tip> -> sc-sunrise.html
    stage 2   the blade                    confirm 10.4 wide on 151 (no link unless it moves)
    stage 3   picture, voice, beat         sc-sunrise -> sc-sunrise-fx.html

§1: "For a while the sun is in the blade. The first blow that lands breaks the
dawn where it lands: a circle of sunlight spreads out from that point over two
seconds, and stays for eight. An enemy standing in the sunlight is smitten and
burned for as long as it stays there."

Declared (design §4, brief §1): the cast ARMS the blade and nothing resolves.
The first blow Dawnbringer LANDS while armed sets the sun at that blow's own
hit point `hx, hy`. `r = 200 * min(1, t / 2)`; a foe is inside while its
centre is within `r + ballR`. Every 0.5s while inside: `foe.apply("smite", 1,
side)` then `hurt(foe, 2, f)` -- ward first, nothing else, no beat but the
killing tick's. The sun sets at `t >= 8` or when Dawnbringer dies. A cast
while a sun is up re-arms the blade; the next landed blow breaks a new dawn
and the old one sets. The arming has no time limit. The caster gets nothing.

THE NAMES ARE NOT THE BRIEF'S, AND THAT IS A COLLISION, NOT A DECISION. The
brief says `f.ultSun`, `tickSun` and a beat flag `sun:true`; all three are
ZENITH's (v71, `morningstar_build.py`), built on this link before the brief
was written against `sc-corollary-c14`. So this relic's state is
`ultSunrise`, its ticker `tickSunrise` and its beat flag `sunrise:true`,
matching the block's `kind:"sunrise"`, which the brief does name.

THE CHARGE. 14: the lab's 16 on the game's clock (Rick's batch ruling,
2026-09-27), measured for this fighter on the line (v97 §2a).

THE READINGS, where the build has to choose and the doc or the engine decides:
  1. THE TICK'S CADENCE is the lab's (`overlays/daybreak_circle.js`): a 0.5s
     cooldown that runs through the sun's whole life and fires on the first
     inside frame it is clear, zeroed at the break.
  2. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract; the lab passes
     the Fighter). Smite ticks damage, and a fatal smite tick is attributed by
     that letter.
  3. "NO BEAT" FOR A TICK -- except a tick that KILLS, which files its own
     `fatal: true` hit beat (the engine's standing rule for a side-channel
     kill; the line's reading 3).
  4. THE ANCHOR IS THE BLOW'S OWN HIT POINT, as §4 declares, where the lab
     used the foe's centre. The probe measures the inside share both ways.
     A blow that lands on one of Twinshade's shades is a blow that landed,
     so the sun comes up where it landed; the lab anchored on the real foe.
  5. THE BREAK FILES A BEAT at the hit point, with the cast beat's own kind
     and fields and `sunrise: true` (brief §1, rule 3). A beat is write-only.
  6. THE TARGET IS THE OPPONENT, never a shade (the lab lights only `foe`).
  7. ARMED AND UP ARE TWO FLAGS ON ONE RECORD: a re-cast while a sun is up
     re-arms the blade and leaves that sun burning until the next break (the
     lab keeps its circle until a new break replaces it).

THE CLOCK. The sun's life and the tick cooldown run on the window tickers'
clock, which stops through a hit stop (tickDawn's and tickSun's convention);
the lab counted every step. So the rim starts moving when the blow that broke
the dawn lets the world go.

STAGE 3's READINGS (the picture, measured by `sunrise_sheet.py`):
  8. THE WASH BREATHES AT ITS SOURCE: +-0.03 on the core's stop, the rim's
     0.20 held. With the breath on both stops the step across the rim fell
     under the brief's 0.12 for half of every cycle (0.17 at the trough).
  9. THE BREAK'S FLASH IS CUT OUT OF BOTH BALLS. The design lets it touch a
     ball; at its 70 it lifted a struck ball's disc by up to +0.31 and past
     the 0.90 ceiling. What is left is the bloom's spill, and the bloom adapts
     to the frame, so the flash's own brightness barely moves it (+0.20 at
     0.55, +0.19 at 0.22): the brightness is kept.
 10. EVERY MARK THAT LIVES A SET TIME IS STAMPED ON THE MATCH CLOCK, which
     runs through a hit stop -- the presentation clock runs twice a normal
     step and once a frozen one, and every break opens with a freeze.
 11. THE NUMBER IS THE DESIGN'S: gold, size 24 (this engine sizes a number by
     its damage). Measured, gold on the amber wash reads a little under the
     echo's pale-blue number on two foes of three; the fix is the colour or
     the size, and both are the design's.

THE BASE is the batch's chain tip, `sc-zenith.html` (sc-leaf + Corollary at
charge 14 + the line through its stage 3 + Zenith through its stage 4), named
and asserted. `--src` takes any later tip that still carries the line: the
design batch is building Ironwood on the same link on DESKTOP-DERRAFT, and
whichever lands second is re-applied onto the other's tip.

THE LINE COMES OUT AS WHOLE SPANS (brief §1): every span v97 inserted, sim and
picture and voice, cut by start and end marker and PINNED BY sha256, so a
carry onto a tip where somebody has edited one of them refuses instead of
cutting something else. The HUD sigil, the banner's rising letters and the
ultFx cast record stay; their comments stop describing the line.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "dawnbringer"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling)
    "dur": 8,         # "life 8s from the contact"
    "grow": 2,        # "r = 200 * min(1, t/2)" -- up in 2s, then UP
    "r": 200,         # "the sun r 200"
    "tick": 0.5,      # "every 0.5s"
    "tickDmg": 2,     # "hurt 2" -- the line's feed (design §3)
    "smite": 1,       # "smite +1"
}
TIP = "The next blow breaks the dawn where it lands; foes in the sunlight burn"

LINE_ULT = '''    ult:{ name:"Daybreak", charge:14, kind:"dawn", dur:8,
         tick:0.5, tickDmg:2, smite:1,
         tip:"The sun rises up the hall: foes below the dawn line are smitten and burn" },'''


def ult_block() -> str:
    u = ULT
    return (f'''    ult:{{ name:"Daybreak", charge:{u["charge"]}, kind:"sunrise", dur:{u["dur"]}, grow:{u["grow"]}, r:{u["r"]},
         tick:{u["tick"]}, tickDmg:{u["tickDmg"]}, smite:{u["smite"]},
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


def cut(src: str, c: dict) -> str:
    """Remove one whole span of the line: from `start` (unique) THROUGH the
    first `end_incl` after it -- the line's OWN last text, so code another
    builder has since put AFTER the span (Zenith's stage 6 did, beside three
    of them) is never inside it -- and the span's sha256 exactly the one read
    off sc-zenith. A span somebody has edited since is refused, not cut."""
    a, b = c["start"], c["end_incl"]
    if src.count(a) != 1:
        raise SystemExit(f"CUT {c['label']}: start marker found {src.count(a)} "
                         f"times, expected 1:\n  {a[:90]!r}")
    i = src.find(a)
    j = src.find(b, i)
    if j < 0:
        raise SystemExit(f"CUT {c['label']}: no end after the start")
    j += len(b)
    span = src[i:j]
    sha = hashlib.sha256(span.encode("utf-8")).hexdigest()[:16]
    if sha != c["sha"]:
        raise SystemExit(f"CUT {c['label']}: the span is not the one this builder "
                         f"was written against (sha {sha}, pinned {c['sha']}).\n"
                         f"  Somebody has edited the line since sc-zenith -- find "
                         f"out what before cutting it.")
    d = span.count("/*") - span.count("*/")
    if d:
        raise SystemExit(f"CUT {c['label']}: the span's comment balance is {d:+d}")
    print(f"  cut   {c['label']:<44} {span.count(chr(10)):>3} lines  sha {sha}")
    return src[:i] + c.get("new", "") + src[j:]


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
# THE LINE OUT: v97's spans, whole. Dicts and not tuples, so `chain_audit`
# (which discovers `(label, old, new)` tuples) audits this builder's INSERTS
# and is not handed six removals with nothing in them to survive.
CUTS1 = [
    dict(label="the line's picture fields (dawnFade .. dawnTagged)",
         start="    /* DAYBREAK'S PICTURE (v86 §4), and none of it is the window:",
         end_incl="    this.dawnTagged = false;\n",
         sha="c6935d486ac9cefb"),
    dict(label="the line's presentation clock (tickPresentation)",
         start="      /* AND THE DAWN'S. Every `life` in this method is in HALF-SECONDS",
         end_incl="          f.dawnAge += dt;\n        }\n      }\n",
         sha="143983db5e827cfe"),
    dict(label="the line's draw call (world pass)",
         start="    /* DAYBREAK'S DAWN, ON THE FLOOR: over the hall's own paint",
         end_incl="    if (__world) this.drawDawn(m);\n",
         sha="f8d5b395269bb76f"),
    dict(label="drawDawn",
         start="  /* ------------------------------------------------------------ THE DAWN ---",
         end_incl="    c.restore();\n  }\n\n",
         sha="cc3d0e0d8ebcacfe"),
    dict(label="the line's voices (cast, steps 1-7, close)",
         start='if (w === "dawnbringer" || w === "dawnbringer-step"){',
         end_incl='}).frequency.value = f;\n        } else ',
         sha="56d97181b911a685"),
]

# THE SUN IN. tickDawn and the SMITE tag that rode it go as one span, and the
# sun's ticker takes their place; everything else is a one-for-one edit.
TICK_SUNRISE = '''  /* =================================================== THE SUNRISE ====
     v99 §4 / brief §1. The sun is a circle anchored where the blow that broke
     it LANDED (`S.x, S.y`, set in `resolveHit`), of radius
     `r * min(1, t / grow)` -- up in `grow` seconds and UP after that -- for
     `dur` seconds from the contact. A foe whose centre is within the radius
     plus R is inside, and every `tick` seconds while inside it is smitten
     +`smite` and takes `tickDmg` through `hurt`: ward first and NOTHING ELSE
     -- no crit, no knock, no hit stop, no hitstun -- and no beat, except the
     tick that KILLS, which files its own (the engine's rule for a
     side-channel kill; the builder's reading 3). The caster gets nothing.

     THE COOLDOWN RUNS THROUGH THE SUN'S WHOLE LIFE, inside or not, and a tick
     fires on the first inside frame it is clear: the lab's cadence, and what
     was priced. On the window tickers' clock, so it freezes through a hit
     stop -- the blow that breaks the dawn opens with its own, and the rim
     starts moving when the world does.

     ARMED AND UP ARE TWO FLAGS ON ONE RECORD, because a cast while a sun is
     up re-arms the blade and leaves that sun burning (v99 §4): it sets when
     the next landed blow breaks a new one. The record goes when neither is
     true, and at once when the caster dies. The target is the OPPONENT only,
     never a shade.

     THE SOURCE IS A SIDE LETTER (Fighter.apply's contract): smite ticks
     damage, and a fatal smite tick is attributed by it. */
  tickSunrise(dt){
    for (const f of [this.a, this.b]){
      const S = f.ultSunrise;
      if (!S) continue;
      if (!f.alive){ f.ultSunrise = null; continue; }
      if (!S.up) continue;
      S.t += dt;
      const u = f.w.ult;
      if (S.t >= u.dur){
        S.up = false;
        if (!S.armed) f.ultSunrise = null;
        continue;
      }
      const T = f.sunriseTally, foe = f === this.a ? this.b : this.a;
      const r = u.r * Math.min(1, S.t / u.grow);
      S.cd -= dt;
      T.frames++;
      if (!foe.alive
          || !(Math.hypot(foe.x - S.x, foe.y - S.y) < r + CONFIG.physics.ballR))
        continue;
      T.litFrames++;
      if (S.cd > 0) continue;
      S.cd = u.tick;
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
                    shotSpd0: 0, sunrise: true });
    }
  }

'''

S1 = [

("dawnbringer's ultimate is the circle",
 LINE_ULT,
 ult_block()),

("the fighter carries the sun: armed, up, where, how long",
 '''    /* {t, dur, cd} while DAYBREAK's dawn is rising (v86). null on every other
       relic and on this one outside its window: `tickDawn` returns after a
       two-iteration loop that does nothing. `dawnTally` is the probe's count,
       cumulative over the fight; nothing in the simulation reads it. */
    this.ultDawn = null;
    this.dawnTally = null;
''',
 '''    /* {armed, up, x, y, t, cd} while DAYBREAK's sun is in the blade or up
       (v99). null on every other relic and on this one before its first
       cast: `tickSunrise` returns after a two-iteration loop that does
       nothing, and the break in `resolveHit` is one `if (self.ultSunrise)`.
       NOT `ultSun`: that name is ZENITH's (v71), built on this link before
       the brief that asked for it was written. `sunriseTally` is the probe's
       count, cumulative over the fight; nothing in the simulation reads it. */
    this.ultSunrise = null;
    this.sunriseTally = null;
'''),

("the cast arms the blade and resolves nothing",
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
''',
 '''    if (u.kind === "sunrise"){
      /* DAYBREAK, THE CIRCLE (v99). THE CAST PUTS THE SUN IN THE BLADE AND
         NOTHING RESOLVES HERE: the next blow Dawnbringer lands breaks the dawn
         where it lands (`resolveHit`), and `tickSunrise` does everything the
         sun does. The arming has no time limit. A cast while a sun is UP
         re-arms the blade and leaves that sun burning -- the next landed blow
         breaks a new dawn and the old one sets. The charge runs from the
         cast, as for every window ultimate. The sparks stay out: nothing sets
         `ultRadiant`, and the spark machinery stays for Lastlight. */
      if (f.ultSunrise) f.ultSunrise.armed = true;
      else f.ultSunrise = { armed: true, up: false, x: 0, y: 0, t: 0, cd: 0 };
      if (!f.sunriseTally)
        f.sunriseTally = { casts: 0, breaks: 0, ticks: 0, dealt: 0,
                           litFrames: 0, frames: 0 };
      f.sunriseTally.casts++;
      return;
    }
'''),

("the blow that lands breaks the dawn where it lands",
 '''      if (crit) self.echoTally.crits++;
    }

    const fatal = foe.hp <= 0;
''',
 '''      if (crit) self.echoTally.crits++;
    }
    /* DAYBREAK'S BREAK (v99). HERE, BESIDE `self.hits++`, FOR COROLLARY'S
       REASON ONE BLOCK UP: this line is what "a blow landed" means in this
       engine, and it is what the lab counted. The first blow Dawnbringer
       lands with the sun in the blade breaks the dawn WHERE IT LANDED --
       `hx, hy`, the blow's own contact point, not the foe's centre (the lab
       anchored at the centre; the hit point sits on the rim, and the probe
       prices the difference). A blow on one of Twinshade's shades is a blow
       that landed. `cd` starts at zero, so the foe is struck on the first
       frame the rim reaches it.

       THE BREAK FILES A BEAT at the contact, with the cast beat's kind and
       fields and `sunrise: true` (rule 3): the set-piece starts HERE, not at
       the cast, and the director has to be able to find it. A beat is
       write-only; nothing in the simulation reads it. */
    if (self.ultSunrise && self.ultSunrise.armed){
      const S = self.ultSunrise, opp = self === this.a ? this.b : this.a;
      S.armed = false; S.up = true; S.x = hx; S.y = hy; S.t = 0; S.cd = 0;
      self.sunriseTally.breaks++;
      this.beat({ kind: "ult", side: self === this.a ? 0 : 1, x: hx, y: hy,
                  w: self.w.id, foeHpFrac: opp.hp / opp.maxHp, sunrise: true });
    }

    const fatal = foe.hp <= 0;
'''),

("the sun ticks with the window tickers, in the line's place",
 '''    this.tickDawn(dt);                  // DAYBREAK (v86)
''',
 '''    this.tickSunrise(dt);               // DAYBREAK, THE CIRCLE (v99)
'''),

("the ultFx life map: say what dawnbringer's entry is now",
 '''      /* DAYBREAK (v97) IS NO LONGER A SET-PIECE ON THIS SLOT. Its dawn is an
         8s window drawn off the fighter (`drawDawn`), where the one ultFx
         slot cannot erase it; the pool and the corona that read this record
         are retired and its field spec is out, so this entry carries the
         CAST's record and nothing draws from it -- as for Corollary. */
''',
 '''      /* DAYBREAK (v99) IS NOT A SET-PIECE ON THIS SLOT. Its sun comes up at
         the next landed blow, not at the cast, and lives 8s off the FIGHTER
         (`ultSunrise`), where the one ultFx slot cannot erase it (open item
         25); the sparks-era pool and corona that read this record were
         retired in v97 and its field spec is out, so this entry carries the
         CAST's record and nothing draws from it -- as for Corollary. */
'''),

("the HUD sigil's comment stops describing the line",
 '''  /* DAYBREAK -- the sun comes up. Rays turn, and the horizon RISES with the
     charge carrying the half-sun on it, which is now the ultimate itself: a
     line of light climbing the hall. The four orbiting shards are gone with
     the sparks they stood for (v86: "sparks out"). */
''',
 '''  /* DAYBREAK -- the sun comes up. Rays turn, and the horizon RISES with the
     charge carrying the half-sun on it: the charge IS the sun coming up.
     (v99: the ultimate itself is a circle of sunlight breaking where the
     next blow lands; the sigil is the charge, not the mechanic.) The four
     orbiting shards are gone with the sparks they stood for (v86). */
'''),

("the banner's comment stops describing the line",
 '''      /* THE LETTERS RISE -- a sunrise -- AND THE HORIZON THAT SWEPT OUT UNDER
         THEM IS GONE. The dawn line is now the ultimate: it appears at the
         floor on the same frames, and a second full-width line of light at
         the CASTER's height, brighter than the real one while it brightens,
         would teach the viewer the wrong line. */
''',
 '''      /* THE LETTERS RISE -- a sunrise -- AND THE HORIZON THAT SWEPT OUT UNDER
         THEM STAYS GONE (v97). The sun now comes up where the next blow
         lands (v99), and a full-width line of light at the CASTER's height
         at the cast would put light where the ultimate is not. */
'''),

]


# THE TICKER GOES IN THROUGH `cut` (it takes tickDawn's span), which is a dict
# `chain_audit` cannot see -- so it is ALSO named here as a row, and the audit
# watches the one insert this relic cannot do without.
S1_TICK = [("tickSunrise, the sun's ticker (in tickDawn's span)", "", TICK_SUNRISE)]


def cut_tick(src: str) -> str:
    """tickDawn and the SMITE tag that rode it: one span, and the sun's
    ticker in its place."""
    return cut(src, dict(
        label="tickDawn and dawnShown -> tickSunrise",
        start="  /* DAYBREAK'S SMITE TAG -- ON A CROSSING, NEVER ON A TICK.",
        end_incl="                    shotSpd0: 0, dawn: true });\n    }\n  }\n\n",
        sha="bdd40c94a794f278",
        new=TICK_SUNRISE))


# ---------------------------------------------------------------- stage 3 --
# PICTURE, VOICE AND THE TICK'S MARKS: design §4.1 and §4.2 as written. Every
# mark is presentation -- engine_ab WITH Dawnbringer in the roster is the
# proof -- and the two picks that are Code's (the rim's crossing flare and the
# arming smear) are named where they are drawn.

# THE VOICES' LEVELS, AND THE ONLY PLACE THEY LIVE: solved by
# `sunrise_voice_lab.py` against a blow (the `hit` voice at the blade's 10.4)
# to design §4.2's bounds, on the loudest 50 ms through the shipped chain.
VOICE = {
    "hum": 0.0239,     # the arming: -16 dB under a blow
    "mallet": 0.02028,   # the break's mallet tick, 30 ms
    "bell": 0.06085,     # the break's bell: -4 dB under a blow
    "up": 0.007317,      # the shimmer: -20 dB under a blow
    "set": 0.009146,     # the sunset's held top note
    "siz": 0.1783,      # the tick's sizzle: the tick -10 dB under a blow
    "chime": 0.1019,    # the tick's chime
}


def voices_js(V: dict) -> str:
    """Daybreak's voices, as the synth's `ult` arms -- and the ONLY copy: the
    voice lab renders exactly this text."""
    return f'''if (w === "dawnbringer" || w === "dawnbringer-arm"){{        // the sun in the blade
          /* DAYBREAK'S ARMING (v99 §4.2): "a low warm tone, re-struck every
             0.25s in phase, rising a minor third over the first 3s and holding
             there ... It is tension, and it STOPS on the break." The bare id is
             the cast (fireUlt plays it for every relic) and strikes the root;
             `tickSunrise` plays `-arm` every quarter second of arming on the
             window clock, `n` the step up the third -- A3, B3, then C4, held.
             ONE STRIKE A CALL, so the hum stops the moment the calls do: the
             break, a death, the end of the fight.
             IN PHASE: a strike is placed a whole number of cycles after the
             first one at its pitch, and `.frequency.value` is set after `_tone`
             (v97: Chromium starts the phase off the param's 440 Hz default). */
          const n = w === "dawnbringer" ? 0 : Math.max(0, Math.min(2, p.n | 0));
          const f = [220, 246.94, 261.63][n];
          const H = this.sunHum;
          let s = t;
          if (w === "dawnbringer" || !H || H.f !== f) this.sunHum = {{ t0: t, f }};
          else s = H.t0 + Math.ceil((t - H.t0) * f - 1e-6) / f;
          this._tone(s, {{ freq: f, gain: {V["hum"]}, dur: 0.42, type:"triangle" }}).frequency.value = f;
        }} else if (w === "dawnbringer-break"){{                    // the dawn breaks
          /* THE BELL (v99 §4.2): "one struck bell (modes 1 : 2.4 : 4.1) on
             ~880 Hz with a 30 ms mallet tick, audible >= 400 ms, peaking
             within 15 ms of the hit, -4 dB under a blow. On the same frame as
             the blow's own hit voice." The hum is over -- no more strikes are
             called -- and the shimmer's phase is counted from here. */
          this.sunHum = null;
          this.sunUp = {{ t0: t }};
          this._burst(t, {{ freq: 4800, q: 1.8, gain: {V["mallet"]}, dur: 0.030, type:"bandpass" }});
          [[880, 1.00, 1.40], [2112, 0.45, 0.90], [3608, 0.22, 0.60]].forEach(([fq, k, d]) =>
            this._tone(t, {{ freq: fq, to: fq * 0.998, gain: {V["bell"]} * k, dur: d,
                            type:"sine" }}));
        }} else if (w === "dawnbringer-up"){{                       // the sun is up
          /* THE SHIMMER (v99 §4.2): "a quiet shimmer pad (two re-struck sines a
             fifth apart, 0.5s period, in phase), -20 dB under a blow, running
             while the sun is up." `tickSunrise` calls it every half second of
             the sun's own clock. A4 and E5 are both whole cycles on a 1/220 s
             grid, so a strike placed on that grid after the break is in phase
             with every strike before it. */
          const U = this.sunUp || (this.sunUp = {{ t0: t }});
          const s = U.t0 + Math.ceil((t - U.t0) * 220 - 1e-6) / 220;
          this._tone(s, {{ freq: 440, gain: {V["up"]}, dur: 1.0, type:"sine" }}).frequency.value = 440;
          this._tone(s, {{ freq: 660, gain: {V["up"]} * 0.8, dur: 1.0, type:"sine" }}).frequency.value = 660;
        }} else if (w === "dawnbringer-set"){{                      // sunset
          /* "the shimmer's top note held 0.4s and released over 380 ms (v97's
             STOP shape), only on a clock sunset". E5 re-struck every 15 cycles
             (22.7 ms) on the shimmer's own grid, in phase, for 0.4 s; the last
             strike's own 0.5 s decay is the release. `tickSunrise` plays it on
             a clock sunset only: never on a death, never after the fight. */
          const U = this.sunUp, t0 = U ? U.t0 : t, dt = 15 / 660;
          const s = t0 + Math.ceil((t - t0) * 220 - 1e-6) / 220;
          for (let k = 0; k * dt < 0.4; k++)
            this._tone(s + k * dt, {{ freq: 660, gain: {V["set"]}, dur: 0.5,
                                     type:"sine" }}).frequency.value = 660;
          this.sunUp = null;
        }} else if (w === "widowmaker"){{'''


def tick_voice_js(V: dict) -> str:
    return f'''      else if (kind === "sunrise-tick"){{
        /* DAYBREAK'S TICK -- the one voice that carries the mechanic (v99
           §4.2): "a short warm sizzle-chime, a 1.2 kHz bandpass burst (40 ms)
           over a 660 Hz sine (60 ms), -10 dB under a blow, once per tick, ON
           the tick's frame with the number." Its own kind, as Scour's tick
           is: it is struck twice a second while the foe burns, and `ult` is
           an event. The sine is the shimmer's own top note. */
        this._burst(t, {{ freq: 1200, q: 1.6, gain: {V["siz"]}, dur: 0.040, type:"bandpass" }});
        this._tone (t, {{ freq: 660, gain: {V["chime"]}, dur: 0.060, type:"sine" }});
      }}
      else if (kind === "scour-tick"){{'''


SUNLIGHT_JS = '''/* DAYBREAK'S SUNLIGHT (v99 §4.1): the sun's own three stops, used nowhere else
   in the game. The school's `glow` is #FFFFFF and a white wash is what Rick
   called dull; amber over a hall of #07050C reads as warm light and gives the
   bloom nothing white to find outside the core. */
const SUNLIGHT = { core: "#FFF6E2", gold: "#FFD98A", amber: "#FFB347" };

function shellHash(a, b){
'''

PICTURE_FIELDS = '''    this.ultSunrise = null;
    this.sunriseTally = null;
    /* DAYBREAK'S PICTURE (v99 §4.1) -- none of it is the sun, and nothing in
       the simulation reads any of it. A sun outlives `ultSunrise` by the half
       second it takes to set, and the break, a tick and a crossing each leave
       a mark that outlasts its frame, so the picture keeps its own state: on
       the FIGHTER and never on `m.ultFx` (one slot, and the opponent's cast
       takes it: open item 25). Kept by `tickPresentation`; `sunriseShown`
       stamps the tick's marks from the sim path. EVERY MARK THAT LIVES A SET
       TIME IS STAMPED ON THE MATCH CLOCK (`t + deathAge`), which runs through
       a hit stop: the presentation clock runs twice a normal step and once a
       frozen one, and every break opens with the blow's own freeze, so a flash
       aged on it would outlive its 0.3s by half the freeze.
         sunriseSeen     {x, y, r, t} of the sun last drawn up
         sunriseSets     suns going down where they stood: {x, y, r, t0, life}
         sunriseFlash    the break's flash at the hit point: {x, y, t0}
         sunriseHit      when the last tick flashed the foe's shell
         sunriseIn       the foe's shell touched the light last frame
         sunriseCross    the rim's flares where the foe crossed it: {a, t0}
         sunriseLitFade  the burning foe's embers, up while it is inside
         sunriseTagged   this stretch inside has had its SMITE tag */
    this.sunriseSeen = null;
    this.sunriseSets = [];
    this.sunriseFlash = null;
    this.sunriseHit = -9;
    this.sunriseIn = false;
    this.sunriseCross = [];
    this.sunriseLitFade = 0;
    this.sunriseTagged = false;
'''

SUNRISE_SHOWN = '''  /* DAYBREAK'S TICK, SHOWN (v99 §4.1): "and the other ball burned whenever it
     was inside it." On EVERY tick three things at once -- the number, a flash
     on the shell, the tick's voice -- because the line drew none of them and
     could not be read. The SMITE tag only on the first tick of each stretch
     inside (Corona's rule, and the line's): at two ticks a second, a tag a
     tick would print SMITE a dozen times over one foe. `tickPresentation`
     re-arms it on the first frame the foe is out of the light.
     PRESENTATION ONLY: `floats`, `tags`, `taught` and the fighter's picture
     fields are read by nothing in the simulation, and this runs after the tick
     has resolved. */
  sunriseShown(f, foe){
    this.float(foe.x, foe.y - 50, f.w.ult.tickDmg, SUNLIGHT.gold, 24);
    f.sunriseHit = this.t + (this.deathAge || 0);
    SFX.play("sunrise-tick");
    if (f.sunriseTagged) return;
    f.sunriseTagged = true;
    if (!(foe.hp > 0)) return;                 // the killing tick: the shatter says it
    const first = !this.taught.smite && !!STATUS.smite.tip;
    if (first) this.taught.smite = true;
    this.statusTag(foe.x, foe.y, "smite", first);
  }

  /* =================================================== THE SUNRISE ===='''

PRESENTATION = '''                 : Math.max(0, f.echoFade - dt / 0.45);
      /* AND THE SUN'S (v99 §4.1). NOT in half-seconds: what lives a set time is
         stamped on the MATCH clock, which runs through a hit stop (the fields'
         own comment says why). The sun ITSELF is drawn off the live
         `ultSunrise` with the tick's own radius,
         so the picture is where the hit test is; what lives here is what
         outlasts it. A sun that goes -- by its clock, with its caster, or
         because the next landed blow broke a new one -- is handed to
         `sunriseSets` where it stood and sets there: 0.5s and the core 0.15s
         after, or 0.3s when a new dawn replaced it. At match end the sun that
         is up sets too (`tickSunrise` never runs again once `over` is set, so
         it would otherwise hold the hall lit through the whole verdict). A new
         sun starts the break's flash. The foe's crossings of the rim are
         tested here against the same radius the tick reads, and the SMITE
         tag is re-armed while the foe is out of the light. */
      { const S = f.ultSunrise, u = f.w.ult, now = this.t + (this.deathAge || 0);
        const live = !this.over && S && S.up ? S : null;
        const seen = f.sunriseSeen;
        if (seen && (!live || live.x !== seen.x || live.y !== seen.y || live.t < seen.t)){
          f.sunriseSets.push({ x: seen.x, y: seen.y, r: seen.r, t0: now,
                               life: live ? 0.3 : 0.65 });
          f.sunriseSeen = null;
        }
        if (live){
          const r = u.r * Math.min(1, live.t / u.grow);
          if (!f.sunriseSeen){
            f.sunriseSeen = { x: live.x, y: live.y, r, t: live.t };
            f.sunriseFlash = { x: live.x, y: live.y, t0: now };
            f.sunriseIn = false;
            f.sunriseCross.length = 0;
          } else { f.sunriseSeen.r = r; f.sunriseSeen.t = live.t; }
          const foe = f === this.a ? this.b : this.a, R = CONFIG.physics.ballR;
          const inside = foe.alive
            && Math.hypot(foe.x - live.x, foe.y - live.y) < r + R;
          if (inside !== f.sunriseIn && live.t > 0)
            f.sunriseCross.push({ a: Math.atan2(foe.y - live.y, foe.x - live.x), t0: now });
          f.sunriseIn = inside;
          if (!inside) f.sunriseTagged = false;
          f.sunriseLitFade = inside ? Math.min(1, f.sunriseLitFade + dt / 0.2)
                                    : Math.max(0, f.sunriseLitFade - dt / 0.7);
        } else if (f.sunriseLitFade > 0 || f.sunriseIn){
          f.sunriseIn = false;
          f.sunriseLitFade = Math.max(0, f.sunriseLitFade - dt / 0.7);
        }
        if (f.sunriseSets.length)
          f.sunriseSets = f.sunriseSets.filter(Z => now - Z.t0 < Z.life);
        if (f.sunriseCross.length)
          f.sunriseCross = f.sunriseCross.filter(X => now - X.t0 < 0.15);
        if (f.sunriseFlash && now - f.sunriseFlash.t0 >= 0.3) f.sunriseFlash = null;
      }
'''

DRAW_CALL = '''    if (__world) this.drawArena(m);
    c.scale(this.scale, this.scale);
    /* DAYBREAK'S SUN, ON THE FLOOR: over the hall's own paint and under
       everything that stands in it. The WORLD pass and never the emissive
       one (CLAUDE.md §4.1b/c): no ball is painted by it and none of it is a
       bloom source. The break's flash is drawn over the balls, as light. */
    if (__world) this.drawSunrise(m);
'''

DRAW_SUNRISE = '''  /* ---------------------------------------------------------- THE SUNRISE ---
     Daybreak's circle (v99 §4.1), "a circle of sunlight", and the four things a
     viewer must be able to say with the card off: he swung -- where the sword
     hit, the sun came up -- a circle of sunlight spread out from there -- and
     the other ball burned whenever it was inside it.

     In the WORLD pass right after the arena, under every emissive layer and
     both balls, so no ball is painted by it (CLAUDE.md §4.1b) and none of it is
     a bloom source (§4.1c): the break's flash is the set-piece's only light.
     Clipped to the live hall. Hung off the FIGHTER, never `m.ultFx` (open item
     25). THE LIVE SUN IS READ OFF `ultSunrise` WITH `tickSunrise`'s OWN
     RADIUS, so the rim on screen IS the boundary the tick tests: the foe burns
     while its shell touches the light.

     Brightest to faintest: the RIM (the crispest thing on the floor -- inside
     and outside is the whole verb), the CORE and its RAYS (what makes it read
     as sunlight and not as a status zone), the WASH (gold at the core to amber
     at the rim, so it has a source), the EMBERS. The burning foe's shell flash
     and embers go under its shell, so they rise off it, never across it.

     PRESENTATION ONLY: no rng, no spawnFx, no Math.random -- every mote is
     shellHash on its index against the match clock -- and nothing here writes
     a field the simulation reads. */
  drawSunrise(m){
    const a = m.a, b = m.b;
    const T = m.t + (m.deathAge || 0);
    if (!a.sunriseSeen && !b.sunriseSeen && !a.sunriseSets.length
        && !b.sunriseSets.length && !(T - a.sunriseHit < 0.2) && !(T - b.sunriseHit < 0.2)
        && !(a.sunriseLitFade > 0) && !(b.sunriseLitFade > 0)) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, R = CONFIG.physics.ballR;
    const n = m.inset || 0, yF = A.h - n;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, yF - n); c.clip();
    for (const f of [a, b]){
      /* SUNSET, first, so a new dawn draws over the one it replaced: the rim
         falls to the core while the wash goes with it, and the core winks out
         last -- or all of it in 0.3s when a new dawn broke */
      for (const Z of f.sunriseSets){
        const age = T - Z.t0, rep = Z.life < 0.5, k = Math.min(1, age / (rep ? 0.3 : 0.5));
        const e = 1 - (1 - k) * (1 - k);
        const r = 14 + Math.max(0, Z.r - 14) * (1 - e);
        if (r > 14.5){
          this._sunWash(c, Z.x, Z.y, r, 1 - e, T);
          this._sunRim(c, Z.x, Z.y, r, 1 - e, T, null);
        }
        this._sunCore(c, Z.x, Z.y, Math.min(14, Z.r),
                      rep ? 1 - k : 1 - clamp((age - 0.5) / 0.15, 0, 1));
      }
      const S = f.ultSunrise;
      if (f.sunriseSeen && S && S.up && !m.over){
        const u = f.w.ult, r = u.r * Math.min(1, S.t / u.grow);
        this._sunWash(c, S.x, S.y, r, 1, T);
        this._sunRays(c, S.x, S.y, r, 1, T);
        this._sunEmbers(c, S.x, S.y, r, 1, T);
        this._sunRim(c, S.x, S.y, r, 1, T, f.sunriseCross, T);
        this._sunCore(c, S.x, S.y, Math.min(14, r), 1);
      }
      const foe = f === a ? b : a;
      if (!foe.alive) continue;
      /* THE TICK, ON THE SHELL: a 2-unit gold ring at R + 4, fading 0.2s */
      if (T - f.sunriseHit < 0.2){
        c.globalAlpha = 1 - (T - f.sunriseHit) / 0.2;
        c.strokeStyle = SUNLIGHT.gold; c.lineWidth = 2;
        c.beginPath(); c.arc(foe.x, foe.y, R + 4, 0, TAU); c.stroke();
      }
      /* AND THE BURNING: the line's twelve motes rising off the foe's upper
         disc, gold, at 1.5x their alpha, while it stands in the light */
      const Lf = f.sunriseLitFade;
      if (Lf > 0.01){
        c.fillStyle = SUNLIGHT.gold;
        for (let i = 0; i < 12; i++){
          const ph = (T * (0.50 + 0.30 * shellHash(9101, i)) + shellHash(9103, i)) % 1;
          const ang = -Math.PI / 2 + (shellHash(9107, i) - 0.5) * 2.4;
          const r0 = R * (0.50 + 0.45 * shellHash(9109, i));
          const mx = foe.x + Math.cos(ang) * r0 + Math.sin(T * 1.9 + i * 2.3) * 2.5;
          const my = foe.y + Math.sin(ang) * r0 - ph * 44;
          c.globalAlpha = Math.min(1, Lf * 1.05 * Math.sin(ph * Math.PI));
          c.beginPath();
          c.arc(mx, my, 1.6 * (0.7 + 0.6 * shellHash(9113, i)), 0, TAU);
          c.fill();
        }
      }
      c.globalAlpha = 1;
    }
    c.restore();
  }

  /* THE WASH: a radial gradient from gold at the core (0.35) to amber at the
     rim (0.20), source-over -- brightest where the sun came up, so it reads as
     light with a source and not as a pool -- breathing +-0.03 at 0.8 Hz AT THE
     SOURCE, while the boundary holds. Measured with the breath on the rim's
     stop as well, the step across the rim fell under the brief's 0.12 for
     half of every cycle (0.20 - 0.03 = 0.17 at the trough). */
  _sunWash(c, x, y, r, k, T){
    if (!(r > 0.5) || !(k > 0.004)) return;
    const br = 0.03 * Math.sin(TAU * 0.8 * T);
    const g = c.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, "rgba(255,217,138," + ((0.35 + br) * k).toFixed(4) + ")");
    g.addColorStop(1, "rgba(255,179,71," + (0.20 * k).toFixed(4) + ")");
    c.globalAlpha = 1;
    c.fillStyle = g;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
  }

  /* THE RAYS: ten tapered shafts of amber from the core, 110-170 long (never
     past 0.85 of the rim), alpha 0.22, turning at 0.15 rad/s, their length
     breathing at 0.6 Hz. They are the "glowing" in Rick's sentence. */
  _sunRays(c, x, y, r, k, T){
    if (r < 30 || !(k > 0.004)) return;
    c.fillStyle = SUNLIGHT.amber;
    c.globalAlpha = 0.22 * k;
    c.beginPath();
    for (let i = 0; i < 10; i++){
      const an = i * TAU / 10 + 0.15 * T;
      const ln = Math.min(r * 0.85, 110 + 60 * (0.5 + 0.5 * Math.sin(TAU * 0.6 * T + i)));
      const ca = Math.cos(an), sa = Math.sin(an);
      c.moveTo(x - sa * 4, y + ca * 4);
      c.lineTo(x + ca * ln - sa * 2.1, y + sa * ln + ca * 2.1);
      c.lineTo(x + ca * ln + sa * 2.1, y + sa * ln - ca * 2.1);
      c.lineTo(x + sa * 4, y - ca * 4);
      c.closePath();
    }
    c.fill();
    c.globalAlpha = 1;
  }

  /* THE EMBERS: 24 slow amber motes drifting up through the lit disc -- the
     line's twelve, doubled and warmed -- and only inside the light. */
  _sunEmbers(c, x, y, r, k, T){
    if (r < 20 || !(k > 0.004)) return;
    c.fillStyle = SUNLIGHT.amber;
    for (let i = 0; i < 24; i++){
      const ph = (T * (0.08 + 0.06 * shellHash(9201, i)) + shellHash(9203, i)) % 1;
      const an = shellHash(9205, i) * TAU;
      const rr = Math.sqrt(shellHash(9207, i)) * r * 0.92;
      const ex = x + Math.cos(an) * rr + Math.sin(T * 1.3 + i * 1.7) * 2;
      const ey = y + Math.sin(an) * rr - ph * 40;
      if (Math.hypot(ex - x, ey - y) > r - 3) continue;
      c.globalAlpha = 0.5 * k * Math.sin(ph * Math.PI);
      c.beginPath(); c.arc(ex, ey, 1.5, 0, TAU); c.fill();
    }
    c.globalAlpha = 1;
  }

  /* THE RIM: a 3-unit gold ring at 0.8, shimmering +-0.1 at 1.2 Hz, and a
     10-unit halo OUTWARD, gold to nothing -- the halo is a ring CUT OUT OF THE
     PATH, because a radial gradient with an inner radius still fills its inner
     circle with the first stop (CLAUDE.md §4.1b). Where the foe crosses it,
     the rim flares locally: a 60-unit arc to alpha 1.0 over 0.15s, so the
     crossing is seen (Code's pick, design §4.1). */
  _sunRim(c, x, y, r, k, T, cross, now){
    if (!(r > 1) || !(k > 0.004)) return;
    const g = c.createRadialGradient(x, y, r, x, y, r + 10);
    g.addColorStop(0, "rgba(255,217,138," + (0.35 * k).toFixed(4) + ")");
    g.addColorStop(1, "rgba(255,217,138,0)");
    c.globalAlpha = 1;
    c.fillStyle = g;
    c.beginPath(); c.arc(x, y, r + 10, 0, TAU); c.arc(x, y, r, TAU, 0, true); c.fill();
    c.globalAlpha = (0.8 + 0.1 * Math.sin(TAU * 1.2 * T)) * k;
    c.strokeStyle = SUNLIGHT.gold; c.lineWidth = 3;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke();
    if (cross) for (const X of cross){
      const q = Math.max(0, 1 - (now - X.t0) / 0.15), half = 30 / Math.max(r, 30);
      c.globalAlpha = q * k;
      c.lineWidth = 3 + 3 * q;
      c.beginPath(); c.arc(x, y, r, X.a - half, X.a + half); c.stroke();
    }
    c.globalAlpha = 1;
  }

  /* THE CORE: a small sun at the contact point, core white at 0.9,
     source-over -- the only white in the sun. */
  _sunCore(c, x, y, rc, k){
    if (!(rc > 0.5) || !(k > 0.004)) return;
    c.globalAlpha = 0.9 * k;
    c.fillStyle = SUNLIGHT.core;
    c.beginPath(); c.arc(x, y, rc, 0, TAU); c.fill();
    c.globalAlpha = 1;
  }

  /* THE SUN IS IN THE BLADE (v99 §4.1, 1): the arming's only tell, and
     deliberately nothing on the floor, so that when the sun appears it is
     unmistakably FROM THE HIT. A gold edge-light along the blade's inset edge
     (not the axis: the sanctified fuller is pierced down it), breathing 1.5 Hz
     between 0.45 and 0.8, and a short warm smear behind it -- the blade's own
     sweep over the last ~0.11s, off the tip history the swing ribbons already
     keep (Code's pick, design §4.1). On every armed frame and on no other.
     SOURCE-OVER in the WORLD pass, over both fighters and occluded by the
     foe's shell as the blade is: the break's flash is the only light. */
  drawSunriseBlade(m){
    const a = m.a, b = m.b;
    if (m.over || (!(a.ultSunrise && a.ultSunrise.armed)
                   && !(b.ultSunrise && b.ultSunrise.armed))) return;
    const c = this.ctx, R = CONFIG.physics.ballR, T = m.t;
    for (const f of [a, b]){
      const S = f.ultSunrise;
      if (!S || !S.armed || !f.alive) continue;
      const dim = f.stun > 0 ? 0.42 : 1;
      const L = f.w.reach * m.actMods.reach * f.reachMul + 6, bh = f.w.artW * 0.19;
      const foe = f === a ? b : a;
      c.save();
      if (foe.alive){
        c.beginPath(); c.rect(-4000, -4000, 8000, 8000);
        c.arc(foe.x, foe.y, R * 0.98, 0, TAU, true); c.clip();
      }
      const r0 = R - 6 + L * 0.225;
      for (const tp of f.tips){
        const N = tp.length >> 1;
        if (N < 3) continue;
        c.beginPath();
        for (let i = 0; i < N; i++) c.lineTo(tp[2 * i], tp[2 * i + 1]);
        for (let i = N - 1; i >= 0; i--){
          const an = Math.atan2(tp[2 * i + 1] - f.y, tp[2 * i] - f.x);
          c.lineTo(f.x + Math.cos(an) * r0, f.y + Math.sin(an) * r0);
        }
        c.closePath();
        const g = c.createLinearGradient(tp[0], tp[1], tp[2 * N - 2], tp[2 * N - 1]);
        g.addColorStop(0, "rgba(255,217,138,0)");
        g.addColorStop(1, "rgba(255,217,138," + (0.25 * dim).toFixed(4) + ")");
        c.globalAlpha = 1;
        c.fillStyle = g; c.fill();
      }
      c.globalAlpha = (0.625 + 0.175 * Math.sin(TAU * 1.5 * T)) * dim;
      c.strokeStyle = SUNLIGHT.gold; c.lineWidth = 2.2;
      c.lineCap = "round"; c.lineJoin = "round";
      for (const s of m.bladeSegments(f)){
        c.save();
        c.translate(f.x, f.y); c.rotate(s.a); c.translate(R - 6, 0);
        c.beginPath();
        c.moveTo(L * 0.25, -bh * 0.58); c.lineTo(L * 0.78, -bh * 0.52);
        c.lineTo(L * 0.95, -bh * 0.10);
        c.stroke();
        c.restore();
      }
      c.restore();
    }
  }

  /* THE BREAK (v99 §4.1, 2): "where the sword hit, the sun came up." A flash
     at the hit point, core white, r 0 -> 70 in 0.2s and gone by 0.3s -- the
     ONLY emissive mark in the set-piece. `lighter`, in the emissive pass,
     drawn after both balls and cut out of both. Timed on the match clock,
     which runs through the blow's own hit stop. */
  drawSunriseFlash(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      const F = f.sunriseFlash;
      if (!F) continue;
      const age = m.t + (m.deathAge || 0) - F.t0;
      const r = 70 * Math.min(1, age / 0.2);
      const al = age < 0.2 ? 1 : Math.max(0, 1 - (age - 0.2) / 0.1);
      if (!(r > 1) || !(al > 0)) continue;
      c.save();
      /* NOT OVER A BALL: the flash lights the floor round the contact, and
         both shells stand in front of it (CLAUDE.md §4.1b). The design lets
         it touch a ball for a fifth of a second; measured at its 70 it lifted
         a struck ball's disc by up to +0.31, past the 0.90 ceiling on 94
         ball-frames that were not over it already. One clip per ball, because
         two holes in one nonzero path fill where they overlap. */
      for (const g of [m.a, m.b]) if (g.alive){
        c.beginPath(); c.rect(-4000, -4000, 8000, 8000);
        c.arc(g.x, g.y, R * 0.98, 0, TAU, true); c.clip();
      }
      c.globalCompositeOperation = "lighter";
      const g = c.createRadialGradient(F.x, F.y, 0, F.x, F.y, r);
      g.addColorStop(0, "rgba(255,246,226," + (0.55 * al).toFixed(4) + ")");
      g.addColorStop(1, "rgba(255,246,226,0)");
      c.fillStyle = g;
      c.beginPath(); c.arc(F.x, F.y, r, 0, TAU); c.fill();
      c.restore();
    }
  }

  drawMotes(m){
'''


def s3_edits() -> list:
    return [

("the sun's palette, used nowhere else",
 "function shellHash(a, b){\n",
 SUNLIGHT_JS),

("the fighter carries the sun's picture",
 '''    this.ultSunrise = null;
    this.sunriseTally = null;
''',
 PICTURE_FIELDS),

("every cast restarts the arming's own clock",
 '''      if (f.ultSunrise) f.ultSunrise.armed = true;
      else f.ultSunrise = { armed: true, up: false, x: 0, y: 0, t: 0, cd: 0 };
''',
 '''      if (f.ultSunrise) f.ultSunrise.armed = true;
      else f.ultSunrise = { armed: true, up: false, x: 0, y: 0, t: 0, cd: 0 };
      /* `w` is the arming's own clock, read by the hum's voice and by nothing
         in the simulation: every cast starts it again, as every cast re-arms
         the blade and restarts the lab's wait. Its own line, so stage 1's
         cast stays byte for byte what `chain_audit` watches. */
      f.ultSunrise.w = 0;
'''),

("the break rings the bell, on the blow's own frame",
 '''      self.sunriseTally.breaks++;
      this.beat({ kind: "ult", side: self === this.a ? 0 : 1, x: hx, y: hy,
''',
 '''      self.sunriseTally.breaks++;
      SFX.play("ult", { w: "dawnbringer-break" });   // the bell (v99 §4.2)
      this.beat({ kind: "ult", side: self === this.a ? 0 : 1, x: hx, y: hy,
'''),

("the hum and the sunset ride the sun's own clocks",
 '''      if (!f.alive){ f.ultSunrise = null; continue; }
      if (!S.up) continue;
      S.t += dt;
      const u = f.w.ult;
      if (S.t >= u.dur){
        S.up = false;
''',
 '''      if (!f.alive){ f.ultSunrise = null; continue; }
      /* THE VOICES RIDE THE SUN'S OWN CLOCKS (v99 §4.2). While ARMED, a strike
         of the hum every quarter second of arming, stepping up the minor third
         at 1.5s and 3s and holding (the cast struck the root: fireUlt plays
         every relic's cast). While UP, a strike of the shimmer every half
         second of the sun's life. At a CLOCK sunset, the shimmer's top note
         held and released. A hit stop freezes both clocks and holds the next
         strike; a death never reaches the sunset voice, and step() stops
         calling this once the fight is over. Presentation only: SFX.play is a
         no-op headless, and `w` is read by nothing else. */
      if (S.armed){
        const q0 = Math.floor(S.w / 0.25);
        S.w += dt;
        if (Math.floor(S.w / 0.25) > q0)
          SFX.play("ult", { w: "dawnbringer-arm", n: Math.min(2, Math.floor(S.w / 1.5)) });
      }
      if (!S.up) continue;
      const h0 = Math.floor(S.t / 0.5);
      S.t += dt;
      const u = f.w.ult;
      if (S.t >= u.dur){
        SFX.play("ult", { w: "dawnbringer-set" });
        S.up = false;
'''),

("the shimmer strikes every half second of the sun",
 '''      const T = f.sunriseTally, foe = f === this.a ? this.b : this.a;
      const r = u.r * Math.min(1, S.t / u.grow);
''',
 '''      if (Math.floor(S.t / 0.5) > h0) SFX.play("ult", { w: "dawnbringer-up" });
      const T = f.sunriseTally, foe = f === this.a ? this.b : this.a;
      const r = u.r * Math.min(1, S.t / u.grow);
'''),

("every tick is shown: the number, the shell's flash, the voice",
 '''                    shotSpd0: 0, sunrise: true });
    }
  }
''',
 '''                    shotSpd0: 0, sunrise: true });
      this.sunriseShown(f, foe);                          // the picture's
    }
  }
'''),

("sunriseShown",
 '''  /* =================================================== THE SUNRISE ====''',
 SUNRISE_SHOWN),

("the sun's presentation clocks (tickPresentation)",
 '''                 : Math.max(0, f.echoFade - dt / 0.45);
''',
 PRESENTATION),

("the sun is drawn on the floor (world pass)",
 '''    if (__world) this.drawArena(m);
    c.scale(this.scale, this.scale);
''',
 DRAW_CALL),

("drawSunrise, its five parts, the blade and the flash",
 "  drawMotes(m){\n",
 DRAW_SUNRISE),

("the sun in the blade, over both fighters (world pass)",
 '''    this.drawEchoGhost(m);
''',
 '''    this.drawEchoGhost(m);
    /* DAYBREAK'S ARMED BLADE: on the blade, so over both fighters, and
       source-over in the world pass -- the break's flash is the only light */
    this.drawSunriseBlade(m);
'''),

("the break's flash, over both balls (emissive pass)",
 '''    this.drawEcho(m);
''',
 '''    this.drawEcho(m);
    /* DAYBREAK'S BREAK: the set-piece's one light, over both balls */
    this.drawSunriseFlash(m);
'''),

("the synth: the arming, the bell, the shimmer, the sunset",
 'if (w === "widowmaker"){',
 voices_js(VOICE)),

("the synth: the tick's sizzle-chime, its own kind",
 '''      else if (kind === "scour-tick"){''',
 tick_voice_js(VOICE)),

    ]


S3 = s3_edits()


def relic_ult(code: str) -> str:
    """The ult block of Dawnbringer's weapon entry, comments stripped."""
    i = code.find('id:"dawnbringer"')
    if i < 0:
        raise SystemExit("no Dawnbringer in this source -- wrong build")
    j = code.find("ult:{", i)
    k = code.find("},", j)
    return code[j:k + 2]


LINE_NAMES = ("ultDawn", "dawnTally", "tickDawn", "drawDawn", "dawnShown",
              "dawnFade", "dawnLitFade", "dawnTagged", "dawnHeld",
              "dawnbringer-step", "dawnbringer-close")


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
    print(f"\nDAWNBRINGER / DAYBREAK, THE CIRCLE -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")

    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the batch's tip, which carries Corollary
    # at charge 14, the line through its stage 3, and Zenith -- whose names
    # (`ultSun`, `tickSun`) are why this relic's are not the brief's.
    for need, why in (('name:"Corollary", charge:14', "no Corollary at charge 14"),
                      ('name:"Zenith"', "no Zenith -- build on sc-zenith or a later tip"),
                      ("tickSun(dt){", "no Zenith ticker -- not the batch tip")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    zenith_refs = len(re.findall(r"\bultSun\b", code))

    if A.stage == "1":
        if "ultSunrise" in code:
            raise SystemExit("this source already carries stage 1 -- built")
        if "dawnShown" not in code or strip_comments(LINE_ULT) not in code:
            raise SystemExit("wrong base: the line (v97 stages 1-3) is not in this "
                             "source as built -- nothing to retire")
        print("  base  the batch tip: Corollary c14, the line through stage 3, Zenith")
        for c in CUTS1:
            s = cut(s, c)
        s = cut_tick(s)
        for label, old, new in S1:
            s = one(s, old, new, label)
    else:
        if "ultSunrise" not in code:
            raise SystemExit("stage 3 needs stage 1 under it -- no sun here")
        if "sunriseShown" in code:
            raise SystemExit("this source already carries stage 3 -- built")
        print("  base  stage 1 (the sun) on the batch tip")
        for label, old, new in S3:
            s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(ult_block()).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Dawnbringer's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if ULT["r"] / ULT["grow"] != 100:
        raise SystemExit("REFUSING TO WRITE -- the rim's speed is not the brief's "
                         "100 px/s (r / grow)")
    print(f"  ok    the rim travels {ULT['r'] / ULT['grow']:.0f} px/s (r {ULT['r']} "
          f"over grow {ULT['grow']}s)")
    left = [n for n in LINE_NAMES if n in out_code]
    if left or re.search(r'kind:"dawn"', out_code):
        raise SystemExit(f"REFUSING TO WRITE -- the line survives: {left}")
    if len(re.findall(r'kind:"sunrise"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one sunrise ultimate")
    if len(re.findall(r"\bultSun\b", out_code)) != zenith_refs:
        raise SystemExit("REFUSING TO WRITE -- this build touched Zenith's `ultSun`")
    if re.search(r'kind:"radiant"', out_code):
        raise SystemExit("REFUSING TO WRITE -- a relic carries kind:\"radiant\"; "
                         "the sparks are back")
    print(f"  ok    the line is out ({len(LINE_NAMES)} names, kind:\"dawn\"); one "
          f"sunrise ultimate; Zenith's ultSun untouched ({zenith_refs} refs); no "
          f"relic is radiant")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S1_TICK + S3:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws "
                             "the match RNG")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    no insert draws the RNG; {n_ids} relics in the roster")
    if A.stage == "3":
        # THE BREAK'S FLASH IS THE ONLY LIGHT: nothing else of the sun's is
        # `lighter`, and every mark but the flash is drawn in the world pass.
        draw = strip_comments(DRAW_SUNRISE)
        flash = draw[draw.find("drawSunriseFlash(m){"):]
        rest = draw[:draw.find("drawSunriseFlash(m){")]
        if '"lighter"' in rest or '"lighter"' not in flash:
            raise SystemExit("REFUSING TO WRITE -- `lighter` is somewhere other "
                             "than the break's flash")
        if "if (__world) this.drawSunrise(m);" not in out_code:
            raise SystemExit("REFUSING TO WRITE -- the sun is not in the world pass")
        # THE SIM READS NONE OF THE PICTURE: the picture fields appear only in
        # the constructor, tickPresentation, sunriseShown and the renderer.
        for fld in ("sunriseSeen", "sunriseSets", "sunriseFlash", "sunriseHit",
                    "sunriseIn", "sunriseCross", "sunriseLitFade"):
            if fld in strip_comments(TICK_SUNRISE):
                raise SystemExit(f"REFUSING TO WRITE -- tickSunrise reads {fld}")
        print("  ok    `lighter` only in the break's flash; the sun in the world pass; "
              "tickSunrise reads no picture field")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    print(f"  charge {ULT['charge']}  sun r {ULT['r']} up in {ULT['grow']}s, "
          f"{ULT['dur']}s from the contact  tick {ULT['tick']}s  "
          f"{ULT['tickDmg']} dmg + smite {ULT['smite']}   blade 10.4 (unchanged)")
    print("\n  GATE -- in this order, and each can fail:")
    if A.stage == "1":
        print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids <the 34 others> --n 8")
        print(f"    python sunrise_probe.py --game {A.out}")
        print("    the relic at 10.4 against stage 0's arm D on 151 (the lab)")
    else:
        print(f"    python sunrise_sheet.py --game {A.out}          # legibility FIRST, then the bloom")
        print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids <ALL 35> --n 6")
        print(f"    python sunrise_probe.py --game {A.out}          # + the stage-3 checks")
        print("    render_ab (defaults identical; a control inside a sun 0/N), shell_identity,")
        print("    chain_audit --builder sunrise_build.py, tip_audit, verify --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
