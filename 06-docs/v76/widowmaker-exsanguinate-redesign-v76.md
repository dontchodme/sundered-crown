# v76 — WIDOWMAKER / EXSANGUINATE, REDESIGNED. The bleed drains into her. The nova was the worst feed in the game; the name always meant this.

**DESIGNED — Cowork, 2026-09-26. The first of the redesigns (Rick, 2026-09-25:
open cells first, then the old fighters to the standard). Build from §5 of
this file; do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick
vetoes from this file.** Lab: `overlays/drain.js`; runs in `06-docs/v76/runs/`.

## Why this one first

v59 §2's feed column: **Exsanguinate is −6.7, the worst in the game** — a
nova that applies three Hemorrhage in a burst, and Widowmaker's bleed is
worth MORE with the ultimate switched off, because the ultimate spends time
not swinging. It is a v5 one-liner (`kind:"nova"`) on Rick's own first
roster. Bloodsworn's four other ultimates all shoot something (Bloodmill,
Bloodhunt, Bloodprice, Garrote's wire, Bloodletting's effigies); the school
has never DRAINED, and *exsanguinate* means to drain of blood.

# 1. §1 (Cowork)

> For a duration the enemy's bleeding drains into Widowmaker. Every tick of
> Hemorrhage on the enemy heals her by the same amount. Her blades are
> unchanged; the wound does the work.

One clause. The feed is the school's own status made to pay twice.

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py` on `sc-trunk`, Widowmaker AS SHIPPED (a redesign: `--cell`
omitted; arm `SHIP` leaves the nova live, `A` suppresses it). Chromium 141,
330 / 660 fights an arm. **The control is the shipped relic itself: SHIP
reads 46.3% (660), against `verify`'s band for Widowmaker on the build of
record.** The drain reads the engine's own hemorrhage tick (`dps × stacks ×
dt × dmgTakenMul`) and heals `hp` by it, capped at `maxHp`.

# 3. THE DRAIN, PRICED (`runs/drain_base`, `drain_full`)

```
arm                                         win (660)   casts  drained/cast  foe bleed on a window frame
A   no ultimate                              37.1%
SHIP the nova as shipped                     46.3%                                 (+9.2)
B   the drain (1.0 x the tick)               57.1%      3.71     24.4 hp           2.23
C   lifesteal on blows only (0.35)           50.0%*                                       * 330
D   drain + lifesteal                        66.7%*
```

**+20 for the drain alone — 24 hp a cast, two and a half times the nova's
worth — from an ultimate that adds no damage and no new object.** Lifesteal
is Triplicate's (umbral) and is not taken. The nova's +9 is replaced by a
+20 and the blade pays the difference:

```
blade    drain (B)
 11.95    57.1%
 11.0     51.5%
 10.5     45.9%    <- the shipped relic's 46
```

**Blade ~10.6–10.8** (the twinblade row: 8.3–11.95). The build settles it
wide on 151 to the SHIPPED win rate, not to 50 — a redesign keeps the
fighter where it was.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND

- The drain is in `tickStatus`'s dps branch: when `key === "hemorrhage"`,
  `st.src` has `ultDrain`, and `src !== f`: `src.hp = min(src.maxHp, src.hp
  + d)`. Corona's `feed` plumbing (status carries `src`) already exists —
  hemorrhage needs its `src` written by `apply` (it is, since v66).
- **Names kept**: WIDOWMAKER is Rick's, EXSANGUINATE now means what it says.
- **Card (≤72):** `Her foe's bleeding drains into her: every tick of it heals her`
  (66).
- **Picture**: the nova art is retired. Cast: her shell flushes dark red for
  0.25s and a thin red thread appears from the foe's bleed drips to her
  shell for as long as the foe bleeds inside the window — the "drains into
  her" line (Zenith's heal thread, in blood). Blessing is NOT used (this is
  hp, not a status); a red "+n" floats on her every 1 hp drained (not per
  tick — `hurt`'s rounding rule). Close: the thread snaps. No new object.
- **Sound**: cast — a low inhale, 0.4s; the drain — the bleed's own drip
  voice reversed and pitched by the foe's stack count, quiet; close —
  nothing.
- No damage change, no knock, no stun; the nova's `radius` and `apply` are
  deleted.

# 5. BUILD BRIEF

Stage 0 — control: `ult_overlay.py --relic widowmaker --mech
overlays/drain.js --arms A,SHIP,B --seeds 20` on 151: SHIP ~46, B ~57 at
11.95. **Stage 1** — the nova out, `f.ultDrain` in, `tickStatus`'s branch;
gate: engine_ab on the 41 others, ~24 hp drained a cast (measured off
`hp` deltas), relic ~57% at 11.95. **Stage 2** — the blade, wide on 151 at
10.5 / 10.75 / 11, target the SHIPPED win rate (~46–50); the card;
tip_audit. **Stage 3** — picture, voice, carry: the thread, the flush, the
float; move nothing in the director (the nova's beat is gone and the drain
files none); field spec REMOVED (the nova's burst spec is dead) — both
copies, sha re-stamped; `shell_identity`, `render_ab`, `chain_audit`, one
fight watched.

# 6. Open decisions

1. Rick's veto — this is his first relic's ultimate.
2. The blade target: the shipped 46 or the band's 50 — Rick's; the build
   assumes 46–50.
3. Whether the drain should ALSO lift her own cap (Bloodletting's 8) — not
   priced; a second payoff on one ultimate (v64 lesson 2) and left out.
