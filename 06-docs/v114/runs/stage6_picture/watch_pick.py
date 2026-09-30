"""Row 8 of the contact sheet out of watch.py's montages (no browser): tiles cut back out of watch/<tag>_<group>_<part>.png
by their order in watch/<tag>.json -- the first window from before the cast to after the close, then the kill and the
verdict. usage: watch_pick.py tag. SCRATCH."""
import sys, json, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
TAG = sys.argv[1]
W = HERE / "watch"
J = json.loads((W / f"{TAG}.json").read_text())
fr = J["frames"]
by = {"all": [], "win": [], "kill": []}
for f in fr: by[f["k"]].append(f)
TW, TH = 453 // 2, 805 // 2


def tile(group, i):
    part, j = divmod(i, 32)
    im = Image.open(W / f"{TAG}_{group}_{part}.png")
    x, y = (j % 8) * TW, (j // 8) * TH
    return im.crop((x, y, x + TW, y + TH))


win = by["win"]
w0 = J["wins"][0]
first = [(i, f) for i, f in enumerate(win) if f["s"] <= (w0[1] or 10**9) + 72]
# before the cast, the cast, the run, the window at a few points, the close and the drain
pick = []
cast_i = next(i for i, f in first if f["win"])
want = [cast_i - 2, cast_i, cast_i + 1, cast_i + 2, cast_i + 8, cast_i + 24, cast_i + 40]
close_i = next((i for i, f in first if i > cast_i and not f["win"]), None)
if close_i is not None: want += [close_i - 1, close_i, close_i + 2, close_i + 4]
want = [i for i in want if 0 <= i < len(first)]
tiles = [tile("win", first[i][0]) for i in want]
ov = J["overAt"]
tiles += [tile("win", i) for i, f in enumerate(win) if ov - 35 <= f["s"] <= ov + 70][:5]   # the kill, the window open: the drain
kill = by["kill"]
tiles += [tile("kill", i) for i in ([len(kill) - 1] if kill else [])]                       # the verdict
o = Image.new("RGB", (len(tiles) * (TW + 4), TH), (12, 10, 16))
for k, t in enumerate(tiles): o.paste(t, (k * (TW + 4), 0))
o.save(W / "sheet_watch.png")
txt = (f"ONE FIGHT WATCHED at the app's size (453x805, chain on, shake as played): Goreshard v Spellbreaker, seed 99015"
       f" -- her first window from 0.25s before the cast to after the drain; then her last window, still open at the kill: the "
       f"red drains inside the kill's own stop, and the verdict "
       f"(winner {J['winner']}; windows at steps {J['wins']}; over at step {J['overAt']}; thrown {J['thrown']}). "
       f"Each tile's first line: t, WIN, fade, age, out, glow; second: foe stacks, STOP, OVER, hp.")
(W / "sheet_watch.txt").write_text(txt)
print(o.size, len(tiles), "tiles;", txt)
