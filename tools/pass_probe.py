#!/usr/bin/env python3
"""THE PASS AND THE TEAR, ASSERTED AGAINST THE BUILD. Brief v57 §5a, STAGE 2.

    python pass_probe.py --game ../02-chain/sc-thepass.html

This is the stage gate, and it is the only part of the CINDERCLEAVE design
that can be falsified before a single beam is drawn.

`06-docs/v57/cindercleave-design-v57.md` §3.2 published a distribution BEFORE
the build existed -- 2,780 passes measured in `vent_size_lab.py`, median 0.63
of the blade, sd 0.32, and 27.4% of passes burying it past 0.9. Rick's size
mechanic is built on that spread being real:

    "can we come up with a way for the size of the vents to vary? so a graze
     to the wall makes a small one but a full slash makes a larger one?"

If the built pass does not reproduce it, "graze" is a word for a thing the
hall never does, `k` is a knob with no range on it, and everything downstream
-- the size, the count, the blade -- is being tuned against a lab that does
not describe the game. THE ANSWER THEN IS TO STOP, NOT TO RETUNE.

  [1] A PASS RESOLVES ONCE. No pass object is ever sampled again after it has
      torn, and a wall change closes one and opens another.
  [2] ONE PASS IS ONE VENT. Counted off the engine's own objects rather than
      recomputed -- `gravemourn_relic_probe`'s lesson: a probe that encodes
      its own model of a rule fails on every legitimate change to it.
  [3] HOW MANY A FIGHT, reported against the lab's 10.7 and NOT gated -- see
      the note in [3]'s output.
  [4] THE DEPTH DISTRIBUTION. **THIS IS THE STAGE GATE.**
  [5] `pen01` IS NORMALISED BY REACH, asserted twice: algebraically against
      the `k` every vent actually got, and empirically by moving `reachMul`.
  [6] A VENT RIDES THE COLLAPSE. On the wall at t=0 and still on the wall
      with the inset at its maximum -- v40 §3.3, and the reason a vent is
      stored as {wall, u}.
  [7] THE BEARING IS NEVER ALONG THE WALL IT WAS TORN FROM, over every vent,
      and all eight compass bearings appear across the four walls.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"\n        {detail}" if detail else ""))


# THE HARNESS. Everything is stepped inside one page evaluate: 260 fights at
# 120Hz is 1.5M steps and a per-step round trip from Python would take hours.
# What comes back is EVENTS, not summaries, so every check below is computed
# here and can be recomputed differently without re-running the sim.
JS = r"""(cfg) => {
  const M = AC.Match.prototype;
  const dt = AC.CONFIG.physics.dt;
  const A = AC.CONFIG.arena;
  const out = { pen: [], k: [], tears: 0, opens: 0, reopen: 0, doubleTear: 0,
                walls: {}, dirs: {}, along: 0, fights: 0, casts: 0, orphan: 0,
                ride: { ok: 0, bad: 0, worst: 0 }, err: null };
  const origTear = M.tearVent;
  try {
    for (const foe of cfg.foes){
      for (const sd of cfg.seeds){
        const m = new AC.Match(cfg.relic, foe, sd);
        out.fights++;
        let seq = 0;
        /* THE RESOLUTION, off the engine's own call rather than reconstructed.
           `P` is the very object the tick has been accumulating into, so
           `maxPen` is what the mechanic used and not what this probe thinks it
           should have been. */
        m.tearVent = function (f, P) {
          const before = f.ultBreach ? f.ultBreach.tears : -1;
          const nv = m.vents.length;
          origTear.call(m, f, P);
          const after = f.ultBreach ? f.ultBreach.tears : -1;
          if (after <= before) return;              // the licence refused it
          if (P.__torn) out.doubleTear++;
          P.__torn = true;
          out.tears++;
          const reach = f.w.reach * f.reachMul;
          const pen01 = Math.max(0, Math.min(1, P.maxPen / reach));
          out.pen.push(pen01);
          const v = m.vents[m.vents.length - 1];
          out.k.push(v.k);
          out.walls[v.wall] = (out.walls[v.wall] || 0) + 1;
          const key = v.ax.toFixed(2) + "," + v.ay.toFixed(2);
          out.dirs[key] = (out.dirs[key] || 0) + 1;
          /* RICK'S RULE, and it is the one thing about the bearing that is not
             free: a hole must never fire along the wall it was torn from. */
          if (v.ax * v.nx + v.ay * v.ny <= 0.01) out.along++;
        };
        for (let i = 0; i < cfg.steps; i++){
          /* THE ONE PASS THAT NEVER GETS TO RESOLVE, and it is the engine's
             rule rather than a defect: `step()` returns from its `over` branch
             before `tickBreach` is reached, so a cut in progress on the frame
             the fight ends is simply never finished. There is nothing left to
             tear into. Held from BEFORE the step so it can be identified after
             the one that ended the match. */
          const held = [m.a.ultBreach && m.a.ultBreach.pass,
                        m.b.ultBreach && m.b.ultBreach.pass];
          m.step(dt);
          if (m.over){
            for (const P of held) if (P && !P.__torn) out.orphan++;
            break;
          }
          /* THE OPENS, sampled off the object the tick keeps. A pass cannot
             open and resolve inside one step -- `dwell` is dt on the frame it
             is created and `passMax` is 1.2 -- so every one of them is seen. */
          for (const f of [m.a, m.b]){
            const V = f.ultBreach, P = V && V.pass;
            if (!P) continue;
            if (P.__torn) out.reopen++;             // [1]: a corpse walking
            if (!P.__id){ P.__id = ++seq; out.opens++; }
          }
          /* [6] THE COLLAPSE. Every live vent, every step: it has to be ON the
             current wall plane, not on the one it was torn from. */
          if (m.vents.length && (i % 37) === 0){
            const n = m.inset;
            for (const v of m.vents){
              const d = v.wall === "W" ? Math.abs(v.x - n)
                      : v.wall === "E" ? Math.abs(v.x - (A.w - n))
                      : v.wall === "N" ? Math.abs(v.y - n)
                      :                  Math.abs(v.y - (A.h - n));
              if (d > 0.51){ out.ride.bad++; out.ride.worst = Math.max(out.ride.worst, d); }
              else out.ride.ok++;
            }
          }
        }
        out.casts += m.a.ultsFired;
        m.tearVent = origTear;
      }
    }
  } catch (e){ out.err = String(e) + " | " + String(e.stack).slice(0, 400); }
  return out;
}"""

# AND THE SAME RUN WITH `reachMul` MOVED. `f.reachMul` is Revenant's window
# multiplier and it is a real field on every fighter; forcing it high makes the
# blade physically longer, which makes `maxPen` larger in PIXELS. If `pen01`
# is normalised the distribution does not move. If it is not, it piles up
# against the clamp.
REACH_PATCH = r"""(cfg) => {
  window.__reachMul = cfg.mul;
  const M = AC.Match.prototype;
  if (!M.__origStep2) M.__origStep2 = M.step;
  M.step = function (dt) {
    for (const f of [this.a, this.b])
      if (f.w.id === cfg.relic) f.reachMul = window.__reachMul;
    return M.__origStep2.call(this, dt);
  };
  return true;
}"""


def hist(xs, bins=10):
    out = [0] * bins
    for x in xs:
        out[min(bins - 1, max(0, int(x * bins)))] += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-thepass.html")
    ap.add_argument("--relic", default="cindercleave")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [2207 + 11 * i for i in range(a.seeds)]

    print(f"\nTHE PASS AND THE TEAR — {gp.name}")
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if a.relic not in ids:
            raise SystemExit(f"{a.relic} is not in this build")
        foes = [i for i in ids if i != a.relic]
        cfg = {"relic": a.relic, "foes": foes, "seeds": seeds,
               "steps": int(a.secs * 120)}
        print(f"  {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes) * len(seeds)} fights\n")
        r = page.evaluate(JS, cfg)
        if r["err"]:
            raise SystemExit("the sim threw: " + r["err"])
        page.evaluate(REACH_PATCH, {"mul": 1.45, "relic": a.relic})
        r2 = page.evaluate(JS, cfg)
        if r2["err"]:
            raise SystemExit("the reachMul arm threw: " + r2["err"])
        assert not errors, errors

    pen, ks = r["pen"], r["k"]
    n_f = r["fights"]

    print(f"[1] A PASS RESOLVES ONCE")
    check("no pass is torn twice, and none is sampled again after it tore",
          r["doubleTear"] == 0 and r["reopen"] == 0,
          f"{r['doubleTear']} double tears, {r['reopen']} zombie samples "
          f"over {r['opens']} passes")

    print(f"\n[2] ONE PASS IS ONE VENT")
    check("every pass that opened resolved into exactly one vent",
          r["opens"] == r["tears"] + r["orphan"],
          f"{r['opens']} passes opened, {r['tears']} vents torn, "
          f"{r['orphan']} still in the blade when the fight ended\n"
          f"        ({abs(r['opens'] - r['tears'] - r['orphan'])} unaccounted "
          f"for)")
    print(f"        The orphans are the ENGINE'S rule and not a defect: "
          f"`step()` returns\n        from its `over` branch before "
          f"`tickBreach` is reached, so a cut in\n        progress on the "
          f"frame the fight ends is never finished — and there is\n"
          f"        nothing left to tear into. "
          f"{r['orphan'] / max(1, n_f):.2f} a fight.")

    print(f"\n[3] HOW MANY A FIGHT")
    print(f"        {r['tears'] / n_f:.1f} passes a fight over {n_f} fights, "
          f"{r['casts'] / n_f:.2f} casts a fight,\n"
          f"        {r['tears'] / max(1, r['casts']):.2f} a cast")
    print(f"        NOT GATED. The lab's 10.7 is an EIGHT-SECOND CLOCK at "
          f"blade 31.35;\n        this stage runs the 14s cap with no count "
          f"behind it, so more passes\n        here is the window being longer "
          f"and not the mechanic disagreeing.")

    print(f"\n[4] THE DEPTH DISTRIBUTION — THE STAGE GATE")
    print(f"        how much of the blade went in, as a fraction of reach\n")
    h = hist(pen)
    for i, c in enumerate(h):
        print(f"        {i/10:.1f}-{(i+1)/10:.1f}  "
              f"{'#' * int(round(c / max(1, max(h)) * 30)):<30}"
              f"{c / max(1, len(pen)):>6.1%}")
    med = statistics.median(pen)
    sd = statistics.pstdev(pen)
    hi = sum(1 for x in pen if x > 0.9) / max(1, len(pen))
    q = statistics.quantiles(pen, n=4)
    print(f"\n        median {med:.2f}   quartiles {q[0]:.2f} / {q[1]:.2f} / "
          f"{q[2]:.2f}   sd {sd:.2f}\n"
          f"        design §3.2:  median 0.63, quartiles 0.30 / 0.63 / 0.92, "
          f"sd 0.32, 27.4% > 0.9\n")
    check("median 0.63 ± 0.05", abs(med - 0.63) <= 0.05, f"{med:.3f}")
    check("sd 0.32 ± 0.05", abs(sd - 0.32) <= 0.05, f"{sd:.3f}")
    check("27% ± 4 of passes bury the blade past 0.9",
          abs(hi - 0.274) <= 0.04, f"{hi:.1%}")
    check("the range is real — a quarter of passes are under a third of the "
          "blade", sum(1 for x in pen if x < 0.30) / max(1, len(pen)) > 0.15,
          f"{sum(1 for x in pen if x < 0.30) / max(1, len(pen)):.1%} under 0.30")

    print(f"\n[5] `pen01` IS NORMALISED BY REACH")
    # ALGEBRAIC: the k every vent got is exactly lerp(kMin, kMax, pen01) of the
    # pen01 recomputed here from maxPen and the fighter's own reach. This is
    # the assertion; the arm below is the demonstration.
    bad = sum(1 for p, k in zip(pen, ks) if abs((0.5 + p) - k) > 1e-9)
    check("every vent's size is exactly lerp(0.5, 1.5, pen01)", bad == 0,
          f"{bad} of {len(ks)} disagree")
    p2 = r2["pen"]
    m2, s2 = statistics.median(p2), statistics.pstdev(p2)
    check("moving reachMul to 1.45 does not move the distribution",
          abs(m2 - med) <= 0.06 and abs(s2 - sd) <= 0.05,
          f"median {med:.3f} -> {m2:.3f}, sd {sd:.3f} -> {s2:.3f} "
          f"over {len(p2)} passes")

    print(f"\n[6] A VENT RIDES THE COLLAPSE")
    check("every live vent is on its own wall's CURRENT plane",
          r["ride"]["bad"] == 0,
          f"{r['ride']['ok']} samples on the plane, {r['ride']['bad']} off it"
          + (f", worst {r['ride']['worst']:.1f}px" if r["ride"]["bad"] else ""))

    print(f"\n[7] THE BEARING")
    check("no hole ever fires along the wall it was torn from",
          r["along"] == 0, f"{r['along']} of {r['tears']}")
    seen = sorted(r["dirs"].items(), key=lambda kv: -kv[1])
    print("        " + "   ".join(f"({k}) {v}" for k, v in seen))
    check("all eight compass bearings appear across the four walls",
          len(r["dirs"]) == 8, f"{len(r['dirs'])} distinct bearings")
    print(f"        walls: " + "  ".join(f"{k} {v}" for k, v in
                                         sorted(r["walls"].items())))

    ok = sum(1 for _, v in PASS if v)
    print(f"\n{ok}/{len(PASS)} checks passed")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"median": med, "sd": sd, "above09": hi,
             "passes": len(pen), "fights": n_f,
             "hist": h, "dirs": r["dirs"], "walls": r["walls"]}, indent=1))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
