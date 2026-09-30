#!/bin/bash
# The carry, dry: spellbreaker_build.py stages 1 -> 2 -> 3 (-> 5 when BLADE is set) on every newest link of the
# batch's lineage (02-chain tips and the in-flight builds' scratch tips), to scratch. Every stage must apply and
# parse, and every tip must take the same lines.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch
cd C:/dev/sundered-crown/tools
OUT=$SB/spellbreaker/compose; rm -rf $OUT; mkdir -p $OUT
FINAL=${1:-3}
TIPS="../02-chain/sc-tendril-t3.html"
for t in sc-aureole-b12.5-fx sc-aureole-fxout sc-censer-fxout sc-censer-consecration-b25.5-fx sc-lightkeeper-fxout sc-lightkeeper-bulwark-b9.5-fx sc-angelus-b9-fx sc-oracle-fx sc-widowmaker-fxout sc-lodestone-b205-fx sc-ironhail-fxout sc-ironhail-sunder-fx sc-coldiron-temper-fx; do
  [ -f ../02-chain/$t.html ] && TIPS="$TIPS ../02-chain/$t.html"; done
for t in aureole/links/sc-aureole-b12.5.html censer/links/sc-censer-consecration-b25.5.html lightkeeper/links/sc-lightkeeper-bulwark-b9.5-fx.html \
         widowmaker/links/sc-widowmaker-b1075-fx-specout.html coldiron/links/sc-coldiron-temper-fx.html angelus/links/sc-angelus-b9-fx.html \
         oracle/links/sc-oracle-fx.html; do [ -f $SB/$t ] && TIPS="$TIPS $SB/$t"; done
for d in heartwood thornwake goreshard censer; do
  L=$(ls -t $SB/$d/links/*.html 2>/dev/null | head -1); [ -n "$L" ] && TIPS="$TIPS $L"; done
for T in $TIPS; do
  n=$(basename $T .html); d=$OUT/$n; mkdir -p $d
  ok=1
  $PY spellbreaker_build.py --stage 1 --src $T --out $d/sc-spellbreaker-stub.html > $d/log.txt 2>&1 || ok=0
  [ $ok = 1 ] && { $PY spellbreaker_build.py --stage 2 --src $d/sc-spellbreaker-stub.html --out $d/sc-spellbreaker-stun.html >> $d/log.txt 2>&1 || ok=0; }
  [ $ok = 1 ] && { $PY spellbreaker_build.py --stage 3 --src $d/sc-spellbreaker-stun.html --out $d/sc-spellbreaker-unmaking.html >> $d/log.txt 2>&1 || ok=0; }
  last=$d/sc-spellbreaker-unmaking.html
  if [ $ok = 1 ] && [ "$FINAL" = 5 ]; then
    $PY spellbreaker_build.py --stage 5 --src $d/sc-spellbreaker-unmaking.html --out $d/sc-spellbreaker-final.html >> $d/log.txt 2>&1 || ok=0
    last=$d/sc-spellbreaker-final.html
  fi
  if [ $ok = 1 ]; then
    h=$(diff $T $last | grep '^[<>]' | sort | md5sum | cut -c1-12)
    r=$(grep -o '[0-9]* relics in the roster' $d/log.txt | tail -1)
    echo "$n ($(sha256sum $T | cut -c1-16)): stages 1-$FINAL apply and parse; $r; the diff's lines md5 $h ($(diff $T $last | grep -c '^[<>]') lines)"
  else
    echo "$n: REFUSED -- $(grep -E 'wrong base|ANCHOR|REFUSING|refusing|already' $d/log.txt | head -1)"
  fi
  rm -f $d/*.html
done
