"""Motion-graphics primitives for the World Cup trailer. Pure PIL/numpy.

House style is the shorts' stakes band: a dark translucent band, gold rules, cream
serif caps (cinema_clip.py STAKES_JS: rgba(7,5,12,.78), #C9A227, #EDE3D0).
"""
from __future__ import annotations
import functools, json, math, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1080, 1920
HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parent / "07-shorts" / "worldcup-trailer"      # every render product lives here (mp4/wav gitignored)
FONTS = {'Cinzel': HERE / 'fonts' / 'cinzel-variable.ttf',          # OFL, tools/fonts/OFL-cinzel.txt
         'Atkinson': HERE / 'fonts' / 'atkinson-hyperlegible-next.woff2'}
GOLD = (201, 162, 39)
GOLD_HI = (255, 222, 130)
CREAM = (237, 227, 208)
INK = (7, 5, 12)
SCHOOL = {  # AC.AFFINITIES core colours, read off the build
    'sanctified': (255, 246, 226), 'bloodsworn': (224, 58, 78), 'dwarven': (232, 163, 78),
    'verdant': (79, 208, 107), 'umbral': (164, 92, 240), 'runic': (74, 158, 255), 'vigil': (240, 107, 184)}
SCHOOLS = ['sanctified', 'bloodsworn', 'dwarven', 'verdant', 'umbral', 'runic', 'vigil']
SHAPES = ['greatsword', 'twinblade', 'warhammer', 'scythe', 'flail', 'bow', 'staff']


def ease_out(u, p=3):
    u = min(max(u, 0.0), 1.0); return 1 - (1 - u) ** p


def ease_in(u, p=2):
    u = min(max(u, 0.0), 1.0); return u ** p


def back_out(u, s=1.9):
    u = min(max(u, 0.0), 1.0); u -= 1; return u * u * ((s + 1) * u + s) + 1


def clamp01(u):
    return min(max(u, 0.0), 1.0)


def window(t, t0, t1, fin=0.12, fout=0.12):
    """0..1 envelope: fade in over fin after t0, out over fout before t1."""
    if t < t0 or t > t1: return 0.0
    a = 1.0 if fin <= 0 else clamp01((t - t0) / fin)
    b = 1.0 if fout <= 0 else clamp01((t1 - t) / fout)
    return min(a, b)


@functools.lru_cache(maxsize=64)
def font(face: str, size: int, weight: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONTS[face]), size)
    f.set_variation_by_axes([weight])
    return f


@functools.lru_cache(maxsize=128)
def text_img(s: str, face: str, size: int, weight: int, color=CREAM, track=0.0,
             glow=0, glow_color=None, glow_alpha=0.7, stroke=0, stroke_color=INK,
             gradient=None) -> Image.Image:
    """RGBA image of a line of text with tracking, optional vertical gradient and glow."""
    f = font(face, size, weight)
    adv = [f.getlength(ch) for ch in s]
    total = sum(adv) + track * size * (len(s) - 1)
    asc, desc = f.getmetrics()
    pad = glow * 3 + stroke + 8
    w, h = int(math.ceil(total)) + 2 * pad, asc + desc + 2 * pad
    mask = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(mask)
    x = pad
    for ch, a in zip(s, adv):
        d.text((x, pad), ch, font=f, fill=255, stroke_width=0)
        x += a + track * size
    if gradient:
        top, bot = gradient
        g = np.linspace(0, 1, h)[:, None]
        arr = (np.array(top)[None, None, :] * (1 - g[..., None]) + np.array(bot)[None, None, :] * g[..., None])
        fill = Image.fromarray(np.broadcast_to(arr, (h, w, 3)).astype(np.uint8), 'RGB')
    else:
        fill = Image.new('RGB', (w, h), color)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if stroke:
        sm = mask.filter(ImageFilter.MaxFilter(stroke * 2 + 1))
        out = Image.composite(Image.new('RGBA', (w, h), stroke_color + (255,)), out, sm)
    if glow:
        gm = mask.filter(ImageFilter.GaussianBlur(glow))
        gm = gm.point(lambda v: int(v * glow_alpha))
        gl = Image.new('RGBA', (w, h), (glow_color or color) + (0,))
        gl.putalpha(gm)
        out = Image.alpha_composite(out, gl)
    txt = fill.convert('RGBA'); txt.putalpha(mask)
    out = Image.alpha_composite(out, txt)
    return out


def fit_text(s, face, size, weight, maxw, **kw):
    img = text_img(s, face, size, weight, **kw)
    while img.width - 2 * (kw.get('glow', 0) * 3 + kw.get('stroke', 0) + 8) > maxw and size > 10:
        size = int(size * 0.94)
        img = text_img(s, face, size, weight, **kw)
    return img


