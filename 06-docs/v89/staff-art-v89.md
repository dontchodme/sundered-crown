# v89 — THE STAFF ROW'S ART: concepts, three heads a school on one pole. Rick picks a letter; Code paints it.

**Cowork, 2026-09-27. CONCEPTS — Rick: *"we are also going to art for the
weapons. how about you do concepts and code builds them?"*** The split is
v63's (the moon): Cowork owns the silhouette spread, Rick chooses from the
sheet, Code pastes the chosen spec and gates it pixel-identical to the sheet.

## The sheets

- `05-reference/v89/staff-sheet.png` — all seven schools × A/B/C, at zoom
  and (inset) at the size it ships at on a 1080-wide phone.
- `05-reference/v89/staff-<school>.png` — one school a sheet.
- `06-docs/v89/staff_spec.js` — the spec every candidate was drawn from:
  `STAFF.pole` (shared), one head function a school with the three
  candidates inside it, `STAFF.staff` the dispatcher. **Code pastes this as
  `SHAPES.staff`, sets `STAFF.pick` to Rick's seven letters, deletes the
  losers.** `tools/staff_art_lab.py` re-renders the sheet from it.
- `06-docs/v89/refs/ref-staff-1..6` — Rick's six references (2026-09-27).

## The three cuts

**Cut 1 was wrong and is gone.** It started the staff at the ball's edge
and kept it inside the sim's reach (60), so every one was a stub with a
bead on it — Rick: *"those all look like wands at best."* The bow's own
lesson, re-learned: slim reads as a stick.

**Cut 2 ran the pole THROUGH the ball** — a shod butt out the far side —
for length. Rick: *"staffs should be longer and not stick through the
whole artifact like that."* Gone too.

**Cut 3 is the sheet.** A wizard's staff, from Rick's six references
(`refs/`), and it is these three things:

1. **LONG, OUT ONE SIDE.** The pole starts at the ball's edge and goes out
   to 1.2 sim reaches; the head sits at **1.6–1.9 reaches** (the lab prints
   each). Nothing on the far side of the ball. It is the longest thing on
   any ball in the game — the greatsword reaches 116 from the centre, the
   staff's head ~135.
2. **A THIN, GNARLED POLE.** One closed path with a wobbling width and a
   slight bend, a wrapped grip at the ball, no ferrule. Pole half-width
   0.09 of the head's W (~5 px at ship size).
3. **A BIG HEAD THAT HOLDS SOMETHING.** Four to five pole-widths across
   (the references), up to 0.4 W either side. The thing it holds is the
   school's light and is where the spell leaves from (v89 §1).

**And it is NOT a wand and NOT a sceptre**, because Rick expects both to
become types: *"keep in mind that scepter and wand could become a weapon
type and we need to make sure to differentiate between them."* The rule,
written once so the two later rows have something to be different FROM:

```
              length (in sim reaches)   pole        head                                  held
STAFF         1.6–1.9, the longest      thin, gnarled, wood   big, HOLDS a light (orb, flame, lamp, glyph)   at one end, far from the head
sceptre       ~0.8, short               thick, straight, metal   heavy and ornate, a crown/mace-head, no held light   close, like a mace
wand          ~0.5, the shortest        thin, straight        none — a tip, a tapered point                  in the hand
```

The staff's signature is LENGTH plus a HELD light; a sceptre is short and
its head is solid; a wand is short and has no head. Any staff on this sheet
that could pass for one of the other two at ship size is a defect.
## The twenty-one, by school

```
BLOODWICK    A  a claw of wood holding a blood-glass orb, a flame standing off it
             B  a THISTLE: a spiked calyx and a bloom of blood (ref 1)
             C  two horns curling back, the flame burning between them
NIGHTGLASS   A  a claw holding a black mirror-orb, one violet glint
             B  a scaled SERPENT coiled up the pole and round the glass, its head over it (ref 4)
             C  the moon's jointed pole ending in a black prism
WATCHLIGHT   A  a cage lantern hung from a hook off the pole's end
             B  a hooded lamp, open toward the foe (the beacon looks where it fires)
             C  the ward's plates down the pole, a round lamp in a claw
BRIARWAND    A  the pole forks into a thorned claw holding a green orb
             B  a tendril coils round the head and grips the orb; leaves on the pole
             C  an open five-petal flower about a lit heart
CIPHER       A  an open RING holding an orb, the glyph in the orb (ref 3)
             B  a broken circle — two arcs, the gap toward the foe
             C  a triangle frame, a rune-stone at each corner
CROZIER      A  the CROOK — a gilt spiral with a bead of light in the curl (refs 2, 6)
             B  a sunburst on a finial
             C  a pierced halo held by two prongs (the bow's monstrance)
CULVERIN     A  a bell muzzle flaring off a banded barrel, an ember in the bore
             B  a mortar — a short fat tube strapped to the pole
             C  a hammer-head with the bore drilled through it, the maker's chevron
```

## What Code does with the pick

1. Paste `staff_spec.js` into `SHAPES` as `staff` (+ `STAFF` beside it),
   set `STAFF.pick`, delete the two losers per school. `shape:"staff"` on
   the seven relics. `weaponGlow` needs nothing: it renders whatever the
   shape draws.
2. Gate: `staff_art_lab.py` on the build must be pixel-identical to the
   chosen cells of the sheet Rick picked from (v63's gate). engine_ab
   identical — nothing here touches the sim.
3. Film one, at ship size, spinning. The silhouette question is answered on
   the sheet; the SCALE question (v53) is answered by the inset and the
   clip.

## Open

1. Rick's seven letters — or "none of these" per school, with what is
   missing (the first umbral round took a "none" and a named gap).
2. **THE SIM REACH.** The art's head sits at 1.6–1.9 sim reaches; the
   melee segment the engine tests runs to 1.0 (54, the bow's). So the head
   does not hit — only the pole's first 54 does. Either that is fine (a
   ranged relic lands one or two melee blows a fight; the bow has the same
   gap the other way, its ARROW occupies the reach) or the staff's `reach`
   grows to ~100 to meet the picture, which is a TYPE decision (STAFF-ROW
   §8.3) and re-prices all seven (a longer stick is a better stick up
   close, and the spell spawns at `R + reach` — further out). Rick's.
3. The heads' sizes are one number (`Wq`) and the length one number (`Lq`)
   in `STAFF.staff`; both are taste and both are cheap to move.
