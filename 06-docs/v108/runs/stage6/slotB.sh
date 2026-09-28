#!/bin/bash
# v108 stage 6: ONE browser at a time, after the clip: timeline, render_ab x2, tip_audit, the probe's mutants, the probe on stage 3.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
until grep -q "^exit" "$S/s6/clip.log"; do sleep 5; done
echo "start $(date +%H:%M:%S)"
$PY "$S/s6/clip_timeline.py" > "$S/s6/clip_timeline.txt" 2>&1; echo "timeline $? $(date +%H:%M:%S)"
{ $PY render_ab.py --a "$S/links/sc-ironhail-sunder.html" --b "$S/links/sc-ironhail-sunder-fx.html" \
    --pairs paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337; echo "exit $?"; } > "$S/s6/render_ab_others.txt" 2>&1
echo "render_ab others $(date +%H:%M:%S)"
{ $PY render_ab.py --a "$S/links/sc-ironhail-sunder.html" --b "$S/links/sc-ironhail-sunder-fx.html" \
    --pairs ironhail:cindercleave:108238 --frames 15,16.5,18,19.5,21,22.5; echo "exit $?"; } > "$S/s6/render_ab_control.txt" 2>&1
echo "render_ab control $(date +%H:%M:%S)"
{ $PY tip_audit.py --game "$S/links/sc-ironhail-sunder-fx.html"; echo "exit $?"; } > "$S/s6/tip_audit_fx.txt" 2>&1
echo "tip_audit $(date +%H:%M:%S)"
for m in mS1-land-before-sunder mS2-close-voice mS3-quarrel-writes mS5-puff-at-foe; do
  { $PY ironhail_probe.py --game "$S/s6/mut/sc-ironhail-$m.html" --seeds 1 --no-draw; echo "exit $?"; } > "$S/s6/probe_mut_$m.txt" 2>&1
  echo "mut $m $(date +%H:%M:%S)"
done
{ $PY ironhail_probe.py --game "$S/s6/mut/sc-ironhail-mS4-draw-writes.html" --seeds 1; echo "exit $?"; } > "$S/s6/probe_mut_mS4-draw-writes.txt" 2>&1
echo "mut mS4 $(date +%H:%M:%S)"
{ $PY ironhail_probe.py --game "$S/links/sc-ironhail-sunder.html" --json "$S/s6/probe_sunder_newprobe.json"; echo "exit $?"; } > "$S/s6/probe_sunder_newprobe.txt" 2>&1
echo "probe sunder $(date +%H:%M:%S)"
echo done > "$S/s6/slotB.done"
