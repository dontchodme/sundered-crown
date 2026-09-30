#!/bin/bash
# a built link's own ultimate (arm SHIP of tw_lab.py), Thornwake side A, the 33 foes x 20 seeds: $1 link path, $2 tag, $3 block
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
$PY $S/tools/tw_lab.py --game $1 --relic thornwake --mech C:/dev/sundered-crown/tools/overlays/bramble.js --arms SHIP --seeds 20 --seed0 $3 --foes $(cat $S/runs/foes33.txt) --label "BUILT $2 block $3" --out $S/runs/built_$2_$3.json > $S/runs/built_$2_$3.txt 2>&1
echo "rc=$?" >> $S/runs/built_$2_$3.txt
