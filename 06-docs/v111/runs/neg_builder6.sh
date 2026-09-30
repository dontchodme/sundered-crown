#!/bin/bash
# STAGE 6's SCAN, tested: copies of spellbreaker_build.py, each with ONE forbidden line written into one of
# stage 6's rows (after a line of that row's own code, at its indent), must refuse and write nothing. A
# harmless line (a local constant in a draw method) must write a page, a different one; the clean copy
# must write the fx link, byte for byte. Each copy runs stage 6 on the final stage-5 link (b7.5).
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
SB=<scratch>
D=$SB/negtest6; rm -rf $D; mkdir -p $D
B=C:/dev/sundered-crown/tools/spellbreaker_build.py
SRC=$SB/links/sc-spellbreaker-b7.5.html
echo "STAGE 6 BUILDER NEGATIVE TESTS (spellbreaker_build.py $(sha256sum $B | cut -c1-16)); each copy runs stage 6 on the b7.5 ($(sha256sum $SRC | cut -c1-16))"
TICK='      f.unmkHC = hc; f.unmkStun = st; f.unmkMul = f.hexStunMul;'
TICK2='      const U = f.w.ult;'
DRAW='    const c = this.ctx, n = m.inset || 0;'
FIELDS='    this.unmkStun = 0;'
STUNV='        if (f.hexStunMul > 1) SFX.play("ult", { w: "spellbreaker-stun" });'
CLOSEV='      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "spellbreaker-close" });'
SFXA='          const g = 0.5194;'
GREY='      const c0 = this.ctx;'
SCRIPT='      if (f.unmkFade > 0) this._unmkScript(c, m, f, reach + 6, off);'
PCALL="    this.tickUnmaking(dt);              // UNMAKING'S PICTURE (v79 section 4)"
FLOOR='    if (__world) this.drawUnmaking(m);'
i=0
mk(){  # mk <anchor> <bad> <copy>
  ANCH="$1" BAD="$2" $PY - "$B" "$3" <<'PYEOF'
import os, sys
s = open(sys.argv[1], encoding="utf-8").read()
a, bad = os.environ["ANCH"], os.environ["BAD"]
ind = a[:len(a) - len(a.lstrip())]
if s.count(a + "\n") == 1:
    s = s.replace(a + "\n", a + "\n" + ind + bad + "\n", 1)
else:
    assert s.count(a + "'''") == 1, a
    s = s.replace(a + "'''", a + "\n" + ind + bad + "'''", 1)
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(s)
PYEOF
}
while IFS='|' read -r where bad; do
  [ -z "$bad" ] && continue
  case $where in tick) A="$TICK";; tick2) A="$TICK2";; draw) A="$DRAW";; fields) A="$FIELDS";; stunv) A="$STUNV";;
                 closev) A="$CLOSEV";; sfx) A="$SFXA";; grey) A="$GREY";; script) A="$SCRIPT";; pcall) A="$PCALL";;
                 floor) A="$FLOOR";; esac
  i=$((i+1)); c=$D/bad_$i.py
  mk "$A" "$bad" "$c"
  out=$($PY $c --stage 6 --src $SRC --out $D/sc-spellbreaker-neg$i.html 2>&1 | grep -m1 -E 'REFUSING|refusing|ANCHOR|wrong base|out sc-')
  echo "- $where + '$bad':"
  echo "    $out"
done <<'LIST'
tick|f.vx *= 0.999;
tick|const q = this.rng();
tick|f.stun = Math.max(f.stun, 0.01);
tick|f.hexClock = 0;
tick|this.ultFx = null;
tick|f.w.reach += 1;
tick|STATUS.hex.stunFor = 0.4;
tick|const H = STATUS.hex;
tick|this.tags.push({ key: "hex", life: 0.9, max: 0.9 });
tick|this.hitStop = 0.02;
tick|f.unmakeTally.extra += 1;
tick|f.ultUnmake = null;
tick|this.beat({ kind: "ult" });
tick|SFX.play("ult", { w: "spellbreaker-close" });
tick|f.apply("hex", 1, "a");
tick|delete f.status.hex;
tick|const r0 = Math.random();
tick|this.shots.splice(0, 1);
tick|this.shots[0] = null;
tick|f.hexStunMul = 1;
tick2|f.status.hex.t = 2.6;
draw|m.t += 0.001;
draw|m.a.x += 1e-9;
draw|Object.assign(m.a, { hp: 0 });
draw|const c = m.a;
fields|this.charge = 0;
fields|SFX.play("ult", { w: "spellbreaker" });
stunv|SFX.play("ult", { w: "spellbreaker-stun" });
closev|SFX.play("ult", { w: "spellbreaker-close" });
sfx|CONFIG.audio = null;
sfx|SFX.play("ult", { w: "spellbreaker" });
grey|this._tone(0, { freq: 440, gain: 0.1, dur: 0.1 });
script|f.theta += 0.01;
pcall|this.tickUnmake(dt);
floor|if (__world) this.statusTag(m.a.x, m.a.y, "hex", false, 2);
LIST
mk "$DRAW" 'const zz = n + 1;' $D/harmless.py
echo "- a harmless line in drawUnmaking ('const zz = n + 1;'): $($PY $D/harmless.py --stage 6 --src $SRC --out $D/sc-spellbreaker-harmless.html 2>&1 | tail -1)"
echo "  its page $(sha256sum $D/sc-spellbreaker-harmless.html | cut -c1-16) (the fx link $(sha256sum $SB/links/sc-spellbreaker-b7.5-fx.html | cut -c1-16): a different page, written)"
cp $B $D/clean.py
echo "- the clean copy: $($PY $D/clean.py --stage 6 --src $SRC --out $D/sc-spellbreaker-clean.html 2>&1 | tail -1)"
echo "  clean copy's stage 6 $(sha256sum $D/sc-spellbreaker-clean.html | cut -c1-16) against the fx link $(sha256sum $SB/links/sc-spellbreaker-b7.5-fx.html | cut -c1-16)"
echo "- copies: $i; html files written by the refusals: $(ls $D/sc-spellbreaker-neg*.html 2>/dev/null | wc -l)"
