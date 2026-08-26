#!/usr/bin/env python3
"""LOOK AT EVERY OPEN CELL BEFORE CHOOSING ONE.

    python3 cell_survey.py --game ../02-chain/sc-redflail.html

v38 ran `flail_probe` on ONE cell after the cell had been chosen, and the
probe turned up two things that would have changed the pricing if they had
been known a step earlier: the art already existed, and the school's status
could not survive on the type. This is that probe generalised to the whole
grid, run BEFORE the choice, so the choice is priced.

It designs nothing and proposes nothing. Seven schools x six types is 42
cells; twenty are filled. What follows is what is measurably true about the
other twenty-two.

  [1] THE GRID. Read from AC.WEAPONS in the build, not from a copy of it in
      a document -- three docs already quote a roster table that has drifted.

  [2] THE CHANNELS. Every school's onHit/onSelf channel and the CLOCK on it,
      plus any status in the table that nobody applies. v38 found the clock,
      not the chain, was what thinned hemorrhage on the flail; the clock is a
      property of the SCHOOL and the contact rate a property of the TYPE, so
      the product is a property of the CELL and can be read off ahead of time.

  [3] THE ART, AND WHETHER IT IS REAL. Every shape dispatches on `p.key` and
      carries a branch per school, so on paper every open cell has art. v38
      found the flail's was genuinely different per school where the weapon
      matrix had scored it IoU 1.000 and called it "the flattest cell in the
      game" -- because the matrix measured the OUTER SILHOUETTE, and the
      difference between a bitten crescent and seven hooked barbs is interior.
      Measured here on the INK MASK at 6x, alpha over a transparent canvas so
      no palette can hide a stroke by matching the background.
      Negative control: a nonsense affinity key must fall to the base branch.

  [4] THE CLOCK ON THE TYPE. For each open cell, time-weighted stack occupancy
      of the school's own status carried by the type's own physics, damage
      pinned across every relic in the comparison and ultimates suppressed --
      both corrections v38 had to make before its numbers meant anything.
      Injection is runtime-only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import pathlib
import statistics
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- [1] grid --

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape,
    reach: w.reach, artW: w.artW, dmg: w.dmg, mode: w.mode, mass: w.mass,
    onHit: w.onHit ? Object.entries(w.onHit)[0] : null,
    onSelf: w.onSelf ? Object.entries(w.onSelf)[0] : null,
    ult: w.ult ? { name: w.ult.name, kind: w.ult.kind, charge: w.ult.charge } : null,
  }));
  const S = {};
  for (const [k, v] of Object.entries(AC.STATUS))
    S[k] = { maxStacks: v.maxStacks, dur: v.dur, tip: v.tip || "" };
  return { weapons: W, status: S, affinities: Object.keys(AC.AFFINITIES),
           shapeFns: Object.keys(AC.SHAPES).filter(n => typeof AC.SHAPES[n] === "function") };
}"""

# ------------------------------------------------------- [3] art dispatch ---
# Every candidate branch is wrapped and the render is run; whichever names
# appear in `fired` are the ones that actually drew. Asking the source which
# branch "should" fire is how the Harrowing shipped as twelve small arrows.

BRANCH_JS = """([shape, palKey, D, artW]) => {
  const names = Object.keys(AC.SHAPES).filter(n => typeof AC.SHAPES[n] === "function");
  const fired = [], orig = {};
  for (const n of names){
    orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this, a); };
  }
  const cv = document.createElement("canvas");
  cv.width = 600; cv.height = 600;
  const c = cv.getContext("2d");
  c.translate(300, 300);
  const pal = palKey === null
    ? { key:"NOT_A_SCHOOL", core:"#888888", glow:"#aaaaaa", dark:"#222222",
        steel:"#cccccc", ink:"#111111", trail:"#999999" }
    : AC.AFFINITIES[palKey];
  let error = null;
  try {
    if (shape === "flail") AC.SHAPES.flailHead(c, artW, pal, 0.7);
    else AC.SHAPES[shape](c, D, artW, pal, 0.55);
  } catch (e) { error = String(e); }
  for (const n of Object.keys(orig)) AC.SHAPES[n] = orig[n];
  return { fired, error };
}"""

# ----------------------------------------------------------- [3] ink masks --
# TRANSPARENT canvas. A near-white barb on a dark plate and a dark rivet on a
# pale one are both ink; the only background-independent question is whether
# the pixel was painted at all, which is exactly what alpha answers.

