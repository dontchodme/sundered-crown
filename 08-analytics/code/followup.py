"""Two follow-ups the headline numbers do not answer on their own."""
import statistics as st

AFF = {"widowmaker":"bloodsworn","goreshard":"bloodsworn",
       "grudgebearer":"dwarven","slagheart":"dwarven","ironhail":"dwarven","emberedge":"dwarven",
       "spellbreaker":"runic","axiom":"runic",
       "gravemourn":"umbral","nightfell":"umbral",
       "thornwake":"verdant","heartwood":"verdant",
       "lightkeeper":"vigil","farwarden":"vigil",
       "dawnbringer":"sanctified","aureole":"sanctified","censer":"sanctified"}

# (a, b, length, avg_watch, cold_open)
V = [("axiom","nightfell",63,13.78,True), ("ironhail","goreshard",44,11.72,True),
     ("emberedge","thornwake",48,11.33,True), ("dawnbringer","censer",48,8.11,True),
     ("dawnbringer","grudgebearer",42,6.85,False), ("ironhail","widowmaker",42,9.71,False),
     ("grudgebearer","thornwake",45,6.46,False), ("gravemourn","dawnbringer",47,7.87,False),
     ("nightfell","emberedge",48,8.41,False), ("farwarden","nightfell",54,8.56,False),
     ("widowmaker","goreshard",40,7.24,False), ("slagheart","lightkeeper",47,7.33,False)]

print("=== 1. THE PALETTE-COLLISION HYPOTHESIS ===")
print("v28 flagged short-08 (dawnbringer v censer) BEFORE any numbers existed:")
print("both relics are `sanctified`, so both balls carry the same palette.")
print("It is the worst cold open. Tempting. Test it against the baseline too.\n")
for grp, want in (("COLD OPEN", True), ("BASELINE", False)):
    rows = [v for v in V if v[4] is want]
    print(f"  {grp}")
    for a,b,L,w,c in sorted(rows, key=lambda r:-100*r[3]/r[2]):
        same = AFF[a] == AFF[b]
        print(f"    {a+' v '+b:28s} {100*w/L:5.1f}%   {AFF[a]:11s} v {AFF[b]:11s} "
              f"{'<-- SAME PALETTE' if same else ''}")
    s = [100*r[3]/r[2] for r in rows if AFF[r[0]]==AFF[r[1]]]
    d = [100*r[3]/r[2] for r in rows if AFF[r[0]]!=AFF[r[1]]]
    if s and d:
        print(f"    same-palette mean {st.mean(s):.1f}%   contrast mean {st.mean(d):.1f}%"
              f"   -> {'SUPPORTS' if st.mean(s) < st.mean(d) else 'CONTRADICTS'} the hypothesis")
    print()
print("  VERDICT: inside the cold-open set the story fits perfectly (n=1).")
print("  Inside the baseline the only same-palette fight, widowmaker v goreshard,")
print("  reads 18.1% -- ABOVE the baseline mean of 17.2%. The one independent")
print("  test of the hypothesis points the OTHER way. It stays a hypothesis.\n")

print("=== 2. DOES EARLY MEASUREMENT INFLATE OR DEFLATE? ===")
print("v28 worried the early read was flattered by a first, more-engaged pool.")
print("Both re-measured videos moved UP, not down:\n")
# (name, age_at_v28_read_hours, then_views, then_watch, then_full, now_views, now_watch, now_full)
M = [("Axiom v Nightfell",     16, 320, 13.54,  6.7, 327, 13.78,  7.1),
     ("Ironhail v Goreshard",   2, 266,  9.98, 10.8, 287, 11.72, 13.5)]
print(f"  {'video':24s} {'age@read':>9s} {'watch then':>11s} {'watch now':>10s} {'drift':>7s} {'views then':>11s} {'views now':>10s}")
for n,age,v0,w0,f0,v1,w1,f1 in M:
    print(f"  {n:24s} {age:8d}h {w0:10.2f}s {w1:9.2f}s {100*(w1/w0-1):+6.1f}% {v0:11d} {v1:10d}")
print("\n  The 2-hour read understated by 17%; the 16-hour read by under 2%.")
print("  So the drift is real but almost all of it lands inside the first day,")
print("  and it runs UPWARD. Views are flat: +7 and +21 over three days -- these")
print("  videos are finished distributing.\n")
print("  Dawnbringer v Censer was ~22h old when read at 8.11s. On this curve it")
print("  should be within a few percent of final -- call it 8.1-8.6s. It does not")
print("  climb into the other three. Its number is bad, not young.")
