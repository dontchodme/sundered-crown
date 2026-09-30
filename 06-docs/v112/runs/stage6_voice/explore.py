"""Scratch: explore green-creak constructions against the lab's gates (no rows, no wavs)."""
import sys, math, pathlib
sys.path.insert(0, "C:/dev/sundered-crown/tools")
import numpy as np
import heartwood_voice_lab as H
from zenith_voice_lab import NOISE_SEEDS, SR, T0, bands, basic, cents, db, pcm
from ironwood_voice_lab import RENDER_JS, centroid
from bindweed_voice_lab import crack_info, hf_env, mod_rate, mreg, pulsed_w
from scpage import game

S = pathlib.Path(sys.argv[1])
TH = pathlib.Path("C:/dev/sundered-crown/02-chain/sc-tendril-fx.html").read_text(encoding="utf-8")
TB = {w: H.tendril_arm(TH, w)[1] for w in ("bindweed", "bindweed-root")}


def alone(x, gap=20):
    e = hf_env(x)[:600]
    i = int(np.argmax(e))
    m = e.copy(); m[max(0, i - gap):i + gap + 1] = 0
    return db(float(e[i]) / max(float(m.max()), 1e-12)), i


def body(pulse, pitch, rate, env="swell", mode=0.4, dur=0.035, fb=1400, fq=1.5, fk=0.5):
    r0, r1 = rate
    iv = (f"(1 / {r0})" if r0 == r1 else f"(1 / ({r0} * Math.pow({H.fmt(round(r1 / r0, 6))}, u)))")
    P = {"sine": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"sine" });' % dur],
         "timber": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"sine" });' % dur,
                    'this._tone(t + s, { freq: f * 2.76, gain: a * %s, dur: 0.025, type:"sine" });' % mode],
         "tri": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"triangle" });' % dur],
         "sapsine": ['this._tone(t + s, { freq: f, to: f * 0.84, gain: a, dur: %s, type:"sine" });' % dur],
         "bp": ['this._burst(t + s, { freq: f, q: 4, gain: a, dur: %s, type:"bandpass" });' % dur],
         "lpsine": ['this._burst(t + s, { freq: f * 1.6, q: 1.2, gain: a * 0.5, dur: 0.02, type:"lowpass" });',
                    'this._tone(t + s, { freq: f, gain: a, dur: %s, type:"sine" });' % dur],
         "fric": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"sine" });' % dur,
                  'this._tone(t + s, { freq: f * 2.76, gain: a * %s, dur: 0.025, type:"sine" });' % mode,
                  'this._burst(t + s, { freq: FB, q: FQ, gain: a * FK, dur: 0.012, type:"bandpass" });'],
         "fricsap": ['this._tone(t + s, { freq: f, to: f * 0.84, gain: a, dur: %s, type:"sine" });' % dur,
                  'this._burst(t + s, { freq: FB, q: FQ, gain: a * FK, dur: 0.012, type:"bandpass" });'],
         "saw": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"sawtooth" });' % dur],
         "square": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"square" });' % dur],
         "sawres": ['this._tone(t + s, { freq: f, gain: a, dur: %s, type:"sawtooth" });' % dur,
                    'this._burst(t + s, { freq: FB, q: FQ, gain: a * FK, dur: 0.03, type:"bandpass" });'],
         "resn": ['this._burst(t + s, { freq: f, q: FQ, gain: a, dur: %s, type:"bandpass" });' % dur,
                  'this._burst(t + s, { freq: f * 2.76, q: FQ, gain: a * FK, dur: %s, type:"bandpass" });' % dur],
         }[pulse]
    P = [q.replace("FB", str(fb)).replace("FQ", str(fq)).replace("FK", str(fk)) for q in P]
    L = ["const g = G;", "for (let s = 0, k = 0; s < 0.38; k++){",
         f"  const u = s / 0.4, f = {pitch}, a = g * {H.CENV[env]};", *["  " + p for p in P],
         f"  s += {iv} * (1 + 0.12 * Math.sin(k * 2.4));", "}"]
    return "\n".join(L)


CANDS = [
    ("sine280", body("sine", "280", (30, 42))),
    ("sine320", body("sine", "320", (30, 42))),
    ("sine360", body("sine", "360", (30, 42))),
    ("sine400", body("sine", "400", (30, 42))),
    ("timber320 .4", body("timber", "320", (30, 42), mode=0.4)),
    ("timber360 .4", body("timber", "360", (30, 42), mode=0.4)),
    ("timber400 .4", body("timber", "400", (30, 42), mode=0.4)),
    ("timber360 .2", body("timber", "360", (30, 42), mode=0.2)),
    ("tri360", body("tri", "360", (30, 42))),
    ("sap380", body("sapsine", "380", (32, 32))),
    ("sine360r", body("sine", "300 * Math.pow(1.3333, Math.min(1, s / 0.3))", (28, 40), "grow")),
    ("sine380 slow", body("sine", "380", (20, 28))),
    ("sine90", body("sine", "90", (30, 42))),
    ("timber90 .6", body("timber", "90", (30, 42), mode=0.6)),
]

