"""Scratch: the docstring for the second cut (no logic change)."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_voice_lab.py")
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


rep('''  * THE BLOW IS THE BLOW: the root lands on the frame of the blow that made
    it, with the blow's own voice (the hit @ 11, Heartwood's blade). It is
    never over that blow (TOP <= the hit @ 11's quietest draw: the ceiling
    Canopy's cast and Tendril's root took), the blow keeps its own
    third-octave >= 6 dB over the root alone, and the root keeps its own
    third-octave >= 6 dB over the blow alone, its crack standing clear after
    it (the crack lands 0.2 s in, when the blow has died).
  * "A GREEN CREAK": a CREAK is the house's (ironwood_voice_lab,
    bindweed_voice_lab): a train of pulses at a creak's rate (stick-slip) --
    RATE 17-83 a second and PULSED >= 0.40 -- never a held tone. GREEN is
    living wood, read against the house's DRY creak (Canopy's wither, "a dry
    creak falling in pitch", `ult/ironwood-wither`): the green creak sits at
    least an octave under it (power centroid <= 0.5x the dry creak's) and
    does not wither (its centroid does not fall more than 200 cents first
    100 audible ms -> last 100). A CREAK, NOT THE ROOT'S CRACK: the root is
    the creak-AND-crack, so the cast carries no crack (the root's crack test
    must FAIL on it). "0.4s": AUDIBLE 330-470 ms, GONE <= 470 ms (the band
    Tendril's wither took for its "0.4s").''',
    '''  * THE BLOW IS THE BLOW: the root lands on the frame of the blow that made
    it, with the blow's own voice. It is never over Heartwood's blow (TOP <=
    the hit @ 11's quietest draw: the ceiling Canopy's cast and Tendril's root
    took, at the blade); and at the blows it really lands with -- the
    lightest, the median and the heaviest plain blow and the heaviest crit a
    root voice landed with in the wire run (the chaos jitter, the foe's
    damage-taken and the crit's x2.1 put them far from 11) -- the blow keeps
    its own third-octave >= 6 dB over the root alone, and the root keeps its
    own third-octave >= 6 dB over the blow alone, its crack standing clear
    after it (the crack lands 0.2 s in, when the blow has died).
  * "A GREEN CREAK": a CREAK is the house's (ironwood_voice_lab,
    bindweed_voice_lab): a train of pulses at a creak's rate (stick-slip) --
    RATE 17-83 a second and PULSED >= 0.40 -- never a held tone. GREEN is
    living wood, read against the house's DRY creak (Canopy's wither, "a dry
    creak falling in pitch", `ult/ironwood-wither`): the green creak's NOTE
    sits under the lowest note the dry creak reaches (its last 100 audible
    ms, 420 Hz: lower than the dry creak everywhere it goes), and it does not
    wither (its note does not fall more than 200 cents, first 100 audible ms
    -> last 100). A CREAK, NOT THE ROOT'S CRACK: the root is the
    creak-AND-crack, so the cast carries no crack: its loudest high-passed
    millisecond does not stand ALONE (< 10 dB over every other one 20 ms or
    more away; the root's crack stands 29 dB). "0.4s": AUDIBLE 330-470 ms,
    GONE <= 470 ms (the band Tendril's wither took for its "0.4s").''')
rep('''  HELD         GROAN's timber held by re-striking at its own cycles, no
               stick-slip: as a cast it must fail CREAK
  WITHER       GROAN falling 180 -> 100 Hz: as a cast it must fail GREEN''',
    '''  HELD         KNOT's 380 Hz sine held by re-striking at its own cycles, no
               stick-slip: as a cast it must fail CREAK
  WITHER       KNOT falling 450 -> 250 Hz: as a cast it must fail GREEN''')
rep('''  * New here, each with a control that can come back wrong:
      GREEN   the power centroid (basic's CEN) over the dry creak's, and
              FALL-C: cents from CENTROID 60 Hz-4 kHz of the first 100 audible
              ms to that of the last 100
      REUSED  REG against Tendril's root (draw for draw) and ENV-CORR against
              it (render.py's draw): both >= 0.95
      ON ONE FRAME   the root and the hit @ 11 rendered together (without and
              with a crit): KEEP-ROOT = the mix over the blow alone in the
              root's own third-octave over 0.35 s; KEEP-BLOW = the mix over
              the root alone in the blow's own third-octave over 0.15 s;
              STAND-MIX = the root's crack millisecond in the MIX over the p90
              of the mix's HF envelope 60-10 ms before it

THE PICKS: filled in by the run that shipped the rows (see __doc__ tail).
''', '''  * New here, each with a control that can come back wrong:
      NOTE    zenith_voice_lab's PITCH (FFT peak, Hann, zero-padded,
              parabolic), 60-2000 Hz, over the audible span; NOTE-FALL: cents
              from PITCH over the first 100 audible ms to PITCH over the last
              100 (the dry creak: 534 Hz, -861 c, down to 420 Hz)
      ALONE   the loudest millisecond of the voice high-passed at 1.5 kHz
              (bindweed_voice_lab's HF envelope) over the loudest millisecond
              20 ms or more away from it, dB. Tendril's root +29.4, the dry
              creak +2.3, a creak's click train 0-2
      REUSED  REG against Tendril's root (draw for draw) and ENV-CORR against
              it (render.py's draw): both >= 0.95
      ON ONE FRAME   the root and a blow rendered together, at each blow the
              wire run heard (above): KEEP-ROOT = the mix over the blow alone
              in the root's own third-octave over 0.35 s; KEEP-BLOW = the mix
              over the root alone in the blow's own third-octave over 0.15 s;
              STAND-MIX = the root's crack millisecond in the MIX over the p90
              of the mix's HF envelope 60-10 ms before it
      Printed, not gated: the power centroid (CEN) and the first cut's FALL-C
      (cents from CENTROID 60 Hz-4 kHz, first 100 audible ms to the last).

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules were written
before the first table (run on one fight seed); that table showed an instrument
blind to what it was built to see, a second instrument reading a steady creak
as falling, and a reading of "green" that no creak could meet without sitting
in the verdant school's own register. Each was changed ONCE, for the reason
given, before the picks:
  * NOT A CRACK was first "the root's crack test (STAND >= 10 dB and JUMP >=
    10 dB) must fail", and every creak PASSED it (STAND +12..+21 dB): a click
    train's 1 ms HF envelope is mostly gap, so the p90 before the loudest
    click is the gap, not the other clicks. ALONE compares the loudest
    millisecond with the loudest OTHER one: the creaks read 0-2 dB, Tendril's
    root +29.4 (the CRACK control, which must fail it, does).
  * GREEN was first "the power centroid <= 0.5x the dry creak's (an octave
    under it) and FALL-C >= -200 cents". FALL-C read the steady 130 Hz GROAN
    as falling -181 c and a steady 110 Hz triangle -443 c (the pulses' clicks
    brighten the head), against -389 c for a creak that really fell 180 ->
    100 Hz: it cannot tell a steady creak from a withering one. And every
    construction under the octave (19 of them, 90-250 Hz: sine, timber,
    triangle, sawtooth, square, friction grains; stage6-voice/explore*.txt in
    the batch scratch) put its note where the verdant school's own casts live
    -- Thornwake's creak-and-cinch 0.82-0.90, Vinesower 0.76-0.84, the blow
    0.78-0.92 -- or, harmonic-rich, crossed Emberedge and Paradox's pin
    instead. The octave was this lab's number, not the design's: GREEN now
    reads the creak's NOTE against the whole range the dry creak covers
    (under the lowest note it reaches), and NOTE-FALL replaces FALL-C. GROAN,
    the first cut's pick, is kept in the table as the evidence (it fails the
    register; its NOTE-FALL at 130 Hz is not evidence either way -- a 35 ms
    pulse holds five cycles and the pitch smears).
  * THE FRAME was first the hit @ 11 with and without a crit; the wire run
    showed the root voices landing with blows of 0-31 (median 16) and crits to
    64, so the frame checks run at the blows the run heard.
''')
rep('''    hex-snap, fork, vine x4, loose x3, aegis, the four scour voices, six ult
    sub-voices and every other relic's cast) must be unchanged;''',
    '''    hex-snap, fork, vine x4, loose x3, aegis, the four scour voices, seven ult
    sub-voices -- `ult/bindweed-root`, rune-crack on this base, among them --
    and every other relic's cast) must be unchanged;''')
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
