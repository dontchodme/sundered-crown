#!/usr/bin/env python3
"""THE CROWN CUP — draw it, seed it by rule, film every match in order, file it.

    python cup.py draw     --game ../02-chain/<frozen tip>.html --seed 20261001
    python cup.py seeds    --game ../02-chain/<frozen tip>.html
    python cup.py status
    python cup.py film     --game ../02-chain/<frozen tip>.html [--only A1] [--dry-run]
    python cup.py schedule
    python cup.py cupjson  A3                     # the verdict card's CONFIG.cup blob (v118)

One ledger, `07-shorts/cup1/ledger.json`, is the whole tournament: the draw,
every fixture, its seed and `k`, its result, its file. Every command reads it
and writes it back; a run that dies is resumed by running the same command
again. Plan: 06-docs/v115/CROWN-CUP-PLAN-v115.md.

THE RULE (plan §3). A match's fight is not chosen, it is computed:

    seed(k) = sha256("<cup>/<fixture>/<side1>/<side2>/<k>")[:8] as an int, k = 0, 1, ...

and the fight is the first k that ENDS IN A KILL. A timeout is a draw and the
tournament has no draws; k is written down. This replaces pick_fight.py's
rank-by-closeness, which is the right tool for a one-off short and the wrong
one for a tournament: ranking candidate seeds by drama is choosing the winner
with a preference.

THE FATAL-CUT FILTER IS DELIBERATELY NOT APPLIED, AND IT WAS MEASURED OUT. The
plan (v115 §3) had the rule also require a fatal cut in the director's plan,
on the grounds that it does not look at the winner. It does not need to: on
sc-tendril-fx at Chromium 141, 240 seeds a pairing, the director finds a fatal
cut in only 6-34% of kills, and REQUIRING one moves the win rate by up to 26
points (Gloamwire v Paradox 84% of all kills -> 58% of fatal-cut kills;
Spellbreaker v Censer 40% -> 17%; Twinshade v Vinesower 58% -> 82%). A kill
the director can film is a kill of a particular kind, and which relic
delivers that kind is not independent of which relic it is. So the only test
is "ended in a kill"; whether the director found the finale is RECORDED per
fixture (`result.fatal`) and a finale without a cut is filmed at plain speed,
which is what every shipped ultimate already gets (CLAUDE.md, cineScore).

DETERMINISM IS PER RUNTIME (docs/RUNTIME-DRIFT.md). The ledger records the
build's sha256, the machine and the Chromium that computed the seeds, and
`film` refuses to run against a different build or machine without --force.
A tournament computed in one place and filmed in another is two tournaments.

WHY THE FILMING IS HERE AND NOT IN THE APP. app/main.js renders one short by
spawning shorts_build.py with a folder to itself (its comment explains the
4,747 decode errors that a shared `_clip_frames` produced). This does the same
thing 65 times in a row, from the same shorts_build.py, with the same
one-folder-per-job rule, and prints the same `[progress]` lines -- so the app
can spawn THIS instead of shorts_build and watch it the same way, and a person
at a terminal gets the same run. Nothing about a render is reimplemented.

THE SHAPE (plan §1). N relics -> G = N // 3 groups of 3; G must be a power of
two (16 for 49); N - 3G may be 0 or 1, and a 1 is the play-in: the 49th relic
drawn plays the 48th for the last slot in the last group. Group pattern
P1 v P2, P2 v P3, P3 v P1 -- every relic is side 1 once and side 2 once.
Knockout: group winners A v B, C v D, ...; the lower draw number is side 1.
3 points a win; a three-way tie is broken on HP remaining across the group's
wins, then on draw number. The ledger says which rule decided every group.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import pathlib
import platform
import random
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DEFAULT_DIR = REPO / "07-shorts" / "cup1"

ROUND_FOLDER = {
    "play-in": "01-play-in", "group": "02-groups", "r16": "03-round-of-16",
    "qf": "04-quarter-finals", "sf": "05-semi-finals", "third": "06-third-place",
    "final": "07-final",
}
ROUND_LABEL = {
    "play-in": "PLAY-IN", "r16": "ROUND OF 16", "qf": "QUARTER-FINAL",
    "sf": "SEMI-FINAL", "third": "THIRD PLACE", "final": "THE FINAL",
}
CROWN_LINE = "ONLY ONE KEEPS THE CROWN"


# ------------------------------------------------------------------ the ledger

def load(d: pathlib.Path) -> dict:
    p = d / "ledger.json"
    if not p.exists():
        sys.exit(f"! no ledger at {p} -- run `cup.py draw` first")
    return json.loads(p.read_text(encoding="utf-8"))


def save(d: pathlib.Path, L: dict) -> None:
    d.mkdir(parents=True, exist_ok=True)
    tmp = d / "ledger.json.tmp"
    tmp.write_text(json.dumps(L, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(d / "ledger.json")


def sha256_of(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------ the rule

def fight_seed(cup: str, fixture: str, a: str, b: str, k: int) -> int:
    h = hashlib.sha256(f"{cup}/{fixture}/{a}/{b}/{k}".encode()).hexdigest()
    return int(h[:8], 16) & 0x7FFFFFFF


# ------------------------------------------------------------------ the draw

def make_draw(roster: dict, draw_seed: int, tries: int = 200000):
    """Groups of three with no school or weapon type repeated inside a group,
    plus the challenger. Deterministic from draw_seed. Returns
    (groups, challenger, draw_no, attempts) where draw_no is each relic's
    position in the shuffle, 1-based -- the knockout's side rule."""
    ids = sorted(roster)
    n = len(ids)
    G = n // 3
    if G & (G - 1) or G == 0:
        sys.exit(f"! {n} relics make {G} groups of 3, and {G} is not a power of two "
                 "-- the knockout needs 4, 8, 16 or 32 group winners")
    extra = n - 3 * G
    if extra not in (0, 1):
        sys.exit(f"! {n} relics leave {extra} over after {G} groups of 3; "
                 "the shape allows 0 or 1 (the play-in)")
    rng = random.Random(draw_seed)

    def legal(rid, grp):
        return all(roster[rid]["school"] != roster[o]["school"] and
                   roster[rid]["type"] != roster[o]["type"] for o in grp)

    order = list(ids)
    for attempt in range(1, tries + 1):
        rng.shuffle(order)
        groups = [[] for _ in range(G)]
        ok = True
        for rid in order[:3 * G]:
            for g in groups:
                if len(g) < 3 and legal(rid, g):
                    g.append(rid)
                    break
            else:
                ok = False
                break
        if not ok:
            continue
        chal = order[3 * G] if extra else None
        # the challenger plays for the LAST group's third slot, so it has to be
        # legal there too -- against the two that are not the slot's holder
        if chal and not legal(chal, groups[-1][:2]):
            continue
        draw_no = {rid: i + 1 for i, rid in enumerate(order)}
        return groups, chal, draw_no, attempt
    sys.exit(f"! no legal draw in {tries} shuffles of seed {draw_seed}")


