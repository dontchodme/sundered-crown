# HEARTWOOD / ROOTFAST -- STAGE 6 VOICES -- STATE
2026-09-30 start: stage6-voice/ did not exist; tools/heartwood_voice_lab.py did not exist. Starting fresh.
BASE for rows: ../links/sc-heartwood-b11.html (want sha256[:16] aff84a04b303a402)
base sha re-checked aff84a04b303a402 (2026-09-30 step 1)
## read so far
- design v85 §4 SOUND: cast "a green creak, 0.4s"; root "a short creak-and-crack (Tendril's root voice, reused,
  quieter at 1.0s than at the vine's longer holds)"; close nothing.
- precedents read: bindweed_voice_lab.py (Tendril; its ROOT = DEEP, arm text in 02-chain/sc-tendril-fx.html 7525-7551,
  g 0.5179 kc 0.2683 kt 0.3464), ironwood_voice_lab.py (RENDER_JS, low_share, pulsed, centroid), zenith_voice_lab.py (basic etc.)
- 'bindweed-root' is NOT on b11 (tendril-t3 based) -> make 'heartwood-root' = Tendril's arm body verbatim, only g changed; say so.
- Vine hold = rootPer 0.3 x entangle stacks (cap 4) = 0.3-1.2 s (82% at cap -> 1.2 s). Heartwood's hold is 1.0.
- hooks: cast = fireUlt's existing SFX.play("ult",{w:"heartwood"}) 16270 -> arm before rune-crack fallback (anchor
  '        } else {                                        // rune-crack', unique). root = rootBlow after '    T.rooted++;'
  (unique in b11 and in every other scratch build's links). The hit voice plays at 15152 AFTER rootBlow (15004): same frame.
- a parallel heartwood/stage6-picture lab exists (just started): if it anchors on T.rooted++ too, both re-emit the anchor once -> compose.
## plan
- tools/heartwood_voice_lab.py: controls reproduce (rune-crack 0.608/450, BAR 0.364/300, hit@11.6 0.443/80); cast 5 candidates +
  controls (HELD, DRY=ironwood-wither, CRACK=Tendril root, WITHER=falling, RUNECRACK); root = Tendril's DEEP at a gain ladder
  (-3..-11 dB) + controls FULL / FAINT / PARADOX-PIN; Sfx row check (arms == candidates 1e-6, 30+ others unchanged);
  rootBlow row wire check (fights identical, other SFX identical, root voices == rooted, none on kill, cast voices == casts,
  nothing from tickRootfast) + sim-write control; real window; end to end in a 2nd browser (after the 1st closes).
## step 2 (lab written)
- tools/heartwood_voice_lab.py written (LF). Readings in its docstring: every rooted blow voiced (T.rooted); root = Tendril's
  DEEP body verbatim, g ladder -3..-11 dB, pick = LOUDEST passing (quieter >= 3 dB under Tendril's quietest draw, <= blow,
  >= 2x wall, on-frame keeps >= 6 dB vs blows 9/11/13/23!); cast = 5 creak candidates (GROAN TRUNK RISING BOUGH SAP),
  green = centroid <= 0.5x dry creak (ironwood-wither) & fall >= -200c, no crack, audible 330-470.
- crit is x2.1 (CONFIG chaos.critMul), jitter +/-15% -> frame blows 9/11/13/23!
- next: smoke run --seeds 1 --e2e-seeds 0 -> run_smoke.txt
## step 3 smoke run (run_smoke.txt, --seeds 1, no e2e): root machinery all good
- controls reproduce; 12 relics on rune-crack incl heartwood + bindweed; ult/bindweed-root on b11 == rune-crack (6e-8)
- ROOT pick G-7dB (g 0.2313): -4.1 dB re Tendril (compressor), -4.3 re hit@11; ladder -3/-5 fail quieter; FULL/FAINT/PARADOX/BACK controls fail right
- wire 74/74 identical, 1167 rooted -> 1167 voices (646 new holds), 0 on 24 kills, 0 at closes; control 6/74
- blows the root lands with: dmg 13-17 mostly (not 9-13!) -> FRAME_BLOWS should come from the wire run's observed dmgs
- CAST: all 5 fail: (a) crack_info stands 12-21 dB on every pulse train (instrument blind: p90 of a click train's
  1 ms HF envelope is the gap) -> need ALONE (loudest HF ms over every other HF ms >= 20 ms away); (b) register vs hit@11
  0.82-0.92 and thornwake 0.82-0.84 (low creaks sit in the blow's register). -> explore constructions (scratch explore.py)
## step 4 exploration (explore.py -> explore1-4.txt)
- ALONE (loudest HF ms over every HF ms >= 20 ms away): Tendril root 29.4 dB, dry creak 2.3, creaks 0-2 -> the cast's no-crack instrument
- any creak with its energy at 110-300 Hz: thornwake 0.82-0.90 / vinesower 0.76-0.84 / hit 0.78-0.92 (the school's register);
  sawtooth/square/friction grains spread into emberedge/paradox/dry 0.80+; notes 320-400 Hz pass every register (max 0.72-0.78,
  the dry creak / paradox pin); a 90 Hz sine groan passes too (0.78 death) but its pitch reads smeared.
- centroid FALL-C reads a steady pulse train as falling (GROAN -181, TRUNK -443, sine90 -293): instrument, replace by NOTE-FALL (pitch)
- DECISION (first cut corrected, recorded in the lab): GREEN = NOTE <= the dry creak's lowest note (its last 100 audible ms, 420 Hz)
  and NOTE-FALL >= -200 c; no crack = ALONE < 10 dB; candidates GROAN(130, kept as the first cut's) KNOT(sine 380) TIMBER(360, mode .2)
  RISING(300->400 over 0.3 s) SAP(380, minor-third give). FRAME_BLOWS from the wire run's observed blows (wire moved before the root).
- step 5: patch2 (second cut: note-based green, ALONE, mid-register candidates) + patch3 (wire before root, FRAME_BLOWS observed) applied; smoke2 running
- step 6: patch4 (what_cast, root rule wording, note-based comment). smoke2: cast pick RISING (0.75 dry-creak), root G-7dB (keepR 6.9 at the 64! crit); blows 0-31 plain, crits 21-64. FULL RUN 1 started (run_full1.txt, wavs 05-reference/v112)
- step 7: patch5 (docstring second cut) NOT yet applied; patch6 (SHIFT, DEEP candidate, docstring) applied? see below
- step 7: patch5 (docstring) + patch6 (SHIFT gate, DEEP candidate 90 Hz, 6 cast candidates) applied, compiled
- step 8: FULL RUN 1 (pre-patch6 code) rc=0: wire 148/148, 2318 rooted->2318 voices, control 11/148; e2e 74/74; cast RISING, root G-7dB. Now: remove run-1 wavs, final run with patched lab
- step 9: final run 1 rc=1: SHIFT sign inverted (WITHER read +669). Fixed (return +lag: A=last,B=first as crack_shift). Removing wavs, final run 2
- step 10: FINAL RUN rc=0 (run_final.txt/json, rows_final.json): cast 5 RISING (g 0.2768), root 3 G-7dB (g 0.2313); wire 148/148, control 11/148; e2e 74/74 patched sha 6a19b58add3cf38e; 22 wavs in 05-reference/v112
- step 11: CARRY CHECK PASS (carry_check.py -> carry_ironhail.txt): builder stages 1/2/3/5 onto sc-ironhail-fxout into stage6-voice/carry/,
  rows_final applied unchanged (anchors once), 76/76 fights identical, counts exact, tip's bindweed-root == reused body (6e-8)
- reg_all*.py (info, not gated): vs all 101 ult voices on that tip RISING >0.80 with 5 (lastlight-cold .88, cindercleave-jet .86 ...);
  KNOT/SAP 3, TIMBER 8, DEEP 13 (redflail .94), GROAN 22; root 0.81-0.83 vs twinshade/shroudmaul/grudgebearer/cindercleave
- next: docstring THE PICKS filled (patch7), re-run final, rows must be byte-identical to rows_final_run2.json
- step 12: docstring-only edits (picks, first-cut notes); final re-run 3 -> compare rows with rows_final_run2.json
## DONE 2026-09-30 (step 13)
- final run 3 rc=0 (run_final.txt/json); rows_final.json code+anchors byte-identical to run 2's, only the `why` render-noise
  numbers (1e-7) differ. rows_final.json sha256[:16] 4c38682da549a943; lab tools/heartwood_voice_lab.py 46d6f498df30b58b (LF)
- picks: cast 5 RISING (g 0.2768), root 3 G-7dB (g 0.2313, Tendril's body verbatim), close nothing
- 22 wavs in 05-reference/v112/heartwood-*.wav (gitignored); nothing else in the repo written (tools/__pycache__ is ignored)
- carry check on sc-ironhail-fxout PASS (carry_ironhail.txt; links in stage6-voice/carry/)
- next: StructuredOutput report
