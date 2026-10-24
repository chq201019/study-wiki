import io
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "docs/chips/stm32/watchdog.mdx"
lines = io.open(path, encoding="utf-8").read().split("\n")

FENCE = "`" * 3
depth = 0
infence = False
for i, l in enumerate(lines, 1):
    s = l.strip()
    if s.startswith(FENCE):
        infence = not infence
        continue
    if infence:
        continue
    if s.startswith(":::"):
        if s == ":::":
            depth -= 1
            print(f"{i:4d}  CLOSE      depth={depth}")
        else:
            depth += 1
            print(f"{i:4d}  OPEN       depth={depth}  {s[:56]}")
print("final depth =", depth)
