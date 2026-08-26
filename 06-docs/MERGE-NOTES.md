# THE MERGE — two patches, and a rebase that was not optional

**2026-08-15.** Rick handed over `scslagburstpatch.zip` and
`scpatchtwotowers.zip`. Both are applied. Chain tip is now
`02-chain/sc-ember.html` **`6e73c5776cdee56a`**, and **01-live has moved off
v21 for the first time**.

---

# 1. What the two patches actually were

**SLAGBURST** — Emberedge's Forgefall retired for `kind:"detonate"`. Authored
against `sc-daybreak.html c25a90cc0ca82f68`, which *is* a node in this chain,
so it looked like a clean fast-forward. It was.

**TWO TOWERS** — a ship package for `01-live`: v21 + Crucible + Daybreak,
`51c9bf566f9eb679`. Authored against v21, so it looked *older* than the
chain. **It was not**, and that is the whole story of this merge.

# 2. The rebase

Diffing the substance rather than trusting the base hash: the TWO TOWERS game
file differs from the chain's `sc-daybreak.html` by 59 lines, and they are
**not a re-tune**. They add a mechanic the chain does not have:

```
sparkGrace: 0.7   an arm chirp, `justArmed`, and a grace period during which
                  a spark cannot be taken by anyone
```

with the measurement that justifies it recorded in the patch: *95% of sparks
died within 0.4s* in the scrum. It also answers the density question that
`NEXT-SESSION` had flagged as open — **6 sparks × 5 damage** against the
chain's 3 × 8 — and repays Dawnbringer's blade to 10.4 rather than 9.6.

So the chain's Daybreak was the older one. **Shipping the chain over live
would have regressed a measured fix.** The chain was rebased onto the patch's
game file and all three builders re-applied:

```
02-chain/sc-daybreak2.html   51c9bf566f9eb679   TWO TOWERS  <-- new base
  introfit_build             465bde798a39e4eb   sc-introfit
  slagheart_build            5c690961c489f8f5   sc-slagheart
    (--no-massref)           b7b816003fbcbc23   sc-slagheart-norm
  ultember_build             6e73c5776cdee56a   sc-ember    <-- TIP
```

**Every anchor in all three builders hit exactly once on the new base.** That
is the whole reason the anchored-builder discipline exists, and this is the
first time it has had to absorb an out-of-order patch.

Superseded, and not to be built from again: `sc-daybreak.html
c25a90cc0ca82f68`, `sc-introfit 71c0a0c0c1ea6996`, `sc-slagheart
f4d8aa660fe0ee0f`.

# 3. A bug the incoming notes caught in MY work

`SLAGBURST-PATCH.md` records: *"THE FX CLOCK RUNS AT 2x SIM TIME. `ultFx.t`
is advanced by BOTH decay paths, so every `life` number in the engine is in
half-seconds."*

Verified before being believed — measured on this build:

```
normal path   ultFx.t advances 1.945x per second of match time
hit-stop      exactly 1.000x
```

`decay(dt)` calls `decayImpactOnly(dt)` (which ticks presentation) and then
calls `tickPresentation(dt)` again itself.

**It had already broken Ironbloom.** Its lit phase shipped with
`life = window + 0.4 = 6.4`, which is **3.3 seconds of screen time against a
6.0 second window** — the tell for the relic's signature state was absent for
nearly half of it, and nothing in my harness could see it. Fixed: normal-path
phases doubled (lit 12.8, blast 3.0, fizzle 1.8). The `held` phase stays at
1× because it runs inside `step()`'s latch branch, which ticks presentation
once — an exception that exists nowhere else in the game, because no other
set-piece owns a frozen branch of its own.

`slagheart_probe [11]` now measures the fx rate live and asserts the lit
set-piece outlives the window it explains. It cannot regress silently again.

# 4. The other correction I have adopted

`verify.py --n 60` has SE ≈ 1.7pp against a field ~5pp wide, and its bar
chart is ordered and looks decisive. The v23 note's "floor" — Farwarden ~46 /
Gravemourn ~47 / Spellbreaker ~47.5 — **is noise**; two disjoint seed sets put
Farwarden near the top. Only Lightkeeper and Nightfell are bottom-three in
both.

This applies to my own numbers too. **Slagheart's 51.4% carries the same
±1.7pp**, so "inside the 46–52 field" is the honest claim and "third strongest
relic" is not. Read the bar chart as a band.

# 5. Every check on the rebased tip `6e73c5776cdee56a`

```
verify.py --n 60    13/13 over 136 pairings
                    Grudgebearer 62.4 · Dawnbringer 54.1 · SLAGHEART 51.4
                    Lightkeeper 50.7 · Censer 50.6 · Emberedge 50.5 ·
                    Aureole 50.2 · Widowmaker 50.0 · Farwarden 49.8 ·
                    Heartwood/Nightfell 49.4 · Gravemourn/Goreshard 47.8 ·
                    Ironhail 47.6 · Thornwake 47.1 · Axiom 45.9 ·
                    Spellbreaker 45.3
                    Both deliberate towers intact. Slagheart needed NO
                    re-tune after the rebase. Emberedge sideways at 50.5,
                    as the Slagburst patch claimed.
engine_ab --n 50    6000/6000 IDENTICAL — sc-slagheart vs sc-ember on the 16
                    non-Emberedge ids. Slagburst is inert.
ultember_check      23/23   (the incoming harness, on the rebased build)
slagheart_probe     17/17   (including the new [11] fx-clock regression)
introfit_probe      8/8 — 17/17 relics fit the card, 34/34 bands clean
intro_probe         [1]-[6] PASS, scoped to the CARD STEP
tip_audit           0 gaps
massref_probe       mean fall multiplier 1.000 at 2.680
```

**A scoping note on `intro_probe [1]`:** run against the tip it fails, and
correctly — the tip's engine differs from the base by a relic, an ultimate
and a physics constant, which is not what [1] asks. [1] is a purity claim
about the CARD, so it is run on the card step alone:
`--src sc-daybreak2.html --out sc-introfit.html --pre sc-c2.html`.

# 6. What is live, and what is not

```
01-live/sundered-crown.html   51c9bf566f9eb679   TWO TOWERS, as instructed
01-live/sc-playable.html      710b5fd95d877e61   its matching share page
```

The tip **strictly dominates** this: same Crucible, same Daybreak, plus the
fight card v3, Slagheart/Ironbloom, Slagburst and the massRef correction.
One `cp 02-chain/sc-ember.html 01-live/sundered-crown.html` followed by
`share_build --src` ships the lot. Not done — that is Rick's word, and the
patch only authorised the two towers.

# 7. Open

1. **Rick's eyes, with sound.** Carried from both patches and still true.
   Slagburst has no mp4 at all; Ironbloom's clip is silent; Daybreak's new
   arm chirp has never been heard.
2. **Ironbloom's clip is now stale** — it was cut before the fx-clock fix, so
   the lit-head glow in it dies early. Re-cut before showing anyone.
3. **Phone perf**, now four ults deep: v21 §3 + Crucible + Daybreak's spark
   field + Slagburst's ≤9 shards + Ironbloom's 0.8s freeze and 9 splinters.
4. **The name "Slagburst"** was the patch author's pick, not an interview
   answer. One constant in `ultember_build.py`.
5. **Next ult: Lightkeeper**, per the Slagburst notes — bottom of the field
   in both seed sets, and `Bulwark`'s contribution cannot be separated from
   zero at 2250 paired games.
6. **21 free cells** on the shape × school grid; chain generalised.
