#!/usr/bin/env python3
"""LOOK AT THE BLOODSWORN FLAIL BEFORE DESIGNING IT.

    python3 flail_probe.py --game ../02-chain/sc-twinshade-scrunch.html

The bloodsworn x flail cell has FINISHED ART and no relic wearing it.
`SHAPES.flailHead` dispatches on `p.key` and the bloodsworn branch --
`_fhBarbed`, seven hooked barbs curving off the ball with core-coloured tips --
has been sitting in the build unreachable. Same situation `purpledagger_probe`
and `whitescythe_probe` were written for, and this file is their sibling.

Before anyone argues about a name or an ultimate, this renders the cell as it
would actually appear and MEASURES THE ONE THING THAT COULD KILL IT.

  [1] DISPATCH, AND THE CHAIN. Two separate claims and they fail differently.

      (a) The injected relic must render through `_fhBarbed` and not through
          the `_fhBase` fallback. `_fhBarbed` CALLS `_fhBall`, and so does
          `_fhBase`, so "the ball drew" is not evidence -- the check is that
          `_fhBarbed` is in the fired list. Negative control with a nonsense
          affinity key must fire `_fhBase` and NOT `_fhBarbed`, or the check
          cannot fail and is worthless.

      (b) `_initChain` reads `f.w.mode` at MATCH CONSTRUCTION. Injection
          rewrites the weapon before the Match exists, so this should hold --
          but "should" is how the Harrowing shipped as twelve small arrows.
          Asserted directly: headAng finite, headR == reach*(1-hilt), and the
          head measurably LAGS the arm over 120 steps. Negative control: a
          spin-mode relic has no headAng at all.

  [2] DOES IT FIGHT -- six opponents, pinned seeds. A cell that draws but
      never lands anything is caught here rather than after a tuner run.

  [3] HEMORRHAGE x CHAIN -- THE HAZARD, AND IT IS THE OPPOSITE OF THE ONE
      THIS CELL LOOKS LIKE IT HAS.

      The obvious worry about a bloodsworn heavy is that it stacks too hard.
      The measurement says look the other way. Hemorrhage is the only bloodsworn
      channel and it DECAYS: maxStacks 4, dur 3.2s. It has to be REFRESHED to
      mean anything. And v36's `contact_rate_probe`, damage pinned across all
      eighteen relics so lethality could not buy a rate:

          bow 0.360 hits/s . greatsword 0.283 . twinblade 0.271 .
          scythe 0.228 . FLAIL 0.205 . warhammer 0.183

      0.205 hits/s is one contact every 4.9 seconds against a 3.2s window.
      **A stack may be reliably gone before the next one lands.** If that is
      true, bloodsworn's entire school contribution evaporates on this type,
      and an ultimate that SPENDS hemorrhage -- the design argument for
      building this cell at all -- has nothing to spend.

      So: time-weighted stack occupancy, measured within the school and across
      the type axis (this cell vs Widowmaker vs Goreshard), with Gravemourn's
      curse on the identical chain as the control that separates "the chain"
      from "the status". Damage pinned across every relic in the comparison,
      because a harder-hitting relic ends the fight sooner and therefore has
      fewer seconds in which to stack.

  [4] LEGIBILITY -- stills against BOTH other chains. v28 found same-affinity
      pairs read as one smudge; the risk here is different and needs its own
      look, because three flails share one silhouette and the matrix doc's
      claim that "a spiked ball is genuinely school-neutral, so the palette
      swap carries it" is a claim about a contact sheet, not about motion.

Injection is runtime-only and the page is thrown away. NOTHING is written to
any build. This is a LOOK, not a build.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import pathlib
import statistics
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v38"
W, H = 1080, 1920

# The provisional cell. Every physics number is the FLAIL profile exactly,
# copied from Gravemourn and Slagheart which share it byte for byte
# (weapon-matrix decision 1: type owns the physics, school owns status and
# palette). A new flail that changes reach/spin/mass/mode is not a new school
# cell, it is a new type wearing a flail's name.
#
# `dmg` is a PLACEHOLDER and nothing here should be read as a balance claim:
# it is the mean of the two shipped flails (44.1, 42.5). Every [3] number is
# taken with damage PINNED anyway, so the placeholder cannot reach them.
#
# `onHit` is an OPEN QUESTION this probe exists to inform, not settle. Both
# shipped bloodsworn relics apply 2 a hit; both shipped flails apply to the
# lower end of their school. Set with --stacks and read [3].
#
# The ult is a STAND-IN so the card has something to lay out. It is NOT a
# design -- the design has to come from Rick, that is the rule this project
# has paid for twice -- and ult set-piece art dispatches on relic ID, so
# anything it draws on screen is the DONOR's set-piece and is a lie.
DONOR = "axiom"
PROVISIONAL = {
    "id": DONOR, "name": "Provisional", "aff": "bloodsworn",
    "shape": "flail",
    "blades": [0], "reach": 96, "width": 22, "artW": 52,
    "dmg": 43.3, "spin": 2.2, "mode": "chain", "mass": 3.6,
    "onHit": {"hemorrhage": 2},
    "ult": {"name": "Placeholder", "charge": 16, "kind": "nova", "radius": 240,
            "dmg": 12, "apply": {"hemorrhage": 3}, "knock": 200,
            "tip": "PLACEHOLDER -- nova: 12 damage, 3 Hemorrhage, knockback"},
    "blurb": "Provisional. Injected at runtime for a look; nothing is built.",
}

# Six foes, one per OTHER school, none of them bloodsworn -- the [3]
# comparison relics must not appear in the field they are measured against.
# Excludes the donor id by construction.
FOES = ["thornwake", "censer", "ironhail", "heartwood", "lightkeeper", "spellbreaker"]
SEEDS = [101, 211, 337, 449, 563, 677, 787, 881]
PIN = 14.0          # the same pin v36's contact_rate_probe used

INJECT_JS = """(relic) => {
  const w = AC.WEAPONS.find(x => x.id === relic.id);
  if (!w) return "donor missing: " + relic.id;
  for (const k of Object.keys(w)) delete w[k];
  Object.assign(w, relic);
  return "overwrote donor " + relic.id + " in place";
}"""

# [1a] Which draw branch actually ran. `flailHead` is the only shape with no
# `aff` argument -- it is called `(c, D, p, spin)` -- so the grammar dispatches
# on `p.key` alone and the only honest way to ask is to wrap every candidate
# branch and see which fires.
BRANCH_JS = """(palKey) => {
  const names = ["_fhBarbed", "_fhBase", "_fhBall", "_fhConjured", "_fhGrown",
                 "_fhEaten", "_fhRadiant", "_fhBuilt", "_fhPlated"];
  const fired = [], orig = {};
  for (const n of names){
    if (typeof AC.SHAPES[n] !== "function") continue;
    orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this, a); };
  }
  const cv = document.createElement("canvas");
  cv.width = 400; cv.height = 400;
  const c = cv.getContext("2d");
  c.translate(200, 200);
  const pal = palKey === null
    ? { key:"NOT_A_SCHOOL", core:"#888", glow:"#aaa", dark:"#222", steel:"#ccc" }
    : AC.AFFINITIES[palKey];
  AC.SHAPES.flailHead(c, 52, pal, 0.7);
  for (const n of Object.keys(orig)) AC.SHAPES[n] = orig[n];
  return fired;
}"""

# [1b] Did `_initChain` run, and does the head actually lag the arm? A rigid
# arm and a chain are the same object until they move, so the claim is tested
# by MOTION, not by the presence of a field.
CHAIN_JS = """([id, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const wrap = a => Math.atan2(Math.sin(a), Math.cos(a));
  const init = {
    headAng: me.headAng, headR: me.headR,
    wantR: me.w.reach * (1 - AC.CONFIG.chain.hilt),
    foeHasHeadAng: th.headAng !== undefined, foeMode: th.w.mode,
  };
  let maxLag = 0, sumLag = 0, n = 0, finite = true;
  const N = Math.round(secs / DT);
  for (let i = 0; i < N; i++){
    m.step(DT);
    if (!Number.isFinite(me.headAng)) { finite = false; break; }
    const lag = Math.abs(wrap(me.headAng - me.theta));
    maxLag = Math.max(maxLag, lag); sumLag += lag; n++;
  }
  return { ...init, finite, maxLag, meanLag: n ? sumLag / n : null, steps: n };
}"""

FIGHT_JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      let steps = 0;
      while (!m.over && steps < 120 / DT){ m.step(DT); steps++; }
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      out.push({ foe: f, seed: s, dur: +(steps * DT).toFixed(2), over: !!m.over,
                 hits: me.hits, dealt: Math.round(th.maxHp - th.hp),
                 won: !!(m.winner && m.winner.w.id === id) });
    }
  }
  return out;
}"""

# [3] THE HAZARD. Sampled every step. `pin` sets every listed relic's dmg to
# the same number so contact rate is isolated from lethality -- restored after.
#
# An application is detected by the status TIMER going UP: `apply()` sets
# `cur.t = def.dur` and nothing else ever increases it, so a step where t rose
# is a hit that applied. This is why the timer is read and not just the stack
# count -- an application at max stacks does not move the count at all, and
# counting only the count would undercount exactly the refreshes this block
# exists to measure.
BLEED_JS = """([id, key, foes, seeds, pin, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const saved = {}, savedUlt = {};
  for (const pid of pinIds){
    const w = AC.WEAPONS.find(x => x.id === pid);
    if (!w) continue;
    saved[pid] = w.dmg; w.dmg = pin;
    if (noult){ savedUlt[pid] = w.ult.charge; w.ult.charge = 1e9; }
  }
  /* Casts are COUNTED, not inferred. `fireUlt` is the single firing site
     (`if (f.charge >= f.w.ult.charge)`), so wrapping it is exact -- reading
     a charge reset would also catch anything else that zeroes the bar. */
  const origFire = AC.Match.prototype.fireUlt;
  let castsA = 0, castsB = 0, cur = null;
  AC.Match.prototype.fireUlt = function(f, foe){
    if (cur){ if (f === cur.me) castsA++; else castsB++; }
    return origFire.call(this, f, foe);
  };
  const rows = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      cur = { me }; castsA = 0; castsB = 0;
      let steps = 0, sum = 0, at = [0,0,0,0,0,0,0,0,0];
      let apps = 0, refresh = 0, prevT = 0, tFirst = null;
      while (!m.over && steps < 120 / DT){
        m.step(DT); steps++;
        const st = th.status[key];
        const t = st ? st.t : 0;
        const n = st ? st.stacks : 0;
        if (t > prevT + 1e-9){                 // the timer went up: an apply
          apps++;
          if (prevT > 0) refresh++;            // ...onto a foe already bleeding
          if (tFirst === null) tFirst = steps * DT;
        }
        prevT = t;
        sum += n;
        at[Math.min(8, n)]++;
      }
      rows.push({ foe: f, seed: s, steps, dur: steps * DT, hits: me.hits,
                  meanStacks: steps ? sum / steps : 0,
                  at, apps, refresh, tFirst, casts: castsA, foeCasts: castsB,
                  won: !!(m.winner && m.winner.w.id === id) });
    }
  }
  cur = null;
  AC.Match.prototype.fireUlt = origFire;
  for (const pid of Object.keys(saved)){
    const w = AC.WEAPONS.find(x => x.id === pid);
    w.dmg = saved[pid];
    if (noult) w.ult.charge = savedUlt[pid];
  }
  return rows;
}"""

ARENA_JS = """([a, b, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  for (let i = 0; i < Math.round(secs / DT); i++) m.step(DT);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

# [4] The three heads, drawn through the real SHAPES functions at the size the
# sim draws them, then blown up. NOT a screenshot of a fight -- this isolates
# the shape from lighting, motion blur and everything else the arena adds.
HEADS_JS = """([keys, D, zoom]) => {
  const out = [];
  for (const k of keys){
    const cv = document.createElement("canvas");
    const S = Math.round(D * 2.6);
    cv.width = S * zoom; cv.height = S * zoom;
    const c = cv.getContext("2d");
    c.scale(zoom, zoom);
    c.fillStyle = "#0B0912"; c.fillRect(0, 0, S, S);
    c.translate(S/2, S/2);
    AC.SHAPES.flailHead(c, D, AC.AFFINITIES[k], 0.7);
    out.push(cv.toDataURL("image/png"));
  }
  return out;
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def sheet(imgs, labels, out, scale, title, bg=(12, 10, 18)):
    cols = len(imgs)
    tw, th = int(imgs[0].width * scale), int(imgs[0].height * scale)
    PAD, LBL = 16, 34
    sh = Image.new("RGB", (cols * (tw + PAD) + PAD, th + PAD * 2 + LBL), bg)
    dr = ImageDraw.Draw(sh)
    dr.text((PAD, 8), title, fill=(201, 162, 39))
    for i, (im, lab) in enumerate(zip(imgs, labels)):
        x = PAD + i * (tw + PAD)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, PAD + LBL))
        dr.text((x + 2, PAD + LBL - 15), lab, fill=(214, 200, 170))
    sh.save(out)
    print(f"  {out.name}  ({sh.width}x{sh.height})")


