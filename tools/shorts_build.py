#!/usr/bin/env python3
"""One short, end to end: capture -> 1080x1920 -> voiceover mix -> measure.

SHORTSHANDOFF.md describes this as three shell stages that a human pastes in
order. That was fine when three shorts were made by hand; it stops being fine
the moment the mix has a mandatory flag in it (`alimiter ... level=false`, §8)
that is invisible in the output if you forget it and merely makes the file
clip. So the graph lives in code, with the reasons attached, and the delivery
measurement runs in the same breath as the encode that produced it.

    python3 shorts_build.py --a slagheart --b lightkeeper --seed 488464971 \
        --vo ../07-shorts/vo-sh-lk.wav --out ../07-shorts/short-5-....mp4

Stages are separable exactly as the handoff requires, because a full 60fps
capture is minutes long and the frames survive a dead tool window:

    --capture-only     frames + wav, then stop
    --encode-only      pick up frames already on disk

WHAT THIS DELIBERATELY DOES NOT DO: re-render audio onto an existing video.
The handoff's law — never patch a mix, re-capture — is enforced by construction
here, because the mix is only ever built from `_clip_frames/on.wav`, which the
capture stage writes and no later stage edits.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

import cinema_vo

HERE = pathlib.Path(__file__).resolve().parent

# §3c, with the §8 addendum folded in. Each term is load-bearing:
#   adelay          WHERE THE SPOKEN LINE STARTS, in ms. Was a hardcoded 300,
#                   chosen so the line began after the 4.0s intro card was up.
#                   The card does not ship (rule 1), so that 300ms waited for
#                   nothing and the line played over the opening by default --
#                   a placement nobody had picked. Rick chose the START of the
#                   fight, 2026-08-28, off a three-way spread rendered on
#                   paradox v heartwood seed 55957 (07-shorts/v44). Default 0.
#   volume 2.0      the VO sits over a full music bed; unlifted it is mush.
#                   Was 1.5. Rick asked for louder; 2.0 is +2.5dB on that.
#                   NOTE this chain is not hook_vo.py's: it targets -14 LUFS
#                   with an alimiter, where hook_vo targets -19.5 with none, so
#                   the +6dB measured there does NOT transfer. Re-measure here.
#   normalize=0     without it amix halves both inputs and the video is quiet
#   apad            a 3s line against a 40s video; amix would end the stream early
#   loudnorm -14    the platform norm
#   TP=-2.0         §8: -1.5 was not enough headroom once ult SFX stacked on a kill
#   alimiter        catches what single-pass loudnorm cannot hold
#   level=false     MANDATORY. alimiter's default re-levels to full scale and
#                   made true peak WORSE (+0.6 dBTP measured on short-4).
def mix_graph(limit, tp, vo_vol=2.0, vo_at=0.0):
    # `adelay` IS THE PLACEMENT, and it was a constant describing a dead card.
    # 300ms was chosen so the line started after the 4.0s intro card was up.
    # The card does not ship (rule 1), so that 300ms now waits for nothing and
    # the line plays over the cold open -- a placement nobody picked. It is a
    # parameter so the choice can be made and measured instead of inherited.
    ms = max(0, int(round(vo_at * 1000)))
    return (f"[1:a]aresample=48000,adelay={ms}|{ms},volume={vo_vol:.3f},apad[v1];"
            "[0:a][v1]amix=inputs=2:duration=first:normalize=0[m];"
            f"[m]loudnorm=I=-14:TP={tp}:LRA=11,aresample=48000,"
            f"alimiter=attack=5:release=60:limit={limit}:level=false[a]")


# THE CEILING IS CONTENT-DEPENDENT AND §8's SINGLE VALUE IS NOT ENOUGH.
# §8 fixed one measured overshoot (the Crucible's implosion on a kill) with
# limit=0.79, and that holds for a fight with one big set-piece. It does NOT
# hold for two Slagburst detonations: short-6 came out of the §8 graph at
# 0.0 dBTP, right on the fence, against a pass mark of -0.3.
#
# `limit` is a SAMPLE-peak ceiling; the pass mark is a TRUE-peak one, and AAC
# plus inter-sample reconstruction puts the second above the first by an amount
# that scales with how dense the transients are. So the ceiling is a ladder,
# tried in order, and the FIRST rung that measures inside the band ships.
#
# Every rung rebuilds the whole mix from `_clip_frames/on.wav`. Nothing is ever
# re-processed from a delivered file — that is the §0 law, and the point of it
# is that a mix patched onto finished video cannot be distinguished, later, from
# one that was right the first time.
CEILINGS = [(0.79, -2.0), (0.63, -3.0), (0.50, -4.0)]


def run(cmd, stream_err=False, **kw):
    """stream_err: let the child's stderr go STRAIGHT THROUGH to ours.

    `capture_output=True` pipes stderr and hands it back only when the child
    exits. cinema_clip's capture emits a progress line a second on stderr, and
    every one of them sat in that pipe for the whole 3-5 minute capture and
    arrived at the end -- so a caller watching for progress saw nothing until
    there was nothing left to wait for. Measured: 0 beats over a 304s render.

    Inheriting instead means the lines reach whoever is reading, live. The
    cost is that a failure's stderr is no longer quotable in the exception --
    it has already been printed, which is where it was wanted anyway."""
    if stream_err:
        q = subprocess.run([str(c) for c in cmd], stdout=subprocess.PIPE,
                           text=True, **kw)
        if q.returncode:
            raise SystemExit("FAILED: " + " ".join(str(c) for c in cmd)
                             + chr(10) + (q.stdout or "")[-2000:])
        return q.stdout
    p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if p.returncode:
        raise SystemExit(f"FAILED: {' '.join(str(c) for c in cmd)}\n"
                         f"{p.stdout[-2000:]}\n{p.stderr[-3000:]}")
    return p.stdout


def display_names(game, ids):
    """Relic id is not always its display name -- `oathwound` shows as
    'Goreshard'. Read them off the build so a rename cannot silently desync
    the voiceover from the card."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox'])
        pg = br.new_page()
        pg.goto(pathlib.Path(HERE / game).resolve().as_uri())
        pg.wait_for_function('window.AC && window.AC.WEAPONS', timeout=30000)
        table = json.loads(pg.evaluate(
            '()=>JSON.stringify(Object.fromEntries(AC.WEAPONS.map(w=>[w.id,w.name])))'))
        br.close()
    for i in ids:
        if i not in table:
            raise SystemExit(f'! {i!r} is not a relic in {game}')
    return [table[i] for i in ids]


