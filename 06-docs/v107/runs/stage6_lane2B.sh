#!/bin/bash
# lane B (one Chromium at a time): the clip, then the probe on the three stage-6 mutants, then the probe v6 on b9.5
cd C:/dev/sundered-crown/tools
export PYTHONIOENCODING=utf-8
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
R=$S/s6int/runs
echo "B clip start $(date +%H:%M:%S)" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd cinema_clip.py --game $S/links/sc-lightkeeper-bulwark-b9.5-fx.html --a lightkeeper --b redflail --seed 107201 --at 47.64 --window 13.22 --end-at-window --fps 60 --w 540 --out ../07-shorts/v107/bulwark-window.mp4 ) > $R/clip.log 2>&1
echo "B clip done $(date +%H:%M:%S) rc $?" >> $S/s6int/lanes.log
for m in mV1 mP1; do
  ( time $S/s6int/bn.cmd lightkeeper_probe.py --game $S/s6int/mut/sc-lightkeeper-$m.html --no-draw ) > $R/probe_mut6_$m.txt 2>&1
  echo "B probe $m done $(date +%H:%M:%S) rc $?" >> $S/s6int/lanes.log
done
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $S/s6int/mut/sc-lightkeeper-mD1.html --seeds 1 --draw-every 30 ) > $R/probe_mut6_mD1.txt 2>&1
echo "B probe mD1 done $(date +%H:%M:%S) rc $?" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $S/links/sc-lightkeeper-bulwark-b9.5-fx.html --seeds 1 --draw-every 30 ) > $R/probe_fx_twin_mD1.txt 2>&1
echo "B probe fx twin (mD1's field) done $(date +%H:%M:%S) rc $?" >> $S/s6int/lanes.log
( time $S/s6int/bn.cmd lightkeeper_probe.py --game $S/links/sc-lightkeeper-bulwark-b9.5.html ) > $R/probe_b9.5_v6.txt 2>&1
echo "B probe b9.5 v6 done $(date +%H:%M:%S) rc $?" >> $S/s6int/lanes.log
