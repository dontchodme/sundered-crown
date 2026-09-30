"""THE CONTACT SHEET (composed from files the snap tools wrote; no browser here). All on hw-tip-fx.html: Heartwood's
stages carried onto 02-chain/sc-tendril-fx (the first tip with Tendril's root, which the root reuses) + the rows
+ SPECS.heartwood out -- the look as it ships.
  row 1  the resting silhouette: the seven greatswords at the app's size (453x805), the shipped look (hw_sil.py)
  row 2  THE CAST as it plays: the caster, groveAge 0.02..1.0 (half-seconds) from the cast frame
  row 3  THE CAST, the banner hidden (to see the blade under it): the same frames
  row 4  THE ROOT: a new hold +3 steps, the shoots up, clenched, held, the pin's last 0.15s, let go; a re-root +3
  row 5  THE CLOSE: the wither, groveOut 0.05..0.8 (half-seconds)
  rows 6-8  the window's key states against a white sanctified foe, a dark foe and an ordinary foe
usage: hw_sheet.py out.png castseq [rootseq] (the cast rows off castseq, the root and close rows off rootseq)"""
import sys, pathlib, json, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
S = HERE / "snaps"
OUT = pathlib.Path(sys.argv[1]); CSEQ = sys.argv[2]; SEQ = sys.argv[3] if len(sys.argv) > 3 else CSEQ
F = lambda n: ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", n)
FB = lambda n: ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", n)
W = 2200
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
    return im if im.width <= w else im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


# row 1: the silhouette
sil = [l for l in (HERE / "sil_final.out").read_text().splitlines() if "WEAPON |dL|" in l]
gs = Image.open(S / "sil_final_gs.png")
tiles = []
for j, l in enumerate(sil):
    nm, aff = l.split()[0], l.split()[1]; v = l.split("med ")[1].split()[0]
    tiles.append(label(gs.crop((200 * j, 0, 200 * j + 200, 200)).resize((280, 280), Image.LANCZOS), f"{nm} ({aff})  |dL| {v}"))
rows.append(("THE RESTING SILHOUETTE at the app's size (453x805, chain on, x1.4): the seven greatswords. Heartwood's verdant "
             "leaf blade (`_gsGrown`), the shipped look, untouched by these rows: 3rd of 7 by weapon |dL| over the floor "
             "(median of 8 frames), between Axiom and Lightkeeper", hstack(tiles)))
M = json.loads((S / f"seq_{SEQ}.json").read_text())
MC = json.loads((S / f"seq_{CSEQ}.json").read_text())
MN = json.loads((S / f"seq_{CSEQ}_nob.json").read_text())


def seq(meta, tag, keys, fmt, sz=300):
    out = []
    for k in keys:
        p = S / f"seq_{tag}_{k}.png"
        if p.exists() and k in meta: out.append(label(Image.open(p).resize((sz, sz), Image.LANCZOS), fmt(meta[k]), 14))
    return out


gk = ["g%d" % i for i in range(8)]
gf = lambda v: f"groveAge {v['age']:.2f}{'  (hit stop)' if v['stop'] else ''}"
rows.append(("THE CAST, as it plays (groveAge in half-seconds; the cast frame is the engine's own 0.08s hit stop, and the "
             "cast's banner sits on the caster): the sword greens from the grip to the tip over 0.3s -- sap up the grip, "
             "then the leaf blade from steel to living green behind a pale front -- and the leaf scale sprouts along both "
             "margins as the green passes; each pair sheds a leaf as it sprouts (the design's field of leaf motes, drawn)",
             hstack(seq(MC, CSEQ, gk, gf, 265))))
rows.append(("THE CAST, the same frames with the banner hidden (to see the blade under it)", hstack(seq(MN, CSEQ + "_nob", gk, gf, 265))))
rk = ["r0", "r1", "r2", "r3", "r4", "r5", "rr"]
rl = {"r0": "a new hold +3 steps", "r1": "shoots up the rim", "r2": "clenched", "r3": "held",
      "r4": "the pin's last 0.15s", "r5": "let go: wilting", "rr": "a re-root +3 steps"}
rows.append(("THE ROOT -- every blow in the window: Tendril's floor root, REUSED (four thorn shoots out of the floor, up the "
             "held ball's rim, dark with core tips, clenched for the pin's second, drying through its last 30%, wilting "
             "0.2s after it lets go; Paradox's hexagon skipped). The blow's own ENTANGLE tag carries the count the root's +1 "
             "leaves. A re-root keeps the shoots up and fresh.",
             hstack([label(Image.open(S / f"seq_{SEQ}_{k}.png").resize((300, 300), Image.LANCZOS),
                           f"{rl[k]}  pin {M[k]['pin']:.2f}  ENT {M[k]['ent']}", 14) for k in rk if k in M])))
ok = ["o%d" % i for i in range(6)]
rows.append(("THE CLOSE (a clock close; no sound): brown runs from the tip to the grip over 0.3s and every leaf pair it passes "
             "lets go and falls; the green fades and the steel is back by 0.4s (groveOut in half-seconds)",
             hstack(seq(M, SEQ, ok, lambda v: f"groveOut {v['out']:.2f}  fade {v['fade']:.2f}", 300))))
for foe, seed, side, what in (("dawnbringer", 99001, "a", "a WHITE SANCTIFIED foe (Dawnbringer)"),
                              ("gravemourn", 99015, "a", "a DARK foe (Gravemourn, umbral)"),
                              ("spellbreaker", 2207, "a", "an ORDINARY foe (Spellbreaker, runic)")):
    P = f"hw-tip-fx_{foe}_{seed}{side}_1080"
    ks = [("cast", "the cast frame"), ("green", "the greening, mid-blade"), ("window", "the window: motes off the blade"),
          ("stop", "a hit stop in the window"), ("root", "a root +3 steps"), ("held", "held (+30 steps)"),
          ("reroot", "a re-root +3 steps"), ("close1", "the wither (+0.1s)"), ("over", "the kill in a window")]
    tl = []
    for k, t in ks:
        p = S / f"{P}_{k}.png"
        if not p.exists() and k == "over": p = S / f"hw-tip-fx_{foe}_{seed}b_1080_over.png"   # the kill in a window: Heartwood side b
        if p.exists(): tl.append(label(Image.open(p).resize((236, 236), Image.LANCZOS), t, 13))
    rows.append((f"THE WINDOW against {what}, 1080x1920 crops (560px round the caster, or the foe for a root)", hstack(tl, 6)))
rows = [(t, fit(im, W - 32)) for t, im in rows]
hdr = ("HEARTWOOD / ROOTFAST -- THE PICTURE (v85 section 4), stage 6, Claude Code's cut under Rick's \"you pick, i overrule\"")
rows = [(textwrap.wrap(t, 215), im) for t, im in rows]
H = 70 + sum(r[1].height + 20 + 24 * len(r[0]) for r in rows)
o = Image.new("RGB", (W, H), (8, 7, 11)); d = ImageDraw.Draw(o)
d.text((16, 14), hdr, fill=(140, 230, 150), font=FB(28))
y = 70
for ls, im in rows:
    for t in ls:
        d.text((16, y), t, fill=(222, 212, 196), font=F(17)); y += 24
    y += 4
    o.paste(im, (16, y)); y += im.height + 16
o.save(OUT, optimize=True)
print(OUT, o.size)
