# v118 — THE WEAPON BALL WORLD CUP: THE DRAW AND THE 65 FILMS — DRAWN; SEEDING AND FILMING

Claude Code on DESKTOP-DERRAFT, 2026-09-30. **IN PROGRESS — do not draw, seed or film the Cup in parallel.**
Rick: "you pick the draw seed. have at it". The card it films with is `cup-card-build-v118.md`.

## The draw — the commitment, made before any fight was computed

| | |
|---|---|
| tournament | **Weapon Ball World Cup** (`cup.py schedule --name`) |
| seed rule | `seed(k) = sha256("weapon-ball-world-cup/<fixture>/<side 1 id>/<side 2 id>/<k>")[:8] & 0x7fffffff`; the fight is the first `k` that ends in a kill (plan v115 §3 as corrected in §10) |
| draw seed | **20260930** — today's date, the day Rick named the Cup and handed Code the pick. Chosen before any draw of the 49 had been computed with any seed; drawn once. (The scratch test draw that used the same number was a 25-relic field under a different cup id, so a different draw.) Legal on shuffle 6. |
| frozen build | `02-chain/sc-cupcard.html`, sha256 `3863ef311c02a1f8e2ac6852549cbb316ef7817ac64c82fbf671085f41e1b75a` (the live `sc-candidate-49` plus the verdict card; the fights are the live game's, 7056/7056) |
| runtime | DESKTOP-DERRAFT / Windows 10, Chromium 151.0.7922.34; drawn 2026-09-30T19:50:40 |
| the ledger as drawn | `07-shorts/cup1-draw/ledger-as-drawn.json`, sha256 `4268598f3245153b20888047c48a907a767fe3b2bbbcb9fb65b4e36d06705339`, no result in it |

```
A  Twinshade      Oracle         Bindweed          I  Vinesower     Paradox        Widowmaker
B  Spellbreaker   Cindercleave   Heartwood         J  Emberedge     Lastlight      Watchlight
C  Bloodwick      Gloamwire      Slagheart         K  Culverin      Bloodmirror    Nightfell
D  Nightglass     Farwarden      Foregone          L  Crozier       Axiom          Coldiron
E  Cipher         Vesper         Gravemourn        M  Goreshard     Duskreave      Lodestone
F  Bulwarden      Ironhail       Angelus           N  Shroudmaul    Starwarden     Briarwand
G  Ravelbone      Morningstar    Thornwake         O  Ironwood      Dawnbringer    Threshmaw
H  Grudgebearer   Aureole        Lightkeeper       P  Censer        Thornshear     Portcullis
                                                   play-in: Marrowdraw v Portcullis, for P's last slot
```

Every group: three schools, three weapon types. Group order P1 v P2, P2 v P3, P3 v P1.

## What is committed, and what is not

**The repo is public** (github.com/dontchodme/sundered-crown answers anonymously), and a seeded ledger is every result
of the tournament — the plan's rule is that the only spoiler is Rick (v115 §4). So:

- **committed**: the ledger as drawn (above) — the seed, the rule, the build hash, the groups, before any fight;
- **not committed**: `07-shorts/cup1/` (now in `.gitignore`) — the live ledger once seeded, `results.json`,
  `SCHEDULE.md` (its bands name winners), each fixture's card blob, and the films (mp4s were ignored already).
  They live on DESKTOP-DERRAFT, the filming machine the ledger is bound to.

Plan §6 says the ledger is "committed to git"; on a public repo that would publish the results before day 1, so
it is not, until the final has posted (or Rick says otherwise).

## Seeds and films

**Seeded 2026-09-30 ~19:55, after the draw was pushed (a6a7364):** `cup.py seeds --game ../02-chain/sc-cupcard.html`,
22 s, 65/65 results, no runtime override. `k` = 0 on all 65 (no timeouts). 8 groups decided on wins, **8 on the HP
tiebreak** (twice the plan's quarter). The director filed a fatal cut on 10 of 65 kills; the rest end at plain speed.
Fights 35.2-96.4 s of match time. (No result is written here — see "What is committed".)

**Filming** from ~19:57: every fixture in posting order through `cup.py film --only <id>` (the card, the 3.5 s hold
and the spoken stakes all come from `film`), one at a time at idle priority (Rick on the PC: build-load-limit), about
10 min a short, so ~10-11 h. The driver runs one fixture per call so a failure does not stop the night, and moves a
failed fixture's mp4 aside (`*.FAILED.mp4`) so a resume films it again instead of skipping it as already filmed
(v115 found item 1). Log: `07-shorts/cup1/film.log` (local).

### Found while filming

1. **The play-in came out too quiet, and the mix's ladder could only make it quieter.** PI (Marrowdraw v Portcullis,
   seed 90360136; a quiet, one-sided fight) measured -16.1 LUFS / -1.3 dBTP at the first rung against the -16..-13
   band; every later rung lowers the ceiling, so it went -16.4, -16.8 and failed. `shorts_build.py` now has
   `QUIET_RUNGS`: when the first rung lands below the band with true peak to spare (<= -1.0 dBTP), the mix is
   rebuilt from the same `on.wav` at loudnorm I=-13, then -12, same ceiling and TP. A short that passes its first
   rung is mixed exactly as before. PI was re-mixed from its retained capture (`--encode-only`, no re-capture):
   **-15.3 LUFS, -0.7 dBTP, every mark passes.** A1 had already started on the old code; A2 onward have the rung.
   PI's ledger entry (file, band, card, announce, delivery) is filled in when the run is idle -- the driver's
   `cup.py film` holds the ledger in memory while a fixture films.
2. **C1 missed both ways at once, which the first fix did not cover.** C1 (Bloodwick v Gloamwire, seed 1671739477,
   two clanks, a very spiky fight) measured -16.3 LUFS AND +0.1 dBTP at the first rung, then -17.0 / -2.3 and
   -17.6 / -4.2 down the ceilings. The louder rung needed peak to spare, so it never ran. The ladder is now
   two-dimensional (`LOUDER = (-13, -12, -11)`): at each ceiling I=-14 first -- exactly the old rung -- and while the
   mix is too quiet with its peak in the band, the same ceiling again louder; a peak over the band moves to the next
   ceiling, as before. A clip that passed on the old ladder passes on the same rung (a lower ceiling never made a
   quiet mix louder), which a simulated walk confirms for the five shapes: passes first rung (1 try, unchanged),
   peaky only (0.63, unchanged), PI's shape, C1's shape, and a hopeless one (fails as before). C1 re-mixed from its
   retained capture: 0.63 / I=-12, **-15.8 LUFS, -1.9 dBTP, every mark passes.** Films started after 22:33 use it.
