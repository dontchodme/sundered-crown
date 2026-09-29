#!/bin/bash
# lane A (one Chromium): probe v6 on the fx link, full field + drawn subset
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
echo "A probe_fx start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $S/links/sc-lightkeeper-bulwark-b9.5-fx.html --json $S/s6int/runs/probe_fx.json ) > $S/s6int/runs/probe_fx.txt 2>&1
echo "A probe_fx done $(date +%H:%M:%S) rc $?" >> $S/s6int/lanes.log
