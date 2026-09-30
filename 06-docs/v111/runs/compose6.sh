#!/bin/bash
# The carry, dry, with stage 6: spellbreaker_build.py stages 1 -> 2 -> 3 -> 5 -> 6 on every newest link of the
# batch's lineage (02-chain tips and the in-flight builds' scratch tips: compose.sh's list), to scratch. Every
# stage must apply and parse; the change set of stages 1-5 and the change set of stage 6 alone are printed
# (md5 of the sorted diff lines) so a tip that takes different lines shows.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch
cd C:/dev/sundered-crown/tools
OUT=$SB/spellbreaker/compose6; rm -rf $OUT; mkdir -p $OUT
echo "builder spellbreaker_build.py $(sha256sum spellbreaker_build.py | cut -c1-16)"
TIPS="../02-chain/sc-tendril-t3.html"
for t in sc-aureole-b12.5-fx sc-aureole-fxout sc-censer-fxout sc-censer-consecration-b25.5-fx sc-lightkeeper-fxout sc-lightkeeper-bulwark-b9.5-fx sc-angelus-b9-fx sc-oracle-fx sc-widowmaker-fxout sc-lodestone-b205-fx sc-ironhail-fxout sc-ironhail-sunder-fx sc-coldiron-temper-fx; do
  [ -f ../02-chain/$t.html ] && TIPS="$TIPS ../02-chain/$t.html"; done
for t in aureole/links/sc-aureole-b12.5.html censer/links/sc-censer-consecration-b25.5.html lightkeeper/links/sc-lightkeeper-bulwark-b9.5-fx.html \
         widowmaker/links/sc-widowmaker-b1075-fx-specout.html coldiron/links/sc-coldiron-temper-fx.html angelus/links/sc-angelus-b9-fx.html \
         oracle/links/sc-oracle-fx.html; do [ -f $SB/$t ] && TIPS="$TIPS $SB/$t"; done
for d in heartwood thornwake goreshard censer; do
  L=$(ls -t $SB/$d/links/*.html 2>/dev/null | head -1); [ -n "$L" ] && TIPS="$TIPS $L"; done
nf=0
for T in $TIPS; do
  n=$(basename $T .html); d=$OUT/$n; mkdir -p $d
  ok=1
  $PY spellbreaker_build.py --stage 1 --src $T --out $d/sc-spellbreaker-stub.html > $d/log.txt 2>&1 || ok=0
  [ $ok = 1 ] && { $PY spellbreaker_build.py --stage 2 --src $d/sc-spellbreaker-stub.html --out $d/sc-spellbreaker-stun.html >> $d/log.txt 2>&1 || ok=0; }
  [ $ok = 1 ] && { $PY spellbreaker_build.py --stage 3 --src $d/sc-spellbreaker-stun.html --out $d/sc-spellbreaker-unmaking.html >> $d/log.txt 2>&1 || ok=0; }
  [ $ok = 1 ] && { $PY spellbreaker_build.py --stage 5 --src $d/sc-spellbreaker-unmaking.html --out $d/sc-spellbreaker-b7.5.html >> $d/log.txt 2>&1 || ok=0; }
  [ $ok = 1 ] && { $PY spellbreaker_build.py --stage 6 --src $d/sc-spellbreaker-b7.5.html --out $d/sc-spellbreaker-b7.5-fx.html >> $d/log.txt 2>&1 || ok=0; }
  if [ $ok = 1 ]; then
    h5=$(diff $T $d/sc-spellbreaker-b7.5.html | grep '^[<>]' | sort | md5sum | cut -c1-12)
    n5=$(diff $T $d/sc-spellbreaker-b7.5.html | grep -c '^[<>]')
    h6=$(diff $d/sc-spellbreaker-b7.5.html $d/sc-spellbreaker-b7.5-fx.html | grep '^[<>]' | sort | md5sum | cut -c1-12)
    n6=$(diff $d/sc-spellbreaker-b7.5.html $d/sc-spellbreaker-b7.5-fx.html | grep -c '^[<>]')
    r=$(grep -o '[0-9]* relics in the roster' $d/log.txt | tail -1)
    echo "$n ($(sha256sum $T | cut -c1-16)): stages 1-6 apply and parse; $r; stages 1-5 md5 $h5 ($n5 lines); stage 6 alone md5 $h6 ($n6 lines); fx $(sha256sum $d/sc-spellbreaker-b7.5-fx.html | cut -c1-16)"
  else
    nf=$((nf+1))
    echo "$n: FAIL -- $(grep -E 'wrong base|ANCHOR|REFUSING|refusing|already|goes on' $d/log.txt | head -1)"
  fi
  rm -f $d/*.html
done
echo "FAIL: $nf"