def build_fixtures(groups, chal, draw_no):
    """Every fixture of the tournament, in POSTING ORDER, with sides filled in
    where they are known now and left as `{from: <fixture>, take: winner|loser}`
    where they depend on a result. `resolve()` fills those in as results land."""
    G = len(groups)
    F = []
    last = chr(65 + G - 1)
    if chal:
        # the 49th drawn v the 48th drawn (the last slot filled), for that slot
        holder = groups[-1][2]
        F.append(dict(id="PI", round="play-in", a=chal, b=holder, label="PLAY-IN",
                      sub=f"{G * 3 + 1} RELICS. {G * 3} PLACES."))
    for gi, g in enumerate(groups):
        name = chr(65 + gi)
        p1, p2, p3 = g
        slot3 = {"from": "PI", "take": "winner"} if (chal and name == last) else p3
        pat = [(p1, p2), (p2, slot3), (slot3, p1)]
        for m, (x, y) in enumerate(pat, 1):
            F.append(dict(id=f"{name}{m}", round="group", group=name, match=m,
                          a=x, b=y, label=f"GROUP {name} \u00b7 MATCH {m} OF 3"))
    # knockout: winners of A v B, C v D ... in group order
    names = [chr(65 + i) for i in range(G)]
    prev = [{"from": f"group:{n}", "take": "winner"} for n in names]
    rnd_seq = {16: ["r16", "qf", "sf"], 8: ["qf", "sf"], 4: ["sf"], 2: []}[G]
    counter = {}
    for rnd in rnd_seq:
        cur = []
        for i in range(0, len(prev), 2):
            counter[rnd] = counter.get(rnd, 0) + 1
            fid = f"{rnd.upper()}-{counter[rnd]}"
            F.append(dict(id=fid, round=rnd, a=prev[i], b=prev[i + 1],
                          label=f"{ROUND_LABEL[rnd]} {counter[rnd]}"))
            cur.append({"from": fid, "take": "winner"})
        prev = cur
    if G == 2:
        sfs = ["group:A", "group:B"]
        F.append(dict(id="F", round="final", a={"from": sfs[0], "take": "winner"},
                      b={"from": sfs[1], "take": "winner"}, label="THE FINAL"))
    else:
        semis = [f"SF-{i}" for i in (1, 2)]
        F.append(dict(id="3P", round="third", a={"from": semis[0], "take": "loser"},
                      b={"from": semis[1], "take": "loser"}, label="THIRD PLACE"))
        F.append(dict(id="F", round="final", a={"from": semis[0], "take": "winner"},
                      b={"from": semis[1], "take": "winner"}, label="THE FINAL"))
    for i, f in enumerate(F, 1):
        f["order"] = i
    return F


