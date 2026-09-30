# The audio trace, 2026-09-30 (Git Bash). Renders are big: they live in $O (scratch), the text readings here.
# Every browser at idle priority, two at once at most (a balance sweep had the rest of the PC).
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SP=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad
L=$SP/batch/spellbreaker/links          # the two links the integrator FILMED (the clip's own copies)
W=$SP/batch/spellbreaker/s6/clipwork    # the integrator's AAC decodes, clip.wav (fx) and base.wav (b7.5)
O=$SP/audio_trace
R=C:/dev/sundered-crown/06-docs/v111/runs/audio_trace
cd $R

# 1. renders (each: one page, the clip's frame loop once, then renderAudio N times on that one event list)
$PY ../idle_exec.py $PY render_trace.py $L/sc-spellbreaker-b7.5.html    b75 $O                    # none,none,1,1
$PY ../idle_exec.py $PY render_trace.py $L/sc-spellbreaker-b7.5-fx.html fx  $O
$PY ../idle_exec.py $PY render_trace.py $L/sc-spellbreaker-b7.5.html    b75v $O --seeds "1,1/drop=spellbreaker"
$PY ../idle_exec.py $PY render_trace.py $L/sc-spellbreaker-b7.5-fx.html fxv  $O \
    --seeds "1,1/drop=spellbreaker-stun+spellbreaker-close,1/drop=spellbreaker+spellbreaker-stun+spellbreaker-close"
$PY ../idle_exec.py $PY render_trace.py C:/dev/sundered-crown/02-chain/sc-spellbreaker-b7.5.html rb75 $O \
    --seeds "1,1/free=0-249636,1/free=0-249636,1/free=249636-278436,1/free=249636-278436,1/free=278436-304896,1/free=278436-304896"
$PY ../idle_exec.py $PY render_trace.py C:/dev/sundered-crown/02-chain/sc-spellbreaker-b7.5-fx.html rfx $O --seeds "1,none"
cat $O/b75.log $O/fx.log $O/b75v.log $O/fxv.log $O/rb75.log $O/rfx.log > renders.txt

# 2. the clip's AAC, on renderAudio's own wavs (and the same wav twice)
$PY ../idle_exec.py $PY aac_roundtrip.py 1 $O/b75_r0_none.wav $O/b75_r1_none.wav $O/fx_r0_none.wav $O/b75_r2_1.wav $O/fx_r2_1.wav $O/b75_r3_1.wav
$PY ../idle_exec.py $PY aac_roundtrip.py 2 $O/b75_r2_1.wav

# 3. readings
bash readings.sh > readings.txt
