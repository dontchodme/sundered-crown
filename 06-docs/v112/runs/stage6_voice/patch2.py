"""Scratch: the second cut of the cast (see STATE.md step 4). Applied once to tools/heartwood_voice_lab.py."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_voice_lab.py")
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


# ---- candidates
i0 = s.index("CAST_CANDIDATES = [")
i1 = s.index('CENV = {')
s = s[:i0] + '''CAST_CANDIDATES = [
    ("1 GROAN", dict(pulse="timber", pitch="130", rate=(30, 42), env="swell"),
     "the FIRST CUT's green creak, kept as the evidence for the second: a timber (a 130 Hz sine and its 2.76 "
     "mode at 0.4) pulsed 30 -> 42 a second, swelling and settling"),
    ("2 KNOT", dict(pulse="sine", pitch="380", rate=(30, 42), env="swell"),
     "a 380 Hz sine pulsed 30 -> 42 a second, swelling and settling"),
    ("3 TIMBER", dict(pulse="timber2", pitch="360", rate=(30, 42), env="swell"),
     "a timber (a 360 Hz sine and its 2.76 mode at 0.2) pulsed 30 -> 42 a second, swelling and settling"),
    ("4 RISING", dict(pulse="sine", pitch="300 * Math.pow(4 / 3, Math.min(1, s / 0.3))", rate=(28, 40),
                      env="grow"),
     "a sine climbing a fourth, 300 -> 400 Hz, over the first 0.3 s (the greening runs hilt to tip in 0.3 s) "
     "and held, pulsed 28 -> 40 a second, growing then settling"),
    ("5 SAP", dict(pulse="sap", pitch="380", rate=(32, 32), env="swell"),
     "a 380 Hz sine, each pulse giving a minor third (a wet give), 32 a second"),
]
CPULSE = {
    "timber": ['this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });',
               'this._tone(t + s, { freq: f * 2.76, gain: a * 0.4, dur: 0.025, type:"sine" });'],
    "timber2": ['this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });',
                'this._tone(t + s, { freq: f * 2.76, gain: a * 0.2, dur: 0.025, type:"sine" });'],
    "sine": ['this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });'],
    "sap": ['this._tone(t + s, { freq: f, to: f * 0.84, gain: a, dur: 0.035, type:"sine" });'],
}
''' + s[i1:]

# ---- held control at the knot's note
rep('''def held_body(g, f=130, ind=10):''', '''def held_body(g, f=380, ind=10):''')
rep('''    """HELD: GROAN's timber held by re-striking''', '''    """HELD: KNOT's sine held by re-striking''')
rep('''         '  this._tone(t + s, { freq: f * 2.76, gain: a * 0.4, dur: 0.025, type:"sine" }).frequency.value = f * 2.76;',
''', '')

# ---- new measures
rep('''def _refuse(src, what):''', '''def alone(x, gap=20):
    """ALONE: the loudest millisecond of the voice high-passed at 1.5 kHz
    (bindweed_voice_lab's HF envelope) over the loudest millisecond at least
    `gap` ms from it, dB, and its time (ms after the event). A crack stands
    alone; a creak's clicks come as a train of near-equals."""
    import numpy as np
    e = hf_env(x)[:600]
    i = int(np.argmax(e))
    m = e.copy(); m[max(0, i - gap):i + gap + 1] = 0
    return db(float(e[i]) / max(float(m.max()), 1e-12)), float(i)


def note_info(x, a0_ms, gone_ms):
    """NOTE: PITCH (FFT peak, Hann, zero-padded, parabolic), 60-2000 Hz, over
    the audible span; NOTE-FALL: cents from PITCH over the first 100 audible ms
    to PITCH over the last 100; and that last PITCH."""
    g0 = T0 + a0_ms / 1000; g1 = T0 + gone_ms / 1000
    last = pitch(x, g1 - 0.1, g1, 60, 2000)
    return pitch(x, g0, g1, 60, 2000), cents(last, pitch(x, g0, g0 + 0.1, 60, 2000)), last


def _refuse(src, what):''')
rep('''    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, db, env_corr, fmt, pcm, write_wav,
    _comment)''', '''    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, db, env_corr, fmt, pcm, pitch, write_wav,
    _comment)''')

# ---- rule and why
rep('''"creak's rate, never a held tone); 'green': its power centroid <= 0.5x the "
    "house's dry creak's (Canopy's wither: an octave under it) and FALL-C >= -200 "
    "cents (it does not wither); a creak and NOT the root's crack: the crack test "
    "the root passes (STAND >= 10 dB and JUMP >= 10 dB) must fail. Register "''',
    '''"creak's rate, never a held tone); 'green': its NOTE under the lowest note the "
    "house's dry creak reaches (Canopy's wither, its last 100 audible ms) and "
    "NOTE-FALL >= -200 cents (it does not wither); a creak and NOT the root's "
    "crack: ALONE < 10 dB (the root's crack stands alone). Register "''')
