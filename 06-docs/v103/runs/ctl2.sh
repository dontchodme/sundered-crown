#!/bin/bash
# stage 2's gap, two more blocks: the lab's B at dur 8 and 9.4, the built stage 2 and its lab-clock variant
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
FOES=$(cat "$S/runs/foes33.txt")
cd C:/dev/sundered-crown/tools
B=$1
$PY ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic widowmaker --cell dwarven:twinblade --mech overlays/anvil.js --arms B --P winCap=9 --seeds 20 --seed0 $B --foes $FOES --label "lab B, block $B" --out "$S/runs/s0_B_$B.json" > "$S/runs/s0_B_$B.txt" 2>&1
$PY ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic widowmaker --cell dwarven:twinblade --mech overlays/anvil.js --arms B --P winCap=9 dur=9.4 --seeds 20 --seed0 $B --foes $FOES --label "lab B dur 9.4, block $B" --out "$S/runs/lab94_B_$B.json" > "$S/runs/lab94_B_$B.txt" 2>&1
bash "$S/runs/built.sh" sc-coldiron-mass $B > /dev/null
bash "$S/runs/built.sh" ctl-labclock-mass $B > /dev/null
echo done $B
