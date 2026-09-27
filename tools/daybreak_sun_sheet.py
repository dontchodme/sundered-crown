#!/usr/bin/env python3
"""A CONCEPT SHEET for Daybreak's circle (v99) — four moments of design §4.1, painted with PIL so
Rick can judge the look before Code builds it. Not the engine's renderer: the palette, the alphas,
the radii and the marks are the design's numbers, drawn by hand on a hall of the game's colour.

    python daybreak_sun_sheet.py --out ../05-reference/v99/daybreak-sun-sheet.png
"""
import argparse, math, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 520, 800
HALL = (7, 5, 12)
CORE, GOLD, AMBER = (255, 246, 226), (255, 217, 138), (255, 179, 71)
R = 34


def over(base, layer):
    return Image.alpha_composite(base, layer)


def hall():
    im = Image.new("RGBA", (W, H), HALL + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(58, 46, 34, 255), width=3)
    return im


def ball(im, x, y, body, edge, glow=None):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    if glow:
        d.ellipse([x - R - 6, y - R - 6, x + R + 6, y + R + 6], fill=glow)
    d.ellipse([x - R, y - R, x + R, y + R], fill=body, outline=edge, width=3)
    return over(im, L)


def sword(im, x, y, ang, armed):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    ex, ey = x + math.cos(ang) * 116, y + math.sin(ang) * 116
    if armed:
        # the sun in the blade: a gold edge-light along the inset edge, and a warm smear behind the sweep
        for k in range(6):
            a = ang - 0.05 * (k + 1)
            sx, sy = x + math.cos(a) * 116, y + math.sin(a) * 116
            d.line([x, y, sx, sy], fill=GOLD + (int(60 * (1 - k / 6)),), width=10)
        d.line([x, y, ex, ey], fill=GOLD + (200,), width=9)
    d.line([x, y, ex, ey], fill=(232, 224, 210, 255), width=6)
    d.line([x, y, ex, ey], fill=(255, 255, 255, 255), width=2)
    return over(im, L)


def sun(im, cx, cy, r, t, alpha_mul=1.0, rays=True):
    """The wash (amber, 0.30 -> 0.20), the rays, the rim (gold, 3u + 10u halo), the core. World pass: under the balls."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    # the wash: a true radial gradient, gold 0.35 at the core -> amber 0.20 at the rim, nothing outside
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W]
    dist = np.hypot(xx - cx, yy - cy)
    k = np.clip(dist / max(r, 1), 0, 1)
    a = np.where(dist <= r, (0.35 - 0.15 * k) * alpha_mul, 0.0)
    a *= 0.97 + 0.03 * np.sin(0.8 * t * 2 * np.pi)          # breathing
    wash = np.zeros((H, W, 4), dtype=np.uint8)
    for ch in range(3):                                      # gold at the core -> amber at the rim
        wash[..., ch] = (GOLD[ch] * (1 - k) + AMBER[ch] * k).astype(np.uint8)
    wash[..., 3] = (a * 255).astype(np.uint8)
    L = over(L, Image.fromarray(wash, "RGBA"))
    d = ImageDraw.Draw(L)
    # rays
    if rays and r > 30:
        RL = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(RL)
        for i in range(10):
            a = i / 10 * 2 * math.pi + 0.15 * t
            ln = min(r * 0.85, 110 + 60 * (0.5 + 0.5 * math.sin(0.6 * t * 2 * math.pi + i)))
            wdt = 14
            p = [(cx + math.cos(a + 0.5 * math.pi) * 4, cy + math.sin(a + 0.5 * math.pi) * 4),
                 (cx - math.cos(a + 0.5 * math.pi) * 4, cy - math.sin(a + 0.5 * math.pi) * 4),
                 (cx + math.cos(a) * ln - math.cos(a + 0.5 * math.pi) * wdt * 0.15,
                  cy + math.sin(a) * ln - math.sin(a + 0.5 * math.pi) * wdt * 0.15),
                 (cx + math.cos(a) * ln + math.cos(a + 0.5 * math.pi) * wdt * 0.15,
                  cy + math.sin(a) * ln + math.sin(a + 0.5 * math.pi) * wdt * 0.15)]
            rd.polygon(p, fill=AMBER + (int(255 * 0.22 * alpha_mul),))
        RL = RL.filter(ImageFilter.GaussianBlur(2))
        L = over(L, RL)
        d = ImageDraw.Draw(L)
    # rim halo (10u outward) then the 3u ring
    for k in range(10, 0, -1):
        d.ellipse([cx - r - k, cy - r - k, cx + r + k, cy + r + k], outline=GOLD + (int(255 * 0.35 * alpha_mul * (1 - k / 10)),), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD + (int(255 * 0.8 * alpha_mul),), width=3)
    # embers
    import random
    rnd = random.Random(9101)
    for i in range(24):
        ang = rnd.random() * 2 * math.pi
        rr = math.sqrt(rnd.random()) * r * 0.95
        ex, ey = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr - rnd.random() * 30
        d.ellipse([ex - 1.5, ey - 1.5, ex + 1.5, ey + 1.5], fill=AMBER + (int(255 * 0.5 * alpha_mul),))
    # the core: a small sun, core white
    if r > 14:
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=CORE + (int(255 * 0.9 * alpha_mul),))
    return over(im, L)


def flash(im, cx, cy, r):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    for k in range(6, 0, -1):
        rr = r * k / 6
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=CORE + (int(255 * 0.18),))
    L = L.filter(ImageFilter.GaussianBlur(6))
    return over(im, L)


def burn(im, x, y, font, number="2"):
    """The foe inside: the number, the shell flash, the embers, the smite bolts."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    d.ellipse([x - R - 4, y - R - 4, x + R + 4, y + R + 4], outline=GOLD + (200,), width=2)
    d.text((x - 7, y - 78), number, font=font, fill=GOLD + (255,))
    import random
    rnd = random.Random(9107)
    for i in range(12):
        ang = -math.pi / 2 + (rnd.random() - 0.5) * 2.4
        r0 = R * (0.5 + 0.45 * rnd.random())
        ph = rnd.random()
        mx, my = x + math.cos(ang) * r0, y + math.sin(ang) * r0 - ph * 44
        d.ellipse([mx - 1.6, my - 1.6, mx + 1.6, my + 1.6], fill=GOLD + (int(255 * 0.7 * math.sin(ph * math.pi)),))
    for i in range(6):  # the smite bolts the status already draws, falling in
        a = (rnd.random() - 0.5) * 1.8 - math.pi / 2
        fall = rnd.random() * R * 3
        d.line([x + math.cos(a) * (R * 0.86 + fall), y + math.sin(a) * (R * 0.86 + fall),
                x + math.cos(a) * (R * 0.86 + fall * 0.42), y + math.sin(a) * (R * 0.86 + fall * 0.42)],
               fill=(255, 231, 168, 140), width=2)
    return over(im, L)


