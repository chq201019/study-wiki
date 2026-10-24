import io
p = "docs/software/c/bit-manipulation.mdx"
t = io.open(p, encoding="utf-8").read()
old = "| 置位 | `x |= (1u \\u003c\\u003c n)` |"
new = "| 置位 | `x &#124;= (1u << n)` |"
if old in t:
    t = t.replace(old, new); print("fixed")
else:
    print("MISS")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
