import io
import re

p = "sidebars.ts"
t = io.open(p, encoding="utf-8").read()
before = t.count("\n")

# 删除形如 'software/python/syntax-01', 的分页条目
t = re.sub(r"\n\s+'[^']+-\d\d',", "", t)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("删除行数:", before - t.count("\n"))
