#!/bin/bash
# The carry, dry (2026-09-29 re-check on the newest tips): aureole_build.py stages 1 -> 2 -> 3 -> 5 on every
# newest link of the batch's lineage, to scratch. Every stage must apply and parse, and every tip must get the same lines.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
cd C:/dev/sundered-crown/tools
OUT=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/aureole/compose2; rm -rf $OUT; mkdir -p $OUT
for T in ../02-chain/sc-tendril-t3.html ../02-chain/sc-widowmaker-fxout.html ../02-chain/sc-ironhail-fxout.html ../02-chain/sc-ironhail-sunder-fx.html ../02-chain/sc-lodestone-b205-fx.html          C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/angelus/links/sc-angelus-b9-fx.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/censer/links/sc-censer-consecration-b25.5.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron/links/sc-coldiron-temper-fx.html          C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper/links/sc-lightkeeper-bulwark-b9.5-fx.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/oracle/links/sc-oracle-fx.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker/links/sc-widowmaker-b1075-fx-specout.html; do
  n=$(basename $T .html); d=$OUT/$n; mkdir -p $d
  ok=1
  $PY aureole_build.py --stage 1 --src $T --out $d/sc-aureole-stub.html > $d/log.txt 2>&1 || ok=0
  [ $ok = 1 ] && { $PY aureole_build.py --stage 2 --src $d/sc-aureole-stub.html --out $d/sc-aureole-halo.html >> $d/log.txt 2>&1 || ok=0; }
  [ $ok = 1 ] && { $PY aureole_build.py --stage 3 --src $d/sc-aureole-halo.html --out $d/sc-aureole-bless.html >> $d/log.txt 2>&1 || ok=0; }
  [ $ok = 1 ] && { $PY aureole_build.py --stage 5 --src $d/sc-aureole-bless.html --out $d/sc-aureole-b12.5.html >> $d/log.txt 2>&1 || ok=0; }
  if [ $ok = 1 ]; then
    h=$(diff $T $d/sc-aureole-b12.5.html | grep '^[<>]' | sort | md5sum | cut -c1-12)
    r=$(grep -o '[0-9]* relics in the roster' $d/log.txt | tail -1)
    echo "$n ($(sha256sum $T | cut -c1-16)): stages 1-5 apply and parse; $r; the diff's lines md5 $h ($(diff $T $d/sc-aureole-b12.5.html | grep -c '^[<>]') lines)"
  else
    echo "$n: REFUSED -- $(grep -E 'wrong base|ANCHOR|REFUSING|refusing' $d/log.txt | head -1)"
  fi
  rm -f $d/*.html
done
