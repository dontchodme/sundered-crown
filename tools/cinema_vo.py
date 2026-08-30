#!/usr/bin/env python3
"""One spoken line per fight: the fighters, by name, ON THEIR OWN IGNITIONS.

## 2026-08-29: THE LINE IS NOW TIMED TO THE PICTURE

It used to be timed to nothing, and that was not sloppiness -- it was a home
that got demolished. The line was written to sit inside the 4.0s intro card;
the card was retired for losing 71-75% of the audience; the line kept its
inherited pacing and played at 0.0 over whatever the fight happened to be
doing. `docs/APP-FEATURES-BRIEF.md` §1 is the whole story.

The ignition open (`src/render/open.js`, v46) gives it a home again, and this
is what the shipped line was doing against it -- measured, ironhail v goreshard:

    0.10s  IRONHAIL ignites
    0.95s  GORESHARD ignites
    1.18s  "Ironhail,"      1.08s after its own flare, 0.23s after the OTHER one
    2.19s  "or Goreshard."  1.24s late, over the pull wide
    3.17s  ends             past the end of the shot and past the first clank

**Every name was spoken over the wrong relic.** Rick chose arm C of a
three-arm spread (one line, one voice, only the timing moving -- the same shape
as the placement spread he answered on 2026-08-28):

    Ironhail,      at 0.10   on its own ignition
    Goreshard.     at 0.95   on its own ignition
    Who wins?      at 1.95   on the pull wide, landing as the hall opens

So the parts are placed at ABSOLUTE ONSETS read out of `src/render/open.js`
rather than joined by constant gaps, because a constant gap is only right for
one pair of names -- see `--at` and `ignition_beats()`. The lead silence is
baked into the wav, so every consumer places the file at 0.0 and gets the sync
for free (`shorts_build.py --vo-at` already defaults to 0.0).

> **THE STAGGER IS 0.85s AND TWELVE NAMES ARE LONGER THAN THAT.** Measured over
> all 25: median 0.84s, worst Emberedge at 1.00s. A name that overruns pushes
> the next one late rather than overlapping it, and the drift is PRINTED. The
> worst case in the roster is **0.15s**, nine frames, which is why this ships
> as-is; the fix if it is ever wanted is `flareB` in `open.js`, one number, and
> that is a change to a look Rick approved, so it is his.

> **A `--lead` CLIP HAS NO OPENING TO SYNC TO.** It starts thirty seconds into
> the fight, so there are no flares and the onsets are just prosody -- exactly
> what the old line was doing everywhere. Same words, same voice, no worse.

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
# THE TIMING IS NOT PUNCTUATION. Kokoro gives "?...", "? ..." and "." the same
# contour, so every beat here is real silence between separately rendered clips.
# It is no longer a list of GAPS: the parts are placed at absolute onsets taken
# from the opening's own flare times, because a gap that lands "Goreshard." on
# its flare lands "Emberedge." 0.15s late (the names differ by 0.31s across the
# roster) while an onset lands both.
OPEN_JS = HERE.parent / "src" / "render" / "open.js"

# How far into the pull wide the question lands. 0.40s puts it at 1.95s on the
# shipped shot table -- arm C, as rendered and as chosen. Relative to the pull
# rather than absolute so it follows the shot if the shot ever moves.
Q_AFTER_PULL = 0.40


def ignition_beats(path: pathlib.Path = OPEN_JS) -> tuple[float, float, float]:
    """(flareA, flareB, question) in seconds, read from src/render/open.js.

    ONE SOURCE OF TRUTH. The alternative is a second copy of the opening's
    timings living in this file, which is the failure post_build.py names in
    its own header: a settings duplicate is how a build ships something nobody
    picked. Loud on failure, never a fallback -- a line silently timed to
    constants that no longer match the picture is the exact defect this whole
    change exists to fix.
    """
    src = path.read_text(encoding="utf-8")
    def one(pattern, what):
        m = re.findall(pattern, src)
        if len(m) != 1:
            raise SystemExit(
                f"! cinema_vo: cannot read {what} out of {path.name} "
                f"({len(m)} matches). The opening's timings have moved and this "
                f"line would be spoken over the wrong relics. Fix the pattern; "
                f"do not add a fallback.")
        return float(m[0])
    fa = one(r"flareA:\s*([0-9.]+)", "flareA")
    fb = one(r"flareB:\s*([0-9.]+)", "flareB")
    # the pull wide is the last shot in the table
    pulls = re.findall(r"\{\s*t0:\s*([0-9.]+),\s*t1:\s*[0-9.]+,\s*from:", src)
    if len(pulls) != 1:
        raise SystemExit(f"! cinema_vo: cannot read the pull-wide start out of "
                         f"{path.name} ({len(pulls)} matches)")
    return fa, fb, float(pulls[0]) + Q_AFTER_PULL


def hook_parts(a: str, b: str) -> list[str]:
    return [f"{a},", f"{b}.", "Who wins?"]


def hook_onsets() -> tuple[float, float, float]:
    return ignition_beats()


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
# AND `@` IS AN ONSET, WHICH IS NOT THE SAME THING AS A PAUSE.
#
#     @0.1 Ironhail, |@0.95 Goreshard. |@1.95 Who wins?
#
# `|@1.95` means "this part starts 1.95s into the clip" -- an absolute time,
# not a distance from the part before it. The shipped line needs this because
# it is timed to the PICTURE: the flares are at fixed times and the names are
# not a fixed length, so a gap that syncs one pairing mis-syncs the next. A
# leading `@T` sets where the first part starts, and that silence is baked into
# the wav so every consumer can place the file at 0.0.
#
# A part that overruns its own onset is placed immediately after the one before
# it and the drift is printed. It is never overlapped and never clipped.
#
# THIS EXISTS BECAUSE LOADING THE DEFAULT LINE INTO THE APP'S BOX CHANGED HOW
# IT WAS SPOKEN. The words were identical and the delivery was not: the shipped
# line is three clips with measured silence between them, and a box that could
# only carry plain text collapsed it to a single utterance. Punctuation cannot
# put it back -- Kokoro gives "?...", "? ..." and "." the same contour -- so the
# pause had to become something the text can actually say.
DEFAULT_GAP = 0.38


def parse_script(text: str, default_gap: float = DEFAULT_GAP):
    """'a |0.4 b |@1.9 c' -> (['a','b','c'], [('gap',0.0), ('gap',0.4),
    ('at',1.9)]).

    Every part gets a PLACEMENT: ('gap', s) is s seconds after the part before
    it, ('at', t) is t seconds into the clip. The first part's placement is its
    lead-in, ('gap', 0.0) unless the script opens with `@T`.
    """
    import re as _re
    lead = ("gap", 0.0)
    m = _re.match(r"\s*@\s*([0-9]*\.?[0-9]+)\s*", text)
    if m:
        lead = ("at", float(m.group(1)))
        text = text[m.end():]
    chunks = _re.split(r"\|\s*(@?[0-9]*\.?[0-9]*)\s*", text)
    parts, place = [chunks[0].strip()], [lead]
    for i in range(1, len(chunks), 2):
        tok = (chunks[i] or "").strip()
        if tok.startswith("@"):
            place.append(("at", float(tok[1:])))
        else:
            place.append(("gap", float(tok) if tok else default_gap))
        parts.append((chunks[i + 1] or "").strip())
    keep = [(p, i) for i, p in enumerate(parts) if p]
    if not keep:
        raise SystemExit("! the script has no words in it")
    parts = [p for p, _ in keep]
    place = [place[i] for _, i in keep]
    place[0] = lead if keep[0][1] == 0 else place[0]
    return parts, place


def hook_script(a: str, b: str) -> str:
    """The shipped line AS A SCRIPT, so the app's box can hold the real thing
    -- its timing included -- and render it identically."""
    ps, ts = hook_parts(a, b), hook_onsets()
    out = f"@{ts[0]:g} {ps[0]}"
    for t, part in zip(ts[1:], ps[1:]):
        out += f" |@{t:g} {part}"
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
                    help="one string with its timing in it: `@0.1 a |0.38 b "
                         "|@1.95 c`. `|` is a pause, an optional number is its "
                         "length in seconds, and `@T` is an absolute onset T "
                         "seconds into the clip. Equivalent to --parts with "
                         "--gaps/--at but writable by a person in a text box.")
    ap.add_argument("--print-hook-script", action="store_true",
                    help="print the default line in --script form and exit")
    ap.add_argument("--hook", action="store_true",
                    help="render THE DEFAULT LINE for --a versus --b, placed on "
                         "the ignition open's own flares. This is what a short "
                         "gets when no --vo is supplied, and the app's preview "
                         "calls it so the two cannot diverge.")
    ap.add_argument("--gaps", default="",
                    help="comma-separated seconds between parts (len(parts)-1)")
    ap.add_argument("--at", default="",
                    help="comma-separated ABSOLUTE onsets, one per part, in "
                         "seconds from the start of the clip. The lead silence "
                         "is baked into the wav, so the file goes in at 0.0. A "
                         "part that overruns its onset is placed after the one "
                         "before it and the drift is printed.")
    args = ap.parse_args()

    if args.print_hook_script:
        print(hook_script(args.a, args.b))
        return 0
    # Every path below ends in ONE representation: `parts`, and a `place` list
    # of ('gap', s) / ('at', t), one per part, the first being the lead-in.
    parts, place = None, None
    if args.script:
        if args.text or args.parts or args.hook:
            raise SystemExit("! --script carries its own parts; do not also pass "
                             "--text, --parts or --hook")
        parts, place = parse_script(args.script)
    if args.hook:
        if args.text or args.parts:
            raise SystemExit("! --hook builds the line itself; do not also pass "
                             "--text or --parts")
        parts = hook_parts(args.a, args.b)
        place = [("at", t) for t in hook_onsets()]
    if parts is None and args.parts:
        parts = [p for p in args.parts.split("|") if p.strip()]
        if args.at and args.gaps:
            raise SystemExit("! --at and --gaps are two ways to place the same "
                             "parts; pass one")
        if args.at:
            ats = [float(t) for t in args.at.split(",") if t.strip()]
            if len(ats) != len(parts):
                raise SystemExit(f"! {len(parts)} parts need {len(parts)} onsets, "
                                 f"got {len(ats)}")
            place = [("at", t) for t in ats]
        else:
            gaps = [float(g) for g in args.gaps.split(",") if g.strip()] \
                if args.gaps else []
            if len(gaps) != len(parts) - 1:
                raise SystemExit(f"! {len(parts)} parts need {len(parts)-1} "
                                 f"gaps, got {len(gaps)}")
            place = [("gap", 0.0)] + [("gap", g) for g in gaps]
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

    if parts:
        chunks, sr, spans, drifted = [], None, [], []
        cursor = 0.0
        for part, (kind, val) in zip(parts, place):
            y, sr = render(part)
            target = val if kind == "at" else cursor + val
            # NEVER OVERLAP AND NEVER CLIP. A name longer than the gap between
            # two flares pushes the next part late; that is a real, visible
            # 0.15s worst case across the roster and it is printed rather than
            # hidden. Silently overlapping two clips would sound like a fault
            # in the voice and read as nothing in any log.
            start = max(target, cursor)
            if start - target > 0.005:
                drifted.append((part, start - target))
            if start > cursor:
                chunks.append(np.zeros(int(round(sr * (start - cursor))),
                                       dtype=np.float32))
            spans.append((start, len(y) / sr, part, target))
            chunks.append(y)
            cursor = start + len(y) / sr
        samples = np.concatenate(chunks)
        line = " ".join(parts)
        for t0, d, txt, target in spans:
            late = "" if abs(t0 - target) <= 0.005 else \
                   f"   {t0 - target:+.2f}s LATE (wanted {target:.2f}s)"
            print(f"[cinema_vo]   {t0:5.2f}s +{d:4.2f}s  {txt!r}{late}")
        if drifted:
            print(f"[cinema_vo]   {len(drifted)} part(s) could not make their "
                  f"onset: " + ", ".join(f"{p!r} by {d:.2f}s" for p, d in drifted))
    else:
        samples, sr = render(line)

    sf.write(args.out, samples, sr)
    print(f"[cinema_vo] {args.out}  {len(samples)/sr:.2f}s  voice={voice}  \"{line}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
