"""THE CONTACT SHEET (composed from files the snap tools wrote; no browser here):
  row 1  the resting silhouette: the seven greatswords at the app's size (453x805), Goreshard's barbed bloodsworn
         greatsword among them (the shipped look, unchanged), plus Goreshard's blade INSIDE the window at the same
         size; and the HUD's charge rune, the retired one (the beam) and the new
  row 2  THE CAST: the red runs down the blade from the guard to the point (goreAge 0.02..1.0, half-seconds; the
         first two inside the cast's own 0.08s stop)
  row 3  THE WINDOW: the glow's stack readout (one frame redrawn at the design's alpha for 0..4 stacks), the live
         window at the foe's 0 / 2 / 4 stacks, a priced blow (+0/+6/+14 steps: the larger float) and an unpriced
         blow's float for scale
  row 4  THE CLOSE: the red drains back from the point into the guard (goreOut 0.05..0.65, half-seconds)
  rows 5-7  the window against a white sanctified foe, a dark foe and an ordinary foe
  row 8  one fight watched at the app's size (453x805): frames of its windows, the kill and the verdict
  footer the gates' numbers (sheet_numbers.txt)
usage: gs_sheet.py out.png"""
import sys, pathlib, json, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
S = HERE / "snaps"
OUT = pathlib.Path(sys.argv[1])
F = lambda n: ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", n)
FB = lambda n: ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", n)
W = 2200
CAST = sys.argv[2] if len(sys.argv) > 2 else "cast"      # the look tag the cast / close strips come from
WIN = sys.argv[3] if len(sys.argv) > 3 else "final"      # the look tag the window strip comes from
rows = []


def label(im, text, sz=15):
    o = Image.new("RGB", (im.width, im.height + sz + 10), (12, 10, 16)); o.paste(im, (0, sz + 10))
    ImageDraw.Draw(o).text((4, 2), text, fill=(232, 222, 204), font=F(sz)); return o


def hstack(ims, gap=8):
    h = max(i.height for i in ims); o = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1), h), (12, 10, 16))
    x = 0
    for i in ims: o.paste(i, (x, 0)); x += i.width + gap
    return o


def fit(im, w):
    if im.width <= w: return im
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


def tile(p, t, sz=300, fs=14, crop=None):
    im = Image.open(p).convert("RGB")
    if crop: im = im.crop(crop)
    return label(im.resize((sz, sz), Image.LANCZOS), t, fs)


# row 1: the silhouette and the sigil
sil = [l for l in (HERE / "sil4.out").read_text().splitlines() if "WEAPON |dL|" in l and not l.startswith(" ")]
gs = Image.open(S / "sil4_gs.png")
names = [l.split()[0] for l in sil]
vals = {l.split()[0]: (l.split("med ")[1].split()[0], l.split("dE ")[1].split()[0]) for l in sil}
tiles = [label(gs.crop((200 * j, 0, 200 * j + 200, 200)).resize((220, 220), Image.LANCZOS),
               f"{names[j].replace('oathwound', 'GORESHARD').replace('@window', ' IN THE WINDOW')}  |dL| {vals[names[j]][0]}", 12) for j in range(len(names))]
sg_old = Image.open(S / "look_base_sigil.png").convert("RGB")
sg_new = Image.open(S / f"look_{WIN}_sigil.png").convert("RGB")
sg = Image.new("RGB", (sg_new.width, sg_new.height * 2 + 30), (12, 10, 16))
d0 = ImageDraw.Draw(sg)
d0.text((6, 0), "the HUD charge rune at charge 0 / 0.35 / 0.7 / full -- retired (the beam and the toll under it):", fill=(232, 222, 204), font=F(15))
sg.paste(sg_old, (0, 22 - 8))
d0.text((6, sg_new.height + 8), "new (the greatsword reddening from the guard as the charge fills, blood off its edge):", fill=(232, 222, 204), font=F(15))
sg.paste(sg_new, (0, sg_new.height + 22))
rows.append(("THE RESTING SILHOUETTE at the app's size (453x805, chain on): the seven greatswords, weapon |dL| over the floor, "
             "median of 8 frames. Goreshard's barbed bloodsworn greatsword is the shipped look (not changed): 5th of 7, mid-row. Last tile: "
             "Goreshard's blade INSIDE Bloodprice's window at the same size -- arterial red is a darkening (v81: \"darkens\"). "
             "Right: the charge rune on the HUD, retired and new.", hstack([hstack(tiles, 6), fit(sg, 640)], 24)))
LC = json.loads((S / f"look_{CAST}.json").read_text())
cs = [tile(S / f"look_{CAST}_cast{i}.png", f"goreAge {LC['cast%d' % i]['age']:.2f}{' (the cast stop)' if LC['cast%d' % i]['stop'] > 0 else ''}", 250)
      for i in range(8) if f"cast{i}" in LC]
