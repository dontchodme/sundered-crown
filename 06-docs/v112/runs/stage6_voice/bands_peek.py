import sys, pathlib
sys.path.insert(0, "C:/dev/sundered-crown/tools")
import numpy as np
from zenith_voice_lab import SR, T0, bands, pcm, BANDS
from ironwood_voice_lab import RENDER_JS
from scpage import game
import heartwood_voice_lab as H
S = pathlib.Path(sys.argv[1])
TH = pathlib.Path("C:/dev/sundered-crown/02-chain/sc-tendril-fx.html").read_text(encoding="utf-8")
TB = {w: H.tendril_arm(TH, w)[1] for w in ("bindweed", "bindweed-root")}
with game(game_path=S) as (page, errors):
    def R(evs):
        return pcm(page.evaluate(RENDER_JS, [evs, 3.0, None, None]))
    V = {}
    for k, p in [("hit11", ("hit", {"dmg": 11, "crit": False})), ("thornwake", ("ult", {"w": "thornwake"})),
                 ("vinesower", ("ult", {"w": "vinesower"})), ("thornshear", ("ult", {"w": "thornshear"})),
                 ("ironwood", ("ult", {"w": "ironwood"})), ("paradox", ("ult", {"w": "paradox-pin"})),
                 ("death", ("death", {})), ("dry", ("ult", {"w": "ironwood-wither"})), ("dawn", ("ult", {"w": "dawnbringer"})),
                 ("ember", ("ult", {"w": "emberedge"})), ("nightfell", ("ult", {"w": "nightfell"})), ("axiom", ("ult", {"w": "axiom"}))]:
        V[k] = bands(R([["play", T0, p[0], p[1]]])[int(T0 * SR):])
    V["t-cast"] = bands(R([["body", T0, TB["bindweed"], {}]])[int(T0 * SR):])
    V["t-root"] = bands(R([["body", T0, TB["bindweed-root"], {}]])[int(T0 * SR):])
    print("band  " + " ".join(f"{k[:6]:>6}" for k in V))
    for i, fc in enumerate(BANDS):
        print(f"{fc:6.0f}" + " ".join(f"{20*np.log10(max(v[i]/v.max(),1e-6)):6.0f}" for v in V.values()))
