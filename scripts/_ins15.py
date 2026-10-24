import io, os

ITEMS = [
    ("docs/software/python/datatypes-01.mdx", "### 为什么必须扩容",
     "py-list-growth-curve.svg",
     "Python list 容量增长：第一次 append 分配 4 个槽位，之后按约 1.125 倍加常数扩容，均摊 O(1) 但偶发 O(n)"),
    ("docs/software/c/pointers.mdx", "## 数组名与指针的区别",
     "c-pointer-array-detail.svg",
     "数组名不是指针：sizeof(arr) 是 20 而 sizeof(&arr[0]) 是 8，数组传参会退化成指针丢失长度信息"),
]

ok = 0
for path, anchor, img, alt in ITEMS:
    if not os.path.exists(path):
        print("MISSING", path); continue
    lines = io.open(path, encoding="utf-8").read().split(chr(10))
    idx = None
    for i, l in enumerate(lines):
        if l.strip() == anchor.strip():
            idx = i; break
    if idx is None:
        print("ANCHOR MISS", path); continue
    if img in chr(10).join(lines):
        print("EXISTS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path); ok += 1
print("inserted", ok)