#!/bin/bash
# The bolt's SPECS.spellbreaker out of both fx.js copies, tried in scratch (the orchestrator's at the carry):
# (1) on the fx link, with a copy of fx.js at the stamp its inlined copy carries (extracted from the page, its
#     sha256 checked against the stamp); (2) the carry, dry, on the newest real tip: stages 1, 2, 3, 5 and 6 on
#     02-chain/sc-aureole-fxout, then fx_remove with a COPY of today's src/render/fx.js. The real fx.js is untouched.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=<scratch>
D=$SB/s6/fxout; rm -rf $D; mkdir -p $D
cd C:/dev/sundered-crown/tools
FX=$SB/links/sc-spellbreaker-b7.5-fx.html
echo "src/render/fx.js on disk before: $(sha256sum ../src/render/fx.js | cut -c1-16)"
$PY - "$FX" "$D/fxjs_at_stamp.js" <<'PYEOF'
import hashlib, re, sys
s = open(sys.argv[1], encoding="utf-8").read()
h = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n", s)
t = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, h.end())
body = s[h.end():t.start()].rstrip("\n") + "\n"
assert hashlib.sha256(body.encode()).hexdigest() == h.group(1), "the extracted copy is not the stamp's"
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(body)
print(f"(1) fx.js at the fx link's stamp, extracted from the page: {h.group(1)[:16]} (sha256 of the copy == the stamp)")
PYEOF
$PY fx_remove.py --relic spellbreaker --src $FX --out $D/sc-spellbreaker-b7.5-fx-specout.html --fxjs $D/fxjs_at_stamp.js
echo "    the copy after: $(sha256sum $D/fxjs_at_stamp.js | cut -c1-16)"
echo "(2) the carry, dry, on 02-chain/sc-aureole-fxout ($(sha256sum ../02-chain/sc-aureole-fxout.html | cut -c1-16))"
T=../02-chain/sc-aureole-fxout.html; C=$D/carry; mkdir -p $C
$PY spellbreaker_build.py --stage 1 --src $T --out $C/sc-spellbreaker-stub.html > $C/log.txt 2>&1 && \
$PY spellbreaker_build.py --stage 2 --src $C/sc-spellbreaker-stub.html --out $C/sc-spellbreaker-stun.html >> $C/log.txt 2>&1 && \
$PY spellbreaker_build.py --stage 3 --src $C/sc-spellbreaker-stun.html --out $C/sc-spellbreaker-unmaking.html >> $C/log.txt 2>&1 && \
$PY spellbreaker_build.py --stage 5 --src $C/sc-spellbreaker-unmaking.html --out $C/sc-spellbreaker-b7.5.html >> $C/log.txt 2>&1 && \
$PY spellbreaker_build.py --stage 6 --src $C/sc-spellbreaker-b7.5.html --out $C/sc-spellbreaker-b7.5-fx.html >> $C/log.txt 2>&1 || echo "    a stage FAILED"
grep "  out " $C/log.txt | sed 's/^/   /'
cp ../src/render/fx.js $D/fxjs_today.js
$PY fx_remove.py --relic spellbreaker --src $C/sc-spellbreaker-b7.5-fx.html --out $C/sc-spellbreaker-fxout.html --fxjs $D/fxjs_today.js
echo "    the copy of today's fx.js after: $(sha256sum $D/fxjs_today.js | cut -c1-16)"
echo "src/render/fx.js on disk after: $(sha256sum ../src/render/fx.js | cut -c1-16) (untouched)"
