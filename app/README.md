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

Not "it opens". Click **Engine identity → Run 200 seeds**, then:

```bash
cd tools
python3 shell_identity.py
```

Every field of every fight summary must match headless Chromium. One differing
digit means the shell changed the engine, and the whole Electron-over-Tauri
argument (§1 of `docs/ARCHITECTURE.md`) is void on this machine.

## What is deliberately not built yet

`swb:createShort` and `swb:speak` return `{ ok: false, reason }` on purpose.
A "Create short" button that appears to work and silently does nothing is worse
than one that says what phase it is waiting on. See `docs/ARCHITECTURE.md`
§4 and §5.

## Which build the window shows

One place — `GAME` in `main.js`, overridable with `SWB_GAME`. Keep it on the
build of record so the app cannot drift from what the video pipeline renders.
