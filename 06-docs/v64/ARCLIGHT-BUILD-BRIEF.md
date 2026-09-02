# ARCLIGHT / STATIC — BUILD BRIEF. THE VIGIL TWINBLADE, THE 34TH RELIC. A PINK LIGHTNING STORM IT GROWS FROM ITS OWN HITS, EATS BACK AS SHIELD, AND DETONATES.

**Cowork, 2026-09-02. FOR CLAUDE CODE. Every decision below is Rick's or is
measured; the measured ones say so and name the tool.** Design record:
`vigil-twinblade-design-v64.md` (the survey, the §1, the pricing, his rulings).
Run outputs in `06-docs/v64/runs/`. Tools: `tools/storm_tracks.py`,
`tools/storm_lab.py` (+2, +3), `tools/storm_price.py`.

Written in stages with a gate after each. **Stop at a gate that fails.** If
anything here cannot be built as written, say so and stop — do not redesign
around it (CLAUDE.md §3 rule 0). Claimed in `06-docs/CLAIMS.md`.

---

# 0. THE RELIC IN ONE TABLE

```
id                arclight
name              ARCLIGHT             Rick, from four
aff               vigil                core #F06BB8 · glow #FFD1EC · dark #4A0A31 · steel #D8B9C9
shape             twinblade            body IDENTICAL to the row: blades:[0,0.5], reach 62, width 8,
                                       artW 30, spin 5.7, mode "spin", mass 1.1
dmg               BISECT (stage 4)     start the sweep at 8.3 (Twinshade, the row's floor) and go DOWN.
                                       Rick, 2026-09-02: "the storm is the fighter" — he accepts the
                                       lightest blade in the game. Expect it under 8.3.
onSelf            { ward: 1 }          the school's channel, exactly as the other four vigil carry it

ult.name          STATIC               Rick, from four
ult.charge        15                   the twinblade row runs 13–18; priced at 15
ult.kind          "static"             new kind; nothing shares it (one sigil, one sound, one picture)
ult.tip           "Hits spawn forking lightning. Caught bolts apply ward. All explode at 8s"
                                       RICK'S OWN LINE, 2026-09-02, 72 chars exactly. One string, both
                                       surfaces. Measure it on both the way Scour's was (§5).

THE STORM — all of it Rick's §1 with his numbers turned up (design §3), and the rulings of 2026-09-02
  window          8.0 s                ONE timer: spawning stops and every bolt detonates at t = 8
  per hit         8 bolts              born AT THE FOE on every blade hit the caster lands inside the window
  bolt radius     16                   fat. Contact = ballR 34 + 16 = 50
  bolt speed      600 px/s             MEASURED FREE (350–800 within noise). Pick for the picture.
  direction       random, seeded       MUST come from the match's own seeded RNG — engine_ab is determinism
  ricochets       6                    a bolt reflects off a wall 6 times; the 7th wall kills it
  on the FOE      fork: +2 MORE bolts  born at the foe in fresh directions; the bolt itself lives on with its
                                       ricochets refreshed to 6. NO DAMAGE. Per-bolt grace 0.30s after
                                       birth or fork so a bolt born on the foe does not fork on the foe.
  on the CASTER   consumed             the bolt is gone; the caster banks 2 WARD through the school's own
                                       channel: shield = min(90, shield + 2), shieldMax kept, apply("ward",1)
                                       (restarts the 5s clock). The ward is fed WHILE THE STORM RUNS.
  cap             60 bolts alive       never binds at these numbers (peak ~30). A safety, not a knob.
  walls only      bolts pass through shots, weapons, clanks — only walls, foe and caster exist to them
  hit-stop        bolts advance by the ordinary step and freeze with everything else

THE DETONATION — at t = 8.0 from the cast
  blast radius    80                   Rick: over his own "small" 50 and over 100. Foe is hit if
                                       dist(bolt, foe) < ballR + 80
  per bolt        15 damage            each bolt inside the radius is one hit of 15 — through the ordinary
                                       damage path (the foe's own ward absorbs first, sunder multiplies,
                                       the vigil channel BANKS 0.55 of it like any blow). No knockback,
                                       no hit-stun — §1 names neither. ONE hit-stop and ONE beat for
                                       the whole detonation, not one per bolt (§3).
  then            every bolt is gone
```

**Priced (design §5, `tools/storm_price.py`, live swarm inside `m.step`, 248
fights an arm, control arm reproduces the no-ult body to the decimal,
Chromium 141.0.7390.37, on `sc-bloodletting.html`, 32 relics):**

