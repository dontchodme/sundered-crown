"""Scratch: move the wire run before the root pick; FRAME_BLOWS from the observed blows."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_voice_lab.py")
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


a0 = s.index("        # ---- THE rootBlow ROW ----")
a1 = s.index("        # ---- THE PICKS IN A REAL WINDOW ----")
block = s[a0:a1]
s = s[:a0] + s[a1:]
r0 = s.index("        # ---- THE ROOT ----")
block += '''        # the blows a root lands with, as the wire run heard them
        nc = sorted(float(k) for k, v in WR["dmg"].items() if not k.startswith("crit") for _ in range(v))
        cr = sorted(float(k.split()[1]) for k, v in WR["dmg"].items() if k.startswith("crit") for _ in range(v))
        blows = [(nc[0], False), (nc[len(nc) // 2], False), (nc[-1], False),
                 ((cr[-1] if cr else round(BLADE * 2.1)), True)]
        FRAME_BLOWS[:] = list(dict.fromkeys(blows))
        print(f"  the blows the root voices landed with: {len(nc)} plain ({nc[0]:g}-{nc[-1]:g}, median "
              f"{nc[len(nc) // 2]:g}) and {len(cr)} crits" + (f" ({cr[0]:g}-{cr[-1]:g})" if cr else "") +
              " -> the frame checks run at " + ", ".join(f"{d_:g}{'!' if c_ else ''}" for d_, c_ in FRAME_BLOWS))
        rec["frame_blows"] = FRAME_BLOWS

'''
s = s[:r0] + block + s[r0:]

rep('''# the blows a root lands with: the blade 11 at the chaos jitter's +/-15% (rounded,
# as resolveHit rounds) and the crit (x 2.1); the wire run prints the real ones
FRAME_BLOWS = [(9, False), (11, False), (13, False), (23, True)]''',
    '''# the blows a root lands with: set from the wire run (the lightest, the median and
# the heaviest plain blow a root voice landed with, and the heaviest crit)
FRAME_BLOWS: list = []''')
rep('''        hband = HB[(11, False)]
''', '')
rep('''f"blow's frame (the worst of the blows 9, 11, 13 and 23!) the root keeps''',
    '''f"blow's frame (the worst of the blows the wire run heard) the root keeps''')
rep('''    ("hit@23!", ("hit", {"dmg": 23, "crit": True})),''' if False else '''                                ("hit@23!", ("hit", {"dmg": 23, "crit": True})),''',
    '''                                ("hit@23!", ("hit", {"dmg": 23, "crit": True})),''')
# attribute the blow: the first hit voice after a root voice is that blow's own
rep('''    const mine = [], other = []; let step = 0, inRB = 0, inTR = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-"))
        mine.push({ step, k: w, inRB: inRB > 0, inTR: inTR > 0, win: !!f.ultRoot, opts: JSON.stringify(p) });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };''',
    '''    const mine = [], other = [], dmgs = []; let step = 0, inRB = 0, inTR = 0, pend = false;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")){
        mine.push({ step, k: w, inRB: inRB > 0, inTR: inTR > 0, win: !!f.ultRoot, opts: JSON.stringify(p) });
        if (w === ME + "-root") pend = true;
      } else {
        other.push([step, kind, JSON.stringify(p || {})]);
        if (kind === "hit" && pend){ dmgs.push({ dmg: p.dmg, crit: !!p.crit, step }); pend = false; }
      }
      return op.call(this, kind, p); };''')
rep('''    const bad = []; let calls = 0, rooted = 0, fresh = 0, rootV = 0, kills = 0, killV = 0;
    const rootSteps = [];''', '''    const bad = []; let calls = 0, rooted = 0, fresh = 0, rootV = 0, kills = 0, killV = 0;''')
rep('''        if (v) rootSteps.push(step);
''', '')
rep('''    const T = f.rootTally || {};
    const dmgs = [];
    for (const s of rootSteps) for (const o of other) if (o[0] === s && o[1] === "hit") dmgs.push(JSON.parse(o[2]));
''', '''    const T = f.rootTally || {};
    if (dmgs.length !== rootV || dmgs.some((d, i) => d.step !== mine.filter(c => c.k === ME + "-root")[i].step))
      bad.push(["a root voice not followed on its step by its blow's hit voice", dmgs.length, rootV]);
''')
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
