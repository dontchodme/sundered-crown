# v41 — HANDOFF. The twenty-third relic, and the first session that asked all six.

**2026-08-20.** Vigil × warhammer built, refuted twice, rebuilt, tuned, filmed.

```
02-chain/sc-bulwarden.html         <- THE RELIC
02-chain/sc-bulwarden-frame.html   <- THE BUILD OF RECORD
built off 02-chain/sc-vinesower.html
01-live UNTOUCHED, still on sixteen

cell_survey        7/7      the grid on the v40 tip — 20 cells open
wh_survey         23/23     the five open warhammer cells, before the choice
bulwarden_probe   44/44     one check per sentence of §1, plus both refutations
bulwarden_sweep     —       reflect x feed, then floor x dur, blade bisected per cell
engine_ab       2310/2310   IDENTICAL on the other twenty-two
verify.py --n 30  13/13
chain_audit       12/12     every insert survives to the tip
07-shorts/v41/aegis-v-vinesower.mp4   seed 8802, 24.3s, won on 2 hp
```

Read `06-docs/v41/` in this order:

| doc | the headline |
|---|---|
| `sundered-crown-warhammer-survey-v41.md` | **The hammer wins 734 of 734 binds** — and its own 2.3× knockback costs it 16 points of win rate unless the ultimate takes the shove back. Crucible pulls: +7%. Consecration knocks: −17%. |
| `sundered-crown-aegis-design-v41.md` | §1 in Rick's words, and the three forks he settled before anything was built. |
| **`README.md`** | The build. **§4 is the shield guarding the wrong side, §4b is the picture coming apart from the hitbox, §5 is a control that could not express zero.** |

---

# RICK'S THREE RULES FROM v40 STILL STAND, AND HERE IS WHERE THEY LANDED

## 1. THE FIGHT CARD IS DEAD

Nothing shipped with one. Still IN the build — `introcard_build.py` writes it,
`m.introT` is on every Match, the guard in `cinema_clip` is what stops it. v40's
sentence is unchanged: *"die completely" means removing it, and that is a
chain-wide change that wants its own session and its own probe.*

## 2. RICK GIVES INPUT ON SIX THINGS

**v40 asked about two of the six. This session asked about all six**, and every
answer changed the relic:

```
  the ult MECHANICS      §1 in his words, and then a SECOND §1 after the probe
                         refuted the first: "the shield tracks the enemy ball
                         and always tries to face them."
  the ult NAME           Aegis. §1 said Bulwark, which is Lightkeeper's; he
                         left Lightkeeper alone rather than rename a shipped
                         relic across the chain and 01-live.
  the FIGHTER name       Bulwarden, from four offered.
  the SCRUNCH CARD       "Raises a shield that reflects damage blocked" — his
                         words, verbatim, and the FIRST TIME in twenty-three
                         relics this was ever put to him.
  the ult ANIMATIONS     the kite shield ("we are way off base here art wise"),
                         and then the cast set-piece.
  the ult SOUND          the door closing, kept after hearing it in a clip.
```

**Two of those six answers came back as refusals of something I had already
built**, which is the whole reason the rule exists. The art was wrong before he
saw it and right after.

## 3. A HIT-HEAVY ULT MUST DECLARE ITSELF TO THE DIRECTOR

Aegis files at most two beats a cast, so the threshold work was not needed here
— but **the OPPOSITE failure showed up and it is the same rule with the sign
flipped.** The shield's reflection goes through `hurt()`, which files no beat at
all, so 21% of this relic's wins were invisible to the director and the clip
tool produced a fight with no ending. A fatal return files a beat now; an
ordinary one does not. Third relic to need that exact distinction.

**The shared `cineFloor` is still not built.** v40's first pickup item, still
first, still four relics deep.

---

# WHAT v41 ADDS TO THE RULES

## A CONTROL THAT CANNOT EXPRESS ZERO IS NOT A CONTROL

The wall-feed read `u.feed || 1`, so every "feed off" run in the sweep silently
measured a feed of ONE. It was caught because two configurations came back
**byte-identical across 100 fights** — not by inspection. The mechanic looked
worthless for an hour and was worth +15% absorbed and 23% fewer breaks.

`|| default` on any number a sweep is allowed to set is this bug waiting.
Use `=== undefined`.

## THE PICTURE IS THE MECHANIC — AND THIS RELIC BREAKS IT ONCE, ON PURPOSE

Aegis DRAWS at `artArc` 1.5 and BLOCKS at `arc` 2.8. Blows that visibly miss
the shield are stopped by it. That is Rick's call, made against four renders
with the cost stated, and the probe asserts the gap is the size it is supposed
to be so it cannot drift.

**It is the only such gap in the build and it should not become a precedent
without being argued again.** The reason it exists is geometric and worth
knowing: a FLAT shape of length L at radius rr subtends `2·atan(L/2/rr)`, which
at this scale caps out near 85° however long it is drawn. A shield that covers
more than that is a curved barrier, not a kite.

---

# THE FIRST FOUR THINGS TO PICK UP

1. **RULE 3, BUILT PROPERLY.** A measured `cineFloor` and a windowed beat in
   `cinema_build.py`, for every crowding mechanic. v40's item 1, unmoved, four
   relics deep. v41 adds a fifth data point from the other direction: the
   engine has damage paths that file NO beat at all (`hurt`, `shatter`), and
   the same session should decide which of those are endings.
2. **`cinePlan` SCORES A KILLING BLOW AND THEN DOES NOT ALWAYS CUT TO IT.**
   Seeds 9732 and 8430 both carry a fatal beat whose `why` reads *"the killing
   blow"* and neither becomes a cut, so `cinema_clip` falls back to the last
   cut and writes a clip with no ending. Pre-existing and relic-independent —
   it silently costs good seeds, and it cost this session two renders.
   `bulwarden_pick` should score on the PLAN, not on its own telemetry.
3. **KILL THE FIGHT CARD OUT OF THE BUILD.** Rule 1. Chain-wide, wants a probe.
4. **`01-live` IS SEVEN RELICS BEHIND.** v27 open decision 1, still the oldest
   open thing in the project, and now one relic worse.

## Still open, unmoved

- **`tip_audit.py` does not check ult tips.** v40's item 3. v41's tip carries no
  number at all (Rick's line), and `bulwarden_probe [1]` guards the general case
  — any percentage in an ult tip must equal the weapon's own field — but that
  guard lives in one relic's probe and not in the shared tool.
- **A kill by ward SHATTER files no beat**, the same hole the reflection had.
  Belongs to Lightkeeper and Farwarden too. Zero occurrences on this relic,
  which is the kind of zero that stops being zero when somebody tunes the pool.
- **`STATUS.ward.bank 0.55 / cap 90` have never been swept.** Vigil od 4, now
  with data at both ends of the type axis and nothing in the middle. The cap is
  reached 0.6% of the time — a ceiling nothing touches.
- **`turn` is a look knob, not a balance knob** — under 0.1 blocks a cast
  between 1.6 rad/s and instant. It stays because it is Rick's sentence and
  because the wall swinging round IS the animation, but nothing is balanced on
  it.
- **`shot.life: 3.4` is dead config on all four bows** (v40).
- **`cell_survey`'s umbral row is suspect on all six types** (v40). `wh_survey`
  §5 is a second instrument on one type and agrees curse is unremarkable in the
  moment — its value is the 84.3 max hp a fight it eats, which no occupancy
  table can see.
- **Every type-level measurement still wants a `--noult` pass** (v38 od 5, v39
  od 5, v40 od 6). `wh_survey` §3 reports both side by side, which is the first
  time the pair has been put next to each other.
