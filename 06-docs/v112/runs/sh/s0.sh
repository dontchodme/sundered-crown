#!/bin/bash
# STAGE 0: the design's own lab (ult_overlay.py + overlays/rootfast.js), unmodified but for the census and
# per-fight rows (rf_lab.py = make_lab.py's copy), on 151, on the base, arms A,SHIP,B,C at the taken
# rootFor=1.0 (the brief's "--arms A,SHIP,C --P rootFor=1.0" plus arm B at 1.0, "run it"), 33 foes x 20 seeds.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
B=$1
$PY C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/tools/rf_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic heartwood --mech C:/dev/sundered-crown/tools/overlays/rootfast.js --arms A,SHIP,B,C --P rootFor=1.0 --seeds 20 --seed0 $B --foes $(cat C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/foes33.txt) --label "stage 0 block $B" --out C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/s0_ASBC_$B.json > C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/s0_ASBC_$B.txt 2>&1
