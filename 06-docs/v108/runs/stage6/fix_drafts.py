"""v108 stage 6: corrections to the doc drafts after re-reading the labs' reports (resumed session)."""
import pathlib
S = pathlib.Path(__file__).resolve().parent
def one(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:90])
    return s.replace(a, b, 1)
p = S / "doc_s6_draft.md"; t = p.read_text(encoding="utf-8")
t = one(t, "- **The picture lab's numbers** (the base, 9 fights, 76 frames at 1080x1920 through the post chain):",
           "- **The picture lab's numbers** (on the final, 9 fights, 76 frames at 540x960 through the post chain):")
t = one(t, """limbs 0.179, the dust 0.070, the motes 0.065. **Frame cost** (Electron, RTX 3070, the picture alone,
  interleaved): +0.2 to +0.6 ms median on a 6-9 ms frame. **Sim identity:** 14 whole fights, the final,
  the final-fx and both drawn, identical to the kill (steps, hashes, winner); the 1e-9 sim-write control
  differs on all 12 Ironhail fights with a landing and on neither without.""",
"""limbs 0.179, the dust 0.070, the motes 0.065. **Frame cost** (Electron 44, RTX 3070, interleaved A/B
  on the same state, the PC busy): the picture's own calls +0.0 to +0.6 ms at the median (+1.2 at most at
  p90) on 6-10 ms of drawing, whole-frame medians inside the noise (-2.5 to +2.1 ms). **Sim identity:**
  14 whole fights (12 with Ironhail, 2 without), every step hashed, the final against the picture link
  undrawn and drawn: identical in all four arms; the 1e-9 sim-write control differs on all 12 Ironhail
  fights and on neither without.""")
t = one(t, """  Portcullis's Sfx rows applied too, in either order, every arm renders alike.
""", """  Portcullis's Sfx rows applied too, in either order, every arm renders alike.
- **The voice lab's flags, printed and not gated** (Rick's to hear): Coldiron's close voice (an iron
  ring on the same A2 bar partials) registers 0.91 against this miss and 0.80 against this landing --
  heard only in an Ironhail v Coldiron fight, and its 0.4s ring is not a 0.13s thud; Portcullis's cast
  registers 0.83 against this miss; and 67% of landings arrive at the sunder cap (6: 1284 of 1906 in the
  lab's fights, 4016 of 5896 in the probe's), so the step-by-step pitch is heard mostly over a fresh
  foe's first five landings -- the design's cap, not the voice. The wavs to hear first:
  `05-reference/v108/ironhail-pick-sequence.wav` (the cast, landings 1-6 each with a miss, the blow) and
  `ironhail-pick-real-window(-without).wav` (the Cindercleave window with and without the three voices).
""")
p.write_text(t, encoding="utf-8", newline="\n")
print("draft ok", len(t))
