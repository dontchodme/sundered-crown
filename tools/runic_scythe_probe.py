#!/usr/bin/env python3
"""LOOK AT THE RUNIC SCYTHE BEFORE DESIGNING IT.

    python3 runic_scythe_probe.py --game ../02-chain/sc-redflail.html

`cell_survey.py` chose the cell. This is the deep look at it, in the shape
`flail_probe` established for v38, and it exists to find the thing that would
otherwise be found after a tuner run.

  [1] DISPATCH. The injected relic must render through `_scConjured` and not
      through `_scBase`. Negative control with a nonsense affinity key must
      fire `_scBase` and NOT `_scConjured`, or the check cannot fail and is
      worthless.

  [2] DOES IT FIGHT -- six opponents, pinned seeds.

  [3] THE HAZARD, AND IT IS NOT THE ONE THE OCCUPANCY TABLE MEASURED.

      Every other school's status is a QUANTITY: smite and hemorrhage deal
      damage per stack per second, sunder multiplies what is taken, curse
      removes max hp, entangle slows. For those, time-weighted stack
      occupancy IS the delivered effect.

      Hex is not a quantity, it is a RATE. From `tickStatus`:

          f.hexClock += dt * hx;
          if (f.hexClock >= STATUS.hex.stunEvery){ f.hexClock = 0;
            f.stun = Math.max(f.stun, STATUS.hex.stunFor); ... }

      The clock accrues at dt x STACKS, so five stacks do not lock harder,
      they lock FIVE TIMES AS OFTEN -- and `Math.max` means two locks that
      overlap are one lock. So occupancy is a proxy twice removed from the
      thing, and `cell_survey`'s 18%-at-two-stacks is not yet an answer.

      What is measured here is the LOCK ITSELF:

        (a) hex fires a second, observed at `f.hexClock` RESETTING. That is
            the engine's own state, not a reimplementation of its one line.
        (b) the share of the fight the foe's weapon is shut, from all
            sources -- and the same matchup run with the relic's onHit
            REMOVED, so hitstun's share can be differenced out. A lock the
            foe was going to be in anyway is not this school's contribution.

      Both, across the school axis (hex on all six types) and against the
      other two scythes, damage pinned and ultimates suppressed throughout.

  [4] WHAT THE CLOCK WOULD HAVE TO BE. `dur` swept on this type alone, so the
      cost of the cell's central constraint is a number rather than an
      adjective. Read only, never written back.

  [5] LEGIBILITY -- stills against BOTH other scythes and BOTH other runics.
      v28 found same-affinity pairs read as one smudge and v37 found a school
      colour doing no work; this cell can fail either way, so it gets both
      looks.

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
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent

# The cell, as a placeholder. A NOVA and a name that is deliberately not a
# name, for the reason v38's probe gives: nothing in this file may read as a
# proposal, because §1 does not exist yet.
DONOR = "censer"      # exists, and nothing in this probe compares against it
CELL = {
    "id": DONOR, "name": "PLACEHOLDER", "aff": "runic", "shape": "scythe",
    "blades": [0], "reach": 104, "width": 11, "artW": 46, "dmg": 14.0,
    "spin": 3.2, "mode": "spin", "mass": 2.4,
    "onHit": {"hex": 1},
    "ult": {"name": "PLACEHOLDER", "charge": 15, "kind": "nova", "radius": 240,
            "dmg": 14, "knock": 200, "tip": "PLACEHOLDER — no design exists yet"},
    "blurb": "PLACEHOLDER — no design exists yet.",
}
FOES = ["dawnbringer", "grudgebearer", "thornwake", "gravemourn",
        "ironhail", "nightfell"]

INJECT_JS = """(relic) => {
  const w = AC.WEAPONS.find(x => x.id === relic.id);
  if (!w) return "donor missing: " + relic.id;
  const keep = relic.id;
  for (const k of Object.keys(w)) delete w[k];
  Object.assign(w, relic, { id: keep });
  return "overwrote donor " + keep + " in place";
}"""

# [1] `scythe` takes (c, L, W, p, k, aff) and dispatches on `p.key` -- `aff`
# is an override the renderer never passes. Every candidate branch is wrapped
# and whichever names appear in `fired` are the ones that actually drew.
BRANCH_JS = """([palKey]) => {
  const names = Object.keys(AC.SHAPES)
    .filter(n => typeof AC.SHAPES[n] === "function" && n.startsWith("_sc"));
  const fired = [], orig = {};
  for (const n of names){
    orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this, a); };
  }
  const cv = document.createElement("canvas");
  cv.width = 500; cv.height = 500;
  const c = cv.getContext("2d");
  c.translate(120, 250);
  const pal = palKey === null
    ? { key:"NOT_A_SCHOOL", core:"#888888", glow:"#aaaaaa", dark:"#222222",
        steel:"#cccccc", ink:"#111111", trail:"#999999" }
    : AC.AFFINITIES[palKey];
  AC.SHAPES.scythe(c, 104, 46, pal, 0.55);
  for (const n of Object.keys(orig)) AC.SHAPES[n] = orig[n];
  return { fired, candidates: names };
}"""

FIGHT_JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      let steps = 0;
      while (!m.over && steps < 120 / DT){ m.step(DT); steps++; }
      out.push({ foe: f, seed: s, dur: steps * DT, over: m.over,
                 hits: me.hits, dealt: me.dealt,
                 won: !!(m.winner && m.winner.w.id === id) });
    }
  }
  return out;
}"""

