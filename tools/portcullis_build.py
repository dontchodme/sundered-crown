#!/usr/bin/env python
"""PORTCULLIS / ONSLAUGHT -- the vigil flail, a NEW relic. v100.

Built from `06-docs/v72/PORTCULLIS-BUILD-BRIEF.md` and
`vigil-flail-design-v72.md` (Cowork, 2026-09-26), which are the input and the
only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-portcullis.html
    stage 2   the charge and the slam     -> sc-ram.html       (arm C)
    stage 3   the bank                    -> sc-onslaught.html (arm D)
    stage 5   the blade                   -> sc-onslaught-b23.html (24.03 -> 23)
    stage 6   picture, voice              -> sc-onslaught-fx.html (no field: drawn sparks, v100 §5)

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

STAGE 6, THE PICTURE AND THE VOICE (v72 §7.1-7.2), picked on measurements
under Rick's "you pick i overrule" (v100 §5). Declared:
  8. THE BANK'S VOICE IS NEW. §7.2 asks for "the ward's existing bank voice,
     reused"; there is none (the synth's 17 kinds: a ward banks in silence,
     and a ward that breaks plays the ordinary hit, a crit). So `ward-bank` is
     the ward's own new kind, as hex-snap is the runic school's, and only
     Onslaught plays it: the vigil blow's own bank stays silent, as it was.
  9. THE SLAM'S VOICE CARRIES THE SHIELD THE SLAM HIT FOR, before the bank; a
     slam at no shield still knocks and banks, so it thuds at the quiet end.
 10. A BANK AT THE CAP STILL SOUNDS: it adds nothing but restarts the ward's
     clock (the brief: "Slams = banks").
 11. THE CLOSE'S VOICE only when the window closes by its clock with the
     caster alive; a death belongs to the death voice and the shatter
     (Zenith's, Daybreak's and Canopy's rule). THE PLATES FALL on a clock
     close and at the match's end with the caster alive (a shell standing at
     the kill would otherwise stand through the verdict), silently at the
     end; on the caster's death nothing falls.
 12. NO fx.js FIELD. §7.1's "Field: spark motes off the plates on each slam,
     both copies" is drawn in the world pass instead (the slam's sparks, off
     the struck plate): a SPECS field spawns once, at the caster, on the cast
     edge of the one ultFx slot, and Portcullis's record lives 0.75s; 24 of
     324 slams land while it lives, and the opponent's cast takes the slot in
     52 of 82 windows (v100 §5). Zenith's and Canopy's precedent; Rick's to
     overrule.
 13. THE HEAD: the vigil route `_fhPlated` becomes the square plated head (a
     gored sphere never drawn by a shipped relic), and the haft's bands are
     gated on the vigil key. Portcullis is the only vigil flail (asserted), so
     no other relic's picture moves (render_ab).
 14. THE WARD'S RING STANDS DOWN while the shell stands (the shell is that
     ring, thickened, and its fill is the pool); it is back the frame the
     plates crack, because the bank outlives the window.
 15. THE PICTURE HANGS OFF THE FIGHTER, never `m.ultFx` (open item 25), and is
     driven in `tickPresentation`, which writes presentation fields, floats,
     tags and `taught` only; a slam is found by `ramTally.slams` rising, and
     its number is read off the slam's own `ram` beat.

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

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v72 §7.1-7.2), picked on measurements under
# Rick's "you pick i overrule" by the picture lab and `portcullis_voice_lab.py`
# (v100 §5). Presentation only: engine_ab over all 38 relics, Portcullis
# included, is the proof. The rows are byte-exact to the labs' own files: the
# five voice rows first, then the eight picture rows; no two share a line of
# the base, so none is merged. Every replace row re-emits its anchor, so
# another relic's row on the same line (Bindweed's voice on rune-crack)
# applies in either order. ONE ANCHOR IS WIDENED: the bank voice's line,
# `T.banked += f.shield - b0;`, is written twice more by Lightkeeper's
# Bulwark (in flight), so its edit takes Portcullis's whole bank block, from
# `if (u.bank > 0){`, and puts it back unchanged: the same bytes out.
S6 = [

("Sfx: Portcullis's cast, slam and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "portcullis"){                 // the gate comes down
          /* PORTCULLIS'S CAST, THE GATE COMES DOWN -- v72 §7.2: "a
             metal-on-stone clang and a low hum settling, 0.4s". BAR, of 5,
             picked on the numbers by `portcullis_voice_lab.py` under Rick's
             "you pick i overrule" (v100). Portcullis had no arm and fell
             through to rune-crack, which Lightkeeper, Farwarden and Bindweed
             still use, so this ADDS arms before that fallback and leaves it
             alone.

             The stone is a lowpass noise burst, 60 ms, that does not ring; the
             clang is an iron bar struck (triangles on the note and its
             free-bar modes 2.76 and 5.40), on E4 (the score's fifth); the hum
             is the score's tonic, A2 over A1, one strike that settles into
             silence. Audible 400 ms; the loudest 50 ms -2.7 dB re Portcullis's
             own blow; the hum -6.2 dB under the clang; the stone -9.0 dB re
             the attack. Register at most 0.71 against rune-crack, the vigil
             and flail casts, the clank, the death voice and the blow. */
          const g = 0.1204, kh = 0.4328, ks = 6.073, F = 329.63;
          this._burst(t, { freq: 600, q: 0.8, gain: g * ks, dur: 0.06, type:"lowpass" });
          for (const [r, k, d] of [[1, 1, 0.55], [2.76, 0.45, 0.4], [5.4, 0.2, 0.25]])
            this._tone(t, { freq: F * r, gain: g * k, dur: d, type:"triangle" });
          this._tone(t, { freq: 110, gain: g * kh, dur: 0.751, type:"triangle" }).frequency.value = 110;
          this._tone(t, { freq: 55, gain: g * kh * 0.5, dur: 0.751, type:"sine" }).frequency.value = 55;
        } else if (w === "portcullis-slam"){            // the shell hits the foe
          /* ONSLAUGHT'S SLAM -- "a heavy gated thud (share below 120 Hz >=
             0.45, <= 0.25s), louder with the shield (peak 0.35 -> 0.65 across
             0 -> 90)" (v72 §7.2). TOM, of 4 (`portcullis_voice_lab.py`).
             `tickRam` plays it on the slam's frame with `shield`, the shield
             the slam hit for, before the bank.

             A held E2 sine and an E3 triangle, cut together on a zero crossing
             (whole cycles; `.frequency.value = f` keeps each tone's phase
             where it was scheduled), under a falling punch and a contact
             click. The gain is a quadratic in the shield, solved so the peak
             is 0.35 / 0.50 / 0.65 at 0 / 45 / 90: measured 0.350 / 0.427 /
             0.500 / 0.574 / 0.650 at 0 / 22.5 / 45 / 67.5 / 90. 0.84 of its
             power below 120 Hz at the worst noise draw; gone by 200 ms; within
             6 dB of its loudest for 95% of its length, then cut in 10 ms.
             Register at most 0.40 against the blow, the death voice,
             rune-crack and the cast. */
          const u = clamp((p.shield || 0) / 90, 0, 1), g = 0.1366 + 0.1937 * u + 0.04482 * u * u, G = 0.194151;
          const o1 = this._tone(t, { freq: 82.41, gain: g, dur: 2, type:"sine" });
          o1.frequency.value = 82.41; o1.stop(t + G);
          const o2 = this._tone(t, { freq: 164.81, gain: g * 0.5, dur: 2, type:"triangle" });
          o2.frequency.value = 164.81; o2.stop(t + G);
          this._tone(t, { freq: 150, to: 55, gain: g * 0.5, dur: 0.05, type:"sine" });
          this._burst(t, { freq: 1800, q: 1.2, gain: g * 0.3, dur: 0.02, type:"bandpass" });
        } else if (w === "portcullis-close"){           // and the plates fall
          /* THE PLATES FALL -- "plates falling -- three short clinks" (v72
             §7.2). FALL, of 3 (`portcullis_voice_lab.py`): three small plates
             struck (modes 1 : 1.59 : 2.14), at 0 / 0.1 / 0.23 s, each lower
             than the last (1319 / 1175 / 1046 Hz), inside the picture's 0.3 s
             fall; each clink audible 50/50/50 ms; register at most 0.65
             against the clank, the blow, rune-crack, the bank and the cast.
             `tickRam` plays it only when the window closes by its clock with
             the caster alive, never on a death. */
          const g = 0.09424, D = 0.0769;
          for (const [s, f, k] of [[0, 1318.51, 1], [0.1, 1174.66, 0.9], [0.23, 1046.5, 0.8]])
            for (const [r, m] of [[1, 1], [1.59, 0.6], [2.14, 0.4]])
              this._tone(t + s, { freq: f * r, gain: g * k * m, dur: D, type:"sine" });
        } else {                                        // rune-crack'''),

("Sfx: the ward's bank voice -- a new kind, `ward-bank`, before hex-snap",
 '''      else if (kind === "hex-snap"){''',
 '''      else if (kind === "ward-bank"){
        /* THE WARD'S BANK -- v72 §7.2 asks for "the ward's existing bank
           voice, reused". There was none: nothing played when a ward banked (a
           ward that breaks plays the ordinary hit, a crit). So this is the
           ward's own new kind, as hex-snap is the runic school's. LATCH, of 4,
           picked on the numbers by `portcullis_voice_lab.py` under Rick's "you
           pick i overrule" (v100).

           A latch catching: two quick struck ticks rising a third, C7 then E7,
           35 ms apart, each with a bar mode. Onslaught's bank plays it on the
           slam's frame, so it stands +13.9 dB over the loudest slam in its own
           band; audible 65 ms; its loudest 50 ms -9.3 dB re Portcullis's blow;
           register at most 0.48 against the spark collect (the blessing's
           chime), the shatter, the clank, the runic snap, rune-crack, the slam
           and the cast. Only Onslaught plays it: the vigil blow's own bank
           stays silent, as it always has. */
        const g = 0.1264;
        for (const [s, f] of [[0, 2093], [0.035, 2637.02]]){
          this._tone(t + s, { freq: f, gain: g, dur: 0.05, type:"triangle" });
          this._tone(t + s, { freq: f * 2.76, gain: g * 0.3, dur: 0.03, type:"sine" });
        }
      }
      else if (kind === "hex-snap"){'''),

("tickRam: the slam voice, on the slam's frame, carrying the shield it hit for",
 '''      T.slams++;''',
 '''      T.slams++;
      /* ONSLAUGHT'S SLAM (v72 §7.2: "a heavy gated thud ..., louder with the
         shield"): on the slam's own frame, carrying the shield the ball
         brings into it -- the one this slam hits for, before the bank. A
         slam at no shield still knocks and banks, so it still thuds, at the
         quiet end. Presentation only: SFX.play draws nothing, is a no-op
         headless, and nothing here is read back (portcullis_voice_lab:
         fights identical). */
      SFX.play("ult", { w: "portcullis-slam", shield: f.shield });'''),

("tickRam: the ward's bank voice, after the bank's three writes",
 '''      if (u.bank > 0){
        const W = STATUS.ward, b0 = f.shield;
        f.shield = Math.min(W.cap, f.shield + u.bank);
        f.shieldMax = Math.max(f.shieldMax, f.shield);
        f.apply("ward", 1);                       // (re)starts the clock
        T.banks++;
        T.banked += f.shield - b0;''',
 '''      if (u.bank > 0){
        const W = STATUS.ward, b0 = f.shield;
        f.shield = Math.min(W.cap, f.shield + u.bank);
        f.shieldMax = Math.max(f.shieldMax, f.shield);
        f.apply("ward", 1);                       // (re)starts the clock
        T.banks++;
        T.banked += f.shield - b0;
        /* THE WARD'S BANK (v72 §7.2: "the ward's existing bank voice,
           reused" -- the synth had none, so `ward-bank` is new, the ward's
           own kind). Once per bank, and every slam banks; at the cap the
           bank adds nothing but restarts the ward's clock, and still sounds.
           Plain SFX.play; nothing is read back. */
        SFX.play("ward-bank");'''),

('tickRam: the close voice, when the window closes by its clock with the caster alive',
 '''      if (Z.t >= Z.dur || !f.alive){ f.ultRam = null; continue; }''',
 '''      /* ONSLAUGHT'S CLOSE (v72 §7.2: "plates falling -- three short
         clinks"): only when the window runs out BY ITS CLOCK with the caster
         alive. A caster's death ends the fight on this frame, and a foe's
         death ends it before any close (step() stops calling this), so both
         endings are left to the death voice, as Zenith's, Daybreak's and
         Canopy's closes are. Plain SFX.play; nothing is read back. */
      if (f.alive && Z.t >= Z.dur) SFX.play("ult", { w: "portcullis-close" });
      if (Z.t >= Z.dur || !f.alive){ f.ultRam = null; continue; }'''),

('onslaught picture: fighter fields',
 '''    this.ultRam = null;
    this.ramTally = null;
''',
 '''    this.ultRam = null;
    this.ramTally = null;
    /* ONSLAUGHT'S PICTURE (v72 section 7.1), and none of it is the window:
       the shell outlives `ultRam` by the 0.3s its plates take to crack and
       fall, so the picture keeps its own state. On the FIGHTER and never on
       `m.ultFx` (one slot, and the opponent's cast takes it: open item 25).
       Driven in `tickPresentation`; nothing in the simulation reads any of it.
         ramFade -- 1 while the shell stands; eased to 0 over the close
         ramAge  -- the presentation clock since the cast (the thickening)
         ramOut  -- the presentation clock since the close
         ramDead -- the caster fell: the shatter owns the ball, nothing falls
         ramSeen -- `ramTally.slams` as last seen (a rise is a slam)
         ramRun  -- the speed-streak's strength, eased: the charge driving the
           ball AT the foe
         ramHits -- the slams: the plate's flash, the glint, the sparks
         ramBits -- the plates falling off at the close */
    this.ramFade = 0;
    this.ramAge = 0;
    this.ramOut = 0;
    this.ramDead = false;
    this.ramSeen = 0;
    this.ramRun = 0;
    this.ramHits = [];
    this.ramBits = [];
'''),

('onslaught picture: the presentation clock',
 '''    if (this.ultFx){
      /* A HELD CRUCIBLE DOES NOT AGE.''',
 '''    /* ONSLAUGHT'S SHELL (v72 section 7.1). HALF-SECONDS, like every `life`
       in this method (it runs twice a normal step): 0.5 is the cast's 0.25s
       thickening, 0.6 the close's 0.3s. A SLAM IS FOUND BY WATCHING
       `ramTally.slams` RISE, so `tickRam` makes no call, and its number is the
       slam's own hit beat (`ram`) read back, never recomputed. Through a hit
       stop the window's clock stops and this one keeps playing, so a flash and
       its sparks finish. Not after the match and not once the caster falls:
       `tickRam` never runs again once `over` is set, so a shell standing at
       the kill would otherwise stand through the verdict. Writes presentation
       fields, `floats`, `tags` and `taught` only. */
    for (const f of [this.a, this.b]){
      const T = f.ramTally;
      if (!T && !(f.ramFade > 0)) continue;                    // <- zero burden
      const Z = (this.over || !f.alive) ? null : f.ultRam;
      const foe = f === this.a ? this.b : this.a, Rb = CONFIG.physics.ballR;
      if (Z){
        if (!(f.ramFade > 0) || f.ramOut > 0){                  // a new shell
          f.ramAge = 0; f.ramOut = 0; f.ramDead = false; f.ramBits.length = 0;
        }
        f.ramFade = 1;
        f.ramAge += dt;
        /* THE STREAK is the charge driving the ball AT the foe: the speed
           along the line to it, so a ball thrown off by its own slam reads as
           knocked back, not as charging. No streak while pinned (no charge). */
        const dx = foe.x - f.x, dy = foe.y - f.y, d = Math.hypot(dx, dy) || 1;
        const go = (foe.alive && !(f.pin > 0)) ? (f.vx * dx + f.vy * dy) / d : 0;
        const want = clamp((go - 250) / 650, 0, 1);
        f.ramRun += (want - f.ramRun) * Math.min(1, dt / 0.12);
      } else if (f.ramFade > 0){
        if (!(f.ramOut > 0)){
          f.ramDead = !f.alive;
          /* THE PLATES CRACK AND FALL, from where the shell is now, each
             kicked off its own face and carrying half the ball's speed. Not on
             a death (the shatter owns the ball). */
          if (!f.ramDead){
            const am = Rb + (2 + 18) / 2;
            const fill = 0.15 + 0.45 * clamp(f.shield / STATUS.ward.cap, 0, 1);
            for (let i = 0; i < 6; i++){
              const q = (i + 0.5) * TAU / 6, kick = 90 + 90 * shellHash(9831 + f.side, i);
              f.ramBits.push({ x: f.x + Math.cos(q) * am, y: f.y + Math.sin(q) * am,
                               vx: Math.cos(q) * kick + f.vx * 0.5, vy: Math.sin(q) * kick + f.vy * 0.5 - 60,
                               q, spin: (shellHash(9833 + f.side, i) - 0.5) * 8, fill, t: 0 });
            }
          }
        }
        f.ramFade = Math.max(0, f.ramFade - dt / 0.6);
        f.ramOut += dt;
        f.ramRun = Math.max(0, f.ramRun - dt / 0.2);
      }
      /* A SLAM: its plate flashes, sparks fly off it, its number floats in
         the school's glow at the contact (an ordinary blow's float, sized the
         same way), and the WARD tag on the caster ticks up to the pool the
         bank left -- the bank is the read. A slam at no shield hits for
         nothing and floats no number; it still flashes, knocks and banks. */
      if (T && T.slams > f.ramSeen){
        f.ramSeen = T.slams;
        const side = f === this.a ? 0 : 1;
        let B = null;
        for (let i = this.beats.length - 1, n = 0; i >= 0 && n < 32; i--, n++)
          if (this.beats[i].ram && this.beats[i].side === side){ B = this.beats[i]; break; }
        const bx = B ? B.x : (f.x + foe.x) / 2, by = B ? B.y : (f.y + foe.y) / 2;
        const a = Math.atan2(by - f.y, bx - f.x), n = B ? Math.round(B.dmg) : 0;
        f.ramHits.push({ a, x: bx, y: by, k: T.slams, t: 0 });
        if (f.ramHits.length > 8) f.ramHits.shift();
        if (n >= 1){ this.float(bx, by, n, f.aff.glow, clamp(22 + n * 0.62, 22, 62)); }
        const first = !this.taught.ward && !!STATUS.ward.tip;
        if (first) this.taught.ward = true;
        this.statusTag(f.x, f.y, "ward", first, Math.round(f.shield));
      }
      for (let i = f.ramHits.length - 1; i >= 0; i--){
        f.ramHits[i].t += dt;
        if (f.ramHits[i].t >= 0.9) f.ramHits.splice(i, 1);
      }
      for (let i = f.ramBits.length - 1; i >= 0; i--){
        f.ramBits[i].t += dt;
        if (f.ramBits[i].t >= 0.6) f.ramBits.splice(i, 1);
      }
    }
    if (this.ultFx){
      /* A HELD CRUCIBLE DOES NOT AGE.'''),

('onslaught picture: the ward ring stands down under the shell',
 '''    if (f.shield > 0){
      const lit   = Math.max(1, Math.ceil(frac * N));
''',
 '''    /* ONSLAUGHT'S SHELL (v72 section 7.1) is this ring, thickened: while it
       stands it draws the pool itself (its fill), so the ring stands down. It
       comes back the frame the plates crack, because the bank outlives the
       window. The break, the spend and the expiry below draw as ever. */
    if (f.shield > 0 && !(f.ramFade >= 1)){
      const lit   = Math.max(1, Math.ceil(frac * N));
'''),

('onslaught picture: the banded haft',
 '''      c.beginPath(); c.arc(hx0, hy0, hw * 0.6, 0, TAU); c.fill();
''',
 '''      c.beginPath(); c.arc(hx0, hy0, hw * 0.6, 0, TAU); c.fill();
      /* PORTCULLIS'S BANDED HAFT (v72 section 7.1): two plate bands in the
         school's core, over a `dark` underlay, where the haft leaves the
         shell. Only a vigil flail draws them, and Portcullis is the only one. */
      if (pal.key === "vigil"){
        for (const [bw, col] of [[hw * 1.05, pal.dark], [hw * 0.55, pal.core]]){
          c.strokeStyle = col; c.lineWidth = bw;
          for (const t of [0.80, 0.93]){
            const gx = hx0 + (px - hx0) * t, gy = hy0 + (py - hy0) * t;
            c.beginPath();
            c.moveTo(gx + nx0 * hw * 1.25, gy + ny0 * hw * 1.25);
            c.lineTo(gx - nx0 * hw * 1.25, gy - ny0 * hw * 1.25);
            c.stroke();
          }
        }
      }
'''),

('onslaught picture: the plated square head',
 '''  /* --------------------------------------------------------------- VIGIL --
     PLATED. THE CELL'S FLAIR: six plates laid over the sphere like the gores
     of a helmet, each stepping proud of the last, so the ball reads as
     ARMOURED rather than spiked -- and the spikes shorten to studs, because a
     vigil weapon's argument is that it survives the exchange, not that it wins
     the exchange. */
  _fhPlated(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);             // short studs
    for (let i = 0; i < 6; i++){
      const a = (i / 6) * TAU + 0.5;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.20) * r * 0.94, Math.sin(a - 0.20) * r * 0.94);
      c.lineTo(Math.cos(a + 0.20) * r * 0.94, Math.sin(a + 0.20) * r * 0.94);
      c.lineTo(Math.cos(a) * r * 1.34,        Math.sin(a) * r * 1.34);
      c.closePath(); c.fill();
    }
    SHAPES._fhBall(c, D, p);
    for (let i = 0; i < 6; i++){                                   // the gores
      const a = (i / 6) * TAU;
      c.save();
      c.rotate(a);
      c.fillStyle = p.dark;
      c.beginPath();
      c.moveTo(0, 0);
      c.arc(0, 0, r * 1.06, -0.50, 0.02);
      c.closePath(); c.fill();
      c.fillStyle = p.core;
      c.beginPath();
      c.moveTo(0, 0);
      c.arc(0, 0, r * 0.94, -0.44, -0.04);
      c.closePath(); c.fill();
      c.fillStyle = p.glow;
      c.beginPath();
      c.moveTo(0, 0);
      c.arc(0, 0, r * 0.94, -0.44, -0.36);
      c.closePath(); c.fill();
      c.restore();
    }
    c.fillStyle = p.dark;                                          // the boss
    c.beginPath(); c.arc(0, 0, r*0.30, 0, TAU); c.fill();
    c.fillStyle = p.glow;
    c.beginPath(); c.arc(0, 0, r*0.17, 0, TAU); c.fill();
    c.restore();
  },
''',
 '''  /* --------------------------------------------------------------- VIGIL --
     PLATED, AND SQUARE (v72 section 7.1: "a plated square head on a banded
     haft, first cut"). The gored sphere this route drew before was never on a
     shipped relic; Portcullis is the first vigil flail. A square block in four
     plates -- a `dark` rim, `core` seams, a lit bevel on each plate -- with a
     stud at each corner and a boss at the centre, so the head reads as a
     gate's weight rather than a spiked ball: the only square head in the
     flail row. */
  _fhPlated(c, D, p, spin){
    const r = D * 0.34, h = r * 1.02, g = h * 0.10;
    const steel = SHAPES._shade(p.steel, 0.62, 0.42), deep = SHAPES._shade(p.steel, 0.34, 0.52);
    c.save();
    c.rotate(spin);
    c.lineJoin = "round";
    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);             // corner studs
    for (let i = 0; i < 4; i++){
      const a = (i + 0.5) * TAU / 4;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.26) * h * 1.30, Math.sin(a - 0.26) * h * 1.30);
      c.lineTo(Math.cos(a + 0.26) * h * 1.30, Math.sin(a + 0.26) * h * 1.30);
      c.lineTo(Math.cos(a) * h * 1.92, Math.sin(a) * h * 1.92);
      c.closePath(); c.fill();
    }
    c.fillStyle = p.dark;                                          // the rim
    c.fillRect(-h * 1.14, -h * 1.14, h * 2.28, h * 2.28);
    for (const [sx, sy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]){  // four plates
      const x0 = sx < 0 ? -h : g, y0 = sy < 0 ? -h : g, w = h - g;
      c.fillStyle = steel; c.fillRect(x0, y0, w, w);
      c.fillStyle = p.glow; c.fillRect(x0, y0, w, w * 0.18);       // the lit bevel
      c.fillRect(x0, y0, w * 0.18, w);
      c.fillStyle = deep;
      c.fillRect(x0, y0 + w * 0.84, w, w * 0.16);
      c.fillRect(x0 + w * 0.84, y0, w * 0.16, w);
      c.fillStyle = p.dark;                                        // its rivet
      c.beginPath(); c.arc(x0 + w * (sx < 0 ? 0.36 : 0.64), y0 + w * (sy < 0 ? 0.36 : 0.64), w * 0.10, 0, TAU); c.fill();
    }
    c.fillStyle = p.core;                                          // the seams
    c.fillRect(-g * 0.55, -h, g * 1.1, h * 2);
    c.fillRect(-h, -g * 0.55, h * 2, g * 1.1);
    c.fillStyle = p.dark;                                          // the boss
    c.beginPath(); c.arc(0, 0, r * 0.30, 0, TAU); c.fill();
    c.fillStyle = p.glow;
    c.beginPath(); c.arc(0, 0, r * 0.15, 0, TAU); c.fill();
    c.restore();
  },
'''),

("onslaught picture: the shell's call (world, under both balls)",
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* ONSLAUGHT'S SHELL, ITS STREAK AND ITS FALLING PLATES (v72 section
       7.1): the WORLD pass, under both balls. The shell stands round the
       caster's glass and a slam brings the foe's shell into it, so drawn over
       the balls it would cover the foe's disc at every slam (CLAUDE.md
       section 4.1b); nothing of it reaches the bloom (section 4.1c). */
    if (__world) this.drawRam(m);
'''),

("onslaught picture: the slam's call (world, over both fighters)",
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* ONSLAUGHT'S SLAM, over both fighters: the glint and the sparks are at
       the contact, between the two shells. World pass, like the ghost blade. */
    this.drawRamTop(m);
'''),

('onslaught picture: drawRam / _drawRamShell / drawRamTop',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------------------- THE RAM ---
     ONSLAUGHT'S PICTURE (v72 section 7.1). It hangs off the FIGHTER (`ramFade`,
     `ramAge`, `ramOut`, `ramRun`, `ramHits`, `ramBits`), never `m.ultFx`.
       drawRam     the WORLD pass under both balls: the plates falling at the
                   close, the speed-streak, and the plated shell, whose fill
                   IS the pool (0.15 at no shield, 0.6 at the cap)
       drawRamTop  the WORLD pass over both fighters: a slam's glint and its
                   sparks, at the contact between the two shells
     No rng: every spark and every plate's kick is a shellHash of its slam's
     count or its plate's index. */
  drawRam(m){
    const a = m.a, b = m.b;
    if (!(a.ramFade > 0) && !(b.ramFade > 0) && !a.ramBits.length && !b.ramBits.length) return;  // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      const P = f.aff;
      /* THE PLATES FALLING: each a plate of the shell as it stood, cracked
         across, tumbling off under gravity and gone in 0.3s. Under both
         balls, so a plate the ball overtakes never crosses a shell. */
      if (f.ramBits.length){
        const ai = R + 2, ao = R + 18, am = (ai + ao) / 2, t = 0.57735, gp = 1.6, ch = 4.5;
        const yi = ai * t - gp, yc = (ao - ch) * t - gp, yo = yc - ch;
        for (const d of f.ramBits){
          const s2 = d.t * 0.5, k2 = d.t / 0.6;
          c.save();
          c.translate(d.x + d.vx * s2, d.y + d.vy * s2 + 700 * s2 * s2);
          c.rotate(d.q + d.spin * s2);
          c.translate(-am, 0);
          c.beginPath();
          c.moveTo(ai, -yi); c.lineTo(ao - ch, -yc); c.lineTo(ao, -yo);
          c.lineTo(ao, yo); c.lineTo(ao - ch, yc); c.lineTo(ai, yi);
          c.closePath();
          const al = 1 - k2 * k2;
          c.fillStyle = P.core; c.globalAlpha = d.fill * al; c.fill();
          c.strokeStyle = P.dark; c.lineWidth = 2.4; c.globalAlpha = al; c.stroke();
          c.strokeStyle = P.glow; c.lineWidth = 1.2; c.globalAlpha = al * 0.6; c.stroke();
          c.beginPath();                                            // the crack
          c.moveTo(ai + 1, -yi * 0.2); c.lineTo(am - 2, yi * 0.25); c.lineTo(am + 3, -yi * 0.15); c.lineTo(ao - 1, yo * 0.3);
          c.strokeStyle = "#1A0512"; c.lineWidth = 2.6; c.globalAlpha = al; c.stroke();
          if (d.t < 0.36){ c.strokeStyle = P.glow; c.lineWidth = 1.3; c.globalAlpha = al * (1 - d.t / 0.36); c.stroke(); }
          c.restore();
        }
      }
      if (!(f.ramFade > 0) || f.ramOut > 0 || !f.alive) continue;
      const v = Math.hypot(f.vx, f.vy);
      /* THE STREAK: speed lines off the back of the ball, along its travel,
         long with its speed and lit only while the charge drives it at the
         foe (`ramRun`). */
      if (f.ramRun > 0.02 && v > 1){
        const ux = f.vx / v, uy = f.vy / v, nx = -uy, ny = ux, k = f.ramRun;
        const L = k * (40 + 80 * clamp(v / CONFIG.physics.speedMax, 0, 1));
        c.strokeStyle = P.glow;
        for (let j = -2; j <= 2; j++){
          const o = j * R * 0.34, back = Math.sqrt(Math.max(0, R * R - o * o));
          const Lj = L * (0.62 + 0.38 * shellHash(9811 + f.side, j + 2)) * (1 - 0.18 * Math.abs(j));
          const x0 = f.x - ux * (back + 4) + nx * o, y0 = f.y - uy * (back + 4) + ny * o;
          const x1 = x0 - ux * Lj * 0.5, y1 = y0 - uy * Lj * 0.5;
          c.globalAlpha = 0.55 * k; c.lineWidth = 2.8 - 0.4 * Math.abs(j);
          c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
          c.globalAlpha = 0.22 * k; c.lineWidth = 1.8 - 0.2 * Math.abs(j);
          c.beginPath(); c.moveTo(x1, y1); c.lineTo(x0 - ux * Lj, y0 - uy * Lj); c.stroke();
        }
      }
      this._drawRamShell(c, f, R);
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* THE SHELL: six hex plates round the glass, a hexagon from R + 2 to
     R + 18 -- the ward's ring (R + 17) thickening inward over the cast's
     0.25s -- with `dark` edges and `core` seams. THE FILL IS THE POOL:
     0.15 + 0.45 x shield / cap, so the bank reads on the ball. A slam flashes
     the plate that met the foe. */
  _drawRamShell(c, f, R){
    const P = f.aff, s = Math.min(1, f.ramAge / 0.5), e = 1 - (1 - s) * (1 - s) * (1 - s);
    const ao = R + 18, ai = R + 14 - (14 - 2) * e, t = 0.57735, gp = 1.6, ch = 4.5 * e;
    const fill = 0.15 + 0.45 * clamp(f.shield / STATUS.ward.cap, 0, 1);
    /* THE HARDENING: the plates' edges run lit as they set and cool over the
       cast's first 0.4s, so the cast reads on a shell with nothing in it yet
       (the pool is empty at most casts). */
    const hard = clamp(1 - f.ramAge / 0.8, 0, 1);
    let hit = -1, fk = 0;
    for (const hh of f.ramHits){
      if (hh.t >= 0.5) continue;
      const k2 = 1 - hh.t / 0.5;
      if (k2 * k2 > fk){ fk = k2 * k2; hit = Math.floor((((hh.a % TAU) + TAU) % TAU) / (TAU / 6)) % 6; }
    }
    c.save();
    c.translate(f.x, f.y);
    c.lineJoin = "round";
    for (let i = 0; i < 6; i++){
      c.save();
      c.rotate((i + 0.5) * TAU / 6);
      const yi = ai * t - gp, yc = (ao - ch) * t - gp, yo = yc - ch;
      c.beginPath();
      c.moveTo(ai, -yi); c.lineTo(ao - ch, -yc); c.lineTo(ao, -yo);
      c.lineTo(ao, yo); c.lineTo(ao - ch, yc); c.lineTo(ai, yi);
      c.closePath();
      c.fillStyle = P.core; c.globalAlpha = fill * (0.45 + 0.55 * e); c.fill();
      /* the struck plate flashes whole and its two neighbours half, so the
         flash reads past the foe's shell, which covers the struck plate */
      const fi = hit < 0 ? 0 : (i === hit ? 1 : ((i - hit + 6) % 6 === 1 || (hit - i + 6) % 6 === 1) ? 0.45 : 0);
      if (fi > 0){ c.fillStyle = P.glow; c.globalAlpha = 0.9 * fk * fi; c.fill(); }
      c.strokeStyle = P.dark; c.lineWidth = 2.4; c.globalAlpha = 0.5 + 0.5 * e; c.stroke();
      const lit = Math.max(hard * 0.85, fk * fi);
      if (lit > 0){ c.strokeStyle = P.glow; c.lineWidth = 1.6; c.globalAlpha = lit; c.stroke(); }
      c.restore();
    }
    c.strokeStyle = P.core; c.lineWidth = 1.8; c.globalAlpha = e;          // the seams
    c.beginPath();
    for (let i = 0; i < 6; i++){
      const q = i * TAU / 6, cq = Math.cos(q), sq = Math.sin(q);
      c.moveTo(cq * ai / 0.866, sq * ai / 0.866); c.lineTo(cq * (ao - ch) / 0.866, sq * (ao - ch) / 0.866);
    }
    c.stroke();
    c.restore();
    c.globalAlpha = 1;
  }

  drawRamTop(m){
    const a = m.a, b = m.b;
    if (!a.ramHits.length && !b.ramHits.length) return;          // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      const P = f.aff;
      for (const h of f.ramHits){
        const s2 = h.t * 0.5, ca = Math.cos(h.a), sa = Math.sin(h.a);
        /* THE GLINT: where the plate met the foe, a short cross of light
           along the two shells' shared tangent. */
        if (h.t < 0.4){
          const k = 1 - h.t / 0.4, L = 10 + 20 * (1 - k * k), l = L * 0.45;
          c.strokeStyle = P.glow; c.globalAlpha = 0.95 * k; c.lineWidth = 1.2 + 3.2 * k;
          c.beginPath();
          c.moveTo(h.x - sa * L, h.y + ca * L); c.lineTo(h.x + sa * L, h.y - ca * L);
          c.moveTo(h.x - ca * l, h.y - sa * l); c.lineTo(h.x + ca * l, h.y + sa * l);
          c.stroke();
        }
        /* SPARKS off the plate, both ways along the tangent and out, falling. */
        for (let i = 0; i < 9; i++){
          const h1 = shellHash(9821 + f.side, h.k * 16 + i), h2 = shellHash(9823 + f.side, h.k * 16 + i);
          const life = 0.55 + 0.35 * shellHash(9825 + f.side, h.k * 16 + i);
          if (h.t >= life) continue;
          const q = h.a + (i % 2 ? 1 : -1) * (0.45 + 1.05 * h1), sp = 170 + 230 * h2;
          const vx = Math.cos(q) * sp, vy = Math.sin(q) * sp + 1040 * s2;
          const x = h.x + Math.cos(q) * sp * s2, y = h.y + Math.sin(q) * sp * s2 + 520 * s2 * s2;
          const vl = Math.hypot(vx, vy) || 1, ln = 3 + 0.02 * vl, k = 1 - h.t / life;
          c.strokeStyle = i % 3 ? P.glow : "#FFFFFF"; c.globalAlpha = 0.95 * k; c.lineWidth = 1.8;
          c.beginPath(); c.moveTo(x, y); c.lineTo(x - vx / vl * ln, y - vy / vl * ln); c.stroke();
        }
      }
    }
    c.globalAlpha = 1;
    c.restore();
  }

  drawMotes(m){
'''),

]

STAGE_OUT = {"1": "sc-portcullis", "2": "sc-ram", "3": "sc-onslaught", "5": "sc-onslaught-b23",
             "6": "sc-onslaught-fx"}


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
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
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
        elif A.stage == "6":
            if f"dmg:{BLADE}," not in relic_row(code, RELIC) or "drawRamTop" in code:
                raise SystemExit("stage 6 goes on stage 5, once")
            # THE HEAD ROUTE AND THE HAFT'S BANDS ARE THE VIGIL FLAIL'S, AND
            # PORTCULLIS IS THE ONLY ONE: no other relic's picture may move.
            vf = re.findall(r'\{ id:"([a-z]+)", name:"[^"]*", aff:"vigil", shape:"flail"', code)
            if vf != [RELIC]:
                raise SystemExit(f"the vigil flails are {vf}, not Portcullis alone -- "
                                 "the head and the haft would move another relic")
            edits, want = S6, ult_block(ULT["charge"], ULT["bank"])
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
    for label, old, new in S1 + S2 + S3 + S5 + S6:
        # WHAT THE INSERT ADDS: an anchor it re-emits (a before / after row,
        # a replace row that keeps its line) is the base's, not the insert's.
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*\s*(=[^=]|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon row")
    if len(re.findall(r'kind:"ram"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one ram ultimate")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one ram ultimate, Portcullis's; no insert draws the RNG, takes the "
          f"ultFx slot or writes the shared weapon row; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
