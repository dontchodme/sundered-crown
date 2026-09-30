"""Picture for the World Cup trailer: footage from the game + generated scenes, to the EDIT.

    python trailer_cut.py --out video.mp4                 # full 1080x1920 60fps
    python trailer_cut.py --preview 0.25 --out prev.mp4   # quarter size, fast
    python trailer_cut.py --still 12.3 --out still.png    # one frame
"""
from __future__ import annotations
import argparse, math, subprocess, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from trailer_gfx import *    # noqa  (W, H, WORK, ...)
from trailer_edit import *   # noqa
from clip_spread import resolve_ffmpeg

FFMPEG = resolve_ffmpeg()
CLIPS = WORK / 'clips'


class Source:
    """Sequential frame reader for one footage segment (source time advances with output time)."""

    def __init__(self, seg):
        self.seg = seg
        path = CLIPS / seg['clip'] / 'clip.mp4'
        self.p = subprocess.Popen([FFMPEG, '-v', 'error', '-ss', f"{seg['s']:.4f}", '-i', str(path),
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL)   # closing a cut early is a broken pipe, not an error
        self.idx = -1; self.frame = None

    def get(self, t):
        want = int(math.floor((t - self.seg['t0']) * self.seg['speed'] * FPS + 1e-6))
        while self.idx < want:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break                     # clip ran out: hold the last frame
            self.frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3); self.idx += 1
        return self.frame

    def close(self):
        self.p.stdout.close(); self.p.kill()


_sources = {}


def footage(seg, t):
    key = id(seg)
    if key not in _sources:
        for k in list(_sources):
            _sources.pop(k).close()
        _sources[key] = Source(seg)
    fr = _sources[key].get(t)
    if fr is None:
        return Image.new('RGBA', (W, H), INK + (255,))
    im = Image.fromarray(fr)
    u = (t - seg['t0']) / max(1e-6, seg['t1'] - seg['t0'])
    z = seg['z'][0] + (seg['z'][1] - seg['z'][0]) * u
    z += seg['punch'] * (1 - ease_out((t - seg['t0']) / 0.18, 3))
    cx, cy = seg['c']
    sh = seg['shake'] * math.exp(-(t - seg['t0']) * 9)
    if sh > 0.3:
        cx += sh * math.sin(t * 91.0); cy += sh * math.cos(t * 77.0)
    if z > 1.001:
        w, h = W / z, H / z
        x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
        im = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
    im = im.convert('RGBA')
    if seg['dim'] < 0.999:
        im = Image.blend(Image.new('RGBA', (W, H), INK + (255,)), im, seg['dim'])
    fl = seg['flash'] * max(0.0, 1 - (t - seg['t0']) / 0.09)
    if fl > 0.01:
        im = Image.blend(im, Image.new('RGBA', (W, H), (255, 250, 240, 255)), min(1.0, fl))
    return im


def label(base, seg, t):
    rid = seg['hero']
    if not rid: return
    name, school, ult = RELIC[rid]
    u = (t - seg['t0'] - 0.04) / 0.14
    if u <= 0: return
    a = clamp01(u * 2) * clamp01((seg['t1'] - t) / 0.08)
    dx = -40 * (1 - ease_out(u, 3))
    n = text_img(name.upper(), 'Atkinson', 58, 800, color=SCHOOL[school], track=0.06, stroke=5, stroke_color=INK,
                 glow=8, glow_alpha=0.45)
    s = text_img(ult.upper(), 'Cinzel', 34, 800, color=CREAM, track=0.08, stroke=4, stroke_color=INK)
    x = 64 + dx; y = 1330
    d = ImageDraw.Draw(base)
    d.rectangle([x, y - 12, x + 70 * ease_out(u), y - 7], fill=GOLD + (int(255 * a),))
    paste_center(base, n, x + n.width / 2 - 14, y + 34, 1.0, a)
    paste_center(base, s, x + s.width / 2 - 12, y + 86, 1.0, a)


_bg_cache = {}


def bg(kind):
    if kind not in _bg_cache:
        _bg_cache[kind] = radial_bg() if kind == 'open' else radial_bg(color=(46, 30, 18), center=(W / 2, 760), radius=1000)
    return _bg_cache[kind].copy()


def scene_open(t):
    """0 - 3.75: the wall of forty-nine, then the crown."""
    im = bg('open')
    t_crown = tb(1, 0)
    if t < t_crown:
        wall(im, t, 0.12, cy=1040)
    else:
        u = (t - t_crown)
        wall(im, t, 0.12, cy=1040, scale=1.0 - 0.06 * ease_out(u / 1.2), dim=max(0.28, 1 - u / 0.18))
        dust(im, t, clamp01(u / 0.3) * 0.7)
        paste_center(im, crown_img(520), W / 2, 700, 1.0 + 0.8 * (1 - ease_out(u / 0.22, 4)) + 0.05 * clamp01(u / 1.6), clamp01(u / 0.07))
        if u < 0.25:   # gold shock flash
            im = Image.blend(im, Image.new('RGBA', (W, H), GOLD_HI + (255,)), 0.45 * (1 - u / 0.25))
    # push into the first cut
    t_end = tb(2, 0)
    if t > t_end - 0.30:
        u = (t - (t_end - 0.30)) / 0.30
        z = 1 + 0.5 * ease_in(u, 3)
        w, h = W / z, H / z
        y0 = max(0.0, (H - h) / 2 - 80 * u)
        im = im.resize((W, H), Image.BICUBIC, box=((W - w) / 2, y0, (W + w) / 2, y0 + h))
        if u > 0.6:
            im = Image.blend(im, Image.new('RGBA', (W, H), (255, 250, 240, 255)), (u - 0.6) / 0.4 * 0.8)
    return im


