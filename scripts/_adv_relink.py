"""扫描 docs/chips/stm32 下指向不存在页面的相对链接，并重定向到进阶导读。"""
import io
import os
import re
import glob

D = "docs/chips/stm32"
existing = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(D, "*.mdx"))}

pat = re.compile(r"\]\(\./([A-Za-z0-9\-]+)\)")
total = 0

for p in glob.glob(os.path.join(D, "*.mdx")):
    t = io.open(p, encoding="utf-8").read()
    o = t
    bad = set()
    for m in pat.finditer(t):
        name = m.group(1)
        if name not in existing:
            bad.add(name)
    for name in bad:
        t = t.replace(f"](./{name})", "](./advanced-index)")
        total += 1
        print(f"  {os.path.basename(p)}: ./{name} -> ./advanced-index")

    if t != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)

print(f"重定向 {total} 处")
print("现有页面:", sorted(existing))
