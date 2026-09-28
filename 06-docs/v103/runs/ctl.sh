#!/bin/bash
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
FOES=$(cat "$S/runs/foes33.txt")
cd C:/dev/sundered-crown/tools
if [ "$1" = "q1" ]; then
  for B in 2207 2317; do
    $PY ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic widowmaker --cell dwarven:twinblade --mech overlays/anvil.js --arms B,C,D --P winCap=9 dur=9.4 --seeds 20 --seed0 $B --foes $FOES --label "CONTROL: the lab at the engine's window, dur 9.4" --out "$S/runs/lab94_BCD_$B.json" > "$S/runs/lab94_BCD_$B.txt" 2>&1
  done
  for B in 2207 2317; do bash "$S/runs/built.sh" ctl-labclock-temper $B > /dev/null; done
else
  for L in mass bind; do for B in 2207 2317; do bash "$S/runs/built.sh" ctl-labclock-$L $B > /dev/null; done; done
fi
echo done $1