def label(im, text, font):
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 46, W, H], fill=(0, 0, 0, 170))
    d.text((12, H - 38), text, font=font, fill=(235, 225, 205, 255))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../05-reference/v99/daybreak-sun-sheet.png")
    a = ap.parse_args()
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
        big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except Exception:
        font = big = ImageFont.load_default()
    ME_BODY, ME_EDGE = (238, 232, 218), (255, 255, 255)
    FOE_BODY, FOE_EDGE = (110, 30, 30), (200, 70, 60)
    panels = []
    # 1 ARMED: the sun in the blade, nothing on the floor
    im = hall(); im = ball(im, 180, 620, ME_BODY, ME_EDGE); im = sword(im, 180, 620, -0.6, True)
    im = ball(im, 360, 560, FOE_BODY, FOE_EDGE)
    panels.append(label(im, "1  ARMED - the sun is in the blade; the floor is dark", font))
    # 2 THE BREAK: the blow lands, the flash at the hit point, the rim leaving it (r ~ 50 at 0.5s)
    im = hall(); cx, cy = 318, 585
    im = sun(im, cx, cy, 50, 0.5, rays=False)
    im = flash(im, cx, cy, 60)
    im = ball(im, 230, 640, ME_BODY, ME_EDGE); im = sword(im, 230, 640, -0.55, False)
    im = ball(im, 350, 560, FOE_BODY, FOE_EDGE)
    panels.append(label(im, "2  THE BREAK - sun comes up where the sword hit", font))
    # 3 UP: r 200, the foe inside burning
    im = hall(); im = sun(im, cx, cy, 200, 4.0)
    im = ball(im, 200, 690, ME_BODY, ME_EDGE); im = sword(im, 200, 690, -1.1, False)
    im = ball(im, 420, 520, FOE_BODY, FOE_EDGE); im = burn(im, 420, 520, big)
    panels.append(label(im, "3  UP - the foe in the sunlight burns, 2 a tick", font))
    # 4 OUT: the foe has left the light; nothing happens to it
    im = hall(); im = sun(im, cx, cy, 200, 6.0)
    im = ball(im, 260, 640, ME_BODY, ME_EDGE); im = sword(im, 260, 640, 0.3, False)
    im = ball(im, 120, 300, FOE_BODY, FOE_EDGE)
    panels.append(label(im, "4  OUT - out of the light, it stops burning", font))
    # 5 SUNSET: the rim back to the core, the wash going
    im = hall(); im = sun(im, cx, cy, 70, 8.2, alpha_mul=0.5, rays=False)
    im = ball(im, 300, 660, ME_BODY, ME_EDGE); im = sword(im, 300, 660, -0.2, False)
    im = ball(im, 150, 480, FOE_BODY, FOE_EDGE)
    panels.append(label(im, "5  SUNSET - the rim falls to the core, goes out", font))

    sheet = Image.new("RGB", (W * len(panels) + 8 * (len(panels) - 1), H), (20, 16, 26))
    for i, p in enumerate(panels):
        sheet.paste(p.convert("RGB"), (i * (W + 8), 0))
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
