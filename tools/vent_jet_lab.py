#!/usr/bin/env python3
"""THE JET, NOT THE BAR — what Rick's reference frame costs and what it buys.

    python3 vent_jet_lab.py --game ../02-chain/sc-nightfell.html

Rick sent a reference for the beam: a jet that tapers to nothing at its origin,
swells along its length, and carries a bright crescent FRONT at the head. That
is not a line switching on. It is a thing that travels, and the picture makes a
promise the simulation has to keep -- v40's Thicket finding, verbatim: a strike
with no duration reads as "a hazard you walked into", and Rick caught it on
sight.

So the beam stops being an instantaneous segment and becomes a front that
crosses the hall at a speed. The damage resolves WHEN THE FRONT REACHES YOU,
which is the frame the crescent is on you.

That is a real mechanical change and it costs something: a quarry that leaves
before the front arrives is missed, and the loss grows with distance from the
vent. This prices it.

  [1] SPEED. Instant against 1800 / 1100 / 650 units a second. The hall's
      diagonal is 950, so the slowest arm takes 1.5s to cross it.
  [2] THE TAPER. Rick's jet is narrow at the wall and wide at the head, so
      `half` is not one number any more. Priced as a ramp against the flat
      width the earlier labs used.
  [3] AND WHETHER THE FRONT CAN BE OUTRUN AT ALL, which is the question the
      picture is really asking -- a threat that cannot be dodged is a tax, and
      a threat that can is a thing to watch.

THIS IS A LAB AND NOT A BUILD. Same standing-in as `vent_size_lab`: thornwake
for the unbuilt dwarven scythe, pulled from the foe field, Bramblesnare
replaced, foes keeping their own ultimates, damage through `hurt` scaled by
`dmgTakenMul` and never `resolveHit`. Injection is runtime-only. NOTHING is
written to any build.
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
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


LAB_JS = r"""([donor, foes, seeds, secs, cfg]) => {
  const DT = AC.CONFIG.physics.dt;
  const A  = AC.CONFIG.arena;
  const R  = AC.CONFIG.physics.ballR;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg, ult: w.ult,
                  onHit:  w.onHit  ? JSON.parse(JSON.stringify(w.onHit))  : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "dwarven";
  delete w.onHit; delete w.onSelf; w.onHit = { sunder: 1 };
  w.ult = Object.assign({}, saved.ult, { name: "LAB", kind: "labvent",
                                         charge: cfg.charge, radius: 0 });

  const probe = new AC.Match(donor, foes[0], 1);
  const M = Object.getPrototypeOf(probe);
  const origStep = M.step, origFire = M.fireUlt;

  const hash01 = (a, b) => { let h = (a * 374761393 + b * 668265263) | 0;
    h = (h ^ (h >>> 13)) * 1274126177 | 0; h ^= h >>> 16;
    return ((h >>> 0) % 100000) / 100000; };
  const DIRS = [[1,0],[0,1],[-1,0],[0,-1],
                [0.7071,0.7071],[0.7071,-0.7071],[-0.7071,0.7071],[-0.7071,-0.7071]];
  const lerp = (a, b, t) => a + (b - a) * t;

  M.fireUlt = function (f, foe) {
    if (f.w.id !== donor) return origFire.call(this, f, foe);
    f.ultsFired++;
    f.ultVent = { t: 0, dur: cfg.dur, pass: null };
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: f.x, y: f.y,
                w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
  };

  M.step = function (dt) {
    origStep.call(this, dt);
    if (this.hitStop > 0) return;
    const m = this;
    if (!m._vents) m._vents = [];
    const n = this.inset;

    for (const f of [this.a, this.b]) {
      const V = f.ultVent;
      if (!V) continue;
      V.t += dt;
      const done = V.t >= V.dur || !f.alive;

      /* THE DEEPEST CROSSING THIS FRAME, over every blade. `pen` is measured
         past the wall FACE, and normalised by the weapon's own reach so the
         scalar is "how much of this blade went in", not a number in pixels
         that stops meaning anything the day reach changes. */
      let wall = null, pen = 0, hx = 0, hy = 0;
      if (!done && f.stun <= 0) {
        for (const s of this.bladeSegments(f)) {
          const cand = [["W", n - s.bx, n, s.by], ["E", s.bx - (A.w - n), A.w - n, s.by],
                        ["N", n - s.by, s.bx, n], ["S", s.by - (A.h - n), s.bx, A.h - n]];
          for (const [wl, p, cx, cy] of cand)
            if (p > pen) { pen = p; wall = wl; hx = cx; hy = cy; }
        }
      }

      if (wall) {
        if (!V.pass || V.pass.wall !== wall) {
          if (V.pass) m._closePass(f, V.pass);
          V.pass = { wall, maxPen: 0, dwell: 0, integ: 0, hx, hy };
        }
        const P = V.pass;
        P.dwell += dt; P.integ += pen * dt;
        if (pen > P.maxPen) { P.maxPen = pen; P.hx = hx; P.hy = hy; }
        if (P.dwell >= cfg.passMax) { m._closePass(f, P); V.pass = null; }
      } else if (V.pass) {
        m._closePass(f, V.pass); V.pass = null;
      }

      if (done) { if (V.pass) m._closePass(f, V.pass); f.ultVent = null; }
    }

    if (!m._vents.length) return;
    for (let i = m._vents.length - 1; i >= 0; i--) {
      const v = m._vents[i];
      v.t += dt;
      if (v.t >= v.life) { m._vents.splice(i, 1); continue; }
      if (v.wall === "N" || v.wall === "S") {
        v.x = n + v.u * Math.max(1, A.w - 2 * n);
        v.y = v.wall === "N" ? n : A.h - n;
      } else {
        v.x = v.wall === "W" ? n : A.w - n;
        v.y = n + v.u * Math.max(1, A.h - 2 * n);
      }
      if (this.over) continue;
      const L = Math.hypot(A.w, A.h);
      const t = v.own === "a" ? this.b : this.a;

      /* THE FRONT. `v.front` is null between firings; a firing sets it to 0
         and it walks out along the bearing at cfg.speed. The quarry is caught
         when the front SWEEPS PAST its projection -- the interval
         [front-prev, front] -- so a fast front cannot step over a ball
         between frames and a slow one can be left behind. cfg.speed 0 is the
         old instantaneous bar, kept as the control. */
      if (v.front !== null && v.front !== undefined) {
        const prev = v.front;
        v.front += cfg.speed * dt;
        if (v.front > L) { v.front = null; }
        else if (t.alive && !v.spent) {
          const px = t.x - v.x, py = t.y - v.y;
          const proj = px * v.ax + py * v.ay;
          const wid = cfg.taper
                    ? v.half * (0.25 + 0.75 * Math.min(1, Math.max(0, proj / (L * 0.55))))
                    : v.half;
          if (proj >= prev && proj <= v.front &&
              Math.abs(px * v.ay - py * v.ax) <= wid + R) {
            this.hurt(t, v.dmg * t.dmgTakenMul(), this[v.own]);
            t.apply("sunder", cfg.sunderN);
            m._hits++; v.spent = true;
          }
        }
      }

      v.next -= dt;
      if (v.next > 0) continue;
      v.next = v.period; v.fired++;
      m._beams++;
      if (cfg.speed > 0) { v.front = 0; v.spent = false; continue; }
      if (!t.alive) continue;
      const px = t.x - v.x, py = t.y - v.y;
      const proj = px * v.ax + py * v.ay;
      if (proj < 0 || proj > L) continue;
      const wid = cfg.taper
                ? v.half * (0.25 + 0.75 * Math.min(1, Math.max(0, proj / (L * 0.55))))
                : v.half;
      if (Math.abs(px * v.ay - py * v.ax) > wid + R) continue;
      this.hurt(t, v.dmg * t.dmgTakenMul(), this[v.own]);
      t.apply("sunder", cfg.sunderN);
      m._hits++;
    }
  };

  /* ONE PASS, ONE VENT. `k` is the size, and every arm below is a different
     answer to "what does k multiply". */
  M._closePass = function (f, P) {
    const m = this;
    const reach = f.w.reach * f.reachMul;
    const pen01 = Math.max(0, Math.min(1, P.maxPen / reach));
    m._pen.push(pen01); m._dwell.push(P.dwell);
    if (P.maxPen < cfg.minPen) { m._grazedOff++; return; }
    const k = cfg.sizeOn ? lerp(cfg.kMin, cfg.kMax, pen01) : 1;
    m._k.push(k);
    const nx = P.wall === "W" ? 1 : P.wall === "E" ? -1 : 0;
    const ny = P.wall === "N" ? 1 : P.wall === "S" ? -1 : 0;
    const idx = (m._ventSeq = (m._ventSeq || 0) + 1);
    let pick = DIRS.filter(d => d[0] * nx + d[1] * ny >= -0.01);
    if (cfg.dirs === "perp") pick = [[nx, ny]];
    const d = pick[Math.floor(hash01(7717, idx) * pick.length) % pick.length];
    if (m._vents.length >= cfg.maxVents) m._vents.shift();
    const n = m.inset;
    m._vents.push({
      own: f === m.a ? "a" : "b", wall: P.wall,
      u: (P.wall === "N" || P.wall === "S")
           ? Math.min(0.98, Math.max(0.02, (P.hx - n) / Math.max(1, A.w - 2 * n)))
           : Math.min(0.98, Math.max(0.02, (P.hy - n) / Math.max(1, A.h - 2 * n))),
      ax: d[0], ay: d[1], t: 0, fired: 0, x: P.hx, y: P.hy,
      half:   cfg.half     * (cfg.drive.indexOf("width")  >= 0 ? k : 1),
      life:   cfg.ventLife * (cfg.drive.indexOf("life")   >= 0 ? k : 1),
      dmg:    cfg.beamDmg  * (cfg.drive.indexOf("dmg")    >= 0 ? k : 1),
      period: cfg.period   / (cfg.drive.indexOf("period") >= 0 ? k : 1),
      next:   cfg.warm, front: null, spent: false,
    });
    m._tears++;
  };

  const rows = [];
  const pen = [], dwell = [], ks = [];
  try {
    for (const f of foes) for (const s of seeds) {
      const m = new AC.Match(donor, f, s);
      const me = m.a.w.id === donor ? m.a : m.b;
      m._vents = []; m._tears = 0; m._beams = 0; m._hits = 0; m._grazedOff = 0;
      m._pen = []; m._dwell = []; m._k = [];
      let steps = 0;
      while (!m.over && steps < secs / DT) { m.step(DT); steps++; }
      for (const p of m._pen) pen.push(p);
      for (const p of m._dwell) dwell.push(p);
      for (const p of m._k) ks.push(p);
      rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  dealt: me.dealt, casts: me.ultsFired, tears: m._tears,
                  beams: m._beams, bhits: m._hits,
                  passes: m._pen.length, grazedOff: m._grazedOff });
    }
  } finally {
    M.step = origStep; M.fireUlt = origFire; delete M._closePass;
    w.aff = saved.aff; w.dmg = saved.dmg; w.ult = saved.ult;
    delete w.onHit; delete w.onSelf;
    if (saved.onHit)  w.onHit  = saved.onHit;
    if (saved.onSelf) w.onSelf = saved.onSelf;
  }
  return { rows, pen, dwell, ks };
}"""

FLOOR_JS = r"""([donor, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, ch: w.ult.charge,
                  onHit:  w.onHit  ? JSON.parse(JSON.stringify(w.onHit))  : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "dwarven"; delete w.onHit; delete w.onSelf; w.onHit = { sunder: 1 };
  w.ult.charge = 1e9;
  const rows = [];
  try {
    for (const f of foes) for (const s of seeds) {
      const m = new AC.Match(donor, f, s);
      const me = m.a.w.id === donor ? m.a : m.b;
      let steps = 0;
      while (!m.over && steps < secs / DT) { m.step(DT); steps++; }
      rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1, dealt: me.dealt });
    }
  } finally {
    w.aff = saved.aff; w.ult.charge = saved.ch;
    delete w.onHit; delete w.onSelf;
    if (saved.onHit)  w.onHit  = saved.onHit;
    if (saved.onSelf) w.onSelf = saved.onSelf;
  }
  return rows;
}"""

CENTRE = dict(charge=15, dur=8.0, maxVents=8, ventLife=9.0, period=1.1,
              warm=0.35, beamDmg=9.0, half=14.0, sunderN=1, dirs="eight",
              passMax=1.2, minPen=0.0, sizeOn=True, kMin=0.5, kMax=1.5,
              drive="width,life", speed=0.0, taper=False)


def summarize(rows):
    fin = [r for r in rows if r["win"] >= 0]
    return {"win": mean(r["win"] for r in fin),
            "casts": mean(r["casts"] for r in rows),
            "tears": mean(r["tears"] for r in rows),
            "passes": mean(r["passes"] for r in rows),
            "beams": mean(r["beams"] for r in rows),
            "bhits": mean(r["bhits"] for r in rows),
            "dealt": mean(r["dealt"] for r in rows)}


def hist(xs, bins=10, lo=0.0, hi=1.0):
    out = [0] * bins
    for x in xs:
        i = min(bins - 1, max(0, int((x - lo) / (hi - lo) * bins)))
        out[i] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--donor", default="thornwake")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [2207 + 11 * i for i in range(a.seeds)]
    arms = [("instant bar (control)", dict(speed=0.0, taper=False)),
            ("front 1800/s", dict(speed=1800.0)),
            ("front 1100/s", dict(speed=1100.0)),
            ("front 650/s", dict(speed=650.0)),
            ("front 350/s", dict(speed=350.0)),
            ("taper, instant", dict(speed=0.0, taper=True)),
            ("taper + front 1100", dict(speed=1100.0, taper=True)),
            ("taper + front 1100, wide", dict(speed=1100.0, taper=True, half=22.0)),
            ("taper + front 1100, +dmg", dict(speed=1100.0, taper=True, beamDmg=13.0))]

    out: dict = {}
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != a.donor]
        reach = page.evaluate(f"() => AC.WEAPONS.find(w=>w.id==='{a.donor}').reach")
        print(f"\nDONOR {a.donor} — {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes)*len(seeds)} fights an arm, reach {reach}\n")

        fl = page.evaluate(FLOOR_JS, [a.donor, foes, seeds, a.secs])
        floor = mean(r["win"] for r in fl if r["win"] >= 0)
        print(f"    floor, no ultimate: {floor:.1%}\n")

        # ------------------------------------------------------------ [1] --
        cfg = dict(CENTRE); cfg.update(arms[0][1])
        res = page.evaluate(LAB_JS, [a.donor, foes, seeds, a.secs, cfg])
        pen, dwell = res["pen"], res["dwell"]
        print(f"[1] THE PASS — {len(pen)} passes across "
              f"{len(foes)*len(seeds)} fights\n")
        h = hist(pen)
        top = max(h) or 1
        print(f"    how much of the blade went in, as a fraction of reach\n")
        for i, c in enumerate(h):
            bar = "#" * int(round(28 * c / top))
            print(f"      {i/10:.1f}-{(i+1)/10:.1f}  {bar:<28} {c:>6}  "
                  f"{c/max(1,len(pen)):>5.1%}")
        q = statistics.quantiles(pen, n=4) if len(pen) > 3 else [0, 0, 0]
        print(f"\n    median {statistics.median(pen):.2f}   "
              f"quartiles {q[0]:.2f} / {q[1]:.2f} / {q[2]:.2f}   "
              f"sd {statistics.pstdev(pen):.2f}")
        print(f"    dwell: median {statistics.median(dwell):.3f}s   "
              f"mean {mean(dwell):.3f}s   "
              f"passes a fight {len(pen)/(len(foes)*len(seeds)):.1f}")
        if len(pen) > 3:
            mp, md = mean(pen), mean(dwell)
            cov = sum((x-mp)*(y-md) for x, y in zip(pen, dwell))
            r = cov / (len(pen) * statistics.pstdev(pen) * statistics.pstdev(dwell))
            print(f"    depth against dwell: r = {r:+.2f} — "
                  + ("they are the same measurement" if abs(r) > 0.8
                     else "they are NOT the same measurement"))
        out["distribution"] = {"pen": h, "median": statistics.median(pen),
                               "sd": statistics.pstdev(pen),
                               "passes": len(pen)}

        # ------------------------------------------------------------ [2] --
        print(f"\n[2] WHAT SIZE SHOULD DRIVE — one arm each, same centre\n")
        print(f"    {'arm':<22}{'passes':>8}{'vents':>7}{'beams':>7}"
              f"{'hits':>7}{'dealt':>8}{'win':>8}{'lift':>8}")
        for name, over in arms:
            cfg = dict(CENTRE); cfg.update(over)
            r = page.evaluate(LAB_JS, [a.donor, foes, seeds, a.secs, cfg])
            rec = summarize(r["rows"])
            rec["lift"] = rec["win"] - floor
            rec["k"] = mean(r["ks"], 1.0)
            out[name] = rec
            print(f"    {name:<22}{rec['passes']:>8.1f}{rec['tears']:>7.1f}"
                  f"{rec['beams']:>7.1f}{rec['bhits']:>7.1f}{rec['dealt']:>8.0f}"
                  f"{rec['win']:>8.1%}{rec['lift']:>+8.1%}")

        ctl = out["instant bar (control)"]
        slow = out["front 350/s"]
        check("a travelling front can be outrun — the slowest arm lands fewer "
              "hits than an instantaneous bar",
              slow["bhits"] < ctl["bhits"],
              f"instant {ctl['bhits']:.1f} hits, 350/s {slow['bhits']:.1f}")
        fast = out["front 1800/s"]
        check("a fast front is not merely the bar again — if it were, the "
              "picture would be free and this lab would be pointless",
              abs(fast["bhits"] - ctl["bhits"]) > 0.2,
              f"instant {ctl['bhits']:.1f} hits, 1800/s {fast['bhits']:.1f}")
        tap = out["taper, instant"]
        check("the taper costs hits near the wall",
              tap["bhits"] < ctl["bhits"],
              f"flat width {ctl['bhits']:.1f} hits, tapered {tap['bhits']:.1f}")
        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
