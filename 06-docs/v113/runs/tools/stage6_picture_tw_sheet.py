"""THE CONTACT SHEET (composed from files the snap tools wrote; no browser here):
  row 1  the resting silhouette: the seven scythes at the app's size (453x805), Thornwake's verdant scythe by the numbers;
         and the HUD charge rune (kept) at four charges
  row 2  THE CAST: the resting blade, then the blade greening, brierAge 0.02..0.62 (half-seconds)
  row 3  A BRAMBLE GROWS out of the blow that planted it, its picture age 0.02..0.62 (half-seconds)
  row 4  THE SNARE: 2 steps before, then the shoots growing, clenching, holding, drying, wilting
  row 5  A BITE: the thorn flash on the foe's rim, ENTANGLE n
  row 6  THE CLOSE: the green goes; then a bramble's last second, browning
  rows 7-9  the window's key states against a white sanctified foe, a dark foe and an ordinary foe
usage: tw_sheet.py out.png LOOKFOE [WHITE DARK ORDINARY as foe:seed:side:castN]"""
import sys, pathlib, json, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
S = HERE / "snaps"
OUT = pathlib.Path(sys.argv[1])
FOE0 = sys.argv[2] if len(sys.argv) > 2 else "gravemourn"
TRIO = [a.split(":") for a in sys.argv[3:6]] if len(sys.argv) > 5 else [["dawnbringer", "99001", "a", "1"], ["gravemourn", "99015", "a", "1"], ["grudgebearer", "31337", "b", "2"]]
F = lambda n: ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", n)
FB = lambda n: ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", n)
W = 2200
rows = []


def label(im, text, sz=15):
    o = Image.new("RGB", (im.width, im.height + sz + 10), (12, 10, 16)); o.paste(im, (0, sz + 10))
    ImageDraw.Draw(o).text((4, 2), text, fill=(214, 226, 240), font=F(sz)); return o


def hstack(ims, gap=8):
    h = max(i.height for i in ims); o = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1), h), (12, 10, 16))
    x = 0
    for i in ims: o.paste(i, (x, 0)); x += i.width + gap
    return o


def fit(im, w):
    if im.width <= w: return im
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


L = json.loads((S / f"look_{FOE0}.json").read_text())
# row 1: the silhouette and the charge rune
sil = [l for l in (HERE / "sil_final.out").read_text().splitlines() if "SCYTHE |dL|" in l and not l.startswith(" ")]
scy = Image.open(S / "sil_final_scythes.png")
names = [l.split()[0] + " (" + l.split()[1] + ")" for l in sil]
vals = {l.split()[0]: l.split("med ")[1].split()[0] for l in sil}
tiles = [label(scy.crop((200 * j, 0, 200 * j + 200, 200)).resize((220, 220), Image.LANCZOS),
               f"{names[j]}  |dL| {vals[names[j].split()[0]]}", 14) for j in range(len(names))]
sig = [label(Image.open(S / f"look_{FOE0}_sig{i}.png").resize((150, 150), Image.LANCZOS),
             f"charge {L['sig%d' % i]['cf']:.2f}{' (ready)' if L['sig%d' % i]['cf'] >= 1 else ''}", 14) for i in range(4)]
rank = sorted(vals.items(), key=lambda kv: -float(kv[1]))
pos = [k for k, _ in rank].index("thornwake") + 1
rows.append((f"THE RESTING SILHOUETTE at the app's size (453x805, chain on): the {len(names)} scythes. Thornwake's verdant scythe "
             f"(SHAPES._scGrown: a grown hook, the crescent one great thorn with a serrated inner edge, a runner putting down two "
             f"shoots) as shipped and unchanged: weapon |dL| over the floor, median of 8 frames, {pos} of {len(names)}. It reads, so no "
             f"row touches SHAPES. RIGHT: the HUD charge rune, KEPT (a thorn ring that closes as the charge fills: the snare).",
             hstack([hstack(tiles, 6), hstack(sig, 6)], gap=30)))
cs = []
if "rest" in L: cs.append(label(Image.open(S / f"look_{FOE0}_rest.png").resize((300, 300), Image.LANCZOS), "at rest (before the first cast)"))
cs += [label(Image.open(S / f"look_{FOE0}_cast{i}.png").resize((300, 300), Image.LANCZOS),
             f"brierAge {L['cast%d' % i]['age']:.2f}{' (hit stop)' if L['cast%d' % i]['stop'] else ''}") for i in range(6) if f"cast{i}" in L]
rows.append(("THE CAST -- the scythe's blade GREENS for the window, over 0.25s (brierAge in half-seconds; the first frames are the "
             "cast's own 0.08s hit stop, under the banner, which now stands on the caster): the pale steel crescent filled green, "
             "core at the edge to dark at the heel, its cutting edge and inner thorns relit in core. It stays green while blows "
             "plant brambles.", hstack(cs)))
pl = [label(Image.open(S / f"look_{FOE0}_plant{i}.png").resize((300, 300), Image.LANCZOS),
            f"bramble age {L['plant%d' % i].get('pAge', 0):.2f}{' (hit stop)' if L['plant%d' % i]['stop'] else ''}") for i in range(6) if f"plant{i}" in L]
