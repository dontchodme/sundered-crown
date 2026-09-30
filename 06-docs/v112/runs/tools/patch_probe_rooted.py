"""v112 §3: [3] and [5] read the blows that ROOTED; whether a blow in the window rooted at all is [2]'s sentence.
Found by m2 (every other blow roots): it failed [2] and, on the same unrooted blows, [3] (the pin not written) and
[5] (no +1) -- three checks for one broken sentence. The coverage conditions (pinOk, entOk > 0) keep [3] and [5]
from passing vacuously; a blow that roots nobody must still leave the pin alone ([3])."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_probe.py"); s = p.read_text(encoding="utf-8")
R = [("    if (expect){\n      const hold = PIN.rootFor;",
      "    /* [3] and [5] read the blows that ROOTED (dr 1); whether a blow in the window rooted is [2]'s. */\n"
      "    const rooted = expect && dr === 1;\n"
      "    if (rooted){\n      const hold = PIN.rootFor;"),
     ("concat(expect && PIN.extraEnt > 0 ?", "concat(rooted && PIN.extraEnt > 0 ?"),
     ("    else if (expect){ inc(\"entOk\");", "    else if (rooted){ inc(\"entOk\");"),
     ("  [3] \"roots ... for a second\": after a rooting blow the opponent's pin is not",
      "  [3] \"roots ... for a second\": after a blow that rooted ([2] reads whether a\n"
      "      blow in the window rooted at all) the opponent's pin is not"),
     ("  [5] \"and entangles it\" (§4 \"+1 on top of the channel's 2\"): a rooted blow",
      "  [5] \"and entangles it\" (§4 \"+1 on top of the channel's 2\"): a blow that rooted")]
for o, n in R:
    assert s.count(o) == 1, o[:60]
    s = s.replace(o, n, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("patched")
