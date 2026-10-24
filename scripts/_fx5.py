import io
p = "docs/software/c/bit-manipulation.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("if (i + 1 < 0) {", "if (i + 1 \u003c 0) {")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed line 66")
