#!/bin/bash
# v105 carry: the carried stage-6 link's own gates on the batch line (after carry.py's A/B against scratch).
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v105/runs/carry; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
IDS=$(grep -o '{ id:"[a-z]*", name:"' $C/sc-oracle-fx.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | paste -sd, -)
echo "$IDS" > $O/ids.txt
# stage 6 moves no fight on THIS tip either, Coldiron's and Ironhail's pairings included
{ $PY engine_ab.py --a $C/sc-oracle-b10.html --b $C/sc-oracle-fx.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab_s6.txt 2>&1 &
{ $PY oracle_probe.py --game $C/sc-oracle-fx.html --json $O/probe_fx.json; echo "exit $?"; } > $O/probe_fx.txt 2>&1 &
wait
echo "engine_ab+probe $(date +%H:%M:%S)"
{ $PY tip_audit.py --game $C/sc-oracle-fx.html; echo "exit $?"; } > $O/tip_audit_fx.txt 2>&1
rm -f "$S/batch/oracle/staves-on-fx.html"
{ $PY staff_carry.py --src $C/sc-oracle-fx.html --out "$S/batch/oracle/staves-on-fx.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
echo "tip_audit+staff $(date +%H:%M:%S)"
( cd $R/app && SWB_GAME=02-chain/sc-oracle-fx.html npm run identity ) > $O/shell_identity_app.txt 2>&1
( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $O/shell_identity.txt 2>&1
git -C $R checkout -- out/shell_identity_app.json
echo "shell_identity $(date +%H:%M:%S)"
echo ALL-DONE