def scene_title(t):
    T0 = TITLE_T0
    u = t - T0
    im = bg('title')
    wall(im, 99, 0, cy=1000, scale=1.35 + 0.025 * u, dim=0.07)
    dust(im, t, 0.6)
    ring_u = u / 0.5
    if 0 < ring_u < 1:   # shockwave ring behind the crown
        d = ImageDraw.Draw(im); r = 80 + 700 * ease_out(ring_u, 2)
        d.ellipse([W / 2 - r, 610 - r, W / 2 + r, 610 + r], outline=GOLD_HI + (int(200 * (1 - ring_u)),), width=int(10 * (1 - ring_u)) + 2)
    paste_center(im, crown_img(520), W / 2, 610, 1.0 + 0.9 * (1 - ease_out(u / 0.25, 4)), clamp01(u / 0.08))
    s1 = text_img('SUPER WEAPON BALL', 'Atkinson', 62, 800, color=CREAM, track=0.22)
    paste_center(im, s1, W / 2, 845 + 20 * (1 - ease_out((u - 0.10) / 0.3)), 1.0, clamp01((u - 0.10) / 0.2))
    s2 = fit_text('WORLD CUP', 'Cinzel', 230, 900, 960, gradient=(GOLD_HI, (176, 118, 24)), glow=16,
                  glow_color=GOLD_HI, glow_alpha=0.5, track=0.02)
    su = (u - 0.18) / 0.22
    paste_center(im, s2, W / 2, 990, 1.0 + 0.3 * (1 - ease_out(su, 3)), clamp01(su * 2.5))
    # a shine that crosses the wordmark once, and again on the last hit
    for ts in (0.9, tb(15, 0) - T0):
        sh = (u - ts) / 0.55
        if 0 < sh < 1:
            _shine(im, s2, W / 2, 990, sh)
    # the last hit: a small pulse
    lh = t - tb(15, 0)
    if 0 < lh < 0.25:
        im = Image.blend(im, Image.new('RGBA', (W, H), GOLD_HI + (255,)), 0.18 * (1 - lh / 0.25))
    t0, t1, txt = FOLLOW
    band(im, t, t0, t1 + 1, 'FOLLOW', y=1190, h=170, size=92, sub="SO YOU DON'T MISS A MATCH", maxw=800)
    if u < 0.10:  # the impact flash
        im = Image.blend(im, Image.new('RGBA', (W, H), (255, 250, 240, 255)), 0.9 * (1 - u / 0.10))
    return im


def _shine(im, word, cx, cy, u):
    w, h = word.size
    x = int(-0.3 * w + 1.6 * w * u)
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).polygon([(x, 0), (x + 90, 0), (x + 30, h), (x - 60, h)], fill=200)
    m = m.filter(ImageFilter.GaussianBlur(14))
    m = ImageChops.multiply(m, word.getchannel('A'))
    sh = Image.new('RGBA', (w, h), (255, 255, 255, 0)); sh.putalpha(m)
    paste_center(im, sh, cx, cy)


def frame_at(t):
    if t < tb(2, 0):
        im = scene_open(t)
    elif t >= TITLE_T0:
        im = scene_title(t)
    else:
        seg = next((s for s in F if s['t0'] <= t < s['t1']), None)
        if seg is None:
            im = Image.new('RGBA', (W, H), INK + (255,))      # the gap
        else:
            im = footage(seg, t)
            label(im, seg, t)
    # graphics on the dimmed cuts
    if tb(4, 0) <= t < tb(4, 3):
        groups(im, t, tb(4, 0), cy=1100)
    if tb(5, 0) <= t < tb(5, 3):
        bracket(im, t, tb(5, 0), cy=1100)
    for (t0, t1, txt, y, h, size) in BANDS:
        band(im, t, t0, t1, txt, y=y, h=h, size=size)
    # fade out to black for the loop
    if t > DUR - 0.40:
        im = Image.blend(im, Image.new('RGBA', (W, H), (0, 0, 0, 255)), clamp01((t - (DUR - 0.40)) / 0.40))
    return im.convert('RGB')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--still', type=float, default=None)
    ap.add_argument('--preview', type=float, default=None, help='scale factor for a fast preview')
    ap.add_argument('--start', type=float, default=0.0)
    ap.add_argument('--end', type=float, default=DUR)
    ap.add_argument('--crf', type=int, default=14)
    a = ap.parse_args()
    if a.still is not None:
        frame_at(a.still).save(a.out); return
    sc = a.preview or 1.0
    ow, oh = int(W * sc) // 2 * 2, int(H * sc) // 2 * 2
    enc = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{ow}x{oh}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow' if sc == 1 else 'veryfast',
                            '-crf', str(a.crf), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', a.out],
                           stdin=subprocess.PIPE)
    n0, n1 = int(round(a.start * FPS)), int(round(a.end * FPS))
    for n in range(n0, n1):
        im = frame_at(n / FPS)
        if sc != 1:
            im = im.resize((ow, oh), Image.BILINEAR)
        enc.stdin.write(im.tobytes())
        if n % 120 == 0:
            print(f'frame {n}/{n1}', flush=True)
    enc.stdin.close(); enc.wait()
    for k in list(_sources):
        _sources.pop(k).close()


if __name__ == '__main__':
    main()
