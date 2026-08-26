#!/usr/bin/env python3
"""The opening hook, mixed onto a finished render.

    python3 hook_vo.py --video short.mp4 --a axiom --b nightfell \
                       --game ../02-chain/sc-cardspin.html --out short-vo.mp4

WHY POST AND NOT BAKED. The copy is the part most likely to change, and it is
the part with the least engineering risk. Mixing after the render means a
rewrite costs seconds instead of a six-minute capture, and the video stream is
copied rather than re-encoded so the picture cannot drift.

THE COPY, AND WHY IT IS THIS SHAPE. Measured on am_onyx, the obvious line --
"Super Weapon Ball. X versus Y. Who wins?" -- runs 3.39s and does not reach the
question until 2.34s. The cold open has a median of 3.18s and can be 1.37s, so
the hook lands ON the clash or after it: too late to be a hook. Dropping the
title from the audio fixes it, because the title is ALREADY ON SCREEN --
"SUPER WEAPON BALL: THE SUNDERED CROWN" is printed at the top of every frame,
including the cold open. Spending 1.4s of a three-second window naming
something the viewer is looking at is the most expensive line in the script.

    Who wins? {A}... or {B}.     2.02s, question at 0.04s, names at 1.64s

NAMES COME FROM THE BUILD. `oathwound` displays as "Goreshard" -- the only id
that is not its own name, and enough to make a hook say the wrong thing. The
ids are read through AC.WEAPONS rather than title-cased, so a future rename
cannot silently desync the voiceover from the card.

LOUDNESS. The bed is ducked under the line and the mix is re-normalised to
render.py's own targets, then the true peak is checked against the ceiling. The
capture is not bit-reproducible (shake jitter, synth noise), so a mix that only
just clears the ceiling is not clear -- the measured margin is printed.
"""
from __future__ import annotations
import argparse, json, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
LUFS_TARGET, TP_TARGET = -19.5, -1.5
# Three clips, two measured gaps. Kokoro ignores punctuation as timing -- "?...",
# "? ..." and "." all produce the same contour -- so every pause here is real
# silence of a stated length.  The beat after the question is the hook landing;
# the shorter one between the names is the pick-a-side moment.
PARTS = ["Who wins?", "{a},", "or {b}."]


def names_from_build(game: pathlib.Path, ids):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--no-sandbox"])
        pg = br.new_page(); pg.goto(game.resolve().as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
        table = json.loads(pg.evaluate(
            "()=>JSON.stringify(Object.fromEntries(AC.WEAPONS.map(w=>[w.id,w.name])))"))
        br.close()
    out = []
    for i in ids:
        if i not in table:
            raise SystemExit(f"! {i!r} is not a relic in {game.name}. "
                             f"Known: {', '.join(sorted(table))}")
        out.append(table[i])
    return out


def ffprobe(path, *entries):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", ",".join(entries),
                        "-of", "json", str(path)], capture_output=True, text=True)
    return json.loads(r.stdout)


def measure(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                        f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    tail = p.stderr[p.stderr.rfind("{"):]
    return json.loads(tail[:tail.find("}") + 1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--a", required=True, help="relic ID (not display name)")
    ap.add_argument("--b", required=True, help="relic ID (not display name)")
    ap.add_argument("--game", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", required=True)
    ap.add_argument("--at", type=float, default=0.15, help="seconds before the line starts")
    ap.add_argument("--duck", type=float, default=-9.0, help="dB the bed drops under the line")
    ap.add_argument("--vo-gain", type=float, default=6.0,
                    help="dB on the line itself. +6 puts the voice ~6dB over the "
                         "ducked bed and leaves ~1.3dB of true-peak ceiling. Do "
                         "not go further without re-measuring: the capture is "
                         "not bit-reproducible and the peak moves ~1dB between "
                         "renders, so a thinner margin clips on some seeds only.")
    ap.add_argument("--text", default=None, help="override the copy entirely (one clip, no gaps)")
    ap.add_argument("--voice", default="bm_lewis")
    ap.add_argument("--gap", type=float, default=0.38,
                    help="silence after the question")
    ap.add_argument("--name-gap", type=float, default=0.14,
                    help="silence between the two relic names")
    A = ap.parse_args()

    vid = pathlib.Path(A.video)
    if not vid.exists():
        print(f"! missing {vid}", file=sys.stderr); return 2
    na, nb = names_from_build(pathlib.Path(A.game), [A.a, A.b])
    line = A.text or " ".join(p.format(a=na, b=nb) for p in PARTS)

    with tempfile.TemporaryDirectory() as td:
        vo = pathlib.Path(td) / "vo.wav"
        cmd = ["python3", str(HERE / "cinema_vo.py"), "--a", na, "--b", nb,
               "--voice", A.voice, "--out", str(vo)]
        if A.text:
            cmd += ["--text", A.text]
        else:
            cmd += ["--parts", "|".join(p.format(a=na, b=nb) for p in PARTS),
                    "--gaps", f"{A.gap},{A.name_gap}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode or not vo.exists():
            print("! cinema_vo failed:\n" + (r.stderr or r.stdout), file=sys.stderr); return 3
        vo_dur = float(ffprobe(vo, "format=duration")["format"]["duration"])
        end = A.at + vo_dur

        # Duck the bed only while the line is speaking; amix with normalize=0 so
        # two inputs are not silently halved.
        fc = (f"[0:a]volume=enable='between(t,{A.at:.2f},{end:.2f})':"
              f"volume={A.duck}dB[g];"
              f"[1:a]adelay={int(A.at*1000)}|{int(A.at*1000)},volume={A.vo_gain}dB[v];"
              f"[g][v]amix=inputs=2:duration=first:normalize=0[m]")
        mixed = pathlib.Path(td) / "mix.mp4"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(vid), "-i", str(vo), "-filter_complex", fc,
                        "-map", "0:v", "-map", "[m]", "-c:v", "copy",
                        "-c:a", "pcm_s16le", str(mixed)], check=True)

        loud = measure(mixed)
        af = (f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA=11"
              f":measured_I={loud['input_i']}:measured_TP={loud['input_tp']}"
              f":measured_LRA={loud['input_lra']}:measured_thresh={loud['input_thresh']}"
              f":offset={loud['target_offset']}:linear=true")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(mixed), "-c:v", "copy", "-af", af,
                        "-c:a", "aac", "-b:a", "128k", "-ac", "2",
                        "-movflags", "+faststart", str(A.out)], check=True)

    final = measure(A.out)
    d_in = float(ffprobe(vid, "format=duration")["format"]["duration"])
    d_out = float(ffprobe(A.out, "format=duration")["format"]["duration"])
    tp = float(final["input_tp"])
    print(json.dumps({
        "out": A.out, "line": line, "names_from_build": [na, nb],
        "voice": A.voice, "gap": A.gap, "name_gap": A.name_gap,
        "vo_seconds": round(vo_dur, 2), "starts_at": A.at,
        "ends_at": round(end, 2),
        "duration_in": round(d_in, 2), "duration_out": round(d_out, 2),
        "duration_held": abs(d_in - d_out) < 0.05,
        "lufs": float(final["input_i"]), "true_peak": tp,
        "tp_margin_db": round(TP_TARGET - tp, 2),
    }, indent=1))
    if abs(d_in - d_out) >= 0.05:
        print("! the mix changed the video length", file=sys.stderr); return 4
    if tp > TP_TARGET:
        print(f"! true peak {tp} is over the {TP_TARGET} ceiling", file=sys.stderr); return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
