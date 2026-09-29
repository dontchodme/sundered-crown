"""Does a scratch variant CHANGE Censer's fights? AC.simulate, Censer against every other
relic, both sides, n seeds, on two builds one after the other; counts results that differ field for field.
    python fightdiff.py A.html B.html [n]"""
import sys, pathlib, json
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
JS = r"""([n]) => { const ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "censer"); const out = []; let s = 7109;
  for (const f of ids) for (let k = 0; k < n; k++){ s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    out.push(AC.simulate("censer", f, s)); out.push(AC.simulate(f, "censer", s)); } return out; }"""
n = int(sys.argv[3]) if len(sys.argv) > 3 else 3
res = []
for g in sys.argv[1:3]:
    with game(game_path=pathlib.Path(g).resolve()) as (page, errors):
        res.append(page.evaluate(JS, [n])); assert not errors, errors
a, b = res
d = sum(1 for x, y in zip(a, b) if x != y)
wa = sum(1 for r in a if r["winner"] == "Censer"); wb = sum(1 for r in b if r["winner"] == "Censer")
print(f"{pathlib.Path(sys.argv[2]).name} vs {pathlib.Path(sys.argv[1]).name}: {d}/{len(a)} fights differ; Censer wins {wa} -> {wb}")