def fmt(x, n=2):
    return "  --  " if x is None else f"{x:.{n}f}"


PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--stacks", type=int, default=2)
    ap.add_argument("--seeds", type=int, default=8)
    args = ap.parse_args()

    gp = pathlib.Path(args.game).resolve()
    seeds = SEEDS[: args.seeds]
    relic = json.loads(json.dumps(PROVISIONAL))
    relic["onHit"] = {"hemorrhage": args.stacks}
    OUT.mkdir(parents=True, exist_ok=True)

    print(f"\nFLAIL PROBE -- the bloodsworn x flail cell")
    print(f"  game    {gp.name}")
    print(f"  relic   flail profile, hemorrhage:{args.stacks}, dmg {relic['dmg']} (PLACEHOLDER)")
    print(f"  donor   {DONOR}   foes {len(FOES)}   seeds {len(seeds)}\n")

    with game(game_path=gp) as (page, errors):

        # ---------------------------------------------------------- [1a] --
        print("[1a] DISPATCH")
        neg = page.evaluate(BRANCH_JS, None)
        print(f"     negative control (nonsense key) fired: {neg}")
        check("control does NOT reach _fhBarbed", "_fhBarbed" not in neg, str(neg))
        check("control falls back to _fhBase", "_fhBase" in neg)

        said = page.evaluate(INJECT_JS, relic)
        print(f"     inject: {said}")
        assert "overwrote" in said, said

        fired = page.evaluate(BRANCH_JS, "bloodsworn")
        print(f"     bloodsworn fired: {fired}")
        check("bloodsworn reaches _fhBarbed", "_fhBarbed" in fired)
        check("bloodsworn does NOT fall back to _fhBase", "_fhBase" not in fired)

        # ---------------------------------------------------------- [1b] --
        print("\n[1b] THE CHAIN IS REAL")
        ch = page.evaluate(CHAIN_JS, [DONOR, "thornwake", 101, 2.0])
        want = relic["reach"] * (1 - 0.46)
        print(f"     headAng {fmt(ch['headAng'], 4)}   headR {fmt(ch['headR'])} "
              f"(want {want:.2f})   finite {ch['finite']}")
        print(f"     lag over {ch['steps']} steps (2.0s): max {fmt(ch['maxLag'], 3)} rad  "
              f"mean {fmt(ch['meanLag'], 3)} rad")
        check("_initChain ran (headAng finite)", ch["headAng"] is not None and ch["finite"])
        check("headR == reach*(1-hilt)", abs((ch["headR"] or 0) - want) < 1e-6,
              f"{fmt(ch['headR'])} vs {want:.2f}")
        check("the head LAGS the arm", (ch["maxLag"] or 0) > 0.15,
              f"max lag {fmt(ch['maxLag'], 3)} rad")
        check("control: spin-mode foe has no headAng", not ch["foeHasHeadAng"],
              f"foe mode {ch['foeMode']}")

        # ----------------------------------------------------------- [2] --
        print("\n[2] DOES IT FIGHT")
        rows = page.evaluate(FIGHT_JS, [DONOR, FOES, seeds])
        print(f"     {'foe':<14}{'dur':>7}{'hits':>7}{'dealt':>8}{'win%':>7}")
        thin = []
        for f in FOES:
            rs = [r for r in rows if r["foe"] == f]
            hits = statistics.mean(r["hits"] for r in rs)
            print(f"     {f:<14}{statistics.mean(r['dur'] for r in rs):>7.1f}"
                  f"{hits:>7.1f}{statistics.mean(r['dealt'] for r in rs):>8.0f}"
                  f"{100*sum(r['won'] for r in rs)/len(rs):>6.0f}%")
            if hits < 1: thin.append(f)
        check("lands at least one hit in every pairing", not thin, str(thin))
        check("no pairing times out", all(r["over"] for r in rows))

        # ----------------------------------------------------------- [3] --
        print("\n[3] HEMORRHAGE x CHAIN -- THE HAZARD")
        print(f"     damage pinned at {PIN} across every relic below AND every foe,")
        print(f"     so contact rate is isolated from lethality.")
        print(f"     RUN TWICE. The first pass is the relics as they exist. The second")
        print(f"     suppresses every ultimate (charge 1e9), because the five relics")
        print(f"     compared here have five DIFFERENT ultimates and three of them move")
        print(f"     bodies around -- Dirge pulls, Ironbloom latches, the stand-in novas.")
        print(f"     On an identical physics profile the first pass returned hits/s of")
        print(f"     0.131 / 0.141 / 0.196 across three flails, which is a 50% spread on")
        print(f"     a number that should not vary at all. Either the ult explains it or")
        print(f"     something else does, and the whole block is unreadable until we know.\n")
        COMPARE = [
            (DONOR,        "hemorrhage", "THIS CELL   bloodsworn flail"),
            ("widowmaker", "hemorrhage", "            bloodsworn twinblade"),
            ("oathwound",  "hemorrhage", "            bloodsworn greatsword"),
            ("gravemourn", "curse",      "CONTROL     umbral flail (curse)"),
            ("slagheart",  "sunder",     "CONTROL     dwarven flail (sunder)"),
        ]
        pin_ids = [c[0] for c in COMPARE] + FOES
        bleed = {}
        for noult in (False, True):
            tag = "ULTS SUPPRESSED" if noult else "AS THEY SHIP"
            print(f"     -- {tag} " + "-" * (52 - len(tag)))
            print(f"     {'':<38}{'dur':>7}{'cast':>6}{'hits/s':>8}{'mean':>7}"
                  f"{'>=2':>7}{'>=4':>7}{'max':>5}{'appl':>7}{'refr%':>7}")
            store = {}
            for rid, key, label in COMPARE:
                rs = page.evaluate(BLEED_JS, [rid, key, FOES, seeds, PIN, pin_ids, noult])
                steps = sum(r["steps"] for r in rs)
                occ = [sum(r["at"][i] for r in rs) / steps for i in range(9)]
                ge = lambda k: sum(occ[i] for i in range(k, 9))
                dur = sum(r["dur"] for r in rs) / len(rs)
                hps = sum(r["hits"] for r in rs) / sum(r["dur"] for r in rs)
                mean = sum(r["meanStacks"] * r["steps"] for r in rs) / steps
                apps = sum(r["apps"] for r in rs) / len(rs)
                refr = sum(r["refresh"] for r in rs) / max(1, sum(r["apps"] for r in rs))
                casts = sum(r["casts"] for r in rs) / len(rs)
                mx = max(i for i in range(9) if occ[i] > 0)
                store[rid] = dict(hps=hps, mean=mean, ge2=ge(2), ge4=ge(4), mx=mx,
                                  apps=apps, refr=refr, dur=dur, casts=casts)
                print(f"     {label:<38}{dur:>7.1f}{casts:>6.1f}{hps:>8.3f}{mean:>7.2f}"
                      f"{100*ge(2):>6.0f}%{100*ge(4):>6.0f}%{mx:>5}{apps:>7.1f}"
                      f"{100*refr:>6.0f}%")
            bleed[noult] = store
            print()

        # The three flails share reach/spin/mass/mode byte for byte. With damage
        # pinned and ultimates suppressed their contact rates are the SAME
        # MEASUREMENT taken three times, so any spread left is the instrument
        # or an unmodelled channel -- not the relic.
        fl = [DONOR, "gravemourn", "slagheart"]
        for noult in (False, True):
            hp = [bleed[noult][r]["hps"] for r in fl]
            spread = (max(hp) - min(hp)) / statistics.mean(hp)
            print(f"     three-flail hits/s spread, {'ults off' if noult else 'ults on '}: "
                  f"{spread*100:5.1f}%   " + " ".join(f"{h:.3f}" for h in hp))
        off = bleed[True]
        hp = [off[r]["hps"] for r in fl]
        check("identical flails agree on contact rate with ults off (<12%)",
              (max(hp) - min(hp)) / statistics.mean(hp) < 0.12,
              " ".join(f"{h:.3f}" for h in hp))

        me, tw, gs = off[DONOR], off["widowmaker"], off["oathwound"]
        gm, sh = off["gravemourn"], off["slagheart"]
        print(f"\n     THE QUESTION: does bloodsworn's only channel survive the chain?")
        print(f"       (ults off, so this is the BASE WEAPON and nothing else)")
        print(f"       holds >=2 stacks {100*me['ge2']:.0f}% of the fight, against "
              f"{100*tw['ge2']:.0f}% (twinblade) and {100*gs['ge2']:.0f}% (greatsword)")
        print(f"       mean stacks {me['mean']:.2f} vs {tw['mean']:.2f} / {gs['mean']:.2f}"
              f"  -- {100*me['mean']/max(1e-9, tw['mean']):.0f}% of the twinblade's")
        print(f"       {100*me['refr']:.0f}% of applications land on a foe already bleeding,"
              f" against {100*tw['refr']:.0f}% / {100*gs['refr']:.0f}%")
        print(f"\n     AND THE CONTROL THAT SAYS WHETHER IT IS THE CHAIN OR THE CLOCK:")
        print(f"       same chain, same contact rate, three different status durations")
        print(f"       hemorrhage dur 3.2  ->  mean {me['mean']:.2f}, >=2 for {100*me['ge2']:.0f}%")
        print(f"       sunder     dur 5.0  ->  mean {sh['mean']:.2f}, >=2 for {100*sh['ge2']:.0f}%")
        print(f"       curse      dur 99   ->  mean {gm['mean']:.2f}, >=2 for {100*gm['ge2']:.0f}%")
        # REPORTED, NOT ASSERTED. There is no correct value here -- this block
        # exists to inform a design decision, and asserting a threshold would
        # be inventing one. The only assertion is that the mechanic is not
        # DEAD, which is a claim about zero and needs no taste.
        check("hemorrhage is not dead on this type (mean stacks > 0)", me["mean"] > 0,
              f"mean {me['mean']:.3f}")
        check("the status does land at all (>=1 application a fight)", me["apps"] >= 1,
              f"{me['apps']:.1f} applications a fight")

        # ----------------------------------------------------------- [4] --
        print("\n[4] LEGIBILITY")
        keys = ["bloodsworn", "umbral", "dwarven"]
        heads = [png(d) for d in page.evaluate(HEADS_JS, [keys, 52, 6])]
        sheet(heads, ["bloodsworn  _fhBarbed  THIS CELL",
                      "umbral  _fhEaten  Gravemourn",
                      "dwarven  _fhBuilt  Slagheart"],
              OUT / "flail-heads-6x.png", 1.0,
              "THE THREE FLAIL HEADS, drawn through SHAPES.flailHead at D=52, 6x")

        shots, labs = [], []
        for foe, lab in [("gravemourn", "vs Gravemourn  umbral flail"),
                         ("slagheart", "vs Slagheart  dwarven flail"),
                         ("thornwake", "vs Thornwake  verdant scythe")]:
            shots.append(png(page.evaluate(ARENA_JS, [DONOR, foe, 337, 4.33])))
            labs.append(lab)
        sheet(shots, labs, OUT / "flail-arena-1to1.png", 0.30,
              "THE CELL IN THE HALL at t=4.3s -- chain against chain")

        check("no page errors", not errors, "; ".join(errors[:3]))

    ok = sum(1 for _, v in PASS if v)
    print(f"\n  {ok}/{len(PASS)} checks pass")
    print(f"  sheets in {OUT}\n")
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
