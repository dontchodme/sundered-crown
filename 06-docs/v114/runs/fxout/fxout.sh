#!/bin/bash
# v114 carry, the last link: Goreshard's (oathwound's) beam SPECS.oathwound out of both fx.js copies with the
# 'negative gravity' note above it -- no negative-gravity beam is left after it -- then its gates, full power.
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v114/runs/fxout; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
{ $PY fx_remove.py --relic oathwound --src $C/sc-goreshard-b10.25-fx.html --out $C/sc-goreshard-fxout.html; echo "exit $?"; } > $O/fx_remove.txt 2>&1
grep -q "^exit 0" $O/fx_remove.txt || { echo "fx_remove FAILED"; exit 1; }
echo "fx_remove $(date +%H:%M:%S)"
IDS=$(grep -o '{ id:"[a-z]*", name:"' $C/sc-goreshard-fxout.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | paste -sd, -)
echo "$IDS" > $O/ids.txt
P4="paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337"
{ $PY engine_ab.py --a $C/sc-goreshard-b10.25-fx.html --b $C/sc-goreshard-fxout.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab.txt 2>&1
echo "engine_ab $(date +%H:%M:%S)"
{ $PY goreshard_probe.py --game $C/sc-goreshard-fxout.html --stage 6 --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1
echo "probe $(date +%H:%M:%S)"
{ $PY render_ab.py --a $C/sc-goreshard-b10.25-fx.html --b $C/sc-goreshard-fxout.html --pairs $P4 --frames 0.5,6,12,22,31,40; echo "exit $?"; } > $O/render_ab_others.txt 2>&1
{ $PY render_ab.py --a $C/sc-goreshard-b10.25-fx.html --b $C/sc-goreshard-fxout.html --pairs oathwound:grudgebearer:114371 --frames 31.84,31.94,32.04,32.14,32.24; echo "exit $?"; } > $O/render_ab_control_cast.txt 2>&1
echo "render_ab $(date +%H:%M:%S)"
{ $PY tip_audit.py --game $C/sc-goreshard-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
rm -f "$S/batch/goreshard/staves-on-fxout.html"
{ $PY staff_carry.py --src $C/sc-goreshard-fxout.html --out "$S/batch/goreshard/staves-on-fxout.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
echo "tip_audit+staff $(date +%H:%M:%S)"
{ $PY cinema_clip.py --game $C/sc-goreshard-fxout.html --a oathwound --b grudgebearer --seed 114371 --at 30.61 --window 12.57 --end-at-window --fps 60 --w 540 --out ../07-shorts/v114/bloodprice-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
echo "clip $(date +%H:%M:%S)"
( cd $R/app && SWB_GAME=02-chain/sc-goreshard-fxout.html npm run identity ) > $O/shell_identity_app.txt 2>&1
( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $O/shell_identity.txt 2>&1
git -C $R checkout -- out/shell_identity_app.json
echo "shell_identity $(date +%H:%M:%S)"
echo ALL-DONE
