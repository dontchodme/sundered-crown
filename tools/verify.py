#!/usr/bin/env python3
"""Falsification pass for The Sundered Crown.

The job of this file is to break the game, not to bless it. Every check states
what would count as evidence against the design, and `--selftest` deliberately
sabotages the roster first to prove the checks can actually fail.

  python3 verify.py                 # full pass
  python3 verify.py --n 40          # faster, wider error bars
  python3 verify.py --selftest      # prove the balance check can fail
"""
from __future__ import annotations

import argparse
import pathlib
import base64
import json
import statistics
import sys
import time

from scpage import game

# Bands. These are assertions about what makes a watchable spectator fight,
# not about what the code currently happens to do.
WINRATE_BAND = (0.30, 0.70)     # no relic may dominate or be a free win
# Widened 62 -> 70 and 48 -> 54 on 2026-08-11. These bands encoded the Shorts
# convention (20-60s), and Rick retired it: "leave the shorts convention. what
# im trying to create is a functional game." They are now here to catch a fight
# that has gone structurally wrong — a stalemate or a one-shot — not to keep a
# match inside a platform's runtime. Narrow them again if publishing length
# ever becomes a constraint.
DURATION_BAND = (18.0, 70.0)    # per-pairing mean
MEAN_DURATION_BAND = (28.0, 54.0)
MAX_TIMEOUT_RATE = 0.10         # a timeout is not an ending

SWEEP_JS = r"""
([n, seed0]) => {
  const ids = AC.WEAPONS.map(w => w.id);
  const names = {}; for (const w of AC.WEAPONS) names[w.id] = w.name;
  const pairs = [];
  const tally = {}; for (const id of ids) tally[id] = { w: 0, g: 0 };
  let s = seed0 >>> 0;
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      let aw = 0, bw = 0, timeouts = 0;
      const durs = [], clanks = [], hits = [];
      for (let k = 0; k < n; k++) {
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = AC.simulate(ids[i], ids[j], s);
        if (r.winner === names[ids[i]]) aw++; else bw++;
        if (r.reason !== 'slain') timeouts++;
        durs.push(r.duration); clanks.push(r.clanks);
        hits.push(r.hits.a + r.hits.b);
      }
      pairs.push({ a: ids[i], b: ids[j], n, aWins: aw, bWins: bw,
                   timeouts, durs, clanks, hits });
      tally[ids[i]].w += aw; tally[ids[i]].g += n;
      tally[ids[j]].w += bw; tally[ids[j]].g += n;
    }
  }
  return { ids, names, pairs, tally };
}
"""

