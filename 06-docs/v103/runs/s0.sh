#!/bin/bash
# stage 0: the design's lab, unmodified, on 151, on the base (sc-tendril-t3). one block per call.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
B=$1
FOES=$(cat "$S/runs/foes33.txt")
cd C:/dev/sundered-crown/tools
G=../02-chain/sc-tendril-t3.html
$PY ult_overlay.py --game $G --relic widowmaker --cell dwarven:twinblade --mech overlays/anvil.js --arms A,S,B,C,D --P winCap=9 --seeds 20 --seed0 $B --foes $FOES --label "s0 cap9 blade 11.95" --out "$S/runs/s0_ASBCD9_$B.json" > "$S/runs/s0_ASBCD9_$B.txt" 2>&1
$PY ult_overlay.py --game $G --relic widowmaker --cell dwarven:twinblade --mech overlays/anvil.js --arms D --seeds 20 --seed0 $B --foes $FOES --label "s0 D at the lab default cap 12, blade 11.95" --out "$S/runs/s0_D12_$B.json" > "$S/runs/s0_D12_$B.txt" 2>&1
$PY ult_overlay.py --game $G --relic widowmaker --cell dwarven:twinblade --mech overlays/anvil.js --arms A,D --P blade=9 winCap=9 --seeds 20 --seed0 $B --foes $FOES --label "s0 the brief's command: blade 9 cap 9" --out "$S/runs/s0_AD9_b9_$B.json" > "$S/runs/s0_AD9_b9_$B.txt" 2>&1
echo done $B
