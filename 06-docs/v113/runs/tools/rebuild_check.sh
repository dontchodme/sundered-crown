#!/bin/bash
# every link rebuilt from the bare base with the final builder, into tmp/rb, against the links on disk; and the carry, dry. $1 = BLADE
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
H=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
cd C:/dev/sundered-crown/tools
B=$1; RB=$S/tmp/rb; rm -rf $RB; mkdir -p $RB
{
echo "REBUILD FROM THE BARE BASE with tools/thornwake_build.py $(sha256sum thornwake_build.py | cut -c1-16)"
echo "base ../02-chain/sc-tendril-t3.html $(sha256sum ../02-chain/sc-tendril-t3.html | cut -c1-16)"
prev=../02-chain/sc-tendril-t3.html
for st in "1 stub" "2 bramble" "3 snare" "5 b$B"; do set -- $st; n=sc-thornwake-$2.html
  $PY thornwake_build.py --stage $1 --src $prev --out $RB/$n > $RB/$n.log 2>&1; rc=$?
  a=$(sha256sum $RB/$n 2>/dev/null | cut -c1-16); b=$(sha256sum $S/links/$n | cut -c1-16)
  echo "stage $1  $n  rebuilt $a  on disk $b  rc $rc  -> $([ "$a" = "$b" ] && echo IDENTICAL || echo DIFFERENT)"; prev=$RB/$n
done
echo; echo "REFUSALS (each must refuse):"
$PY thornwake_build.py --stage 1 --src $RB/sc-thornwake-stub.html --out $RB/sc-thornwake-x1.html 2>&1 | tail -1 | sed 's/^/  stage 1 on stage 1: /'
$PY thornwake_build.py --stage 3 --src $RB/sc-thornwake-stub.html --out $RB/sc-thornwake-x3.html 2>&1 | tail -1 | sed 's/^/  stage 3 on stage 1: /'
$PY thornwake_build.py --stage 5 --src $RB/sc-thornwake-bramble.html --out $RB/sc-thornwake-x5.html 2>&1 | tail -1 | sed 's/^/  stage 5 on stage 2: /'
$PY thornwake_build.py --stage 2 --src $RB/sc-thornwake-snare.html --out $RB/sc-thornwake-x2.html 2>&1 | tail -1 | sed 's/^/  stage 2 on stage 3: /'
$PY thornwake_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $S/links/sc-thornwake-stub.html 2>&1 | tail -1 | sed 's/^/  overwrite a link: /'
$PY thornwake_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $RB/sc-other.html 2>&1 | tail -1 | sed 's/^/  a name not sc-thornwake*: /'
} > $S/runs/rebuild_final.txt 2>&1
{
echo "THE CARRY, DRY: stages 1, 2, 3, 5 on later tips (scratch files, not links)"
for tip in ../02-chain/sc-spellbreaker-fxout.html ../02-chain/sc-aureole-fxout.html ../02-chain/sc-ironhail-fxout.html ../02-chain/sc-coldiron-temper-fx.html $H/links/sc-heartwood-b11.html; do
  D=$S/tmp/carry/$(basename $tip .html); rm -rf $D; mkdir -p $D; prev=$tip; line="$(basename $tip) $(sha256sum $tip | cut -c1-16) ->"
  for st in "1 stub" "2 bramble" "3 snare" "5 b$B"; do set -- $st; n=sc-thornwake-$2.html
    out=$($PY thornwake_build.py --stage $1 --src $prev --out $D/$n 2>&1); rc=$?
    line="$line s$1 $( [ $rc = 0 ] && sha256sum $D/$n | cut -c1-16 || echo "REFUSED:$(echo "$out" | tail -1)")"; prev=$D/$n
  done
  echo "$line   ($(echo "$out" | grep -o '[0-9]* relics in the roster'))"
done
echo; echo "AND THE OTHER FREEZE REDESIGN ON THIS BUILD'S FINAL: heartwood_build.py stages 1,2,3,5 on sc-thornwake-b$B"
D=$S/tmp/carry/heartwood-on-final; rm -rf $D; mkdir -p $D; prev=$S/links/sc-thornwake-b$B.html; line="sc-thornwake-b$B ->"
for st in "1 stub" "2 root" "3 rootfast" "5 b11"; do set -- $st; n=sc-heartwood-$2.html
  out=$($PY heartwood_build.py --stage $1 --src $prev --out $D/$n 2>&1); rc=$?
  line="$line s$1 $( [ $rc = 0 ] && sha256sum $D/$n | cut -c1-16 || echo "REFUSED:$(echo "$out" | tail -1)")"; prev=$D/$n
done
echo "$line"
} > $S/runs/carry_dry.txt 2>&1
cat $S/runs/rebuild_final.txt $S/runs/carry_dry.txt
