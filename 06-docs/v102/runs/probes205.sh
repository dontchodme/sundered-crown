#!/bin/bash
# Review round 2: the probe (with [0] and the close split) on stages 2, 3 and the b205 mutants. ONE browser (verify holds the other).
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
cd C:/dev/sundered-crown/tools
P(){ $PY lodestone_probe.py --game "$1" --json "$S/runs/probe_$2.json" > "$S/runs/probe_$2.txt" 2>&1; echo "$2 rc=$?"; }
P "$S/links/sc-lodestone-runes.html" runes
P "$S/links/sc-lodestone-rebuttal.html" rebuttal
for m in mut-dur mut-pad mut-cd mut-hex2 mut-impulse mut-bite mut-self mut-death; do P "$S/ctl/mut205/$m.html" b205_$m; done
echo PROBES205-DONE
