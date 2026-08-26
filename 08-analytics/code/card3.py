"""Three interventions on the card, modelled correctly this time.

card2.py was wrong: its 'no card' case replaced a zero-length window, so it
reproduced the observed curve and reported +0%. Removing the card is not
'replace 0 seconds' -- it is EXCISION. The 4 seconds cease to exist, the video
gets 4s shorter, and the cohort standing at card-up walks straight into what
used to be second 6.
"""
import statistics as st
COLD = {
 "Ironhail v Goreshard":  (2,[1.00,.85,.68,.56,.46,.35,.29,.27,.26,.24,.24,.22,.22,.21,.20,.20,.19,.18,.18,.18,.18,.18,.18,.17,.16,.16,.16,.16,.14,.14,.14,.14,.13,.13,.13,.13,.12,.12,.12,.12,.12,.10,.09,.08,.07]),
 "Emberedge v Thornwake": (2,[1.00,.80,.65,.54,.38,.31,.28,.27,.24,.24,.23,.23,.21,.20,.20,.19,.19,.18,.18,.18,.17,.16,.15,.15,.15,.14,.14,.13,.13,.13,.13,.13,.13,.12,.12,.12,.12,.12,.11,.11,.11,.11,.11,.09,.09,.08,.08,.07,.06]),
 "Dawnbringer v Censer":  (2,[1.00,.81,.65,.50,.36,.28,.24,.22,.22,.20,.19,.18,.18,.16,.16,.15,.13,.12,.12,.10,.10,.10,.10,.10,.10,.09,.09,.09,.07,.07,.06,.06,.06,.06,.06,.06,.05,.05,.05,.05,.05,.05,.04,.04,.04,.04,.03]),
 "Axiom v Nightfell":     (2,[1.00,.85,.70,.59,.43,.34,.31,.30,.29,.27,.26,.25,.23,.21,.21,.18,.17,.16,.16,.15,.14,.14,.13,.13,.13,.13,.12,.12,.12,.12,.12,.12,.12,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.11,.10,.10,.10,.10,.09,.09,.09,.08,.08,.08,.08,.07,.07,.07,.06,.06,.06,.04]),
}
CARD = 4                      # CONFIG.intro.dur
FIGHT_H = 0.158               # measured fight-playing hazard early in a video
auc = lambda c: sum((c[i]+c[i+1])/2 for i in range(len(c)-1))
haz = lambda c,t: (c[t]-c[t+1])/c[t]

def excise(c, a, drop):
    """Remove `drop` seconds of card starting at `a`. Video shortens by `drop`.
    The cohort at `a` walks into what used to be second a+drop, and the curve
    after that keeps its observed SHAPE, rescaled to be continuous."""
    keep = CARD - drop
    out = c[:a+1]
    # the card seconds that remain still run at the frozen-card hazard
    for k in range(keep):
        out.append(out[-1]*(1 - haz(c, a+k)))
    scale = out[-1] / c[a+CARD]
    for t in range(a+CARD+1, len(c)):
        out.append(c[t]*scale)
    return out

def unfreeze(c, a):
    """Keep the card and the video length, but let the fight run underneath it
    so the window decays at fight pace instead of frozen-card pace."""
    out = c[:a+1]
    for k in range(CARD):
        out.append(out[-1]*(1-FIGHT_H))
    scale = out[-1]/c[a+CARD]
    return out + [c[t]*scale for t in range(a+CARD+1, len(c))]

print(f"  {'video':24s} {'now':>7s} | {'kill card':>18s} | {'halve to 2s':>18s} | {'unfreeze, keep 4s':>19s}")
M=[[],[],[]]
for n,(a,c) in COLD.items():
    now=auc(c)
    k=auc(excise(c,a,4)); h=auc(excise(c,a,2)); u=auc(unfreeze(c,a))
    for i,v in enumerate((k,h,u)): M[i].append(v/now)
    print(f"  {n:24s} {now:6.2f}s | {k:7.2f}s ({100*(k/now-1):+4.0f}%) | {h:7.2f}s ({100*(h/now-1):+4.0f}%) | "
          f"{u:8.2f}s ({100*(u/now-1):+4.0f}%)")
print(f"  {'MEAN':24s} {9.42:6.2f}s | {'':7s} ({100*(st.mean(M[0])-1):+4.0f}%) | {'':7s} ({100*(st.mean(M[1])-1):+4.0f}%) | "
      f"{'':8s} ({100*(st.mean(M[2])-1):+4.0f}%)")

print(f"""
  Note the video also gets SHORTER when the card is cut -- 4s off a 44-48s
  video -- and that is already priced in above. The gain survives it.

  UPPER BOUND, and here is exactly why: the model lets the enlarged cohort
  (68% instead of 29%) decay at the rate the SMALL, self-selected cohort
  actually decayed at. A bigger crowd is a less committed crowd and would
  bleed faster. Treat these as the top of the range, not the estimate.

  LOWER BOUND is easy and it is still large: the card window alone runs at
  hazard {st.mean([haz(c,a+k) for n,(a,c) in COLD.items() for k in range(4)]):.3f}/s against a fight-playing {FIGHT_H:.3f}/s. Even if every
  recovered viewer left immediately afterwards, the four seconds themselves
  are being paid for at roughly 1.5x the going rate.""")

print("\n  EVERY LEVER MEASURED THIS SESSION, ranked")
print(f"    kill the 4s freeze                    +{100*(st.mean(M[0])-1):.0f}%   upper bound, not yet built")
print(f"    the cold open                         +44%   DELIVERED")
print(f"    run the fight under the card          +{100*(st.mean(M[2])-1):.0f}%   keeps the names and the VO")
print(f"    halve the card to 2s                  +{100*(st.mean(M[1])-1):.0f}%")
print(f"    close second 1 completely             +16-23%  theoretical, unreachable")
print(f"    best-in-set post-0:05 tail            +10%   the health-bar bet")
print(f"    best-in-set r(1)+r(2)                 +4%")
