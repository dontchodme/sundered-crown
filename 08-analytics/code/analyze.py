"""TikTok cold-open read, v2 -- measured 2026-08-19 from TikTok Studio.

Every row below was read off the per-video analytics page today, so ages are
comparable in the sense that they are all "as of now" -- but NOT in the sense
that the videos are the same age. That is handled explicitly, not ignored.
"""
import itertools, statistics as st
from scipy.stats import mannwhitneyu, pearsonr

# name, posted (iso), length_s, views, avg_watch_s, full_pct, stopped_at_s, cold_open
ROWS = [
 ("Axiom v Nightfell",        "2026-08-16T02:14", 63, 327, 13.78,  7.1, 4, True),
 ("Ironhail v Goreshard",     "2026-08-16T15:56", 44, 287, 11.72, 13.5, 2, True),
 ("Emberedge v Thornwake",    "2026-08-17T08:15", 48, 301, 11.33,  7.9, 1, True),
 ("Dawnbringer v Censer",     "2026-08-18T08:15", 48, 278,  8.11,  4.6, 1, True),

 ("Grudgrwaker v Thornwake",  "2026-08-12T16:41", 38,  18, 24.87, 14.7, 1, False),
 ("Dawnbringer v Grudgebearer","2026-08-13T15:03",42, 302,  6.85,  3.5, 2, False),
 ("Ironhail v Widowmaker",    "2026-08-13T23:08", 42, 240,  9.71,  7.7, 1, False),
 ("Grudgebearer v Thornwake", "2026-08-13T23:26", 45, 337,  6.46,  3.8, 1, False),
 ("Gravemourn v Dawnbringer", "2026-08-13T23:27", 47, 325,  7.87,  5.0, 2, False),
 ("Nightfell v Emberedge",    "2026-08-14T16:46", 48, 498,  8.41,  6.9, 2, False),
 ("Farwarden v Nightfell",    "2026-08-14T16:46", 54, 652,  8.56,  4.8, 2, False),
 ("Widowmaker v Goreshard",   "2026-08-14T17:13", 40, 300,  7.24,  3.9, 2, False),
 ("Grudgebearer v Thornwake2","2026-08-14T18:29", 31,  31, 15.09, 20.8, 2, False),
 ("Slagheart v Lightkeeper",  "2026-08-15T12:47", 47, 247,  7.33,  6.4, 2, False),
]

# A video with 18 or 31 views has an average watch time computed over a pool
# small enough that a handful of loops dominates it. Both tiny-n rows sit at
# the TOP of the channel on watch time and at the top on completion -- exactly
# the signature of a near-dead post seen almost only by people who sought it
# out. They are excluded from every comparison and reported separately, rather
# than quietly dropped.
MIN_VIEWS = 100
big  = [r for r in ROWS if r[3] >= MIN_VIEWS]
tiny = [r for r in ROWS if r[3] <  MIN_VIEWS]

def show(rows, title):
    print(f"\n{title}")
    print(f"  {'video':28s} {'len':>4s} {'views':>6s} {'watch':>7s} {'ret%':>6s} {'full%':>6s} {'stop':>5s}")
    for n,d,L,v,w,f,s,c in sorted(rows, key=lambda r:-r[4]):
        print(f"  {n:28s} {L:4d} {v:6d} {w:7.2f} {100*w/L:5.1f}% {f:5.1f}% {s:4d}s")

cold = [r for r in big if r[7]]
base = [r for r in big if not r[7]]
show(cold, "COLD OPEN  (n=%d, views>=%d)" % (len(cold), MIN_VIEWS))
show(base, "NO COLD OPEN  (n=%d, views>=%d)" % (len(base), MIN_VIEWS))
show(tiny, "EXCLUDED -- too few views for the mean to mean anything")

