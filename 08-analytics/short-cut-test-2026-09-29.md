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
