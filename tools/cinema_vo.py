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


# THE DEFAULT LINE, IN ONE PLACE. shorts_build.py built these three parts and
# their two gaps inline, and the app needed the same line for its preview --
# two constructions of one thing, which is how the preview ends up sounding
# like something the short does not. Both call `--hook` now.
#
# THE GAPS ARE THE LINE'S TIMING AND THEY ARE NOT PUNCTUATION. Kokoro gives
# "?...", "? ..." and "." the same contour, so every beat here is real silence
# between separately rendered clips.
HOOK_GAPS = (0.38, 0.14)


def hook_parts(a: str, b: str) -> list[str]:
    return ["Who wins?", f"{a},", f"or {b}."]


# A LINE WITH ITS PAUSES IN IT, IN ONE SYNTAX.
#
# `--parts`/`--gaps` are two parallel lists, which is fine for a builder and
# useless for a text box: a person types a sentence, not a list and a matching
# list of floats. So a script is ONE string with the pauses written where they
# fall:
#
#     Who wins? |0.38 Paradox, |0.14 or Heartwood.
#
# `|` is a pause. A number after it is its length in seconds; bare `|` uses
# DEFAULT_GAP. Text with no pipes is one continuous read, exactly as --text.
#
# THIS EXISTS BECAUSE LOADING THE DEFAULT LINE INTO THE APP'S BOX CHANGED HOW
# IT WAS SPOKEN. The words were identical and the delivery was not: the shipped
# line is three clips with measured silence between them, and a box that could
# only carry plain text collapsed it to a single utterance. Punctuation cannot
# put it back -- Kokoro gives "?...", "? ..." and "." the same contour -- so the
# pause had to become something the text can actually say.
DEFAULT_GAP = 0.38


def parse_script(text: str, default_gap: float = DEFAULT_GAP):
    """'a |0.4 b |c' -> (['a','b','c'], [0.4, DEFAULT_GAP])"""
    import re as _re
    chunks = _re.split(r"\|\s*([0-9]*\.?[0-9]+)?\s*", text)
    parts, gaps = [chunks[0].strip()], []
    for i in range(1, len(chunks), 2):
        gaps.append(float(chunks[i]) if chunks[i] else default_gap)
        parts.append((chunks[i + 1] or "").strip())
    keep = [(p, i) for i, p in enumerate(parts) if p]
    if not keep:
        raise SystemExit("! the script has no words in it")
    parts = [p for p, _ in keep]
    gaps = [gaps[i - 1] for _, i in keep[1:]]
    return parts, gaps


def hook_script(a: str, b: str) -> str:
    """The shipped line AS A SCRIPT, so the app's box can hold the real thing
    -- pauses included -- and render it identically."""
    ps, gs = hook_parts(a, b), HOOK_GAPS
    out = ps[0]
    for g, part in zip(gs, ps[1:]):
        out += f" |{g:g} {part}"
    return out


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
    ap.add_argument("--script", default=None,
                    help="one string with its pauses in it: `a |0.38 b |c`. "
                         "`|` is a pause, an optional number is its length in "
                         "seconds. Equivalent to --parts/--gaps but writable by "
                         "a person in a text box.")
    ap.add_argument("--print-hook-script", action="store_true",
                    help="print the default line in --script form and exit")
    ap.add_argument("--hook", action="store_true",
                    help="render THE DEFAULT LINE for --a versus --b, with the "
                         "shipped parts and gaps. This is what a short gets when "
                         "no --vo is supplied, and the app's preview calls it so "
                         "the two cannot diverge.")
    ap.add_argument("--gaps", default="",
                    help="comma-separated seconds between parts (len(parts)-1)")
    args = ap.parse_args()

    if args.print_hook_script:
        print(hook_script(args.a, args.b))
        return 0
    if args.script:
        if args.text or args.parts or args.hook:
            raise SystemExit("! --script carries its own parts; do not also pass "
                             "--text, --parts or --hook")
        ps, gs = parse_script(args.script)
        args.parts = "|".join(ps)
        args.gaps = ",".join(str(g) for g in gs)
    if args.hook:
        if args.text or args.parts:
            raise SystemExit("! --hook builds the line itself; do not also pass "
                             "--text or --parts")
        args.parts = "|".join(hook_parts(args.a, args.b))
        if not args.gaps:
            args.gaps = ",".join(str(g) for g in HOOK_GAPS)
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
