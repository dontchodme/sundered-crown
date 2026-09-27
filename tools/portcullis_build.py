#!/usr/bin/env python
"""PORTCULLIS / ONSLAUGHT -- the vigil flail, a NEW relic. v100.

Built from `06-docs/v72/PORTCULLIS-BUILD-BRIEF.md` and
`vigil-flail-design-v72.md` (Cowork, 2026-09-26), which are the input and the
only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-portcullis.html
    stage 2   the charge and the slam     -> sc-ram.html       (arm C)
    stage 3   the bank                    -> sc-onslaught.html (arm D)
    stage 5   the blade                   -> sc-onslaught-b23.html (24.03 -> 23)
    stage 6   picture, voice, field       (not written yet)

§1: "For a duration the ward hardens the shell and the ball itself becomes
the weapon. It charges at the enemy. Every time the two balls slam together,
the enemy takes a hit worth a share of the shield the ball is carrying, is
knocked back, and the slam banks more shield. The flail head keeps swinging."

Declared (design §6, brief §0-§1):
  THE CHARGE  vx, vy += unit(foe) x 600 x dt each window frame, not while
              pinned, speed clamped at speedMax. On top of the engine's own
              motion: the ball still bounces and falls.
  A SLAM      centres closer than 2R + 3, once per 0.5s: hurt(foe, 0.25 x
              shield, f) -- ward first, nothing else: no crit, no jitter, no
              sunder, no hit stop but a ward's own shatter -- then knock 500
              away from the caster, then the bank: +8 ward through the three
              writes resolveHit's vigil branch makes (shield to the cap,
              shieldMax, apply("ward", 1)). A slam files a hit beat.
  The head's blow is untouched, and `ballCollision` runs as ever: a slam is
  an extra payment on the same contact.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop
freezes; Rick, 2026-09-27, for the whole batch: "use the game's equivalent".
Measured for this fighter at build time (v100 §0).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE SLAM IS 0.25 x SHIELD AND NOTHING ELSE (design §4: "the flat 10 is
     dropped"). The lab's `ramDmg` defaults to that rejected 10, so every lab
     arm here passes ramDmg=0, as the settled runs did.
  2. BOTH COMPONENTS of the charge (the brief's "vx,vy"; §6 writes vx only).
  3. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab tests
     `foe`; Corollary's and Zenith's reading). Portcullis still bounces off
     shades through `_ballPair`.
  4. A SLAM AT ZERO SHIELD IS STILL A SLAM: no damage (hurt is skipped at 0,
     as the lab's H.hurt skips it), but the knock, the bank and the cooldown.
  5. THE KNOCK skips a dead or pinned foe (the lab's H.knock): a foe the slam
     killed keeps whatever `hurt` gave it.
  6. `hurt`'s SOURCE IS THE FIGHTER (its contract: a shatter reads src), and
     the bank's `apply("ward", 1)` passes none (the vigil branch's own).
  7. EVERY SLAM FILES A HIT BEAT (design §6, brief §1), marked `ram`, with
     honest kinematics; its `fatal` is set when the slam killed.

THE CLOCK. The window, the charge's acceleration and the slam's cooldown run
on the window tickers' clock, which stops through a hit stop (Corollary's,
Daybreak's, Zenith's and Canopy's convention). The lab ran all three through
freezes; v99 §4 measured what that is worth on Canopy.

THE BASE is the chain tip, named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "portcullis"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v100 §0)
    "dur": 8,         # "the window 8s"
    "accel": 600,     # "vx,vy += unit(foe) x 600 x dt"
    "share": 0.25,    # "hurt 0.25 x shield"
    "pad": 3,         # "d < 2R + 3"
    "cd": 0.5,        # "once per 0.5s"
    "knock": 500,     # "knock 500 away"
    "bank": 8,        # "bank +8 ward" -- stage 3
}
TIP = "The shell charges the foe. Each slam hits for the shield and banks more"
# Gravemourn's flail profile, the lab's donor (cell_ults_on.TYPE_DONOR), and
# its blade; stage 5 settles it wide.
PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:24.03, spin:2.2, '
        'mode:"chain", mass:3.6')
FLAILS = ("gravemourn", "redflail", "slagheart", "morningstar")
VIGIL_MELEE = ("lightkeeper", "bulwarden", "vesper", "starwarden")
BLURB = ("A flail whose ball becomes the weapon: it charges, every slam hits for "
         "the shield it carries, and every slam banks more.")


def ult_block(charge, bank: int) -> str:
    return (f'''    ult:{{ name:"Onslaught", charge:{charge}, kind:"ram", dur:{ULT["dur"]},
          accel:{ULT["accel"]}, share:{ULT["share"]}, pad:{ULT["pad"]}, cd:{ULT["cd"]}, knock:{ULT["knock"]},
          bank:{bank},          // v72: the bank (stage 3)
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
# THE RELIC, APPENDED AFTER IRONWOOD, ITS ULTIMATE STUBBED at charge 1e9 (the
# clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. Every other table keyed by relic id falls back.
ROW_ANCHOR = ('''    blurb:"A hammer that takes root and grows into a tree: three boughs sweep the hall, and whoever stands beneath them is entangled." },

];''')

S1 = [

("portcullis joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 ROW_ANCHOR[:-4] + f'''
  /* PORTCULLIS / ONSLAUGHT (v72; built v100) -- THE VIGIL FLAIL, the 37th
     relic built. Gravemourn's flail profile and its blade (the lab's donor;
     stage 5 settles it), and the school's channel, onSelf ward. Stage 1
     stubs the ultimate at charge 1e9; stages 2-3 give it its charge and its
     slam, then its bank. */
  {{ id:"portcullis", name:"Portcullis", aff:"vigil", shape:"flail",
    {PHYS},
    onSelf:{{ ward:1 }},
{ult_block("1e9", 0)}
    blurb:"{BLURB}" }},

];'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the ram has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Onslaught", charge:1e9, kind:"ram", dur:8,
''',
 f'''    ult:{{ name:"Onslaught", charge:{ULT["charge"]}, kind:"ram", dur:{ULT["dur"]},   // v72 stage 2: the ball charges
'''),

("the fighter carries the ram's window",
 '''    this.treeTally = null;
''',
 '''    this.treeTally = null;
    /* {t, dur, cd} while ONSLAUGHT's ball charges and slams (v72). null on
       every other relic and on this one outside its window: `tickRam`
       returns after a two-iteration loop that does nothing. `ramTally` is the
       probe's count, cumulative over the fight; nothing in the simulation
       reads it. */
    this.ultRam = null;
    this.ramTally = null;
'''),

("the cast opens the ram and resolves nothing",
 '''    if (u.kind === "tree"){
''',
 '''    if (u.kind === "ram"){
      /* ONSLAUGHT (v72). NOTHING RESOLVES HERE: the cast turns the ball into
         the weapon for `u.dur` seconds, and `tickRam` does everything the
         window does. `cd` starts at zero, so balls already touching slam on
         the first frame. */
      f.ultRam = { t: 0, dur: u.dur, cd: 0 };
      if (!f.ramTally)
        f.ramTally = { casts: 0, frames: 0, shieldSum: 0, slams: 0, dealt: 0,
                       banks: 0, banked: 0 };
      f.ramTally.casts++;
      return;
    }
    if (u.kind === "tree"){
'''),

("the ram ticks with the window tickers",
 '''    this.tickTree(dt);                  // CANOPY (v69)
''',
 '''    this.tickTree(dt);                  // CANOPY (v69)
    this.tickRam(dt);                   // ONSLAUGHT (v72)
'''),

("tickRam charges, slams and banks",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE RAM =========
     v72 §1 / §6, brief §0-§1. While the window runs the caster's BALL is the
     weapon:
       THE CHARGE  vx, vy += unit(foe) x accel x dt, unless pinned, then the
                   speed clamped at speedMax -- on top of the engine's own
                   motion, so the ball still bounces and falls; `move` spends
                   it next step.
       A SLAM      the centres closer than 2R + pad, once per `cd` (the
                   cooldown runs through the whole window): hurt(foe, share x
                   shield, f) -- ward first, nothing else -- then `knock` away
                   from the caster (not a dead or pinned foe), then the bank:
                   the vigil branch's three writes. A slam at no shield still
                   knocks and banks. Every slam files a hit beat (`ram`).
     After `ballCollision`, so the balls are tested separated, as the lab
     tested them after the whole step; the shoulder happens as ever and the
     slam is an extra payment on it. The target is the OPPONENT only. On the
     window tickers' clock, so all of it freezes through a hit stop. */
  tickRam(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultRam;
      if (!Z) continue;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive){ f.ultRam = null; continue; }
      const u = f.w.ult, T = f.ramTally;
      const foe = f === this.a ? this.b : this.a;
      const R = CONFIG.physics.ballR;
      T.frames++;
      T.shieldSum += f.shield;
      Z.cd -= dt;
      if (!foe.alive) continue;
      const dx = foe.x - f.x, dy = foe.y - f.y, d = Math.hypot(dx, dy) || 1;
      if (f.pin <= 0){
        f.vx += dx / d * u.accel * dt;
        f.vy += dy / d * u.accel * dt;
        const v = Math.hypot(f.vx, f.vy), vmax = CONFIG.physics.speedMax;
        if (v > vmax){ f.vx *= vmax / v; f.vy *= vmax / v; }
      }
      if (Z.cd > 0 || !(d < 2 * R + u.pad)) continue;
      Z.cd = u.cd;
      T.slams++;
      const dmg = u.share * f.shield;
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      if (dmg > 0) this.hurt(foe, dmg, f);
      T.dealt += before - (foe.hp + foe.shield);
      if (foe.alive && !(foe.pin > 0)){
        foe.vx += dx / d * u.knock;
        foe.vy += dy / d * u.knock;
      }
      if (u.bank > 0){
        const W = STATUS.ward, b0 = f.shield;
        f.shield = Math.min(W.cap, f.shield + u.bank);
        f.shieldMax = Math.max(f.shieldMax, f.shield);
        f.apply("ward", 1);                       // (re)starts the clock
        T.banks++;
        T.banked += f.shield - b0;
      }
      this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                  x: (f.x + foe.x) / 2, y: (f.y + foe.y) / 2, dmg, crit: false,
                  fatal: wasUp && foe.hp <= 0, hpAfter: Math.max(0, foe.hp),
                  hpFrac: Math.max(0, foe.hp) / foe.maxHp, maxHp: foe.maxHp,
                  selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                  close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                  ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                  shotSpd0: 0, ram: true });
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the bank",
 '''          bank:0,          // v72: the bank (stage 3)
''',
 f'''          bank:{ULT["bank"]},          // v72: the bank (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (brief §2 stage 5: "Wide on 151 at 22 / 23 / 24. Expect
# 22.5-23.5."). Both sides, two blocks, 1440 fights a point (relic_rate):
# 22 -> 46.8, 23 -> 50.8, 24 -> 53.9; the crossing ~22.8. The measured point
# at the crossing, and inside the brief's band. Nothing else moves.
BLADE = 23

S5 = [
("the blade: at the crossing",
 '''  { id:"portcullis", name:"Portcullis", aff:"vigil", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:24.03,''',
 f'''  {{ id:"portcullis", name:"Portcullis", aff:"vigil", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:{BLADE},'''),
]

STAGE_OUT = {"1": "sc-portcullis", "2": "sc-ram", "3": "sc-onslaught", "5": "sc-onslaught-b23"}


def relic_row(code: str, rid: str) -> str:
    i = code.find(f'{{ id:"{rid}"')
    if i < 0:
        raise SystemExit(f"no {rid} in this source")
    return code[i:code.find("blurb:", i)]


def relic_ult(code: str) -> str:
    row = relic_row(code, RELIC)
    j = row.find("ult:{")
    k = row.find("},", j)
    return row[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)
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
    print(f"\nPORTCULLIS / ONSLAUGHT -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Ironwood
    # through its stage 5.
    for need, why in (("tickTree(dt){", "no tickTree -- not the chain tip"),
                      ("winDmg:0.38,", "no Canopy stage 5 -- not the chain tip"),
                      ("sunShown", "no Zenith stage 6 -- not the chain tip")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    # AND THE DONOR'S FLAIL PROFILE IS STILL WHAT THIS BUILDER COPIES; THE
    # SCHOOL'S CHANNEL AND THE VIGIL FLAIL HEAD ARE WHERE THEY WERE.
    if PHYS not in " ".join(relic_row(code, "gravemourn").split()):
        raise SystemExit("Gravemourn's flail profile has moved -- the donor is "
                         "not what this builder copies")
    for fl in FLAILS:
        if 'shape:"flail"' not in relic_row(code, fl):
            raise SystemExit(f"{fl} is not a flail any more")
    for v in VIGIL_MELEE:
        if "onSelf:{ ward:1 }" not in relic_row(code, v):
            raise SystemExit(f"{v} does not carry the school's channel, onSelf ward 1")
    if not re.search(r'if \(key === "vigil"\)\s+return SHAPES\._fhPlated\(', code):
        raise SystemExit("SHAPES.flailHead no longer routes vigil to _fhPlated")
    print("  base  the chain tip (Canopy stage 5, Zenith stage 6); the donor's flail "
          "profile, the vigil channel and the vigil head hold")

    if A.stage == "1":
        if f'id:"{RELIC}"' in code:
            raise SystemExit("this source already carries Portcullis -- built")
        edits, want = S1, ult_block("1e9", 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultRam" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "ultRam" not in code or "bank:0," not in code:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["bank"])
        else:
            if f'bank:{ULT["bank"]},' not in code or f"dmg:{BLADE}," in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bank"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Portcullis's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
    if len(re.findall(r'kind:"ram"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one ram ultimate")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one ram ultimate, Portcullis's; no insert draws the RNG; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
