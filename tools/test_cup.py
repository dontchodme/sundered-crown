#!/usr/bin/env python3
"""Falsify cup.py's bookkeeping against hand-worked cases. No browser.

    python test_cup.py

Each test states what the plan says and checks the code against it, with a
case that would FAIL if the rule were implemented the obvious wrong way.
"""
from __future__ import annotations
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cup

SCHOOLS = ["dwarven", "verdant", "runic", "vigil", "sanctified", "bloodsworn", "umbral"]
TYPES = ["greatsword", "scythe", "twinblade", "flail", "warhammer", "bow", "staff"]
# a Latin-square walk, so any prefix of it is as balanced as a prefix can be
ROSTER49 = {}
for i in range(49):
    s, t = SCHOOLS[i % 7], TYPES[(i // 7 + i) % 7]
    ROSTER49[f"{s[:3]}_{t[:3]}"] = dict(name=f"{s[:3]}_{t[:3]}", school=s, type=t)
assert len(ROSTER49) == 49
FAILS = 0


def check(cond, what):
    global FAILS
    print(("  ok   " if cond else "  FAIL ") + what)
    if not cond:
        FAILS += 1


def ledger(n_relics=49, seed=7):
    roster = dict(list(ROSTER49.items())[:n_relics])
    groups, chal, draw_no, _ = cup.make_draw(roster, seed)
    return dict(cup="t", roster=roster, draw_no=draw_no,
                groups={chr(65 + i): g for i, g in enumerate(groups)},
                challenger=chal, fixtures=cup.build_fixtures(groups, chal, draw_no))


def play(L, fid, winner, hp):
    f = cup.fixture_by_id(L, fid)
    a, b = cup.sides(L, f)
    assert a and b, f"{fid} not resolvable"
    f["side1"], f["side2"] = a, b
    w = a if winner == "a" else b
    f["result"] = dict(winner=w, loser=(b if w == a else a), hp=hp, dur=60.0,
                       reason="slain", cuts=5, clanks=20)
    return a, b


# --- the draw --------------------------------------------------------------
print("draw")
L = ledger()
check(len(L["groups"]) == 16 and all(len(g) == 3 for g in L["groups"].values()),
      "49 relics -> 16 groups of 3")
check(L["challenger"] is not None, "and one challenger")
for g in L["groups"].values():
    check(len({L["roster"][r]["school"] for r in g}) == 3 and
          len({L["roster"][r]["type"] for r in g}) == 3, f"group {g} has 3 schools, 3 types")
chal, last = L["challenger"], L["groups"]["P"]
check(all(L["roster"][chal]["school"] != L["roster"][o]["school"] and
          L["roster"][chal]["type"] != L["roster"][o]["type"] for o in last[:2]),
      "the challenger is legal in group P")
L2 = ledger()
check(L2["groups"] == L["groups"] and L2["challenger"] == L["challenger"],
      "the same seed gives the same draw")
check(ledger(seed=8)["groups"] != L["groups"], "a different seed gives a different draw")
check(len(L["fixtures"]) == 65, f"65 fixtures ({len(L['fixtures'])})")
check([f["id"] for f in L["fixtures"][:5]] == ["PI", "A1", "A2", "A3", "B1"], "posting order starts PI, A1, A2, A3, B1")
check([f["round"] for f in L["fixtures"][-3:]] == ["sf", "third", "final"], "and ends SF, third place, final")

# --- side balance in a group --------------------------------------------------
print("sides")
sides = {}
for m in (1, 2, 3):
    f = cup.fixture_by_id(L, f"A{m}")
    a, b = cup.sides(L, f)
    sides.setdefault(a, []).append(1); sides.setdefault(b, []).append(2)
check(all(sorted(v) == [1, 2] for v in sides.values()), "every relic in a group is side 1 once and side 2 once")

# --- standings and tiebreaks ------------------------------------------------
print("standings")
L = ledger()
p1, p2 = play(L, "A1", "a", 100)        # P1 beats P2
rows, decided = cup.standings(L, "A")
check(decided is None, "a group is not decided after one match")
play(L, "A2", "b", 50)                   # P3 beats P2  -> P2 is 0-2
play(L, "A3", "a", 10)                   # P3 beats P1  -> P3 2-0
rows, decided = cup.standings(L, "A")
check(rows[0]["w"] == 2 and decided == "wins", "two wins takes the group on wins")
check(rows[-1]["l"] == 2, "the 0-2 relic is last")

L = ledger()
play(L, "B1", "a", 200)   # P1 beats P2, 200 left
play(L, "B2", "a", 40)    # P2 beats P3, 40 left
play(L, "B3", "a", 90)    # P3 beats P1, 90 left  -> three-way tie
rows, decided = cup.standings(L, "B")
check(decided == "hp" and rows[0]["hp"] == 200, "a three-way tie goes to HP remaining (200 > 90 > 40)")
check([r["pts"] for r in rows] == [3, 3, 3], "all on 3 points")

L = ledger()
play(L, "C1", "a", 77); play(L, "C2", "a", 77); play(L, "C3", "a", 77)
rows, decided = cup.standings(L, "C")
check(decided == "draw number" and
      rows[0]["draw_no"] == min(r["draw_no"] for r in rows), "an HP tie goes to the lower draw number")

# --- the play-in feeds group P --------------------------------------------
print("play-in")
L = ledger()
f = cup.fixture_by_id(L, "P2")
check(cup.sides(L, f) == (None, None) or None in cup.sides(L, f), "P2 cannot be sided before the play-in")
a, b = play(L, "PI", "a", 30)   # the challenger wins
check(a == L["challenger"], "the challenger is side 1 of the play-in")
f = cup.fixture_by_id(L, "P2")
x, y = cup.sides(L, f)
check(y == L["challenger"], "the challenger takes group P's third slot")
check(L["groups"]["P"][2] not in (x, y), "the relic it beat is gone")

# --- the knockout resolves from results, lower draw number is side 1 --------
print("knockout")
L = ledger()
play(L, "PI", "b", 30)
for g in "ABCDEFGHIJKLMNOP":
    play(L, f"{g}1", "a", 100); play(L, f"{g}2", "b", 100); play(L, f"{g}3", "b", 100)
winners = {g: cup.standings(L, g)[0][0]["id"] for g in "ABCDEFGHIJKLMNOP"}
f = cup.fixture_by_id(L, "R16-1")
a, b = cup.sides(L, f)
check({a, b} == {winners["A"], winners["B"]}, "R16-1 is the winners of A and B")
check(L["draw_no"][a] < L["draw_no"][b], "the lower draw number is side 1")
f = cup.fixture_by_id(L, "QF-1")
check(cup.sides(L, f) == (None, None) or None in cup.sides(L, f), "QF-1 waits on the round of 16")
for i in range(1, 9):
    play(L, f"R16-{i}", "a", 60)
for i in range(1, 5):
    play(L, f"QF-{i}", "a", 60)
play(L, "SF-1", "a", 60); play(L, "SF-2", "b", 60)
f3, ff = cup.fixture_by_id(L, "3P"), cup.fixture_by_id(L, "F")
l1 = cup.fixture_by_id(L, "SF-1")["result"]["loser"]; w2 = cup.fixture_by_id(L, "SF-2")["result"]["winner"]
check(l1 in cup.sides(L, f3), "the third-place match takes the semi-final losers")
check(w2 in cup.sides(L, ff), "the final takes the semi-final winners")

# --- the band never spoils, and says the right thing --------------------------
print("band")
L = ledger()
play(L, "PI", "a", 1)
p1, p2 = play(L, "A1", "b", 100)                 # P2 beat P1
f = cup.fixture_by_id(L, "A2"); f["side1"], f["side2"] = cup.sides(L, f)
main, sub = cup.band_lines(L, f)
check(sub == f"WIN AND {p2.upper()} TAKES THE GROUP", f"m2 after P2 won m1: '{sub}'")
L = ledger(); play(L, "PI", "a", 1)
p1, p2 = play(L, "A1", "a", 100)                 # P1 beat P2
f = cup.fixture_by_id(L, "A2"); f["side1"], f["side2"] = cup.sides(L, f)
main, sub = cup.band_lines(L, f)
check(sub == f"LOSE AND {p2.upper()} IS OUT", f"m2 after P2 lost m1: '{sub}'")
play(L, "A2", "b", 50)                            # P3 beat P2 -> P1 3, P3 3
f = cup.fixture_by_id(L, "A3"); f["side1"], f["side2"] = cup.sides(L, f)
play(L, "A3", "a", 5)                             # result in -- the band must not see it
main, sub = cup.band_lines(L, f)
check(sub == "WINNER TAKES THE GROUP", f"m3 at 3 v 3: '{sub}'")
check(main == "GROUP A · MATCH 3 OF 3", f"main line is the round: '{main}'")
L = ledger(); play(L, "PI", "a", 1)
play(L, "B1", "b", 100); play(L, "B2", "a", 100)  # P2 won both
f = cup.fixture_by_id(L, "B3"); f["side1"], f["side2"] = cup.sides(L, f)
main, sub = cup.band_lines(L, f)
check(sub.startswith("GROUP DECIDED"), f"a dead rubber says so: '{sub}'")

# knockout spoilers: R16-1's band must not name R16-2's winner (posts later)
L = ledger(); play(L, "PI", "b", 30)
for g in "ABCDEFGHIJKLMNOP":
    play(L, f"{g}1", "a", 100); play(L, f"{g}2", "b", 100); play(L, f"{g}3", "b", 100)
for i in range(1, 9):
    f = cup.fixture_by_id(L, f"R16-{i}"); f["side1"], f["side2"] = cup.sides(L, f)
    play(L, f"R16-{i}", "a", 60)
m1, s1 = cup.band_lines(L, cup.fixture_by_id(L, "R16-1"))
m2, s2 = cup.band_lines(L, cup.fixture_by_id(L, "R16-2"))
w1 = cup.fixture_by_id(L, "R16-1")["result"]["winner"]
check(s1 == "WINNER INTO THE QUARTER-FINALS", f"R16-1 does not name R16-2's winner: '{s1}'")
check(s2 == f"WINNER MEETS {w1.upper()}", f"R16-2 names R16-1's winner, already posted: '{s2}'")

# --- the seed rule ----------------------------------------------------------------
print("rule")
s0 = cup.fight_seed("crown-cup-1", "A1", "x", "y", 0)
check(s0 == cup.fight_seed("crown-cup-1", "A1", "x", "y", 0), "the rule is deterministic")
check(s0 != cup.fight_seed("crown-cup-1", "A1", "y", "x", 0), "and depends on the sides")
check(s0 != cup.fight_seed("crown-cup-1", "A1", "x", "y", 1), "and on k")
check(0 <= s0 < 2 ** 31, "31-bit seed")

# --- the verdict card (v118) ---------------------------------------------------------
# Posting order with the play-in: PI 1, A1 2, A2 3, A3 4, B1 5, B2 6, B3 7 ... and two a day,
# so A1 is day 1, A2 and A3 day 2, B1 and B2 day 3, B3 day 4.
print("card")
import json
NAME = "Weapon Ball World Cup"


def card(L, fid):
    return cup.card_blob(L, cup.fixture_by_id(L, fid))


def rows(c):
    return [(r["id"], r["w"], r["l"], r["hp"], r["mark"]) for r in c["rows"]]


L = ledger(); L["name"] = NAME
play(L, "PI", "a", 30)
p1, p2 = play(L, "A1", "a", 120)        # P1 beats P2, 120 left
_, p3 = play(L, "A2", "b", 80)          # P2 v P3: P3 wins on 80 -> P2 is 0-2
play(L, "A3", "a", 45)                  # P3 v P1: P3 wins on 45 -> P3 2-0 on 125
before = json.dumps(L, sort_keys=True)
c1 = card(L, "A1")
check(json.dumps(L, sort_keys=True) == before, "building a card leaves the ledger as it was")
r1 = rows(c1)
check(c1["kind"] == "group" and c1["title"] == "GROUP A", f"A1 is a group card: {c1['title']!r}")
check(r1[0] == (p1, "1", "0", "120", True), f"after A1 the winner tops on 1-0, 120, marked: {r1[0]}")
check(dict((x[0], x) for x in r1)[p3][1:3] == ("0", "0"),
      "after A1, P3 has played nothing -- A2 and A3 are in the ledger but not posted yet")
check(all(x[3] == "—" for x in r1[1:]), "no wins, no HP: a dash")
check(c1["footer"] == "2 MATCHES LEFT · A2 TOMORROW", f"A1 footer: {c1['footer']!r}")
c2 = card(L, "A2")
check(rows(c2) == [(p1, "1", "0", "120", False), (p3, "1", "0", "80", True), (p2, "0", "2", "—", False)],
      f"after A2: P1 on 120 over P3 on 80, P2 0-2, the marker on A2's winner: {rows(c2)}")
check(c2["footer"] == "1 MATCH LEFT · A3 LATER TODAY", f"A2 and A3 post the same day: {c2['footer']!r}")
c3 = card(L, "A3")
check(rows(c3)[0] == (p3, "2", "0", "125", True), f"after A3: P3 2-0 on 125, marked: {rows(c3)[0]}")
check(c3["footer"] == f"GROUP DECIDED · {p3.upper()} IS THROUGH", f"A3 footer: {c3['footer']!r}")
check(c3["winner"] == p3 and c3["hp"] == 45, "the blob carries the match's own result for the film to check")
L["per_day"] = 1
check(card(L, "A2")["footer"] == "1 MATCH LEFT · A3 TOMORROW", "one a day: the next match is always tomorrow")
del L["per_day"]

play(L, "B1", "a", 200)                 # P1 beats P2, 200
play(L, "B2", "a", 40)                  # P2 beats P3, 40
q3, q1 = play(L, "B3", "a", 90)         # P3 beats P1, 90 -> three-way tie, HP 200 / 90 / 40
cb = card(L, "B3")
check([x[3] for x in rows(cb)] == ["200", "90", "40"] and rows(cb)[1][4] and rows(cb)[1][0] == q3,
      f"a three-way tie lists on HP, the marker on B3's winner in second: {rows(cb)}")
check(cb["footer"] == f"{q1.upper()} IS THROUGH ON HP REMAINING", f"HP tiebreak footer: {cb['footer']!r}")
check(card(L, "B2")["footer"] == "1 MATCH LEFT · B3 TOMORROW", "B2 (day 3) -> B3 (day 4)")

d1, d2 = play(L, "C1", "b", 100)        # P2 beats P1
play(L, "C2", "a", 100)                 # P2 beats P3 -> P2 6 points with a match to play
cc = card(L, "C2")
check(cc["footer"] == f"GROUP DECIDED · {d2.upper()} IS THROUGH",
      f"two wins decides the group a match early: {cc['footer']!r}")
play(L, "C3", "a", 15)                  # the dead rubber: P3 beats P1
cd = card(L, "C3")
check(rows(cd)[0][:3] == (d2, "2", "0") and not rows(cd)[0][4] and any(x[4] for x in rows(cd)[1:]),
      f"the dead rubber: P2 still tops, the marker is on C3's winner: {rows(cd)}")
check(cd["footer"] == f"GROUP DECIDED · {d2.upper()} IS THROUGH", f"dead rubber footer: {cd['footer']!r}")

play(L, "D1", "a", 77); play(L, "D2", "a", 77); play(L, "D3", "a", 77)
cdn = card(L, "D3")
check(cdn["footer"].endswith("IS THROUGH ON DRAW NUMBER"), f"an HP tie: {cdn['footer']!r}")

# the play-in and the knockout
L = ledger(); L["name"] = NAME
play(L, "PI", "b", 30)
for g in "ABCDEFGHIJKLMNOP":
    play(L, f"{g}1", "a", 100); play(L, f"{g}2", "b", 100); play(L, f"{g}3", "b", 100)
for rid in [f"R16-{i}" for i in range(1, 9)] + [f"QF-{i}" for i in range(1, 5)]:
    play(L, rid, "a", 60)
play(L, "SF-1", "a", 60); play(L, "SF-2", "b", 60); play(L, "3P", "a", 20); play(L, "F", "b", 5)
W = lambda fid: cup.fixture_by_id(L, fid)["result"]["winner"].upper()
cp = card(L, "PI")
check((cp["kind"], cp["title"], cp["verdict"]) == ("knockout", "PLAY-IN", "through"), f"PI card: {cp['title']!r}")
check(cp["next"] == f"next: v {L['groups']['P'][1].upper()} · P2",
      f"the play-in winner meets P's second relic in P2: {cp['next']!r}")
check(cp["footer"] == "weapon ball world cup · 48 relics left", f"PI footer: {cp['footer']!r}")
k1, k2, k4 = card(L, "R16-1"), card(L, "R16-2"), card(L, "R16-4")
check(k1["title"] == "ROUND OF 16" and k1["name"] == W("R16-1"), f"R16-1: {k1['title']!r} {k1['name']!r}")
check(k1["next"] == "next: QF 1", f"R16-1 does not name R16-2's winner, which posts later: {k1['next']!r}")
check(k2["next"] == f"next: v {W('R16-1')} · QF 1", f"R16-2 names R16-1's, already posted: {k2['next']!r}")
check((k1["footer"], k4["footer"]) == ("weapon ball world cup · 15 relics left",
                                       "weapon ball world cup · 12 relics left"),
      f"relics left count only what has posted: {k1['footer']!r} / {k4['footer']!r}")
check(card(L, "QF-2")["next"] == f"next: v {W('QF-1')} · SF 1", "QF-2 -> SF 1 against QF-1's winner")
s1, s2 = card(L, "SF-1"), card(L, "SF-2")
check((s1["next"], s2["next"]) == ("next: THE FINAL", f"next: v {W('SF-1')} · THE FINAL"),
      f"the semis point at the final: {s1['next']!r} / {s2['next']!r}")
check(s2["footer"].endswith("· 2 relics left"), f"two left after the second semi: {s2['footer']!r}")
c3p, cf = card(L, "3P"), card(L, "F")
check((c3p["verdict"], c3p["footer"][-13:]) == ("third place", "2 relics left"),
      f"third place: {c3p['verdict']!r}, {c3p['footer']!r}")
check((cf["title"], cf["verdict"], cf["footer"]) == ("THE FINAL", "keeps the crown",
                                                      "weapon ball world cup · 1 relic left"),
      f"the final: {cf['verdict']!r}, {cf['footer']!r}")
check(cf["next"] == f"over {cup.fixture_by_id(L, 'F')['result']['loser'].upper()}", f"final: {cf['next']!r}")
del L["name"]
try:
    card(L, "R16-1"); refused = False
except SystemExit:
    refused = True
check(refused, "a knockout card without the tournament's name is refused, not printed blank")
check(card(L, "A1")["kind"] == "group", "a group card does not need the name")

# --- shapes ----------------------------------------------------------------------
print("shapes")
for n, G, fx in ((25, 8, 1 + 24 + 4 + 2 + 1 + 1), (48, 16, 48 + 8 + 4 + 2 + 1 + 1), (13, 4, 1 + 12 + 2 + 1 + 1)):
    Ln = ledger(n)
    check(len(Ln["groups"]) == G and len(Ln["fixtures"]) == fx,
          f"{n} relics -> {G} groups, {fx} fixtures ({len(Ln['fixtures'])})")

print(f"\n{'ALL OK' if not FAILS else str(FAILS) + ' FAILED'}")
sys.exit(1 if FAILS else 0)
