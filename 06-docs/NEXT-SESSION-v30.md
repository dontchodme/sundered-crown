# Next session — v30

**2026-08-18.** The session that added the eighteenth relic and merged two
incoming patches into one chain. Everything below is on
`02-chain/sc-health18.html` **`b57041681d7ee45b`**.

`01-live/sundered-crown.html` `51c9bf566f9eb679` **untouched.**

---

# 0. The one command

```
cd tools
python3 shatter_build.py   --src ../02-chain/sc-cardspin.html         --out ../02-chain/sc-shatter.html
python3 lastlight_build.py --src ../02-chain/sc-shatter.html          --out sc-shatter-lastlight.html
python3 health_build.py    --src ../02-chain/sc-shatter-lastlight.html --out ../02-chain/sc-health18.html
```

Three builders, one order, and the order is forced — `health_build.py` exits if
any relic has no ult sigil, so it must run after the relic that needs one.

# 1. What is in the tip that was not in v27

**LASTLIGHT** — the sanctified scythe, eighteenth relic, first free cell of the
6x7 grid filled since the four greatswords. Rick's design: the ultimate sprays
twelve mini scythes radially; they latch into the quarry and weigh it down;
after 2.4s they all burst at once, scaling on how many stuck, leaving
Daybreak's own sparks. Blade tuned to 17.5 (measured, not derived — the
placeholder sat at 71.0%). Full record: `06-docs/LASTLIGHT-NOTES.md`.

**AXIOM v3, the shatter** — the runic greatsword as a 2-D fracture, 10 pieces.
Incoming patch, composed unchanged. `06-docs/README-SHATTER-PATCH.md`.

**THE HEALTH HUD** — gauge on the shell, lifeline above the hall, four stage
chunks with the third on `CONFIG.desperation.at`, a bespoke ult sigil per
relic, Atkinson Hyperlegible embedded. Incoming patch, composed, plus one new
sigil written for Lastlight. `06-docs/health/APPLY-ME.md`.

The merge itself, including the one incoming claim that did not survive:
`06-docs/MERGE-v30.md`.

# 2. NEXT SESSION'S JOB

1. **Watch it, at phone size, with sound** — and then decide items 2 and 3 of
   `06-docs/MERGE-v30.md` §7. Three sessions have now asked whether
   `sc-cardspin.html` is still the tip of record; this build makes it a bigger
   question, not a smaller one.
2. **Perf on real hardware.** This tip adds the HUD (+2.2% by ratio in a
   GPU-less box) AND art that micro-benchmarks at ~2.5x the shipped weapon,
   and neither number means anything here. `bench_build.py` on the machine, or
   `03-bench/` on a handset. The budget is ~6 ms at 165 Hz and has never once
   been measured against any of the last four sessions' work.
3. **Shorts on the new tip.** The whole week-one pipeline films `sc-cardspin`;
   nothing has been shot on this. Lastlight v Axiom is the pairing that shows
   all three changes at once.

# 3. The Harrowing pattern, for the next ult

Cast resolves NOTHING and throws objects · the objects are `shots`, so they are
clankable, bouncing and missable like everything else · payoff on a single
shared fuse, on the CASTER, so the director gets one peak · everything about
the payoff scales on a count the viewer can see on screen · a debuff that is
physics (mass, drag) rather than a status, when the status that fits belongs to
another school · reuse the actual function, not a copy of it (`spawnSpark` reads
its numbers off `f.w.ult`, so Lastlight's sparks ARE Daybreak's) · the dud case
kept, made visible, and MEASURED rather than designed away.

# 4. Still open, carried

sc-scflip decision · 24 free grid cells (twinblade 5, warhammer 5, scythe 5,
flail 5, bow 4) · `o.dark` · Nightfell silhouette · same-type tape ties ·
render.py wall-time audio port · cinema director's unretracted 21.85ms phone
regression · fireUlt life-table `grudgebearer: 1.7` shadowed by the forge
branch · `cineScore` still cannot film an ultimate (the Harrowing is the best
candidate yet — one bloom, one spike, a countable object) · the HUD spill ·
shorts 1-4 live only in the v23 seed · **a 2-D fracture has no probe** ·
**nothing spends Smite** — sanctified is now five appliers and no drain ·
kokoro models are not in this seed (`tools/FETCH-KOKORO.md`).
