import io
p = "scripts/gen_diagrams12.py"
lines = io.open(p, encoding="utf-8").read().split(chr(10))
# 第 380 行（0-based 379）缺续行
bad = lines[379]
if bad.rstrip().endswith(chr(34) + chr(41)):
    lines[379] = bad.rstrip()[:-1] + chr(44)
    print("fixed line 380")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))