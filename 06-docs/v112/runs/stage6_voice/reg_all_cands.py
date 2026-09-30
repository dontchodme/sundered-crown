"""Scratch: every cast candidate's register against every ult voice on a page (information, not a gate)."""
import sys, pathlib, json, re
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from zenith_voice_lab import NOISE_SEEDS, SR, T0, bands, pcm
from ironwood_voice_lab import RENDER_JS
from bindweed_voice_lab import mreg
import heartwood_voice_lab as H
from scpage import game
pg = pathlib.Path(sys.argv[1])
run = json.loads(pathlib.Path("run_final.json").read_text(encoding="utf-8"))
G = {c["name"]: c["g"] for c in run["cast"]}
with game(game_path=pg) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
    subs = sorted(set(re.findall(r'w === "([a-z]+-[a-z-]+)"', src)))
    def B(ev):
        return [bands(pcm(page.evaluate(RENDER_JS, [[ev], 3.0, sd, None]))[int(T0 * SR):]) for sd in NOISE_SEEDS[:4]]
    refs = {w: B(["play", T0, "ult", {"w": w, "n": 2}]) for w in [i for i in ids if i != "heartwood"] + [s for s in subs if not s.startswith("heartwood")]}
    refs["hit@16"] = B(["play", T0, "hit", {"dmg": 16, "crit": False}]); refs["death"] = B(["play", T0, "death", {}])
    for nm, sp, _ in H.CAST_CANDIDATES:
        D = B(["body", T0, H.cast_body(sp, G[nm]), {}])
        r = sorted(((mreg(D, v), k) for k, v in refs.items()), reverse=True)
        print(f"{nm:<10} max {r[0][0]:.2f} ({r[0][1]}); over 0.80: {sum(1 for v, _ in r if v > 0.80)} -- " +
              ", ".join(f"{k} {v:.2f}" for v, k in r[:5]))
