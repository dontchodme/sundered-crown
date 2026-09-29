"""The beat gate for the voice rows (brief stage 6: "cast files `ult`; a touch files
nothing"): Lodestone both sides x every foe x 2 seeds, on the base and on the base
with the voice rows, one browser at a time. Per fight: the whole beat list (JSON)
must be identical; on the voice page, count Lodestone's ult beats against its
casts, and the beats filed on a touch's own step (by kind). The director's plan
(cinePlan) for Lodestone side A x every foe, one seed, must be identical too.
CONTROL: the same run on a copy of the voice page whose touch row also files a
beat ({kind:'ult'}) must come back NOT identical and with beats on touch steps."""
import sys, json, pathlib, hashlib
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone")
BASE = S / "links/sc-lodestone-b205.html"
VOICE = S / "stage6-voice/sc-lodestone-voice.html"
CTL = S / "stage6-voice/chk/sc-lodestone-voice-beatctl.html"
v = VOICE.read_text(encoding="utf-8")
A = 'SFX.play("hex-snap");\n'
i = v.index('SFX.play("ult", { w: "lodestone-touch"')
j = v.index(A, i) + len(A)
ctl = v[:j] + '        this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y });\n' + v[j:]
CTL.write_text(ctl, encoding="utf-8", newline="")
JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, ME = "lodestone";
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const out = [];
  for (const fid of foes) for (const side of [0, 1]) for (const sd of seeds){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const L = side ? m.b : m.a, me = side ? 1 : 0;
    let n = 0, onTouch = {}, prevT = 0;
    while (!m.over && n < 170 / DT){
      const nb = m.beats.length, t0 = L.runeTally ? L.runeTally.touches : 0;
      m.step(DT); n++;
      const t1 = L.runeTally ? L.runeTally.touches : 0;
      if (t1 > t0) for (const b of m.beats.slice(nb)) onTouch[b.kind] = (onTouch[b.kind] || 0) + 1;
    }
    const ult = m.beats.filter(b => b.kind === "ult" && b.side === me).length;
    out.push({ fid, side, sd, beats: JSON.stringify(m.beats), nb: m.beats.length, ult,
               casts: L.runeTally.casts, touches: L.runeTally.touches, onTouch });
  }
  const plans = [];
  if (window.cinePlan) for (const fid of foes){
    const p = window.cinePlan(ME, fid, seeds[0]);
    plans.push(JSON.stringify(p.scored || p));
  }
  return { out, plans };
}"""
res = {}
for tag, p in (("base", BASE), ("voice", VOICE), ("ctl", CTL)):
    with game(game_path=p.resolve()) as (page, errors):
        r = page.evaluate(JS, [[102701, 102702]])
        r["errors"] = list(errors)
    res[tag] = r
    print(tag, p.name, hashlib.sha256(p.read_bytes()).hexdigest()[:16], len(r["out"]), "fights", len(r["plans"]), "plans", "errors", len(r["errors"]))
b, vo, c = res["base"]["out"], res["voice"]["out"], res["ctl"]["out"]
same = sum(x["beats"] == y["beats"] for x, y in zip(b, vo))
print(f"beats identical base vs voice: {same}/{len(b)}")
ps = sum(x == y for x, y in zip(res['base']['plans'], res['voice']['plans']))
print(f"director's plan identical base vs voice: {ps}/{len(res['base']['plans'])}")
casts = sum(x["casts"] for x in vo); ult = sum(x["ult"] for x in vo); tch = sum(x["touches"] for x in vo)
ot = {}
for x in vo:
    for k, n in x["onTouch"].items(): ot[k] = ot.get(k, 0) + n
print(f"voice page: Lodestone casts {casts}, its ult beats {ult} (equal: {casts == ult}); touches {tch}; beats filed on a touch's own step, by kind: {ot or 'none'}")
print("  (a beat on a touch's step can be a blow landed on the same step; the probe [6] reads the rune tick itself)")
kinds = {}
for x in vo:
    for bb in json.loads(x["beats"]): kinds[bb["kind"]] = kinds.get(bb["kind"], 0) + 1
print("voice page beats by kind:", kinds)
cs = sum(x["beats"] == y["beats"] for x, y in zip(b, c))
cot = {}
for x in c:
    for k, n in x["onTouch"].items(): cot[k] = cot.get(k, 0) + n
cult = sum(x["ult"] for x in c)
print(f"CONTROL (a beat filed on every touch): beats identical {cs}/{len(b)}; ult beats {cult} vs casts {sum(x['casts'] for x in c)}; on touch steps {cot}",
      "-> fails, as it must" if cs < len(b) and cult != sum(x['casts'] for x in c) else "-> DID NOT FAIL")
ok = same == len(b) and ps == len(res['base']['plans']) and casts == ult and not any(res[t]["errors"] for t in res) and cs < len(b)
print("BEATS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
