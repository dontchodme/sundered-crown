#!/bin/bash
# STAGE 6's CARRY (v104 §5e): the final builder, stages 1-2-3-5-6, on the base,
# the batch line's newest chain links and every in-flight scratch build's
# newest link. Read-only on every source; writes under s6/compose6/ only.
. "C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/angelus/env.sh"
B="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch"
cd $T
C=$S/s6/compose6; rm -rf $C; mkdir -p $C
echo "compose6 $(date '+%F %H:%M %Z')  builder $(sha256sum angelus_build.py | cut -c1-16)"
srcs="$BASE $R/02-chain/sc-ironhail-fxout.html $R/02-chain/sc-ironhail-sunder-fx.html $R/02-chain/sc-coldiron-temper-fx.html $R/02-chain/sc-widowmaker-fxout.html $R/02-chain/sc-lodestone-b205-fx.html"
for d in bindweed coldiron ironhail lightkeeper lodestone oracle portcullis widowmaker; do
  f=$(ls -t $B/$d/links/sc-*.html 2>/dev/null | head -1); [ -n "$f" ] && srcs="$srcs $f"
done
addh() { diff <(tr -d '\r' < "$1") <(tr -d '\r' < "$2") | grep '^>' | sha256sum | cut -c1-12; }
remh() { diff <(tr -d '\r' < "$1") <(tr -d '\r' < "$2") | grep '^<' | sha256sum | cut -c1-12; }
cnt() { diff "$1" "$2" | grep -c "^$3"; }
echo "REFERENCE  b9 -> b9-fx (the scratch links): +$(cnt $S/links/sc-angelus-b9.html $S/links/sc-angelus-b9-fx.html '>') -$(cnt $S/links/sc-angelus-b9.html $S/links/sc-angelus-b9-fx.html '<') lines, added $(addh $S/links/sc-angelus-b9.html $S/links/sc-angelus-b9-fx.html) removed $(remh $S/links/sc-angelus-b9.html $S/links/sc-angelus-b9-fx.html)"
i=0
for f in $srcs; do
  i=$((i+1)); nm=$(basename $f .html); o=$C/$i-$nm; mkdir -p $o
  ok=ok
  $PY angelus_build.py --stage 1 --src $f --out $o/sc-angelus.html > $o/log.txt 2>&1 || ok=FAIL1
  [ $ok = ok ] && { $PY angelus_build.py --stage 2 --src $o/sc-angelus.html --out $o/sc-angelus-rise.html >> $o/log.txt 2>&1 || ok=FAIL2; }
  [ $ok = ok ] && { $PY angelus_build.py --stage 3 --src $o/sc-angelus-rise.html --out $o/sc-angelus-heal.html >> $o/log.txt 2>&1 || ok=FAIL3; }
  [ $ok = ok ] && { $PY angelus_build.py --stage 5 --src $o/sc-angelus-heal.html --out $o/sc-angelus-b9.html >> $o/log.txt 2>&1 || ok=FAIL5; }
  [ $ok = ok ] && { $PY angelus_build.py --stage 6 --src $o/sc-angelus-b9.html --out $o/sc-angelus-b9-fx.html >> $o/log.txt 2>&1 || ok=FAIL6; }
  if [ $ok = ok ]; then
    x=""; [ "$f" = "$BASE" ] && x="  scratch link $(sha256sum $S/links/sc-angelus-b9-fx.html | cut -c1-16) built $(sha256sum $o/sc-angelus-b9-fx.html | cut -c1-16)"
    echo "$nm  src $(sha256sum $f|cut -c1-16)  ok  stage 5->6 +$(cnt $o/sc-angelus-b9.html $o/sc-angelus-b9-fx.html '>') -$(cnt $o/sc-angelus-b9.html $o/sc-angelus-b9-fx.html '<') added $(addh $o/sc-angelus-b9.html $o/sc-angelus-b9-fx.html) removed $(remh $o/sc-angelus-b9.html $o/sc-angelus-b9-fx.html)  1-5 added $(addh $f $o/sc-angelus-b9.html)  $(grep -o '[0-9]* relics in the roster' $o/log.txt | tail -1)$x"
  else echo "$nm  src $(sha256sum $f|cut -c1-16)  $ok  $(grep -i 'refus\|wrong\|error' $o/log.txt | head -2 | tr '\n' ' ')"; fi
  rm -f $o/sc-angelus.html $o/sc-angelus-rise.html $o/sc-angelus-heal.html
done
