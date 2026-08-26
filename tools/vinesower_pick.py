#!/usr/bin/env python3
"""WHICH VINESOWER FIGHT IS WORTH FILMING.

    python3 vinesower_pick.py --game ../02-chain/sc-vinesower-frame.html

`cinema_pick.py` is the ancestor and it is hardcoded to `sc-cinema.html` and to
eight pairings that predate half the roster. This is the same idea pointed at
one relic, with one addition that matters for THIS relic:

    A CUT LIST IS NOT ENOUGH. The Thicket is a slow bloom -- seeds for 8.1s, a
    1s sprout, and plants that live 14.1s after that. A fight the director
    scores highly but that ENDS before the garden is up demonstrates nothing,
    and a fight where the ultimate never fires demonstrates less than nothing.

So every candidate is simulated as well as planned, and the columns that decide
are: does it cast, how many plants stand at the peak, how many lashes land, and
does the kill happen while the garden is on screen.

THE MIRROR IS EXCLUDED BY CONSTRUCTION. Thornwake and Heartwood are verdant and
`verdant_bow_probe` rendered what that looks like: two green balls, v28's
same-affinity smudge. They are not in the foe list and the reason is in the
list, not in a comment somewhere else.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "vinesower"

JS = r"""([rid, foes, n, seed0, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let s = seed0 >>> 0;
  const out = [];
  for (const b of foes){
    for (let k = 0; k < n; k++){
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const p = window.cinePlan(rid, b, s);
      if (p.err) continue;

      /* AND THEN ACTUALLY RUN IT. The plan is the director's opinion; this is
         what the garden did. */
      const m  = new AC.Match(rid, b, s);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let whips = 0, peak = 0, castAt = -1, firstBloomAt = -1, inVine = false;
      let dVine = 0;
      const oR = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, ov){
        const d0 = self.dealt;
        const r = oR.call(m, self, foe2, hx, hy, seg, mul, ov);
        if (inVine && self === me) dVine += self.dealt - d0;
        return r;
      };
      const oT = AC.Match.prototype.tickVines;
      m.tickVines = function(dt){
        inVine = true;
        const before = m.vines.map(v => ({ v, w: v.whips }));
        const r = oT.call(m, dt);
        inVine = false;
        for (const q of before) if (q.v.whips > q.w) whips++;
        const armed = m.vines.filter(v => v.t >= v.sprout).length;
        if (armed > peak) peak = armed;
        if (armed > 0 && firstBloomAt < 0) firstBloomAt = m.t;
        return r;
      };
      let st = 0;
      while (!m.over && st < secs / DT){
        const had = !!me.ultBloom;
        m.step(DT); st++;
        if (!had && me.ultBloom && castAt < 0) castAt = m.t;
      }
      const dur = st * DT;
      const kill = p.cuts.find(c => c.fatal);
      out.push({ b, seed: s, dur: +dur.toFixed(1), cuts: p.cuts.length,
                 kill: !!kill, won: m.winner === me,
                 castAt: +castAt.toFixed(1),
                 bloomAt: +firstBloomAt.toFixed(1),
                 peak, whips, dVine: Math.round(dVine),
                 /* the garden is still standing at the finish */
                 liveAtEnd: m.vines.filter(v => v.t >= v.sprout).length,
                 hpEnd: Math.round(th.hp),
                 list: p.cuts.map(c => ({ t: +c.t.toFixed(1),
                                          tier: c.fatal ? "KILL" : "T" + c.tier,
                                          score: +c.score.toFixed(2),
                                          kind: c.kind || "hit",
                                          why: (c.why || []).join(", ") })) });
    }
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-vinesower-frame.html")
    ap.add_argument("--n", type=int, default=22)
    ap.add_argument("--seed0", type=lambda x: int(x, 0), default=0xF11E)
    ap.add_argument("--secs", type=float, default=85.0)
    ap.add_argument("--show", type=int, default=8)
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    gp = (HERE / A.game).resolve()
    # NOT thornwake, NOT heartwood: verdant on verdant is v28's smudge and
    # verdant_bow_probe rendered it. Everything else spans the parry column
    # (bow_survey §2.2, 5.9% to 12.0%) and four different palettes.
    FOES = ["grudgebearer",   # dwarven warhammer, orange, parries least
            "widowmaker",     # bloodsworn twinblade, red, parries most
            "twinshade",      # umbral twinblade, purple
            "emberedge",      # dwarven greatsword, orange
            "censer",         # sanctified warhammer, white
            "gravemourn"]     # umbral flail, purple

    with game(game_path=gp) as (page, errors):
        rows = page.evaluate(JS, [RID, FOES, A.n, A.seed0, A.secs])
        assert not errors, errors[:3]

    # WHAT MAKES A CLIP: the ultimate has to fire early enough that the garden
    # is up for the back half, the garden has to be a real one, the lashes have
    # to land, and the finish has to be a cut the director will take.
    good = [r for r in rows
            if r["castAt"] > 0 and r["peak"] >= 5 and r["whips"] >= 6
            and 26 <= r["dur"] <= 55 and r["cuts"] >= 3]
    good.sort(key=lambda r: (-int(r["kill"]), -int(r["won"]),
                             -r["peak"], -r["cuts"], -r["whips"]))
    print(f"\n{len(rows)} fights planned and simulated, {len(good)} filmable\n")
    print(f"    {'foe':<14}{'seed':>10}{'dur':>7}{'cuts':>6}{'kill':>6}"
          f"{'won':>6}{'cast':>7}{'bloom':>7}{'peak':>6}{'whips':>7}"
          f"{'vine dmg':>10}{'garden at end':>15}")
    seen, shortlist = set(), []
    for r in good:
        if r["b"] in seen:
            continue
        seen.add(r["b"]); shortlist.append(r)
        print(f"    {r['b']:<14}{r['seed']:>10}{r['dur']:>6.1f}s{r['cuts']:>6}"
              f"{'Y' if r['kill'] else '-':>6}{'Y' if r['won'] else '-':>6}"
              f"{r['castAt']:>6.1f}s{r['bloomAt']:>6.1f}s{r['peak']:>6}"
              f"{r['whips']:>7}{r['dVine']:>10}{r['liveAtEnd']:>15}")
        if len(shortlist) >= A.show:
            break

    if shortlist:
        top = shortlist[0]
        print(f"\n    THE CUT LIST for {RID} v {top['b']}, seed {top['seed']}:\n")
        for c in top["list"]:
            print(f"      {c['t']:>6.1f}s  {c['tier']:<5}{c['score']:>7.2f}  "
                  f"{c['kind']:<9}{c['why']}")
        print(f"\n    render:")
        print(f"      python3 cinema_clip.py --game {A.game} \\")
        print(f"        --a {RID} --b {top['b']} --seed {top['seed']} --full \\")
        print(f"        --fps 60 --w 540 --q 0.80 --out ../07-shorts/v40/thicket-full.mp4")
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(shortlist, indent=1))
        print(f"    wrote {A.json}")
    return 0 if shortlist else 1


if __name__ == "__main__":
    sys.exit(main())
