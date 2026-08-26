# v35 — THE SCRUNCH IS LIVE, AND THE VESSEL ROUND IS SHOT

**2026-08-19.** Two things were asked for: apply the live patch, then build the
next round of shorts. Both are done. Along the way the seed turned out to be
two divergent branches rather than one tree, and the shorts pipeline turned out
to have two defects that the pass marks could not see.

**Closed out the same day: Rick watched the round on the phone and passed it.
The liquid's standing gate is cleared — see §6.**

---

# 1. THE UPLOADS WERE TWO PARALLEL SESSIONS, NOT TWO VERSIONS

`scseedv31.zip` and `scseedv31_1.zip` both call themselves v31 and both name
themselves the chain tip candidate. They are **siblings**, built by two
different builders on the same v30 tip `sc-health18.html` `b57041681d7ee45b`:

```
scseedv31.zip     SEED.md: "THE RELIC IS A VESSEL"
                  liquid_build.py  -> sc-liquid.html          0277dc5fc464f8b0
                  + LIQUID-NOTES.md, _liquid_core.js, 4 liquid tools

scseedv31_1.zip   SEED.md: "THE CARD STOPS FREEZING THE FIGHT"
                  scrunch_build.py -> sc-health18-scrunch.html a833b87f05780e9a
                  + 07-live-patch/, 08-analytics/, nameplate work
```

Neither zip contains the other's work. Taking either one as "the seed" silently
drops a whole session. The merged tree keeps both, with each branch's own
`SEED.md` / `NEXT-SESSION.md` preserved as `06-docs/*-v31-liquid.md` rather than
overwritten, and `tools/README.md` reunited with the liquid builders' entries.

All eight hashes claimed across the two `SEED.md` files and
`07-live-patch/APPLY-ME.md` verify exactly against the delivered bytes.

# 2. APPLIED, AND RE-PROBED RATHER THAN TRUSTED

`07-live-patch/APPLY-ME.md` run verbatim. `01-live` now:

```
sc-playable.html                 dafddc51096ca2e4   (was 710b5fd95d877e61)
sc-playable.PRE-SCRUNCH.html     710b5fd95d877e61
sundered-crown.html              71f2b2a3e6870365   (was 51c9bf566f9eb679)
sundered-crown.PRE-SCRUNCH.html  51c9bf566f9eb679
```

