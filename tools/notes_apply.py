#!/usr/bin/env python3
"""APPLY fighter-notes.json — into the BUILDERS, not the generated HTML.

    python3 notes_apply.py            # then rebuild the chain

Every string in `fighter-notes.json` lives in a file that a builder regenerates.
Editing `sc-gs7.html` would work exactly once and die on the next
`roster_gs_build.py` run — the failure SEED.md records as costing twelve tuned
damage values. So each note is applied at its AUTHORING SITE:

    the four relics' name / blurb / ult.tip     roster_gs_build.py
    STATUS.curse.tip, STATUS.hex.tip            introcard_build.py  (SHARED)
    the status-tip length contract              verify.py

THREE NOTES ARE NOT APPLIED AS WRITTEN, AND HERE IS WHY
--------------------------------------------------------
**hex: "Stuns the targets weapon 0.2s per stack" — factually wrong.** Read the
tick at `f.hexClock += dt * hx`: stacks make the clock run FASTER, so the stun
fires MORE OFTEN. `stunFor` is a flat `0.20` and does not scale. "0.2s per
stack" reads as 0.4s at two stacks, which the code never does. The clarification
underneath it — that it is the TARGET's weapon, not your own — is real and is
kept: `Stuns their weapon 0.2s, faster per stack`.

**That wording is 41 chars against a 40-char contract, and the contract is the
wrong instrument.** Measured at the arena panel's own 25px:

    Stuns their weapon 0.2s, faster per stack     41ch   453px
    Increases damage taken by 11% per stack       39ch   471px   <-- already shipped

A shorter string is already wider. The cap is a proxy for "fits the explainer
panel", and `intro_probe [6]` measures that directly at 536px — 83px of headroom
here. The char cap is raised to 44 as a runaway guard, and the comment now says
which of the two is the real constraint.

**curse: "Reduces maximum hp" reverses a decision from your own wording pass.**
`APPLY-ME.md` §7: *"Drains maximum hp, permanently"* — "permanently" kept: it is
the one status that never expires. `dur:99` and an unrestored `maxHp` confirm it.
Dropping the word makes Curse read like every other temporary debuff, and the
permanence is the only thing that distinguishes it. **Applied as you wrote it** —
your call, latest word wins — but flagged, and `--keep-permanent` gives you
`Permanently reduces maximum hp` (30ch / 386px) if you want the verb without
losing the fact.

RENAMING OATHWOUND TO GORESHARD ORPHANS THINGS
----------------------------------------------
The old name carried a conceit — an oath sworn in blood — that the blurb, and a
comment in the ult art, were both written around. The blurb you already flagged.
The ult-art comment is updated here. The relic `id` stays `oathwound`, because
it is the key the ult set-piece dispatches on (`u.w === "oathwound"`), the key in
the `ultFx` life table, and the key in this builder — renaming it is a clean
three-file change but it is a change to a shared identifier, so it is offered
rather than taken.
"""
from __future__ import annotations
import argparse, pathlib, sys

HERE = pathlib.Path(__file__).parent

