# v85 — HEARTWOOD / ROOTFAST, REDESIGNED. Every blow roots the foe where it stands — ball and weapon, for a second — so the next swing finds it still there. The one-shot root was Bramblesnare with a smaller number, on the weakest relic in the game.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0);
claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab:
`overlays/rootfast.js`; runs in `06-docs/v85/runs/`.

## Why

`kind:"freeze"` 1.3s / 9 damage / 3 Entangle — Bramblesnare's twin (v68
§9), and Heartwood has been the floor of the roster since v59 (38.5%; 40.0%
here). Bramblesnare (v84) took the brambles; Rootfast keeps the ROOT, and
puts it where a greatsword's problem is: a swing that aims (`mode:"swing"`)
throws its target out of reach with its own knock (v51 §4.3: "knockback
eating its own window"; Gravemourn's blade curve bends DOWN for it).
**Rootfast means held fast** — a foe that cannot be thrown away by the
blow that hit it.

# 1. §1 (Cowork)

> For a duration every blow the sword lands roots the enemy where it
> stands — ball and weapon — for a second, and entangles it. The knock
> that would have thrown it across the hall has nothing to throw; the
> next swing finds it still there.

Two clauses: the root on every hit (a 1.0s pin, ball and weapon — the
pin discards the knock, which is the point); entangle +1 on every hit
(**the feed**, on top of the channel's 2).

# 2. THE HARNESS, AND THE CONTROL

Heartwood as shipped on `sc-trunk`, Chromium 141. **SHIP 40.0% (330), A
26.4%.**

# 3. PRICED (`runs/rootfast_*`)

```
arm                                            win    casts  hits in/out  roots/cast  foe pinned (window)
A   no ultimate                               26.4%           —  / 21.7
SHIP the 1.3s root                            40.0%
B   root 0.45s on every hit                   35.8%   3.75   10.7 / 12.0    2.8         22%
C   + entangle +1 a hit, root 0.45            37.3%   3.76   10.5 / 12.0    2.7         21%
C   root 0.8                                  52.1%   3.80   11.7 / 12.3    3.0         35%
C   root 1.0   (taken)                        55.8%   3.83   11.8 / 12.3    3.0         40%
```

**The root's length is the lever**: 0.45s holds the foe 22% of the window
and is worth less than the shipped one-shot; 1.0s holds it 40% and is
+30. Three roots a cast, the foe planted almost half the window. 55.8
against a shipped 40.0 — **the redesign is also the fix for the floor**:
verify's band is 30–70 and the build lands the blade (12.65) at about
**11.5–12** for 50, or leaves it at 12.65 and takes 56; Rick's call (§6).

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND

- On every blow Heartwood lands inside the window: `pin 1.0` on the foe
  (Grasp's write — `pinV` stored, `pin`/`pinMax` max'd; NOT `pinFree`, so
  `tickStasis` locks the weapon too), and `foe.apply("entangle", 1, f)` on
  top of the channel's 2. **`resolveHit`'s knock is applied and then
  frozen by the pin** — a rooted ball's `pinV` keeps the vector it was
  hit with and resumes on it a second later (the Stasis clamp rule: an
  upward resume is zeroed). Declare that order in the build.
- No damage change. Charge 15 (the relic's), window 8.
- Names kept: HEARTWOOD / ROOTFAST. **Card (72):** `Every blow roots the foe
  where it stands, ball and weapon, and entangles`.
- **Picture**: the root — the Tendril floor-root picture (four thorn shoots
  up the rim, `dark` with `core` tips, for the pin's length; the runic
  hexagon skipped); the sword's blade greens for the window with a leaf
  scale along it; a rooted foe carries the entangle tag. Cast: the greening
  runs hilt to tip over 0.3s. Field: leaf motes off the blade, both copies.
- **Sound**: cast — a green creak, 0.4s; a root — a short creak-and-crack
  (Tendril's root voice, reused, quieter at 1.0s than at the vine's
  longer holds); close — nothing.

# 5. BUILD BRIEF

Stage 0 control on 151 (`--arms A,SHIP,C --P rootFor=1.0`). Stage 1 —
freeze out, `f.ultRoot` in, the pin on hit; gate: ~3 roots a cast counted
as transitions, foe pinned ~40% of window frames, ~11.8 hits in windows,
relic ~52% at 12.65 (arm B at 1.0 — run it). Stage 2 — the entangle; gate:
entangle applied = 3 × hits in windows (2 channel + 1); relic ~56%. Stage 3
— the blade: Rick's target (§6); wide on 151. Stage 4 — picture, voice,
carry; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one
fight watched.

# 6. Open decisions

1. Rick's veto. 2. **The target**: Heartwood has been the roster floor; the
redesign reads 56 at its own blade. Leave the blade and lift the relic, or
bring the blade to 11.5–12 for 50 — Rick's. 3. Root length 1.0 vs 0.8
(52%) — a feel call; a full second is a beat the viewer can count.
