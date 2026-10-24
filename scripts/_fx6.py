import io
p = "docs/software/c/bit-manipulation.mdx"
t = io.open(p, encoding="utf-8").read()
rep = [
    ("| 置位 | `x |= (1u << n)` |", "| 置位 | `x |= (1u \\u003c\\u003c n)` |"),
    ("| 清位 | `x &= ~(1u << n)` |", "| 清位 | `x \\u0026= ~(1u \\u003c\\u003c n)` |"),
    ("| 取反某位 | `x ^= (1u << n)` |", "| 取反某位 | `x ^= (1u \\u003c\\u003c n)` |"),
    ("| 判位 | `if (x & (1u << n))` |", "| 判位 | `if (x \\u0026 (1u \\u003c\\u003c n))` |"),
]
for a, b in rep:
    if a in t:
        t = t.replace(a, b)
        print("fixed:", a[:30])
    else:
        print("MISS:", a[:30])
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
