#!/usr/bin/env python3
"""THE FOUR CAST VOICES, HEARD INSIDE A REAL FIGHT. v66.

    python corona_voice_audition.py --game ../02-chain/sc-corona-fx.html

Rick, 2026-09-03, handed four bare renders: *"i cant judge the sound like
this."*

HE IS RIGHT AND THIS REPO HAS ALREADY LEARNED IT ONCE. `sentinel_hum_lab`'s
own docstring says a candidate has to be heard ARRIVING the way it will in the
fight, "a hum judged cold is judged in a context the game never produces" --
and `sentinel_hum_audition` was written when a spread turned out to be the
wrong instrument for a timing question. A cast voice is not judged against
silence. It is judged against a hall with two balls in it, the clanks, the
hits, the seal, and whatever the other relic is doing.

SO THIS RECORDS A REAL WINDOW AND REPLAYS IT FOUR TIMES. One match is driven
to a real Corona cast; every `SFX.play` call the engine makes across the clip's
own fourteen seconds is written down with its time; and the whole list is then
rendered four times, IDENTICAL except that the cast's own call is replaced by
one of the four candidates. Nothing is invented and nothing is re-timed.

WHAT COMES OUT IS FOUR MP4s WITH THE SAME PICTURE. The video is muxed from the
clip that already exists, so the only difference between the four files is one
sound at 1.2 seconds. That is the comparison; anything else in the frame moving
between them would be a confound.

THE VOICES ARE A SHARED CONSTANT (`corona_voice_lab.VOICES_JS`) and not a copy.
A hand-copied recipe in a second file is how a lab and its audition come to
disagree about what was auditioned.

Touches no build.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from clip_spread import resolve_ffmpeg  # noqa: E402
from corona_voice_lab import (CANDIDATES, VOICES_JS, POP_CANDIDATES,
                              POP_VOICES_JS, BURN_CANDIDATES,
                              BURN_VOICES_JS, CHAIN_CANDIDATES,
                              CHAIN_VOICES_JS, measure)  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "starwarden"


# RECORD. `SFX.play` returns on its first line headless, which is exactly why
# it can be wrapped this cheaply -- and why a silent ultimate has shipped
# through every other check in this repo (v42, CLAUDE.md 4.1).
RUN_JS = r"""([rid, foe, seed, t0, span]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const S = AC.SFX;
  const log = [];
  let rec = false;
  const orig = S.play.bind(S);
  /* EVERY CALL, NOT JUST THIS RELIC'S. The thing being judged is whether the
     cast can be heard and read among the sounds the fight is already making,
     so a recording filtered down to the ultimate would be a second version of
     the bare render Rick has already rejected. */
  S.play = function(kind, p){
    if (rec) log.push({ kind: kind, p: p ? JSON.parse(JSON.stringify(p)) : null,
                        t: m.t - t0 });
    return orig(kind, p);
  };
  let step = 0, castAt = -1, popAt = -1;
  const burnTs = [], chainTs = [];
  let lastEntries = 0, lastChained = 0;
  while (!m.over && step < 156 / DT){
    const had = !!me.ultCorona;
    const wasPopped = had && me.ultCorona.popped;
    m.step(DT); step++;
    if (!rec && m.t >= t0) rec = true;
    const C = me.ultCorona;
    if (rec && !had && C && castAt < 0) castAt = m.t - t0;
    /* THE POP IS SILENT IN THE BUILD, so there is no call to substitute --
       its moment is read off the sim's own `popped` transition and the
       candidate is INJECTED there. That is the difference between auditioning
       a replacement and auditioning something that does not exist yet. */
    if (rec && popAt < 0 && C && C.popped && !wasPopped)
      popAt = m.t - t0;
    /* THE CROSSINGS AND THE CHAINED DETONATIONS ARE COUNTERS, so their
       moments are TRANSITIONS in them and not frames on which something was
       true -- five times in one file in v60, and it is the default way a probe
       goes wrong on this engine. */
    if (rec && C){
      if (C.entries > lastEntries){ burnTs.push(m.t - t0); }
      if (C.chained > lastChained){ chainTs.push(m.t - t0); }
      lastEntries = C.entries; lastChained = C.chained;
    }
    if (rec && m.t - t0 > span) break;
  }
  S.play = orig;
  return { log, castAt, popAt, burnTs, chainTs, n: log.length };
}"""


# RENDER the recorded list, with ONE substitution.
RENDER_JS = r"""async ([log, secs, ats, pick, voices, rid, inject, indexed]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  /* SCHEDULED AT AN ABSOLUTE TIME. `SFX.play` reads `this.ctx.currentTime`,
     which is 0 for the whole of an offline render -- so without this proxy
     every sound in fourteen seconds of fight would land on the same frame.
     `sentinel_hum_audition` is where this trick is from. */
  let now = 0;
  const proxy = new Proxy(oc, { get(o, k){
    if (k === 'currentTime') return now;
    const v = Reflect.get(o, k);
    return typeof v === 'function' ? v.bind(o) : v; } });
  S.ctx = proxy;
  const V = indexed ? null : eval(voices)(S);
  let swapped = 0, played = 0;
  for (const e of log){
    now = Math.max(0, e.t);
    /* THE ONE SUBSTITUTION. The cast is `SFX.play("ult", {w:<relic>})` from
       `fireUlt`; every other call in the list is played exactly as the engine
       played it. `pick < 0` renders the list UNTOUCHED, which is the control:
       it is what the clip Rick already has sounds like, and if it is not
       recognisably that then this tool is measuring something else. */
    if (!inject && pick >= 0 && e.kind === "ult" && e.p && e.p.w === rid){
      V[pick](now); swapped++; continue;
    }
    S.play(e.kind, e.p); played++;
  }
  /* INJECTED rather than substituted, for an event the build makes no sound
     for yet. Played LAST so it is scheduled after every other call, which is
     irrelevant to the render -- these are absolute times -- and is stated so
     nobody reads the order as a mix decision. */
  if (inject && pick >= 0){
    /* EVERY OCCURRENCE, NOT ONE. The burn fires on each crossing and the chain
       on each leftover star, so auditioning a single instance would be
       auditioning a different mechanic -- and the chain's whole question is
       what THREE of them 70ms apart sound like. `indexed` hands the voice its
       place in the run, which only the chain uses. */
    for (let k = 0; k < ats.length; k++){
      now = ats[k];
      const fns = indexed ? eval(voices)(S, k, ats.length) : V;
      fns[pick](now); swapped++;
    }
  }
  const buf = await oc.startRendering();
  S.on=sv.on; S.ok=sv.ok; S.ctx=sv.ctx; S.bus=sv.bus; S.noise=sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  let peak = 0;
  for (let i = 0; i < d.length; i++){ out[i] = d[i];
    const v = Math.abs(d[i]); if (v > peak) peak = v; }
  return { pcm: out, sr, peak: +peak.toFixed(4), swapped, played };
}"""


def write_wav(path, pcm, sr, norm):
    import numpy as np
    d = np.asarray(pcm, dtype=np.float32)
    top = float(np.abs(d).max())
    if top < 1e-6:
        raise SystemExit(f"REFUSING TO WRITE {path.name} -- it rendered "
                         "SILENCE (v42's defect).")
    # NORMALISED AGAINST THE WHOLE SET AND NOT EACH FILE ON ITS OWN. Four
    # clips each normalised to their own peak would be four clips at four
    # different gains, and Rick would be judging loudness rather than register
    # -- which is the single easiest way to make a spread lie.
    pcm = np.clip(d / norm * 0.92, -1, 1)
    w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()
    return top


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--a", default=RID)
    ap.add_argument("--b", default="gravemourn")
    ap.add_argument("--seed", type=int, default=33138)
    ap.add_argument("--at", type=float, default=30.67,
                    help="the clip's own start, in match seconds")
    ap.add_argument("--span", type=float, default=14.0)
    ap.add_argument("--video", default="../07-shorts/v66/corona-window4.mp4",
                    help="the picture to mux onto; the same one for all four")
    ap.add_argument("--event", choices=["cast", "pop", "burn", "chain"],
                    default="cast",
                    help="which voice to audition: the cast (SUBSTITUTED for "
                         "the one the build plays) or the star pop (INJECTED, "
                         "because the build is silent there)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    gp = resolve_game(a.game)
    vid = (HERE / a.video).resolve()
    stem = (HERE / (a.out or f"../05-reference/v66/corona-{a.event}-in-fight")
            ).resolve()
    stem.parent.mkdir(parents=True, exist_ok=True)
    ff = resolve_ffmpeg()

    print(f"\nCORONA -- THE CAST, INSIDE A REAL FIGHT\n"
          f"  {a.a} vs {a.b}, seed {a.seed}, from {a.at:g}s "
          f"for {a.span:g}s\n")
    made = []
    with game(game_path=gp) as (page, errors):
        r = page.evaluate(RUN_JS, [a.a, a.b, a.seed, a.at, a.span])
        assert not errors, errors[:3]
        if r["castAt"] < 0:
            raise SystemExit("no cast inside that window -- run _corona_pick")
        kinds = {}
        for e in r["log"]:
            kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        print(f"  {r['n']} sounds in the window, cast at "
              f"{r['castAt']:.2f}s, pop at {r['popAt']:.2f}s: "
              + ", ".join(f"{k} x{v}" for k, v in
                          sorted(kinds.items(), key=lambda x: -x[1])))
        # THE CONTROL RUNS FIRST AND SETS THE GAIN. It is the list untouched --
        # what the clip Rick already has sounds like.
        SET = {"cast":  (CANDIDATES, VOICES_JS, False, False),
               "pop":   (POP_CANDIDATES, POP_VOICES_JS, True, False),
               "burn":  (BURN_CANDIDATES, BURN_VOICES_JS, True, False),
               "chain": (CHAIN_CANDIDATES, CHAIN_VOICES_JS, True, True)}
        CANDS, SRC, INJECT, INDEXED = SET[a.event]
        ats = {"cast": [r["castAt"]], "pop": [r["popAt"]],
               "burn": r["burnTs"], "chain": r["chainTs"]}[a.event]
        ats = [x for x in ats if x is not None and x >= 0]
        if not ats:
            raise SystemExit(f"no {a.event} inside that window -- run "
                             "_corona_pick or _corona_tight for one that has "
                             "it")
        print(f"  {a.event}: {len(ats)} occurrence(s) at "
              + ", ".join(f"{x:.2f}s" for x in ats[:8])
              + ("..." if len(ats) > 8 else "") + "\n")
        ctrl = page.evaluate(RENDER_JS, [r["log"], a.span + 1.5, ats,
                                         -1, SRC, a.a, INJECT, INDEXED])
        assert not errors, errors[:3]
        assert ctrl["swapped"] == 0
        norm = ctrl["peak"]
        print(f"  control (WHATEVER THIS BUILD SHIPS) renders at peak {norm}, "
              f"{ctrl['played']} calls\n")
        print(f"  {'candidate':<12}{'swapped':>9}{'peak':>8}{'in-fight':>10}")
        # AND THE CONTROL IS WRITTEN OUT TOO, WHICH IS THE GATE ONCE A VOICE
        # HAS LANDED. Before the pick it is the generic fallback; after it, it
        # is the shipped branch -- so `-0` against `-<pick>` is the check that
        # what was BUILT is what was AUDITIONED, and it is a check that can
        # fail. A voice that drifted from the file Rick approved is INAUDIBLE
        # as an error: it simply sounds a little different, and nothing else in
        # this repo would say so.
        cw = stem.with_name(stem.name + "-0.wav")
        write_wav(cw, ctrl["pcm"], ctrl["sr"], norm)
        cm = measure(ctrl["pcm"], ctrl["sr"])
        print(f"  {'0  CONTROL':<12}{0:>9}{ctrl['peak']:>8.3f}"
              f"{1.00:>9.2f}x   what this build actually plays "
              f"({cm['cen']:.0f}Hz)")
        mp0 = stem.with_name(stem.name + "-0.mp4")
        p0 = subprocess.run([ff, "-y", "-i", str(vid), "-i", str(cw),
                             "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                             "-c:a", "aac", "-b:a", "160k", "-shortest",
                             str(mp0)], capture_output=True, text=True)
        if p0.returncode != 0:
            raise SystemExit("ffmpeg mux failed (control):\n"
                             + (p0.stderr or "").strip()[-600:])
        made.append(mp0)
        for i, (name, blurb) in enumerate(CANDS):
            g = page.evaluate(RENDER_JS, [r["log"], a.span + 1.5, ats,
                                          i, SRC, a.a, INJECT, INDEXED])
            assert not errors, errors[:3]
            if g["swapped"] != len(ats):
                raise SystemExit(
                    f"{name}: the voice landed {g['swapped']} times, not "
                    f"{len(ats)}. The recording or the relic id has moved.")
            wav = stem.with_name(stem.name + f"-{i + 1}.wav")
            write_wav(wav, g["pcm"], g["sr"], norm)
            M = measure(g["pcm"], g["sr"])
            print(f"  {name:<12}{g['swapped']:>9}{g['peak']:>8.3f}"
                  f"{M['peak'] / norm:>9.2f}x   {blurb}")
            # MUX ONTO THE SAME PICTURE. `-shortest` so a wav a hair longer
            # than the clip cannot stretch it.
            mp4 = stem.with_name(stem.name + f"-{i + 1}.mp4")
            cmd = [ff, "-y", "-i", str(vid), "-i", str(wav),
                   "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                   "-c:a", "aac", "-b:a", "160k", "-shortest", str(mp4)]
            p = subprocess.run(cmd, capture_output=True, text=True)
            if p.returncode != 0:
                raise SystemExit("ffmpeg mux failed:\n"
                                 + (p.stderr or "").strip()[-800:])
            made.append(mp4)
    print("\n  same picture in all four; the only difference is one sound at "
          f"{r['castAt']:.2f}s")
    for m in made:
        print(f"    {m.name}   {m.stat().st_size / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
