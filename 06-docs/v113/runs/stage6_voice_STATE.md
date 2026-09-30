# Thornwake / Bramblesnare stage 6 -- VOICES (lab state)

2026-09-30 start. No prior stage6-voice dir, no tools/thornwake_voice_lab.py: fresh start.

## Steps
- [ ] read design (§4 picture+sound, §5 brief stage 6), precedents (ironwood/zenith voice labs, canopy-fx wiring)
- [x] read: v84 (§4 SOUND: cast rustle-and-creak 0.4s replacing the arm; bramble opening dry crackle; snare = Tendril's root reused; bite soft snap), spellbreaker/bindweed/zenith/ironwood labs, widowmaker rows (precedent for REPLACING an own arm with a 4-line anchor)
- base links/sc-thornwake-b26.5.html fd5031063ecb6807; Sfx primitives (_burst/_sweep/_tone/buildChain) identical in base, sc-tendril-fx, sc-spellbreaker-fxout (d9baf15b7f8fa6d9)
- bindweed-root body (sc-tendril-fx 7525+) sha c5f203750ce3ed89, 609 bytes -> transcribe as thornwake-snare (the voice is not on this base: made, said so)
- --also target: tmp/carry/sc-spellbreaker-fxout/sc-thornwake-b26.5.html f7c32e86063abb8d (42 relics, carries bindweed-root)
- parallel: heartwood/stage6-voice (heartwood-root = Tendril body, g changed; anchors rune-crack fallback + '    T.rooted++;') -- no overlap
## plan
- ids: ult/thornwake (cast, replaces 'creak and cinch' 4-line arm, widowmaker precedent), thornwake-crackle (planted++), thornwake-snare (T.snares++), thornwake-bite (T.ticks++)
- rows: Sfx replace (4-line anchor); plantBramble after '    f.brambleTally.planted++;'; tickBramble after '            T.snares++;' and after '          T.ticks++;' (all unique in base)
- 05:46 wrote tools/thornwake_voice_lab.py (first draft); next: round 1 --no-wire
- round 1 (iter1.log, --no-wire): controls reproduce (rune-crack 0.608/450, BAR 0.364/300, hit@11.6 0.443/80); snare == Tendril root 1.8e-7, OFF 4.7e-5
  cast: NONE pass -- reg vs scour woosh 0.84-0.93 (spectrum-blind: rustle & woosh both band noise), thornshear 0.82 (LEAVES/BOUGH), BRIAR centroid 3.9-4.9k
  bite: STEM pick (0.39), but BRIGHT control PASSED (whole-voice centroid is the body's, blind to the snap)
  crackle: NONE pass -- reg vs wall 0.96, T:wither 0.87-0.91, scour tick 0.95 (all HF noise: REG blind to time)
  Sfx row fine: arms==candidates <=1.2e-7, 138 others unchanged 2e-7
- next: scratch explore.py for cast variants vs thornshear; round 2 rule changes (documented)
- round 2 (iter2.log): added cast 5 THORNS/6 BURRS, crackle 5 KNOTS/6 SPLINTERS; bite "soft" now reads the SNAP (first 10 ms centroid) -- BRIGHT now fails (2339 Hz)
  bite STEM (0.39 fork) PASS; crackle KNOTS PASS (0.73 scour tick); cast: THORNS out only on rustle centroid 3436-4143 (>4000), BURRS centroid + woosh 0.80
  NOTE Tendril's bite first-10ms centroid 1136-1301 Hz (body-dominated) -- docstring must not call it a bright snap
- next: explore Q5 lower centres / Q8 for the cast (centroid <4000, woosh <=0.80), then round 3
- round 3 (iter3.log --no-wire): ALL PASS. picks cast 8 NEEDLES (Q8 grains 2310-3900 + 330 Hz timber creak; 0.77 scour woosh), crackle 5 KNOTS (Q6 clicks 1185-2160; 0.73 scour tick), bite 1 STEM (0.39 fork), snare = Tendril root (same 8.9e-8, OFF 4.7e-5)
- round 4: BITE anchor moved '          T.ticks++;' -> '          f.brambleCd = u.tickCd;' (T.ticks++ occurs TWICE on the spellbreaker-fxout / aureole-fxout carries: a smite ticker). planted++/snares++/brambleCd unique on base + all carries.
- 06:15 RUNNING full run4 (bg): --also tmp/carry/sc-spellbreaker-fxout/sc-thornwake-b26.5.html, peers heartwood/bindweed/spellbreaker/widowmaker -> run4.log, rows_run4.json, run4.json
- 06:40 run4 (full) ALL CHECKS PASS: wire 148/148 (control 1/148), 490/856/1781/4287 voiced exactly; real window heard (cast +32.6, crackles med +11.6, bites med +14.0); e2e 74/74; also spellbreaker-fxout carry 82/82, snare == page's bindweed-root 1.2e-7; peers heartwood/bindweed/spellbreaker/widowmaker co-apply both orders
- text-only edits after run4: arm comments (nearest register named, bite audible), docstring PICKS/ROUNDS/SOFT. NEXT: final full run -> run_final.log, rows_final.json
## RESUME 2026-09-30 09:05 (new session: the earlier process exited)
- found: lab complete (run4 ALL CHECKS PASS, rows_run4.json); run_final.log CUT OFF at 06:28 inside the peer checks (after Heartwood's), no rows_final.json
- re-checked: base fd5031063ecb6807, sc-tendril-fx eea0cde5536955b3, carries unchanged (03:57); no other python/browser of mine running
- next: py_compile the lab, rows_check on rows_run4 vs every carry, then the final full run again -> run_final.log / rows_final.json / run_final.json
- 09:08 RUNNING final full run again (bg), same args as run4 -> run_final.log / rows_final.json / run_final.json (the cut log kept as run_final_cut0628.log)
- 09:20 docstring text only (lab running from memory): the per-cast figures ~1.6/~3.3/~7.7 were stage 3's; now stage 5 probe's 1.61/3.46/8.17 and this lab's 1.75/3.63/8.75. Final run past the voice picks (same picks as run4)
- 09:35 FINAL RUN DONE: run_final.log ALL CHECKS PASS exit 0; rows_final.json 11598 bytes sha a539532139eb01b7 (4 rows; differ from run4's in arm comments only); wire 148/148 (control 1/148), 490/856/1781/4287 voiced; e2e 74/74 (fd50..->8f8d06e90d66fc3f +7290); also spellbreaker-fxout 82/82 + snare==bindweed-root 1.2e-7; peers x4 both orders
- rows_check.py on rows_final: every anchor once on base + 5 carries; heartwood-on-final co-apply both orders IDENTICAL
- docstring text only after the run (round 4 note on the cut run; per-cast figures). DONE -- StructuredOutput next
