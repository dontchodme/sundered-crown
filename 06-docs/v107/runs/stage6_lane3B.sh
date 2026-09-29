#!/bin/bash
# lane B (one Chromium at a time), the FINAL probe v6: mD1 on the drawn first seed (every 30th step), its clean twin on the
# same field, the b9.5 (no stage 6), then mP1
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
R=$S/s6int/runs; L=$S/links; M=$S/s6int/mut
echo "B3 start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $M/sc-lightkeeper-mD1.html --seeds 1 --draw-every 30 ) > $R/probe_mut6_mD1.txt 2>&1; rc=$?
echo "B3 probe mD1 done rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $L/sc-lightkeeper-bulwark-b9.5-fx.html --seeds 1 --draw-every 30 ) > $R/probe_fx_twin_mD1.txt 2>&1; rc=$?
echo "B3 probe fx twin done rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $L/sc-lightkeeper-bulwark-b9.5.html ) > $R/probe_b9.5_v6.txt 2>&1; rc=$?
echo "B3 probe b9.5 v6 done rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $M/sc-lightkeeper-mP1.html --no-draw ) > $R/probe_mut6_mP1.txt 2>&1; rc=$?
echo "B3 probe mP1 done rc $rc $(date +%H:%M:%S)" >> $S/s6int/lanes.log
