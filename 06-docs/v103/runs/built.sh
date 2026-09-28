#!/bin/bash
# a built link against the lab: ult_overlay --relic coldiron --arms SHIP, the design's 33 foes, 20 seeds, one block.
# usage: built.sh <link basename without .html> <seed0> [extra ult_overlay args]
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
L=$1; B=$2; shift 2
FOES=$(cat "$S/runs/foes33.txt")
cd C:/dev/sundered-crown/tools
$PY ult_overlay.py --game "$S/links/$L.html" --relic coldiron --arms SHIP --mech overlays/anvil.js --seeds 20 --seed0 $B --foes $FOES --label "built $L" --out "$S/runs/built_${L}_$B.json" "$@" > "$S/runs/built_${L}_$B.txt" 2>&1
cat "$S/runs/built_${L}_$B.txt"
