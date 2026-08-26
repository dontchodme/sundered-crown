#!/usr/bin/env python3
"""LOOK AT THE WHITE SCYTHE BEFORE DESIGNING IT.

    python3 whitescythe_probe.py --game ../02-chain/sc-cardspin.html

The sanctified scythe cell has finished art (`SHAPES._scRadiant`, dispatched on
`p.key === "sanctified"`) and no relic wearing it. Before anyone argues about a
name or an ultimate, this renders the cell as it would actually appear: the
fight card, an arena still mid-swing, and a bare silhouette pass — with a
PROVISIONAL relic injected at runtime and NOTHING written to any build.

What it deliberately checks while it is in there:

  * that the injected relic renders through `SHAPES.scythe`'s sanctified
    branch and not the `_scBase` fallback — a `p.key` that does not match
    silently falls through to the base crescent, which would make this whole
    sheet a picture of the wrong thing;
  * that it fights — four opponents, pinned seeds, so a cell that draws but
    never lands anything is caught here rather than after a tuner run;
  * legibility against a sanctified opponent, because the school already has
    three relics and v28 found that same-affinity pairs read as one smudge.

Injection is runtime-only and the page is thrown away. This is a LOOK, not a
build.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
W, H = 1080, 1920

# The provisional cell. Every physics number is Thornwake's, exactly — the
# scythe archetype is fixed by the TYPE (weapon-matrix decision 1), so a new
# scythe that changes reach/spin/mass is not a new school cell, it is a new
# type wearing a scythe's name. dmg is a PLACEHOLDER and is Thornwake's until
# a tuner pass says otherwise; the ult below is a stand-in so the card has
# something to lay out, NOT a design.
#
# THE ID IS BORROWED, AND THAT IS NOT COSMETIC. `WEAPON_BY_ID` is built once
# at load and is NOT on the `AC` surface, so pushing onto `AC.WEAPONS` gets a
# relic the roster can see and `new AC.Match()` cannot construct ("Unknown
# relic id" — hit on the first run of this probe). The reachable injection is
# to overwrite an existing relic OBJECT in place, since the map and the array
# hold the same reference. `axiom` is the donor: a runic greatsword, so every
# field this cell cares about is replaced, and losing it for one page costs
# nothing. Consequence to hold onto — ult set-piece art is dispatched on the
# relic ID, so anything the placeholder ult draws is AXIOM's set-piece, not
# this cell's. The weapon art is the sanctified scythe; the ult art is a lie.
DONOR = "axiom"
PROVISIONAL = {
    "id": DONOR, "name": "Whitescythe", "aff": "sanctified",
    "shape": "scythe",
    "blades": [0], "reach": 104, "width": 11, "artW": 46,
    "dmg": 31.35, "spin": 3.2, "mode": "spin", "mass": 2.4,
    "onHit": {"smite": 1},
    "ult": {"name": "Placeholder", "charge": 15, "kind": "nova", "radius": 260,
            "dmg": 10, "apply": {"smite": 3}, "knock": 200,
            "tip": "PLACEHOLDER — nova: 10 damage, 3 Smite, knockback"},
    "blurb": "Provisional. Injected at runtime for a look; nothing is built.",
}

INJECT_JS = """(relic) => {
  const w = AC.WEAPONS.find(x => x.id === relic.id);
  if (!w) return "donor missing: " + relic.id;
  for (const k of Object.keys(w)) delete w[k];
  Object.assign(w, relic);
  return "overwrote donor " + relic.id + " in place";
}"""

# Which draw branch actually ran. `SHAPES.scythe` dispatches on `p.key`, so the
# only honest way to ask is to wrap each candidate branch and see which fires.
BRANCH_JS = """(id) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const names = ["_scRadiant", "_scBase", "_scGrown", "_scBuilt", "_scPlated",
                 "_scBarbed", "_scEaten", "_scConjured"];
  const fired = [];
  const orig = {};
  for (const n of names){
    orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this, a); };
  }
  const cv = document.createElement("canvas");
  cv.width = 400; cv.height = 400;
  const c = cv.getContext("2d");
  c.translate(60, 200);
  const pal = AC.AFFINITIES[w.aff];
  AC.SHAPES.scythe(c, w.reach, w.width, pal, undefined, w.aff);
  for (const n of names) AC.SHAPES[n] = orig[n];
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

