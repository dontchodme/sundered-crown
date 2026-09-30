#!/bin/bash
# STAGE 0, THE DESIGN'S STATED CHARGE: the same lab at --P charge=15 (v85 §4 "Charge 15 (the relic's)",
# read on the lab's clock), arms B and C at rootFor 1.0, 33 foes x 20 seeds, with the census.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
B=$1
$PY C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/tools/rf_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic heartwood --mech C:/dev/sundered-crown/tools/overlays/rootfast.js --arms B,C --P rootFor=1.0 charge=15 --seeds 20 --seed0 $B --foes $(cat C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/foes33.txt) --label "stage 0 at the design's charge 15, block $B" --out C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/s0_c15_BC_$B.json > C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/s0_c15_BC_$B.txt 2>&1
