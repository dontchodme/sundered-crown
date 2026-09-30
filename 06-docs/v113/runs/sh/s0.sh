#!/bin/bash
# STAGE 0: the design's lab (overlays/bramble.js, unmodified) on the base, arms A,SHIP,B,C, 33 foes x 20 seeds, block $1
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
$PY $S/tools/tw_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic thornwake --mech C:/dev/sundered-crown/tools/overlays/bramble.js --arms A,SHIP,B,C --seeds 20 --seed0 $1 --foes $(cat $S/runs/foes33.txt) --label "stage 0 block $1" --out $S/runs/s0_ASBC_$1.json > $S/runs/s0_ASBC_$1.txt 2>&1
echo "rc=$?" >> $S/runs/s0_ASBC_$1.txt
