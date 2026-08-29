#!/usr/bin/env python3
"""THE ENVELOPE, ON ONE ULTIMATE AT A TIME — FX-RUNTIME-BRIEF.md Stage 1.

    python ult_envelope_lab.py                       three relics, two arms
    python ult_envelope_lab.py --ids widowmaker --envelopes linear,snap,hard
    python ult_envelope_lab.py --ids lastlight --phase bloom

THE THESIS BEING TESTED, in the brief's words: every ultimate in this game runs
on `k = t / life`, one clamped linear ratio, and that is the ONLY timing
structure any of the twenty-five have. No anticipation, no snap, no hold, no
settle. Give the same geometry a real clock and it should read as a different
animation for no new drawing code at all.

If it does not, Stage 2's particle runtime and Stage 3's displacement pass are
being planned on a false premise, and that answer is worth a session.

WHY THE CLOCK IS `u.t` AND NOT `k`. `_ult()` hands each branch
`k = clamp(u.t / u.life, 0, 1)`, so `k` looks like the clock. It is not the
only one. Counted in `drawUltOver`, fifteen branches compute their own fade
straight off the seconds:

    fade = 1 - clamp((u.t - 0.42) / 1.0, 0, 1)
    grow = clamp(u.t / 0.40, 0, 1)

Reshaping `k` would leave every one of those on its original linear ramp and
the set-piece would come apart -- the light snapping while its own fade did
not. Warp `u.t` instead and `k`, `fade`, `grow`, `heat` and `e3` all reshape
together, because every one of them is derived from it.

NOTHING IS PATCHED TO MEASURE THIS. The set-piece is driven directly: `ultFx`
is assigned and `u.t` is set per frame, the same zero-fight sample
`ult_bloom_probe.py` and `ult_filmstrip.py` take. So an arm is just a different
list of `t` values, and the "linear" arm is the game exactly as it ships. When
this graduates from a lab to the build, the one-line home for it is `_ult()`
returning a shallow copy of `u` with a warped `t` -- checked, and safe: no
branch in `drawUltOver` or `drawUltUnder` ever WRITES to `u`.

`m.t` still advances a real 1/60 per frame so the oscillators that read wall
time keep running. The fighters do not move: this is the set-piece under a
clock, not a fight, and a fight would put motion in the picture that is not
the thing being judged.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
from clip_spread import resolve_ffmpeg

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-pace.html"
LIB = REPO / "05-reference" / "post" / "ultfx-library.json"

# THREE SHAPES, WHICH IS THE BRIEF'S OWN INSTRUCTION -- "a nova, a beam, a
# sustained field" -- so the answer cannot be a property of one silhouette.
# The same reasoning that picked blurscale_spread.py's defaults, and the same
# reasoning as CLAUDE.md §4.8: look at the superset before generalising.
DEFAULT_IDS = ["widowmaker", "aureole", "lastlight"]


def shape(x, ant, snap, snap_to, p):
    """[0,1] -> [0,1], monotonic, with a pause, a snap and a long settle.

    MONOTONIC ON PURPOSE, and this is the one place the brief has to be read
    carefully. §3.1 asks for overshoot, and overshoot in a t-warp is not the
    same thing as overshoot in a radius: `t` running past `life` and back would
    drive every `fade = 1 - clamp((u.t - X) / Y)` down and then UP again, which
    is a flicker rather than a bounce. Overshoot belongs in the geometry, per
    branch, and that is Stage 4. What this can honestly offer is where the
    time GOES, which is most of what reads as timing anyway.

      ant      dead time before anything happens -- the anticipation beat
      snap     what fraction of the remaining time the burst occupies
      snap_to  how much of the animation that burst covers
      p        how sharply it decelerates inside the burst
    """
    if x <= ant:
        return 0.0
    u = (x - ant) / max(1e-6, 1.0 - ant)
    if snap >= 1.0 or u < snap:
        return snap_to * (1.0 - (1.0 - min(1.0, u / max(1e-6, snap))) ** p)
    v = (u - snap) / max(1e-6, 1.0 - snap)
    return snap_to + (1.0 - snap_to) * (v * v * (3.0 - 2.0 * v))


# A SPREAD, NOT A RECOMMENDATION (Rule 2). `linear` is the control and it is
# the game as it ships -- shape() returns x exactly, so that arm is not an
# approximation of today, it IS today.
ENVELOPES = {
    "linear": dict(ant=0.00, snap=1.00, snap_to=1.00, p=1.0),
    "snap":   dict(ant=0.06, snap=0.30, snap_to=0.72, p=3.0),
    "hard":   dict(ant=0.10, snap=0.18, snap_to=0.82, p=4.0),
}

def life_map(build: pathlib.Path, page) -> dict:
    """The engine's own per-relic ult life, read out of the build.

    It is an object literal inline inside `Match`, so nothing exposes it and
    there is nothing to import. `ult_bloom_probe.py` keeps a hand-copy of it
    and warns that a drift makes both wrong -- so this brace-matches the
    literal out of the build text and hands it to the PAGE to evaluate,
    comments and all. One source of truth, and it is the shipped build.

    A guessed life would be worse here than anywhere else in the repo: the
    whole measurement is where time goes inside `life`.
    """
    src = build.read_text(encoding="utf-8", errors="replace")
    anchor = src.index("this.ultFx = {")
    i = src.index("life: {", anchor) + len("life: ")
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    return page.evaluate("(t) => eval('(' + t + ')')", src[i:j + 1])


SETUP_JS = r"""([id, foe, block, w, h]) => {
  const cv = document.getElementById('cv');
  AC.setResolution(w, h);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const wp = AC.WEAPONS.find(x => x.id === id);
  const m = new AC.Match(id, foe, 25064);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.30; m.a.y = A.h * 0.34;
  m.b.x = A.w * 0.70; m.b.y = A.h * 0.64;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.shake = 0;                        /* Math.random in the draw path */
  window.__lab = { m: m, block: block, wp: wp };
  /* The engine's own life for this ultimate where it has one. A guessed life
     would make every arm a comparison against a clock the game never runs. */
  return { life: (wp.ult && wp.ult.life) || null,
           id: id,
           kind: wp.ult ? wp.ult.kind : null, name: wp.ult ? wp.ult.name : id };
}"""

FRAME_JS = r"""([t, mt, q, life]) => {
  /* `life` is passed in per frame rather than stashed at setup. It is
     resolved on the Python side -- wp.ult.life where the relic has one, else
     Match's own map -- and an earlier version read it off window.__lab, which
     never carried it. Every frame then drew with `life: undefined`, so
     `k = clamp(u.t / u.life)` was NaN and the arms were being compared on a
     picture the game cannot produce. Nothing errored. CLAUDE.md §4.1's defect
     class, in the harness rather than the art. */
  const L = window.__lab, m = L.m, b = L.block, wp = L.wp;
  if (!(life > 0)) throw new Error("bad life: " + life);
  m.t = mt;
  m.ultFx = b
    ? Object.assign({}, b, { src:"a", tgt:"b", x:m.a.x, y:m.a.y,
        tx:m.b.x, ty:m.b.y, aff:m.a.aff, t:t, life:life })
    : { w: wp.id, kind: wp.ult.kind, src:"a", tgt:"b", x:m.a.x, y:m.a.y,
        tx:m.b.x, ty:m.b.y, hit:true, radius:(wp.ult.radius||300),
        aff:m.a.aff, t:t, life:life };
  /* Unmaking's flicker is a live Math.random inside drawUltOver. Pinned per
     FRAME index rather than once per clip, so the two arms see the same
     random stream at the same MOMENT of the animation and the comparison is
     the envelope and not the noise. */
  const real = Math.random;
  Math.random = (function(s){ return function(){
    s |= 0; s = (s + 0x6D2B79F5) | 0;
    var x = Math.imul(s ^ (s >>> 15), 1 | s);
    x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  }; })(0x5EEDF00D);
  AC.__draw(m);
  Math.random = real;
  const u = document.getElementById('cv').toDataURL('image/jpeg', q);
  return u.slice(u.indexOf(',') + 1);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--ids", default=",".join(DEFAULT_IDS))
    ap.add_argument("--envelopes", default="linear,snap")
    ap.add_argument("--phase", default=None,
                    help="which captured phase; default is the last, which is "
                         "the payload for every multi-phase ult")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--lead", type=float, default=0.35,
                    help="seconds of quiet before the cast, so the "
                         "anticipation beat has something to be quiet against")
    ap.add_argument("--tail", type=float, default=0.9,
                    help="seconds held after life, so the settle is on screen")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--q", type=float, default=0.95)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--out", default=str(REPO / "07-shorts" / "envelope"))
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2
    lib = json.loads(LIB.read_text(encoding="utf-8")) if LIB.exists() else {}
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    envs = [e.strip() for e in args.envelopes.split(",") if e.strip()]
    for e in envs:
        if e not in ENVELOPES:
            print(f"! unknown envelope {e!r}; have {list(ENVELOPES)}")
            return 2

    ff = resolve_ffmpeg("ffmpeg")
    LIVES = {}
    out_root = pathlib.Path(args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    H = round(args.w * 16 / 9)
    made = []

    with game(game_path=path) as (page, errors):
        LIVES = life_map(path, page)
        print(f"[life] {len(LIVES)} relics from Match's own map in "
              f"{path.name}")
        for ident in ids:
            entry = lib.get(ident)
            phase, block = None, None
            if entry and entry.get("phases"):
                phase = args.phase or entry["phases"][-1]
                block = entry["blocks"].get(phase)
            foe = "dawnbringer" if ident == "grudgebearer" else "grudgebearer"
            info = page.evaluate(SETUP_JS, [ident, foe, block, args.w, H])
            # wp.ult.life where the relic carries its own (the later ones do);
            # otherwise Match's inline map, which is where the original
            # twenty-one live. Never a default.
            life = info["life"] or LIVES.get(ident)
            if not life:
                print(f"! {ident} has no life in wp.ult and is not in Match's "
                      f"map; skipping rather than guessing one")
                continue
            print(f"\n{ident}  {info['name']}  kind={info['kind']}  "
                  f"life={life:.2f}s  phase={phase or '-'}")

            n_lead = round(args.lead * args.fps)
            n_life = round(life * args.fps)
            n_tail = round(args.tail * args.fps)
            for env in envs:
                P = ENVELOPES[env]
                tmp = out_root / f"_frames_{ident}_{env}"
                if tmp.exists():
                    shutil.rmtree(tmp)
                tmp.mkdir(parents=True)
                i = 0
                for f in range(n_lead):
                    mt = f / args.fps
                    b64 = page.evaluate(FRAME_JS,
                                        [-1.0, mt, args.q, life])
                    (tmp / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(b64))
                    i += 1
                for f in range(n_life + n_tail):
                    x = min(1.0, f / max(1, n_life))
                    t = life * shape(x, **P)
                    mt = (n_lead + f) / args.fps
                    b64 = page.evaluate(FRAME_JS,
                                        [t, mt, args.q, life])
                    (tmp / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(b64))
                    i += 1

                mp4 = out_root / f"{ident}-{env}.mp4"
                subprocess.run(
                    [ff, "-y", "-hide_banner", "-loglevel", "error",
                     "-framerate", str(args.fps), "-i", str(tmp / "f_%05d.jpg"),
                     "-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf),
                     "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                     str(mp4)], check=True)
                shutil.rmtree(tmp)
                made.append(mp4)
                print(f"   {env:<7} {i} frames -> {mp4.name}  "
                      f"{mp4.stat().st_size/1e6:.1f} MB")

        if errors:
            print("\n! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    print(f"\n{len(made)} clips in {out_root}")
    print("\nEVERY ARM IS THE SAME LENGTH AND THE SAME GEOMETRY. Only where the "
          "time\ngoes is different, so anything that reads differently is the "
          "envelope.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
