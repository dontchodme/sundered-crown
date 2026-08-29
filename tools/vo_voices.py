#!/usr/bin/env python3
"""THE VOICE LIST, AS JSON, WITHOUT LOADING THE 310 MB MODEL.

    python vo_voices.py

`Kokoro.get_voices()` needs the model open, which is seconds and 310 MB for a
list of names. The voices file is an npz and its KEYS ARE THE NAMES, so this
reads them in ~0.01s. The app's picker calls it, so the list cannot drift from
the file the way a hardcoded list in the UI would.

English only, and named rather than filtered silently: Kokoro ships 54 voices
across several languages and the other 34 would be noise in a picker for an
English announcer. `--all` returns everything.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
VOICES = HERE / "voices-v1.0.bin"

# a/b = American/British, f/m = female/male. Kokoro's own convention.
GROUP = {"af": "American female", "am": "American male",
         "bf": "British female",  "bm": "British male"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="every language, not just English")
    a = ap.parse_args()
    if not VOICES.exists():
        print(json.dumps({"ok": False,
                          "reason": f"missing {VOICES.name} — see tools/FETCH-KOKORO.md"}))
        return 1
    import numpy as np
    z = np.load(VOICES, allow_pickle=True)
    names = sorted(z.files if hasattr(z, "files") else z.keys())
    out = []
    for n in names:
        pre = n[:2]
        if pre in GROUP:
            out.append({"id": n, "group": GROUP[pre]})
        elif a.all:
            out.append({"id": n, "group": "other"})
    print(json.dumps({"ok": True, "voices": out, "default": "bm_lewis"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
