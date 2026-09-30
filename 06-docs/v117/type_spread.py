"""v117 §5: each batch relic's win rate BY FOE TYPE on the game roster (items 12/32's instrument).
    python type_spread.py <roster.html> <out.json>
relic_rate.py both sides, n 10, seed block 2207, one run per relic, four at a time."""
import json, pathlib, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
PY = sys.executable
TOOLS = pathlib.Path("C:/dev/sundered-crown/tools")
RELICS = "axiom morningstar ironwood portcullis bindweed coldiron ironhail lodestone widowmaker oracle angelus lightkeeper censer aureole spellbreaker heartwood thornwake oathwound".split()
game, out = sys.argv[1], pathlib.Path(sys.argv[2])
tmp = pathlib.Path(tempfile.mkdtemp())
def one(r):
    j = tmp / f"{r}.json"
    subprocess.run([PY, "relic_rate.py", "--game", game, "--relic", r, "--n", "10", "--seed0", "2207", "--json", str(j)],
                   cwd=TOOLS, capture_output=True, text=True, check=True)
    d = json.loads(j.read_text())
    bt = d["byType"]
    lo, hi = min(bt, key=bt.get), max(bt, key=bt.get)
    return {"relic": r, "rate": d["rate"], "byType": bt, "low": [lo, bt[lo]], "high": [hi, bt[hi]], "spread": bt[hi] - bt[lo]}
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, RELICS))
out.write_text(json.dumps(res, indent=1))
print(f"{'relic':<13} {'rate':>6}  {'spread':>7}   worst type        best type")
for x in sorted(res, key=lambda x: -x["spread"]):
    print(f"{x['relic']:<13} {x['rate']*100:5.1f}%  {x['spread']*100:6.1f}pp   {x['low'][0]:<9} {x['low'][1]*100:5.1f}%   {x['high'][0]:<9} {x['high'][1]*100:5.1f}%")