# The legibility contract, checked as data rather than trusted.
# Every explanatory string a viewer can see is sourced from STATUS[k].tip and
# weapon.ult.tip. A missing tip is a silent legibility regression: the ultimate
# still fires, the sim is unaffected, every balance number stays green, and the
# viewer simply never learns what happened. That is exactly how three of the
# six ultimates shipped with no subtitle — a tip was accidentally nested inside
# the ult's `apply` object, where it also became a bogus status key.
LEGIBILITY_JS = r"""
() => {
  const bad = [];
  const statusKeys = Object.keys(AC.STATUS);
  for (const w of AC.WEAPONS) {
    const u = w.ult;
    if (!u.tip || !u.tip.trim()) bad.push(`${w.name}: ultimate ${u.name} has no tip`);
    // 44 -> 72 with the v2 fight card (2026-08-14): ult tips render on
    // their own 25px line now, so the budget is the line, not the tag row.
    // Status tips keep 40 — the in-arena first-landing panel still prints those.
    else if (u.tip.length > 72) bad.push(`${w.name}: ult tip ${u.tip.length} chars (max 72)`);
    for (const k of Object.keys(u.apply || {}))
      if (!statusKeys.includes(k))
        bad.push(`${w.name}: ult.apply has non-status key "${k}"`);
    // Both application channels, not just onHit. `onSelf` was added for the
    // seventh school (a wielder-directed buff has nowhere to live, because
    // onHit is hardcoded to the foe) -- and a new channel the contract does not
    // inspect is a new hole in it, which is precisely how three ultimates once
    // shipped with no subtitle and twelve checks green.
    for (const chan of ["onHit", "onSelf"]) {
      for (const k of Object.keys(w[chan] || {})) {
        if (!statusKeys.includes(k)) { bad.push(`${w.name}: ${chan} has unknown status "${k}"`); continue; }
        const s = AC.STATUS[k];
        if (!s.tip || !s.tip.trim()) bad.push(`${w.name}: status ${k} has no tip`);
        else if (s.tip.length > 48) bad.push(`${k}: status tip ${s.tip.length} chars (max 48)`);
      }
    }
    // ...and now the RENDER check, not just the data check. The above proves a
    // tip exists. It does not prove the fight card can FIND it, and those are
    // different claims: Lightkeeper shipped with a blank status line on its card
    // while every one of these checks stayed green, because the card had its own
    // private copy of the lookup that only knew about `onHit`.
    // So call the same function the card calls. If they ever diverge again, this
    // fails instead of the viewer.
    const rs = AC.relicStatus ? AC.relicStatus(w)
                              : { key: Object.keys(w.onHit || {})[0] };
    if (!rs.key) bad.push(`${w.name}: the fight card has no status to show`);
    else if (!statusKeys.includes(rs.key))
      bad.push(`${w.name}: card status "${rs.key}" is not in STATUS`);

    // RANGED. A projectile is a mechanic, so under rule 1 it ships with its
    // explanation in the same change. This is EXTENDING the contract, not
    // widening it: a new mechanic gets a new requirement, and the existing
    // requirements are untouched.
    //
    // Same standing rule as the status lookup above -- call the function the
    // renderer calls, because a check that does not is checking a different
    // thing. `relicShot` is what the fight card asks whether to print a SHOOTS
    // line and whether the REACH bar is lying.
    //
    // A bow's `reach` is 54, the shortest in the game, and the card normalises
    // that bar across the roster. Left alone it teaches a first-time viewer the
    // OPPOSITE of the truth about the relic with the longest effective range in
    // the game, so `mode:"ranged"` without the card treatment is a legibility
    // failure that no balance number would ever surface.
    if (w.mode === "ranged" && !AC.relicShot)
      bad.push(`${w.name}: mode "ranged" but the build has no relicShot()`);
    const sh = AC.relicShot ? AC.relicShot(w) : null;
    if (w.mode === "ranged" && !sh)
      bad.push(`${w.name}: mode "ranged" but no shot definition`);
    if (sh) {
      if (!sh.tip || !sh.tip.trim()) bad.push(`${w.name}: the shot has no tip`);
      // 46, not 40: the shot line sits on its own full-width band under the
      // stat bars rather than in the narrow status column, and the cap exists
      // to protect the layout rather than as a style rule. Stated here because
      // an unexplained different number is how a check quietly becomes wider.
      else if (sh.tip.length > 46)
        bad.push(`${w.name}: shot tip ${sh.tip.length} chars (max 46)`);
      if (!(sh.speed > 0)) bad.push(`${w.name}: shot has no speed — a hitscan shot cannot be clanked`);
      if (!(sh.cadence > 0)) bad.push(`${w.name}: shot has no cadence`);
      if (!(sh.r > 0)) bad.push(`${w.name}: shot has no radius`);
      if (!(sh.life > 0)) bad.push(`${w.name}: shot has no lifetime — it would never expire`);
    }
  }
  return bad;
}
"""

RENDER_JS = r"""
() => {
  window.__frozen = true;
  // The live page now sizes its backing store to the pixels actually on
  // screen, so a headless 620x1000 viewport would otherwise be photographed at
  // 348x620. The video's resolution is a property of the capture path, not of
  // whatever window a harness opened, so state it.
  const pinned = AC.setResolution(1080, 1920);
  const m = new AC.Match('grudgebearer', 'spellbreaker', 987654321);
  AC.__inject(m);
  for (let i = 0; i < 1800; i++) m.step(AC.CONFIG.physics.dt);   // 15s in
  AC.__draw(m);
  const cv = document.getElementById('cv');
  const g = cv.getContext('2d');
  // Sample a coarse grid and count distinct colours. A blank or single-colour
  // canvas means the renderer silently drew nothing.
  const seen = new Set();
  for (let y = 0; y < cv.height; y += 37) {
    for (let x = 0; x < cv.width; x += 37) {
      const d = g.getImageData(x, y, 1, 1).data;
      seen.add((d[0] >> 3) + ',' + (d[1] >> 3) + ',' + (d[2] >> 3));
    }
  }
  return { colours: seen.size, w: cv.width, h: cv.height, k: pinned.k,
           png: cv.toDataURL('image/jpeg', 0.9).slice(23) };
}
"""


