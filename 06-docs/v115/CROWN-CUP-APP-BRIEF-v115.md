# CROWN CUP — the app drives it (build brief, v115)

Cowork, 2026-09-27. For Claude Code, **after the design batch and the staves have
landed** — nothing here touches the chain. Plan: `CROWN-CUP-PLAN-v115.md` in
this folder. Rick: *"can we update the clip tool so i can drive this from
there? … film every clip in sequence and then organize them in a file for me?"*

## What already exists (Cowork, tested)

`tools/cup.py` does the tournament end to end from a terminal, and
`tools/test_cup.py` falsifies its bookkeeping (43 checks, all green):

```
python cup.py draw   --game ../02-chain/<frozen tip>.html --seed <n>   # roster off the build → ledger
python cup.py seeds  --game ../02-chain/<frozen tip>.html              # every fixture's seed by the rule, results, standings
python cup.py film   --game ../02-chain/<frozen tip>.html [--dry-run]  # every fixture, in order, one folder each; resumable
python cup.py status                                                   # groups, knockout, filmed count
python cup.py schedule --start YYYY-MM-DD --name "…"                   # SCHEDULE.md with dates, captions, band copy
```

Tested live in Cowork's container on `sc-tendril-fx` (38 relics, `--field 25`
as a stand-in field): draw → 33 fixtures seeded in 52s → dry-run film → a
schedule file. `film` itself needs the machine with Kokoro and ffmpeg, so its
first real run is on yert; the command it issues per fixture is `shorts_build.py`
with exactly `app/main.js`'s arguments plus `--stakes`/`--stakes-sub`.

**Where things land** (`07-shorts/cup1/`, mp4s gitignored as ever):

```
ledger.json                 the whole tournament: draw, build hash, machine, every seed/k/result/file
results.json                the same, flat, for the bracket page
SCHEDULE.md                 post #, day, slot, fixture, file, caption, band copy
01-play-in/01 - PI - Paradox vs Lastlight/01 - PI - Paradox vs Lastlight.mp4
02-groups/A/02 - A1 - Threshmaw vs Bulwarden/…mp4
02-groups/A/03 - A2 - …
03-round-of-16/…   04-quarter-finals/…   05-semi-finals/…   06-third-place/…   07-final/…
```

One folder per render, because `shorts_build` puts `_clip_frames` beside its
output (main.js's 4,747-decode-error note). The number prefix is the posting
order, so the folders sort into the slate.

## What the app gets — one panel, three IPC handlers

Same pattern as `swb:createShort`: a named capability per thing, nothing
generic. **Reuse the `JOB` guard** — a cup run and a single short must not
overlap (they would share `_clip_frames` only if someone pointed them at the
same folder, but they DO share the machine's capture budget and the progress
channel).

```js
// preload.js
cupLedger: () => ipcRenderer.invoke('swb:cupLedger'),          // reads 07-shorts/cup1/ledger.json, or {none:true}
cupRun:    (opts) => ipcRenderer.invoke('swb:cupRun', opts),   // {cmd:'draw'|'seeds'|'film', seed?}  spawns cup.py
cupCancel: () => ipcRenderer.invoke('swb:cupCancel'),          // taskkill /T /F, like cancelShort
onCupProgress: (fn) => …  // {i, total, id, a, b}    from "[cup] i/total ID a v b seed …"
                          // {stage:'capture', frames, elapsed}  from shorts_build's own [progress] line
onCupLog, onCupDone       // as the short's
```

`swb:cupRun` spawns `PYTHON cup.py <cmd> --game <gameAbs> [--seed n]` with
`cwd: tools/`, `env: childEnv()`, `windowsHide`. `--game` is the app's own
`GAME` pointer made absolute (the same line createShort uses); `cup.py`
refuses to run against a build whose sha256 differs from the ledger's, which
is the freeze (plan §3) enforced by the tool rather than by memory.

**Parse two progress lines.** The outer one is cup.py's:

```
[cup] 12/65 A3 thornshear v vesper seed 1606666929 -> 02-groups/A/13 - A3 - …mp4
[cup] band: GROUP A · MATCH 3 OF 3 / WINNER TAKES THE GROUP
[cup] done 12/65
```

The inner one is shorts_build's `[progress] capture frames=… elapsed=…`,
passed through unchanged — the regex in createShort's `feed` works as is.
Everything else is log.

**The panel** (`shell.html` / `shell.js`), under the existing short controls:

```
CROWN CUP                                   [ledger: 65 fixtures · 65 seeded · 31 filmed]
  draw seed  [ 20261001 ]  [Draw]           disabled once a ledger exists (a draw is a commitment; --force is terminal-only)
  [Seed all]                                 disabled until drawn; a minute for 65
  [Film all]     [Cancel]                    disabled until seeded
  ████████████░░░░░░░░  31/65  A3 Thornshear v Vesper     ← outer, from [cup]
  ████░░░░░░░░░░░░░░░░  capture 2,140 frames · 38s         ← inner, from [progress]
  [Open folder]                              revealFile on 07-shorts/cup1/SCHEDULE.md
```

`Film all` is resumable by construction: cup.py skips fixtures whose mp4
exists, so a cancelled or crashed run continues from where it stopped by
pressing it again. Show the last `[cup] band:` line while a fixture films —
it is what Rick will want to veto if the copy reads wrong.

## The one build change on the chain — NOT this brief

Plan §5.3 (the `CONFIG.cup` standings card on the verdict panel) is a chain
link and gets its own brief when the copy is settled. This brief is app-only.

## A director finding, for a separate decision

Measured while building cup.py (`cup.py` docstring): on the current tip the
director finds a fatal cut in **6–34% of kills**, and in the 33-fixture test
run **4 of 33** finales had one. Requiring a fatal cut moved win rates by up to
26 points, so the tournament rule does not require one — which means most
finales in the series will play at plain speed. A director change that files a
fatal cut on EVERY kill (a rule, not a score — the kill is always the finale)
would fix that for the tournament and for every short. It is a `cinePlan`
change, sim-inert, gated by `engine_ab` and `render_ab`; it is Rick's to call
and not part of this brief.

## Gates

1. `python test_cup.py` green on yert (it has no browser in it; it should be
   green everywhere).
2. `python cup.py --dir ../07-shorts/_cuptest draw --game <tip> --seed 20261001 --field 25`
   then `seeds`, then `film --dry-run` (same `--dir`): the same 33-fixture run
   the container did, on the pinned Chromium. Delete `_cuptest` after. (`--dir`
   goes before the subcommand; `--field` takes the first N relics, and the
   first 13 of this roster are seven greatswords, which no 4-group draw can
   hold — 25 is the smallest field that works on it.)
3. The panel drives one real `film --only A1` to an mp4 and the progress bars
   move; `Cancel` kills the tree (no orphan Chromium — check Task Manager).
4. `npm run identity` + `shell_identity` unchanged: the panel touches no game.
