#!/bin/bash
# Stage 6 added: every link rebuilt from the builder as it now stands (stages 1, 2, 3, 5 x3 and 6), chained
# from the bare tip sc-tendril-t3 to a temporary folder; each must match its link's sha. Then stage 6's
# refusals (and stage 5's and the alt flags' against stage 6), none of which may write a file.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=<scratch>
cd C:/dev/sundered-crown/tools
R=$SB/rebuild6; rm -rf $R; mkdir -p $R
echo "builder spellbreaker_build.py $(sha256sum spellbreaker_build.py | cut -c1-16); base sc-tendril-t3 $(sha256sum ../02-chain/sc-tendril-t3.html | cut -c1-16)"
$PY spellbreaker_build.py --stage 1 --src ../02-chain/sc-tendril-t3.html --out $R/sc-spellbreaker-stub.html > /dev/null || echo "stage 1 FAILED"
$PY spellbreaker_build.py --stage 2 --src $R/sc-spellbreaker-stub.html --out $R/sc-spellbreaker-stun.html > /dev/null || echo "stage 2 FAILED"
$PY spellbreaker_build.py --stage 3 --src $R/sc-spellbreaker-stun.html --out $R/sc-spellbreaker-unmaking.html > /dev/null || echo "stage 3 FAILED"
$PY spellbreaker_build.py --stage 5 --src $R/sc-spellbreaker-unmaking.html --out $R/sc-spellbreaker-b7.5.html > /dev/null || echo "stage 5 FAILED"
$PY spellbreaker_build.py --stage 5 --alt50 --src $R/sc-spellbreaker-unmaking.html --out $R/sc-spellbreaker-b7.7.html > /dev/null || echo "stage 5 --alt50 FAILED"
$PY spellbreaker_build.py --stage 5 --alt-row --src $R/sc-spellbreaker-unmaking.html --out $R/sc-spellbreaker-b8.3.html > /dev/null || echo "stage 5 --alt-row FAILED"
$PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-b7.5.html --out $R/sc-spellbreaker-b7.5-fx.html > /dev/null || echo "stage 6 FAILED"
all=1
for n in sc-spellbreaker-stub sc-spellbreaker-stun sc-spellbreaker-unmaking sc-spellbreaker-b7.5 sc-spellbreaker-b7.7 sc-spellbreaker-b8.3 sc-spellbreaker-b7.5-fx; do
  a=$(sha256sum $SB/links/$n.html | cut -c1-16); b=$(sha256sum $R/$n.html | cut -c1-16)
  cr=$(tr -cd '\r' < $R/$n.html | wc -c)
  [ "$a" = "$b" ] && echo "  $n  link $a  rebuilt $b  SAME  (CR bytes: $cr)" || { echo "  $n  link $a  rebuilt $b  DIFFERENT"; all=0; }
done
[ $all = 1 ] && echo "EVERY LINK REBUILDS BYTE FOR BYTE (the seven, stage 6's included)" || echo "A LINK DOES NOT REBUILD"
echo "stage 6's refusals:"
echo -n "  stage 6 twice (on the fx link): "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-b7.5-fx.html --out $R/sc-spellbreaker-r1.html 2>&1 | tail -1
echo -n "  stage 6 on Rick's row-floor link (b8.3): "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-b8.3.html --out $R/sc-spellbreaker-r2.html 2>&1 | tail -1
echo -n "  stage 6 on Rick's 50% link (b7.7): "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-b7.7.html --out $R/sc-spellbreaker-r3.html 2>&1 | tail -1
echo -n "  stage 6 on stage 3: "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-unmaking.html --out $R/sc-spellbreaker-r4.html 2>&1 | tail -1
echo -n "  stage 6 on stage 2: "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-stun.html --out $R/sc-spellbreaker-r5.html 2>&1 | tail -1
echo -n "  stage 6 on stage 1: "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-stub.html --out $R/sc-spellbreaker-r6.html 2>&1 | tail -1
echo -n "  stage 6 on the bare tip: "; $PY spellbreaker_build.py --stage 6 --src ../02-chain/sc-tendril-t3.html --out $R/sc-spellbreaker-r7.html 2>&1 | tail -1
echo -n "  stage 6 over an existing link: "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-b7.5.html --out $SB/links/sc-spellbreaker-b7.5-fx.html 2>&1 | tail -1
echo -n "  stage 6 to a name outside sc-spellbreaker*: "; $PY spellbreaker_build.py --stage 6 --src $R/sc-spellbreaker-b7.5.html --out $R/sc-other-fx.html 2>&1 | tail -1
echo -n "  stage 5 on the fx link: "; $PY spellbreaker_build.py --stage 5 --src $R/sc-spellbreaker-b7.5-fx.html --out $R/sc-spellbreaker-r8.html 2>&1 | tail -1
echo -n "  --alt50 with stage 6: "; $PY spellbreaker_build.py --stage 6 --alt50 --src $R/sc-spellbreaker-b7.5.html --out $R/sc-spellbreaker-r9.html 2>&1 | tail -1
echo -n "  --alt-row with stage 6: "; $PY spellbreaker_build.py --stage 6 --alt-row --src $R/sc-spellbreaker-b7.5.html --out $R/sc-spellbreaker-r10.html 2>&1 | tail -1
echo -n "  stage 3 on the fx link: "; $PY spellbreaker_build.py --stage 3 --src $R/sc-spellbreaker-b7.5-fx.html --out $R/sc-spellbreaker-r11.html 2>&1 | tail -1
echo "  html written by the refusals: $(ls $R/sc-spellbreaker-r*.html $R/sc-other-fx.html 2>/dev/null | wc -l); the fx link untouched: $(sha256sum $SB/links/sc-spellbreaker-b7.5-fx.html | cut -c1-16)"
