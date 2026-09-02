# v63 — CURSE KEEPS THE LAST 3 HITS INSTEAD OF THE 3 BIGGEST. RICK'S RULING, 2026-09-02. ITS OWN COMMIT, AND NOT UNTIL GLOAMWIRE IS IN A LINK.

**Cowork, 2026-09-02. DESIGNED. NOT TO LAND YET.** Rick proposed this on
2026-09-01 (v62 §13), it was measured that day (v62 §13–§16) and again on
2026-09-02 with the donor's ultimate stubbed (`duskreave-check-v63.md`), and he
ruled it in — with the timing condition above, and knowing what it costs
Duskreave. This note is the design; the numbers live in the two files named.

---

# 1. THE RULE

Today (`Fighter.pushCurse`, `sc-garrote.html` 6696–6701): push `n` copies of
the memory, **sort descending, truncate to 3.** The pool converges on the three
biggest blows ever landed on this fighter, for the whole fight (`dur` 99).

Ruled: push `n` copies, **drop the OLDEST until the length is 3.** The pool is
the three most recent blows, whatever their size.

```js
pushCurse(v, n){
  for (let i = 0; i < n; i++) this.cursePool.push(v);
  while (this.cursePool.length > STATUS.curse.maxStacks) this.cursePool.shift();
}
```

That is the whole change. `curseSum`, `curseEcho`, `apply` (which derives the
stack count from the pool's length), the echo at `resolveHit` 10812, the tag
that prints `curseSum()`, Revenant's `cursePool.length = 0` and Deadfall's
read-only `curseSum()` all keep working unchanged. **The tooltip Rick wrote —
"Hits reflect 8% of the damage that cursed, stacks 3 times" — is still true
under the window and does not need to change.**

`tools/curse_fifo.py` and `tornado_fifo.py` install exactly this at runtime and
are the reference for the shape.

---

# 2. WHAT IT DOES, MEASURED

**Nearly nothing to the shipped game** (v62 §13a–b, 320–350 fights an arm):
pools drop 5–12% across every weapon type because consecutive blows from one
weapon are similar in size; the spread across weapons goes 3.4x → 3.0x; the
four built umbral relics move **−2.6 / −4.6 / −4.0 / +0.0** (Gravemourn,
Nightfell, Twinshade, Shroudmaul — the last is the control, pool-independent by
Rick's ruling, and it moved by exactly nothing).

**A quarter of Duskreave's damage** (v63 §3 and the fifo re-run, 986 fights an
arm, donor ult off): Scour's echo halves, 113 → 49 a fight; **+59.2pp becomes
+40.5pp.** The reason is v62 §16 in four lines: `shift()` drops the oldest and
not the smallest, so every tornado tick that applies curse trades one of the
scythe's 35-damage memories for a 5. Rick was shown this and ruled: **"last-3
goes in; Scour lands at ~+40."**

**It is not monotone** (v62 §16, `push_monotone.py`): under the shipped rule
applying curse can only help or do nothing; under the window it can lower the
pool by 45 in one push. That is a property, not a bug, and it is the reason
the window is a design change and not a tuning change.

---

# 3. WHEN AND HOW IT LANDS

- **After `sc-crossweave.html` (or its successor) is the build of record.** Not
  under it. CLAIMS.md shows Gloamwire BUILDING; a rule change beneath a live
  build is the collision shape v60/v61 already paid for.
- **Its own link, its own commit, its own claim** (already in CLAIMS.md).
- **Gate:** re-run `ult_price.py` on the four built umbral relics and on
  Duskreave if it is built by then; confirm the four land within the error bar
  of the numbers above and Duskreave near +40; `engine_ab` must DIFFER on every
  pairing that involves curse and be identical on every pairing that does not
  (a rule change that leaves the curse pairings byte-identical did not go in).
- **Write** `06-docs/v63/curse-window-build-v63.md` and update CLAUDE.md §0
  and the curse paragraph in §4.

---

# Open decisions

1. **ORDER RELATIVE TO DUSKREAVE'S BUILD.** Either order is accepted by Rick.
   If Duskreave is built first, its gate 6 prices it under the old rule and
   this note's gate re-prices it under the new one.
2. **WHETHER THE STATUS TAG SHOULD SHOW THE POOL FALLING.** Under the window
   `CURSE 96` can be followed by `CURSE 40` on the next blow. Today's tag
   prints `curseSum()` and would show that honestly. Nothing to decide unless
   Rick dislikes the picture when he sees it.
