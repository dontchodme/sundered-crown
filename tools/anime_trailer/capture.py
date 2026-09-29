#!/usr/bin/env python3
"""Render the trailer's frames through headless Chromium.

  python3 capture.py --out frames            # every frame, 2 workers
  python3 capture.py --out prev --only 0,40,120 --png
  python3 capture.py --cues cues.json        # just export the cue list

Frames are a pure function of their number (lib.js keeps no state), so the
workers split the range by stride and never talk to each other.
"""
from __future__ import annotations
import argparse, base64, json, multiprocessing as mp, pathlib, sys, time

HERE = pathlib.Path(__file__).resolve().parent
URL = (HERE / "trailer.html").as_uri()


def open_page(p):
    from playwright.sync_api import sync_playwright  # noqa
    b = p.chromium.launch(args=["--disable-gpu-vsync", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto(URL)
    pg.evaluate("window.ready")
    return b, pg, errs


def worker(args):
    k, n, frames, out, q, png = args
    from playwright.sync_api import sync_playwright
    out = pathlib.Path(out)
    with sync_playwright() as p:
        b, pg, errs = open_page(p)
        mine = frames[k::n]
        t0 = time.time()
        for j, i in enumerate(mine):
            pg.evaluate(f"window.renderFrame({i})")
            if errs:
                print(f"[w{k}] frame {i}: {errs[:3]}", flush=True)
                errs.clear()
            if png:
                data = pg.evaluate("document.getElementById('cv').toDataURL('image/png')")
                (out / f"f{i:05d}.png").write_bytes(base64.b64decode(data.split(",", 1)[1]))
            else:
                data = pg.evaluate(f"window.grab({q})")
                (out / f"f{i:05d}.jpg").write_bytes(base64.b64decode(data.split(",", 1)[1]))
            if j % 50 == 0:
                el = time.time() - t0
                print(f"[w{k}] {j+1}/{len(mine)}  {el/(j+1):.2f}s/frame", flush=True)
        b.close()
    return len(mine)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="frames")
    ap.add_argument("--only", default=None, help="comma list of frame numbers")
    ap.add_argument("--range", default=None, help="a:b frame range")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--q", type=float, default=0.95)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--cues", default=None, help="write the cue list to this json and exit")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg, errs = open_page(p)
        total = pg.evaluate("window.totalFrames()")
        if a.cues:
            pathlib.Path(a.cues).write_text(pg.evaluate("window.cues()"))
            print(f"cues -> {a.cues}  (total frames {total})")
            if errs:
                print("page errors:", errs)
            b.close()
            return 0
        b.close()
    if a.only:
        frames = [int(x) for x in a.only.split(",") if x.strip()]
    elif a.range:
        s, e = a.range.split(":")
        frames = list(range(int(s), int(e)))
    else:
        frames = list(range(total))
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    n = max(1, min(a.workers, len(frames)))
    t0 = time.time()
    with mp.Pool(n) as pool:
        done = sum(pool.map(worker, [(k, n, frames, str(out), a.q, a.png) for k in range(n)]))
    print(f"{done} frames in {time.time()-t0:.1f}s -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
