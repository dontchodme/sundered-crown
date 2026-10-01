# v118 — THE WEAPON BALL WORLD CUP'S VERDICT CARD (plan v115 §5.3): BUILDING

**2026-09-30 18:16: a new Claude Code session on DESKTOP-DERRAFT has taken the handoff below and is building the card. Do not build it in parallel.** The build record replaces this file when the card is done.

Claude Code on DESKTOP-DERRAFT, 2026-09-30. **Nothing of the card is built yet.** A build agent was started and
stopped within minutes, before it changed any file. Rick is near his weekly limit and is handing the rest to a new
session. This file is the handoff: the state, Rick's rulings, and the next steps in order.

## Where things stand

- **The game is LIVE on `02-chain/sc-candidate-49.html`** (`app/main.js` GAME, commit e045c02).
  - 49 relics: the batch tip `sc-balance` (all nineteen v68-v86 designs, built and balanced, v88-v117), Rick's
    Daybreak circle, and yert's seven staves, made by `06-docs/v117/make_roster.sh`.
  - **This is the tournament's frozen build** (plan §7 step 2). The card link goes on top of it.
- **Kokoro is installed on THIS PC (DESKTOP-DERRAFT)**, so the Cup films here.
  - `tools/kokoro-v1.0.onnx` (325,532,387 bytes) and `tools/voices-v1.0.bin` (28,214,398 bytes); both gitignored.
  - pip into Python 3.13: kokoro-onnx 0.6.1, onnxruntime 1.30.0, soundfile 0.14.0.
  - The smoke-test short's result is the "Smoke test" section at the end.
- **The Cup's app panel is built and committed** (v115, `crown-cup-app-build-v115.md`).
  - Its gate 4, the Electron identity check, is effectively passed: `npm run identity` + `shell_identity.py`
    read 196/196 on the live app, which includes the panel (06-docs/v117/runs/live/).
  - Its gate 3, one real film driven from the panel, is still owed. It can run here now.

## Rick's rulings, 2026-09-30 (do not re-ask)

| | ruling |
|---|---|
| name | **"Weapon Ball World Cup"**: `cup.py schedule --name "Weapon Ball World Cup"`; the seed-rule id at the draw, e.g. `cup.py draw --cup weapon-ball-world-cup` |
| filming machine | **this PC** (Kokoro installed above); the ledger binds the draw to the filming machine |
| stakes-band copy (plan §5.1) | **the drafts, as written** |
| verdict card (plan §5.3) | **"build it from the sketch"** -- this doc's build |
| still Rick's | **the draw seed** (any number, published with the draw); plan §9.2 / 9.5-9.7 (third place, post slots, draw-reveal post, dead rubbers) |

## Next steps, in order

1. **Build the card**, from `06-docs/v118/BUILD-BRIEF-v118.md` (the brief given to the stopped agent):
   `tools/cupcard_build.py` -> `02-chain/sc-cupcard.html` on `sc-candidate-49`; cup.py `cupjson` + film
   passing it; shorts_build `--cup-json`; the gates; this doc.
2. **Move GAME to `sc-cupcard.html`**, the card link: presentation-only, so the fights are identical. Then run
   `cd app && npm run identity` + `cd tools && python shell_identity.py`, and commit the json as the go-live
   commit did. Only when Rick is not using the PC: it launches Electron (memory: build-load-limit).
3. **Rick's draw seed**, then `cup.py draw --game ../02-chain/sc-cupcard.html --seed <his> --cup weapon-ball-world-cup`
   and `cup.py schedule --name "Weapon Ball World Cup"`. Publish the empty bracket (plan §7 step 5).
4. **`cup.py seeds`, then `cup.py film`** (or the app panel's Seed all / Film all). That is 65 shorts, about
   3-4 hours of machine time, resumable. Mind v115's "found" item 1: resume can pass over a failed short.
5. **Spot-check** the play-in, one group's three, and a semi (plan §7 step 7). Then Rick queues the posts.

## Smoke test

**PASSED, 2026-09-30 18:06: this PC films a full short with the voice-over.**

```
python shorts_build.py --game ../02-chain/sc-candidate-49.html --a angelus --b lodestone --seed 20260930 --no-card --stakes "SMOKE TEST" --stakes-sub "NOT A CUP MATCH" --out <scratch>/smoke.mp4
```

- **Capture:** 3951 frames (65.8s), in 539s. Angelus wins on 520 hp; 24 clanks.
- **Voice-over:** Kokoro's bm_lewis spoke "Angelus, or Lodestone. Who wins?"
- **Delivery:** 1080x1920 h264+aac, 65.9s, 32.2 MB, -15.3 LUFS, -0.8 dBTP. Every delivery mark passes.
- The file lives in Claude Code's scratch. It is not a Cup match and is not kept in the repo.
