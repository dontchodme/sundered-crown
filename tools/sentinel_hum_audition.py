#!/usr/bin/env python3
"""THE HUM, PLAYED BACK OFF A REAL WINDOW, SO THE CUE IS AUDITIONED AGAINST
THE THING IT IS A CUE FOR.

    python sentinel_hum_audition.py --out ../05-reference/v48-sentinel/hum-load.wav

Rick asked the sustain to carry one specific fact: *"we need the sound effect
to reflect weather or not the beam is connecting. the audio should be our cue
that its doing damage"*, and then said what shape that takes -- *"a static hum
and then the sawtooth of dynamo is the damage connecting"*.

**A SPREAD CANNOT ANSWER THAT AND NEITHER CAN A SYNTHETIC RUN.** Whether a cue
reads depends on the RHYTHM of the thing it is cueing, and this beam's rhythm
is not something anyone gets to choose -- it is a ballistic ball blundering
through a turning line about four times a window, at intervals nothing in the
design sets. So this drives a REAL match to a real cast, records what the
engine actually played and when, and renders exactly that.

What comes out is the audio of one window, in order, with nothing invented:
the release, then the bed, then the dynamo swelling every time the beam is
genuinely on the quarry, with the pass and tip stingers where they truly fell.
If the sawtooth does not line up with the hits in this file, the cue does not
work -- and that is a thing to hear rather than a thing to argue about.

Writes one wav. Touches no build.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

# RECORD, THEN RENDER. The recording wraps `SFX.play` and writes down (voice,
# time, params) for one window -- so what is rendered is the engine's own call
# list and not a second guess at it. `SFX.play` returns on its first line
# headless, which is exactly why it can be wrapped this cheaply.
RUN_JS = r"""([rid, foe, seed, want]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, seed);
  m.slLive = false;
  const me = m.a.w.id === rid ? m.a : m.b;
  const S = AC.SFX;
  const log = [];
  let t0 = null, windows = 0, rec = false;

  const orig = S.play.bind(S);
  S.play = function(kind, p){
    if (rec && kind === "ult" && p && /^vesper/.test(p.w || ""))
      log.push({ w: p.w, t: m.t - t0, n: p.n || 0, load: p.load || 0 });
    return orig(kind, p);
  };

  let step = 0;
  while (!m.over && step < 120 / DT){
    const p0 = me.ultBeam ? me.ultBeam.phase : null;
    m.step(DT); step++;
    const B = me.ultBeam, p = B ? B.phase : null;
    if (p === "beam" && p0 === "wind"){
      windows++;
      if (windows === want){ rec = true; t0 = m.t; }
    }
    if (rec && p !== "beam"){ break; }
  }
  S.play = orig;
  const passes = log.filter(x => x.w === "vesper-pass").length;
  const tips = log.filter(x => x.w === "vesper-tip").length;
  const hums = log.filter(x => x.w === "vesper-hum");
  const lit = hums.filter(x => x.load > 0.03).length;
  return { log, dur: log.length ? log[log.length - 1].t : 0,
           passes, tips, hums: hums.length, lit };
}"""

# RENDER the recorded call list through `buildChain`, which is the path that
# ships. Every voice is the SHIPPED one, reached through `SFX.play` itself --
# so this file cannot drift from the build the way a hand-copied recipe would.
RENDER_JS = r"""async ([log, secs, lead]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  /* SCHEDULED AT AN ABSOLUTE TIME. `SFX.play` reads `this.ctx.currentTime`,
     so the proxy is what puts each event where the fight put it -- and an
     AudioParam whose first event is at t > 0 behaves differently from one
     anchored at 0, which is why nothing here starts at zero. */
  let now = lead;
  const proxy = new Proxy(oc, { get(o, k){
    if (k === 'currentTime') return now;
    const v = Reflect.get(o, k);
    return typeof v === 'function' ? v.bind(o) : v; } });
  S.ctx = proxy;
  /* the release, first, so the window is heard arriving */
  S.play("ult", { w: "vesper-open" });
  for (const e of log){ now = lead + e.t; S.play("ult", e); }
  const buf = await oc.startRendering();
  S.on=sv.on; S.ok=sv.ok; S.ctx=sv.ctx; S.bus=sv.bus; S.noise=sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  let peak = 0;
  for (let i = 0; i < d.length; i++){ out[i] = d[i];
    const v = Math.abs(d[i]); if (v > peak) peak = v; }
  return { pcm: out, sr, peak: +peak.toFixed(3) };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-vesper.html")
    ap.add_argument("--a", default="vesper")
    ap.add_argument("--b", default="emberedge")
    ap.add_argument("--seed", type=int, default=683570)
    ap.add_argument("--window", type=int, default=1, help="which cast to record")
    ap.add_argument("--lead", type=float, default=0.7)
    ap.add_argument("--out",
                    default="../05-reference/v48-sentinel/hum-load.wav")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with game(game_path=gp) as (page, errors):
        r = page.evaluate(RUN_JS, [a.a, a.b, a.seed, a.window])
        assert not errors, errors[:3]
        if not r["log"]:
            raise SystemExit(f"no window {a.window} in {a.a} vs {a.b} "
                             f"seed {a.seed}")
        secs = a.lead + r["dur"] + 2.0
        g = page.evaluate(RENDER_JS, [r["log"], secs, a.lead])
        assert not errors, errors[:3]

    import numpy as np
    d = np.asarray(g["pcm"], dtype=np.float32)
    pcm = np.clip(d * 0.92 / max(1e-9, np.abs(d).max()), -1, 1)
    w = wave.open(str(out), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(g["sr"])
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()

    print(f"\n  ONE REAL WINDOW — {a.a} vs {a.b}, seed {a.seed}, "
          f"cast {a.window}   ({r['dur']:.2f}s)")
    print(f"    hum strikes        {r['hums']}")
    print(f"    of them, LOADED    {r['lit']}   "
          f"({100 * r['lit'] / max(1, r['hums']):.0f}% of the window has the "
          f"dynamo in it)")
    print(f"    passes / tips      {r['passes']} / {r['tips']}")
    print(f"\n  the load, strike by strike (. idle, : spinning, # on the ball):")
    line = "".join("#" if e["load"] > 0.55 else (":" if e["load"] > 0.03 else ".")
                   for e in r["log"] if e["w"] == "vesper-hum")
    print(f"    {line}")
    hits = "".join("T" if e["w"] == "vesper-tip" else "p"
                   for e in r["log"] if e["w"] in ("vesper-pass", "vesper-tip"))
    print(f"    and it paid: {hits}")
    print(f"\n  wrote {out}   (raw peak {g['peak']})")


if __name__ == "__main__":
    main()
