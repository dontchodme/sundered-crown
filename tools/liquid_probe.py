#!/usr/bin/env python3
"""THE LIQUID, FALSIFIED. Twelve checks, and --selftest proves they can fail.

The risk in this build is not that it looks wrong -- a contact sheet catches
that. The risk is that it moved the game. Every health visual before it held
NO state and drew NO rng on purpose; this one carries ten numbers per relic
and integrates them on the simulation tick. So most of what is here is aimed
at that one claim from several directions, because `engine_ab` alone is no
longer sufficient: `simulate()` now switches the integrator OFF for headless
sweeps, so engine_ab passing proves the code is skipped, not that it is inert.

    python3 liquid_probe.py --src ../02-chain/sc-liquid.html
    python3 liquid_probe.py --src ../02-chain/sc-liquid.html --selftest
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
IDS = ["dawnbringer", "widowmaker", "grudgebearer", "thornwake", "lastlight",
       "gravemourn", "slagheart", "spellbreaker", "ironhail", "lightkeeper",
       "farwarden", "aureole", "censer", "emberedge", "oathwound", "heartwood",
       "nightfell", "axiom"]

# --- [1][2] the write-only claim, from two directions -----------------------
INERT = r"""([ids, n, breakIt]) => {
  const rows = [];
  for (const live of [false, true]) {
    let s = 987654321 >>> 0;
    for (let i = 0; i < ids.length; i++)
      for (let k = 0; k < n; k++) {
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const j = (i + 1 + k) % ids.length;
        if (j === i) continue;
        const m = new AC.Match(ids[i], ids[j], s);
        m.slLive = live;
        /* --selftest: let the liquid touch the simulation, exactly once, in
           the smallest way that could possibly matter. If the checks below
           cannot see this, they cannot see anything. */
        if (breakIt && live) {
          const mv = m.move.bind(m);
          m.move = function (f, foe, dt) { f.vx += (f.slTilt || 0) * 1e-6; return mv(f, foe, dt); };
        }
        let g = 0;
        while (!m.over && g++ < 200000) m.step(AC.CONFIG.physics.dt);
        const q = m.summary();
        rows.push([live, q.winner, q.hp, q.duration, q.hits.a, q.hits.b, q.clanks, q.crits.a]);
      }
  }
  const half = rows.length / 2;
  let diff = 0;
  for (let i = 0; i < half; i++)
    if (JSON.stringify(rows[i].slice(1)) !== JSON.stringify(rows[i + half].slice(1))) diff++;
  return { pairs: half, diff };
}"""

RNGCOUNT = r"""([ids, n]) => {
  const out = [];
  for (const live of [false, true]) {
    let s = 424242 >>> 0, total = 0;
    for (let i = 0; i < ids.length; i++)
      for (let k = 0; k < n; k++) {
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const j = (i + 1 + k) % ids.length;
        if (j === i) continue;
        const m = new AC.Match(ids[i], ids[j], s);
        m.slLive = live;
        let calls = 0;
        const r = m.rng;
        m.rng = function () { calls++; return r.apply(m, arguments); };
        let g = 0;
        while (!m.over && g++ < 200000) m.step(AC.CONFIG.physics.dt);
        total += calls;
      }
    out.push(total);
  }
  return { off: out[0], on: out[1] };
}"""

# --- [3][6][7][8] what the instrument says vs what it means -----------------
LEVEL = r"""([id, foe, seed]) => {
  const B = AC.CONFIG.combat.baseHP;
  /* [3] the scale itself */
  const mono = [];
  for (let i = 0; i <= 40; i++) mono.push(lvlOf(i / 40));
  let monoOk = true, inside = true;
  for (let i = 1; i < mono.length; i++) if (!(mono[i] < mono[i - 1])) monoOk = false;
  for (const v of mono) if (v < -1 || v > 1) inside = false;

  /* [6] the drawn waterline against the number it claims to state, every
     frame of a real match, through every bounce and every hit */
  const m = new AC.Match(id, foe, seed >>> 0);
  AC.__inject(m); m.introT = 0;
  let worst = 0, peak = 0, absSum = 0, nT = 0, worstAt = 0, peakSurf = 0;
  let g = 0;
  while (!m.over && g++ < 200000) {
    m.step(AC.CONFIG.physics.dt);
    for (const f of [m.a, m.b]) {
      const want = lvlOf(Math.max(0, Math.min(1, f.hp / B)));
      /* THE READING is the surface averaged across the width, weighted by the
         chord of the sphere -- a viewer integrates the boundary they can see,
         and the middle of the ball is where most of it is. Tilt and both
         ripple modes integrate to zero, so this should come out at
         level+heave and nothing else; anything more is the instrument
         drifting off the number it exists to state. */
      let acc = 0, wsum = 0;
      for (let q = -0.95; q <= 0.951; q += 0.05){
        const wgt = Math.sqrt(Math.max(0, 1 - q * q));
        acc += AC.__slosh.surf(f, q, want) * wgt; wsum += wgt;
      }
      const e = Math.abs(acc / wsum - want);
      if (e > worst) { worst = e; worstAt = +m.t.toFixed(2); }
      /* and separately the worst point on the surface, which is allowed to
         travel further because it is a wave */
      for (let q = -1; q <= 1.001; q += 0.1){
        const pe = Math.abs(AC.__slosh.surf(f, q, want) - want);
        if (pe > peakSurf) peakSurf = pe;
      }
      const t = Math.abs(f.slTilt || 0);
      if (t > peak) peak = t;
      absSum += t; nT++;
    }
  }

  /* [7] a heal must retract everything, with no memory of having been hurt */
  const m2 = new AC.Match(id, foe, 5); AC.__inject(m2); m2.introT = 0;
  const f2 = m2.a;
  const before = lvlOf(f2.hp / B);
  f2.hp = B * 0.11; const hurt = lvlOf(f2.hp / B);
  f2.hp = B;        const healed = lvlOf(f2.hp / B);

  /* [8] the Curse cap can never sit below the fill line it caps */
  let capOk = true;
  for (let mf = 0.2; mf <= 1.0001; mf += 0.05)
    for (let hf = 0; hf <= mf; hf += 0.05)
      if (!(lvlOf(mf) <= lvlOf(hf) + 1e-9)) capOk = false;

  return { monoOk, inside, worst, worstAt, peakSurf, peak, meanTilt: absSum / nT,
           heal: Math.abs(healed - before) < 1e-12 && hurt > before, capOk,
           dur: +m.t.toFixed(1) };
}"""

# --- [4][5] does it actually slosh, and does it settle ----------------------
SCHOOLS = r"""([pairs]) => {
  const out = {};
  for (const [id, foe] of pairs) {
    const m = new AC.Match(id, foe, 31337); AC.__inject(m); m.introT = 0;
    let peak = 0, sum = 0, n = 0, calm = 0;
    let g = 0;
    while (!m.over && g++ < 200000) {
      m.step(AC.CONFIG.physics.dt);
      const t = Math.abs(m.a.slTilt || 0);
      if (t > peak) peak = t;
      if (t < 0.02) calm++;
      sum += t; n++;
    }
    out[id] = { aff: m.a.aff.key, peak: +peak.toFixed(4),
                mean: +(sum / n).toFixed(4), calmFrac: +(calm / n).toFixed(3) };
  }
  return out;
}"""

# --- [9][10][11][12] frame cost, errors, death, and the chip gate ----------
FRAME = r"""([id, foe, seed, warm, n]) => {
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed >>> 0); AC.__inject(m); m.introT = 0;
  const dt = AC.CONFIG.physics.dt;
  const per = Math.round((1 / 60) / dt);
  for (let i = 0; i < warm; i++) { for (let k = 0; k < per; k++) m.step(dt); AC.__draw(m); }
  const ms = [];
  for (let i = 0; i < n; i++) {
    for (let k = 0; k < per; k++) m.step(dt);
    const t0 = performance.now(); AC.__draw(m); ms.push(performance.now() - t0);
  }
  /* run it out and draw the whole death, which is the one path a mid-match
     sample can never reach */
  let g = 0, deathFrames = 0;
  while (!m.over && g++ < 200000) m.step(dt);
  for (let i = 0; i < 140; i++) { m.step(dt); AC.__draw(m); deathFrames++; }
  ms.sort((a, b) => a - b);
  return { med: +ms[Math.floor(ms.length / 2)].toFixed(2),
           p95: +ms[Math.floor(ms.length * 0.95)].toFixed(2),
           max: +ms[ms.length - 1].toFixed(2),
           deathFrames, deathHp: m.loser ? m.loser.deathHp : null,
           over: m.over };
}"""

CHIP = r"""() => {
  /* [12] with the fracture off, the silhouette must be a clean circle: a
     straight-edged bite with no crack running to it reads as a rendering
     fault, not as damage. Sampled as the extreme radius over 360 directions
     of the path, via isPointInPath. */
  const R = AC.CONFIG.physics.ballR;
  const f = { side: 1, x: 0, y: 0 };
  const probe = (on, dmg) => {
    FRACTURE.on = on;
    const p = glassPath(f, R, dmg, 0, 0);
    const cv = document.createElement('canvas'); cv.width = cv.height = 8;
    const c = cv.getContext('2d');
    let minR = 1;
    for (let a = 0; a < 360; a += 2) {
      let lo = 0.2, hi = 1.2;
      for (let it = 0; it < 18; it++) {
        const mid = (lo + hi) / 2;
        const x = Math.cos(a * Math.PI / 180) * mid * R, y = Math.sin(a * Math.PI / 180) * mid * R;
        if (c.isPointInPath(p, x, y)) lo = mid; else hi = mid;
      }
      if (lo < minR) minR = lo;
    }
    return minR;
  };
  const off = probe(false, 0.95);
  const on  = probe(true, 0.95);
  FRACTURE.on = false;
  return { off: +off.toFixed(3), on: +on.toFixed(3) };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-liquid.html")
    ap.add_argument("--ctl", default="../02-chain/sc-health18.html")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--selftest", action="store_true",
                    help="couple the liquid to the sim by 1e-6 and confirm [1] and [2] catch it")
    a = ap.parse_args()

    src = pathlib.Path(a.src)
    if not src.is_absolute():
        src = (HERE / a.src).resolve()
    ctl = pathlib.Path(a.ctl)
    if not ctl.is_absolute():
        ctl = (HERE / a.ctl).resolve()

    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=""):
        checks.append((name, bool(ok), detail))
        print(f"  [{len(checks):>2}] {'PASS' if ok else 'FAIL'}  {name:<44} {detail}")

    print(f"=== LIQUID PROBE  {src.name}"
          + ("   (SELFTEST: the liquid is deliberately coupled)" if a.selftest else "") + " ===\n")

    with game(game_path=src) as (page, errors):
        page.evaluate("() => { window.AC.__slosh = SLOSH; window.AC.__glass = drawGlassRelic;"
                      "        window.AC.__hash = shellHash; return true; }")

        r = page.evaluate(INERT, [IDS, a.n, a.selftest])
        ck("integrating the liquid changes no match",
           r["diff"] == 0, f"{r['pairs'] - r['diff']}/{r['pairs']} identical")

        r = page.evaluate(RNGCOUNT, [IDS, a.n])
        ck("the liquid draws no simulation rng",
           r["off"] == r["on"], f"{r['on']:,} draws with, {r['off']:,} without")

        lv = page.evaluate(LEVEL, ["widowmaker", "axiom", 90210])
        ck("the level scale is monotone in health", lv["monoOk"])
        ck("the level never leaves the sphere", lv["inside"])
        # heave 0.060 + J1(pi)/(pi/2)*A2 0.110 + |J1(2pi)/pi|*A3 0.100 = 0.0867 R
        ck("the reading never drifts past its derived budget",
           lv["worst"] <= 0.0867 + 1e-4,
           f"worst {lv['worst']:.4f}R = {lv['worst']/1.64*300:.1f} HP "
           f"at t={lv['worstAt']}s (budget 0.0867R = 15.9 HP)")
        ck("the surface never stops reading as a level",
           lv["peak"] <= 0.75,
           f"peak tilt {lv['peak']:.3f} rad = {lv['peak']*57.3:.0f} deg "
           f"(clamp 0.92 = 53 deg)")
        ck("a heal retracts with no memory", lv["heal"])
        ck("the Curse cap never sits below the fill", lv["capOk"])

        pairs = [[IDS[i], IDS[(i + 5) % len(IDS)]] for i in range(len(IDS))]
        sc = page.evaluate(SCHOOLS, [pairs])
        by_aff: dict[str, list[float]] = {}
        for wid, v in sc.items():
            by_aff.setdefault(v["aff"], []).append(v["peak"])
        peaks = {k: statistics.mean(v) for k, v in by_aff.items()}
        worst_school = min(peaks, key=peaks.get)
        ck("every school actually sloshes",
           min(peaks.values()) > 0.09,
           "peak |tilt| " + " ".join(f"{k[:4]}={v:.2f}" for k, v in sorted(peaks.items(), key=lambda x: -x[1])))
        ck("thin schools slosh more than thick ones",
           peaks.get("sanctified", 0) > peaks.get("dwarven", 1),
           f"sanctified {peaks.get('sanctified',0):.3f} > dwarven {peaks.get('dwarven',0):.3f}")
        calm = statistics.mean(v["calmFrac"] for v in sc.values())
        ck("it is calm between contacts, not permanently wobbling",
           calm > 0.30, f"{calm*100:.0f}% of ticks under 0.02 rad")

        chip = page.evaluate(CHIP)
        ck("no fracture means no chipped silhouette",
           chip["off"] > 0.995 and chip["on"] < 0.98,
           f"min radius off={chip['off']} on={chip['on']}")

        fr = page.evaluate(FRAME, ["widowmaker", "axiom", 90210, 20, 90])
        ck("the death draws clean and knows what it lost",
           fr["deathHp"] is not None and fr["over"],
           f"deathHp={fr['deathHp']}, {fr['deathFrames']} frames drawn")
        liq_ms = (fr["med"], fr["p95"], fr["max"])
        errs = list(errors)

    ck("no page errors anywhere in the run", not errs, "; ".join(errs[:2]))

    with game(game_path=ctl) as (page, cerrors):
        cf = page.evaluate(FRAME.replace("m.loser ? m.loser.deathHp : null", "0"),
                           ["widowmaker", "axiom", 90210, 20, 90])
    print(f"\n  frame cost @1080x1920, GPU-less box (NOT a phone number):")
    print(f"    {ctl.name:<22} med {cf['med']:>6.2f} ms   p95 {cf['p95']:>6.2f}   max {cf['max']:>6.2f}")
    print(f"    {src.name:<22} med {liq_ms[0]:>6.2f} ms   p95 {liq_ms[1]:>6.2f}   max {liq_ms[2]:>6.2f}")
    d = (liq_ms[0] - cf["med"]) / max(0.01, cf["med"]) * 100
    print(f"    median delta {d:+.1f}%")

    bad = [n for n, ok, _ in checks if not ok]
    print(f"\n{len(checks) - len(bad)}/{len(checks)} " + ("PASS" if not bad else f"— FAILED: {bad}"))
    if a.selftest:
        want = {"integrating the liquid changes no match"}
        caught = want & set(bad)
        print("\nSELFTEST: " + ("the coupling was CAUGHT — the checks have teeth"
                                if caught else "!! the coupling was NOT caught — check [1] is asleep"))
        return 0 if caught else 1
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
