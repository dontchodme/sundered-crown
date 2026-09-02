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
        if stage in ("3", "4"):
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


def cut_eaten(html: str) -> tuple[str, int]:
    """Delete `_scEaten` whole, by brace matching from its own header.

    Spec build note 2, and v58's precedent: `_whEaten` was DELETED when
    `_whGnawed` replaced it rather than left beside it. A dead grammar that
    still parses is a grammar the next `SHAPES.scythe` edit can route back to
    by accident, and it would be the shape Rick rejected on sight.

    Brace-matched and not regexed, because the function contains braces inside
    strings and comments and a regex that "works" here is one that breaks on
    the next grammar.
    """
    key = "  _scEaten(c, L, W, p){"
    i = html.find(key)
    if i < 0:
        return html, 0
    # WALK BACK OVER THE DOC COMMENT THAT BELONGS TO IT, and find it by its
    # END rather than by a prefix. The first cut searched backwards for `/* -`
    # and found one INSIDE the function pasted just above, so it cut from the
    # middle of `_scMoon` and took that function's tail with it -- caught by
    # the syntax gate, which is the entire reason that gate exists. The
    # comment that belongs to a header is the one whose `*/` is separated from
    # it by whitespace and nothing else.
    j = i
    end = html.rfind("*/", 0, i)
    if end > 0 and html[end + 2:i].strip() == "":
        start = html.rfind("/*", 0, end)
        if start > 0:
            j = start
    k = html.index("{", i + len(key) - 1)
    depth = 0
    while k < len(html):
        if html[k] == "{":
            depth += 1
        elif html[k] == "}":
            depth -= 1
            if depth == 0:
                break
        k += 1
    k += 1
    # step past the separator the object literal / class body uses
    sep = "," + chr(10)
    while k < len(html) and html[k] in sep:
        k += 1
        if html[k - 1] == ",":
            break
    return html[:j] + html[k:], i


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
        "tick": 7.0,
        # THE TICK'S DAMAGE, MEASURED, and it is the floor of its own range.
        # The brief's number was 5 ("Rick: lots of ticks for less damage") and
        # the relic measured 96.2% on `verify` with 13 of 32 opponents going
        # 0/40 against it. Rick, shown that: "lets drop the damage... i ment
        # drop the ults damage to 1 per tick if you have to."
        #
        #   tick   block 0   block 1     896 fights a point, both sides
        #   1.00     51.5%     55.0%     <- pooled ~53%, IN BAND
        #   1.50        -      72.4%
        #   2.00     82.8%     83.7%     <- reproduces across blocks
        #   3.00     90.6%         -
        #   5.00     96.8%         -     <- the brief's value
        #
        # THE CURVE IS A CLIFF: thirty points for one point of tick damage,
        # and no crossing above 1. There is no fine tuning available on this
        # axis -- 1 is the only value in band and it is also the lowest value
        # the engine can express, because `resolveHit` rounds and a base below
        # 1 would round to 0 on some rolls and 1 on others.
        #
        # AND THE REASON IT IS A CLIFF IS THE CURSE WINDOW. Under the old
        # three-biggest rule the echo was 60% of every tick and the pool held
        # the scythe's 35-damage blows; under the last-3 window every tick
        # displaces those with its own small `dmgBase`, so THE POOL FILLS WITH
        # THE TICK'S OWN DAMAGE and the echo collapses. What is left is raw
        # output -- 70 ticks a window -- which is linear in this number and
        # very nearly lethal at 5 (350 against a 400 hp fighter).
        "tickdmg": 1.0,
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
    /* A ZERO OVERRIDE DOES NOT TOUCH THE CLOCK AT ALL. `Math.max(hitStop, 0)`
       looks like a no-op and is not: the clock carries a small NEGATIVE
       residue between freezes, and clamping it up to exactly 0 is a write.
       Nothing reads the difference -- `step()` tests `hitStop > 0` -- but an
       invariant that is "nearly true" cannot be asserted, and a probe that has
       to allow 155 exceptions is a probe that will not notice the 156th.
       Identical for every ordinary hit, where `stop` is always positive. */
    if (stop > 0) this.hitStop = Math.max(this.hitStop, stop);'''),

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
    /* AND `seg` CANNOT BE NULL, WHICH THE BRIEF'S OWN SNIPPET PASSES.
       `resolveHit` reads `seg.bx - seg.ax` unconditionally, to fly the impact
       sparks ALONG the blade rather than outward from the point, so a null
       throws on the first tick that ever lands -- and it throws inside the
       step, which kills the match rather than the frame. Every projectile
       call site synthesises one; `tickShots` builds a 20-unit segment along
       the shot's own velocity.

       THE TORNADO'S IS HORIZONTAL, along the sweep. It is the bearing the
       thing is actually travelling on, so the sparks come off the way the
       band is moving -- the same reasoning that gave Breach's jets their own
       bearing instead of the caster's. */
    const sgx = T.dir || 1;
    const seg = { ax: foe.x - sgx * 10, ay: foe.y,
                  bx: foe.x + sgx * 10, by: foe.y, a: 0 };
    this.resolveHit(src, foe, foe.x, foe.y, seg, u.dmg / src.w.dmg,
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


# ------------------------------------------------------------------ stage 4 --

# IT EATS PROJECTILES. Flavour, never priced (v62 section 2) -- it fires in 9-10
# matchups of 30 and is busy only against the bows.
S4 = [

# ---- 1. THE EAT, AND IT RUNS BEFORE `tickShots` -----------------------------
# THE ORDER IS THE GUARANTEE, and it is the whole of the brief's "do not let the
# eaten shot deal damage". `tickShots` MOVES an arrow and RESOLVES it in the
# same pass, so an eat placed after it (where `tickScour` lives, with the other
# window tickers) would let a shot that was already inside the band travel and
# connect on the frame before it was removed. Running first, anything standing
# in the band at the top of the frame is gone before it can do anything at all.
#
# The band is the same `w` and `top` the catch uses and the drawing uses: one
# geometry, three readers. `drawVents`'s lesson -- a hazard drawn wider than it
# tests is a hazard that lies.
("eat-call", '''    this.tickNet(dt);
    this.tickShots(dt);''',
 '''    this.tickNet(dt);
    /* BEFORE `tickShots`, WHICH BOTH MOVES AND RESOLVES. An eat placed with the
       other window tickers -- after it, where `tickScour` runs -- would let an
       arrow already standing in the band travel and connect on the frame before
       it was eaten. The brief's "do not let the eaten shot deal damage" is an
       ORDERING requirement, not a flag. */
    this.scourEat();
    this.tickShots(dt);'''),

# ---- 2. THE METHOD ----------------------------------------------------------
("eat", '''  tickScour(dt){''',
 '''  /* ANY ENEMY SHOT INSIDE THE BAND IS REMOVED. `own` is the side string the
     shot was loosed by, so the test is "not the caster's" -- a Duskreave does
     not eat its own arrows, and it has none anyway, which is exactly why the
     check is written against the OWNER rather than against the weapon type.

     THE MARK IS A RING AND NOT A SPARK FIELD, and that is determinism rather
     than taste. `spawnFx` draws twice from `this.rng()` per particle, so a
     debris field here would move the RNG stream on every frame an arrow was
     eaten -- which is how Breach's sparks had to become DRAWN rather than
     spawned, after the same hazard re-invalidated a blade twice. `Match.ring`
     is a pure push and touches no randomness.

     ZERO BURDEN: returns on its first line with no tornado, and again with no
     shots, so 32 relics pay two null tests a frame. */
  scourEat(){
    const T = this.tornado;
    if (!T || !this.shots.length) return;
    const A = CONFIG.arena, half = T.w * 0.5;
    const floorY = A.h - this.inset;
    for (let i = this.shots.length - 1; i >= 0; i--){
      const s = this.shots[i];
      if (s.own === T.src) continue;
      if (s.y < T.top || s.y > floorY) continue;
      if (Math.abs(s.x - T.cx) > half) continue;
      /* IT VANISHES AND PAYS NOTHING. Not a hit, not a parry, no damage, no
         curse, nothing added to `shotHits` -- the arrow simply stops existing,
         which is what "absorbs projectiles" means on Rick's own card line. */
      this.shots.splice(i, 1);
      T.eaten++;
      this.ring(s.x, s.y, AFFINITIES.umbral.glow, 3, 26, 0.28, 3);
    }
  }

  tickScour(dt){'''),

# ---- 3. THE CAST COUNTS THEM ------------------------------------------------
("cast4", '''                       cd: 0, dealt: 0, filed: 0 };''',
 '''                       cd: 0, dealt: 0, filed: 0, eaten: 0 };'''),

]


# ----------------------------------------------------------------- stage 5a --

# THE SILHOUETTE, AND IT IS NOT THIS SESSION'S. Cowork owns the redraw
# (CLAIMS.md, 2026-09-02 03:58 UTC); Rick chose arm A, THE MOON, from a spread
# of four; the spec is `06-docs/v63/scmoon_spec.js` and it was CHECKED at 0
# pixels differing against the arm he actually picked (`scmoon_check.py`).
# `tools/umbral_scythe_lab.py`'s candidates -- this session's A-F and G-J -- are
# SUPERSEDED, and the file says so at its head.
#
# THE SPEC IS PASTED VERBATIM. Retyping any of it would be re-deciding a picture
# that is already settled, and the 0-pixel check would stop meaning anything.
S5A = [

("moon", '''  _scEaten(c, L, W, p){''', '  /* ------------------------------------------------------------------ UMBRAL --\n     THE MOON. Rick\'s, 2026-09-02, from three references (`06-docs/v63/\n     ref-scythe-1/2/3.jpg`) and a spread of four (`umbral-scythe-silhouette-\n     v63.md`). Replaces `_scEaten`, which he rejected on sight the first time it\n     was ever drawn ("this one is rough and should be redone").\n\n     WHAT IT IS: a thin blade sweeping ~175 degrees, its tip curling back toward\n     the shaft -- the blade is HALF the weapon\'s footprint, where `_scBase`\'s\n     crescent is a third. A faceted hub with a lit gem at the junction. A\n     near-black jointed shaft with three segments and a hex gem at the butt.\n     Near-black body, cold rim on the back, the honed edge lit twice.\n\n     CONSTRUCTION, and why:\n     * The honed edge is ONE cubic -- it carries the glow stroke, so it has to\n       be a clean curve. The back edge is that cubic pushed out along its\n       outward normal by a width profile w(t), so the blade\'s width is one\n       function and cannot disagree with the edge it belongs to.\n     * ONE closed path for the blade. v58\'s rule: a limb goes INTO the outline,\n       never behind it.\n     * The hub is drawn AFTER the blade and the blade\'s root sits inside it, so\n       the join is hidden at every zoom.\n     * The furthest point of the blade from the ball is 1.08 L (sim reach is\n       1.00 L; the shipped crescent was 1.02 L). Printed by the lab, not judged.\n     * Does not call `_scBase`, `_scCrescent` or `_scOuter`: the blade is a\n       different curve, and the inverted-normal defect those carry (open item,\n       `_scOuter`\'s comment) is not inherited.\n     * Nothing here touches the sim. `litWeapon` bakes it; no probe reads the\n       path. engine_ab must come back identical.\n  */\n  _scMoon(c, L, W, p){\n    const TAU = Math.PI * 2;\n    const S = SHAPES;\n\n    /* ---- the shaft: near-black, a cold highlight line, three segments, a\n            hex gem at the butt. The line is `_scBase`\'s own quadratic, moved\n            to meet the hub at (0.71L, 0.10W). ---- */\n    const at = (u) => { const it = 1 - u;\n      return { x: 2*it*u*(L*0.44) + u*u*(L*0.71), y: 2*it*u*(W*0.30) + u*u*(W*0.10),\n               a: Math.atan2(2*it*(W*0.30) + 2*u*(W*0.10 - W*0.30),\n                             2*it*(L*0.44) + 2*u*(L*0.71 - L*0.44)) }; };\n    c.lineCap = "round";\n    c.strokeStyle = S._ink(p.dark, 16); c.lineWidth = W*0.17;\n    c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(L*0.44, W*0.30, L*0.71, W*0.10); c.stroke();\n    c.strokeStyle = S._shade(p.steel, 0.55, 0.45); c.lineWidth = W*0.05;\n    c.beginPath(); c.moveTo(L*0.05, -W*0.03); c.quadraticCurveTo(L*0.44, W*0.25, L*0.66, W*0.08); c.stroke();\n    for (let i = 0; i < 3; i++){\n      /* a SEGMENT of the rod, longer along the shaft than across it, so the\n         shaft reads as jointed rather than beaded (ref 1) */\n      const q = at(0.20 + 0.20*i);\n      c.save(); c.translate(q.x, q.y); c.rotate(q.a);\n      c.beginPath();\n      c.moveTo(-W*0.20, 0); c.lineTo(-W*0.13, -W*0.13); c.lineTo(W*0.13, -W*0.13);\n      c.lineTo( W*0.20, 0); c.lineTo( W*0.13,  W*0.13); c.lineTo(-W*0.13, W*0.13);\n      c.closePath();\n      c.fillStyle = S._ink(p.dark, 24); c.fill();\n      c.strokeStyle = p.core + "BB"; c.lineWidth = Math.max(1, W*0.028); c.stroke();\n      c.restore();\n    }\n    c.save(); c.rotate(at(0.02).a);                          // pommel gem\n    c.beginPath();\n    for (let i = 0; i < 6; i++){ const a = i*TAU/6, r = W*0.20;\n      if (i === 0) c.moveTo(Math.cos(a)*r, Math.sin(a)*r); else c.lineTo(Math.cos(a)*r, Math.sin(a)*r); }\n    c.closePath();\n    c.fillStyle = S._ink(p.dark, 22); c.fill();\n    c.strokeStyle = S._shade(p.steel, 1.0, 0.40); c.lineWidth = Math.max(1, W*0.03); c.stroke();\n    c.save(); c.globalCompositeOperation = "lighter";\n    { const g = c.createRadialGradient(0, 0, 0, 0, 0, W*0.30);\n      g.addColorStop(0, p.glow); g.addColorStop(0.4, p.core + "AA"); g.addColorStop(1, p.core + "00");\n      c.fillStyle = g; c.beginPath(); c.arc(0, 0, W*0.30, 0, TAU); c.fill(); }\n    c.restore();\n    c.fillStyle = p.glow; c.beginPath(); c.arc(0, 0, W*0.07, 0, TAU); c.fill();\n    c.restore();\n\n    /* ---- the blade ---- */\n    const P = [[L*0.72, W*0.02], [L*1.05, -W*0.24], [L*0.99, -W*1.46], [L*0.48, -W*1.52]];\n    const bez = (u) => {\n      const it = 1 - u;\n      const b  = (a,bq,cq,d) => it*it*it*a + 3*it*it*u*bq + 3*it*u*u*cq + u*u*u*d;\n      const db = (a,bq,cq,d) => 3*it*it*(bq-a) + 6*it*u*(cq-bq) + 3*u*u*(d-cq);\n      const x = b(P[0][0],P[1][0],P[2][0],P[3][0]), y = b(P[0][1],P[1][1],P[2][1],P[3][1]);\n      let tx = db(P[0][0],P[1][0],P[2][0],P[3][0]), ty = db(P[0][1],P[1][1],P[2][1],P[3][1]);\n      const m = Math.hypot(tx, ty) || 1; tx /= m; ty /= m;\n      return { x, y, tx, ty };\n    };\n    /* outward = toward the control points, which sit on the convex side of a\n       single-bend cubic; the sign is taken once at the midpoint */\n    const M = [(P[1][0]+P[2][0])/2, (P[1][1]+P[2][1])/2], mid = bez(0.5);\n    const sgn = (mid.ty*(M[0]-mid.x) - mid.tx*(M[1]-mid.y)) > 0 ? 1 : -1;\n    const edge = (t) => { const q = bez(t); return { x:q.x, y:q.y, nx: sgn*q.ty, ny: -sgn*q.tx }; };\n    const wAt = (t) => W*0.34 * Math.pow(1 - t, 0.62) * (t < 0.10 ? 0.75 + 2.5*t : 1);\n    const N = 48;\n    const blade = () => {\n      c.beginPath();\n      c.moveTo(P[0][0], P[0][1]);\n      c.bezierCurveTo(P[1][0],P[1][1],P[2][0],P[2][1],P[3][0],P[3][1]);   // honed edge, root -> tip\n      for (let i = N; i >= 0; i--){                                       // back edge, tip -> root\n        const t = i / N, q = edge(t), w = wAt(t);\n        c.lineTo(q.x + q.nx*w, q.y + q.ny*w);\n      }\n      c.closePath();\n    };\n    blade();\n    { const g = c.createLinearGradient(P[0][0], P[0][1], P[3][0], P[3][1]);\n      g.addColorStop(0, S._ink(p.dark, 30)); g.addColorStop(0.5, S._ink(p.dark, 18)); g.addColorStop(1, S._ink(p.dark, 26));\n      c.fillStyle = g; c.fill(); }\n    c.save(); c.shadowBlur = 0;                                  // the lit face, clipped\n    { const wl = S._litN(c); c.globalAlpha = 0.55 * Math.abs(wl) + 0.25;\n      blade(); c.clip();\n      c.strokeStyle = S._shade(p.steel, 0.70, 0.30); c.lineWidth = Math.max(1, W*0.09);\n      c.beginPath();\n      for (let i = 0; i <= 40; i++){ const t = i/40, q = edge(t), w = wAt(t)*0.66;\n        const x = q.x + q.nx*w, y = q.y + q.ny*w; if (i === 0) c.moveTo(x, y); else c.lineTo(x, y); }\n      c.stroke(); }\n    c.restore();\n    c.strokeStyle = S._shade(p.steel, 1.15, 0.55); c.lineWidth = Math.max(1, W*0.035);   // cold rim\n    blade(); c.stroke();\n    const honed = () => { c.beginPath(); c.moveTo(P[0][0], P[0][1]);\n      c.bezierCurveTo(P[1][0],P[1][1],P[2][0],P[2][1],P[3][0],P[3][1]); c.stroke(); };\n    c.lineCap = "round";\n    c.strokeStyle = p.core + "77"; c.lineWidth = Math.max(1, W*0.15); honed();          // wide and soft\n    c.strokeStyle = p.glow;        c.lineWidth = Math.max(1, W*0.055); honed();         // tight and bright\n\n    /* ---- the hub: a faceted plate over the blade\'s root, a lit gem, the\n            school\'s mark (tarnish) on its face ---- */\n    const hx = L*0.71, hy = W*0.10, r = W*0.30;\n    c.save(); c.translate(hx, hy);\n    c.beginPath();\n    for (let i = 0; i < 6; i++){ const a = -Math.PI/2 + i*TAU/6;\n      if (i === 0) c.moveTo(Math.cos(a)*r, Math.sin(a)*r); else c.lineTo(Math.cos(a)*r, Math.sin(a)*r); }\n    c.closePath();\n    c.fillStyle = S._ink(p.dark, 20); c.fill();\n    c.strokeStyle = S._shade(p.steel, 1.05, 0.40); c.lineWidth = Math.max(1, W*0.035); c.stroke();\n    c.beginPath();                                               // inner facet\n    for (let i = 0; i < 6; i++){ const a = -Math.PI/2 + i*TAU/6 + Math.PI/6;\n      if (i === 0) c.moveTo(Math.cos(a)*r*0.62, Math.sin(a)*r*0.62); else c.lineTo(Math.cos(a)*r*0.62, Math.sin(a)*r*0.62); }\n    c.closePath();\n    c.strokeStyle = p.core + "88"; c.lineWidth = Math.max(1, W*0.025); c.stroke();\n    const gr = r*0.36;                                           // the gem\n    c.save(); c.globalCompositeOperation = "lighter";\n    { const g = c.createRadialGradient(0, 0, 0, 0, 0, gr*2.2);\n      g.addColorStop(0, p.glow); g.addColorStop(0.35, p.core + "AA"); g.addColorStop(1, p.core + "00");\n      c.fillStyle = g; c.beginPath(); c.arc(0, 0, gr*2.2, 0, TAU); c.fill(); }\n    c.restore();\n    c.fillStyle = p.glow; c.beginPath(); c.arc(0, 0, gr*0.55, 0, TAU); c.fill();\n    c.restore();\n    S._makerMark(c, hx + r*0.55, hy + r*0.45, W*0.10, W*0.62, p);\n  },\n\n' +
 '''  _scEaten(c, L, W, p){'''),

("route", '''    if (key === "umbral")     return SHAPES._scEaten(c, L, W, p);''',
 '''    if (key === "umbral")     return SHAPES._scMoon(c, L, W, p);'''),

]


# ----------------------------------------------------------------- stage 5b --

# THE FUNNEL, BUILT AGAINST RICK'S OWN REFERENCE. `06-docs/v63/ref-vortex.mp4`,
# and the brief writes down what is in it so it can be built without the video:
# a neon-purple CEL-SHADED funnel, narrow at the floor and widening upward, made
# of STACKED GLOWING BANDS -- magenta cores with lilac-white rims -- that tilt
# and slide against each other as it turns; a large bright RING around the top
# like a halo, wider than the funnel; ragged near-black DEBRIS orbiting between
# the bands; and at the floor a hard horizontal glow line with a bright magenta
# POOL. Hard edges, high contrast, NO SOFT PARTICLE SMOKE -- it is drawn, not
# simulated. Rick, on the placeholder: "the tornado is just a purple box."
#
# THE ONE THING THE REFERENCE AND THE MECHANIC DISAGREE ABOUT, AND IT IS NOT
# SETTLED BY DRAWING IT PRETTIER. The reference funnel is NARROW AT THE FLOOR;
# the catch is a full-width band at every height (`|x - cx| <= w/2 + R`). Drawn
# literally, the picture would say the floor is safe where the hazard is
# widest -- and CLAUDE.md is explicit that a picture claiming a SMALLER hazard
# than the one that exists is the hardest kind of bug in this repo to see.
# So the taper is drawn as the reference has it AND the floor carries the
# reference's own answer: the hard glow line and the pool span the FULL band
# width, so the footprint is stated by the brightest thing in the picture. The
# hazard's extent is never implied by the funnel alone.
#
# NOT ONE `this.rng()` CALL. Every phase is derived from `T.t` and an index, the
# way Breach's sparks had to be after `spawnFx` re-invalidated a blade twice --
# it draws twice from the stream per particle. A debris field here would move
# every Duskreave fight and put gate 6's price on a different sim.
#
# AND NO PER-FRAME GRADIENTS IN A LOOP. `GRAIN_CACHE`'s comment names nine
# `createRadialGradient` calls per relic per frame as "the single cause of the
# stutter Rick reported", and Breach's billow put one inside a lobe loop for
# seventy-two a frame and cost 14x the render time. Everything below is flat
# fills and strokes under `lighter`.
S5B = [

("funnel", '''    const P = AFFINITIES.umbral;''',
 '''    const P = AFFINITIES.umbral;
    /* ONE DETERMINISTIC HASH, standing in for the randomness this must not
       have. Index in, a number in [0,1) out, stable for the life of the
       build -- so the debris and the lightning are the same on every replay
       of a seed, which is what `engine_ab` and every recorded number rest on. */
    const h1 = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
                        return x - Math.floor(x); };'''),

("funnel-body", '''    if (!over){
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
    }''',
 '''    /* THE FUNNEL'S OWN GEOMETRY. `u` runs 0 at the floor to 1 at the top, and
       the radius opens with it -- the reference's taper. `THROAT` is how narrow
       the foot gets; it is a picture number and the pool below states the real
       width regardless. */
    const NB = 15, THROAT = 0.34, spin = T.t * 2.3;
    const GAP = (y1 - y0) / NB;          // what one band has to cover
    const bandAt = (u) => {
      const r = half * (THROAT + (1 - THROAT) * Math.pow(u, 0.78));
      /* THE SLIDE. Each ring is offset along the sweep by its own phase, so
         the stack leans and shears instead of sitting like a stack of plates
         -- "tilt and slide against each other as it turns". */
      const ph = spin + u * 3.1;
      /* THE TILT AND THE ELONGATION, and they are one motion rather than two
         effects. Rick, 2026-09-02: "give the whole thing a better sense of
         motion by adding slight tilts to the rings and having them slightly
         elongate into ellipses when appropriate."

         A ring seen edge-on is a line and a ring seen from above is a circle;
         everything between is an ellipse whose SHORT axis and whose TILT both
         follow the same phase. So `ry` opens and closes on `cos(ph)` while
         `rot` leans on `sin(ph)` -- a quarter-turn apart, which is what makes
         a rolling ring read as rolling instead of as a shape being squashed.
         Small on purpose: "slight", and a big tilt turns a funnel into a
         stack of thrown hoops. */
      const e = 0.5 + 0.5 * Math.cos(ph);
      return { y: y1 - (y1 - y0) * u, r: r,
               cx: T.cx + Math.sin(ph) * r * 0.16,
               ry: Math.max(3, r * (0.15 + 0.13 * e)),
               rot: Math.sin(ph) * 0.13,
               ph: ph };
    };
    if (!over){
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = fade;
      /* THE POOL AND THE HARD LINE, AND THEY ARE THE FULL BAND WIDTH. This is
         the picture's statement of where the hazard actually is, and it is
         deliberately the brightest thing in it. */
      c.fillStyle = P.core + "44";
      c.beginPath();
      c.ellipse(T.cx, y1, half, 15, 0, 0, Math.PI * 2);
      c.fill();
      c.fillStyle = P.glow + "88";
      c.beginPath();
      c.ellipse(T.cx, y1, half * 0.62, 7, 0, 0, Math.PI * 2);
      c.fill();
      c.fillStyle = P.glow;
      c.fillRect(x0, y1 - 1.5, T.w, 3);
      /* THE BODY, AND IT IS WHAT STOPS THIS READING AS A STACK OF HOOPS.
         Rick, on the first cut: "lets fill in the gaps now so it looks less
         like disconnected rings."

         One closed skin down the left edge of every band and back up the
         right, so the funnel is a SURFACE the rings sit on rather than a set
         of separate objects at different heights. Filled once, flat, at a low
         alpha under `lighter` -- a gradient here would be a per-frame
         `createLinearGradient` and this loop already runs fifteen times.

         Drawn BEFORE the rings so they read as bands ON the body, and under
         the fighters so a caught ball is inside it. */
      c.beginPath();
      for (let i = 0; i <= NB; i++){
        const b = bandAt(i / NB);
        if (i === 0) c.moveTo(b.cx - b.r, b.y);
        else c.lineTo(b.cx - b.r, b.y);
      }
      for (let i = NB; i >= 0; i--){
        const b = bandAt(i / NB);
        c.lineTo(b.cx + b.r, b.y);
      }
      c.closePath();
      c.globalAlpha = fade * 0.52;
      c.fillStyle = P.core;
      c.fill();
      /* AND A DARKER CORE DOWN THE MIDDLE, so the body has depth rather than
         being one flat wash -- the throat of a funnel is the part you are
         looking INTO. Source-over, not lighter: it has to take light away. */
      c.globalCompositeOperation = "source-over";
      c.globalAlpha = fade * 0.34;
      c.fillStyle = SHAPES._ink(P.dark, 10);
      c.beginPath();
      for (let i = 0; i <= NB; i++){
        const b = bandAt(i / NB);
        if (i === 0) c.moveTo(b.cx - b.r * 0.46, b.y);
        else c.lineTo(b.cx - b.r * 0.46, b.y);
      }
      for (let i = NB; i >= 0; i--){
        const b = bandAt(i / NB);
        c.lineTo(b.cx + b.r * 0.46, b.y);
      }
      c.closePath();
      c.fill();
      c.globalCompositeOperation = "lighter";
      /* THE BACK HALF OF EVERY BAND. Drawn under the fighters, so a ball
         inside the funnel is IN it rather than in front of a picture of it. */
      c.lineCap = "butt";
      for (let i = 0; i < NB; i++){
        const u = (i + 0.5) / NB, b = bandAt(u);
        c.globalAlpha = fade * (0.26 + 0.30 * u);
        c.strokeStyle = P.core;
        c.lineWidth = Math.max(3, GAP * 0.92);
        c.beginPath();
        c.ellipse(b.cx, b.y, b.r, b.ry, b.rot, Math.PI, Math.PI * 2);
        c.stroke();
      }
      c.restore();
      return;
    }'''),

("funnel-over", '''    /* THE TWO EDGES, over everything, because they are the boundary the whole
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
    c.restore();''',
 '''    /* THE FRONT HALF OF EVERY BAND, over the balls, with the lilac-white rim
       the reference gives them. Cel-shaded: a hard core stroke and a hard rim
       stroke, no gradient between -- "hard edges, high contrast". */
    c.globalCompositeOperation = "lighter";
    c.lineCap = "butt";
    for (let i = 0; i < NB; i++){
      const u = (i + 0.5) / NB, b = bandAt(u);
      c.globalAlpha = fade * (0.40 + 0.42 * u);
      c.strokeStyle = P.core;
      c.lineWidth = Math.max(3, GAP * 0.92);
      c.beginPath();
      c.ellipse(b.cx, b.y, b.r, b.ry, b.rot, 0, Math.PI);
      c.stroke();
      c.globalAlpha = fade * (0.55 + 0.40 * u);
      c.strokeStyle = P.glow;
      c.lineWidth = Math.max(1, GAP * 0.22);
      c.beginPath();
      c.ellipse(b.cx, b.y, b.r, b.ry, b.rot, 0.12, Math.PI - 0.12);
      c.stroke();
    }
    /* THE DEBRIS. Ragged near-black shards orbiting BETWEEN the bands -- the
       one dark element, and what stops the funnel reading as a light effect
       rather than as something with things caught in it. `_ink` keeps them the
       school's hue at the school's own value instead of a literal near-black,
       which no instrument in this project can see. */
    c.globalCompositeOperation = "source-over";
    c.fillStyle = SHAPES._ink(P.dark, 16);
    /* FOUR SHARD PROFILES, not one. Rick: "lets also draw more debris so it
       varies more." A single outline repeated twenty times reads as a texture
       and stops reading as OBJECTS -- the eye finds the repeat long before it
       counts the pieces. Each profile is a unit polygon scaled by `sz`, so
       adding a fifth is four numbers. */
    const SHARD = [
      [[-1,-0.40],[0.50,-1.00],[1.00,0.50],[-0.30,0.80]],           // a chip
      [[-1,-0.16],[0.20,-0.62],[1.00,0.10],[0.30,0.66],[-0.60,0.50]],// a plate
      [[-0.90,-0.80],[0.95,-0.25],[0.20,0.90]],                      // a splinter
      [[-1,-0.25],[-0.10,-0.95],[0.85,-0.55],[1.00,0.35],
       [0.10,0.95],[-0.80,0.55]]                                     // a lump
    ];
    const shard = (dx, dy, sz, rot, k) => {
      const P4 = SHARD[k & 3], ca = Math.cos(rot), sa = Math.sin(rot);
      c.beginPath();
      for (let j = 0; j < P4.length; j++){
        const px = P4[j][0] * sz, py = P4[j][1] * sz;
        const qx = dx + px * ca - py * sa, qy = dy + px * sa + py * ca;
        if (j === 0) c.moveTo(qx, qy); else c.lineTo(qx, qy);
      }
      c.closePath(); c.fill();
    };
    /* THE ORBIT. Twenty-four pieces at their own heights, radii and rates, and
       each TUMBLES on its own axis as it goes -- debris that keeps its
       orientation reads as a decal on a cylinder. */
    for (let i = 0; i < 24; i++){
      const u = h1(i * 3.7);
      const b = bandAt(0.05 + u * 0.92);
      const rate = 1.05 + h1(i) * 0.75;
      const a = spin * rate + i * 2.1;
      /* SOME RIDE THE SKIN AND SOME FLY THROUGH IT. Rick: "more debris flying
         through it." A piece at `rr > 1` is outside the band it belongs to and
         crosses the funnel's face; one under it is down in the throat. */
      const rr = 0.55 + h1(i * 5.3) * 0.75;
      const dx = b.cx + Math.cos(a) * b.r * rr;
      const dy = b.y + Math.sin(a) * b.ry * rr;
      const sz = 2.5 + h1(i * 1.9) * 5.5;
      c.globalAlpha = fade * (Math.sin(a) > 0 ? 0.88 : 0.30);
      shard(dx, dy, sz, a * (0.6 + h1(i * 7.1)), i);
    }
    /* THE HALO. A single bright ring around the top, WIDER than the funnel --
       the reference's most distinctive shape and the thing that says which end
       is the mouth. */
    c.globalCompositeOperation = "lighter";
    const topB = bandAt(1.0);
    c.globalAlpha = fade * 0.9;
    c.strokeStyle = P.glow;
    c.lineWidth = 3;
    c.beginPath();
    c.ellipse(topB.cx, y0, half * 1.16, half * 0.24 + topB.ry * 0.30,
              topB.rot * 0.6, 0, Math.PI * 2);
    c.stroke();
    c.globalAlpha = fade * 0.45;
    c.strokeStyle = P.core;
    c.lineWidth = 8;
    c.beginPath();
    c.ellipse(topB.cx, y0, half * 1.16, half * 0.24 + topB.ry * 0.30,
              topB.rot * 0.6, 0, Math.PI * 2);
    c.stroke();
    /* THE ELECTRICITY. Rick's section 1: "crackling with electricity." Between
       the bands always, and JUMPING TO A CAUGHT BALL while one is held -- which
       is the only element in the whole picture that changes when the mechanic
       fires, so it is the tell that the thing is working. Stepped off a
       quantised clock so a bolt lasts several frames instead of strobing. */
    const tick = Math.floor(T.t * 14);
    c.strokeStyle = P.glow;
    /* A BOLT IS A POLYLINE WITH SEVERAL KINKS, not one elbow. Three segments
       is the least that reads as electricity rather than as a bent stick, and
       the kinks come off the quantised clock so a bolt holds for a few frames
       instead of strobing. */
    const bolt = (x0b, y0b, x1b, y1b, n, jit, seedn) => {
      c.beginPath();
      c.moveTo(x0b, y0b);
      for (let k = 1; k < n; k++){
        const f = k / n;
        c.lineTo(x0b + (x1b - x0b) * f + (h1(seedn + k * 9.7) - 0.5) * jit,
                 y0b + (y1b - y0b) * f + (h1(seedn + k * 4.3) - 0.5) * jit);
      }
      c.lineTo(x1b, y1b);
      c.stroke();
    };
    /* BETWEEN THE BANDS -- seven now rather than three. Rick: "more lightning
       arching off the tornado." */
    c.lineWidth = 1.6;
    for (let i = 0; i < 7; i++){
      const s0 = h1(tick * 7.3 + i), s1 = h1(tick * 3.1 + i * 5.7);
      const a0 = bandAt(0.10 + s0 * 0.8), a1 = bandAt(0.10 + s1 * 0.8);
      c.globalAlpha = fade * (0.45 + h1(tick + i * 3.3) * 0.45);
      bolt(a0.cx + (h1(tick + i) - 0.5) * a0.r * 1.7, a0.y,
           a1.cx + (h1(tick + i * 2.3) - 0.5) * a1.r * 1.7, a1.y,
           4, 20, tick * 1.7 + i);
    }
    /* AND FOUR THAT LEAVE IT. A bolt that only ever runs between two bands
       stays inside the silhouette and reads as internal wiring; one that
       arcs OUT and dies in the air is what makes the thing look like it is
       throwing charge off itself. They start on the skin and end well
       outside it, and they are dimmer because they are further away. */
    c.lineWidth = 1.3;
    for (let i = 0; i < 4; i++){
      const b = bandAt(0.15 + h1(tick * 2.9 + i * 6.1) * 0.8);
      const ang = h1(tick * 5.7 + i) * Math.PI * 2;
      const reach = b.r * (1.5 + h1(tick + i * 8.9) * 1.4);
      c.globalAlpha = fade * (0.30 + h1(tick * 4.1 + i) * 0.35);
      bolt(b.cx + Math.cos(ang) * b.r * 0.9, b.y + Math.sin(ang) * b.ry * 0.9,
           b.cx + Math.cos(ang) * reach, b.y + Math.sin(ang) * reach * 0.55,
           3, 16, tick * 3.3 + i * 2.7);
    }
    /* ------------------------------------------------------------- THE COW
       THE FIRST EASTER EGG IN THIS GAME. Rick, 2026-09-02: "lets have a small
       amount of seeds 10-15% show a cow flying around the tornado."

       IT IS CHOSEN FROM THE MATCH'S OWN SEED AND NOT FROM `this.rng()`, and
       that is the whole engineering problem in one line. The seed IS the
       fight: every recorded number, every clip, `engine_ab` and the entire
       history of this project rest on `(build, relics, seed)` naming one
       fight. A draw that consumed a random number would move the sim, so the
       cow would change the fight it appears in -- and an easter egg that
       alters the balance is a bug wearing a joke.

       `m.seed` is stable, it is per-fight, and it is already the thing the
       viewer would quote if they wanted to see it again -- which is what an
       easter egg is FOR. Seeds are dense in the low integers, so the hash is
       taken on a scaled seed to avoid the banding a raw `sin(n)` gives on
       consecutive inputs.

       12.5%, inside Rick's 10-15%, and it is one line to move. */
    if (h1(m.seed * 0.61803398875) < 0.125){
      /* SHE ORBITS WIDER AND SLOWER THAN THE DEBRIS, so she reads as a
         separate object caught in the thing rather than as one more shard --
         and she tumbles, because a cow in a tornado is not flying, she is
         being thrown. */
      const cowA = T.t * 1.05;
      const cb = bandAt(0.52 + Math.sin(T.t * 0.55) * 0.30);
      const cx2 = cb.cx + Math.cos(cowA) * cb.r * 1.55;
      const cy2 = cb.y + Math.sin(cowA) * cb.ry * 1.9;
      const cs = 9;
      c.save();
      c.globalCompositeOperation = "source-over";
      c.globalAlpha = fade * (Math.sin(cowA) > 0 ? 0.95 : 0.45);
      c.translate(cx2, cy2);
      c.rotate(cowA * 1.7);
      /* Drawn small and read as a SILHOUETTE: body, head, four legs, tail,
         one ear. The patches are the only lighter mark and they are what makes
         it a cow rather than a dog -- at nine pixels the outline alone is a
         quadruped and nothing more. */
      c.fillStyle = SHAPES._ink(P.dark, 12);
      c.beginPath();
      c.ellipse(0, 0, cs, cs * 0.60, 0, 0, Math.PI * 2);
      c.fill();
      c.beginPath();                                       // head and snout
      c.ellipse(cs * 1.02, -cs * 0.22, cs * 0.42, cs * 0.34, -0.25,
                0, Math.PI * 2);
      c.fill();
      c.fillRect(-cs * 0.62, cs * 0.40, cs * 0.26, cs * 0.62);   // legs
      c.fillRect(-cs * 0.16, cs * 0.44, cs * 0.24, cs * 0.60);
      c.fillRect( cs * 0.34, cs * 0.42, cs * 0.24, cs * 0.60);
      c.fillRect( cs * 0.70, cs * 0.36, cs * 0.22, cs * 0.56);
      c.beginPath();                                       // tail
      c.moveTo(-cs * 0.95, -cs * 0.10);
      c.quadraticCurveTo(-cs * 1.60, cs * 0.10, -cs * 1.35, cs * 0.75);
      c.lineTo(-cs * 1.12, cs * 0.70);
      c.quadraticCurveTo(-cs * 1.30, cs * 0.14, -cs * 0.88, cs * 0.16);
      c.closePath(); c.fill();
      c.beginPath();                                       // ear
      c.moveTo(cs * 1.16, -cs * 0.52);
      c.lineTo(cs * 1.52, -cs * 0.74);
      c.lineTo(cs * 1.24, -cs * 0.28);
      c.closePath(); c.fill();
      c.fillStyle = P.glow;                                // the patches
      c.globalAlpha *= 0.80;
      c.beginPath();
      c.ellipse(-cs * 0.34, -cs * 0.10, cs * 0.28, cs * 0.22, 0.3,
                0, Math.PI * 2);
      c.fill();
      c.beginPath();
      c.ellipse(cs * 0.36, cs * 0.14, cs * 0.20, cs * 0.16, -0.2,
                0, Math.PI * 2);
      c.fill();
      c.restore();
    }

    if (T.caught){
      /* A BOLT INTO THE THING IT IS GRINDING. The tick deals no knock, no hit
         stop and no stagger by design, so without this the most violent part
         of the relic has NO representation on the quarry at all -- which is
         the fault v59 found on the bleed drips and v54 on the arming sigil. */
      const q = T.src === "a" ? m.b : m.a;
      const b = bandAt(0.45);
      c.globalAlpha = fade * 0.95;
      c.lineWidth = 2.2;
      c.beginPath();
      c.moveTo(b.cx, b.y);
      const mx2 = (b.cx + q.x) * 0.5 + (h1(tick * 2.9) - 0.5) * 30;
      const my2 = (b.y + q.y) * 0.5 + (h1(tick * 5.1) - 0.5) * 20;
      c.lineTo(mx2, my2);
      c.lineTo(q.x, q.y);
      c.stroke();
    }
    c.restore();'''),

]


# ----------------------------------------------------------------- stage 5c --

# SCOUR'S VOICE. The candidates are `tools/scour_sound_lab.py`'s, verbatim, so
# what Rick hears in a clip is exactly what he heard in the spread -- a voice
# retyped between the audition and the build is a voice nobody chose.
#
# `--cast A1|A2|A3  --holdv B1|B2|B3  --tickv C1|C2` select; the default is the
# neutral set the spread itself used.
#
# THE SIM CALLS IT AND THAT IS SAFE, WHICH IS ASSERTED RATHER THAN ASSUMED.
# `SFX.play` returns on its first line when `!this.on` -- which is every
# headless run -- and nothing in the audio path draws from `this.rng()`. So
# `engine_ab` over the roster is the proof, and it is the same proof v42's
# silent ultimate never had.
#
# AND THE HOLD IS RE-STRUCK ON THE WINDOW'S OWN CLOCK, not on a frame counter.
# CLAUDE.md 4.5: `_burst` does not loop its 0.6s noise buffer and `_tone` ends
# on a ramp over its whole length, so A HELD NOTE DOES NOT EXIST in this
# toolkit. `T.hum` counts down in window time, so the cadence survives hit stop
# the way the window does.
S5C = [

# ---- 1. THE THREE NEW KINDS -------------------------------------------------
("sweep", '''  _tone(t, {freq=180, to=null, gain=0.3, dur=0.2, type="sine"}, dest){''',
 '''  /* A SWEPT NOISE BAND. THE TOOLKIT DID NOT HAVE ONE, and that is why the
     first two wooshes read as ticks -- Rick, 2026-09-02: "those read as ticks
     not wooshes."

     `_burst` sets its filter with `setValueAtTime` -- FIXED, never ramped --
     and its gain starts at full and decays exponentially. That is a percussive
     envelope on a static filter, so **every `_burst` in this game is a tick by
     construction**, and five of them at rising frequencies is a xylophone run
     rather than a sweep. No amount of gain or spacing fixes that; the envelope
     and the fixed filter are the sound.

     This is the same shape of finding as CLAUDE.md 4.5's "a held note does not
     exist in this toolkit", one primitive along: **swept noise did not exist
     either.** Two things make it a woosh rather than a tick:

       * THE FILTER RAMPS -- `f0` to `f1` across the whole duration, so the
         band MOVES and the ear hears one object passing instead of several
         objects struck;
       * THE GAIN HAS AN ATTACK -- it swells over `atk` and only then falls.
         An instant attack is a transient, and a transient IS a tick, however
         long the tail behind it.

     `dur` IS CAPPED AT THE NOISE BUFFER. `this.noise` is 0.6s and does not
     loop (4.5), so a longer sweep plays silence for its tail -- the same trap
     that shapes every burst in this file. Refused rather than truncated,
     because silence is the failure this project has shipped before.

     General, not Scour's: any relic wanting wind, a passing object or a
     filter sweep now has one call for it. */
  _sweep(t, {f0=300, f1=2400, q=0.7, gain=0.10, dur=0.45, atk=0.14,
             type="bandpass"}, dest){
    if (dur > 0.58) dur = 0.58;
    const src = this.ctx.createBufferSource(); src.buffer = this.noise;
    const flt = this.ctx.createBiquadFilter(); flt.type = type;
    flt.frequency.setValueAtTime(f0, t);
    flt.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t + dur);
    flt.Q.value = q;
    const g = this.ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + Math.min(atk, dur * 0.6));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(flt); flt.connect(g); g.connect(dest || this.bus);
    src.start(t); src.stop(t + dur + 0.02);
    return src;
  }

  _tone(t, {freq=180, to=null, gain=0.3, dur=0.2, type="sine"}, dest){'''),

("sfx", '''      else if (kind === "ult"){
        const w = p.w;''',
 '''      /* SCOUR'S HOLD, TICK AND MOO. Their own kinds rather than `ult`
         sub-cases, because they are struck seventy times a window and `ult`
         is an event -- and because `kind` is what the whole toolkit
         dispatches on. */
      else if (kind === "scour-hold"){
%HOLDJS%
      }
      else if (kind === "scour-tick"){
%TICKJS%
      }
      else if (kind === "scour-woosh"){
        /* THE WOOSH. Rick, 2026-09-02, having taken B1 for the hold: "can we
           also give the tornado a wooshing sound."

           IT IS A DIFFERENT JOB FROM THE BED AND THAT IS WHY IT IS A SEPARATE
           LAYER. B1 says the tornado EXISTS -- a flat wind floor, struck four
           times a second, deliberately even so ten seconds of it does not
           wear out. A woosh says the tornado is MOVING, and this one really is
           moving: it sweeps the hall at 200 px/s and bounces off the walls.
           Folding the movement into the bed would mean a bed that swells and
           fades, which is the one thing a ten-second floor must not do.

           A WOOSH IS A MOVING FILTER, NOT A MOVING PITCH. A rising pitch is a
           whistle; a cutoff climbing through a noise band and falling back is
           air going past. Five overlapping bursts up and down, because one
           long burst would play silence past 0.6s (CLAUDE.md 4.5) -- the same
           reason the cast sweeps in six.

           Under the bed on purpose: it is the second thing you notice, not
           the first. */
        const n = p.n || 0, v = 1 + (n % 3) * 0.11;
        /* UP AND THEN DOWN, as two overlapping sweeps -- something passing
           gets closer and then goes away, and a sweep that only rises is a
           siren. The second starts before the first has finished so there is
           no seam between them.

           Q IS LOW (0.55). A high Q is a resonant whistle -- pitch -- and this
           has to read as AIR, which is a wide band moving rather than a note
           moving. */
        this._sweep(t, { f0: 240 * v, f1: 1650 * v, q: 0.55, gain: 0.105,
                         dur: 0.34, atk: 0.20, type:"bandpass" });
        this._sweep(t + 0.26, { f0: 1500 * v, f1: 300 * v, q: 0.55,
                                gain: 0.078, dur: 0.40, atk: 0.10,
                                type:"bandpass" });
        /* AND A LOW BODY UNDER IT, swelling with the pass, so the woosh has
           weight rather than being all air. */
        this._sweep(t + 0.05, { f0: 120, f1: 260, q: 0.5, gain: 0.055,
                                dur: 0.46, atk: 0.22, type:"lowpass" });
      }
      else if (kind === "scour-moo"){
        /* THE COW. Rick, 2026-09-02: "lets also make sure our cow gets a good
           moo." Two falling tones a fifth apart with a wobble on the tail --
           a moo is a PITCH THAT SAGS, which is what separates it from a horn,
           and the wobble is the animal running out of breath. Quiet: she is
           thirty feet up and inside a tornado, and an easter egg that shouts
           stops being one the second time you hear it. */
        this._tone(t, { freq: 172, to: 128, gain: 0.115, dur: 0.62,
                        type:"sawtooth" });
        this._tone(t + 0.02, { freq: 258, to: 190, gain: 0.052, dur: 0.55,
                               type:"triangle" });
        this._tone(t + 0.30, { freq: 138, to: 116, gain: 0.070, dur: 0.46,
                               type:"sine" });
        this._burst(t + 0.30, { freq: 900, q: 0.8, gain: 0.030, dur: 0.30,
                                type:"bandpass" });
      }
      else if (kind === "ult"){
        const w = p.w;
        if (w === "duskreave"){
%CASTJS%
        } else'''),

# ---- 2. THE WINDOW STRIKES ITS OWN VOICE ------------------------------------
("hum", '''    T.cx = Math.max(lo, Math.min(hi, T.cx));

    /* ------------------------------------------------------------- THE CATCH''',
 '''    T.cx = Math.max(lo, Math.min(hi, T.cx));

    /* ------------------------------------------------------------- THE VOICE
       RE-STRUCK ON THE WINDOW'S OWN CLOCK. `T.hum` is decremented by `dt`
       inside `tickScour`, so it stops while the world is frozen exactly as the
       window does -- a cadence on a frame counter would drift against the
       thing it is describing every time somebody landed a blow.

       A HELD NOTE DOES NOT EXIST IN THIS TOOLKIT (CLAUDE.md 4.5), so ten
       seconds of standing tornado is 38 strikes at 0.26s and there is no
       other way to do it. `SFX.play` is a no-op headless and draws no
       randomness, so none of this reaches the sim. */
    T.hum -= dt;
    if (T.hum <= 0){ T.hum += %HOLDCAD%; SFX.play("scour-hold", { n: T.hums++ }); }

    /* THE WOOSH, ON ITS OWN CLOCK AND NOT THE BED'S. 1.15s against the bed's
       0.26 -- deliberately not a multiple, so the two layers drift against
       each other instead of locking into one repeating bar. A woosh that
       landed on every fourth wind strike would turn a floor into a rhythm,
       and this thing is supposed to sound like weather. */
    T.wsh -= dt;
    if (T.wsh <= 0){ T.wsh += 1.15; SFX.play("scour-woosh", { n: T.wshN++ }); }

    /* AND THE COW LOWS. Same seed test as the picture, so she is only ever
       heard in a fight she can be seen in -- a moo with no cow is a bug that
       would take somebody a long time to explain. Twice a window: once as she
       comes round the first time, once late. */
    if (T.moo >= 0){
      T.moo -= dt;
      if (T.moo <= 0){
        const cow = (() => { const x = Math.sin(this.seed * 0.61803398875
                                                * 127.1 + 311.7) * 43758.5453;
                             return x - Math.floor(x) < 0.125; })();
        if (cow) SFX.play("scour-moo", {});
        T.moo = T.mooN++ < 1 ? 4.6 : -1;
      }
    }

    /* ------------------------------------------------------------- THE CATCH'''),

# ---- 3. AND EVERY TICK IS HEARD ---------------------------------------------
("tickvoice", '''    T.dealt += Math.max(0, before - foe.hp);''',
 '''    T.dealt += Math.max(0, before - foe.hp);
    /* SEVEN A SECOND, AND THAT IS THE WHOLE QUESTION THE SPREAD ASKED. The
       tick carries no hit stop, no knock and no stagger by design, so the
       SOUND is most of what says a tick landed at all. */
    SFX.play("scour-tick", { n: T.ticks });'''),

# ---- 4. THE CAST CARRIES THE CLOCKS -----------------------------------------
("cast5c", '''                       cd: 0, dealt: 0, filed: 0, eaten: 0 };''',
 '''                       cd: 0, dealt: 0, filed: 0, eaten: 0,
                       hum: 0, hums: 0, moo: 1.1, mooN: 0,
                       wsh: 0.35, wshN: 0 };'''),

]


CASTJS = {'A1': '          [[0,300,0.10],[0.10,520,0.13],[0.20,820,0.15],\n           [0.30,1250,0.15],[0.40,1800,0.13],[0.50,2500,0.10]]\n            .forEach(([d,f,g]) =>\n              this._burst(t + d, { freq: f, q: 0.55, gain: g, dur: 0.34,\n                                   type:"bandpass" }));\n          this._tone(t + 0.44, { freq: 150, to: 46, gain: 0.34, dur: 0.85,\n                                 type:"sine" });\n          this._burst(t + 0.46, { freq: 220, q: 0.5, gain: 0.26, dur: 0.70,\n                                  type:"lowpass" });', 'A2': '          this._burst(t, { freq: 5200, q: 0.9, gain: 0.30, dur: 0.09,\n                           type:"highpass" });\n          this._burst(t + 0.01, { freq: 700, q: 0.6, gain: 0.32, dur: 0.34,\n                                  type:"bandpass" });\n          this._tone(t + 0.02, { freq: 320, to: 62, gain: 0.30, dur: 0.75,\n                                 type:"sawtooth" });\n          this._tone(t + 0.06, { freq: 214, to: 48, gain: 0.18, dur: 0.80,\n                                 type:"sawtooth" });\n          this._burst(t + 0.30, { freq: 180, q: 0.5, gain: 0.20, dur: 0.55,\n                                  type:"lowpass" });', 'A3': '          [[0,0.05],[0.12,0.08],[0.24,0.12],[0.36,0.17]].forEach(([d,g]) =>\n            this._burst(t + d, { freq: 900, q: 0.7, gain: g, dur: 0.30,\n                                 type:"bandpass" }));\n          this._burst(t + 0.50, { freq: 3000, q: 1.3, gain: 0.26, dur: 0.07,\n                                  type:"bandpass" });\n          this._tone(t + 0.52, { freq: 420, to: 54, gain: 0.32, dur: 0.90,\n                                 type:"triangle" });\n          this._burst(t + 0.54, { freq: 160, q: 0.5, gain: 0.24, dur: 0.80,\n                                  type:"lowpass" });'}
HOLDJS = {'B1': ('        const n = p.n || 0;\n        const w = 640 + Math.sin(n * 0.37) * 260 + Math.sin(n * 0.11) * 120;\n        this._burst(t, { freq: w, q: 0.42, gain: 0.085, dur: 0.42,\n                         type:"bandpass" });\n        this._burst(t, { freq: 190, q: 0.5, gain: 0.045, dur: 0.40,\n                         type:"lowpass" });\n        if (n % 5 === 0)\n          this._burst(t + 0.05, { freq: 2600, q: 1.5, gain: 0.020, dur: 0.05,\n                                  type:"bandpass" });', '0.26'), 'B2': ('        const n = p.n || 0, w = 1 + Math.sin(n * 0.9) * 0.014;\n        this._tone(t, { freq: 62 * w, to: 58 * w, gain: 0.090, dur: 0.34,\n                        type:"sawtooth" });\n        this._tone(t, { freq: 93 * w, to: 87 * w, gain: 0.042, dur: 0.30,\n                        type:"sawtooth" });\n        this._burst(t, { freq: 1400, q: 0.5, gain: 0.022, dur: 0.20,\n                         type:"bandpass" });', '0.16'), 'B3': ('        const n = p.n || 0, w = 1 + ((n * 29) % 5 - 2) * 0.005;\n        this._tone(t, { freq: 74 * w, to: 70 * w, gain: 0.105, dur: 0.72,\n                        type:"sine" });\n        this._tone(t, { freq: 222 * w, to: 214 * w, gain: 0.026, dur: 0.55,\n                        type:"triangle" });\n        if (n % 2 === 0)\n          this._burst(t, { freq: 520, q: 0.9, gain: 0.028, dur: 0.34,\n                           type:"bandpass" });', '0.44')}
TICKJS = {'C1': '        this._burst(t, { freq: 3200, q: 1.7, gain: 0.075, dur: 0.030,\n                         type:"bandpass" });\n        this._burst(t, { freq: 900, q: 1.1, gain: 0.030, dur: 0.026,\n                         type:"bandpass" });', 'C2': '        const n = p.n || 0;\n        this._burst(t, { freq: 2400, q: 1.4, gain: 0.055, dur: 0.022,\n                         type:"bandpass" });\n        this._tone(t, { freq: 1180 + (n % 3) * 90, to: 640, gain: 0.045,\n                        dur: 0.075, type:"triangle" });'}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=("1", "2", "3", "4", "5a", "5b", "5c"))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=BLADE)
    ap.add_argument("--charge", type=float, default=ULT_CHARGE)
    ap.add_argument("--cast", default="A1", choices=("A1", "A2", "A3"))
    ap.add_argument("--holdv", default="B1", choices=("B1", "B2", "B3"))
    ap.add_argument("--tickv", default="C1", choices=("C1", "C2"))
    for k, v in ULT.items():
        ap.add_argument(f"--{k}", type=float, default=v)
    A = ap.parse_args()

    if A.stage not in ("1", "2", "3", "4", "5a", "5b", "5c"):
        raise SystemExit(
            f"stage {A.stage} is not built yet. Stage 5 is the art, the sound\n"
            "  and the beat, and it is gated on Rick having SEEN the first two\n"
            "  (brief section 2, and CLAUDE.md rule 2).")

    src = A.src or {"1": "../02-chain/sc-bloodletting.html",
                    "2": "../02-chain/sc-duskreave.html",
                    "3": "../02-chain/sc-scour.html",
                    "4": "../02-chain/sc-grind.html",
                    "5a": "../02-chain/sc-scourwind.html",
                    "5b": "../02-chain/sc-duskmoon.html",
                    "5c": "../02-chain/sc-vortex.html"}[A.stage]
    out = A.out or {"1": "../02-chain/sc-duskreave.html",
                    "2": "../02-chain/sc-scour.html",
                    "3": "../02-chain/sc-grind.html",
                    "4": "../02-chain/sc-scourwind.html",
                    "5a": "../02-chain/sc-duskmoon.html",
                    "5b": "../02-chain/sc-vortex.html",
                    "5c": "../02-chain/sc-scourvoice.html"}[A.stage]
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
             "3": "IT CATCHES, DRAGS AND TICKS -- THIS IS THE RELIC",
             "4": "IT EATS PROJECTILES",
             "5a": "THE SILHOUETTE -- Cowork's `_scMoon`, Rick's pick",
             "5b": "THE FUNNEL -- built against Rick's own reference",
             "5c": "THE VOICE -- the cast, the hold, the tick and the MOO"}[A.stage])
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
    # THE ROUTING IS CHECKED, AND WHICH GRAMMAR IT POINTS AT CHANGES AT
    # STAGE 5a. Before it, `_scEaten` -- the shape Rick rejected on sight the
    # first time this relic ever drew it. After, `_scMoon`, which is Cowork's
    # redraw and his pick from a spread of four. Either is legitimate; NEITHER
    # is, if the dispatch has fallen through to the generic crescent, and no
    # measurement in this repo would say so.
    art = re.search(r'if \(key === "umbral"\)\s*return SHAPES\.(_sc\w+)', s0)
    if not art:
        raise SystemExit(
            "`SHAPES.scythe` does not route `umbral` anywhere. This relic is\n"
            "  the first umbral scythe in the game, so the routing has never\n"
            "  been exercised -- if it has fallen through, the silhouette that\n"
            "  ships is the generic crescent and nothing here would notice.")
    if A.stage == "5a" and art.group(1) != "_scEaten":
        raise SystemExit(
            f"stage 5a replaces `_scEaten` and this source already routes\n"
            f"  umbral to `{art.group(1)}` -- it has run. A stage applied twice\n"
            "  is how a builder writes numbers its own log does not describe.")
    print(f"  art   SHAPES.scythe routes umbral -> {art.group(1)}")

    table = {"1": S1, "2": S2, "3": S3, "4": S4, "5a": S5A,
             "5b": S5B, "5c": S5C}[A.stage]
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
                  .replace("%DRAG%", f"{A.drag:g}")
                  .replace("%CASTJS%", CASTJS[A.cast])
                  .replace("%HOLDJS%", HOLDJS[A.holdv][0])
                  .replace("%HOLDCAD%", HOLDJS[A.holdv][1])
                  .replace("%TICKJS%", TICKJS[A.tickv]))

    for label, old, new in table:
        s = one(s, fill(old), fill(new), label)

    # STRIPPED FIRST, because this check fired on its own explanation the
    # moment the cow's comment had to say the words `this.rng()` to explain why
    # it does not call it. `curse_check` and `curse_build` both did exactly this
    # on the same day in v53, and CLAUDE.md's note says it will keep happening
    # to anything that greps shipped source in a codebase that explains itself
    # in the file.
    if A.stage == "5b" and "this.rng()" in strip_comments(
            "".join(n for _, _, n in S5B)):
        raise SystemExit(
            "REFUSING TO WRITE -- the funnel draws from `this.rng()`. Breach's "
            "sparks\n  had to become DRAWN rather than spawned for exactly "
            "this reason: `spawnFx`\n  takes two draws per particle and would "
            "move every Duskreave fight.")

    if A.stage == "5a":
        s, at = cut_eaten(s)
        if not at:
            raise SystemExit("`_scEaten` is not in this source to delete")
        if "_scEaten" in strip_comments(s):
            raise SystemExit(
                "REFUSING TO WRITE -- `_scEaten` is still referenced after "
                "the cut. A dead grammar that still parses is one the next "
                "dispatch edit can route back to by accident.")
        if "_scMoon(c, L, W, p)" not in s:
            raise SystemExit("`_scMoon` did not land")
        print("  ok    _scEaten DELETED, 0 references remain")

    ult_matches(s, A, "4" if A.stage in ("5a", "5b", "5c") else A.stage)

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
    if A.stage == "5c":
        print(f"  voice: cast {A.cast}, hold {A.holdv} every "
              f"{HOLDJS[A.holdv][1]}s, tick {A.tickv} at {A.tick:g}/s, + the MOO")
        print("  the candidates are scour_sound_lab.py's VERBATIM -- a voice")
        print("    retyped between the audition and the build is a voice")
        print("    nobody chose")
        print("  the hold is re-struck on the WINDOW's clock, so it stops with")
        print("    the window through a hit stop (4.5: a held note does not")
        print("    exist in this toolkit)")
        print("  the moo fires on the SAME seed test as the cow, so a moo with")
        print("    no cow can never happen")
        print("\n  GATE 5c:")
        print("    python engine_ab.py --a ../02-chain/sc-vortex.html \\")
        print("      --b <out> --ids <all 33> --n 8")
        print("      IDENTICAL. `SFX.play` returns on its first line headless")
        print("      and draws no randomness, so sound in a tick loop is")
        print("      provably free -- which is what v42 never had.")
        return 0

    if A.stage == "5b":
        print("  the funnel: 11 stacked bands, a halo, near-black debris,")
        print("    a full-width floor pool and the lightning")
        print("  NO this.rng() ANYWHERE -- every phase is derived from T.t and")
        print("    an index, the way Breach's sparks had to be")
        print("  NO per-frame gradients -- flat fills under `lighter`, because")
        print("    nine createRadialGradient calls a frame is the named cause")
        print("    of the one stutter Rick has ever reported")
        print("\n  THE TAPER AND THE HIT BOX DISAGREE, AND THE POOL IS THE")
        print("  ANSWER: the reference funnel is NARROW AT THE FLOOR and the")
        print("  catch is full width at every height. The floor line and pool")
        print("  span the whole band, so the brightest thing in the picture")
        print("  states the real footprint. Watch for it reading as safe.")
        print("\n  GATE 5b:")
        print("    python engine_ab.py --a ../02-chain/sc-duskmoon.html \\")
        print("      --b ../02-chain/sc-vortex.html --ids <all 33> --n 8")
        print("      IDENTICAL. Presentation only, Duskreave's own pairings")
        print("      included -- that is what proves no rng was touched.")
        print("    python duskreave_sheet.py --scour --caught \\")
        print("      --game ../02-chain/sc-vortex.html")
        print("    THEN FILM IT. Rick has asked for the clip.")
        return 0

    if A.stage == "5a":
        print("  `_scMoon` pasted verbatim from 06-docs/v63/scmoon_spec.js,")
        print("    `_scEaten` DELETED, umbral routed to the moon")
        print("  RENDER-ONLY: SHAPES is not read by the sim, so engine_ab over")
        print("    all 33 is the cheapest proof this project has -- v58 got")
        print("    3024/3024 for the same class of change")
        print("\n  GATE 5a:")
        print("    python engine_ab.py --a ../02-chain/sc-scourwind.html \\")
        print("      --b ../02-chain/sc-duskmoon.html --ids <all 33> --n 8")
        print("      IDENTICAL, INCLUDING DUSKREAVE'S OWN PAIRINGS. A non-zero")
        print("      diff means the paste landed in the wrong scope.")
        print("    python silhouette_probe.py --game ../02-chain/sc-duskmoon.html \\")
        print("      --types scythe --sheet ../05-reference/v63/scythe-row-moon.png")
        print("      AND IT WILL NOW SEE THE GRAMMAR: the moon takes no")
        print("      destination-out bites, so nothing goes white-on-white and")
        print("      the row's IoU finally describes the shape it draws.")
        return 0

    if A.stage == "4":
        print("  enemy shots inside the band are removed, paying nothing")
        print("  RUNS BEFORE tickShots, which both moves and resolves -- the")
        print("    brief's 'do not let the eaten shot deal damage' is an")
        print("    ORDERING requirement and not a flag")
        print("  the mark is a RING, not spawnFx: `spawnFx` draws twice from")
        print("    this.rng() per particle and would move the stream")
        print("\n  GATE 4:")
        print("    python scour_probe.py --game ../02-chain/sc-scourwind.html \\")
        print("      --foes ironhail,widowmaker,marrowdraw,farwarden,gloamwire")
        print("      shots eaten > 0 against every bow")
        print("    python scour_probe.py --game ../02-chain/sc-scourwind.html \\")
        print("      --foes nightfell,heartwood,oathwound,axiom,grudgebearer")
        print("      shots eaten === 0 EXACTLY -- a greatsword and a warhammer")
        print("      loose nothing, so any eat at all is a bug in the owner test")
        print("    python engine_ab.py --a ../02-chain/sc-grind.html \\")
        print("      --b ../02-chain/sc-scourwind.html --ids <the 32> --n 8")
        return 0

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
