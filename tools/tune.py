#!/usr/bin/env python3
"""Closed-loop balance and pace tuner for The Sundered Crown."""
from __future__ import annotations
import argparse, json, pathlib, re, sys, time
from scpage import game, GAME

MEASURE_JS = r"""
([n, seed0]) => {
  const ids = AC.WEAPONS.map(w => w.id);
  const names = {}; for (const w of AC.WEAPONS) names[w.id] = w.name;
  const tally = {}; for (const id of ids) tally[id] = { w: 0, g: 0 };
  const durs = [], hitsAll = [], clanksAll = [];
  let s = seed0 >>> 0, timeouts = 0, total = 0;
  const worst = { pair: null, dur: 0 };
  const thin  = { pair: null, ids: null, hits: 1e9 };
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      let aw = 0, pd = 0, ph = 0;
      for (let k = 0; k < n; k++) {
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = AC.simulate(ids[i], ids[j], s);
        if (r.winner === names[ids[i]]) aw++;
        if (r.reason !== 'slain') timeouts++;
        durs.push(r.duration); pd += r.duration; total++;
        const hh = r.hits.a + r.hits.b;
        ph += hh;
        hitsAll.push(hh); clanksAll.push(r.clanks);
      }
      if (pd / n > worst.dur) worst.dur = pd / n, worst.pair = names[ids[i]] + '/' + names[ids[j]];
      if (ph / n < thin.hits) thin.hits = ph / n, thin.ids = [ids[i], ids[j]],
                              thin.pair = names[ids[i]] + '/' + names[ids[j]];
      tally[ids[i]].w += aw;      tally[ids[i]].g += n;
      tally[ids[j]].w += n - aw;  tally[ids[j]].g += n;
    }
  }
  const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
  const wr = {}; for (const id of ids) wr[id] = tally[id].w / tally[id].g;
  return { wr, names,
           meanDur: mean(durs), meanHits: mean(hitsAll), meanClanks: mean(clanksAll),
           timeoutRate: timeouts / total, worst, thin,
           dmg: Object.fromEntries(AC.WEAPONS.map(w => [w.id, w.dmg])) };
}
"""
SET_JS = "(m) => { for (const w of AC.WEAPONS) if (m[w.id] != null) w.dmg = m[w.id]; }"


def tune(rounds=8, n=90, pace=38.0, gain=0.55, pace_gain=0.30, seed0=424242,
         thin_floor=7.0, avg_last=5, verbose=True, game_path=None, only=None):
    hist = []; t0 = time.time()
    with game(game_path=game_path) as (page, errors):
        cur = page.evaluate("Object.fromEntries(AC.WEAPONS.map(w=>[w.id,w.dmg]))")
        start = dict(cur); best = None
        for r in range(rounds + 1):
            m = page.evaluate(MEASURE_JS, [n, seed0 + r * 7919])
            spread = (max(m["wr"].values()) - min(m["wr"].values())) * 100
            thin_hits = m["thin"]["hits"]
            cost = (spread + abs(m["meanDur"] - pace) * 1.2
                    + m["timeoutRate"] * 200
                    + max(0.0, thin_floor - thin_hits) * 7.0)
            hist.append({"round": r, "spread": round(spread, 2),
                         "meanDur": round(m["meanDur"], 2), "cost": round(cost, 2),
                         "dmg": dict(cur)})
            if best is None or cost < best[0]: best = (cost, dict(cur), m)
            if verbose:
                print(f"  round {r}: spread {spread:5.1f}pp  dur {m['meanDur']:5.1f}s  "
                      f"hits {m['meanHits']:4.1f}  clanks {m['meanClanks']:4.1f}  "
                      f"timeouts {m['timeoutRate']:.1%}  cost {cost:6.1f}"
                      f"   thinnest {m['thin']['pair']} {thin_hits:.1f} hits", flush=True)
            if r == rounds: break
            nxt = {}
            for k, v in cur.items():
                nxt[k] = v * (1.0 - gain * (m["wr"][k] - 0.5) * 2.0)
            scale = 1.0 + pace_gain * ((m["meanDur"] - pace) / pace)
            for k in nxt: nxt[k] = nxt[k] * scale
            if thin_hits < thin_floor and m["thin"]["ids"]:
                for k in m["thin"]["ids"]: nxt[k] *= 0.93
            for k in nxt: nxt[k] = round(max(1.0, nxt[k]), 2)
            if only:
                for k in nxt:
                    if k not in only: nxt[k] = start[k]
            cur = nxt
            page.evaluate(SET_JS, cur)
        tail = [h["dmg"] for h in hist[-avg_last:]]
        if len(tail) >= 2:
            avg = {k: round(sum(t[k] for t in tail) / len(tail), 2) for k in tail[0]}
            page.evaluate(SET_JS, avg)
            m_avg = page.evaluate(MEASURE_JS, [int(n * 1.5), seed0 + 99991])
            sp = (max(m_avg["wr"].values()) - min(m_avg["wr"].values())) * 100
            if verbose:
                print(f"\n  averaged last {len(tail)} rounds, re-measured on "
                      f"{int(n*1.5)} fresh seeds: spread {sp:5.1f}pp  "
                      f"dur {m_avg['meanDur']:5.1f}s", flush=True)
            best = (None, avg, m_avg)
        if errors: raise SystemExit("page errors while tuning:\n  " + "\n  ".join(errors))
    cost, dmg, m = best
    if verbose:
        print(f"\nconverged after {time.time()-t0:.0f}s")
        print(f"  spread {(max(m['wr'].values())-min(m['wr'].values()))*100:.1f}pp   "
              f"mean duration {m['meanDur']:.1f}s   mean hits {m['meanHits']:.1f}")
        for k in sorted(m["wr"], key=lambda k: -m["wr"][k]):
            print(f"  {m['names'][k]:<14} {m['wr'][k]*100:5.1f}%   "
                  f"dmg {start[k]:>6.2f} -> {dmg[k]:>6.2f}")
    return dmg, m, hist


