#!/usr/bin/env python3
"""THE STINGER — payoff-first open, look prototype. Hook brief v46 §3.

Open on ~0.9s of the killing blow AS THE DIRECTOR FILMS IT, a stakes line
over it, snap to black, then the fight from t=0 — here stitched onto the
ignition open, so the stack is: the payoff, the fighters igniting, the fight.

Same fight throughout: the stinger is the SAME SEED's own ending, captured
with the director on from just before the fatal cut. Nothing is staged and
nothing is edited into the fight — it is segment selection, which is all the
shipping version is either.

THE COPY IS FOR A FIRST-TIME VIEWER — Rick, 2026-08-30: a line like "ends in
7 traded blows" "means nothing to someone whos never seen one of these
videos before. we need to introduce them to the project and show them the
value of staying to watch in language a first time watcher can understand."
Five candidates are rendered over the real death frame in
05-reference/v46-ignition/stakes-copy-spread.png; the default below is the
working pick, not a decision.

The spoiler objection is answered in the brief: the post-0:05 tail is
memoryless (v32 §2) — there is no suspense to protect, and the stinger
spends the fight's best second where 100% of viewers are.

Uses ignition_lab's harness and patches (same directory). Same runtime
caveat as that tool: re-pick seeds on the pinned pair before shipping.

    python stinger_lab.py --a ironhail --b oathwound --seed 52744 \
        --kill-t 31.27 --stakes "ENDS IN 7 TRADED BLOWS"

Output: out-stinger/ — stinger.mp4, hook-stack.mp4 (stinger + ignition open),
hook-stack-plain.mp4 (stinger + control open), plus raw frames.
"""
from __future__ import annotations

import argparse, base64, json, pathlib, subprocess, sys, time

from scpage import game
from ignition_lab import (DRAW_GATE_JS, BLUR_IGNITE_JS, OPEN_JS, HARNESS,
                          VARIANTS)

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out-stinger"

# Stakes line drawn in the verdict panel's own register: 700 ui-serif/Georgia,
# parchment on a dark band with a gold hairline — screen space, over the
# composited frame. Copy is Rick's call (Rule 2); this is a placeholder shape.
STAKES_JS = r"""([text, sub]) => {
  window.__stakes = function () {
    const cv = document.getElementById('cv');
    const c = cv.getContext('2d');
    const W = cv.width, H = cv.height, k = W / 1080;
    c.save();
    c.setTransform(1, 0, 0, 1, 0, 0);
    const bandH = 150 * k, y0 = H * 0.145;
    c.fillStyle = 'rgba(7,5,12,0.78)';
    c.fillRect(0, y0, W, bandH);
    c.fillStyle = '#C9A227';
    c.fillRect(0, y0, W, 3 * k);
    c.fillRect(0, y0 + bandH - 3 * k, W, 3 * k);
    c.textAlign = 'center'; c.textBaseline = 'middle';
    c.fillStyle = '#EDE3D0';
    c.font = 700 * 0 + '700 ' + Math.round(64 * k) + 'px ui-serif, Georgia, serif';
    c.fillText(text, W / 2, y0 + bandH * (sub ? 0.40 : 0.5));
    if (sub) {
      c.fillStyle = '#C9A227';
      c.font = '700 ' + Math.round(26 * k) + 'px "Atkinson Hyperlegible Next", sans-serif';
      c.fillText(sub, W / 2, y0 + bandH * 0.78);
    }
    c.restore();
  };
  return "ok";
}"""


def capture(page, tag, n_frames, q, jpg_dir, stakes=False, stop_after_over=None,
            fps=60):
    jpg_dir.mkdir(parents=True, exist_ok=True)
    for f in jpg_dir.glob("*"):
        f.unlink()
    states, over_idx = [], None
    for i in range(n_frames):
        r = page.evaluate(
            "([raw,q,st]) => { const r = window.__clip.frame(raw,q);"
            " if (st && window.__stakes) { window.__stakes();"
            "   const u = document.getElementById('cv')"
            "     .toDataURL('image/jpeg', q); r.i = u.slice(u.indexOf(',')+1); }"
            " return r; }",
            [1.0 / fps, q, stakes])
        (jpg_dir / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(r["i"]))
        states.append((r["t"], r["c"], r["o"]))
        if r["o"] and over_idx is None:
            over_idx = i
        if over_idx is not None and stop_after_over is not None \
                and i >= over_idx + int(stop_after_over * fps):
            break
    return states, over_idx


