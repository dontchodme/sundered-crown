# SCRUNCH — THE LIVE PATCH.  `07-live-patch/`

**2026-08-19.** Built by `tools/scrunch_build.py`. **`01-live` is untouched** —
both artifacts are STAGED, not applied. Applying is one copy, and it is Rick's.

```
01-live/sc-playable.html      710b5fd95d877e61
  -> 07-live-patch/sc-playable-scrunch.html      dafddc51096ca2e4   (+14,579 B)

01-live/sundered-crown.html   51c9bf566f9eb679
  -> 07-live-patch/sundered-crown-scrunch.html   71f2b2a3e6870365   (+14,579 B)
```

The artifact is **generated, never hand-edited**. To change anything in it,
change the builder and rebuild, or the live page drifts out of the file that
was checked.

```
python3 tools/scrunch_build.py \
  --src ../01-live/sc-playable.html \
  --out ../07-live-patch/sc-playable-scrunch.html --k 0.70
```

## APPLY

```
cp 01-live/sc-playable.html      01-live/sc-playable.PRE-SCRUNCH.html
cp 01-live/sundered-crown.html   01-live/sundered-crown.PRE-SCRUNCH.html
cp 07-live-patch/sc-playable-scrunch.html     01-live/sc-playable.html
cp 07-live-patch/sundered-crown-scrunch.html  01-live/sundered-crown.html
```

## ROLLBACK

Restore the two `.PRE-SCRUNCH.html` copies, or re-download the seed. Nothing
else in the tree changes, and the patch adds no external dependency — no fonts,
no assets, no network.

---

# WHAT IT DOES IN THE LIVE PAGE

On the first clank the hall scales to **0.70** over 0.42s, holds 3.0s, and
scales back. The freed strip carries a two-column legend — for each relic, its
on-hit status and its ultimate, with the real effect text and the cooldown. At
the kill the hall scrunches again and the strip carries the verdict, with the
winning HP at 92px. **The simulation is never paused**; the old fight card
froze it for 4.0 seconds.

**A `Scrunch` button is added to the button bar**, beside `Intro card`, because
the live page keeps every feature A/B-able in two clicks and this one replaces
the thing that button toggles. It flips `CONFIG.scrunch.on` and re-arms the
running match.

# WHAT THE PATCH DOES *NOT* DO

**It does not bring `01-live` up to the chain tip, and the gap is wider than it
looks.** Measured, not assumed:

```
                       01-live          02-chain tip (sc-cardspin)
roster                 16 relics        17 relics  (Slagheart is chain-only)
_introFacts/_introWrap  absent          present
Emberedge's ultimate   FORGEFALL        SLAGBURST
```

The panel therefore reads **the live build's own data** — on live it prints
`FORGEFALL · Nova: 17 damage, 4 Sunder, short knockback`, and on the chain it
prints `SLAGBURST`. That is correct behaviour and it is also the clearest
possible demonstration that live and the chain are different games right now.
Promoting the chain tip to live is v27 open decision 1 and is **still open**;
this patch neither does it nor depends on it.

Because those helpers are absent on live, the panel composes its own facts
(`_scrunchFacts` / `_scrunchWrap`) instead of calling `_introFacts` /
`_introWrap`. The **strings** still come from the one source — `STATUS[].tip`,
`relicStatus()`, `w.ult.tip`, `w.ult.charge` — so they cannot drift; only the
composition is duplicated, and the panel is its own surface with its own layout.

# THE CHECKS — 13/13 ON ALL FOUR BUILDS

`tools/scrunch_probe.py <base> <patched>`, run against every pair:

```
sc-cardspin -> sc-scrunch          ALL PASS
sc-health   -> sc-healthscrunch    ALL PASS
sc-playable -> sc-playable-scrunch ALL PASS
sundered-crown -> ...-scrunch      ALL PASS
```

The two that carry the argument:

```
[1]  engine_ab: 72 matches simulate identically, base vs patched — on all four
[2a] CONTROL: with the CARD up, 3s of stepping moves the clock 0.0000s
[2b] with the SCRUNCH up, 3s of stepping moves the clock 3.0000s
```

`[4b]` reads `aw` and `pad` back after a scrunched draw and requires the design
values exactly (1056 / 12). The whole mechanism is mutating four layout fields
for the duration of one draw; if they ever leaked, the next frame would compound.

# TWO THINGS THE LIVE BUILD TAUGHT THE PROBE

**(a) A hardcoded pairing that does not exist on live.** The probe asked for
`slagheart v lightkeeper` and 01-live threw `Unknown relic id`. It now derives
its pairs from the roster the two builds SHARE, so it cannot fail this way again
on any point in the chain.

**(b) `01-live` does not render deterministically, and that predates this patch.**
Drawing the identical match state twice differs by **0.697** on the UNPATCHED
`sc-playable.html` whenever `m.shake` is non-zero, against **0.000** on the
chain tip — because `draw()` feeds `Math.random()` straight into the shake
offset. This is v26 §4's open item (*"worth a seeded rng for shake and the SFX
noise buffer if renders are ever expected to be reproducible"*), found again
here. The probe now zeroes `m.shake` before its image comparisons so it measures
the hall rather than the RNG. **Nothing was changed in the build to make a check
pass.**

# Open decisions

1. **Apply, or wait for the chain tip?** Applying puts the scrunch on a
   16-relic build with the old ult tuning. The alternative is promoting
   `sc-cardspin` (or `sc-health`) to live first and patching that — which is a
   bigger, older decision this patch has no opinion on.
2. **Does `01-live` want the verdict beat at all?** In the live page a match
   ends and the next one is one click away; the 999s hold that keeps the verdict
   panel up for a video may be wrong for a session where you just want to hit
   Fight again.
3. **The `Scrunch` button starts ON.** If live should default to the old card
   until the read is in, that is `CONFIG.scrunch.on = false` and one line.
4. **`BAND.pos` is load-bearing for two features** (v34 §8). Not a live concern
   yet — `01-live` has no `BAND` — but it will be if the health rework lands
   there.
5. **Seeded RNG for shake** — (b) above. Not this patch's job, but it is now
   measured twice and it blocks any future frame-exact regression test.
