#!/bin/bash
# Every link rebuilt from the builder as it now stands, to a temporary folder, chained from the base;
# each must match the link's sha.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
cd C:/dev/sundered-crown/tools
R=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/aureole/rebuild; rm -rf $R; mkdir -p $R
echo "builder aureole_build.py $(sha256sum aureole_build.py | cut -c1-16); base sc-tendril-t3 $(sha256sum ../02-chain/sc-tendril-t3.html | cut -c1-16)"
$PY aureole_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $R/sc-aureole-stub.html > /dev/null || echo "stage 1 FAILED"
$PY aureole_build.py --stage 2 --src $R/sc-aureole-stub.html --out $R/sc-aureole-halo.html > /dev/null || echo "stage 2 FAILED"
$PY aureole_build.py --stage 3 --src $R/sc-aureole-halo.html --out $R/sc-aureole-bless.html > /dev/null || echo "stage 3 FAILED"
$PY aureole_build.py --stage 5 --src $R/sc-aureole-bless.html --out $R/sc-aureole-b12.5.html > /dev/null || echo "stage 5 FAILED"
$PY aureole_build.py --stage 5 --alt50 --src $R/sc-aureole-bless.html --out $R/sc-aureole-b11.5.html > /dev/null || echo "stage 5 --alt50 FAILED"
all=1
for n in sc-aureole-stub sc-aureole-halo sc-aureole-bless sc-aureole-b12.5 sc-aureole-b11.5; do
  a=$(sha256sum C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/aureole/links/$n.html | cut -c1-16); b=$(sha256sum $R/$n.html | cut -c1-16)
  [ "$a" = "$b" ] && echo "  $n  link $a  rebuilt $b  SAME" || { echo "  $n  link $a  rebuilt $b  DIFFERENT"; all=0; }
done
[ $all = 1 ] && echo "EVERY LINK REBUILDS BYTE FOR BYTE" || echo "A LINK DOES NOT REBUILD"
# and the refusals
echo "refusals:"
$PY aureole_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/aureole/links/sc-aureole-stub.html 2>&1 | tail -1
$PY aureole_build.py --stage 2 --src $R/sc-aureole-halo.html --out $R/sc-aureole-x.html 2>&1 | tail -1
$PY aureole_build.py --stage 1 --src $R/sc-aureole-stub.html --out $R/sc-aureole-y.html 2>&1 | tail -1
$PY aureole_build.py --stage 3 --src ../02-chain/sc-tendril-t3.html --out $R/sc-aureole-z.html 2>&1 | tail -1
$PY aureole_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $R/sc-other.html 2>&1 | tail -1
$PY aureole_build.py --stage 1 --src ../02-chain/sc-trunk.html --out $R/sc-aureole-w.html 2>&1 | tail -1
