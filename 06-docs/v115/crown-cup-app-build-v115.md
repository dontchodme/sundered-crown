# v115 — THE CROWN CUP APP PANEL, BUILD. BUILT: gates 1-2 green on DESKTOP-DERRAFT; gate 3 (one real film) and gate 4 (the Electron identity check) owed.

Claude Code on DESKTOP-DERRAFT, 2026-09-30. Built from `CROWN-CUP-APP-BRIEF-v115.md`,
before the batch lands, on Rick's ask (*"can you get started on it now without the
whole roster being finished?"*). **App only: no file in `02-chain/` touched, `GAME`
not moved, nothing drawn into `07-shorts/cup1/`.** `tools/cup.py` and
`tools/test_cup.py` are Cowork's and are unchanged.

## What was built

| file | what |
|---|---|
| `app/main.js` | `swb:cupLedger`, `swb:cupRun`, `swb:cupCancel`. `cupRun` spawns `python -u cup.py --dir <cup dir> <draw\|seeds\|film> --game <GAME, absolute> [--seed n] [--only ID]` with `cwd: tools/`, `childEnv()`, `windowsHide`, and shares createShort's `JOB`. |
| `app/cuplines.js` | the output reader: bytes to lines, lines to progress events (`[cup] i/n ID a v b seed … -> file`, `[cup] band:`, `[cup] done i/n`, `[cup] … already filmed`, and shorts_build's `[progress]` with createShort's own regex). Everything else is log. |
| `app/preload.js` | `cupLedger`, `cupRun`, `cupCancel`, `onCupProgress`, `onCupLog`, `onCupDone`. |
| `app/ui/shell.html`, `app/ui/cup.js`, `app/ui/shell.css` | the CROWN CUP card under Create short: ledger line, the ledger's build/machine line, draw seed + **Draw**, **Seed all**, **Film all** + **Cancel**, the outer bar (fixture i/n and the two names), the inner bar (the fixture's stage), the band line while it films, the log, **Open folder**. |
| `app/test_cuplines.js` | 21 checks on the reader, no Electron: `node app/test_cuplines.js`. |

`shell.js` is untouched: the panel is its own script, like `post-dev.js`, and needs
nothing from the game frame. The ledger is the whole state and is read back from disk
after every run and after every fixture.

## Choices the brief left open, and why

- **The draw seed box starts empty** (placeholder "any number"), not on the brief
  mockup's `20261001`. That number is the gates' test seed. The real one is Rick's
  pick (plan §7 step 4), and a box that is already filled invites a commitment
  nobody chose. **Draw asks for confirmation**, naming the build and its relic
  count, because a draw cannot be undone from the app.
- **"Film all disabled until seeded"** is read as *until every fixture has its
  fight*. Seed all is on from the draw until every fixture has one.
- **The inner bar shows stages, not a percentage.** It lights a third per stage from
  shorts_build's own `[1/3]`/`[2/3]`/`[3/3]` lines (the same lines the short card
  reads). Inside the capture it shows a frame COUNT and the elapsed time. The capture
  runs until the match ends, and cinema_clip.py says at its `[progress]` line why a
  denominator there would be invented. The brief's mockup drew the capture as a
  partly filled bar; this is the one place the panel departs from the mockup.