# [3] THE LOCK. `hexClock` is read every step and a RESET is a fire -- the
# engine's own field, so this is an observation rather than a second
# implementation of the rule. `noHit` runs the identical matchup with the
# relic's onHit deleted, which is the only way to say what share of the
# foe's locked time this school is responsible for: hitstun locks the weapon
# too, and it was going to happen anyway.
LOCK_JS = """([id, aff, shape, key, per, foes, seeds, pin, pinIds, secs, noHit]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === id);
  const sv = { aff: w.aff, shape: w.shape, reach: w.reach, width: w.width,
               artW: w.artW, spin: w.spin, mode: w.mode, mass: w.mass,
               onHit: w.onHit, arc: w.arc, blades: w.blades };
  const PROTO = { scythe:{reach:104,width:11,artW:46,spin:3.2,mode:"spin",mass:2.4,arc:undefined,blades:[0]},
                  greatsword:{reach:116,width:14,artW:40,spin:3.4,mode:"swing",mass:3.0,arc:1.5,blades:[0]},
                  twinblade:{reach:62,width:8,artW:30,spin:5.7,mode:"spin",mass:1.1,arc:undefined,blades:[0,0.5]},
                  warhammer:{reach:76,width:26,artW:54,spin:1.6,mode:"spin",mass:5.0,arc:undefined,blades:[0]},
                  flail:{reach:96,width:22,artW:22,spin:2.2,mode:"chain",mass:3.6,arc:undefined,blades:[0]},
                  bow:{reach:54,width:9,artW:44,spin:2.8,mode:"ranged",mass:1.6,arc:undefined,blades:[0]} };
  const P = PROTO[shape];
  w.aff = aff; w.shape = shape;
  for (const f of ["reach","width","artW","spin","mode","mass","arc","blades"]) w[f] = P[f];
  /* `tickFire` reads `f.w.shot` and does NOT gate on mode -- `relicShot()`
     gates on mode and `tickFire` does not use it. So a `shot` field left on
     a melee weapon fires a bow on top of the melee, at cadence, forever.
     The first cut of this probe added one for the bow row and never took it
     off, and the five rows after it were a scythe with a bow bolted to it:
     0.356 hits/s against the 0.204 the same cell measures clean, and every
     stack and lock number downstream inflated ~1.9x. `addedShot` is why
     this is a tracked mutation now and not a convenience. */
  let addedShot = false;
  if (shape === "bow" && !w.shot){
    addedShot = true;
    w.shot = { cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0, tip:"" };
  }
  if (noHit) delete w.onHit; else { w.onHit = {}; w.onHit[key] = per; }

  const saved = {}, savedUlt = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid);
    if (!x) continue;
    saved[pid] = x.dmg; x.dmg = pin;
    savedUlt[pid] = x.ult.charge; x.ult.charge = 1e9;
  }

  const rows = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let steps = 0, live = 0, fires = 0, locked = 0, sumStacks = 0;
      let sumHxLive = 0, prevClock = 0, ge2 = 0;
      while (!m.over && steps < secs / DT){
        /* HITSTOP. `step` returns on its first branch while `hitStop > 0`,
           so `tickStatus` never runs and the hex clock does not advance --
           but the second does. Read BEFORE stepping, because the step is
           what spends it. Without this the clock integral is taken over
           wall time and comes out ~15% above the fires the engine actually
           delivered, which is a discrepancy in the instrument that reads
           exactly like a discrepancy in the rule. */
        const frozen = m.hitStop > 0 || !!m.latch || !!m.splitHold;
        /* Read BEFORE the step. `tickStatus` advances the clock with the
           stacks standing at the top of the step; a hit lands later in the
           same step, in `tickHits`. Reading after attributes that hit's
           stack to a step the clock never saw it in. */
        const pre = th.status[key];
        const preN = pre ? pre.stacks : 0;
        m.step(DT); steps++;
        const c = th.hexClock || 0;
        if (c < prevClock - 1e-9) fires++;      // the clock reset: it fired
        prevClock = c;
        if (th.stun > 0) locked++;
        const st = th.status[key];
        const n = st ? st.stacks : 0;
        sumStacks += n;
        if (!frozen){ live++; sumHxLive += preN * DT; }
        if (n >= 2) ge2++;
      }
      const dur = steps * DT;
      rows.push({ foe: f, seed: s, dur, hits: me.hits,
                  fires, firesPerS: dur ? fires / dur : 0,
                  /* The clock is at 0 at the first step and holds `prevClock`
                     unspent at the bell, so the integral buys
                     (integral - tail) / stunEvery fires, not integral / it. */
                  predFires: (sumHxLive - prevClock) / AC.STATUS.hex.stunEvery,
                  hitStop: steps ? 1 - live / steps : 0,
                  lockShare: steps ? locked / steps : 0,
                  meanStacks: steps ? sumStacks / steps : 0,
                  p2: steps ? ge2 / steps : 0 });
    }
  }

  Object.assign(w, sv);
  if (!sv.onHit) delete w.onHit;
  if (sv.arc === undefined) delete w.arc;
  if (addedShot) delete w.shot;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid]; x.ult.charge = savedUlt[pid];
  }
  return rows;
}"""

