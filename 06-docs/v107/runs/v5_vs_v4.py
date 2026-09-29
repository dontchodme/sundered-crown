"""THIRD REVIEW ROUND: the v5 probe against the v4 probe on the same links. The header and the three mechanism lines
after it must be character for character the same; only the whole-state line and the check texts may differ.
Prints the whole-state line of each v5 run.
    python v5_vs_v4.py"""
import pathlib
R = pathlib.Path(__file__).parent
PAIRS = [("probe_wall_v4.txt", "probe_wall_v5.txt"), ("probe_bulwark_v4.txt", "probe_bulwark_v5.txt"),
         ("probe_b9.5_v4.txt", "probe_b9.5_v5.txt"), ("probe_onfx_b9.5.txt", "probe_onfx_b9.5_v5.txt")]
allok = True
for a, b in PAIRS:
    A = (R / a).read_text(encoding="utf-8").splitlines() if (R / a).exists() else []
    B = (R / b).read_text(encoding="utf-8").splitlines() if (R / b).exists() else []
    ha = [l for l in A if l.startswith("BULWARK PROBE")]; hb = [l for l in B if l.startswith("BULWARK PROBE")]
    if not ha or not hb:
        print(f"{b}: MISSING"); allok = False; continue
    ia, ib = A.index(ha[0]), B.index(hb[0])
    mech_a, mech_b = A[ia:ia + 4], B[ib:ib + 4]   # the header and the three mechanism lines
    same = mech_a == mech_b
    score = [l.strip() for l in B if l.strip().endswith("/8")]
    state = [l.strip() for l in B if l.strip().startswith("whole-state")]
    allok &= same and score == ["8/8"]
    print(f"{b}: {score[0] if score else '?'}   mechanism lines {'IDENTICAL to' if same else 'DIFFER from'} {a}")
    print(f"    {state[0] if state else '-'}")
print("\nEVERY v5 RUN 8/8 WITH THE v4 MECHANISM LINES" if allok else "\nNOT ALL (see above)")
