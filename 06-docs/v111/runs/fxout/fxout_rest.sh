#!/bin/bash
# v111: the fx-out gates the 22:35 pause cut off (Rick: "minimum usage until 3 am"), re-run at full power
# 2026-09-30 03:05; fx_remove and engine_ab 5166/5166 had finished (fx_remove.txt, engine_ab.txt).
# Then the Electron gates that waited for Rick to be off the PC: shell_identity on Spellbreaker's fx-out
# link AND on Lightkeeper's, Censer's and Aureole's (their docs say PENDING), one app run at a time.
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v111/runs/fxout; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
P4="paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337"
{ $PY spellbreaker_probe.py --game $C/sc-spellbreaker-fxout.html --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1 &
{ $PY render_ab.py --a $C/sc-spellbreaker-b7.5-fx.html --b $C/sc-spellbreaker-fxout.html --pairs $P4 --frames 0.5,6,12,22,31,40; echo "exit $?"; } > $O/render_ab_others.txt 2>&1
{ $PY render_ab.py --a $C/sc-spellbreaker-b7.5-fx.html --b $C/sc-spellbreaker-fxout.html --pairs spellbreaker:vesper:111075 --frames 79.21,79.31,79.41,79.51,79.61; echo "exit $?"; } > $O/render_ab_control_cast.txt 2>&1
{ $PY tip_audit.py --game $C/sc-spellbreaker-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
rm -f "$S/batch/spellbreaker/staves-on-fxout.html"
{ $PY staff_carry.py --src $C/sc-spellbreaker-fxout.html --out "$S/batch/spellbreaker/staves-on-fxout.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
{ $PY cinema_clip.py --game $C/sc-spellbreaker-fxout.html --a spellbreaker --b vesper --seed 111075 --at 77.98 --window 12.77 --end-at-window --fps 60 --w 540 --out ../07-shorts/v111/unmaking-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
wait
echo "spellbreaker gates $(date +%H:%M:%S)"
for pair in v107:sc-lightkeeper-fxout v109:sc-censer-fxout v110:sc-aureole-fxout v111:sc-spellbreaker-fxout; do
  v=${pair%%:*}; L=${pair#*:}
  ( cd $R/app && SWB_GAME=02-chain/$L.html npm run identity ) > $R/06-docs/$v/runs/fxout/shell_identity_app.txt 2>&1
  ( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $R/06-docs/$v/runs/fxout/shell_identity.txt 2>&1
  git -C $R checkout -- out/shell_identity_app.json
  echo "shell_identity $L $(grep -E 'PASS|FAIL' $R/06-docs/$v/runs/fxout/shell_identity.txt | head -1) $(date +%H:%M:%S)"
done
echo ALL-DONE