# ------------------------------------------------------------------ standings

def standings(L: dict, group: str):
    """Rows sorted by the plan's rule. Each row: id, w, l, pts, hp, draw_no.
    Returns (rows, decided_by) where decided_by is None until all three matches
    are in, else 'wins' | 'hp' | 'draw number'."""
    ids = list(L["groups"][group])
    # the play-in winner stands in the last group's third slot; until the
    # play-in is in, that slot is empty
    if L.get("challenger") and group == sorted(L["groups"])[-1]:
        ids[2] = resolve_side(L, {"from": "PI", "take": "winner"})
    rows = {rid: dict(id=rid, w=0, l=0, pts=0, hp=0, draw_no=L["draw_no"].get(rid, 999))
            for rid in ids if rid}
    played = 0
    for f in L["fixtures"]:
        if f.get("group") != group or not f.get("result"):
            continue
        played += 1
        r = f["result"]
        if r["winner"] not in rows or r["loser"] not in rows:
            sys.exit(f"! ledger inconsistent: {f['id']} has a result between relics not in "
                     f"group {group} -- a redo that did not clear downstream? "
                     "run `cup.py seeds --redo`")
        rows[r["winner"]]["w"] += 1
        rows[r["winner"]]["pts"] += 3
        rows[r["winner"]]["hp"] += r["hp"]
        rows[r["loser"]]["l"] += 1
    out = sorted(rows.values(), key=lambda r: (-r["pts"], -r["hp"], r["draw_no"]))
    decided = None
    if played == 3 and len(out) == 3:
        if out[0]["pts"] > out[1]["pts"]:
            decided = "wins"
        elif out[0]["hp"] > out[1]["hp"]:
            decided = "hp"
        else:
            decided = "draw number"
    return out, decided


def fixture_by_id(L, fid):
    for f in L["fixtures"]:
        if f["id"] == fid:
            return f
    return None


def resolve_side(L, side):
    """A side is a relic id, or a dependency on a result not yet in (None)."""
    if not isinstance(side, dict):
        return side
    src, take = side["from"], side["take"]
    if src.startswith("group:"):
        rows, decided = standings(L, src[6:])
        return rows[0]["id"] if decided else None
    f = fixture_by_id(L, src)
    if not f or not f.get("result"):
        return None
    return f["result"][take]


def sides(L, f):
    """(a, b) for a fixture, with the knockout side rule applied: in the
    knockout the lower draw number is side 1 whatever the bracket said."""
    a, b = resolve_side(L, f["a"]), resolve_side(L, f["b"])
    if a and b and f["round"] not in ("group", "play-in"):
        if L["draw_no"][b] < L["draw_no"][a]:
            a, b = b, a
    return a, b


# ------------------------------------------------------------------ browser

SIM_JS = r"""([a, b, seed]) => {
  let s;
  try { s = AC.simulate(a, b, seed); } catch (e) { return { err: String(e) }; }
  if (!s.winner) return { seed, reason: 'draw', kill: false, fatal: false };
  let fatal = false, cuts = 0;
  if (s.reason !== 'timeout') {
    try { const p = window.cinePlan(a, b, seed);
          if (p && !p.err) { cuts = (p.cuts || []).length;
                             fatal = !!(p.cuts || []).find(c => c.fatal); } }
    catch (e) { fatal = false; }
  }
  const names = Object.fromEntries(AC.WEAPONS.map(w => [w.name, w.id]));
  return { seed, winnerName: s.winner, winner: names[s.winner] || null, hp: s.hp,
           dur: +s.duration.toFixed(2), reason: s.reason, cuts,
           kill: s.reason !== 'timeout', fatal, clanks: s.clanks };
}"""

ROSTER_JS = r"""() => AC.WEAPONS.map(w => ({ id: w.id, name: w.name, school: w.aff, type: w.shape }))"""


def open_game(spec):
    sys.path.insert(0, str(HERE))
    from scpage import game, resolve_game   # noqa: E402
    return game, resolve_game(spec)


def runtime_of(page):
    ua = page.evaluate("() => navigator.userAgent")
    import re
    m = re.search(r"Chrome/([\d.]+)", ua)
    return m.group(1) if m else ua


def machine_id():
    return f"{platform.node()} / {platform.system()} {platform.release()}"


# ------------------------------------------------------------------ commands

