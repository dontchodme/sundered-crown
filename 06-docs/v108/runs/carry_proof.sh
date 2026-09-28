#!/bin/bash
# v108 carry proof, re-run after the session that wrote the four links ended during its engine_ab:
# the links are rebuilt from the tip into scratch and must match 02-chain byte for byte, then the
# engine A/B against the scratch build, then the fx-out link and its gates, then yert's staff carry
# dry run on the new tip.
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown; O=$R/06-docs/v108/runs
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
T="$S/batch/ironhail/carry_check"; rm -rf "$T"; mkdir -p "$T"
cd $R/tools
src=../02-chain/sc-coldiron-temper-fx.html
: > $O/carry_links.txt
echo "sc-coldiron-temper-fx.html  the batch line's tip  $(sha256sum ../02-chain/sc-coldiron-temper-fx.html | cut -c1-16)" >> $O/carry_links.txt
for st in 1:sc-ironhail-stub 2:sc-ironhail-hail 3:sc-ironhail-sunder 6:sc-ironhail-sunder-fx; do
  n=${st#*:}; g=${st%%:*}; c=${n/sc-ironhail-/sc-ironhail-chk-}
  $PY ironhail_build.py --stage $g --src "$src" --out "$T/$c.html" > "$T/$c.log" 2>&1 || { echo "REBUILD FAILED $n"; exit 1; }
  a=$(sha256sum "$T/$c.html" | cut -c1-16); b=$(sha256sum ../02-chain/$n.html | cut -c1-16)
  [ "$a" = "$b" ] && ok=same || ok=DIFFERENT
  echo "  stage $g  $n.html  $b  (rebuilt from the tip: $a, $ok)" >> $O/carry_links.txt
  [ "$ok" = same ] || { echo "LINK MISMATCH $n"; exit 1; }
  src="$T/$c.html"
done
echo "links $(date +%H:%M:%S)"
IDS=$(cat $O/stage6/ids38.txt | tr -d '\r\n')
$PY engine_ab.py --a "$S/batch/ironhail/links/sc-ironhail-sunder-fx.html" --b ../02-chain/sc-ironhail-sunder-fx.html --ids "$IDS" --n 6 > $O/carry_engine_ab.txt 2>&1
grep -q "ENGINE A/B PASS" $O/carry_engine_ab.txt || { echo "CARRY ENGINE_AB FAILED"; exit 1; }
echo "carry engine_ab $(date +%H:%M:%S)"
bash $O/fxout/fxout.sh || exit 1
$PY staff_carry.py --src ../02-chain/sc-ironhail-fxout.html --out "$S/batch/ironhail/staves-on-fxout.html" > $O/fxout/staff_carry_dry.txt 2>&1; echo "exit $?" >> $O/fxout/staff_carry_dry.txt
echo "staff_carry $(date +%H:%M:%S)"
echo ALL-DONE
