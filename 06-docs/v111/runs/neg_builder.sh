#!/bin/bash
# The builder's own scan, tested: copies of spellbreaker_build.py, each with ONE forbidden line added to an
# insert (tickUnmake's, the cast branch's or the second-hex insert's), must refuse and write nothing; the
# clean copy must write the stage-2 link unchanged. The list after v111's review adds the stun, status, hex
# clock, reach, stun-DR, charge, burden and apply() writes the review found unscanned, and the one allowed
# stun line copied into the wrong insert.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=<scratch>
D=$SB/negtest; rm -rf $D; mkdir -p $D
B=C:/dev/sundered-crown/tools/spellbreaker_build.py
echo "BUILDER NEGATIVE TESTS (spellbreaker_build.py $(sha256sum $B | cut -c1-16)); each copy runs stage 2 on the stage-1 link"
TICK='      f.unmakeTally.foeHex += foe.stacks("hex");'
CAST='      f.unmakeTally.casts++;'
INS='      self.unmakeTally.blows++;'
i=0
while IFS='|' read -r where bad; do
  [ -z "$bad" ] && continue
  case $where in tick) A="$TICK";; cast) A="$CAST";; ins) A="$INS";; esac
  i=$((i+1)); c=$D/bad_$i.py
  ANCH="$A" BAD="$bad" $PY - "$B" "$c" <<'PYEOF'
import os, sys
s = open(sys.argv[1], encoding="utf-8").read()
a = os.environ["ANCH"] + "\n"
assert s.count(a) == 1, (s.count(a), a)
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(s.replace(a, a + "      " + os.environ["BAD"] + "\n", 1))
PYEOF
  out=$($PY $c --stage 2 --src $SB/links/sc-spellbreaker-stub.html --out $D/sc-spellbreaker-neg$i.html 2>&1 | tail -1)
  echo "- $where + '$bad':"
  echo "    $out"
done <<'LIST'
tick|foe.vx *= 0.99;
tick|const q = this.rng();
tick|f.w.dmg = 9;
tick|f.w.spin += 1;
tick|this.hurt(foe, 1, f);
tick|this.hitStop = Math.max(this.hitStop, 0.01);
tick|STATUS.hex.stunFor = 0.4;
tick|const H = STATUS.hex; H.stunFor = 0.4;
tick|CONFIG.chaos.critMul *= 1.1;
tick|foe.theta += 0.1;
tick|foe.stun = Math.max(foe.stun, 0.1);
tick|foe.status.hex = { stacks: 5, t: 2.6 };
tick|foe.status["hex"].t = 9;
tick|const st = foe.status; st.hex = null;
tick|delete foe.status.hex;
tick|foe.hexClock += 0.5;
tick|foe.reachMul = Math.max(0.4, foe.reachMul - 0.0005);
tick|foe.stunDR = 0;
tick|f.charge += 1;
tick|foe.burden = 1;
tick|foe.apply("chill", 1);
tick|f.stun = Math.max(f.stun, STATUS.hex.stunFor * f.hexStunMul);
cast|foe.stun = 0.4;
cast|foe.hexClock = 1.1;
ins|foe.reachMul = Math.max(0.4, foe.reachMul - 0.12);
ins|foe.apply("hex", 1, "a");
ins|foe.stun = Math.max(foe.stun, 0.4);
LIST
cp $B $D/clean.py
echo "- the clean copy: $($PY $D/clean.py --stage 2 --src $SB/links/sc-spellbreaker-stub.html --out $D/sc-spellbreaker-clean.html 2>&1 | tail -1)"
echo "  clean copy's stage 2 $(sha256sum $D/sc-spellbreaker-clean.html | cut -c1-16) against the link $(sha256sum $SB/links/sc-spellbreaker-stun.html | cut -c1-16)"
echo "- copies: $i; html files written by the refusals: $(ls $D/sc-spellbreaker-neg*.html 2>/dev/null | wc -l)"
