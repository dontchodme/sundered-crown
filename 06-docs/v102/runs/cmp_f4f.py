# Review round 3: stage 1 against lab arm A, FIGHT FOR FIGHT. Each fight's record from f4f_overlay.py: winner, steps,
# both fighters' hits, hp, shield, crits and damage dealt, clanks, end reason. Any field differing in any fight is printed.
import json, sys
lab, built = sys.argv[1], sys.argv[2]
L = json.load(open(lab))["arms"]["A"]["fights"]; B = json.load(open(built))["arms"]["SHIP"]["fights"]
FIELDS = ["foe", "seed", "win", "steps", "hits", "foe hits", "hp", "foe hp", "shield", "foe shield", "crits", "foe crits",
          "dealt", "foe dealt", "clanks", "reason"]
diff = [(a, b) for a, b in zip(L, B) if a != b]
wins = lambda R: sum(1 for r in R if r[2] == 1) / len(R)
print(f"lab arm A {len(L)} fights (win {wins(L):.4f}) | stage 1 SHIP {len(B)} fights (win {wins(B):.4f}) | "
      f"{len(FIELDS)} fields a fight | fights differing in any field: {len(diff) + abs(len(L) - len(B))}"
      + ("   IDENTICAL, FIGHT FOR FIGHT" if not diff and len(L) == len(B) else ""))
for a, b in diff[:10]:
    print("   ", {FIELDS[i]: (a[i], b[i]) for i in range(len(a)) if a[i] != b[i]}, "in", a[0], a[1])
sys.exit(0 if not diff and len(L) == len(B) else 1)
