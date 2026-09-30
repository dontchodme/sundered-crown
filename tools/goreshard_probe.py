#!/usr/bin/env python
"""BLOODPRICE'S PROBE (v114) -- one check per sentence of v81 §1 / §4 / §5, and
the build's declared readings, read INSIDE the hooks.

    python goreshard_probe.py --game <stage-2 link> --stage 2
    python goreshard_probe.py --game <stage-5 link> --stage 5

Wraps `step`, `fireUlt`, `tickPrice`, `tickCharge`, `tickWeapon`,
`bladeSegments`, `tickHits`, `resolveHit`, `resolveClank` and `checkEnd` on the
Match prototype (and, per blow, the struck fighter's `stacks` and the
attacker's `dmgMul`, to bracket the price's own lines -- hers, and every other
attacker's in her fights; and her `ultPrice` / `priceTally` as watched
accessors, [10]), and reads each event where it happens. Runs Goreshard (`oathwound`) against every other relic, both sides,
and prints N/N. The same probe gates every stage from 2 on.

THE BUILD'S NUMBERS ARE PINNED, never read from the row under test (the
Widowmaker and Spellbreaker reviews): the window (`dur` 8), the charge (14) and
`perStack` (0.3) come from the builder's ULT; the greatsword's profile (reach,
width, spin, arc, mode, mass, blades, onHit) from the builder's SHIP_HEAD; the
blade from the stage (--stage 2: the shipped 9.17; --stage 5: the builder's
TUNED). A link whose row says anything else fails the check that owns it.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration", 8 s ON THE WINDOW TICKERS' CLOCK (reading 1; the
      standing ruling): the row's `dur` anything but the build's 8; a FROZEN
      step (hitStop > 0, the latch or the split, read on entry) that moves the
      window at all; a LIVE step with the window open whose clock does not move
      by exactly dt; a clock close after any number of window steps but exactly
      the ones whose dt sum first reaches 8; a death that `tickPrice` sees and
      does not close on; a window unaccounted for (every cast is a clock close,
      a death close, or a window still set when the match ends -- reading 5 --
      counted, not failed); any relic but Goreshard carrying `ultPrice`
  [2] "every blow Goreshard lands hits harder for every stack of Hemorrhage
      the enemy is carrying", `dmg x (1 + 0.30 x foe hemorrhage stacks)` "read
      BEFORE this blow's own application (the blow pays on the stacks it found,
      then bleeds)" (§1, §4; §5's gate "measured multiplier on every window
      blow = 1 + 0.3 x stacks-before-the-blow (asserted against a log)"): a
      blow of the caster's with the window open whose damage is not exactly
      round(blade x (1 + 0.3 x n) x act dmg x desperation x jitter x Sunder
      [x critMul]) (+ the foe's curse echo, - what Bulwarden's wall ate), from
      the blow's own captured crit and jitter draws, where n is the struck
      fighter's Hemorrhage as its status holds it when the blow arrives (read
      off `status`, not through `stacks()`), and 0.3 is the builder's; or the
      row's perStack anything but 0.3. The log: the measured multiplier of every
      window blow (its blade part over the same blow rebuilt at n = 0), by n
  [3] "then bleeds", and the cap (§1 "cap 4 -> up to +120%"; reading 11): a
      blow of the caster's whose onHit is not +2 Hemorrhage where the ceiling
      cannot bind, or not stopped at hemorrhage's own 4 where it does; the
      struck fighter's `bleedCap` anything but 4 at any blow of the caster's,
      window open or shut; a window blow priced on n > 4
  [4] "in the window" and nowhere else: a blow of the caster's with the window
      SHUT whose damage is not exactly the plain blade (the same rebuild at a
      multiplier of 1)
  [5] THE BLADE IS OTHERWISE THE SHIPPED GREATSWORD, in the window and out,
      every factor rebuilt from its definition (readings 3 and 10): the row
      (reach 116, width 14, spin 3.4, arc 1.5, mode "swing", mass 3.0, blades
      [0], onHit hemorrhage 2, no knockMul, the pinned blade); THE SWING on
      every live step (swingPhase += spin x spinMul x dt x spinDir, theta = aim
      + sin(swingPhase) x arc; held while stunned; no frozen step moves it);
      THE SEGMENT (theta, from ballR - 4 to ballR + reach x act reach); THE HIT
      TEST AND THE COOLDOWN (ballR + width / 2, combat.hitCd); and for every
      blow, priced or plain, what the engine does with its damage: the KNOCK
      (combat.knock x 1.5 on a crit, away from the caster), the foe's HITSTUN
      (impact's stun off the damage handed to hurt(), with its diminishing
      return; none on a kill) and the STOP (impact's, x critStopMul, killStop
      on a kill, the wall's 0.05 and a ward shatter's 0.10 where they happen);
      THE CLANK (her side of every bind, from the two rows' masses)
  [6] THE CAST RESOLVES NOTHING ("beam out"): the cast changing ANY field of
      either fighter (every own number, flag and string, and every status) but
      the window (`ultPrice`), the tally (`priceTally`) and the engine's cast
      count (`ultsFired`) -- the beam's 16 damage and 3 Hemorrhage are gone; the
      cast drawing the RNG; adding to any array of the match but the common
      ult beat (exactly one) and the note; a stop other than the common 0.08;
      a window that is not {t 0, the row's dur}
  [7] THE CHARGE, 14 on the caster's live clock (the lab's 16 converted;
      Rick's batch ruling): the row's charge anything but the build's 14; a
      cast after any number of her live steps (steps on which `tickCharge` runs
      with her standing) but exactly the ones whose dt sum first reaches 14,
      counted from the match's start or her last cast; a fight ending owed a
      cast; a cast while her window is open (reading 6: no wait clause)
  [8] THE SHARED WEAPON IS NEVER WRITTEN (reading 4; the lab wrote `w.dmg`
      every frame): any own field of Goreshard's WEAPONS row, or of its `ult`,
      different after any step, or at any blow, from what it was when the fight
      began
  [9] THE PRICE'S OWN CODE WRITES NOTHING BUT ITS WINDOW AND ITS TALLY
      (reading 10: no status, no stop, no beat, no float, no knock, no heal):
      across every `tickPrice` call (every call while a window is open or
      closing, and one in 16 of the rest), any change to either fighter (every
      own number, flag and string, every status, every array's length), any
      shade or the match (every own number, flag and string, every array's
      length), or an RNG draw, but the window's clock, the window's close and
      the tally's frame counts; and across the price's read inside
      `resolveHit` (bracketed from the struck fighter's Hemorrhage read to the
      caster's `dmgMul` on the damage line), any change but the tally's blow
      counts
  [10] "every blow GORESHARD lands" -- THE PRICE IS HERS ALONE (v114's review,
      2026-09-30: its mutant R2 priced the foe's blows on her while her window was
      open, by her own Hemorrhage, changed 20 fights in 148 and read 9/9). In
      every other attacker's blow in her fights -- the foe's, or a shade's;
      her window open or shut -- any read or write of HER `ultPrice` or
      `priceTally` anywhere inside that `resolveHit` (both are watched
      accessors on her, armed only for the length of another's blow), or a
      read of the struck fighter's Hemorrhage between the blow's second draw
      and the attacker's `dmgMul` on the damage line (where the price's read
      and clause stand; no other attacker reads Hemorrhage there on this
      engine -- the garrote's consume is below the damage line). Coverage:
      other attackers' blows that reached the damage line with her window
      open, and with it shut

STAGE 6 (the picture and the voice, the builder's readings 13-21), each check
run only where the link carries it -- the voices detected by their own
presence in `AC.SFX.play.toString()` (Goreshard's cast arm, `w ===
"oathwound"`, and the priced-blow branch, `kind === "hit" && p.price`), the
picture by `tickGore` on the Match -- so the same probe still gates stages 2
and 5 at 10/10, every line as before; `--stage 6` requires both. Once a fight
is over the probe steps 2 s more of the verdict (the step's `over` path: only
the presentation clock runs) for these two checks alone; [1]-[10] read none of
those steps, and every [1]-[10] number on the stage-6 link must be the stage-5
link's, line for line (the picture and the voice move no fight).
  [11] THE VOICES fire exactly on their events and nowhere else (v81 §4's
      sound). Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns), each call tagged with where it
      was made. Evidence: a cast of hers playing anything but exactly one `ult`
      voice with w "oathwound", inside fireUlt, or that voice anywhere else; a
      blow of hers whose hit voice (resolveHit's own line -- a ward's shatter
      plays its own crit hit voice inside hurt(), told apart by its caller and
      never priced) is not exactly one call, carrying `price` = the stacks the
      blow was priced on with its dmg and crit when the window is open and
      n > 0, and no `price` otherwise (x1 window blows and every shut-window
      blow keep the plain call); `price` on any other call (the foe's blows, a
      shade's, a shatter); ANY voice inside tickPrice -- the design's "close --
      nothing": a window closing by its clock or on a death plays nothing, and
      never a close voice on a death; a voice of hers in the picture's hook, a
      drawn frame or the verdict. Coverage: casts voiced one for one, priced
      blows voiced at n 2 and 4 one for one, x1 and shut-window blows plain,
      the foe's blows unpriced with her window open and shut, clock closes and
      death closes silent, a quiet verdict.
  [12] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S, AND IS THE
      PICTURE DECLARED. `tickGore` (tickPresentation: the picture's one call on
      the step path, through hit stops and in the verdict) is wrapped: evidence
      is any change across it to either fighter or a shade (every own number,
      flag and string but the picture's `gore*` fields, every array's length,
      every status, the window) or to the match (every own number, flag and
      string, every array's length), an RNG draw or a voice; the foe (not
      Goreshard) carrying any of the picture; the picture up before her first
      cast. And the picture REBUILT from what the simulation did, exactly, in
      the builder's own arithmetic (readings 13-16): the red up (`goreFade` 1)
      exactly while her window is open with the match on and both standing; its
      run clock the presentation clock since the cast, the cast found by
      `priceTally.casts` rising; a drain to 0 over DRAIN of its clock at any
      close (the clock, a death, the kill with the window still set); the glow
      eased (GLOWT) toward G0 + G1 x the foe's Hemorrhage -- v81's "0 -> 4 maps
      alpha 0.2 -> 0.8", pinned from the design; the motes shed at RATE a clock
      unit while the window is open and never while it is shut, each born within
      her reach, aged to DLIFE and capped at CAP; nothing up after 2 s of the
      verdict. THE FLOAT (reading 17): the damage float of every blow in her
      fights sized exactly clamp(22 + dmg x 0.62, 22, 62) x (crit ? 1.3 : 1) x
      (1 + FK x n) for a blow of hers priced on n, and the old size (x1) for
      every other (hers with the window shut or n 0, the foe's, a shade's).
      DRAIN, GLOWT, RATE, DLIFE, CAP and FK are read from the builder's S6
      table (Code's picks); 0.2 and 0.8 are v81's.
  --drawn N (default 0 = off): on the FIRST seed, both sides, every foe,
      each fight is also drawn through the renderer (`AC.__draw`, the post
      chain off, 270x480) every Nth step while the picture shows and every
      120th otherwise, through the kill and the verdict. [12] fails a drawn
      frame that throws, draws the match's RNG, plays a voice or changes the
      simulation or the picture's clocks. It runs on any link, so the stage-5
      link's draws are its control.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
import goreshard_build as GB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--stage", choices=["2", "5", "6"], required=True,
                help="the stage this link is: pins the blade (2: the shipped 9.17; 5 and 6: the builder's TUNED); "
                     "6 also requires the picture and the voice")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=114001)
ap.add_argument("--blade", type=float, default=None, help="override the stage's blade (a variant)")
ap.add_argument("--json", default=None)
ap.add_argument("--drawn", type=int, default=0, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()

# THE PINS: the build's numbers from the builder, the one place they live.
_m = re.search(r'blades:\[([^\]]*)\], reach:([\d.]+), width:([\d.]+), artW:[\d.]+, spin:([\d.]+), '
               r'mode:"(\w+)", arc:([\d.]+), mass:([\d.]+), dmg:([\d.]+),\s*onHit:\{ hemorrhage:(\d+) \}',
               GB.SHIP_HEAD)
assert _m, "the builder's SHIP_HEAD no longer parses"
assert "knockMul" not in GB.SHIP_HEAD and "lifesteal" not in GB.SHIP_HEAD
if a.blade is not None:
    BLADE = a.blade
elif a.stage == "2":
    BLADE = float(_m.group(8))
else:
    assert GB.TUNED["dmg"] is not None, "the builder has no stage-5 blade"
    BLADE = float(GB.TUNED["dmg"])
# THE PICTURE'S NUMBERS: v81's glow map (alpha 0.2 at 0 stacks -> 0.8 at 4), and Code's picks read
# from the builder's S6 table (the tickGore row and the float's sim-path line), never from the page.
_tick = [new for label, _old, new in GB.S6 if label.startswith(GB.S6_TICK_ROW)]
assert len(_tick) == 1, "the builder has no single tickGore row"
_tick = _tick[0]


def _pin(rx, txt=None):
    m_ = re.search(rx, txt if txt is not None else _tick)
    assert m_, f"the builder's S6 no longer carries {rx}"
    return float(m_.group(1))


PIC = {"G0": 0.2, "G1": 0.15,           # v81: alpha 0.2 at 0 stacks, 0.8 at 4 (0.2 + 4 x 0.15)
       "GLOWT": _pin(r"Math\.min\(1, dt / ([\d.]+)\)"), "RATE": _pin(r"f\.goreAcc \+= dt \* ([\d.]+);"),
       "DRAIN": _pin(r"1 - f\.goreOut / ([\d.]+)\)"), "DLIFE": _pin(r"f\.goreDrops\[i\]\.t >= ([\d.]+)\)"),
       "CAP": _pin(r"f\.goreDrops\.length > (\d+)\)"),
       "FK": _pin(r"\(1 \+ ([\d.]+) \* priceN\)",
                  [v[0] for k, v in GB.S6_SIM_LINES.items() if "float" in k][0])}
assert abs(PIC["G0"] + 4 * PIC["G1"] - 0.8) < 1e-12
assert f"({PIC['G0']} + {PIC['G1']} * n - f.goreGlow)" in _tick, "the builder's glow is not v81's 0.2 -> 0.8"
PIN = {"dur": GB.ULT["dur"], "charge": GB.ULT["charge"], "perStack": GB.ULT["perStack"], "pic": PIC,
       "blades": [float(x) for x in _m.group(1).split(",")], "reach": float(_m.group(2)),
       "width": float(_m.group(3)), "spin": float(_m.group(4)), "mode": _m.group(5),
       "arc": float(_m.group(6)), "mass": float(_m.group(7)), "onHit": int(_m.group(9)),
       "blade": BLADE}

JS = r"""([seeds, PIN, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, ST = AC.STATUS;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, critCh = C.chaos.critChance;
  /* the constants every multiplier, ceiling and impulse is rebuilt from, read once before any fight */
  const ACTS = C.acts, DESP = C.desperation, SUNT = ST.sunder.taken, HB = ST.hemorrhage.maxStacks, ENT = ST.entangle.spin;
  const IMP = C.impact, CLK = C.clank, KNOCK = C.combat.knock, HITCD = C.combat.hitCd, RB = C.physics.ballR;
  const TAU = Math.PI * 2;
  const clampD = (v, a, b) => v < a ? a : v > b ? b : v;                 // the page's clamp, as defined
  const segDistD = (ax, ay, bx, by, px, py) => {                         // the page's segDist, as defined
    const dx = bx - ax, dy = by - ay, len2 = dx*dx + dy*dy;
    let t = len2 === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / len2;
    t = clampD(t, 0, 1);
    const cx = ax + dx * t, cy = ay + dy * t;
    return { d: Math.hypot(px - cx, py - cy), x: cx, y: cy };
  };
  const ROW = AC.WEAPONS.find(w => w.id === "oathwound"), U = ROW.ult;
  const MASSES = {}; for (const w of AC.WEAPONS) MASSES[w.id] = w.mass;
  /* THE PINS (the builder's numbers), never the row under test */
  const DUR = PIN.dur, CHARGE = PIN.charge, PS = PIN.perStack, SPIN = PIN.spin, REACH = PIN.reach, WIDTH = PIN.width,
        ARC = PIN.arc, MASS = PIN.mass, BLADES = PIN.blades, ONHIT = PIN.onHit, BLADE = PIN.blade;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  /* THE ROW AGAINST THE PINS: each number is failed by the check that owns it */
  if (U.kind !== "price") fail(6, `the row's ultimate is kind ${U.kind}, not the price`);
  if (U.dur !== DUR) fail(1, `the row's window is ${U.dur}, the build's ${DUR}`);
  if (U.charge !== CHARGE) fail(7, `the row's charge is ${U.charge}, the build's ${CHARGE}`);
  if (U.perStack !== PS) fail(2, `the row's perStack is ${U.perStack}, the design's ${PS}`);
  for (const k of ["dmg", "apply", "radius", "knock", "heal", "freeze"]) if (k in U) fail(6, `the row's ultimate still carries the beam's ${k}: ${JSON.stringify(U[k])}`);
  { const got = { reach: ROW.reach, width: ROW.width, spin: ROW.spin, arc: ROW.arc, mass: ROW.mass, mode: ROW.mode,
                  blades: JSON.stringify(ROW.blades), onHit: JSON.stringify(ROW.onHit), knockMul: ROW.knockMul, dmg: ROW.dmg };
    const want = { reach: REACH, width: WIDTH, spin: SPIN, arc: ARC, mass: MASS, mode: PIN.mode,
                   blades: JSON.stringify(BLADES), onHit: JSON.stringify({ hemorrhage: ONHIT }), knockMul: undefined, dmg: BLADE };
    for (const k in want) if (got[k] !== want[k]) fail(5, `the row's ${k} is ${got[k]}, the pinned greatsword's ${want[k]}`); }
  /* [8] the shared weapon row, as it stands before any fight */
  const rowSnap = () => { const o = []; for (const k of Object.keys(ROW)){ const v = ROW[k]; o.push(k, v === null || typeof v !== "object" ? v : JSON.stringify(v)); }
                          for (const k of Object.keys(U)){ const v = U[k]; o.push("ult." + k, v === null || typeof v !== "object" ? v : JSON.stringify(v)); } return o.join("|"); };
  const ROW0 = rowSnap();

  const oStep = P.step, oFire = P.fireUlt, oTick = P.tickPrice, oResolve = P.resolveHit;
  const oCharge = P.tickCharge, oWeap = P.tickWeapon, oSegs = P.bladeSegments, oHits = P.tickHits, oClank = P.resolveClank, oEnd = P.checkEnd;
  const isG = f => f && f.w && f.w.id === "oathwound";
  const isMe = f => isG(f) && !f.shade;
  /* ---- STAGE 6, DETECTED BY ITS OWN PRESENCE: Goreshard's cast arm and the priced-blow branch in the
     synth [11], `tickGore` on the match [12]. A link without them runs [1]-[10] only. ---- */
  const playSrc = AC.SFX.play.toString();
  const hasArm = /w === "oathwound"/.test(playSrc), hasBr = /kind === "hit" && p\.price/.test(playSrc);
  const S6V = hasArm && hasBr, S6P = typeof P.tickGore === "function", S6PART = hasArm !== hasBr;
  const PIC = PIN.pic, oGore = P.tickGore, oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  let FIGHT = null, vctx = "a step", vrec = null, tail = false;
  const isCastV = (kind, q) => kind === "ult" && !!q && q.w === "oathwound";
  const isPriced = (kind, q) => !!q && typeof q === "object" && Object.prototype.hasOwnProperty.call(q, "price");
  if (S6PART) fail(11, `only one of the two voice arms is on this link (cast arm ${hasArm}, priced branch ${hasBr})`);
  if (S6V !== S6P && (S6V || S6P)) fail(12, `half of stage 6 on this link (voices ${S6V}, picture ${S6P})`);
  if (S6V) AC.SFX.play = function(kind, q){
    if (FIGHT){
      if (vrec) vrec.push([kind, q && typeof q === "object" ? Object.assign({}, q) : q, vctx]);
      if (isCastV(kind, q) && vctx !== "her cast") fail(11, `her cast voice played in ${vctx}`);
      if (isPriced(kind, q) && vctx !== "her blow") fail(11, `a priced voice (price ${q.price}) played in ${vctx}`);
    }
    return oPlay.call(this, kind, q);
  };
  const GORE = new Set(["goreFade", "goreAge", "goreOut", "goreGlow", "goreSeen", "goreAcc", "goreDropN", "goreDrops",
                        "goreTh", "goreT", "goreW"]);
  const floatOld = (d, crit) => clampD(22 + d * 0.62, 22, 62) * (crit ? 1.3 : 1);
  /* a blow's damage float: the call at the blow's point whose text is its number (and "!" on a crit) */
  const dmgFloat = (fl, hx, hy) => { let r = null; for (const q of fl) if (q.x === hx && q.y === hy && /^\d+(\.\d+)?!?$/.test(String(q.text))) r = q; return r; };
  /* [9] the simulation's state, as one array in a fixed key order: both
     fighters' own numbers, flags and strings, every array's length, every
     status, the window and the tally; every shade's the same; the match's own
     numbers, flags and strings and every array's length. The weapon row is
     [8]'s. `skip` names what the code under test may move. */
  const snapF = (f, o, skip) => {
    for (const k of Object.keys(f)){
      if (skip && skip.has(k)) continue;
      const v = f[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
      else if (Array.isArray(v)) o.push(k, v.length);
    }
    for (const k in f.status){ const s = f.status[k]; o.push(k, s.stacks, s.t, s.src); }
    if (f.hitCd) o.push(...f.hitCd);
  };
  const simSnap = (m, skip) => {
    const o = [];
    for (const f of [m.a, m.b]) snapF(f, o, skip);
    for (const s of (m.shades || [])) snapF(s, o, null);
    for (const k of Object.keys(m)){
      const v = m[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
      else if (Array.isArray(v)) o.push(k, v.length);
    }
    return o;
  };
  const same = (p, q) => p === q || (Number.isNaN(p) && Number.isNaN(q));
  const diffAt = (s0, s1) => { if (s0.length !== s1.length) return `the shape ${s0.length} -> ${s1.length}`;
    for (let i = 0; i < s0.length; i++) if (!same(s0[i], s1[i])) return `${typeof s0[i - 1] === "string" ? s0[i - 1] : "field " + i} ${s0[i]} -> ${s1[i]}`; return null; };

  let nClock = 0; { let t = 0; while (t < DUR){ t += DT; nClock++; } }
  let nCharge = 0; { let t = 0; while (t < CHARGE){ t += DT; nCharge++; } }
  const live = new WeakMap();       // window -> tickPrice increments (the window clock)
  const mt = new WeakMap();         // window -> steps of match time
  let per = null, castStep = 0, weapN = 0, chargeLive = 0, hitLog = null, inEnd = false, tickN = 0;
  const log = {};                   // [2] the multiplier's log, by n: [blows, sum of measured multipliers]

  /* the greatsword's one segment, from its definition */
  const segsDef = (m, f) => {
    const reach = REACH * ACTS[m.act].reach * 1, out = [];
    for (const off of BLADES){
      const a = f.theta + off * TAU, ca = Math.cos(a), sa = Math.sin(a);
      out.push({ ax: f.x + ca * (RB - 4), ay: f.y + sa * (RB - 4), bx: f.x + ca * (RB + reach), by: f.y + sa * (RB + reach), a });
    }
    return out;
  };

  P.step = function(dt){
    if (tail) return oStep.call(this, dt);          /* the verdict: [11]-[12] only */
    for (const f of [this.a, this.b]) if (f.ultPrice && !isMe(f)) fail(1, `${f.w.id}${f.shade ? " (a shade)" : ""} carries ultPrice`);
    for (const s of (this.shades || [])) if (s.ultPrice) fail(1, "a shade carries ultPrice");
    const W = isMe(this.a) ? this.a : isMe(this.b) ? this.b : null;
    if (!W) return oStep.call(this, dt);
    /* [1] THE WINDOW TICKERS' CLOCK: the step's path, and the window and its
       clock as they stood, read on entry */
    const frozen = !this.over && (this.hitStop > 0 || !!this.latch || !!this.splitHold);
    const liveStep = !this.over && !frozen;
    const z0 = W.ultPrice, zt0 = z0 ? z0.t : null;
    if (z0 && !this.over){ inc("winSteps"); mt.set(z0, (mt.get(z0) || 0) + 1); if (frozen) inc("winFrozen"); }
    castStep = 0; weapN = 0;
    const th0 = W.theta, ph0 = W.swingPhase;
    const r = oStep.call(this, dt);
    if (frozen){
      if (W.ultPrice !== z0 || (z0 && z0.t !== zt0))
        fail(1, `a frozen step moved the window: t ${zt0} -> ${W.ultPrice ? W.ultPrice.t : null}${W.ultPrice !== z0 ? " (opened/closed)" : ""}`);
      else if (z0) inc("winHeldFrozen");
      /* [5] and no frozen step moves her swing */
      if (weapN !== 0 || W.theta !== th0 || W.swingPhase !== ph0) fail(5, `her swing moved on a frozen step: ${th0} -> ${W.theta}`);
      else inc("turnFrozenOk");
    } else if (liveStep){
      if (z0 && !castStep){
        if (z0.t !== zt0 + dt) fail(1, `a live step moved the window's clock by ${z0.t - zt0}, want ${dt}`);
        else if (W.ultPrice === z0) inc("winLiveAdv");
        else if (W.ultPrice === null) inc("winLiveClose");
        else fail(1, "a live step replaced an open window");
      }
      if (weapN !== 1) fail(5, `her weapon ticked ${weapN} times on a live step`);
    }
    /* [8] the shared weapon row, after every step */
    if (rowSnap() !== ROW0) fail(8, `the shared weapon row moved during a step (her window ${W.ultPrice ? "open" : "shut"}): dmg ${ROW.dmg}`);
    else inc(W.ultPrice ? "rowStepIn" : "rowStepOut");
    return r;
  };

  P.checkEnd = function(){ inEnd = true; try { return oEnd.call(this); } finally { inEnd = false; } };

  /* [7] HER LIVE CLOCK: the steps on which the charge runs with her standing */
  P.tickCharge = function(f, foe, dt){
    if (isMe(f) && f.hp > 0 && !this.over) chargeLive++;
    return oCharge.call(this, f, foe, dt);
  };

  /* [6] every own number, flag and string of a fighter, and every status */
  const snapObj = (x, mine) => {
    const o = {};
    for (const k of Object.keys(x)){
      if (mine && (k === "ultPrice" || k === "priceTally" || k === "ultsFired")) continue;
      const v = x[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o[k] = v;
      else if (Array.isArray(v)) o[k + "#"] = v.length;
    }
    o["status"] = JSON.stringify(Object.entries(x.status).map(([k, s]) => [k, s.stacks, s.t, s.src]));
    return o;
  };

  P.fireUlt = function(f, foe){
    if (!isMe(f)){ const vc = vctx; vctx = "another's cast"; try { return oFire.call(this, f, foe); } finally { vctx = vc; } }
    castStep++; if (per) per.casts++;
    if (f.ultPrice) fail(7, `a cast with the window at ${f.ultPrice.t.toFixed(3)} of ${f.ultPrice.dur}`); else inc("castOk");
    if (chargeLive !== nCharge) fail(7, `a cast after ${chargeLive} steps of her live clock, want ${nCharge} (charge ${CHARGE})`);
    else inc("cadenceOk");
    chargeLive = 0;
    const s0 = snapObj(foe, false), m0 = snapObj(f, true), hs0 = this.hitStop, len0 = {};
    for (const k of Object.keys(this)) if (Array.isArray(this[k])) len0[k] = this[k].length;
    let draws = 0; const oRng = this.rng;
    this.rng = () => { draws++; return oRng(); };
    let r;
    const vc0 = vctx, vr0 = vrec; vctx = "her cast"; vrec = [];
    let heardCast = null;
    try { r = oFire.call(this, f, foe); } finally { this.rng = oRng; heardCast = vrec; vctx = vc0; vrec = vr0; }
    /* [11] THE CAST'S VOICE: exactly one, inside fireUlt (the common `SFX.play("ult", { w: f.w.id })`) */
    if (S6V){
      const cv = heardCast.filter(c => isCastV(c[0], c[1]));
      if (cv.length !== 1) fail(11, `a cast of hers played ${cv.length} cast voices (${JSON.stringify(heardCast.map(c => c[0] + (c[1] && c[1].w ? "/" + c[1].w : "")))})`);
      else inc("v11CastOk");
    }
    const s1 = snapObj(foe, false), m1 = snapObj(f, true);
    let clean = true;
    for (const k of new Set([...Object.keys(s0), ...Object.keys(s1)]))
      if (!same(s0[k], s1[k])){ clean = false; fail(6, `the cast moved the foe's ${k}: ${s0[k]} -> ${s1[k]}`); }
    for (const k of new Set([...Object.keys(m0), ...Object.keys(m1)]))
      if (!same(m0[k], m1[k])){ clean = false; fail(6, `the cast moved her ${k}: ${m0[k]} -> ${m1[k]}`); }
    if (draws){ clean = false; fail(6, `the cast drew the RNG ${draws} times`); }
    for (const k in len0){
      const d = this[k].length - len0[k];
      if (k === "beats"){ if (d !== 1 || this.beats[this.beats.length - 1].kind !== "ult"){ clean = false; fail(6, `the cast filed ${d} beats (want the common ult beat)`); } }
      else if (k === "events") continue;          // the cast's note, the common head's
      else if (d){ clean = false; fail(6, `the cast added ${d} to ${k}`); }
    }
    if (this.hitStop !== Math.max(hs0, 0.08)){ clean = false; fail(6, `hitStop ${hs0} -> ${this.hitStop}`); }
    if (!f.ultPrice || f.ultPrice.t !== 0 || f.ultPrice.dur !== U.dur){ clean = false; fail(6, "the cast did not open {t 0, dur}"); }
    if (clean) inc("castClean");
    if (f.ultPrice) live.set(f.ultPrice, 0);
    return r;
  };

  P.tickPrice = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]) if (f.ultPrice){
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z: f.ultPrice, t1: f.ultPrice.t + dt, fa: f.alive, oa: foe.alive,
                 T0: f.priceTally ? [f.priceTally.casts, f.priceTally.frames, f.priceTally.foeStk, f.priceTally.blows, f.priceTally.stk] : null,
                 stk: foe.stacks("hemorrhage") });
    }
    /* [9] every call with a window open (or closing), one in 16 of the rest */
    tickN++;
    const snap = pre.length > 0 || (tickN & 15) === 0;
    const skip = new Set(["ultPrice", "priceTally"]);
    const s0 = snap ? simSnap(this, skip) : null;
    let draws = 0; const oRng = this.rng;
    this.rng = () => { draws++; return oRng(); };
    let r;
    const vc0 = vctx, vr0 = vrec; vctx = "the price's ticker"; vrec = [];
    let heardT = null;
    try { r = oTick.call(this, dt); } finally { this.rng = oRng; heardT = vrec; vctx = vc0; vrec = vr0; }
    /* [11] "close -- nothing": the window's ticker plays no voice, by its clock or ON A DEATH */
    if (S6V && heardT.length) fail(11, `the window's ticker played ${JSON.stringify(heardT.map(c => c[0] + (c[1] && c[1].w ? "/" + c[1].w : "")))}${pre.some(q => !q.fa || !q.oa) ? " -- ON A DEATH" : ""}`);
    if (snap){
      const d = diffAt(s0, simSnap(this, skip));
      if (d) fail(9, `tickPrice moved ${d}${pre.length ? "" : " (no window open)"}`);
      else if (draws) fail(9, `tickPrice drew the RNG ${draws} times`);
      else inc(pre.length ? "tickCleanWin" : "tickCleanIdle");
    }
    for (const f of [this.a, this.b]) if (!pre.some(p => p.f === f) && f.ultPrice) fail(9, "tickPrice opened a window");
    for (const p of pre){
      const k = (live.get(p.Z) || 0) + 1; live.set(p.Z, k);
      const clock = p.t1 >= p.Z.dur, death = !p.fa || !p.oa;
      const T = p.f.priceTally, T1 = [T.casts, T.frames, T.foeStk, T.blows, T.stk];
      if (clock || death){
        if (p.f.ultPrice){ fail(1, "the window did not close"); continue; }
        if (T1.some((v, i) => v !== p.T0[i])) fail(9, "a closing tickPrice moved the tally");
        inc("closes"); if (per) per.closes++;
        if (S6V && !heardT.length) inc(death ? "v11CloseDeathQuiet" : "v11CloseClockQuiet");
        if (!death){ if (k !== nClock) fail(1, `a clock close after ${k} window steps, want ${nClock} (${DUR}s)`); else { inc("clockOk"); inc("clockMatchSteps", mt.get(p.Z) || 0); } }
        else inc("deathClose");
      } else {
        if (p.f.ultPrice !== p.Z){ fail(1, `closed at ${p.t1.toFixed(3)} of ${p.Z.dur} with both alive`); continue; }
        if (p.Z.t !== p.t1) fail(1, "the window clock is not t + dt");
        if (T1[1] !== p.T0[1] + 1 || T1[2] !== p.T0[2] + p.stk || T1[0] !== p.T0[0] || T1[3] !== p.T0[3] || T1[4] !== p.T0[4])
          fail(9, `tickPrice's tally moved otherwise than one frame and the foe's stacks: ${p.T0} -> ${T1}`);
        inc("winFrames"); inc("winFoeStk", p.stk);
      }
    }
    return r;
  };

  /* [5] THE SWING: once a live step, from its definition */
  P.tickWeapon = function(f, foe, dt){
    if (!isMe(f)) return oWeap.call(this, f, foe, dt);
    weapN++;
    const th0 = f.theta, ph0 = f.swingPhase, dir = f.spinDir, stun0 = f.stun, open = !!f.ultPrice;
    const ent = f.status.entangle ? f.status.entangle.stacks : 0;
    let sm = ACTS[this.act].spin * (1 + ENT * ent);
    if (f.hp > 0 && f.hp / f.maxHp <= DESP.at) sm *= DESP.spin;
    sm = Math.max(0.15, sm);
    const spin = SPIN * sm * 1;
    let wPh = ph0, wTh = th0;
    if (!(stun0 > 0)){
      const aim = Math.atan2(foe.y - f.y, foe.x - f.x);
      wPh = ph0 + spin * dt * dir;
      wTh = aim + Math.sin(wPh) * ARC;
    }
    const r = oWeap.call(this, f, foe, dt);
    if (f.swingPhase !== wPh || f.theta !== wTh) fail(5, `${open ? "IN" : "out of"} the window: her swing phase ${ph0} -> ${f.swingPhase} (want ${wPh}), theta -> ${f.theta} (want ${wTh})${stun0 > 0 ? " (stunned)" : ""}`);
    else inc(stun0 > 0 ? "turnStunOk" : open ? "turnIn" : "turnOut");
    return r;
  };

  /* [5] THE SEGMENT: every one of hers, wherever it is asked for */
  P.bladeSegments = function(f){
    const r = oSegs.call(this, f);
    if (!isMe(f)) return r;
    const e = segsDef(this, f);
    if (r.length !== e.length || r.some((s, i) => s.ax !== e[i].ax || s.ay !== e[i].ay || s.bx !== e[i].bx || s.by !== e[i].by || s.a !== e[i].a))
      fail(5, `${f.ultPrice ? "IN" : "out of"} the window: her blade segment is not the greatsword's (reach ${REACH} x act ${ACTS[this.act].reach})`);
    else inc(f.ultPrice ? "segIn" : "segOut");
    return r;
  };

  /* [5] THE HIT TEST AND THE COOLDOWN, rebuilt from the width and hitCd */
  P.tickHits = function(self, foe, dt, cool){
    if (!isMe(self)) return oHits.call(this, self, foe, dt, cool);
    const open = !!self.ultPrice;
    const early = (this.killFlight && self.hp <= 0) || !(self.hp > 0) || !(foe.hp > 0);
    const cd0 = BLADES.map((_, i) => self.hitCd[i]);
    const exp = { cd: [], hits: [] };
    if (!early){
      const segs = segsDef(this, self);
      for (let i = 0; i < segs.length; i++){
        let cd = Math.max(0, (cd0[i] || 0) - (cool === false ? 0 : dt));
        if (!(cd > 0 || self.stun > 0)){
          const s = segs[i], h = segDistD(s.ax, s.ay, s.bx, s.by, foe.x, foe.y);
          if (h.d < RB + WIDTH * 0.5){ cd = HITCD; exp.hits.push(s.a); }
        }
        exp.cd.push(cd);
      }
    }
    const outer = hitLog; hitLog = [];
    let r, lg;
    try { r = oHits.call(this, self, foe, dt, cool); } finally { lg = hitLog; hitLog = outer; }
    const got = BLADES.map((_, i) => self.hitCd[i]);
    if (early){
      if (lg.length || got.some((v, i) => v !== cd0[i])) fail(5, `her tickHits struck ${lg.length} or moved a cooldown with her or the foe down`);
      else inc("hitSkipOk");
    } else if (got.some((v, i) => v !== exp.cd[i])) fail(5, `${open ? "IN" : "out of"} the window: her blade cooldown ${got}, want ${exp.cd} (hitCd ${HITCD})`);
    else if (lg.length !== exp.hits.length || lg.some((x, i) => x !== exp.hits[i]))
      fail(5, `${open ? "IN" : "out of"} the window: her blade landed ${lg.length} blows, the hit test (reach ${REACH}, width ${WIDTH}) wants ${exp.hits.length}`);
    else inc(open ? "hitTestIn" : "hitTestOut");
    return r;
  };

  /* [5] THE CLANK: her side of every bind, from the two rows' masses */
  P.resolveClank = function(A, B, hx, hy){
    const meA = isMe(A), meB = isMe(B);
    if (!meA && !meB) return oClank.call(this, A, B, hx, hy);
    const me = meA ? A : B, open = !!me.ultPrice;
    const s0 = { dir: me.spinDir, stun: me.stun, vx: me.vx, vy: me.vy };
    const st = Math.min(CLK.maxStreak, this.clankStreak + 1);
    const knockMul = 1 + CLK.knockGrowth * st, stunMul = 1 / (1 + CLK.stunFalloff * st);
    if ((me.massMul ?? 1) !== 1) fail(5, `her clank mass multiplier is ${me.massMul}, not 1`);
    const mA = (meA ? MASS : MASSES[A.w.id]) * (A.massMul ?? 1), mB = (meB ? MASS : MASSES[B.w.id]) * (B.massMul ?? 1);
    const wA = Math.pow(mA, 1.7), wB = Math.pow(mB, 1.7), tot = wA + wB;
    const shareA = wB / tot, shareB = wA / tot;
    const decisive = Math.abs(shareA - shareB) > 0.16, aWins = shareA < shareB;
    /* her spin lock: none (she has no ultSpin and no ultWire) */
    const flip = meA ? (!decisive || !aWins) : (!decisive || aWins);
    const share = meA ? shareA : shareB;
    const dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy) || 1, nx = dx / d, ny = dy / d;
    const want = { dir: flip ? s0.dir * -1 : s0.dir, stun: Math.max(s0.stun, CLK.stun * share * 2 * stunMul),
                   vx: meA ? s0.vx - nx * CLK.knock * shareA * 2 * knockMul : s0.vx + nx * CLK.knock * shareB * 2 * knockMul,
                   vy: meA ? s0.vy - ny * CLK.knock * shareA * 2 * knockMul : s0.vy + ny * CLK.knock * shareB * 2 * knockMul };
    const r = oClank.call(this, A, B, hx, hy);
    const got = { dir: me.spinDir, stun: me.stun, vx: me.vx, vy: me.vy };
    const off = Object.keys(want).filter(k => got[k] !== want[k]);
    if (off.length) fail(5, `a clank ${open ? "IN" : "out of"} the window: her ${off.map(k => `${k} ${s0[k]} -> ${got[k]} (want ${want[k]})`).join(", ")}`);
    else inc(open ? "clankIn" : "clankOut");
    return r;
  };

  /* [10] THE PRICE IS HERS ALONE. Her `ultPrice` and `priceTally` are watched
     accessors for the whole fight (installed on her in the fight loop below,
     backed by `herStore`); they record only while `herWatch` is set, which
     is for the length of another attacker's `resolveHit`. The accessor
     returns exactly what the field holds, so no fight moves (the unmutated
     link reads the same win rate and counts as the probe without [10]). */
  let herWatch = null;
  const otherBlow = function(G, self, foe, hx, hy, seg_, mul, over){
    const open = !!G.ultPrice, who = self.shade ? "a shade's" : `${self.w ? self.w.id : "?"}'s`;
    let draws = 0, pastDmg = false, bleed = 0;
    const oRng = this.rng;
    this.rng = () => { draws++; return oRng(); };
    const hadS = Object.prototype.hasOwnProperty.call(foe, "stacks"), oS = foe.stacks;
    foe.stacks = function(key){
      if (key === "hemorrhage" && draws >= 2 && !pastDmg) bleed++;
      return oS.call(this, key);
    };
    const canD = typeof self.dmgMul === "function";
    const hadD = Object.prototype.hasOwnProperty.call(self, "dmgMul"), oD = self.dmgMul;
    if (canD) self.dmgMul = function(x){ pastDmg = true; return oD.call(this, x); };
    const outer = herWatch; herWatch = [];
    const vc0 = vctx, vr0 = vrec; vctx = "another's blow"; vrec = [];
    const fl = [], hadF = Object.prototype.hasOwnProperty.call(this, "float"), oF = this.float;
    this.float = function(x, y, text, color, size){ fl.push({ x, y, text, size }); return oF.call(this, x, y, text, color, size); };
    let r, seen, heardO;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally {
      seen = herWatch; herWatch = outer;
      heardO = vrec; vctx = vc0; vrec = vr0;
      if (hadF) this.float = oF; else delete this.float;
      this.rng = oRng;
      if (hadS) foe.stacks = oS; else delete foe.stacks;
      if (canD){ if (hadD) self.dmgMul = oD; else delete self.dmgMul; }
    }
    const where = `${who} blow on ${foe === G ? "her" : foe.shade ? "a shade" : "?"} with her window ${open ? "OPEN" : "shut"}`;
    if (seen.length) fail(10, `${where} touched her ${[...new Set(seen)].join(", ")}`);
    else if (bleed) fail(10, `${where} read the struck fighter's Hemorrhage ${bleed}x between its second draw and its dmgMul (a price on another's blow)`);
    else if (pastDmg) inc((self.shade ? "othShade" : "oth") + (open ? "In" : "Out"));
    /* [11] another's blow is never priced (the wrapper fails a priced call by where it was made) */
    if (S6V && pastDmg && !heardO.some(c => isPriced(c[0], c[1]))) inc(open ? "v11OthIn" : "v11OthOut");
    /* [12] and its damage float is the old size */
    if (S6P && pastDmg){
      const q = dmgFloat(fl, hx, hy);
      if (q){
        const t = String(q.text), d = parseFloat(t), cr = t.endsWith("!");
        if (q.size !== floatOld(d, cr)) fail(12, `${where}: its damage float ${q.size}, want the old size ${floatOld(d, cr)}`);
        else inc("f12Oth");
      }
    }
    return r;
  };

  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isMe(self)){
      const G = isMe(this.a) ? this.a : isMe(this.b) ? this.b : null;
      if (!G) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
      return otherBlow.call(this, G, self, foe, hx, hy, seg_, mul, over);
    }
    const open = !!self.ultPrice, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    if (mul !== undefined) fail(5, `a blow of hers with mul ${mul} (the greatsword has no projectile)`);
    if (hitLog) hitLog.push(seg_ ? seg_.a : NaN); else fail(5, "a blow of hers landed outside her tickHits");
    if (rowSnap() !== ROW0) fail(8, `the shared weapon row has moved at a blow of hers (window ${open ? "open" : "shut"}): dmg ${ROW.dmg}`);
    else inc(open ? "rowBlowIn" : "rowBlowOut");
    /* THE MULTIPLIERS FROM THEIR DEFINITIONS, never from the engine's own
       methods: the act's dmg, desperation, Sunder's `taken` per stack on the
       struck fighter -- and THE PRICE'S n, the struck fighter's Hemorrhage as
       its STATUS holds it when the blow arrives (not through `stacks()`). */
    const desp = self.hp > 0 && self.hp / self.maxHp <= DESP.at;
    const nFound = foe.status.hemorrhage ? foe.status.hemorrhage.stacks : 0;
    const pre = { dm: ACTS[this.act].dmg * (desp ? DESP.dmg : 1),
                  dt: 1 + SUNT * (foe.status.sunder ? foe.status.sunder.stacks : 0),
                  echo: Math.round((foe.cursePool || []).reduce((x, v) => x + v, 0) * ST.curse.echo),
                  wall: foe.ultAegis || null, ate: foe.ultAegis ? foe.ultAegis.ate : 0,
                  bl: nFound, ceil: foe.bleedCap,
                  vx: foe.vx, vy: foe.vy, kx: foe.x - self.x, ky: foe.y - self.y,
                  stun: foe.stun, sdr: foe.stunDR, hs: this.hitStop, sh: foe.shield };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let hurtD = null; const oHurt = this.hurt;
    this.hurt = function(t, d, s){
      if (t === foe && hurtD === null) hurtD = d;
      const vh = vctx; vctx = "hurt() in her blow";
      try { return oHurt.call(this, t, d, s); } finally { vctx = vh; }
    };
    const flH = [], oFl = this.float;
    this.float = function(x, y, text, color, size){ flH.push({ x, y, text, size }); return oFl.call(this, x, y, text, color, size); };
    /* [9] THE PRICE'S READ, BRACKETED: from the struck fighter's Hemorrhage
       read to the caster's dmgMul on the damage line. Between the two, only
       the tally's blow counts may move. */
    /* (the tally is an object, so the snapshot holds none of it: it is
       compared on its own, one blow and its n) */
    const M = this;
    let brk = null, brkState = 0, brkD = null, nRead = null, T0 = null, pastDmg = false;
    const oStacks = foe.stacks, oDM = self.dmgMul;
    foe.stacks = function(key){
      const v = oStacks.call(this, key);
      if (key === "hemorrhage" && brkState === 0 && !pastDmg && draws.length === 2){
        brkState = 1; nRead = v; brk = simSnap(M, null);
        const T = self.priceTally; T0 = T ? [T.casts, T.frames, T.foeStk, T.blows, T.stk] : null;
      }
      return v;
    };
    self.dmgMul = function(x){
      if (!pastDmg){
        pastDmg = true;
        if (brkState === 1){ brkState = 2; brkD = diffAt(brk, simSnap(M, null)); }
      }
      return oDM.call(this, x);
    };
    let r;
    const watch0 = herWatch; herWatch = null;       /* [10] her own blow is not another's */
    const vcB = vctx, vrB = vrec; vctx = "her blow"; vrec = [];
    let heardB = null;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { herWatch = watch0; this.rng = oRng; delete this.hurt; delete this.float; delete foe.stacks; delete self.dmgMul;
              heardB = vrec; vctx = vcB; vrec = vrB; }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    /* [9] the bracket's verdict (a window blow reads the stacks; a shut one reads nothing) */
    if (open){
      if (brkState !== 2) fail(9, `a window blow of hers never read the struck fighter's Hemorrhage before the damage line (bracket ${brkState})`);
      else {
        const T = self.priceTally, T1 = T ? [T.casts, T.frames, T.foeStk, T.blows, T.stk] : null;
        const tallyOk = T0 && T1 && T1[0] === T0[0] && T1[1] === T0[1] && T1[2] === T0[2] && T1[3] === T0[3] + 1;
        if (brkD) fail(9, `the price's read moved ${brkD}`);
        else if (!tallyOk) fail(9, `the price's read moved the tally otherwise than one blow: ${T0} -> ${T1}`);
        else inc("readClean");
        /* [2] the n the price recorded is the n the blow found */
        if (nRead !== pre.bl || !(T1 && T1[4] === T0[4] + pre.bl)) fail(2, `the price read n ${nRead} and recorded ${T1 && T0 ? T1[4] - T0[4] : "?"}, the struck fighter's status held ${pre.bl}`);
      }
    } else if (brkState !== 0) fail(4, "a blow of hers with the window shut read the struck fighter's Hemorrhage for the price");
    const D = self.dealt - d0, crit = draws[0] < critCh;       // the crit from its draw, not the engine's count
    if (crit !== (self.crits > c0)) fail(5, `${open ? "IN" : "out of"} the window: the crit draw ${draws[0]} says ${crit}, the engine counted ${self.crits > c0}`);
    const fatal = foe.hp <= 0, Dh = hurtD === null ? D : hurtD;
    if (hurtD === null) fail(5, `${open ? "IN" : "out of"} the window: her blow never reached hurt()`);
    const jit = 1 + (draws[1] - 0.5) * jitK;
    const k = open ? 1 + PS * pre.bl : 1;
    const raw = BLADE * k * pre.dm * jit * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    const eaten = pre.wall ? pre.wall.ate - pre.ate : 0;
    const wantD = want + pre.echo - eaten;
    const chk = open ? 2 : 4;
    if (Math.abs(Dh - wantD) > 1e-6 || Math.abs(D - Dh) > 1e-6)
      fail(chk, `${open ? "IN" : "out of"} the window: dealt ${D} (to hurt ${Dh}), want ${wantD} (blade ${want}${open ? ` at n ${pre.bl}, x${k}` : ""}${pre.echo ? `, echo +${pre.echo}` : ""}${eaten ? `, wall -${eaten}` : ""})`);
    else if (open){
      inc(foe.shade ? "blowInShade" : pre.echo || eaten ? "blowInFoeRule" : "blowInOk");
      inc("stkAtBlow", pre.bl);
      if (pre.bl > HB) fail(3, `a window blow priced on n ${pre.bl} > hemorrhage's ${HB}`);
      /* the log: the measured multiplier, the blade part as dealt over the same blow at n 0 */
      const raw0 = BLADE * pre.dm * jit * pre.dt * (crit ? critMul : 1);
      const L = log[pre.bl] || (log[pre.bl] = [0, 0, 0]);
      L[0]++; L[1] += want / raw0;
      /* the read is load-bearing: the count after its own onHit would have priced it otherwise */
      const nPost = Math.min(HB, pre.bl + ONHIT), rawP = BLADE * (1 + PS * nPost) * pre.dm * jit * pre.dt;
      if (Math.round(crit ? rawP * critMul : rawP) !== want) L[2]++;
      if (pre.bl > 0){ const w1 = Math.round(crit ? raw0 : raw0); if (w1 !== want) inc("blowScaledDiff"); }
    } else inc(pre.echo || eaten ? "blowOutFoeRule" : "blowOutOk");
    /* THE KNOCK: combat.knock x 1.5 on a crit (her row has no knockMul), away from her */
    const kl = Math.hypot(pre.kx, pre.ky) || 1, power = KNOCK * 1 * (crit ? 1.5 : 1) * 1;
    const wvx = pre.vx + (pre.kx / kl) * power, wvy = pre.vy + (pre.ky / kl) * power;
    if (foe.vx !== wvx || foe.vy !== wvy) fail(5, `${open ? "IN" : "out of"} the window: her blow's knock moved the foe's velocity ${foe.vx - pre.vx}, ${foe.vy - pre.vy}; want ${wvx - pre.vx}, ${wvy - pre.vy}`);
    else inc(open ? "knockIn" : "knockOut");
    /* THE FOE'S HITSTUN: impact's, off the damage handed to hurt(), with its diminishing return; none on a kill */
    let wStun = pre.stun, wDR = pre.sdr;
    if (!fatal){
      const sraw = Math.min(IMP.stunMax, IMP.stunBase + Dh * IMP.stunPerDmg);
      wStun = Math.max(pre.stun, sraw / (1 + IMP.stunDR * pre.sdr)); wDR = pre.sdr + 1;
    }
    if (foe.stun !== wStun || foe.stunDR !== wDR) fail(5, `${open ? "IN" : "out of"} the window: her blow left the foe's stun ${foe.stun} (DR ${foe.stunDR}), want ${wStun} (DR ${wDR})`);
    else inc(open ? "stunIn" : "stunOut");
    /* THE STOP: impact's off the damage, x critStopMul, killStop on a kill; the wall's 0.05; the ward shatter's 0.10 */
    let stop = Math.min(IMP.stopMax, IMP.stopBase + Dh * IMP.stopPerDmg);
    if (crit) stop *= IMP.critStopMul;
    if (fatal) stop = IMP.killStop;
    const shattered = pre.sh > 0 && Dh > 0 && pre.sh - Math.min(pre.sh, Dh) <= 0;
    const wHs = Math.max(pre.hs, eaten > 0 ? 0.05 : -Infinity, shattered ? 0.10 : -Infinity, stop);
    if (this.hitStop !== wHs) fail(5, `${open ? "IN" : "out of"} the window: her blow's stop ${this.hitStop}, want ${wHs}`);
    else inc(open ? "stopIn" : "stopOut");
    if (shattered) inc("wardShatter");
    /* [3] THEN BLEEDS: +2 where the ceiling cannot bind, hemorrhage's own 4 where it does */
    if (pre.ceil !== HB) fail(3, `her blow ${open ? "IN" : "out of"} the window: the struck fighter's bleed ceiling ${pre.ceil}, want hemorrhage's ${HB}`);
    const bl = foe.status.hemorrhage ? foe.status.hemorrhage.stacks : 0;
    if (pre.bl + ONHIT <= HB){
      if (bl !== pre.bl + ONHIT) fail(3, `onHit ${open ? "IN" : "out of"} the window: hemorrhage ${pre.bl} -> ${bl}, want +${ONHIT}`); else inc(open ? "bleedIn" : "bleedOut");
    } else {
      const wantBl = pre.bl < HB ? HB : pre.bl;
      if (bl !== wantBl) fail(3, `onHit at the ceiling ${open ? "IN" : "out of"} the window: hemorrhage ${pre.bl} -> ${bl}, want ${wantBl}`);
      else inc(open ? "ceilBindIn" : "ceilBindOut");
    }
    /* [11] HER BLOW'S VOICE: resolveHit's own hit line, priced exactly when the window is open and n > 0 */
    if (S6V){
      const own = heardB.filter(c => c[2] === "her blow" && c[0] === "hit");
      const nPaid = open ? pre.bl : 0;
      if (own.length !== 1) fail(11, `a blow of hers played ${own.length} hit voices from its own line (${JSON.stringify(own.map(c => c[1]))})`);
      else {
        const q = own[0][1] || {};
        if (nPaid > 0){
          if (!isPriced("hit", q) || q.price !== nPaid || !(Math.abs(q.dmg - D) < 1e-6) || q.crit !== crit)
            fail(11, `a blow of hers priced on n ${nPaid} voiced ${JSON.stringify(q)}, want price ${nPaid}, dmg ${D}, crit ${crit}`);
          else inc("v11Priced" + nPaid);
        } else if (isPriced("hit", q)) fail(11, `a ${open ? "x1 window" : "shut-window"} blow of hers voiced price ${q.price}`);
        else if (!(Math.abs(q.dmg - D) < 1e-6) || q.crit !== crit) fail(11, `a blow of hers voiced dmg ${q.dmg} crit ${q.crit}, dealt ${D} crit ${crit}`);
        else inc(open ? "v11PlainX1" : "v11PlainShut");
      }
      if (heardB.some(c => c[2] === "hurt() in her blow" && c[0] === "hit")) inc("v11Shatter");
    }
    /* [12] HER BLOW'S FLOAT: x(1 + FK x n) on a priced blow, the old size otherwise */
    if (S6P){
      /* the float prints the blow's own `dmg` (a wall that ate part of it leaves a fraction): read it off the
         text, which round-trips the number exactly, and hold it to what she dealt */
      const nPaid = open ? pre.bl : 0, q = dmgFloat(flH, hx, hy);
      const qd = q ? parseFloat(String(q.text)) : NaN, want = floatOld(qd, crit) * (1 + PIC.FK * nPaid);
      if (!q) fail(12, `a blow of hers (dealt ${D}) drew no damage float at its point`);
      else if (!(Math.abs(qd - D) < 1e-6) || String(q.text).endsWith("!") !== crit) fail(12, `her blow's float reads ${q.text}, dealt ${D}${crit ? " (crit)" : ""}`);
      else if (q.size !== want) fail(12, `her blow ${open ? "IN" : "out of"} the window (n ${nPaid}): its float ${q.size}, want ${want}`);
      else inc(nPaid > 0 ? "f12Priced" : open ? "f12X1" : "f12Shut");
    }
    return r;
  };

  /* [12] THE PICTURE'S HOOK: `tickGore`, on the presentation clock, REBUILT from what the simulation did */
  if (S6P) P.tickGore = function(dt){
    if (!FIGHT || FIGHT.m !== this) return oGore.call(this, dt);
    inc("g12Calls");
    const me = FIGHT.me, foe = FIGHT.foe;
    const s0 = simSnap(this, GORE);
    const pre = { fade: me.goreFade, age: me.goreAge, out: me.goreOut, glow: me.goreGlow, seen: me.goreSeen,
                  acc: me.goreAcc, dropN: me.goreDropN, drops: me.goreDrops.map(q => [q.t, q.n]) };
    const open = !!me.ultPrice && !this.over && me.alive && foe.alive;
    const nS = Math.min(4, foe.stacks("hemorrhage"));
    let draws = 0; const oRng = this.rng;
    this.rng = function(){ draws++; return oRng.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "the picture's hook"; vrec = [];
    let r, heard = null;
    try { r = oGore.call(this, dt); } finally { this.rng = oRng; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = diffAt(s0, simSnap(this, GORE));
    if (d) fail(12, `the picture wrote the simulation: ${d}${this.over ? " (after over)" : ""}`);
    else if (draws) fail(12, `the picture drew the RNG ${draws} times`);
    else if (heard.length) fail(12, `the picture played ${JSON.stringify(heard.map(c => c[0]))}`);
    else inc("g12Clean");
    if (foe.goreFade !== 0 || foe.goreAge !== 0 || foe.goreOut !== 0 || foe.goreGlow !== 1 || foe.goreSeen !== 0
        || foe.goreAcc !== 0 || foe.goreDropN !== 0 || foe.goreDrops.length)
      fail(12, `${foe.w.id}, which is not Goreshard, carries the picture`);
    const T = me.priceTally;
    if (!T){
      if (me.goreFade !== 0 || me.goreDrops.length || me.goreDropN !== 0 || me.goreSeen !== 0) fail(12, "the picture up before her first cast");
      else inc("g12Idle");
      return r;
    }
    /* THE REBUILD, in the builder's own arithmetic and order */
    let seen = pre.seen, age = pre.age, out = pre.out, glow = pre.glow, fade = pre.fade, acc = pre.acc, sheds = 0, cast = false;
    if (T.casts !== seen){ seen = T.casts; if (open){ age = 0; out = 0; glow = 1; cast = true; } }
    if (open){
      fade = 1; out = 0; age += dt;
      glow += (PIC.G0 + PIC.G1 * nS - glow) * Math.min(1, dt / PIC.GLOWT);
      acc += dt * PIC.RATE;
      while (acc >= 1){ acc -= 1; sheds++; }
    } else if (fade > 0){ out += dt; fade = Math.max(0, 1 - out / PIC.DRAIN); }
    const want = { goreFade: fade, goreAge: age, goreOut: out, goreGlow: glow, goreSeen: seen, goreAcc: acc, goreDropN: pre.dropN + sheds };
    const off = Object.keys(want).filter(k => me[k] !== want[k]);
    if (off.length) fail(12, `the picture ${open ? "IN an open window" : pre.fade > 0 ? "draining" : "down"}: ${off.map(k => `${k} ${me[k]} (want ${want[k]})`).join(", ")}`);
    else {
      if (cast) inc("g12Cast");
      if (open){ inc("g12Open"); inc("g12GlowN" + nS); }
      else if (pre.fade > 0){
        if (pre.fade === 1) inc(this.over ? (me.ultPrice ? "g12CloseKillOpen" : "g12CloseOver") : "g12CloseClock");
        inc(fade === 0 ? "g12Gone" : "g12Drain");
      } else inc("g12Down");
    }
    /* the motes: the old ones aged, the new ones born at t 0 and aged with them, none past DLIFE, capped */
    let M = pre.drops.map(q => q.slice());
    for (let i = 0; i < sheds; i++){ M.push([0, pre.dropN + i]); if (M.length > PIC.CAP) M.shift(); }
    for (const q of M) q[0] += dt;
    M = M.filter(q => !(q[0] >= PIC.DLIFE));
    const got = me.goreDrops.map(q => [q.t, q.n]);
    if (got.length !== M.length || got.some((q, i) => q[0] !== M[i][0] || q[1] !== M[i][1]))
      fail(12, `the motes: ${got.length} in flight, the shedding clock says ${M.length}${open ? "" : " (the window shut)"}`);
    else if (sheds){
      inc("g12Shed", sheds);
      const Lr = C.physics.ballR + me.w.reach * this.actMods.reach * me.reachMul + 6 + me.w.artW;
      for (const q of me.goreDrops) if (q.n >= pre.dropN){
        if (!(Math.hypot(q.x - me.x, q.y - me.y) <= Lr)) fail(12, `a mote born ${Math.hypot(q.x - me.x, q.y - me.y).toFixed(1)} from her centre, past her reach ${Lr.toFixed(1)}`);
        else inc("g12MoteOnBlade");
      }
    } else if (!open && got.length) inc("g12MotesFalling");
    return r;
  };

  /* THE DRAWN SUBSET [12]: a frame through the renderer, the simulation and the picture's clocks read before and after */
  const drawOn = drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const goreClocks = m => [m.a, m.b].map(q => [q.goreFade, q.goreAge, q.goreOut, q.goreGlow, q.goreSeen, q.goreAcc, q.goreDropN,
                                               q.goreDrops ? q.goreDrops.map(o => o.t).join(":") : "-"].join()).join("|");
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.goreFade > 0 || (q.goreDrops && q.goreDrops.length));
    if (!(vis ? steps % drawEvery === 0 : steps % 120 === 0)) return;
    const s0 = simSnap(m, null), g0 = goreClocks(m), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "a drawn frame"; vrec = [];
    let threw = null, heard = null;
    try { AC.__draw(m); } catch (e){ threw = String((e && e.message) || e); }
    finally { m.rng = oR; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = diffAt(s0, simSnap(m, null));
    if (threw) fail(12, "a drawn frame threw: " + threw);
    else if (dr) fail(12, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(12, "a drawn frame changed the simulation: " + d);
    else if (goreClocks(m) !== g0) fail(12, "a drawn frame changed the picture's clocks");
    else if (heard.length) fail(12, `a drawn frame played ${JSON.stringify(heard.map(c => c[0]))}`);
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "oathwound");
  const T = { casts: 0, frames: 0, foeStk: 0, blows: 0, stk: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "oathwound", sd) : new AC.Match("oathwound", fid, sd);
    const me = side ? m.b : m.a;
    /* [10] her window and tally as watched accessors, for this fight */
    const herStore = { ultPrice: me.ultPrice, priceTally: me.priceTally };
    for (const k of ["ultPrice", "priceTally"])
      Object.defineProperty(me, k, { configurable: true, enumerable: true,
        get(){ if (herWatch) herWatch.push("read " + k); return herStore[k]; },
        set(v){ if (herWatch) herWatch.push("wrote " + k); herStore[k] = v; } });
    herWatch = null;
    per = { in: 0, out: 0, casts: 0, closes: 0 };
    chargeLive = 0; hitLog = null;
    let steps = 0;
    if (S6P) for (const f of [m.a, m.b]){
      if (f.goreFade !== 0 || f.goreAge !== 0 || f.goreOut !== 0 || f.goreGlow !== 1 || f.goreSeen !== 0 || f.goreAcc !== 0
          || f.goreDropN !== 0 || !Array.isArray(f.goreDrops) || f.goreDrops.length) fail(12, `a fresh Match's ${f.w.id} carries a picture`);
      else inc("g12Fresh");
    }
    FIGHT = (S6V || S6P || drawOn) ? { m, me, foe: side ? m.a : m.b } : null;
    const drawn = drawOn && sd === seeds[0];
    if (drawn) inc("drawnFights");
    try {
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.priceTally) for (const k in T) T[k] += me.priceTally[k];
    /* [1] EVERY WINDOW ACCOUNTED FOR */
    const still = me.ultPrice ? 1 : 0;
    if (per.casts !== per.closes + still) fail(1, `${per.casts} casts, ${per.closes} closes, ${still} still open at the end`);
    else inc("acctOk");
    if (still){
      if (m.over && m.reason === "slain") inc("openAtKill");
      else if (m.over) inc("openAtTimeout");
      else inc("openAtCap");
    }
    /* [7] no cast owed at the end */
    if (chargeLive >= nCharge) fail(7, `the fight ended ${chargeLive} live steps after her last cast (a cast is due at ${nCharge})`);
    else inc("owedOk");
    if (rowSnap() !== ROW0) fail(8, "the shared weapon row moved during a fight");
    /* [11]-[12] THE VERDICT: 2 s of the step's `over` path (the presentation clock only), read by them alone */
    if ((S6V || S6P || drawn) && m.over){
      const openAt = !!me.ultPrice, up = me.goreFade > 0, x11 = n.x11 || 0;
      tail = true; vctx = "the verdict"; vrec = [];
      let heardV = null;
      try { for (let i = 0; i < 2 / DT; i++){ m.step(DT); if (drawn) drawFrame(m, steps + i + 1); } }
      finally { tail = false; vctx = "a step"; heardV = vrec; vrec = null; }
      if (S6V){
        if (heardV.some(c => isCastV(c[0], c[1]) || isPriced(c[0], c[1]))) fail(11, "a voice of hers in the verdict");
        else if ((n.x11 || 0) === x11) inc(openAt ? "v11VerdictQuietOpen" : "v11VerdictQuiet");
      }
      if (S6P && me.priceTally){
        if (me.goreFade !== 0 || me.goreDrops.length)
          fail(12, `after 2 s of the verdict the red at ${me.goreFade}, ${me.goreDrops.length} motes${openAt ? " -- the window the sim left set" : ""}`);
        else inc(up ? (openAt ? "g12EndGoneOpen" : "g12EndGoneUp") : "g12EndGoneOk");
      }
    }
    } finally { FIGHT = null; }
  }
  P.step = oStep; P.fireUlt = oFire; P.tickPrice = oTick; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.tickWeapon = oWeap; P.bladeSegments = oSegs; P.tickHits = oHits; P.resolveClank = oClank; P.checkEnd = oEnd;
  if (S6P) P.tickGore = oGore;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  return { n, bad, T, log, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, nClock, nCharge, HB, ONHIT,
           u: { charge: U.charge, dur: U.dur, kind: U.kind, perStack: U.perStack }, blade: ROW.dmg, pin: PIN,
           s6: { v: S6V, p: S6P, part: S6PART } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickPrice === 'function'"):
        raise SystemExit("no tickPrice in this build -- not a Bloodprice link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN, a.drawn])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
g = lambda k: n.get(k, 0)
casts = T["casts"] or 1
frames = max(1, T["frames"])
frozen = g("winFrozen") / max(1, g("winSteps"))
print(f"\nBLOODPRICE PROBE  {pathlib.Path(a.game).name}  stage {a.stage}  Chromium {ver}  {R['fights']} fights "
      f"(Goreshard both sides x every foe x {a.seeds} seeds, seed0 {a.seed0})   ult {U}  blade {R['blade']}")
print(f"  pinned from the builder: window {PIN['dur']}s, charge {PIN['charge']}, perStack {PIN['perStack']}, the greatsword "
      f"reach {PIN['reach']:g} width {PIN['width']:g} spin {PIN['spin']:g} arc {PIN['arc']:g} mass {PIN['mass']:g} "
      f"blades {PIN['blades']} onHit +{PIN['onHit']}, blade {PIN['blade']:g}")
wb = g("blowInOk") + g("blowInShade") + g("blowInFoeRule")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Goreshard win {R['win']:.1%}")
print(f"  per cast: {T['blows']/casts:.2f} priced blows (the tally)   the foe's stacks on a window frame "
      f"{T['foeStk']/frames:.2f}   stacks a window blow found {g('stkAtBlow')/max(1, wb):.2f} "
      f"(mean multiplier x{1 + PIN['perStack'] * g('stkAtBlow')/max(1, wb):.2f})")
print(f"  window: {R['nClock']} steps of the window clock ({R['nClock']/120:.3f}s); match time a window "
      f"{g('clockMatchSteps')/max(1,g('clockOk'))/120:.2f}s (a clock close)   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  the window clock: held on {g('winHeldFrozen')} frozen steps, moved by dt on "
      f"{g('winLiveAdv') + g('winLiveClose')} live steps ({g('winLiveClose')} of them closing)")
print(f"  {T['casts']} windows: {g('clockOk')} closed by the clock, {g('deathClose')} on a death tickPrice saw, "
      f"{g('openAtKill')} still set at `over` (a kill after tickPrice in the last step), "
      f"{g('openAtTimeout')} at the timeout, {g('openAtCap')} at the probe's cap")
print(f"  the charge: {g('cadenceOk')} casts each exactly {R['nCharge']} steps of her live clock after the last "
      f"({R['nCharge']/120:.3f}s); {g('owedOk')} fights ended owing none")
logrows = sorted(((int(k), v) for k, v in R["log"].items()), key=lambda kv: kv[0])
print("  THE LOG (§5's gate): the measured multiplier of every window blow, by the stacks it found:")
for k, (cnt, s, dis) in logrows:
    print(f"      n {k}: {cnt:6d} blows   measured x{s/cnt:.4f}   design x{1 + PIN['perStack']*k:.2f}   "
          f"({dis} would have been priced otherwise on the stacks after the blow's own onHit)")
print(f"  window blows: {g('blowInOk')} on the foe, {g('blowInShade')} on a shade (its own stacks), {g('blowInFoeRule')} with a "
      f"foe rule (curse echo / wall); {g('blowScaledDiff')} of those at n > 0 dealt more than the plain blade")
print(f"  shut-window blows rebuilt plain: {g('blowOutOk')} (+{g('blowOutFoeRule')} with a foe rule)")
print(f"  the blade: swing rebuilt on {g('turnIn')} live steps in windows and {g('turnOut')} outside ({g('turnStunOk')} "
      f"stunned, held); held on {g('turnFrozenOk')} frozen steps; segment {g('segIn')} in / {g('segOut')} out; "
      f"hit test {g('hitTestIn')} in / {g('hitTestOut')} out ({g('hitSkipOk')} skipped with one down)")
print(f"             knock {g('knockIn')}/{g('knockOut')}, hitstun {g('stunIn')}/{g('stunOut')}, stop {g('stopIn')}/{g('stopOut')} "
      f"(in/out; {g('wardShatter')} ward shatters); clanks {g('clankIn')} in / {g('clankOut')} out")
print(f"  then bleeds: onHit +{R['ONHIT']} {g('bleedIn')} in / {g('bleedOut')} out; at the ceiling {R['HB']}: "
      f"{g('ceilBindIn')} in / {g('ceilBindOut')} out")
print(f"  the shared weapon row: unmoved after {g('rowStepIn')} steps in windows and {g('rowStepOut')} outside, "
      f"and at {g('rowBlowIn')} / {g('rowBlowOut')} blows")
print(f"  the price's code: tickPrice clean on {g('tickCleanWin')} window calls and {g('tickCleanIdle')} sampled idle ones; "
      f"the read clean on {g('readClean')} window blows")
print(f"  hers alone: other attackers' blows unpriced, her window and tally untouched -- the foe's {g('othIn')} with her "
      f"window open and {g('othOut')} shut; a shade's {g('othShadeIn')} open and {g('othShadeOut')} shut")
checks = [
    (1, "the window is the build's 8 s on the window tickers' clock: held on every frozen step, dt on every live one; "
        "closes on a death tickPrice sees; every window accounted for; only Goreshard carries ultPrice",
        g("clockOk") > 0 and g("deathClose") > 0 and g("winHeldFrozen") > 0
        and g("winLiveAdv") > 0 and g("winLiveClose") > 0 and g("acctOk") == R["fights"]),
    (2, "every window blow deals round(blade x (1 + 0.3 x n) x ...) exactly, n the struck fighter's Hemorrhage "
        "before its own onHit (the log above)",
        g("blowInOk") > 0 and g("blowScaledDiff") > 0 and len(logrows) >= 3 and logrows[0][0] == 0),
    (3, "then bleeds: onHit +2 after the price, stopped at hemorrhage's own 4; the ceiling 4 at every blow; n <= 4",
        g("bleedIn") > 0 and g("bleedOut") > 0 and g("ceilBindIn") > 0 and g("ceilBindOut") > 0),
    (4, "the window only: every shut-window blow is the plain blade, and reads no stacks for a price",
        g("blowOutOk") > 0),
    (5, "the blade is otherwise the shipped greatsword, in the window and out: the row, the swing, the segment, "
        "the hit test and cooldown, each blow's knock, hitstun and stop off its damage, the clank",
        all(g(k) > 0 for k in ("turnIn", "turnOut", "turnFrozenOk", "segIn", "segOut", "hitTestIn", "hitTestOut",
                               "knockIn", "knockOut", "stunIn", "stunOut", "stopIn", "stopOut", "clankIn", "clankOut"))),
    (6, "the cast resolves nothing: no damage, no status (the beam's 16 and 3 Hemorrhage gone), no knock, no RNG, "
        "no new object; the common 0.08 stop and ult beat only; a window {t 0, dur}",
        g("castClean") > 0),
    (7, "the build's charge 14 on her live clock: every cast exactly then, none owed at the end, none while her "
        "window is open",
        g("castOk") > 0 and g("cadenceOk") > 0 and g("owedOk") == R["fights"]),
    (8, "the shared weapon row is never written: unmoved after every step and at every blow",
        g("rowStepIn") > 0 and g("rowStepOut") > 0 and g("rowBlowIn") > 0 and g("rowBlowOut") > 0),
    (9, "the price's own code writes nothing but its window and tally: tickPrice (every window call) and the read "
        "inside resolveHit (every window blow)",
        g("tickCleanWin") > 0 and g("tickCleanIdle") > 0 and g("readClean") > 0),
    (10, "the price is hers alone: no other attacker's blow (the foe's or a shade's, her window open or shut) reads "
         "or writes her window or tally, or reads the struck fighter's Hemorrhage for a price",
         g("othIn") > 0 and g("othOut") > 0),
]
S6 = R["s6"]
if S6["v"] or S6["p"] or a.stage == "6":
    pc = PIN["pic"]
    priced = {k: g(f"v11Priced{k}") for k in range(1, 5)}
    nlog = {int(k): v[0] for k, v in R["log"].items()}
    print(f"  STAGE 6 on this link: voices {S6['v']}, picture {S6['p']}   picture pins: glow {pc['G0']:g} + {pc['G1']:g} x n "
          f"(v81: 0.2 -> 0.8), ease {pc['GLOWT']:g}, drain {pc['DRAIN']:g}, motes {pc['RATE']:g} a clock unit living "
          f"{pc['DLIFE']:g} (cap {pc['CAP']:g}), float x(1 + {pc['FK']:g} n)   (clock units: half-seconds)")
    print(f"  [11] casts voiced {g('v11CastOk')} of {T['casts']}; priced blows voiced by n {priced} (the log's n > 0: "
          f"{ {k: v for k, v in nlog.items() if k > 0} }); plain: {g('v11PlainX1')} x1 window blows, {g('v11PlainShut')} "
          f"shut-window; {g('v11Shatter')} ward shatters' own voices unpriced; the foe's blows unpriced {g('v11OthIn')} open / "
          f"{g('v11OthOut')} shut; closes silent: {g('v11CloseClockQuiet')} by the clock, {g('v11CloseDeathQuiet')} ON A DEATH; "
          f"verdicts quiet {g('v11VerdictQuiet')} (+{g('v11VerdictQuietOpen')} with the window left set)")
    print(f"  [12] tickGore clean on {g('g12Clean')} of {g('g12Calls')} calls ({g('g12Idle')} before a first cast); rebuilt: "
          f"{g('g12Cast')} casts found, {g('g12Open')} open calls (glow at n 0/2/4: {g('g12GlowN0')}/{g('g12GlowN2')}/"
          f"{g('g12GlowN4')}), closes {g('g12CloseClock')} with the match on (the clock, or a death before `over`) / "
          f"{g('g12CloseKillOpen')} at a kill with the window set / {g('g12CloseOver')} at `over` after a death close, "
          f"{g('g12Drain')} draining calls, {g('g12Gone')} "
          f"gone; motes {g('g12Shed')} shed ({g('g12MoteOnBlade')} born on her blade), {g('g12MotesFalling')} calls with "
          f"motes falling after a close; after the verdict {g('g12EndGoneOk') + g('g12EndGoneUp') + g('g12EndGoneOpen')} "
          f"clean ({g('g12EndGoneOpen')} with the window left set); fresh fighters {g('g12Fresh')}")
    print(f"       floats: {g('f12Priced')} priced x(1 + {pc['FK']:g} n), {g('f12X1')} x1 window and {g('f12Shut')} "
          f"shut-window blows of hers the old size, {g('f12Oth')} of other attackers' the old size")
    if a.drawn:
        print(f"  drawn subset: {g('drawnFights')} fights drawn every {a.drawn}th step while the picture shows (every 120th "
              f"otherwise): {g('drawOk')} frames clean ({g('drawPic')} with the picture up, {g('drawPicStop')} in a hit stop, "
              f"{g('drawVerdict')} in the verdict)")
    both = S6["v"] and S6["p"] and not S6["part"]
    checks.append((11, "the voices fire exactly on their events: one cast voice a cast, in fireUlt; a blow priced on "
                       "n > 0 voiced with price n (its dmg and crit), every other blow plain; the close silent, by the "
                       "clock and ON A DEATH; none in the picture, a drawn frame or the verdict",
                   both and g("v11CastOk") == T["casts"] and priced[2] > 0 and priced[4] > 0
                   and sum(priced.values()) == sum(v for k, v in nlog.items() if k > 0)
                   and g("v11PlainX1") > 0 and g("v11PlainShut") > 0 and g("v11OthIn") > 0 and g("v11OthOut") > 0
                   and g("v11CloseClockQuiet") > 0 and g("v11CloseDeathQuiet") > 0
                   and g("v11VerdictQuiet") + g("v11VerdictQuietOpen") > 0))
    checks.append((12, "the picture's hook writes nothing of the simulation's and is the picture declared: the red "
                       "exactly while the window is open, its run and drain, the glow toward 0.2 + 0.15 n, the motes "
                       "while open only; the float x(1 + 0.1 n) on a priced blow and the old size on every other"
                       + ("; the drawn subset clean" if a.drawn else ""),
                   both and g("g12Clean") == g("g12Calls") and g("g12Cast") > 0 and g("g12Open") > 0
                   and all(g(f"g12GlowN{k}") > 0 for k in (0, 2, 4)) and g("g12CloseClock") > 0
                   and g("g12CloseKillOpen") > 0 and g("g12Drain") > 0 and g("g12Gone") > 0 and g("g12Shed") > 0
                   and g("g12MoteOnBlade") > 0 and g("g12EndGoneOk") + g("g12EndGoneUp") + g("g12EndGoneOpen") > 0
                   and g("f12Priced") > 0 and g("f12X1") > 0 and g("f12Shut") > 0 and g("f12Oth") > 0
                   and g("g12Fresh") == 2 * R["fights"] and (g("drawOk") > 0 if a.drawn else True)))
elif a.drawn:
    print(f"  stage 6: not on this link -- [11] not run; the drawn subset alone: {g('drawnFights')} fights, {g('drawOk')} "
          f"frames clean")
    checks.append((12, "the drawn subset only (no picture on this link): no drawn frame throws, draws the RNG or changes "
                       "the simulation", g("drawOk") > 0))
else:
    print("  stage 6: not on this link (no cast arm or priced branch in the synth, no tickGore) -- [11]-[12] not run")
ok = 0
for k, text, cover in checks:
    fails = g(f"x{k}")
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
