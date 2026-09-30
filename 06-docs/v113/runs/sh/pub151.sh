#!/bin/bash
# THE DESIGN'S OWN RUN REPLAYED ON 151: sc-trunk, seed0 2207, 10 seeds, the published 33 foes, arms A,SHIP,B,C
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
$PY $S/tools/tw_lab.py --game C:/dev/sundered-crown/02-chain/sc-trunk.html --relic thornwake --mech C:/dev/sundered-crown/tools/overlays/bramble.js --arms A,SHIP,B,C --seeds 10 --seed0 2207 --foes $(cat $S/runs/foes33.txt) --label "published run replayed on 151 (sc-trunk)" --out $S/runs/pub151_base.json > $S/runs/pub151_base.txt 2>&1
echo "rc=$?" >> $S/runs/pub151_base.txt
