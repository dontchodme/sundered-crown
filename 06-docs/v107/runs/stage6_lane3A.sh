#!/bin/bash
# lane A (one Chromium at a time), the FINAL probe v6 (SHAPES key by key, a draw's memo writes taken in): the fx link, full field + drawn 74; then mV1
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
R=$S/s6int/runs; L=$S/links; M=$S/s6int/mut
echo "A3 probe $(sha256sum lightkeeper_probe.py | cut -c1-16) start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $L/sc-lightkeeper-bulwark-b9.5-fx.html --json $R/probe_fx.json ) > $R/probe_fx.txt 2>&1; rc=$?
echo "A3 probe_fx done rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $M/sc-lightkeeper-mV1.html --no-draw ) > $R/probe_mut6_mV1.txt 2>&1; rc=$?
echo "A3 probe mV1 done rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