```
    A  the body, ward, no ultimate                 56.9%
    B  ward only (eaten bolts bank, no blast)      +16.1pp     ~35 ward a cast
    C  detonation only (bolts bank nothing)        +25.0pp     ~60 damage a cast, 18% of casts nothing
    D  the whole of STATIC                         +33.1pp     on a body already at 57% — near the ceiling
```

**Both halves are real and the feed is the school's first** — Aegis reflects
the shield, Reprisal fires it, Sentinel drinks it; Static PAYS INTO it.
The model's detonation goes through `m.hurt` and skips `resolveHit`'s
multipliers; the built one will price differently. Gate 6 writes the gap down.

**What the cast looks like, per cast (live run):** ~2.5 blade hits inside the
window → ~17 bolts born → ~30 forks → ~21 eaten by the caster → ~24 alive at
the detonation → ~4 inside the blast. **8–12% of casts see no blade hit in
the window and produce nothing.** That is the mechanic — a storm needs a
spark — and Code must NOT add a fallback spawn.

---

# 1. WHAT THIS CELL IS, SO THE BLADE NUMBER DOES NOT SURPRISE ANYONE

`budget-v59.md` §3: ward is the most weapon-speed-sensitive status in the game
and the twinblade is the fastest weapon, so this body wins **57–60% with no
ultimate at all** (design §1, two seed blocks). Static adds ~33 on top. To land
in the field the blade gives back ~40 points, which puts it under every
twinblade and probably under every blade in the game. **Rick has ruled that
this is the fighter he wants.** Do not soften the storm to save the blade; do
not stop the sweep at 8.3 because it "looks too low."

---

# 2. STAGES AND GATES

## STAGE 1 — THE RELIC, ULT STUBBED. `02-chain/sc-arclight.html`

