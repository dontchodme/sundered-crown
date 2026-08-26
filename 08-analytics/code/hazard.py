"""Is the post-0:05 tail a CONSTANT-HAZARD process?

This is the question that decides whether ANY mid-video content change can work.
- Constant hazard: viewers leave at a fixed rate per second regardless of what is
  on screen. Memoryless. Departure is scroll habit, not a reaction to content.
- Structured hazard: spikes where something loses them, troughs where something
  holds them. Then content in the tail is a lever and it is worth pulling.

A comprehension problem -- "I can't tell who's winning, I'm out" -- would show as
an ELBOW: a cluster of departures at a particular moment. A habit would not.
"""
import statistics as st
exec(open("ceilings.py").read().split("cold = {")[0])

print("PER-SECOND HAZARD after 0:05  h(t) = (r(t)-r(t+1))/r(t)\n")
print(f"  {'video':26s} {'mean h':>7s} {'sd':>6s} {'CV':>6s} {'max h':>6s} {'@t':>4s} {'h(5-15)':>8s} {'h(15-30)':>9s} {'h(30+)':>7s}")
allh=[]
for n,(cd,c) in C.items():
    L=len(c)-1
    h=[(c[t]-c[t+1])/c[t] for t in range(5,L) if c[t]>0]
    if not h: continue
    seg=lambda a,b:[x for i,x in enumerate(h) if a<=i+5<b]
    s1,s2,s3 = seg(5,15), seg(15,30), seg(30,999)
    mx=max(h); at=h.index(mx)+5
    print(f"  {n:26s} {st.mean(h):7.3f} {st.pstdev(h):6.3f} {st.pstdev(h)/st.mean(h):6.2f} "
          f"{mx:6.3f} {at:4d} {st.mean(s1) if s1 else 0:8.3f} {st.mean(s2) if s2 else 0:9.3f} "
          f"{st.mean(s3) if s3 else 0:7.3f}")
    allh.append((n,cd,h))

print("\nIS THERE AN ELBOW? A content failure should put an unusually large share of")
print("the tail's departures in ONE place, in the SAME place, across videos.\n")
import collections
peaks=collections.Counter()
for n,cd,h in allh:
    order=sorted(range(len(h)), key=lambda i:-h[i])[:3]
    peaks.update([i+5 for i in order])
print("  seconds that appear in a video's top-3 hazard spikes, across all 8:")
print("   ", ", ".join(f"{t}s x{c}" for t,c in peaks.most_common(10)))
print("\n  Departures cluster at the END of each video (the last seconds before it")
print("  loops or the viewer's decision point), not at any shared mid-video moment.")

print("\nDECAY-RATE COMPARISON: front vs tail hazard")
for n,(cd,c) in C.items():
    hf=[(c[t]-c[t+1])/c[t] for t in range(0,3)]
    ht=[(c[t]-c[t+1])/c[t] for t in range(5,len(c)-1) if c[t]>0]
    print(f"  {n:26s} {'COLD' if cd else 'base':5s}  seconds 0-3 hazard {st.mean(hf):.3f}   after 0:05 hazard {st.mean(ht):.3f}"
          f"   ratio {st.mean(hf)/st.mean(ht):5.1f}x")
print("\n  A viewer in the first three seconds is an order of magnitude more likely")
print("  to leave in the next second than a viewer at 0:20. The front of the video")
print("  is where the audience is decided; the tail just bleeds slowly.")
