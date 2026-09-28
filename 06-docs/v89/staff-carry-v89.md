# v89 — THE STAFF ROW IS IN THE GAME. `app/main.js` → `sc-nightglass-fx`, and the carry that will take the staves onto the batch line when it ships. Claude Code on yert, 2026-09-27.

Rick, off the seven staff clips: *"looks good get it in the game"*.

## 1. What moved

`GAME` in `app/main.js`: `02-chain/sc-leaf.html` → **`02-chain/sc-nightglass-fx.html`**. That link is sc-leaf — the build of record Rick passed at gate 4 — plus the seven staves, each through stage 6, and nothing else: 34 relics + 7 = 41.

**shell_identity on the moved pointer: 195/195 identical** (`runs/carry/game_shell_identity.txt`) — the app run with NO `SWB_GAME` override, so it loaded the new pointer by itself (`build 02-chain/sc-nightglass-fx.html`), app Chromium 152 against headless 151. `out/shell_identity_app.json` is the new record and is committed with the pointer, as it was when sc-leaf took it.

The staff line's own gates stand behind it (each relic's build doc, v90–v96): engine_ab at every stage, each stage-6 link WITH its relic; the shipped voices equal the picks; render_ab; the probes; verify at each tip (Nightglass's: 10/13, Nightglass 50.7%, the reds the two clock bands, Starwarden v Watchlight 40/0, and Lightkeeper v Nightglass 40/0 — the design's named counter, items 12/32).

## 2. Why the staff tip, and not the staves carried onto the batch line's tip

Every staff build doc said the staff line would not move `GAME` until it and the design batch's line were carried onto one another. That was Code's sequencing note (v96 build §intro), not a ruling — and on the day the pointer moved it would have shipped things Rick has not passed:

- the batch tip (`sc-coldiron-temper-fx`) carries **Daybreak's LINE**, and its CLAIMS row says in capitals **"THE LINE DOES NOT SHIP — THE CIRCLE IS BUILDING ON yert"** (Rick's redesign, `sc-sunrise-e26`, a separate branch);
- Corollary is "BUILT, AWAITING RICK'S EYE"; Morningstar, Ironwood, Portcullis, Bindweed and Coldiron are "CLIP WITH RICK";
- the batch's own orchestrator (v103 build §8) moves `GAME` "only when Rick has nothing to overrule on the batch's clips";
- and the batch line is still being built on DESKTOP-DERRAFT (Angelus, Oracle and nine redesigns in flight), so a merged link would be stale the day the next relic lands.

So the pointer moved by exactly what Rick passed. **The batch line is not in the game, on purpose.**

## 3. The carry, ready for when the batch ships — `tools/staff_carry.py`

```
python tools/staff_carry.py --src 02-chain/<batch tip>.html --out 02-chain/<link>.html
```

It re-runs every staff builder's every stage (35 of them), in v89 §7's order, with `--src` on the given tip; the builders are the numbers' only home (CLAUDE.md §4.9), so the carry is nothing but them. Intermediate links go to a temporary directory (`--keep DIR` keeps them); the last is written to `--out` with the carry's stamp. Every builder's own checks, syntax check and RNG refusal run on every stage.

**Dry run on `sc-coldiron-temper-fx` (67cc3e6e05d5326e): all 35 stages hold** (`runs/carry/dry_run_coldiron.txt`), the merged link 6b4fb72f75e03e40, 46 relics (the batch's 39, then the seven staves). **Every builder's insert audit passes on it** (`runs/carry/dry_run_audits.txt`): Briarwand 26/26, Cipher 27/27, Watchlight 24/24, Crozier 26/26, Bloodwick 28/28, Nightglass 29/29, and Culverin 31/33 — the same 31/33 it reads on the staff line's own tip, because Briarwand's builder rewrites two of Culverin's lines on purpose (the verdant head's pick, and a `quiet` guard on the release voice).

**One anchor had moved and was given a second form.** Coldiron (v103) added a SUNDER clause to the status tag's value expression after the hemorrhage one, so Cipher's stage-6 hex clause (v94 §6.1, "the hex tag ticks by two") goes in between them on that line; on the staff branch the expression still ends at the hemorrhage clause and the edit is unchanged. `cipher_build.py` picks the form by the source (`SUNDER_TAG`), its audit by the tip — and it still rebuilds `sc-cipher-fx` from `sc-converge-blade` byte for byte (7cf7d7330f7b1128) and audits 27/27 there.

**The dry run is not a gate for a pointer move, and the merged link was NOT written to 02-chain**: it bundles the Daybreak line that does not ship. When Rick passes the batch, the carry is re-run on whatever its tip is then, and proved there: engine_ab batch tip → carried link over the batch roster (identical: the staves' inserts are guarded by staff-only fields — every staff stage proved it on its own line); engine_ab staff tip → carried link over the staves and every relic the batch did not change (identical unless a batch edit reaches them); verify; shell_identity; the seven audits.

**A `GAME` move to a batch tip WITHOUT this carry takes the staves out of the game.** CLAUDE.md §0 says so where the batch's orchestrator will read it.

## 4. Open, and Rick's

- The row re-priced against the whole roster (v89 §8.2): every staff blade is provisional, measured against 34 + the staves before it. The batch line will change the field again when it ships.
- The matchups a relic cannot win (items 12/32): Lightkeeper v Nightglass, Starwarden v Watchlight.
- Bloodwick's lunge fires on one globule 91% of the time (v90 build).
- Daybreak's circle (`sc-sunrise-e26`, another session's branch) is not in the game either; it is awaiting Rick's eye.