def has_scrunch(game):
    """Does this build carry the scrunch panel? Measured off the build, because
    the answer decides whether the intro card is a feature or a defect."""
    src = (HERE / game).resolve().read_text(errors="replace")
    return "CONFIG.scrunch" in src or "scrunchAuto" in src


def capture(game, a, b, seed, out, fps, w, q, cold_open=None, card=True,
            verdict_hold=None, lead=None, stakes=None, stakes_sub=None):
    """THE CARD AND THE SCRUNCH ARE NOT ADDITIVE -- THEY STACK, AND STACKING IS
    THE WORST OF THE THREE OPTIONS.

    `cinema_clip.py` sets `m.introT` from --intro and then calls `AC.__inject`,
    which sets `scrunchAuto = CONFIG.scrunch.on`. On a scrunch build BOTH fire.
    Measured on sc-liquid-scrunch, ironhail v emberedge 3709119762:

        --intro      match clock after 4s of wall time = 0.00s  (frozen card)
                     scrunch panel then arms at wall 5.92s
                     -> a 4s dead stop AND a second legend two seconds later
        no --intro   match clock after 4s of wall = 4.00s
                     scrunch panel arms at wall 1.91s, on the first clank
                     -> fight from frame one, legend rides the live fight

    The 4s freeze is the single most expensive thing in these videos
    (08-analytics: card-first videos lose 71-75% of the audience present when it
    appears). Shipping it ON a scrunch build reintroduces the cliff the scrunch
    exists to remove. So --card defaults ON for the older builds that need it and
    the tool SHOUTS when the combination is live.
    """
    if card and has_scrunch(game):
        print("  !! WARNING: this build has the SCRUNCH and you are also filming")
        print("  !! the 4s intro CARD. They stack: 4s of frozen video, then the")
        print("  !! panel again at ~6s. Pass --no-card unless you mean it.")
    print(f"[1/3] capture  {a} v {b}  seed {seed}"
          f"   card={'on' if card else 'OFF (scrunch carries the names)'}")
    print(run([sys.executable, HERE / "cinema_clip.py",
               "--game", game,
               # `--full` OVERRIDES `--lead` -- cinema_clip line 414 is
               # `start = 0.0 if a.full else max(0.0, kill["t"] - a.lead)`.
               # It was hardcoded here, so every short this tool has ever
               # produced was the WHOLE fight, and passing --lead did nothing
               # at all. That is why the output ran 46s against a shipped
               # length of ~23s: not a missing flag, a flag that could never
               # take effect.
               *([] if lead is not None else ["--full"]),
               "--capture-only",
               *(["--intro"] if card else []),
               *(["--cold-open", str(cold_open)] if cold_open is not None else []),
               "--a", a, "--b", b, "--seed", seed,
               *(["--verdict-hold", str(verdict_hold)]
                 if verdict_hold is not None else []),
               # --lead IS WHY THE SHIPPED CLIPS ARE SHORT AND THE FIGHTS ARE NOT.
               # paradox_pick wants a 30-55s fight -- two windows and their
               # holds -- and the v43 clip of record was 23.0s because
               # `--lead 18` filmed only the last stretch of one. Without
               # this passthrough shorts_build could only ever produce the
               # WHOLE fight, so its output was twice the length of anything
               # that has ever been posted.
               *(["--lead", str(lead)] if lead is not None else []),
               # THE STAKES BAND RIDES WITH THE OPEN, NOT SEPARATELY.
               # Hook brief §5a and §6: band and ignition open are ONE
               # bundle so a posting slate stays a single variable. No
               # default copy is baked in here -- the line is Rule 2 and
               # Rick's pick, so no band unless one is passed.
               *(["--stakes"] if stakes == "" else
                 (["--stakes", stakes] if stakes else [])),
               *(["--stakes-sub", stakes_sub] if stakes_sub else []),
               "--fps", fps, "--w", w, "--q", q, "--out", out],
              cwd=HERE, stream_err=True).strip())


