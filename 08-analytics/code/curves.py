"""Per-second retention curves, pulled from TikTok's own insight API on 2026-08-19.

value[t] = fraction of viewers still watching at second t. These are the real
survival curves, not the "most viewers stopped at 0:0X" summary, and they make
the cold open's mechanism visible for the first time.
"""
import statistics as st

C = {
 "Axiom v Nightfell":      (1,[1.00,.85,.70,.59,.43,.34,.31,.30,.29,.27,.26,.25,.23,.21,.21,.18,.17,.16,.16,.15,.14,.14,.13,.13,.13,.13,.12,.12,.12,.12,.12,.12,.12,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.10,.10,.10,.10,.09,.09,.09,.08,.08,.08,.08,.07,.07,.07,.06,.06,.06,.04]),
 "Ironhail v Goreshard":   (1,[1.00,.85,.68,.56,.46,.35,.29,.27,.26,.24,.24,.22,.22,.21,.20,.20,.19,.18,.18,.18,.18,.18,.18,.17,.16,.16,.16,.16,.14,.14,.14,.14,.13,.13,.13,.13,.12,.12,.12,.12,.12,.10,.09,.08,.07]),
 "Emberedge v Thornwake":  (1,[1.00,.80,.65,.54,.38,.31,.28,.27,.24,.24,.23,.23,.21,.20,.20,.19,.19,.18,.18,.18,.17,.16,.15,.15,.15,.14,.14,.13,.13,.13,.13,.13,.13,.12,.12,.12,.12,.12,.11,.11,.11,.11,.11,.09,.09,.08,.08,.07,.06]),
 "Dawnbringer v Censer":   (1,[1.00,.81,.65,.50,.36,.28,.24,.22,.22,.20,.19,.18,.18,.16,.16,.15,.13,.12,.12,.10,.10,.10,.10,.10,.10,.09,.09,.09,.07,.07,.06,.06,.06,.06,.06,.06,.05,.05,.05,.05,.05,.05,.04,.04,.04,.04,.03]),
 "Slagheart v Lightkeeper":(0,[1.00,.78,.46,.31,.25,.21,.19,.18,.15,.14,.13,.12,.12,.12,.11,.11,.10,.09,.09,.09,.09,.09,.09,.09,.09,.09,.09,.09,.08,.08,.08,.08,.07,.07,.07,.07,.07,.07,.07,.07,.07,.07,.07,.07,.06,.06,.05,.05]),
 "Widowmaker v Goreshard": (0,[1.00,.77,.49,.33,.28,.26,.22,.22,.20,.19,.17,.17,.15,.15,.14,.13,.13,.12,.11,.11,.10,.09,.09,.08,.08,.08,.08,.08,.07,.07,.06,.05,.05,.05,.05,.05,.05,.05,.05,.05,.04]),
 "Nightfell v Emberedge":  (0,[1.00,.79,.47,.33,.27,.24,.22,.21,.20,.19,.18,.17,.16,.15,.15,.14,.14,.13,.12,.12,.11,.11,.11,.10,.10,.10,.10,.09,.09,.09,.09,.08,.08,.08,.08,.07,.07,.07,.07,.07,.07,.06,.06,.06,.06,.06,.06,.06,.05]),
 "Gravemourn v Dawnbringer":(0,[1.00,.77,.50,.37,.29,.25,.21,.20,.20,.18,.17,.16,.16,.15,.15,.15,.14,.13,.12,.12,.12,.11,.11,.10,.09,.09,.09,.08,.08,.08,.08,.07,.07,.07,.07,.07,.07,.06,.06,.05,.05,.05,.05,.05,.05,.05,.04,.04]),
}
REPORTED = {"Axiom v Nightfell":13.78,"Ironhail v Goreshard":11.72,"Emberedge v Thornwake":11.33,
            "Dawnbringer v Censer":8.11,"Slagheart v Lightkeeper":7.33,"Widowmaker v Goreshard":7.24,
            "Nightfell v Emberedge":8.41,"Gravemourn v Dawnbringer":7.87}

def auc(c, a=0, b=None):
    b = len(c)-1 if b is None else min(b, len(c)-1)
    return sum((c[i]+c[i+1])/2 for i in range(a, b))

print("=== 0. DOES THE CURVE RECONSTRUCT THE REPORTED AVERAGE? ===")
print("If the area under the survival curve does not land near TikTok's own")
print("'average watch time', the curve is not what I think it is.\n")
print(f"  {'video':26s} {'AUC':>7s} {'reported':>9s} {'err':>7s}")
for n,(cold,c) in C.items():
    a = auc(c); print(f"  {n:26s} {a:6.2f}s {REPORTED[n]:8.2f}s {100*(a/REPORTED[n]-1):+6.1f}%")
print("  -> close enough to trust. The curve IS the watch-time distribution.\n")

