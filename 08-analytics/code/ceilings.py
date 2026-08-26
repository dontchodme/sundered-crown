"""Realistic ceilings. The theoretical ceiling ('everyone watches to the end')
prices an outcome no video on earth achieves. Price each lever instead against
the BEST SHAPE ALREADY OBSERVED on this channel -- an outcome that is known to
be reachable, because it was reached."""
import statistics as st
exec(open("/home/claude/tt/curves.py").read().split('REPORTED =')[0].split('C = {')[0])
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
def auc(c,a=0,b=None):
    b=len(c)-1 if b is None else min(b,len(c)-1)
    return sum((c[i]+c[i+1])/2 for i in range(a,b))
def cond(c,t):           # conditional survival curve past 5s, normalised to r(5)
    return [c[min(i,len(c)-1)]/c[5] for i in range(5,t)]

cold = {k:v for k,v in C.items() if v[0]}
BEST_R1 = max(c[1] for _,c in C.values())
BEST_R2 = max(c[2] for _,c in C.values())
# best observed conditional tail, measured as area under r(t)/r(5) per second of video
tails = {k: auc(c,5)/c[5]/(len(c)-1-5) for k,(cd,c) in C.items()}
BEST_TAIL = max(tails.values()); best_tail_name = max(tails, key=tails.get)

print("REALISTIC CEILINGS — each lever priced at the BEST SHAPE THIS CHANNEL HAS")
print("ALREADY PRODUCED, not at perfection.\n")
print(f"  best survival to 0:01 observed : {BEST_R1:.2f}  (Axiom / Ironhail)")
print(f"  best survival to 0:02 observed : {BEST_R2:.2f}  (Axiom)")
print(f"  best post-0:05 tail observed   : {BEST_TAIL:.3f} avg conditional survival/s  ({best_tail_name})")
print(f"  tail spread across all 8 videos: {min(tails.values()):.3f} to {BEST_TAIL:.3f}"
      f"  (ratio {BEST_TAIL/min(tails.values()):.2f}x)\n")

print(f"  {'video':24s} {'now':>7s} | {'FRONT: best r1+r2':>19s} | {'TAIL: best post-5s':>20s}")
tot_f=tot_t=tot_n=0
for n,(cd,c) in cold.items():
    now=auc(c); L=len(c)-1
    # FRONT: lift the whole curve past 0:02 by the ratio needed to hit best r(1) and r(2),
    # leaving the conditional shape after 0:02 exactly as it is.
    front = auc(c,0,1)*(BEST_R1/c[1]) if False else None
    lift2 = BEST_R2/c[2]
    f_new = (c[0]+BEST_R1)/2 + (BEST_R1+BEST_R2)/2 + lift2*auc(c,2)
    # TAIL: keep everything to 0:05 identical, replace the conditional tail with the best observed
    t_new = auc(c,0,5) + c[5]*BEST_TAIL*(L-5)
    print(f"  {n:24s} {now:6.2f}s | {f_new:8.2f}s ({100*(f_new/now-1):+4.0f}%) | {t_new:8.2f}s ({100*(t_new/now-1):+4.0f}%)")
    tot_f+=f_new; tot_t+=t_new; tot_n+=now
print(f"  {'MEAN':24s} {tot_n/4:6.2f}s | {tot_f/4:8.2f}s ({100*(tot_f/tot_n-1):+4.0f}%) | {tot_t/4:8.2f}s ({100*(tot_t/tot_n-1):+4.0f}%)")

print("\nAND THE COMPARISON THAT MATTERS:")
print(f"  The cold open already DELIVERED a 47% cut to the second-2 cliff and")
print(f"  {100*(11.23/7.80-1):.0f}% on average watch time. That is the size of win a front-door")
print(f"  change can produce here, because it is the size of win one just did.")
print(f"  For the tail to match it, post-0:05 conditional survival would have to")
print(f"  improve by more than the ENTIRE observed spread across eight videos")
print(f"  ({BEST_TAIL/min(tails.values()):.2f}x between the best and worst fight this channel has posted).")