Add the weapon with `ult` present and `kind: "static"` wired to a no-op cast
(a banner and nothing else) so the charge clock and the ult bar behave. Blade
at **8.3** for now. Art: **the vigil twinblade silhouette** — the row's outline
in vigil's palette. **Film it and show Rick a strip before stage 2** (CLAUDE.md
§4.0; `_whEaten` and `_scEaten` were both rejected on sight after they were
built). A twinblade's whole outline is 30 units of artW; keep any lightning
motif ON the closed path, not layered behind it (v58's rule).

**GATE 1.** `engine_ab` byte-identical on every existing pairing at that
build; `verify` unchanged; the new relic's no-ult win rate against the roster
with their ultimates live near **57–60%** (`storm_price.py --arms A` is exactly
this measurement at blade 11.95; at 8.3 expect a few points under). If it
lands near 10% the ward channel is not wired; if near 80% something fires
that should not.

## STAGE 2 — THE STORM EXISTS. NO WARD, NO DAMAGE.

On cast: `Match.storm = { src, t, dur: 8, bolts: [] }`. Each blade hit the
caster lands while `storm` stands spawns 8 bolts at the foe. Bolts move,
reflect, die on the 7th wall, fork on the foe (+2, refresh), vanish on the
caster. At `t >= dur` the swarm is cleared (no damage yet). Directions from
the match RNG. Cap 60. `ultFx` for the set-piece, `ULTSIG.arclight`, a banner.

**GATE 2.** Instrument the cast and print per-cast means over ~90 fights
(3 seeds × the roster): **spawned ~17–20, forked ~30, eaten ~21, alive at the
end ~24, peak ~30, cap never reached.** These are `storm_price.py`'s live
counts (`runs/storm_price_loud8.json`); a build within ~25% of them is the
same swarm. **A build that shows ~7 peak has fork +1 or thin bolts — stop.**
`engine_ab` identical on every OTHER pairing (the storm must not touch fights
it is not in). Film 3 casts on 3 seeds before tuning: the arena should read
as full of pink lightning by the 4th second of the cast.

## STAGE 3 — THE WARD AND THE DETONATION. THIS IS THE RELIC.

- Eaten bolt → `self.shield = min(STATUS.ward.cap, self.shield + 2)`;
  `shieldMax = max(shieldMax, shield)`; `self.apply("ward", 1)`; the float and
  tag the channel already prints for a bank (`resolveHit`'s vigil branch is
  the reference — same fields, same order, and the Aegis branch shows what
  "feed while it stands" looks like when a wall is up. If Arclight ever gets
  an Aegis-like wall this bank must go to it; it does not today).
- At `t >= dur`: count bolts with `dist(bolt, foe) < ballR + 80`; each is one
  hit of 15 through the ordinary damage path with `mul` semantics like a
  projectile (crit/jitter as the engine does for shots), no knockback, no
  hit-stun. **One** hit-stop, **one** beat (`cinePlan` needs to know this is
  the legible moment — rule 3, every relic since Vesper), one sound. Then
  `storm = null`.
- If the foe is dead or the caster is dead at the detonation, nothing fires.

**GATE 3.** Re-run the four-arm budget shape on the built relic (port
`storm_price.py`'s A/B/C/D toggles to the builder's probe — the toggles are
`bank` → 0 and `dmg` → 0): **B − A in the +16 tier, C − A in the +25 tier,
D − A in the +33 tier, each ±6pp at 250 fights.** Ward per cast ~35, damage per
cast ~60, casts with zero detonation damage ~18%. A D − A over +45 or under
+20 is a different relic — stop and say what changed.

## STAGE 4 — THE BLADE. BISECT DOWN FROM 8.3.

The usual sweep to the field band. **Go down from 8.3, not up**, and do not
stop at the row's floor. Write the crossing and the number Rick gets. Expect
the lightest blade in the game; that is ruled.

**GATE 4.** Shipped win rate in the field band; spread across the roster
reported (this relic will have a wide one — ward is worth nothing against DoT
schools and everything against burst); `verify` green; `engine_ab` identical
on every other pairing.

## STAGE 5 — ART, SOUND, BEAT. RICK'S, RENDERED AS SPREADS.

- **The bolt.** Pink lightning, fat (r 16 is the HIT volume; draw it as a
  jagged segment with a glow, not a 32px ball). Render a strip of 3–4 bolt
  styles at arena scale and show Rick — he has not chosen the look.
- **The fork.** The one moment that explains the mechanic: one bolt touches
  the foe and three leave. Make the foe flash the school colour on a fork.
- **The eat.** A bolt reaching the caster should visibly go INTO the shell
  and the ward float should print — that is the "harvest" half of the fighter
  and it is otherwise invisible.
- **The detonation.** Every bolt pops at once; the ones near the foe are the
  hits. One shake, one hit-stop.
- **Sound.** No preference from Rick; render a spread as for Scour.
- **The card / scrunch line.** Rick's (§5). `verify` enforces ≤72.

## STAGE 6 — THE REAL PRICE

`ult_price`-style on the built relic at the shipped blade, and the four-arm
shape again. Write the gap between the model's +33 and the built number into
`arclight-build-v64.md`, with the reason if it is over 8pp.

---

# 3. THE TRAPS, NAMED BEFORE THEY BITE

1. **`Math.random` anywhere in the storm breaks `engine_ab`.** Bolt directions
   come from the match's seeded RNG. This is the first thing to check.
2. **A bolt born on the foe forks on the foe.** The 0.30s grace exists for
   this; without it every spawn is an instant fork chain and the cap binds on
   the first hit. The overlay showed exactly that before the grace went in.
3. **A bolt born on the foe flies into the caster.** A third of all bolts are
   eaten within half a second of birth (design §2). That is the mechanic —
   the caster is in melee range — not a bug to fix with a spawn offset.
4. **Fork +1 is not fork +2.** "Fork into two more" is literal: the bolt
   survives AND two are born. +1 gives a swarm that never grows (peak 7).
5. **Ricochets refresh on a fork.** Without the refresh the swarm dies on the
   walls by the 6th second.
6. **The detonation is one event.** 24 bolts popping must not file 24 beats,
   24 hit-stops, or 24 sounds. `hurt` per bolt is fine; presentation once.
7. **The ward the storm banks goes UNDER the 90 cap** with the blade's own
   banking. At 2/bolt and ~21 eaten a cast, ~35 lands and ~2 is lost to the
   cap (overlay `w.cap` column). Do not raise the cap for this relic.
8. **`w.aff` is inert** (v59 §4) — the school lives in `onSelf`, the palette
   in `AFFINITIES`. Set both anyway.
9. **The no-ult floor of this body is ~57%, not ~10%.** `cell_ults_on`'s 10.7%
   is the body with NO channel; with the ward it is 56%. Gate 1 uses the
   latter.

---

# 4. WHAT IS RICK'S AND STILL OPEN

Of his seven: cell ✓, mechanics ✓ (with the three rulings of 2026-09-02),
fighter name ✓ Arclight, ult name ✓ Static, card line ✓ (§5). **Open: the
bolt art, the sound.** Both are rendered spreads (stage 5) — do not ask him
in words.

# 5. THE CARD LINE — RICK'S

```
Hits spawn forking lightning. Caught bolts apply ward. All explode at 8s        72
```

His. He wrote "Hits spawn forking lightning. Bolts hitting #name# apply ward.
bolts explode after X seconds" (94 filled in), was shown the 72 cap, called the
first trim's middle sentence "pretty rough", and took this middle from four.
Every word but "caught" is his. **Measure it on the ult-bar reminder (390px at
18px Atkinson Next) and the scrunch panel at 21px before stage 5 closes**, the
way Scour's line was; it is exactly at the cap.
