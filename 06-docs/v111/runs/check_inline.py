"""The two labs' reports, as the orchestrator relayed them in this task, against the row files: the
relayed text is {"rows": [...]} serialised compactly; each report's opening, a fragment from its middle and
its last characters before the relay cut it must stand in the file's own JSON at the same place (the
opening as a prefix). A one-character change to any of them must fail (the control)."""
import json, pathlib, sys
S = pathlib.Path(r"<scratch>")
def rel(f):
    rows = json.loads((S / f).read_text(encoding="utf-8"))
    return json.dumps({"rows": rows}, ensure_ascii=False, separators=(",", ":"))
V = rel("stage6-voice/rows_final.json"); P = rel("stage6-picture/rows_final.json")
# transcribed from the relayed task text (opening, a middle fragment, the last characters before the cut)
VO = r'''{"rows":[{"label":"Sfx: Spellbreaker's cast, stun and close arms, before the shared rune-crack fallback","anchor":"        } else {                                        // rune-crack","mode":"before","code":"        } else if (w === \"spellbreaker\"){               // the weapon unmade\n          /* SPELLBREAKER'S CAST, THE UNMAKING -- v79 s4: \"cast -- a glass\n             crack into a hum, 0.4s\". DRONE, of 5, picked on the numbers by\n'''
VM = r'''          this.play(\"hex-snap\", {});\n          this._tone (t, { freq: 2500, gain: 0.07249 * 0.2244, dur: 0.401 * 2.5, type:\"triangle\" });\n'''
VE = r'''so the 11 other relics that still fall through keep it and another relic's row anchored there applies in either order. Through the patched play('''
PO = r'''{"rows":[{"label":"unmaking picture: fighter fields","anchor":"    this.ultUnmake = null;\n    this.unmakeTally = null;\n    this.hexStunMul = 1;\n","mode":"after","code":"    /* UNMAKING'S PICTURE (v79 section 4), and none of it is the window: the\n       script unwrites for 0.2s after `ultUnmake` is gone, the motes outlive\n'''
PM = r'''{"label":"unmaking picture: the presentation call","anchor":"  tickPresentation(dt){\n    this.tickNovaFx(dt);\n","mode":"after","code":"    this.tickUnmaking(dt);              // UNMAKING'S PICTURE (v79 section 4)\n","why":"tickPresentation runs through hit stops and after the match; one call to tickUnmaking."}'''
PE = r'''if (g.key !== \"hex\" || g.first || g.life !== g.max || g.unmk) continue;\n          if (g.x === f.x && g.y === f.y) contin'''
def check(name, full, o, m, e):
    ok = full.startswith(o) and m in full and e in full and full.find(m) < full.find(e)
    cut = full.find(e) + len(e) if e in full else -1
    print(f"  {name}: opening ({len(o)} chars) is the file JSON's prefix: {full.startswith(o)}; the middle fragment "
          f"({len(m)}) in it: {m in full}; the last characters before the relay's cut ({len(e)}) in it, after the "
          f"middle: {e in full and full.find(m) < full.find(e)} (the relay ran {cut} of the file JSON's {len(full)} characters)")
    return ok
print("THE RELAYED REPORTS AGAINST THE ROW FILES")
a = check("voice   (rows_final.json 090b35214e0efe05)", V, VO, VM, VE)
b = check("picture (rows_final.json 6a3c73a527df3e45)", P, PO, PM, PE)
print("CONTROL: one character changed in each fragment in turn")
bad = 0
for name, full, frs in (("voice", V, (VO, VM, VE)), ("picture", P, (PO, PM, PE))):
    for i, fr in enumerate(frs):
        k = len(fr) // 2
        mut = fr[:k] + ("X" if fr[k] != "X" else "Y") + fr[k + 1:]
        hit = full.startswith(mut) if i == 0 else (mut in full)
        print(f"  {name} fragment {i}: the changed copy found: {hit}")
        bad += hit
print("PASS" if a and b and not bad else "FAIL")
sys.exit(0 if a and b and not bad else 1)