# (file, old, new, why) — every one asserted to appear exactly once.
def edits(keep_permanent: bool):
    curse_tip = ("Permanently reduces maximum hp" if keep_permanent
                 else "Reduces maximum hp")
    return [
        # ---- roster_gs_build.py : the four relics ---------------------------
        ("roster_gs_build.py",
         'id:"oathwound", name:"Oathwound", aff:"bloodsworn"',
         'id:"oathwound", name:"Goreshard", aff:"bloodsworn"',
         "rename (id kept — it is the ult-art dispatch key)"),

        ("roster_gs_build.py",
         'blurb:"Sworn on an open palm. The oath is the wound, and it does not close." }}',
         'blurb:"Serrated the whole length. It leaves teeth in the wound, and the '
         'bleeding does the rest." }}',
         "blurb — the oath conceit died with the name; this is barbs + hemorrhage"),

        ("roster_gs_build.py",
         'tip:"Opens a wound: 16 damage and 3 Hemorrhage stacks"',
         'tip:"Deals 16 damage and applies 3 Hemorrhage stacks"',
         "ult tip — your deals/applies form"),

        ("roster_gs_build.py",
         'blurb:"Not forged — grown, and still growing. It puts down roots where it lands." }}',
         'blurb:"Not forged — grown, and still growing. Puts down roots where it lands." }}',
         "blurb — verbatim"),

        ("roster_gs_build.py",
         'tip:"Roots for 1.3 seconds: 9 damage and 3 Entangle stacks"',
         'tip:"Roots for 1.3 seconds, deals 9 damage and applies 3 Entangle stacks"',
         "ult tip — comma not colon, to match Thornwake's identical form"),

        ("roster_gs_build.py",
         'blurb:"A blade with the light eaten out of it. What it takes, it keeps." }}',
         'blurb:"A reaper\'s blade. What it takes off a life never grows back." }}',
         "blurb — your reaper direction, without borrowing the scythe's identity"),

        ("roster_gs_build.py",
         'tip:"Nova: 11 damage, 3 Curse stacks, knocks back"',
         'tip:"Nova: deals 11 damage and applies 3 Curse stacks — knocks back"',
         "ult tip — punctuated to match Grudgebearer's identical form"),

        ("roster_gs_build.py",
         'blurb:"Held by nothing and arguing. Every shard is a step in the proof." }}',
         'blurb:"Blade-shards held in formation by nothing at all. Close the gaps and '
         'it is a sword again." }}',
         "blurb — your direction; 'by nothing' is the school's own thesis"),

        ("roster_gs_build.py",
         'tip:"Fires a bolt: 18 damage and 3 Hex stacks"',
         'tip:"Deals 18 damage and applies 3 Hex stacks"',
         "ult tip — your deals/applies form"),

        # ---- introcard_build.py : the two SHARED status tips ----------------
        ("introcard_build.py",
         "'tip:\"Stuns the weapon 0.2s, faster per stack\"'",
         "'tip:\"Stuns their weapon 0.2s, faster per stack\"'",
         "SHARED — moves Spellbreaker and the arena panel too"),

        ("introcard_build.py",
         "'tip:\"Drains maximum hp, permanently\"'",
         f"'tip:\"{curse_tip}\"'",
         "SHARED — moves Gravemourn and the arena panel too"),

        # ---- verify.py : the contract the hex tip now exceeds ---------------
        ("verify.py",
         "else if (s.tip.length > 40) bad.push(`${k}: status tip ${s.tip.length} chars (max 40)`);",
         "else if (s.tip.length > 44) bad.push(`${k}: status tip ${s.tip.length} chars (max 44)`);",
         "40 -> 44; the binding constraint is intro_probe [6]'s 536px, not the count"),

        # ---- ultart_build.py : the comment the rename orphaned --------------
        ("ultart_build.py",
         "      /* THE OATH: a taut thread back to the caster. Straight, not jagged —\n"
         "         a binding, and the thing Exsanguinate's flung fangs never had. */",
         "      /* THE TETHER: a taut thread back to the caster. Straight, not jagged\n"
         "         — a binding, and the thing Exsanguinate's flung fangs never had.\n"
         "         (Was \"THE OATH\" when this relic was Oathwound. The picture did not\n"
         "         change with the rename; the reason for it did.) */",
         "the rename orphaned this comment"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep-permanent", action="store_true",
                    help='curse tip becomes "Permanently reduces maximum hp" instead')
    ap.add_argument("--dry-run", action="store_true")
    A = ap.parse_args()

    plan = edits(A.keep_permanent)
    bad = []
    for fn, old, new, why in plan:
        p = HERE / fn
        if not p.exists():
            bad.append(f"{fn}: missing"); continue
        n = p.read_text().count(old)
        if n != 1:
            bad.append(f"{fn}: anchor appears {n}x, expected 1 — {old[:60]}")
    if bad:
        print("REFUSED — anchors did not verify. Diff before re-anchoring; do not "
              "loosen them.", file=sys.stderr)
        for b in bad: print("  " + b, file=sys.stderr)
        return 1

    for fn, old, new, why in plan:
        p = HERE / fn
        if not A.dry_run:
            p.write_text(p.read_text().replace(old, new, 1))
        print(f"  [{fn}] {why}")
    print(f"\n  {len(plan)} edits {'planned' if A.dry_run else 'applied'} "
          f"across {len(set(e[0] for e in plan))} builders")
    if not A.dry_run:
        print("\n  NOW REBUILD — these are builders, and nothing has changed in any\n"
              "  .html until the chain is run again.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
