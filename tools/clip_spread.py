#!/usr/bin/env python3
"""N CLIPS SIDE BY SIDE IN ONE FILE, at native resolution, for Rule 2.

Rick, 2026-08-28: *"i cannot judge anything from the sheet. only you can read
stuff like that. i need clips and pictures to judge every time."* And then:
*"send them all together side by side when they are done."*

Both are the same instruction and this tool is it. A spread is only a spread if
the person deciding can actually see the difference, and this project has now
twice offered a still where the question lived in motion:

  - `docs/RENDER-LAYERS.md` §5b -- two post effects chosen off sheets and
    rejected once they moved.
  - `CLAUDE.md` §4.0 -- film before you tune, if the ultimate is a picture.

Separate files are not a spread either. Flipping between two players loses the
frame, the moment and the eye's memory of what it just saw; side by side in one
timeline, the difference either reads or it does not.

    python clip_spread.py --clips a.mp4 b.mp4 --labels "TODAY" "FIXED"
    python clip_spread.py --clips a.mp4 b.mp4 c.mp4 --out ../07-shorts/x.mp4

NATIVE RESOLUTION, NOT FITTED TO A SCREEN. Two 1080-wide panels make a
2160-wide file and five make 5400, and that is deliberate: half of what these
comparisons are FOR is resolution and compression, and downscaling the panels
to something convenient destroys exactly the evidence being weighed. The player
can zoom. The file cannot un-throw-away a pixel.

    --width N   scales every panel, for when the question is motion rather
                than detail and a smaller file is worth more than the pixels.

THE FRAME COUNTS ARE CHECKED AND A MISMATCH IS LOUD. Two clips of the same
fight that came out different lengths are not a picture comparison -- they are
two different fights, and every frame after the first divergence is comparing
unrelated moments. That is the failure this tool exists to make impossible to
miss, because on a 5400px timeline it looks like nothing at all.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent


def resolve_ffmpeg(name: str = "ffmpeg") -> str:
    """ffmpeg, wherever winget hid it.

    Mirrors `app/main.js`'s resolveFfmpeg. winget installs ffmpeg WITHOUT a
    shim, so it is on PATH only if the user put it there -- and the failure
    mode is vicious: the capture succeeds, three minutes pass, and the encode
    dies with a bare `FileNotFoundError [WinError 2]` that names no file. The
    app already resolves this and injects PATH into its children; tools run
    from a terminal got nothing, which means the canonical command in
    `CLAUDE.md` §5 fails this way on a machine where the app works fine.
    """
    from shutil import which
    found = which(name)
    if found:
        return found
    local = os.environ.get("LOCALAPPDATA")
    if local:
        base = pathlib.Path(local) / "Microsoft" / "WinGet" / "Packages"
        try:
            for d in base.iterdir():
                if not d.name.startswith("Gyan.FFmpeg"):
                    continue
                for b in d.iterdir():
                    exe = b / "bin" / f"{name}.exe"
                    if exe.exists():
                        return str(exe)
        except OSError:
            pass
    return name


def font_arg() -> str:
    """`fontfile=` for drawtext, because Windows has no fontconfig.

    Without it ffmpeg prints `Fontconfig error: Cannot load default config
    file` and the whole filtergraph fails -- so a label is not a cosmetic
    detail here, it is the difference between a spread and an ffmpeg error.
    The colon in `C:/` has to be escaped twice: once for the filter's own
    option parser and once for the filtergraph's argument separator.
    """
    for name in ("segoeui.ttf", "arial.ttf", "tahoma.ttf", "consola.ttf"):
        f = pathlib.Path(os.environ.get("SystemRoot", "C:/Windows")) / "Fonts" / name
        if f.exists():
            return "fontfile='" + str(f).replace("\\", "/").replace(":", "\:") + "':"
    return ""      # non-Windows: fontconfig will find something


def probe(ffprobe: str, path: pathlib.Path) -> dict:
    out = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=width,height,nb_read_frames,r_frame_rate",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    return {"w": int(s["width"]), "h": int(s["height"]),
            "n": int(s.get("nb_read_frames") or 0), "fps": s["r_frame_rate"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", nargs="+", required=True)
    ap.add_argument("--labels", nargs="*", default=None,
                    help="burned into each panel. Defaults to the filenames, "
                         "because an unlabelled spread is a memory test")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=None,
                    help="scale each panel to this width. Omit for native, "
                         "which is what a resolution comparison needs")
    ap.add_argument("--crf", type=int, default=18,
                    help="the spread is a REVIEW artefact, not a deliverable, "
                         "so it is encoded well above what ships")
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--allow-mismatch", action="store_true",
                    help="stack clips of differing length anyway. Read the "
                         "warning first; it is almost never what you want")
    a = ap.parse_args()

    ff, ffp = resolve_ffmpeg("ffmpeg"), resolve_ffmpeg("ffprobe")
    clips = [pathlib.Path(c).resolve() for c in a.clips]
    for c in clips:
        if not c.exists():
            print(f"! {c} does not exist")
            return 2
    labels = a.labels or [c.stem for c in clips]
    if len(labels) != len(clips):
        print(f"! {len(clips)} clips but {len(labels)} labels")
        return 2

    info = [probe(ffp, c) for c in clips]
    print(f"{'clip':<28}{'size':>12}{'frames':>9}{'fps':>10}")
    for c, i in zip(clips, info):
        print(f"{c.name:<28}{i['w']}x{i['h']:<6}{i['n']:>9}{i['fps']:>10}")

    counts = {i["n"] for i in info}
    if len(counts) > 1:
        print(f"\n! THE CLIPS ARE DIFFERENT LENGTHS: {sorted(counts)}")
        print("  Past the first divergence these panels show DIFFERENT MOMENTS "
              "of the fight,\n  so any difference the eye reports is timing "
              "and not the thing being tested.")
        print("  If these are the same seed, something changed the fight. That "
              "is the finding;\n  the spread is not.")
        if not a.allow_mismatch:
            print("\n  Refusing to stack. --allow-mismatch overrides.")
            return 1
        print("  --allow-mismatch given; stacking anyway, shortest wins.")

    sizes = {(i["w"], i["h"]) for i in info}
    if len(sizes) > 1 and a.width is None:
        print(f"\n  panels differ in size {sorted(sizes)}; normalising to the "
              f"tallest.")

    H = max(i["h"] for i in info)
    W = a.width or max(i["w"] for i in info)

    # LABEL SIZE TRACKS PANEL SIZE. A 22px caption on a 1080-wide panel in a
    # 5400-wide file is unreadable at the zoom level the panels demand, which
    # would make the labels decorative and the spread a guessing game.
    fs = max(20, round(W * 0.038))
    font = font_arg()
    parts, filt = [], []
    for n, c in enumerate(clips):
        parts += ["-i", str(c)]
        txt = labels[n].replace("'", "").replace(":", " ")
        filt.append(
            f"[{n}:v]scale={W}:{H}:flags=lanczos,"
            f"drawtext={font}text='{txt}':x=(w-tw)/2:y=40:fontsize={fs}:"
            f"fontcolor=white:box=1:boxcolor=0x000000C0:boxborderw={fs//2}"
            f"[v{n}]")
    filt.append("".join(f"[v{n}]" for n in range(len(clips)))
                + f"hstack=inputs={len(clips)}[out]")

    out = pathlib.Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error", *parts,
           "-filter_complex", ";".join(filt),
           "-map", "[out]",
           # ONE audio stream, from the first clip. They are the same fight, so
           # mixing them would comb-filter into a phasing mess that sounds like
           # a broken render -- and this file is watched to judge a PICTURE.
           "-map", "0:a?",
           "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", str(out)]
    print(f"\nstacking {len(clips)} x {W}x{H} -> {W*len(clips)}x{H} ...")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("! ffmpeg failed")
        return 1
    mb = out.stat().st_size / 1e6
    print(f"wrote {out}  {mb:.1f} MB  {W*len(clips)}x{H}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