def apply_to_html(dmg, path=None):
    path = path or GAME
    src = path.read_text(encoding="utf-8"); changed = 0
    def sub_one(wid, value, text):
        nonlocal changed
        i = text.find(f'id:"{wid}"')
        if i < 0: raise SystemExit(f"could not locate weapon id {wid}")
        j = text.find("ult:", i)
        block = text[i:j]
        new, k = re.subn(r"dmg:\s*[0-9.]+", f"dmg:{value:g}", block, count=1)
        if k != 1: raise SystemExit(f"expected exactly one dmg: for {wid}, found {k}")
        changed += 1
        return text[:i] + new + text[j:]
    for wid, value in dmg.items(): src = sub_one(wid, round(value, 2), src)
    if changed != len(dmg): raise SystemExit(f"patched {changed}, expected {len(dmg)}")
    path.write_text(src, encoding="utf-8")
    print(f"wrote {changed} damage values into {path.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--n", type=int, default=90)
    ap.add_argument("--pace", type=float, default=38.0)
    ap.add_argument("--gain", type=float, default=0.55)
    ap.add_argument("--pace-gain", type=float, default=0.30)
    ap.add_argument("--avg-last", type=int, default=5)
    ap.add_argument("--thin-floor", type=float, default=7.0)
    ap.add_argument("--game", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--seed0", type=int, default=424242)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = pathlib.Path(a.game) if a.game else None
    if path and not path.is_absolute(): path = pathlib.Path(__file__).parent / path
    only = {s.strip() for s in a.only.split(",") if s.strip()} if a.only else None
    print("=== The Sundered Crown — closed-loop tuner ===")
    print(f"target pace {a.pace}s, {a.rounds} rounds x {a.n} seeds"
          + (f"   [{path.name}]" if path else "") + "\n")
    dmg, m, hist = tune(a.rounds, a.n, a.pace, a.gain, a.pace_gain, seed0=a.seed0,
                        thin_floor=a.thin_floor, avg_last=a.avg_last,
                        game_path=path, only=only)
    print("\n" + json.dumps({"damage": dmg}, indent=1))
    if a.apply:
        # REFUSE A GENERATED FILE BY WHAT IT SAYS IT IS, not by what it is
        # called. The old guard matched -bow/-vigil/-phone/-perf in the name;
        # sc-r15.html slipped straight through it and twelve tuned values were
        # written into a file that regenerates from a builder. Builders stamp
        # GENERATED into their output; this reads that.
        if path and "<!-- GENERATED by " in path.read_text(encoding="utf-8"):
            print(f"\nREFUSED — {path.name} is GENERATED. Put these numbers in "
                  f"the builder that writes it and rebuild, or they die on the "
                  f"next build.")
            return 1
        apply_to_html(dmg, path)
    else: print("\n(not applied — pass --apply to write them into the HTML)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
