"""检查文档内部相对链接是否指向真实存在的页面。"""
import io, os, re, glob, sys

DOCS = "docs"
ids = set()
for p in glob.glob(os.path.join(DOCS, "**", "*.mdx"), recursive=True):
    rel = os.path.relpath(p, DOCS).replace(os.sep, "/")[:-4]
    ids.add(rel)
    # 也记录目录形式（index）
    if rel.endswith("/index"):
        ids.add(rel[:-6])
    if rel == "index":
        ids.add("")

pat = re.compile(r"\]\((\.[^)\s#]+)\)")
bad = []
for p in glob.glob(os.path.join(DOCS, "**", "*.mdx"), recursive=True):
    t = io.open(p, encoding="utf-8").read()
    base = os.path.dirname(os.path.relpath(p, DOCS)).replace(os.sep, "/")
    for m in pat.finditer(t):
        link = m.group(1)
        if link.startswith("./"):
            target = os.path.normpath(os.path.join(base, link[2:])).replace(os.sep, "/")
        else:
            target = os.path.normpath(os.path.join(base, link)).replace(os.sep, "/")
        target = target[2:] if target.startswith("./") else target
        if target in ids or target + "/index" in ids or target.rstrip("/") + "/index" in ids:
            continue
        # 目录形式：target 是目录，检查 target/index
        if (target + "/index") in ids:
            continue
        bad.append((os.path.relpath(p, DOCS).replace(os.sep, "/"), link, target))

if bad:
    print(f"发现 {len(bad)} 处失效相对链接：")
    for src, link, target in bad:
        print(f"  {src}: {link}  ->  {target}")
    sys.exit(1)
print("所有相对链接有效")
