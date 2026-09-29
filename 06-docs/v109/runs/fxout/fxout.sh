#!/bin/bash
# v109 carry, the last link: the nova's SPECS.censer out of both fx.js copies (tools/fx_remove.py; the
# NOVAS header above it stays, heading nothing now), then its gates ONE AT A TIME (Rick is on the PC: limited mode, no Electron --
# shell_identity waits for his word).
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v109/runs/fxout; C=../02-chain
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
cd $R/tools
{ $PY fx_remove.py --relic censer --src $C/sc-censer-consecration-b25.5-fx.html --out $C/sc-censer-fxout.html; echo "exit $?"; } > $O/fx_remove.txt 2>&1
grep -q "^exit 0" $O/fx_remove.txt || { echo "fx_remove FAILED"; exit 1; }
echo "fx_remove $(date +%H:%M:%S)"
IDS=$(grep -o '{ id:"[a-z]*", name:"' $C/sc-censer-fxout.html | sed 's/{ id:"\([a-z]*\)".*/\1/' | paste -sd, -)
echo "$IDS" > $O/ids.txt
P4="paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337"
{ $PY engine_ab.py --a $C/sc-censer-consecration-b25.5-fx.html --b $C/sc-censer-fxout.html --ids "$IDS" --n 6; echo "exit $?"; } > $O/engine_ab.txt 2>&1
echo "engine_ab $(date +%H:%M:%S)"
{ $PY censer_probe.py --game $C/sc-censer-fxout.html --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1
echo "probe $(date +%H:%M:%S)"
{ $PY render_ab.py --a $C/sc-censer-consecration-b25.5-fx.html --b $C/sc-censer-fxout.html --pairs $P4 --frames 0.5,6,12,22,31,40; echo "exit $?"; } > $O/render_ab_others.txt 2>&1
{ $PY render_ab.py --a $C/sc-censer-consecration-b25.5-fx.html --b $C/sc-censer-fxout.html --pairs censer:slagheart:109149 --frames 31.25,31.35,31.45,31.55,31.65; echo "exit $?"; } > $O/render_ab_control_cast.txt 2>&1
echo "render_ab $(date +%H:%M:%S)"
{ $PY tip_audit.py --game $C/sc-censer-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
rm -f "$S/batch/censer/staves-on-fxout.html"
{ $PY staff_carry.py --src $C/sc-censer-fxout.html --out "$S/batch/censer/staves-on-fxout.html"; echo "exit $?"; } > $O/staff_carry_dry.txt 2>&1
echo "tip_audit+staff $(date +%H:%M:%S)"
{ $PY cinema_clip.py --game $C/sc-censer-fxout.html --a censer --b slagheart --seed 109149 --at 30.02 --window 12.79 --end-at-window --fps 60 --w 540 --out ../07-shorts/v109/consecration-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
echo "clip $(date +%H:%M:%S)"
echo ALL-DONE-BUT-SHELL-IDENTITY
