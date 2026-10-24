import io
p = "docs/software/c/bit-manipulation.mdx"
t = io.open(p, encoding="utf-8").read()
F = "`"
# 用 &#124; 表示表格里的管道符，代码内容保持原样
rep = [
    ("| 置位 | " + F + "x \\u003c\\u003c= (1u \\u003c\\u003c n)" + F + " |",
     "| 置位 | " + F + "x &#124;= (1u << n)" + F + " |"),
    ("| 清位 | " + F + "x \\u0026= ~(1u \\u003c\\u003c n)" + F + " |",
     "| 清位 | " + F + "x &= ~(1u << n)" + F + " |"),
    ("| 取反某位 | " + F + "x ^= (1u \\u003c\\u003c n)" + F + " |",
     "| 取反某位 | " + F + "x ^= (1u << n)" + F + " |"),
    ("| 判位 | " + F + "if (x \\u0026 (1u \\u003c\\u003c n))" + F + " |",
     "| 判位 | " + F + "if (x & (1u << n))" + F + " |"),
]
for a, b in rep:
    if a in t:
        t = t.replace(a, b); print("ok")
    else:
        print("MISS:", a[:40])
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
