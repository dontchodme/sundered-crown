#!/usr/bin/env python3
"""SLAGBURST, AS A FILMSTRIP — AND AT THE SIZE IT WILL ACTUALLY BE WATCHED.

    python3 ember_filmstrip.py --game ../02-chain/sc-ember.html \
                               --out ../05-reference/ember-filmstrip.png

`ult_filmstrip.py` stamps an `ultFx` block by hand and moves `u.t`. That cannot
sample this ultimate: Slagburst has PHASES and a stack count, and a hand-stamped
fx block has neither, so it would photograph a set-piece that never happens.
Every frame here comes from a real cast that really detonated.

TWO ROWS, AND THE COMPARISON BETWEEN THEM IS THE POINT. The top row is a
zero-bank cast (n=3, the floor the split guarantees); the bottom is a full-bank
cast (n=9). If the two rows look the same, the central design claim — that the
spectacle IS the mechanic, one shard per consumed stack — is false, and no
amount of passing asserts makes it true.

THE PHONE STRIP. Daybreak's sparks passed every automated check and Rick still
could not see them: "a pixel-diff check cannot see 'too small to notice'". So
the last row is the burst frame downscaled to a real phone width, which is the
only scale at which "can you see it" is a question worth asking.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

SHOT_JS = r"""
([bank, marks, foeId]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match("emberedge", foeId, 8813377);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  const A = AC.CONFIG.arena, dt = AC.CONFIG.physics.dt;
  /* Posed, not stepped-to. Close enough to be inside the 230 radius, far
     enough apart that the fuse ring around the FOE is not sitting on top of
     the wielder. Both held still so the only thing moving is the ultimate. */
  m.a.x = A.w * 0.34; m.a.y = A.h * 0.46;
  m.b.x = A.w * 0.66; m.b.y = A.h * 0.54;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.a.stun = 1e9; m.b.stun = 1e9;
  m.a.hitCd = []; m.b.hitCd = [];
  if (bank) m.b.apply("sunder", bank);
  const t0 = m.t;
  m.fireUlt(m.a, m.b);
  const shots = [];
  let i = 0;
  for (const mk of marks) {
    while (m.t - t0 < mk) { m.step(dt); i++; if (i > 100000) break; }
    AC.__draw(m);
    shots.push({ t: +(m.t - t0).toFixed(3),
                 phase: m.ultFx ? m.ultFx.phase : null,
                 n: m.ultFx ? m.ultFx.n : null,
                 png: document.getElementById('cv').toDataURL('image/png') });
  }
  return shots;
}
"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-ember.html")
    ap.add_argument("--out", default="../05-reference/ember-filmstrip.png")
    ap.add_argument("--foe", default="nightfell")
    ap.add_argument("--scale", type=float, default=0.20)
    ap.add_argument("--phone", type=int, default=390,
                    help="phone width for the read-at-size row")
    a = ap.parse_args()

    # cast · mid-fuse · the instant before · the blow · shards out · slag
    marks = [0.02, 0.32, 0.58, 0.68, 0.86, 1.20]

    with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
        rows = []
        for bank in (0, 6):
            rows.append((bank, page.evaluate(SHOT_JS, [bank, marks, a.foe])))
        if errors:
            raise SystemExit(f"page errors: {errors[:3]}")

    imgs = {b: [png(s["png"]) for s in shots] for b, shots in rows}
    meta = {b: shots for b, shots in rows}

    W, H = imgs[0][0].size
    tw, th = int(W * a.scale), int(H * a.scale)
    pad, label = 8, 26
    # the phone row: the burst frame at real phone width
    burst_idx = 4   # after the flash dies, when the shards are countable
    ph_w = a.phone
    ph_h = int(H * ph_w / W)

    cols = len(marks)
    sheet_w = pad + cols * (tw + pad)
    sheet_h = (label + pad + 2 * (th + label + pad)
               + label + ph_h + pad * 2)
    sheet = Image.new("RGB", (sheet_w, max(sheet_h, ph_h + 120)), (16, 14, 13))
    d = ImageDraw.Draw(sheet)

    y = pad
    d.text((pad, y), "SLAGBURST — every frame from a real cast that really "
                     "detonated", fill=(240, 220, 190))
    y += label

    for bank in (0, 6):
        n = meta[bank][burst_idx]["n"] or "?"
        d.text((pad, y), f"banked {bank}  ->  {n} stacks consumed, "
                         f"{n} shards", fill=(255, 184, 99))
        y += label
        for i, im in enumerate(imgs[bank]):
            x = pad + i * (tw + pad)
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
            s = meta[bank][i]
            d.text((x + 3, y + th - 14),
                   f"{s['t']:.2f}s {s['phase'] or '-'}", fill=(210, 190, 170))
        y += th + pad

    d.text((pad, y), f"THE BURST AT {ph_w}px — phone width. If the shards are "
                     f"not readable here they are not readable.",
           fill=(255, 246, 226))
    y += label
    sheet.paste(imgs[6][burst_idx].resize((ph_w, ph_h), Image.LANCZOS), (pad, y))
    # side by side with the 3-stack burst at the same size, for the contrast
    sheet.paste(imgs[0][burst_idx].resize((ph_w, ph_h), Image.LANCZOS),
                (pad * 2 + ph_w, y))
    d.text((pad, y - 2), "9 stacks", fill=(255, 184, 99))
    d.text((pad * 2 + ph_w, y - 2), "3 stacks", fill=(255, 184, 99))

    out = pathlib.Path(a.out)
    if not out.is_absolute():
        out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"{out}  {sheet.size[0]}x{sheet.size[1]}")
    for bank in (0, 6):
        print(f"  banked {bank}: "
              + "  ".join(f"{s['t']:.2f}s/{s['phase']}/n={s['n']}"
                          for s in meta[bank]))


if __name__ == "__main__":
    sys.exit(main())
