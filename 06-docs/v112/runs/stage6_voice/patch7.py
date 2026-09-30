"""Scratch: THE PICKS in the docstring (no logic change)."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_voice_lab.py")
s = p.read_text(encoding="utf-8")
anchor = '''THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:'''
assert s.count(anchor) == 1
picks = '''THE PICKS, on Chromium 151.0.7922.34, sc-heartwood-b11 aff84a04b303a402, Tendril's
voices read from sc-tendril-fx eea0cde5536955b3, fight seeds 112601-112602 (148
fights), end to end 112651 (74):

  cast    5 RISING  a sine climbing a fourth, 300 -> 400 Hz, over the first 0.3 s
                    (the greening runs hilt to tip in 0.3 s) and held, pulsed 28 ->
                    40 a second, growing then settling. RATE 33 a second, PULSED
                    0.65; NOTE 356 Hz, under the dry creak's lowest 420 (SHIFT +130
                    c: it grows); ALONE +0.3 dB (no crack); audible 390 ms; TOP -2.9
                    dB re the hit @ 11, +16.8 dB re the wall; register at most 0.75
                    (the dry creak). KNOT (0.73), TIMBER (0.74) and SAP (0.73) tie
                    it to 0.05 and lose on calls (14, 28) or the order listed (SAP,
                    13); DEEP loses the register (0.78, the death voice); GROAN out
                    (the blow, 0.84).
  root    3 G-7dB   Tendril's root body verbatim, g 0.5179 -> 0.2313: TOP 0.0698,
                    -4.1 dB re Tendril's (the chain compresses a 7 dB gain step to
                    4.1), -4.3 dB re the hit @ 11, +14.8 dB re the wall; REG 0.99
                    and ENV-CORR 0.99 against Tendril's; the crack at 206 ms
                    standing +46.4 dB; on the blow's frame (blows of 0, 16 and 32
                    and a crit of 66) the root keeps +6.9 dB in its 50 Hz
                    third-octave, the blow +22.9 dB in its own, the crack +44.0 dB
                    in the mix; register at most 0.46 (the cast). G-3dB and G-5dB
                    out (-1.6 / -2.8 dB: not 3 dB quieter); G-9dB and G-11dB out
                    (under the heaviest crit: +5.8 / +4.6 dB).
  close   nothing (the design): no voice from tickRootfast in 637 windows.

  In play (148 fights; 637 windows -- 557 closed by the clock, 17 by the
  caster's death, 63 by the fight's end): 637 casts and 637 cast voices; 2363
  blows in a window, 2318 rooted (1282 new holds, 1036 re-roots) and 2318 root
  voices, none on the 45 killing blows; 148/148 fights identical and every other
  SFX call identical in order and opts; the sim-write control 11/148. The root
  voices landed with blows of 0-32 (median 16) and crits to 66. In a real window
  (v Twinshade, 112602, 13 rooted blows) the cast stands +21.1 dB over
  everything else on its frame in its own third-octave (400 Hz) and the roots
  +10.9 dB (median) in theirs (50 Hz), five of the thirteen under +3 dB where the
  fight is loud. End to end: 74/74 fights identical to the unpatched page's with
  every voice count exact, and the two voices through the patched page's own
  SFX.play equal the candidates to 6e-8. Main-thread cost a call: cast 0.5 ms,
  root 0.7 ms (the hit's 0.1).

  Carried (in scratch, not a gate of this lab): heartwood_build.py's four
  stages onto sc-ironhail-fxout (39 relics, Tendril's voices on it) and the two
  rows applied unchanged: each anchor once, 76/76 fights identical to the
  carried link's, every voice count exact; there the tip's own
  ult/bindweed-root equals the body this row reuses (6e-8).

  Outside the rule's scope (printed for Rick, not gated -- the house's cast rule
  reads the school and the type): against every ult voice on that tip (101
  casts and sub-voices), RISING sits over 0.80 with five other relics' voices
  (Lastlight's cold 0.88, Cindercleave's jet 0.86, Foregone's reverse 0.81,
  Gravemourn's hand and Ironhail's cast 0.80); KNOT and SAP with three, TIMBER
  eight, DEEP thirteen (Threshmaw's cast 0.94), GROAN twenty-two. The reused
  root, Tendril's own voice, sits 0.81-0.83 against Twinshade's, Shroudmaul's,
  Grudgebearer's and Cindercleave's casts.

'''
s = s.replace(anchor, picks + anchor, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
