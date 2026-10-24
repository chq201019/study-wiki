import io, glob, os, re

rows = []
for p in glob.glob("docs/**/*.mdx", recursive=True):
    t = io.open(p, encoding="utf-8").read()
    has_img = "/img/diagrams/" in t
    has_mermaid = "```mermaid" in t
    n = len(t.split(chr(10)))
    rows.append((p, n, has_img, has_mermaid))

rows.sort(key=lambda r: -r[1])
total = len(rows)
with_img = sum(1 for r in rows if r[2])
with_mermaid = sum(1 for r in rows if r[3])
print("总页数:", total)
print("已有 svg 图:", with_img)
print("已有 mermaid:", with_mermaid)
print("两者都没有:", sum(1 for r in rows if not r[2] and not r[3]))
print()
print("=== 无图且 >=180 行的页面（配图价值高）===")
c = 0
for p, n, img, mer in rows:
    if not img and n >= 180:
        print("%4d  %s%s" % (n, p.replace(chr(92), "/"), "  [mermaid]" if mer else ""))
        c += 1
        if c >= 45: break