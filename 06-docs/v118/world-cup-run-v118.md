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

(in progress)
