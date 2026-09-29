#!/bin/bash
# v106 carry, the last link: the nova's SPECS.widowmaker out of both fx.js copies (tools/fx_remove.py,
# the three lines only -- the NOVAS header stays), then its gates.
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v106/runs/fxout; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
{ $PY fx_remove.py --relic widowmaker --src $C/sc-widowmaker-b1075-fx.html --out $C/sc-widowmaker-fxout.html; echo "exit $?"; } > $O/fx_remove.txt 2>&1
grep -q "^exit 0" $O/fx_remove.txt || { echo "fx_remove FAILED"; exit 1; }
echo "fx_remove $(date +%H:%M:%S)"
IDS=$(grep -o '{ id:"[a-z]*", name:"' $C/sc-widowmaker-fxout.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | paste -sd, -)
echo "$IDS" > $O/ids.txt
P4="paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337"
{ $PY engine_ab.py --a $C/sc-widowmaker-b1075-fx.html --b $C/sc-widowmaker-fxout.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab.txt 2>&1 &
{ $PY widowmaker_probe.py --game $C/sc-widowmaker-fxout.html --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1 &
wait
echo "engine_ab+probe $(date +%H:%M:%S)"
{ $PY render_ab.py --a $C/sc-widowmaker-b1075-fx.html --b $C/sc-widowmaker-fxout.html --pairs $P4 --frames 0.5,6,12,22,31,40; echo "exit $?"; } > $O/render_ab_others.txt 2>&1
{ $PY render_ab.py --a $C/sc-widowmaker-b1075-fx.html --b $C/sc-widowmaker-fxout.html --pairs widowmaker:spellbreaker:106223 --frames 47.25,47.35,47.45,47.55,47.65; echo "exit $?"; } > $O/render_ab_control_cast.txt 2>&1
echo "render_ab $(date +%H:%M:%S)"
{ $PY tip_audit.py --game $C/sc-widowmaker-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
rm -f "$S/batch/widowmaker/staves-on-fxout.html"
{ $PY staff_carry.py --src $C/sc-widowmaker-fxout.html --out "$S/batch/widowmaker/staves-on-fxout.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
echo "tip_audit+staff $(date +%H:%M:%S)"
( cd $R/app && SWB_GAME=02-chain/sc-widowmaker-fxout.html npm run identity ) > $O/shell_identity_app.txt 2>&1
( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $O/shell_identity.txt 2>&1
git -C $R checkout -- out/shell_identity_app.json
echo "shell_identity $(date +%H:%M:%S)"
cd $R/tools
{ $PY cinema_clip.py --game $C/sc-widowmaker-fxout.html --a widowmaker --b spellbreaker --seed 106223 --at 46.02 --window 12.41 --end-at-window --fps 60 --w 540 --out ../07-shorts/v106/exsanguinate-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
echo "clip $(date +%H:%M:%S)"
echo ALL-DONE