- **Lines are decoded per line: UTF-8, else cp1252.** Python writes a pipe in the
  machine's ANSI code page (cp1252 here), unless the shell sets PYTHONIOENCODING
  (Claude Code's shell sets utf-8). Every group band has a middle dot. Read as plain
  UTF-8, the cp1252 dot arrives as U+FFFD, on the line Rick reads to veto the copy.
  The integration run below proves both halves.
- **`python -u`.** cup.py's own lines are print()s without a flush, and a pipe is
  block-buffered, so without it the log would arrive in 8 KB lumps (a whole Seed
  all at the end).
- **A guard for the seconds before a job starts.** createShort renders a typed
  announcer line (several seconds) between its guard and the spawn that sets `JOB`.
  A cup run pressed in that window would have passed a guard that reads only `JOB`.
  The handler is wrapped: `busyReason()` reads `JOB` and a `STARTING` flag. It has
  no other effect on createShort. **cancelShort no longer cancels a cup run**, and
  cupCancel cancels only a cup run.
- **Cancel removes the in-flight fixture's mp4 if the ledger has no clean film of
  it.** Found while building (see below): shorts_build writes the delivered mp4 in
  place during its mix, and cup.py resumes by skipping any fixture whose mp4
  exists. A cancel in the mix would otherwise leave a partial file that the next
  Film all passes over as filmed. Only that one file is touched, and only when the
  ledger has no `filmed` stamp for it, which cup.py writes after shorts_build
  exits 0.
- **Closing the app ends a cup run** (the tree, as Cancel does) rather than
  leaving hours of hidden browsers behind. The run resumes when Film all is
  pressed again.
- **`SWB_CUP_DIR`** points the panel at another folder inside the repo, the way
  `SWB_GAME` points the window at another build. This is how gate 3 runs without a
  draw in `07-shorts/cup1/`. `cupRun` accepts `only` (a fixture id) for gate 3,
  and no button sends it. `--force` and `--redo` are never sent: a redraw is
  terminal-only.

## Gates

1. **`python test_cup.py`: 54 checks, ALL OK** (DESKTOP-DERRAFT, Python 3.13.15).
   The brief and the CLAIMS row say 43; the file has 54 now. `runs/cup-app/gate1-test_cup.txt`.
2. **draw → seeds → film --dry-run on the pinned Chromium 151.0.7922.34**
   (`sc-tendril-fx`, `--field 25`, draw seed 20261001, `--dir ../07-shorts/_cuptest`,
   deleted after). `runs/cup-app/gate2-*.txt`.
   - **The draw reproduces the container's:** the play-in is Paradox v Lastlight and
     A1 is Threshmaw v Bulwarden, the brief's own example folders. It was legal on
     shuffle 6; there are 33 fixtures.
   - **Seeds: 33/33 in 9.3 s, `k=0` on every fixture** (as the container found).
   - **The fights are not all the container's.** On 151 the director found the
     finale in **8 of 33** (the container, Chromium 141: 4 of 33), and **2 of 8** groups went
     to the HP tiebreak (the container: 3 of 8). The seeds are identical, since
     they depend only on the fixture and its sides, so some fights resolve
     differently on the two runtimes. This is plan §3's "determinism is per
     runtime", measured. It is why the whole tournament must be seeded and filmed
     on one machine.
   - **The dry run's commands are createShort's arguments plus the band**:
     `shorts_build.py --game <abs> --a --b --seed --no-card --stakes … --stakes-sub … --out …`.
3. **NOT RUN — a real `film --only A1` driven from the panel, then a Cancel.**
   DESKTOP-DERRAFT cannot film a short: `tools/kokoro-v1.0.onnx` and
   `voices-v1.0.bin` are not installed here, and shorts_build renders the hook
   with them. The brief puts film's first real run on yert. It also needs an Electron
   launch, which waits for Rick's word on this PC. Steps below.
4. **NOT RUN — `npm run identity` + `python shell_identity.py`.** It launches
   Electron, so it waits for Rick to be off this PC (his load rule). The panel does
   not touch the game (it reads `AC.WEAPONS.length` for the Draw confirmation and
   nothing else), and main.js's protocol and window code are unchanged. The
   gate still has to run.

**Checked beyond the brief:**
- **`node app/test_cuplines.js`: 21 checks, ALL OK.** Two wrong implementations
  were run against it, and both were caught: a plain UTF-8 decode (two FAILs) and
  decoding each chunk as it arrives (a character cut between reads).
- **Integration: real `cup.py film --dry-run` output through `cuplines.js`**, once as
  cp1252 (no PYTHONIOENCODING, an app launched from a shortcut) and once as UTF-8.
  Both give 33 fixture events in posting order, 24 group bands with a real middle
  dot, no U+FFFD, and identical lines. **Control:** the cp1252 run really sent
  0xB7, and a plain UTF-8 read of it contains U+FFFD. `runs/cup-app/integ_cuplines.*`.
- **The panel in a browser**, with the real card markup lifted from shell.html,
  the real cup.js and the real gate-2 ledger, and the main process replaced by a
  script:
  - no ledger: only Draw is on;
  - Draw: the confirmation names the build, and the call carries only `{cmd, seed}`;
  - while a run is going: only Cancel is on;
  - drawn: Seed all is on; seeded: Film all is on;
  - while filming: "3/33 A2 Bulwarden v Ironhail" (ids to names, `redflail` to
    Threshmaw), the frame count, and the stage bar at a third;
  - the band line keeps its dot;
  - Cancel: "press Film all again to carry on";
  - a refusal is said on the button;
  - a failed film is warned about on every read;
  - an unreadable ledger turns everything off and says why.

## Gate 3, on yert (where Kokoro is)

```
cd tools
python cup.py --dir ../07-shorts/_cuptest draw --game ../02-chain/sc-nightglass-fx.html --seed 20261001 --field 25
```

The test ledger has to be drawn on the app's own `GAME` (sc-nightglass-fx today), or
`film` refuses it as a different build. Then start the app pointed at it (PowerShell,
in `app/`): `$env:SWB_CUP_DIR='07-shorts/_cuptest'; npm start`.
1. Press **Seed all**.
2. In devtools, run `swb.cupRun({cmd:'film', only:'A1'})`. An mp4 should land in
   `_cuptest/02-groups/A/…`, and both bars should move.
3. Press **Film all**, then **Cancel** mid-capture. Task Manager should show no
   orphaned `chrome-headless-shell` or `python`.
4. Delete `_cuptest`.

## Found while building, for Rick and Cowork (cup.py is Cowork's, and it is unchanged)

1. **cup.py's resume can pass over a failed short.** `film` skips any fixture
   whose mp4 exists. shorts_build writes the mp4 BEFORE it measures it, and exits 1
   when a delivery mark fails (length 180 s, loudness), leaving the file. cup.py then
   records `film_error` and stops. The next `film` prints "already filmed", sets
   `file`, and moves on. The same happens after a crash, or after a quit during the
   mix. The panel's own Cancel cleans up after itself, and the panel warns about any
   `film_error` fixture every time it reads the ledger. The root fix is cup.py's:
   skip only when the ledger holds a clean film
   (`out.exists() and f.get("filmed") and not f.get("film_error")`), otherwise film
   again. That is a behaviour choice (a deterministic failure would then fail again
   on every press), so it is theirs to make.
2. **The ledger is bound to one machine** (`film` refuses another without
   `--force`), and only yert can film. So the tournament machine is yert, unless
   Kokoro is installed here, and the draw has to happen on that machine.
3. `tools/README.md` has no cup.py section yet, and `app/README.md`'s "What is
   deliberately not built yet" still says Create short and the announcer return
   `{ok:false}`; both have been built for weeks. Neither is changed here.
