#!/usr/bin/env python3
"""One spoken line per fight: the fighters, by name, over the intro card.

Same engine as the Weapon Balls voiceover (Kokoro ONNX -- see
weapon-balls-voiceover.md for why Kokoro and why nothing else works from this
container), but NOT the same voice: Rick asked for a fantasy/mythic register in
place of bm_lewis's announcer read. **am_onyx is the pick**, and it beat the
earlier name-based choice of bm_fable on a measured sweep of five candidates
over the actual line:

    bm_fable   f0 120 Hz   3.7s     bm_george  f0 150 Hz
    bm_daniel  f0 128 Hz            am_fenrir  f0 137 Hz (rushed, 2.8s)
    am_onyx    f0  86 Hz   3.6s   <- deepest by 34 Hz, unhurried

Mythic is a register, not a nationality: onyx sits a clean third below every
other male voice and holds the slow, weighted pace of an epic trailer read.
Kokoro has no emotion control, so pitch and pace ARE the delivery, and the copy
does the rest: title, then the two names with a beat between them. Sits inside
the 4.0s intro card with air on both sides; lang stays en-us for this voice.

  python3 cinema_vo.py --a Gravemourn --b Dawnbringer --out vo.wav
"""
from __future__ import annotations
import argparse, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
MODEL = HERE / "kokoro-v1.0.onnx"
VOICES = HERE / "voices-v1.0.bin"
# bm_lewis, 2026-08-16. am_onyx won the first sweep on depth alone and is the
# FLATTEST of the deep voices (pitch IQR 3.7st) -- which is the "not engaging"
# Rick heard. Kokoro has no emotion control, so pitch movement IS the delivery:
# authority is median f0, engagement is f0 variation, and lewis wins both
# (85 Hz vs 89, 5.5st vs 3.7) while reading a full second shorter than fable.
VOICE, SPEED, SR = "bm_lewis", 1.00, 24000

# Relic names as the model should hear them. Anything absent is spoken as written.
# The pattern is COMPOUND SPLITTING: Kokoro runs "Ironhail" together into one
# mushy syllable cluster. Slagheart/Lastlight/Emberedge added for the v31
# vessel round -- same rule, and the two chain-only relics have never been
# spoken before. Aureole is left alone: it is a real word, not a compound.
SPOKEN = {
    "Gravemourn": "Grave mourn",
    "Farwarden": "Far warden",
    "Ironhail": "Iron hail",
    "Thornwake": "Thorn wake",
    "Lightkeeper": "Light keeper",
    "Slagheart": "Slag heart",
    "Lastlight": "Last light",
    "Emberedge": "Ember edge",
    # v38. Both are compounds and both are new: Kokoro runs "Threshmaw" into
    # one cluster and "Twinshade" into "twinshaid". Same rule as the other
    # eight -- split the compound and let the model breathe between the parts.
    "Threshmaw": "Thresh maw",
    "Twinshade": "Twin shade",
}


def normalise(text: str) -> str:
    for raw, spoken in SPOKEN.items():
        text = re.sub(rf"\b{re.escape(raw)}\b", spoken, text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="display name of relic A")
    ap.add_argument("--b", required=True, help="display name of relic B")
    ap.add_argument("--text", default=None,
                    help="override the whole line (names ignored)")
    ap.add_argument("--out", default="vo.wav")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--parts", default=None,
                    help="pipe-separated segments rendered as SEPARATE clips and "
                         "joined by --gaps. Punctuation does not control timing "
                         "in Kokoro -- '?...', '? ...' and '.' all give the same "
                         "contour -- so a pause has to be real silence, measured, "
                         "rather than punctuation and hope.")
    ap.add_argument("--gaps", default="",
                    help="comma-separated seconds between parts (len(parts)-1)")
    args = ap.parse_args()

    line = args.text or f"The Sundered Crown. {args.a}... versus {args.b}."
    from kokoro_onnx import Kokoro
    import soundfile as sf
    import numpy as np
    for p in (MODEL, VOICES):
        if not p.exists():
            raise SystemExit(f"missing {p} — see cinema_vo.py docstring / tts.py")
    k = Kokoro(str(MODEL), str(VOICES))
    voice = args.voice
    lang = "en-us" if voice.startswith("a") else "en-gb"

    def render(text):
        sm, sr = k.create(normalise(text), voice=voice, speed=SPEED, lang=lang)
        sm = np.asarray(sm, dtype=np.float32)
        loud = np.where(np.abs(sm) > 0.012)[0]
        if len(loud):
            sm = sm[max(0, loud[0]-int(sr*0.03)): min(len(sm), loud[-1]+int(sr*0.06))]
        return sm, sr

    if args.parts:
        parts = [p for p in args.parts.split("|") if p.strip()]
        gaps = [float(g) for g in args.gaps.split(",") if g.strip()] if args.gaps else []
        if len(gaps) != len(parts) - 1:
            raise SystemExit(f"! {len(parts)} parts need {len(parts)-1} gaps, got {len(gaps)}")
        chunks, sr, spans = [], None, []
        for i, part in enumerate(parts):
            y, sr = render(part)
            spans.append((sum(len(c) for c in chunks)/sr, len(y)/sr, part))
            chunks.append(y)
            if i < len(gaps):
                chunks.append(np.zeros(int(sr*gaps[i]), dtype=np.float32))
        samples = np.concatenate(chunks)
        line = " ".join(parts)
        for t0, d, txt in spans:
            print(f"[cinema_vo]   {t0:5.2f}s +{d:4.2f}s  {txt!r}")
    else:
        samples, sr = render(line)

    sf.write(args.out, samples, sr)
    print(f"[cinema_vo] {args.out}  {len(samples)/sr:.2f}s  voice={voice}  \"{line}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
