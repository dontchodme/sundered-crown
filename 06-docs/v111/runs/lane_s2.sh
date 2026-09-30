#!/bin/bash
# lane S2: the clip's fight headless, render_ab's control inside its window, the clip, and the same window on the b7.5
SB=<scratch>
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $SB/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$SB/links; R=$SB/runs; W=$SB/s6/clipwork
log(){ echo "$(date +%H:%M:%S) $*" >> $SB/s6/laneS.log; }
log start S2
$I $SB/tools/clip_timeline6.py $L/sc-spellbreaker-b7.5-fx.html vesper 111075 77.9 90.8 > $R/stage6_clip_timeline.txt 2>&1; log "timeline rc $?"
$I render_ab.py --a $L/sc-spellbreaker-b7.5.html --b $L/sc-spellbreaker-b7.5-fx.html --pairs spellbreaker:vesper:111075 --frames 79.5,81,83,85,87,88.5 > $R/stage6_render_ab_control.txt 2>&1; log "render_ab control rc $?"
$I cinema_clip.py --game $L/sc-spellbreaker-b7.5-fx.html --a spellbreaker --b vesper --seed 111075 --at 77.98 --window 12.77 --end-at-window --fps 60 --w 540 --out ../07-shorts/v111/unmaking-window.mp4 > $R/stage6_clip_log.txt 2>&1; log "clip rc $?"
$I cinema_clip.py --game $L/sc-spellbreaker-b7.5.html --a spellbreaker --b vesper --seed 111075 --at 77.98 --window 12.77 --end-at-window --fps 60 --w 540 --out $W/clip_base_b7.5.mp4 > $R/stage6_clip_base_log.txt 2>&1; log "clip base rc $?"
log done S2
echo done > $SB/s6/laneS2.done
