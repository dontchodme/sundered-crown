#!/bin/bash
# STAGE 6 BUILDER CHECKS (v107): refusals, and every link rebuilt from the bare tip. Scratch only.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D=$S/tmp/rebuild15; rm -rf $D; mkdir -p $D
echo "# builder_checks6b $(date +%H:%M) lightkeeper_build.py $(sha256sum lightkeeper_build.py | cut -c1-16)"
refuse(){ local what=$1; shift
  if $PY lightkeeper_build.py "$@" > $D/r.log 2>&1; then echo "FAIL  $what: it WROTE"; else echo "ok    $what refuses: $(grep -vE '^\s*ok|^$|^LIGHTKEEPER|^  src|^  base' $D/r.log | tail -1)"; fi; }
L=$S/links
refuse "stage 6 twice (on the fx link)" --stage 6 --src $L/sc-lightkeeper-bulwark-b9.5-fx.html --out $D/sc-lightkeeper-x1.html
refuse "stage 6 on stage 3's link (blade 10.54)" --stage 6 --src $L/sc-lightkeeper-bulwark.html --out $D/sc-lightkeeper-x2.html
refuse "stage 6 on stage 2's link" --stage 6 --src $L/sc-lightkeeper-wall.html --out $D/sc-lightkeeper-x3.html
refuse "stage 6 on stage 1's link" --stage 6 --src $L/sc-lightkeeper-stub.html --out $D/sc-lightkeeper-x4.html
refuse "stage 6 on the bare tip" --stage 6 --src ../02-chain/sc-tendril-t3.html --out $D/sc-lightkeeper-x5.html
refuse "stage 6 over an existing link" --stage 6 --src $L/sc-lightkeeper-bulwark-b9.5.html --out $L/sc-lightkeeper-bulwark-b9.5-fx.html
refuse "stage 6 to a name not sc-lightkeeper*" --stage 6 --src $L/sc-lightkeeper-bulwark-b9.5.html --out $D/sc-other-fx.html
refuse "stage 5 on the fx link" --stage 5 --src $L/sc-lightkeeper-bulwark-b9.5-fx.html --out $D/sc-lightkeeper-x6.html
# every link rebuilt from the bare tip, stages 1, 2, 3, 5, 6
src=../02-chain/sc-tendril-t3.html; n=0
for sn in 1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html 6:sc-lightkeeper-bulwark-b9.5-fx.html; do
  st=${sn%%:*}; nm=${sn#*:}
  if ! $PY lightkeeper_build.py --stage $st --src $src --out $D/$nm > $D/$nm.log 2>&1; then echo "FAIL  stage $st refused: $(tail -2 $D/$nm.log)"; n=$((n+1)); break; fi
  if cmp -s $D/$nm $L/$nm; then echo "ok    stage $st -> $nm $(sha256sum $D/$nm | cut -c1-16) == the link (cmp), CR $($PY -c "import sys; print(open(sys.argv[1], 'rb').read().count(13))" $D/$nm)"; else echo "FAIL  stage $st -> $nm differs from the link"; n=$((n+1)); fi
  src=$D/$nm; done
echo "# builder_checks6b: $n FAIL"
