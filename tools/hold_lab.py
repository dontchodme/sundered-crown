#!/usr/bin/env python3
"""HOW LONG DOES THE WIRE ACTUALLY HOLD, AND WHAT WOULD A CAP COST?

    python hold_lab.py --game ../02-chain/sc-garrote.html --sn 8

Rick, 2026-09-01, on the shipped clip: *"the hold needs to expire if the hammer
doesn't hit in time."*

As built there is no cap. A catch is released by exactly two things -- the
connect, or the window running out -- so a quarry the head never reaches is
held for the remainder of the eight seconds. `garrote_relic_probe` reports 22
windows of 337 letting go without a connect, and a MEAN hold of 1.85s, and a
mean is the wrong statistic for a question about a tail.

**THE DESIGN SAYS THE HOLD SHOULD BE SHORT BY CONSTRUCTION.** `wirering-design
-v60.md` §0: *"The hold's length is not a number. It is however long the head
takes to come around."* At `spin` 1.6 x `spinMul` 6 that is **9.6 rad/s, one
revolution every 0.65s** -- so a hold of more than about a second means the
head is coming round and MISSING, which it does because the quarry is pinned at
up to 144 units between centres while the head reaches about 110. The wielder
has to drift in. When it does not, the wire just holds.

SO THIS PRICES EVERY CANDIDATE CAP AT ONCE, off ONE run, rather than sweeping
builds. Each catch is recorded as `(seconds held, did it connect)`; a cap of T
would have released every catch that ran past T, so the connects that survive a
cap are exactly those whose hold was <= T. That is an upper bound on what a cap
costs -- a released quarry is free to be caught again by a LATER cast, which
this cannot see and which can only help.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "ravelbone"

HOLDS_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const M = AC.Match.prototype;
  const origHit = M.resolveHit;
  const holds = [];          // [secondsHeld, connected]
  let casts = 0, fights = 0;
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a;
      fights++;
      let connectedThisCatch = false;
      m.resolveHit = function (self, foe, hx, hy, seg, mul, over){
        if (self === me && me.ultWire && me.ultWire.caught && foe.pinFree
            && !foe.shade && mul === undefined) connectedThisCatch = true;
        return origHit.apply(this, arguments);
      };
      let i = 0, held = 0, wasCaught = false, hadWire = false;
      while (!m.over && i < secs / DT){
        const W0 = me.ultWire;
        const caught0 = !!(W0 && W0.caught);
        m.step(DT); i++;
        const W = me.ultWire;
        if (W && !hadWire) casts++;
        hadWire = !!W;
        const caught = !!(W && W.caught);
        if (caught){ held += DT; wasCaught = true; }
        /* THE CATCH ENDED. Either the connect resolved it (in which case
           `connectedThisCatch` was set inside `resolveHit` on this very step)
           or the window ran out and it was let go. */
        if (wasCaught && !caught){
          holds.push([+held.toFixed(4), connectedThisCatch ? 1 : 0]);
          held = 0; wasCaught = false; connectedThisCatch = false;
        }
      }
      /* a catch still standing when the clock ran out */
      if (wasCaught) holds.push([+held.toFixed(4), connectedThisCatch ? 1 : 0]);
      m.resolveHit = origHit;
    }
  }
  M.resolveHit = origHit;
  return { holds, casts, fights };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-garrote.html")
    ap.add_argument("--sn", type=int, default=8, help="seeds a pairing")
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [7717 + 419 * i for i in range(a.sn)]
    print(f"\nTHE HOLD, AND WHAT A CAP WOULD COST — {gp.name}")

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if RID not in ids:
            raise SystemExit(f"{RID} is not in this build")
        U = page.evaluate("(r) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(w=>w.id===r).ult))", RID)
        W = page.evaluate("(r) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(w=>w.id===r)))", RID)
        foes = [i for i in ids if i != RID]
        print(f"  {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes)*len(seeds)} fights   dur {U['dur']:g}s  "
              f"spinMul {U['spinMul']:g}  holdMax "
              f"{U.get('holdMax', '(none)')}")
        rev = 2 * 3.141592653589793 / (W["spin"] * U["spinMul"])
        print(f"  one revolution at spin {W['spin']:g} x {U['spinMul']:g} "
              f"= {rev:.2f}s\n")
        R = page.evaluate(HOLDS_JS, [RID, foes, seeds, a.secs])
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))

    holds = R["holds"]
    if not holds:
        raise SystemExit("no catches recorded")
    holds.sort()
    n = len(holds)
    conn = [h for h, c in holds if c]
    miss = [h for h, c in holds if not c]

    def pct(p):
        return holds[min(n - 1, int(p * n))][0]

    print(f"  {n} catches over {R['casts']} casts and {R['fights']} fights\n")
    print(f"  ALL CATCHES        p10 {pct(0.10):.2f}s   median "
          f"{pct(0.50):.2f}s   p90 {pct(0.90):.2f}s   max "
          f"{holds[-1][0]:.2f}s")
    if conn:
        conn.sort()
        print(f"  THAT CONNECTED     n {len(conn):<4} median "
              f"{conn[len(conn)//2]:.2f}s   p90 "
              f"{conn[int(0.9*len(conn))]:.2f}s   max {conn[-1]:.2f}s")
    if miss:
        miss.sort()
        print(f"  THAT NEVER DID     n {len(miss):<4} median "
              f"{miss[len(miss)//2]:.2f}s   p90 "
              f"{miss[int(0.9*len(miss))]:.2f}s   max {miss[-1]:.2f}s")
        print(f"                     and they are dead weight: the wire holds "
              f"a quarry the head\n                     never reaches, for a "
              f"total of {sum(miss):.0f}s across this run")

    print(f"\n  WHAT A CAP WOULD COST. A cap of T releases every catch that ran"
          f" past T, so\n  the connects it keeps are those whose hold was <= T."
          f" This is an UPPER bound\n  on the cost -- a released quarry can be"
          f" caught again by a later cast.\n")
    print("    holdMax    connects kept    of all catches    dead hold cut")
    total_conn = len(conn)
    dead = sum(miss)
    for T in (0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0):
        kept = sum(1 for h in conn if h <= T + 1e-9)
        # seconds of NON-connecting hold a cap of T removes
        cut = sum(max(0.0, h - T) for h in miss)
        print(f"    {T:>5.2f}s    {kept:>5} / {total_conn:<5} "
              f"{100*kept/max(1,total_conn):>5.1f}%   "
              f"{100*kept/max(1,n):>5.1f}%          "
              f"{cut:>6.0f}s of {dead:.0f}s")

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"holds": holds, "casts": R["casts"], "fights": R["fights"],
             "ult": U}, indent=1), encoding="utf-8")
        print(f"\n  wrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
