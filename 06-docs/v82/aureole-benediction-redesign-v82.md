# v82 — AUREOLE / BENEDICTION, REDESIGNED. A halo stands around her: a foe inside it is smitten, and she is blessed for as long as one is. The beam that hit for 15 and healed 28 was a lump of both.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0);
claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab:
`overlays/halo.js`; runs in `06-docs/v82/runs/`.

## Why

`kind:"beam"`: 15 damage, heals 28, once — feed +6.2. Aureole IS a halo; the
beam was borrowed from Bloodprice's shape. The school's verbs are LIGHT and
HEAL, delivered continuously (Zenith, Consecration, Ascension all do; the
beam does neither).

# 1. §1 (Cowork)

> For a duration a halo of light stands around Aureole, wide enough to
> reach half the hall. An enemy inside the halo is smitten for as long as
> it stays there — and for as long as an enemy is inside it, Aureole is
> blessed.

Two clauses: the halo (r 150, on the caster); smite inside (**the feed**);
the blessing tied to the foe being inside (Zenith's rule — the heal is
earned by the mechanic touching the foe, not by standing there).

# 2. THE HARNESS, AND THE CONTROL

Aureole as shipped on `sc-trunk`, Chromium 141. **SHIP 55.5% (330), A 27.9%
— Benediction is worth +27.6 and the bar is high.**

# 3. PRICED (`runs/halo_base`)

```
arm                                            win    casts  foe inside  smite/cast  bless/cast  foe stk
A   no ultimate                               27.9%
SHIP the beam                                 55.5%
B   smite inside the halo                     49.7%    2.88    36%         7.7          —         3.47
C   + blessing while a foe is inside          69.4%    3.08    36%         7.9         5.8        3.47
D   + arrows through the halo smite +1        70.6%    3.06    36%         7.9         5.8        3.51
```

The foe is inside the halo **36%** of the window — a bow's foe closes in
— and comes out at 3.5 smite. The blessing is +20; blessed arrows are +1
and not taken. **C at 69.4 against a shipped 55.5**: the blade comes from
16.01 to about **14** (the bow row 9.5–16.2), settled wide to the shipped
rate.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND

- The halo is a disc r 150 on the caster's centre; inside = foe centre
  within 150 + R. `foe.apply("smite", 1, f)` every 0.5s inside;
  `f.apply("blessing", 1, f)` every 0.8s while inside. No damage, no
  knock, no beat.
- Names kept: AUREOLE / BENEDICTION. **Card (67):** `A halo: foes inside it
  are smitten, and she is blessed while one is`.
- **Picture** (§4.1b/c applies — sanctified light): a RING, not a disc — a
  10-unit band at r 150 in sanctified `glow`, alpha 0.4, with the hole
  cut in the path; the interior gets a 0.04 wash and nothing under
  `lighter`. The ring brightens (alpha 0.4 → 0.7) while a foe is inside —
  the tell that the blessing is running. Cast: the ring expands from the
  ball over 0.3s; close: it contracts. Bloom gate ≤ +0.02 measured. Field:
  motes drifting inward along the ring, both copies.
- **Sound**: cast — a soft choir swell (two re-struck tones, a fifth),
  0.5s; a foe entering — a single bright note; the blessing — the `spark
  collect` voice reused; close — the swell reversed.

# 5. BUILD BRIEF

Stage 0 control on 151 (`--arms A,SHIP,C`). Stage 1 — beam out, `f.ultHalo`
in, the inside test and the smite; gate: foe inside ~36%, ~7.7 smite a
cast, relic ~50% at 16.01 (arm B). Stage 2 — the blessing; gate: ~5.8
blessing a cast, relic ~69%. Stage 3 — the blade, wide on 151 at 13.5 / 14 /
14.5 to the shipped rate. Stage 4 — picture (bloom measured), voice, carry;
beam's field spec out; `engine_ab`, `shell_identity`, `render_ab`,
`chain_audit`, one fight watched.

# 6. Open decisions

1. Rick's veto. 2. The blade target. 3. Whether a bow's own ARROWS should
interact with the halo at all (D, +1) — no, by the numbers.
