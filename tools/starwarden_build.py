#!/usr/bin/env python
"""STARWARDEN and CORONA -- the vigil twinblade, the 34th relic, SECOND design.

Built from `06-docs/v66/STARWARDEN-BUILD-BRIEF.md` (Cowork, 2026-09-03) and
`06-docs/v66/vigil-twinblade-design-v66.md`, which are the input and the only
input. Nothing in this file is a design decision: every number below is Rick's
or is measured, and the measured ones name the tool. CLAUDE.md section 3
rule 0.

    stage 1   the relic, its ultimate STUBBED        sc-minute -> sc-starwarden
    stage 2   the ring and the burn. No star
    stage 3   the star and the shower
    stage 4   the chain -- THE RELIC
    stage 5   THE ONE KNOB: the burn's per-stack damage, bisected
    stage 6   art, sound, beat, the carry

ARCLIGHT WAS THE FIRST DESIGN FOR THIS CELL AND RICK SCRAPPED IT BUILT.
`tools/arclight_build.py` still rebuilds it byte-identically from
`sc-lastthree` and four of its measurements outlive it (`06-docs/v64/
vigil-twinblade-CONSTRAINTS.md`); NOTHING ELSE of it survives, not the names.

THE BASE IS THE CHAIN TIP AND NOT THE BUILD OF RECORD. `sc-minute.html` is the
newest link -- 33 relics, the LAST-3 curse window, and the minute pace (baseHP
520, seals 27/64, timeout 156), which is the pace every number in `06-docs/v66/`
was priced on. THE CHAIN IS FORKED: Crossweave's stages 7-12 live in `sc-nova`
ONLY, which is what the app loads, and this branch does not have them. Named
here rather than settled here -- CLAUDE.md section 0.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "starwarden"

# ------------------------------------------------------------- the numbers --

# THE BLADE IS RICK'S AND IS NOT A BISECTION START. Design section 10 ruling 4:
# 8.3 -- Twinshade's, the twinblade row's floor -- over 7.0 and 9.5, and the
# design was priced whole on it (17.2% body -> 49.1% with Corona). v64's
# constraint 2 is why this is not the balance lever: the blade is worth about
# 13 points across its whole usable range once an ultimate carries the relic.
# THE ONE KNOB IS THE BURN'S PER-STACK DAMAGE (stage 5), not this.
BLADE = 8.3

ULT_NAME = "Corona"
ULT_KIND = "corona"         # its own kind. Nothing shares it -- one sigil, one
                            # sound, one picture.
ULT_CHARGE = 15.0

# RICK'S OWN LINE, 2026-09-03, trimmed twice WITH HIM to 67 against `verify`'s
# 72. Design section 11: his original was 78, he cut "burning" to "burn" and
# then took the drop of the second "damage" from three offered. Every word that
# ships is his, and it goes in at STAGE 1 because the brief's gate 1 asks the
# tip audit to see it.
ULT_TIP = "Ring and stars deal burn damage over time. Burn is gained as shield"

BLURB = ("A ring of light worn like a sash, and a star at the heart of it. "
         "Whatever touches either one goes on burning.")

# THE BURN'S OWN LINE IS NOT RICK'S YET. Brief section 4 item 2: offer three at
# stage 2; 40 characters is `verify`'s cap on a status tip. This is the
# placeholder and it is written in the house form -- effect clause, verb first,
# numbers real, "per stack" -- because a tip nobody has chosen still has to be
# a legal one, and the number in it is substituted from the shipped `dps` so a
# stage-5 bisection cannot leave the line describing the old relic (v40's card
# read "5s" after a sweep moved it to 8.1 and nothing caught it).
BURN_TIP = "Deals %BDPS% damage per second per stack"


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
    i = s.index('id:"' + rid + '"')
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
    for f in ("reach", "width", "artW", "spin", "mass", "mode"):
        m = re.search(r"\b" + f + r"\s*:\s*(\"[a-z]+\"|[\d.]+)", e)
        if m:
            out[f] = m.group(1)
    m = re.search(r"\bblades\s*:\s*\[([^\]]*)\]", e)
    if m:
        out["blades"] = "[" + re.sub(r"\s+", "", m.group(1)) + "]"
    return out


def fn_body(s: str, name: str) -> str:
    """One class method's body, by brace matching from its header.

    Used to ask a question of the SHIPPED function rather than of the insert
    that wrote it -- see the renderer check in `main`.
    """
    m = re.search(r"\n  " + re.escape(name) + r"\s*\([^)]*\)\s*\{", s)
    if not m:
        return ""
    j = s.index("{", m.start())
    depth, k = 0, j
    while k < len(s):
        if s[k] == "{":
            depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0:
                return strip_comments(s[j:k + 1])
        k += 1
    return ""


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
    want = {"name": '"' + A.ult + '"', "kind": '"' + ULT_KIND + '"'}
    if stage == "1":
        want["charge"] = "1e9"
    else:
        want["charge"] = f"{A.charge:g}"
        for k in ULT:
            want[k] = f"{getattr(A, k):g}"
    missing = [f"{k}:{v}" for k, v in want.items()
               if not re.search(r"\b" + re.escape(k) + r"\s*:\s*"
                                + re.escape(v) + r"\s*[,}]", blk)]
    if missing:
        raise SystemExit(
            "REFUSING TO WRITE -- the shipped `ult` block does not carry what "
            "this run printed:\n  missing " + ", ".join(missing)
            + "\n  (v56 shipped an ultimate whose numbers the log did not "
              "describe. Never again.)")


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will.

    CLAUDE.md 4.11. Every failure mode this builder can produce -- a stray
    comma between class methods, an unbalanced comment, a missing brace --
    lands as a TWENTY-SECOND PLAYWRIGHT TIMEOUT with no error text, which is
    indistinguishable from a slow machine and costs an afternoon.
    """
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        print("  WARN  no `node` on PATH -- output NOT syntax checked.")
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
                    + "\n  ".join(msg[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


# ------------------------------------------------------------------ stage 1 --

S1 = [

("relic", '''    blurb:"A hole in the floor of the world, turning. Whatever it catches, it keeps hold of long enough to finish." },

];''',
 '''    blurb:"A hole in the floor of the world, turning. Whatever it catches, it keeps hold of long enough to finish." },

  /* STARWARDEN -- THE VIGIL TWINBLADE, the thirty-fourth relic, and the fifth
     vigil. THE SECOND DESIGN FOR THIS CELL: Arclight and Static were built to
     `06-docs/v64/`, gated green, and scrapped whole by Rick on 2026-09-02
     after he watched them -- "i dont like what ive built. lets start over."
     Nothing of that relic survives here, not the names. What does survive is
     four measurements about the CELL (`v64/vigil-twinblade-CONSTRAINTS.md`)
     and this build is written against them.

     EVERY PHYSICAL STAT IS THE TWINBLADE'S, copied off Widowmaker,
     Spellbreaker, Twinshade and Thornshear -- the type owns
     `blades:[0,0.5], reach:62, width:8, artW:30, spin:5.7, mass:1.1,
     mode:"spin"` and there is no fifth set to invent. This builder asserts
     that against the shipped file before it writes rather than trusting this
     comment.

     `dmg` 8.3 IS RICK'S AND IS NOT A BISECTION START. Design section 10
     ruling 4, from three priced arms (7.0 / 8.3 / 9.5, reading 6% / 17% / 35%
     as a body with no ultimate at the minute pace): Twinshade's blade, the
     row's floor, and not under it. v64's second constraint is why nothing here
     tunes it -- once an ultimate carries a relic the blade is worth about
     thirteen points across its whole usable range. THE ONE KNOB IS THE BURN'S
     PER-STACK DAMAGE and it lands at stage 5.

     `onSelf:{ ward:1 }` is the school's channel, carried exactly as the three
     melee vigil relics carry it -- and it is load-bearing here in a way it is
     not anywhere else, because THE ULTIMATE PAYS INTO IT. Rick's third ruling
     (design section 8) is that the burn banks shield at the blade's own rate,
     so Corona is the first thing in this game whose STATUS TICKS feed a
     shield, and `resolveHit`'s vigil branch is the reference for how.

     THE BODY IS ALREADY STRONG AND THE ULTIMATE IS FITTED UNDER WHAT IS LEFT.
     Ward is the most weapon-speed-sensitive status in the game and this is the
     fastest weapon: measured at the minute pace, this body wins 17.2% at 8.3
     with no ultimate and 57% at the donor blade. Gate 1 has a number to hit --
     15-25%, not 10% and not 50%.

     THE ART IS ALREADY ON THE ROW AND HAS NEVER BEEN SEEN. `SHAPES.twinblade`
     routes `vigil` to `_tbPlated` and has since before this cell had anything
     in it, so this is the first relic that will ever draw it. It ships as the
     first cut and a redraw is a later, separate claim (brief section 4 item
     3) -- the umbral scythe's precedent. */
  { id:"starwarden", name:"Starwarden", aff:"vigil", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:%DMG%, spin:5.7, mode:"spin", mass:1.1,
    onSelf:{ ward:1 },
    /* CORONA. STUBBED AT `charge:1e9` IN STAGE 1 -- the same "OFF" the charge
       sweep in v55b used, and the same one Cindercleave's stage 1,
       Shroudmaul's stage 2, Gloamwire's stage 1, Bloodmirror's stage 1 and
       Duskreave's stage 1 used: the clock can never reach it, `fireUlt` never
       runs, and the relic is measured as a blade and a channel and nothing
       else.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       `kind:"corona"` IS ITS OWN AND SHARES WITH NOTHING. The twinblade row
       already carries `detonate` (Widowmaker), `sling` (Spellbreaker), `split`
       (Twinshade) and `winnow` (Thornshear); a fifth set-piece on one weapon
       type has to be separable by its sigil, its voice and its picture, and
       sharing a kind is how two relics quietly become one.

       THE CARD LINE IS RICK'S OWN AND IT IS IN AT STAGE 1, which is where this
       build differs from every other stubbed one. He wrote it, trimmed it
       twice himself, and it is 67 characters against `verify`'s 72 -- so there
       is nothing left to settle and no reason to ship a stub the tip audit
       cannot read. */
    ult:{ name:"%ULT%", charge:1e9, kind:"corona", tip:"%TIP%" },
    blurb:"%BLURB%" },

];'''),

]


# ------------------------------------------------------------------ stage 2 --

# EVERY NUMBER HERE IS THE BRIEF'S SECTION 0 TABLE, and the four composition
# rulings are Rick's of 2026-09-03 (design section 10): the 8-second window
# over 6, the ring at 120 x 42 band 24, 16 stars over 10 and 6, and the blade.
# Ruling 1 is `burn.maxStacks` 99 -- UNCAPPED, and it is the ruling everything
# else rests on: under a cap the ring and the shower substitute for each other
# and every look knob is inert, uncapped they ADD and the knobs are levers
# (design sections 6.1 and 9). Do not reintroduce a cap "for safety".
#
# THE SHOWER'S AND THE CHAIN'S NUMBERS ARE WRITTEN NOW AND ARE INERT UNTIL
# STAGES 3 AND 4. Bloodmirror's `strandW`/`strandKnock` precedent and
# Duskreave's `tick`/`dmg`, and the reason is v56: a stage-2 insert wrote a
# whole `ult` block, stage 3 rewrote one line of it, and the run LOGGED
# numbers the shipped relic did not carry. `ult_matches` refuses to write
# unless every number this run printed is in the block, so they go in together.
ULT = { "dur": 8.0,
        # the ring, fixed in the world and centred on the ball
        "A": 120.0, "B": 42.0, "wd": 24.0, "tilt": 0.45,
        "rate": 10.0, "tickDmg": 1.0, "entry": 1, "tickStacks": 1,
        # the shower -- stage 3
        "stars": 16, "sSpeed": 380.0, "sR": 12.0, "sGrace": 0.15,
        "mineBurn": 2, "knock": 600.0,
        # the chain -- stage 4
        "blast": 80.0, "gap": 0.07,
        # THE STAR'S SEAT IN THE RING -- PICTURE NUMBERS, read by `drawCorona`
        # and by nothing else. `starAt` is the ring's own parameter angle and 0
        # is the end of the major axis, which is the only seat of the four
        # offered that is unambiguously NOT on the ball: 108 units out against
        # a ball radius of 34. Rick's, from `corona_star_sheet.py`.
        "starAt": 0.0, "starR": 26.0 }

# THE BURN'S OWN TWO NUMBERS LIVE IN `STATUS`, NOT IN THE `ult` BLOCK, because
# it is a status and every other status in this game keeps its rate and its
# clock there.
#
# `dps` IS THE ONE KNOB THIS BUILD OWNS AND IT IS MEASURED, NOT FITTED.
# The design's placeholder was 0.10 and its own ladder (n=192, Chromium 141)
# put the band at 0.20 -- and said in as many words that a +15pp step for 0.05
# is a sample and not a curve. `corona_sweep.py`, on the PINNED runtime, both
# sides of every pairing, two seed blocks, 2112 fights a point:
#
#     0.120   45.7%      0.140   50.9%   (blocks 50.8 / 51.0)
#     0.130   49.4%      0.145   51.5%   (blocks 51.5 / 51.5)
#                        0.170   56.5%
#
# 0.14 IS A MEASURED ROW AND NOT AN INTERPOLATION, which is Cindercleave's
# rule. It is not the row nearest 50% -- 0.130 is, by 0.6pp against 0.9pp --
# and it is taken over that one because 0.130's two blocks came back 47.8% and
# 50.9%, a 3.1pp swing that is larger than the difference being decided, while
# 0.140 reproduces to two tenths of a point. THE HONEST PRECISION IS THE
# INTERVAL 0.130-0.145, every row of which is inside 1.5pp of even.
#
# AND THE DESIGN'S 0.20 IS NOT REFUTED BY THIS. Its own lab, UNMODIFIED, at its
# own settled settings, reads +25.9pp on this runtime against a published
# +31.9 -- CLAUDE.md 4.2b, and the reproduction control is in the build doc.
BURN_DPS = 0.14
BURN_DPS_DESIGN = 0.10          # the design's placeholder, kept for the record
BURN_DUR = 3.0
BURN_MAX = 99          # "uncapped" in this engine's terms -- see `apply`

S2 = [

# ---- 1. THE REAL ULT BLOCK --------------------------------------------------

("ult block",
 '''    ult:{ name:"%ULT%", charge:1e9, kind:"corona", tip:"%TIP%" },''',
 '''    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"corona",
          /* THE WINDOW. Rick, design section 10 ruling 3: eight seconds over
             six, cast every fifteen -- so the ring is up for more than half of
             a minute-long fight. Priced at +45.8pp against the 6s window's
             +34.9 before he chose, and the bisection compensates, so what the
             pick decides is what the relic is MADE of and not how strong it
             is. */
          dur:%DUR%,
          /* THE RING IS SATURN'S, and that is Rick's own correction to the
             first reading of his section 1: "its like the rings of saturn. a
             sash that floats off the body and extends beyond." A flat tilted
             band around the ball, floating clear of it, reaching well past it
             on both sides -- not an aura and not a bandolier hugging the
             shell.

             THE TEST IS AN ELLIPTICAL ANNULUS IN THE CASTER'S FRAME and the
             design's lab (`tools/ring_price.py`, `inRing`) is the reference
             implementation: `coronaRing` below is a port of it and not a
             rewrite, because every number in `06-docs/v66/` was measured
             through that function. A build that changes the test has to
             re-run the lab against itself.

             120 x 42 WITH A BAND OF 24 IS RICK'S (ruling 2), from three
             priced reaches -- 100x35 at +25.0, this at +34.9, 150x52 at
             +38.0. Uncapped, reach is a real lever rather than a picture:
             it buys dwell, dwell buys stacks, and stacks are the ultimate. */
          A:%A%, B:%B%, wd:%WD%, tilt:%TILT%,
          /* THE TICKS ARE A BRUSH AND THE BURN IS THE MECHANIC. Measured
             before anything was designed on it (`tools/sash_tracks.py`, 403
             windows): an enemy spends about two thirds of a second inside this
             band per cast, in four or five crossings. So "rapid tics" at 10/s
             is six or seven ticks a cast and 6 damage -- the ring is the FUSE.

             EVERY TICK ADDS A STACK. Rick's second ruling, from three offered
             (a sizzle, a stack per tick, a real bite): dwell feeds the burn,
             worth +8pp at the time it was priced. `entry` is the stack a
             crossing leaves on its own, which is the "left with a burn" half
             of his sentence -- the two are separate numbers because a fast
             crossing pays the entry and almost no ticks. */
          rate:%RATE%, tickDmg:%TICKDMG%, entry:%ENTRY%, tickStacks:%TICKSTACKS%,
          /* THE SHOWER. WRITTEN AND INERT UNTIL STAGE 3 -- v56's lesson: a
             stage that logs numbers it does not ship is how a build gets
             measured as something the log is not describing. */
          stars:%STARS%, sSpeed:%SSPEED%, sR:%SR%, sGrace:%SGRACE%,
          mineBurn:%MINEBURN%, knock:%KNOCK%,
          /* THE CHAIN. WRITTEN AND INERT UNTIL STAGE 4. */
          blast:%BLAST%, gap:%GAP%,
          /* AND THE STAR'S SEAT IN THE RING. PICTURE NUMBERS: `drawCorona`
             reads them and nothing else does, so they are provably inert in
             `engine_ab` -- which is the whole reason the placement can still
             be moved after the blade and the burn are settled. `starAt` is the
             ring's own parameter angle, 0 being the end of the major axis. */
          starAt:%STARAT%, starR:%STARR%,
          tip:"%TIP%" },'''),

# ---- 2. THE BURN ------------------------------------------------------------

("burn status",
 '''  blessing:   { name:"Blessing",   maxStacks:5, dur:6.0, hps:1.2,
                tip:"Heals 1.2 hp per second per stack" },''',
 '''  blessing:   { name:"Blessing",   maxStacks:5, dur:6.0, hps:1.2,
                tip:"Heals 1.2 hp per second per stack" },
  /* BURN -- CORONA's, and it is TWO firsts in one entry.

     IT IS UNCAPPED, which no other status here is. Rick's first ruling
     (design section 8), and it is the ruling the whole relic rests on: under a
     ceiling the ring and the shower compete for the same slots and SUBSTITUTE
     for one another -- (B-A) + (C-A) = 86 against a whole of 54 -- so star
     count, ring reach and the shower's aim are all pictures. Uncapped they
     ADD, 30.0 against a whole of 31.9, and every one of those becomes a lever.
     `maxStacks:99` rather than no cap at all because `apply` reads a number
     and every tool in `tools/` expects one; the peak measured on the settled
     design is 49. DO NOT REINTRODUCE A CAP "FOR SAFETY" -- it is not a safety,
     it is the relic.

     AND ITS TICKS FEED THE FIGHTER THAT APPLIED IT. Rick's third ruling: "the
     burn feeds the shield", at the blade's own rate. `feed` is the flag
     `tickStatus` reads; the SHARE is `STATUS.ward.bank` and not a number of
     its own, because "the blade's rate" is what he said and one source of
     truth is what stops the two drifting. That needs a SOURCE on the status,
     which nothing in this engine has ever had -- see `apply` and the fatal-tick
     beat, whose own comment predicted this day from the other direction.

     `dur` 3.0 IS "a few seconds" AND IT IS REFRESHED WHOLE on every
     application, which is what this engine does to any status: it expires as a
     whole rather than a stack at a time. At ~34 applications a cast the clock
     is effectively continuous while the window runs and the burn is what
     outlives it.

     `dps` IS THE ONE KNOB IN THIS BUILD (stage 5) and 0.10 is the design's
     placeholder, not a ruling -- section 9's ladder has a step between 0.15
     and 0.20 that n=192 cannot resolve. The tip's number is SUBSTITUTED from
     this line by the builder, so a bisection cannot leave the card describing
     the old relic (v40 shipped "5s" after a sweep moved it to 8.1). */
  burn:       { name:"Burn",       maxStacks:%BMAX%, dur:%BDUR%, dps:%BDPS%, feed:1,
                tip:"%BTIP%" },'''),

# ---- 3. THE WINDOW IS ON THE FIGHTER ----------------------------------------

("fighter state",
 '''    this.wireFade = 0;''',
 '''    this.wireFade = 0;
    /* THE RING, THE STAR AND THE SHOWER. `{t, dur, popped, inb, tickAcc,
       stars, chain, ...counters}` while CORONA's window is open, and null on
       every other relic and on this one outside it -- which is the whole
       zero-burden argument: `tickCorona` returns on its first line, `drawCorona`
       returns on its first line, and the one new clause in `tickCharge` is a
       comparison against null on a field nothing else writes.

       IT IS ON THE FIGHTER AND NOT ON `m.ultFx`, and that is v54 section 2a
       and chain-wide open item 25: `ultFx` is ONE SLOT, the opponent casting
       anything overwrites it, and a window ultimate's art was measured at 0.0%
       survival against Ironhail. A ring that is on screen for eight seconds
       cannot live in a field the other fighter can clear.

       THE SMALL STARS LIVE IN HERE TOO rather than beside `shots`. They are
       not arrows: they never expire, they ignore the ward, the parry and every
       other projectile, and only a touch or the chain removes them. Keeping
       them on the window is what makes "the leftovers" a list something can be
       built from when it shuts. */
    this.ultCorona = null;
    /* AND THE RING'S OWN FADE, because the window closing is not the same
       event as the picture of it ending. Same shape as `wireFade`,
       `graspFade`, `breachFade`, `deadfallFade` and `winnowFade`, and driven
       in `tickPresentation` for the reason they all give: a detonation sets
       `hitStop`, and a presentation clock on the normal path freezes for
       exactly the frames the viewer is staring hardest at. */
    this.coronaFade = 0;
    /* WHAT THE BURN HAS DEALT AND BANKED, FOR THIS FIGHTER, ALL FIGHT. Two
       plain accumulators rather than counters on the window, because the burn
       OUTLIVES the window it was applied in -- a cast's last stacks are still
       ticking three seconds after the ring has gone, and a counter that dies
       with the window would under-report exactly the part of the mechanic the
       design says is 94% of it. Read by `corona_relic_probe`; nothing in the
       simulation reads either. */
    this.burnDealt = 0;
    this.burnBanked = 0;'''),

# ---- 4. A STATUS CAN NOW SAY WHO APPLIED IT ---------------------------------

("apply source",
 '''  apply(key, n){
    const def = STATUS[key];
    if (!def) return;''',
 '''  /* `src` IS "a" OR "b" AND IT IS THE FIRST TIME A STATUS IN THIS GAME HAS
     KNOWN WHO APPLIED IT. The fatal-tick beat in `tickStatus` has carried the
     note for four versions -- "the day a third party can apply a bleed, this
     needs a source on the status" -- and CORONA is that day from the other
     direction: the burn does not need to know who to BLAME, it needs to know
     who to PAY. Optional and undefined at all 40-odd existing call sites, so
     every one of them is unchanged and `engine_ab` is the proof.

     A SIDE LETTER AND NOT A FIGHTER. A reference would put a live object graph
     inside a status the renderer snapshots every frame, and there are exactly
     two fighters that can apply this. Twinshade's shades cannot: nothing but
     Corona writes a source. */
  apply(key, n, src){
    const def = STATUS[key];
    if (!def) return;'''),

("apply store",
 '''    if (cur.stacks < cap) cur.stacks = Math.min(cap, cur.stacks + n);
    cur.t = def.dur;''',
 '''    if (cur.stacks < cap) cur.stacks = Math.min(cap, cur.stacks + n);
    cur.t = def.dur;
    /* THE LAST APPLIER OWNS THE POOL. One fighter can burn the other and this
       relic cannot fight itself, so "last" and "only" are the same thing here
       -- but it is written as a plain overwrite rather than a first-writer
       wins, because a status that remembered a dead applier would go on paying
       a shield to nobody. */
    if (src) cur.src = src;'''),

# ---- 5. THE BURN TICKS, AND ITS TICK PAYS A SHIELD --------------------------

("burn tick",
 '''      if (def.dps && key !== "blessing"){
        const hp0 = f.hp;
        f.hp -= def.dps * st.stacks * dt * f.dmgTakenMul();
        if (this.rng() < dt * 8){''',
 '''      if (def.dps && key !== "blessing"){
        const hp0 = f.hp;
        /* THE TICK IS A NAMED VALUE NOW BECAUSE SOMETHING ELSE READS IT. It
           was `f.hp -= ...` inline and the arithmetic is untouched; CORONA's
           burn banks a share of what it just dealt, so the damage has to exist
           as a number before it can be spent. `engine_ab` over the other 33 is
           the proof that this is the same subtraction. */
        const d = def.dps * st.stacks * dt * f.dmgTakenMul();
        f.hp -= d;
        /* AND THIS IS THE FIRST STATUS TICK IN THIS GAME THAT PAYS ANYBODY
           ANYTHING. Rick's third ruling (design section 8): the burn feeds the
           shield, at the blade's rate. So the share is `STATUS.ward.bank` --
           the same 0.55 `resolveHit`'s vigil branch uses -- and not a constant
           of its own, because "the blade's rate" is his sentence and two
           copies of a number are two numbers waiting to drift.

           SAME THREE WRITES, SAME ORDER, AS THE BLADE MAKES: the pool, its
           high-water mark, and the clock. DECLARED, because the brief leaves
           it to the build: EVERY BANKED TICK RESTARTS THE 5s WARD CLOCK, which
           is exactly what the design priced (`ring_price --feed-burn`), and it
           means a burning enemy keeps the caster's plate lit on its own.

           NO FLOAT AND NO TAG ON A TICK. A tick banks a fraction of a point
           and `resolveHit`'s "+n" would print nothing but zeroes a hundred
           times a second; what a viewer reads is the plate itself filling. The
           float on the BLADE's bank is untouched.

           `me !== f` IS NOT DEFENSIVE. It is the only thing standing between
           this and a fighter burning itself into an unbounded shield, and it
           costs one comparison on a path that is already only reached by one
           relic. */
        if (def.feed && st.src){
          const me = st.src === "a" ? this.a : this.b;
          me.burnDealt += d;
          if (me !== f && me.alive && !this.over){
            const W = STATUS.ward, b0 = me.shield;
            me.shield = Math.min(W.cap, me.shield + d * W.bank);
            if (me.shield > b0){
              me.shieldMax = Math.max(me.shieldMax, me.shield);
              me.apply("ward", 1);
              me.burnBanked += me.shield - b0;
            }
          }
        }
        if (this.rng() < dt * 8){'''),

("fatal tick source",
 '''        if (hp0 > 0 && f.hp <= 0){
          const src = f === this.a ? this.b : this.a;''',
 '''        if (hp0 > 0 && f.hp <= 0){
          /* AND THE ATTRIBUTION IS NO LONGER A GUESS FOR EVERY STATUS. The
             paragraph above says a status does not record who applied it and
             that the day a third party can apply one it will need a source.
             The burn HAS one, so it is used; hemorrhage and smite still fall
             back to "the other fighter", which is sound for them for the
             reason stated -- neither school has a summon. */
          const src = st.src ? (st.src === "a" ? this.a : this.b)
                             : (f === this.a ? this.b : this.a);'''),

# ---- 6. THE CAST ------------------------------------------------------------

("cast",
 '''    if (u.kind === "breach"){
      /* NOTHING RESOLVES HERE. The cast opens a LICENCE''',
 '''    if (u.kind === "corona"){
      /* NOTHING RESOLVES HERE AND NOTHING IS SPAWNED HERE EITHER. The cast
         puts a ring of light on the caster and a star on its body; everything
         the ultimate does happens because the OTHER fighter comes and touches
         one of them. There is no radius test, no nova and no damage on this
         frame -- which is also why a cast with the foe across the hall is
         worth nothing until it arrives.

         THE COUNTERS ARE THE GATE. `entries`, `ticks`, `stacks`, `ringF`,
         `spawned`, `touched`, `chained`, `chainHit` and `dmg` are what stages
         2-4 are read against: the design publishes ~5.6 crossings, ~0.82s of
         dwell, ~34 stacks, ~11 touched stars and ~3.4 chained per cast, and a
         build that misses those is a different relic no matter what its win
         rate says.

         `stars` AND `chain` ARE EMPTY UNTIL STAGE 3 and the fields exist now
         so the window's shape does not change under the probe that measures
         it. */
      f.ultCorona = { t: 0, dur: u.dur, popped: false, inb: false, tickAcc: 0,
                      stars: [], chain: [], next: 0, born: 0,
                      entries: 0, ticks: 0, stacks: 0, ringF: 0, dmg: 0,
                      pops: 0, spawned: 0, touched: 0, chained: 0,
                      chainHit: 0, refused: 0 };
      /* THE SET-PIECE'S CLOCK IS THE WINDOW'S, the way Aegis, the Thicket, the
         ballista, the Stasis Field, the Winnowing, the Sentinel, the tornado
         and the licence all set it at their own cast sites rather than from
         the `life` map. */
      if (this.ultFx) this.ultFx.life = u.dur;
      return;
    }
    if (u.kind === "breach"){
      /* NOTHING RESOLVES HERE. The cast opens a LICENCE'''),

# ---- 7. AND IT IS TICKED ----------------------------------------------------

("tick order",
 '''    this.tickScour(dt);
    this.tickBallista(dt);''',
 '''    this.tickScour(dt);
    /* WITH THE OTHER WINDOW TICKERS, and after the fighter loop that moved both
       balls -- the ring is centred on one shell and tested against the other,
       so a crossing resolved against last frame's positions is a crossing that
       did not happen. Before `tickHits` for the reason `tickWinnow`,
       `tickBreach` and `tickScour` all give.

       ON THE NORMAL STEP PATH AND NOT IN `tickPresentation`, which is the
       opposite of Deadfall's flash and Grasp's crush: the ring pays damage,
       the stars are hazards and the chain detonates, so all of it is the
       SIMULATION and has to freeze with everything else through a hit stop. */
    this.tickCorona(dt);
    this.tickBallista(dt);'''),

# ---- 8. THE TICKER ITSELF ---------------------------------------------------

("ticker",
 '''  tickScour(dt){
    const T = this.tornado;''',
 '''  /* ----------------------------------------------------------- THE CORONA ---
     Rick's section 1, clauses 1 and 2: for a duration the fighter wears a ring
     of light, and an enemy that enters it is burned for rapid ticks and left
     with a burn that goes on dealing damage for a few seconds. Clauses 3-6 --
     the star, the shower and the chain -- are stages 3 and 4 and are not here.

     THE RING IS THE FUSE AND THE BURN IS THE ULTIMATE. That is the design's
     first finding and it is worth restating where the code is: 94% of what
     this relic delivers is the burn, the ticks themselves are about six
     damage a cast, and the reason the ring matters at all is that every tick
     and every crossing puts another stack on a pool with no ceiling. */
  coronaRing(f, foe, u){
    /* A PORT OF `ring_price.py`'s `inRing`, DELIBERATELY LINE FOR LINE. Every
       decimal in `06-docs/v66/` -- the dwell, the crossing rate, the whole
       price -- was measured through that function, so a test that is merely
       equivalent is not good enough: it would silently re-price the relic and
       the design's table would no longer be judging this build.

       THE FOE IS IN THE BAND IF ITS DISC OVERLAPS IT, not if its centre does.
       Twelve points on the rim and the centre, which is thirteen samples of a
       disc whose radius is a third of the band's own width -- a centre-only
       test would let a ball pass clean through the band on a fast crossing and
       never be caught.

       `rho` IS THE ELLIPSE'S OWN RADIUS, so the band is an elliptical annulus
       and not a stroked outline: inside at `(A - wd) / A`, outside at 1. The
       tilt is FIXED IN THE WORLD -- it does not turn with the fighter or with
       the weapon, which is what makes the ring a thing the enemy learns the
       shape of rather than a thing that chases. */
    const R = CONFIG.physics.ballR;
    const dx = foe.x - f.x, dy = foe.y - f.y;
    const ca = Math.cos(u.tilt), sa = Math.sin(u.tilt), kin = (u.A - u.wd) / u.A;
    const px = dx * ca + dy * sa, py = -dx * sa + dy * ca;
    for (let k = 0; k <= 12; k++){
      const ang = k * Math.PI / 6, rr = k === 12 ? 0 : R;
      const rho = Math.hypot((px + rr * Math.cos(ang)) / u.A,
                             (py + rr * Math.sin(ang)) / u.B);
      if (rho <= 1 && rho >= kin) return true;
    }
    return false;
  }

  /* ONE PLACE THE BURN IS APPLIED FROM, and it is the only place in this
     engine that hands `apply` a source. The tag is fired on a CROSSING and on
     a star, never on a tick: at ten ticks a second a tag per stack would be a
     status name printed a hundred times over the quarry, and the count the
     viewer wants is the one already on the tag. */
  burnFoe(f, foe, n, tag){
    if (!foe.alive || n <= 0) return;
    foe.apply("burn", n, f === this.a ? "a" : "b");
    const C = f.ultCorona;
    if (C) C.stacks += n;
    if (tag){
      const first = !this.taught.burn && !!STATUS.burn.tip;
      if (first) this.taught.burn = true;
      this.statusTag(foe.x, foe.y, "burn", first, foe.stacks("burn"));
    }
  }

  tickCorona(dt){
    if (!this.a.ultCorona && !this.b.ultCorona) return;   // <- zero burden
    for (const f of [this.a, this.b]){
      const C = f.ultCorona;
      if (!C) continue;
      const foe = f === this.a ? this.b : this.a;
      const u = f.w.ult;
      C.t += dt;
      const open = C.t < C.dur && f.alive && !this.over;
      if (open){
        const now = foe.alive && this.coronaRing(f, foe, u);
        if (now){
          C.ringF++;
          /* THE CROSSING IS ITS OWN PAYMENT. "Enemy fighters who enter the
             ring ... are left with a burn": the entry stack is what a fast
             pass through the band leaves behind, and it is separate from the
             ticks because a crossing at speed collects almost none of them. */
          if (!C.inb){ C.entries++; this.burnFoe(f, foe, u.entry, true); }
          /* THE ACCUMULATOR CARRIES ITS FRACTION, so the rate is exact at any
             dt and does not drift with the timestep -- the spike storm's rule.
             It is RESET on leaving rather than kept, so a foe that brushes the
             band four times does not bank four part-ticks into a free one. */
          C.tickAcc += dt * u.rate;
          while (C.tickAcc >= 1){
            C.tickAcc -= 1; C.ticks++;
            /* THROUGH `hurt` AND NOT `resolveHit`, WHICH IS WHAT WAS PRICED
               and is declared in the design: the quarry's own ward absorbs it
               first, there is no crit, no jitter, no Sunder scaling and no
               beat. Routing it through `resolveHit` instead would bank ward on
               the tick as well -- measured at +0.5pp, inert at one damage a
               tick -- and would re-price the relic for nothing. */
            const hp0 = foe.hp + foe.shield;
            this.hurt(foe, u.tickDmg, f);
            C.dmg += hp0 - (foe.hp + foe.shield);
            this.burnFoe(f, foe, u.tickStacks, false);
          }
        } else C.tickAcc = 0;
        C.inb = now;
      }
      /* THE WINDOW ENDS AND, AT STAGE 2, SO DOES THE OBJECT. Stage 4 holds it
         open while the chain drains. A dead caster takes its ring with it --
         the burn it already applied does NOT go with it, because a burn is on
         the fighter that is burning and it has its own three seconds to run. */
      if (C.t >= C.dur || !f.alive || this.over) f.ultCorona = null;
    }
  }

  tickScour(dt){
    const T = this.tornado;'''),

# ---- 9. THE PICTURE'S CLOCK -------------------------------------------------

("fade",
 '''      f.wireFade = f.ultWire ? 1
                 : Math.max(0, f.wireFade - dt / 0.35);''',
 '''      f.wireFade = f.ultWire ? 1
                 : Math.max(0, f.wireFade - dt / 0.35);
      /* AND THE CORONA'S. Up instantly, down over 0.4s, so the ring dims
         rather than being switched off. HERE and not in `tickCorona` for
         v54's reason: a star's detonation sets `hitStop`, and a presentation
         clock on the normal path freezes for exactly the frames the viewer is
         staring hardest at. */
      f.coronaFade = f.ultCorona ? 1
                   : Math.max(0, f.coronaFade - dt / 0.4);'''),

# ---- 10. THE RING IS DRAWN --------------------------------------------------

("draw under",
 '''    /* the band is a hazard the balls are inside, so they are in front of it */
    if (__emit) this.drawScour(m, false);''',
 '''    /* the band is a hazard the balls are inside, so they are in front of it */
    if (__emit) this.drawScour(m, false);
    /* AND SATURN'S FAR SIDE PASSES BEHIND THE PLANET. The ring is drawn twice
       -- whole here, front half again over the shell -- and that split is the
       entire reason it reads as a ring around a body rather than as an ellipse
       painted on the floor. */
    if (__emit) this.drawCorona(m, false);'''),

("draw over",
 '''    /* and the band's own edges go over the balls, because inside them is
       caught and outside is not -- that boundary is the mechanic */
    this.drawScour(m, true);''',
 '''    /* and the band's own edges go over the balls, because inside them is
       caught and outside is not -- that boundary is the mechanic */
    this.drawScour(m, true);
    /* the near half of the ring, the star on the body, and the shower */
    this.drawCorona(m, true);'''),

("renderer",
 '''  drawScour(m, over){
    const T = m.tornado;''',
 '''  /* THE RING, AND IT IS A FIRST CUT. Rule 2: the ult animations are Rick's,
     and brief stage 6 says he sees them as a RENDERED SPREAD before he is
     asked anything in words. What is here is built to the two sentences that
     are already settled -- "an elliptical ring of neon light" and "like the
     rings of saturn ... a sash that floats off the body and extends beyond" --
     and every choice in it is a candidate rather than an answer.

     THE PICTURE IS THE HIT TEST AND NOTHING ELSE. `A`, `B` and `wd` are read
     off the same `ult` block `coronaRing` reads, and the inner ellipse is the
     annulus's own `(A - wd) / A` rather than a number that looks right --
     Cindercleave's constraint, where `half` IS the hit box and a jet drawn
     wider than it tests is a jet that looks like it connected and did not.

     NO `this.rng()`, EVER. A renderer that spends from the match's own stream
     moves every fight it draws (Breach's sparks had to become DRAWN rather
     than spawned for exactly this reason), so the shimmer below is a function
     of the window's own clock and of the index of the mark being drawn. */
  drawCorona(m, over){
    const A = m.a, B = m.b;
    if (!(A.ultCorona || A.coronaFade > 0 || B.ultCorona || B.coronaFade > 0))
      return;
    /* `this.ctx`, NOT `this.c`. v48: `_drawBeam` reached for a Match method
       from the Renderer and `drawUltUnder` handed a NaN to
       createRadialGradient, both green across 27 probe checks and a 280-match
       A/B, and both threw on the first rendered frame. */
    const c = this.ctx, P = AFFINITIES.vigil;
    for (const f of [A, B]){
      const C = f.ultCorona;
      if (!C && !(f.coronaFade > 0)) continue;
      const u = f.w.ult;
      if (!u || u.kind !== "corona") continue;
      /* THE WINDOW FADES AT BOTH ENDS rather than popping. A hazard that
         appears on a frame is one the viewer cannot anticipate, and this one
         is on screen for eight seconds and is a CONTACT hazard -- the whole
         mechanic is the enemy choosing to cross it. */
      const k = C ? Math.min(1, C.t / 0.30) * Math.min(1, (C.dur - C.t) / 0.45)
                  : f.coronaFade;
      if (k <= 0.001) continue;
      const ai = u.A - u.wd, bi = u.B * (u.A - u.wd) / u.A;
      const s0 = over ? 0 : -Math.PI, s1 = Math.PI;
      c.save();
      c.globalCompositeOperation = "lighter";
      /* THE BAND, FILLED. Not a stroked outline: a stroke of constant width is
         the wrong shape at the ends of an ellipse, and the thing being drawn
         is an annulus the enemy is either inside or outside of. */
      c.beginPath();
      c.ellipse(f.x, f.y, u.A, u.B, u.tilt, s0, s1);
      c.ellipse(f.x, f.y, ai, bi, u.tilt, s1, s0, true);
      c.closePath();
      c.globalAlpha = 0.30 * k;
      c.fillStyle = P.dark;
      c.fill();
      c.globalAlpha = 0.22 * k;
      c.fillStyle = P.core;
      c.fill();
      /* AND ITS TWO RIMS, WHICH ARE THE BOUNDARY THE MECHANIC IS MADE OF.
         `shadowBlur` is what makes a line read as neon and it is the most
         expensive thing in this method -- ONE pair of strokes carries it, not
         a pass per mark. Breach's art cost 14x the render time by putting a
         gradient inside a loop; this stays outside one. */
      c.shadowColor = P.glow; c.shadowBlur = 14;
      c.strokeStyle = P.glow; c.lineWidth = 2.4; c.globalAlpha = 0.95 * k;
      c.beginPath(); c.ellipse(f.x, f.y, u.A, u.B, u.tilt, s0, s1); c.stroke();
      c.beginPath(); c.ellipse(f.x, f.y, ai, bi, u.tilt, s0, s1); c.stroke();
      c.shadowBlur = 0;
      /* THE TRAVELLING LIGHTS. Saturn's rings are made of countable things and
         a flat band is not; these also say which way the ring is turning,
         which is the cheapest way to say the thing is alive rather than
         painted on. Their positions are a function of the window's clock and
         the mark's index -- no state, no random. */
      const N = 22, spin = (C ? C.t : 0) * 0.55;
      c.fillStyle = P.glow;
      for (let i = 0; i < N; i++){
        const th = spin + i * TAU / N;
        if (over && Math.sin(th) < 0) continue;
        if (!over && Math.sin(th) > 0) continue;
        const rr = 1 - 0.5 * (u.wd / u.A);
        const px = Math.cos(th) * u.A * rr, py = Math.sin(th) * u.B * rr;
        const ca = Math.cos(u.tilt), sa = Math.sin(u.tilt);
        c.globalAlpha = (0.35 + 0.45 * (0.5 + 0.5 * Math.sin(th * 3 + spin * 5))) * k;
        c.beginPath();
        c.arc(f.x + px * ca - py * sa, f.y + px * sa + py * ca, 2.1, 0, TAU);
        c.fill();
      }
      c.restore();
    }
  }

  drawScour(m, over){
    const T = m.tornado;'''),

# ---- 11. THE BURN IS DRAWN --------------------------------------------------

("status dispatch",
 '''    if ((n = f.stacks("hex")))        this._stHex(m, f, R, n);''',
 '''    if ((n = f.stacks("hex")))        this._stHex(m, f, R, n);
    if ((n = f.stacks("burn")))       this._stBurn(m, f, R, n);'''),

("status art",
 '''  _stWard(m, f, R){''',
 '''  /* BURN -- AND IT IS THE FIRST STATUS IN THIS GAME WITH NO CEILING TO DRAW
     AGAINST. Every other one here draws a mark a stack against a cap of four
     to six; this one peaks near fifty. Bloodmirror learned the general form of
     this the hard way -- `_stBleed` drew `Math.min(4, n)` drips, so eight
     stacks looked exactly like four and a whole mechanic had no representation
     on screen at all.

     SO THE COUNT IS CARRIED TWO WAYS AND NEITHER OF THEM IS "one mark a
     stack": the number of licks saturates at twelve, and everything else --
     their length, their brightness and the heat under the shell -- goes on
     climbing with `n`. The exact figure is on the status tag, which prints it.

     ORANGE ON A PINK CASTER'S QUARRY, and that is a first cut for Rick's
     spread (brief stage 6). Fire is warm in every reference there is, the
     victim can be any school, and vigil's own rose would read as the caster
     having painted the enemy rather than set it alight. The near-black
     outline is `_stSunder`'s rule and it is not optional -- a self-coloured
     mark on an arbitrary shell separates by VALUE or it does not separate. */
  _stBurn(m, f, R, n){
    const c = this.ctx;
    const HOT = "#FFC061", CORE = "#FF7A1F", EDGE = "#2A0C02";
    const heat = Math.min(1, n / 24);
    const N = Math.min(12, n);
    const t = m.t;
    c.save();
    /* THE SHELL IS HOT UNDER THE LICKS, which is what carries a count of forty
       when the licks themselves stopped counting at twelve. `lighter` over the
       ball, not a ring beside it. */
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = 0.10 + 0.30 * heat;
    c.fillStyle = CORE;
    c.beginPath(); c.arc(f.x, f.y, R * 0.96, 0, TAU); c.fill();
    c.globalCompositeOperation = "source-over";
    for (let i = 0; i < N; i++){
      /* NO `this.rng()`. The flicker is a function of the match clock and the
         lick's own index, so two replays of a seed draw the same fire. */
      const a = i * TAU / N + Math.sin(t * 0.7 + i) * 0.06;
      const wob = 0.5 + 0.5 * Math.sin(t * 9 + i * 2.1);
      const L = (7 + 5 * wob) * (0.7 + 0.5 * heat);
      const x0 = f.x + Math.cos(a) * (R + 1), y0 = f.y + Math.sin(a) * (R + 1);
      const x1 = f.x + Math.cos(a) * (R + 1 + L), y1 = f.y + Math.sin(a) * (R + 1 + L);
      const sx = Math.cos(a + 1.2) * 3 * (wob - 0.5);
      c.lineCap = "round";
      c.beginPath();
      c.moveTo(x0, y0);
      c.quadraticCurveTo((x0 + x1) / 2 + sx, (y0 + y1) / 2 + sx, x1, y1);
      c.lineWidth = 5.4; c.strokeStyle = EDGE; c.globalAlpha = 0.85;
      c.stroke();
      c.lineWidth = 3.0; c.strokeStyle = CORE; c.globalAlpha = 0.95;
      c.stroke();
      c.lineWidth = 1.3; c.strokeStyle = HOT; c.globalAlpha = 0.5 + 0.5 * wob;
      c.stroke();
    }
    c.restore();
  }

  _stWard(m, f, R){'''),

]


# ------------------------------------------------------------------ stage 3 --

S3 = [

# ---- 1. THE POP, THE SHOWER, AND WHAT A TOUCHED STAR PAYS -------------------

("ticker tail",
 '''        } else C.tickAcc = 0;
        C.inb = now;
      }
      /* THE WINDOW ENDS AND, AT STAGE 2, SO DOES THE OBJECT. Stage 4 holds it
         open while the chain drains. A dead caster takes its ring with it --
         the burn it already applied does NOT go with it, because a burn is on
         the fighter that is burning and it has its own three seconds to run. */
      if (C.t >= C.dur || !f.alive || this.over) f.ultCorona = null;''',
 '''        } else C.tickAcc = 0;
        C.inb = now;
        /* THE STAR, AND IT IS A BODY-TO-BODY CONTACT. Rick's clause 3: "if the
           enemy is hit by the star it explodes". The star sits ON THE BODY --
           his own "a small gap left for a large star in the middle" -- so
           being hit by it is the two shells touching, `2R + 2`, which is
           `ballCollision`'s own test with two units of slack so that a
           shoulder registers rather than only a dead-centre hit.

           ONCE A WINDOW. `popped` is on the window and not on the fighter: the
           star is what the ring is wearing, so it comes back with the next
           cast. Measured before anything was built on it
           (`tools/sash_tracks.py`): the first body contact of a window lands
           at a median 1.32s in 90% of windows, so nine casts in ten produce a
           shower and the tenth is a ring that nobody walked into. THAT IS THE
           MECHANIC and not a hole in it -- the same sentence Arclight's storm
           needed a spark for. */
        if (!C.popped && foe.alive && f.alive
            && Math.hypot(foe.x - f.x, foe.y - f.y)
               < 2 * CONFIG.physics.ballR + 2){
          C.popped = true; C.pops++;
          this.coronaPop(f, foe, C, u);
        }
      }
      /* THE SHOWER FLIES WHETHER THE WINDOW IS OPEN OR NOT, which is the lab's
         own rule and it is not an accident of implementation: the stars are
         what is LEFT of the ultimate, and clause 6 gives them their own
         ending. Until stage 4 builds that ending they simply go with the
         window. */
      if (C.stars.length) this.coronaFly(f, foe, C, u, dt);
      /* THE WINDOW ENDS AND, AT STAGE 3, SO DOES THE OBJECT. Stage 4 holds it
         open while the chain drains. A dead caster takes its ring with it --
         the burn it already applied does NOT go with it, because a burn is on
         the fighter that is burning and it has its own three seconds to run. */
      if (C.t >= C.dur || !f.alive || this.over) f.ultCorona = null;'''),

# ---- 2. THE THREE METHODS --------------------------------------------------

("shower",
 '''  tickCorona(dt){
    if (!this.a.ultCorona && !this.b.ultCorona) return;   // <- zero burden''',
 '''  /* SIXTEEN STARS, WHICH IS RICK'S (design section 10 ruling 1) OVER TEN AND
     SIX. Uncapped, star count stopped being a look knob and became the biggest
     lever on the roster: 6 stars price at +23.4, 10 at +34.9, 16 at +44.3, and
     the share of the fire coming from the shower goes 35% -> 50% -> 60%. He
     took the dense shower, so THE RING IS THE FUSE AND THE SHOWER IS THE
     ULTIMATE, and the bisection at stage 5 pays for it.

     THE ANGLES COME FROM THE MATCH'S OWN SEEDED STREAM. `Math.random` here
     would break `engine_ab` silently -- the page runs, the fight looks right,
     and two runs of one seed differ -- and every recorded number in this repo
     rests on a seed naming a fight. */
  coronaPop(f, foe, C, u){
    for (let i = 0; i < u.stars; i++){
      /* THE CEILING IS DECLINED, NOT SHIFTED. `CONFIG.shot.maxLive` is 64 and
         it is SHARED with whatever the foe has in the air -- `spawnShot`
         shifts the oldest entry out when it is reached, and doing that from
         inside a loop that is also iterating would move every index under the
         iterator (Thornshear's fork learned it). Sixteen stars is well inside
         64; a bow foe's volley is not accounted for, which is exactly why this
         has to be here and why `refused` is printed. */
      if (this.shots.length + C.stars.length >= CONFIG.shot.maxLive){
        C.refused++; break;
      }
      const a = this.rng() * TAU;
      C.stars.push({ x: f.x, y: f.y, vx: Math.cos(a) * u.sSpeed,
                     vy: Math.sin(a) * u.sSpeed, born: C.t, n: ++C.born });
      C.spawned++;
    }
    /* THE POP IS A BEAT, AND IT HAS TO BE ONE. CLAUDE.md section 3 rule 3: an
       ultimate that does something `cinePlan` cannot see has its best moment
       scored as empty air. The cast files a beat 1-8 seconds earlier and the
       shower is the picture -- so the pop files its own, and the chain's first
       detonation files another at stage 4.

       A RING AND A SHAKE AND NOTHING ELSE. `spawnFx` draws twice from
       `this.rng()` per particle, so a debris field here would move every
       Starwarden fight and re-invalidate the blade the moment anybody adjusted
       the art -- Breach's sparks had to become DRAWN rather than spawned for
       exactly this reason. `ring` and `shake` are presentation lists nothing
       in the simulation reads. */
    this.ring(f.x, f.y, f.aff.core, 10, 104, 0.5, 5);
    this.shake = Math.max(this.shake, 14);
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: f.x, y: f.y,
                w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
  }

  /* A SMALL STAR IS NOT AN ARROW, and that is why it is not in `shots`. It
     never expires, it is not parried, it does not clank, no ward absorbs it
     and the caster walks through it. Only a touch or the chain removes one. */
  coronaFly(f, foe, C, u, dt){
    const A = CONFIG.arena, n = this.inset, R = CONFIG.physics.ballR;
    const lo = n + u.sR, hiX = A.w - n - u.sR, hiY = A.h - n - u.sR;
    for (let i = C.stars.length - 1; i >= 0; i--){
      const s = C.stars[i];
      s.x += s.vx * dt; s.y += s.vy * dt;
      /* THE WALLS ARE THE CURRENT INSET AND NOT THE ARENA. v64's third
         measurement, and it is the one that made the last attempt at this cell
         unmeasurable: `storm_price` bounced its swarm off `P.rb` while the
         engine's own projectiles use `n = this.inset`, which the seals walk
         0 -> 140. In the open hall the two agree; once the hall closes the lab
         was five times wrong. ANYTHING PLACED IN THIS ROOM CLOSES WITH IT.

         REFLECTED ABOUT THE WALL rather than clamped to it, so a star keeps
         the distance it travelled this frame. The clamp after it is for the
         one case reflection cannot handle -- a wall that has closed PAST a
         star since the last frame, where the reflection would put it outside
         the other wall. */
      if (s.x < lo){ s.x = 2 * lo - s.x; s.vx = -s.vx; }
      else if (s.x > hiX){ s.x = 2 * hiX - s.x; s.vx = -s.vx; }
      if (s.y < lo){ s.y = 2 * lo - s.y; s.vy = -s.vy; }
      else if (s.y > hiY){ s.y = 2 * hiY - s.y; s.vy = -s.vy; }
      s.x = Math.min(hiX, Math.max(lo, s.x));
      s.y = Math.min(hiY, Math.max(lo, s.y));
      /* THE GRACE IS WHY A SHOWER IS NOT AN EXPLOSION. Every star is born
         inside the caster's own shell, and the foe is by definition touching
         that shell -- that is what popped the star. Without it all sixteen
         detonate on the frame they are born and the ultimate is a nova.
         0.15s at 380 px/s is 57 units of travel. */
      if (foe.alive && !this.over && C.t - s.born > u.sGrace
          && Math.hypot(foe.x - s.x, foe.y - s.y) < R + u.sR){
        C.stars.splice(i, 1);
        this.coronaBoom(f, foe, C, u, s, true);
      }
    }
  }

  /* WHAT A STAR PAYS. Rick's clause 4 -- "if an enemy hits one of the stars it
     detonates, dealing damage over time and knocking them back" -- and BOTH
     halves of that sentence are his rulings elsewhere: the damage over time is
     `mineBurn` stacks of the burn (there is no instant damage anywhere in this
     ultimate), and the knock is 600, which he took over 300 and 150 because
     "stars read as bombs". Measured, 0 / 300 / 600 all land inside one SE of
     each other, so it is a LOOK choice made on the picture rather than a
     balance number -- which is the only reason it was his to make.

     FOE ONLY. The caster passes through its own shower: `coronaFly` only ever
     tests the foe. The roster precedent is quarry-only (no Deadfall mine has
     ever been set off by a copy) and a hazard that catches its own caster is a
     different relic. */
  coronaBoom(f, foe, C, u, s, touched){
    const R = CONFIG.physics.ballR;
    const dx = foe.x - s.x, dy = foe.y - s.y, d = Math.hypot(dx, dy) || 1;
    const hit = foe.alive && !this.over && (touched || d < R + u.blast);
    if (hit){
      this.burnFoe(f, foe, u.mineBurn, true);
      /* ALONG THE STAR'S TRAVEL FOR A TOUCH, AWAY FROM THE BLAST FOR A CHAINED
         ONE -- the kunai's rule. `resolveHit`'s knock fires away from the
         CASTER, and a hazard that is not the caster needs its own bearing or
         the shove reads as coming from the wrong place (the Thicket, then
         Breach). */
      const vl = Math.hypot(s.vx, s.vy) || 1;
      const kx = touched ? s.vx / vl : dx / d;
      const ky = touched ? s.vy / vl : dy / d;
      /* ON A LIVE, UNPINNED FOE. A pinned ball is held by something else and
         adding velocity to it would be banked and released later, which is the
         v43 bug this engine has already fixed once. */
      if (foe.pin <= 0){ foe.vx += kx * u.knock; foe.vy += ky * u.knock; }
    }
    this.ring(s.x, s.y, f.aff.glow, 3, touched ? 46 : u.blast * 0.8,
              0.30, 3.5);
    /* THE COUNT IS OF THE DETONATION AND NOT OF THE PAYMENT, which is what
       makes `spawned = touched + chained + alive` an invariant a probe can
       assert. A star that goes off next to a corpse still went off. */
    if (touched) C.touched++; else { C.chained++; if (hit) C.chainHit++; }
  }

  tickCorona(dt){
    if (!this.a.ultCorona && !this.b.ultCorona) return;   // <- zero burden'''),

# ---- 3. AND THEY ARE DRAWN --------------------------------------------------

("star art",
 '''      c.restore();
    }
  }

  drawScour(m, over){''',
 '''      /* THE STAR ON THE BODY, and Rick's "a small gap left for a large star
         in the middle" is what the gap in the band is FOR. It is drawn in the
         over pass only -- it sits on the shell, and a star behind the ball is
         not a star anybody can be hit by. `_sparkStar` is the game's own star
         path, shared with the banner, so the thing that pops is recognisably
         the thing that was sitting there. */
      if (over && C && !C.popped){
        const pul = 1 + 0.06 * Math.sin(C.t * 7.5);
        c.save();
        c.translate(f.x, f.y);
        c.globalAlpha = 0.95 * k;
        c.shadowColor = P.glow; c.shadowBlur = 16;
        c.fillStyle = P.core;
        this._sparkStar(c, 17 * pul, 0.34);
        c.fill();
        c.shadowBlur = 0;
        c.globalAlpha = 0.9 * k;
        c.fillStyle = "#FFFFFF";
        this._sparkStar(c, 7.4 * pul, 0.30);
        c.fill();
        c.restore();
      }
      /* AND THE SHOWER. Over the balls, because a star the enemy is about to
         walk into cannot be behind them.

         NO `shadowBlur` PER STAR. Sixteen of them at up to two shells' worth
         of glow is the fault Breach's jets shipped with -- nine gradients a
         frame took the capture to 0.19 frames a second, and `shadowBlur` on 64
         sparks was the other half of it. A flat disc under `lighter` is the
         same picture at arena scale and costs nothing. */
      if (over && C && C.stars.length){
        c.save();
        c.globalCompositeOperation = "lighter";
        for (const s of C.stars){
          const age = C.t - s.born;
          /* BORN BRIGHT AND SETTLING, which is the only thing on screen that
             says these are what the star broke into. A function of the star's
             own clock -- no state, no `this.rng()`. */
          const pop = age < 0.22 ? 1 + 1.4 * (1 - age / 0.22) : 1;
          c.globalAlpha = 0.30 * k;
          c.fillStyle = P.core;
          c.beginPath(); c.arc(s.x, s.y, u.sR * 1.7 * pop, 0, TAU); c.fill();
          c.save();
          c.translate(s.x, s.y);
          c.rotate(Math.atan2(s.vy, s.vx));
          c.globalAlpha = 0.95 * k;
          c.fillStyle = P.glow;
          this._sparkStar(c, u.sR * pop, 0.36);
          c.fill();
          c.globalAlpha = 0.85 * k;
          c.fillStyle = "#FFFFFF";
          this._sparkStar(c, u.sR * 0.42 * pop, 0.30);
          c.fill();
          c.restore();
        }
        c.restore();
      }
      c.restore();
    }
  }

  drawScour(m, over){'''),

]


# ------------------------------------------------------------------ stage 4 --

S4 = [

("chain",
 '''      if (C.stars.length) this.coronaFly(f, foe, C, u, dt);
      /* THE WINDOW ENDS AND, AT STAGE 3, SO DOES THE OBJECT. Stage 4 holds it
         open while the chain drains. A dead caster takes its ring with it --
         the burn it already applied does NOT go with it, because a burn is on
         the fighter that is burning and it has its own three seconds to run. */
      if (C.t >= C.dur || !f.alive || this.over) f.ultCorona = null;''',
 '''      if (C.stars.length) this.coronaFly(f, foe, C, u, dt);
      /* THE CHAIN. Rick's clause 6, and it is the only clause in his section 1
         that is pure picture: "after a duration the leftover stars detonate
         anyways, not all at once, in a chain reaction like effect from one end
         of the arena to the other."

         ORDERED BY `y`, TOP OF THE HALL FIRST, one every `gap`. With sixteen
         stars and three or four left standing it runs for about a quarter of a
         second. Measured and DECLARED INERT: the chain lands a blast on the
         enemy in a third of casts at `blast` 80 and half at 130, and the win
         rate does not move either way -- so its radius is a look number and
         the design says so in as many words.

         THE QUEUE IS BUILT ONCE, on the frame the window's clock passes `dur`,
         and the window object OUTLIVES ITS OWN WINDOW until the queue drains.
         That is what "the leftovers" means: the ring is gone, the ticks have
         stopped, and the last of the shower is still going off. */
      if (C.t >= C.dur && C.stars.length){
        C.stars.sort((p, q) => p.y - q.y);
        C.chain = C.stars.map((s, i) => ({ s, at: C.t + i * u.gap }));
        C.stars = [];
      }
      while (C.chain.length && C.chain[0].at <= C.t){
        const q = C.chain.shift();
        this.coronaBoom(f, foe, C, u, q.s, false);
      }
      /* AND THE OBJECT GOES WHEN THE LAST ONE HAS. A dead caster takes the
         whole thing with it, leftovers included -- sixteen stars still
         bouncing over a corpse is not a final image, it is a thing nobody
         turned off, and the same clause is why Scour's band and Arclight's
         swarm are cleared on `over`. The burn it already applied does NOT go
         with it, because a burn is on the fighter that is burning and it has
         its own three seconds to run. */
      if ((C.t >= C.dur && !C.chain.length) || !f.alive || this.over)
        f.ultCorona = null;'''),

("first chained beat",
 '''    if (touched) C.touched++; else { C.chained++; if (hit) C.chainHit++; }''',
 '''    /* THE CHAIN'S FIRST DETONATION FILES A BEAT, and only its first. Rule 3
       again: the finale is the last thing this ultimate does and `cinePlan`
       would otherwise score it as empty air -- but a beat per star would file
       four inside a quarter of a second and hand the director a cut made of
       one picture. */
    if (!touched && C.chained === 0)
      this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: s.x, y: s.y,
                  w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
    if (touched) C.touched++; else { C.chained++; if (hit) C.chainHit++; }'''),

("cast waits",
 '''    f.charge += dt;
    if (f.charge >= f.w.ult.charge){ f.charge = 0; this.fireUlt(f, foe); }''',
 '''    f.charge += dt;
    /* AND A CAST WAITS FOR THE LAST ONE'S CHAIN TO FINISH. `f.ultCorona` is
       null on every other relic and on this one outside its own window, so
       this is a comparison against null on a field nothing else writes --
       `engine_ab` over the other 33 is the proof.

       IT CANNOT BIND AT THE SHIPPED NUMBERS and it is here anyway. The window
       is 8 seconds and the charge is 15, so the chain has drained six seconds
       before the clock comes round; the probe reports the count and it is
       zero. What it stops is the state the design names -- a cast that starts
       under a running chain, which is two set-pieces on one screen -- if any
       of those three numbers ever moves. THE CHARGE IS NOT SPENT while it
       waits, so the cast lands on the frame the last star goes off. */
    if (f.charge >= f.w.ult.charge && !f.ultCorona){
      f.charge = 0; this.fireUlt(f, foe);
    }'''),

]


# ------------------------------------------------------------------ stage 6 --
# AND IT GETS A PARTICLE FIELD, IN BOTH COPIES OR IN NEITHER.
# `ULTFX.sync` RETURNS SILENTLY on a missing spec -- it is not an error, which
# is exactly why it ships -- and `SPECS` carries 31 entries today with NO
# `ravelbone` and NO `gloamwire` (open item 46). A spec added only to the page
# is one the next `fx_build` run drops; a spec added only to the module is one
# this build never shows.
#
# THE NUMBERS IN IT ARE ART AND ARE THEREFORE A FIRST CUT FOR RICK'S SPREAD.
# What is NOT a judgement call is the mode and where it is drawn: only `burst`
# is drawn at the quarry, so a `swirl` needs no `atSelf` and lands on the
# caster, which is where this ultimate happens.
#
# AND IT IS THE CAST'S FLOURISH, NOT THE WINDOW. The field is drawn at
# `[u.x, u.y]` -- the caster's position AT THE CAST -- so a field with an
# eight-second life would drift off the fighter it belongs to. Shroudmaul's
# spec says the same thing about its own window and Cindercleave's about its
# licence: the seconds after the cast are a DRAWN OBJECT, not a particle field.
FX_SPEC = """,
    /* THE RING LIGHTING, AND IT IS THE CAST AND NOT THE WINDOW. `swirl` is
       already drawn at `[u.x, u.y]` -- only a `burst` goes to the quarry --
       so this one needs no `atSelf`, and it is SHORT because the eight
       seconds after it are a drawn ring, a drawn star and sixteen drawn
       stars rather than a field.

       IT TURNS AND IT DOES NOT FALL. `grav` is barely negative and `drag` is
       low, so what a viewer reads is material taking up an ORBIT around the
       shell -- which is the one thing the ring has to say in the half second
       before anybody has walked into it. Vesper's spec is the reference: the
       other vigil relic whose ultimate is a thing that then STANDS. */
    starwarden: { mode: 'swirl', n: 1150, sp: [70, 230], grav: -12, drag: 0.85,
                  life: [0.40, 1.25], heavy: 0.0, size: [0.6, 2.0],
                  spawn: 0.28, up: 0 }"""

FX_ANCHOR = """                   size: [0.8, 2.4], spawn: 0.06, up: 20, atSelf: 1 }
  };"""


# ---- AND THE LARGE STAR IS REDRAWN, BECAUSE RICK COULD NOT SEE IT ----------
# 2026-09-03, off the first rendered window: "looking good. i cant see the
# large star in the ring though." CLAUDE.md 4.1 -- the deliverable is a
# MEASUREMENT of the thing he saw, and `corona_star_probe.py` is it. Measured
# on the first cut: the star stands 2.72s of a 9.26s window (29% -- so it is
# NOT a duration problem), and its brightest pixel moves the picture by
# |dL| 0.167 with a mean of 0.017 over its own footprint.
#
# THREE FAULTS AT ONCE, and every one of them is a rule this repo already had:
#   1. it was drawn inside `drawCorona`'s `lighter` block, so it ADDED pink
#      light to an already-bright pink shell -- section 4.1b, twice before
#   2. radius 17 against `ballR` 34, so it sat entirely inside the ball's disc
#   3. `P.core` on a vigil relic is the ball's own hue -- and `_stWard`'s
#      docstring says it in capitals: A SELF-BUFF MUST SEPARATE BY VALUE, NOT
#      BY HUE. This is the second self-coloured mark on a vigil ball and it
#      made the same mistake.
S6_STAR = [

("the star, redrawn",
 '''      if (over && C && !C.popped){
        const pul = 1 + 0.06 * Math.sin(C.t * 7.5);
        c.save();
        c.translate(f.x, f.y);
        c.globalAlpha = 0.95 * k;
        c.shadowColor = P.glow; c.shadowBlur = 16;
        c.fillStyle = P.core;
        this._sparkStar(c, 17 * pul, 0.34);
        c.fill();
        c.shadowBlur = 0;
        c.globalAlpha = 0.9 * k;
        c.fillStyle = "#FFFFFF";
        this._sparkStar(c, 7.4 * pul, 0.30);
        c.fill();
        c.restore();
      }''',
 '''      if (over && C && !C.popped){
        /* OUT OF `lighter`, BIGGER THAN THE BALL, AND OUTLINED IN THE DARK.
           Rick, off the first rendered window: "i cant see the large star in
           the ring though." Measured before it was touched
           (`corona_star_probe.py`): it stood for 29% of its own window, so it
           was never a duration problem -- its brightest pixel moved the
           picture by 0.167 and its mean by 0.017, which is a slight warming
           of a shell that was already that colour.

           `source-over` AND NOT `lighter`, which is the whole of it. The band
           above wants `lighter` -- it is light in the air. The star is an
           OBJECT ON A BODY, and adding it to a bright shell of its own hue is
           section 4.1b for the third time in this project: the ball is not
           lit, the mark is erased.

           SIZED AGAINST THE BALL AND NOT IN PIXELS. `ballR` is 34 and the
           first cut drew 17, so the whole star fitted inside the disc it was
           supposed to be sitting on. At 1.02R its points cross the rim, which
           is what makes it read as worn rather than as a marking.

           AND IT IS OUTLINED IN THE SCHOOL'S DARK BEFORE IT IS FILLED.
           `_stWard` has said why since the ward shipped, in capitals: A
           SELF-BUFF MUST SEPARATE BY VALUE, NOT BY HUE -- every ward plate
           gets a near-black outline first, because a rose mark on a rose ball
           has no contrast at all. This is the second self-coloured mark on a
           vigil ball in the game and it had to learn the same thing.

           STILL A FIRST CUT IN EVERY OTHER RESPECT. Rule 2: the animations
           are Rick's, from a spread. */
        const R0 = CONFIG.physics.ballR;
        const pul = 1 + 0.05 * Math.sin(C.t * 7.5);
        c.save();
        c.globalCompositeOperation = "source-over";
        c.translate(f.x, f.y);
        c.globalAlpha = k;
        c.lineJoin = "round";
        this._sparkStar(c, R0 * 1.02 * pul, 0.32);
        c.lineWidth = 7; c.strokeStyle = P.dark; c.stroke();
        c.shadowColor = P.glow; c.shadowBlur = 20;
        c.fillStyle = P.core; c.fill();
        c.shadowBlur = 0;
        /* the hot centre, which is the only white in the whole relic and is
           what survives the phone screen once the bloom has had it */
        c.fillStyle = "#FFF3FA";
        this._sparkStar(c, R0 * 0.44 * pul, 0.28);
        c.fill();
        c.restore();
      }'''),

]


# ---- AND THEN THE STAR MOVED OFF THE BALL AND INTO THE RING ----------------
# Rick, 2026-09-03, on the second rendered window: "the star should live within
# the ring. not the ball."
#
# HIS SECTION 1 SAID SO FROM THE START AND TWO CUTS OF THIS BUILD MISSED IT:
# "an elliptical ring of neon light WITH A SMALL GAP LEFT FOR a large star in
# the middle." The band is BROKEN and the star is what the break is for. Drawn
# on the shell instead, the gap was decorative and the star was a marking.
#
# THE PLACEMENT IS HIS AND IT IS A SPREAD, NOT A GUESS (rule 2). `starAt` is
# the ring's own parameter angle and `corona_star_sheet.py` photographs four of
# them off one real frame. The default is the end of the major axis, which is
# the only one of the four that is unambiguously NOT on the ball: 108 units out
# against a ball radius of 34.
S6_GAP = [

("the gap in the band",
 '''      const ai = u.A - u.wd, bi = u.B * (u.A - u.wd) / u.A;
      const s0 = over ? 0 : -Math.PI, s1 = Math.PI;
      c.save();
      c.globalCompositeOperation = "lighter";''',
 '''      const ai = u.A - u.wd, bi = u.B * (u.A - u.wd) / u.A;
      /* THE GAP IN THE BAND, AND THE STAR THAT LIVES IN IT. Rick, on the
         second rendered window: "the star should live within the ring. not the
         ball." His own section 1 had said it -- "an elliptical ring of neon
         light WITH A SMALL GAP LEFT FOR a large star in the middle" -- and two
         cuts of this build drew the star on the shell instead, which made the
         gap decorative and the star a marking on a relic.

         THE GAP IS SIZED FROM THE STAR RATHER THAN TYPED IN. `|dP/dt|` on an
         ellipse is `hypot(A sin t, B cos t)`, so dividing the star's own radius
         by it gives a break of constant ARC LENGTH wherever the star is put --
         at the end of the major axis the parameter has to travel four times as
         far as it does at the end of the minor one to cover the same pixels. A
         fixed angle would leave the star swimming in one seat and jammed in
         another, and the seat is Rick's to move. */
      const at = u.starAt, sR = u.starR;
      const sp = Math.hypot(u.A * Math.sin(at), u.B * Math.cos(at)) || 1;
      const gapH = Math.min(1.2, (sR * 1.35) / sp);
      const ca = Math.cos(u.tilt), sa = Math.sin(u.tilt);
      const pt = (rx, ry, t) => {
        const px = Math.cos(t) * rx, py = Math.sin(t) * ry;
        return [f.x + px * ca - py * sa, f.y + px * sa + py * ca];
      };
      /* the star's seat is ON THE BAND'S CENTRE LINE, so it fills the break
         rather than floating inside or outside it */
      const seat = pt((u.A + ai) / 2, (u.B + bi) / 2, at);
      const near = (t) => {
        const d = Math.abs(((t - at + Math.PI) % TAU + TAU) % TAU - Math.PI);
        return d < gapH;
      };
      /* THE UNDER PASS DRAWS THE WHOLE RING AND THE OVER PASS THE FRONT HALF,
         which is unchanged -- that split is what makes it read as a ring
         around a body rather than an ellipse painted on the floor. */
      const keep = (t) => !near(t) && (over ? Math.sin(t) > 0 : true);
      const SEG = 64;
      c.save();
      c.globalCompositeOperation = "lighter";'''),

("the band in segments",
 '''      c.beginPath();
      c.ellipse(f.x, f.y, u.A, u.B, u.tilt, s0, s1);
      c.ellipse(f.x, f.y, ai, bi, u.tilt, s1, s0, true);
      c.closePath();
      c.globalAlpha = 0.30 * k;''',
 '''      /* IN SEGMENTS NOW, WHICH IS WHAT THE GAP COSTS. Two `ellipse` calls
         cannot express "all of it except that bit", and a clip path would cost
         a save, a restore and a second path every pass. Sixty-four segments
         accumulated into ONE path and filled ONCE keeps this at two fills and
         two strokes a pass -- the same count it had before the gap existed,
         which is the constraint Breach's jets taught (nine gradients inside a
         loop took a capture to 0.19 frames a second).

         THE `moveTo` BEFORE EACH ARC IS NOT DECORATION: without it canvas
         joins each new sub-path to the last with a straight line, and the
         band would be drawn with a chord across the gap. */
      c.beginPath();
      for (let i = 0; i < SEG; i++){
        const t0 = i * TAU / SEG, t1 = (i + 1) * TAU / SEG;
        if (!keep((t0 + t1) / 2)) continue;
        const o0 = pt(u.A, u.B, t0);
        c.moveTo(o0[0], o0[1]);
        c.ellipse(f.x, f.y, u.A, u.B, u.tilt, t0, t1);
        c.ellipse(f.x, f.y, ai, bi, u.tilt, t1, t0, true);
        c.closePath();
      }
      c.globalAlpha = 0.30 * k;'''),

("the rims in segments",
 '''      c.beginPath(); c.ellipse(f.x, f.y, u.A, u.B, u.tilt, s0, s1); c.stroke();
      c.beginPath(); c.ellipse(f.x, f.y, ai, bi, u.tilt, s0, s1); c.stroke();''',
 '''      for (const [rx, ry] of [[u.A, u.B], [ai, bi]]){
        c.beginPath();
        for (let i = 0; i < SEG; i++){
          const t0 = i * TAU / SEG, t1 = (i + 1) * TAU / SEG;
          if (!keep((t0 + t1) / 2)) continue;
          const q = pt(rx, ry, t0);
          c.moveTo(q[0], q[1]);
          c.ellipse(f.x, f.y, rx, ry, u.tilt, t0, t1);
        }
        c.stroke();
      }'''),

("the lights go round the gap",
 '''        const th = spin + i * TAU / N;
        if (over && Math.sin(th) < 0) continue;
        if (!over && Math.sin(th) > 0) continue;
        const rr = 1 - 0.5 * (u.wd / u.A);
        const px = Math.cos(th) * u.A * rr, py = Math.sin(th) * u.B * rr;
        const ca = Math.cos(u.tilt), sa = Math.sin(u.tilt);
        c.globalAlpha = (0.35 + 0.45 * (0.5 + 0.5 * Math.sin(th * 3 + spin * 5))) * k;
        c.beginPath();
        c.arc(f.x + px * ca - py * sa, f.y + px * sa + py * ca, 2.1, 0, TAU);
        c.fill();''',
 '''        const th = spin + i * TAU / N;
        if (over && Math.sin(th) < 0) continue;
        if (!over && Math.sin(th) > 0) continue;
        /* AND THEY GO ROUND THE GAP RATHER THAN THROUGH IT. A light crossing
           the break would say the band is continuous after all, which is the
           one thing the break exists to deny. */
        if (near(th)) continue;
        const rr = 1 - 0.5 * (u.wd / u.A);
        const q = pt(u.A * rr, u.B * rr, th);
        c.globalAlpha = (0.35 + 0.45 * (0.5 + 0.5 * Math.sin(th * 3 + spin * 5))) * k;
        c.beginPath();
        c.arc(q[0], q[1], 2.1, 0, TAU);
        c.fill();'''),

("the star sits in the gap",
 '''      if (over && C && !C.popped){''',
 '''      /* AND THE STAR IS IN THE BREAK, NOT ON THE SHELL. It is drawn in
         whichever pass its own seat belongs to -- the front half over the
         balls, the back half behind them -- so a star on the far side of the
         ring passes behind the fighter exactly as the band does. That is the
         Saturn read applied to the one object that is not the band.

         IT TURNS WITH THE RING. `rotate(u.tilt)` puts the star upright
         relative to the band it is seated in rather than to the screen, which
         is what says it belongs to the ring. */
      if (C && !C.popped && (over ? Math.sin(at) >= 0 : Math.sin(at) < 0)){'''),

("the star is seated",
 '''        const R0 = CONFIG.physics.ballR;
        const pul = 1 + 0.05 * Math.sin(C.t * 7.5);
        c.save();
        c.globalCompositeOperation = "source-over";
        c.translate(f.x, f.y);
        c.globalAlpha = k;
        c.lineJoin = "round";
        this._sparkStar(c, R0 * 1.02 * pul, 0.32);
        c.lineWidth = 7; c.strokeStyle = P.dark; c.stroke();
        c.shadowColor = P.glow; c.shadowBlur = 20;
        c.fillStyle = P.core; c.fill();
        c.shadowBlur = 0;
        /* the hot centre, which is the only white in the whole relic and is
           what survives the phone screen once the bloom has had it */
        c.fillStyle = "#FFF3FA";
        this._sparkStar(c, R0 * 0.44 * pul, 0.28);
        c.fill();
        c.restore();''',
 '''        const pul = 1 + 0.05 * Math.sin(C.t * 7.5);
        c.save();
        c.globalCompositeOperation = "source-over";
        c.translate(seat[0], seat[1]);
        c.rotate(u.tilt);
        c.globalAlpha = k;
        c.lineJoin = "round";
        this._sparkStar(c, sR * pul, 0.32);
        c.lineWidth = 7; c.strokeStyle = P.dark; c.stroke();
        c.shadowColor = P.glow; c.shadowBlur = 20;
        c.fillStyle = P.core; c.fill();
        c.shadowBlur = 0;
        /* the hot centre, which is the only white in the whole relic and is
           what survives the phone screen once the bloom has had it */
        c.fillStyle = "#FFF3FA";
        this._sparkStar(c, sR * 0.44 * pul, 0.28);
        c.fill();
        c.restore();'''),

]


# ---- AND THE BURN IS EMBERS, WITH NO RING ---------------------------------
# Rick, 2026-09-03, from a spread of four (`corona_burn_sheet.py`): "b looks
# best but the full ring of red is really confusing."
#
# TWO NOTES, AND BOTH OF THEM WERE ALREADY WRITTEN DOWN IN THIS ENGINE:
#
#   THE WORMS. The first cut stroked a curve of constant width three times.
#   Nothing in fire is a line of even thickness that bends, so it read as
#   something ANIMAL. Embers have no long axis at all -- there is nothing to
#   wriggle.
#
#   THE RING. Variant B carried a full stroked circle at `R * 0.99` for heat,
#   and a continuous ring around a ball in this game is a GAUGE: `_stWard`'s
#   own docstring records the ward arc being moved to R+17 because "at R+9 it
#   was fighting the health ring for the same annulus". A red ring at 0.99R is
#   inside both of them. It is gone; the heat is a DISC, which is a surface and
#   not a readout, and the count is carried by how many motes are in the air.
S6_BURN = [

("the burn is embers",
 '''  _stBurn(m, f, R, n){
    const c = this.ctx;
    const HOT = "#FFC061", CORE = "#FF7A1F", EDGE = "#2A0C02";
    const heat = Math.min(1, n / 24);
    const N = Math.min(12, n);
    const t = m.t;
    c.save();
    /* THE SHELL IS HOT UNDER THE LICKS, which is what carries a count of forty
       when the licks themselves stopped counting at twelve. `lighter` over the
       ball, not a ring beside it. */
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = 0.10 + 0.30 * heat;
    c.fillStyle = CORE;
    c.beginPath(); c.arc(f.x, f.y, R * 0.96, 0, TAU); c.fill();
    c.globalCompositeOperation = "source-over";
    for (let i = 0; i < N; i++){
      /* NO `this.rng()`. The flicker is a function of the match clock and the
         lick's own index, so two replays of a seed draw the same fire. */
      const a = i * TAU / N + Math.sin(t * 0.7 + i) * 0.06;
      const wob = 0.5 + 0.5 * Math.sin(t * 9 + i * 2.1);
      const L = (7 + 5 * wob) * (0.7 + 0.5 * heat);
      const x0 = f.x + Math.cos(a) * (R + 1), y0 = f.y + Math.sin(a) * (R + 1);
      const x1 = f.x + Math.cos(a) * (R + 1 + L), y1 = f.y + Math.sin(a) * (R + 1 + L);
      const sx = Math.cos(a + 1.2) * 3 * (wob - 0.5);
      c.lineCap = "round";
      c.beginPath();
      c.moveTo(x0, y0);
      c.quadraticCurveTo((x0 + x1) / 2 + sx, (y0 + y1) / 2 + sx, x1, y1);
      c.lineWidth = 5.4; c.strokeStyle = EDGE; c.globalAlpha = 0.85;
      c.stroke();
      c.lineWidth = 3.0; c.strokeStyle = CORE; c.globalAlpha = 0.95;
      c.stroke();
      c.lineWidth = 1.3; c.strokeStyle = HOT; c.globalAlpha = 0.5 + 0.5 * wob;
      c.stroke();
    }
    c.restore();
  }''',
 '''  _stBurn(m, f, R, n){
    /* EMBERS, AND NO RING. Rick's pick from a spread of four, with one
       correction: "b looks best but the full ring of red is really
       confusing."

       THE FIRST CUT WAS WORMS AND HE SAID SO. It stroked a curve of constant
       width three times over -- and nothing in fire is a line of even
       thickness that bends, so twelve of them crawling round a shell read as
       something animal. An ember has no long axis; there is nothing to
       wriggle.

       AND THE RING HE KILLED WAS A GAUGE, WHICH THIS ENGINE ALREADY KNEW.
       The spread's variant B carried a stroked circle at `R * 0.99` to say
       heat, and a continuous ring around a ball in this game is a READOUT:
       `_stWard`'s own docstring records the ward arc being moved out to R+17
       because "at R+9 it was fighting the health ring for the same annulus".
       A red ring at 0.99R sits inside both of them and says QUANTITY. So the
       heat is a DISC -- a surface, not a readout -- and the count is carried
       by how many motes are in the air.

       THE COUNT IS THE ONE HARD PART OF THIS STATUS. It is the only one in
       the game with no ceiling: it peaks near 60 where every other status
       caps at four to six, and `_stBleed` shipped a bug for exactly that
       reason (`Math.min(4, n)` drips, so eight stacks looked like four). So
       nothing here draws one mark per stack -- the mote COUNT saturates at 22
       and the heat under the shell goes on climbing to 24 stacks, and the
       exact figure is on the status tag, which prints it.

       NO `this.rng()`. Every mote's phase is a function of the match clock and
       its own index, so two replays of a seed draw the same fire -- a renderer
       that spends from the sim's stream moves every fight it draws. */
    const c = this.ctx;
    const HOT = "#FFD08A", CORE = "#FF6A12";
    /* THE SCALE RUNS TO THE MEASURED PEAK AND NOT TO A ROUND NUMBER. The first
       cut divided by 24, and the mote count saturated at 22 by eighteen stacks
       -- so a quarry on SIXTY looked exactly like one on twenty, on the one
       status in this game that has no ceiling. `corona_relic_probe` measures
       the peak at 59, so 48 is the number that leaves the top of the range
       legible instead of clipped. This is `_stBleed`'s bug in a second
       costume: it is not enough to draw more than four marks, the SCALE has to
       reach where the status actually goes. */
    const heat = Math.min(1, n / 48);
    const N = Math.min(34, 5 + Math.round(n * 0.7));
    const t = m.t;
    c.save();
    c.globalCompositeOperation = "lighter";
    /* THE SHELL IS HOT -- A DISC AND NOT A RIM (Rick killed the rim: a
       continuous ring around a ball in this game is a gauge). KEPT DELIBERATELY
       LOW, because the first cut of this washed the ball toward white at forty
       stacks and section 4.1b is exactly that: a bright thing added to a bright
       thing is not lit, it is ERASED. The shell has to still be a relic with a
       colour and a health ring when it is burning hardest, so the heat here
       tops out well under saturation and the COUNT is carried by the motes.

       TWO FLAT FILLS, NOT A GRADIENT. `GRAIN_CACHE`'s comment is the reason --
       nine `createRadialGradient` calls a relic a frame were the single cause
       of the stutter Rick reported, and Breach's billow put one inside a loop
       and took a capture to 0.19 frames a second. */
    c.globalAlpha = 0.09 + 0.22 * heat;
    c.fillStyle = CORE;
    c.beginPath(); c.arc(f.x, f.y, R * 0.97, 0, TAU); c.fill();
    c.globalAlpha = 0.05 + 0.17 * heat;
    c.beginPath(); c.arc(f.x, f.y, R * 0.60, 0, TAU); c.fill();
    for (let i = 0; i < N; i++){
      /* THE PHASE IS PER-MOTE AND IRRATIONAL-ISH, so they do not pulse
         together -- a field that breathes in unison reads as one object
         flashing rather than as many small ones rising. */
      const ph = (t * (0.9 + 0.25 * ((i * 37) % 7) / 7) + i * 0.618) % 1;
      const a = i * TAU / N + 0.9 * Math.sin(i * 2.3);
      /* AND THE COLUMN GETS TALLER WITH THE COUNT, which is the second half of
         the count read: at six stacks a few embers come off the shell, at
         sixty there is a plume standing over it. Height is legible at arena
         scale in a way that a brighter ball is not. */
      const rise = ph * (22 + 40 * heat);
      const x = f.x + Math.cos(a) * (R - 2) + Math.sin(i * 1.7) * rise * 0.30;
      const y = f.y + Math.sin(a) * (R - 2) - rise;
      const r = (3.2 - 2.0 * ph) * (0.75 + 0.6 * heat);
      if (r <= 0.2) continue;
      c.globalAlpha = (1 - ph * 0.85) * (0.55 + 0.4 * heat);
      c.fillStyle = ph < 0.28 ? HOT : CORE;
      c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    }
    c.restore();
  }'''),

]


# ---- AND THE CAST HAS A VOICE ---------------------------------------------
# Rick, 2026-09-03, from four rendered candidates heard INSIDE A REAL FIGHT:
# "3 sounds the best." SWEEP.
#
# HE COULD NOT JUDGE THEM COLD AND SAID SO -- "i cant judge the sound like
# this" -- which is `sentinel_hum_lab`'s own docstring being right again: a
# candidate has to be heard ARRIVING the way it will in the fight, because
# there are 134 other sounds in the fourteen seconds this one has to be picked
# out of. `corona_voice_audition.py` is what settled it, and it is a permanent
# tool: it records the engine's own `SFX.play` call list over one window and
# replays it with ONE call substituted, so the four differ by a single sound
# and by nothing else.
#
# THE SOURCE IS THE LAB'S, NOT A COPY OF IT. `corona_voice_lab.VOICES_JS`
# candidate 3, transcribed here with `this._` in place of the lab's helpers and
# nothing else changed -- and `voice_matches` below refuses to write unless the
# shipped branch carries every one of its numbers.
S6_VOICE = [

("the cast voice",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "starwarden"){
          /* CORONA -- SWEEP. Rick's, from four rendered into a real window
             (`corona_voice_audition.py`): the band coming ROUND, and then
             LOCKING.

             IT IS A SWEEP AND NOT A STRIKE, which is the whole reason it fits
             this cast. Nothing has been hit when this plays -- for a median
             1.31 seconds afterwards the ultimate has touched nobody -- so an
             impact voice would promise a contact that has not happened. Every
             other ult voice in this game is a thing landing.

             `_sweep` IS THE PRIMITIVE SCOUR ADDED and this is its second use:
             the only swept noise in a toolkit otherwise made of struck ones.

             THE LOCK IS THE POINT. The two re-struck triangles a fifth apart
             at 0.50 and 0.86 are what says the ring has taken its shape and
             is going to STAND there for eight seconds -- and they are
             re-struck rather than held because `_tone` decays over its whole
             length and A HELD NOTE DOES NOT EXIST IN THIS TOOLKIT (CLAUDE.md
             4.5, open item 6). No burst here is over 0.55s for the other half
             of that bug: `_burst` does not loop its 0.6s noise buffer, so a
             longer one plays silence for its tail. */
          this._sweep(t, { f0: 240, f1: 2600, q: 0.8, gain: 0.16, dur: 0.52,
                           atk: 0.16 });
          this._sweep(t + 0.34, { f0: 1800, f1: 700, q: 1.1, gain: 0.085,
                                  dur: 0.40, atk: 0.10 });
          this._burst(t + 0.50, { freq: 900, q: 1.4, gain: 0.10, dur: 0.12,
                                  type:"bandpass" });
          [0.50, 0.86].forEach((d, i) => {
            this._tone(t + d, { freq: 294, to: 294, gain: 0.10 - i * 0.03,
                                dur: 0.50, type:"triangle" });
            this._tone(t + d, { freq: 441, to: 441, gain: 0.055 - i * 0.02,
                                dur: 0.44, type:"triangle" });
          });
          this._tone(t + 0.02, { freq: 140, to: 190, gain: 0.11, dur: 0.46,
                                 type:"sine" });
        } else {                                        // rune-crack'''),

]


# ---- AND THE STAR POP HAS ONE -----------------------------------------------
# Rick, 2026-09-03, from four auditioned TWICE -- once in a window with 3.35s
# between the cast and the pop, and once in one with 1.28s, which is the
# measured median: "3 sounds best." CHIMES.
#
# THE SECOND AUDITION IS WHY THIS PICK IS TRUSTWORTHY. The pop lands a median
# 1.31s after the cast and SWEEP runs 1.15s, so in the typical window the two
# OVERLAP -- and the first window offered had nearly three seconds of air
# between them, which hears them as separate events by construction. A voice
# chosen there could have fused into the cast on every ordinary cast and
# nothing would have said so. `_corona_tight.py` exists to find the hard case.
#
# AND THE BUILD WAS SILENT HERE, so this adds the CALL as well as the voice.
# `coronaPop` filed a beat, a ring and a shake and made no sound at all --
# which is v42's defect sitting in the open, and it is why the audition had to
# INJECT the candidate rather than substitute it.
S6_POP = [

("the pop is heard",
 '''    this.ring(f.x, f.y, f.aff.core, 10, 104, 0.5, 5);
    this.shake = Math.max(this.shake, 14);''',
 '''    this.ring(f.x, f.y, f.aff.core, 10, 104, 0.5, 5);
    this.shake = Math.max(this.shake, 14);
    /* AND IT IS HEARD. Its own voice and not the cast's: this is the moment
       the ultimate stops being a ring and becomes a room full of hazards, and
       it is the second-biggest thing the relic does. The convention is the
       roster's -- `lastlight-stick`, `vesper-wind`, `grudgebearer-fizzle`,
       `gravemourn-hand` all name a sub-event this way.

       `SFX.play` CANNOT MOVE A FIGHT. It returns on its first line headless,
       wraps its body in try/catch and draws from nothing -- which is exactly
       why a silent ultimate once shipped through every check in this repo, and
       why `engine_ab` is still run over this insert rather than argued about. */
    SFX.play("ult", { w: "starwarden-pop" });'''),

("the pop voice",
 '''        } else if (w === "starwarden"){''',
 '''        } else if (w === "starwarden-pop"){
          /* THE STAR BURSTING -- CHIMES. Rick's, from four heard in two real
             windows (`corona_voice_audition.py --event pop`).

             IT SAYS STAR AND NOT BOMB, which is the choice: a struck
             inharmonic cluster and then a spray of small partials scattering
             off it, one after another, where the alternatives were glass
             breaking, a magnesium flare and sixteen countable ticks.

             AND IT HAD TO SURVIVE LANDING ON THE CAST'S TAIL. The pop is a
             median 1.31s after the cast and SWEEP runs 1.15s, so these two
             voices overlap in the ordinary window -- the low body at 131 Hz is
             what keeps this one underneath a cast that has almost nothing
             below 120, and the cluster sits an octave above SWEEP's lock at
             294/441.

             THE SPRAY IS DETERMINISTIC. `h` is the hash `drawScour` uses --
             index in, a number in [0,1) out -- because `Math.random` in a
             voice would make two renders of one clip differ, and this project
             compares renders. */
          const h = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
                             return x - Math.floor(x); };
          [[523,1.00],[784,0.60],[1109,0.38],[1567,0.22]].forEach(([fq, k]) =>
            this._tone(t, { freq: fq, to: fq * 0.992, gain: 0.10 * k,
                            dur: 0.85, type:"triangle" }));
          this._burst(t, { freq: 5200, q: 1.4, gain: 0.16, dur: 0.05,
                           type:"bandpass" });
          this._tone(t, { freq: 131, to: 118, gain: 0.16, dur: 0.40,
                          type:"sine" });
          for (let i = 0; i < 8; i++){
            const j = h(i * 7 + 5);
            this._tone(t + 0.06 + i * 0.042,
                       { freq: 1200 + j * 2400, to: (1200 + j * 2400) * 0.985,
                         gain: 0.055 * (1 - i / 10), dur: 0.34,
                         type:"triangle" });
          }
        } else if (w === "starwarden"){'''),

]


# ---- AND THE LAST TWO VOICES, WHICH RICK DELEGATED --------------------------
# Rick, 2026-09-03: "pick voices for the burn and the chain." Three candidates
# each, auditioned in the same real window as the pop, and picked on MEASURED
# grounds rather than on taste -- which is the only honest way to make a call
# that is normally his.
#
#   THE BURN IS **WHUMP**. It fires on a ring CROSSING -- 7 of them in the
#   audition window -- and at that rate the requirement is that it not become
#   the fight's dominant sound. Measured in-fight against the same control:
#   SIZZLE +27%, TICK +20%, WHUMP **+8%**. And it is the only one of the three
#   that separates by REGISTER: almost all of it is under 400 Hz, where SWEEP
#   has 0.6% of its energy and CHIMES 4.1%. A cue that fires seven times a cast
#   has to sit somewhere nothing else is.
#
#   THE CHAIN IS **FALLING**. The queue is sorted by `y` and fires from the top
#   of the hall down, so a pitch that steps DOWN runs the same way the eye
#   does -- Rick's own "a chain reaction like effect from one end of the arena
#   to the other", made audible. FLAT was in the spread as a control that ought
#   to be worse, and it is: five identical sounds 70ms apart are a stutter, not
#   a run.
#
# THE CHAIN'S VOICE TAKES AN INDEX, WHICH NOTHING ELSE IN THIS GAME'S AUDIO
# DOES. It has to: 70ms is faster than any voice in this toolkit decays, so
# without the step the five detonations fuse into one buzz.
S6_LAST = [

("the crossing is heard",
 '''          if (!C.inb){ C.entries++; this.burnFoe(f, foe, u.entry, true); }''',
 '''          if (!C.inb){
            C.entries++;
            this.burnFoe(f, foe, u.entry, true);
            /* THE CROSSING IS THE ONLY THING THE BURN CAN SOUND ON. The status
               ticks 120 times a second and is applied ~34 times a cast; a
               voice on either would be the whole mix. A crossing is ~5.6 a
               cast, which is a rate this roster already lives with -- and it
               is the same gate the status tag uses, so what a viewer hears and
               what they read arrive together.

               DELIBERATELY NOT INSIDE `burnFoe`: that helper is also called by
               every touched star, eleven a cast, and a voice there would be a
               different mechanic making the same sound. */
            SFX.play("ult", { w: "starwarden-burn" });
          }'''),

("the chain knows its length",
 '''        C.chain = C.stars.map((s, i) => ({ s, at: C.t + i * u.gap }));
        C.stars = [];''',
 '''        C.chain = C.stars.map((s, i) => ({ s, at: C.t + i * u.gap }));
        /* HOW MANY THERE ARE, so each detonation knows where it is in the run.
           The voice steps its pitch across the queue and cannot do that from a
           count that only goes up -- it needs the total, and the total is only
           knowable here, on the frame the queue is built. */
        C.chainN = C.chain.length;
        C.stars = [];'''),

("the chain is heard",
 '''    if (!touched && C.chained === 0)''',
 '''    /* AND EVERY LINK IS HEARD, WITH ITS PLACE IN THE RUN. `k` runs 0 at the
       top of the hall to 1 at the bottom and the voice steps its pitch down
       across it: at 70ms apart -- faster than anything in this toolkit decays
       -- an unstepped run is a buzz rather than a chain. The beat below is
       filed only for the FIRST, because a beat per star would hand the
       director four cuts of one picture; the SOUND is per star, because that
       is the thing the ear counts. */
    if (!touched){
      const n = C.chainN || 1;
      SFX.play("ult", { w: "starwarden-chain",
                        k: n > 1 ? C.chained / (n - 1) : 0 });
    }
    if (!touched && C.chained === 0)'''),

("the last two voices",
 '''        } else if (w === "starwarden-pop"){''',
 '''        } else if (w === "starwarden-burn"){
          /* THE CROSSING CATCHES -- WHUMP. Gas taking light: almost all of it
             under 400 Hz, which is where neither of the other two voices
             lives, so it separates by REGISTER rather than by timing. That
             matters more here than anywhere else in this relic, because this
             is the only voice that fires SEVEN times in a window -- measured
             in-fight it adds 8% to the window's peak against SIZZLE's 27% and
             TICK's 20%.

             SHORT, AND THAT IS NOT AN AESTHETIC. 0.22s is under the shortest
             gap between two crossings the design measured; anything longer
             and the fast double-crossing this ultimate is full of would stack
             two of these on top of each other. */
          this._burst(t, { freq: 300, q: 0.5, gain: 0.11, dur: 0.20,
                           type:"lowpass" });
          this._tone(t, { freq: 110, to: 62, gain: 0.085, dur: 0.22,
                          type:"sine" });
          this._burst(t + 0.03, { freq: 1800, q: 1.2, gain: 0.028, dur: 0.07,
                                  type:"bandpass" });
        } else if (w === "starwarden-chain"){
          /* THE LEFTOVERS GOING OFF -- FALLING, and it is the only voice in
             this game that knows where it is in its own run. `p.k` is 0 at the
             top of the hall and 1 at the bottom, and the pitch falls a fifth
             across it: the queue is sorted by `y` and fires downward, so the
             sound runs the way the eye does. Rick's sentence is "a chain
             reaction like effect from one end of the arena to the other" and
             this is that sentence in audio.

             WITHOUT THE STEP IT IS A BUZZ. 70ms apart is faster than anything
             in this toolkit decays, so five identical strikes fuse. FLAT was
             offered as a control for exactly that and it lost. */
          const k = p.k || 0;
          const fq = 880 * Math.pow(0.5, k * 0.58);
          this._burst(t, { freq: 2200, q: 1.5, gain: 0.11, dur: 0.05,
                           type:"bandpass" });
          this._tone(t, { freq: fq, to: fq * 0.72, gain: 0.085, dur: 0.20,
                          type:"triangle" });
          this._tone(t, { freq: fq * 0.5, to: fq * 0.42, gain: 0.045,
                          dur: 0.24, type:"sine" });
        } else if (w === "starwarden-pop"){'''),

]


def voice_matches(s: str) -> None:
    """The shipped cast voice carries every number the lab auditioned.

    `ult_matches`'s argument, pointed at the sound: v56 shipped an ultimate
    whose numbers its own log did not describe. Here the risk is worse, because
    a voice that has drifted from the one Rick picked is INAUDIBLE as an error
    -- it just sounds slightly different from the file he approved, and no
    check in this repo would say so.
    """
    def branch(w):
        """One voice's own branch, comments out, whitespace gone.

        `} else ` and not `} else {`: the fallback is the LAST arm, so a
        `} else {` search from the cast's branch runs straight past the pop's
        and reads two voices as one. That is how the first cut of this check
        passed while asserting nothing about the pop at all.
        """
        i = s.index('w === "' + w + '"')
        j = s.index("} else ", i + 10)
        return re.sub(r"\s+", "", strip_comments(s[i:j]))

    cast = branch("starwarden")
    want = ["f0:240,f1:2600", "f0:1800,f1:700", "freq:900,q:1.4",
            "freq:294,to:294", "freq:441,to:441", "freq:140,to:190",
            "[0.50,0.86]"]
    missing = [w for w in want if w.replace(" ", "") not in cast]
    if missing:
        raise SystemExit(
            "REFUSING TO WRITE -- the shipped CAST voice is not the one that "
            "was auditioned:\n  missing " + ", ".join(missing))
    print("  voice SWEEP  (the cast)     -- every number checked against the "
          "lab")

    if 'w === "starwarden-pop"' in s:
        pop = branch("starwarden-pop")
        wantp = ["[523,1.00]", "[784,0.60]", "[1109,0.38]", "[1567,0.22]",
                 "freq:5200,q:1.4", "freq:131,to:118", "i*0.042",
                 "1200+j*2400"]
        miss2 = [w for w in wantp if w.replace(" ", "") not in pop]
        if miss2:
            raise SystemExit(
                "REFUSING TO WRITE -- the shipped POP voice is not the one "
                "that was auditioned:\n  missing " + ", ".join(miss2))
        # AND SOMETHING PLAYS IT. A voice that is defined and never called is
        # the same shipped defect as no voice at all, and it is invisible to
        # every other check in this repo -- v42 exactly.
        if 'SFX.play("ult", { w: "starwarden-pop" })' not in s:
            raise SystemExit(
                "REFUSING TO WRITE -- the pop voice is defined and NOTHING "
                "PLAYS IT.")
        print("  voice CHIMES (the star pop) -- every number checked, and the "
              "call site asserted")
    # AND THE LAST TWO, WHICH RICK DELEGATED. Same rule: a voice defined and
    # never called is the same shipped defect as no voice at all.
    for w, want, site in (
        ("starwarden-burn",
         ["freq:300,q:0.5", "freq:110,to:62", "freq:1800,q:1.2"],
         'SFX.play("ult", { w: "starwarden-burn" })'),
        ("starwarden-chain",
         ["880*Math.pow(0.5,k*0.58)", "freq:2200,q:1.5", "fq*0.72", "fq*0.42"],
         'SFX.play("ult", { w: "starwarden-chain",')):
        if 'w === "' + w + '"' not in s:
            continue
        got = branch(w)
        miss = [x for x in want if x.replace(" ", "") not in got]
        if miss:
            raise SystemExit(
                f"REFUSING TO WRITE -- the shipped `{w}` voice is not the one "
                "that was auditioned:\n  missing " + ", ".join(miss))
        if site not in s:
            raise SystemExit(
                f"REFUSING TO WRITE -- `{w}` is defined and NOTHING PLAYS IT.")
    if 'w === "starwarden-burn"' in s:
        print("  voice WHUMP  (a crossing)   -- checked, and its call site is "
              "the CROSSING and not `burnFoe`")
        print("  voice FALLING (the chain)   -- checked, and it is handed its "
              "place in the run")


def fx_spec(s: str, out_name: str) -> str:
    """The spec into the page AND into `src/render/fx.js`, and the sha re-stamped.

    `bloodmirror_build` is the shape this follows and it stops one step short:
    it writes both copies and compares them, but leaves the page's STAMP
    claiming a sha the module no longer has. Measured before this ran -- the
    page said `3fe5a2bb` and `src/render/fx.js` hashed to `91a5a1b7`, because
    every SPECS insert since `fx_build` last ran has changed both copies
    without touching the stamp. THE STAMP IS THE ONLY THING THAT SAYS THE
    INLINE IS THE MODULE, so it is recomputed here rather than left to say
    something false more quietly.
    """
    import hashlib as _h
    fx_p = (HERE / "../src/render/fx.js").resolve()
    if not fx_p.exists():
        raise SystemExit(f"no such file: {fx_p} -- the spec source")
    fx0 = fx_p.read_text(encoding="utf-8")
    grown = FX_ANCHOR.replace(" }\n  };", " }" + FX_SPEC + "\n  };")
    # THE SIGNATURE AND NOT THE NAME. `starwarden:` appears in the `ultFx`
    # `life` map too, so a bare name test would report "already built".
    SIG = RELIC + ": { mode: 'swirl'"
    if SIG in s:
        raise SystemExit("the page already carries this spec -- built")
    if FX_ANCHOR not in s:
        raise SystemExit(
            "cannot find the end of the SPECS table in the page.\n"
            "  The spec goes in BOTH copies or in NEITHER.")
    s = one(s, FX_ANCHOR, grown, "fx spec (page)")
    if SIG in fx0:
        fx1 = fx0
        print("  ok    fx spec (src/render/fx.js)  already present")
    elif FX_ANCHOR in fx0:
        fx1 = fx0.replace(FX_ANCHOR, grown, 1)
        fx_p.write_text(fx1, encoding="utf-8", newline="\n")
        print("  ok    fx spec (src/render/fx.js)  written")
    else:
        raise SystemExit(
            "cannot find the end of the SPECS table in src/render/fx.js, and "
            "it does\n  not already carry this spec. Find out what moved -- do "
            "not write only the page.")
    # AND THE TWO COPIES ARE COMPARED, NOT ASSUMED (thornshear_build's rule,
    # scoped to the table because the page's copy has been through the inliner).
    i0 = fx1.index("var SPECS = {"); i1 = fx1.index("\n  };", i0)
    j0 = s.index("var SPECS = {");   j1 = s.index("\n  };", j0)
    if fx1[i0:i1] != s[j0:j1]:
        raise SystemExit(
            "REFUSING TO WRITE -- the SPECS table in the page and in "
            "src/render/fx.js\n  are not identical after the insert.")
    n_fx = fx1[i0:i1].count("mode:")
    print(f"        {n_fx} specs, byte-identical in both copies")
    # THE STAMP, RECOMPUTED. Both places it appears.
    sha = _h.sha256(fx1.encode("utf-8")).hexdigest()
    old_full = re.search(r"inlined by fx_build\.py\. sha256:([0-9a-f]{64})", s)
    old_short = re.search(r"\(src/render/fx\.js sha256 ([0-9a-f]{16})\)", s)
    if not old_full or not old_short:
        raise SystemExit("cannot find the fx sha stamp in the page")
    was = old_full.group(1)
    s = s.replace("sha256:" + was, "sha256:" + sha, 1)
    s = s.replace("sha256 " + old_short.group(1), "sha256 " + sha[:16], 1)
    print(f"        stamp {was[:16]} -> {sha[:16]}  (it was STALE before this "
          "run -- see the docstring)")
    print("        NOTE: `ravelbone` and `gloamwire` still have NONE, and")
    print("        `ULTFX.sync` returns silently on a missing spec. Item 46.")
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "4", "6"], default="1")
    ap.add_argument("--src", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=BLADE)
    ap.add_argument("--charge", type=float, default=ULT_CHARGE)
    ap.add_argument("--bdps", type=float, default=BURN_DPS)
    ap.add_argument("--bdur", type=float, default=BURN_DUR)
    ap.add_argument("--bmax", type=int, default=BURN_MAX)
    for k, v in ULT.items():
        ap.add_argument("--" + k, type=float, default=float(v))
    A = ap.parse_args()

    src = A.src or {"1": "../02-chain/sc-minute.html",
                    "2": "../02-chain/sc-starwarden.html",
                    "3": "../02-chain/sc-ring.html",
                    "4": "../02-chain/sc-shower.html",
                    "6": "../02-chain/sc-corona.html"}[A.stage]
    out = A.out or {"1": "../02-chain/sc-starwarden.html",
                    "2": "../02-chain/sc-ring.html",
                    "3": "../02-chain/sc-shower.html",
                    "4": "../02-chain/sc-corona.html",
                    "6": "../02-chain/sc-corona-fx.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nSTARWARDEN -- STAGE " + A.stage + ": "
          + {"1": "the 34th relic, its ultimate STUBBED",
             "2": "THE RING AND THE BURN -- no star, no shower",
             "3": "THE STAR AND THE SHOWER -- no chain",
             "4": "THE CHAIN -- THIS IS THE RELIC",
             "6": "THE PARTICLE FIELD"}[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR AND THE BASE IS NAMED, NOT GUESSED (brief section 2).
    # Two assertions, because "the tip" is two claims: 33 relics ending in
    # Duskreave, and the MINUTE PACE, which is the pace every decimal in
    # `06-docs/v66/` was priced on. A build of this design on the 48-second
    # clock would be a different relic measured against the wrong table.
    if 'id:"duskreave"' not in s0:
        raise SystemExit(
            "this source is not the Duskreave tip -- no `duskreave` in it.\n"
            "  Starwarden is the 34th relic and builds on the 33rd; if the\n"
            "  intention is to build it somewhere else, say so with --src and\n"
            "  say why in the write-up, because the relic count in every doc\n"
            "  moves with it.")
    pace = strip_comments(s0)
    want_pace = [("baseHP", "520"), ("timeout", "156")]
    off = [f"{k} != {v}" for k, v in want_pace
           if not re.search(r"\b" + k + r"\s*:\s*" + v + r"\b", pace)]
    if off:
        raise SystemExit(
            "this source is not on the MINUTE PACE (" + ", ".join(off) + ").\n"
            "  Every number in `06-docs/v66/` -- the 17.2% body, the 49.1%\n"
            "  whole, the dwell, the crossing rate -- was priced on\n"
            "  `sc-minute.html`. On the old clock this is a different relic\n"
            "  and the design's table cannot judge it.")
    print("  base  33 relics, Duskreave tip, minute pace (baseHP 520, "
          "timeout 156)")
    if A.stage == "1" and 'id:"' + RELIC + '"' in s0:
        raise SystemExit("this source already has Starwarden -- built")
    if A.stage == "2":
        if 'id:"' + RELIC + '"' not in s0:
            raise SystemExit("stage 2 needs stage 1's link -- no Starwarden in "
                             "this source")
        if "charge:1e9" not in body_block(s0, RELIC, "ult"):
            raise SystemExit(
                "the ultimate in this source is not stubbed, so stage 2 has\n"
                "  already run against it. Rebuild stage 1 first -- a stage\n"
                "  applied twice is how a builder writes numbers its own log\n"
                "  does not describe.")
        # THE BURN IS A NEW STATUS AND IT MUST BE NEW. A `burn` key already in
        # STATUS would mean this insert is landing on top of somebody else's
        # status and every number in the design is measuring two mechanics.
        if re.search(r"^\s*burn\s*:", strip_comments(s0), re.M):
            raise SystemExit("this source already has a `burn` status")
    if A.stage in ("3", "4"):
        code0 = strip_comments(s0)
        if "tickCorona" not in code0:
            raise SystemExit(f"stage {A.stage} needs the ring -- no "
                             "`tickCorona` in this source")
        if A.stage == "3" and "coronaPop" in code0:
            raise SystemExit(
                "this source already has the shower -- stage 3 has run "
                "against it. A stage applied twice is how a builder writes "
                "numbers its own log does not describe.")
        if A.stage == "4":
            if "coronaPop" not in code0:
                raise SystemExit("stage 4 needs stage 3's link -- no shower in "
                                 "this source")
            if "C.chain.shift()" in code0:
                raise SystemExit("this source already chains -- stage 4 has "
                                 "run against it")

    # THE PHYSICAL STATS ARE THE TYPE'S, ASSERTED AND NOT ASSUMED. Every number
    # in the design was measured on a twinblade body built by `cell_ults_on`;
    # they are only transferable to a fifth twinblade if the four shipped ones
    # really do agree. If they do not, the design's numbers are not this
    # relic's numbers, and that is a finding rather than a detail.
    twins = ["widowmaker", "spellbreaker", "twinshade", "thornshear"]
    got = {r: phys(s0, r) for r in twins}
    keys = ("blades", "reach", "width", "artW", "spin", "mass", "mode")
    base = {k: got[twins[0]].get(k) for k in keys}
    odd = {r: {k: v.get(k) for k in keys if v.get(k) != base[k]}
           for r, v in got.items()}
    odd = {r: d for r, d in odd.items() if d}
    if odd:
        raise SystemExit(
            "the four shipped twinblades do NOT agree on the type's own stats,\n"
            "  so the design's numbers -- all measured on one twinblade body --\n"
            "  are not transferable to a fifth:\n  "
            + "\n  ".join(f"{r}: {d}" for r, d in odd.items()))
    print(f"  body  one set across {len(twins)} twinblades -- the TYPE owns it: "
          + ", ".join(f"{k}:{base[k]}" for k in keys))

    # THE SILHOUETTE EXISTS AND IS ROUTED. This relic is the first ever to draw
    # it, so an unrouted school would ship the generic dagger and nobody would
    # see it in a number.
    art = re.search(r'if \(key === "vigil"\)\s*return SHAPES\.(_tb\w+)', s0)
    if not art:
        raise SystemExit(
            "`SHAPES.twinblade` does not route `vigil` anywhere. This relic is\n"
            "  the first vigil twinblade in the game, so the routing has never\n"
            "  been exercised -- if it has fallen through, the silhouette that\n"
            "  ships is the generic dagger and nothing here would notice.")
    if f"  {art.group(1)}(c, L, W, p)" not in s0:
        raise SystemExit(f"`SHAPES.twinblade` routes vigil to "
                         f"`{art.group(1)}` and that function is not in this "
                         f"source.")
    print(f"  art   SHAPES.twinblade routes vigil -> {art.group(1)}")

    # THE SCHOOL'S CHANNEL IS COPIED, NOT INVENTED. Three melee vigil relics
    # carry `{ ward:1 }`; FARWARDEN carries 2.5 and its own comment says why
    # (`onSelf`'s value is a per-relic bank multiplier and a bow banks three
    # small hits a window where a greatsword banks one big one). The design
    # priced this body at ward:1, so that is what ships -- and the bow is named
    # as the deliberate exception rather than silently averaged in.
    melee = ["lightkeeper", "bulwarden", "vesper"]
    chan = {r: body_block(s0, r, "onSelf") for r in melee}
    bad = {r: c for r, c in chan.items() if c.replace(" ", "") != "{ward:1}"}
    if bad:
        raise SystemExit("the shipped melee vigil relics do not agree on the "
                         f"school's channel: {bad}")
    bow = body_block(s0, "farwarden", "onSelf").replace(" ", "")
    if bow != "{ward:2.5}":
        raise SystemExit(
            f"Farwarden's channel is {bow}, not the 2.5 this builder was "
            "written against.\n  The per-relic bank multiplier has moved and "
            "the note above is stale.")
    print(f"  chan  onSelf {{ ward:1 }} across {len(melee)} melee vigil relics"
          "  (farwarden 2.5, its own bow correction)")

    table = {"1": S1, "2": S2, "3": S3, "4": S4,
             "6": S6_STAR + S6_GAP + S6_BURN + S6_VOICE
                  + S6_POP + S6_LAST}[A.stage]

    # THE ANCHOR IS SUBSTITUTED TOO. A later stage's anchors quote text an
    # earlier one WROTE, and it wrote it with the placeholders already filled
    # in -- so an un-substituted anchor can never match its own builder's
    # output.
    btip = BURN_TIP.replace("%BDPS%", f"{A.bdps:g}")

    def fill(txt):
        txt = (txt.replace("%DMG%", f"{A.dmg:g}")
                  .replace("%ULT%", A.ult)
                  .replace("%TIP%", A.tip)
                  .replace("%BLURB%", BLURB)
                  .replace("%CHARGE%", f"{A.charge:g}")
                  .replace("%BDPS%", f"{A.bdps:g}")
                  .replace("%BDUR%", f"{A.bdur:g}")
                  .replace("%BMAX%", f"{A.bmax:g}")
                  .replace("%BTIP%", btip))
        for k in ULT:
            txt = txt.replace("%" + k.upper() + "%", f"{getattr(A, k):g}")
        return txt

    for label, old, new in table:
        s = one(s, fill(old), fill(new), label)

    if A.stage == "6":
        voice_matches(s)
        s = fx_spec(s, out_p.name)

    # TRAP 1, AND IT IS THE FIRST THING TO CHECK ON ANY NEW OBJECT IN THIS
    # ENGINE. `Math.random` anywhere in the ring, the shower or the chain breaks
    # `engine_ab`, and it breaks it SILENTLY -- the page runs, the fight looks
    # fine, and two runs of one seed differ. And a RENDERER that draws from the
    # match's own stream moves every fight it draws, which is why Breach's
    # sparks are drawn rather than spawned. STRIPPED FIRST, because a check that
    # cannot tell code from the comment explaining it fires on its own
    # explanation (`curse_check` and `curse_build`, both on the same day).
    if A.stage != "1":
        code = strip_comments("".join(n for _, _, n in table))
        if "Math.random" in code:
            raise SystemExit(
                "REFUSING TO WRITE -- the corona calls `Math.random`. Every\n"
                "  number it needs comes from the match's own seeded stream\n"
                "  (`this.rng`) or from a clock.")
        # AND THE RENDERER IS CHECKED IN THE OUTPUT, NOT IN THE TABLE. The
        # first cut of this split the insert table on the method's own header
        # and, on a stage whose inserts do not contain that header, measured
        # the SIM code instead -- and refused to write over `coronaPop`'s
        # perfectly legitimate `this.rng()`. What has to be true is a property
        # of the shipped function, so the shipped function is what is read.
        for fn in ("drawCorona", "_stBurn"):
            body = fn_body(s, fn)
            if not body:
                continue
            if "this.rng()" in body or "spawnFx" in body or "Math.random" in body:
                raise SystemExit(
                    f"REFUSING TO WRITE -- `{fn}` spends from the sim's\n"
                    "  stream. A renderer that draws from `this.rng()` moves\n"
                    "  every fight it is drawn over, and Breach's sparks had to\n"
                    "  become DRAWN rather than spawned for exactly that.")
        print("  ok    no Math.random anywhere, no rng in the renderer")

    ult_matches(s, A, A.stage)

    if A.stage != "1":
        # THE SHIPPED BURN CARRIES WHAT THIS RUN PRINTED, which is `ult_matches`
        # pointed at the other half of the relic: the burn's two numbers live in
        # STATUS and not in the `ult` block, so `ult_matches` cannot see them --
        # and `dps` is the one number a later stage rewrites.
        blk = re.search(r"\n  burn:\s*\{[^}]*\}", strip_comments(s))
        if not blk:
            raise SystemExit("the shipped build has no `burn` status")
        got = re.sub(r"\s+", " ", blk.group(0)).strip()
        for k, v in (("maxStacks", f"{A.bmax:g}"), ("dur", f"{A.bdur:g}"),
                     ("dps", f"{A.bdps:g}")):
            if not re.search(r"\b" + k + r":" + re.escape(v) + r"\b",
                             got.replace(" ", "")):
                raise SystemExit(
                    "REFUSING TO WRITE -- the shipped `burn` status does not "
                    f"carry the {k} this run printed ({v}).\n  {got}")
        if len(btip) > 40:
            raise SystemExit(
                f"the burn's tip is {len(btip)} characters against `verify`'s "
                "40.")
        if 'tip:"' + btip + '"' not in s:
            raise SystemExit("REFUSING TO WRITE -- the shipped burn tip is not "
                             "the line this run printed.")
        print(f"  burn  maxStacks {A.bmax:g} (UNCAPPED -- Rick's ruling 1), "
              f"dur {A.bdur:g}s, dps {A.bdps:g} a stack")
        print(f"  btip  {btip!r} -- {len(btip)} of 40, AND IT IS A PLACEHOLDER: "
              "Rick has not written this one")

    if len(A.tip) > 72:
        raise SystemExit(f"the card line is {len(A.tip)} characters against "
                         f"`verify`'s 72. It is Rick's line and it is not this "
                         f"session's to cut (CLAUDE.md 3 rule 2).")
    if 'tip:"' + A.tip + '"' not in s:
        raise SystemExit("REFUSING TO WRITE -- the shipped tip is not the line "
                         "this run printed.")
    print(f"  tip   Rick's line is {len(A.tip)} characters against a cap of 72")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"  {len(s)} bytes")
    print(f"  relic dmg {A.dmg:g}, onSelf ward 1, ult {A.ult} "
          + ("STUBBED (charge 1e9, kind " + ULT_KIND + ")" if A.stage == "1"
             else f"LIVE (charge {A.charge:g}, kind " + ULT_KIND + ")"))

    if A.stage == "2":
        print(f"  ring  {A.A:g} x {A.B:g}, band {A.wd:g}, tilt {A.tilt:g} rad, "
              f"fixed in the world and centred on the ball")
        print(f"  ticks {A.rate:g}/s of {A.tickDmg:g} damage AND "
              f"+{A.tickStacks:g} burn, +{A.entry:g} on each crossing")
        print(f"  feed  the burn banks STATUS.ward.bank of every tick on the "
              f"caster -- and RESTARTS the 5s ward clock, which is what the "
              f"design priced")
        print(f"  window {A.dur:g}s every {A.charge:g}s")
        print("  the shower and the chain are WRITTEN AND INERT until "
              "stages 3 and 4")
        print("\n  GATE 2 -- the design's arm B, on the BUILT relic:")
        print("    python corona_relic_probe.py --game ../02-chain/sc-ring.html")
        print("      per cast: ~0.8s of dwell, ~5.6 crossings, ~12 stacks,")
        print("      ~6 damage and ~3.4 shield. The status source is ASSERTED")
        print("      and not commented: burn applied by A moves B's ward and")
        print("      moves nobody else's.")
        print("    python engine_ab.py --a ../02-chain/sc-starwarden.html \\")
        print("      --b ../02-chain/sc-ring.html --ids <the 33> --n 10")
        print("      IDENTICAL -- `apply` gained an optional third argument and")
        print("      `tickStatus` gained a named variable; neither moves a")
        print("      relic that cannot apply a burn.")
        print("    AND FILM ONE CAST. The ring is a first cut and CLAUDE.md 4.0")
        print("      says the argument is not the test.")
        return 0

    if A.stage in ("3", "4"):
        print(f"  shower {A.stars:g} stars at {A.sSpeed:g}, r {A.sR:g}, "
              f"grace {A.sGrace:g}s -- +{A.mineBurn:g} burn and knock "
              f"{A.knock:g} on a touch, FOE ONLY")
        print(f"  walls  the CURRENT inset, not the arena (v64's third "
              f"measurement)")
        print(f"  ceiling declined at CONFIG.shot.maxLive, never shifted")
        if A.stage == "3":
            print("  the chain is WRITTEN AND INERT until stage 4 -- the "
                  "leftovers go with the window")
            print("\n  GATE 3 -- the design's arm C/D shape, on the BUILT "
                  "relic:")
            print("    python corona_relic_probe.py "
                  "--game ../02-chain/sc-shower.html")
            print("      the star pops in ~90% of casts, ~11 stars touched a")
            print("      cast, refusals 0 with no bow foe, and the bookkeeping")
            print("      holds every cast: spawned = touched + chained + alive")
            print("    python engine_ab.py --a ../02-chain/sc-ring.html \\")
            print("      --b ../02-chain/sc-shower.html --ids <the 33> --n 10")
            print("    AND FILM ONE POP. CLAUDE.md 4.0.")
            return 0
        print(f"  chain  top to bottom, one every {A.gap:g}s, blast "
              f"{A.blast:g} -- MEASURED INERT and it is the finale picture")
        print("  and the next cast waits for the queue to drain")
        print("\n  GATE 4 -- and then the ONE KNOB:")
        print("    python corona_relic_probe.py "
              "--game ../02-chain/sc-corona.html")
        print("      ~3.4 chained a cast, ~0.35 of them landing inside the")
        print("      blast, no star outliving its chain, no cast under one")
        print("    python engine_ab.py --a ../02-chain/sc-shower.html \\")
        print("      --b ../02-chain/sc-corona.html --ids <the 33> --n 10")
        print("    python verify.py --game ../02-chain/sc-corona.html --n 40")
        print("      the relic is WHOLE here and the burn is still at its")
        print("      placeholder -- read it, do not tune it. Stage 5 bisects")
        print("      `dps` at n >= 700 a point on the pinned runtime, against")
        print("      a LOCAL reproduction of the design's 141 numbers and not")
        print("      against the published decimals (CLAUDE.md 4.2b).")
        return 0

    print("\n  GATE 1 -- run all four, and each can fail:")
    print("    python engine_ab.py --a ../02-chain/sc-minute.html "
          "--b ../02-chain/sc-starwarden.html --n 10")
    print("      IDENTICAL on all 33 -- a new entry at the END of WEAPONS "
          "moves nothing")
    print("    python verify.py --game ../02-chain/sc-starwarden.html --n 40")
    print("      Starwarden reads 15-25%: the ward body at the row floor with")
    print("      NO ultimate. Near 10% means the ward channel is not wired;")
    print("      near 50% means something is firing that should not.")
    print("    python tip_audit.py --game ../02-chain/sc-starwarden.html")
    print("    AND FILM THE SILHOUETTE -- `_tbPlated` has never been drawn.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
