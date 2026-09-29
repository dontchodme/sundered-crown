"""v106 scratch: stage 1 (the stub) against the lab's arm A, FIGHT FOR FIGHT.

Arm A is `ult_overlay`'s: the shipped Widowmaker with `w.ult.charge = 1e9`, as
side A, seeds seed0 + 11 i. This plays exactly those fights (and the same
seeds from side B too) on the base with the charge set to 1e9 and on the stub
link untouched, and compares every field of `AC.simulate`'s summary.
A control that can fail: the base with its SHIPPED charge (the nova live)
against the stub must differ.
"""
import json, pathlib, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

base, stub, foes = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
JS = r"""([foes, seed0s, stubCharge]) => {
  const w = AC.WEAPONS.find(x => x.id === "widowmaker"), c0 = w.ult.charge;
  if (stubCharge !== null) w.ult.charge = stubCharge;
  const out = [];
  try {
    for (const s0 of seed0s) for (const f of foes) for (let i = 0; i < 20; i++){
      const sd = s0 + 11 * i;
      out.push(AC.simulate("widowmaker", f, sd)); out.push(AC.simulate(f, "widowmaker", sd));
    }
  } finally { w.ult.charge = c0; }
  return out;
}"""
res = {}
for label, path, ch in (("A", base, 1e9), ("ship", base, None), ("stub", stub, None)):
    with game(game_path=pathlib.Path(path)) as (page, errors):
        res[label] = page.evaluate(JS, [foes, [2207, 2317], ch])
        assert not errors, errors
A, S, SH = res["A"], res["stub"], res["ship"]
same = sum(1 for x, y in zip(A, S) if x == y)
ctl = sum(1 for x, y in zip(SH, S) if x != y)
print(f"stub vs arm A (base, charge 1e9): {same}/{len(A)} fights identical, every field "
      f"(33 foes x 20 seeds x 2 blocks x both sides)")
print(f"control, the shipped nova live vs the stub: {ctl}/{len(A)} fights differ (must be > 0)")
sys.exit(0 if same == len(A) and ctl > 0 else 1)