DUR_JS = """([id, foes, seeds, pin, pinIds, secs, durs]) => {
  const DT = AC.CONFIG.physics.dt;
  const S = AC.STATUS.hex, sv = S.dur;
  const saved = {}, savedUlt = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid);
    if (!x) continue;
    saved[pid] = x.dmg; x.dmg = pin;
    savedUlt[pid] = x.ult.charge; x.ult.charge = 1e9;
  }
  const out = [];
  for (const d of durs){
    S.dur = d;
    let fires = 0, dur = 0, locked = 0, steps = 0, sum = 0, wins = 0, n = 0;
    for (const f of foes){
      for (const s of seeds){
        const m = new AC.Match(id, f, s);
        const me = m.a.w.id === id ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        let st2 = 0, prev = 0;
        while (!m.over && st2 < secs / DT){
          m.step(DT); st2++;
          const c = th.hexClock || 0;
          if (c < prev - 1e-9) fires++;
          prev = c;
          if (th.stun > 0) locked++;
          const s3 = th.status.hex;
          sum += s3 ? s3.stacks : 0;
        }
        steps += st2; dur += st2 * DT; n++;
        if (m.winner && m.winner.w.id === id) wins++;
      }
    }
    out.push({ dur: d, firesPerS: fires / dur, lockShare: locked / steps,
               meanStacks: sum / steps, win: wins / n });
  }
  S.dur = sv;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid]; x.ult.charge = savedUlt[pid];
  }
  return out;
}"""

