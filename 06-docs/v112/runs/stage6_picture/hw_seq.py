"""Sequences off one real Heartwood fight for the sheet: THE CAST (the first window's greening, caster crops at
groveAge thresholds, half-seconds, from the cast frame), THE ROOT (the first new hold on a live foe: +3 steps, then
by the held ball's own clock, to the pin's last 0.15s and 0.1s after it lets go; then the first re-root +3), THE
CLOSE (the first clock close: groveOut thresholds). Optional `nobanner`: drawUltName shadowed (to see the blade
under the cast's banner). usage: hw_seq.py page foe seed side [nobanner]. Writes snaps/seq_<tag>_*.png + json."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
JS = r"""([foe, seed, side, nob]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(1080, 1920); AC.SFX.play = function(){}; AC.SFX.resume = function(){}; AC.CINE.on = false;
  const r = AC.renderer; if (nob) r.drawUltName = function(){};
  const DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const m = side === "a" ? new AC.Match("heartwood", foe, seed) : new AC.Match(foe, "heartwood", seed);
  const me = m.a.w.id === "heartwood" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const out = {};
  const snap = (k, who) => { const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D); AC.__draw(m);
    Math.random = realRandom; m.shake = ks;
    out[k] = { png: cv.toDataURL("image/png"), who, c: who === "me" ? toDev(me.x, me.y) : toDev(th.x, th.y),
               t: +m.t.toFixed(3), age: +me.groveAge.toFixed(3), out: +me.groveOut.toFixed(3), fade: +me.groveFade.toFixed(3),
               stop: m.hitStop > 0, pin: +(th.pin || 0).toFixed(3), heldAge: +(th.twineHeldAge || 0).toFixed(3),
               rootFade: +(th.twineRootFade || 0).toFixed(3), ent: th.stacks("entangle"),
               tag: (m.tags.filter(g => g.key === "entangle").slice(-1)[0] || {}).val }; };
  const G = [0.017, 0.08, 0.2, 0.3, 0.42, 0.56, 0.7, 1.0], O = [0.05, 0.2, 0.35, 0.5, 0.65, 0.8];
  let step = 0, prev = null, gi = 0, oi = 0, closing = false, seenR = 0, seenN = 0, hold = null, holdN = 0, rer = null;
  while (step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultRoot, T = me.rootTally;
    if (Z && !prev && gi === 0 && me.groveAge <= 0.02){ snap("g0", "me"); gi = 1; }
    else if (Z && gi > 0 && gi < G.length && me.groveAge >= G[gi]){ snap("g" + gi, "me"); gi++; }
    if (!Z && prev && me.alive && th.alive && oi === 0) closing = true;
    prev = Z;
    if (closing && oi < O.length && me.groveOut >= O[oi]){ snap("o" + oi, "me"); oi++; }
    const nr = T ? T.roots - seenR : 0, nn = T ? T.rooted - seenN : 0;
    if (T){ seenR = T.roots; seenN = T.rooted; }
    if (hold === null && nr > 0 && th.alive && th.pin > 0 && Z && Z.t > 0.5){ hold = step; holdN = 0; }
    if (hold !== null && holdN < 7){
      const ha = th.twineHeldAge || 0;
      if (holdN === 0 && step - hold === 3){ snap("r0", "foe"); holdN = 1; }
      else if (holdN === 1 && ha >= 0.12){ snap("r1", "foe"); holdN = 2; }
      else if (holdN === 2 && ha >= 0.24){ snap("r2", "foe"); holdN = 3; }
      else if (holdN === 3 && ha >= 0.6){ snap("r3", "foe"); holdN = 4; }
      else if (holdN === 4 && th.pin > 0 && th.pin <= 0.15){ snap("r4", "foe"); holdN = 5; }
      else if (holdN === 5 && !(th.pin > 0) && th.twineRootFade < 0.8){ snap("r5", "foe"); holdN = 6; }
      else if (holdN >= 1 && holdN < 6 && nn > 0 && nr === 0) { holdN = 7; }       // a re-root cut it short
    }
    if (rer === null && nr === 0 && nn > 0 && th.alive) rer = step;
    if (rer !== null && step - rer === 3 && !out.rr) snap("rr", "foe");
    if (gi >= G.length && oi >= O.length && holdN >= 6 && out.rr) break;
  }
  return out;
}"""
if __name__ == "__main__":
    PAGE = pathlib.Path(sys.argv[1]); PAGE = PAGE if PAGE.is_absolute() else HERE / PAGE
    FOE, SEED, SIDE = sys.argv[2], int(sys.argv[3]), sys.argv[4]
    NOB = len(sys.argv) > 5 and sys.argv[5] == "nobanner"
    TAG = f"{FOE}_{SEED}{SIDE}" + ("_nob" if NOB else "")
    OUTD = HERE / "snaps"; OUTD.mkdir(exist_ok=True)
    with game(game_path=PAGE) as (page, errors):
        r = page.evaluate(JS, [FOE, SEED, SIDE, NOB])
        assert not errors, errors[:5]
    meta = {}
    for k, v in r.items():
        im = Image.open(io.BytesIO(base64.b64decode(v.pop("png").split(",", 1)[1]))).convert("RGB")
        cx, cy = v["c"]; W = 520 if v["who"] == "me" else 560
        x0 = int(max(0, min(im.width - W, cx - W / 2))); y0 = int(max(0, min(im.height - W, cy - W / 2)))
        if k.startswith("r") and v["who"] == "foe":
            y0 = int(max(0, min(im.height - W, cy - W * 0.35)))       # the stalks run down to the floor
        im.crop((x0, y0, x0 + W, y0 + W)).save(OUTD / f"seq_{TAG}_{k}.png")
        meta[k] = v
    (OUTD / f"seq_{TAG}.json").write_text(json.dumps(meta, indent=1))
    print(TAG, sorted(meta))
