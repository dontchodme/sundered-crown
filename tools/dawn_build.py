#!/usr/bin/env python
"""DAWNBRINGER / DAYBREAK, REDESIGNED -- the sun rises up the hall. v97.

Built from `06-docs/v86/dawnbringer-daybreak-redesign-v86.md` §5 (Cowork,
2026-09-26) and its §7 rulings, which are the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the dawn, sparks out     sc-corollary-c14 -> sc-dawn.html
    stage 2   the blade                confirm 10.4 wide on 151 (no link unless it moves)
    stage 3   picture, voice, field    (not written yet)

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
    ap.add_argument("--stage", choices=["1"], required=True)
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

    if "ultDawn" in code:
        raise SystemExit("this source already carries stage 1 -- built")
    if strip_comments(SHIPPED_ULT) not in code:
        raise SystemExit("Dawnbringer's shipped Daybreak is not in this source "
                         "as shipped -- the base has moved under the builder")
    for label, old, new in S1:
        s = one(s, old, new, label)

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
    for label, _old, new in S1:
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

    syntax_check(s, out_p.name)
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
