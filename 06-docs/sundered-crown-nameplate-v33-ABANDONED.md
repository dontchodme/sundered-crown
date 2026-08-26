# NAME PLATE — the matchup over a fight that never stops. BUILT AND CHECKED.

**2026-08-19.** `nameplate_build.py --src ../02-chain/sc-cardspin.html --out
../02-chain/sc-nameplate.html`, applied to `ec9b8d753235385d`; result
**`921cf9425e0a8856`**. `01-live` untouched. Implements v32 §6 open decision 3.

Rick: *"The design question isn't 'card or no card' — it's how to keep the
naming without stopping the fight. lets do this."*

Three new tools: `nameplate_build.py` (the builder — the artifact is generated,
never hand-edited), `nameplate_probe.py` (seven checks, two of them controls),
`plate_occupancy.py` (where the plate goes, measured).

---

# 1. WHAT THE CARD ACTUALLY COSTS, AND WHAT WAS REPLACED

`CONFIG.intro.dur` is 4.0s and while `introT > 0` **`step()` returns early** —
the simulation does not advance. v32 §6 measured what that costs: card-first
videos lose 71–75% of the audience present when the card appears, cold opens
55–63%, and the hazard spike moves through the video with the card.

The plate keeps everything the card was carrying that a viewer needs — both
names, both affinities, both palettes, both ultimates — and lets the fight run.

```
                          CARD                        PLATE
duration                  4.0s                        3.0s
simulation                FROZEN                      running
frame occupied            ~58% cards + 80% scrim      236px, of which the HUD
                                                      already owned 152
what it leaves behind     nothing                     the HUD, still naming both
```

# 2. PLACEMENT WAS MEASURED, AND THE MEASUREMENT OVERRULED THE BRIEF

"Lower third" is the broadcast convention and it is wrong here.
`plate_occupancy.py` sampled 128 matches across eight pairings, inside the
3.0s window the plate would occupy, and asked where the relics actually are:

```
sim y   0-100   screen  176- 379    1.5% of relic-time   <-- quietest
sim y 600-700   screen 1394-1598   25.4% of relic-time   17.1x busier
```

**The relics live in the BOTTOM of the hall during that window** — a lower
third would land squarely on them. The top band is 17x quieter, and it is
where the names already are, so the plate can be the HUD briefly enlarged
rather than a second object competing with it.

# 3. TWO DEFECTS THE CONTACT SHEET MISSED AND 1:1 CAUGHT

**(a) The first cut printed every name twice.** The plate sat *below* the HUD —
but the HUD already carries both names, so the frame read `GORESHARD /
BLOODSWORN` at two sizes, 100px apart. Invisible at contact-sheet scale,
obvious at 1:1. Fixed by moving the plate ON to the HUD: it now covers y 0–236,
of which the HUD already owned 0–152, so the genuinely new occlusion is **84px**
— and that 84px is inside the band §2 cleared.

**(b) The clip rectangle travelled with the plate.** `c.translate()` was called
before `c.clip()`, so the clip that was supposed to hide the plate behind the
HUD moved with it and hid nothing. The retraction ghosted large text over the
HUD. The redesign removed the need for a clip entirely.

**(c) The exit printed names twice for ~0.2s.** The plate is taller than the HUD
it covers, so on the way out its lower row and the HUD's row were briefly both
on screen. Fixed by redrawing the HUD over the plate during the fall only — the
plate now slides up *behind* the HUD, which is the read the motion was claiming
anyway.

**The motion is a pure slide, never a cross-fade,** for the same reason: a
translucent plate shows the HUD's copy of both names through itself.

# 4. THE PROBE

```
PASS  [1]  engine_ab: 72 matches simulate identically in both builds
PASS  [2a] CONTROL -- with the CARD up, 3s of stepping moves the clock 0.0000s
PASS  [2b] with the PLATE up, 3s of stepping moves the clock 3.0000s
PASS  [3a] CONTROL -- the same frame twice reads 0.000 in the hall bands
PASS  [3b] the hall MOVES while the plate is up -- 6.422 against control 0.000
PASS  [4a] the plate band differs from the same frame without it -- 21.293
PASS  [4c] nothing below the plate changes -- 0.0000, the occlusion is bounded
PASS  [4b] by 3.6s the plate is GONE -- 0.000 against a frame that never had it
```

[2a]/[2b] is the whole thesis in one line, and it is falsifiable: the card build
and the plate build are handed the same three seconds and the card's clock does
not move. [4c] is stronger than "the plate is drawn" — it proves the occlusion
is **bounded** to the band that was cleared for it, so the plate cannot be
quietly eating hall that `plate_occupancy.py` never measured.

The probe reads the plate's geometry from `AC.CONFIG.plate` at runtime rather
than hardcoding it. An earlier version hardcoded the old band, and when the
plate moved it reported a FAIL that was the probe's fault, not the build's.

# 5. WHAT IS NOT DONE

1. **`cinema_clip.py` has no `--plate` flag.** The shorts pipeline still raises
   `introT`. Nothing can be *shipped* until that is wired — this is a build and
   a preview, not a deliverable video.
2. **The VO is not re-aligned.** `sc_cinema_clip.py` delays the voiceover 300ms
   into the video, which was written for a card at t=0. With the plate raised on
   the first clank (~1.6–2.0s) the names are spoken before they appear.
3. **Nobody has heard it.** The `seal` bell now fires at plate-down (3.0s)
   instead of card-down (4.0s), and the card's synthetic `clank` is gone — the
   real clank that triggers the plate is doing that job now, which is an
   improvement in theory and unheard in fact.
4. **The card's stat block is lost and that is a real loss.** The card showed
   damage/hit, reach, swing speed and weight for both relics, plus the passive
   and ultimate descriptions. The plate shows names, affinities and ult names.
   Stated rather than quietly dropped.

# 6. Open decisions

1. **Watch `card-vs-plate.mp4` first.** Everything above is measured; this is
   the judgement, and it is Rick's. 10s, side by side, same fight and seed.
2. **Is 3.0s right?** It is readable inside 0.5s. 2.2s would return another
   0.8s of fight and is a one-constant change.
3. **The stat block (§5.4) — gone, or does it come back somewhere?** It could
   ride the HUD after the plate retracts, or be dropped as something 55–75% of
   viewers never stayed for anyway.
4. **The retraction is cubic ease-in, so it sits still and then snaps out in
   the last ~0.15s.** Deliberate (get out of the way fast), and it may read as
   abrupt on a phone.
5. **Does the plate raise on the first clank, like the card?** Kept, because
   `firstbeat.py` made that a measured anchor rather than a taste call. But the
   plate does not need an event to hide behind — it could rise at t=0 and let
   the cold open be the fight from frame one.
6. **Promote to chain tip?** Two candidate tips are now behind
   `sc-cardspin.html`: this and `sc-health.html` `d0bb4890b19edc47`. They are
   independent and should not ship in the same video.
