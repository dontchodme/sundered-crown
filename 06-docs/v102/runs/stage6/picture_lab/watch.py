"""ONE FIGHT WATCHED: a whole Lodestone fight on the final bytes, drawn the way the app draws it (chain on, the
scrunch armed as the app arms it, 540x960, Chromium 151), every 4th step (30 fps) from the first step through the
kill and 2.5s of verdict. Writes watch/f%05d.jpg, an mp4 (ffmpeg via clip_spread.resolve_ffmpeg), contact grids of
every 8th frame (4 fps, 8x5 a grid) for looking at, and a per-frame log (t, window lit, lodeFade, touches, hex, over,
stop). Throws are collected by scpage. usage: watch.py foe seed side tag. SCRATCH."""
import sys, base64, pathlib, json, subprocess
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from clip_spread import resolve_ffmpeg
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
PAGE = HERE / "ld-final.html"
FOE, SEED, SIDE, TAG = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
OUT = HERE / "watch" / TAG
OUT.mkdir(parents=True, exist_ok=True)
INIT = r"""([foe, seed, side]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
  m.scrunchAuto = AC.CONFIG.scrunch.on;
  window.__W = { m, step: 0, overAt: -1, done: false };
  return [m.a.w.id, m.b.w.id];
}"""
CHUNK = r"""(n) => {
  const W = window.__W, m = W.m, DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const me = m.a.w.id === "lodestone" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const out = [];
  while (out.length < n && !W.done){
    for (let i = 0; i < 4; i++){ m.step(DT); W.step++; if (m.over && W.overAt < 0) W.overAt = W.step; }
    AC.__draw(m);
    out.push({ jpg: cv.toDataURL("image/jpeg", 0.86), t: +m.t.toFixed(3), lit: !!me.ultRunes, fade: +(me.lodeFade || 0).toFixed(3),
               touches: me.runeTally ? me.runeTally.touches : 0, hex: th.stacks("hex"), over: m.over, stop: m.hitStop > 0,
               fx: (me.lodeFx || []).length, inset: +(m.inset || 0).toFixed(1), hpMe: Math.round(me.hp), hpTh: Math.round(th.hp) });
    if (W.overAt >= 0 && (W.step - W.overAt) * DT > 2.5) W.done = true;
    if (W.step > 200 / DT) W.done = true;
  }
  return { out, done: W.done, winner: m.over ? (m.winner && m.winner.w ? m.winner.w.id : String(m.winner)) : null };
}"""
log = []
with game(game_path=PAGE) as (page, errors):
    ids = page.evaluate(INIT, [FOE, SEED, SIDE])
    k = 0
    while True:
        r = page.evaluate(CHUNK, 60)
        for fr in r["out"]:
            (OUT / f"f{k:05d}.jpg").write_bytes(base64.b64decode(fr.pop("jpg").split(",", 1)[1]))
            fr["i"] = k; log.append(fr); k += 1
        if r["done"]:
            winner = r["winner"]; break
    errs = list(errors)
(OUT / "log.json").write_text(json.dumps({"ids": ids, "seed": SEED, "winner": winner, "errors": errs, "frames": log}))
ff = resolve_ffmpeg()
mp4 = HERE / "watch" / f"{TAG}.mp4"
subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", "30", "-i", str(OUT / "f%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", str(mp4)], check=True)
F = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
sel = log[::8]
per = 40
for g in range(0, len(sel), per):
    part = sel[g:g + per]
    tw, th_ = 180, 320
    o = Image.new("RGB", (8 * tw, 5 * (th_ + 16)), (12, 10, 16))
    for j, fr in enumerate(part):
        im = Image.open(OUT / f"f{fr['i']:05d}.jpg").convert("RGB").resize((tw, th_), Image.LANCZOS)
        x, y = (j % 8) * tw, (j // 8) * (th_ + 16)
        o.paste(im, (x, y + 16))
        ImageDraw.Draw(o).text((x + 2, y), f"{fr['t']:.2f}s{' LIT' if fr['lit'] else ''}{' f%.2f' % fr['fade'] if fr['fade'] and not fr['lit'] else ''} T{fr['touches']} H{fr['hex']}{' OVER' if fr['over'] else ''}",
                                   fill=(230, 220, 200), font=F)
    o.save(HERE / "watch" / f"{TAG}_grid{g // per:02d}.png")
lit = sum(1 for f in log if f["lit"])
print(f"{TAG}: {ids} seed {SEED} winner {winner}; {len(log)} frames ({len(log) / 30:.1f}s at 30 fps), lit {lit}, "
      f"touches {log[-1]['touches']}, errors {len(errs)}; mp4 {mp4.name}; grids {(len(sel) + per - 1) // per}")
