#!/usr/bin/env python3
"""WHICH ULTS BLOW OUT, AND BY HOW MUCH — measured, not eyeballed.

    python ult_bloom_probe.py --game ../02-chain/sc-paradox-arc.html
    python ult_bloom_probe.py --game ... --ids paradox,slagheart --frames 9

Rick: "the bloom is still really intense on some of the ults." This turns
"some" into a ranked list, so the animation work can be aimed rather than
swept across all twenty-five.

WHAT IS MEASURED, and why these three numbers:

  blown    fraction of arena pixels over 0.90 luma WITH the chain on. This is
           the thing being complained about — white area with no detail in it.
  gain     blown(on) - blown(off). How much of that white the BLOOM added, as
           against how much the art was already asking for. A relic with high
           blown and near-zero gain is not a bloom problem at all; its own art
           is white, and turning the chain down would not touch it.
  lift     mean luma delta over the arena. The gentler read of the same thing,
           and the one that catches a wide soft wash that never crosses 0.90.

THE SAMPLE IS THE SET-PIECE, NOT A FIGHT. `ultFx` is set directly and only
`u.t` moves, exactly as ult_filmstrip.py does it — same placement, same seed,
same positions. This costs ZERO simulated fights: nothing is stepped. See
CLAUDE.md §6 on what a session's matches actually go on.

ADAPTATION IS PER-FRAME AND SPATIAL, not temporal — the avg chain is built
from this frame's own mip chain every render (SWBPost, `o.adapt`). So one
draw is a complete measurement and no warm-up is needed. If that ever becomes
a running average, this tool needs a warm-up loop and this comment is the
thing that will be stale.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

# Mirrors the engine's map at Match.castUlt. The four absent from it build
# their own ultFx and never reach that path; they are marked in the output.
LIFE = {"dawnbringer":1.6,"widowmaker":1.3,"grudgebearer":1.7,"thornwake":2.4,
        "gravemourn":1.6,"spellbreaker":1.4,"oathwound":1.5,"heartwood":2.2,
        "nightfell":1.4,"axiom":1.5,"ironhail":1.3,"lightkeeper":1.5,
        "farwarden":2.6,"aureole":1.6,"censer":1.6,"emberedge":1.5,
        "slagheart":4.9,"vinesower":5.4,"bulwarden":9.5,"marrowdraw":8.6,
        "paradox":9.5}
FOE, ALT_FOE = "grudgebearer", "dawnbringer"

MEASURE_JS = """([id, foe, seed, t, life, block]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const w = AC.WEAPONS.find(x => x.id === id);
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.26; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.74; m.b.y = A.h * 0.68;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  /* THE CAMERA SHAKE IS A Math.random() IN THE DRAW PATH (Renderer.draw, and
     again in POSTFX.frame for the pair). Left alone it puts the chain-on and
     chain-off arms at two different camera offsets, so the difference between
     them is shake plus bloom and the tool reports the sum as bloom. It showed
     up as spellbreaker moving 0.46 -> 0.42 between two identical runs.
     Zeroed here: this measures light, not camera. */
  m.shake = 0;
  if (block) {
    /* A REAL BLOCK, CAPTURED OUT OF A REAL FIGHT by ult_fx_capture.py. Every
       relic-specific field and `phase` are the engine's own; only the geometry
       is substituted, so each relic is judged on the same frame. Writing those
       fields by hand instead would put a picture on the sheet that the game
       never draws -- CLAUDE.md 4.1, committed on purpose. */
    m.ultFx = Object.assign({}, block, {
      src: "a", tgt: "b",
      x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y,
      aff: m.a.aff, t: t, life: life });
  } else {
    m.ultFx = { w: id, kind: w.ult.kind, src: "a", tgt: "b",
                x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y, hit: true,
                radius: w.ult.radius || 300, aff: m.a.aff, t: t, life: life };
  }

  const r = AC.renderer, cv = document.getElementById('cv');
  const ctx = cv.getContext('2d');
  /* The arena only. The HUD is bright chrome and constant, and averaging it
     in would flatten the difference between the relics being compared. */
  const rect = { x: Math.round(r.pad * r.k), y: Math.round(r.arenaTop * r.k),
                 w: Math.round(r.aw * r.k), h: Math.round(r.ah * r.k) };

  function read(){
    const d = ctx.getImageData(rect.x, rect.y, rect.w, rect.h).data;
    let sum = 0, n90 = 0, n98 = 0;
    const N = d.length / 4;
    for (let i = 0; i < d.length; i += 4){
      /* Rec.709, the same luma the bright-pass uses. */
      const L = (0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2]) / 255;
      sum += L; if (L > 0.90) n90++; if (L > 0.98) n98++;
    }
    return { mean: sum / N, blown: n90 / N, clipped: n98 / N };
  }

  /* THE CASTER'S DISC, which is the thing Rick named: a white ball washed out
     by the light landing on it. The relic body is NOT in the bloom's source
     (roMode 3 is `lighter` only) -- so any lift here is the ULT's glow
     spilling over a body that already sits near 0.89, not the body blooming
     itself. Measuring the whole arena averages that away. */
  /* THE DISC, IN DEVICE PIXELS, and the transform is not one multiply.
     Renderer.draw does setTransform(k,0,0,k,0,0), THEN translate(pad, arenaTop)
     in unscaled units, THEN scale(this.scale). So arena->device is
       px = k * (pad + scale * x)
     and a rect built as `pad*k + x*k` -- which is what the first version of
     this tool used -- lands on empty floor and dutifully reports 0.05 luma for
     a body that is actually at 0.89. Read `r.scale` rather than restating it. */
  const S = r.scale, RR = AC.CONFIG.physics.ballR * S * r.k * 1.25;
  const bx = r.k * (r.pad + S * m.a.x), by = r.k * (r.arenaTop + S * m.a.y);
  const disc = { x: Math.max(0, Math.round(bx - RR)),
                 y: Math.max(0, Math.round(by - RR)),
                 w: Math.round(2*RR), h: Math.round(2*RR) };
  function readDisc(){
    const d = ctx.getImageData(disc.x, disc.y, disc.w, disc.h).data;
    let sum = 0, n98 = 0; const N = d.length / 4;
    for (let i = 0; i < d.length; i += 4){
      const L = (0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2]) / 255;
      sum += L; if (L > 0.98) n98++;
    }
    return { mean: sum / N, clipped: n98 / N };
  }

  /* PIN Math.random FOR THE DRAW. Two sites reach it from inside a frame:
     the camera shake (zeroed above) and Unmaking's flicker at
     `const flick = 0.55 + Math.random() * 0.45`. The flicker left spellbreaker
     moving 0.347 -> 0.354 between identical runs, and -- worse -- gave the
     chain-on and chain-off arms two different pictures, so the +bloom column
     for that relic was flicker, not bloom. Reseeded to the SAME value before
     every draw below, so the pair differs in one variable. Restored after:
     this is a measurement harness, not a change to the game.

     mulberry32, the same generator the sim's seed uses. Nothing is stepped
     here, so no simulation state can see this. */
  const __realRandom = Math.random;
  const __pin = function (seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  const SEED = 0x5EEDF00D;

  const was = AC.POSTFX.on;

  /* IS THERE ANY ULT ART AT ALL? The synthetic block sets `kind` but no
     `phase`, and every phase-driven branch is if/else-if with no fallback --
     so eight relics render an empty frame and the old version of this tool
     ranked those empty frames as though they were measurements. That is the
     §4.1 fault the tool exists to find, living in the tool. Baselined against
     this relic's OWN arena with no ultFx, not against a constant. */
  AC.POSTFX.on = false;
  const keep = r.roMode|0;
  const fx = m.ultFx;
  Math.random = __pin(SEED); m.ultFx = null; AC.__draw(m); const bare = readDisc();
  Math.random = __pin(SEED); m.ultFx = null; r.roMode = 3; r.draw(m);
  let base = 0; { const d = ctx.getImageData(0,0,cv.width,cv.height).data;
                  for (let i=3; i<d.length; i+=4) if (d[i] > 8) base++; }
  Math.random = __pin(SEED); m.ultFx = fx; r.roMode = 3; r.draw(m);
  let lit = 0;  { const d = ctx.getImageData(0,0,cv.width,cv.height).data;
                  for (let i=3; i<d.length; i+=4) if (d[i] > 8) lit++; }
  r.roMode = keep;

  Math.random = __pin(SEED);
  AC.POSTFX.on = true;  AC.__draw(m); const on  = read(),  onD  = readDisc();
  Math.random = __pin(SEED);
  AC.POSTFX.on = false; AC.__draw(m); const off = read(), offD = readDisc();
  AC.POSTFX.on = was;
  Math.random = __realRandom;
  return { on, off, onD, offD, bare, emis: lit - base };
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-paradox-arc.html")
    ap.add_argument("--ids", default=",".join(LIFE) + ",lastlight,twinshade,redflail,foregone")
    ap.add_argument("--seed", type=int, default=31337)
    ap.add_argument("--frames", type=int, default=7)
    ap.add_argument("--json", default="")
    ap.add_argument("--fx", default="../05-reference/post/ultfx-library.json",
                    help="captured ultFx blocks from ult_fx_capture.py. Without "
                         "it the synthetic block is used and eight relics "
                         "render empty frames.")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")
    ids = [i.strip() for i in A.ids.split(",") if i.strip()]
    fxlib = {}
    fxp = (HERE / A.fx).resolve() if A.fx else None
    if fxp and fxp.exists():
        fxlib = json.loads(fxp.read_text(encoding="utf8"))
        print(f"  fx library: {fxp.name}, {len(fxlib)} relics")
    elif A.fx:
        print(f"  ! no fx library at {fxp} -- falling back to the SYNTHETIC "
              f"block, which renders eight ultimates as empty frames.")
    fr = [round(0.06 + 0.82 * (i / max(1, A.frames - 1)) ** 1.5, 3)
          for i in range(A.frames)]

    rows = []
    with game(game_path=g) as (page, errors):
        if not page.evaluate("() => !!(AC.POSTFX && AC.POSTFX.on)"):
            sys.exit("POSTFX is OFF in this runtime -- no WebGL2? "
                     "Every number here would be a measurement of nothing.")
        for rid in ids:
            life = LIFE.get(rid, 1.5)
            foe = ALT_FOE if rid == FOE else FOE
            # One entry per captured PHASE: a latch's `blast` and its `lit`
            # are two different pictures and the worst of them is the one that
            # gets watched. Falls back to a single synthetic pass (None) for a
            # relic the library does not carry.
            entry = fxlib.get(rid)
            variants = ([(ph, entry["blocks"][ph]) for ph in entry["phases"]]
                        if entry else [(None, None)])
            peak, peak_t, emis, peak_ph = None, None, 0, None
            for ph, blk in variants:
              for f in fr:
                s = page.evaluate(MEASURE_JS, [rid, foe, A.seed, f * life, life, blk])
                emis = max(emis, s["emis"])
                # The worst frame is the one that gets watched. Ranked on the
                # DISC, because the complaint is about the ball.
                if peak is None or s["onD"]["mean"] > peak["onD"]["mean"]:
                    peak, peak_t, peak_ph = s, f, ph
            rows.append({"id": rid, "life": life, "guessed": rid not in LIFE,
                         "t": peak_t, "emis": emis, "drew": emis > 500,
                         "phase": peak_ph,
                         "blown": peak["on"]["blown"],
                         "gain": peak["on"]["blown"] - peak["off"]["blown"],
                         "body": peak["onD"]["mean"],
                         "bodyRaw": peak["offD"]["mean"],
                         "bare": peak["bare"]["mean"],
                         "bodyLift": peak["onD"]["mean"] - peak["offD"]["mean"],
                         "bodyClip": peak["onD"]["clipped"],
                         "lift": peak["on"]["mean"] - peak["off"]["mean"]})
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    drew  = [r for r in rows if r["drew"]]
    blank = [r for r in rows if not r["drew"]]
    drew.sort(key=lambda r: -r["bodyLift"])
    print(f"  ULT BLOWOUT -- {g.name}, worst of {A.frames} frames per relic")
    print("  ranked on THE CASTER'S DISC: how far the ult's light pushes a")
    print("  body that the bloom never reads directly.")
    print("")
    print(f"  {'relic':<14}{'phase':<9}{'t/life':>7}{'bare':>7}{'body':>8}"
          f"{'+bloom':>8}{'clip%':>8}{'arena%':>8}")
    for r in drew:
        mark = " *" if r["guessed"] else ""
        print(f"  {r['id']:<14}{(r['phase'] or '-'):<9}{r['t']:>7}"
              f"{r['bare']:>7.3f}{r['body']:>8.3f}{r['bodyLift']:>+8.3f}"
              f"{100*r['bodyClip']:>8.2f}{100*r['blown']:>8.2f}{mark}")
    if blank:
        print("")
        print(f"  NOT MEASURED -- {len(blank)} ults render an EMPTY frame here.")
        print("  NOT a phase problem -- that was the first diagnosis and it was")
        print("  only half right. These ultimates do not draw from `ultFx` at")
        print("  all: their picture lives in MATCH STATE that a frozen match")
        print("  does not have -- m.splitHold for the Split, and the same shape")
        print("  for the Stasis Field, the Ballista window, the Spinstorm and")
        print("  the Retrace's laid wave. drawSplitHold(m) and its dozen")
        print("  siblings are called from draw() beside drawUltOver, not from")
        print("  it. Replaying a captured block cannot reach them; only")
        print("  stepping a real fight to the moment can. These are not low")
        print("  scores, they are no measurement at all:")
        for r in blank:
            print(f"    {r['id']:<14}{r['emis']:>8,} emissive px above the empty arena")
    if any(r["guessed"] for r in rows):
        print("")
        print("  * life guessed at 1.5s -- builds its own ultFx, never reaches")
        print("    the generic cast path")

    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(rows, indent=2), encoding="utf8")
        print(f"  -> {A.json}")


if __name__ == "__main__":
    main()