with game(game_path=S) as (page, errors):
    def R(evs, seed=None):
        r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None]); assert not errors, errors[:3]
        return pcm(r)
    def play(k, p, seed=None): return R([["play", T0, k, p]], seed)
    def bod(t, seed=None, p=None): return R([["body", T0, t, p or {}]], seed)
    refs = {"hit@11": ("hit", {"dmg": 11, "crit": False}), "death": ("death", {}), "rune-crack": ("ult", {"w": "spellbreaker"}),
            "dry": ("ult", {"w": "ironwood-wither"}), "paradox-pin": ("ult", {"w": "paradox-pin"})}
    for w in ["thornwake", "vinesower", "thornshear", "ironwood", "dawnbringer", "emberedge", "nightfell", "axiom"]:
        refs[w] = ("ult", {"w": w})
    RB = {k: [bands(play(*v, seed=sd)[int(T0 * SR):]) for sd in NOISE_SEEDS[:4]] for k, v in refs.items()}
    RB["tendril-cast"] = [bands(bod(TB["bindweed"], sd)[int(T0 * SR):]) for sd in NOISE_SEEDS[:4]]
    RB["tendril-root"] = [bands(bod(TB["bindweed-root"], sd)[int(T0 * SR):]) for sd in NOISE_SEEDS[:4]]
    dry_cen = basic(play("ult", {"w": "ironwood-wither"}))["cen"]
    from zenith_voice_lab import pitch as fpitch
    _dx = play("ult", {"w": "ironwood-wither"}); _dm = basic(_dx)
    DRYN = fpitch(_dx, T0 + _dm["a0"] / 1000, T0 + _dm["gone"] / 1000, 60, 2000)
    print("dry creak note", DRYN, "first/last", fpitch(_dx, T0 + _dm["a0"] / 1000, T0 + _dm["a0"] / 1000 + 0.1, 60, 2000), fpitch(_dx, T0 + _dm["gone"] / 1000 - 0.1, T0 + _dm["gone"] / 1000, 60, 2000))
    h_lo = min(basic(play("hit", {"dmg": 11, "crit": False}, seed=sd))["top"] for sd in NOISE_SEEDS)
    h_hi = max(basic(play("hit", {"dmg": 11, "crit": False}, seed=sd))["top"] for sd in NOISE_SEEDS)
    tgt = math.sqrt(0.5 * h_hi * h_lo)
    for nm, x in (("tendril-root", bod(TB["bindweed-root"])), ("dry", play("ult", {"w": "ironwood-wither"})),
                  ("hit@11", play("hit", {"dmg": 11, "crit": False}))):
        print(f"ALONE {nm}: {alone(x)}")
    print(f"{'cand':<14}{'top':>7}{'aud':>5}{'rate':>5}{'puls':>6}{'cen':>5}{'grn':>6}{'fall':>6}{'alone':>7}{'note':>6}{'n/dry':>6}{'nfall':>6}  regs>0.70")
    for nm, t in CANDS:
        g = 0.1
        for _ in range(5):
            g = float(f"{g * tgt / basic(bod(t.replace('G', H.fmt(g), 1)))['top']:.4g}")
        tt = t.replace("G", H.fmt(g), 1)
        x = bod(tt); M = basic(x)
        a_ = M["a0"] / 1000 + 0.01; b_ = M["gone"] / 1000 - 0.01
        rate = mod_rate(x, a_, b_); pul = pulsed_w(x, a_, b_)[0]
        g0 = T0 + M["a0"] / 1000; g1 = T0 + M["gone"] / 1000
        fall = cents(centroid(x, g1 - 0.1, g1, 60, 4000), centroid(x, g0, g0 + 0.1, 60, 4000))
        al = alone(x)[0]
        from zenith_voice_lab import pitch as fpitch
        note = fpitch(x, g0, g1, 60, 2000)
        nf = cents(fpitch(x, g1 - 0.1, g1, 60, 2000), fpitch(x, g0, g0 + 0.1, 60, 2000))
        DB = [bands(bod(tt, sd)[int(T0 * SR):]) for sd in NOISE_SEEDS[:4]]
        regs = {k: mreg(DB, v) for k, v in RB.items()}
        hi = sorted(((v, k) for k, v in regs.items() if v > 0.70), reverse=True)
        print(f"{nm:<14}{M['top']:>7.4f}{M['aud']:>5.0f}{rate:>5.0f}{pul:>6.2f}{M['cen']:>5.0f}{M['cen'] / dry_cen:>6.2f}"
              f"{fall:>6.0f}{al:>7.1f}{note:>6.0f}{note / DRYN:>6.2f}{nf:>6.0f}  " + " ".join(f"{k} {v:.2f}" for v, k in hi))