def encode(frames_dir, wav, out, fps, start=0, nframes=None, ss=0.0,
           fade_out=None):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-framerate", str(fps), "-start_number", str(start),
           "-i", str(frames_dir / "f_%05d.jpg"),
           "-ss", f"{ss:.3f}", "-i", str(wav)]
    if nframes:            # OUTPUT option — after every input, or ffmpeg
        cmd += ["-frames:v", str(nframes)]   # reads it against the wav

    af = f"afade=t=out:st={(nframes or 0)/fps - 0.09:.3f}:d=0.09" if fade_out else "anull"
    cmd += ["-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-af", af,
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="build.html")
    ap.add_argument("--a", default="ironhail")
    ap.add_argument("--b", default="oathwound")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--kill-t", type=float, required=True,
                    help="the fatal cut's t from cinePlan; capture starts lead before it")
    ap.add_argument("--lead", type=float, default=2.2)
    ap.add_argument("--stakes", default="TWO WEAPONS. ONE SURVIVES.")
    ap.add_argument("--stakes-sub", default="YOU'RE SEEING THE ENDING FIRST")
    ap.add_argument("--sting-pre", type=float, default=0.78,
                    help="seconds of stinger kept before the death frame")
    ap.add_argument("--sting-post", type=float, default=0.18)
    ap.add_argument("--open-secs", type=float, default=5.4)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--q", type=float, default=0.85)
    a = ap.parse_args()
    fps, q = a.fps, a.q
    OUT.mkdir(exist_ok=True)

    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        page.evaluate(f"AC.setResolution({a.w}, {round(a.w*16/9)})")
        for js in (DRAW_GATE_JS, BLUR_IGNITE_JS, OPEN_JS):
            r = page.evaluate(js)
            if r not in ("ok", "already"):
                sys.exit(f"! patch failed: {r}")
        page.evaluate(HARNESS)
        page.evaluate(STAKES_JS, [a.stakes, a.stakes_sub])

        # ---- 1. the kill window, director on, from lead before the fatal cut.
        # No opening cfg: the director films the death exactly as it ships.
        page.evaluate("() => { window.__openCfg = null; window.__openShot = false;"
                      " window.__igniteMul = 1; }")
        start_at = max(0.0, a.kill_t - a.lead)
        info = page.evaluate("([A,B,s,on,at]) => window.__clip.init(A,B,s,on,at)",
                             [a.a, a.b, a.seed, True, start_at])
        print(f"stinger capture from match t={start_at:.2f}s "
              f"(fatal cut at {a.kill_t:.2f}s)")
        t0 = time.time()
        states, over_idx = capture(page, "sting", int(30 * fps), q,
                                   OUT / "sting", stakes=True,
                                   stop_after_over=0.6, fps=fps)
        if over_idx is None:
            sys.exit("! the match never ended inside the capture window")
        wav = page.evaluate("([d]) => window.__clip.renderAudio(d, 0)",
                            [len(states) / fps + 0.2])
        (OUT / "sting" / "a.wav").write_bytes(base64.b64decode(wav))
        print(f"  {len(states)} frames in {time.time()-t0:.0f}s; "
              f"death at frame {over_idx} ({over_idx/fps:.2f}s wall)")

        # ---- 2. the two opens on the same seed: ignition 'both' and control.
        for tag in ("both", "control"):
            cfg = VARIANTS[tag]
            page.evaluate("([c]) => { window.__openCfg = c; window.__openShot = false;"
                          " window.__igniteMul = 1; }", [cfg])
            page.evaluate("([A,B,s,on,at]) => window.__clip.init(A,B,s,on,at)",
                          [a.a, a.b, a.seed, True, 0])
            t0 = time.time()
            n = int(a.open_secs * fps)
            capture(page, tag, n, q, OUT / f"open_{tag}", stakes=False, fps=fps)
            wav = page.evaluate("([d]) => window.__clip.renderAudio(d, 0)",
                                [n / fps + 0.2])
            (OUT / f"open_{tag}" / "a.wav").write_bytes(base64.b64decode(wav))
            print(f"  open[{tag}]: {n} frames in {time.time()-t0:.0f}s")
        if errors:
            print("page errors:", errors[:6], file=sys.stderr)
            if any("pageerror" in e for e in errors):
                sys.exit("! page errors during capture")

    # ---- 3. cut the stinger window and encode the segments
    pre, post = int(a.sting_pre * fps), int(a.sting_post * fps)
    s0 = max(0, over_idx - pre)
    n_sting = min(pre + post, over_idx + post - s0)
    encode(OUT / "sting", OUT / "sting" / "a.wav", OUT / "seg_sting.mp4",
           fps, start=s0, nframes=n_sting, ss=s0 / fps, fade_out=True)
    for tag in ("both", "control"):
        encode(OUT / f"open_{tag}", OUT / f"open_{tag}" / "a.wav",
               OUT / f"seg_open_{tag}.mp4", fps,
               nframes=int(a.open_secs * fps))
    # the snap: 3 frames of the game's own void, silent
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", f"color=c=0x0C0507:s={a.w}x{round(a.w*16/9)}:d=0.05:r={fps}",
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", str(OUT / "seg_snap.mp4")], check=True)

    # ---- 4. the stacks
    for name, open_tag in (("hook-stack", "both"), ("hook-stack-plain", "control")):
        lst = OUT / f"{name}.txt"
        lst.write_text("".join(f"file '{OUT / s}'\n" for s in
                               ("seg_sting.mp4", "seg_snap.mp4",
                                f"seg_open_{open_tag}.mp4")))
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", "-movflags", "+faststart",
                        str(OUT / f"{name}.mp4")], check=True)
    print(json.dumps({"death_frame": over_idx, "sting_frames": n_sting,
                      "sting_secs": round(n_sting / fps, 2)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