def block(metric, fn, unit=""):
    c = [fn(r) for r in cold]; b = [fn(r) for r in base]
    u, p = mannwhitneyu(c, b, alternative="greater")
    # exact permutation p as well: with n=4 vs n=8 the U-test's tie handling
    # and continuity are worth cross-checking against brute force.
    allv = c + b; obs = st.mean(c) - st.mean(b); hits = tot = 0
    for combo in itertools.combinations(range(len(allv)), len(c)):
        cc = [allv[i] for i in combo]; bb = [allv[i] for i in range(len(allv)) if i not in combo]
        tot += 1
        if st.mean(cc) - st.mean(bb) >= obs - 1e-12: hits += 1
    print(f"\n{metric}")
    print(f"  cold open   mean {st.mean(c):6.2f}{unit}   median {st.median(c):6.2f}{unit}   range {min(c):.2f}-{max(c):.2f}")
    print(f"  baseline    mean {st.mean(b):6.2f}{unit}   median {st.median(b):6.2f}{unit}   range {min(b):.2f}-{max(b):.2f}")
    print(f"  difference  {st.mean(c)-st.mean(b):+.2f}{unit}  ({100*(st.mean(c)/st.mean(b)-1):+.1f}%)")
    print(f"  Mann-Whitney one-sided p = {p:.4f}    exact permutation p = {hits/tot:.4f}  ({tot} arrangements)")
    print(f"  overlap: {sum(1 for x in b if x >= min(c))}/{len(b)} baseline videos reach the WORST cold open")

block("AVERAGE WATCH TIME", lambda r: r[4], "s")
block("RETENTION -- watch time as a share of the video's own length", lambda r: 100*r[4]/r[2], "%")
block("WATCHED FULL VIDEO", lambda r: r[5], "%")
block("VIEWS", lambda r: float(r[3]))

print("\nLENGTH IS A CONFOUND -- test it, do not assume it")
L = [r[2] for r in big]; W = [r[4] for r in big]
rr, pp = pearsonr(L, W)
print(f"  length vs avg watch, all {len(big)} videos:  r = {rr:+.3f}  p = {pp:.3f}")
Lb = [r[2] for r in base]; Wb = [r[4] for r in base]
rr2, pp2 = pearsonr(Lb, Wb)
print(f"  length vs avg watch, baseline only (n={len(base)}): r = {rr2:+.3f}  p = {pp2:.3f}")
print("  -> the longest video on the channel is a cold open (63s). If longer")
print("     videos mechanically earn more watch SECONDS, the raw-seconds")
print("     comparison flatters the cold open and the ret% row is the honest one.")

print("\nTHE ORDER EFFECT -- cold opens in the order they were posted")
for n,d,L,v,w,f,s,c in cold:
    print(f"  {d[5:16]}  {n:24s} {w:6.2f}s   {100*w/L:5.1f}% of length   full {f:4.1f}%   stopped {s}s")
print("  strictly monotonic decline on watch time across all four.")

print("\nWHAT THE PRE-REGISTERED THRESHOLD ACTUALLY SAID")
print("  v28 registered: >9s mean avg watch = worked; 7-8.5s = did not.")
print(f"  cold-open mean now: {st.mean([r[4] for r in cold]):.2f}s  -> clears it.")
over9 = [r for r in base if r[4] > 9]
print(f"  BUT {len(over9)} baseline video(s) already exceeded 9s: " +
      ", ".join(f"{r[0]} {r[4]:.2f}s" for r in over9))
print("  That video is not in the v28 baseline table. The threshold was set")
print("  against an incomplete baseline, so clearing it proves less than it looks.")

print("\nDROP-OFF POINT -- the v28 headline claim")
from collections import Counter
print("  cold open   stopped-at:", Counter(r[6] for r in cold).most_common())
print("  baseline    stopped-at:", Counter(r[6] for r in base).most_common())
print("  0:04 (Axiom) is unique on the channel. Two of four cold opens read")
print("  0:01 -- WORSE than the baseline mode of 0:02. The cliff did not move.")
