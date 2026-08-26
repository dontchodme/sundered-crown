# SUPER WEAPON BALL: THE SUNDERED CROWN

A deterministic two-relic arena fight, rendered to vertical short-form video.
Twenty-five relics, a cinema director that decides what is worth watching, a
synthesized soundtrack, and a local voiceover.

**New here?** Read [`CLAUDE.md`](CLAUDE.md). It is the whole project in one
file, and it replaces the handoff zip.

---

## State

```
02-chain/sc-paradox-frame.html   BUILD OF RECORD   25 relics · Stasis Field
01-live/sundered-crown.html      LIVE              16 relics — nine behind
```

## Run it

**In a browser.** Open `01-live/sc-playable.html`. No build step, no
dependencies — the whole game is one self-contained HTML file.

**As a desktop app.** `cd app && npm install && npm start`. See
[`app/README.md`](app/README.md).

## The layout

| folder | what is in it |
|---|---|
| `01-live/` | what ships |
| `02-chain/` | how the build was made, in order. `sc-base.html` is the root. |
| `04-experiments/` | unshipped variants **and controls** |
| `05-reference/` | images, filmstrips, the clickable fighter review |
| `06-docs/` | the write-ups, one folder per version |
| `07-shorts/` | delivered videos — **mp4s are gitignored; the seed rebuilds them** |
| `08-analytics/` | retention curves and cold-open reads off real posts |
| `tools/` | 195 builders, probes and renderers. Flat on purpose — `tools/README.md` groups them. |
| `app/` | the Electron desktop shell |
| `docs/` | [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) — where the app is going |

## The two things worth knowing before you touch anything

**The seed is the fight.** `(build, relic A, relic B, seed)` produces the same
fight every time. That is why no mp4 is committed — the command that made it is
worth keeping, the bytes are not — and it is why anything that breaks
determinism invalidates the whole history of the project, not just the current
session.

**The simulation does not know a screen exists.** `Fighter`, `Match` and `Sfx`
contain zero references to `document`, `canvas` or `getContext`. The renderer
can be replaced without changing a single fight.

## What is not in the repo

The Kokoro voiceover model (353 MB), rendered mp4s and wavs, and frame caches.
All of it regenerates — see
[`06-docs/WHATS-NOT-IN-THE-REPO.md`](06-docs/WHATS-NOT-IN-THE-REPO.md) and
[`tools/FETCH-KOKORO.md`](tools/FETCH-KOKORO.md).

## Working on it

```bash
git pull                            # start here, always
# ...
git add -A && git commit -m "..."   # end here, always
git push
```

A commit that changes the build of record **names its verification in the
message** — which probes ran, at what count. A green claim with no run behind
it is worse than a red one.
