#!/usr/bin/env python3
"""Render one Sundered Crown match to a finished vertical mp4.

This replaces the screen-capture pipeline entirely: the sim is stepped in
lockstep with the renderer so a frame is never dropped or duplicated, and the
audio is re-rendered offline from the sim's own event log through the game's
own synth, so the video sounds exactly like the live match.

  python3 render.py --a gravemourn --b dawnbringer --seed 2901315739 --out fight.mp4
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import subprocess
import sys
import time

from scpage import game

HERE = pathlib.Path(__file__).parent
COMMIT_LIMIT = 20 * 1024 * 1024  # device_commit_files rejects anything larger

# -19.5, and here is the MEASURED cost curve rather than a vibe.
#
# A CORRECTION, 2026-08-13. A session raised this to -17.0 on the reasoning
# that the delivered file peaked at -4.12 dBTP against a -1.5 ceiling, so
# 2.6 dB were free. That reasoning was wrong in a way worth naming: -4.12 dBTP
# is the OUTPUT of this very loudnorm call. It says nothing about the input.
#
# The raw mix, measured directly off the kept wav:
#
#   I -19.89 LUFS   TP +0.07 dBTP   LRA 2.40
#
# It is already OVER full scale before mastering. There is no headroom at all,
# `linear=true` cannot stay linear, and every dB of loudness is bought with
# limiting. The comment that used to stand here -- "it needs either a drone
# louder than the fight or heavy limiting on the transients that carry the hit
# stop" -- was right, and the correction was the error.
#
# What IS new is the price, measured on real renders of the same seed over 24
# transient events (punch = peak(+-6 ms) / RMS(150 ms before)):
#
#   LUFS_TARGET   punch mean   vs -19.5      loudness vs platform norm
#      -19.5        15.03 dB     baseline      5.9 dB under
#      -17.0        13.80 dB     -1.23 dB      3.4 dB under
#      -14.0        (~-2.5 to -3 dB, extrapolated; not rendered)
#
# So: roughly HALF A dB OF PUNCH PER dB OF LOUDNESS, all the way down. No free
# portion. Staying at -19.5 until an ear says otherwise, because every platform
# that normalises will lift this to -14 by itself without touching a transient.
LUFS_TARGET = -19.5
TP_TARGET = -1.5


def measure_loudness(wav: pathlib.Path) -> dict:
    """First loudnorm pass. Two-pass is the only accurate way to hit a target."""
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(wav),
         "-af", f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    tail = p.stderr[p.stderr.rfind("{"):]
    tail = tail[: tail.find("}") + 1]
    return json.loads(tail)

# Installed into the page once, then driven a frame at a time from Python.
CAPTURE_JS = r"""
window.__cap = {
  events: [], m: null,

  init(idA, idB, seed, introSec) {
    window.__frozen = true;                 // stop the rAF loop stepping the sim
    AC.setResolution(1080, 1920);           // the live page fits the window; the video does not
    const m = new AC.Match(idA, idB, seed >>> 0);
    m.introT = introSec;                    // 0 disables the card entirely
    AC.__inject(m);
    this.m = m;
    this.events.length = 0;
    const self = this;
    // Trap the sim's own sound calls with their match timestamps. The sim is
    // not modified; SFX is just a normal object and play is a normal property.
    /* `intro` is the card clock AT THE MOMENT THE SOUND FIRED. It is the
       only way to tell the card's own clank from a clank in the hall:
       both are pushed with the same frozen m.t. */
    AC.SFX.play = function (kind, p) {
      self.events.push({ t: m.t, intro: m.introT, kind, p: p || {} });
    };
    AC.SFX.resume = function () {};
    AC.__draw(m);
    return { seed: m.seed, a: m.a.w.name, b: m.b.w.name };
  },

  frame(steps, q) {
    for (let i = 0; i < steps; i++) this.m.step(AC.CONFIG.physics.dt);
    AC.__draw(this.m);
    const m = this.m;
    return {
      i: document.getElementById('cv').toDataURL('image/jpeg', q).slice(23),
      o: m.over, t: m.t, c: m.clankCount,
    };
  },

  /* Raise the card mid-match. Nothing else is touched: step() gates the
     whole simulation on introT, so the fight is frozen, not rewound, and
     it resumes on the identical frame. Returns the match time of the cut,
     which the audio pass needs to place events either side of it. */
  raiseCard(sec) { this.m.introT = sec; return this.m.t; },

  state() {
    const m = this.m;
    return { over: m.over, t: m.t, clanks: m.clankCount,
             winner: m.winner ? m.winner.w.name : null, reason: m.reason };
  },

  summary() { return this.m.summary(); },

  /* ---- offline audio -----------------------------------------------------
     Re-uses the game's own Sfx voices against an OfflineAudioContext. play()
     reads this.ctx.currentTime, so the context is wrapped in a proxy whose
     currentTime is the event's match time. Nothing in the synth changes. */
  /* `offset` is the intro-card duration. The match clock is held at zero while
     the card is up, so every recorded event time is relative to the bell, not
     to the first frame of video. Without this the whole soundtrack plays early
     by the length of the card. */
  async renderAudio(dur, offset, cutT) {
    /* cutT < 0 means the card was first and every event sits after it --
       the original behaviour. Otherwise the mix has three regions:
         ev.intro > 0     the card's own clank: placed by how much card
                          was left when it fired
         ev.t <= cutT     fight audio from the cold open: NOT shifted
         ev.t >  cutT     fight audio after the card: shifted by offset
       The triggering clank itself sits exactly at cutT and belongs to the
       cold open, so the comparison is strict. */
    const vtime = (t, intro) =>
      (intro > 0) ? cutT + (offset - intro)
                  : (cutT < 0 || t > cutT) ? t + offset : t;
    const sr = 48000, tail = 2.0;
    const oc = new OfflineAudioContext(1, Math.ceil((dur + tail) * sr), sr);
    let cursor = 0;
    const proxy = new Proxy(oc, {
      get(t, k) {
        if (k === 'currentTime') return cursor;
        const v = Reflect.get(t, k);
        return typeof v === 'function' ? v.bind(t) : v;
      },
    });

    const S = Object.create(Object.getPrototypeOf(AC.SFX));
    S.ok = true; S.on = true; S.ctx = proxy;
    // Same chain builder the live context uses, so the two cannot diverge.
    S.bus = S.constructor.buildChain(oc, oc.destination);

    // deterministic noise so two renders of one seed are bit-identical
    const n = Math.floor(sr * 0.6);
    const nb = oc.createBuffer(1, n, sr);
    const d = nb.getChannelData(0);
    let s = 0x9e3779b9;
    for (let i = 0; i < n; i++) {
      s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0;
      d[i] = (s / 4294967296) * 2 - 1;
    }
    S.noise = nb;

    /* The bed, through the game's own implementation. Seal times are offset
       by the intro because the match clock is held at zero while the card is
       up. Scheduled from 0 so the drone covers the card too — four seconds of
       silence before the bell was its own problem. */
    cursor = 0;
    try {
      S.bed(0, dur + tail,
            AC.CONFIG.acts.slice(1).map(a => vtime(a.t, 0)));
    } catch (e) { /* never break the render */ }

    for (const ev of this.events) {
      cursor = vtime(ev.t, ev.intro || 0);
      try { S.play(ev.kind, ev.p); } catch (e) { /* never break the render */ }
    }

    const buf = await oc.startRendering();
    const len = buf.length, ch = buf.getChannelData(0);
    const bytes = 44 + len * 2;
    const ab = new ArrayBuffer(bytes), dv = new DataView(ab);
    const ws = (o, str) => { for (let i = 0; i < str.length; i++) dv.setUint8(o + i, str.charCodeAt(i)); };
    ws(0, 'RIFF'); dv.setUint32(4, bytes - 8, true); ws(8, 'WAVE');
    ws(12, 'fmt '); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true);
    dv.setUint16(22, 1, true); dv.setUint32(24, sr, true);
    dv.setUint32(28, sr * 2, true); dv.setUint16(32, 2, true); dv.setUint16(34, 16, true);
    ws(36, 'data'); dv.setUint32(40, len * 2, true);
    for (let i = 0; i < len; i++) {
      const v = Math.max(-1, Math.min(1, ch[i]));
      dv.setInt16(44 + i * 2, v < 0 ? v * 0x8000 : v * 0x7fff, true);
    }
    let bin = '';
    const u8 = new Uint8Array(ab);
    for (let i = 0; i < u8.length; i += 0x8000) {
      bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
    }
    return btoa(bin);
  },
};
"""


def render(a, b, seed, out, fps=30, hold=3.8, quality=0.94, max_seconds=90,
           headless=True, verbose=True, keep=False, intro=None, game_path=None,
           cold_open=None):
    if seed is None:
        raise SystemExit("--seed is required; a render must be reproducible")
    out = pathlib.Path(out)
    tmp_wav = out.with_suffix(".wav")
    t_start = time.time()

    with game(headless=headless, game_path=game_path) as (page, errors):
        page.evaluate(CAPTURE_JS)
        sim_dt = page.evaluate("AC.CONFIG.physics.dt")
        steps = round((1.0 / fps) / sim_dt)
        if abs(steps * sim_dt - 1.0 / fps) > 1e-9:
            raise SystemExit(
                f"fps {fps} does not divide the {1/sim_dt:.0f}Hz sim evenly "
                f"({steps} steps = {steps*sim_dt:.5f}s, want {1/fps:.5f}s)"
            )

        if intro is None:
            intro = page.evaluate("AC.CONFIG.intro.dur")
        # The card must be a whole number of output frames or the bell drifts
        # off the cut by up to one frame.
        intro = round(intro * fps) / fps
        # On a cold open the card starts DOWN and is raised on the first
        # clank (or at the cap), so the fight opens on the hall.
        page.evaluate("([a,b,s,i]) => window.__cap.init(a,b,s,i)",
                      [a, b, seed, 0.0 if cold_open is not None else intro])
        cut_t = -1.0            # match time of the cut; <0 means no cold open
        card_up = cold_open is None

        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-an",
             str(out.with_suffix(".video.mp4"))],
            stdin=subprocess.PIPE,
        )

        n = 0
        hold_frames = int(hold * fps)
        held = 0
        cap_frames = int(max_seconds * fps)
        while True:
            fr = page.evaluate("([s,q]) => window.__cap.frame(s,q)", [steps, quality])
            proc.stdin.write(base64.b64decode(fr["i"]))
            n += 1
            if verbose and n % (fps * 5) == 0:
                print(f"  {n/fps:5.1f}s  sim {fr['t']:5.1f}s  "
                      f"{fr['c']} clanks", flush=True)
            if not card_up and (fr["c"] > 0 or fr["t"] >= cold_open):
                # The event is the anchor and the clock is only the cap. A
                # timer alone would cut mid-approach: only 17% of matches
                # have clanked by 1.5s, 48% by 3.0s (144-match sweep).
                cut_t = page.evaluate("([s]) => window.__cap.raiseCard(s)",
                                      [intro])
                card_up = True
                if verbose:
                    why = "first clank" if fr["c"] > 0 else "cap"
                    print(f"  cold open ends at sim {cut_t:.2f}s ({why}); "
                          f"card up for {intro:.2f}s", flush=True)
            if fr["o"]:
                held += 1
                if held >= hold_frames:
                    break
            if n >= cap_frames:
                print("hit the frame cap before the match ended", file=sys.stderr)
                break

        proc.stdin.close()
        proc.wait()

        summary = page.evaluate("window.__cap.summary()")
        events = page.evaluate("window.__cap.events.length")
        dur = n / fps
        wav_b64 = page.evaluate("([d,o,c]) => window.__cap.renderAudio(d,o,c)",
                                [dur, intro, cut_t])
        tmp_wav.write_bytes(base64.b64decode(wav_b64))
        if not wav_b64:
            raise SystemExit("offline audio render returned nothing")

        if errors:
            raise SystemExit("page errors during render:\n  " + "\n  ".join(errors))

    loud = measure_loudness(tmp_wav)

    # Mux, capping the bitrate so the result stays inside the commit limit.
    budget_bits = int(COMMIT_LIMIT * 8 * 0.90)
    v_bitrate = max(1_200_000, int(budget_bits / max(dur, 1)) - 128_000)
    af = (
        f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA=11"
        f":measured_I={loud['input_i']}:measured_TP={loud['input_tp']}"
        f":measured_LRA={loud['input_lra']}:measured_thresh={loud['input_thresh']}"
        f":offset={loud['target_offset']}:linear=true:print_format=summary"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(out.with_suffix(".video.mp4")), "-i", str(tmp_wav),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
         "-maxrate", str(v_bitrate), "-bufsize", str(v_bitrate * 2),
         "-pix_fmt", "yuv420p",
         "-af", af,
         "-c:a", "aac", "-b:a", "128k", "-ac", "2",
         "-shortest", "-movflags", "+faststart", str(out)],
        check=True,
    )
    if not keep:
        out.with_suffix(".video.mp4").unlink(missing_ok=True)
        tmp_wav.unlink(missing_ok=True)

    size = out.stat().st_size
    report = {
        "out": str(out), "frames": n, "fps": fps, "duration": round(dur, 2),
        "bytes": size, "mb": round(size / 1024 / 1024, 2),
        "wall_seconds": round(time.time() - t_start, 1),
        "intro_seconds": intro,
        "cold_open_seconds": round(cut_t, 2) if cut_t >= 0 else None,
        "lufs_raw": float(loud["input_i"]), "lufs_target": LUFS_TARGET,
        "true_peak_raw": float(loud["input_tp"]),
        "sfx_events": events,
        **summary,
    }
    # A sparse mix cannot be lifted to platform loudness without crushing the
    # impacts. Say so rather than shipping something that plays back inaudibly.
    # Always state the remaining gap to the platform norm so it stays visible
    # rather than quietly drifting once someone stops looking.
    gap = -14.0 - float(loud["input_i"])
    report["lufs_gap_to_platform"] = round(gap, 1)
    if gap > 4.0:
        report["AUDIO_NOTE"] = (
            f"raw mix is {float(loud['input_i']):.1f} LUFS, {gap:.1f} dB under the ~-14 "
            "platform norm. Closing the rest needs a judgement call with ears: "
            "a louder bed buries the fight, more glue flattens the hit stop."
        )
    if size > COMMIT_LIMIT:
        report["WARNING"] = f"{size} bytes exceeds the {COMMIT_LIMIT} commit limit"
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", default="fight.mp4")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--hold", type=float, default=3.8)
    ap.add_argument("--quality", type=float, default=0.94)
    ap.add_argument("--keep", action="store_true",
                    help="keep the silent video and the wav for audio-only re-muxes")
    ap.add_argument("--intro", type=float, default=None,
                    help="intro card seconds (default: CONFIG.intro.dur)")
    ap.add_argument("--no-intro", action="store_true", help="skip the intro card")
    ap.add_argument("--cold-open", type=float, nargs="?", const=5.0, default=None,
                    metavar="CAP",
                    help="open on the fight and play the card on the first "
                         "clank, or at CAP seconds, whichever comes first "
                         "(default cap 5.0s -- p75 of first clank is 4.58s)")
    ap.add_argument("--quiet", action="store_true")
    # See the note in pick.py. A variant that cannot be rendered cannot be
    # judged, and this project does not accept a change judged from code,
    # statistics or a still.
    ap.add_argument("--game", default=None,
                    help="render a variant HTML instead of sundered-crown.html")
    a = ap.parse_args()
    intro = 0.0 if a.no_intro else a.intro
    print(json.dumps(render(a.a, a.b, a.seed, a.out, fps=a.fps, hold=a.hold,
                            quality=a.quality, verbose=not a.quiet,
                            keep=a.keep, intro=intro, cold_open=a.cold_open,
                            game_path=pathlib.Path(a.game).resolve() if a.game else None),
                     indent=2))


if __name__ == "__main__":
    main()
