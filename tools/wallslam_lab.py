#!/usr/bin/env python3
"""THE WALL, PRICED BEFORE A BUILDER IS OPENED. v60 §1, the red hammer.

    python wallslam_lab.py --game ../02-chain/sc-breach.html

Rick took `bloodsworn x warhammer` and, off four priced directions, took the
KNOCKBACK: the hammer throws the quarry into a wall and the wall pays, scaled
by how hard it arrived.

The engine already has the event. `move()` clamps a ball at `n + R` and
reflects it, sets `bounced`, spawns fx and plays "wall" -- so this ultimate,
like CINDERCLEAVE's, is A TEST NOBODY IS RUNNING plus a rule about how often
it may fire. There is no new collision in it. What there IS, and what cannot
be assumed, is whether the thing being read has any range on it.

THREE PREDICTIONS, REGISTERED HERE BEFORE THE BUILD EXISTS. `pass_probe`'s
rule: if the gate fails, THE DESIGN CHANGES, NOT THE NUMBER.

  P1  THE SPREAD IS REAL. Arrival speed on a hammer-thrown quarry has a top
      decile at least 1.6x its bottom decile. "Scaled by how hard it arrived"
      rests entirely on this; if arrival speed is flat, the scale is a
      constant wearing a costume and the mechanic must be redesigned.

  P2  THE HAMMER IS THE CAUSE. A quarry thrown by a warhammer arrives at
      least 25% faster (median) than one thrown by anything else. `knockMul`
      2.3 is the only value above 1.0 in the roster and it is the whole
      premise of the direction. If a greatsword throws them into the wall
      just as hard, this is not a warhammer ultimate, it is a generic one.

  P3  THE ARRIVAL IS NOT MOSTLY THE FLOOR. Fewer than 70% of hammer-thrown
      arrivals land on the floor plane. Open item 37 measured gravity nearly
      erasing the north wall for CINDERCLEAVE's tears; the same physics acts
      on a thrown body, pointed the other way. If this is a floor mechanic,
      the ART has to know that before it is drawn, and so does the name.

  [1] BOTH ARMS EXIST -- the sensitivity control. A run that saw no
      non-warhammer blows cannot test P2 and must not report it.
  [2] ONE BLOW IS ONE ARRIVAL. First bounce only, deduped across frames, and
      a blow whose quarry never reaches a wall inside the window is counted
      as a MISS rather than dropped.
  [2b] THE INSTRUMENT SEES THE IMPULSE. |dv| on a blow must come back at
      exactly `CONFIG.combat.knock x knockMul`. Speed is the WRONG instrument
      for an impulse pointed away from an attacker the victim was moving
      toward, and without this gate a refuted P2 could just as easily be a
      probe that never read the knock at all.
  [3] P1, THE SPREAD.        <- GATE
  [4] P2, THE CAUSE.         <- GATE
  [5] P3, THE FLOOR.         <- GATE
  [6] no JS errors.

Reported and NOT gated: the contact rate and its latency (what share of blows
ever reach a wall -- BREACH's "second contact rate" question), the four-wall
split, and what the throw costs the hammer in its own next swing (v51 §4.3,
the knockback eating its own window). Those are inputs to the design, not
claims it can fail on.

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


def q(xs, p):
    if not xs:
        return 0.0
    s = sorted(xs)
    i = max(0, min(len(s) - 1, int(round(p * (len(s) - 1)))))
    return s[i]


# THE HARNESS. Everything is stepped inside one page evaluate -- a per-step
# round trip from Python would take hours. What comes back is EVENTS, not
# summaries, so every number below is computed here in Python and can be
# recomputed differently without re-running the sim.
#
# THE SPEED IS SAMPLED BEFORE `move`, WHICH IS ONE dt OF GRAVITY EARLY. The
# reflection happens inside the clamp and nothing outside can see the instant
# between integration and reflection. At dt = 1/120 that is 7.5 px/s against
# arrivals in the hundreds, and it is the same error on both arms of P2.
JS = r"""(cfg) => {
  const dt = AC.CONFIG.physics.dt;
  const A  = AC.CONFIG.arena, R = AC.CONFIG.physics.ballR;
  const out = { slams: [], miss: 0, blows: 0, gaps: [], fights: 0,
                doubles: 0, deps: [], whBlows: 0, othBlows: 0, err: null };
  try {
    for (const foeId of cfg.foes){
      for (const relic of cfg.relics){
        if (relic === foeId) continue;
        for (const sd of cfg.seeds){
          const m = new AC.Match(relic, foeId, sd);
          out.fights++;
          const origHit = m.resolveHit, origMove = m.move;

          /* THE BLOW, off the engine's own call. `foe` is the victim and
             `self.w` is the weapon that threw it -- not this probe's idea of
             which relic was swinging. */
          m.resolveHit = function (self, foe, hx, hy, seg, mul, over){
            const pre = Math.hypot(foe.vx, foe.vy);
            const pvx = foe.vx, pvy = foe.vy;
            const r = origHit.call(m, self, foe, hx, hy, seg, mul, over);
            /* THE IMPULSE ITSELF, as a VECTOR. Speed is the wrong instrument
               for it: the knock points away from the attacker and the victim
               was, by construction, moving toward the attacker -- that is why
               they touched. So a bigger impulse REVERSES a ball rather than
               speeding it up, and the median speed change is negative at both
               knockMul values. |dv| has no such problem, and it doubles as
               this probe's own self-test: it must come back at exactly
               CONFIG.combat.knock x knockMul, 165 and 379.5. If it does not,
               the instrument is not reading the impulse and nothing below
               about P2 is worth anything. */
            const dv = Math.hypot(foe.vx - pvx, foe.vy - pvy);
            /* THE INJECTED ARM. Runtime only, and it is a LAB rather than a
               measurement of the shipped build: when `kick` is non-zero a
               warhammer blow gets the red hammer's proposed extra impulse
               along the engine's own knock bearing, plus `launch`.
               `f.launch` is a PERMISSION and not a push -- it raises vmax and
               adds no velocity -- so a launch without a kick moves nothing,
               and a kick without a launch is clipped at speedMax. The
               Crucible already pairs them; this prices the pair. */
            if (cfg.kick && self.w.shape === "warhammer"){
              const kx = foe.x - self.x, ky = foe.y - self.y;
              const kl = Math.hypot(kx, ky) || 1;
              foe.vx += (kx / kl) * cfg.kick;
              foe.vy += (ky / kl) * cfg.kick;
              foe.launch = Math.max(foe.launch || 0, cfg.launchT);
            }
            out.blows++;
            /* THE DEPARTURE, and it is the half of P2 that `knockMul`
               actually controls. The knock is applied INSIDE resolveHit, so
               reading the victim's velocity here is post-impulse and
               pre-clamp -- `move` has not run yet and has not had the chance
               to relax it toward `target` or clip it at `speedMax`.
               `launch` is Grudgebearer's forge strike raising its own vmax;
               tagged, not dropped, because excluding it silently would be a
               probe deciding which of the row's blows count. */
            const wh = self.w.shape === "warhammer";
            if (wh) out.whBlows++; else out.othBlows++;
            const dep = Math.hypot(foe.vx, foe.vy);
            out.deps.push([dep, self.w.shape, foe.launch > 0 ? 1 : 0,
                           (self.w.knockMul || 1), pre, self.w.id, dv]);
            /* v51 4.3, the cost side: the gap to this wielder's NEXT landed
               blow, tagged with whether the quarry reached a wall in it. A
               blow that supersedes an unresolved one closes it as a MISS --
               [2]'s "one blow is one arrival". */
            const prev = self.__blow;
            if (prev){
              out.gaps.push([m.t - prev.t, prev.slammed ? 1 : 0, prev.shape]);
              if (!prev.slammed) out.miss++;
            }
            self.__blow = { t: m.t, shape: self.w.shape, dep: dep,
                            lau: foe.launch > 0 ? 1 : 0,
                            km: (self.w.knockMul || 1), slammed: false };
            foe.__slam = self.__blow;
            return r;
          };

          /* THE ARRIVAL. The clamp ASSIGNS the plane exactly, so equality is
             exact rather than an epsilon. `__wall` dedupes the frames a ball
             spends pinned against a plane it has not left yet -- without it a
             ball resting on the floor is a thousand arrivals. */
          m.move = function (f, foe2, d){
            const sp = Math.hypot(f.vx, f.vy);
            origMove.call(m, f, foe2, d);
            const n = m.inset;
            const loX = n + R, hiX = A.w - n - R, loY = n + R, hiY = A.h - n - R;
            let w = "";
            if (f.x === loX) w = "W"; else if (f.x === hiX) w = "E";
            else if (f.y === loY) w = "N"; else if (f.y === hiY) w = "S";
            if (!w){ f.__wall = ""; return; }
            if (f.__wall === w) return;                 // still against it
            f.__wall = w;
            const B = f.__slam;
            if (!B) return;                             // arrived on its own
            if (m.t - B.t > cfg.window) { f.__slam = null; return; }
            if (B.slammed){ out.doubles++; return; }     // [2]
            B.slammed = true;
            f.__slam = null;
            out.slams.push([sp, w, m.t - B.t, B.shape, B.km, B.dep, B.lau]);
          };

          for (let i = 0; i < cfg.steps; i++){
            m.step(dt);
            if (m.over) break;
          }
          /* The blow in flight when the fight ended never gets its gap. It is
             not a miss and it is not an arrival -- it is simply unfinished,
             and dropping it silently is what `breach_relic_probe` had to fix. */
          m.resolveHit = origHit; m.move = origMove;
        }
      }
    }
  } catch (e){ out.err = String(e) + " | " + String(e.stack).slice(0, 400); }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-breach.html")
    ap.add_argument("--relics", default="grudgebearer,censer,bulwarden,shroudmaul",
                    help="the wielders whose blows are watched -- the warhammer row")
    ap.add_argument("--foes", default="oathwound,redflail,widowmaker,marrowdraw,"
                                      "emberedge,thornshear",
                    help="a spread of the six types, and the CONTROL arm: their "
                         "blows are watched too")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--window", type=float, default=1.5,
                    help="seconds a blow may claim an arrival for")
    ap.add_argument("--kick", type=float, default=0.0,
                    help="LAB ARM: extra impulse px/s on a warhammer's knock. "
                         "0 measures the shipped build.")
    ap.add_argument("--launch-t", type=float, default=1.2, dest="launch_t",
                    help="LAB ARM: seconds of raised vmax granted with --kick")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    path = resolve_game(a.game)
    cfg = {
        "relics": [s for s in a.relics.split(",") if s],
        "foes": [s for s in a.foes.split(",") if s],
        "seeds": [1000 + 7919 * i for i in range(a.seeds)],
        "steps": int(a.secs * 120),
        "window": a.window,
        "kick": a.kick,
        "launchT": a.launch_t,
    }

    print(f"=== the wall, priced before a builder is opened - {a.game} ===")
    print(f"    {len(cfg['relics'])} wielders x {len(cfg['foes'])} foes x "
          f"{a.seeds} seeds, claim window {a.window}s")
    print("    SHIPPED BUILD, no injection" if not a.kick else
          f"    *** LAB ARM: warhammer kick +{a.kick:.0f} px/s, "
          f"launch {a.launch_t}s -- NOT the shipped build ***")
    print()

    with game(game_path=path) as (page, errors):
        out = page.evaluate(JS, cfg)
    if out["err"]:
        print("JS ERROR:", out["err"])
        sys.exit(2)

    slams = out["slams"]
    ham = [s for s in slams if s[3] == "warhammer"]
    oth = [s for s in slams if s[3] != "warhammer"]
    hs = [s[0] for s in ham]
    os_ = [s[0] for s in oth]

    print(f"[0] {out['fights']} fights, {out['blows']} blows landed, "
          f"{len(slams)} arrivals attributed\n")

    # --- reported, not gated -------------------------------------------------
    # THE DENOMINATOR IS EVERY BLOW, NOT EVERY CLOSED ONE. The first cut of
    # this divided by `gaps`, which only fills when a wielder lands a SECOND
    # blow -- so the last blow of every fight was missing from the bottom and
    # the rate read 103.3%. A contact rate over 100% is the cheapest possible
    # sign that a denominator is wrong, and it is the only reason this was
    # caught.
    print("[R] THE CONTACT RATE - what share of blows ever reach a wall")
    for lab, rows, n in (("warhammer", ham, out["whBlows"]),
                         ("everything else", oth, out["othBlows"])):
        rate = len(rows) / n * 100 if n else 0.0
        lat = statistics.median([r[2] for r in rows]) if rows else 0.0
        print(f"    {lab:16s} {len(rows):5d} arrivals of {n:5d} blows"
              f"   {rate:5.1f}%   median latency {lat:.2f}s")

    # WHY P2 READS THE WAY IT DOES. The departure is what `knockMul` sets; the
    # arrival is what the ultimate would read. If those two disagree, the
    # engine is eating the difference in between and that is the finding.
    print("\n[R] DEPARTURE against ARRIVAL - the impulse, and what survives of it")
    dep_w = [d[0] for d in out["deps"] if d[1] == "warhammer" and not d[2]]
    dep_o = [d[0] for d in out["deps"] if d[1] != "warhammer" and not d[2]]
    dep_l = [d[0] for d in out["deps"] if d[2]]
    print(f"    departure  warhammer      median {q(dep_w,0.5):6.0f} px/s  n={len(dep_w)}")
    print(f"    departure  everything else median {q(dep_o,0.5):5.0f} px/s  n={len(dep_o)}")
    if dep_l:
        print(f"    departure  forge launch    median {q(dep_l,0.5):5.0f} px/s  n={len(dep_l)}"
              f"   (excluded above — it raises its own vmax)")
    print(f"    arrival    warhammer      median {q(hs,0.5):6.0f} px/s")
    print(f"    arrival    everything else median {q(os_,0.5):5.0f} px/s")

    # THE PROBE BEFORE THE FINDING. A departure that does not move with
    # `knockMul` would mean this instrument is not reading the impulse at all,
    # and the refutation of P2 would be worth nothing. Grouped by the value
    # the blow actually carried, and `pre` is the victim's speed the instant
    # before it -- so `delta` is the impulse this probe can see.
    print("\n[R] IS THE IMPULSE VISIBLE AT ALL - departure grouped by knockMul")
    kms = sorted({d[3] for d in out["deps"]})
    for km in kms:
        rows = [d for d in out["deps"] if d[3] == km and not d[2]]
        if not rows:
            continue
        ids = sorted({d[5] for d in rows})
        print(f"    knockMul {km:<4}  n={len(rows):5d}   pre {q([d[4] for d in rows],0.5):5.0f}"
              f"  ->  departure {q([d[0] for d in rows],0.5):5.0f} px/s"
              f"   delta {q([d[0]-d[4] for d in rows],0.5):+5.0f}"
              f"   |dv| {q([d[6] for d in rows],0.5):5.1f}"
              f"   {','.join(ids[:3])}")

    print("\n[R] ARRIVAL BY LATENCY - how fast the impulse washes out")
    for lo, hi in ((0.0, 0.15), (0.15, 0.35), (0.35, 0.7), (0.7, 1.5)):
        a_w = [r[0] for r in ham if lo <= r[2] < hi]
        a_o = [r[0] for r in oth if lo <= r[2] < hi]
        if a_w and a_o:
            g = (q(a_w, 0.5) / q(a_o, 0.5) - 1) * 100
            print(f"    {lo:.2f}-{hi:.2f}s   warhammer {q(a_w,0.5):6.0f}  "
                  f"other {q(a_o,0.5):6.0f}   {g:+5.1f}%   n={len(a_w)}/{len(a_o)}")

    print("\n[R] THE FOUR WALLS - where a hammer-thrown quarry actually lands")
    tot = len(ham) or 1
    for w, name in (("S", "S  floor"), ("W", "W  left"), ("E", "E  right"), ("N", "N  roof")):
        c = sum(1 for r in ham if r[1] == w)
        print(f"    {name:10s} {c:5d}   {c/tot*100:5.1f}%")

    print("\n[R] WHAT THE THROW COSTS - gap to the hammer's own next landed blow")
    for tag, want in (("reached a wall", 1), ("did not", 0)):
        g = [x[0] for x in out["gaps"] if x[2] == "warhammer" and x[1] == want]
        if g:
            print(f"    {tag:16s} n={len(g):5d}   median {statistics.median(g):5.2f}s"
                  f"   mean {statistics.fmean(g):5.2f}s")
    print()

    # --- the gates -----------------------------------------------------------
    check("[1] both arms exist - the run can test P2 at all",
          len(hs) >= 50 and len(os_) >= 50,
          f"warhammer {len(hs)} arrivals, everything else {len(os_)}")

    check("[2] one blow is one arrival - no blow claimed twice",
          out["doubles"] == 0,
          f"{out['doubles']} double-claims over {len(slams)} arrivals")

    # THE GATE THAT MAKES P2'S VERDICT WORTH ANYTHING. `resolveHit` applies
    # `CONFIG.combat.knock * knockMul` and nothing else touches velocity in
    # between, so |dv| has one correct value per arm and this probe either
    # reads it exactly or is not reading the impulse at all.
    base = 165.0
    imp_ok, imp_detail = True, []
    for km in sorted({d[3] for d in out["deps"]}):
        rows = [d[6] for d in out["deps"] if d[3] == km and not d[2]]
        if not rows:
            continue
        med, want = q(rows, 0.5), base * km
        if abs(med - want) > 0.1:
            imp_ok = False
        imp_detail.append(f"knockMul {km}: |dv| {med:.1f} against {want:.1f}")
    check("[2b] the instrument sees the impulse - |dv| == knock x knockMul",
          imp_ok, "   ".join(imp_detail))

    d1, d9 = q(hs, 0.10), q(hs, 0.90)
    ratio = d9 / d1 if d1 else 0.0
    check("[3] P1 THE SPREAD IS REAL - top decile >= 1.6x bottom decile",
          ratio >= 1.6,
          f"p10 {d1:.0f}  median {q(hs,0.5):.0f}  p90 {d9:.0f} px/s"
          f"   ratio {ratio:.2f}  (registered 1.6)"
          f"\n        sd {statistics.pstdev(hs) if hs else 0:.0f}  n={len(hs)}")

    mh = q(hs, 0.5)
    mo = q(os_, 0.5)
    gain = (mh / mo - 1) * 100 if mo else 0.0
    check("[4] P2 THE HAMMER IS THE CAUSE - >= 25% over everything else",
          gain >= 25.0,
          f"warhammer median {mh:.0f} px/s against {mo:.0f}"
          f"   +{gain:.1f}%  (registered 25%)")

    floor = sum(1 for r in ham if r[1] == "S") / tot * 100
    check("[5] P3 THE ARRIVAL IS NOT MOSTLY THE FLOOR - under 70%",
          floor < 70.0,
          f"{floor:.1f}% of hammer-thrown arrivals land on the floor plane")

    check("[6] no JS errors or page exceptions", not errors,
          "; ".join(errors[:3]))

    ok = sum(1 for _, v in PASS if v)
    print(f"\n{ok}/{len(PASS)} checks passed")

    if a.json:
        p = pathlib.Path(a.json)
        if not p.is_absolute():
            p = pathlib.Path(__file__).parent / p
        p.parent.mkdir(parents=True, exist_ok=True)
        # A SUMMARY AND NOT THE EVENT LOG. The first cut wrote every arrival
        # and every gap -- 1.27 MB against `06-docs/v59/pass-probe.json`'s 492
        # bytes. The events are recomputable from the seeds in `cfg`, which is
        # what makes them the wrong thing to keep.
        def dist(xs):
            return {"n": len(xs), "p10": round(q(xs, 0.10), 1),
                    "median": round(q(xs, 0.5), 1), "p90": round(q(xs, 0.90), 1),
                    "sd": round(statistics.pstdev(xs), 1) if len(xs) > 1 else 0.0}
        p.write_text(json.dumps({
            "game": str(path),
            "cfg": {k: v for k, v in cfg.items() if k != "seeds"},
            "seeds": cfg["seeds"],
            "fights": out["fights"], "blows": out["blows"],
            "arrival": {"warhammer": dist(hs), "other": dist(os_)},
            "impulse": {str(km): round(q([d[6] for d in out["deps"]
                                          if d[3] == km and not d[2]], 0.5), 1)
                        for km in sorted({d[3] for d in out["deps"]})},
            "contact": {"warhammer": [len(ham), out["whBlows"]],
                        "other": [len(oth), out["othBlows"]]},
            "walls": {w: sum(1 for r in ham if r[1] == w) for w in "SWEN"},
            "gates": {n: v for n, v in PASS},
        }, indent=1), encoding="utf-8")
        print(f"wrote {p}")

    sys.exit(0 if ok == len(PASS) else 1)


if __name__ == "__main__":
    main()
