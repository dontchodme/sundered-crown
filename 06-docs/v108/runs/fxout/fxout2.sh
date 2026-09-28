#!/bin/bash
# The fx-out link's gates that the 01:28 process sweep cut off (Rick asked for less load), re-run ONE
# AT A TIME at idle priority. engine_ab over every id on the link (fxout.sh's run had no --ids and
# compared engine_ab's default 6). shell_identity waits: it launches the Electron app Rick is using.
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v108/runs/fxout
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
IDS=$(grep -o '{ id:"[a-z]*", name:"' ../02-chain/sc-ironhail-fxout.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | paste -sd, -)
echo "$IDS" > $O/ids39.txt
{ $PY engine_ab.py --a ../02-chain/sc-ironhail-sunder-fx.html --b ../02-chain/sc-ironhail-fxout.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab.txt 2>&1
echo "engine_ab $(date +%H:%M:%S)"
{ $PY ironhail_probe.py --game ../02-chain/sc-ironhail-fxout.html --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1
echo "probe $(date +%H:%M:%S)"
{ $PY tip_audit.py --game ../02-chain/sc-ironhail-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
echo "tip_audit $(date +%H:%M:%S)"
rm -f "$S/batch/ironhail/staves-on-fxout.html"
{ $PY staff_carry.py --src ../02-chain/sc-ironhail-fxout.html --out "$S/batch/ironhail/staves-on-fxout.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
echo "staff_carry $(date +%H:%M:%S)"
cd $R
{ $PY tools/cinema_clip.py --game 02-chain/sc-ironhail-fxout.html --a ironhail --b cindercleave --seed 108238 --at 13.63 --window 11.57 --end-at-window --fps 60 --w 540 --out 07-shorts/v108/quarrelstorm-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
echo "clip $(date +%H:%M:%S)"
echo ALL-DONE
