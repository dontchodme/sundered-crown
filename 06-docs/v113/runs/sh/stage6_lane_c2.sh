#!/bin/bash
# lane C2: the clip's fight headless, render_ab's control inside its window, the clip, and the same window on the b26.5
T=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $T/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$T/links; R=$T/runs; W=$T/s6/clipwork
log(){ echo "$(date +%H:%M:%S) $*" >> $T/s6/laneC.log; }
log start C2
$I $T/s6/clip_timeline6.py $L/sc-thornwake-b26.5-fx.html grudgebearer 113075 29.8 41.5 > $R/stage6_clip_timeline.txt 2>&1; log "timeline rc $?"
$I render_ab.py --a $L/sc-thornwake-b26.5.html --b $L/sc-thornwake-b26.5-fx.html --pairs thornwake:grudgebearer:113075 --frames 31.3,33,35,36.5,38,39.3 > $R/stage6_render_ab_control.txt 2>&1; log "render_ab control rc $?"
$I cinema_clip.py --game $L/sc-thornwake-b26.5-fx.html --a thornwake --b grudgebearer --seed 113075 --at 29.89 --window 11.48 --end-at-window --fps 60 --w 540 --out ../07-shorts/v113/bramblesnare-window.mp4 > $R/stage6_clip_log.txt 2>&1; log "clip rc $?"
$I cinema_clip.py --game $L/sc-thornwake-b26.5.html --a thornwake --b grudgebearer --seed 113075 --at 29.89 --window 11.48 --end-at-window --fps 60 --w 540 --out $W/clip_base_b26.5.mp4 > $R/stage6_clip_base_log.txt 2>&1; log "clip base rc $?"
log done C2
echo done > $T/s6/laneC2.done
