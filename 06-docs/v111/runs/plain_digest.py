"""A control on the probe: the probe's own 444 fights (both sides, every other relic, 6 seeds from
111001 step 13) played with NO hooks at all, and the digest compared with a probe json's.
Identical => the probe's hooks do not move a fight on that link.
    python plain_digest.py <link> <probe json>"""
import json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
JS = r"""(seeds) => { const DT = AC.CONFIG.physics.dt, out = [];
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "spellbreaker");
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "spellbreaker", sd) : new AC.Match("spellbreaker", fid, sd);
    const me = side ? m.b : m.a; let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    out.push([side, fid, sd, m.winner ? (m.winner === me ? 1 : 0) : -1, steps]); }
  return out; }"""
link, pj = sys.argv[1], sys.argv[2]
with game(game_path=pathlib.Path(link).resolve()) as (page, errors):
    d = page.evaluate(JS, [111001 + 13 * i for i in range(6)])
    assert not errors, errors
p = json.load(open(pj))["digest"]
same = sum(1 for a, b in zip(d, p) if a == b)
w = sum(1 for x in d if x[3] == 1) / max(1, sum(1 for x in d if x[3] >= 0))
print(f"{pathlib.Path(link).name}: no hooks {len(d)} fights, win {100*w:.1f}%; the probe's digest ({pathlib.Path(pj).name}) "
      f"{same}/{len(d)} fights identical -> " + ("THE PROBE MOVES NO FIGHT" if same == len(d) == len(p) else "THE PROBE MOVES FIGHTS"))
sys.exit(0 if same == len(d) == len(p) else 1)
