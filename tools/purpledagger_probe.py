#!/usr/bin/env python3
"""LOOK AT THE PURPLE DAGGERS BEFORE DESIGNING THEM.

    python3 purpledagger_probe.py --game ../02-chain/sc-health18.html

The umbral x twinblade cell has finished art (`SHAPES._tbEaten`, dispatched on
`p.key === "umbral"`) and no relic wearing it. Same situation
`whitescythe_probe.py` was written for, and this file is its sibling.

Before anyone argues about a name or an ultimate, this renders the cell as it
would actually appear and MEASURES THE ONE THING THAT COULD KILL IT.

  [1] DISPATCH — that the injected relic renders through `SHAPES.twinblade`'s
      umbral branch and not the `_twinDagger` fallback. `_tbEaten` CALLS
      `_twinDagger`, so "the dagger drew" is not evidence; the check is that
      `_tbEaten` is in the fired list. A negative control with a nonsense
      affinity key must fire ONLY `_twinDagger`, or this check cannot fail and
      is worthless.

  [2] DOES IT FIGHT — four opponents, pinned seeds. A cell that draws but never
      lands anything is caught here rather than after a tuner run.

  [3] CURSE x TWINBLADE — the hazard, measured. Curse is the only status that
      never expires and eats MAXIMUM life.

      THIS BLOCK'S ORIGINAL RATIONALE WAS FALSE and is corrected here rather
      than quietly deleted. It read "twinblade is the highest contact-rate
      type in the game (reach 62, spin 5.7, TWO blades)". v36 §2 falsified it
      with `contact_rate_probe.py`, damage pinned at 14.0 across all eighteen
      relics so lethality could not buy a rate:

          bow 0.360 hits/s · greatsword 0.283 · TWINBLADE 0.271 ·
          scythe 0.228 · flail 0.205 · warhammer 0.183

      Third of six. Contact rate in this sim is REACH-dominated, not
      spin-dominated: a greatsword sweeping 3.5x the area more than cancels
      reach 62. `_tbEaten`'s own comment ("the fastest thing on the floor")
      and `weapon-matrix.md` §4's "closest, fastest" are claims about the
      picture, not about the sim.

      What survives measurement, and is the real reason to run this block:
      the twinblade lands FIRST among melee — 3.10s to first hit against the
      greatsword's 3.78s and the flail's 4.40s. Permanence x the type that
      OPENS EARLIEST is still a hazard. It is a different hazard from the one
      this probe was written to test, and the numbers below are what decide
      it, not this paragraph.

  [4] LEGIBILITY — a still against both umbral relics, because v28 found
      same-affinity pairs read as one smudge and this school now has three.

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
W, H = 1080, 1920

# The provisional cell. Every physics number is the TWINBLADE profile exactly,
# copied from Widowmaker and Spellbreaker which share it byte for byte
# (weapon-matrix decision 1: type owns the physics, school owns status and
# palette). A new twinblade that changes reach/spin/mass is not a new school
# cell, it is a new type wearing a dagger's name.
#
# `dmg` is a PLACEHOLDER and nothing here should be read as a balance claim:
# it is the mean of the two shipped twinblades (11.95, 8.81).
#
# v36 REGISTERED A PREDICTION HERE AND IT WAS WRONG, which is worth more than
# the number. The factored model says umbral's school modifier should sit
# BELOW 1.0 because curse compounds, so the tuned blade should have landed
# under 10.38. It landed at 19.0 — above Widowmaker's 11.95 on the identical
# physics profile. The reason: curse's value DECAYS inside a fight in a way
# hemorrhage's does not. An application on a full-health foe takes 13 real hp,
# because `hp` is clamped to `maxHp`; the same application on a foe already at
# half health takes nothing until the ceiling catches up. Hemorrhage is worth
# its 9.6 whenever it lands.
#
# So umbral's school modifier is not a scalar — it is a function of WHEN in the
# fight the hit lands, and no `mod[school]` term can express that. DO NOT TRUST
# A DERIVED BLADE FOR THIS CELL. Sweep it.
#
# `onHit` is an OPEN QUESTION this probe exists to inform. Widowmaker applies
# 2 stacks a hit on the same physics; Gravemourn and Nightfell both apply
# curse:1. Set with --stacks and look at [3].
#
# The ult is a STAND-IN so the card has something to lay out. It is not a
# design, and ult set-piece art dispatches on relic ID, so anything it draws
# on screen is the DONOR's set-piece and is a lie. Same caveat whitescythe
# carried.
DONOR = "axiom"
BASE_PROVISIONAL = {
    "id": DONOR, "name": "Purpledagger", "aff": "umbral",
    "shape": "twinblade",
    "blades": [0, 0.5], "reach": 62, "width": 8, "artW": 30,
    "dmg": 10.38, "spin": 5.7, "mode": "spin", "mass": 1.1,
    "onHit": {"curse": 1},
    "ult": {"name": "Placeholder", "charge": 14, "kind": "nova", "radius": 240,
            "dmg": 12, "apply": {"curse": 3}, "knock": 200,
            "tip": "PLACEHOLDER — nova: 12 damage, 3 Curse, knockback"},
    "blurb": "Provisional. Injected at runtime for a look; nothing is built.",
}

INJECT_JS = """(relic) => {
  const w = AC.WEAPONS.find(x => x.id === relic.id);
  if (!w) return "donor missing: " + relic.id;
  for (const k of Object.keys(w)) delete w[k];
  Object.assign(w, relic);
  return "overwrote donor " + relic.id + " in place";
}"""

# Which draw branch actually ran. `SHAPES.twinblade` dispatches on `p.key`, so
# the only honest way to ask is to wrap every candidate branch and see which
# fires. `aff` is passed separately because the dispatcher reads `p.key || aff`.
BRANCH_JS = """([id, palKey]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const names = ["_tbEaten", "_twinDagger", "_twinConjured", "_tbGrown",
                 "_tbBarbed", "_tbRadiant", "_tbBuilt", "_tbPlated"];
  const fired = [];
  const orig = {};
  for (const n of names){
    if (typeof AC.SHAPES[n] !== "function") continue;
    orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this, a); };
  }
  const cv = document.createElement("canvas");
  cv.width = 400; cv.height = 400;
  const c = cv.getContext("2d");
  c.translate(60, 200);
  const pal = palKey === null ? { key: "NOT_A_SCHOOL",
                                  core:"#888", glow:"#aaa", dark:"#222",
                                  steel:"#ccc" }
                              : AC.AFFINITIES[palKey];
  AC.SHAPES.twinblade(c, w.reach, w.width, pal, undefined, pal.key);
  for (const n of Object.keys(orig)) AC.SHAPES[n] = orig[n];
  return fired;
}"""

CARD_JS = """([a, b, seed, e]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = Math.max(0, AC.CONFIG.intro.dur - e);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

ARENA_JS = """([a, b, seed, steps]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  for (let i = 0; i < steps; i++) m.step(1 / 60);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

FIGHT_JS = """([id, foes, seed]) => {
  const out = [];
  for (const f of foes){
    const m = new AC.Match(id, f, seed);
    let steps = 0;
    while (!m.over && steps < 60 * 120){ m.step(1/60); steps++; }
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    out.push({ foe: f, dur: +(steps/60).toFixed(2), over: !!m.over,
               hits: me.hits, myHp: Math.round(me.hp), foeHp: Math.round(th.hp),
               dealt: Math.round(th.maxHp - th.hp),
               winner: m.winner ? m.winner.w.name : null });
  }
  return out;
}"""

# [3] THE HAZARD. One relic against one field, sampled every step.
#
# `pin` sets every listed relic's dmg to the same number so contact rate is
# isolated from lethality — time-to-8-stacks is otherwise confounded by the
# fact that a harder-hitting relic ends the fight sooner and therefore has
# fewer seconds in which to stack. Restored after each run.
CURSE_JS = """([id, foes, seeds, pin, pinIds]) => {
  const saved = {};
  if (pin !== null){
    for (const pid of pinIds){
      const w = AC.WEAPONS.find(x => x.id === pid);
      saved[pid] = w.dmg; w.dmg = pin;
    }
  }
  const rows = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let steps = 0, tFull = null, tFirst = null;
      const startMax = th.maxHp;
      while (!m.over && steps < 60 * 120){
        m.step(1/60); steps++;
        const st = th.stacks("curse");
        if (tFirst === null && st >= 1) tFirst = steps / 60;
        if (tFull === null && st >= 8) tFull = steps / 60;
      }
      rows.push({ foe: f, seed: s, dur: steps/60, hits: me.hits,
                  stacks: th.stacks("curse"),
                  tFirst: tFirst, tFull: tFull,
                  maxLost: startMax - th.maxHp, startMax: startMax,
                  won: !!(m.winner && m.winner.w.id === id) });
    }
  }
  for (const pid of Object.keys(saved)){
    AC.WEAPONS.find(x => x.id === pid).dmg = saved[pid];
  }
  return rows;
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def contact(imgs, labels, out, scale, title):
    cols = len(imgs)
    tw, th = int(W * scale), int(H * scale)
    PAD, LBL = 16, 34
    sh = Image.new("RGB", (cols * (tw + PAD) + PAD, th + PAD * 2 + LBL), (12, 10, 18))
    dr = ImageDraw.Draw(sh)
    dr.text((PAD, 8), title, fill=(201, 162, 39))
    for i, (im, lab) in enumerate(zip(imgs, labels)):
        x = PAD + i * (tw + PAD)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, PAD + LBL))
        dr.text((x + 2, PAD + LBL - 15), lab, fill=(214, 200, 170))
    sh.save(out)
    print(f"  {out.name}  ({sh.width}x{sh.height})")
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fmt(x, n=2):
    return "  --  " if x is None else f"{x:.{n}f}"


