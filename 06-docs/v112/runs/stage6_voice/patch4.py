"""Scratch: what_cast for the second cut's pulses; the root rule's frame wording."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_voice_lab.py")
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


rep('''        what_cast = {
            "timber": "A timber (a sine and its 2.76 mode at 0.4, Canopy's and Tendril's wood) pulsed",
            "tri": "A triangle pulsed", "bough": "A woody knock (bandpass noise, Q 3) over a sine, pulsed",
            "sap": "The timber pulsed, each pulse giving a minor third,"}[C_["sp"]["pulse"]]
        cdesc = dict((n_, b_) for n_, _s, b_ in CAST_CANDIDATES)[C_["name"]]''',
    '''        cdesc = dict((n_, b_) for n_, _s, b_ in CAST_CANDIDATES)[C_["name"]]
        what_cast = cdesc[0].upper() + cdesc[1:]''')
rep('''            c_what=f"{what_cast}: {cdesc}.", ''', '''            c_what=f"{what_cast}.", ''')
rep('''    "wall tick's loudest; on the blow's frame (hit @ 11, with and without a "
    "crit, the worse): KEEP-ROOT >= 6 dB, KEEP-BLOW >= 6 dB, STAND-MIX >= 10 dB. "''',
    '''    "wall tick's loudest; on the blow's frame (the lightest, the median and the "
    "heaviest plain blow a root voice landed with in the wire run, and its "
    "heaviest crit; the worst of each): KEEP-ROOT >= 6 dB, KEEP-BLOW >= 6 dB, "
    "STAND-MIX >= 10 dB. "''')
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
s = p.read_text(encoding="utf-8")
rep('''        f"{info['c_pulsed']:.2f}), never a held tone. Green, not dry: its power centroid {info['c_cen']:.0f} Hz, "
        f"{info['c_green']:.2f}x the house's dry creak's (Canopy's wither), and it does not wither "
        f"({info['c_fall']:+.0f} cents first to last); no crack (that is the root's). Audible "''',
    '''        f"{info['c_pulsed']:.2f}), never a held tone. Green, not dry: its note, {info['c_note']:.0f} Hz, sits "
        f"under the lowest the house's dry creak (Canopy's wither) reaches, {info['c_dry']:.0f} Hz, and it does "
        f"not wither ({info['c_nfall']:+.0f} cents first to last); no crack (that is the root's). Audible "''')
rep('''c_cen=C_["cen"],
            c_green=C_["green"], c_fall=C_["fall"], ''', '''c_note=C_["note"],
            c_dry=dry_low, c_nfall=C_["nfall"], ''')
p.write_text(s, encoding="utf-8", newline="\n")
print("ok2")
