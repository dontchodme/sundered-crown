# ANIME TRAILER (trailer 2) — v116

**Cowork, 2026-09-29.** Rick, in Cowork: *"while trailer 1 builds. can you make
an anime style trailer? please fully animate it (no actual gameplay clips) and
give it over the top anime style fight sequences"*. This is not trailer 1 —
that one belongs to another session and nothing here touches it.

---

## 1. What it is

```
file        07-shorts/v116/anime-trailer.mp4   (gitignored, like every clip)
length      42.5 s — 102 beats at 144 bpm, 10 frames a beat
picture     1080x1920, 24 fps (anime's rate; the relics animate ON TWOS)
            H.264 High, CRF 15, -tune animation, yuv420p, ~55 MB
sound       AAC 256k, 48 kHz stereo, -14.0 LUFS integrated, -1.4 dBTP
source      tools/anime_trailer/   (canvas scenes + Playwright + numpy/scipy)
rebuild     python tools/anime_trailer/build.py --out 07-shorts/v116/anime-trailer.mp4
```

**Every frame is drawn and every sound is synthesized.** No gameplay capture,
no samples, no third-party music — there is nothing in it to license. The
build is deterministic: a from-scratch rebuild decoded frame-identical to the
delivered file (framemd5 of all 1020 frames).

The build needs the **Noto Sans CJK JP** font (Black) installed. `lib.js`
falls back to Yu Gothic / Arial Black on Windows so a render stays legible
without it, but it will not match the delivered file.

## 2. The cut

```
time         beats    scene
0.0 - 3.3    0-8      COLD OPEN. Frame one is already moving: Thornshear and
                      Duskreave rush in on speed lines, clash at 0.42s (ink
                      impact frames, 決戦), grind, blast apart. "ONE CROWN."
3.3 - 6.7    8-16     THE CROWN cracks three times and shatters into seven
                      shards, one per school. "SHATTERED INTO SEVEN."
6.7 - 10.0   16-24    THE SEVEN — one relic a beat, one of every school AND
                      every weapon: Dawnbringer, Ravelbone, Cindercleave,
                      Thornshear, Gloamwire, Paradox, Watchlight. "SEVEN SCHOOLS."
10.0 - 15.0  24-36    THE WINNOWING. Gloamwire's Crossweave; Thornshear dodges,
                      cut-in, blades to leaf kunai, the fan ricochets and grows
                      on every wall, the last legs land, the big one puts
                      Gloamwire through the wall.
15.0 - 20.0  36-48    BREACH / SENTINEL. Cindercleave tears three vents that
                      spit heat; Vesper charges and sweeps the beam; the far
                      end detonates.
20.0 - 25.0  48-60    SCOUR. Culverin lobs shells; Duskreave's tornado eats
                      them, paths along the floor, drags Culverin into seven
                      ticks a second, collapses.
25.0 - 27.5  60-66    GARROTE. Ravelbone spins up the wire; Shroudmaul comes
                      in reaching with its hand, is held, the hammer comes
                      round, the ring goes up.
27.5 - 30.8  66-74    MONTAGE, a beat each: Corona, Crucible, Radiance, Gyre,
                      Convergence, Bloom, Backlash, Beacon.
30.8 - 35.8  74-86    THE REMATCH. VS card; "TO THE LAST DROP." (the liquid in
                      the glass is the life); the charge; HALF A BEAT OF TOTAL
                      SILENCE; the clash — ten ink frames, the screen cracks,
                      white.
35.8 - 42.5  86-102   THE CROWN re-forms from the seven. SUPER WEAPON BALL /
                      THE SUNDERED CROWN / 砕かれた王冠. "WHO TAKES THE CROWN?"
                      "FOLLOW TO FIND OUT".
```

## 3. What it depicts — and what it does not

**Every ultimate on screen is the shipped ultimate's own verb**, from the build
of record (`sc-nightglass-fx`), and all eighteen relics shown are in it. The
tips each scene was drawn from are quoted at the top of its block in
`s_fights.js` / `s_end.js`.

**The choreography is staging, not mechanics** — who fights whom, Scour
eating Culverin's shells, Vesper's beam carrying Cindercleave to its far end.
Scale is exaggerated on purpose (Scour's funnel stands taller than the
design's third of the arena). **No mechanic was designed for this**; nothing
here is an input to a build.

The anime grammar: ink impact frames (the picture thresholded to black and
white, sometimes tinted), 集中線 focus lines, speed lines, smears and
afterimages, cut-ins with a 奥義 card, screentone, characters on twos, the
silent beat before the final hit, a screen crack. The game's glass-and-liquid
orb is kept, inked and cel-shaded. Japanese used: 決戦 *decisive battle*,
奥義 *secret technique* (the special-move card), 砕かれた王冠 *the shattered
crown*.

## 4. Checks, and the controls that can fail them

```
check                              result                     control
A/V offset, encoded vs source mix  0 samples (cross-corr)     +100 ms copy reads +100.00
isolated hits, picture vs sound    -2 ms at beats 1, 11, 81.5   +120 ms shift flagged OUT
loudness                           -14.0 LUFS, -1.4 dBTP      —
tone                               low end measured +8 dB over pink before EQ;
                                   shelved -5 dB <120 Hz for phone speakers
rebuild                            framemd5 identical          —
page errors during render          0 of 1020 frames            —
```

Sound effects are placed from the picture's own cue list
(`capture.py --cues`), so a hit and its sound are the same number. At the five
busier hits (4, 33.5, 45, 57, 63.5) the two detectors (peak and onset)
disagree with each other by up to 180 ms because other onsets sit in the
window, so those are NOT independently confirmed beyond the shared number.

Safe zones: the titles sit inside TikTok's right rail and caption band. **In
some wide fight shots the arena's bottom strip still passes under the
caption.**

**NOT CHECKED: nobody has heard it or watched it at speed.** The score is
synthesized and was judged only by measurement — spectrum, loudness, envelope,
the silent gap. A change that passes the suite and was never watched is
half-tested; watch it before it is posted.

## 5. Open decisions — Rick's

1. **The title** reads SUPER WEAPON BALL, as the in-game footer does. The
   project is also called Super Weapon Balls. Which one is the brand?
2. **No voiceover.** Kokoro is not on DESKTOP-DERRAFT (`tools/FETCH-KOKORO.md`).
   A narrator line or called-out attack names can go in; it is a re-mix, not a
   re-render.
3. **The leads** — Thornshear and Duskreave open and close it. Swap either?
4. **The end card** says FOLLOW TO FIND OUT. When the Crown Cup has a name, the
   card can plug it.
