#!/bin/bash
# stage 6: every link rebuilt from the bare base with the stage-6 builder (tmp/rb6), the stage-6 refusals,
# and the carry, dry, stages 1-6 on later tips. -> runs/stage6_rebuild.txt, runs/stage6_carry_dry.txt
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
H=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
cd C:/dev/sundered-crown/tools
B=26.5; RB=$S/tmp/rb6; rm -rf $RB; mkdir -p $RB
{
echo "REBUILD FROM THE BARE BASE with tools/thornwake_build.py $(sha256sum thornwake_build.py | cut -c1-16)"
echo "base ../02-chain/sc-tendril-t3.html $(sha256sum ../02-chain/sc-tendril-t3.html | cut -c1-16)"
prev=../02-chain/sc-tendril-t3.html
for st in "1 stub" "2 bramble" "3 snare" "5 b$B" "6 b$B-fx"; do set -- $st; n=sc-thornwake-$2.html
  $PY thornwake_build.py --stage $1 --src $prev --out $RB/$n > $RB/$n.log 2>&1; rc=$?
  a=$(sha256sum $RB/$n 2>/dev/null | cut -c1-16); b=$(sha256sum $S/links/$n | cut -c1-16)
  echo "stage $1  $n  rebuilt $a  on disk $b  rc $rc  -> $([ "$a" = "$b" ] && echo IDENTICAL || echo DIFFERENT)"; prev=$RB/$n
done
echo; echo "REFUSALS (each must refuse, and write nothing):"
r() { lab="$1"; shift; out="${@: -1}"; txt=$($PY thornwake_build.py "$@" 2>&1); rc=$?; w=$([ -e "$out" ] && echo "WROTE $(basename $out)" || echo "wrote nothing");
      echo "  $lab: rc $rc, $w -- $(echo "$txt" | tail -1)"; }
r "stage 6 on stage 6 (twice)" --stage 6 --src $RB/sc-thornwake-b$B-fx.html --out $RB/sc-thornwake-x6a.html
r "stage 6 on stage 3 (the shipped blade)" --stage 6 --src $RB/sc-thornwake-snare.html --out $RB/sc-thornwake-x6b.html
r "stage 6 on stage 2" --stage 6 --src $RB/sc-thornwake-bramble.html --out $RB/sc-thornwake-x6c.html
r "stage 6 on the bare base" --stage 6 --src ../02-chain/sc-tendril-t3.html --out $RB/sc-thornwake-x6d.html
r "stage 5 on stage 6" --stage 5 --src $RB/sc-thornwake-b$B-fx.html --out $RB/sc-thornwake-x5.html
r "stage 3 on stage 6" --stage 3 --src $RB/sc-thornwake-b$B-fx.html --out $RB/sc-thornwake-x3.html
r "stage 1 on stage 6" --stage 1 --src $RB/sc-thornwake-b$B-fx.html --out $RB/sc-thornwake-x1.html
h0=$(sha256sum $S/links/sc-thornwake-b$B-fx.html | cut -c1-16)
txt=$($PY thornwake_build.py --stage 6 --src $RB/sc-thornwake-b$B.html --out $S/links/sc-thornwake-b$B-fx.html 2>&1); rc=$?
echo "  overwrite the fx link: rc $rc, the link $h0 -> $(sha256sum $S/links/sc-thornwake-b$B-fx.html | cut -c1-16) -- $(echo "$txt" | tail -1)"
r "a name not sc-thornwake*" --stage 6 --src $RB/sc-thornwake-b$B.html --out $RB/sc-other-fx.html
sed 's/\r$//' $RB/sc-thornwake-b$B.html > /dev/null; $PY -c "import sys;p=sys.argv[1];open(sys.argv[2],'wb').write(open(p,'rb').read().replace(b'\n',b'\r\n'))" $RB/sc-thornwake-b$B.html $RB/crlf-b$B.html
r "a CRLF source" --stage 6 --src $RB/crlf-b$B.html --out $RB/sc-thornwake-x6e.html
$PY - "$RB" <<'PY'
import sys, pathlib
RB = pathlib.Path(sys.argv[1]); s = (RB / "sc-thornwake-b26.5.html").read_text(encoding="utf-8")
# a base where one of stage 6's names is already taken, and one without the freeze's voice to replace
(RB / "taken-b26.5.html").write_text(s.replace("  tickWinnow(dt){\n", "  tickBrier(dt){}\n  tickWinnow(dt){\n", 1), encoding="utf-8", newline="\n")
old = '        } else if (w === "thornwake"){                  // creak and cinch\n'
assert s.count(old) == 1
(RB / "noarm-b26.5.html").write_text(s.replace(old, '        } else if (w === "thornwake"){\n', 1), encoding="utf-8", newline="\n")
PY
r "a base with tickBrier already in it" --stage 6 --src $RB/taken-b$B.html --out $RB/sc-thornwake-x6f.html
r "a base without the freeze's voice" --stage 6 --src $RB/noarm-b$B.html --out $RB/sc-thornwake-x6g.html
echo; echo "links written by the refusals: $(ls $RB/sc-thornwake-x* $RB/sc-other* 2>/dev/null | wc -l)"
} > $S/runs/stage6_rebuild.txt 2>&1
{
echo "THE CARRY, DRY: stages 1, 2, 3, 5, 6 on later tips (scratch files, not links)"
for tip in ../02-chain/sc-spellbreaker-fxout.html ../02-chain/sc-aureole-fxout.html ../02-chain/sc-ironhail-fxout.html ../02-chain/sc-coldiron-temper-fx.html ../02-chain/sc-tendril-fx.html $H/links/sc-heartwood-b11.html; do
  D=$S/tmp/carry6/$(basename $tip .html); rm -rf $D; mkdir -p $D; prev=$tip; line="$(basename $tip) $(sha256sum $tip | cut -c1-16) ->"
  for st in "1 stub" "2 bramble" "3 snare" "5 b$B" "6 b$B-fx"; do set -- $st; n=sc-thornwake-$2.html
    out=$($PY thornwake_build.py --stage $1 --src $prev --out $D/$n 2>&1); rc=$?
    line="$line s$1 $( [ $rc = 0 ] && sha256sum $D/$n | cut -c1-16 || echo "REFUSED:$(echo "$out" | tail -1)")"; prev=$D/$n
  done
  echo "$line   ($(echo "$out" | grep -o '[0-9]* relics in the roster'))"
  $PY - "$D/sc-thornwake-b$B.html" "$D/sc-thornwake-b$B-fx.html" "$S/links/sc-thornwake-b$B.html" "$S/links/sc-thornwake-b$B-fx.html" <<'PY'
import sys, difflib
a, b, c, d = [open(p, encoding="utf-8").read().splitlines(keepends=True) for p in sys.argv[1:5]]
def added(x, y):
    out = []
    for op in difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes():
        if op[0] != "equal": out.append(("".join(x[op[1]:op[2]]), "".join(y[op[3]:op[4]])))
    return out
t, o = added(a, b), added(c, d)
TOK = ("thornwake:1, ", "thornwake: 2.4, ")
def same(p, q):
    if p == q: return "same"
    for k in TOK:   # a shared map line another relic's stage 6 already edited: the same token out of it
        if p[0].count(k) == 1 and p[0].replace(k, "", 1) == p[1] and q[0].replace(k, "", 1) == q[1]: return "token"
    return "DIFF"
r = [same(p, q) for p, q in zip(t, o)] if len(t) == len(o) else ["DIFF"]
ok = "DIFF" not in r
print(f"      stage 6's change on this tip == its change on the base: {'YES' if ok else 'NO'} ({len(t)} hunks: "
      f"{r.count('same')} byte-identical, {r.count('token')} the same token out of a shared map line)")
PY
done
echo; echo "AND THE OTHER FREEZE REDESIGN ON THIS BUILD'S FX LINK: heartwood_build.py stages 1,2,3,5 on sc-thornwake-b$B-fx"
D=$S/tmp/carry6/heartwood-on-fx; rm -rf $D; mkdir -p $D; prev=$S/links/sc-thornwake-b$B-fx.html; line="sc-thornwake-b$B-fx ->"
for st in "1 stub" "2 root" "3 rootfast" "5 b11"; do set -- $st; n=sc-heartwood-$2.html
  out=$($PY heartwood_build.py --stage $1 --src $prev --out $D/$n 2>&1); rc=$?
  line="$line s$1 $( [ $rc = 0 ] && sha256sum $D/$n | cut -c1-16 || echo "REFUSED:$(echo "$out" | tail -1)")"; prev=$D/$n
done
echo "$line"
} > $S/runs/stage6_carry_dry.txt 2>&1
cat $S/runs/stage6_rebuild.txt $S/runs/stage6_carry_dry.txt