def cmd_draw(A):
    d = pathlib.Path(A.dir)
    if (d / "ledger.json").exists() and not A.force:
        sys.exit(f"! {d / 'ledger.json'} exists. A draw is a commitment; --force to redo it")
    game, gpath = open_game(A.game)
    with game(game_path=gpath) as (page, errors):
        weapons = page.evaluate(ROSTER_JS)
        chromium = runtime_of(page)
    if errors:
        sys.exit(f"! page errors: {errors[:3]}")
    if A.field:
        weapons = weapons[:A.field]
    roster = {w["id"]: {"name": w["name"], "school": w["school"], "type": w["type"]}
              for w in weapons}
    groups, chal, draw_no, attempts = make_draw(roster, A.seed)
    L = dict(
        cup=A.cup, created=dt.datetime.now().isoformat(timespec="seconds"),
        draw_seed=A.seed, draw_attempts=attempts,
        build=dict(path=str(gpath.relative_to(REPO)) if gpath.is_relative_to(REPO) else str(gpath),
                   sha256=sha256_of(gpath)),
        machine=machine_id(), chromium=chromium,
        roster=roster, draw_no=draw_no, groups={chr(65 + i): g for i, g in enumerate(groups)},
        challenger=chal, fixtures=build_fixtures(groups, chal, draw_no), cursor=0,
    )
    save(d, L)
    print(f"  {len(roster)} relics - {len(groups)} groups of 3"
          f"{' - play-in' if chal else ''} - {len(L['fixtures'])} fixtures")
    print(f"  draw seed {A.seed} (legal on shuffle {attempts}) - build {L['build']['sha256'][:12]}"
          f" - {L['machine']} - Chromium {chromium}")
    for name, g in L["groups"].items():
        print(f"  {name}  " + "  -  ".join(f"{roster[r]['name']} ({roster[r]['school']} {roster[r]['type']})" for r in g))
    if chal:
        print(f"  challenger: {roster[chal]['name']} v {roster[groups[-1][2]]['name']} for the last slot in group {chr(64 + len(groups))}")
    print(f"\n  ledger: {d / 'ledger.json'}")
    print("  PUBLISH THE DRAW SEED, THE RULE AND THE BUILD HASH BEFORE `cup.py seeds`.")
    return 0


def check_runtime(L, gpath, page, force):
    problems = []
    h = sha256_of(gpath)
    if h != L["build"]["sha256"]:
        problems.append(f"build differs: ledger {L['build']['sha256'][:12]}, this file {h[:12]}")
    if machine_id() != L["machine"]:
        problems.append(f"machine differs: ledger '{L['machine']}', this is '{machine_id()}'")
    if page is not None and runtime_of(page) != L["chromium"]:
        problems.append(f"Chromium differs: ledger {L['chromium']}, this is {runtime_of(page)}")
    if problems and not force:
        sys.exit("! not the tournament's runtime (docs/RUNTIME-DRIFT.md):\n    "
                 + "\n    ".join(problems) + "\n  --force to override; the ledger will say so.")
    return problems


def cmd_seeds(A):
    d = pathlib.Path(A.dir)
    L = load(d)
    game, gpath = open_game(A.game)
    done = 0
    with game(game_path=gpath) as (page, errors):
        overrides = check_runtime(L, gpath, page, A.force)
        if overrides:
            L.setdefault("runtime_overrides", []).append(
                dict(at=dt.datetime.now().isoformat(timespec="seconds"), command="seeds",
                     problems=overrides))
        # A REDO CLEARS EVERYTHING DOWNSTREAM. A result feeds the fixtures after
        # it (group standings, the knockout's sides), so recomputing one fixture
        # and keeping the rest would leave results that refer to relics no
        # longer in that group. Filmed files for cleared fixtures are stale on
        # disk and are said so; they are not deleted from here.
        if A.redo:
            start = next((f["order"] for f in L["fixtures"] if f["id"] == A.only), 1) if A.only else 1
            stale = []
            for f in L["fixtures"]:
                if f["order"] >= start and f.get("result"):
                    if f.get("file"):
                        stale.append(f["file"])
                    for key in ("result", "side1", "side2", "seed", "k", "file", "band", "card",
                                "delivery", "filmed", "decides_group", "film_error"):
                        f.pop(key, None)
            if stale:
                print(f"  !! {len(stale)} filmed files are now STALE and should be deleted "
                      f"before `cup.py film`:")
                for x in stale:
                    print(f"     {x}")
            save(d, L)
        for f in L["fixtures"]:
            if f.get("result"):
                continue
            if A.only and f["id"] != A.only and not A.redo:
                continue
            a, b = sides(L, f)
            if not (a and b):
                print(f"  {f['id']:<6} waits on a result")
                continue
            f["side1"], f["side2"] = a, b
            for k in range(0, A.max_k):
                seed = fight_seed(L["cup"], f["id"], a, b, k)
                r = page.evaluate(SIM_JS, [a, b, seed])
                if r.get("err"):
                    sys.exit(f"! {f['id']}: {r['err']}")
                if r["kill"]:
                    break
                print(f"  {f['id']:<6} k={k} seed {seed}: timeout -- next k")
            else:
                sys.exit(f"! {f['id']}: no usable fight in {A.max_k} values of k")
            loser = b if r["winner"] == a else a
            f["seed"], f["k"] = seed, k
            f["result"] = dict(winner=r["winner"], loser=loser, hp=r["hp"], dur=r["dur"],
                               reason=r["reason"], cuts=r["cuts"], fatal=r["fatal"],
                               clanks=r["clanks"])
            done += 1
            n = L["roster"]
            print(f"  {f['id']:<6} {n[a]['name']:>13} v {n[b]['name']:<13} seed {seed:<11} k={k} "
                  f"-> {n[r['winner']]['name']} by {r['hp']}hp in {r['dur']:.1f}s"
                  f"{'' if r['fatal'] else '  (no director cut on the kill)'}")
            if f["round"] == "group":
                rows, decided = standings(L, f["group"])
                if decided:
                    f["decides_group"] = decided
                    print(f"         group {f['group']} -> {n[rows[0]['id']]['name']} "
                          f"(on {decided})")
            save(d, L)
        if errors:
            print(f"  !! page errors: {errors[:3]}")
    print(f"\n  {done} fixtures seeded; {sum(1 for f in L['fixtures'] if f.get('result'))}"
          f"/{len(L['fixtures'])} have results")
    return 0