class Check:
    def __init__(self):
        self.rows = []

    def add(self, ok, name, detail=""):
        self.rows.append((bool(ok), name, detail))
        return ok

    @property
    def failed(self):
        return [r for r in self.rows if not r[0]]

    def report(self):
        for ok, name, detail in self.rows:
            print(f"  {'PASS' if ok else 'FAIL'}  {name}"
                  + (f"  — {detail}" if detail else ""))
        n = len(self.rows)
        f = len(self.failed)
        print(f"\n{n - f}/{n} checks passed"
              + ("" if not f else f"  ({f} FAILED)"))


def run(n=60, seed0=20260811, sabotage=None, write_frame=None, game_path=None):
    t0 = time.time()
    c = Check()

    with game(game_path=game_path) as (page, errors):
        if sabotage:
            page.evaluate(
                "([id,mul]) => { const w = AC.WEAPONS.find(w=>w.id===id); w.dmg *= mul; }",
                list(sabotage),
            )
            print(f"!! sabotage: {sabotage[0]}.dmg x{sabotage[1]}\n")

        data = page.evaluate(SWEEP_JS, [n, seed0])
        rend = page.evaluate(RENDER_JS)
        legib = page.evaluate(LEGIBILITY_JS)

        # Page errors are checked last so a thrown exception during the sweep
        # is attributed here rather than silently producing tidy numbers.
        c.add(not errors, "no JS errors or page exceptions",
              "; ".join(errors[:3]) if errors else "")

    pairs, tally, names = data["pairs"], data["tally"], data["names"]

    # --- legibility ---------------------------------------------------------
    # First law, checked first. A mechanic the viewer cannot read is a defect
    # even when every number is green.
    c.add(not legib, "every status and ultimate has viewer-facing text",
          "; ".join(legib[:4]) + (f" (+{len(legib)-4} more)" if len(legib) > 4 else ""))

    # --- resolution ---------------------------------------------------------
    # Was hardcoded to 15, which encoded "the roster is six relics" rather than
    # the requirement, which is "the complete round robin ran". The roster is a
    # variable now (see the weapon-matrix plan), so it is derived. This is not a
    # widening: the check still demands every pairing, it just stopped asserting
    # the roster size as a side effect.
    want = len(data["ids"]) * (len(data["ids"]) - 1) // 2
    c.add(len(pairs) == want, f"all {want} pairings ran", f"{len(pairs)} pairings")

    unresolved = [p for p in pairs if p["aWins"] + p["bWins"] != p["n"]]
    c.add(not unresolved, "every match resolved",
          f"{len(unresolved)} pairings had unresolved matches")

    # --- both sides can win -------------------------------------------------
    deterministic = [f"{names[p['a']]} vs {names[p['b']]} "
                     f"{p['aWins']}/{p['bWins']}"
                     for p in pairs if p["aWins"] == 0 or p["bWins"] == 0]
    c.add(not deterministic, "both sides can win every matchup",
          "; ".join(deterministic))

    # --- timeouts -----------------------------------------------------------
    tos = sum(p["timeouts"] for p in pairs)
    total = sum(p["n"] for p in pairs)
    c.add(tos / total <= MAX_TIMEOUT_RATE,
          f"timeout rate <= {MAX_TIMEOUT_RATE:.0%}",
          f"{tos}/{total} = {tos/total:.1%}")

    # --- balance ------------------------------------------------------------
    wr = {k: v["w"] / v["g"] for k, v in tally.items()}
    lo_k = min(wr, key=wr.get)
    hi_k = max(wr, key=wr.get)
    band_ok = all(WINRATE_BAND[0] <= v <= WINRATE_BAND[1] for v in wr.values())
    c.add(band_ok,
          f"every relic winrate in {WINRATE_BAND[0]:.0%}-{WINRATE_BAND[1]:.0%}",
          f"{names[lo_k]} {wr[lo_k]:.1%} .. {names[hi_k]} {wr[hi_k]:.1%} "
          f"(spread {(wr[hi_k]-wr[lo_k])*100:.1f}pp)")

    # --- pace ---------------------------------------------------------------
    pair_means = [statistics.mean(p["durs"]) for p in pairs]
    slowest = pairs[pair_means.index(max(pair_means))]
    fastest = pairs[pair_means.index(min(pair_means))]
    c.add(all(DURATION_BAND[0] <= d <= DURATION_BAND[1] for d in pair_means),
          f"every pairing mean duration in {DURATION_BAND[0]:.0f}-{DURATION_BAND[1]:.0f}s",
          f"{names[fastest['a']]}/{names[fastest['b']]} {min(pair_means):.1f}s .. "
          f"{names[slowest['a']]}/{names[slowest['b']]} {max(pair_means):.1f}s")

    overall = statistics.mean(pair_means)
    c.add(MEAN_DURATION_BAND[0] <= overall <= MEAN_DURATION_BAND[1],
          f"overall mean duration in {MEAN_DURATION_BAND[0]:.0f}-{MEAN_DURATION_BAND[1]:.0f}s",
          f"{overall:.1f}s")

    # --- clanks -------------------------------------------------------------
    noclank = [f"{names[p['a']]}/{names[p['b']]}"
               for p in pairs if max(p["clanks"]) == 0]
    c.add(not noclank, "every pairing clanks at least once", "; ".join(noclank))
    mean_clanks = statistics.mean(statistics.mean(p["clanks"]) for p in pairs)

    # --- contact ------------------------------------------------------------
    thin = [f"{names[p['a']]}/{names[p['b']]} {statistics.mean(p['hits']):.1f}"
            for p in pairs if statistics.mean(p["hits"]) < 6]
    c.add(not thin, "no pairing resolves on fewer than 6 hits", "; ".join(thin))

    # --- render -------------------------------------------------------------
    # Was "canvas is 1080x1920", asserted against the element's fixed width.
    # The requirement it encodes has not changed — the VIDEO must be 1080x1920 —
    # but the live page no longer renders at that size, so the check now asserts
    # that the capture path can pin it and that the pin took effect end to end.
    c.add(rend["w"] == 1080 and rend["h"] == 1920 and abs(rend["k"] - 1.0) < 1e-9,
          "capture path pins the canvas to 1080x1920",
          f"{rend['w']}x{rend['h']} k={rend['k']}")
    c.add(rend["colours"] > 40, "renderer draws a non-blank frame",
          f"{rend['colours']} distinct sampled colours")
    if write_frame:
        open(write_frame, "wb").write(base64.b64decode(rend["png"]))

    # The pairing count was hardcoded to 15, the same way `len(pairs) == 15`
    # was: it encoded "the roster is six relics" rather than the requirement.
    # It is only a log line, but a log line that says "15 pairings" above a
    # check that says "21 pairings ran" is a harness telling you two different
    # things about the same sweep, and the whole point of this file is that you
    # can believe what it prints.
    print(f"\n# sweep: {total} matches in {time.time()-t0:.1f}s "
          f"({n} seeds x {len(pairs)} pairings)")
    print(f"# mean duration {overall:.1f}s   mean clanks {mean_clanks:.1f}\n")
    for k in sorted(wr, key=lambda k: -wr[k]):
        bar = "#" * round(wr[k] * 50)
        print(f"  {names[k]:<14} {wr[k]*100:5.1f}%  {bar}")
    print()
    c.report()
    return c, {"winrate": wr, "meanDur": overall, "meanClanks": mean_clanks}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60, help="seeds per pairing")
    ap.add_argument("--seed", type=int, default=20260811)
    ap.add_argument("--frame", default=None, help="write the render-check frame here")
    ap.add_argument("--game", default=None,
                    help="verify a variant HTML instead of sundered-crown.html")
    ap.add_argument("--selftest", action="store_true",
                    help="sabotage the roster first and require the balance check to fail")
    a = ap.parse_args()

    if a.selftest:
        print("=== SELFTEST: the balance check must FAIL on a sabotaged roster ===\n")
        c, _ = run(n=max(20, a.n // 3), seed0=a.seed, sabotage=("grudgebearer", 6.0),
                   game_path=pathlib.Path(a.game).resolve() if a.game else None)
        names = [r[1] for r in c.failed]
        want = "every relic winrate"
        if any(want in nm for nm in names):
            print(f"\nSELFTEST PASS — the balance check failed for the right reason.")
            return 0
        print(f"\nSELFTEST FAIL — sabotage did not trip the balance check. "
              f"The check is not measuring what it claims.", file=sys.stderr)
        return 2

    print("=== The Sundered Crown — falsification pass ===\n")
    c, summary = run(n=a.n, seed0=a.seed, write_frame=a.frame,
                     game_path=pathlib.Path(a.game).resolve() if a.game else None)
    if c.failed:
        print("\n" + json.dumps(summary, indent=1), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
