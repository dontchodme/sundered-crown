# Writes rune_census.py: a copy of tools/ult_overlay.py that counts, BEFORE each lab step,
# whether that step is frozen (m.hitStop > 0 || m.latch || m.splitHold), over the whole
# arm and inside windows. Nothing else changes: the counting only reads.
import pathlib, sys
src = pathlib.Path("C:/dev/sundered-crown/tools/ult_overlay.py").read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new, 1)
s = src
s = one(s, "sys.path.insert(0, str(pathlib.Path(__file__).parent))",
        "sys.path.insert(0, 'C:/dev/sundered-crown/tools')")
s = one(s, "    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, casts = 0, hitsIn = 0, hitsOut = 0;\n    while (!m.over && step < secs / DT){\n      const h0 = me.hits;\n",
        "    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, casts = 0, hitsIn = 0, hitsOut = 0;\n    let cSteps = 0, cFrozen = 0, cWin = 0, cWinFrozen = 0;\n    while (!m.over && step < secs / DT){\n      const h0 = me.hits;\n      { const fz = m.hitStop > 0 || !!m.latch || !!m.splitHold, ow = castEnd >= 0 && t < castEnd;\n        cSteps++; if (fz) cFrozen++; if (ow){ cWin++; if (fz) cWinFrozen++; } }\n")
s = one(s, "                dur: step * DT, casts, hitsIn, hitsOut, S });",
        "                dur: step * DT, casts, hitsIn, hitsOut, S, cen: [cSteps, cFrozen, cWin, cWinFrozen] });")
s = one(s, "                            byFoe={k: sum(v) / len(v) for k, v in byFoe.items()})",
        "                            byFoe={k: sum(v) / len(v) for k, v in byFoe.items()})\n"
        "    _c = [sum(r['cen'][i] for r in rs) for i in range(4)]\n"
        "    out['arms'][arm]['census'] = dict(steps=_c[0], frozen=_c[1], win=_c[2], winFrozen=_c[3])\n"
        "    _fs = _c[1] / max(1, _c[0]); _fw = _c[3] / max(1, _c[2]); _fo = (_c[1] - _c[3]) / max(1, _c[0] - _c[2])\n"
        "    print(f\"      census {arm}: frozen {_fs:.4f} of lab steps ({_c[1]} of {_c[0]}), {_fw:.4f} inside windows, {_fo:.4f} outside; \"\n"
        "          f\"lab {P['charge']:g} -> engine {P['charge']*(1-_fs):.2f}; window {P['dur']:g} lab-s = {P['dur']*(1-_fw):.2f} engine window-s\")")
out = pathlib.Path(sys.argv[1]); out.write_text(s, encoding="utf-8", newline="\n"); print("wrote", out)