# --- the copy on the band. Computed from the ledger, never typed; the main
# line is the round, the sub-line what the fight decides (plan §5.1). A
# knockout sub-line names the next opponent only when that opponent's own
# fixture POSTS EARLIER, so a band never spoils a result the viewer has not
# seen. All of it is Rick's to veto.

def band_lines(L, f):
    n = L["roster"]
    a, b = f.get("side1"), f.get("side2")
    main = f["label"]
    if f["round"] == "play-in":
        return main, f["sub"]
    if f["round"] == "group":
        g, m = f["group"], f["match"]
        if m == 1:
            return main, CROWN_LINE
        rows, _ = standings_before(L, f)
        pts = {r["id"]: r["pts"] for r in rows}
        if m == 2:
            # the relic playing its second match already lost its first, or won it
            second = fixture_by_id(L, f"{g}1")["side2"]   # P2: m1 P1vP2, m2 P2vP3
            if pts[second] == 0:
                return main, f"LOSE AND {n[second]['name'].upper()} IS OUT"
            return main, f"WIN AND {n[second]['name'].upper()} TAKES THE GROUP"
        # match 3
        top = rows[0]
        if top["pts"] == 6:
            return main, f"GROUP DECIDED \u00b7 {n[top['id']]['name'].upper()} IS THROUGH"
        if pts[a] == 3 and pts[b] == 3:
            return main, "WINNER TAKES THE GROUP"
        # 3 v 0: the 0 needs a win to force a three-way tie on HP
        return main, "WIN OR GO HOME"
    # knockout
    nxt = next_fixture(L, f)
    if f["round"] == "final":
        return main, CROWN_LINE
    if f["round"] == "third":
        return main, "THE LAST FIGHT BEFORE THE FINAL"
    if nxt:
        other = [s for s in (nxt["a"], nxt["b"])
                 if isinstance(s, dict) and s["from"] != f["id"]]
        if other:
            src = fixture_by_id(L, other[0]["from"])
            if src and src["order"] < f["order"] and src.get("result"):
                return main, f"WINNER MEETS {n[src['result']['winner']]['name'].upper()}"
        return main, {"r16": "WINNER INTO THE QUARTER-FINALS",
                      "qf": "WINNER INTO THE SEMI-FINALS",
                      "sf": "ONE FIGHT FROM THE FINAL"}[f["round"]]
    return main, CROWN_LINE


def standings_before(L, f):
    """Standings as they stood BEFORE fixture f -- the band is read before the
    fight, so it must not know the result."""
    saved = f.get("result")
    f["result"] = None
    try:
        return standings(L, f["group"])
    finally:
        f["result"] = saved


def next_fixture(L, f):
    for g in L["fixtures"]:
        for s in (g["a"], g["b"]):
            if isinstance(s, dict) and s["from"] == f["id"] and s["take"] == "winner":
                return g
    return None


# --- the verdict card (v118, Claude Code; plan §5.3 and §6's `cupjson`). The CONFIG.cup blob
# for one fixture, built from the ledger AS THE VIEWER OF THAT FIXTURE HAS SEEN IT: every result
# posted after it is hidden first, so a card never counts a match that has not gone up -- the
# band's no-spoiler rule, applied to the result side. Every string on the card is made here;
# the renderer (cupcard_build.py's _panelCup) draws the blob and decides nothing.

CARD_VERSION = 1


@contextlib.contextmanager
def posted_through(L, f):
    """The ledger with every result that posts AFTER f hidden, for the length of a with."""
    hidden = [(g, g["result"]) for g in L["fixtures"]
              if g["order"] > f["order"] and g.get("result") is not None]
    for g, _ in hidden:
        g["result"] = None
    try:
        yield
    finally:
        for g, r in hidden:
            g["result"] = r


