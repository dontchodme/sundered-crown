"""montage.py out.png tag [keys...] [--size N] -- tile snaps/<tag>_<key>.png with labels. SCRATCH."""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
size = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--size=")), 360))
cols = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--cols=")), 4))
out, tag, keys = args[0], args[1], args[2:]
ims = []
for k in keys:
    p = HERE / "snaps" / f"{tag}_{k}.png"
    if p.exists(): ims.append((k, Image.open(p).convert("RGB").resize((size, size), Image.LANCZOS)))
rows = (len(ims) + cols - 1) // cols
M = Image.new("RGB", (cols * size, rows * (size + 22)), (20, 20, 24))
d = ImageDraw.Draw(M)
for i, (k, im) in enumerate(ims):
    x, y = (i % cols) * size, (i // cols) * (size + 22)
    M.paste(im, (x, y + 22)); d.text((x + 6, y + 4), k, fill=(230, 230, 230))
M.save(HERE / out); print(out, M.size)
