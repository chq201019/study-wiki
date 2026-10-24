import io, re, sys

FENCE = "`" * 3
path = sys.argv[1]
lines = io.open(path, encoding="utf-8").read().split("\n")
infence = False
for i, l in enumerate(lines, 1):
    s = l.strip()
    if s.startswith(FENCE):
        infence = not infence
        continue
    if infence:
        continue
    if re.match(r"^:::[a-z]+(\[.*\])?\s*$", s) or s == ":::":
        kind = "CLOSE" if s == ":::" else "OPEN "
        print(f"{i:4}: {kind} {s[:60]}")
