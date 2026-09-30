# Every reading in findings.md, from the renders in $O (commands.sh steps 1-2). bash readings.sh > readings.txt
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SP=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad
W=$SP/batch/spellbreaker/s6/clipwork
O=$SP/audio_trace
cd C:/dev/sundered-crown/06-docs/v111/runs/audio_trace
short() { sed "s#$O/##g; s#$W/#clipwork/#g"; }

echo "=== A. PAIRS, whole track (renderAudio's 16-bit PCM unless marked AAC) ==="
while IFS='|' read lab a b; do
  $PY diff_wavs.py "$a" "$b" --label "$lab" --quiet | short
done <<EOF
integrator's pair (AAC decodes): fx clip vs b7.5 clip|$W/clip.wav|$W/base.wav
NULL, Math.random free: b7.5 vs b7.5 (one page, one event list, two renders)|$O/b75_r0_none.wav|$O/b75_r1_none.wav
NULL, Math.random free: fx vs fx|$O/fx_r0_none.wav|$O/fx_r1_none.wav
NULL, Math.random pinned: b7.5 vs b7.5|$O/b75_r2_1.wav|$O/b75_r3_1.wav
NULL, Math.random pinned, two page loads: b7.5|$O/b75v_r0_1.wav|$O/b75_r2_1.wav
NULL, Math.random pinned, two page loads: fx|$O/fxv_r0_1.wav|$O/fx_r2_1.wav
BUILD, Math.random free: fx vs b7.5|$O/fx_r0_none.wav|$O/b75_r0_none.wav
BUILD, Math.random pinned: fx vs b7.5|$O/fx_r2_1.wav|$O/b75_r2_1.wav
BUILD, pinned, repo 02-chain links: fx vs b7.5|$O/rfx_r0_1.wav|$O/rb75_r0_1.wav
SHARED VOICES, pinned: fx synth vs b7.5 synth on the same 107 events (cast, stuns, close left out)|$O/fxv_r2_1_drop-spellbreaker-spellbreaker-stun-spellbreaker-close.wav|$O/b75v_r1_1_drop-spellbreaker.wav
CAST ONLY, pinned: fx synth vs b7.5 synth on the same 108 events (stuns, close left out)|$O/fxv_r1_1_drop-spellbreaker-stun-spellbreaker-close.wav|$O/b75v_r0_1.wav
WHICH RANDOM, b7.5 repo link: only the hall's impulse response free (calls 0-249635)|$O/rb75_r1_1_free-0-249636.wav|$O/rb75_r2_1_free-0-249636.wav
WHICH RANDOM: only the synth's noise buffer free (calls 249636-278435)|$O/rb75_r3_1_free-249636-278436.wav|$O/rb75_r4_1_free-249636-278436.wav
WHICH RANDOM: only the bed's noise buffer free (calls 278436-304895)|$O/rb75_r5_1_free-278436-304896.wav|$O/rb75_r6_1_free-278436-304896.wav
AAC: the same wav encoded twice|$O/b75_r2_1_aac1.wav|$O/b75_r2_1_aac2.wav
EOF

echo; echo "=== B. OVER TIME, 0.5 s windows ==="
$PY window_table.py 0.5 "integrator AAC fx-b7.5" $W/clip.wav $W/base.wav \
  "AAC NULL, random free, b7.5" $O/b75_r0_none_aac1.wav $O/b75_r1_none_aac1.wav \
  "PCM NULL, synth noise free" $O/rb75_r3_1_free-249636-278436.wav $O/rb75_r4_1_free-249636-278436.wav \
  "PCM BUILD, pinned fx-b7.5" $O/fx_r2_1.wav $O/b75_r2_1.wav \
  "PCM CAST ONLY, pinned" $O/fxv_r1_1_drop-spellbreaker-stun-spellbreaker-close.wav $O/b75v_r0_1.wav | short

echo; echo "=== C. clip_audio6.py's CONTROL rows, on each pair ==="
$PY control_rows.py "integrator AAC: fx vs b7.5" $W/clip.wav $W/base.wav \
  "PCM random free: fx vs b7.5" $O/fx_r0_none.wav $O/b75_r0_none.wav \
  "PCM random free NULL: b7.5 x2" $O/b75_r0_none.wav $O/b75_r1_none.wav \
  "PCM random free NULL: fx x2" $O/fx_r0_none.wav $O/fx_r1_none.wav \
  "PCM pinned: fx vs b7.5" $O/fx_r2_1.wav $O/b75_r2_1.wav \
  "PCM pinned NULL: b7.5 x2" $O/b75_r2_1.wav $O/b75_r3_1.wav \
  "AAC random free: fx vs b7.5" $O/fx_r0_none_aac1.wav $O/b75_r0_none_aac1.wav \
  "AAC random free NULL: b7.5 x2" $O/b75_r0_none_aac1.wav $O/b75_r1_none_aac1.wav \
  "AAC pinned: fx vs b7.5" $O/fx_r2_1_aac1.wav $O/b75_r2_1_aac1.wav \
  "AAC pinned NULL: b7.5 x2" $O/b75_r2_1_aac1.wav $O/b75_r3_1_aac1.wav

echo; echo "=== D. THE EVENT LISTS AND THE DIRECTOR'S SEND (filmed links) ==="
$PY events_diff.py $O fx b75
echo; echo "--- repo 02-chain links ---"
$PY events_diff.py $O rfx rb75 | head -12

echo; echo "=== E. WHERE THE PINNED BUILD PAIRS FIRST DIFFER BY MORE THAN THE 1-LSB FLOOR ==="
$PY first_real_diff.py $O fx_r2_1.wav b75_r2_1.wav rfx_r0_1.wav rb75_r0_1.wav \
  fxv_r1_1_drop-spellbreaker-stun-spellbreaker-close.wav b75v_r0_1.wav \
  fxv_r2_1_drop-spellbreaker-spellbreaker-stun-spellbreaker-close.wav b75v_r1_1_drop-spellbreaker.wav \
  b75_r2_1.wav b75_r3_1.wav
