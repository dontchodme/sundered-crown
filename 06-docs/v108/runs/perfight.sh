#!/bin/bash
# stage 1 against the lab's arm A FIGHT BY FIGHT (the review's note 4): arm A on the base and the
# stub's own ultimate (SHIP) on sc-ironhail-stub, same 33 foes x 20 seeds, both blocks, every row kept
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
for B in 2207 2317; do
  $PY $S/tools/perfight_overlay.py --game ../02-chain/sc-tendril-t3.html --relic ironhail --mech overlays/hail.js --arms A --P fallT=0.3 hitR=60 dropDmg=4 --seeds 20 --seed0 $B --foes $(cat $S/runs/foes33.txt) --label "per-fight arm A block $B" --out $S/runs/pf_A_$B.json > $S/runs/pf_A_$B.txt 2>&1
  $PY $S/tools/perfight_overlay.py --game $S/links/sc-ironhail-stub.html --relic ironhail --mech overlays/hail.js --arms SHIP --seeds 20 --seed0 $B --foes $(cat $S/runs/foes33.txt) --label "per-fight stub block $B" --out $S/runs/pf_stub_$B.json > $S/runs/pf_stub_$B.txt 2>&1
done
$PY - <<PYEOF > $S/runs/stage1_vs_A_perfight.txt
import json
S = "$S/runs"
print("STAGE 1 (sc-ironhail-stub, SHIP arm = its own stubbed ultimate) AGAINST THE LAB'S ARM A (base), FIGHT BY FIGHT")
print("(perfight_overlay.py = ult_overlay.py + every fight's row; 33 foes x 20 seeds, Ironhail side A)\n")
allok = True
for B in ("2207", "2317"):
    A = json.load(open(f"{S}/pf_A_{B}.json"))["rows"]; T = json.load(open(f"{S}/pf_stub_{B}.json"))["rows"]
    key = lambda r: (r["foe"], r["seed"])
    a = {key(r): r for r in A}; t = {key(r): r for r in T}
    diff = [k for k in a if k not in t or any(a[k][f] != t[k][f] for f in ("win", "dur", "hitsIn", "hitsOut", "casts"))]
    ok = len(a) == len(t) == len(A) == len(T) and not diff
    allok &= ok
    wa = sum(r["win"] == 1 for r in A); wt = sum(r["win"] == 1 for r in T)
    print(f"block {B}: {len(A)} / {len(T)} fights; wins {wa} / {wt}; fights differing in winner, duration (to the step), "
          f"blows in/out or casts: {len(diff)}  -> {'IDENTICAL FIGHT BY FIGHT' if ok else 'DIFFERENT: ' + str(diff[:5])}")
print("\nSTAGE 1 IS ARM A FIGHT BY FIGHT" if allok else "\nSTAGE 1 IS NOT ARM A")
PYEOF
cat $S/runs/stage1_vs_A_perfight.txt