# One call per shape. The first cut returned the pixel arrays and compared
# them in Python -- a quarter of a million ints per render, nine renders a
# shape, over CDP. The comparison is a loop over two arrays; it belongs where
# the arrays already are.
INK_JS = """([shape, keys, D, artW, zoom, S, cx]) => {
  const draw = (palKey) => {
    const cv = document.createElement("canvas");
    cv.width = S * zoom; cv.height = S * zoom;
    const c = cv.getContext("2d");
    c.scale(zoom, zoom);
    c.translate(S * cx, S / 2);
    /* ONE palette, N keys. AFFINITIES.dwarven supplies every field so no
       branch can trip over one this probe forgot to fake; `key` is the only
       thing that varies, so it is the only thing a difference can be. */
    const pal = Object.assign({}, AC.AFFINITIES.dwarven,
                              { key: palKey === null ? "NOT_A_SCHOOL" : palKey });
    if (shape === "flail") AC.SHAPES.flailHead(c, artW, pal, 0.7);
    else AC.SHAPES[shape](c, D, artW, pal, 0.55);
    const d = c.getImageData(0, 0, cv.width, cv.height).data;
    const n = cv.width * cv.height;
    const px = new Int32Array(n);
    let x0 = cv.width, y0 = cv.height, x1 = -1, y1 = -1, ink = 0;
    for (let p = 0; p < n; p++){
      const i = p << 2;
      if (d[i+3] > 24){
        px[p] = 1 + ((d[i] << 16) | (d[i+1] << 8) | d[i+2]);
        ink++;
        const yy = (p / cv.width) | 0, xx = p % cv.width;
        if (xx < x0) x0 = xx; if (xx > x1) x1 = xx;
        if (yy < y0) y0 = yy; if (yy > y1) y1 = yy;
      }
    }
    return { px, ink, box: [x0, y0, x1, y1], w: cv.width, h: cv.height };
  };

  const shots = {};
  for (const k of keys) shots[k === null ? "NEG" : k] = draw(k);
  const rerun = draw(keys.find(k => k !== null));

  const cmp = (A, B) => {
    let union = 0, differ = 0, inter = 0;
    const a = A.px, b = B.px, n = a.length;
    for (let p = 0; p < n; p++){
      const x = a[p], y = b[p];
      if (x || y){ union++; if (x !== y) differ++; if (x && y) inter++; }
    }
    return { diff: union ? differ / union : 0, iou: union ? inter / union : 1 };
  };

  const names = keys.map(k => k === null ? "NEG" : k);
  const M = {};
  for (let i = 0; i < names.length; i++)
    for (let j = i + 1; j < names.length; j++)
      M[names[i] + "|" + names[j]] = cmp(shots[names[i]], shots[names[j]]);
  const first = names.find(n => n !== "NEG");
  const boxes = {}, inks = {};
  for (const n of names){ boxes[n] = shots[n].box; inks[n] = shots[n].ink; }
  return { m: M, rerun: cmp(shots[first], rerun).diff, boxes, inks,
           w: shots[first].w, h: shots[first].h };
}"""

# ------------------------------------------------------------ [4] the clock --
# BLEED_JS, from flail_probe, with the donor's channel swapped so one type's
# physics can carry another school's status. `pin` and `noult` are not
# optional: a harder-hitting relic ends the fight sooner and therefore has
# fewer seconds in which to stack, and four of the twenty ultimates are worth
# more contact than the weapon is.

CLOCK_JS = """([donor, aff, key, per, foes, seeds, pin, pinIds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const savedW = JSON.parse(JSON.stringify({ aff: w.aff, onHit: w.onHit || null,
                                             onSelf: w.onSelf || null }));
  w.aff = aff;
  delete w.onSelf;
  w.onHit = {}; w.onHit[key] = per;

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
      const m = new AC.Match(donor, f, s);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let steps = 0, sum = 0, ge2 = 0, geMax = 0, apps = 0, refresh = 0, prevT = 0;
      const cap = AC.STATUS[key].maxStacks;
      while (!m.over && steps < secs / DT){
        m.step(DT); steps++;
        const st = th.status[key];
        const t = st ? st.t : 0;
        const n = st ? st.stacks : 0;
        if (t > prevT + 1e-9){ apps++; if (prevT > 0) refresh++; }
        prevT = t;
        sum += n;
        if (n >= 2) ge2++;
        if (n >= cap) geMax++;
      }
      rows.push({ foe: f, seed: s, steps, dur: steps * DT, hits: me.hits,
                  meanStacks: steps ? sum / steps : 0,
                  p2: steps ? ge2 / steps : 0, pMax: steps ? geMax / steps : 0,
                  apps, refresh });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid]; x.ult.charge = savedUlt[pid];
  }
  return rows;
}"""

SHAPE_FN = {"flail": "flailHead"}