def encode(out, fps, crf, vo, keep=False, vo_vol=2.0, vo_at=0.0):
    tmp = pathlib.Path(out).resolve().parent / "_clip_frames"
    frames = sorted(tmp.glob("on_*.jpg"))
    wav = tmp / "on.wav"
    if not frames or not wav.exists():
        raise SystemExit(f"no captured frames in {tmp} — run the capture stage")
    print(f"[2/3] encode   {len(frames)} frames ({len(frames)/fps:.1f}s) -> 1080x1920")
    raw = tmp / "_raw.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-framerate", fps, "-i", tmp / "on_%05d.jpg", "-i", wav,
         "-vf", "scale=1080:1920:flags=lanczos",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", crf,
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ac", "2",
         "-shortest", raw])

    m = None
    for i, (limit, tp) in enumerate(CEILINGS):
        print(f"[3/3] mix      {pathlib.Path(vo).name} -> {pathlib.Path(out).name}"
              f"   (limit={limit} TP={tp})")
        # Video is COPIED, never re-encoded: the picture in the delivered file is
        # bit-identical to the one measured at the encode stage, and identical
        # across every rung of the ceiling ladder.
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-i", raw, "-i", vo, "-filter_complex", mix_graph(limit, tp, vo_vol, vo_at),
             "-map", "0:v", "-map", "[a]", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
             "-movflags", "+faststart", out])
        m = measure(out)
        m["limit"], m["tp_target"] = limit, tp
        if all(m["pass"].values()):
            if i:
                print(f"         §8's 0.79 measured {m['dbtp']} dBTP on this "
                      f"content; {limit} holds it.")
            break
        print(f"         {m['lufs']} LUFS / {m['dbtp']} dBTP — "
              f"{[k for k, ok in m['pass'].items() if not ok]}")

    # The capture is kept until the delivery MEASURES clean. Deleting it on the
    # first attempt is what turns a 20-second re-mix into a 4-minute re-capture,
    # and a pipeline that expensive to correct is one that tempts you into
    # patching the delivered file instead — the exact thing §0 forbids.
    if all(m["pass"].values()) and not keep:
        raw.unlink()
        for f in frames:
            f.unlink()
        wav.unlink()
    else:
        raw.unlink(missing_ok=True)
        print(f"         capture RETAINED in {tmp} — re-mix without re-capturing")
    return m


