# v68 — THE VERDANT FLAIL, THE 35TH CELL. IN PROGRESS — DO NOT BUILD.

**Cowork, claimed 2026-09-26 06:17 UTC. Designed end to end by Cowork** — Rick,
2026-09-25: *"how do you feel about designing the rest of the fighters
yourself?"* and, asked which of the seven inputs he wanted to keep, *"Nothing —
you run it all."* So this file carries the cell, the §1, the rulings, both
names, the card, and the animation and sound specs, and Rick vetoes the cell
after reading it. It is written as the design goes, not at the close. Claimed
in `06-docs/CLAIMS.md`. Code: do not build from this until the header says
DESIGNED and a `BUILD-BRIEF.md` sits beside it.

**Open cells first, then the redesigns** — Rick's ordering, 2026-09-25, when
he asked whether the old fighters could be brought up to the new standard.
The redesign list (v59's feed table plus the v5-era kinds) is at the bottom.

---

## Why this cell

Eight cells were open at `sc-trunk` (34 relics, the minute pace) and all eight
were re-priced this session with `cell_ults_on.py` — 4 arms, 33 foes × 10
seeds = 330 fights an arm, Chromium 141, `06-docs/v68/runs/open8_trunk.txt`.
**The reproduction control ran first and could have failed**: the same tool on
`sc-ravelbone.html` for vigil × twinblade returns **33.1% / +47.9pp / 10.7% /
+45.5pp**, v62's table to the decimal.

```
cell                      FIELD ULTS OFF          FIELD ULTS ON        body, ults on
                         floor     lift          floor     lift        (floor + lift)
dwarven x twinblade      36.1%   +40.3pp          9.7%   +23.9pp         33.6%
sanctified x twinblade   36.1%   +33.3pp          9.7%   +20.6pp         30.3%
runic x bow              35.8%   +24.5pp         13.0%   +20.6pp         33.6%
vigil x flail            16.7%   +36.1pp          3.6%   +23.6pp         27.2%
runic x warhammer        36.7%   +13.6pp         13.6%    +9.1pp         22.7%
verdant x warhammer      36.7%    +7.3pp         13.6%    +2.1pp         15.7%
sanctified x flail       16.7%   +12.7pp          3.6%    +3.3pp          6.9%
VERDANT x FLAIL          16.7%    +7.3pp          3.6%    +3.3pp          6.9%
```

Three things the table says, in order of weight:

1. **A flail with no ultimate wins 3.6% of fights in this field.** The minute
   pace and 33 live ultimates have moved the floors a long way from v62's
   table (the flail floor was 7.2% ults-on at 30 relics on the 48s clock) —
   which is why this was re-measured rather than read off v62.
2. **Entangle on a flail is worth +3.3pp with the field's ultimates on.** v59
   §3.1's contact-rate law, again: the flail lands a blow every ~6.6s and
   entangle is gone in 2.8. The channel does nothing on this weapon unless
   something else applies it.
3. So on this cell **the ultimate is the entire fighter** — it has ~43 points
   to carry and the blade can go UP to help it (flails run 24–42.5). That is
   the opposite of the Arclight trap (a body already at 57% before design).
   It is also the type with three empty cells, so what is learned here is
   reused twice, and the school with the weakest set of ultimates on v59's
   feed table (Rootfast +3.4, The Winnowing +4.8, Bramblesnare +7.2).

The two twinblade cells and the runic bow start at 30–34% with no ultimate
and would repeat v64's problem. The vigil flail is v59 §3's "most spoken-for"
cell on a fourth vigil ultimate. The warhammer cells are second choices on the
same reasoning as this one and are next.

## What the cell is made of — from the repo

**The flail** (v43 survey, confirmed in `sc-trunk`'s chain tick): a 44-unit
haft turning with the weapon and a chain hung off its tip whose head has its
own angle and angular velocity — a spring toward the facing, a pendulum under
gravity, centrifugal extension. **The head is the weapon and it is 13.2 units
long**: `bladeSegments` returns one stub `width × 0.6` around the head, so the
type covers the most ground of any (the head roams out to ~119) and is live in
the least of it. Contacts/s 0.152, the lowest; 25–42.5 damage a blow, the
highest; mass 3.6. Row: Threshmaw / Bloodmill (winds up, throws spikes),
Slagheart / Ironbloom (latches, bursts), Paradox / Stasis Field (rings itself,
freezes), Gravemourn / Revenant (chain ×1.35, hands). **`f.reachMul` already
exists at seven read sites and grows the chain live** — Revenant's line.

**Verdant** — entangle: `{maxStacks 4, dur 2.8, spin −0.13, move −0.06}`,
applied 2 a blow. Ultimates: Bramblesnare and Rootfast root (a true stun, 1.6s
/ 1.3s — one ultimate with two names), Thicket looses seeds that root at a
wall and lash, The Winnowing's kunai grow on every bounce. The school's verbs
are ROOT and GROW.

## §1 — THE MECHANIC, IN PLAIN WORDS (Cowork's, 2026-09-26)

> For a duration the whole chain becomes a living thorned vine. Anywhere the
> vine touches the enemy it bites — a small hit that leaves entangle — and it
> keeps biting for as long as it stays on them. Every bite makes the vine grow
> longer, so the more it catches the further it reaches, until it is whipping
> across half the hall. The head is still a flail head and still hits like
> one. When the duration ends the vine withers, and the thorns it left in the
> enemy take root: the enemy is held where it stands for a moment for every
> entangle stack it is carrying.

Read as written, four clauses:

1. **The whole chain is live for the window.** The 13-unit stub becomes the
   pivot-to-head span, ~52 units at full extension and growing — the type's
   own weakness inverted, which is the same move Breach made for the scythe
   (already through the wall) and Ravelbone for the hold.
2. **A vine touch is a bite: small damage + 1 entangle, on its own cooldown**,
   not a blade blow through `resolveHit`. Bloodletting's discs and Corona's
   ring are the precedents: a hazard that ticks. The head's own blow is
   unchanged. **This is the feed** — v59 §2's column says the ultimates that
   pay are the ones that put the school's status on the foe continuously, and
   on this weapon the status is worth nothing until something does.
3. **Growth: each bite lengthens the chain** (`reachMul += g`, capped), so a
   vine that keeps catching reaches further — The Winnowing's rule on the
   weapon itself.
4. **The finale is a root**: when the window closes, the foe is pinned
   (ball AND weapon — `f.pin`, which `tickStasis` turns into a weapon lock)
   for `rootPer × stacks`. The school's other verb, spent once, sized by how
   well the window went.

Clauses 2–3 pull together (more bites → longer vine → more bites). Clause 4
is a second payoff on one ultimate and v64's lesson 2 says two payoffs can
be substitutes — so it is priced as its own arm and kept only if it adds.

*(sections below are written as they are measured)*
