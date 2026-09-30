#!/bin/bash
# THE LAB GIVEN THE ENGINE'S WINDOW: arms B and C at dur $2 (8 / (1 - the built window's frozen share)), block $1
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
$PY $S/tools/tw_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic thornwake --mech C:/dev/sundered-crown/tools/overlays/bramble.js --arms B,C --P dur=$2 --seeds 20 --seed0 $1 --foes $(cat $S/runs/foes33.txt) --label "lab at the engine's window, dur $2, block $1" --out $S/runs/lab_dur${3}_$1.json > $S/runs/lab_dur${3}_$1.txt 2>&1
echo "rc=$?" >> $S/runs/lab_dur${3}_$1.txt
