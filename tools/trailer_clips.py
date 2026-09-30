#!/usr/bin/env python3
"""Film every fight moment the trailer cuts from. Serial on purpose: two captures at once on a
2-core box ran SLOWER in total than one (0.53 vs 0.74 frames/s measured), and cinema_clip's
frame cache is per output folder, so each clip gets its own.

    python trailer_clips.py            # skips clips already on disk
    python trailer_clips.py --only kill_gloamwire,vesper

THE BUILD IS GAME (sc-nightglass-fx), Rick-passed, 41 relics. Nothing is filmed off the
design batch's line: it is awaiting his eye, and its redesigns change several foes' ultimates
(dawnbringer, widowmaker, ironhail, lightkeeper, aureole, censer, axiom). Foes were chosen
from relics whose ultimate is the same on both lines, EXCEPT the first three clips below,
filmed before that rule was in; in each, the foe's ultimate is not on screen in the frames
the edit uses (trailer_scan.py prints the foe's cast times).

Fights come from trailer_scan.py: the relic's cast with the most damage in the 3 s after it,
cast between 4 s and 40 s, the foe still alive 3 s later. At = cast - 0.3 s.
"""
import argparse, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parent / "07-shorts" / "worldcup-trailer"
GAME = "../02-chain/sc-nightglass-fx.html"

# (name, a, b, seed, at, window, frame format). at=None: filmed back from the kill with --lead.
JOBS = [
    ("duskreave", "widowmaker", "duskreave", 7739596, 15.8, 3.0, "png"),
    ("cindercleave", "axiom", "cindercleave", 7723758, 33.07, 2.4, "png"),
    ("thornshear", "thornshear", "axiom", 7739596, 35.96, 2.4, "png"),
    ("kill_gloamwire", "gloamwire", "emberedge", 7700001, None, 1.4, "jpg"),
    ("starwarden", "emberedge", "starwarden", 7715839, 33.25, 2.8, "jpg"),
    ("culverin", "farwarden", "culverin", 7700001, 30.31, 2.4, "jpg"),
    ("crozier", "crozier", "foregone", 7731677, 29.42, 2.4, "jpg"),
    ("cipher", "heartwood", "cipher", 7723758, 15.27, 2.4, "jpg"),
    ("vesper", "heartwood", "vesper", 7731677, 35.52, 2.4, "jpg"),
    ("shroudmaul", "emberedge", "shroudmaul", 7723758, 16.13, 2.4, "jpg"),
    ("bloodmirror", "bloodmirror", "spellbreaker", 7700001, 33.42, 2.4, "jpg"),
    ("lastlight", "redflail", "lastlight", 7715839, 32.29, 2.4, "jpg"),
    ("paradox", "emberedge", "paradox", 7739596, 35.73, 2.4, "jpg"),
    ("briarwand", "briarwand", "bulwarden", 7715839, 30.07, 2.4, "jpg"),
    ("nightglass", "nightglass", "emberedge", 7700001, 32.0, 2.4, "jpg"),
    ("ravelbone", "spellbreaker", "ravelbone", 7723758, 34.51, 2.4, "jpg"),
    # the director files no cut on this fight, so --lead refuses it; filmed by start time instead.
    # The kill lands at 69.62.
    ("kill_duskreave", "emberedge", "duskreave", 7700001, 68.3, 1.7, "jpg"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    for name, ra, rb, seed, at, win, fmt in JOBS:
        if only and name not in only:
            continue
        d = WORK / "clips" / name
        d.mkdir(parents=True, exist_ok=True)
        out = d / "clip.mp4"
        if out.exists():
            print(f"{name}: on disk, skipped"); continue
        cmd = [sys.executable, str(HERE / "trailer_clip.py"), "--game", GAME, "--a", ra, "--b", rb,
               "--seed", str(seed), "--w", "1080", "--no-card", "--out", str(out)]
        cmd += ["--png"] if fmt == "png" else ["--q", "0.95"]
        cmd += (["--at", str(at), "--window", str(win), "--end-at-window"] if at is not None
                else ["--lead", str(win), "--verdict-hold", "0.8"])
        t0 = time.time()
        with open(d / "log.txt", "w") as log:
            rc = subprocess.call(cmd, cwd=str(HERE), stdout=log, stderr=subprocess.STDOUT)
        print(f"{name}: rc {rc}, {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
