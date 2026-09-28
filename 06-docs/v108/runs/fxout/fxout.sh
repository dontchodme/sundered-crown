#!/bin/bash
# v108 carry, the last link: the nova's field spec out of both fx.js copies (tools/fx_remove.py),
# then its gates, one browser at a time.
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v108/runs/fxout; C=$R/02-chain
cd $R/tools
{ $PY fx_remove.py --relic ironhail --src ../02-chain/sc-ironhail-sunder-fx.html --out ../02-chain/sc-ironhail-fxout.html; echo "exit $?"; } > $O/fx_remove.txt 2>&1
grep -q "^exit 0" $O/fx_remove.txt || { echo "fx_remove FAILED"; exit 1; }
echo "fx_remove $(date +%H:%M:%S)"
{ $PY engine_ab.py --a ../02-chain/sc-ironhail-sunder-fx.html --b ../02-chain/sc-ironhail-fxout.html --n 6; echo "exit $?"; } > $O/engine_ab.txt 2>&1
echo "engine_ab $(date +%H:%M:%S)"
P4="paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337"
{ $PY render_ab.py --a ../02-chain/sc-ironhail-sunder-fx.html --b ../02-chain/sc-ironhail-fxout.html --pairs $P4 --frames 0.5,6,12,22,31,40; echo "exit $?"; } > $O/render_ab_others.txt 2>&1
{ $PY render_ab.py --a ../02-chain/sc-ironhail-sunder-fx.html --b ../02-chain/sc-ironhail-fxout.html --pairs ironhail:cindercleave:108238 --frames 2,6,10,13.5; echo "exit $?"; } > $O/render_ab_ironhail_before_cast.txt 2>&1
{ $PY render_ab.py --a ../02-chain/sc-ironhail-sunder-fx.html --b ../02-chain/sc-ironhail-fxout.html --pairs ironhail:cindercleave:108238 --frames 14.95,15.05,15.15,15.25,15.35; echo "exit $?"; } > $O/render_ab_control_cast.txt 2>&1
echo "render_ab $(date +%H:%M:%S)"
{ $PY ironhail_probe.py --game ../02-chain/sc-ironhail-fxout.html --json $O/probe_fxout.json; echo "exit $?"; } > $O/probe_fxout.txt 2>&1
echo "probe $(date +%H:%M:%S)"
{ $PY tip_audit.py --game ../02-chain/sc-ironhail-fxout.html; echo "exit $?"; } > $O/tip_audit_fxout.txt 2>&1
echo "tip_audit $(date +%H:%M:%S)"
( cd $R/app && SWB_GAME=02-chain/sc-ironhail-fxout.html npm run identity ) > $O/shell_identity_app.txt 2>&1
( cd $R/tools && $PY shell_identity.py; echo "exit $?" ) > $O/shell_identity.txt 2>&1
git -C $R checkout -- out/shell_identity_app.json
echo "shell_identity $(date +%H:%M:%S)"
cd $R
{ $PY tools/cinema_clip.py --game 02-chain/sc-ironhail-fxout.html --a ironhail --b cindercleave --seed 108238 --at 13.63 --window 11.57 --end-at-window --fps 60 --w 540 --out 07-shorts/v108/quarrelstorm-window.mp4; echo "exit $?"; } > $O/clip.txt 2>&1
echo "clip $(date +%H:%M:%S)"
