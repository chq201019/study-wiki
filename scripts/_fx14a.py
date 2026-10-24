import io
p = "docs/software/cpp/templates-01.mdx"
t = io.open(p, encoding="utf-8").read()
old = "模板实例化：max<T> 是图纸，编译器为 int/double/char 各生成一份独立机器码"
new = "模板实例化：max 模板是图纸，编译器为 int / double / char 各生成一份独立机器码"
if old in t:
    t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
    print("fixed alt text")
else:
    print("MISS")