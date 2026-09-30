# SHORT-CUT TEST — registered 2026-09-29, before any clip is filmed

**Rick, 2026-09-29:** test a few 15–20 second cuts. Everything else is unchanged:
the full-opening ruling of 2026-09-16 stands for all other shorts, and the
Super Weapon Ball World Cup waits for the full roster.

**The question.** About 97% of every audience leaves before the end of a
full-length short (finish rate 0.8–5.0% across the 16 posts since 8/24), and no
post shorter than 41s has ever been fairly tested. Does a 15–20s cut get
finished more, and does that buy distribution?

## How to make one (the desktop app — no build change needed)

1. Pick the two fighters and press Fight. Watch it; keep fights whose finish is
   a clear, readable kill.
2. In **Create short**, untick **Film the whole fight**.
3. Set **seconds before the finish** to **15** (delivers ~20s with the verdict).
4. Press **Create short**.

The app passes `--lead 15` to `shorts_build.py` (main.js:440); the seed is the
live one on screen (shell.js `__lastSeed`).

## The four fights (Cowork's picks — Rick: "you pick them")

Post one a day, in this order. In the app: pick the two fighters, type the seed
into **Seed**, press **Replay**, check the winner and the rough finish time match
the line below, then make the short as above. If the winner or time is different,
the app's browser is playing the seed differently (see the caveat) — use the
backup seed, or press Fight until a fight ends with the winner nearly dead.

```
day  fight                     seed   expected finish                   backup seed
 1   Vesper vs Culverin        1005   Vesper wins at ~49s on ~1% HP     1039 (Culverin, ~57s, ~3%)
 2   Gravemourn vs Censer      1033   Gravemourn wins at ~52s on ~1%    1014 (Gravemourn, ~51s, ~2%)
 3   Cindercleave vs Briarwand 1035   Briarwand wins at ~58s on a sliver 1018 (Cindercleave, ~58s, ~1%)
 4   Goreshard vs Gloamwire    1044   Gloamwire wins at ~62s on ~1%     1041 (Gloamwire, ~57s, ~1%)
```

**How they were chosen** (`tools/finish_probe.py`, 15s window):
- Every one of the 788 pairings never posted, 6 seeds each (4,728 fights): 96% of
  fights have an ultimate inside the last 15s, and the median winner ends on 20% HP
  — the endings are good roster-wide, so the pick is for variety and a live finish.
- Dropped any fighter already posted 3+ times (Dawnbringer, Nightfell, Emberedge,
  Grudgebearer, Ironhail, Slagheart, Threshmaw, Twinshade, Lastlight); kept only
  cross-type pairings. The four cover all four weapon forms (spin, swing, chain,
  ranged), eight different fighters, two of them staves.
- Ranked on: result still open when the window starts (both sides at 35%+ HP),
  close finish, and both sides able to win. Then 80 seeds per pairing; seeds kept
  only if the kill is a slay at 40–75s, the result is open at the window, an ult
  lands inside it, the winner ends on 15% HP or less, and the window is busier than
  that pairing's median.

```
pairing (n=80)             side-A wins     open at window   ult in window   winner HP (median)
Vesper v Culverin          Vesper 30%      72%              100%            21%
Gravemourn v Censer        Gravemourn 59%  86%               99%            32%
Cindercleave v Briarwand   Cindercleave 62% 72%             100%            18%
Goreshard v Gloamwire      Goreshard 21%   69%              100%            14%
```

**Caveat, stated because it can bite:** measured on HeadlessChrome 141 in Cowork's
container, not the repo's pinned runtime. A seed is the same fight only on the same
engine arithmetic; Replay in the app is the check. Reproduction control: the
committed `finish_probe.py` re-run on four of the seeds returned the same winners,
times (±0.2s) and HP as the exploratory run.

## Posting rules (the account has live duplicate-content strikes)

- **Four posts, one a day.** Never two inside a few hours, never a batch.
- **A fresh fight each time**, and a pairing not posted in the last few weeks.
  Never upload the same file twice, including after a delete.
- Caption: `Super Weapon Ball <A> vs <B> #weaponball #weaponballs #superweaponball`
  — **no `#earclacks`**. That drops a tag at the same time as the length change;
  accepted for strike safety, and no tag set has ever predicted views here.
- Nothing else posts during the four days (Rick's call: wait for the Cup), so
  the baseline is the recent full-length posts below, not a same-week control.

## Baseline (per-video pull 2026-09-29, `tiktok-posts-2026-09-29.csv`)

```
16 full-length posts, 8/24-9/28     finish rate median 2.3%  (0.8-5.0%)
                                    views median 238  (130-377, one 903)
                                    avg watch median 8.3s    shares 0
last four (9/19-9/28)               views 231 354 312 282    finish 2.0-4.5%
```

## Prediction, registered before filming (v44 open decision 1, unchanged)

**Finish rate above 25% and views above 400**, on at least three of the four.

Read each post at 48 hours (about 90% of a post's views land on day one).

```
finish >25% AND views >400   length was a gate -> short cuts go into the Cup plan
finish up, views ~150-350    finishing is not the gate either -> ruling stands, look at shares/format
neither moves                length is not a lever -> ruling stands, with evidence
```

Also record per post: shares, saves, new followers, traffic source. Pull: the
Studio insight endpoint (v32 §0) from a logged-in browser — Cowork runs it on request.
