# Summarise the probe on the b205 link and its mutants: win in the probe's 456 fights, and which checks fail.
# Review round 3: the round-2 eight re-made from the rebuilt link, plus the review's three (rv-drain, rv-spin, rv-dir)
# and two more whole-state ones (mut-clank on the Match, mut-charge on the caster).
import json, pathlib, re, sys
R = pathlib.Path(__file__).parent
WANT = {"mut-dur": "1", "mut-pad": "2", "mut-cd": "3", "mut-hex2": "4", "mut-impulse": "5", "rv-dir": "5", "mut-bite": "6",
        "rv-drain": "6", "rv-spin": "6", "mut-clank": "6", "mut-self": "7", "mut-charge": "7", "mut-death": None}
WHAT = {"mut-dur": "Z.t += dt * 0.9           (the window 11% long)",
        "mut-pad": "e = u.pad + 4.5           (a 6-unit band)",
        "mut-cd": "Z.cd = u.cd * 0.8         (a touch every 0.4s)",
        "mut-hex2": 'apply("hex", u.hex + 1)   (two stacks a touch)',
        "mut-impulse": "foe.vx += ..., vy += ...  (an impulse, not the throw)",
        "rv-dir": "dx = foe.x - f.x, ...     (the hurl AWAY from the hammer; the review's)",
        "mut-bite": "this.hurt(foe, 4, f)      (the design's rejected bite)",
        "rv-drain": "foe.charge -= 1 a touch   (drains the foe's ultimate; the review's)",
        "rv-spin": "foe.spinDir = -spinDir    (flips the foe's spin; the review's)",
        "mut-clank": "this.clankCd >= 0.3       (a touch mutes clanks: the Match)",
        "mut-self": "the caster pushed off its own left wall",
        "mut-charge": "f.charge += 0.25 a touch  (the caster's ultimate fed)",
        "mut-death": "drops `|| !foe.alive` from the close (EQUIVALENT: the branch is unreachable)"}
base = json.loads((R / "probe_b205.json").read_text())
L = [f"The probe on sc-lodestone-b205 and its mutants (ctl/mut205r3, runs/make_ctl.py), 456 fights each.",
     f"  link         win {base['win']:.1%}   " + open(R / "probe_b205.txt").read().strip().splitlines()[-1].strip()]
allok = True
for m, want in WANT.items():
    t = (R / f"probe_b205_{m}.txt").read_text()
    J = json.loads((R / f"probe_b205_{m}.json").read_text())
    fails = re.findall(r"\[(\d)\] FAIL", t)
    nx = {k: J["n"].get("x" + k, 0) for k in fails}
    if want is None:
        same = J["win"] == base["win"] and J["n"] == base["n"] and J["T"] == base["T"]
        ok = not fails and same
        L.append(f"  {m:<12} {WHAT[m]:<72} win {J['win']:.1%}   fails {fails or 'none'}   every count identical to the link: {same}   -> {'EQUIVALENT, as expected' if ok else 'NOT EQUIVALENT'}")
    else:
        ok = fails == [want]
        first = (J["bad"].get(want) or [""])[0][:90]
        L.append(f"  {m:<12} {WHAT[m]:<72} win {J['win']:.1%}   fails {['[%s] x%d' % (k, nx[k]) for k in fails]}   -> {'fails ONLY its own check [' + want + ']' if ok else 'WRONG'}   first: {first}")
    allok &= ok
L.append("ALL AS EXPECTED" if allok else "SOMETHING IS WRONG")
(R / "probe_mutants_b205.txt").write_text("\n".join(L) + "\n"); print("\n".join(L))
