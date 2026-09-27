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
    ap.add_argument("--stage", choices=["1", "2"], required=True)
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
    else:
        if "ultEcho" not in code:
            raise SystemExit("stage 2 needs stage 1 under it -- no echo here")
        if strip_comments(ult1) in code:
            raise SystemExit("this source already carries stage 2 -- built")
        edits = S2

    for label, old, new in edits:
        s = one(s, old, new, label)

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
    for label, _old, new in S1:
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

    syntax_check(s, out_p.name)
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
