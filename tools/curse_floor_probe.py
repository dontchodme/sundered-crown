#!/usr/bin/env python3
"""INDEPENDENT re-derivation of the Curse floor. Nothing is written.

v36 §3 claimed: `Fighter.apply` caps the STACK COUNTER at 8 and reduces max hp
OUTSIDE that cap, so the drain runs past the displayed ceiling to a floor of
60 of 300 — and therefore CURSE CANNOT KILL.

That claim is load-bearing for any ultimate designed on this school, so it is
re-derived here by a different instrument than the one that made it, reading
the engine's own numbers rather than v36's prose.

  [A] THE STACK CAP vs THE DRAIN — apply() N times with no match in the way.
  [B] THE FLOOR — where maxHp stops falling, and what fraction of baseHP it is.
  [C] CAN CURSE KILL — drive maxHp to the floor and ask whether `hp` ever
      reaches 0 from the clamp alone. If it cannot, an ult that wins by taking
      maximum life has a wall, and the wall is worth knowing before design.
  [D] WHAT THE PLAYER IS TOLD — the tip string, the mote count, the chip.
"""
from __future__ import annotations
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

DRAIN_JS = """([maxN]) => {
  // A match is needed to construct Fighters, but it is never stepped: this
  // isolates apply() from every other source of hp change in the sim.
  const rows = [];
  for (let n = 0; n <= maxN; n++){
    const m = new AC.Match("gravemourn", "thornwake", 4242);
    const t = m.b;
    const base = t.maxHp, baseHp = t.hp;
    for (let i = 0; i < n; i++) t.apply("curse", 1);
    rows.push({ n, stacks: t.stacks("curse"), maxHp: Math.round(t.maxHp),
                hp: Math.round(t.hp), base, baseHp, alive: !!t.alive });
  }
  return rows;
}"""

TIP_JS = """() => {
  const s = AC.STATUS && AC.STATUS.curse;
  const out = { status: s ? JSON.parse(JSON.stringify(s)) : null };
  // every relic that applies curse, and what its card says
  out.appliers = AC.WEAPONS.filter(w =>
      (w.onHit && w.onHit.curse) ||
      (w.ult && w.ult.apply && w.ult.apply.curse))
    .map(w => ({ id: w.id, name: w.name, aff: w.aff, shape: w.shape,
                 onHit: w.onHit || null,
                 ultApply: (w.ult && w.ult.apply) || null }));
  out.spenders = AC.WEAPONS.filter(w => {
      const j = JSON.stringify(w.ult || {});
      return /consume|spend|detonat|drain/i.test(j);
    }).map(w => w.id);
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-health18.html")
    ap.add_argument("--max", type=int, default=26)
    A = ap.parse_args()
    g = (HERE / A.game).resolve()

    ok = {}
    with game(game_path=g) as (page, errors):
        rows = page.evaluate(DRAIN_JS, [A.max])
        info = page.evaluate(TIP_JS)

    base = rows[0]["base"]
    print(f"game  {g.name}   baseHP {base}\n")
    print("[A] apply('curse') N times, match never stepped")
    print(f"    {'applications':>12} {'stacks':>7} {'maxHp':>7} {'lost':>6} {'hp':>6} {'alive':>6}")
    prev = None
    floor_at = None
    for r in rows:
        mark = ""
        if prev is not None and r["maxHp"] == prev and floor_at is None:
            floor_at = r["n"] - 1
            mark = "   <-- maxHp stops falling"
        if r["stacks"] == 8 and (prev_st := None) is None:
            pass
        print(f"    {r['n']:>12} {r['stacks']:>7} {r['maxHp']:>7} "
              f"{r['base']-r['maxHp']:>6} {r['hp']:>6} {str(r['alive']):>6}{mark}")
        prev = r["maxHp"]

    cap = max(r["stacks"] for r in rows)
    floor = min(r["maxHp"] for r in rows)
    stopped = next((r["n"] for r in rows if r["stacks"] == cap), None)
    print(f"\n[B] stack counter caps at {cap} (first reached at N={stopped})")
    print(f"    maxHp floor is {floor} of {base}  = {100*floor/base:.0f}% of baseHP")
    ok["drain_exceeds_cap"] = rows[-1]["maxHp"] < rows[stopped]["maxHp"]
    print(f"    drain continues past the stack cap:  "
          f"{'CONFIRMED' if ok['drain_exceeds_cap'] else 'REFUTED'}"
          f"   (maxHp {rows[stopped]['maxHp']} at N={stopped} -> {rows[-1]['maxHp']} at N={rows[-1]['n']})")

    print(f"\n[C] can curse kill?")
    dead = [r for r in rows if not r["alive"] or r["hp"] <= 0]
    ok["cannot_kill"] = not dead
    print(f"    fighters killed by {A.max} applications alone: {len(dead)}")
    print(f"    lowest hp reached: {min(r['hp'] for r in rows)}")
    print(f"    CURSE CANNOT KILL:  "
          f"{'CONFIRMED' if ok['cannot_kill'] else 'REFUTED — it killed'}")
    print(f"    -> the last {floor} hp of any foe must come off as DAMAGE.")

    print(f"\n[D] what the player is told")
    print(f"    STATUS.curse = {info['status']}")
    print(f"    appliers ({len(info['appliers'])}):")
    for a in info["appliers"]:
        print(f"      {a['name']:<14} {a['aff']:<11} {a['shape']:<11} "
              f"onHit={a['onHit']}  ult={a['ultApply']}")
    print(f"    anything that SPENDS/detonates curse: "
          f"{info['spenders'] or 'NONE'}")
    ok["no_spender"] = not info["spenders"]

    if errors:
        print("\nPAGE ERRORS:"); [print("   ", e) for e in errors[:5]]
        ok["clean"] = False
    else:
        ok["clean"] = True

    print("\n" + "=" * 58)
    for k, v in ok.items():
        print(f"  {k:<20} {'PASS' if v else 'FAIL'}")
    print("=" * 58)
    print("NOTHING WAS WRITTEN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
