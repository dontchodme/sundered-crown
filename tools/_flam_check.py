"""THREE NOVAS ON ONE FRAME -- DOES THE FLAM CLIP?

A volley completes when its LAST arrow resolves, so all three novas fire on one
frame. `SFX.play` reads `currentTime`, so the only thing separating them is the
26 ms offset the voice applies from `p.k`. This renders exactly that -- three
calls at k = 0, 1, 2 -- through `buildChain`, the path that ships, and measures
what comes out against one nova alone and against three with the flam removed.

The no-flam row is the control and it is the point: if it comes back at nearly
three times the peak of one, the offset is doing the work it was added for.
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

JS = r"""async ([calls, secs]) => {
  const OC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
  if (!OC) return { skip: true };
  const S = AC.SFX, sr = 44100;
  const sv = { on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise };
  const off = new OC(1, Math.round(sr * secs), sr);
  S.ctx = off; S.ok = true; S.on = true;
  S.bus = S.constructor.buildChain(off, off.destination);
  S.noise = S._noiseBuffer();
  S.ctx = new Proxy(off, { get(o, k){
    if (k === 'currentTime') return 1.0;
    const v = Reflect.get(o, k);
    return typeof v === 'function' ? v.bind(o) : v; } });
  let threw = null;
  try { for (const c of calls) S.play(c[0], c[1] || {}); }
  catch (e) { threw = String(e); }
  const buf = await off.startRendering();
  S.on = sv.on; S.ok = sv.ok; S.ctx = sv.ctx; S.bus = sv.bus; S.noise = sv.noise;
  const d = buf.getChannelData(0);
  let peak = 0, clipped = 0, rms = 0;
  for (let i = 0; i < d.length; i++){
    const v = Math.abs(d[i]);
    if (v > peak) peak = v;
    if (v >= 0.999) clipped++;
    rms += d[i] * d[i];
  }
  return { threw, peak, clipped, rms: Math.sqrt(rms / d.length) };
}"""

CASES = {
    "one nova":               [["nova", {"k": 0}]],
    "a volley, 3 flammed":    [["nova", {"k": 0}], ["nova", {"k": 1}],
                               ["nova", {"k": 2}]],
    "3 with the flam REMOVED": [["nova", {"k": 0}], ["nova", {"k": 0}],
                                ["nova", {"k": 0}]],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
    a = ap.parse_args()
    with game(game_path=resolve_game(a.game)) as (page, errors):
        print(f"\n    {'case':<26}{'peak':>8}{'rms':>9}{'clipped':>9}")
        out = {}
        for name, calls in CASES.items():
            r = page.evaluate(JS, [calls, 2.6])
            assert not errors, errors[:4]
            if r.get("skip"):
                raise SystemExit("no OfflineAudioContext in this runtime")
            if r.get("threw"):
                print(f"    {name:<26}  THREW {r['threw']}")
                continue
            out[name] = r
            print(f"    {name:<26}{r['peak']:>8.3f}{r['rms']:>9.4f}"
                  f"{r['clipped']:>9}")
        one = out.get("one nova", {}).get("peak", 0)
        fl = out.get("a volley, 3 flammed", {}).get("peak", 0)
        no = out.get("3 with the flam REMOVED", {}).get("peak", 0)
        if one:
            print(f"\n    flammed is {fl/one:.2f}x one nova; "
                  f"unflammed is {no/one:.2f}x")
            print("    (unflammed near 3x is the three voices summing in phase,")
            print("     which is one louder pop rather than three pops)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
