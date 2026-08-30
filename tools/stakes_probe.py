#!/usr/bin/env python3
"""THE STAKES BAND, MEASURED — is it there, is it timed, and what does it hide?

    python stakes_probe.py
    python stakes_probe.py --stakes "TWO ENTER. ONE FALLS." --stakes-sub "..."

Hook brief §5a. The band is a caption over the opening, and a caption has
exactly three ways to be wrong that no number in this repo would otherwise
catch:

    1  it is not drawn at all                       <- the v42 fault, again
    2  it is drawn on the wrong clock -- late in, or still up when the
       scrunch legend arrives, so two things introduce the fight at once
    3  it covers something. The brief placed it at y=14.5% BY EYE, against
       both opening camera shots, because "a low band crowds the fighter name
       in shot B". This turns that eye into a number: how much lit picture is
       underneath the band while it is up.

And a fourth, which is the one a flag has to earn: with `--stakes` absent the
capture must be **bit-identical** to a capture from before the hook existed.

The band is drawn inside `cinema_clip`'s own capture harness, not in the
renderer, so this probe drives that harness rather than `AC.__draw` -- and it
imports `HARNESS` and `STAKES_JS` from `cinema_clip` so it cannot measure a
copy of them that has drifted.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import pathlib
import sys

import numpy as np
from PIL import Image

import cinema_clip
from scpage import game

HERE = pathlib.Path(__file__).parent
W, H = 540, 960


# TWO THINGS MAKE A CAPTURE DIFFER FROM ITSELF, AND BOTH ARE ALREADY KNOWN.
# render_ab.py pins them for exactly this reason and this probe's check 4 --
# "the hook is a no-op" -- failed on both before it pinned them too:
#   * m.shake draws from Math.random every frame it is non-zero
#   * the post chain's grain is keyed to POSTFX's frame COUNTER, which keeps
#     climbing across passes, so a second pass is a different picture even
#     from an identical sim
FRAME_JS = r"""([raw, q, pin]) => {
  if (pin) window.__clip.m.shake = 0;
  const r = window.__clip.frame(raw, q, 1, 1.0);
  const rd = AC.renderer, m = window.__clip.m;
  const cam = rd._cineCam;
  const proj = (sx, sy) => {
    let lx = sx * rd.scale, ly = sy * rd.scale;
    if (cam){ lx = cam[0] + (lx - cam[0]) * cam[2];
              ly = cam[1] + (ly - cam[1]) * cam[2]; }
    return [(rd.pad + lx) * rd.k, (rd.arenaTop + ly) * rd.k];
  };
  const z = cam ? cam[2] : 1;
  r.discs = [proj(m.a.x, m.a.y), proj(m.b.x, m.b.y)];
  r.rpx = 34 * rd.scale * z * rd.k;
  /* WHICH RELIC THE SHOT IS ON. The caption must not crowd the relic being
     FILMED -- the brief's own words, "a low band crowds the fighter name in
     shot B". The other one drifting behind a caption it is not the subject of
     is not a fault, and testing both made this fail on relic B falling through
     the top of the frame during relic A's shot. */
  r.subject = null;
  if (typeof SWBOpen !== 'undefined')
    for (const sh of SWBOpen.SHOTS)
      if (m.t >= sh.t0 && m.t < sh.t1) { r.subject = sh.at || null; break; }
  return r;
}"""


def frames(page, n, q=0.92, pin=True):
    """n consecutive captured frames, as numpy RGB, plus their state."""
    page.evaluate("() => { if (typeof POSTFX !== 'undefined') POSTFX.reset(); }")
    out = []
    for i in range(n):
        r = page.evaluate(FRAME_JS, [1.0 / 60, q, pin])
        im = np.asarray(Image.open(io.BytesIO(base64.b64decode(r["i"])))
                        .convert("RGB"), dtype=np.float32)
        out.append((i / 60.0, im, r["c"], r["t"], r["discs"], r["rpx"],
                    r["subject"]))
    return out


def luma(a):
    return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1]
                  + 0.0722 * a[..., 2]).mean() / 255.0)


def band_rows(y0f):
    k = W / 1080.0
    top = int(round(H * y0f))
    return top, top + int(round(150 * k))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--a", default="ironhail")
    ap.add_argument("--b", default="oathwound")
    ap.add_argument("--seed", type=int, default=55196)
    ap.add_argument("--stakes", default="TWO WEAPONS. ONE SURVIVES.")
    ap.add_argument("--stakes-sub", default="ONLY ONE KEEPS THE CROWN")
    ap.add_argument("--stakes-in", type=float, default=0.25)
    ap.add_argument("--stakes-out", type=float, default=0.35)
    ap.add_argument("--stakes-y", type=float, default=0.145)
    ap.add_argument("--secs", type=float, default=3.6)
    A = ap.parse_args()

    rows = []
    def check(ok, label, detail=""):
        rows.append((bool(ok), label, detail))
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}"
              + (f"\n          {detail}" if detail else ""))

    n = int(A.secs * 60)
    top, bot = band_rows(A.stakes_y)
    gpath = (HERE / A.game).resolve()

    with game(game_path=gpath) as (page, errors):
        page.evaluate(f"AC.setResolution({W}, {H})")
        # THE ONE SOURCE OF NONDETERMINISM IN A CAPTURE, PINNED. The sim runs on
        # mulberry32 off its own seed (CLAUDE.md §1) and never touches
        # Math.random; the camera shake and one ult branch do, inside the
        # harness's own draw where no caller can reach them. render_ab.py pins
        # `m.shake` for the same reason -- this probe pins the source instead,
        # because one frame before the first clank still differed without it.
        page.evaluate("() => { Math.random = () => 0.5; }")
        page.evaluate(cinema_clip.HARNESS)

        # ---- pass 1: no band. This is also the control for check 4.
        page.evaluate("([a,b,s]) => window.__clip.init(a,b,s,true,0,false)",
                      [A.a, A.b, A.seed])
        bare = frames(page, n)

        # ---- pass 2: the band, same seed, same everything
        r = page.evaluate(cinema_clip.STAKES_JS,
                          [A.stakes, A.stakes_sub or None, A.stakes_in,
                           A.stakes_out, A.stakes_y])
        check(r == "ok", "0  the band installs", f"STAKES_JS -> {r}")
        page.evaluate("([a,b,s]) => window.__clip.init(a,b,s,true,0,false)",
                      [A.a, A.b, A.seed])
        band = frames(page, n)

        # ---- pass 3: uninstalled again, for the no-op check
        # AND THE INSET GOES WITH IT. --stakes publishes the band's bottom
        # edge to SWBOpen.topInset, which MOVES THE CAMERA; leaving it set
        # while pretending the flag is absent made this control a different
        # shot, and check 4 read 105/133 for a reason that was the probe's.
        page.evaluate("() => { delete window.__stakes;"
                      " if (typeof SWBOpen !== 'undefined') SWBOpen.topInset = 0; }")
        page.evaluate("([a,b,s]) => window.__clip.init(a,b,s,true,0,false)",
                      [A.a, A.b, A.seed])
        again = frames(page, n)

        if errors:
            print("\npage errors:", errors[:3], file=sys.stderr)

    clank = next((t for t, _im, c, *_ in band if c > 0), None)
    k = W / 1080.0
    hair = max(1, int(round(3 * k)))

    # 1. IS IT THERE? The band strip, with against without.
    d = [(t, luma(b[top:bot]) - luma(a[top:bot]))
         for (t, a, *_), (_t2, b, *_) in zip(bare, band)]
    peak = max(abs(x[1]) for x in d)
    check(peak > 0.02, "1  the band is actually drawn",
          f"peak {peak:.4f} luma change on the strip, against the same "
          f"frames without it")

    # 2. THE CLOCK, READ OFF THE HAIRLINE AND NOT OFF THE STRIP.
    #
    # The first version of this check measured the whole band strip's luma
    # against the same strip without it, and reported the band reaching full
    # at 0.93s when it was asked for 0.25s. It was not late: the band is DARK
    # and 78% opaque, so while relic A's corona is blazing underneath, drawing
    # the band makes the strip DARKER, and the difference does not peak until
    # the flare fades. The measurement was reading the ignition, not the band.
    #
    # The gold hairline is the honest instrument: 3px of one constant colour
    # composited at the band's own alpha over dark hall.
    G = np.array([0xC9, 0xA2, 0x27], dtype=np.float32)
    def alpha(a_im, b_im):
        u = a_im[top:top + hair].reshape(-1, 3).mean(axis=0)
        o = b_im[top:top + hair].reshape(-1, 3).mean(axis=0)
        den = G - u
        m = np.abs(den) > 12
        return float(np.clip(((o - u)[m] / den[m]).mean(), 0, 1)) if m.any() else 0.0
    al = [(t, alpha(a_im, b_im))
          for (t, a_im, *_), (_t2, b_im, *_) in zip(bare, band)]
    full = max(v for _t, v in al)
    in_by = next((t for t, v in al if v >= 0.95 * full), None)
    gone = next((t for t, v in al if t > (clank or 0) and v <= 0.05 * full), None)
    ok_in = in_by is not None and in_by <= A.stakes_in + 2 / 60
    ok_out = (clank is not None and gone is not None
              and gone <= clank + A.stakes_out + 3 / 60)
    check(ok_in and ok_out,
          "2  it is in on the clock and out on the CLANK",
          (f"alpha full by {in_by:.2f}s (asked {A.stakes_in}s), first clank "
           f"{clank:.2f}s, gone by {gone:.2f}s (asked "
           f"{clank + A.stakes_out:.2f}s)") if clank and gone else
          f"in_by={in_by} clank={clank} gone={gone}")

    # 3. WHAT DOES IT COVER? The brief placed the band at y=14.5% BY EYE
    #    against both camera shots, because "a low band crowds the fighter
    #    name in shot B". The falsifiable version of that eye is: while the
    #    band is up, neither relic's magnified disc may reach into its rows.
    upt = {t for t, v in al if v > 0.05 * full}
    clear, closest = [], None
    for t, a_im, _c, _st, discs, rpx, subj in band:
        if t not in upt or subj is None:
            continue
        for (dx, dy) in [discs[0] if subj == "a" else discs[1]]:
            # A RELIC THAT IS NOT IN THE FRAME CANNOT BE CROWDED BY A CAPTION.
            # The first version of this check measured the off-screen relic --
            # during shot A, relic B is hundreds of pixels above the viewport,
            # which read as "452px into the band" and failed.
            if dx + rpx < 0 or dx - rpx > W:
                continue
            if dy + rpx < 0 or dy - rpx > H:
                continue
            gap = max(top - (dy + rpx), (dy - rpx) - bot)
            if closest is None or gap < closest[0]:
                closest = (gap, t)
            if gap < 0:
                clear.append((t, round(gap, 1)))
    check(not clear, "3  and the relic being FILMED never reaches its rows",
          f"closest approach {closest[0]:.0f}px clear of the band at "
          f"{closest[1]:.2f}s, over the {len(upt)} frames it is up"
          if closest else "no samples")
    under = max(((luma(a_im[top:bot]), t) for t, a_im, *_ in bare if t in upt),
                default=(0, 0))
    print(f"  --    and what the band sits ON TOP of, for the record\n"
          f"          the picture under it peaks at {under[0]:.4f} mean luma "
          f"at {under[1]:.2f}s -- the ignition's own glow reaching the top of "
          f"the frame. The band is 78% opaque, so that light is dimmed, not "
          f"lost; it is the one place the band and the open overlap.")

    # 4. THE NO-OP. Uninstalled, the capture must be what it always was.
    # UP TO THE FIRST CLANK, WHICH IS EXACTLY AS LONG AS THE BAND LIVES.
    # After it, `m.shake` is non-zero and draws from Math.random inside the
    # harness's own draw -- render_ab.py pins it by hand for the same reason and
    # nothing outside frame() can reach it. Comparing those frames would be
    # measuring the shake, and 4 of 216 differed on exactly that.
    h = lambda ims: [hashlib.sha256(im.astype(np.uint8).tobytes()).hexdigest()[:12]
                     for _t, im, *_ in ims]
    stop = next((i for i, (_t, _im, c, *_) in enumerate(bare) if c > 0),
                len(bare))
    hb, ha = h(bare[:stop]), h(again[:stop])
    same = sum(1 for x, y in zip(hb, ha) if x == y)
    tail_b, tail_a = h(bare[stop:]), h(again[stop:])
    tail_same = sum(1 for x, y in zip(tail_b, tail_a) if x == y)
    check(same == len(hb),
          "4  with no --stakes the hook is a no-op, frame for frame",
          f"{same}/{len(hb)} identical over the whole life of the band "
          f"(to the first clank at {clank:.2f}s). After it "
          f"{tail_same}/{len(tail_b)} match, and the rest is the camera "
          f"shake's Math.random inside frame(), which no caller can pin")

    # 5. DOES THE LINE FIT? A caption that runs off both edges is invisible to
    #    every number in this repo and obvious in one glance -- CLAUDE.md §4.1's
    #    whole defect class. It got here honestly: the prototype's font string
    #    was built as `700 * 0 + '700 ' + ...`, which is the STRING "0700 32px
    #    ...", which is not a valid font, so the canvas silently kept whatever
    #    font it already had and drew the line smaller than asked. It fitted for
    #    the wrong reason. Transcribing that correctly made the text its real
    #    size and it ran off both edges.
    m = max(4, int(round(10 * k)))
    txt_top, txt_bot = top + 2 * hair, bot - 2 * hair
    bleed = []
    for t, b_im, *_ in band:
        if t not in upt:
            continue
        left = b_im[txt_top:txt_bot, :m]
        right = b_im[txt_top:txt_bot, W - m:]
        hot = max(float(left.max()), float(right.max())) / 255.0
        if hot > 0.55:
            bleed.append((round(t, 2), round(hot, 3)))
    check(not bleed, "5  and the line fits inside the frame",
          f"no bright pixel in the outer {m}px of the band on any of the "
          f"{len(upt)} frames it is up"
          if not bleed else
          f"the copy reaches the frame edge on {len(bleed)} frames, first at "
          f"{bleed[0][0]}s -- it is being CROPPED")

    good = sum(1 for ok, _, _ in rows if ok)
    print(f"\n{good}/{len(rows)} checks")
    return 0 if good == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
