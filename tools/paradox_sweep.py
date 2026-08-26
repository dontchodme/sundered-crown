#!/usr/bin/env python3
"""SOLVE THE STASIS FIELD. `need` against `bleed`, then the blow, then damage.

    python3 paradox_sweep.py --game ../02-chain/sc-paradox.html

THE PAIR IS NOT SEPARABLE and that is the whole reason this file exists.
`need` is how much accrued dwell a hold costs and `bleed` is how fast it comes
back; between them they set how often the field fires, and neither number
means anything alone. A `need` of 0.6 with a 2/s bleed and a `need` of 1.2 with
no bleed land the hold at almost the same rate and are completely different
mechanics -- one is a trap that has to be sprung in a single pass, the other is
a stopwatch that never resets.

EVERY CELL BISECTS `dmg` FIRST. v40's rule: a share measured against a blade
that is not the shipping blade is a statement about the blade. AND THE
BISECTION IS AGAINST THE WHOLE FIELD -- v41 open decision 2, closed the
expensive way: Bulwarden's dmg was bisected on a five-foe subset that read 50%
and the full field read 55.2% on the same number.

AND THE COLUMN THAT MATTERS IS NOT DAMAGE. `runic_flail_probe [4]` measured
this ultimate at +42% damage over nothing, and every point of that came from
LANDING blows that would otherwise have missed -- the flail's live blade is
13.2 units (flail_survey §2) and the whole mechanic is removing the reason it
misses. So the telemetry here splits damage by whether the quarry was HELD when
it arrived.

  [1] THE BASELINE. The relic with the window suppressed, so every share below
      has something to be a share of.
  [2] need x bleed, dmg bisected per cell.
  [3] `blow` at the chosen pair -- what a landed hit should be worth to the
      charge, which is §1's second sentence and Rick's call.
  [4] THE FINAL BISECTION at the chosen numbers, wider.

INJECTION IS RUNTIME-ONLY. Nothing is written to any build; the chosen numbers
go back into `paradox_build.py`'s ULT dict by hand, which is the only place
this project keeps a tuned number.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "paradox"


WIN_JS = r"""([id, dmg, ult, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0, timeouts = 0;
  for (const foe of ids){
    for (let k = 0; k < n; k++){
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const r = AC.simulate(id, foe, s);
      if (r.winner === w.name) win++;
      games++; dur += r.duration;
      if (r.reason !== "slain") timeouts++;
    }
  }
  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  return { win, games, rate: win / games, dur: dur / games, timeouts };
}"""


TEL_JS = r"""([id, dmg, ult, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(id, f, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      /* SPLIT AT THE SOURCE, by whether the quarry was HELD when the blow
         arrived. "What is the window worth" cannot be answered by counting
         casts on an ultimate whose whole effect is making ORDINARY blows land. */
      let dHeld = 0, dFree = 0, hHeld = 0, hFree = 0, taken = 0;
      const oRes = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
        const held = f2.pin > 0, before = self.dealt;
        const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
        const dd = self.dealt - before;
        if (self === me && !f2.shade){
          if (held){ dHeld += dd; hHeld++; } else { dFree += dd; hFree++; }
        }
        return r;
      };

      let steps = 0, casts = 0, up = 0, wasUp = false;
      let holds = 0, heldFrames = 0, p0 = 0, qPeak = 0, frozen = 0;
      while (!m.over && steps < secs / DT){
        const fr = m.hitStop > 0;
        m.step(DT); steps++;
        if (fr) frozen++;
        const F = me.ultField;
        if (F){ up++; if (!wasUp) casts++; if (F.q > qPeak) qPeak = F.q; }
        wasUp = !!F;
        if (th.pin > 0){ heldFrames++; if (p0 <= 0) holds++; }
        p0 = th.pin;
      }
      rows.push({ foe: f, seed: sd, dur: steps * DT, steps,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  casts, up, holds, heldFrames, qPeak, frozen,
                  dHeld, dFree, hHeld, hFree,
                  taken: th.dealt, ultsFired: me.ultsFired });
    }
  }
  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  return rows;
}"""


def bisect(page, ult, n, lo, hi, steps, seed=20260821, target=0.50, quiet=False):
    """Find the `dmg` at which the relic is even against the WHOLE field."""
    best = None
    for i in range(steps):
        mid = (lo + hi) / 2
        r = page.evaluate(WIN_JS, [RID, mid, ult, n, seed + i])
        if not quiet:
            print(f"      dmg {mid:6.2f}  ->  {r['rate']:6.1%}  "
                  f"({r['win']}/{r['games']}, mean {r['dur']:.1f}s, "
                  f"{r['timeouts']} timeouts)")
        if best is None or abs(r["rate"] - target) < abs(best[1] - target):
            best = (mid, r["rate"], r)
        if r["rate"] > target:
            hi = mid
        else:
            lo = mid
    return best


def agg(rows):
    n = len(rows)
    tot = lambda k: sum(r[k] for r in rows)          # noqa: E731
    dAll = (tot("dHeld") + tot("dFree")) or 1
    steps = tot("steps") or 1
    casts = tot("casts") or 1
    return dict(
        casts=tot("casts") / n,
        holds=tot("holds") / n,
        holdsPerCast=tot("holds") / casts,
        holdsPerMin=tot("holds") / max(1e-9, tot("dur")) * 60,
        heldFrac=tot("heldFrames") / steps,
        upFrac=tot("up") / steps,
        heldShare=tot("dHeld") / dAll,
        hpsHeld=tot("hHeld") / max(1e-9, tot("heldFrames") * (1 / 120)),
        hpsFree=tot("hFree") / max(1e-9, (steps - tot("heldFrames")) * (1 / 120)),
        dmgPerHold=tot("dHeld") / max(1, tot("holds")),
        taken=tot("taken") / max(1e-9, tot("dur")),
        dur=statistics.mean(r["dur"] for r in rows),
        win=statistics.mean(r["win"] for r in rows if r["win"] >= 0),
        qPeak=statistics.mean(r["qPeak"] for r in rows),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox.html")
    ap.add_argument("--n", type=int, default=10, help="seeds per pairing, bisection")
    ap.add_argument("--nfinal", type=int, default=40)
    ap.add_argument("--steps", type=int, default=5)
    ap.add_argument("--seeds", type=int, default=5, help="seeds per foe, telemetry")
    ap.add_argument("--secs", type=float, default=90.0)
    ap.add_argument("--lo", type=float, default=18.0)
    ap.add_argument("--hi", type=float, default=44.0)
    ap.add_argument("--phase", default="1,2,3,4")
    ap.add_argument("--need", type=float, default=0.9)
    ap.add_argument("--bleed", type=float, default=0.5)
    ap.add_argument("--blow", type=float, default=0.35)
    ap.add_argument("--dmg", type=float, default=0.0, help="skip the bisection")
    ap.add_argument("--json", default="../05-reference/v43/paradox-sweep.json")
    a = ap.parse_args()

    phases = set(a.phase.split(","))
    gp = (HERE / a.game).resolve()
    seeds = [911 + i * 137 for i in range(a.seeds)]
    FOES = ["heartwood", "grudgebearer", "twinshade", "lastlight",
            "widowmaker", "slagheart", "aureole", "axiom"]
    out = {}

    with game(game_path=gp) as (page, errors):
        base = json.loads(page.evaluate(
            """() => JSON.stringify(AC.WEAPONS.find(w => w.id === "%s").ult)""" % RID))
        d0 = page.evaluate(
            """() => AC.WEAPONS.find(w => w.id === "%s").dmg""" % RID)
        print(f"\nSTASIS FIELD SWEEP — shipped dmg {d0:g}, "
              f"need {base['need']:g} bleed {base['bleed']:g} "
              f"blow {base['blow']:g} pin {base['pin']:g} rad {base['rad']:g}")

        # ------------------------------------------------------------ [1] --
        if "1" in phases:
            print(f"\n[1] THE BASELINE — the relic with the window suppressed, "
                  f"so every share below has something to be a share OF\n")
            b = bisect(page, {"charge": 1e9}, a.n, a.lo, a.hi, a.steps)
            print(f"\n    a flail with hex and no ultimate is even at "
                  f"dmg {b[0]:.2f} ({b[1]:.1%})")
            print(f"    the type ships 25.0 (Threshmaw) .. 44.1 (Gravemourn)")
            out["baseline"] = {"dmg": b[0], "rate": b[1]}

        # ------------------------------------------------------------ [2] --
        grid = {}
        if "2" in phases:
            NEEDS = [0.6, 0.9, 1.2]
            BLEEDS = [0.25, 0.5, 1.0]
            print(f"\n[2] need x bleed — `dmg` BISECTED IN EVERY CELL against "
                  f"all 24 opponents before its telemetry is read\n")
            print(f"    {'need':>6}{'bleed':>7}{'dmg':>8}{'win':>7}"
                  f"{'holds/cast':>12}{'holds/min':>11}{'held':>7}"
                  f"{'window share':>14}{'hits/s held':>13}{'free':>7}"
                  f"{'per hold':>10}")
            for need in NEEDS:
                for bleed in BLEEDS:
                    ult = {"need": need, "bleed": bleed, "blow": a.blow}
                    b = bisect(page, ult, a.n, a.lo, a.hi, a.steps, quiet=True)
                    rows = page.evaluate(TEL_JS,
                                         [RID, b[0], ult, FOES, seeds, a.secs])
                    q = agg(rows)
                    grid[(need, bleed)] = dict(dmg=b[0], rate=b[1], **q)
                    print(f"    {need:>6.2f}{bleed:>7.2f}{b[0]:>8.2f}"
                          f"{b[1]:>7.1%}{q['holdsPerCast']:>12.2f}"
                          f"{q['holdsPerMin']:>11.2f}{q['heldFrac']:>7.1%}"
                          f"{q['heldShare']:>14.1%}{q['hpsHeld']:>13.3f}"
                          f"{q['hpsFree']:>7.3f}{q['dmgPerHold']:>10.1f}")
            out["grid"] = {f"{k[0]}/{k[1]}": v for k, v in grid.items()}

        # ------------------------------------------------------------ [3] --
        if "3" in phases:
            print(f"\n[3] `blow` — what a landed hit is worth to the charge, at "
                  f"need {a.need:g} / bleed {a.bleed:g}\n")
            print(f"    {'blow':>6}{'dmg':>8}{'win':>7}{'holds/cast':>12}"
                  f"{'holds/min':>11}{'held':>7}{'window share':>14}"
                  f"{'per hold':>10}")
            blows = {}
            for blow in (0.0, 0.2, 0.35, 0.5, 0.8):
                ult = {"need": a.need, "bleed": a.bleed, "blow": blow}
                b = bisect(page, ult, a.n, a.lo, a.hi, a.steps, quiet=True)
                rows = page.evaluate(TEL_JS, [RID, b[0], ult, FOES, seeds, a.secs])
                q = agg(rows)
                blows[blow] = dict(dmg=b[0], rate=b[1], **q)
                print(f"    {blow:>6.2f}{b[0]:>8.2f}{b[1]:>7.1%}"
                      f"{q['holdsPerCast']:>12.2f}{q['holdsPerMin']:>11.2f}"
                      f"{q['heldFrac']:>7.1%}{q['heldShare']:>14.1%}"
                      f"{q['dmgPerHold']:>10.1f}")
            out["blow"] = {str(k): v for k, v in blows.items()}

        # ------------------------------------------------------------ [4] --
        if "4" in phases:
            ult = {"need": a.need, "bleed": a.bleed, "blow": a.blow}
            print(f"\n[4] THE FINAL BISECTION — need {a.need:g}, bleed "
                  f"{a.bleed:g}, blow {a.blow:g}, {a.nfinal} seeds x 24 "
                  f"opponents\n")
            if a.dmg > 0:
                r = page.evaluate(WIN_JS, [RID, a.dmg, ult, a.nfinal, 20260821])
                print(f"      dmg {a.dmg:6.2f}  ->  {r['rate']:6.1%}  "
                      f"({r['win']}/{r['games']}, mean {r['dur']:.1f}s, "
                      f"{r['timeouts']} timeouts)")
                out["final"] = {"dmg": a.dmg, "rate": r["rate"]}
            else:
                b = bisect(page, ult, a.nfinal, a.lo, a.hi, a.steps + 2)
                print(f"\n    ships at dmg {b[0]:.2f} ({b[1]:.1%})")
                out["final"] = {"dmg": b[0], "rate": b[1]}

    if errors:
        print("\n!! page errors:")
        for e in errors[:10]:
            print("   ", e)
    p = (HERE / a.json).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, default=float))
    print(f"\nwrote {p}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