def iou(x, y):
    """Coverage agreement. Sees added geometry; blind to interior ornament."""
    inter = sum(1 for p, q in zip(x, y) if p and q)
    union = sum(1 for p, q in zip(x, y) if p or q)
    return inter / union if union else 1.0


def diff(x, y):
    """Share of DRAWN pixels that disagree, over the union of the two inks.

    On a held palette this is dispatch: a pixel differs because a branch put
    something else there. Interior ornament and added geometry both land in
    it, which is the whole reason it exists.
    """
    union = sum(1 for p, q in zip(x, y) if p or q)
    if not union:
        return 0.0
    return sum(1 for p, q in zip(x, y) if p != q) / union


PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-redflail.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--foes", type=int, default=4)
    ap.add_argument("--only", default="")
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--zoom", type=int, default=6)
    ap.add_argument("--skip-clock", action="store_true")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    out = {}

    with game(game_path=gp) as (page, errors):
        # ------------------------------------------------------------ [1] --
        g = page.evaluate(GRID_JS)
        W, ST = g["weapons"], g["status"]
        schools = sorted({w["aff"] for w in W})
        shapes = sorted({w["shape"] for w in W})
        filled = {(w["aff"], w["shape"]): w["name"] for w in W}
        # A school in AFFINITIES with no relic would never appear above.
        schools = sorted(set(schools) | set(g["affinities"]))
        open_cells = [(s, t) for s in schools for t in shapes if (s, t) not in filled]

        print(f"\n[1] THE GRID — {len(W)} relics, {len(schools)}x{len(shapes)} "
              f"= {len(schools)*len(shapes)} cells, {len(open_cells)} open\n")
        hdr = "".join(f"{t[:10]:>12}" for t in shapes)
        print(f"    {'':<12}{hdr}    school")
        for s in schools:
            row = "".join(f"{filled.get((s,t),'·')[:11]:>12}" for t in shapes)
            n = sum(1 for t in shapes if (s, t) in filled)
            print(f"    {s:<12}{row}    {n}/{len(shapes)}")
        print(f"    {'type':<12}" + "".join(
            f"{sum(1 for s in schools if (s,t) in filled):>12}" for t in shapes))

        check("every relic's shape has a SHAPES function",
              all(w["shape"] in g["shapeFns"] or SHAPE_FN.get(w["shape"], "") in g["shapeFns"]
                  for w in W),
              f"{len(shapes)} shapes")
        check("no duplicate cell",
              len(filled) == len(W),
              f"{len(filled)} distinct cells for {len(W)} relics")

        # ------------------------------------------------------------ [2] --
        print("\n[2] THE CHANNELS — what each school applies, and its clock\n")
        chan = {}
        for s in schools:
            rel = [w for w in W if w["aff"] == s]
            hits = {tuple(w["onHit"]) for w in rel if w["onHit"]}
            selfs = {tuple(w["onSelf"]) for w in rel if w["onSelf"]}
            chan[s] = {"onHit": sorted(hits), "onSelf": sorted(selfs), "n": len(rel)}
        print(f"    {'school':<12}{'relics':>7}  {'channel':<22}{'stacks':>7}{'dur':>8}"
              f"  {'note':<34}")
        for s in schools:
            c = chan[s]
            if c["onHit"]:
                k, per = c["onHit"][0]
                st = ST[k]
                note = "shared with " + ", ".join(
                    o for o in schools if o != s and chan[o]["onHit"]
                    and chan[o]["onHit"][0][0] == k) if any(
                    o != s and chan[o]["onHit"] and chan[o]["onHit"][0][0] == k
                    for o in schools) else ""
                extra = f" (+{len(c['onHit'])-1} more)" if len(c["onHit"]) > 1 else ""
                print(f"    {s:<12}{c['n']:>7}  {f'onHit {k}:{per}'+extra:<22}"
                      f"{st['maxStacks']:>7}{st['dur']:>8.1f}  {note:<34}")
            elif c["onSelf"]:
                k, per = c["onSelf"][0]
                st = ST[k]
                print(f"    {s:<12}{c['n']:>7}  {f'onSelf {k}:{per}':<22}"
                      f"{st['maxStacks']:>7}{st['dur']:>8.1f}  {'NO onHit channel':<34}")
            else:
                print(f"    {s:<12}{c['n']:>7}  {'—':<22}")
        applied = {k for s in schools for (k, _) in chan[s]["onHit"] + chan[s]["onSelf"]}
        # An ultimate can apply a status without any weapon carrying it.
        ult_applied = page.evaluate(
            "() => { const s=new Set(); for (const w of AC.WEAPONS){ "
            "const u=w.ult||{}; for (const f of ['apply','applySelf']) "
            "if (u[f]) Object.keys(u[f]).forEach(k=>s.add(k)); } return [...s]; }")
        src_txt = gp.read_text()
        code_applied = {k for k in ST
                        if f'apply("{k}"' in src_txt or f"apply('{k}'" in src_txt}
        orphan = sorted(set(ST) - applied - set(ult_applied) - code_applied)
        print(f"\n    statuses in the table: {len(ST)}   by a weapon: {len(applied)}"
              f"   by an ultimate: {len(set(ult_applied) - applied)}"
              f"   by a mechanic only: {len(code_applied - applied - set(ult_applied))}"
              f"  ({', '.join(sorted(code_applied - applied - set(ult_applied))) or '—'})")
        if orphan:
            print(f"    NOBODY APPLIES: {', '.join(orphan)}")
        check("every status in the table has an applier", not orphan,
              ", ".join(orphan) if orphan else "8/8")

        # ------------------------------------------------------------ [3] --
        print("\n[3] THE ART — branches per shape, and whether they differ\n")
        art = {}
        keys = schools + [None]

        def pair(M, x, y):
            return M.get(f"{x}|{y}") or M[f"{y}|{x}"]

        for t in shapes:
            rep = next(w for w in W if w["shape"] == t)
            D, aw = rep["reach"], rep["artW"]
            neg = page.evaluate(BRANCH_JS, [t, None, D, aw])
            assert not neg["error"], (t, neg["error"])
            negset = set(neg["fired"])

            # The canvas is sized by MEASUREMENT, not by `reach`. `_artBox`'s
            # own comment: "reach and artW predict a greatsword's box and lie
            # about a bow's". Grown until no school's ink touches an edge --
            # the first cut of this probe measured a clipped bow.
            S = int(aw * 3.0) if t == "flail" else int(D * 1.6)
            cx, tries = 0.5, 0
            while True:
                r = page.evaluate(INK_JS, [t, keys, D, aw, a.zoom, S, cx])
                bx = list(r["boxes"].values())
                clipped = any(b[0] <= 0 or b[1] <= 0 or b[2] >= r["w"] - 1
                              or b[3] >= r["h"] - 1 for b in bx)
                if not clipped or tries >= 4:
                    break
                if any(b[0] <= 0 for b in bx):
                    cx = min(0.82, cx + 0.13)
                S = int(S * 1.45); tries += 1

            M = r["m"]
            fired_by = {sch: sorted(set(page.evaluate(BRANCH_JS, [t, sch, D, aw])["fired"])
                                    - negset) for sch in schools}
            vsneg = {sch: pair(M, sch, "NEG")["diff"] for sch in schools}
            own = {sch for sch in schools if fired_by[sch] or vsneg[sch] > 0.002}
            flat = sorted(set(schools) - own)
            pairs = [(x, y, pair(M, x, y)["diff"], pair(M, x, y)["iou"])
                     for i, x in enumerate(schools) for y in schools[i + 1:]]
            art[t] = {"fired": fired_by, "flat": flat, "pairs": pairs,
                      "det": r["rerun"], "fit": not clipped, "S": S, "cx": cx,
                      "vsNeg": vsneg, "D": D, "artW": aw,
                      "named": sum(1 for sch in schools if fired_by[sch])}
            mean_d = statistics.mean(d_ for _, _, d_, _ in pairs)
            closest = min(pairs, key=lambda q: q[2])
            print(f"    {t:<11} own art {len(own)}/{len(schools)}"
                  f"  (named {art[t]['named']}, inline {len(own)-art[t]['named']})"
                  f"   pixel diff  mean {mean_d:>5.1%}"
                  f"  min {closest[2]:>5.1%} ({closest[0][:4]}/{closest[1][:4]})"
                  f"   {S}px fit={'y' if not clipped else 'N'}"
                  f" rerun={r['rerun']:.0e}")
            if flat:
                print(f"    {'':<11} NO OWN ART: {', '.join(flat)}")

        check("the render is deterministic — same key twice is the same pixels",
              all(art[t]["det"] < 1e-9 for t in shapes),
              f"max rerun diff {max(art[t]['det'] for t in shapes):.1e}"
              " — every number below is noise otherwise")
        check("no shape is measured clipped",
              all(art[t]["fit"] for t in shapes),
              ", ".join(t for t in shapes if not art[t]["fit"])
              or "every school's ink inside its canvas on all 6")
        check("the comparator is sensitive — a nonsense key draws different "
              "pixels from a real school",
              all(max(art[t]["vsNeg"].values()) > 0.002 for t in shapes),
              "smallest largest-difference over the six: "
              + f"{min(max(art[t]['vsNeg'].values()) for t in shapes):.1%}")
        check("every open cell has its own art on its shape",
              all(s2 not in art[t2]["flat"] for s2, t2 in open_cells),
              "22/22" if all(s2 not in art[t2]["flat"] for s2, t2 in open_cells)
              else ", ".join(f"{s2}x{t2}" for s2, t2 in open_cells
                             if s2 in art[t2]["flat"]))

        print(f"\n    per open cell — how far this school's art is from the "
              f"CLOSEST other school on the same type, palette held\n")
        print(f"    {'cell':<26}{'nearest sibling':<14}{'diff':>7}{'inkIoU':>8}"
              f"   reads as")
        cell_iou = {}
        for s2, t2 in sorted(open_cells, key=lambda c: (c[1], c[0])):
            sibs = [(o, d_, i_) for x, y, d_, i_ in art[t2]["pairs"]
                    for o in ([y] if x == s2 else [x] if y == s2 else [])]
            near = min(sibs, key=lambda q: q[1])
            cell_iou[(s2, t2)] = near[1]
            within = sorted(d_ for _, d_, _ in sibs)
            allp = sorted(d_ for _, _, d_, _ in art[t2]["pairs"])
            rank = sum(1 for v in allp if v < near[1]) + 1
            print(f"    {s2 + ' x ' + t2:<26}{near[0]:<14}{near[1]:>7.1%}"
                  f"{near[2]:>8.3f}   closest pair #{rank} of {len(allp)} "
                  f"on this type")

        # ------------------------------------------------------------ [4] --
        clock = {}
        if not a.skip_clock:
            print(f"\n[4] THE CLOCK ON THE TYPE — measured, dmg pinned {a.pin}, "
                  f"ultimates suppressed\n")
            foes = [w["id"] for w in W][:a.foes]
            pin_ids = [w["id"] for w in W]
            seeds = [101 + 7 * i for i in range(a.seeds)]
            donor_for = {}
            for t in shapes:
                cands = [w for w in W if w["shape"] == t]
                donor_for[t] = cands[0]["id"]
            print(f"    {'cell':<26}{'':<3}{'status':<11}{'hits/s':>8}{'mean':>7}"
                  f"{'>=2':>7}{'cap':>7}{'appl':>7}{'refr':>7}")
            todo = sorted([(s2, t2) for s2 in schools for t2 in shapes],
                          key=lambda c: (c[1], c[0]))
            if a.only:
                todo = [c for c in todo if f"{c[0]}x{c[1]}" in a.only.split(",")]
            for s, t in todo:
                ch = chan[s]["onHit"]
                mark = "  " if (s, t) in filled else "->"
                if not ch:
                    print(f"    {s+' x '+t:<26}{mark:<3}"
                          f"{'— vigil has no onHit channel —':<11}")
                    continue
                k, per = ch[0]
                d = donor_for[t]
                use_foes = [f for f in foes if f != d][:a.foes]
                rows = page.evaluate(CLOCK_JS, [d, s, k, per, use_foes, seeds,
                                                a.pin, pin_ids, a.secs])
                dur = sum(r["dur"] for r in rows)
                hps = sum(r["hits"] for r in rows) / dur
                mean = statistics.mean(r["meanStacks"] for r in rows)
                p2 = statistics.mean(r["p2"] for r in rows)
                pmx = statistics.mean(r["pMax"] for r in rows)
                apps = statistics.mean(r["apps"] for r in rows)
                refr = sum(r["refresh"] for r in rows) / max(1, sum(r["apps"] for r in rows))
                clock[f"{s}x{t}"] = {"open": (s, t) not in filled, "status": k, "per": per, "hps": hps,
                                     "mean": mean, "p2": p2, "pMax": pmx,
                                     "apps": apps, "refr": refr,
                                     "n": len(rows), "dur": dur}
                print(f"    {s+' x '+t:<26}{mark:<3}{k:<11}{hps:>8.3f}"
                      f"{mean:>7.2f}{p2:>7.0%}{pmx:>7.0%}{apps:>7.1f}"
                      f"{refr:>7.0%}"
                      + ("" if (s, t) in filled else "   OPEN"))

        assert not errors, errors[:4]

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED)" if bad else ""))

    out = {"grid": {f"{s}x{t}": filled.get((s, t)) for s in schools for t in shapes},
           "open": [f"{s}x{t}" for s, t in open_cells],
           "channels": chan, "status": ST,
           "artDiff": {f"{s}x{t}": v for (s, t), v in cell_iou.items()},
           "clock": clock}
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
