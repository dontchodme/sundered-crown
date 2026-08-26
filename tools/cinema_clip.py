#!/usr/bin/env python3
"""Render the SAME fight twice -- director off, then director on -- to one mp4.

The demo argument in fifteen seconds. Same relics, same seed, same winner, same
duration in match time; the only difference is what the camera and the mix did
with it.

  python3 cinema_clip.py --a gravemourn --b dawnbringer --lead 6 --out clip.mp4

It drives the real frame loop by hand at a fixed wall rate, so the director
runs exactly as it does live -- including the freeze, where the loop feeds the
accumulator nothing and only the impact art advances. Audio is re-rendered
offline through the game's own synth using render.py's proxy trick, against the
WALL timeline rather than the match timeline, because that is what dilation
changes. The score is the tape-slowed bed and the send automation is replayed
from the curve the director actually asked for.
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

HARNESS = r"""
window.__clip = {
  m: null, events: [], curve: [], wall: 0, acc: 0, on: true,

  /* Build the match, run the director's prescan, and fast-forward silently to
     `startAt` seconds of MATCH time so the clip can begin just before the
     moment worth showing. The fast-forward is plain step() at 1x with the
     director idle: it is the same sim, just not photographed. */
  init(idA, idB, seed, on, startAt, intro) {
    const AC = window.AC;
    this.on = on; this.events = []; this.curve = []; this.wall = 0; this.acc = 0;
    window.__frozen = true;                       // the live rAF loop stands down
    CINE.on = on; CINE.interp = true; CINE.reset(); CINE.acc = 0;
    if (on) { const p = cinePlan(idA, idB, seed); CINE.plan = p.cuts; }
    else CINE.plan = [];

    const m = new AC.Match(idA, idB, seed);
    /* On a cold open the card starts DOWN; run_pass raises it on the first
       clank. The fight is then the first thing on screen. */
    m.introT = (intro && !window.__coldOpen) ? AC.CONFIG.intro.dur : 0;
    this.m = m; window.__match = m; AC.__inject && AC.__inject(m);
    const dt = AC.CONFIG.physics.dt;
    let g = 0;
    while (!m.over && m.t < startAt && g++ < 200000) m.step(dt);

    /* Record, do not play. Same technique render.py uses: SFX is a plain
       object, so play() can be replaced without touching the synth. Times are
       WALL times, because that is the timeline the video runs on. */
    const self = this;
    AC.SFX.play = function (kind, p) {
      self.events.push({ t: self.wall, kind, p: p || {} });
    };
    AC.SFX.resume = function () {};
    AC.__draw(m);
    return { seed: m.seed, t: m.t, kill: (CINE.plan.find(c => c.fatal) || {}).t };
  },

  /* One output frame. `raw` is real seconds of video time.
     Routed through CINE.pump and CINE.drawLerped -- the SAME code the live
     page runs -- so the mp4 cannot show something the game does not, which is
     exactly the trap a bespoke capture loop sets. */
  frame(raw, q) {
    const AC = window.AC, m = this.m, dt = AC.CONFIG.physics.dt;
    let alpha = 0;
    if (this.on) {
      alpha = CINE.pump(raw, m, 1);
    } else {
      this.acc += raw;
      let steps = 0;
      while (this.acc >= dt && steps < 4000) { m.step(dt); this.acc -= dt; steps++; }
    }
    if (alpha > 0) CINE.drawLerped(AC.renderer, m, alpha); else AC.__draw(m);
    this.wall += raw;
    this.curve.push([ +this.wall.toFixed(4),
                      this.on ? +CINE.timeScale.toFixed(4) : 1,
                      this.on ? +CINE.send.wet.toFixed(3) : 0,
                      this.on ? Math.round(CINE.send.lp) : 20000,
                      this.on ? +CINE.send.dry.toFixed(3) : 1,
                      +m.t.toFixed(4) ]);
    return { i: document.getElementById('cv').toDataURL('image/jpeg', q).slice(23),
             o: m.over, t: m.t, c: m.clankCount,
             /* the scrunch's verdict beat is an EVENT the capture loop has to
                wait for; a frame count cannot see it. See run_pass. */
             sm: m.scrunchMode || null,
             ts: this.on ? CINE.timeScale : 1 };
  },

  /* Raise the fight card mid-match, for a cold open. step() gates the whole
     simulation on introT, so the fight FREEZES rather than rewinds and
     resumes on the identical frame. Unlike render.py this needs no audio
     remapping: events here are stamped at WALL time, which keeps advancing
     under the card, so the mix already lines up with the picture. */
  raiseCard(sec) { this.m.introT = sec; return this.m.t; },

  /* ---- offline audio -------------------------------------------------------
     render.py's proxy: play() reads this.ctx.currentTime, so the context is
     wrapped in a proxy whose currentTime is the event's scheduled time. The
     synth is not modified. Added here on top of that: the director's send
     (lowpass -> convolver -> duck) and the tape-slowed bed, both replayed from
     the recorded curve so the mix matches the picture frame for frame. */
  async renderAudio(dur) {
    const AC = window.AC, sr = 48000, tail = 2.4;
    const oc = new OfflineAudioContext(2, Math.ceil((dur + tail) * sr), sr);
    let cursor = 0;
    const proxy = new Proxy(oc, {
      get(t, k) {
        if (k === 'currentTime') return cursor;
        const v = Reflect.get(t, k);
        return typeof v === 'function' ? v.bind(t) : v;
      },
    });

    /* the send */
    const input = oc.createGain();
    const lp = oc.createBiquadFilter(); lp.type = 'lowpass'; lp.Q.value = 0.7;
    const dry = oc.createGain();
    const conv = oc.createConvolver(); conv.buffer = CineAudio.hall(oc, 2.6, 2.4);
    const wet = oc.createGain(); wet.gain.value = 0;
    input.connect(lp); lp.connect(dry); dry.connect(oc.destination);
    lp.connect(conv); conv.connect(wet); wet.connect(oc.destination);

    let pw = -1, pl = -1, pd = -1;
    for (const [t, ts, w, f, d] of this.curve) {
      if (w !== pw) { wet.gain.setValueAtTime(w, t); pw = w; }
      if (f !== pl) { lp.frequency.setValueAtTime(f, t); pl = f; }
      if (d !== pd) { dry.gain.setValueAtTime(d, t); pd = d; }
    }

    /* the synth, pointed at the send */
    const S = Object.create(Object.getPrototypeOf(AC.SFX));
    S.ok = true; S.on = true; S.ctx = proxy;
    S.bus = AC.SFX.constructor.buildChain(oc, input);
    S.noise = S._noiseBuffer.call({ ctx: oc });
    for (const e of this.events) { cursor = Math.max(0, e.t); S.play(e.kind, e.p); }

    /* the bed, on tape. Rendered at rate 1 through the game's own bed(), then
       played back with the playbackRate the director asked for at each frame --
       so when the picture drags, the music drags and drops in pitch with it. */
    /* The bed is consumed at playbackRate, so BED time and WALL time diverge
       as soon as a set-piece drags the tape. Over a six-second clip that is
       invisible; over a full 45s fight it is not, because the score steps a
       level and adds a voice at each seal and those steps have to land ON the
       seals. So: integrate the rate to get bed time per frame, find the frame
       where the match clock crosses each seal, and schedule the bed's seals at
       THOSE bed times. */
    const bedT = []; let bt = 0, pwall = 0;
    for (const row of this.curve) {
      const [w, ts] = row;
      bt += Math.max(0.06, Math.min(1, this.on ? ts : 1)) * (w - pwall);
      pwall = w; bedT.push(bt);
    }
    const sealMatch = AC.CONFIG.acts.slice(1).map(a => a.t);
    const sealBed = [];
    for (const st of sealMatch) {
      const i = this.curve.findIndex(r => r[5] >= st);
      if (i >= 0) sealBed.push(+bedT[i].toFixed(3));
    }

    let bedBuf = null;
    try {
      const bd = bt + 4;
      const ob = new OfflineAudioContext(2, Math.ceil(bd * 44100), 44100);
      const S2 = Object.create(Object.getPrototypeOf(AC.SFX));
      S2.ok = true; S2.on = true; S2.ctx = ob;
      S2.bus = ob.createGain(); S2.bus.connect(ob.destination);
      S2.noise = S2._noiseBuffer.call({ ctx: ob });
      S2.bed.call(S2, 0, bd, sealBed);
      bedBuf = await ob.startRendering();
    } catch (e) { bedBuf = null; }

    if (bedBuf) {
      const src = oc.createBufferSource(); src.buffer = bedBuf;
      const g = oc.createGain(); g.gain.value = 0.9;
      src.connect(g); g.connect(input);
      let pr = -1;
      for (const [t, ts] of this.curve) {
        const v = Math.max(0.06, Math.min(1, this.on ? ts : 1));
        if (Math.abs(v - pr) > 0.01) { src.playbackRate.setValueAtTime(v, t); pr = v; }
      }
      src.start(0);
    }

    const buf = await oc.startRendering();
    /* 16-bit stereo wav */
    const n = buf.length, L = buf.getChannelData(0), R = buf.getChannelData(1);
    const bytes = new Uint8Array(44 + n * 4), dv = new DataView(bytes.buffer);
    const wr = (o, s) => { for (let i = 0; i < s.length; i++) dv.setUint8(o + i, s.charCodeAt(i)); };
    wr(0, 'RIFF'); dv.setUint32(4, 36 + n * 4, true); wr(8, 'WAVEfmt ');
    dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 2, true);
    dv.setUint32(24, sr, true); dv.setUint32(28, sr * 4, true);
    dv.setUint16(32, 4, true); dv.setUint16(34, 16, true);
    wr(36, 'data'); dv.setUint32(40, n * 4, true);
    let o = 44;
    for (let i = 0; i < n; i++) {
      for (const C of [L, R]) {
        let v = Math.max(-1, Math.min(1, C[i]));
        dv.setInt16(o, v < 0 ? v * 32768 : v * 32767, true); o += 2;
      }
    }
    let bin = '';
    for (let i = 0; i < bytes.length; i += 8192)
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 8192));
    return btoa(bin);
  },
};
"""


def run_pass(page, idA, idB, seed, on, start_at, fps, max_secs, q, outdir, tag,
             intro=False, cold_open=None, verdict_hold=2.4):
    page.evaluate("([c]) => { window.__coldOpen = c; }", [cold_open is not None])
    info = page.evaluate("([a,b,s,o,t,i]) => window.__clip.init(a,b,s,o,t,i)",
                         [idA, idB, seed, on, start_at, intro])
    card_up = cold_open is None or not intro
    cut_t = -1.0
    # WALL seconds to the first clank. `scrunchAuto` arms the tape on exactly
    # this event (`!this.scrunchMode && this.clankCount > 0`), so with the card
    # gone this is where the introduction actually happens on screen -- and the
    # director dilates, so it is not the sim time and cannot be computed from it.
    clank_wall = None
    raw = 1.0 / fps
    frames, i = [], 0
    t0 = time.time()
    hit_cap = True
    while i < int(max_secs * fps):
        r = page.evaluate("([raw,q]) => window.__clip.frame(raw,q)", [raw, q])
        if not card_up and (r["c"] > 0 or r["t"] >= cold_open):
            # The EVENT is the anchor; the clock is only a cap. Measured over
            # 144 matches, a timer alone cuts mid-approach: 17% have clanked
            # by 1.5s, 48% by 3.0s.
            cut_t = page.evaluate("([s]) => window.__clip.raiseCard(s)",
                                  [page.evaluate("AC.CONFIG.intro.dur")])
            card_up = True
            print(f"    cold open ends at sim {cut_t:.2f}s "
                  f"({'first clank' if r['c'] > 0 else 'cap'})")
        if clank_wall is None and r["c"] > 0:
            clank_wall = i / fps
        p = outdir / f"{tag}_{i:05d}.jpg"
        p.write_bytes(base64.b64decode(r["i"]))
        frames.append(p)
        i += 1
        if r["o"]:
            # THE TAIL IS ANCHORED ON THE VERDICT EVENT, NOT ON A FRAME COUNT.
            #
            # A flat 2.2s tail shipped a broken ending on every scrunch build and
            # the failure was invisible in the pass marks. `CONFIG.scrunch
            # .resultDelay` is 1.05s of MATCH time, and the kill is exactly where
            # the director is running the tape slowest, so that 1.05s stretches to
            # ~2.0s of VIDEO -- measured on slagheart v aureole 1970938319:
            #
            #     verdict panel armed at +2.00s of video after `over`
            #     old fixed tail                     2.20s
            #     -> the payoff beat got 12 frames and then capture stopped
            #
            # The stretch factor is the cut's timeScale, which differs per fight,
            # so any constant here is wrong for some fight. Wait for the event.
            held, cap = 0, int(fps * (verdict_hold + 8.0))
            for k in range(cap):
                r2 = page.evaluate("([raw,q]) => window.__clip.frame(raw,q)", [raw, q])
                p2 = outdir / f"{tag}_{i:05d}.jpg"
                p2.write_bytes(base64.b64decode(r2["i"]))
                frames.append(p2)
                i += 1
                if r2.get("sm") == "result":
                    held += 1
                    if held >= int(fps * verdict_hold):
                        break
                elif r2.get("sm") is None and k >= int(fps * 2.2):
                    break        # no scrunch on this build: the old 2.2s tail
            else:
                print(f"    !! verdict never armed in {cap/fps:.1f}s of tail")
            if held:
                print(f"    verdict panel held {held/fps:.2f}s of the "
                      f"{(k+1)/fps:.2f}s tail (armed {(k+1-held)/fps:.2f}s after the kill)")
            hit_cap = False
            break
    if hit_cap:
        print(f"    !! CAPTURE HIT THE {max_secs:.0f}s CAP BEFORE THE MATCH "
              f"ENDED — this clip has no ending. Raise --lead's cap or shorten "
              f"the window; do not ship it.")
    dur = len(frames) / fps
    wav_b64 = page.evaluate("(d) => window.__clip.renderAudio(d)", dur + 0.5)
    wav = outdir / f"{tag}.wav"
    wav.write_bytes(base64.b64decode(wav_b64))
    print(f"    {tag}: {len(frames)} frames, {dur:.1f}s wall, "
          f"{time.time()-t0:.0f}s to render, match ended {info}")
    info = dict(info or {}); info['clankWall'] = clank_wall
    return frames, wav, dur, info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sc-cinema.html")
    ap.add_argument("--a", default="gravemourn")
    ap.add_argument("--b", default="dawnbringer")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--lead", type=float, default=6.0,
                    help="seconds of match time before the kill to start from")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--q", type=float, default=0.80)
    ap.add_argument("--crf", type=int, default=22)
    ap.add_argument("--out", default="cinema-clip.mp4")
    ap.add_argument("--cold-open", type=float, nargs="?", const=5.0, default=None,
                    metavar="CAP",
                    help="open on the fight and play the card on the first "
                         "clank, or at CAP seconds, whichever comes first. "
                         "Requires --intro. Roster p75 of first clank is 4.58s.")
    ap.add_argument("--verdict-hold", type=float, default=2.4,
                    help="seconds to hold the scrunch VERDICT panel after it "
                         "arms. The tail waits for the event, so this is a real "
                         "hold and not a guess at when it appears.")
    ap.add_argument("--intro", action="store_true",
                    help="DEAD. The 4s intro card was replaced by the scrunch "
                         "and Rick has asked for it to stop appearing: "
                         "\"id like the fight cards to die completely. they "
                         "have been replaced with the scrunch and thats the "
                         "only thing id like to see going forward.\" Requires "
                         "--legacy-card to actually render, and nothing "
                         "shipping should pass either.")
    ap.add_argument("--legacy-card", action="store_true",
                    help="unlock --intro / --cold-open. Present so the rule is "
                         "ENFORCED rather than remembered: three clips went out "
                         "with the card on because the flag was in a command "
                         "somebody copied.")
    ap.add_argument("--vo", default=None,
                    help="wav to mix over the start (made by cinema_vo.py)")
    ap.add_argument("--vo-at", default="0.3",
                    help="seconds into the video to place the voiceover, or "
                         "'clank' to place it on the first clank -- which is "
                         "where the scrunch arms, and therefore where the "
                         "introduction happens when there is no intro card. "
                         "0.3 (into the card) is the historical behaviour and "
                         "stays the default so nothing that worked changes.")
    ap.add_argument("--capture-only", action="store_true",
                    help="stop after frames + wav (finish with --encode-only); "
                         "the two halves each fit the tool window where the "
                         "whole no longer does at shorts resolution")
    ap.add_argument("--encode-only", action="store_true",
                    help="encode previously captured frames")
    ap.add_argument("--shorts", action="store_true",
                    help="delivery encode for TikTok/YT Shorts: loudness "
                         "normalised to -14 LUFS / -1.5 dBTP, faststart")
    ap.add_argument("--full", action="store_true",
                    help="render the whole match from t=0 rather than a window "
                         "around the finish")
    ap.add_argument("--ab", action="store_true",
                    help="also render the director-OFF half. Off by default: "
                         "the A/B has served its purpose and nobody needs to "
                         "watch the control a fourth time.")
    a = ap.parse_args()

    # THE CARD IS DEAD. The scrunch replaced it and Rick wants it gone from
    # everything shipping. A flag that merely defaults off is a flag that comes
    # back the first time a command is copied from a doc -- which is exactly how
    # it came back three times in v40 -- so it refuses instead.
    if (a.intro or a.cold_open is not None) and not a.legacy_card:
        raise SystemExit(
            "--intro / --cold-open render the retired fight card.\n"
            "  The scrunch replaced it and it is the only opening that ships.\n"
            "  Drop the flags, or pass --legacy-card if you genuinely want the\n"
            "  old card and know why.")

    out = pathlib.Path(a.out).resolve()
    tmp = out.parent / "_clip_frames"
    tmp.mkdir(exist_ok=True)
    # NOT ON --encode-only. This ran unconditionally and deleted the frames
    # the encode pass was about to read, so the two-step flow this tool's own
    # --help advertises ("stop after frames + wav; finish with --encode-only")
    # could never once have completed. Caught the first time anyone split a
    # render at shorts resolution, which is exactly the case the flag exists
    # for -- so it had been broken for as long as it had been needed.
    if not a.encode_only:
        for f in tmp.glob("*"):
            f.unlink()

    seed = a.seed if a.seed is not None else 2901315739

    if a.encode_only:
        f_on = sorted(tmp.glob("on_*.jpg")); w_on = tmp / "on.wav"
        d_on = len(f_on) / a.fps; d_off = 0.0; f_off = w_off = None
        cap = 0
    else:
      with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        page.evaluate(f"AC.setResolution({a.w}, {round(a.w*16/9)})")
        page.evaluate(HARNESS)

        # Where is the killing blow? Ask the prescan, then back up `lead`.
        plan = page.evaluate("([a,b,s]) => window.cinePlan(a,b,s)",
                             [a.a, a.b, seed])
        kill = next((c for c in plan["cuts"] if c.get("fatal")), None)
        if not kill:
            print("no killing blow on this seed (timeout finish); using the last cut")
            kill = plan["cuts"][-1]
        start = 0.0 if a.full else max(0.0, kill["t"] - a.lead)
        print(f"seed {seed}: kill at {kill['t']:.2f}s, clip starts at {start:.2f}s")
        print(f"cut list: " + ", ".join(
            f"{c['t']:.1f}s {'KILL' if c.get('fatal') else 'T'+str(c['tier'])}"
            for c in plan["cuts"]))

        # SECONDS OF VIDEO against a window measured in seconds of MATCH, and
        # the director dilates between the two. 2.6x covers every cut tier plus
        # the split holds that stop the hall for 1.55s a cast, which is a
        # dilation source no ultimate had when the old `lead + 14` was written.
        cap = 150 if a.full else a.lead * 2.6 + 16
        d_off = 0.0
        if a.ab:
            print("  rendering director OFF ...")
            f_off, w_off, d_off, _ = run_pass(page, a.a, a.b, seed, False, start,
                                              a.fps, cap, a.q, tmp, "off")
        print("  rendering director ON ...")
        f_on, w_on, d_on, info_on = run_pass(page, a.a, a.b, seed, True, start,
                                       a.fps, cap, a.q, tmp, "on",
                                       intro=a.full and a.intro,
                                       verdict_hold=a.verdict_hold,
                                       cold_open=a.cold_open)
        if errors:
            print("  page errors:", errors[:4])
    if a.capture_only:
        print(f"captured; finish with --encode-only")
        return 0

    # stitch: OFF, then ON, with a title on each half burned in by ffmpeg
    parts = []
    segs = ([("off", f_off, w_off, "DIRECTOR OFF")] if a.ab else []) \
           + [("on", f_on, w_on, "DIRECTOR ON" if a.ab else None)]
    for tag, frames, wav, label in segs:
        seg = tmp / f"{tag}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-framerate", str(a.fps), "-i", str(tmp / f"{tag}_%05d.jpg"),
             "-i", str(wav),
             # trunc/2*2 first: libx264 rejects an odd dimension, and a
             # width-derived vertical frame lands on one about half the time.
             # Shorts delivery is 1080x1920. The platform call limit cannot fit
             # a native-1080 capture in one run, so frames are captured smaller
             # and scaled here, in the ONE encode -- no second generation.
             # PLATFORM-SAFE COMPOSITION, AND IT IS NOT DONE HERE ANY MORE.
             #
             # This used to read `scale=852:1512,pad=1080:1920:114:96`, which
             # shrank the whole video to 79% and boxed it so that TikTok's
             # caption bar could not cover the bottom wall. The diagnosis was
             # right -- cinema_edge_probe showed the FILE was clean, 0/8 wall
             # cuts clipped the near relic, and the platform was covering it --
             # but the fix was in the wrong place: it spends every pixel in the
             # frame to protect the bottom sixth of it, and Rick's read of the
             # result was "poorly cropped ... missing a lot of the bottom of
             # the frame."
             #
             # The reserve lives in the GAME now (FRAME.foot, frame_build.py):
             # the arena fits a box instead of a width and ends above the safe
             # line, so the strip the platform draws over is background rather
             # than playfield. That leaves this encode with nothing to do but
             # deliver what was rendered, full-bleed. A source that is already
             # exactly 9:16 scales to 1080x1920 with no padding at all.
             #
             # A build WITHOUT FRAME still renders its hall down to y=1800 and
             # will have its bottom wall covered. That is the correct trade to
             # surface loudly rather than to paper over here a second time.
             "-vf", ("scale=1080:1920:flags=lanczos" if a.shorts
                     else "scale=trunc(iw/2)*2:trunc(ih/2)*2") + (
                     f",drawtext=text='{label}':x=(w-tw)/2:y=h-52:"
                     f"fontsize=22:fontcolor=0xC9A227:box=1:boxcolor=0x000000AA:"
                     f"boxborderw=8" if label else ""),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", str(a.crf),
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ac", "2",
             "-shortest", str(seg)], check=True)
        parts.append(seg)

    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    if a.vo or a.shorts:
        # DELIVERY PASS. TikTok and Shorts normalise to about -14 LUFS and
        # these renders sit ~6 dB under that (a standing note on the project;
        # "optimise for those formats" is the direction that makes the call).
        # The VO is delayed 300ms into the card, gently lifted, and the whole
        # mix is loudnorm'd in one pass. Video stream is copied untouched.
        raw = out.with_name(out.stem + "_raw.mp4")
        out.rename(raw)
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw)]
        if a.vo:
            if a.vo_at == "clank":
                cw = (info_on or {}).get("clankWall")
                if cw is None:
                    print("    NO CLANK in this fight -- the scrunch never armed, "
                          "so the voiceover has nowhere to sit. Falling back to 0.3s.")
                    vo_ms = 300
                else:
                    vo_ms = int(round(cw * 1000))
                    print(f"    voiceover placed on the first clank, {cw:.2f}s "
                          f"of video (the scrunch arms there)")
            else:
                vo_ms = int(round(float(a.vo_at) * 1000))
            cmd += ["-i", a.vo, "-filter_complex",
                    f"[1:a]aresample=48000,adelay={vo_ms}|{vo_ms},volume=1.5,apad[v1];"
                    "[0:a][v1]amix=inputs=2:duration=first:normalize=0[m];"
                    "[m]loudnorm=I=-14:TP=-1.5:LRA=11[a]"]
        else:
            cmd += ["-filter_complex", "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]"]
        cmd += ["-map", "0:v", "-map", "[a]", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
        raw.unlink()

    mb = out.stat().st_size / 1024 / 1024
    print(f"\nwrote {out}  {mb:.2f} MB  "
          f"({d_off:.1f}s off + {d_on:.1f}s on)")
    print("the two halves are the same seed. If the winner differs, the "
          "feature is broken.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
