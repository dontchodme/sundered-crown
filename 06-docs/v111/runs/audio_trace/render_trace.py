"""The clip's OWN audio render, without the frame capture: cinema_clip.py's harness (imported, not copied), the same
fight window, the same director-ON frame loop minus toDataURL, then __clip.renderAudio -- several times on ONE
recorded event list and curve, so the renders differ only in what renderAudio itself does.

    python render_trace.py <link.html> <tag> <outdir> [--a spellbreaker --b vesper --seed 111075 --at 77.98
                                                      --window 12.77 --fps 60 --w 540] [--seeds none,none,1,1]

--seeds: one render per entry. `none` = the page's own Math.random (what cinema_clip does); an integer = Math.random
replaced by mulberry32(seed) for the duration of that renderAudio call only (the frame loop is untouched);
`<seed>/drop=a+b` = that, with the ult voices a and b (SFX.play('ult', {w})) left out of the list for that render;
`<seed>/free=A-B` = seeded, except Math.random calls number A..B-1 inside the render, which get the page's own. Writes, in
<outdir>: <tag>_r<k>_<seed>.wav (16-bit stereo 48 kHz, renderAudio's own bytes), <tag>_events.json (every recorded
SFX.play: wall t, kind, opts), <tag>_curve.json (the director's send curve), <tag>_meta.json (frames, end state, the
Math.random call count inside each render, sha256 of each render's float32 buffers and of each wav).
"""
import argparse, base64, hashlib, json, pathlib, sys, time
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game, resolve_game          # noqa: E402
from cinema_clip import HARNESS                # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("link"); ap.add_argument("tag"); ap.add_argument("outdir")
ap.add_argument("--a", default="spellbreaker"); ap.add_argument("--b", default="vesper")
ap.add_argument("--seed", type=int, default=111075)
ap.add_argument("--at", type=float, default=77.98); ap.add_argument("--window", type=float, default=12.77)
ap.add_argument("--fps", type=int, default=60); ap.add_argument("--w", type=int, default=540)
ap.add_argument("--verdict-hold", type=float, default=2.4)
ap.add_argument("--seeds", default="none,none,1,1")
a = ap.parse_args()
out = pathlib.Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

LOOP = r"""([stopT, fps, chunk]) => {
  /* frame() with N = 1, minus the stakes hook (not installed) and minus toDataURL: _sub, wall, curve -- verbatim. */
  const C = window.__clip, CINE = window.CINE, raw = 1 / fps, m = C.m;
  let k = 0, done = false;
  while (k < chunk) {
    C._sub(raw);
    C.wall += raw;
    C.curve.push([ +C.wall.toFixed(4),
                   C.on ? +CINE.timeScale.toFixed(4) : 1,
                   C.on ? +CINE.send.wet.toFixed(3) : 0,
                   C.on ? Math.round(CINE.send.lp) : 20000,
                   C.on ? +CINE.send.dry.toFixed(3) : 1,
                   +m.t.toFixed(4) ]);
    k++;
    if (m.over || m.t >= stopT) { done = true; break; }
  }
  return { k, done, over: !!m.over, t: m.t };
}"""

SAFE = r"""() => {
  const seen = new WeakSet();
  const clean = (v, d) => {
    if (v === null || typeof v !== 'object') return (typeof v === 'number') ? +v.toFixed(6) : v;
    if (d > 3 || seen.has(v)) return '<obj>';
    seen.add(v);
    if (Array.isArray(v)) return v.map(x => clean(x, d + 1));
    const o = {}; for (const k of Object.keys(v).sort()) o[k] = clean(v[k], d + 1); return o;
  };
  return window.__clip.events.map(e => [+e.t.toFixed(6), e.kind, clean(e.p, 0)]);
}"""

RENDER = r"""async ([dur, hold, seed, free]) => {
  /* Math.random pinned (or not) for this render only; the float32 result of every OfflineAudioContext render
     inside it is hashed before renderAudio's 16-bit conversion. */
  const mul = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
                           t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const oR = Math.random, gen = seed === null ? oR : mul(seed);
  let calls = 0;
  /* free = [a, b): the calls with index a..b-1 get the page's own Math.random (the seeded stream is still advanced,
     so every other call gets the same number it gets in a fully seeded render). */
  Math.random = function () { const i = calls++; const v = gen();
                              return (free && i >= free[0] && i < free[1]) ? oR() : v; };
  const P = OfflineAudioContext.prototype, oS = P.startRendering, bufs = [];
  P.startRendering = function () { return oS.call(this).then(b => { bufs.push(b); return b; }); };
  let wav;
  try { wav = await window.__clip.renderAudio(dur, hold); }
  finally { Math.random = oR; P.startRendering = oS; }
  const hex = async a => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', a))).map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 16);
  const bh = [];
  for (const b of bufs) { const ch = []; for (let c = 0; c < b.numberOfChannels; c++) ch.push(await hex(b.getChannelData(c).buffer.slice(0)));
                          bh.push({ sr: b.sampleRate, len: b.length, ch }); }
  return { wav, calls, bufs: bh };
}"""

