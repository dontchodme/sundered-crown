#!/usr/bin/env python3
"""WHAT THE `_blur(px)` FIX ACTUALLY LOOKS LIKE — the spread for Rule 2.

`shadowblur_probe.py` establishes that `shadowBlur` is in device space and
that 0 of the build's 74 live sites honour `this.k`, so every glow in the game
is 2.00x wider relative to the frame at the shipped `--w 540` and 2.24x wider
in the app than at the 1080 the art was authored at.

That is arithmetic on one blurred circle. THIS tool renders the consequence on
real ult art, because a set-piece is forty-five overlapping additive arcs and
what a 2x-wider glow does to that is not a multiply. `CLAUDE.md` §4.0 and
`docs/RENDER-LAYERS.md` §5b: two effects were chosen off sheets and rejected in
motion, so a sheet is where a spread STARTS, not where it is decided.

    python blurscale_spread.py                       the three defaults
    python blurscale_spread.py --ids dawnbringer,lastlight,foregone --crop
    python blurscale_spread.py --ids paradox --phase bloom

THE THREE ARMS, and the third is the control:

    540 SHIP    what cinema_clip.py --w 540 writes today
    540 FIXED   the same frame with shadowBlur scaled by k, the proposed fix
    1080        the design resolution, unpatched -- and the fix is a NO-OP here

Both 540 arms are upscaled 2x for display so the glow is compared in FRAME
terms, which is the only space the question lives in. A viewer sees a 1080-tall
phone regardless of what the capture was.

THE FIX IS APPLIED AT RUNTIME, NOT TO THE BUILD. A property descriptor
multiplies every `shadowBlur` write by the CONTEXT'S OWN transform scale --
`hypot(t.a, t.b)`, which is `this.k` on the main canvas -- so the sheet shows
what `_blur(px){ ctx.shadowBlur = px * this.k; }` would draw at all 74 sites
without editing a file in `02-chain/`. Nothing here can be committed by
accident, and the answer arrives before the 74 edits do.

IT PATCHES TWO SURFACES, NOT ONE, AND THAT IS A FINDING RATHER THAN A DETAIL.
`docs/DELIVERY-QUALITY-BRIEF.md` §1 describes the fix as 129 sites on the
renderer's context. Traced live, the frame does not work that way:

  - `_ballBuf` (:13790) bakes each relic body into an offscreen canvas sized
    `ceil(rad * 2 * k)` and scaled by the same `k`, then draws it back 1:1.
    So `drawGlassRelic`'s halo -- `shadowBlur = 8 + hpFrac * 26`, up to 34 --
    is device-space on the frame exactly as if it were drawn directly. It is
    on screen for BOTH relics on EVERY frame of every fight, ult or not.
  - the sealed-walls buffer (:11561) is EXCLUDED. It already compensates by
    hand with `30 / D` for its own downscale, and scaling it again would
    double-compensate and put a picture on the sheet the fix never produces.
    That is the one place in the build whose author knew about this property.

The allow-list is `[#cv, AC.renderer._bbuf]`, named explicitly, because a
blanket prototype patch is how the sealed walls would have quietly changed.

THE K=1 IDENTITY IS ASSERTED, NOT ASSUMED. `docs/DELIVERY-QUALITY-BRIEF.md` §1
sequences step 2 before step 3 on the claim that the two changes cancel at
k = 1. The tool renders 1080 both patched and unpatched and reports whether
they are bit-identical. If they are not, the sequencing argument is wrong and
the sheet says so.

Costs ZERO simulated fights: `ultFx` is set directly and nothing is stepped,
the same sample `ult_bloom_probe.py` and `ult_filmstrip.py` take.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-arc.html"
LIB = REPO / "05-reference" / "post" / "ultfx-library.json"
OUT = REPO / "05-reference" / "post"

# Mirrors Match.castUlt, copied from ult_bloom_probe.py rather than imported --
# that tool is a script with a module-level argparse and importing it would run
# it. If one of these drifts the other is wrong; they are checked against the
# engine by ult_fx_capture.py, which reads the real value.
LIFE = {"dawnbringer": 1.6, "widowmaker": 1.3, "grudgebearer": 1.7,
        "thornwake": 2.4, "gravemourn": 1.6, "spellbreaker": 1.4,
        "oathwound": 1.5, "heartwood": 2.2, "nightfell": 1.4, "axiom": 1.5,
        "ironhail": 1.3, "lightkeeper": 1.5, "farwarden": 2.6, "aureole": 1.6,
        "censer": 1.6, "emberedge": 1.5, "slagheart": 4.9, "vinesower": 5.4,
        "bulwarden": 9.5, "marrowdraw": 8.6, "paradox": 9.5}

# THREE SHAPES, NOT THREE FAVOURITES. FX-RUNTIME-BRIEF.md §3.1 asks for a nova,
# a beam and a sustained field so the answer is not a property of one silhouette.
#   dawnbringer  Daybreak     the nova, and CLAUDE.md §4.1b's own subject
#   lastlight    The Harrowing the sustained field, §4.1c, the widest art here
#   foregone     Retrace      the largest measured light source in the game, §4.1d
DEFAULT_IDS = ["dawnbringer", "lastlight", "foregone"]

FOE = "grudgebearer"

RENDER_JS = r"""([id, foe, seed, t, life, block, w, h, patch, crop]) => {
  const cv = document.getElementById('cv');
  const ctx = cv.getContext('2d');

  AC.setResolution(w, h);

  /* THE FIX, AS A PROPERTY DESCRIPTOR ON THE PROTOTYPE with an allow-list.

     THE FACTOR IS `cv.width / 1080` AND NOTHING ELSE -- not the context's
     transform scale, which was this tool's first answer and was wrong. Inside
     the arena the CTM is k * this.scale, and `this.scale` is aw / arena.w off
     a design width of 1080: a CONSTANT 2.03 at every resolution. Scaling by
     the full transform therefore multiplies every glow by 2.03 at 1080 too,
     which the k=1 identity check below caught immediately. The only part of
     the transform that moves with the capture size is `k`, so `k` is the whole
     correction -- exactly the helper DELIVERY-QUALITY-BRIEF.md §1 proposes.

     _bbuf is resolved at write time, not captured, because it is created
     lazily on the first ball drawn. Anything off the list falls straight
     through to the native setter. */
  const proto = CanvasRenderingContext2D.prototype;
  const base = Object.getOwnPropertyDescriptor(proto, 'shadowBlur');
  Object.defineProperty(proto, 'shadowBlur', {
    configurable: true,
    get(){ return base.get.call(this); },
    set(v){
      if (patch && v && this.canvas &&
          (this.canvas === cv || this.canvas === AC.renderer._bbuf)) {
        v = v * (cv.width / 1080);
      }
      base.set.call(this, v);
    }
  });
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};

  const wp = AC.WEAPONS.find(x => x.id === id);
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.26; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.74; m.b.y = A.h * 0.68;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.shake = 0;                       /* Math.random in the draw path, ult_bloom_probe.py */

  if (block) {
    m.ultFx = Object.assign({}, block, {
      src: "a", tgt: "b", x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y,
      aff: m.a.aff, t: t, life: life });
  } else {
    m.ultFx = { w: id, kind: wp.ult.kind, src: "a", tgt: "b",
                x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y, hit: true,
                radius: wp.ult.radius || 300, aff: m.a.aff, t: t, life: life };
  }

  /* Unmaking's flicker is a live Math.random inside drawUltOver. Unpinned it
     gives the two arms two different pictures and the sheet reads the flicker
     as the fix. Same pin value in every arm. */
  const real = Math.random;
  Math.random = (function(s){ return function(){
    s |= 0; s = (s + 0x6D2B79F5) | 0;
    var x = Math.imul(s ^ (s >>> 15), 1 | s);
    x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  }; })(0x5EEDF00D);

  AC.__draw(m);
  Math.random = real;
  Object.defineProperty(proto, 'shadowBlur', base);   /* harness, not a change */

  const r = AC.renderer;
  const rect = crop
    /* The caster and one arena-width around it, in DEVICE px. arena->device is
       k * (pad + scale * x) -- not k * pad + k * x. ult_bloom_probe.py lost a
       whole measurement to that once. */
    ? (function(){
        const S = r.scale, R = 300 * S * r.k;
        const bx = r.k * (r.pad + S * m.a.x), by = r.k * (r.arenaTop + S * m.a.y);
        return { x: Math.max(0, Math.round(bx - R)),
                 y: Math.max(0, Math.round(by - R)),
                 w: Math.round(2 * R), h: Math.round(2 * R) };
      })()
    : { x: Math.round(r.pad * r.k), y: Math.round(r.arenaTop * r.k),
        w: Math.round(r.aw * r.k), h: Math.round(r.ah * r.k) };

  const d = ctx.getImageData(rect.x, rect.y, rect.w, rect.h).data;
  let sum = 0, n90 = 0, n98 = 0, halo = 0;
  const N = d.length / 4;
  for (let i = 0; i < d.length; i += 4){
    const L = (0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2]) / 255;
    sum += L;
    if (L > 0.90) n90++;
    if (L > 0.98) n98++;
    /* THE GLOW BAND, and the threshold is the finding-shaped part. A blur is a
       soft skirt, so widening it moves pixels into the MIDDLE of the range and
       not into the top -- `blown` and `clipped` are the core's numbers and
       barely move. The first version of this tool counted L > 0.03 and got
       0.9999 in every arm: the arena floor and the vignette are already above
       that, so the metric was saturated before it reached the glow. CLAUDE.md
       §4.1c happening to the instrument, again. */
    if (L > 0.25 && L <= 0.90) halo++;
  }

  /* The full frame, not the crop -- the sheet wants the whole vertical. */
  const png = cv.toDataURL('image/png');
  return {
    k: cv.width / 1080, w: cv.width, h: cv.height,
    rect: rect,
    mean: sum / N, blown: n90 / N, clipped: n98 / N, halo: halo / N,
    png: png.slice(png.indexOf(',') + 1),
  };
}"""


def out_dir_for(args):
    d = OUT / "blurscale"
    d.mkdir(parents=True, exist_ok=True)
    return d


def render(page, ident, seed, t, life, block, w, h, patch, crop):
    return page.evaluate(RENDER_JS, [ident, FOE, seed, t, life, block,
                                     w, round(w * 16 / 9), patch, crop])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--ids", default=",".join(DEFAULT_IDS))
    ap.add_argument("--lib", default=str(LIB),
                    help="captured ultFx blocks from ult_fx_capture.py")
    ap.add_argument("--phase", default=None,
                    help="which captured phase; default is the last one, "
                         "which is the payload for every multi-phase ult")
    ap.add_argument("--at", type=float, default=0.35,
                    help="t/life at which the set-piece is sampled")
    ap.add_argument("--seed", type=int, default=25064)
    ap.add_argument("--ship", type=int, default=540,
                    help="the resolution that ships today")
    ap.add_argument("--crop", action="store_true",
                    help="600 design px around the caster instead of the arena")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2

    lib = {}
    libp = pathlib.Path(args.lib)
    if libp.exists():
        lib = json.loads(libp.read_text(encoding="utf-8"))
    else:
        print(f"  (no {libp.name} -- falling back to synthetic ultFx blocks, "
              f"which eight relics render BLANK. FX-RUNTIME-BRIEF.md §1.)")

    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    rows = []

    with game(game_path=path) as (page, errors):
        if not page.evaluate("() => !!document.createElement('canvas')"
                             ".getContext('webgl2')"):
            print("! no WebGL2 -- the chain would be off and this sheet would "
                  "not be\n  the picture that ships. Stopping.")
            return 2

        for ident in ids:
            entry = lib.get(ident)
            block, phase = None, None
            if entry and entry.get("phases"):
                phase = args.phase or entry["phases"][-1]
                block = entry["blocks"].get(phase)
                if block is None:
                    print(f"! {ident} has no captured phase {phase!r}; "
                          f"has {entry['phases']}")
                    return 2
            life = LIFE.get(ident, 1.5)
            t = args.at * life

            ship_off = render(page, ident, args.seed, t, life, block,
                              args.ship, 0, False, args.crop)
            ship_on = render(page, ident, args.seed, t, life, block,
                             args.ship, 0, True, args.crop)
            ref_off = render(page, ident, args.seed, t, life, block,
                             1080, 0, False, args.crop)
            ref_on = render(page, ident, args.seed, t, life, block,
                            1080, 0, True, args.crop)

            rows.append({"id": ident, "phase": phase, "life": life, "t": t,
                         "ship_off": ship_off, "ship_on": ship_on,
                         "ref_off": ref_off, "ref_on": ref_on})

        if errors:
            print("! page errors:")
            for e in errors[:10]:
                print("   ", e)
            return 1

    # ---- the k = 1 identity, which is what step 2-before-step-3 rests on ----
    print(f"[k=1 identity]  does the fix change the 1080 picture?")
    all_same = True
    for r in rows:
        same = r["ref_off"]["png"] == r["ref_on"]["png"]
        all_same &= same
        print(f"   {r['id']:<14} {'identical' if same else 'DIFFERS'}")
    if all_same:
        print("   The helper is a no-op at k = 1, so raising --w to 1080 AFTER "
              "this fix\n   changes nothing about the 1080 picture and every "
              "smaller surface\n   converges on it. DELIVERY-QUALITY-BRIEF.md "
              "§1's sequencing holds.")
    else:
        print("   ! NOT a no-op at k = 1. §1's 'the two changes cancel' is "
              "wrong and\n     steps 2 and 3 cannot be sequenced on it.")

    # ---- what it does to the picture that ships ----
    print(f"\n[{args.ship}]  {'caster crop' if args.crop else 'arena'}, "
          f"chain ON, t/life {args.at:.2f}\n")
    print(f"   {'':<23}{'SHIPS TODAY':^26}{'WITH THE FIX':^26}"
          f"{'1080 CONTROL':^17}")
    print(f"   {'relic':<14}{'phase':<9}"
          f"{'halo':>8}{'mean':>9}{'blown':>9}"
          f"{'halo':>8}{'mean':>9}{'blown':>9}"
          f"{'halo':>8}{'mean':>9}")
    for r in rows:
        a, b, c = r["ship_off"], r["ship_on"], r["ref_off"]
        print(f"   {r['id']:<14}{(r['phase'] or '-'):<9}"
              f"{a['halo']:>8.4f}{a['mean']:>9.4f}{a['blown']:>9.4f}"
              f"{b['halo']:>8.4f}{b['mean']:>9.4f}{b['blown']:>9.4f}"
              f"{c['halo']:>8.4f}{c['mean']:>9.4f}")
    print(f"\n   `halo` is the soft skirt -- arena pixels between 0.25 and 0.90"
          f" luma --\n   which is where a blur's width actually lives. THE FIX "
          f"IS RIGHT IF THE MIDDLE\n   BLOCK MOVES TOWARD THE RIGHT ONE. "
          f"`blown` is the core and is expected to sit\n   still; it is in the "
          f"table so that a change which quietly DIMS the set-piece\n   cannot "
          f"pass as one that narrows the glow.")

    # ---- the sheet ----
    from PIL import Image, ImageDraw

    def load(b64):
        return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")

    COL_W, PAD, LBL = 300, 14, 26
    cells = []
    for r in rows:
        for arm in ("ship_off", "ship_on", "ref_off"):
            im = load(r[arm]["png"])
            rc = r[arm]["rect"]
            im = im.crop((rc["x"], rc["y"], rc["x"] + rc["w"], rc["y"] + rc["h"]))
            # Every arm to the same DISPLAY size. A 540 capture upscaled 2x is
            # exactly what shorts_build.py does to it today, so this is not a
            # courtesy -- it is the delivery path.
            h = round(COL_W * im.height / im.width)
            cells.append(im.resize((COL_W, h), Image.LANCZOS))

    ch = max(c.height for c in cells)
    sheet = Image.new("RGB", (COL_W * 3 + PAD * 4,
                              (ch + LBL) * len(rows) + PAD * (len(rows) + 1)
                              + LBL), (10, 8, 14))
    d = ImageDraw.Draw(sheet)
    heads = [f"{args.ship} SHIP (today)", f"{args.ship} + _blur(px)", "1080 (control)"]
    for i, hd in enumerate(heads):
        d.text((PAD + i * (COL_W + PAD) + 4, 6), hd, fill=(210, 200, 225))

    for ri, r in enumerate(rows):
        y = LBL + PAD + ri * (ch + LBL + PAD)
        for ci in range(3):
            sheet.paste(cells[ri * 3 + ci], (PAD + ci * (COL_W + PAD), y))
        d.text((PAD + 4, y + ch + 5),
               f"{r['id']}  {r['phase'] or '-'}  t={r['t']:.2f}/{r['life']:.1f}",
               fill=(170, 160, 185))

    # ---- ONE FILE PER ARM, AT FULL SIZE ----
    #
    # Rick, 2026-08-28: "i cannot judge anything from the sheet. only you can
    # read stuff like that. i need clips and pictures to judge every time."
    #
    # He is right and it is the same mistake CLAUDE.md §4.1 keeps recording
    # from the other side: a contact sheet is an INSTRUMENT'S output. Three
    # 300px columns is a layout for ranking twenty-five things at a glance, and
    # it is useless for judging whether one of them looks better -- the
    # difference being argued about here is a glow a few pixels wide, and the
    # sheet threw those pixels away before he ever saw it.
    #
    # So the sheet stays as the tool's own read-out, and the DELIVERABLE is one
    # full-resolution file per arm, every arm at the same 1080x1920 so flipping
    # between them holds the frame still. Nothing to read, only to look at.
    singles = out_dir_for(args)
    for r in rows:
        for arm, name in (("ship_off", "1-ships-today"),
                          ("ship_on", "2-blur-fix"),
                          ("ref_off", "3-at-1080")):
            im = load(r[arm]["png"])
            if args.crop:
                rc = r[arm]["rect"]
                im = im.crop((rc["x"], rc["y"],
                              rc["x"] + rc["w"], rc["y"] + rc["h"]))
            # EVERY ARM TO THE SAME 1080 WIDE, which is the frame the viewer
            # actually sees. The 540 arms get upscaled here exactly as
            # shorts_build.py upscales them, so this is the delivery path and
            # not a courtesy -- and it is what makes flipping between the files
            # a fair comparison instead of a size illusion.
            im = im.resize((1080, round(1080 * im.height / im.width)),
                           Image.LANCZOS)
            f = singles / f"{r['id']}-{name}{'-crop' if args.crop else ''}.png"
            im.save(f)
            print(f"   {f}")

    tag = "-crop" if args.crop else ""
    out = pathlib.Path(args.out) if args.out else \
        OUT / f"blurscale-spread-{'-'.join(ids)}-{args.ship}{tag}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"\n   wrote {out}")
    print("   LOOK AT IT BEFORE READING THE TABLE. The numbers rank; only the "
          "picture\n   decides, and this sheet is a still -- the gate is a "
          "played clip.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