def post_day(L, f):
    """The posting day of a fixture -- write_schedule's own arithmetic."""
    return (f["order"] - 1) // L.get("per_day", 2) + 1


def fixture_short(fid):
    """How the card names a fixture: F3 and QF 2, as the sketch does; the final by its name."""
    return "THE FINAL" if fid == "F" else fid.replace("-", " ")


def card_next(L, f):
    """'next: v VESPER · QF 2' -- the opponent named only when it is already known to the
    viewer: drawn into that slot, or the winner of a fixture that posted before this one."""
    n = L["roster"]
    nxt = next_fixture(L, f)
    if not nxt:
        return ""
    where = fixture_short(nxt["id"])
    for s in (nxt["a"], nxt["b"]):
        if not isinstance(s, dict):
            return f"next: v {n[s]['name'].upper()} · {where}"
        if s["from"] == f["id"]:
            continue
        src = fixture_by_id(L, s["from"])
        if src and src["order"] < f["order"] and src.get("result"):
            return f"next: v {n[src['result'][s['take']]]['name'].upper()} · {where}"
    return f"next: {where}"


def relics_left(L, f):
    """Relics still in it for the crown once f has posted."""
    if f["round"] == "play-in":
        return len(L["roster"]) - 1
    out = sum(1 for g in L["fixtures"] if g["round"] in ("r16", "qf", "sf", "final")
              and g["order"] <= f["order"] and g.get("result"))
    return len(L["groups"]) - out


def card_blob(L, f):
    r = f.get("result")
    if not r:
        sys.exit(f"! {f['id']} has no result -- `cup.py seeds` first; the card shows the result")
    n = L["roster"]
    blob = dict(v=CARD_VERSION, fixture=f["id"], winner=r["winner"], hp=r["hp"])
    with posted_through(L, f):
        if f["round"] == "group":
            g = f["group"]
            rows, decided = standings(L, g)
            left = sorted((x for x in L["fixtures"] if x.get("group") == g
                           and x["order"] > f["order"]), key=lambda x: x["order"])
            top = n[rows[0]["id"]]["name"].upper()
            if decided == "hp":
                footer = f"{top} IS THROUGH ON HP REMAINING"
            elif decided == "draw number":
                footer = f"{top} IS THROUGH ON DRAW NUMBER"
            elif decided or rows[0]["w"] == 2:
                # two wins is six points, and nobody else in a group of three can reach six
                footer = f"GROUP DECIDED · {top} IS THROUGH"
            else:
                gap = post_day(L, left[0]) - post_day(L, f)
                when = {0: "LATER TODAY", 1: "TOMORROW"}.get(gap, f"ON DAY {post_day(L, left[0])}")
                k = len(left)
                footer = f"{k} MATCH{'' if k == 1 else 'ES'} LEFT · {left[0]['id']} {when}"
            blob.update(kind="group", title=f"GROUP {g}", cols=["W", "L", "HP"], footer=footer,
                        rows=[dict(id=x["id"], name=n[x["id"]]["name"], w=str(x["w"]),
                                   l=str(x["l"]), hp=str(x["hp"]) if x["hp"] else "—",
                                   mark=x["id"] == r["winner"]) for x in rows])
            return blob
        if not L.get("name"):
            sys.exit("! the ledger has no tournament name, and a knockout card prints it -- "
                     "`cup.py schedule --name \"...\"` first")
        left = relics_left(L, f)
        if f["round"] == "final":
            verdict, nxt = "keeps the crown", f"over {n[r['loser']]['name'].upper()}"
        elif f["round"] == "third":
            verdict, nxt = "third place", f"over {n[r['loser']]['name'].upper()}"
        else:
            verdict, nxt = "through", card_next(L, f)
        blob.update(kind="knockout", title=ROUND_LABEL[f["round"]],
                    name=n[r["winner"]]["name"].upper(), verdict=verdict, next=nxt,
                    footer=f"{L['name'].lower()} · {left} relic{'' if left == 1 else 's'} left")
    return blob


def card_line(blob):
    """The card in one log line. cp1252-safe: the app reads cup.py through a cp1252 pipe."""
    if blob["kind"] == "group":
        rows = " / ".join(f"{x['name']} {x['w']}-{x['l']} {x['hp']}{' *' if x['mark'] else ''}"
                          for x in blob["rows"])
        return f"{blob['title']}: {rows} · {blob['footer']}"
    return (f"{blob['title']}: {blob['name']} {blob['verdict']}"
            + (f" · {blob['next']}" if blob["next"] else "") + f" · {blob['footer']}")


