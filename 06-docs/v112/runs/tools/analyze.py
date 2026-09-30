import sys, re, collections
sys.path.insert(0, "C:/dev/sundered-crown/tools")
import heartwood_build as HB
WRITE = r"\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)"
RECV = r"(?<![\w$.])((?:this|[A-Za-z_$][\w$]*)(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*)"
for label, old, new in HB.S6:
    ins = HB.strip_comments(new.replace(old, "", 1) if old in new else new)
    print("=====", label)
    calls = collections.Counter()
    for mc in re.finditer(r"([\w$]+)\s*\(", ins):
        name = mc.group(1); j = mc.start() - 1
        while j >= 0 and ins[j] in " \t": j -= 1
        if j >= 0 and ins[j] == ".":
            k = j - 1
            while k >= 0 and ins[k] in " \t": k -= 1
            if ins[k] in ")]": recv = ins[k]
            else:
                m2 = re.search(r"((?:[\w$]+\s*\.\s*)*[\w$]+)\s*$", ins[:k+1]); recv = re.sub(r"\s+", "", m2.group(1))
        else: recv = None
        calls[(recv, name)] += 1
    print("CALLS", sorted(calls.items(), key=lambda x: str(x)))
    w = collections.Counter()
    for mw in re.finditer(RECV + r"\s*\.\s*([A-Za-z_$][\w$]*)" + WRITE, ins):
        w[(re.sub(r"\s+", "", mw.group(1)), mw.group(2))] += 1
    for mw in re.finditer(r"(?:\+\+|--)\s*" + RECV + r"\s*\.\s*([A-Za-z_$][\w$]*)", ins):
        w[("PRE " + re.sub(r"\s+", "", mw.group(1)), mw.group(2))] += 1
    print("WRITES", sorted(w.items(), key=lambda x: str(x)))
    print("IDX", re.findall(RECV + r"\s*\[([^\]]*)\]" + WRITE, ins))
    print("BARE-ASSIGN", sorted(set(re.findall(r"(?<![\w$.\]\)])([A-Za-z_$][\w$]*)\s*(?:=(?![=>])|\+=|-=|\*=|/=|\+\+|--)", ins))))
    print("ARROWS", re.findall(r"[^\n]*=>[^\n]*", ins))
    print("TABLES", sorted(set(re.findall(r"\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES|SFX|AC)\b(?:\s*\.\s*[A-Za-z_$][\w$]*)*", ins))))
    print("DECL", sorted(set(re.findall(r"\b(?:const|let|var)\s+([^;=]+?)\s*=", ins)))[:40])
