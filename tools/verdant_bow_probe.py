#!/usr/bin/env python3
"""LOOK AT THE VERDANT BOW BEFORE DESIGNING IT.

    python3 verdant_bow_probe.py --game ../02-chain/sc-foregone.html

The cell is Rick's call out of four measured candidates (v40 bow survey, §1).
Verdant is 2/6, the thinnest school in the game that has a channel at all, and
it is the only one of the four with two same-school relics instead of three —
so it is the only one that can carry a marquee fight against its own school.

This renders the cell as it would actually appear and prices the two things a
verdant bow would be built out of, with a PROVISIONAL relic injected at runtime
and NOTHING written to any build.

  [1] THE DRAW BRANCH. `SHAPES.bow` dispatches INLINE on `p.key` with no named
      `_bow*` helper (v40 §3), so the branch cannot be caught by wrapping a
      function the way the scythe's was. It is caught by holding the palette
      and varying only the key: a differing pixel is the dispatch.

  [2] DOES IT FIGHT. Four opponents, pinned seeds. A cell that draws and never
      lands anything is caught here rather than after a tuner run.

  [3] THE MIRROR. v28: same-affinity pairs read as one smudge. Two verdant
      relics exist and both would stand beside this one. Rendered, and the
      SHAPE separation measured, because palette separation is zero by
      construction and shape is the only thing left.

  [4] WHAT VERDANT'S OWN GRAMMAR IS WORTH HERE. Both verdant ultimates are
      `kind:"freeze"`, and `freeze` is `foe.stun` — the same field hex writes.
      A stunned fighter has NO blade segments, so verdant's existing ultimate
      grammar already does the one thing the survey proved a status can do to
      the ranged path. Priced directly: root the foe and count the arrows.

  [5] THE WALL, MAPPED. 82% of every arrow ends on one. This is where, and how
      close the misses came — so "attack the wall" has a shape before anyone
      writes a mechanic.

  [6] THE KNOBS ENTANGLE HAS. `ward` had to become 2.5 on Farwarden because
      the constant was authored on a greatsword; that is the precedent for a
      per-relic value on a channel the type does not suit. Swept, so the price
      of each knob is known before one is chosen.
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
W, H = 1080, 1920

# THE PROVISIONAL CELL. Every physics number is Ironhail's, exactly — the bow
# archetype is fixed by the TYPE and all three existing bows share one `shot`
# block byte for byte (v40 §1), so a new bow that changes reach/spin/mass/shot
# is not a new school cell, it is a new type wearing a bow's name.
#
# `dmg` is Ironhail's and is a PLACEHOLDER. The channel is verdant's exactly.
# The ultimate is the literal string PLACEHOLDER and a bare nova so that
# nothing in this file can be read as a proposal — v39 §1, held to.
#
# THE ID IS BORROWED. `WEAPON_BY_ID` is built once at load and is not on the
# `AC` surface, so pushing onto `AC.WEAPONS` gets a relic the roster can see
# and `new AC.Match()` cannot construct. The reachable injection is to
# overwrite an existing relic OBJECT in place. `axiom` is the donor: a runic
# greatsword, not a foil this probe needs, and losing it for one page costs
# nothing. CONSEQUENCE TO HOLD ONTO — ult set-piece art dispatches on the
# relic ID, so anything the placeholder ult draws is AXIOM's set-piece. The
# weapon art is the verdant bow; the ult art is a lie.
DONOR = "axiom"
PROVISIONAL = {
    "id": DONOR, "name": "Verdantbow", "aff": "verdant", "shape": "bow",
    "blades": [0], "reach": 54, "width": 9, "artW": 44,
    "dmg": 16.23, "spin": 2.8, "mode": "ranged", "mass": 1.6,
    "shot": {"cadence": 0.34, "speed": 380, "r": 24, "life": 3.4, "grav": 0,
             "dmgMul": 1.0, "tip": "Fires along its facing · shots can be clanked"},
    "onHit": {"entangle": 2},
    "ult": {"name": "Placeholder", "charge": 15, "kind": "nova", "radius": 260,
            "dmg": 10, "apply": {"entangle": 3}, "knock": 200,
            "tip": "PLACEHOLDER — nova: 10 damage, 3 Entangle, knockback"},
    "blurb": "Provisional. Injected at runtime for a look; nothing is built.",
}

INJECT_JS = """(relic) => {
  const w = AC.WEAPONS.find(x => x.id === relic.id);
  if (!w) return "donor missing: " + relic.id;
  for (const k of Object.keys(w)) delete w[k];
  Object.assign(w, relic);
  return "overwrote donor " + relic.id + " in place";
}"""

# Palette HELD, key varied. The only instrument that can see this shape's
# dispatch — v39 learned it when an alpha mask reported the dwarven bow had no
# art and was flatly wrong, and v40 §3 confirmed the bow does all seven schools
# inline with no named helper to wrap.
BRANCH_JS = """([key, D, artW]) => {
  const draw = (k) => {
    const cv = document.createElement("canvas");
    cv.width = 480; cv.height = 480;
    const c = cv.getContext("2d");
    c.translate(140, 240);
    const pal = Object.assign({}, AC.AFFINITIES.dwarven, { key: k });
    AC.SHAPES.bow(c, D, artW, pal, 0.55);
    return c.getImageData(0, 0, 480, 480).data;
  };
  const a = draw(key), b = draw("NOT_A_SCHOOL"), a2 = draw(key);
  let differ = 0, union = 0, rerun = 0;
  for (let i = 0; i < a.length; i += 4){
    const A0 = a[i+3] > 24, B0 = b[i+3] > 24;
    if (A0 || B0){
      union++;
      if (!A0 || !B0 || a[i] !== b[i] || a[i+1] !== b[i+1] || a[i+2] !== b[i+2]) differ++;
    }
    if (a[i] !== a2[i] || a[i+3] !== a2[i+3]) rerun++;
  }
  return { diff: union ? differ / union : 0, union, rerun };
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

ARENA_JS = """([a, b, seed, steps, shake]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  const DT = AC.CONFIG.physics.dt;
  for (let i = 0; i < steps; i++) m.step(DT);
  /* v37 open decision 8: draw() feeds Math.random() into every frame through
     m.shake, so a frame-exact capture has to pin it first. Nothing else in
     this file is frame-exact, but the sheets should be reproducible. */
  if (shake) m.shake = 0;
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

FIGHT_JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes){
    let dur = 0, dealt = 0, wins = 0, over = 0, n = 0, hits = 0, shots = 0;
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      let steps = 0;
      while (!m.over && steps < 100 / DT){ m.step(DT); steps++; }
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      dur += steps * DT; dealt += th.maxHp - th.hp; hits += me.hits;
      shots += me.shotsFired;
      if (m.over) over++;
      if (m.winner === me) wins++;
      n++;
    }
    out.push({ foe: f, dur: dur / n, dealt: dealt / n, win: wins / n,
               over: over / n, hits: hits / n, shots: shots / n, n });
  }
  return out;
}"""

# [4] What a ROOT is worth on this type. `freeze` writes `foe.stun`, and
# `tickShots` builds the foe's blade list as `stun > 0 ? [] : segments`, so a
# rooted foe cannot parry at all. Pinned rather than earned: the root is held
# for the whole run at each level so the answer is about the root and not
# about how often an ultimate happens to land.
ROOT_JS = """([shooter, foes, seeds, secs, pin, pinIds, modes]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null,
                   onSelf: x.onSelf ? JSON.parse(JSON.stringify(x.onSelf)) : null };
    x.dmg = pin; if (x.ult) x.ult.charge = 1e9;
    delete x.onHit; delete x.onSelf;
  }
  const out = [];
  for (const mode of modes){
    let fired = 0, hit = 0, parried = 0, walled = 0, steps = 0, dealt = 0, melee = 0;
    let sep = 0, dmgShot = 0, dmgMelee = 0;
    for (const f of foes) for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let inShots = false; const pfx = [];
      const oFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, c, n, s2, l, z, dx, dy){
        if (inShots && c === "#FFF4D0" && n === 9 && s2 === 240) pfx.push(x + "," + y);
        return oFx.call(m, x, y, c, n, s2, l, z, dx, dy);
      };
      const oR = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, ov){
        const sh = m._cineShot, d0 = self.dealt;
        const r = oR.call(m, self, foe2, hx, hy, seg, mul, ov);
        if (self === me){
          if (sh){ sh._pHit = true; dmgShot += self.dealt - d0; }
          else { melee++; dmgMelee += self.dealt - d0; }
        }
        return r;
      };
      const oS = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, a2){ if (fg === me) fired++; return oS.call(m, fg, a2); };
      const oT = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice(); pfx.length = 0; inShots = true;
        const r = oT.call(m, dt); inShots = false;
        if (pre.length){
          const P = new Set(pfx), L = new Set(m.shots), own = me === m.a ? "a" : "b";
          for (const q of pre){
            if (L.has(q) || q.own !== own) continue;
            if (P.has(q.x + "," + q.y)) parried++;
            else if (q._pHit) hit++;
            else walled++;
          }
        }
        return r;
      };
      let st = 0;
      while (!m.over && st < secs / DT){
        /* ROOTED: `freeze` sets foe.stun, so this is exactly what a verdant
           ultimate already does, held open instead of decaying. PINNED, not
           applied, so nothing about an ultimate's cadence is in the answer. */
        if (mode === "rooted") th.stun = Math.max(th.stun, 1.0);
        /* PLANTED: the foe cannot MOVE but its weapon runs. Not a mechanic
           that exists — it is the control that separates "cannot parry" from
           "is standing still", which a root does both of at once. */
        if (mode === "planted"){ th.vx = 0; th.vy = 0; }
        m.step(DT); st++; steps++;
        sep += Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;
      }
      dealt += me.dealt;
    }
    out.push({ mode, fired, hit, parried, walled, melee, steps, dealt,
               dmgShot, dmgMelee,
               hitRate: fired ? hit / fired : 0,
               parryRate: fired ? parried / fired : 0,
               wallRate: fired ? walled / fired : 0,
               sep: steps ? sep / steps : 0,
               secs: steps * DT });
  }
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg; if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
    delete x.onHit; delete x.onSelf;
    if (saved[pid].onHit) x.onHit = saved[pid].onHit;
    if (saved[pid].onSelf) x.onSelf = saved[pid].onSelf;
  }
  return out;
}"""

# [5] Where the arrows die, and how close the misses came. `minD` is the
# closest the arrow ever got to the foe's SHELL over its whole flight, so a
# "near miss" is a number and not an impression.
WALL_JS = """([shooter, foes, seeds, secs, pin, pinIds]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena, R = AC.CONFIG.physics.ballR;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null,
                   onSelf: x.onSelf ? JSON.parse(JSON.stringify(x.onSelf)) : null };
    x.dmg = pin; if (x.ult) x.ult.charge = 1e9;
    delete x.onHit; delete x.onSelf;
  }
  const bins = 12;
  const deaths = { N: 0, S: 0, E: 0, W: 0 };
  const near = new Array(bins).fill(0);
  let n = 0, sumTravel = 0, sumLife = 0, hitTravel = 0, nHit = 0;
  const wallTravel = [];
  for (const f of foes) for (const sd of seeds){
    const m  = new AC.Match(shooter, f, sd);
    const me = m.a.w.id === shooter ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let inShots = false; const pfx = [];
    const oFx = AC.Match.prototype.spawnFx;
    m.spawnFx = function(x, y, c, k, s2, l, z, dx, dy){
      if (inShots && c === "#FFF4D0" && k === 9 && s2 === 240) pfx.push(x + "," + y);
      return oFx.call(m, x, y, c, k, s2, l, z, dx, dy);
    };
    const oR = AC.Match.prototype.resolveHit;
    m.resolveHit = function(self, foe2, hx, hy, seg, mul, ov){
      if (m._cineShot) m._cineShot._pHit = true;
      return oR.call(m, self, foe2, hx, hy, seg, mul, ov);
    };
    const oT = AC.Match.prototype.tickShots;
    const own = me === m.a ? "a" : "b";
    m.tickShots = function(dt){
      const pre = m.shots.slice(); pfx.length = 0; inShots = true;
      const r = oT.call(m, dt); inShots = false;
      if (pre.length){
        const P = new Set(pfx), L = new Set(m.shots);
        for (const q of pre){
          if (L.has(q) || q.own !== own) continue;
          const trav = Math.hypot(q.x - q.x0, q.y - q.y0);
          if (q._pHit){ nHit++; hitTravel += trav; continue; }
          if (P.has(q.x + "," + q.y)) continue;
          /* a wall death. Which wall, how far it got, and how close it came */
          n++; sumTravel += trav; sumLife += (q.max - q.life) / q.max;
          wallTravel.push(trav);
          const dN = q.y, dS = A.h - q.y, dE = A.w - q.x, dW = q.x;
          const mn = Math.min(dN, dS, dE, dW);
          if (mn === dN) deaths.N++; else if (mn === dS) deaths.S++;
          else if (mn === dE) deaths.E++; else deaths.W++;
          const md = Math.max(0, (q._minD === undefined ? 9999 : q._minD) - R - q.r);
          near[Math.min(bins - 1, Math.floor(md / 40))]++;
        }
      }
      /* closest approach, tracked on the survivors for the next frame */
      for (const q of m.shots){
        if (q.own !== own) continue;
        const d = Math.hypot(q.x - th.x, q.y - th.y);
        if (q._minD === undefined || d < q._minD) q._minD = d;
      }
      return r;
    };
    let st = 0;
    while (!m.over && st < secs / DT){ m.step(DT); st++; }
  }
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg; if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
    delete x.onHit; delete x.onSelf;
    if (saved[pid].onHit) x.onHit = saved[pid].onHit;
    if (saved[pid].onSelf) x.onSelf = saved[pid].onSelf;
  }
  wallTravel.sort((a, b) => a - b);
  return { n, deaths, near, bins, arena: [A.w, A.h],
           meanTravel: n ? sumTravel / n : 0,
           medTravel: n ? wallTravel[Math.floor(n / 2)] : 0,
           meanLifeUsed: n ? sumLife / n : 0,
           hitTravel: nHit ? hitTravel / nHit : 0, nHit };
}"""

# [6] What each knob on entangle is worth, one at a time, on this body.
KNOB_JS = """([shooter, foes, seeds, secs, pin, pinIds, knobs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === shooter);
  const S = AC.STATUS.entangle;
  const base = { spin: S.spin, move: S.move, maxStacks: S.maxStacks, dur: S.dur };
  const savedOnHit = w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    x.dmg = pin; if (x.ult) x.ult.charge = 1e9;
  }
  const out = [];
  for (const kn of knobs){
    for (const f2 of Object.keys(base)) S[f2] = base[f2];
    delete w.onHit;
    if (kn.per > 0){ w.onHit = { entangle: kn.per }; }
    for (const f2 of Object.keys(kn)) if (f2 !== "per" && f2 !== "label") S[f2] = kn[f2];
    let hp20 = [], ttk = [], stacks = 0, steps = 0, hits = 0, dur = 0;
    for (const f of foes) for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const hp0 = th.hp;
      let st = 0, k20 = -1, ss = 0;
      while (!m.over && st < secs / DT){
        m.step(DT); st++;
        ss += th.stacks("entangle");
        if (k20 < 0 && st * DT >= 20) k20 = hp0 - th.hp;
      }
      if (k20 >= 0) hp20.push(k20);
      if (!th.alive) ttk.push(st * DT);
      stacks += ss; steps += st; hits += me.hits; dur += st * DT;
    }
    out.push({ label: kn.label, per: kn.per,
               spin: S.spin, move: S.move, maxStacks: S.maxStacks, dur: S.dur,
               hp20: hp20.length ? hp20.reduce((a, b) => a + b, 0) / hp20.length : null,
               ttk: ttk.length ? ttk.reduce((a, b) => a + b, 0) / ttk.length : null,
               killed: ttk.length / (foes.length * seeds.length),
               meanStacks: steps ? stacks / steps : 0,
               hps: dur ? hits / dur : 0 });
  }
  for (const f2 of Object.keys(base)) S[f2] = base[f2];
  delete w.onHit; if (savedOnHit) w.onHit = savedOnHit;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg; if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return out;
}"""

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


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
    out.parent.mkdir(parents=True, exist_ok=True)
    sh.save(out)
    print(f"    {out.name}  ({sh.width}x{sh.height})")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-foregone.html")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--hold", type=float, default=2.2)
    ap.add_argument("--steps", type=int, default=900)
    ap.add_argument("--scale", type=float, default=0.42)
    ap.add_argument("--secs", type=float, default=85.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--outdir", default="../05-reference/v40")
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    gp = (HERE / A.game).resolve()
    if not gp.exists():
        sys.exit(f"no such build: {gp}")
    outdir = (HERE / A.outdir).resolve()
    seeds = [101 + 7 * i for i in range(A.seeds)]
    out = {}

    # Foils. The two the school already owns are both mirrors and both must be
    # looked at; the two on the ends are the extremes of the parry column
    # (v40 §2.2) — a twinblade eats twice the arrows a warhammer does, and
    # nothing in the roster has ever been shown that spread.
    FOILS = [("thornwake", "v Thornwake  (VERDANT scythe — mirror)"),
             ("heartwood", "v Heartwood  (VERDANT greatsword — mirror)"),
             ("widowmaker", "v Widowmaker  (twinblade — eats 12.0% of arrows)"),
             ("grudgebearer", "v Grudgebearer  (warhammer — eats 5.9%)")]

    with game(game_path=gp) as (page, errors):
        print(f"\n{page.evaluate(INJECT_JS, PROVISIONAL)} — provisional cell injected\n")
        pin_ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")

        # ------------------------------------------------------------ [1] --
        print("[1] THE DRAW BRANCH — palette held, only p.key varies\n")
        br = page.evaluate(BRANCH_JS, ["verdant", PROVISIONAL["reach"],
                                       PROVISIONAL["artW"]])
        print(f"    verdant vs a nonsense key: {br['diff']:.1%} of "
              f"{br['union']} inked pixels differ")
        check("the verdant branch fires — it does not fall through to the bare recurve",
              br["diff"] > 0.05, f"{br['diff']:.1%} differ")
        check("the render is deterministic",
              br["rerun"] == 0, f"{br['rerun']} pixels moved on a rerun")

        # ------------------------------------------------------------ [2] --
        print("\n[2] DOES IT FIGHT — provisional dmg, provisional ult, real everything else\n")
        fights = page.evaluate(FIGHT_JS, [PROVISIONAL["id"],
                                          [f for f, _ in FOILS], seeds[:4]])
        print(f"    {'foe':<16}{'dur':>8}{'over':>7}{'dealt':>8}{'win':>7}"
              f"{'hits':>7}{'shots':>8}")
        ok_fight = True
        for r in fights:
            bad = r["over"] < 1.0 or r["dealt"] < 40
            ok_fight &= not bad
            print(f"    {r['foe']:<16}{r['dur']:>7.1f}s{r['over']:>7.0%}"
                  f"{r['dealt']:>8.0f}{r['win']:>7.0%}{r['hits']:>7.1f}"
                  f"{r['shots']:>8.0f}" + ("   <-- FAIL" if bad else ""))
        check("it fights — every matchup resolves and lands real damage", ok_fight,
              f"{len(fights)} foes x {len(seeds[:4])} seeds")

        # ------------------------------------------------------------ [4] --
        print(f"\n[4] WHAT VERDANT'S OWN GRAMMAR IS WORTH HERE. Both verdant ultimates "
              f"are\n    kind:\"freeze\", and freeze is `foe.stun = max(stun, u.freeze)`. "
              f"A stunned\n    fighter has NO blade segments, so a root is already the "
              f"strongest thing a\n    verdant relic can do to the ranged path. Held "
              f"open, not applied:\n")
        roots = page.evaluate(ROOT_JS, [PROVISIONAL["id"],
                                        [f for f, _ in FOILS], seeds, A.secs,
                                        A.pin, pin_ids,
                                        ["free", "rooted", "planted"]])
        out["root"] = roots
        print(f"    {'the foe is':<12}{'fired':>8}{'landed':>8}{'parried':>9}"
              f"{'wall':>7}{'melee/s':>9}{'arrow dmg':>11}{'sep':>7}")
        for r in roots:
            tot = max(1e-9, r["dmgShot"] + r["dmgMelee"])
            lab = {"free": "free", "rooted": "ROOTED",
                   "planted": "planted*"}[r["mode"]]
            print(f"    {lab:<12}{r['fired']:>8}{r['hitRate']:>8.1%}"
                  f"{r['parryRate']:>9.1%}{r['wallRate']:>7.1%}"
                  f"{r['melee']/max(1e-9,r['secs']):>9.3f}"
                  f"{r['dmgShot']/tot:>11.0%}{r['sep']:>7.0f}")
        print(f"    * planted is not a mechanic — the foe's velocity is zeroed but its "
              f"weapon runs.\n      It is the control that separates \"cannot parry\" "
              f"from \"is standing still\".")
        free = next(r for r in roots if r["mode"] == "free")
        root = next(r for r in roots if r["mode"] == "rooted")
        plant = next(r for r in roots if r["mode"] == "planted")
        print(f"\n    A PERMANENT root — far more than any ultimate could buy — moves "
              f"the landed\n    rate {free['hitRate']:.1%} -> {root['hitRate']:.1%} "
              f"({root['hitRate']-free['hitRate']:+.1%}). Standing the foe still without "
              f"disarming it\n    moves it {plant['hitRate']-free['hitRate']:+.1%}. "
              f"The wall keeps "
              f"{root['wallRate']:.0%} of the arrows either way.")
        check("the root instrument works — a permanently rooted foe parries "
              "essentially nothing",
              root["parryRate"] < 0.01,
              f"parry {free['parryRate']:.1%} free -> {root['parryRate']:.1%} rooted")
        check("and the arrows it stops still do not reach the foe — the wall, not the "
              "parry, is what a bow is fighting",
              (root["hitRate"] - free["hitRate"]) < (free["parryRate"] * 0.6),
              f"parry gave up {free['parryRate']:.1%} and landed gained only "
              f"{root['hitRate']-free['hitRate']:+.1%}")

        # ------------------------------------------------------------ [5] --
        print(f"\n[5] THE WALL, MAPPED — where the 82% actually end\n")
        wl = page.evaluate(WALL_JS, [PROVISIONAL["id"], [f for f, _ in FOILS],
                                     seeds, A.secs, A.pin, pin_ids])
        out["wall"] = wl
        aw, ah = wl["arena"]
        d = wl["deaths"]
        tot = max(1, sum(d.values()))
        print(f"    arena {aw}x{ah}.  {wl['n']} arrows died on a wall.")
        print(f"      N (ceiling) {d['N']/tot:>6.1%}    S (floor) {d['S']/tot:>6.1%}"
              f"    E {d['E']/tot:>6.1%}    W {d['W']/tot:>6.1%}")
        print(f"      travelled {wl['meanTravel']:.0f} on average "
              f"(median {wl['medTravel']:.0f}) and used "
              f"{wl['meanLifeUsed']:.0%} of a 3.4s life")
        print(f"      an arrow that LANDS travelled {wl['hitTravel']:.0f}")
        print(f"\n    how close a wall-bound arrow ever came to the shell, "
              f"in 40-unit bins:\n")
        nb = wl["near"]
        mx = max(1, max(nb))
        for i, v in enumerate(nb):
            lo = i * 40
            lab = f"{lo}-{lo+40}" if i < len(nb) - 1 else f"{lo}+"
            bar = "#" * int(round(38 * v / mx))
            print(f"      {lab:>9}  {v/max(1,wl['n']):>6.1%}  {bar}")
        within80 = sum(nb[:2]) / max(1, wl["n"])
        print(f"\n      {within80:.1%} of wasted arrows passed within 80 units of the "
              f"shell.")
        check("the near-miss histogram is not degenerate — the misses are spread, "
              "so 'nearly hit' is a real population and not an artefact",
              0.02 < within80 < 0.60,
              f"{within80:.1%} within 80 units of {wl['n']} wall deaths")

        # ------------------------------------------------------------ [6] --
        print(f"\n[6] THE KNOBS ENTANGLE HAS. Farwarden carries ward:2.5 because the "
              f"constant was\n    authored on a greatsword and a bow deals a third as "
              f"much a blow — that is the\n    precedent for a per-relic value. "
              f"One knob at a time, everything else stock:\n")
        S0 = page.evaluate("() => ({...AC.STATUS.entangle})")
        knobs = [
            {"label": "none (control)", "per": 0},
            {"label": "stock verdant", "per": 2},
            {"label": "per-relic 4", "per": 4},
            {"label": "maxStacks 8", "per": 2, "maxStacks": 8},
            {"label": "dur 2.8 -> 6.0", "per": 2, "dur": 6.0},
            {"label": "spin -13% -> -26%", "per": 2, "spin": -0.26},
            {"label": "move -6% -> -20%", "per": 2, "move": -0.20},
            {"label": "everything at once", "per": 4, "maxStacks": 8, "dur": 6.0,
             "spin": -0.26, "move": -0.20},
        ]
        kn = page.evaluate(KNOB_JS, [PROVISIONAL["id"], [f for f, _ in FOILS],
                                     seeds, A.secs, A.pin, pin_ids, knobs])
        out["knobs"] = kn
        base = kn[0]
        print(f"    {'knob':<22}{'per':>5}{'stk':>5}{'dur':>6}{'spin':>7}{'move':>7}"
              f"{'mean':>7}{'hp@20s':>9}{'net':>7}{'ttk':>7}")
        for r in kn:
            netv = (r["hp20"] or 0) - (base["hp20"] or 0)
            ttkT = f"{r['ttk']:.0f}s" if r["ttk"] else "—"
            print(f"    {r['label']:<22}{r['per']:>5}{r['maxStacks']:>5}"
                  f"{r['dur']:>6.1f}{r['spin']:>7.2f}{r['move']:>7.2f}"
                  f"{r['meanStacks']:>7.2f}{(r['hp20'] or 0):>9.0f}"
                  f"{netv:>+7.0f}{ttkT:>7}")
        allin = kn[-1]
        print(f"\n    Everything at once — double the per-hit value, double the cap, "
              f"double the\n    duration, double the slow on both axes — buys "
              f"{(allin['hp20'] or 0) - (base['hp20'] or 0):+.0f} hp over "
              f"twenty seconds.")
        check("the entangle knobs were restored",
              page.evaluate("() => JSON.stringify({...AC.STATUS.entangle})")
              == json.dumps(S0).replace(", ", ",").replace('": ', '":')
              or page.evaluate(
                  "(s) => AC.STATUS.entangle.spin === s.spin && "
                  "AC.STATUS.entangle.move === s.move && "
                  "AC.STATUS.entangle.maxStacks === s.maxStacks && "
                  "AC.STATUS.entangle.dur === s.dur", S0),
              "STATUS.entangle back to spin/move/maxStacks/dur as found")

        # ------------------------------------------------------------ [3] --
        print(f"\n[3] THE LOOK — cards and arena stills, {A.steps} steps in\n")
        cards, arenas, labels = [], [], []
        for fid, lab in FOILS:
            cards.append(png(page.evaluate(CARD_JS,
                                           [PROVISIONAL["id"], fid, A.seed, A.hold])))
            arenas.append(png(page.evaluate(ARENA_JS,
                                            [PROVISIONAL["id"], fid, A.seed,
                                             A.steps, True])))
            labels.append(lab)
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    c = contact(cards, labels, outdir / "verdant-bow-cards.png", A.scale,
                f"PROVISIONAL VERDANT BOW — fight card, {A.hold}s into the intro")
    ar = contact(arenas, labels, outdir / "verdant-bow-arena.png", A.scale,
                 f"PROVISIONAL VERDANT BOW — mid-fight, {A.steps} steps, seed {A.seed}")
    print(f"\n    The first two are the MIRROR. v28: same-affinity pairs read as one "
          f"smudge,\n    and palette separation between two verdant relics is zero by "
          f"construction —\n    the bow's 179px art against a 348px scythe and a 268px "
          f"greatsword is the only\n    thing carrying it. That is a judgement and it "
          f"is Rick's, not this file's.")

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"   ({len(bad)} FAILED: {'; '.join(bad)})" if bad else ""))
    print("nothing was written to any build")
    out["sheets"] = {"cards": str(c), "arena": str(ar)}
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1, default=str))
        print(f"wrote {A.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