def summarise(label, rows):
    """One line per relic. Everything here is derived from the sampled rows."""
    n = len(rows)
    dur = statistics.mean(r["dur"] for r in rows)
    hps = statistics.mean(r["hits"] / r["dur"] for r in rows)
    full = [r for r in rows if r["tFull"] is not None]
    lost = statistics.mean(r["maxLost"] for r in rows)
    wr = sum(1 for r in rows if r["won"]) / n
    return {
        "label": label, "n": n, "dur": dur, "hits_per_s": hps,
        "reached8": len(full) / n, "t_to_8": med([r["tFull"] for r in rows]),
        "t_first": med([r["tFirst"] for r in rows]),
        "max_lost": lost, "max_lost_pct": 100 * lost / rows[0]["startMax"],
        "winrate": wr,
    }


def table(title, rowsets):
    print(f"\n{title}")
    print(f"    {'relic':<26} {'hits/s':>7} {'dur':>7} {'1st curse':>10} "
          f"{'t->8':>7} {'hit 8':>7} {'maxHP lost':>12} {'win':>6}")
    for s in rowsets:
        print(f"    {s['label']:<26} {s['hits_per_s']:>7.2f} {s['dur']:>7.1f} "
              f"{fmt(s['t_first']):>10} {fmt(s['t_to_8']):>7} "
              f"{100*s['reached8']:>6.0f}% "
              f"{s['max_lost']:>6.0f} ({s['max_lost_pct']:>3.0f}%) "
              f"{100*s['winrate']:>5.0f}%")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-health18.html")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--seeds", type=int, default=12,
                    help="matches per (relic, foe) cell in [3]")
    ap.add_argument("--stacks", type=int, default=1,
                    help="curse stacks the provisional relic applies per hit")
    ap.add_argument("--dmg", type=float, default=None,
                    help="override the placeholder damage")
    ap.add_argument("--pin", type=float, default=12.0,
                    help="damage all three umbral relics are pinned to for the "
                         "isolated pass in [3]")
    ap.add_argument("--hold", type=float, default=2.2)
    ap.add_argument("--steps", type=int, default=150)
    ap.add_argument("--scale", type=float, default=0.42)
    ap.add_argument("--outdir", default="..")
    ap.add_argument("--tag", default="", help="suffix for the written PNGs")
    ap.add_argument("--no-render", action="store_true",
                    help="checks and measurement only, no images")
    A = ap.parse_args()

    prov = dict(BASE_PROVISIONAL)
    prov["onHit"] = {"curse": A.stacks}
    if A.dmg is not None:
        prov["dmg"] = A.dmg

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")
    outdir = (HERE / A.outdir).resolve()

    # Foils: the type's own column (the two shipped twinblades), and the
    # school's own two relics, which are both the sibling argument and the
    # v28 same-affinity smudge risk.
    FOILS = [("widowmaker", "v Widowmaker  (bloodsworn twinblade — the column)"),
             ("spellbreaker", "v Spellbreaker  (runic twinblade — the column)"),
             ("gravemourn", "v Gravemourn  (SAME AFFINITY — smudge risk)"),
             ("nightfell", "v Nightfell  (SAME AFFINITY — smudge risk)")]

    print(f"game   {g.name}")
    print(f"cell   umbral x twinblade   onHit curse:{A.stacks}   "
          f"dmg {prov['dmg']} (placeholder)")

    cards, arenas, labels = [], [], []
    ok = {}
    with game(game_path=g) as (page, errors):
        print(page.evaluate(INJECT_JS, prov), "— relic injected")

        # ---------------------------------------------------------- [1]
        fired = page.evaluate(BRANCH_JS, [prov["id"], "umbral"])
        ctrl = page.evaluate(BRANCH_JS, [prov["id"], None])
        print(f"\n[1] draw branch")
        print(f"    umbral palette   fired: {fired}")
        print(f"    nonsense key     fired: {ctrl}   <- negative control")
        ok["branch"] = "_tbEaten" in fired
        ok["control"] = ("_tbEaten" not in ctrl) and ("_twinDagger" in ctrl)
        print(f"    _tbEaten reached:            "
              f"{'PASS' if ok['branch'] else 'FAIL — fell through to the base dagger'}")
        print(f"    control falls through only:  "
              f"{'PASS' if ok['control'] else 'FAIL — the check cannot fail, so it proves nothing'}")

        # ---------------------------------------------------------- [2]
        fights = page.evaluate(FIGHT_JS,
                               [prov["id"], [f for f, _ in FOILS], A.seed])
        print("\n[2] does it fight?")
        ok["fights"] = True
        for r in fights:
            bad = (not r["over"]) or r["dealt"] <= 0 or r["hits"] < 6
            ok["fights"] &= not bad
            print(f"    v {r['foe']:<13} {r['dur']:>6.1f}s  {r['hits']:>3} hits  "
                  f"dealt {r['dealt']:>4}  winner {str(r['winner']):<14}"
                  f"{'  <-- FAIL' if bad else ''}")

        # ---------------------------------------------------------- [3]
        seeds = [A.seed + i * 7919 for i in range(A.seeds)]
        FIELD = ["widowmaker", "spellbreaker", "thornwake", "emberedge",
                 "lightkeeper", "dawnbringer"]
        UMBRAL = [prov["id"], "gravemourn", "nightfell"]
        NAMES = {prov["id"]: "provisional twinblade",
                 "gravemourn": "Gravemourn (flail)",
                 "nightfell": "Nightfell (greatsword)"}

        print(f"\n[3] curse x twinblade — {len(FIELD)} foes x {len(seeds)} seeds "
              f"= {len(FIELD)*len(seeds)} matches per relic")
        shipped, pinned = [], []
        for rid in UMBRAL:
            rows = page.evaluate(CURSE_JS, [rid, FIELD, seeds, None, UMBRAL])
            shipped.append(summarise(NAMES[rid], rows))
            rows = page.evaluate(CURSE_JS, [rid, FIELD, seeds, A.pin, UMBRAL])
            pinned.append(summarise(NAMES[rid], rows))

        table("    AS SHIPPED (each relic at its own damage)", shipped)
        table(f"    PINNED to dmg {A.pin} — contact isolated from lethality", pinned)

        tw, gm = pinned[0], pinned[1]
        print(f"\n    contact ratio, twinblade / flail, pinned: "
              f"{tw['hits_per_s']/gm['hits_per_s']:.2f}x")
        print(f"    max HP taken, twinblade vs flail, pinned: "
              f"{tw['max_lost']:.0f} vs {gm['max_lost']:.0f} of "
              f"{300} baseHP")

        # ---------------------------------------------------------- [4]
        if not A.no_render:
            print("\n[4] the pictures")
            for foe, lab in FOILS:
                cards.append(png(page.evaluate(
                    CARD_JS, [prov["id"], foe, A.seed, A.hold])))
                arenas.append(png(page.evaluate(
                    ARENA_JS, [prov["id"], foe, A.seed, A.steps])))
                labels.append(lab)

        if errors:
            print("\nPAGE ERRORS (a silent exception reads as a clean run):")
            for e in errors[:10]:
                print("   ", e)
            ok["clean"] = False
        else:
            ok["clean"] = True

    if cards:
        contact(cards, labels, outdir / f"purpledagger-cards{A.tag}.png", A.scale,
                "PURPLE DAGGERS — the card, provisional, nothing built")
        contact(arenas, labels, outdir / f"purpledagger-arena{A.tag}.png", A.scale,
                f"PURPLE DAGGERS — arena at {A.steps} steps")

    print("\n" + "=" * 62)
    for k, v in ok.items():
        print(f"  {k:<10} {'PASS' if v else 'FAIL'}")
    print("=" * 62)
    print("NOTHING WAS WRITTEN. This is a look, not a build.")
    return 0 if all(ok.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
