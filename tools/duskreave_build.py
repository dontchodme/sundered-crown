#!/usr/bin/env python
"""DUSKREAVE and SCOUR -- the umbral scythe, the 33rd relic, THE LAST SCYTHE.

Built from `06-docs/v63/DUSKREAVE-BUILD-BRIEF.md` (Cowork, 2026-09-02), which is
the input and the only input. Nothing in this file is a design decision: every
number below is Rick's or is measured, and the ones that are measured name the
tool. CLAUDE.md section 3 rule 0.

    stage 1   the relic, its ultimate STUBBED          sc-bloodletting -> sc-duskreave
    stage 2   the tornado exists and sweeps, no damage
    stage 3   it catches, drags and ticks -- THE RELIC
    stage 4   it eats projectiles
    stage 5   art, sound, beat
    stage 6   the real price

THE CURSE RULE THIS IS BUILT AGAINST IS THE ONE IN THE LINK, and the link has
the shipped rule: `pushCurse` sorts descending and truncates to the three
BIGGEST blows. Rick ruled on 2026-09-02 that the school moves to a LAST-3
window, and that it lands as its own commit after Gloamwire ships -- so it is
not here, it is not this builder's, and brief section 1 says to build against
whatever is actually present. The tick behaves identically under both; only the
price moves (+59.2pp against +40.5pp) and Rick has accepted both. Stage 1
ASSERTS which rule it found and prints it, so the number gate 6 produces can
never be read against the wrong rule.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "duskreave"

# ------------------------------------------------------------- the numbers --

# THE BLADE IS RICK'S AND IT IS NOT A BISECTION START. Brief section 0: `dmg 21`,
# "Rick: Bloodmirror's weight (v62 section 12/17)", and section 3 lists the blade
# among the things already given with "DO NOT RE-ASK". There is no blade stage in
# this brief and there is no `TUNED_DR` in this file, deliberately -- gate 6
# prices the built relic and writes the gap down, it does not tune the blade to
# hit a model's number.
BLADE = 21.0

ULT_NAME = "Scour"
ULT_KIND = "scour"          # its own kind. Nothing shares it -- one sigil, one
                            # sound, one picture (brief section 0, RULE 9).
ULT_CHARGE = 15.0

# RICK'S OWN LINE, 2026-09-02, and it is ELEVEN CHARACTERS OVER WHAT `verify`
# ALLOWS. See `TIP_OVER_BUDGET` below -- this is not stage 1's problem, because
# stage 1 stubs the tip, but it is a decision that has to be Rick's and it is
# raised the moment it is known rather than at gate 5.
ULT_TIP = ("Conjures a tornado that absorbs projectiles. "
           "Enemies caught in it take rapid damage")
ULT_TIP1 = "-"              # stage 1, stubbed. `verify` asks only that it is
                            # non-empty; the real line lands with the mechanic
                            # it describes.

TIP_OVER_BUDGET = """
  RICK'S CARD LINE IS 83 CHARACTERS AND `verify` CAPS AN ULT TIP AT 72.

  It is his own wording, given 2026-09-02, so it is not this session's to cut
  (CLAUDE.md section 3 rule 2 -- the scrunch card wording is one of the seven).
  And the brief says it was MEASURED to fit: two lines in the ult-bar reminder
  at 390px, two on the scrunch panel at 21px, nothing dropped.

  Both of those can be true at once, because the 72 is a CHARACTER count and
  v53 settled that characters are the wrong unit for this box -- and because
  `tip_audit`, the gate CLAUDE.md calls the one that actually protects the
  layout, does not look at ult tips at all (open item 4, five versions old).

  So the choice is Rick's and it is one of two:
    a. the cap moves, on a PIXEL measurement taken on this machine -- which is
       what raised it from 44 to 72 in the first place; or
    b. the line comes down to 72 characters, in his words.

  Stage 1 does not need it settled. Stage 3 does.
"""

BLURB = ("A hole in the floor of the world, turning. Whatever it catches, it "
         "keeps hold of long enough to finish.")


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse.

    The comment-balance check is `bloodmirror_build`'s and it is here for the
    same reason: an unbalanced `*/` in an inserted block surfaces only as a
    twenty-second Playwright timeout with no error attached (CLAUDE.md 4.11).
    """
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
    """Code with the prose taken out.

    Every refusal in this file greps shipped source, and this build explains
    itself IN that source -- so a check that cannot tell code from the comment
    explaining it fires on its own explanation. It has happened twice in this
    repo (`curse_check`, `curse_build`) and both times on the same day.
    """
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def entry(s: str, rid: str) -> str:
    """One relic's own WEAPONS entry, by brace matching from its id."""
    i = s.index(f'id:"{rid}"')
    j = s.rindex("{", 0, i)
    depth, k = 0, j
    while k < len(s):
        if s[k] == "{":
            depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0:
                return s[j:k + 1]
        k += 1
    raise SystemExit(f"unbalanced braces in the entry for {rid}")


def body_block(s: str, rid: str, key: str) -> str:
    """One named sub-object of a relic's entry, comments out, space collapsed."""
    e = strip_comments(entry(s, rid))
    m = re.search(key + r"\s*:\s*\{", e)
    if not m:
        return ""
    j = e.index("{", m.start())
    depth, k = 0, j
    while k < len(e):
        if e[k] == "{":
            depth += 1
        elif e[k] == "}":
            depth -= 1
            if depth == 0:
                return re.sub(r"\s+", " ", e[j:k + 1]).strip()
        k += 1
    return ""


def phys(s: str, rid: str) -> dict:
    """The physical stats a TYPE owns, off one relic's entry."""
    e = strip_comments(entry(s, rid))
    out = {}
    for f in ("reach", "width", "artW", "spin", "mass", "mode", "arc"):
        m = re.search(rf"\b{f}\s*:\s*(\"[a-z]+\"|[\d.]+)", e)
        if m:
            out[f] = m.group(1)
    return out


