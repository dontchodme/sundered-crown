#!/bin/bash
# the stage-6 clip (v112 §8): the pick's best window, Heartwood v Lightkeeper 112312
cd C:/dev/sundered-crown
powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'BelowNormal'"
C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe tools/cinema_clip.py --game C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/links/sc-heartwood-b11-fx.html --a heartwood --b lightkeeper --seed 112312 --at 75.26 --window 13.28 --end-at-window --fps 60 --w 540 --out 07-shorts/v112/rootfast-window.mp4 > C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/stage6_clip_log.txt 2>&1
echo "rc=$?" >> C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/stage6_clip_log.txt
