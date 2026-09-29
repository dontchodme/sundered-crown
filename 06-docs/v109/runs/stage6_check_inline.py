"""The rows the labs RETURNED (their reports as the orchestrator relayed them, truncated) are a prefix
of the row files: json.dumps({"rows": rows}) of each rows_final.json starts with the relayed text."""
import json, sys, pathlib
S6 = pathlib.Path(__file__).parent; S = S6.parent
for k, f in (("voice", "inline_voice.txt"), ("picture", "inline_picture.txt")):
    rows = json.loads((S / f"stage6-{k}" / "rows_final.json").read_text(encoding="utf-8"))
    full = json.dumps({"rows": rows}, ensure_ascii=False, separators=(",", ":"))
    pre = (S6 / f).read_text(encoding="utf-8").rstrip("\n").rstrip(" ")
    n = 0
    while n < len(pre) and n < len(full) and pre[n] == full[n]:
        n += 1
    ok = n == len(pre)
    print(f"{k}: relayed report {len(pre)} chars (rows {len(rows)}); equal to the row file's for {n} chars "
          + ("-> PREFIX OK" if ok else f"-> DIFFERS at {n}: {pre[n-40:n+40]!r} / {full[n-40:n+40]!r}"))
    # a control that must fail: one character changed in the file's text
    bad = full[:len(pre) // 2] + ("X" if full[len(pre) // 2] != "X" else "Y") + full[len(pre) // 2 + 1:]
    print(f"   control (one char changed half way): prefix {'HOLDS (BAD)' if bad.startswith(pre) else 'fails, as it must'}")
