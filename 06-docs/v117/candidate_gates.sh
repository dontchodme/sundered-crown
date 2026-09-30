#!/bin/bash
# v117: the game candidate (the balance tip + Rick's Daybreak circle + yert's seven staves, 49 relics).
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v117/runs/candidate; C=../02-chain
cd $R/tools
{ $PY verify.py --game $C/sc-candidate-49.html --n 40; echo "exit $?"; } > $O/verify.txt 2>&1 &
{ $PY tip_audit.py --game $C/sc-candidate-49.html; echo "exit $?"; } > $O/tip_audit.txt 2>&1
( cd $R/app && SWB_GAME=02-chain/sc-candidate-49.html npm run identity ) > $O/shell_identity_app.txt 2>&1
( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $O/shell_identity.txt 2>&1
git -C $R checkout -- out/shell_identity_app.json
wait
echo ALL-DONE
