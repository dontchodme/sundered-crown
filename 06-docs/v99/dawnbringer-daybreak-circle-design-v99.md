# v99 — DAWNBRINGER / DAYBREAK, RICK'S CIRCLE. The cast puts the sun in the blade; the next blow that lands breaks the dawn WHERE IT LANDS, and a circle of sunlight spreads from that point and stays. A foe in the sunlight burns. Priced at the line's own feed; the blade stays 10.4.

**DESIGNED — Cowork, 2026-09-27. Build from §5 (the brief beside this file is the input); do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick rules from this file.** Lab: `tools/overlays/daybreak_circle.js`; runs in `06-docs/v99/runs/`. Supersedes v86's line (built and gated as `sc-daybreak-fx`; it does not ship).

## Why
Rick, after watching the built line (`06-docs/v97/DAYBREAK-REDESIGN-REQUEST-v97.md`): *"how about daybreak begins at a point of contact after a hit and grows in a circle from that point. lets also make the animation look more like sunlight glowing rather than the dul white. its also hard to tell what exactly it does by watching it."* And in Cowork, handing it over: *"make sure we are building something that the viewer can understand just by watching it."*

That second sentence is the design constraint, and it is the engine's own standing rule for ultimates (the `ultimates` comment in the renderer): *built so that a viewer who has never seen the game can say what happened … without a word of text and without knowing a single relic's name.* The line failed it for a reason that is measurable and is written into v97 §4a: a white wash at alpha 0.10, a 4-unit band, ticks that drew no number and made no sound, a SMITE tag on one tick in five. Everything the mechanic did was either invisible or indistinguishable from the smite the blade already applies. §4 below is written against that failure, mark by mark.

# 1. §1 (Cowork, from Rick's sentence)
> For a while the sun is in the blade. The first blow that lands breaks the dawn where it lands: a circle of sunlight spreads out from that point over two seconds, and stays for eight. An enemy standing in the sunlight is smitten and burned for as long as it stays there.