def measure(path):
    """§3's pass marks, as data rather than as something to eyeball."""
    j = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=width,height,codec_name,codec_type",
                        "-show_entries", "format=duration,size",
                        "-of", "json", path]))
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    au = next((s for s in j["streams"] if s["codec_type"] == "audio"), {})
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                        "loudnorm=I=-14:TP=-2.0:print_format=summary",
                        "-f", "null", "-"], capture_output=True, text=True)
    lufs = tp = None
    for line in p.stderr.splitlines():
        if "Input Integrated" in line:
            lufs = float(line.split(":")[1].strip().split()[0])
        if "Input True Peak" in line:
            tp = float(line.split(":")[1].strip().split()[0])
    dur = float(j["format"]["duration"])
    res = {"w": v["width"], "h": v["height"], "vcodec": v["codec_name"],
           "acodec": au.get("codec_name"), "dur": round(dur, 2),
           "mb": round(int(j["format"]["size"]) / 1e6, 1),
           "lufs": lufs, "dbtp": tp}
    res["pass"] = {
        "1080x1920": v["width"] == 1080 and v["height"] == 1920,
        "h264+aac": v["codec_name"] == "h264" and au.get("codec_name") == "aac",
        "under 60s": dur < 60.0,
        "-16..-13 LUFS": lufs is not None and -16.0 <= lufs <= -13.0,
        "TP <= -0.3": tp is not None and tp <= -0.3,
    }
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="../02-chain/sc-ember.html")
    ap.add_argument("--a", required=True, help="relic id, side 1")
    ap.add_argument("--b", required=True, help="relic id, side 2")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--vo", default=None,
                    help="wav from cinema_vo.py. Omitted: the opening hook is\n"
                         "generated here from the BUILD's display names -- "
                         "oathwound displays as Goreshard, so title-casing the "
                         "id would say the wrong name on camera.")
    ap.add_argument("--voice", default="bm_lewis")
    ap.add_argument("--gap", type=float, default=0.38)
    ap.add_argument("--name-gap", type=float, default=0.14)
    # nargs="?" with an EMPTY const, so a bare --stakes is passed through
    # bare and cinema_clip supplies the shipped line. The copy lives in ONE
    # place (cinema_clip.STAKES_LINE) and this tool never learns it.
    ap.add_argument("--stakes", nargs="?", const="", default=None,
                    metavar="LINE",
                    help="a stakes band over the opening, passed "
                         "through to cinema_clip. Fades out on the "
                         "first clank.")
    ap.add_argument("--stakes-sub", default=None, metavar="LINE",
                    help="the gold sub-line under it")
    ap.add_argument("--vo-vol", type=float, default=2.0)
    ap.add_argument("--lead", type=float, default=None,
                    help="seconds of fight to film before the finish; the "
                         "rest of the opening is trimmed. The shipped shorts "
                         "are ~23s clips of 40-50s fights.")
    ap.add_argument("--verdict-hold", type=float, default=None,
                    help="seconds the verdict panel is held. Passed straight to "
                         "cinema_clip; the rendered AUDIO tail follows it, so a "
                         "line placed in the tail is not cut off by silence.")
    ap.add_argument("--vo-at", type=float, default=0.0,
                    help="seconds into the video where the spoken line starts. "
                         "0 is Rick's choice, 2026-08-28: the announcer belongs "
                         "at the start of the fight. The old 0.300 was inherited "
                         "from an intro card that no longer ships.")
    ap.add_argument("--cold-open", type=float, nargs="?", const=5.0, default=None,
                    metavar="CAP")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--q", type=float, default=0.80)
    ap.add_argument("--crf", type=int, default=23)
    ap.add_argument("--no-card", dest="card", action="store_false", default=True,
                    help="film WITHOUT the 4s intro card. Correct on any build "
                         "carrying the scrunch -- see capture()'s docstring for "
                         "the measurement.")
    ap.add_argument("--capture-only", action="store_true")
    ap.add_argument("--encode-only", action="store_true")
    ap.add_argument("--keep", action="store_true",
                    help="keep the captured frames even on a clean pass")
    a = ap.parse_args()

    out = pathlib.Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if not a.encode_only:
        capture(a.game, a.a, a.b, a.seed, out, a.fps, a.w, a.q,
                cold_open=a.cold_open, card=a.card,
                verdict_hold=a.verdict_hold, lead=a.lead,
                stakes=a.stakes, stakes_sub=a.stakes_sub)
    if a.capture_only:
        print("captured; finish with --encode-only")
        return 0

    # The hook, built here rather than mixed onto a finished file: this tool's
    # law is never patch a mix, re-capture, and it holds it by only ever
    # mixing from the capture stage's on.wav. Generating the line BEFORE the
    # mix keeps that true; hook_vo.py, which mixes onto an existing mp4, does
    # not and is for one-off experiments only.
    vo = a.vo
    if vo is None:
        vo = out.resolve().parent / (out.stem + '-hook.wav')
        na, nb = display_names(a.game, [a.a, a.b])
        # `--hook` rather than the parts restated here. They were built inline
        # in this file and the app's preview needed the same line; one of the
        # two would have drifted, and the failure mode is a preview that sounds
        # like something the short does not contain.
        print(f"[vo]  {a.voice}  \"{' '.join(cinema_vo.hook_parts(na, nb))}\"")
        print(run([sys.executable, HERE / 'cinema_vo.py', '--a', na, '--b', nb,
                   '--voice', a.voice, '--hook',
                   '--gaps', f'{a.gap},{a.name_gap}', '--out', vo],
                  cwd=HERE).strip())
    m = encode(out, a.fps, a.crf, pathlib.Path(vo).resolve(), keep=a.keep,
               vo_vol=a.vo_vol, vo_at=a.vo_at)
    print(f"\n  {out.name}")
    print(f"  {m['w']}x{m['h']} {m['vcodec']}+{m['acodec']}  {m['dur']}s  "
          f"{m['mb']}MB  {m['lufs']} LUFS  {m['dbtp']} dBTP  "
          f"(limiter {m['limit']})")
    for k, ok in m["pass"].items():
        print(f"    {'PASS' if ok else 'FAIL'}  {k}")
    print("\n  NOT VERIFIED BY THIS TOOL: whether it looks right. "
          "Pull frames and watch it — SHORTSHANDOFF §0.")
    return 0 if all(m["pass"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
