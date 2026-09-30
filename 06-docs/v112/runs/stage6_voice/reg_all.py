"""Scratch: the picks' register against EVERY cast (and the named sub-voices) on a page."""
import sys, pathlib
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from zenith_voice_lab import NOISE_SEEDS, SR, T0, bands, pcm
from ironwood_voice_lab import RENDER_JS
from bindweed_voice_lab import mreg
from scpage import game
pg = pathlib.Path(sys.argv[1])
with game(game_path=pg) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
    import re
    subs = sorted(set(re.findall(r'w === "([a-z]+-[a-z-]+)"', src)))
    def B(k, p):
        return [bands(pcm(page.evaluate(RENDER_JS, [[["play", T0, k, p]], 3.0, sd, None]))[int(T0 * SR):]) for sd in NOISE_SEEDS[:4]]
    mine = {"cast": B("ult", {"w": "heartwood"}), "root": B("ult", {"w": "heartwood-root"})}
    res = []
    for w in [i for i in ids if i != "heartwood"] + [s for s in subs if not s.startswith("heartwood")]:
        D = B("ult", {"w": w, "n": 2})
        res.append((w, mreg(mine["cast"], D), mreg(mine["root"], D)))
    for nm in ("cast", "root"):
        col = 1 if nm == "cast" else 2
        top = sorted(res, key=lambda r: -r[col])[:6]
        print(f"{pg.name}: the {nm} against {len(res)} ult voices (every cast and sub-voice)")
        print("  top: " + ", ".join(f"{t[0]} {t[col]:.2f}" for t in top))
    print("  over 0.80: cast " + str([t[0] for t in res if t[1] > 0.80]) + "  root " + str([t[0] for t in res if t[2] > 0.80]))
