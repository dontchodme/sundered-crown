#!/usr/bin/env python3
"""THE SPIKE STORM, PHOTOGRAPHED. Wind-up and spray, on one seed.

    python3 flail_strip.py --game ../02-chain/sc-redflail.html

A STEPPED filmstrip: the match is advanced to a real cast and frames are drawn
at chosen offsets from THE RELEASE, not from the cast. The release is emergent
-- the head fires when it actually reaches the ceiling -- so an offset measured
from `fireUlt` would land in a different place every seed and the strip would
be photographing the variance instead of the effect.

Frames are cropped around the caster because the head is 52px in a 520x800
hall and a full-hall frame at strip scale shows a red dot.

Writes PNGs into 05-reference/v38. Touches no build.
"""
from __future__ import annotations

import argparse, base64, io, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v38"
RID = "redflail"

# Offsets from the RELEASE frame. Negative is wind-up.
OFFSETS = [-0.70, -0.35, -0.06, 0.10, 0.35, 0.90, 1.80, 3.20]

RUN_JS = """([id, foe, seed, offsets, force]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;

  /* Wind forward to a cast. `force` sets the bar rather than waiting, because
     a natural cast can be 20 seconds in and the strip is about the ultimate,
     not about how long the bar takes. The WIND-UP and everything after it are
     entirely natural either way -- forcing sets `charge`, nothing else. */
  let guard = 0;
  if (force){ for (let i = 0; i < Math.round(4.0 / DT); i++) m.step(DT);
              me.charge = me.w.ult.charge; }
  while (!me.ultSpin && guard++ < 120 / DT && !m.over) m.step(DT);
  if (!me.ultSpin) return { ok: false, why: "no cast" };

  /* Roll to the RELEASE, buffering nothing: we cannot rewind, so the wind-up
     frames are captured on the way past. */
  const shots = {};
  const want = offsets.slice().sort((a,b)=>a-b);
  const preT = -want[0];
  const buf = [];
  let t = 0;
  while (me.ultSpin && me.ultSpin.phase === "wind" && !m.over){
    buf.push(t); m.step(DT); t += DT;
    if (t > 5) break;
  }
  const release = t;
  return { ok: true, release, windLen: release, msg: "release at " + release.toFixed(2) };
}"""

# Two passes: the first finds the release time, the second replays the same
# seed and captures at release+offset. Replay is exact -- the seed IS the fight.
CAP_JS = """([id, foe, seed, at, force, cx, cy]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  if (force){ for (let i = 0; i < Math.round(4.0 / DT); i++) m.step(DT);
              me.charge = me.w.ult.charge; }
  let guard = 0;
  while (!me.ultSpin && guard++ < 120 / DT && !m.over) m.step(DT);
  const t0 = m.t;
  for (let i = 0; i < Math.round(at / DT) && !m.over; i++) m.step(DT);
  AC.__draw(m);
  return { png: document.getElementById('cv').toDataURL('image/png'),
           x: me.x, y: me.y, phase: me.ultSpin ? me.ultSpin.phase : "-",
           shots: m.shots.length, hp: Math.round(me.hp) };
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-redflail.html")
    ap.add_argument("--foe", default="emberedge")
    ap.add_argument("--seed", type=int, default=177319)
    ap.add_argument("--crop", type=int, default=560)
    A = ap.parse_args()
    g = (HERE / A.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)

    with game(game_path=g) as (page, errors):
        r = page.evaluate(RUN_JS, [RID, A.foe, A.seed, OFFSETS, True])
        if not r.get("ok"):
            sys.exit(f"no cast: {r}")
        rel = r["release"]
        print(f"\n  wind-up took {rel:.2f}s on seed {A.seed} vs {A.foe}")

        frames, labels = [], []
        for off in OFFSETS:
            at = max(0.0, rel + off)
            c = page.evaluate(CAP_JS, [RID, A.foe, A.seed, at, True, 0, 0])
            im = png(c["png"])
            # the hall is drawn into a 1080x1920 canvas; crop on the caster
            sx = im.width / 520.0
            cx, cy = int(c["x"] * sx), int(c["y"] * sx)
            h = A.crop
            box = (max(0, cx - h), max(0, cy - h),
                   min(im.width, cx + h), min(im.height, cy + h))
            frames.append(im.crop(box))
            tag = "WIND" if off < 0 else "STORM"
            labels.append(f"{off:+.2f}s  {tag}  {c['shots']} spikes")
            print(f"    {off:+.2f}s  phase {c['phase']:6} shots {c['shots']:3} hp {c['hp']}")
        if errors:
            print("  PAGE ERRORS:", errors[:3])

    try:
        F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        FB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except OSError:
        F = FB = ImageFont.load_default()

    per, cols = 300, 4
    rows = (len(frames) + cols - 1) // cols
    PAD, LBL = 12, 26
    W = PAD + cols * (per + PAD)
    H = 34 + rows * (per + PAD + LBL)
    sh = Image.new("RGB", (W, H), (11, 9, 18))
    d = ImageDraw.Draw(sh)
    d.text((PAD, 8), f"THE SPIKE STORM — offsets from RELEASE, seed {A.seed} vs {A.foe}"
                     f"  (wind-up {rel:.2f}s)", font=FB, fill=(224, 58, 78))
    for i, (im, lab) in enumerate(zip(frames, labels)):
        x = PAD + (i % cols) * (per + PAD)
        y = 34 + (i // cols) * (per + PAD + LBL)
        sh.paste(im.resize((per, per), Image.LANCZOS), (x, y))
        d.text((x + 2, y + per + 4), lab, font=F, fill=(214, 200, 170))
    out = OUT / "spike-storm-strip.png"
    sh.save(out)
    print(f"\n  {out.name}  ({sh.width}x{sh.height})\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
