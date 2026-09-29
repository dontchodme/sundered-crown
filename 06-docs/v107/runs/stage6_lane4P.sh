#!/bin/bash
# lane 4P (bonus, not a gate the task names): the final probe v6 on the stage-6 link as the builder writes it on the
# line's tip of 08:04, sc-angelus-b9-fx (42 relics), one seed, both sides, every foe, drawn every 30th step
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
R=$S/s6int/runs
echo "4P probe on angelus tip start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $S/s6int/tip/sc-lightkeeper-bulwark-b9.5-fx-on-angelus.html --seeds 1 --draw-every 30 ) > $R/probe_fx_on_angelus_s1.txt 2>&1
echo "4P probe on angelus tip done $(date +%H:%M:%S) $(grep -E '^  [0-9]+/[0-9]+' $R/probe_fx_on_angelus_s1.txt)" >> $S/s6int/lanes.log