ARENA_JS = """([a, b, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  m.introT = 0;
  for (let i = 0; i < Math.round(secs / DT); i++) m.step(DT);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

BLADES_JS = """([keys, L, W, zoom]) => {
  const out = [];
  for (const k of keys){
    const S = Math.round(L * 1.7);
    const cv = document.createElement("canvas");
    cv.width = S * zoom; cv.height = S * zoom;
    const c = cv.getContext("2d");
    c.scale(zoom, zoom);
    c.fillStyle = "#0B0912"; c.fillRect(0, 0, S, S);
    c.translate(S * 0.30, S / 2);
    AC.SHAPES.scythe(c, L, W, AC.AFFINITIES[k], 0.55);
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


PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-redflail.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--out", default="../05-reference/v39")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    outdir = (HERE / a.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    seeds = [101 + 7 * i for i in range(a.seeds)]
    res = {}

    with game(game_path=gp) as (page, errors):
        pin_ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")

        # ------------------------------------------------------------ [1] --
        print("\n[1] DISPATCH — does the runic scythe reach its own branch?\n")
        neg = page.evaluate(BRANCH_JS, [None])
        said = page.evaluate(INJECT_JS, CELL)
        print(f"    {said}")
        pos = page.evaluate(BRANCH_JS, ["runic"])
        print(f"    runic fires:        {', '.join(pos['fired'])}")
        print(f"    nonsense key fires: {', '.join(neg['fired'])}")
        check("_scConjured draws the runic scythe",
              "_scConjured" in pos["fired"], "the runic branch, reached")
        check("negative control — a nonsense key does NOT reach _scConjured",
              "_scConjured" not in neg["fired"],
              "falls to " + ", ".join(neg["fired"]))

        # ------------------------------------------------------------ [2] --
        print("\n[2] DOES IT FIGHT — 6 foes, pinned seeds, placeholder nova\n")
        rows = page.evaluate(FIGHT_JS, [CELL["id"], FOES, seeds])
        durs = [r["dur"] for r in rows]
        print(f"    {len(rows)} matches   mean {statistics.mean(durs):.1f}s"
              f"   min {min(durs):.1f}   max {max(durs):.1f}"
              f"   timeouts {sum(1 for r in rows if not r['over'])}"
              f"   win {statistics.mean(1 if r['won'] else 0 for r in rows):.0%}")
        check("no timeouts", all(r["over"] for r in rows),
              f"{sum(1 for r in rows if not r['over'])}/{len(rows)}")
        check("it lands hits on every foe",
              all(statistics.mean(r["hits"] for r in rows if r["foe"] == f) > 0
                  for f in FOES),
              "min per-foe mean "
              f"{min(statistics.mean(r['hits'] for r in rows if r['foe'] == f) for f in FOES):.1f}")

        # ------------------------------------------------------------ [3] --
        print(f"\n[3] THE LOCK — hex delivered, not hex held. dmg pinned "
              f"{a.pin}, ults suppressed\n")
        print(f"    {'carried on':<24}{'hits/s':>8}{'mean':>7}{'>=2':>6}"
              f"{'fires/s':>9}{'lock':>7}{'net':>7}{'hitStop':>9}")
        lock = {}
        types = ["bow", "twinblade", "greatsword", "scythe", "warhammer", "flail"]
        for shape in types:
            foes = [f for f in FOES if f != CELL["id"]]
            on = page.evaluate(LOCK_JS, [CELL["id"], "runic", shape, "hex", 1,
                                         foes, seeds, a.pin, pin_ids, a.secs, False])
            off = page.evaluate(LOCK_JS, [CELL["id"], "runic", shape, "hex", 1,
                                          foes, seeds, a.pin, pin_ids, a.secs, True])
            d = sum(r["dur"] for r in on)
            row = {
                "hps": sum(r["hits"] for r in on) / d,
                "mean": statistics.mean(r["meanStacks"] for r in on),
                "p2": statistics.mean(r["p2"] for r in on),
                "fps": statistics.mean(r["firesPerS"] for r in on),
                "lock": statistics.mean(r["lockShare"] for r in on),
                "base": statistics.mean(r["lockShare"] for r in off),
                "hitStop": statistics.mean(r["hitStop"] for r in on),
                "obs": sum(r["fires"] for r in on),
                "pred": sum(r["predFires"] for r in on),
            }
            row["net"] = row["lock"] - row["base"]
            lock[shape] = row
            star = "  <-- THIS CELL" if shape == "scythe" else ""
            print(f"    {'hex x ' + shape:<24}{row['hps']:>8.3f}{row['mean']:>7.2f}"
                  f"{row['p2']:>6.0%}{row['fps']:>9.3f}{row['lock']:>7.1%}"
                  f"{row['net']:>+6.1%}{row['hitStop']:>9.1%}{star}")
        check("removing onHit lowers the foe's locked share on every type",
              all(lock[s]["net"] > 0 for s in types),
              "min " + f"{min(lock[s]['net'] for s in types):+.3f}"
              " — a negative would mean the A/B is not isolating hex")
        # The rule is `hexClock += dt * stacks`, fire at 1.15 -- but only on
        # steps the engine actually ticks. Predicted fires are the integral
        # of stacks over UNFROZEN time; the residual is the clock left
        # unspent at the bell, at most one fire per match.
        # Asserted in aggregate. Per match the residual is dominated by the
        # overshoot `hexClock = 0` throws away on each fire, which is real and
        # is bounded by dt x stacks; across 36 matches it should stay small
        # against the fires actually delivered. A mechanic feeding the clock
        # from anywhere else would not.
        rel = {s2: abs(lock[s2]["pred"] - lock[s2]["obs"]) / lock[s2]["obs"]
               for s2 in types}
        check("fires are the integral of stacks over unfrozen time / "
              "stunEvery — nothing else feeds the clock",
              all(v < 0.03 for v in rel.values()),
              "worst disagreement over "
              + f"{int(lock['scythe']['obs'])}+ observed fires: "
              + f"{max(rel.values()):.2%}")
        check("hitstop is not negligible — it is why occupancy overstates "
              "the lock",
              all(lock[s2]["hitStop"] > 0.02 for s2 in types),
              "scythe spends "
              + f"{lock['scythe']['hitStop']:.1%} of the fight frozen")

        # ------------------------------------------------------------ [4] --
        print(f"\n[4] WHAT THE CLOCK WOULD HAVE TO BE — hex `dur` swept on "
              f"the scythe alone\n")
        page.evaluate(INJECT_JS, CELL)
        foes = [f for f in FOES if f != CELL["id"]]
        sw = page.evaluate(DUR_JS, [CELL["id"], foes, seeds, a.pin, pin_ids,
                                    a.secs, [2.6, 3.4, 4.2, 5.0, 6.5, 99]])
        print(f"    {'hex dur':>9}{'mean':>8}{'fires/s':>9}{'lock':>8}{'win':>8}")
        for r in sw:
            tag = "   <-- shipped" if abs(r["dur"] - 2.6) < 1e-9 else ""
            print(f"    {r['dur']:>9.1f}{r['meanStacks']:>8.2f}"
                  f"{r['firesPerS']:>9.3f}{r['lockShare']:>8.1%}{r['win']:>8.0%}{tag}")
        check("a longer clock delivers more lock — the sweep is connected",
              sw[-1]["lockShare"] > sw[0]["lockShare"],
              f"{sw[0]['lockShare']:.1%} at 2.6 -> {sw[-1]['lockShare']:.1%} at 99")

        # ------------------------------------------------------------ [5] --
        print(f"\n[5] LEGIBILITY\n")
        blades = [png(d) for d in page.evaluate(
            BLADES_JS, [["runic", "verdant", "sanctified"], 104, 46, 5])]
        sheet(blades, ["runic (THIS CELL)", "verdant / Thornwake",
                       "sanctified / Lastlight"],
              outdir / "runic-scythe-5x.png", 1.0,
              "THE THREE SCYTHES AT 5x — runic against the two that ship")
        shots = []
        for foe, lab in ((("thornwake"), "v Thornwake, the verdant scythe"),
                         (("spellbreaker"), "v Spellbreaker, the runic twinblade"),
                         (("axiom"), "v Axiom, the runic greatsword")):
            shots.append((png(page.evaluate(ARENA_JS, [CELL["id"], foe, 337, 5.2])), lab))
        sheet([s for s, _ in shots], [l for _, l in shots],
              outdir / "runic-scythe-arena.png", 0.34,
              "1:1 — same type, then same school twice")

        assert not errors, errors[:4]

    res = {"lock": lock, "durSweep": sw}
    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED)" if bad else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(res, indent=1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
