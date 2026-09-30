"""Scratch: SHIFT for 'does not wither' (NOTE-FALL smears below ~200 Hz); the DEEP candidate
(the one construction under the first cut's octave that passes every register)."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_voice_lab.py")
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


# ---- the DEEP candidate
rep('''    ("2 KNOT", dict(pulse="sine", pitch="380", rate=(30, 42), env="swell"),
     "a 380 Hz sine pulsed 30 -> 42 a second, swelling and settling"),
    ("3 TIMBER", dict(pulse="timber2", pitch="360", rate=(30, 42), env="swell"),
     "a timber (a 360 Hz sine and its 2.76 mode at 0.2) pulsed 30 -> 42 a second, swelling and settling"),
    ("4 RISING", dict(pulse="sine", pitch="300 * Math.pow(4 / 3, Math.min(1, s / 0.3))", rate=(28, 40),
                      env="grow"),
     "a sine climbing a fourth, 300 -> 400 Hz, over the first 0.3 s (the greening runs hilt to tip in 0.3 s) "
     "and held, pulsed 28 -> 40 a second, growing then settling"),
    ("5 SAP", dict(pulse="sap", pitch="380", rate=(32, 32), env="swell"),
     "a 380 Hz sine, each pulse giving a minor third (a wet give), 32 a second"),
]''', '''    ("2 DEEP", dict(pulse="sine", pitch="90", rate=(30, 42), env="swell"),
     "a 90 Hz sine groan pulsed 30 -> 42 a second, swelling and settling -- the one construction under the "
     "first cut's octave that clears every register"),
    ("3 KNOT", dict(pulse="sine", pitch="380", rate=(30, 42), env="swell"),
     "a 380 Hz sine pulsed 30 -> 42 a second, swelling and settling"),
    ("4 TIMBER", dict(pulse="timber2", pitch="360", rate=(30, 42), env="swell"),
     "a timber (a 360 Hz sine and its 2.76 mode at 0.2) pulsed 30 -> 42 a second, swelling and settling"),
    ("5 RISING", dict(pulse="sine", pitch="300 * Math.pow(4 / 3, Math.min(1, s / 0.3))", rate=(28, 40),
                      env="grow"),
     "a sine climbing a fourth, 300 -> 400 Hz, over the first 0.3 s (the greening runs hilt to tip in 0.3 s) "
     "and held, pulsed 28 -> 40 a second, growing then settling"),
    ("6 SAP", dict(pulse="sap", pitch="380", rate=(32, 32), env="swell"),
     "a 380 Hz sine, each pulse giving a minor third (a wet give), 32 a second"),
]''')
rep('''        wsp = dict(rows_c[1]["sp"], pitch="450 * Math.pow(250 / 450, u)")''',
    '''        wsp = dict(rows_c[2]["sp"], pitch="450 * Math.pow(250 / 450, u)")''')

# ---- SHIFT
rep('''def _refuse(src, what):''', '''def shift(x, a0_ms, gone_ms, lo=60.0, hi=4000.0):
    """SHIFT: cents that the voice's last 100 audible ms sit from its first 100
    -- the lag (12.5 c steps, parabolic) that best correlates the two windows'
    log power spectra (Hann, zero-padded, each point the mean power in a
    1/12-octave window on a 1/96-octave grid, lo-hi). A steady creak reads ~0
    whatever its note; a creak that falls reads its fall."""
    import numpy as np
    NF = 1 << 16
    fr = np.fft.rfftfreq(NF, 1 / SR)
    grid = lo * 2 ** (np.arange(0, int(96 * math.log2(hi / lo)) + 1) / 96)
    l1 = np.searchsorted(fr, grid * 2 ** (-1 / 24)); h1 = np.searchsorted(fr, grid * 2 ** (1 / 24))

    def spec(a, b):
        seg = x[int(a * SR):int(b * SR)]
        P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), NF)) ** 2
        cs = np.concatenate([[0.0], np.cumsum(P)])
        v = (cs[h1] - cs[l1]) / np.maximum(h1 - l1, 1)
        return 10 * np.log10(v + v.max() * 1e-6)
    g0 = T0 + a0_ms / 1000; g1 = T0 + gone_ms / 1000
    A, B = spec(g1 - 0.1, g1), spec(g0, g0 + 0.1)
    L = list(range(-128, 129))
    best = []
    for s_ in L:
        u, v = (A[:s_], B[-s_:]) if s_ < 0 else ((A[s_:], B[:-s_]) if s_ > 0 else (A, B))
        best.append(float(np.corrcoef(u, v)[0, 1]))
    i = int(np.argmax(best)); d = 0.0
    if 0 < i < len(best) - 1:
        y0, y1, y2 = best[i - 1], best[i], best[i + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if den else 0.0
    return -(L[i] + d) * 12.5


def _refuse(src, what):''')
rep('''    if M["nfall"] < -200: why.append(f"note falls {M['nfall']:+.0f} c, not >= -200 (withers)")''',
    '''    if M["shift"] < -200: why.append(f"shifts {M['shift']:+.0f} c, not >= -200 (withers)")''')
rep('''            M["alone"], M["alone_at"] = alone(x)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]''', '''            M["alone"], M["alone_at"] = alone(x)
            M["shift"] = shift(x, M["a0"], M["gone"])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]''')
rep('''                  f"{M['gone']:>6.0f}{M['mrate']:>6.0f}{M['pulsed']:>7.2f}{M['note']:>6.0f}{M['nfall']:>7.0f}"''',
    '''                  f"{M['gone']:>6.0f}{M['mrate']:>6.0f}{M['pulsed']:>7.2f}{M['note']:>6.0f}{M['shift']:>7.0f}"
                  f"{M['nfall']:>7.0f}"''')
rep('''f"{'note':>6}{'nfall':>7}{'alone':>7}''', '''f"{'note':>6}{'shift':>7}{'nfall':>7}{'alone':>7}''')
rep('''    "house's dry creak reaches (Canopy's wither, its last 100 audible ms) and "
    "NOTE-FALL >= -200 cents (it does not wither); a creak and NOT the root's "''',
    '''    "house's dry creak reaches (Canopy's wither, its last 100 audible ms) and "
    "SHIFT >= -200 cents (it does not wither); a creak and NOT the root's "''')
rep('''        want_fail = {"0 HELD": ("rate",), "0 WITHER": ("note falls",), "0 DRY": ("note ",),''',
    '''        want_fail = {"0 HELD": ("rate",), "0 WITHER": ("shifts",), "0 DRY": ("note ", "shifts"),''')
rep('''        print(f"  the house's dry creak (Canopy's wither): note {dry_note:.0f} Hz, falling {dry_nfall:+.0f} cents to "
              f"{dry_low:.0f} Hz over its last 100 audible ms; centroid {dry_cen:.0f} Hz; ALONE "''',
    '''        print(f"  the house's dry creak (Canopy's wither): note {dry_note:.0f} Hz, falling {dry_nfall:+.0f} cents to "
              f"{dry_low:.0f} Hz over its last 100 audible ms (SHIFT "
              f"{shift(ctl['dry-creak']['x'], ctl['dry-creak']['a0'], ctl['dry-creak']['gone']):+.0f} c); centroid "
              f"{dry_cen:.0f} Hz; ALONE "''')
# the arm comment: the shift, not the note fall
rep('''c_nfall=C_["nfall"], ''', '''c_nfall=C_["shift"], ''')

# ---- docstring
rep('''    ms, 420 Hz: lower than the dry creak everywhere it goes), and it does not
    wither (its note does not fall more than 200 cents, first 100 audible ms
    -> last 100). A CREAK, NOT THE ROOT'S CRACK: the root is the''',
    '''    ms, 420 Hz: lower than the dry creak everywhere it goes), and it does not
    wither (SHIFT >= -200 cents: its last 100 audible ms do not sit more than
    200 cents under its first 100). A CREAK, NOT THE ROOT'S CRACK: the root is the''')
rep('''      NOTE    zenith_voice_lab's PITCH (FFT peak, Hann, zero-padded,
              parabolic), 60-2000 Hz, over the audible span; NOTE-FALL: cents
              from PITCH over the first 100 audible ms to PITCH over the last
              100 (the dry creak: 534 Hz, -861 c, down to 420 Hz)''',
    '''      NOTE    zenith_voice_lab's PITCH (FFT peak, Hann, zero-padded,
              parabolic), 60-2000 Hz, over the audible span, and over the last
              100 audible ms (the dry creak: 534 Hz, down to 420 Hz)
      SHIFT   cents that the last 100 audible ms sit from the first 100: the
              lag (12.5 c steps, parabolic) that best correlates the two
              windows' log power spectra, 60 Hz-4 kHz, each point the mean in a
              1/12-octave window on a 1/96-octave grid (ironwood_voice_lab's
              CRACK, run between two windows of one voice). A steady creak
              reads ~0 at any note; WITHER must read its fall''')
rep('''      Printed, not gated: the power centroid (CEN) and the first cut's FALL-C
      (cents from CENTROID 60 Hz-4 kHz, first 100 audible ms to the last).''',
    '''      Printed, not gated: the power centroid (CEN), NOTE-FALL (cents from
      PITCH over the first 100 audible ms to the last 100) and the first cut's
      FALL-C (the same from CENTROID 60 Hz-4 kHz).''')
rep('''  * GREEN was first "the power centroid <= 0.5x the dry creak's (an octave
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
    pulse holds five cycles and the pitch smears).''',
    '''  * "DOES NOT WITHER" was first FALL-C (the CENTROID's fall), which read the
    steady 130 Hz GROAN as falling -181 c and a steady 110 Hz triangle -443 c
    (the pulses' clicks brighten the head) against -389 c for a creak that
    really fell 180 -> 100 Hz: it cannot tell a steady creak from a withering
    one. The first replacement tried, NOTE-FALL (PITCH's fall), smears below
    ~200 Hz (a 35 ms pulse holds a few cycles: the steady 130 Hz GROAN -338 c,
    a steady 90 Hz groan -608 c). SHIFT compares the two windows' whole
    spectra instead; both others are printed.
  * GREEN was first "the power centroid <= 0.5x the dry creak's (an octave
    under it)". Of the constructions tried under the octave (33 of them,
    90-290 Hz: sine, timber, triangle, sawtooth, square, friction grains, a
    wet give; stage6-voice/explore*.txt in the batch scratch), 32 put their
    energy where the verdant school's own casts and the blow live --
    Thornwake's creak-and-cinch 0.82-0.90, Vinesower 0.76-0.84, Paradox's pin
    0.83-0.84, the blow 0.78-0.92 -- and the one that cleared every register,
    a 90 Hz groan (DEEP, now a candidate), clears the death voice by 0.02.
    The octave was this lab's number, not the design's, and it asks more than
    "green" does: green wood is heavier and softer than seasoned wood, not a
    register apart. GREEN now reads the creak's NOTE against the whole range
    the dry creak covers -- under the lowest note it reaches -- which DEEP
    still passes, so the octave's one survivor stays in the race and the
    written tiebreak (the most distinct register) decides. GROAN, the first
    cut's pick, stays in the table as the evidence (it fails the register).''')
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
