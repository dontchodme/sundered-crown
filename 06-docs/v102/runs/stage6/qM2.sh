#!/bin/bash
# the second browser: the new probe on b205 (no stage 6), then mP3 and mP2 (qM.sh is stopped before it reaches them)
L=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone
P=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
$P -u lodestone_probe.py --game $L/links/sc-lodestone-b205.html --json $L/s6/probe_b205_newprobe.json > $L/s6/probe_b205_newprobe.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_b205_newprobe.txt
for m in mP3-ungated mP2-draw-writes; do
  $P -u lodestone_probe.py --game $L/s6/mut/sc-lodestone-$m.html --seeds 1 > $L/s6/probe_mut_$m.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_mut_$m.txt
done
echo QM2 DONE
