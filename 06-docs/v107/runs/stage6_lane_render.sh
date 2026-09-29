#!/bin/bash
# lane 1, part 2 (one Chromium at a time): render_ab others + control, tip_audit on the fx link and on b9.5 (the reference)
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
L=$S/links
echo "render start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
$S/s6int/bn.cmd render_ab.py --a $L/sc-lightkeeper-bulwark-b9.5.html --b $L/sc-lightkeeper-bulwark-b9.5-fx.html --pairs paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337 > $S/s6int/runs/render_ab_others.txt 2>&1
echo "render_others rc $? $(date +%H:%M:%S)" >> $S/s6int/lanes.log
$S/s6int/bn.cmd render_ab.py --a $L/sc-lightkeeper-bulwark-b9.5.html --b $L/sc-lightkeeper-bulwark-b9.5-fx.html --pairs lightkeeper:gloamwire:107602 --frames 64.5,66,68,70,72,74 > $S/s6int/runs/render_ab_control.txt 2>&1
echo "render_control rc $? $(date +%H:%M:%S)" >> $S/s6int/lanes.log
$S/s6int/bn.cmd tip_audit.py --game $L/sc-lightkeeper-bulwark-b9.5-fx.html > $S/s6int/runs/tip_audit_fx.txt 2>&1
echo "tip_audit_fx rc $? $(date +%H:%M:%S)" >> $S/s6int/lanes.log