rows.append(("THE CAST -- the red runs down the blade from the guard to the point in 0.3s (goreAge in half-seconds), a bright seam at "
             "its front; it eases out, so it is already moving inside the engine's own 0.08s cast stop (the first frames). The glow "
             "crossfades from the rest pose's to the window's. The BLOODPRICE banner is the engine's common cast banner, not this picture.",
             hstack(cs, 6)))
LW = json.loads((S / f"look_{WIN}.json").read_text())
lad = [tile(S / f"look_{WIN}_lad{i}.png", f"{i} stacks: glow {0.2 + 0.15 * i:.2f}", 230) for i in range(5) if f"lad{i}" in LW]
live = [tile(S / f"look_{WIN}_live{k}.png", f"live: foe at {k}", 230) for k in (0, 2, 4) if f"live{k}" in LW]
n = LW.get("blowN", "?")
bl = [tile(S / f"look_{WIN}_blow{i}.png", t, 230) for i, t in enumerate([f"a priced blow (n {n}) +0", "+6 steps", f"+14: the float, x{1 + 0.1 * n:.1f}" if isinstance(n, int) else "+14: the float"]) if f"blow{i}" in LW]
z = [tile(S / f"look_{WIN}_zero1.png", "an unpriced blow's float (n 0)", 230)] if "zero1" in LW else []
rows.append(("THE WINDOW -- the blade is arterial red for all 8s; its GLOW is the stack readout: the blade's glow sprite baked at 1.6x its width in the school's "
             "bright glow, added at 0.2 + 0.15 a foe Hemorrhage stack (v81: 0 -> 4 maps 0.2 -> 0.8). Left, one frame redrawn at each "
             "level; then the live window at the foe's 0 / 2 / 4 (in play the stacks run 0 / 2 / 4). A PRICED BLOW's float is "
             "x(1 + 0.1 n) larger; an unpriced blow's float for scale. Blood motes drip off the four barbs and the point all window.",
             hstack(lad + live + bl + z, 6)))
dr = [tile(S / f"look_{CAST}_drain{i}.png", f"goreOut {LC['drain%d' % i]['out']:.2f}", 250) for i in range(6) if f"drain{i}" in LC]
rows.append(("THE CLOSE -- the red drains back from the point into the guard over 0.35s (goreOut in half-seconds) and the glow "
             "returns to the rest pose's; the same drain plays at the verdict when the match ends with the window open. No sound "
             "(the design), no debris.", hstack(dr, 6)))
for P, what in json.loads((HERE / "sheet_foes.json").read_text()):
    ks = [("rest", "at rest"), ("cast2", "the run"), ("win0", "window, foe 0"), ("win2", "foe 2"), ("win4", "foe 4"),
          ("blow", "a priced blow"), ("stop", "in a hit stop"), ("close2", "the drain"), ("over", "at the verdict")]
    tl = []
    for k, t in ks:
        p = S / f"{P}_{k}.png"
        if p.exists(): tl.append(tile(p, t, 232, 14))
    rows.append((f"THE WINDOW against {what}, 1080x1920 crops (640 px round the caster)", hstack(tl, 6)))
wf = HERE / "watch" / "sheet_watch.png"
if wf.exists():
    rows.append(((HERE / "watch" / "sheet_watch.txt").read_text().strip(), Image.open(wf).convert("RGB")))
rows = [(t, fit(im, W - 32)) for t, im in rows]
hdr = ("GORESHARD / BLOODPRICE -- THE PICTURE (v81 section 4), stage 6 (v114), Claude Code's pick under Rick's "
       "\"you pick, i overrule\"")
foot = (HERE / "sheet_numbers.txt").read_text().strip().splitlines() if (HERE / "sheet_numbers.txt").exists() else []
rows = [(textwrap.wrap(t, 205), im) for t, im in rows]
fl = [w for line in foot for w in (textwrap.wrap(line, 215) or [""])]
H = 70 + sum(r[1].height + 20 + 24 * len(r[0]) for r in rows) + 30 + 22 * len(fl)
o = Image.new("RGB", (W, H), (8, 7, 11)); d = ImageDraw.Draw(o)
d.text((16, 14), hdr, fill=(255, 150, 162), font=FB(28))
y = 70
for ls, im in rows:
    for t in ls:
        d.text((16, y), t, fill=(222, 212, 196), font=F(17)); y += 24
    y += 4
    o.paste(im, (16, y)); y += im.height + 16
y += 10
for t in fl:
    d.text((16, y), t, fill=(200, 196, 186), font=F(15)); y += 22
o.save(OUT, optimize=True)
print(OUT, o.size)