if pl:
    rows.append(("A BLOW LEAVES A BRAMBLE -- a tangle of thorned canes grows out of the struck ball over 0.3s on the presentation "
                 "clock (it plays through the blow's own hit stop): seven canes arching through it, each with an offshoot, dark with "
                 "core seams and thorns, alpha 0.5, inside the sim's own radius (patchR 80), leaves lifting off it. Floor: world pass, "
                 "source-over, under both balls.", hstack(pl)))
sn = []
for i in range(6):
    k = f"snare{i}"
    if k not in L: continue
    v = L[k]
    t = "2 steps before" if i == 0 else f"+{[1, 8, 20, 50, 84][i - 1]} steps  pin {v.get('pin', 0):.2f}"
    sn.append(label(Image.open(S / f"look_{FOE0}_{k}.png").resize((300, 300), Image.LANCZOS), t))
if sn:
    rows.append(("THE SNARE -- the foe steps into a bramble and is rooted 0.6s: four thorn shoots rise out of the bramble under it, "
                 "climb its rim and clench (0.12s + 0.1s), hold for the pin, dry through its last 30% and wilt 0.2s after it lets go "
                 "-- Tendril's root picture, reused; Paradox's hexagon is kept off the snared ball.", hstack(sn)))
bt = []
for i in range(4):
    k = f"bite{i}"
    if k not in L: continue
    v = L[k]
    t = "1 step before a bite" if i == 0 else f"+{[1, 4, 9][i - 1]} steps  entangle {v.get('ent', 0)}"
    bt.append(label(Image.open(S / f"look_{FOE0}_{k}.png").resize((300, 300), Image.LANCZOS), t))
if bt:
    rows.append(("A BITE -- every 0.5s in a bramble the thorns bite (2 damage, entangle +1): four thorns flash out of the foe's rim "
                 "on the bramble's side for 0.12s, and the ENTANGLE tag counts (a new one when the count changes, or the count "
                 "written onto the blow's own tag already up).", hstack(bt)))
co = [label(Image.open(S / f"look_{FOE0}_close{i}.png").resize((260, 260), Image.LANCZOS),
            f"brierOut {L['close%d' % i]['outT']:.2f}  green {L['close%d' % i]['green']:.2f}", 14) for i in range(6) if f"close{i}" in L]
br = [label(Image.open(S / f"look_{FOE0}_brown{i}.png").resize((200, 200), Image.LANCZOS),
            f"age {L['brown%d' % i]['bAge']:.2f} of 6", 14) for i in range(5) if f"brown{i}" in L]
rows.append(("THE CLOSE -- the blade's green goes over 0.3s; the brambles STAY (they outlive the window by up to 6s and still "
             "snare and bite). RIGHT: a bramble's last second, browning on the sim's own clock and gone on the step the simulation "
             "removes it. The kill and the verdict take the green and the brambles out over 0.3s.",
             hstack([hstack(co, 6)] + ([hstack(br, 6)] if br else []), gap=24)))
for (foe, seed, side, cn), what in zip(TRIO, ("a WHITE SANCTIFIED foe", "a DARK foe", "an ORDINARY foe")):
    P = f"tw-final-fx_{foe}_{seed}{side}_1080" + (f"_c{cn}" if cn != "1" else "")
    ks = [("cast", "the cast frame"), ("green", "the blade green"), ("plant", "a bramble growing"), ("bramble", "brambles, foe out"),
          ("snare", "the snare"), ("bite", "a bite +2"), ("stop", "in a hit stop"), ("close1", "the close +0.1s"),
          ("after", "after the window"), ("brown", "its last 0.6s")]
    tl = []
    for k, t in ks:
        p = S / f"{P}_{k}.png"
        if p.exists(): tl.append(label(Image.open(p).resize((200, 200), Image.LANCZOS), t, 13))
    if tl:
        rows.append((f"THE WINDOW against {what} ({foe.capitalize()}, seed {seed}, Thornwake as side {side}"
                     f"{', cast ' + cn if cn != '1' else ''}), 1080x1920 crops (460 units) round the caster, the foe or the newest bramble",
                     hstack(tl, gap=5)))
rows = [(t, fit(im, W - 32)) for t, im in rows]
hdr = ("THORNWAKE / BRAMBLESNARE -- THE PICTURE (v84 section 4), stage 6, Claude Code's first cut under Rick's "
       "\"you pick, i overrule\"")
sub = (HERE / "sheet_header.txt").read_text().strip() if (HERE / "sheet_header.txt").exists() else ""
rows = [(textwrap.wrap(t, 215), im) for t, im in rows]
subl = textwrap.wrap(sub, 200) if sub else []
H = 70 + 26 * len(subl) + sum(r[1].height + 20 + 24 * len(r[0]) for r in rows)
o = Image.new("RGB", (W, H), (8, 7, 11)); d = ImageDraw.Draw(o)
d.text((16, 14), hdr, fill=(200, 255, 210), font=FB(28))
y = 62
for t in subl:
    d.text((16, y), t, fill=(200, 214, 232), font=F(18)); y += 26
y += 8
for ls, im in rows:
    for t in ls:
        d.text((16, y), t, fill=(222, 212, 196), font=F(17)); y += 24
    y += 4
    o.paste(im, (16, y)); y += im.height + 16
o.save(OUT, optimize=True)
print(OUT, o.size)
