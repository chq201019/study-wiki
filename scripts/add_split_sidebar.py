import io
import glob
import os

targets = [
    ("docs/software/python", "syntax"),
    ("docs/software/cpp", "transition"),
    ("docs/software/python", "stdlib"),
    ("docs/software/python", "oop"),
    ("docs/software/python", "concurrency"),
    ("docs/software/cpp", "advanced"),
    ("docs/hardware/linux", "kernel"),
    ("docs/hardware/linux", "shell"),
    ("docs/software/cpp", "templates"),
    ("docs/software/python", "datatypes"),
    ("docs/hardware/linux", "debug"),
    ("docs/software/cpp", "embedded-cpp"),
]

path = "sidebars.ts"
t = io.open(path, encoding="utf-8").read()

added = 0
total_new = 0
for d, stem in targets:
    docid = d.replace("docs/", "") + "/" + stem
    pats = sorted(glob.glob(f"{d}/{stem}-*.mdx"))
    newids = [d.replace("docs/", "") + "/" + os.path.basename(x)[:-4] for x in pats]
    if not newids:
        continue
    needle = "'" + docid + "',\n"
    if needle in t:
        block = needle + "".join("            '" + nid + "',\n" for nid in newids)
        t = t.replace(needle, block, 1)
        added += 1
        total_new += len(newids)
    else:
        print("未在侧边栏找到:", docid)

io.open(path, "w", encoding="utf-8", newline="\n").write(t)
print(f"为 {added} 个原页插入了 {total_new} 个分页条目")
