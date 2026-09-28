#!/bin/bash
# the builder's carry (stages 1-3) on the base and on later tips / other scratch builds; the diff each writes
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
rm -rf $S/compose4; mkdir -p $S/compose4
for SRC in ../02-chain/sc-tendril-t3.html ../02-chain/sc-tendril-fx.html ../02-chain/sc-onslaught-fx.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/angelus/links/sc-angelus-b9.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/oracle/links/sc-oracle-sight.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron/links/sc-coldiron-temper-b93.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper/links/sc-lightkeeper-bulwark-b9.5.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone/links/sc-lodestone-b215.html C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker/links/sc-widowmaker-b1075.html; do
  N=$(basename $SRC .html); D=$S/compose4/$N; mkdir -p $D
  $PY ironhail_build.py --stage 1 --src $SRC --out $D/sc-ironhail-c1.html > $D/log.txt 2>&1 &&   $PY ironhail_build.py --stage 2 --src $D/sc-ironhail-c1.html --out $D/sc-ironhail-c2.html >> $D/log.txt 2>&1 &&   $PY ironhail_build.py --stage 3 --src $D/sc-ironhail-c2.html --out $D/sc-ironhail-c3.html >> $D/log.txt 2>&1
  rc=$?
  if [ $rc = 0 ]; then diff $SRC $D/sc-ironhail-c3.html | grep '^[<>]' > $D/diff.txt; echo "$N rc=0 lines=$(wc -l < $D/diff.txt) $(md5sum < $D/diff.txt | cut -c1-12) relics=$(grep -o '[0-9]* relics in the roster' $D/log.txt | tail -1)"; else echo "$N rc=$rc $(tail -3 $D/log.txt | tr '\n' ' ')"; fi
done