def paste_center(base: Image.Image, img: Image.Image, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.003 or scale <= 0.01: return
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BICUBIC)
    if rot:
        img = img.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = img.getchannel('A').point(lambda v: int(v * alpha))
        img = img.copy(); img.putalpha(a)
    x, y = int(round(cx - img.width / 2)), int(round(cy - img.height / 2))
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(img.width, base.width - x), min(img.height, base.height - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    base.alpha_composite(img, (max(0, x), max(0, y)), (sx0, sy0, sx1, sy1))


# ------------------------------------------------------------------ the band
def band(base: Image.Image, t, t0, t1, text, y, h=210, size=118, sub=None, face='Cinzel', weight=900,
         maxw=900, out=0.14):
    """Stakes-band style caption. Rules draw out from the centre, text slams in."""
    if t < t0 or t > t1: return
    u = (t - t0)
    a_out = clamp01((t1 - t) / out) if out > 0 else 1.0
    grow = ease_out(u / 0.16)
    ov = Image.new('RGBA', (W, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    bw = int(W * grow)
    x0 = (W - bw) // 2
    d.rectangle([0, 6, W, 6 + h], fill=INK + (int(200 * grow * a_out),))
    d.rectangle([x0, 0, x0 + bw, 5], fill=GOLD + (int(255 * a_out),))
    d.rectangle([x0, h + 6, x0 + bw, h + 11], fill=GOLD + (int(255 * a_out),))
    base.alpha_composite(ov, (0, int(y - 6)))
    tu = clamp01((u - 0.04) / 0.14)
    if tu > 0:
        img = fit_text(text, face, size, weight, maxw, color=CREAM, track=0.04, glow=10,
                       glow_color=GOLD_HI, glow_alpha=0.35)
        sc = 1.0 + 0.35 * (1 - ease_out(tu, 3))
        cy = y + (h * (0.42 if sub else 0.5))
        paste_center(base, img, W / 2, cy, sc, clamp01(tu * 1.5) * a_out)
        if sub:
            s = fit_text(sub, 'Atkinson', 38, 800, maxw, color=GOLD, track=0.16)
            paste_center(base, s, W / 2, y + h * 0.80, 1.0, clamp01(tu * 1.5) * a_out)


# ------------------------------------------------------------------ the crown
@functools.lru_cache(maxsize=4)
def crown_img(width=520):
    """A five-point crown, gold, with jewels in the seven school colours. Drawn at 3x and reduced."""
    k = 3; w = width * k; h = int(width * 0.72) * k
    m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    base_y0, base_y1 = int(h * 0.70), int(h * 0.92)
    pts = [(0.04, 0.70), (0.00, 0.18), (0.24, 0.46), (0.33, 0.08), (0.50, 0.40), (0.67, 0.08),
           (0.76, 0.46), (1.00, 0.18), (0.96, 0.70)]
    X = lambda x: int((0.05 + 0.90 * x) * w)
    poly = [(X(x), int(y * h)) for x, y in pts]
    d.polygon(poly, fill=255)
    d.rounded_rectangle([X(0.03), base_y0, X(0.97), base_y1], radius=int(0.03 * h), fill=255)
    for x, y in [(0.00, 0.18), (0.33, 0.08), (0.67, 0.08), (1.00, 0.18), (0.5, 0.40)]:
        r = int(0.045 * w)
        cx, cy = X(x), int(y * h)
        if (x, y) == (0.5, 0.40):
            continue
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    pad = 60 * k
    M = Image.new('L', (w + 2 * pad, h + 2 * pad), 0); M.paste(m, (pad, pad))
    g = np.linspace(0, 1, M.height)[:, None]
    top, mid, bot = np.array(GOLD_HI), np.array((230, 186, 70)), np.array((150, 105, 20))
    col = np.where(g < 0.55, top * (1 - g / 0.55) + mid * (g / 0.55), mid * (1 - (g - 0.55) / 0.45) + bot * ((g - 0.55) / 0.45))
    fill = Image.fromarray(np.broadcast_to(col[:, None, :] if col.ndim == 2 else col, (M.height, M.width, 3)).astype(np.uint8))
    img = fill.convert('RGBA'); img.putalpha(M)
    # inner shading line on the band
    dd = ImageDraw.Draw(img)
    dd.rectangle([pad + X(0.03), pad + base_y0 + int(0.02 * h), pad + X(0.97), pad + base_y0 + int(0.035 * h)], fill=(120, 80, 10, 200))
    # jewels on the band: seven schools
    for i, s in enumerate(SCHOOLS):
        cx = pad + X(0.14 + 0.72 * i / 6); cy = pad + int((base_y0 + base_y1) / 2)
        r = int(0.028 * w)
        dd.ellipse([cx - r - 6 * k, cy - r - 6 * k, cx + r + 6 * k, cy + r + 6 * k], fill=(110, 70, 8, 255))
        dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SCHOOL[s] + (255,))
        dd.ellipse([cx - r // 3 - r // 3, cy - r // 2 - r // 3, cx - r // 3 + r // 4, cy - r // 2 + r // 4], fill=(255, 255, 255, 190))
    glow = M.filter(ImageFilter.GaussianBlur(28 * k)).point(lambda v: int(v * 0.55))
    gl = Image.new('RGBA', M.size, GOLD_HI + (0,)); gl.putalpha(glow)
    out = Image.alpha_composite(gl, img)
    return out.resize((out.width // k, out.height // k), Image.LANCZOS)


# ------------------------------------------------------------------ the wall
@functools.lru_cache(maxsize=1)
def wall_data():
    grid = json.load(open(WORK / 'portraits' / 'grid.json'))
    meta = json.load(open(WORK / 'portraits' / 'meta.json'))
    return grid, meta


@functools.lru_cache(maxsize=64)
def tile_img(rid, size=138, mystery=False):
    grid, meta = wall_data()
    aff = meta[rid]['aff']
    im = Image.open(WORK / 'portraits' / f'{rid}.png').convert('RGB').resize((size, size), Image.LANCZOS)
    if mystery:
        arr = np.asarray(im).astype(np.float32)
        lum = arr.mean(axis=2, keepdims=True)
        arr = np.clip(lum * 0.16, 0, 255).repeat(3, axis=2)
        im = Image.fromarray(arr.astype(np.uint8))
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=14, fill=255)
    out = Image.new('RGBA', (size + 8, size + 8), (0, 0, 0, 0))
    ring = Image.new('L', (size + 8, size + 8), 0)
    ImageDraw.Draw(ring).rounded_rectangle([0, 0, size + 7, size + 7], radius=17, fill=255)
    col = SCHOOL[aff] if not mystery else (70, 64, 80)
    rimg = Image.new('RGBA', ring.size, col + (0,)); rimg.putalpha(ring.point(lambda v: int(v * 0.9)))
    out.alpha_composite(rimg)
    t = im.convert('RGBA'); t.putalpha(mask)
    out.alpha_composite(t, (4, 4))
    if mystery:
        q = text_img('?', 'Cinzel', 92, 900, color=SCHOOL[aff], glow=10, glow_alpha=0.8)
        paste_center(out, q, out.width / 2, out.height / 2 + 4)
    return out


MYSTERY = {'morningstar', 'ironwood', 'portcullis', 'bindweed', 'coldiron', 'lodestone', 'oracle', 'angelus'}


def wall(base, t, t0, cx=W / 2, cy=H / 2, scale=1.0, dim=1.0, tile=138, gap=10, order_seed=7):
    grid, meta = wall_data()
    keys = list(grid)
    step = tile + 8 + gap
    x0 = cx - 3 * step * scale; y0 = cy - 3 * step * scale
    for i, key in enumerate(keys):
        r, c = divmod(i, 7)
        rid = grid[key]
        ti = t0 + r * (60 / 128 / 4) + c * 0.018      # a row per sixteenth note
        u = (t - ti) / 0.20
        if u <= 0: continue
        img = tile_img(rid, tile, rid in MYSTERY)
        s = back_out(u, 2.2) * scale if u < 1 else scale
        s = 0.55 * scale + (s - 0.55 * scale) if u < 1 else s
        a = clamp01(u * 2.5) * dim
        px = x0 + c * step * scale; py = y0 + r * step * scale
        paste_center(base, img, px, py, s, a)
        if 0 < u < 0.6:  # ignition flash
            fl = Image.new('RGBA', img.size, SCHOOL[meta[rid]['aff']] + (int(200 * (1 - u / 0.6) * dim),))
            fl.putalpha(img.getchannel('A').point(lambda v, k=(1 - u / 0.6) * dim: int(v * 0.8 * k)))
            paste_center(base, fl, px, py, s, 1.0)


# ------------------------------------------------------------------ groups & bracket
def groups(base, t, t0, cy=1010, dim=1.0):
    """Sixteen group cards A-P slam in, a sixteenth of a bar apart."""
    cw, ch, gx, gy = 222, 150, 18, 18
    x0 = W / 2 - 1.5 * (cw + gx); y0 = cy - 1.5 * (ch + gy)
    rng = np.random.default_rng(16)
    for i in range(16):
        r, c = divmod(i, 4)
        ti = t0 + 0.05 + i * 0.045
        u = (t - ti) / 0.16
        if u <= 0: continue
        card = _group_card(chr(65 + i), tuple(rng.permutation(7)[:3].tolist()))
        s = 1.0 + 0.5 * (1 - ease_out(u, 3))
        paste_center(base, card, x0 + c * (cw + gx), y0 + r * (ch + gy), s, clamp01(u * 3) * dim)


@functools.lru_cache(maxsize=32)
def _group_card(letter, schools):
    cw, ch = 222, 150
    im = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=16, fill=(16, 12, 26, 235), outline=GOLD + (255,), width=3)
    L = text_img(letter, 'Cinzel', 70, 900, color=GOLD_HI, glow=6, glow_alpha=0.5)
    paste_center(im, L, cw / 2, 52)
    for k, si in enumerate(schools):
        cx = cw / 2 + (k - 1) * 46; cy = 112
        col = SCHOOL[SCHOOLS[si]]
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=col + (255,))
        d.ellipse([cx - 8, cy - 11, cx - 1, cy - 4], fill=(255, 255, 255, 170))
    return im


def bracket(base, t, t0, cy=1030, dim=1.0):
    """Sixteen slots, four rounds of gold lines converging on a crown in the middle."""
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    top, bot = cy - 420, cy + 420
    ys = [top + (bot - top) * (i + 0.5) / 8 for i in range(8)]
    colx = [70, 190, 300, 400]  # left side x per round; mirrored on the right
    rounds_t = [0.02, 0.26, 0.50, 0.74]
    width = 5
    # slots
    for side in (-1, 1):
        for i, y in enumerate(ys):
            u = (t - t0 - i * 0.02) / 0.14
            if u <= 0: continue
            x = colx[0] if side < 0 else W - colx[0]
            r = 26 * ease_out(u)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(16, 12, 26, int(240 * dim)), outline=GOLD + (int(255 * dim),), width=4)
    # rounds
    level = ys
    for rd in range(3):
        u = clamp01((t - t0 - rounds_t[rd]) / 0.22)
        if u <= 0: break
        nxt = [(level[2 * j] + level[2 * j + 1]) / 2 for j in range(len(level) // 2)]
        for side in (-1, 1):
            xa = colx[rd] if side < 0 else W - colx[rd]
            xb = colx[rd + 1] if side < 0 else W - colx[rd + 1]
            xa2 = xa + (26 if rd == 0 else 0) * (-side)
            for j, yn in enumerate(nxt):
                for yy in (level[2 * j], level[2 * j + 1]):
                    # horizontal out, then vertical to the join, then horizontal in
                    xm = xa2 + (xb - xa2) * 0.5
                    seg = [(xa2, yy), (xm, yy), (xm, yn), (xb, yn)]
                    _draw_partial(d, seg, ease_out(u), GOLD + (int(255 * dim),), width)
        level = nxt
    # final: the two semi-lines run into the centre
    u = clamp01((t - t0 - rounds_t[3]) / 0.2)
    if u > 0:
        for side in (-1, 1):
            xa = colx[3] if side < 0 else W - colx[3]
            xe = W / 2 - 60 * (-side) * -1 if False else (W / 2 + side * 70)
            _draw_partial(d, [(xa, level[0]), (xe, level[0])], ease_out(u), GOLD_HI + (int(255 * dim),), width + 2)
    glow = ov.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(glow); base.alpha_composite(ov)
    u = (t - t0 - rounds_t[3] - 0.16) / 0.22
    if u > 0:
        paste_center(base, crown_img(300), W / 2, level[0] - 10, 0.55 * back_out(u, 2.0) if u < 1 else 0.55, clamp01(u * 3) * dim)


def _draw_partial(d, pts, u, col, width):
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(L); left = total * u
    for i, l in enumerate(L):
        if left <= 0: break
        a, b = pts[i], pts[i + 1]
        f = min(1.0, left / l) if l > 0 else 1
        e = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        d.line([a, e], fill=col, width=width)
        left -= l


# ------------------------------------------------------------------ particles
@functools.lru_cache(maxsize=1)
def _dust():
    rng = np.random.default_rng(3)
    n = 140
    return (rng.random(n) * W, rng.random(n) * H, rng.random(n) * 2.4 + 0.6, rng.random(n) * 28 + 8, rng.random(n) * 6.28)


def dust(base, t, alpha=1.0):
    xs, ys, rs, vs, ph = _dust()
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x, y, r, v, p in zip(xs, ys, rs, vs, ph):
        yy = (y - v * t) % H; xx = x + 12 * math.sin(t * 0.8 + p)
        a = int(180 * alpha * (0.5 + 0.5 * math.sin(t * 2 + p)))
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=GOLD_HI + (a,))
    base.alpha_composite(ov.filter(ImageFilter.GaussianBlur(1.2)))


def radial_bg(color=(26, 16, 40), center=(W / 2, H * 0.45), radius=900, base=INK):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) / radius
    k = np.clip(1 - r, 0, 1) ** 1.6
    arr = np.array(base)[None, None, :] * (1 - k[..., None]) + np.array(color)[None, None, :] * k[..., None]
    return Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