def cmd_cupjson(A):
    L = load(pathlib.Path(A.dir))
    f = fixture_by_id(L, A.fixture)
    if not f:
        sys.exit(f"! no fixture {A.fixture!r}")
    # ASCII on purpose: on Windows a console or a pipe encodes stdout as cp1252, so a blob
    # redirected to a file would not be UTF-8. Escaped, it reads the same everywhere.
    print(json.dumps(card_blob(L, f), indent=1))
    return 0


def file_for(L, f, d: pathlib.Path):
    n = L["roster"]
    a, b = f.get("side1"), f.get("side2")
    stem = f"{f['order']:02d} - {f['id']} - {n[a]['name']} vs {n[b]['name']}"
    sub = ROUND_FOLDER[f["round"]]
    folder = d / sub / (f["group"] if f["round"] == "group" else "") / stem
    return folder / f"{stem}.mp4"


def caption(L, f):
    n = L["roster"]
    a, b = f.get("side1"), f.get("side2")
    where = f["label"].title().replace(" Of ", " of ")
    return f"{L.get('name', 'Crown Cup')} - {where} — {n[a]['name']} vs {n[b]['name']}"


def cmd_film(A):
    d = pathlib.Path(A.dir)
    L = load(d)
    _, gpath = open_game(A.game)
    overrides = check_runtime(L, gpath, None, A.force)
    if overrides:
        L.setdefault("runtime_overrides", []).append(
            dict(at=dt.datetime.now().isoformat(timespec="seconds"), command="film",
                 problems=overrides))
        save(d, L)
    todo = [f for f in L["fixtures"] if f.get("result") and (not A.only or f["id"] == A.only)]
    total = len(todo)
    # THE CARD PRINTS THE NAME (v118), so a run without one would bake "no name" into every
    # knockout short -- refused here, before the first capture, not at the round of 16
    if todo and not L.get("name"):
        sys.exit("! the ledger has no tournament name, and the verdict card prints it -- "
                 "`cup.py schedule --name \"...\"` first")
    for i, f in enumerate(todo, 1):
        out = file_for(L, f, d)
        rel = out.relative_to(d)
        if out.exists() and not A.redo:
            f["file"] = str(rel)
            print(f"[cup] {i}/{total} {f['id']} already filmed: {rel}")
            continue
        main, sub = band_lines(L, f)
        # v118: the verdict card's blob, beside the mp4 it is filmed into
        card = card_blob(L, f)
        card_path = out.parent / f"{out.stem}-cup.json"
        args = [sys.executable, str(HERE / "shorts_build.py"), "--game", str(gpath),
                "--a", f["side1"], "--b", f["side2"], "--seed", str(f["seed"]),
                "--no-card", "--stakes", main, "--stakes-sub", sub,
                "--cup-json", str(card_path), "--out", str(out)]
        print(f"[cup] {i}/{total} {f['id']} {f['side1']} v {f['side2']} seed {f['seed']} "
              f"-> {rel}")
        print(f"[cup] band: {main} / {sub}")
        print(f"[cup] card: {card_line(card)}")
        if A.dry_run:
            print("       " + " ".join(f'"{x}"' if " " in x else x for x in args[1:]))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(json.dumps(card, indent=1, ensure_ascii=False), encoding="utf-8")
        # THE SAME PROCESS THE APP SPAWNS, ONE FOLDER TO ITSELF (app/main.js on
        # `_clip_frames`). Output streams through so the app sees shorts_build's
        # own [progress] lines exactly as it does for a single short.
        proc = subprocess.Popen(args, cwd=str(HERE), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, bufsize=1)
        measured = None
        for line in proc.stdout:
            line = line.rstrip("\n")
            print(line, flush=True)
            if "MB" in line and "LUFS" in line:
                measured = line.strip()
        code = proc.wait()
        if code != 0 or not out.exists():
            f["film_error"] = f"shorts_build exited {code}"
            save(d, L)
            sys.exit(f"! {f['id']} failed (exit {code}); fix it and run `cup.py film` again "
                     "-- everything filmed so far is kept")
        f["file"] = str(rel)
        f["band"] = [main, sub]
        f["card"] = card
        f["delivery"] = measured
        f.pop("film_error", None)
        f["filmed"] = dt.datetime.now().isoformat(timespec="seconds")
        save(d, L)
        print(f"[cup] done {i}/{total}", flush=True)
    write_schedule(L, d)
    filmed = sum(1 for f in L["fixtures"] if f.get("file"))
    print(f"\n[cup] {filmed}/{len(L['fixtures'])} filmed - schedule: {d / 'SCHEDULE.md'}")
    return 0


