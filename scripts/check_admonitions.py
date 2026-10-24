import io, re, sys, os, glob

FENCE = "`" * 3

def check(path):
    txt = io.open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    depth = 0
    bad = []
    infence = False
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith(FENCE):
            infence = not infence
            continue
        if infence:
            continue
        if re.match(r"^:::[a-z]+(\[.*\])?\s*$", s):
            depth += 1
            if depth > 1:
                bad.append((i, s[:45]))
        elif s == ":::":
            depth -= 1
            if depth < 0:
                bad.append((i, "多余闭合"))
                depth = 0
    return depth, bad

for p in sorted(glob.glob("docs/software/c-basics/*.mdx")):
    d, b = check(p)
    status = "OK" if d == 0 and not b else "问题"
    print(f"{os.path.basename(p):26} depth={d:2} {status}")
    for ln, s in b[:4]:
        print(f"    行{ln}: {s}")
