#!/usr/bin/env python3
"""Build the anime trailer end to end: picture, score, encode.

  python tools/anime_trailer/build.py --out 07-shorts/v116/anime-trailer.mp4

Needs: playwright (+ its Chromium), numpy, scipy, ffmpeg on PATH, and the
Noto Sans CJK JP font (Black weight) installed — the committed render used it.
Deterministic: the same files make the same frames and the same mix.
"""
from __future__ import annotations
import argparse, json, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run(cmd, check=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="anime-trailer.mp4")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--crf", type=int, default=15)
    ap.add_argument("--keep", action="store_true", help="keep the frame folder")
    a = ap.parse_args()
    py = sys.executable
    out = pathlib.Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="anime_trailer_"))
    try:
        cues, mix, frames = tmp / "cues.json", tmp / "mix.wav", tmp / "frames"
        print("1/4 cue list (the picture's hits, for the score)")
        run([py, HERE / "capture.py", "--cues", cues])
        print("2/4 score and sound")
        run([py, HERE / "audio.py", "--cues", cues, "--out", mix])
        print("3/4 frames")
        run([py, HERE / "capture.py", "--out", frames, "--png", "--workers", str(a.workers)])
        print("4/4 encode, loudness to -14 LUFS / -1.5 dBTP (two-pass, linear)")
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mix, "-af",
                            "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True)
        txt = r.stderr
        m = json.loads(txt[txt.rfind("{"): txt.rfind("}") + 1])
        ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
        run(["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", frames / "f%05d.png", "-i", mix,
             "-af", ln, "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-tune", "animation",
             "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.2", "-r", "24",
             "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
             "-shortest", out])
        print(f"done -> {out}")
    finally:
        if a.keep:
            print(f"frames kept in {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