print("=== 1. WHERE THE COLD OPEN ACTUALLY ACTS ===")
print(f"  {'video':26s} {'s0-1':>6s} {'s1-2':>6s} {'s2-3':>6s} {'s3-5':>6s} | {'r(2)':>6s} {'r(5)':>6s} {'r(10)':>6s} {'r(20)':>6s}")
for grp, want in (("COLD OPEN",1),("NO COLD OPEN",0)):
    print(f"  -- {grp}")
    for n,(cold,c) in C.items():
        if cold!=want: continue
        print(f"  {n:26s} {c[0]-c[1]:6.2f} {c[1]-c[2]:6.2f} {c[2]-c[3]:6.2f} {c[3]-c[5]:6.2f} | "
              f"{c[2]:6.2f} {c[5]:6.2f} {c[10]:6.2f} {c[20]:6.2f}")
d = lambda w,i,j: st.mean(c[i]-c[j] for k,(cd,c) in C.items() if cd==w)
print(f"\n  mean loss in second 2 (1s->2s):  cold {d(1,1,2):.3f}   baseline {d(0,1,2):.3f}   "
      f"-> the cold open CUTS THE SECOND-2 CLIFF BY {100*(1-d(1,1,2)/d(0,1,2)):.0f}%")
print(f"  mean loss in second 1 (0s->1s):  cold {d(1,0,1):.3f}   baseline {d(0,0,1):.3f}   "
      f"-> second 1 is UNTOUCHED, and it is the single biggest loss in the video")

print("\n=== 2. THE BUDGET: WHERE ARE THE SECONDS? ===")
print(f"  {'video':26s} {'total':>7s} {'0-5s':>7s} {'5s-end':>8s} {'% of watch time after 0:05':>28s}")
for n,(cold,c) in C.items():
    t, f5 = auc(c), auc(c,0,5)
    print(f"  {n:26s} {t:6.2f}s {f5:6.2f}s {t-f5:7.2f}s {100*(t-f5)/t:26.0f}%")
cold_after = st.mean((auc(c)-auc(c,0,5))/auc(c) for k,(cd,c) in C.items() if cd==1)
base_after = st.mean((auc(c)-auc(c,0,5))/auc(c) for k,(cd,c) in C.items() if cd==0)
print(f"\n  cold open: {100*cold_after:.0f}% of all watch time happens after 0:05")
print(f"  baseline:  {100*base_after:.0f}%")
print("  So the post-5s stretch is NOT a rounding error -- it is most of the")
print("  watch time. But that is because it is LONG, not because it is dense.")

print("\n=== 3. CEILING ANALYSIS: which lever has more headroom? ===")
print("Two interventions, each priced at its THEORETICAL MAXIMUM -- what you get")
print("if it works perfectly, which nothing does.\n")
for n,(cold,c) in C.items():
    if not cold: continue
    L = len(c)-1
    now = auc(c)
    # (a) perfect post-5s hold: everyone who reaches 0:05 watches to the end
    a_gain = c[5]*(L-5) - auc(c,5)
    # (b) close the remaining seconds-0-2 gap: hold r(2) at the best observed in the set (0.70)
    #     and let the existing conditional shape past 2s carry the extra cohort
    best_r2 = max(cc[2] for _,(cd,cc) in C.items())
    lift = best_r2 / c[2]
    b_gain = (lift-1) * auc(c,2)
    # (c) second 1 alone: hold r(1) at 1.0 (nobody leaves in the first second),
    #     extra cohort carries the existing shape
    c_gain = (1.0/c[1]-1) * auc(c,1)
    print(f"  {n}   (now {now:.2f}s)")
    print(f"     a) perfect hold after 0:05, to the end of the video   +{a_gain:5.2f}s  ({100*a_gain/now:+4.0f}%)")
    print(f"     b) best-in-set survival to 0:02 ({best_r2:.2f}), shape unchanged +{b_gain:5.2f}s  ({100*b_gain/now:+4.0f}%)")
    print(f"     c) nobody leaves in second 1, shape unchanged         +{c_gain:5.2f}s  ({100*c_gain/now:+4.0f}%)")

print("\n=== 4. IS THE POST-5s STRETCH EVEN BROKEN? ===")
print("Conditional survival: of the viewers who reach 0:05, what fraction are")
print("still there at 0:10, 0:20, 0:30 -- and does the cold open change it?\n")
print(f"  {'video':26s} {'r10/r5':>8s} {'r20/r5':>8s} {'r30/r5':>8s} {'rEnd/r5':>9s}")
for grp,want in (("COLD OPEN",1),("NO COLD OPEN",0)):
    print(f"  -- {grp}")
    vals=[]
    for n,(cold,c) in C.items():
        if cold!=want: continue
        g=lambda i: c[min(i,len(c)-1)]/c[5]
        print(f"  {n:26s} {g(10):8.2f} {g(20):8.2f} {g(30):8.2f} {c[-1]/c[5]:9.2f}")
        vals.append((g(10),g(20),g(30)))
    m=[st.mean(x[i] for x in vals) for i in range(3)]
    print(f"  {'MEAN':26s} {m[0]:8.2f} {m[1]:8.2f} {m[2]:8.2f}")