def ult_matches(s: str, A, stage: str) -> None:
    """The shipped `ult` block carries every number this run printed.

    v56's failure, verbatim: a stage-2 insert wrote the whole `ult` block and
    stage 3 rewrote only the line carrying `charge`, so the run LOGGED the new
    rhythm and SHIPPED the old one, and every gate downstream measured a relic
    the log was not describing.
    """
    blk = body_block(s, RELIC, "ult")
    if not blk:
        raise SystemExit("the shipped relic has no `ult` block")
    want = {"name": f'"{A.ult}"', "kind": f'"{ULT_KIND}"'}
    if stage == "1":
        want["charge"] = "1e9"
    else:
        want["charge"] = f"{A.charge:g}"
        for k in ("dur", "w", "top", "sweep", "tick"):
            want[k] = f"{getattr(A, k):g}"
        want["dmg"] = f"{A.tickdmg:g}"
        if stage == "3":
            want["drag"] = f"{A.drag:g}"
    missing = [f"{k}:{v}" for k, v in want.items()
               if not re.search(rf"\b{re.escape(k)}\s*:\s*{re.escape(v)}\s*[,}}]",
                                blk)]
    if missing:
        raise SystemExit(
            "REFUSING TO WRITE -- the shipped `ult` block does not carry what "
            "this run printed:\n  missing " + ", ".join(missing)
            + "\n  (v56 shipped an ultimate whose numbers the log did not "
              "describe. Never again.)")


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will.

    CLAUDE.md 4.11, closed at last. Every failure mode this builder can produce
    -- a stray comma between class methods, an unbalanced comment, a missing
    brace -- lands as a TWENTY-SECOND PLAYWRIGHT TIMEOUT with no error text,
    which is indistinguishable from a slow machine and costs an afternoon. Node
    is already a dependency of this repo (the app pins electron), and one
    `node --check` turns that into a line number.

    A machine without node gets a warning, not a refusal: this is a net that
    catches a known class of bug, not a gate anybody should be blocked by.
    """
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        print("  WARN  no `node` on PATH -- output NOT syntax checked. "
              "A bad write will surface as a 20s Playwright timeout "
              "(CLAUDE.md 4.11).")
        return
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>",
                        html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output -- the page "
                         "shape has changed and this check is measuring "
                         "nothing")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                msg = (r.stderr or "").strip().splitlines()
                raise SystemExit(
                    f"REFUSING TO WRITE -- {label} does not parse.\n  "
                    + "\n  ".join(msg[:12])
                    + "\n\n  (CLAUDE.md 4.11. Without this the symptom is a "
                      "20-second\n  Playwright timeout naming no file and no "
                      "line.)")
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


def curse_rule(s: str) -> str:
    """Which curse rule is in this link -- the three BIGGEST, or the last three.

    Brief section 1: build against whichever is present, and NEVER build a tick
    that behaves differently under the two. This does not choose; it reports,
    so that gate 6's price can never be read against the wrong rule.
    """
    code = strip_comments(s)
    m = re.search(r"pushCurse\s*\(v,\s*n\)\s*\{[\s\S]{0,400}?\n\s{2}\}", code)
    if not m:
        raise SystemExit("no `pushCurse` in this source -- it predates v53")
    body = m.group(0)
    sorts = "sort(" in body
    trims = "length =" in body or "shift(" in body or "splice(" in body
    if sorts and trims:
        return "BIGGEST-3"
    if trims and not sorts:
        return "LAST-3"
    return "UNRECOGNISED"


# ------------------------------------------------------------------ stage 1 --

S1 = [

("relic", '''    blurb:"A copy of the blade, cut loose and left standing. It does not chase anything - it makes the room smaller." },

];''',
 '''    blurb:"A copy of the blade, cut loose and left standing. It does not chase anything - it makes the room smaller." },

  /* DUSKREAVE -- THE UMBRAL SCYTHE, the thirty-third relic, and THE LAST
     SCYTHE. Seven schools, seven scythes; this closes the row.

     EVERY PHYSICAL STAT IS THE SCYTHE'S, copied off Lastlight, Thornwake,
     Foregone, Vesper, Cindercleave and Bloodmirror -- the type owns
     `reach:104, width:11, artW:46, spin:3.2, mass:2.4, blades:[0], mode:"spin"`
     and there is no seventh set to invent. This builder asserts that against
     the shipped file before it writes rather than trusting this comment.

     `dmg` 21 IS RICK'S AND IT IS NOT A BISECTION START. It is Bloodmirror's
     weight (v62 section 12/17), and the brief lists it among the things already
     settled. There is no blade stage in this build; gate 6 prices what was
     built and writes down where it lands.

     `onHit:{ curse:1 }` is the school's channel, carried exactly as the other
     four umbral relics carry it -- and it is load-bearing here in a way it is
     not anywhere else, because THE ULTIMATE'S TICKS ARE HITS. A tick goes
     through `resolveHit`, so it collects `curseEcho()` off the target the way
     every other blow does. Measured before anything was built
     (`duskreave-check-v63.md` section 0): the echo is HALF the tornado's
     damage, 113 of 226 a fight. That is the relic.

     THE ART IS ALREADY ON THE ROW AND HAS NEVER BEEN SEEN. `SHAPES.scythe`
     routes `umbral` to `_scEaten` and has since before this cell had anything
     in it, so this is the first relic that will ever draw it. The brief says to
     film it and show Rick a strip BEFORE stage 2, and the reason is v58: he
     rejected `_whEaten` on sight after it had been built and tuned. The two are
     not the same object -- `_whEaten` subtracted from a shape that was already
     rectilinear and produced smaller rectangles, where the crescent is a curve
     and `_scEaten`'s bites are RIMMED so they read as absences rather than as
     holes in the light -- but "it is a different shape" is an argument, and
     CLAUDE.md 4.0 says the argument is not the test. */
  { id:"duskreave", name:"Duskreave", aff:"umbral", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:%DMG%, spin:3.2, mode:"spin", mass:2.4,
    onHit:{ curse:1 },
    /* SCOUR. STUBBED AT `charge:1e9` IN STAGE 1 -- the same "OFF" the charge
       sweep in v55b used, and the same one Cindercleave's stage 1,
       Shroudmaul's stage 2, Gloamwire's stage 1 and Bloodmirror's stage 1
       used: the clock can never reach it, `fireUlt` never runs, and the relic
       is measured as a blade and a channel and nothing else.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       `kind:"scour"` IS ITS OWN AND SHARES WITH NOTHING. The scythe row
       already carries `harrow` (Lastlight), `converse` (Foregone), `sentinel`
       (Vesper), `breach` (Cindercleave) and `effigy` (Bloodmirror); a sixth
       set-piece on one weapon type has to be separable by its sigil, its voice
       and its picture, and sharing a kind is how two relics quietly become
       one. */
    ult:{ name:"%ULT%", charge:1e9, kind:"scour", tip:"%TIP1%" },
    blurb:"%BLURB%" },

];'''),

]


# ------------------------------------------------------------------ stage 2 --

# EVERY NUMBER HERE IS THE BRIEF'S SECTION 0 TABLE AND ALL OF THEM ARE RICK'S.
# `dur` 10.0 (a duration, not a count), `w` 160 (31% of the 520 hall), `top`
# y=600, `sweep` 200 px/s (MEASURED FREE -- v62 section 8b read contact at
# 17.3/17.3/17.4% across 120/200/300, so the sweep speed is a LOOKS decision),
# `charge` 15.
#
# `tick` AND `dmg` ARE WRITTEN NOW AND ARE INERT UNTIL STAGE 3. Bloodmirror's
# `strandW`/`strandKnock` precedent, and the reason is v56: a stage-2 insert
# wrote a whole `ult` block, stage 3 rewrote one line of it, and the run LOGGED
# numbers the shipped relic did not carry. `ult_matches` refuses to write unless
# every number this run printed is in the block, so they go in together.
ULT = { "dur": 10.0, "w": 160.0, "top": 600.0, "sweep": 200.0,
        "tick": 7.0, "tickdmg": 5.0,
        # CODE'S KNOB, and the labs never modelled it (brief open decision 1,
        # v62 HANDOFF section 6). An acceleration toward the band's floor
        # centre, in units of "per second, per unit of offset" -- at the band's
        # edge (80 units out) 6.0 buys about 480 px/s^2 inward, so a ball
        # entering from the side is still inside a second later, which is the
        # brief's own test. Filmed before it is tuned.
        "drag": 6.0 }

S2 = [

# ---- 1. THE REAL ULT BLOCK --------------------------------------------------
("ult-block",
 '''    ult:{ name:"%ULT%", charge:1e9, kind:"scour", tip:"%TIP1%" },''',
 '''    /* SCOUR. `charge` 15, and the ultimate is now live.

       THE TIP IS STILL THE STUB AND THAT IS A DECISION WAITING ON RICK, NOT AN
       OVERSIGHT. His own card line -- "Conjures a tornado that absorbs
       projectiles. Enemies caught in it take rapid damage" -- is 83 characters
       and `verify` caps an ult tip at 72. The brief records it as MEASURED to
       fit both surfaces in PIXELS (390px, two lines, nothing dropped), and v53
       settled that characters are the wrong unit for that box -- but the pixel
       gate for ult tips does not exist (`tip_audit` does not read them, open
       item 4). So either the cap moves on a measurement or the line comes down,
       and both are his. Stage 3 is where it has to be settled.

       `tick` AND `dmg` ARE INERT UNTIL STAGE 3 and are written here rather than
       added later: v56 shipped an ultimate whose numbers its own log did not
       describe, because a stage-2 insert wrote the block and stage 3 rewrote
       one line of it. */
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"scour", tip:"%TIP1%",
          dur:%DUR%, w:%W%, top:%TOP%, sweep:%SWEEP%,
          tick:%TICK%, dmg:%TICKDMG% },'''),

# ---- 2. THE MATCH CARRIES ONE TORNADO ---------------------------------------
("match-field", '''    this.vents = [];
    this.ventSeq = 0;         // deterministic per-vent bearing''',
 '''    this.vents = [];
    this.ventSeq = 0;         // deterministic per-vent bearing
    /* THE TORNADO. One per match and not one per fighter, because two
       Duskreaves cannot meet -- `verify` pairs distinct relics -- and a single
       slot is the honest shape for a thing the hall contains. It carries its
       caster in `src` so the catch can never take the wrong fighter.

       NOT ON `m.ultFx`, AND THAT IS DEADFALL'S LESSON RATHER THAN A TASTE.
       `ultFx` is ONE SLOT: the opponent casting anything overwrites it, and
       that cast's own shorter `life` then nulls it -- measured at 0.0%
       survival against Ironhail for a window ultimate (v54 section 2a,
       chain-wide open item 25). A ten-second window whose picture can be
       erased by somebody else's nova is a window nobody can see. So the
       tornado is a SIM OBJECT and it is drawn off itself. */
    this.tornado = null;'''),

# ---- 3. THE CAST ------------------------------------------------------------
("cast", '''    if (u.kind === "breach"){''',
 '''    if (u.kind === "scour"){
      /* NOTHING RESOLVES HERE. The cast stands a band in the hall and that is
         all; the catch, the drag and the ticks are `tickScour`'s, and until
         stage 3 there are none of them. No radius test, no nova, no damage on
         this frame.

         WHERE IT STARTS AND WHICH WAY IT GOES ARE CODE'S CALL (brief open
         decision 2), and this is the one the brief points at: "starting under
         the caster and heading toward the foe will read better." The labs
         started it at the left wall and bounced it wall to wall, which is a
         lab's convenience -- it makes every run comparable -- and on screen it
         would mean a set-piece that begins somewhere nobody is looking. The
         sweep SPEED is measured free (v62 section 8b), so the start almost
         certainly is too; it is chosen for the picture and filmed at gate 2.

         `dir` IS SNAPSHOTTED AT THE CAST and never recomputed. Reading it live
         off the foe's position would make the band turn round every time the
         quarry crossed it -- a hazard that chases is a different mechanic, and
         it is not this one. Bloodmirror's copies take their bearing the same
         way and for the same reason.

         CLAMPED INTO THE HALL AT BIRTH. `m.inset` walks 0 -> 140 as the walls
         close, and a band centred where the caster happens to be standing can
         start with its edge already outside the room. */
      const A = CONFIG.arena, n = this.inset, half = u.w * 0.5;
      const cx = Math.max(n + half, Math.min(A.w - n - half, f.x));
      this.tornado = { src: f === this.a ? "a" : "b",
                       cx: cx, dir: (foe.x >= f.x ? 1 : -1),
                       t: 0, dur: u.dur, w: u.w, top: u.top,
                       sweep: u.sweep, caught: false, ticks: 0 };
      /* THE SET-PIECE'S CLOCK IS THE WINDOW'S, the way Aegis, the Thicket, the
         ballista, the Stasis Field, the Winnowing and the Sentinel all set it
         at their own cast sites rather than from the `life` map. */
      if (this.ultFx) this.ultFx.life = u.dur;
      return;
    }
    if (u.kind === "breach"){'''),

# ---- 4. AND IT IS TICKED ----------------------------------------------------
("tick-call", '''    this.tickBreach(dt);
    this.tickBallista(dt);''',
 '''    this.tickBreach(dt);
    /* WITH THE OTHER WINDOW TICKERS, and after the fighter loop that moved both
       balls -- the band's position and the quarry's have to be current on the
       same frame or the catch is testing where somebody used to be. Before
       `tickHits` for the same reason `tickWinnow` and `tickBreach` give one
       line up. */
    this.tickScour(dt);
    this.tickBallista(dt);'''),

# ---- 5. THE TICKER ITSELF ---------------------------------------------------
("ticker", '''  tickBreach(dt){''',
 '''  /* THE BAND SWEEPS, AND IN STAGE 2 THAT IS ALL IT DOES. No catch, no drag, no
     damage, no projectiles -- each of those is its own stage with its own gate,
     because the whole point of staging this relic is that a tornado that sweeps
     and a tornado that grinds are separately wrong in different ways.

     ZERO BURDEN WHEN NOBODY HAS CAST. Returns on its first line, so a roster
     with no Duskreave in it pays one null test a frame -- which is what makes
     `engine_ab` over the other 32 relics a meaningful check rather than a
     hopeful one. */
  tickScour(dt){
    const T = this.tornado;
    if (!T) return;
    T.t += dt;
    if (T.t >= T.dur){ this.tornado = null; return; }
    const A = CONFIG.arena, n = this.inset, half = T.w * 0.5;
    /* THE EDGE REACHES THE WALL, NOT THE CENTRE (brief stage 2). A band that
       bounced on its centre would put half its width through the stone, and
       the drawn hazard would stop agreeing with the tested one -- which is the
       fault `drawVents` names: `half` IS the hit box. */
    const lo = n + half, hi = A.w - n - half;
    /* AND THE HALL CLOSES ON IT. Once `inset` has walked far enough that the
       band is wider than what is left of the room, `lo > hi` and the clamp
       below would return `lo` -- `clamp(v,a,b)` with `a > b` returns `a`, which
       is how `_tagFirst` runs off the right edge (open item 47). Pinned to the
       middle instead, which is the only place a too-wide band can be. */
    if (lo >= hi){ T.cx = A.w * 0.5; return; }
    T.cx += T.dir * T.sweep * dt;
    if (T.cx < lo){ T.cx = lo + (lo - T.cx); T.dir = 1; }
    if (T.cx > hi){ T.cx = hi - (T.cx - hi); T.dir = -1; }
    T.cx = Math.max(lo, Math.min(hi, T.cx));
  }

  tickBreach(dt){'''),

# ---- 6. AND IT DOES NOT OUTLIVE THE MATCH -----------------------------------
("over", '''      this.vents.length = 0;
      this.a.ultBreach = null; this.b.ultBreach = null;
    }''',
 '''      this.vents.length = 0;
      this.a.ultBreach = null; this.b.ultBreach = null;
    }
    /* THE TORNADO DOES NOT OUTLIVE THE MATCH. The holes above deliberately do
       -- a hall still venting after the kill is section 4.5's strong final
       image -- and this is the opposite case: a band that goes on grinding
       across a corpse is not a final image, it is a thing nobody turned off. */
    if (this.over && this.tornado) this.tornado = null;'''),

# ---- 7. THE SIGIL -----------------------------------------------------------
# RULE 9, one sigil per kind. A funnel: three arcs narrowing downward, turning,
# with a ring above them -- the reference's halo -- and a bar at the foot where
# it touches down. Read at ~20px in the HUD, so it is three strokes and not a
# picture of a tornado.
("sigil", '''const ULTSIG = {''',
 '''const ULTSIG = {
  /* SCOUR -- a funnel, turning, under a halo. Three arcs narrowing toward the
     floor and a bar where it touches down: at HUD size a tornado has to be
     read from its TAPER, because a spiral at 20px is a smudge. */
  duskreave(c, t, cf, P){
    for (let i = 0; i < 3; i++){
      const u = i / 2;
      const y = -0.62 + u * 1.18;
      const r = 0.72 - u * 0.50;
      const ph = t * 2.2 + i * 0.7;
      SG.arc(c, Math.sin(ph) * 0.06, y, r, 0.15, Math.PI - 0.15,
             i === 2 ? P.glow : P.core, 0.085, 0.45 + cf * 0.5);
    }
    SG.ring(c, 0, -0.74, 0.84, P.glow, 0.055, 0.30 + cf * 0.55);
    SG.path(c, [[-0.34, 0.60], [0.34, 0.60]], P.glow, 0.08, 0.5 + cf * 0.5);
  },'''),

# ---- 8. AND THE BAND IS DRAWN, OFF ITSELF -----------------------------------
# NOT off `m.ultFx`. See the `this.tornado` declaration: that field is one slot
# and the opponent's next cast erases it, which is open item 25 and measured at
# 0.0% survival against Ironhail. A ten-second window has to be drawn from the
# object that IS the window.
#
# AND THIS IS PLACEHOLDER ART, DELIBERATELY. Stage 5 builds the funnel against
# Rick's own reference (`ref-vortex.mp4`); what gate 2 has to answer is whether
# the GEOMETRY reads -- a third of the width, a quarter of the height, sweeping
# -- and geometry is best judged without a picture arguing over it.
("draw", '''  drawVents(m, over){''',
 '''  /* THE BAND. Under the fighters when `over` is false -- it is a hazard they
     are inside, so they are in FRONT of its body -- and a light pass over them
     after, so the thing holding a ball reads as holding it.

     `half` IS THE HIT BOX, and stage 3 makes that literal: `tickScour`'s catch
     test and this drawing read the same `w`. `drawVents` learned that the hard
     way -- a beam drawn wider than it tests is a jet that looks like it
     connected and did not. */
  drawScour(m, over){
    const T = m.tornado;
    if (!T) return;
    const A = CONFIG.arena, n = m.inset, R = CONFIG.physics.ballR;
    const half = T.w * 0.5;
    const x0 = T.cx - half, x1 = T.cx + half;
    const y0 = T.top, y1 = A.h - n;
    if (y1 <= y0) return;
    const P = AFFINITIES.umbral;
    /* THE WINDOW FADES AT BOTH ENDS rather than popping. A hazard that appears
       and vanishes on a frame is one the viewer cannot anticipate, and this one
       is on screen for ten seconds. */
    const fade = Math.min(1, T.t / 0.35) * Math.min(1, (T.dur - T.t) / 0.5);
    /* `this.ctx`, NOT `this.c`. The first cut had the latter, every headless
       check stayed green -- the probe, the syntax check and engine_ab do not
       draw -- and it threw on the first rendered frame. That is v48's fault
       exactly: `_drawBeam` reached for a Match method from the Renderer and
       `drawUltUnder` handed a NaN to createRadialGradient, both green across
       27 probe checks and a 280-match A/B. */
    const c = this.ctx;
    c.save();
    if (!over){
      c.globalCompositeOperation = "lighter";
      const g = c.createLinearGradient(0, y0, 0, y1);
      g.addColorStop(0, P.core + "00");
      g.addColorStop(0.45, P.core + "3A");
      g.addColorStop(1, P.core + "62");
      c.globalAlpha = fade;
      c.fillStyle = g;
      c.fillRect(x0, y0, T.w, y1 - y0);
      /* THE POOL WHERE IT TOUCHES DOWN. The one place the band meets something
         the viewer already understands -- the floor -- so it is the edge worth
         drawing hardest. */
      c.fillStyle = P.glow + "55";
      c.beginPath();
      c.ellipse(T.cx, y1, half, 14, 0, 0, Math.PI * 2);
      c.fill();
      c.restore();
      return;
    }
    /* THE TWO EDGES, over everything, because they are the boundary the whole
       mechanic is defined by: inside is caught and outside is not. */
    c.globalAlpha = fade * 0.85;
    c.strokeStyle = P.glow;
    c.lineWidth = 2;
    c.beginPath();
    c.moveTo(x0, y0); c.lineTo(x0, y1);
    c.moveTo(x1, y0); c.lineTo(x1, y1);
    c.stroke();
    /* AND THE TOP LIP, so `top` is a line a person can see rather than a
       number in a table. Gate 2 is asking whether this height reads. */
    c.globalAlpha = fade * 0.5;
    c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y0); c.stroke();
    c.restore();
  }

  drawVents(m, over){'''),

("draw-under", '''    if (__emit) this.drawVents(m, false);
    if (__world){''',
 '''    if (__emit) this.drawVents(m, false);
    /* the band is a hazard the balls are inside, so they are in front of it */
    if (__emit) this.drawScour(m, false);
    if (__world){'''),

("draw-over", '''    /* and a jet crosses the room, so it goes over what it crosses */
    this.drawVents(m, true);''',
 '''    /* and a jet crosses the room, so it goes over what it crosses */
    this.drawVents(m, true);
    /* and the band's own edges go over the balls, because inside them is
       caught and outside is not -- that boundary is the mechanic */
    this.drawScour(m, true);'''),

]


# ------------------------------------------------------------------ stage 3 --

# THE TICK IS A HIT. It goes through `resolveHit`, so it collects the foe's
# curse echo the way every other blow does -- and that is the relic. v62 11b:
# on the `hurt` path this is a +17.8 ultimate; on the `resolveHit` path it is
# +29.7 at 4.5 ticks and +59 at 7. Sentinel's `beamHit` uses `hurt` and is the
# precedent you will be tempted by. DO NOT FOLLOW IT.
#
# `drag` IS CODE'S KNOB (brief open decision 1) and the labs never modelled it.
# Guidance from the brief: strong enough that a ball entering from the side is
# still in the band a second later; NOT a pin. It is an acceleration toward the
# band's floor centre, proportional to how far out the quarry is, so a ball at
# the edge is pulled hardest and one already in the throat is barely touched.
S3 = [

# ---- 1. THE ULT BLOCK GAINS THE DRAG ----------------------------------------
("ult3", '''          tick:%TICK%, dmg:%TICKDMG% },''',
 '''          tick:%TICK%, dmg:%TICKDMG%, drag:%DRAG% },'''),

# ---- 2. `over` LEARNS TO SWITCH THE FOUR THINGS OFF --------------------------
# EXTENDED, NOT FORKED. The brief is explicit: "do not fork `resolveHit`." A
# second copy of a 500-line function is how two damage paths drift apart, and
# this one is read by thirty tools.
("over-stop", '''    let stop = Math.min(I.stopMax, I.stopBase + dmg * I.stopPerDmg);
    if (crit) stop *= I.critStopMul;
    if (fatal){ stop = I.killStop; this.finisher = 1.0; }
    this.hitStop = Math.max(this.hitStop, stop);''',
 '''    let stop = Math.min(I.stopMax, I.stopBase + dmg * I.stopPerDmg);
    if (crit) stop *= I.critStopMul;
    if (fatal){ stop = I.killStop; this.finisher = 1.0; }
    /* `over.stop` LETS ONE CALL SITE SAY IT CARRIES NO WEIGHT, and Scour is
       why it exists: `stopBase 0.045 + 0.0022 x dmg` is about 0.067s a tick,
       and SEVEN of those a second would freeze the world for ~45% of every
       second the tornado holds someone. A grind is the one thing in this game
       that must not stutter.

       `=== undefined` and not `|| default` -- CLAUDE.md 4.3, because 0 is a
       value a call site means. A fatal blow keeps its `killStop` regardless:
       the kill is the shot, and no ultimate gets to take that away. */
    if (over && over.stop !== undefined && !fatal) stop = over.stop;
    this.hitStop = Math.max(this.hitStop, stop);'''),

("over-beat", '''    if (!this._cineVine || fatal)
    this.beat({ kind: "hit", side: _side, x: hx, y: hy,''',
 '''    /* `over.beat` -- AND THE FATAL CASE IS NOT NEGOTIABLE. Seven ticks a
       second is ~23 `hit` beats a fight from one ultimate, and `cinePlan`
       would cut to every one of them; that is why a tick files nothing.
       But a tick that KILLS has to file, or the director scores the end of
       the fight as empty air -- which is exactly what happened to Gravemourn,
       where 30 of 58 kills were landed by a hand and ALL THIRTY produced a
       clip with no killing blow. `_cineVine` one line up is the same rule
       arriving from the Thicket. */
    if ((!this._cineVine || fatal) && (fatal || !(over && over.beat === false)))
    this.beat({ kind: "hit", side: _side, x: hx, y: hy,'''),

("over-stun", '''    if (!fatal) foe.takeHitstun(dmg);
    /* THE BLOW FEEDS THE FIELD.''',
 '''    /* `over.stun`. Seven stagger-locks a second is a weapon lock, not a
       grind -- `stunDR` would grind most of it down (v56's trap) but the first
       second is a lock either way, and the DRAG is the control this design
       uses to hold a quarry, not the stun. */
    if (!fatal && !(over && over.stun === false)) foe.takeHitstun(dmg);
    /* THE BLOW FEEDS THE FIELD.'''),

("over-knock", '''    const kx = foe.x - self.x, ky = foe.y - self.y, kl = Math.hypot(kx, ky) || 1;
    const power = CONFIG.combat.knock * (self.w.knockMul || 1) * (crit ? 1.5 : 1);
    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;''',
 '''    const kx = foe.x - self.x, ky = foe.y - self.y, kl = Math.hypot(kx, ky) || 1;
    /* `over.knock` SCALES THE IMPULSE, and Scour passes 0. The ordinary knock
       fires AWAY FROM THE CASTER'S BALL at 165 x knockMul, and seven of those
       a second would throw the quarry straight out of the thing that is
       supposed to be holding it -- the ultimate would be its own counter.
       `=== undefined` again: 0 is the value this call site means. */
    const kMul = (over && over.knock !== undefined) ? over.knock : 1;
    const power = CONFIG.combat.knock * (self.w.knockMul || 1)
                * (crit ? 1.5 : 1) * kMul;
    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;'''),

# ---- 3. THE CATCH, THE DRAG AND THE TICK ------------------------------------
("catch", '''    T.cx = Math.max(lo, Math.min(hi, T.cx));
  }''',
 '''    T.cx = Math.max(lo, Math.min(hi, T.cx));

    /* ------------------------------------------------------------- THE CATCH
       THE EDGE RULE, and it is the one every v62 number was measured with:
       the quarry's SHELL touching the band is caught, not its centre. v62 8a
       is the control that failed when the two rules were mixed -- do not mix
       them. */
    const src = T.src === "a" ? this.a : this.b;
    const foe = T.src === "a" ? this.b : this.a;
    const R = CONFIG.physics.ballR;
    const caught = foe.alive && !this.over
                && (foe.y + R >= T.top)
                && Math.abs(foe.x - T.cx) <= T.w * 0.5 + R;
    T.caught = caught;
    if (!caught){ T.cd = 0; return; }

    /* -------------------------------------------------------------- THE DRAG
       Rick's section 1: "dragged down into it." An ACCELERATION toward the
       band's floor centre, proportional to how far out the quarry is -- so a
       ball at the edge is pulled hardest and one already in the throat is
       barely touched, which is what makes it read as a vortex rather than as a
       magnet.

       NOT A PIN. `foe.pin` stays 0 and that is load-bearing three ways over:
       `tickStasis` carries `f.stun = Math.max(f.stun, f.pin)` for BOTH
       fighters on every frame outside any guard, so writing `pin` would hand
       this relic a weapon lock from a file nowhere near it (v60's finding);
       `_drawField` would draw PARADOX'S HEXAGON on the caught ball (open item
       41, live on Shroudmaul today); and `ballCollision` treats a held ball as
       an immovable object (open item 42). A pull is a pull.

       AND IT IS NOT A KNOCK EITHER. `resolveHit`'s knock fires away from the
       caster; this is a hazard that is not the caster, so it needs its own
       bearing -- the Thicket's rule, and Breach's shove learned it too. */
    const u = src.w.ult;
    const floorY = CONFIG.arena.h - n - R;
    const dx = T.cx - foe.x, dy = floorY - foe.y;
    foe.vx += dx * u.drag * dt;
    foe.vy += dy * u.drag * dt * 0.5;

    /* -------------------------------------------------------------- THE TICK
       ONE call into `resolveHit`, every 1/rate seconds, and it is a REAL HIT:
       it collects `foe.curseEcho()`, it rolls crit and jitter, it reads
       `dmgTakenMul` for Sunder, a ward absorbs it, and it pushes its own
       `dmgBase` into the pool and applies a curse. THE ECHO IS THE RELIC --
       measured at HALF the tornado's damage before anything was built.

       `mul` IS DEFINED, which makes this a projectile-class hit rather than a
       melee connect. That is what keeps Ironbloom's latch, the Crucible's
       strike, Garrote's connect, Deadfall's stamp and Revenant's sling from
       firing off a tornado tick: every one of them tests `mul === undefined`.
       `u.dmg / w.dmg` because `resolveHit` scales the WEAPON's blade by `mul`,
       so this is how a tick states its own base damage of `u.dmg`.

       `u.tick` IS A RATE IN TICKS A SECOND and `u.dmg` is the damage of one.
       The brief's own snippet writes `u.tick / f.w.dmg`, which reads as if
       `tick` were the damage; it is not, here. The probe asserts BOTH -- the
       observed rate and the observed base -- so the naming cannot drift into
       a wrong number silently. */
    T.cd -= dt;
    if (T.cd > 0) return;
    T.cd += 1 / u.tick;
    T.ticks++;
    const before = foe.hp;
    this.resolveHit(src, foe, foe.x, foe.y, null, u.dmg / src.w.dmg,
                    { onHit: { curse: 1 }, knock: 0, stop: 0,
                      stun: false, beat: false });
    T.dealt += Math.max(0, before - foe.hp);

    /* THE DIRECTOR (CLAUDE.md section 3 rule 3). One `hit`-class beat the
       FIRST time a cast catches somebody, carrying what the cast has dealt so
       far -- a hit-heavy ultimate that files nothing is scored as empty air,
       and this one files nothing on 22 of its 23 ticks by design. The fatal
       tick files its own beat inside `resolveHit`, because `over.beat` does
       not silence a kill. */
    if (!T.filed){
      T.filed = 1;
      this.beat({ kind: "hit", side: src === this.a ? 0 : 1,
                  x: foe.x, y: foe.y, dmg: T.dealt, crit: false,
                  fatal: !foe.alive, hpAfter: Math.max(0, foe.hp),
                  hpFrac: Math.max(0, foe.hp) / foe.maxHp,
                  maxHp: foe.maxHp, selfHpFrac: src.hp / src.maxHp,
                  spd: src.speed, foeSpd: foe.speed,
                  close: Math.hypot(src.vx - foe.vx, src.vy - foe.vy),
                  ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                  shotSpd0: 0 });
    }
  }'''),

# ---- 4. THE CAST CARRIES THE NEW STATE --------------------------------------
("cast3", '''                       sweep: u.sweep, caught: false, ticks: 0 };''',
 '''                       sweep: u.sweep, caught: false, ticks: 0,
                       cd: 0, dealt: 0, filed: 0 };'''),

]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=("1", "2", "3", "4", "5"))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=BLADE)
    ap.add_argument("--charge", type=float, default=ULT_CHARGE)
    for k, v in ULT.items():
        ap.add_argument(f"--{k}", type=float, default=v)
    A = ap.parse_args()

    if A.stage not in ("1", "2", "3"):
        raise SystemExit(
            f"stage {A.stage} is not built yet. Stage 4 is the projectiles and\n"
            "  it comes after gate 3 (brief section 2).")

    src = A.src or {"1": "../02-chain/sc-bloodletting.html",
                    "2": "../02-chain/sc-duskreave.html",
                    "3": "../02-chain/sc-scour.html"}[A.stage]
    out = A.out or {"1": "../02-chain/sc-duskreave.html",
                    "2": "../02-chain/sc-scour.html",
                    "3": "../02-chain/sc-grind.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nDUSKREAVE -- STAGE " + A.stage + ": "
          + {"1": "the 33rd relic, its ultimate STUBBED",
             "2": "THE TORNADO EXISTS AND SWEEPS -- and touches nobody",
             "3": "IT CATCHES, DRAGS AND TICKS -- THIS IS THE RELIC"}[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR. Every stage asserts what has to be under it.
    if "cursePool" not in s0:
        raise SystemExit("this source predates the v53 curse rework")
    if "tickSpectre" not in s0:
        raise SystemExit(
            "this source is not the Bloodmirror tip -- `tickSpectre` is absent.\n"
            "  Duskreave is the 33rd relic and builds on the 32nd; if the\n"
            "  intention is to build it somewhere else, say so with --src and\n"
            "  say why in the write-up, because the relic count in every doc\n"
            "  moves with it.")
    if A.stage == "1" and f'id:"{RELIC}"' in s0:
        raise SystemExit("this source already has Duskreave -- built")
    if A.stage == "2":
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("stage 2 needs stage 1's link -- no Duskreave in "
                             "this source")
        if "charge:1e9" not in body_block(s0, RELIC, "ult"):
            raise SystemExit(
                "the ultimate in this source is not stubbed, so stage 2 has\n"
                "  already run against it. Rebuild stage 1 first -- a stage\n"
                "  applied twice is how a builder writes numbers its own log\n"
                "  does not describe.")

    rule = curse_rule(s0)
    if rule == "UNRECOGNISED":
        raise SystemExit(
            "`pushCurse` in this source is neither the shipped three-biggest\n"
            "  rule nor the last-3 window. Brief section 1 says to build\n"
            "  against whichever is present and this builder cannot tell which\n"
            "  that is, so it stops rather than guessing.")
    print(f"  curse {rule}  "
          + ("keep the 3 BIGGEST -- the shipped rule. Scour prices in the "
             "+59.2pp tier." if rule == "BIGGEST-3" else
             "the LAST-3 window has landed. Scour prices in the +40.5pp tier."))

    # THE PHYSICAL STATS ARE THE TYPE'S, ASSERTED AND NOT ASSUMED. Every number
    # in the design was measured on Thornwake's body; they are only transferable
    # to a seventh scythe if the six shipped ones really do agree. If they do
    # not, the design's numbers are not this relic's numbers, and that is a
    # finding rather than a detail.
    scythes = ["lastlight", "thornwake", "foregone", "vesper", "cindercleave",
               "bloodmirror"]
    got = {r: phys(s0, r) for r in scythes}
    keys = ("reach", "width", "artW", "spin", "mass", "mode")
    base = {k: got[scythes[0]].get(k) for k in keys}
    odd = {r: {k: v.get(k) for k in keys if v.get(k) != base[k]}
           for r, v in got.items()}
    odd = {r: d for r, d in odd.items() if d}
    if odd:
        raise SystemExit(
            "the six shipped scythes do NOT agree on the type's own stats, so\n"
            "  the design's numbers -- all measured on one scythe body -- are\n"
            "  not transferable to a seventh:\n  "
            + "\n  ".join(f"{r}: {d}" for r, d in odd.items()))
    print(f"  body  one set across {len(scythes)} scythes -- the TYPE owns it: "
          + ", ".join(f"{k}:{base[k]}" for k in keys))

    # THE SILHOUETTE EXISTS AND IS ROUTED. This relic is the first ever to draw
    # it, so an unrouted school would ship a generic `_scBase` and nobody would
    # see it in a number.
    if 'if (key === "umbral")     return SHAPES._scEaten' not in s0:
        raise SystemExit(
            "`SHAPES.scythe` does not route `umbral` to `_scEaten`. This relic\n"
            "  is the first umbral scythe in the game, so the routing has never\n"
            "  been exercised -- if it has moved, the silhouette that ships is\n"
            "  the generic crescent and no measurement in this repo would say so.")
    print("  art   SHAPES.scythe routes umbral -> _scEaten (first ever use)")

    table = {"1": S1, "2": S2, "3": S3}[A.stage]
    # THE ANCHOR IS SUBSTITUTED TOO. Stage 2's anchors quote text stage 1
    # WROTE, and stage 1 wrote it with the placeholders already filled in -- so
    # an un-substituted anchor can never match its own builder's output.
    def fill(txt):
        return (txt.replace("%DMG%", f"{A.dmg:g}")
                  .replace("%ULT%", A.ult)
                  .replace("%TIP1%", ULT_TIP1)
                  .replace("%BLURB%", BLURB)
                  .replace("%CHARGE%", f"{A.charge:g}")
                  .replace("%DUR%", f"{A.dur:g}")
                  .replace("%W%", f"{A.w:g}")
                  .replace("%TOP%", f"{A.top:g}")
                  .replace("%SWEEP%", f"{A.sweep:g}")
                  .replace("%TICK%", f"{A.tick:g}")
                  .replace("%TICKDMG%", f"{A.tickdmg:g}")
                  .replace("%DRAG%", f"{A.drag:g}"))

    for label, old, new in table:
        s = one(s, fill(old), fill(new), label)

    ult_matches(s, A, A.stage)

    if len(A.tip) > 72:
        print("\n  NOTE -- THE SHIPPED TIP IS OVER `verify`'S BUDGET:")
        print(f"    {len(A.tip)} characters against 72, over by {len(A.tip) - 72}")
        print(TIP_OVER_BUDGET.rstrip())

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"  {len(s)} bytes")
    print(f"  relic dmg {A.dmg:g}, onHit curse 1, ult {A.ult} "
          + (f"STUBBED (charge 1e9, kind {ULT_KIND})" if A.stage == "1"
             else f"LIVE (charge {A.charge:g}, kind {ULT_KIND})"))
    if A.stage == "3":
        print(f"  tick {A.tick:g}/s at base {A.tickdmg:g}, drag {A.drag:g}, "
              f"EDGE catch rule (|x-cx| <= w/2 + R, y + R >= top)")
        print("  the tick goes through resolveHit and COLLECTS THE CURSE ECHO")
        print("    -- knock 0, stop 0, stun off, beat off; the FATAL tick")
        print("    still files, because a kill the director cannot see is")
        print("    Gravemourn's 30-of-58 all over again")
        print("\n  GATE 3 -- five checks, and each can fail:")
        print("    python scour_probe.py --game ../02-chain/sc-grind.html")
        print("      ticks must average WELL ABOVE base when the pool is not")
        print("      empty -- a tick that always deals round(5 x jitter) is")
        print("      collecting no echo and is on the wrong path")
        print("    and: no knock, no hit stop, no hitstun, no beat except the")
        print("      first catch and the fatal; stacks == pool after each tick")
        print("    python engine_ab.py --a ../02-chain/sc-scour.html \\")
        print("      --b ../02-chain/sc-grind.html --ids <the 32> --n 8")
        print("    FILM IT before tuning the drag (brief open decision 1)")
        return 0

    if A.stage == "2":
        print(f"  tornado dur {A.dur:g}s, w {A.w:g}, top y={A.top:g}, "
              f"sweep {A.sweep:g} px/s, charge {A.charge:g}")
        print("  starts UNDER THE CASTER heading toward the foe (Code's call,")
        print("    brief open decision 2) -- filmed at gate 2, not tuned")
        print("\n  GATE 2 -- and the first one is Rick's eye:")
        print("    FILM 3 CASTS ON 3 SEEDS, BEFORE ANY TUNING. The band must")
        print("      read as a third of the hall's width and a third of its")
        print("      height. CLAUDE.md 4.0: thirty seconds of clip on")
        print("      placeholder numbers costs four minutes.")
        print("    python engine_ab.py --a ../02-chain/sc-duskreave.html \\")
        print("      --b ../02-chain/sc-scour.html --ids <the 32> --n 8")
        print("      IDENTICAL on every pairing with no Duskreave in it.")
        print("\n  AND THE BAND IS A QUARTER OF THE HALL, NOT A THIRD.")
        print("    CONFIG.arena.h is 800 and `top` is 600, so the band is 200")
        print("    tall = 25%. The brief's own gloss on Rick's words says a")
        print("    third, which would be y=533. The NUMBER is what v62")
        print("    measured, so the number is what is built -- but the number")
        print("    and the sentence do not agree and he should know it.")
        print("    (The width does agree: 160/520 = 30.8%.)")
        return 0

    print("\n  GATE 1 -- run all three, and each can fail:")
    print("    python engine_ab.py --a ../02-chain/sc-bloodletting.html "
          "--b ../02-chain/sc-duskreave.html --n 10")
    print("    python verify.py --game ../02-chain/sc-duskreave.html --n 40")
    print("    the no-ult floor for duskreave, expected near 17.6% (v63 sec 3,")
    print("    control 2) -- near 26% means something is firing that should not")
    return 0


if __name__ == "__main__":
    sys.exit(main())
