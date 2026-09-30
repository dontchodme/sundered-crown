#!/bin/bash
# v117: the balance link's gates (full power).
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v117/runs; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
MOVED=$($PY -c "import balance_build as b; print(','.join(b.BLADES))")
IDS=$(grep -o '{ id:"[a-z]*", name:"' $C/sc-balance.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | grep -vxF -f <(echo "$MOVED" | tr ',' '\n') | paste -sd, -)
echo "$IDS" > $O/ids_untouched.txt
# 1. the untouched relics' fights are identical
{ $PY engine_ab.py --a $C/sc-goreshard-fxout.html --b $C/sc-balance.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab_untouched.txt 2>&1 &
# 2. verify on the balance link
{ $PY verify.py --game $C/sc-balance.html --n 40; echo "exit $?"; } > $O/verify_balance.txt 2>&1 &
# 3. the game roster on the balance link, and the final numbers there
( bash $R/06-docs/v117/make_roster.sh $R/02-chain/sc-balance.html > $O/make_roster_final.txt 2>&1; cp "$S/balance/roster49.html" "$S/balance/roster49-final.html";
  $PY -u balance_sweep.py --game "$S/balance/roster49-final.html" --relics axiom,morningstar,ironwood,portcullis,bindweed,coldiron,ironhail,lodestone,widowmaker,oracle,angelus,lightkeeper,censer,aureole,spellbreaker,heartwood,thornwake,oathwound --n 10 --blocks 2207,2317 --tol 100 --max 1 --parallel 3 --out "$S/balance/round3.json" > $O/round3_final.txt 2>&1 ) &
wait
echo "engine_ab + verify + round3 $(date +%H:%M:%S)"
{ $PY tip_audit.py --game $C/sc-balance.html; echo "exit $?"; } > $O/tip_audit_balance.txt 2>&1
( cd $R/app && SWB_GAME=02-chain/sc-balance.html npm run identity ) > $O/shell_identity_app.txt 2>&1
( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $O/shell_identity.txt 2>&1
git -C $R checkout -- out/shell_identity_app.json
echo "tip_audit + shell_identity $(date +%H:%M:%S)"
echo ALL-DONE
