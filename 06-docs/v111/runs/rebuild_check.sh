#!/bin/bash
# Every link rebuilt from the builder as it now stands, to a temporary folder, chained from the base;
# each must match the link's sha. Then the refusals.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=<scratch>
cd C:/dev/sundered-crown/tools
R=$SB/rebuild; rm -rf $R; mkdir -p $R
FIN=$1; ALT=$2; ALTR=$3
echo "builder spellbreaker_build.py $(sha256sum spellbreaker_build.py | cut -c1-16); base sc-tendril-t3 $(sha256sum ../02-chain/sc-tendril-t3.html | cut -c1-16)"
$PY spellbreaker_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $R/sc-spellbreaker-stub.html > /dev/null || echo "stage 1 FAILED"
$PY spellbreaker_build.py --stage 2 --src $R/sc-spellbreaker-stub.html --out $R/sc-spellbreaker-stun.html > /dev/null || echo "stage 2 FAILED"
$PY spellbreaker_build.py --stage 3 --src $R/sc-spellbreaker-stun.html --out $R/sc-spellbreaker-unmaking.html > /dev/null || echo "stage 3 FAILED"
$PY spellbreaker_build.py --stage 5 --src $R/sc-spellbreaker-unmaking.html --out $R/$FIN.html > /dev/null || echo "stage 5 FAILED"
$PY spellbreaker_build.py --stage 5 --alt50 --src $R/sc-spellbreaker-unmaking.html --out $R/$ALT.html > /dev/null || echo "stage 5 --alt50 FAILED"
$PY spellbreaker_build.py --stage 5 --alt-row --src $R/sc-spellbreaker-unmaking.html --out $R/$ALTR.html > /dev/null || echo "stage 5 --alt-row FAILED"
all=1
for n in sc-spellbreaker-stub sc-spellbreaker-stun sc-spellbreaker-unmaking $FIN $ALT $ALTR; do
  a=$(sha256sum $SB/links/$n.html | cut -c1-16); b=$(sha256sum $R/$n.html | cut -c1-16)
  [ "$a" = "$b" ] && echo "  $n  link $a  rebuilt $b  SAME" || { echo "  $n  link $a  rebuilt $b  DIFFERENT"; all=0; }
done
[ $all = 1 ] && echo "EVERY LINK REBUILDS BYTE FOR BYTE" || echo "A LINK DOES NOT REBUILD"
echo "refusals:"
echo -n "  overwrite: "; $PY spellbreaker_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $SB/links/sc-spellbreaker-stub.html 2>&1 | tail -1
echo -n "  stage 2 on stage 3: "; $PY spellbreaker_build.py --stage 2 --src $R/sc-spellbreaker-unmaking.html --out $R/sc-spellbreaker-x.html 2>&1 | tail -1
echo -n "  stage 1 on stage 1: "; $PY spellbreaker_build.py --stage 1 --src $R/sc-spellbreaker-stub.html --out $R/sc-spellbreaker-y.html 2>&1 | tail -1
echo -n "  stage 3 on the base: "; $PY spellbreaker_build.py --stage 3 --src ../02-chain/sc-tendril-t3.html --out $R/sc-spellbreaker-z.html 2>&1 | tail -1
echo -n "  stage 5 on stage 5: "; $PY spellbreaker_build.py --stage 5 --src $R/$FIN.html --out $R/sc-spellbreaker-v.html 2>&1 | tail -1
echo -n "  stage 5 on stage 2: "; $PY spellbreaker_build.py --stage 5 --src $R/sc-spellbreaker-stun.html --out $R/sc-spellbreaker-u.html 2>&1 | tail -1
echo -n "  --alt50 on stage 3: "; $PY spellbreaker_build.py --stage 3 --alt50 --src $R/sc-spellbreaker-stun.html --out $R/sc-spellbreaker-t.html 2>&1 | tail -1
echo -n "  --alt50 with --alt-row: "; $PY spellbreaker_build.py --stage 5 --alt50 --alt-row --src $R/sc-spellbreaker-unmaking.html --out $R/sc-spellbreaker-s.html 2>&1 | tail -1
echo -n "  a name outside sc-spellbreaker*: "; $PY spellbreaker_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $R/sc-other.html 2>&1 | tail -1
echo -n "  a base without Tendril (sc-trunk): "; $PY spellbreaker_build.py --stage 1 --src ../02-chain/sc-trunk.html --out $R/sc-spellbreaker-w.html 2>&1 | tail -1
echo "  html written by the refusals: $(ls $R/sc-spellbreaker-x.html $R/sc-spellbreaker-y.html $R/sc-spellbreaker-z.html $R/sc-spellbreaker-v.html $R/sc-spellbreaker-u.html $R/sc-spellbreaker-t.html $R/sc-spellbreaker-s.html $R/sc-spellbreaker-w.html $R/sc-other.html 2>/dev/null | wc -l)"