Three clauses: **the arming** (cast → the first landed blow; the charge is spent at the cast); **the sun** (a circle anchored to the contact point, r 0 → 200 over 2s, held to 8s from the contact, then set); **the feed** (smite +1 and 2 damage every 0.5s to a foe inside — the line's numbers exactly, so the two mechanics price against each other on the same feed). The caster gets nothing; the heal is still Rick's flag (v86 §3, +17).

# 2. THE HARNESS, AND THE CONTROL
`tools/ult_overlay.py`, redesign mode (arm `SHIP` = the sparks as shipped, live; every other arm has the relic's own ultimate off). **Runtime: Chromium 141.0.7390.37** (a Cowork cloud container, Playwright 1.56) — the same runtime v86 was priced on, and declared because the repo's pin is 151. **The control reproduces v86 to the digit** (`runs/ctl_trunk.*`, `sc-trunk`, 330 fights an arm): A 13.6%, SHIP 57.0%, B (the line) 54.8%, casts 3.34, foe lit 60.7%, 9.99 ticks, 19.98 damage a cast — against v86 §3's 13.6 / 57.0 / 54.8 / 3.34 / 61% / 10.0 / 20.0.

**The pricing base is `sc-corollary-c14`**, the chain tip before the line was built into the engine (so `SHIP` is still the sparks, and the 33 others are what Code builds against). Seeds 20 (660 fights an arm), two blocks (seed0 2207, 2317) on the taken arm and the base.

# 3. PRICED (`runs/`)
Charge 16 (the lab's clock; the engine's 14 — the batch ruling), blade 10.4, tick 2 damage + smite 1 every 0.5s, dur 8s from the contact, the arming until a blow lands.

```
arm                                              win (660)  block 2  pooled   casts  breaks  wait(s)  foe in  ticks  dmg/cast
A     no ultimate                                 17.6%      20.5     19.1
SHIP  the sparks                                  59.7%      61.7     60.7
B     the v86 line (dawn.js)                      53.8%      51.4     52.6     3.33                     60.5%   10.0   19.9
D     THE SUN r 200, grows 2s, holds  (TAKEN)     54.2%      51.2     52.7     3.35   3.21    2.96      56.0%    9.8   19.5
D     r 200, grows 1.5s                           54.1%                        3.35   3.22    2.93      58.2%   10.0   20.1
D     r 220, grows 1.5s                           55.0%                        3.34   3.19    2.96      63.1%   10.6   21.2
D     r 220, grows 2s                             55.0%                        3.34   3.20    2.95      60.6%   10.3   20.6
D     r 220, grows 4s                             47.7%                        3.37   3.22    2.96      51.3%    9.2   18.3
D     r 160, grows 1.5s                           49.8%                        3.39   3.24    2.93      47.1%    8.7   17.5
D     r 300, grows 1.5s                           60.2%                        3.30   3.16    2.92      79.1%   12.4   24.8
D     r 200, grows 1.5s, tick 3                   62.7%                        3.27   3.13    2.97      57.7%    9.8   29.5
D     r 180, grows 1.5s, tick 3                   61.2%                        3.30   3.15    2.90      51.6%    9.1   27.4
C     r 220, grows over the whole 8s              43.2%                        3.40   3.26    2.95      34.1%    7.0   14.1
C     r 300, grows over the whole 8s              48.2%                        3.36   3.22    2.92      45.3%    8.5   17.0
E     r 220, FOLLOWS the foe (a control)          63.5%                        3.25   3.12    2.93     100.0%   14.6   29.3
D     r 200, grows 2s, BLADE 11.2                 56.5%                        3.30   3.14    3.05      54.7%    9.5   19.0
```
`breaks` = suns per fight (nearly every cast breaks — the blade waits a mean 3.0s for its blow, and the few casts that never break are fights that end armed). `foe in` = the share of the sun's life the foe spends inside it.

**What the table says.**
- **The circle at r 200 IS the line's feed** — 9.8 ticks, 19.5 damage, the foe inside 56% of the time against the line's 60% — **and it prices where the line priced: 52.7% pooled against 52.6%.** The blade stays at 10.4 (Rick's ruling on the line: land where Cowork priced; 8 under the sparks is the same gap he accepted then). The slope is ~2.9 points a blade unit (11.2 → 56.5); parity with the sparks would want ~13, not taken.
- **Radius is the throttle: ~0.09 points a pixel** (160 → 49.8, 200 → 52.7–54.1, 220 → 55.0, 300 → 60.2). r 300 is the sparks' parity, and it is a diameter of 600 in a hall 520 wide — it would not read as a circle, it would read as "the floor". r 200 (diameter 400) is the largest that still reads as a shape with the hall around it. **If Rick wants the relic stronger, the tick's damage is the number to move, not the radius: tick 3 at r 200 is 62.7%** (+10, and a "3" floats where a "2" did).
- **Growing for the whole window is the line's mistake in a new shape** (arm C: the foe is inside only a third of the time, 43%). The sun comes up in 2s and is UP; two seconds is slow enough to watch the rim travel (100 px/s) and costs nothing against 1.5s (55.0 / 55.0 at r 220).
- **Anchoring is the counterplay, and it costs 8.5 points** (arm E, the same sun following the foe: 63.5%). That is what the viewer sees when the foe walks out of the light and stops burning — the design keeps it.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND
- **The mechanic, declared.** Cast: `f.ultSun = { armed: true, x, y, t, cd }`; the charge is spent; nothing resolves. Arming: the first blow Dawnbringer LANDS while armed (`resolveHit`, the blow's own hit point `hx, hy` — the lab used the foe's centre, within `ballR` of it, and the build's probe measures the difference) sets `x, y` and `t = 0`, `armed = false`. The sun: `r = 200 · min(1, t / 2)`; a foe is inside when `hypot(foe − centre) < r + ballR`. Every 0.5s while inside, on the window tickers' clock (it freezes through a hit stop, as `tickDawn` did): `foe.apply("smite", 1, side)` then `hurt(foe, 2, f)` — ward first, no beat, except the tick that kills, which files its own fatal `hit` beat (the engine's standing rule). The sun sets at `t ≥ 8` or when Dawnbringer dies. **A cast while the sun is up re-arms the blade; the next landed blow breaks a NEW dawn and the old one sets where it is (0.3s).** The arming has no time limit (a blade with the sun in it stays armed until it lands); the next charge runs from the cast as for every window ultimate. The caster gets nothing. `H` for the hall's clip is the live inset, as `drawDawn` read it.
- **Names kept: DAWNBRINGER / DAYBREAK** (Rick's redesign keeps them; the ult is a daybreak now more literally than the line was).
- **Card (71): `The next blow breaks the dawn where it lands; foes in the sunlight burn`.** Alternatives for Rick, same register: `Sunlight spreads from where the next blow lands; foes inside it burn` (68) · `Where the next blow lands the sun comes up; foes in its light burn` (66).

## 4.1 The picture — the four things a viewer must be able to say
The test for every mark below is the one Rick set, and each mark exists to make one sentence sayable with the card off: *he swung — where the sword hit, the sun came up — a circle of sunlight spread out from there — and the other ball burned whenever it was inside it.* The bloom gates from v86 still hold (they are §4.1b/c and they are this relic's), but **they are gates, not the design; legibility is measured FIRST and the bloom is measured after**, and where the two collide the fix is the shape (world pass, area, warm colour), never the strength. The line was built the other way round and Rick could not read it.

**Colour: SUNLIGHT, not sanctified white.** The school's `glow` is `#FFFFFF` and a white wash is what Rick called dull. The sun has its own three-stop palette, used nowhere else in the game: **core `#FFF6E2`** (the school's core — the only white, and only at the centre), **gold `#FFD98A`** (the rim, the numbers, the embers), **amber `#FFB347`** (the wash). Amber over a hall of `#07050C` reads as warm light; it also gives the bloom nothing white to find outside the core.

1. **ARMED — "the sun is in the blade"** (cast → the blow; a mean 3.0s). Nothing appears in the hall. The greatsword carries the sun: a gold (`#FFD98A`) edge-light along the blade's inset edge for the whole arming, breathing 1.5 Hz between alpha 0.45 and 0.8 (Corollary's rune-marks-on-the-blade precedent, v88 §6c — "the window's only tell"), and a short warm smear (the blade's own sweep, 0.12s, alpha 0.25, gold) behind the edge while it swings. Nothing on the floor yet — so that when the sun appears it is unmistakably FROM THE HIT and not from the cast.
2. **THE BREAK — "where the sword hit, the sun came up"** (the landed blow). At the hit point: a flash, core white, r 0 → 70 in 0.2s then gone by 0.3s — the ONLY emissive (`lighter`) mark in the whole set-piece, and the only one that may touch a ball, for a fifth of a second. The rim leaves the point at once and travels outward at 100 px/s, the wash filling behind it. The blow's own hit stop; no extra freeze (v80's rule holds).
3. **THE SUN IS UP — "a circle of sunlight"** (2s → 8s). Drawn in the **WORLD pass, right after the arena and under every emissive layer and both balls** (exactly where `drawDawn` sat; the balls are never painted — §4.1b), clipped to the live hall, hung off `f.ultSun` and NOT `m.ultFx` (open item 25: an opponent's cast must not erase it). Four parts, brightest to faintest:
   - **the rim**: a 3-unit ring in gold at alpha 0.8, with a 10-unit soft halo outward (gold → 0). It shimmers, alpha ±0.1 at 1.2 Hz. The rim is the mechanic's boundary and it must be the crispest thing on the floor: inside and outside is the whole verb.
   - **the core**: a small sun at the contact point — a disc r 14 in core white (source-over, alpha 0.9) — and **rays**: 10 shafts of amber from the core to 110–170 units, tapered, alpha 0.22, turning slowly (0.15 rad/s) with a 0.6 Hz breathing on their length. The rays are what makes it read as sunlight and not as a status zone; they are the "glowing" in Rick's sentence.
   - **the wash**: a radial gradient from gold at the core (alpha 0.35) to amber at the rim (0.20), source-over, breathing ±0.03 at 0.8 Hz — brightest where the sun came up, so it reads as light with a source and not as a pool. That is three times the line's 0.10, in colours that read as light on a near-black floor; the line's wash measured +0.085 luma over the floor and was not enough. **A concept sheet of the five moments, painted to these numbers: `05-reference/v99/daybreak-sun-sheet.png` (`tools/daybreak_sun_sheet.py`).** It is a painting, not the renderer; Rick judges the look on it and Code builds it in the engine.
   - **embers**: 24 slow amber motes drifting up through the lit disc (shellHash, no RNG), the line's 12 doubled and warmed.
   **The foe inside — "burned whenever it was inside it"**: on EVERY tick, three things at once: a number (`float(foe.x, foe.y − 50, 2, gold, 24)` — the echo's number, v88, and the mark the line never drew), a flash on its shell (a 2-unit gold ring at `ballR + 4` fading over 0.2s, drawn, presentation-only), and the tick's voice (4.2). Between ticks: 12 embers rising off its upper disc (the line's motes, in gold at 1.5x their alpha) and its smite bolts. The SMITE tag on the first tick of each stretch inside, as built. **The foe outside: nothing at all.** The absence is the lesson, and the rim flares locally when a ball crosses it (a 60-unit arc, 0.15s, alpha to 1.0) so the crossing is seen — Code's pick whether that stays, on the numbers.
   Dawnbringer inside: nothing, and the wash never paints its disc.
4. **SUNSET — "and then it went down"** (t = 8, a death, or a new dawn). The rim contracts to the core over 0.5s while the wash fades with it; the core winks out last (0.15s after). Never a cut-off: the line's fade at match end holds here too.

**Bloom, measured after, the same gates as before:** arena-mean lift ≤ +0.02 with the sun fully up (180 frames, six foes, both sides — v97's method); a ball's disc ≤ 0.90 at any frame, the white Aureole standing on the contact point included; **and the wash and rim measured with the chain off must give the same luma as with it on** (v97's "none of it is bloom" check). The break flash is the one mark allowed to raise a disc, and only to 0.90 and only for 0.3s. If the gate fails, the first knob is the core's area (r 14 → 10), then the flash's radius; the wash's alpha and the rim's are not knobs — they are the design.

## 4.2 The sound — heard, and heard stopping
Every voice re-struck (`_tone` holds nothing, §4.5), rendered in the OfflineAudioContext and measured as v88/v97 did, plain-number opts, `SFX.play` a no-op headless.
- **Armed:** a low warm tone, re-struck every 0.25s in phase (`.frequency.value` set — the v97 finding), rising a minor third over the first 3s and holding there; −16 dB under a blow. It is tension, and it STOPS on the break, which is half of what makes the break heard.
- **The break:** a bell — the old Daybreak voice was "a chord and a bell" (`w === "dawnbringer"` in the synth, retired in v97 4a) and the bell is the right register for a daybreak: one struck bell (modes 1 : 2.4 : 4.1) on ~880 Hz with a 30 ms mallet tick, audible ≥ 400 ms, peaking within 15 ms of the hit, −4 dB under a blow. On the same frame as the blow's own hit voice.
- **Up:** a quiet shimmer pad (two re-struck sines a fifth apart, 0.5s period, in phase), −20 dB under a blow, running while the sun is up. It is the floor under the ticks and it ends at sunset; it is not the line's eight-step scale, which climbed with a line that no longer climbs.
- **A tick — the one voice that carries the mechanic:** a short warm sizzle-chime, a 1.2 kHz bandpass burst (40 ms) over a 660 Hz sine (60 ms), −10 dB under a blow, once per tick, ON the tick's frame with the number. Two a second while the foe is inside, and silent the frame it steps out. Scour's ticks (`scour-tick`) are the precedent for a ticking voice.
- **Sunset:** the shimmer's top note held 0.4s and released over 380 ms (v97's STOP shape), only on a clock sunset — never on a death, never after the fight is over.
Levels are the lab's to set inside these bounds; the registers (bell for the break, sizzle for the tick) are the design.

# 5. BUILD BRIEF — `06-docs/v99/DAYBREAK-CIRCLE-BUILD-BRIEF.md`
Stages, gates and the legibility measurements are in the brief beside this file; in one line: stage 0 reproduces §3's A / SHIP / B / D on 151 on the chain tip; stage 1 the mechanic (the line's `tickDawn` and `kind:"dawn"` out, `ultSun` in), gated on breaks, ticks, damage, inside share and the relic at 10.4; stage 2 the blade confirmed; stage 3 the picture, voices and beat, gated on legibility numbers that can fail BEFORE the bloom numbers, `engine_ab` with Dawnbringer in, `render_ab` with a control that fails, `shell_identity`, `chain_audit`, one filmstrip and one clip for Rick.

# 6. Open decisions (Rick's)
1. **The card**: the 71 above, or one of the two alternatives.
2. **Strength**: as priced (52.7%, the line's own number, 8 under the sparks), or the tick to 3 (+10, reads a "3"). One number in the builder.
3. **The colour**: amber/gold/core as §4.1, or the school's white kept. Amber is the design's answer to "dull white"; his eye rules.
4. **The heal**: still one flag, still +17, still under the row (v86 §3). Not taken.
5. **The rim's crossing flare** and the arming smear are Code's picks on the numbers ("you pick i overrule"); everything else in §4.1 is specified and built as written.