t0 = time.time()
meta = {"link": str(a.link), "args": vars(a)}
with game(game_path=resolve_game(a.link)) as (page, errors):
    page.evaluate(f"AC.setResolution({a.w}, {round(a.w * 16 / 9)})")
    page.evaluate(HARNESS)
    info = page.evaluate("([x,y,s,o,t]) => window.__clip.init(x,y,s,o,t)", [a.a, a.b, a.seed, True, a.at])
    meta["init"] = info
    stop_t = a.at + a.window
    frames = 0
    while True:
        r = page.evaluate(LOOP, [stop_t, a.fps, 60])
        frames += r["k"]
        if r["done"] or frames > a.window * 2.6 * a.fps + 6 * a.fps:
            break
    dur = frames / a.fps
    fight = page.evaluate("() => { const m = window.__clip.m; return { over: m.over || null, t: +m.t.toFixed(4),"
                          " clanks: m.clankCount, hp: [Math.round(m.a.hp*1000)/1000, Math.round(m.b.hp*1000)/1000] }; }")
    meta.update(frames=frames, dur=dur, fight=fight)
    print(f"{a.tag}: {frames} frames ({dur:.3f} s video), fight {fight}, {time.time() - t0:.0f}s", flush=True)
    ev = page.evaluate(SAFE)
    curve = page.evaluate("() => window.__clip.curve")
    (out / f"{a.tag}_events.json").write_text(json.dumps(ev, separators=(",", ":")), encoding="utf-8")
    (out / f"{a.tag}_curve.json").write_text(json.dumps(curve, separators=(",", ":")), encoding="utf-8")
    meta["n_events"] = len(ev)
    meta["renders"] = []
    page.evaluate("() => { window.__allEvents = window.__clip.events.slice(); }")
    for k, spec in enumerate(a.seeds.split(",")):
        # `seed` or `seed/drop=voiceA+voiceB`: the second form renders with those ult voices (SFX.play('ult',{w}))
        # taken out of the recorded list, for that render only -- the list is restored before the next.
        spec, _, fr = spec.partition("/free=")
        free = [int(v) for v in fr.split("-")] if fr else None
        s, _, drop = spec.partition("/drop=")
        sd = None if s == "none" else int(s)
        drops = [x for x in drop.split("+") if x]
        nkept = page.evaluate("(d) => { window.__clip.events = window.__allEvents.filter(e => !(e.kind === 'ult' && e.p"
                              " && d.includes(e.p.w))); return window.__clip.events.length; }", drops)
        R = page.evaluate(RENDER, [dur + 0.5, a.verdict_hold, sd, free])
        page.evaluate("() => { window.__clip.events = window.__allEvents.slice(); }")
        wb = base64.b64decode(R["wav"])
        s = s + ("_drop-" + "-".join(drops) if drops else "") + (f"_free-{free[0]}-{free[1]}" if free else "")
        p = out / f"{a.tag}_r{k}_{s}.wav"
        p.write_bytes(wb)
        rec = {"k": k, "seed": s, "dropped": drops, "events_rendered": nkept, "wav": p.name,
               "wav_sha16": hashlib.sha256(wb).hexdigest()[:16],
               "random_calls": R["calls"], "float_bufs": R["bufs"]}
        meta["renders"].append(rec)
        print(f"  render {k} seed={s} events={nkept}: wav {rec['wav_sha16']}  Math.random calls {R['calls']}  "
              f"float32 " + " | ".join(f"{b['sr']}Hz x{b['len']} {','.join(b['ch'])}" for b in R["bufs"]), flush=True)
    meta["errors"] = errors[:10]
(out / f"{a.tag}_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
print(f"{a.tag}: done in {time.time() - t0:.0f}s; page errors {len(meta['errors'])}")
