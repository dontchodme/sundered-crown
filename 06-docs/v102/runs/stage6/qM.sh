#!/bin/bash
# one browser at a time: the clean link and the five stage-6 mutants on one seed; then the new probe on b205 (no stage 6)
L=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone
P=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
$P -u lodestone_probe.py --game $L/links/sc-lodestone-b205-fx.html --seeds 1 > $L/s6/probe_fx_s1.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_fx_s1.txt
for m in mV1-close-on-death mV2-touch-before-hex mP1-lode-writes mP2-draw-writes mP3-ungated; do
  $P -u lodestone_probe.py --game $L/s6/mut/sc-lodestone-$m.html --seeds 1 > $L/s6/probe_mut_$m.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_mut_$m.txt
done
$P -u lodestone_probe.py --game $L/links/sc-lodestone-b205.html --json $L/s6/probe_b205_newprobe.json > $L/s6/probe_b205_newprobe.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_b205_newprobe.txt
echo QM DONE
