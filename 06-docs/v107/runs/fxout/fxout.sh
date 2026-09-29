#!/bin/bash
# v107 carry, the last link: the nova's SPECS.lightkeeper out of both fx.js copies (tools/fx_remove.py; the
# NOVAS header above it stays), then its gates ONE AT A TIME (Rick is on the PC: limited mode, no Electron --
# shell_identity waits for his word).
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v107/runs/fxout; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
{ $PY fx_remove.py --relic lightkeeper --src $C/sc-lightkeeper-bulwark-b9.5-fx.html --out $C/sc-lightkeeper-fxout.html; echo "exit $?"; } > $O/fx_remove.txt 2>&1
grep -q "^exit 0" $O/fx_remove.txt || { echo "fx_remove FAILED"; exit 1; }
echo "fx_remove $(date +%H:%M:%S)"
IDS=$(grep -o '{ id:"[a-z]*", name:"' $C/sc-lightkeeper-fxout.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | paste -sd, -)
echo "$IDS" > $O/ids.txt
P4="paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337"
{ $PY engine_ab.py --a $C/sc-lightkeeper-bulwark-b9.5-fx.html --b $C/sc-lightkeeper-fxout.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab.txt 2>&1
echo "engine_ab $(date +%H:%M:%S)"
{ $PY lightkeeper_probe.py --game $C/sc-lightkeeper-fxout.html --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1
echo "probe $(date +%H:%M:%S)"
{ $PY render_ab.py --a $C/sc-lightkeeper-bulwark-b9.5-fx.html --b $C/sc-lightkeeper-fxout.html --pairs $P4 --frames 0.5,6,12,22,31,40; echo "exit $?"; } > $O/render_ab_others.txt 2>&1
{ $PY render_ab.py --a $C/sc-lightkeeper-bulwark-b9.5-fx.html --b $C/sc-lightkeeper-fxout.html --pairs lightkeeper:redflail:107201 --frames 48.87,48.95,49.05,49.15,49.25; echo "exit $?"; } > $O/render_ab_control_cast.txt 2>&1
echo "render_ab $(date +%H:%M:%S)"
{ $PY tip_audit.py --game $C/sc-lightkeeper-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
rm -f "$S/batch/lightkeeper/staves-on-fxout.html"
{ $PY staff_carry.py --src $C/sc-lightkeeper-fxout.html --out "$S/batch/lightkeeper/staves-on-fxout.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
echo "tip_audit+staff $(date +%H:%M:%S)"
{ $PY cinema_clip.py --game $C/sc-lightkeeper-fxout.html --a lightkeeper --b redflail --seed 107201 --at 47.64 --window 13.22 --end-at-window --fps 60 --w 540 --out ../07-shorts/v107/bulwark-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
echo "clip $(date +%H:%M:%S)"
echo ALL-DONE-BUT-SHELL-IDENTITY