The doc claims 13/13. **That claim was re-run, not accepted** —
`scrunch_probe.py` against both applied pairs, ALL PASS both times, including
the two that carry the argument (`[2a]` the card build's clock does not move in
3s; `[2b]` the scrunch build's moves 3.0000s) and `[4b]`, which reads the four
mutated layout fields back after a scrunched draw and requires 1056 / 12 exactly.

# 3. THE TWO BRANCHES COMPOSE — `sc-liquid-scrunch.html` `46a14e5710fad1e1`

Rick's call: the filming build should carry the liquid **and** the scrunch. It
did not exist; both are single builders over the same v30 tip, so:

```
python3 scrunch_build.py --src ../02-chain/sc-liquid.html \
                         --out ../02-chain/sc-liquid-scrunch.html --k 0.70
```

```
scrunch_probe.py  sc-liquid -> sc-liquid-scrunch     13/13 ALL PASS
liquid_probe.py   --src sc-liquid-scrunch            14/14 PASS
frame cost @1080x1920, median                        -2.8% vs sc-health18
```

18 relics, `SLAGBURST`, the glass vessel, and the scrunch panel. It is faster
than the build it derives from, because the liquid integrator is off in headless
sweeps and the scrunch replaced a full-frame card draw with a strip.

# 4. TWO DEFECTS IN THE SHORTS PIPELINE, BOTH INVISIBLE TO THE PASS MARKS

Every rendered clip would have passed all five delivery checks with both of
these live. Neither was found by a check; both were found by looking.

## (a) The card and the scrunch STACK — and `shorts_build.py` forced it

`cinema_clip.py` sets `m.introT` from `--intro`, then calls `AC.__inject`, which
sets `scrunchAuto = CONFIG.scrunch.on`. On a scrunch build **both fire.**
`shorts_build.py`'s `capture()` hardcoded `--intro` with no way to turn it off.
Measured on `sc-liquid-scrunch`, ironhail v emberedge `3709119762`:

```
                   match clock after 4s of wall     scrunch panel arms
--intro                    0.00s  (frozen card)     wall 5.92s
no --intro                 4.00s  (fight running)   wall 1.91s, on first clank
```

So `--intro` on this build ships **a 4-second dead stop and then a second
legend two seconds later** — it reintroduces the exact cliff the scrunch was
built to remove (08-analytics: card-first videos lose 71-75% of the audience
present when the card appears). Fixed: `shorts_build.py --no-card`, and the tool
now shouts when it detects `CONFIG.scrunch` in a build it is filming with the
card on.

## (b) The verdict beat was being cut off — the payoff never rendered

`cinema_clip.py` held a flat `fps * 2.2` seconds of frames after `m.over`.
`CONFIG.scrunch.resultDelay` is **1.05s of MATCH time**, and the kill is exactly
where the director runs the tape slowest, so it stretches to **~1.9-2.0s of
VIDEO**. The panel got 12 frames and capture stopped. The first render of
v31-1 ends on a frozen clock, `0% / 0%`, and no verdict at all.

The stretch factor is the kill cut's `timeScale`, which differs per fight, so
**no constant is right for every fight.** Fixed by anchoring on the event, which
is the principle that file already states for the cold open — `frame()` now
reports `scrunchMode`, and the tail runs until the verdict has actually been up
for `--verdict-hold` seconds (default 2.4), with an 8s runaway cap and a fallback
to the old 2.2s tail on builds with no scrunch. All three clips report:

```
verdict panel held 2.40s of the 4.30s tail (armed 1.90s after the kill)
```

# 5. THE ROUND — `07-shorts/vessel/`

Picked by a new tool, `tools/vessel_pick.py`. This round is judging an
instrument as well as selling a game, so `|winner_hp - 55|` (≈18% of baseHP 300,
the criterion the v31 liquid clips used) is a **first-class scoring term**, not a
tiebreak: a fight the winner finishes at 80% says nothing about whether a
falling liquid level reads. Every rejection is reported rather than silently
dropped.

```
1620 matches over 9 pairings -> 81 qualify (5.0%)
rejected: slow open x945, 1 cut x193, 0 cuts x176, duration x8
```

The 945 slow opens are `firstbeat.py`'s median-3.18s-to-first-clank finding
showing up again. The bar was not lowered to find fights.

```
                                      seed      video  match  winner   cuts
v31-1  Slagheart v Aureole       1970938319     42.0s  33.8s   2/300      3
v31-2  Ironhail v Emberedge      3709119762     40.8s  32.8s  66/300      4
v31-3  Lastlight v Lightkeeper    669544401     51.3s  42.2s  66/300      3
```

All three: `sc-liquid-scrunch.html`, `--no-card`, 60fps, w540 -> 1080x1920,
crf 23, `bm_lewis`, limiter rung 0.79 / TP -2.0. Re-measured independently of
the builder's own report: **-15.9 / -15.8 / -15.7 LUFS, -1.0 / -1.6 / -0.6 dBTP**,
all inside the §3 pass band.

Why these three:

- **v31-1 is the instrument clip.** Slagheart wins on **2 of 300** — the winner's
  vessel is a sliver of amber at the bottom of the glass and the loser's has
  failed outright. Both vessels legible in the same frame, which is the only
  configuration that tests the feature.
- **v31-2 is the television clip.** Four distinct cuts, and both ultimates
  detonate — `QUARRELSTORM` and `SLAGBURST`. Live has never had Slagburst.
- **v31-3 is the new content.** Lastlight and Lightkeeper, and it is the only
  one with a magenta palette, so the reel does not read as one video three times.

`cinema_vo.py`'s `SPOKEN` table gained `Slagheart / Lastlight / Emberedge` on the
file's own compound-splitting rule; Aureole was left alone because it is a real
word. The id-to-name check was re-run for the 18-relic roster as
SHORTSHANDOFF requires: still exactly one mismatch, `oathwound -> Goreshard`,
and it is not in this round.

# 6. THE GATE CLEARED — the liquid was judged on the phone and passed

**2026-08-19, Rick, on the delivered round:** *"looks good on the phone. call
this done."*

This closes the liquid branch's own next-session instruction, which was the one
thing 14 passing checks could not settle. The record matters because of what the
branch had already been through: **Rick cut the graduations and then the fracture,
both on the picture** — the vessel's history is a history of things removed after
being looked at, so a pass on the picture is the gate that was actually load-
bearing, not the probe suite.

What this does and does not establish:

```
established   the vessel reads at phone size, in motion, with sound,
              at Shorts bitrate, on the composed liquid+scrunch build
NOT           anything about retention, shares or saves -- that is §2 of the
              open decisions below and needs the posts, not an opinion
```

The vessel is therefore promoted from *unjudged* to **shipped-quality**, and
`sc-liquid-scrunch.html` `46a14e5710fad1e1` is the build of record for this
round. The three clips are final; nothing further is queued.

---

# Open decisions

1. **The slate protocol was not honoured, and this is the place it is recorded.**
   `retention-curves` open decision 2 says *finish the slate on `sc-cardspin`,
   then change one thing.* This round changes three at once — no card, the
   scrunch, and a new health visual — on a build that was also never promoted to
   live. It buys speed and costs attribution: if these three move, the read will
   not say which change did it. Worth deciding whether a `sc-cardspin` control
   post goes up alongside them. **Still open at close of session.**
2. **The registered prediction still stands and should be graded, not
   forgotten.** shares > 0, saves/view roughly double, **post-0:05 hazard flat**
   (0.032-0.050 across every video ever posted). If watch time rises and the
   hazard curve is unchanged, the gain came from somewhere else. The phone pass
   in §6 is not evidence for or against any of this.
3. **The verdict hold is 2.4s and that number is a guess.** It is the first hold
   that is long enough to *read*; nobody has tested whether 2.4s is where a
   viewer shares or where they swipe. It is one flag.
4. **`01-live` is now a scrunch build, and the shorts are not shot on it.** Live
   is 16 relics on FORGEFALL; the round is 18 relics on SLAGBURST with a liquid
   vessel. Promoting the chain tip to live is v27 open decision 1 and is **still
   open** — and §6 sharpens it rather than settling it: the vessel has now passed
   the only gate that was blocking it, so the reason not to promote is no longer
   "unjudged".
5. **v31-3 is 51.3s against a 60s cap.** 42.2s of match became 51.3s of video —
   +9.1s of director dilation over three cuts, well above the +1s-per-set-piece
   rule of thumb in SHORTSHANDOFF §4. That rule needs re-deriving on tape-heavy
   builds before a longer fight gets picked.
6. ~~**The liquid still has not been judged the way Rick judges things.**~~
   **CLOSED 2026-08-19** — see §6. Passed on the phone.