def write_schedule(L, d: pathlib.Path):
    """The file a person posts from: order, day and slot, file, caption, band.
    Two a day (plan §0); day 1 is the first post, dates are filled in when
    --start is given to `schedule`."""
    per_day = L.get("per_day", 2)
    start = L.get("start_date")
    n = L["roster"]
    lines = [f"# {L.get('name', 'Crown Cup')} — posting schedule",
             f"draw seed {L['draw_seed']} - build {L['build']['sha256'][:12]} - "
             f"{L['machine']} - Chromium {L['chromium']}", "",
             "| # | day | slot | fixture | file | caption | band |", "|---|---|---|---|---|---|---|"]
    for f in L["fixtures"]:
        i = f["order"]
        day = (i - 1) // per_day + 1
        slot = "AM" if (i - 1) % per_day == 0 else "PM"
        when = day
        if start:
            when = (dt.date.fromisoformat(start) + dt.timedelta(days=day - 1)).isoformat()
        if not f.get("side1"):
            lines.append(f"| {i} | {when} | {slot} | {f['id']} | — | — | — |")
            continue
        band = " / ".join(f.get("band") or band_lines(L, f))
        lines.append(f"| {i} | {when} | {slot} | {f['id']} | {f.get('file', '—')} | "
                     f"{caption(L, f)} | {band} |")
    (d / "SCHEDULE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # results, for the bracket page and for anyone checking the rule
    res = [dict(order=f["order"], id=f["id"], round=f["round"], a=f.get("side1"),
                b=f.get("side2"), seed=f.get("seed"), k=f.get("k"), result=f.get("result"),
                file=f.get("file")) for f in L["fixtures"]]
    (d / "results.json").write_text(json.dumps(res, indent=1), encoding="utf-8")


def cmd_status(A):
    d = pathlib.Path(A.dir)
    L = load(d)
    n = L["roster"]
    seeded = sum(1 for f in L["fixtures"] if f.get("result"))
    filmed = sum(1 for f in L["fixtures"] if f.get("file"))
    print(f"  {L.get('name', L['cup'])}: {len(n)} relics - {len(L['groups'])} groups - "
          f"{len(L['fixtures'])} fixtures - {seeded} seeded - {filmed} filmed")
    print(f"  build {L['build']['path']} {L['build']['sha256'][:12]} - {L['machine']} - "
          f"Chromium {L['chromium']}")
    fat = [f["result"]["fatal"] for f in L["fixtures"] if f.get("result")]
    if fat:
        print(f"  the director found the finale in {sum(fat)}/{len(fat)} fights; "
              "the rest end at plain speed")
    for g in L["groups"]:
        rows, decided = standings(L, g)
        cells = "  ".join(f"{n[r['id']]['name']:<13}{r['w']}-{r['l']} {r['hp']:>3}" for r in rows)
        print(f"  {g}  {cells}  {'-> ' + n[rows[0]['id']]['name'] + ' (' + decided + ')' if decided else ''}")
    for f in L["fixtures"]:
        if f["round"] == "group":
            continue
        a, b = f.get("side1"), f.get("side2")
        who = f"{n[a]['name']} v {n[b]['name']}" if a and b else "…"
        r = f.get("result")
        print(f"  {f['id']:<6} {who:<32} {(n[r['winner']]['name'] + ' by ' + str(r['hp'])) if r else ''}"
              f"  {'filmed' if f.get('file') else ''}")
    return 0


def cmd_schedule(A):
    d = pathlib.Path(A.dir)
    L = load(d)
    if A.start:
        L["start_date"] = A.start
    if A.per_day:
        L["per_day"] = A.per_day
    if A.name:
        L["name"] = A.name
    save(d, L)
    write_schedule(L, d)
    print(f"  {d / 'SCHEDULE.md'}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(DEFAULT_DIR), help="the tournament folder")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("draw"); p.add_argument("--game", required=True)
    p.add_argument("--seed", type=int, required=True, help="the draw seed; publish it")
    p.add_argument("--cup", default="crown-cup-1", help="the id in the seed rule")
    p.add_argument("--field", type=int, default=0, help="TESTING: first N relics only")
    p.add_argument("--force", action="store_true")
    p = sp.add_parser("seeds"); p.add_argument("--game", required=True)
    p.add_argument("--only"); p.add_argument("--redo", action="store_true")
    p.add_argument("--max-k", type=int, default=50); p.add_argument("--force", action="store_true")
    p = sp.add_parser("film"); p.add_argument("--game", required=True)
    p.add_argument("--only"); p.add_argument("--redo", action="store_true")
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--force", action="store_true")
    sp.add_parser("status")
    p = sp.add_parser("cupjson"); p.add_argument("fixture", help="e.g. A3, QF-2 -- the card's blob")
    p = sp.add_parser("schedule"); p.add_argument("--start", help="YYYY-MM-DD of post 1")
    p.add_argument("--per-day", type=int); p.add_argument("--name")
    A = ap.parse_args()
    return {"draw": cmd_draw, "seeds": cmd_seeds, "film": cmd_film,
            "status": cmd_status, "schedule": cmd_schedule, "cupjson": cmd_cupjson}[A.cmd](A)


if __name__ == "__main__":
    sys.exit(main())
