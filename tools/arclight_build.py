#!/usr/bin/env python
"""ARCLIGHT and STATIC -- the vigil twinblade, the 34th relic.

Built from `06-docs/v64/ARCLIGHT-BUILD-BRIEF.md` (Cowork, 2026-09-02), which is
the input and the only input. Nothing in this file is a design decision: every
number below is Rick's or is measured, and the measured ones name the tool.
CLAUDE.md section 3 rule 0.

    stage 1   the relic, its ultimate STUBBED       sc-lastthree -> sc-arclight
    stage 2   the storm exists. No ward, no damage
    stage 3   the ward and the detonation -- THE RELIC
    stage 4   the blade, bisected DOWN from 8.3
    stage 5   art, sound, beat
    stage 6   the real price

THE BASE IS THE CHAIN TIP AND NOT THE BUILD OF RECORD. `sc-lastthree.html`
carries 33 relics, Duskreave and Scour, and the LAST-3 curse window; the app
still loads `sc-nova.html` at 32. Arclight is the 34th relic, so it builds on
the 33rd -- CLAUDE.md section 0.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "arclight"

# ------------------------------------------------------------- the numbers --

# THE BLADE IS A BISECTION START AND THE DIRECTION IS RULED. Brief stage 4:
# start at 8.3 -- Twinshade's, the twinblade row's floor -- and go DOWN. Rick,
# 2026-09-02: "the storm is the fighter", and he accepts the lightest blade in
# the game. `TUNED_AL` stays None until stage 4 has measured one.
BLADE = 8.3
TUNED_AL = None

ULT_NAME = "Static"
ULT_KIND = "static"         # its own kind. Nothing shares it -- one sigil, one
                            # sound, one picture (brief section 0).
ULT_CHARGE = 15.0

# RICK'S OWN LINE, 2026-09-02, and it is EXACTLY at `verify`'s 72. Brief
# section 5. One string, both surfaces; measured on both before stage 5 closes.
ULT_TIP = ("Hits spawn forking lightning. Caught bolts apply ward. "
           "All explode at 8s")
ULT_TIP1 = "-"              # stage 1, stubbed. `verify` asks only that it is
                            # non-empty; the real line lands with the mechanic
                            # it describes.

BLURB = ("Light struck across a gap. What it throws off its own hits comes "
         "home as armour, and what does not, lets go at once.")


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
    for f in ("reach", "width", "artW", "spin", "mass", "mode"):
        m = re.search(rf"\b{f}\s*:\s*(\"[a-z]+\"|[\d.]+)", e)
        if m:
            out[f] = m.group(1)
    m = re.search(r"\bblades\s*:\s*\[([^\]]*)\]", e)
    if m:
        out["blades"] = "[" + re.sub(r"\s+", "", m.group(1)) + "]"
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
        for k in ("dur", "per", "r", "speed", "ric", "fork", "grace", "cap",
                  "ward", "blast"):
            want[k] = f"{getattr(A, k):g}"
        want["dmg"] = f"{A.boltdmg:g}"
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

  /* ARCLIGHT -- THE VIGIL TWINBLADE, the thirty-fourth relic, and the fifth
     vigil. The cell Rick chose from four priced candidates: the v62 table put
     vigil x twinblade at +47.9pp of headroom, the most of any open cell by a
     tier, and it had been passed over four times.

     EVERY PHYSICAL STAT IS THE TWINBLADE'S, copied off Widowmaker,
     Spellbreaker, Twinshade and Thornshear -- the type owns
     `blades:[0,0.5], reach:62, width:8, artW:30, spin:5.7, mass:1.1,
     mode:"spin"` and there is no fifth set to invent. This builder asserts
     that against the shipped file before it writes rather than trusting this
     comment.

     `dmg` 8.3 IS A BISECTION START AND NOT THE ANSWER. It is Twinshade's --
     the row's floor today -- and brief stage 4 says to go DOWN from it and not
     to stop there. `budget-v59.md` section 3 is why: ward is the most
     weapon-speed-sensitive status in the game and this is the fastest weapon,
     so THIS BODY WINS 57-60% OF ITS FIGHTS WITH NO ULTIMATE AT ALL (design
     section 1, two seed blocks) and STATIC adds ~33 on top of that. To land in
     the field the blade gives back about forty points. Rick, 2026-09-02: "the
     storm is the fighter" -- he has accepted the lightest blade in the game.

     `onSelf:{ ward:1 }` is the school's channel, carried exactly as the other
     four vigil relics carry it -- and it is load-bearing here in a way it is
     not anywhere else, because THE ULTIMATE PAYS INTO IT. Aegis reflects the
     shield, Reprisal fires it, Sentinel drinks it; Static is the first thing
     in this school that FEEDS it, and it feeds it while the storm runs
     (`resolveHit`'s vigil branch is the reference -- same fields, same order).

     THE ART IS ALREADY ON THE ROW AND HAS NEVER BEEN SEEN. `SHAPES.twinblade`
     routes `vigil` to `_tbPlated` and has since before this cell had anything
     in it, so this is the first relic that will ever draw it. Brief stage 1
     says to film it and show Rick a strip BEFORE stage 2, and the reason is
     v58: `_whEaten` and `_scEaten` were both rejected on sight AFTER they had
     been built. "It is a different shape" is an argument, and CLAUDE.md 4.0
     says the argument is not the test. */
  { id:"arclight", name:"Arclight", aff:"vigil", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:%DMG%, spin:5.7, mode:"spin", mass:1.1,
    onSelf:{ ward:1 },
    /* STATIC. STUBBED AT `charge:1e9` IN STAGE 1 -- the same "OFF" the charge
       sweep in v55b used, and the same one Cindercleave's stage 1,
       Shroudmaul's stage 2, Gloamwire's stage 1, Bloodmirror's stage 1 and
       Duskreave's stage 1 used: the clock can never reach it, `fireUlt` never
       runs, and the relic is measured as a blade and a channel and nothing
       else. That measurement is gate 1 and it has a number to hit -- 57-60%,
       not 10% -- because the body is already spoken for by the ward.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       `kind:"static"` IS ITS OWN AND SHARES WITH NOTHING. The twinblade row
       already carries `detonate` (Widowmaker), `sling` (Spellbreaker), `split`
       (Twinshade) and `winnow` (Thornshear); a fifth set-piece on one weapon
       type has to be separable by its sigil, its voice and its picture, and
       sharing a kind is how two relics quietly become one. */
    ult:{ name:"%ULT%", charge:1e9, kind:"static", tip:"%TIP1%" },
    blurb:"%BLURB%" },

];'''),

]


# ------------------------------------------------------------------ stage 2 --

# EVERY NUMBER HERE IS THE BRIEF'S SECTION 0 TABLE. The three that are Rick's
# rulings of 2026-09-02 are `per` 8, `r` 16 and `fork` 2 (the big storm, over an
# in-between at +23pp and the sentence as written at +7pp) and `blast` 80 (over
# his own "small" 50 and over 100). `speed` 600 is MEASURED FREE -- 350 to 800
# all inside noise on the finale -- so it is a picture choice. `ric` 6 is
# "several", measured within a bolt of unlimited. `dur` 8 is ONE timer:
# spawning stops and every bolt detonates at the same instant, which the design
# measured as better than stopping the spawns early (2.97 in-blast against
# 2.73).
#
# `ward`, `blast` AND `boltdmg` ARE WRITTEN NOW AND ARE INERT UNTIL STAGE 3.
# Bloodmirror's `strandW`/`strandKnock` precedent and Duskreave's `tick`/`dmg`,
# and the reason is v56: a stage-2 insert wrote a whole `ult` block, stage 3
# rewrote one line of it, and the run LOGGED numbers the shipped relic did not
# carry. `ult_matches` refuses to write unless every number this run printed is
# in the block, so they go in together.
ULT = { "dur": 8.0, "per": 8, "r": 16.0, "speed": 600.0, "ric": 6,
        "fork": 2, "grace": 0.30, "cap": 60,
        "ward": 2.0, "blast": 80.0, "boltdmg": 15.0 }

S2 = [

# ---- 1. THE REAL ULT BLOCK --------------------------------------------------

("ult block",
 '''    ult:{ name:"%ULT%", charge:1e9, kind:"static", tip:"%TIP1%" },''',
 '''    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"static",
          /* ONE TIMER AND NOT TWO. Rick's section 1 names "another timer"
             after the window opens; the design priced both readings and one
             moment is the stronger of the two -- stopping the spawns early and
             letting the swarm fly on only thins the finale (2.73 bolts in the
             blast against 2.97). So `dur` is the whole ultimate: spawning
             stops and every bolt detonates on the same frame. */
          dur:%DUR%,
          /* THE SPARK. Eight bolts born AT THE FOE on every blade hit the
             caster lands inside the window -- and 8-12% of casts see no blade
             hit at all and produce NOTHING. That is the mechanic (a storm
             needs a spark) and the brief says in as many words not to add a
             fallback spawn. */
          per:%PER%, r:%R%, speed:%SPEED%, ric:%RIC%,
          /* "FORK INTO TWO MORE", LITERAL: three bolts leave the foe where one
             arrived, because the arriving bolt LIVES ON with its ricochets
             refreshed. Fork +1 is a different relic -- the swarm never grows
             and peaks at 7 (design section 3). */
          fork:%FORK%, grace:%GRACE%, cap:%CAP%,
          ward:%WARD%, blast:%BLAST%, dmg:%BOLTDMG%,
          tip:"%TIP1%" },'''),

# ---- 2. THE MATCH CARRIES ONE STORM -----------------------------------------

("match state",
 '''    this.tornado = null;
    this.clankCd = 0;''',
 '''    this.tornado = null;
    /* THE STORM, AND IT IS ON THE MATCH FOR THE SAME REASON THE TORNADO IS.
       `ultFx` is ONE SLOT -- the opponent casting anything overwrites it and
       that cast's own shorter `life` then nulls it, measured at 0.0% survival
       against Ironhail for a window ultimate (v54 section 2a, chain-wide open
       item 25). An eight-second swarm whose picture can be erased by somebody
       else's nova is a swarm nobody can see. So the bolts are SIM OBJECTS and
       they are drawn off themselves.

       ONE STORM AND NOT ONE PER FIGHTER: a relic cannot fight itself and there
       is exactly one relic in the roster with `kind:"static"`, so two storms
       can never exist at once. `S.src` still says whose it is, because every
       test in `tickStatic` is asymmetric -- the foe forks a bolt and the caster
       eats it. */
    this.storm = null;
    this.clankCd = 0;'''),

("match over",
 '''    if (this.over && this.tornado) this.tornado = null;''',
 '''    if (this.over && this.tornado) this.tornado = null;
    /* AND NEITHER DOES THE STORM. Thirty bolts still ricocheting over a corpse
       is not a final image, it is a thing nobody turned off -- and the
       detonation is explicitly gated on both fighters being alive, so a swarm
       that outlived the match would be a swarm that could never pay. */
    if (this.over && this.storm) this.storm = null;'''),

# ---- 3. THE CAST ------------------------------------------------------------

("cast",
 '''      if (this.ultFx) this.ultFx.life = u.dur;
      return;
    }
    if (u.kind === "breach"){''',
 '''      if (this.ultFx) this.ultFx.life = u.dur;
      return;
    }

    if (u.kind === "static"){
      /* NOTHING RESOLVES HERE, AND NOTHING IS SPAWNED HERE EITHER. The cast
         opens a window and that is all: the storm is grown from the caster's
         own blade hits inside it, so a cast that lands no blow produces no
         bolts and detonates on nothing. Measured at 8-12% of casts, and the
         brief forbids a fallback spawn -- "that is the mechanic. A storm needs
         a spark."

         THE COUNTERS ARE NOT DECORATION. `spawned`, `forked`, `eaten`, `died`,
         `walls`, `peak` and `refused` are gate 2: the brief publishes the live
         model's per-cast means (spawn ~17-20, fork ~30, eaten ~21, alive ~24,
         peak ~30, cap never reached) and a build within ~25% of them is the
         same swarm. A build that peaks near 7 has fork +1 or thin bolts. */
      this.storm = { src: f === this.a ? "a" : "b",
                     t: 0, dur: u.dur, bolts: [], born: 0,
                     blows: 0, spawned: 0, forked: 0, eaten: 0, died: 0,
                     walls: 0, refused: 0, peak: 0,
                     banked: 0, dealt: 0, hits: 0, filed: 0 };
      /* THE SET-PIECE'S CLOCK IS THE WINDOW'S, the way Aegis, the Thicket, the
         ballista, the Stasis Field, the Winnowing, the Sentinel and the
         tornado all set it at their own cast sites rather than from the `life`
         map. */
      if (this.ultFx) this.ultFx.life = u.dur;
      return;
    }
    if (u.kind === "breach"){'''),

# ---- 4. AND IT IS TICKED ----------------------------------------------------

("tick order",
 '''    this.tickScour(dt);
    this.tickBallista(dt);''',
 '''    this.tickScour(dt);
    /* WITH THE OTHER WINDOW TICKERS, and after the fighter loop that moved both
       balls -- a bolt is tested against where the two shells ARE, and a fork or
       an eat resolved against last frame's positions is a contact that did not
       happen. Before `tickHits` for the reason `tickWinnow`, `tickBreach` and
       `tickScour` all give.

       ON THE NORMAL STEP PATH AND NOT IN `tickPresentation`, which is the
       opposite of Deadfall's flash and Grasp's crush: the bolts are the
       SIMULATION -- they fork, they are eaten, and they detonate for damage --
       so they must freeze with everything else through a hit stop. The brief
       says so in one line: "bolts advance by the ordinary step and freeze with
       everything else." */
    this.tickStatic(dt);
    this.tickBallista(dt);'''),

# ---- 5. THE TICKER ITSELF ---------------------------------------------------

("ticker",
 '''  tickScour(dt){
    const T = this.tornado;''',
 '''  /* ------------------------------------------------------------ THE STORM ---
     Rick's section 1, clauses 1-5: bolts are born at the foe on the caster's
     own hits, they ricochet off the walls several times and vanish, a bolt that
     touches the FOE forks into two more and has its ricochets refreshed, and a
     bolt that touches the CASTER is consumed. Clause 7 -- the detonation -- is
     stage 3 and is not here.

     THE GROWTH IS THE FORK AND THE BRAKE IS THE CASTER, which is what makes
     this a swarm that fills the arena rather than one that explodes. A blade
     hit means the caster is standing ~100 units from the foe, and the bolts are
     born AT the foe, so a third of them are eaten within half a second of birth
     (design section 2). Fork and eat run at about the same rate and the swarm
     settles near 30 -- the cap of 60 is a safety and never binds. */
  stormBolt(S, u, x, y){
    /* THE DIRECTION COMES FROM THE MATCH'S OWN SEEDED STREAM. `Math.random`
       anywhere in this ultimate breaks determinism, and determinism is what
       every recorded number in this repo rests on -- brief section 3, trap 1,
       "the first thing to check". */
    const a = this.rng() * TAU;
    S.born++;
    return { x, y, a, vx: Math.cos(a) * u.speed, vy: Math.sin(a) * u.speed,
             ric: u.ric, grace: u.grace, n: S.born, t: 0 };
  }

  tickStatic(dt){
    const S = this.storm;
    if (!S) return;
    const src = S.src === "a" ? this.a : this.b;
    const foe = S.src === "a" ? this.b : this.a;
    const u = src.w.ult;
    S.t += dt;
    /* STAGE 2 CLEARS THE SWARM AND PAYS NOTHING. Stage 3 detonates here. */
    if (S.t >= S.dur){ this.storm = null; return; }

    const A = CONFIG.arena, n = this.inset, R = CONFIG.physics.ballR;
    const B = S.bolts;
    /* DOWNWARD, because an eaten bolt is spliced out and a fork pushes two more
       onto the END -- so the new ones are past the iterator and cannot fork or
       be eaten on the frame they were born. Their `grace` would refuse a fork
       anyway; this makes it structural as well. */
    for (let i = B.length - 1; i >= 0; i--){
      const b = B[i];
      b.t += dt;
      b.x += b.vx * dt; b.y += b.vy * dt;
      if (b.grace > 0) b.grace -= dt;

      /* --- THE WALLS, AND THEY ARE THE ONLY GEOMETRY A BOLT KNOWS. It passes
         through shots, through weapons and through clanks: brief section 0,
         "only walls, foe and caster exist to them". That is not an omission --
         a parry-able bolt would hand every spinning weapon in the game a
         counter to an ultimate that deals no damage until it ends.

         NO SPEED LOSS ON A BOUNCE. `tickShots` damps an arrow by 0.88 a wall
         and this deliberately does not: the design's whole swarm was measured
         at a constant 600, and a bolt that slowed would sit in the corner it
         was born near instead of crossing the room. */
      let wall = false;
      if (b.x < n + u.r){ b.x = n + u.r; b.vx = Math.abs(b.vx); wall = true; }
      else if (b.x > A.w - n - u.r){ b.x = A.w - n - u.r; b.vx = -Math.abs(b.vx); wall = true; }
      if (b.y < n + u.r){ b.y = n + u.r; b.vy = Math.abs(b.vy); wall = true; }
      else if (b.y > A.h - n - u.r){ b.y = A.h - n - u.r; b.vy = -Math.abs(b.vy); wall = true; }
      if (wall){
        /* SIX RICOCHETS, AND THE SEVENTH WALL KILLS IT. "Ricochet several
           times before disappearing" -- and 6 is within a bolt of unlimited on
           the finale (design section 3), so the clause survives its own
           measurement rather than being kept out of loyalty to the sentence. */
        if (b.ric <= 0){ B.splice(i, 1); S.died++; continue; }
        b.ric--; S.walls++;
        b.a = Math.atan2(b.vy, b.vx);
        SFX.play("wall");
      }

      /* --- THE FOE. FORK, REFRESH, AND NO DAMAGE. Section 1 names a fork and
         a refresh for this contact and nothing else; the only damage in the
         whole ultimate is the detonation. The design read it that way before
         anything was priced and the brief carries it in capitals.

         THE GRACE IS WHY THIS TERMINATES. A bolt born on the foe is INSIDE the
         foe, so without it every spawn forks on its first frame and the cap
         binds on the first blade hit -- the overlay showed exactly that before
         the grace went in (brief trap 2). 0.30s after birth OR after a fork,
         which at 600 px/s is 180 units of travel: far enough that a bolt has
         to come back to fork again. */
      if (foe.alive && !this.over && b.grace <= 0 && !foe.shade
          && Math.hypot(b.x - foe.x, b.y - foe.y) < R + u.r){
        b.ric = u.ric;
        b.grace = u.grace;
        for (let k = 0; k < u.fork; k++){
          /* THE CAP DECLINES, IT DOES NOT SHIFT. A shift inside the loop this
             ticker is running would move every index under the iterator --
             Thornshear's fork learned that, and the protection is the same
             without the corruption. At these numbers it never fires (peak ~30
             against 60) and `refused` is printed so that stays checkable. */
          if (B.length >= u.cap){ S.refused++; break; }
          B.push(this.stormBolt(S, u, foe.x, foe.y));
          S.forked++;
        }
        /* THE FOE IS TESTED FIRST AND A CONTACT IS ONE THING. In melee the two
           shells can both be inside a bolt's 50 units; without this the same
           bolt would fork on the quarry and then be eaten by the caster on one
           frame, which is a bolt paying twice. */
        continue;
      }

      /* --- THE CASTER. CONSUMED. Stage 3 banks the ward here; at stage 2 the
         bolt simply goes, so the swarm's shape -- which is what gate 2
         measures -- is already the shipped one. */
      if (src.alive && Math.hypot(b.x - src.x, b.y - src.y) < R + u.r){
        B.splice(i, 1); S.eaten++;
        continue;
      }
    }
    if (B.length > S.peak) S.peak = B.length;
  }

  tickScour(dt){
    const T = this.tornado;'''),

# ---- 6. THE SPARK -- A BLADE HIT INSIDE THE WINDOW ---------------------------

("spawn hook",
 '''    if (mul === undefined && self.ultRadiant && self.w.ult.sparks)
      for (let i = 0; i < self.w.ult.sparks; i++) this.spawnSpark(self, hx, hy);
''',
 '''    if (mul === undefined && self.ultRadiant && self.w.ult.sparks)
      for (let i = 0; i < self.w.ult.sparks; i++) this.spawnSpark(self, hx, hy);

    /* STATIC: A BLADE HIT INSIDE THE WINDOW THROWS EIGHT BOLTS OFF THE QUARRY.
       Rick: "when the artifact lands a hit several lightning bolts arch off the
       enemy fighter and begin to bounce around the arena."

       `mul === undefined` IS AN ORDINARY MELEE CONNECT and not a projectile --
       the same test Ironbloom's latch, the Crucible's strike, Garrote's
       connect, Deadfall's stamp and Revenant's sling all use. It is doing real
       work here rather than following a habit: stage 3's detonation is fifteen
       damage a bolt routed through this very function, and without this test a
       detonation landing inside a still-open window would spawn a second storm
       out of the first one's payoff.

       AT THE FOE, NOT AT THE POINT OF IMPACT. The bolts "arch off the enemy
       fighter"; a blade contact is up to 62 units out from the shell, and born
       there they would miss the quarry they are supposed to fork on.

       A DEAD QUARRY GROWS NOTHING and neither does a shade. `foe.alive` is
       tested after `resolveHit` has already resolved the damage, so a killing
       blow ends the storm's growth rather than seeding it -- Twinshade's
       precedent, where a blade does not stick into a corpse. Shades are
       excluded for the reason `tickStatic` gives: the bolts test the real foe
       and the caster and nothing else, so a swarm grown off a copy would fork
       on a body that is not there. */
    if (mul === undefined && this.storm && foe.alive && !foe.shade
        && !this.over && this.storm.src === (self === this.a ? "a" : "b")){
      const S = this.storm, U = self.w.ult;
      S.blows++;
      for (let i = 0; i < U.per; i++){
        if (S.bolts.length >= U.cap){ S.refused++; break; }
        S.bolts.push(this.stormBolt(S, U, foe.x, foe.y));
        S.spawned++;
      }
      if (S.bolts.length > S.peak) S.peak = S.bolts.length;
    }
'''),

# ---- 7. THE SIGIL -----------------------------------------------------------

("sigil",
 '''const ULTSIG = {
  /* SCOUR -- a funnel, turning, under a halo.''',
 '''const ULTSIG = {
  /* STATIC -- one bolt, forking. At HUD size a storm has to be read from a
     SINGLE stroke that splits, because thirty overlapping zigzags at 20px is a
     smudge: a jagged spine down the badge, two forks off it, and a ring that
     tightens as the charge fills so the sigil says "about to let go". */
  arclight(c, t, cf, P){
    const zig = (x0, y0, x1, y1, k, col, w, al) => {
      const pts = [];
      for (let i = 0; i <= 4; i++){
        const u = i / 4;
        const off = i === 0 || i === 4 ? 0
                  : Math.sin(u * 9.4 + k * 2.1 + t * 6) * 0.13;
        pts.push([x0 + (x1 - x0) * u - off * (y1 - y0),
                  y0 + (y1 - y0) * u + off * (x1 - x0)]);
      }
      SG.path(c, pts, col, w, al);
    };
    zig(-0.12, -0.86, 0.10, 0.30, 0, P.core, 0.10, 0.45 + cf * 0.5);
    zig(0.06, -0.10, 0.62, 0.52, 1, P.glow, 0.07, 0.35 + cf * 0.5);
    zig(0.04, 0.02, -0.52, 0.70, 2, P.glow, 0.07, 0.35 + cf * 0.5);
    SG.ring(c, 0, 0, 0.94 - cf * 0.26, P.glow, 0.05, 0.25 + cf * 0.6);
  },
  /* SCOUR -- a funnel, turning, under a halo.'''),

# ---- 8. AND THE BOLTS ARE DRAWN, OFF THEMSELVES -----------------------------

("draw call",
 '''    this.drawShots(m);
    this.drawHands(m);''',
 '''    this.drawShots(m);
    /* OVER the fighters, with the arrows: a bolt is an object crossing the
       room, not a hazard the balls are standing inside. */
    this.drawStorm(m);
    this.drawHands(m);'''),

("draw",
 '''  drawScour(m, over){
    const T = m.tornado;''',
 '''  /* THE STORM. A FIRST CUT AND NOTHING MORE -- brief stage 5 says the bolt's
     look is Rick's, from a rendered strip of three or four styles, and he has
     not been asked. What is here is the minimum that lets stage 2 be FILMED:
     the swarm has to be countable and its bolts have to read as lightning
     rather than as pink dots, or the gate-2 question ("does the arena read as
     full of pink lightning by the fourth second") cannot be answered at all.

     `r` 16 IS THE HIT VOLUME AND NOT THE PICTURE. A 32-pixel ball drawn at the
     test radius would be a bead; a jagged streak of about that width across is
     the same volume drawn as the thing it is. `drawVents` is the standing
     warning in the other direction -- a beam drawn WIDER than it tests looks
     like it connected when it did not -- so this stays inside its own contact
     radius. */
  drawStorm(m){
    const S = m.storm;
    if (!S || !S.bolts.length) return;
    const P = AFFINITIES.vigil;
    const c = this.ctx;
    const src = S.src === "a" ? m.a : m.b;
    const u = src.w.ult;
    /* ONE DETERMINISTIC HASH, standing in for the randomness this must not
       have -- `spawnFx` draws twice from `this.rng()` per particle and a
       renderer that drew from the match stream would move every Arclight
       fight. Index in, a number in [0,1) out. */
    const h1 = (k) => { const x = Math.sin(k * 127.1 + 311.7) * 43758.5453;
                        return x - Math.floor(x); };
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round";
    c.lineJoin = "round";
    for (const b of S.bolts){
      const len = u.r * 2.6;
      const dx = Math.cos(b.a), dy = Math.sin(b.a);
      /* THE ZIGZAG IS A FUNCTION OF THE BOLT AND THE CLOCK, so a bolt flickers
         in place instead of the whole swarm strobing together. */
      const ph = Math.floor(m.t * 22) + b.n * 7;
      const pts = [];
      for (let i = 0; i <= 3; i++){
        const s = (i / 3 - 0.5) * len;
        const off = i === 0 || i === 3 ? 0 : (h1(ph + i * 3.3) - 0.5) * u.r * 1.5;
        pts.push([b.x + dx * s - dy * off, b.y + dy * s + dx * off]);
      }
      /* A NEW BOLT FLASHES. The birth is the one event in this ultimate a
         viewer can attribute to a blade hit, and eight of them arrive at once. */
      const young = Math.max(0, 1 - b.t / 0.22);
      for (const [w, col, al] of [[u.r * 0.95, P.dark, 0.30],
                                  [u.r * 0.55, P.core, 0.55 + young * 0.35],
                                  [u.r * 0.20, P.glow, 0.85]]){
        c.strokeStyle = col;
        c.lineWidth = w;
        c.globalAlpha = al;
        c.beginPath();
        c.moveTo(pts[0][0], pts[0][1]);
        for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
        c.stroke();
      }
      if (young > 0){
        c.globalAlpha = young * 0.7;
        c.fillStyle = P.glow;
        c.beginPath();
        c.arc(b.x, b.y, u.r * (0.5 + young * 0.8), 0, TAU);
        c.fill();
      }
    }
    c.restore();
  }

  drawScour(m, over){
    const T = m.tornado;'''),

]


# ------------------------------------------------------------------ stage 3 --
#
# THE WARD AND THE DETONATION. THIS IS THE RELIC -- and it is the first thing in
# the vigil school that PAYS INTO the shield rather than spending it: Aegis
# reflects it, Reprisal fires it, Sentinel drinks it. That separation was in
# Rick's fourth sentence before anything was measured.

S3 = [

# ---- 1. RICK'S CARD LINE, WITH THE MECHANIC IT DESCRIBES --------------------

("tip",
 '''          ward:%WARD%, blast:%BLAST%, dmg:%BOLTDMG%,
          tip:"%TIP1%" },''',
 '''          ward:%WARD%, blast:%BLAST%, dmg:%BOLTDMG%,
          /* RICK'S OWN LINE, 2026-09-02, and it is EXACTLY at `verify`'s 72.
             He wrote "Hits spawn forking lightning. Bolts hitting #name# apply
             ward. bolts explode after X seconds" (94 filled in), was shown the
             cap, called the first trim's middle sentence "pretty rough", and
             took this middle from four. Every word but "caught" is his.

             ONE STRING, BOTH SURFACES -- the ult-bar reminder and the scrunch
             panel read the same field, and v53 settled that CHARACTERS are the
             wrong unit for either box: `tip_audit` measures pixels and is the
             gate that protects the layout. This one is at the cap, so it is
             measured on both before stage 5 closes. */
          tip:"%TIP%" },'''),

# ---- 2. THE EAT BANKS THE WARD ----------------------------------------------

("the eat banks",
 '''      if (src.alive && Math.hypot(b.x - src.x, b.y - src.y) < R + u.r){
        B.splice(i, 1); S.eaten++;
        continue;
      }''',
 '''      if (src.alive && Math.hypot(b.x - src.x, b.y - src.y) < R + u.r){
        B.splice(i, 1); S.eaten++;
        /* THE HARVEST, AND IT IS THE SCHOOL'S OWN CHANNEL RUN BACKWARDS.
           `resolveHit`'s vigil branch is the reference and these are its
           fields in its order: raise the pool under the cap, keep the
           high-water mark the shatter scales to, and re-apply the status so
           the 5-second clock restarts. Two a bolt and ~21 bolts a cast is ~35
           of a 90 cap, with about 2 lost to the ceiling -- and the ceiling is
           NOT raised for this relic (brief trap 7).

           THE FEED IS CONTINUOUS AND THAT IS WHY IT WORKS. The school's oldest
           measured problem is that the pool at a cast is a MEDIAN OF ZERO --
           charge is wall time, the plate is up 42% of the fight, and the two
           are uncorrelated -- so Aegis and Sentinel both had to move to
           feeding while the ultimate stands. This one is fed by its own storm
           for the whole eight seconds.

           IF THIS RELIC EVER GETS AN AEGIS-LIKE WALL THE BANK MUST GO TO IT
           (brief stage 3). It does not have one today, so there is no
           `ultAegis` branch here -- and adding one blind would be a second
           destination for a payment nobody has measured. */
        if (src.alive){
          const Wd = STATUS.ward;
          const was = src.shield;
          src.shield = Math.min(Wd.cap, src.shield + u.ward);
          src.shieldMax = Math.max(src.shieldMax, src.shield);
          src.apply("ward", 1);
          const got = Math.round(src.shield - was);
          S.banked += src.shield - was;
          /* A BOLT GOING INTO THE SHELL IS THE HALF OF THIS FIGHTER THAT IS
             OTHERWISE INVISIBLE (brief stage 5). The float is the same one the
             blade's own bank prints, in the same colour and at the same place,
             because it is the same event arriving by another road. */
          if (got >= 1){
            const first = !this.taught.ward && !!STATUS.ward.tip;
            if (first) this.taught.ward = true;
            this.statusTag(src.x, src.y, "ward", first);
            this.float(src.x, src.y - 44, "+" + got,
                       AFFINITIES.vigil.glow, 22 + got * 0.5);
          }
        }
        continue;
      }'''),

# ---- 3. THE DETONATION ------------------------------------------------------

("detonate",
 '''    /* STAGE 2 CLEARS THE SWARM AND PAYS NOTHING. Stage 3 detonates here. */
    if (S.t >= S.dur){ this.storm = null; return; }''',
 '''    if (S.t >= S.dur){ this.stormBlow(S, src, foe, u); return; }'''),

("blow",
 '''  tickStatic(dt){
    const S = this.storm;''',
 '''  /* --------------------------------------------------------- THE DETONATION
     Section 1, clause 7: "when the timer ends all the lightning bolts explode
     in a small area for damage and expire."

     THE WHOLE CAST IS PRICED BY ONE FRAME. The payoff is not the bolt COUNT --
     it is how many of them happen to be within `blast` of the quarry at the
     instant the timer ends, which is a lottery whose odds are the radius: at 80
     the median cast catches 4 and 18% catch nothing at all. `blast` 80 is
     RICK'S, about the twinblade's own reach, over his own "small" 50 (blank a
     third of the time) and over 100.

     ONE EVENT, NOT TWENTY-FOUR (brief trap 6). Every bolt's hit is resolved
     with `stop:0, stun:false, beat:false`, and the freeze, the shake, the ring
     and the beat are filed ONCE after the loop. Twenty-four beats would be the
     director scoring one moment twenty-four times; twenty-four hit stops would
     be a two-second freeze. */
  stormBlow(S, src, foe, u){
    const R = CONFIG.physics.ballR;
    /* COUNTED BEFORE ANYTHING RESOLVES. `resolveHit` knocks, kills and can
       shatter a ward, all of which move the quarry -- so a loop that measured
       distance as it went would price the later bolts against a body the
       earlier ones had already thrown. */
    const inside = [];
    for (const b of S.bolts)
      if (Math.hypot(b.x - foe.x, b.y - foe.y) < R + u.blast) inside.push(b);
    S.inBlast = inside.length;
    /* EVERY BOLT POPS AND ONLY THE ONES INSIDE ARE PAID. "All the lightning
       bolts explode" is the sentence, and both halves of it matter: a swarm
       that vanished silently would end the ultimate on nothing, and a swarm
       that popped only where it hurt would draw the blast radius as a ring of
       survivors. RINGS AND NOT `spawnFx` -- `spawnFx` draws twice from
       `this.rng()` per particle and thirty of them would move every Arclight
       fight, which is Breach's sparks learning it the expensive way. */
    for (const b of S.bolts)
      this.ring(b.x, b.y, AFFINITIES.vigil.glow, 3, u.r * 2.2, 0.22, 3);

    /* NOTHING FIRES OVER A CORPSE, in either direction (brief stage 3). */
    if (foe.alive && src.alive && !this.over && inside.length){
      const before = foe.hp;
      for (const b of inside){
        /* A SEGMENT ALONG THE BOLT'S OWN TRAVEL. `resolveHit` reads
           `seg.bx - seg.ax` unconditionally, to fly the impact sparks ALONG
           the blade rather than outward from the point, so a null throws on
           the first detonation that ever lands -- and it throws inside the
           step, which kills the match rather than the frame. Every projectile
           call site synthesises one. */
        const cs = Math.cos(b.a) * 10, sn = Math.sin(b.a) * 10;
        const seg = { ax: b.x - cs, ay: b.y - sn,
                      bx: b.x + cs, by: b.y + sn, a: b.a };
        /* `mul` IS DEFINED, which makes this a projectile-class hit rather
           than a melee connect, and `u.dmg / src.w.dmg` is how a call site
           states its own base damage through a function that scales the
           WEAPON's blade. That is not bookkeeping: it is what keeps
           Ironbloom's latch, the Crucible's strike, Garrote's connect,
           Deadfall's stamp, Revenant's sling AND THIS RELIC'S OWN SPAWN HOOK
           from firing off a detonation -- every one of them tests
           `mul === undefined`. Without it a detonation landing inside a still
           open window would seed a second storm out of the first one's payoff.

           EVERYTHING ELSE ABOUT IT IS AN ORDINARY BLOW, which is the whole of
           "through the ordinary damage path": crit and jitter are rolled, the
           Sunder multiplier reads, the quarry's OWN ward absorbs it first, and
           the vigil channel banks 0.55 of what lands. The design priced this
           through `m.hurt`, which skips all four, and declared the gap -- gate
           3 and gate 6 write down what it turned out to be. */
        this.resolveHit(src, foe, b.x, b.y, seg, u.dmg / src.w.dmg,
                        { knock: 0, stop: 0, stun: false, beat: false });
        S.hits++;
        /* A CORPSE TAKES NO MORE BOLTS. The fatal one files its own beat inside
           `resolveHit` -- `over.beat` does not silence a kill -- so the
           director still sees the kill even though this loop is silent. */
        if (!foe.alive) break;
      }
      /* HP AND NOT INTENT. A ward that absorbed the blast means the relic did
         less to this fighter than fifteen a bolt, and the beat should be
         scored on what actually happened. */
      S.dealt += Math.max(0, before - foe.hp);
      this.hitStop = Math.max(this.hitStop, 0.10);
      this.shake = Math.min(44, this.shake + 26);
      this.ring(foe.x, foe.y, AFFINITIES.vigil.core, 6, R + u.blast, 0.34, 6);
      /* THE DIRECTOR (CLAUDE.md section 3 rule 3), and it is the one beat this
         ultimate files. `cinePlan` scores an ultimate off the beats filed for
         it; a payload that resolves with `beat:false` twenty-four times over
         would be scored as empty air, which is the hole five relics since
         Vesper have had to close by hand. */
      this.beat({ kind: "hit", side: src === this.a ? 0 : 1,
                  x: foe.x, y: foe.y, dmg: S.dealt, crit: false,
                  fatal: !foe.alive, hpAfter: Math.max(0, foe.hp),
                  hpFrac: Math.max(0, foe.hp) / foe.maxHp,
                  maxHp: foe.maxHp, selfHpFrac: src.hp / src.maxHp,
                  spd: src.speed, foeSpd: foe.speed,
                  close: Math.hypot(src.vx - foe.vx, src.vy - foe.vy),
                  ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                  shotSpd0: 0 });
      S.filed = 1;
    }
    this.storm = null;
  }

  tickStatic(dt){
    const S = this.storm;'''),

]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=("1", "2", "3"))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=TUNED_AL or BLADE)
    ap.add_argument("--charge", type=float, default=ULT_CHARGE)
    for k, v in ULT.items():
        ap.add_argument(f"--{k}", type=float, default=float(v))
    A = ap.parse_args()

    src = A.src or {"1": "../02-chain/sc-lastthree.html",
                    "2": "../02-chain/sc-arclight.html",
                    "3": "../02-chain/sc-storm.html"}[A.stage]
    out = A.out or {"1": "../02-chain/sc-arclight.html",
                    "2": "../02-chain/sc-storm.html",
                    "3": "../02-chain/sc-static.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nARCLIGHT -- STAGE " + A.stage + ": "
          + {"1": "the 34th relic, its ultimate STUBBED",
             "2": "THE STORM EXISTS -- no ward, no damage",
             "3": "THE WARD AND THE DETONATION -- THIS IS THE RELIC"}[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR. Every stage asserts what has to be under it.
    if 'id:"duskreave"' not in s0:
        raise SystemExit(
            "this source is not the Duskreave tip -- no `duskreave` in it.\n"
            "  Arclight is the 34th relic and builds on the 33rd; if the\n"
            "  intention is to build it somewhere else, say so with --src and\n"
            "  say why in the write-up, because the relic count in every doc\n"
            "  moves with it.")
    if A.stage == "1" and f'id:"{RELIC}"' in s0:
        raise SystemExit("this source already has Arclight -- built")
    if A.stage == "2":
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("stage 2 needs stage 1's link -- no Arclight in "
                             "this source")
        if "charge:1e9" not in body_block(s0, RELIC, "ult"):
            raise SystemExit(
                "the ultimate in this source is not stubbed, so stage 2 has\n"
                "  already run against it. Rebuild stage 1 first -- a stage\n"
                "  applied twice is how a builder writes numbers its own log\n"
                "  does not describe.")

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

    # THE SCHOOL'S CHANNEL IS COPIED, NOT INVENTED -- AND THE BRIEF'S SENTENCE
    # ABOUT IT IS NOT QUITE TRUE. Brief section 0: `onSelf { ward: 1 }`, "the
    # school's channel, exactly as the other four vigil carry it". Three of them
    # do. FARWARDEN CARRIES 2.5, and its own comment says why: `onSelf`'s value
    # is a per-relic bank multiplier (`resolveHit` banks `dmg * W.bank * n`),
    # ward was designed on a greatsword landing 30-point blows, and a bow deals
    # ~11 a hit three times in a 5-second window, so at n=1 its pool topped out
    # near 20 of a 90 cap.
    #
    # The NUMBER the brief gives is still right for this relic and is not this
    # session's to move: the twinblade is the fastest weapon in the game, the
    # design measured this body at 57-60% with `ward:1` and nothing else, and
    # every price in `06-docs/v64/` is on that setting. What is checked here is
    # therefore the three MELEE vigil relics, with the bow named as the
    # deliberate exception rather than silently averaged in.
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

    if A.stage == "3":
        if "kind:\"static\"" not in strip_comments(s0):
            raise SystemExit("stage 3 needs stage 2's link -- no storm in this "
                             "source")
        if "stormBlow" in strip_comments(s0):
            raise SystemExit(
                "this source already detonates -- stage 3 has run against it. "
                "A stage applied twice is how a builder writes numbers its "
                "own log does not describe.")

    table = {"1": S1, "2": S2, "3": S3}[A.stage]

    # THE ANCHOR IS SUBSTITUTED TOO. Stage 2's anchors quote text stage 1
    # WROTE, and stage 1 wrote it with the placeholders already filled in -- so
    # an un-substituted anchor can never match its own builder's output.
    def fill(txt):
        txt = (txt.replace("%DMG%", f"{A.dmg:g}")
                  .replace("%ULT%", A.ult)
                  .replace("%TIP1%", ULT_TIP1)
                  .replace("%TIP%", A.tip)
                  .replace("%BLURB%", BLURB)
                  .replace("%CHARGE%", f"{A.charge:g}"))
        for k in ULT:
            txt = txt.replace(f"%{k.upper()}%", f"{getattr(A, k):g}")
        return txt

    for label, old, new in table:
        s = one(s, fill(old), fill(new), label)

    # TRAP 1, AND IT IS THE FIRST THING THE BRIEF SAYS TO CHECK. `Math.random`
    # anywhere in the storm breaks `engine_ab`, and it breaks it silently --
    # the page runs, the fight looks fine, and two runs of one seed differ.
    # STRIPPED FIRST, because a check that cannot tell code from the comment
    # explaining it fires on its own explanation (`curse_check` and
    # `curse_build`, both on the same day in v53).
    if A.stage in ("2", "3"):
        code = strip_comments("".join(
            n for _, _, n in {"2": S2, "3": S3}[A.stage]))
        if "Math.random" in code:
            raise SystemExit(
                "REFUSING TO WRITE -- the storm calls `Math.random`. Bolt\n"
                "  directions come from the match's own seeded stream "
                "(`this.rng`).")
        if "spawnFx" in code.split("drawStorm")[0]:
            raise SystemExit(
                "REFUSING TO WRITE -- the storm calls `spawnFx`, which draws\n"
                "  twice from `this.rng()` per particle. Breach's sparks had to\n"
                "  become DRAWN rather than spawned for exactly this reason.")
        if "drawStorm(m)" in code and "this.rng()" in code.split("drawStorm(m)")[1]:
            raise SystemExit(
                "REFUSING TO WRITE -- `drawStorm` draws from the match's rng.\n"
                "  A renderer that spends from the sim's stream moves every\n"
                "  fight it draws.")
        print("  ok    no Math.random, no spawnFx in the swarm, no rng in the "
              "renderer")

    ult_matches(s, A, A.stage)

    if len(A.tip) > 72:
        raise SystemExit(f"the card line is {len(A.tip)} characters against "
                         f"`verify`'s 72. It is Rick's line and it is not this "
                         f"session's to cut (CLAUDE.md 3 rule 2).")
    print(f"  tip   Rick's line is {len(A.tip)} characters against a cap of 72")
    if A.stage == "3" and f'tip:"{A.tip}"' not in s:
        raise SystemExit("REFUSING TO WRITE -- the shipped tip is not the line "
                         "this run printed.")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"  {len(s)} bytes")
    print(f"  relic dmg {A.dmg:g}, onSelf ward 1, ult {A.ult} "
          + (f"STUBBED (charge 1e9, kind {ULT_KIND})" if A.stage == "1"
             else f"LIVE (charge {A.charge:g}, kind {ULT_KIND})"))

    if A.stage == "3":
        print(f"  the eat banks {A.ward:g} ward a bolt under the 90 cap; the "
              f"detonation is {A.boltdmg:g} a bolt inside {A.blast:g}")
        print("  through resolveHit and NOT m.hurt, so crit, jitter, Sunder,")
        print("    the quarry's OWN ward and the vigil bank all read -- the")
        print("    design priced it through `hurt` and DECLARED the gap")
        print("  ONE hit stop, ONE beat, ONE ring for the whole detonation")
        print("\n  GATE 3 -- the four-arm budget shape, on the BUILT relic:")
        print("    python arclight_probe.py --game ../02-chain/sc-static.html")
        print("      ward a cast ~35, damage a cast ~60, casts with no")
        print("      detonation damage ~18%")
        print("    python arclight_price.py --game ../02-chain/sc-static.html")
        print("      B-A in the +16 tier, C-A in the +25, D-A in the +33,")
        print("      each +/-6pp at 250 fights. A D-A over +45 or under +20 is")
        print("      a different relic -- STOP and say what changed.")
        print("    python engine_ab.py --a ../02-chain/sc-storm.html \\")
        print("      --b ../02-chain/sc-static.html --ids <the 33> --n 8")
        return 0

    if A.stage == "2":
        print(f"  storm dur {A.dur:g}s, {A.per:g} bolts a blade hit at r "
              f"{A.r:g}, {A.speed:g} px/s, {A.ric:g} ricochets, fork "
              f"+{A.fork:g}, grace {A.grace:g}s, cap {A.cap:g}")
        print(f"  ward {A.ward:g}, blast {A.blast:g}, {A.boltdmg:g} a bolt -- "
              "WRITTEN AND INERT until stage 3")
        print("  the bolts are a SIM OBJECT on `m.storm` and are drawn off")
        print("    themselves, so an opponent's cast cannot erase them")
        print("\n  GATE 2 -- and the first one is Rick's eye:")
        print("    FILM 3 CASTS ON 3 SEEDS, BEFORE ANY TUNING. The arena must")
        print("      read as full of pink lightning by the 4th second of the")
        print("      cast. CLAUDE.md 4.0.")
        print("    python arclight_probe.py --game ../02-chain/sc-storm.html")
        print("      per cast: spawned ~17-20, forked ~30, eaten ~21, alive at")
        print("      the end ~24, peak ~30, cap NEVER reached. Within ~25% of")
        print("      those is the same swarm; a peak near 7 is fork +1 or thin")
        print("      bolts -- STOP.")
        print("    python engine_ab.py --a ../02-chain/sc-arclight.html \\")
        print("      --b ../02-chain/sc-storm.html --ids <the 33> --n 8")
        print("      IDENTICAL on every pairing with no Arclight in it.")
        return 0

    print("\n  GATE 1 -- run all three, and each can fail:")
    print("    python engine_ab.py --a ../02-chain/sc-lastthree.html "
          "--b ../02-chain/sc-arclight.html --n 10")
    print("    python verify.py --game ../02-chain/sc-arclight.html --n 40")
    print("    the no-ult win rate against the roster WITH their ultimates")
    print("      live, expected 57-60% at dmg 11.95 and a few points under at")
    print("      8.3 (brief gate 1). NEAR 10% MEANS THE WARD CHANNEL IS NOT")
    print("      WIRED; near 80% means something is firing that should not.")
    print("    AND FILM THE SILHOUETTE -- `_tbPlated` has never been drawn.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