# Does it fight? Four opponents, pinned seeds, hard cap. A relic that exists,
# draws, and never lands anything is the failure this guards — copied in
# spirit from roster_gs_build.py's CHECK_JS.
FIGHT_JS = """([id, foes, seed]) => {
  const out = [];
  for (const f of foes){
    const m = new AC.Match(id, f, seed);
    let steps = 0;
    while (!m.over && steps < 60 * 120){ m.step(1/60); steps++; }
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    out.push({ foe: f, dur: +(steps/60).toFixed(2), over: !!m.over,
               myHp: Math.round(me.hp), foeHp: Math.round(th.hp),
               dealt: Math.round(th.maxHp - th.hp),
               winner: m.winner ? m.winner.w.name : null });
  }
  return out;
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--hold", type=float, default=2.2)
    ap.add_argument("--steps", type=int, default=150)
    ap.add_argument("--scale", type=float, default=0.42)
    ap.add_argument("--outdir", default="..")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")
    outdir = (HERE / A.outdir).resolve()

    # Foils: the type it shares a column with (verdant scythe), the school's
    # own flagship (the same-affinity legibility risk), and one loud contrast.
    FOILS = [("thornwake", "v Thornwake  (verdant scythe — the column)"),
             ("dawnbringer", "v Dawnbringer  (SAME AFFINITY — smudge risk)"),
             ("gravemourn", "v Gravemourn  (umbral flail — contrast)")]

    cards, arenas, labels = [], [], []
    with game(game_path=g) as (page, errors):
        print(page.evaluate(INJECT_JS, PROVISIONAL), "— relic injected")

        fired = page.evaluate(BRANCH_JS, PROVISIONAL["id"])
        print(f"\n[1] draw branch: {fired}")
        ok_branch = "_scRadiant" in fired
        print(f"    _scRadiant reached: {'PASS' if ok_branch else 'FAIL — fell through to base'}")

        fights = page.evaluate(FIGHT_JS,
                               [PROVISIONAL["id"], [f for f, _ in FOILS] + ["censer"],
                                A.seed])
        print("\n[2] does it fight?")
        ok_fight = True
        for r in fights:
            bad = (not r["over"]) or r["dealt"] < 40
            ok_fight &= not bad
            print(f"    v {r['foe']:<13} {r['dur']:>6.2f}s  over={r['over']!s:<5} "
                  f"dealt={r['dealt']:>4}  hp {r['myHp']}/{r['foeHp']}  "
                  f"won: {r['winner']}{'   <-- FAIL' if bad else ''}")

        for fid, lab in FOILS:
            cards.append(png(page.evaluate(CARD_JS, [PROVISIONAL["id"], fid, A.seed, A.hold])))
            arenas.append(png(page.evaluate(ARENA_JS, [PROVISIONAL["id"], fid, A.seed, A.steps])))
            labels.append(lab)

        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    print("\n[3] sheets")
    c = contact(cards, labels, outdir / "whitescythe-cards.png", A.scale,
                f"PROVISIONAL SANCTIFIED SCYTHE — fight card, {A.hold}s into the intro")
    a = contact(arenas, labels, outdir / "whitescythe-arena.png", A.scale,
                f"PROVISIONAL SANCTIFIED SCYTHE — mid-fight, {A.steps} steps, seed {A.seed}")

    print(f"\nbranch {'PASS' if ok_branch else 'FAIL'} · fights "
          f"{'PASS' if ok_fight else 'FAIL'} · nothing was written to any build")
    print(json.dumps({"cards": str(c), "arena": str(a)}, indent=2))
    return 0 if (ok_branch and ok_fight) else 1


if __name__ == "__main__":
    sys.exit(main())
