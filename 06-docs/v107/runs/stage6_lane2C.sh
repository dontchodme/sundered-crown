#!/bin/bash
# lane C (one Chromium, after lane A's probe is done): the engine_ab control (b9.5 against mP1, whose
# picture writes the foe 1e-9 on a bank), the clip fight's timeline, SHAPES' memo writes on a draw
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
R=$S/s6int/runs; L=$S/links
until grep -q "A probe_fx done" $S/s6int/lanes.log; do sleep 15; done
echo "C start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
$S/s6int/bn.cmd engine_ab.py --a $L/sc-lightkeeper-bulwark-b9.5.html --b $S/s6int/mut/sc-lightkeeper-mP1.html --ids lightkeeper,gloamwire,redflail,aureole --n 6 > $R/engine_ab_control.txt 2>&1
rc=$?; echo "C engine_ab control rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
$S/s6int/bn.cmd $S/s6int/clip_timeline.py $L/sc-lightkeeper-bulwark-b9.5-fx.html > $R/clip_timeline.txt 2>&1
rc=$?; echo "C clip timeline rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
$S/s6int/bn.cmd $S/s6int/shapes_draw.py $L/sc-lightkeeper-bulwark-b9.5.html $L/sc-lightkeeper-bulwark-b9.5-fx.html > $R/shapes_draw.txt 2>&1
rc=$?; echo "C shapes_draw rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
echo "C done $(date +%H:%M:%S)" >> $S/s6int/lanes.log