rep('''    if M["green"] > 0.5: why.append(f"centroid {M['green']:.2f}x the dry creak's, not <= 0.5 (not green)")
    if M["fall"] < -200: why.append(f"falls {M['fall']:+.0f} c, not >= -200 (withers)")
    if M["stand"] >= 10 and M["jump"] >= 10:
        why.append(f"a crack at {M['crack_at']:.0f} ms (stands {M['stand']:+.0f}, jumps {M['jump']:+.0f} dB)")''',
    '''    if M["note"] > lev["dry_low"]:
        why.append(f"note {M['note']:.0f} Hz, not under the dry creak's lowest {lev['dry_low']:.0f} (not green)")
    if M["nfall"] < -200: why.append(f"note falls {M['nfall']:+.0f} c, not >= -200 (withers)")
    if M["alone"] >= 10: why.append(f"a crack at {M['alone_at']:.0f} ms (stands alone {M['alone']:+.1f} dB)")''')

# ---- cast measure
rep('''            M["crack_at"], M["stand"], M["jump"] = crack_info(x, M["a0"])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CAST_REGS''',
    '''            M["crack_at"], M["stand"], M["jump"] = crack_info(x, M["a0"])
            M["note"], M["nfall"], _nl = note_info(x, M["a0"], M["gone"])
            M["alone"], M["alone_at"] = alone(x)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CAST_REGS''')
rep('''                  f"{M['gone']:>6.0f}{M['mrate']:>6.0f}{M['pulsed']:>7.2f}{M['depth']:>6.1f}{M['cen']:>6.0f}"
                  f"{M['green']:>6.2f}{M['fall']:>7.0f}{M['stand']:>7.1f}{M['jump']:>6.1f}{max(r_.values()):>6.2f} "''',
    '''                  f"{M['gone']:>6.0f}{M['mrate']:>6.0f}{M['pulsed']:>7.2f}{M['note']:>6.0f}{M['nfall']:>7.0f}"
                  f"{M['alone']:>7.1f}{M['cen']:>6.0f}{M['fall']:>7.0f}{M['stand']:>7.1f}{max(r_.values()):>6.2f} "''')
rep('''f"{'cen':>6}{'green':>6}{'fall c':>7}{'stand':>7}{'jump':>6}{'reg':>6}")''',
    '''f"{'note':>6}{'nfall':>7}{'alone':>7}{'cen':>6}{'cfall':>7}{'stand':>7}{'reg':>6}")''')
rep('''{'depth':>6}"
              f"{'note':>6}''', '''"
              f"{'note':>6}''')
rep('''        dry_cen = ctl["dry-creak"]["cen"]
''', '''        dry_cen = ctl["dry-creak"]["cen"]
        dry_note, dry_nfall, dry_low = note_info(ctl["dry-creak"]["x"], ctl["dry-creak"]["a0"],
                                                 ctl["dry-creak"]["gone"])
        print(f"  the house's dry creak (Canopy's wither): note {dry_note:.0f} Hz, falling {dry_nfall:+.0f} cents to "
              f"{dry_low:.0f} Hz over its last 100 audible ms; centroid {dry_cen:.0f} Hz; ALONE "
              f"{alone(ctl['dry-creak']['x'])[0]:+.1f} dB (Tendril's root: {alone(RX['tendril-root'][0])[0]:+.1f})")
''')
rep('''        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)''', '''        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo, dry_low=dry_low)''')
rep('''f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}); the dry creak's centroid {dry_cen:.0f} Hz")''',
    '''f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}); green: a note under {dry_low:.0f} Hz")''')
rep('''        wsp = dict(g0_["sp"], pitch="180 * Math.pow(100 / 180, u)")''',
    '''        wsp = dict(rows_c[1]["sp"], pitch="450 * Math.pow(250 / 450, u)")''')
rep('''"    0 HELD     GROAN's timber held by re-striking''', '''"    0 HELD     KNOT's sine held by re-striking''')
rep('''"    0 WITHER   GROAN falling 180 -> 100 Hz''', '''"    0 WITHER   KNOT falling 450 -> 250 Hz''')
rep('''        want_fail = {"0 HELD": ("rate",), "0 WITHER": ("falls",), "0 DRY": ("centroid", "falls"),''',
    '''        want_fail = {"0 HELD": ("rate",), "0 WITHER": ("note falls",), "0 DRY": ("note ",),''')
rep('''        g0_ = rows_c[0]
''', '')
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
