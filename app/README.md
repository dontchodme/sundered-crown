# The desktop app

Electron shell over the existing engine. **Phase 1: the game HTML is loaded
unchanged.** Nothing here edits, injects into, or forks the engine.

```bash
cd app
npm install
npm start
```

Requires Node 18+. `npm install` pulls Electron (~150 MB) once.

## Why the game runs in an iframe on a custom protocol

Two `file://` pages are opaque, mutually inaccessible origins — the shell could
not reach `window.AC` inside the frame to drive it. Serving both from one
`swb://app` origin makes them same-origin **without turning `webSecurity` off**,
which would work and would be the wrong habit to build.

The shell hides the game's own title/panel/log with a stylesheet injected from
the shell side. That keeps the look clean while leaving the engine file
byte-identical, which is Phase 1's rule.

## The test that says Phase 1 is done

Not "it opens". It runs without a person now — the window is hidden and the
process exits on the result:

```bash
cd app && npm run identity      # 192 fights, ~3s, writes out/shell_identity_app.json
cd ../tools && python shell_identity.py
```

(Or click **Engine identity → Run 200 seeds** in a running app; same code path.)

Every field of every fight summary must match headless Chromium. Current
state, 2026-08-26:

```
[identity] app      Chromium 152.0.7977.54  192 fights
[identity] headless Chromium 151.0.7922.34
PASS  192/192 identical.
```

**It did not always pass.** On Electron 32 (Chromium 128) it came back 80/192,
and the failure was not the shell — V8 does not promise a last bit for
`Math.pow`, which the sim integrates gravity through every step. The Electron
and playwright versions are now pinned as a *pair*, and the pair is checked by:

```bash
cd tools && python math_fingerprint.py
```

Do not bump `electron` in `package.json` without re-running that. The two
Chromiums are deliberately different versions that agree to the last bit; a
newer Electron that fails the fingerprint is not usable here whatever its
version number says. See `docs/RUNTIME-DRIFT.md`.

## What is deliberately not built yet

`swb:createShort` and `swb:speak` return `{ ok: false, reason }` on purpose.
A "Create short" button that appears to work and silently does nothing is worse
than one that says what phase it is waiting on. See `docs/ARCHITECTURE.md`
§4 and §5.

## Which build the window shows

One place — `GAME` in `main.js`, overridable with `SWB_GAME`. Keep it on the
build of record so the app cannot drift from what the video pipeline renders.
