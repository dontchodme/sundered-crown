#!/usr/bin/env python3
"""THE STASIS FIELD, PHOTOGRAPHED — the ring at four moments of its own cycle.

    python3 paradox_field.py --game ../02-chain/sc-paradox.html

The hexagon is 400 units across in a hall 520 wide, so unlike a bolt or an eye
it does not need cropping in on -- it needs the WHOLE hall, because most of
what has to be judged is how much of the room it takes and whether the beams
read against the walls.

Four moments, and they are the four the mechanic actually has:

    the field up, charge cold      the quarry is out, the beams are quiet
    the charge nearly full         the quarry is in, and the beams say so --
                                   this is the entire legibility argument, and
                                   if it does not read here it does not exist
    the frame the hold lands
    inside the hold                the hexagon closed on the quarry, tightening

The frames are SOLVED FOR rather than guessed at: the run steps until the
charge is inside the band the pane asks for, so a pane is never "whatever the
clock happened to be on".

Writes one PNG into 05-reference/v43. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v43"

CAP_JS = r"""([id, foe, seed, warm, want, hold, maxSecs]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const u = me.w.ult;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = u.charge;
  /* STEP UNTIL THE PANE'S OWN CONDITION HOLDS. `want` is a band on the charge
     as a fraction of `need`; `hold` asks for the quarry to be held instead.
     A pane that is "whatever the clock happened to be on" cannot be compared
     with the pane beside it. */
  let n = 0, ok = false;
  const cap = Math.round(maxSecs / DT);
  while (n < cap && !m.over){
    m.step(DT); n++;
    const F = me.ultField;
    if (!F) continue;
    if (hold){ if (th.pin > 0 && th.pin < u.pin * (want[1])) { ok = true; break; } }
    else {
      if (th.pin > 0) continue;
      /* NOT THE FIRST FRAME OF THE WINDOW. The field fades in over 0.30s and
         the first cut of the cold pane caught it at F.t = 0.01, which
         photographed an empty hall and read as "the field is invisible when
         the charge is cold". It is not; it was not up yet. */
      if (F.t < 0.7) continue;
      const q = F.q / u.need;
      if (q >= want[0] && q <= want[1]){ ok = true; break; }
    }
  }
  m.shake = 0;
  AC.__draw(m);
  const F = me.ultField;
  return { png: document.getElementById('cv').toDataURL('image/png'),
           ok, t: +m.t.toFixed(2),
           q: F ? +(F.q / u.need).toFixed(2) : -1,
           inside: F ? !!F.in : false,
           pin: +th.pin.toFixed(2),
           left: F ? +(F.dur - F.t).toFixed(1) : 0,
           sep: Math.round(Math.hypot(th.x - me.x, th.y - me.y)),
           rad: u.rad };
}"""


def font(sz, bold=True):
    for p in (HERE / "fonts" / ("AtkinsonHyperlegibleNext-Bold.ttf" if bold
                                else "AtkinsonHyperlegibleNext-Regular.ttf"),
              pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if p.exists():
            try:
                return ImageFont.truetype(str(p), sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox.html")
    ap.add_argument("--id", default="paradox")
    ap.add_argument("--foe", default="heartwood")
    ap.add_argument("--seed", type=int, default=3307)
    ap.add_argument("--warm", type=float, default=7.0)
    ap.add_argument("--max", type=float, default=30.0)
    ap.add_argument("--scale", type=float, default=0.46)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    out_p = pathlib.Path(a.out) if a.out else OUT / "stasis-field.png"

    PANES = [("the field up, charge cold", (0.0, 0.12), False),
             ("charge half", (0.45, 0.60), False),
             ("charge nearly full", (0.80, 0.97), False),
             ("inside the hold", (0.0, 0.80), True)]

    tiles = []
    with game(game_path=gp) as (page, errors):
        for label, band, hold in PANES:
            r = page.evaluate(CAP_JS, [a.id, a.foe, a.seed, a.warm, band, hold,
                                       a.max])
            full = Image.open(io.BytesIO(base64.b64decode(
                r["png"].split(",", 1)[1]))).convert("RGB")
            im = full.resize((int(full.width * a.scale),
                              int(full.height * a.scale)), Image.LANCZOS)
            sub = (f"t {r['t']}s · charge {max(0, r['q']):.0%} · "
                   + ("HELD " + f"{r['pin']:.2f}s left" if r["pin"] > 0
                      else ("quarry inside" if r["inside"] else "quarry out"))
                   + f" · sep {r['sep']}")
            tiles.append((label, sub, im, r["ok"]))
            print(f"  {label:<28} {'ok' if r['ok'] else 'MISSED'}  {sub}")
        assert not errors, errors[:3]

    PAD, HEAD, GAP = 26, 108, 16
    W = PAD * 2 + sum(t[2].width for t in tiles) + GAP * (len(tiles) - 1)
    H = PAD * 2 + HEAD + max(t[2].height for t in tiles) + 30
    sheet = Image.new("RGB", (W, H), (11, 10, 13))
    d = ImageDraw.Draw(sheet)
    d.text((PAD, PAD - 4), "THE STASIS FIELD — the shipped renderer, the whole "
           "hall. The beams brighten, thicken and go jagged as the charge fills.",
           font=font(22), fill=(240, 232, 234))
    d.text((PAD, PAD + 26), "There is no bar and no number: the picture IS the "
           "charge, and it bleeds back off when the quarry gets clear.",
           font=font(18, False), fill=(176, 170, 178))
    x = PAD
    for label, sub, im, ok in tiles:
        d.text((x, PAD + HEAD - 40), label, font=font(19),
               fill=(238, 226, 228) if ok else (240, 120, 120))
        d.text((x, PAD + HEAD - 19), sub, font=font(15, False),
               fill=(150, 146, 154))
        sheet.paste(im, (x, PAD + HEAD))
        x += im.width + GAP
    sheet.save(out_p)
    print(f"  wrote {out_p}  ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
