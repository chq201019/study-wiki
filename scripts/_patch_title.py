import io

p = "scripts/auto_split.py"
t = io.open(p, encoding="utf-8").read()

old = '''        raw_head = chunk[0].lstrip("# ").strip() if chunk[0].startswith("#") else f"第 {i+1} 部分"'''
new = '''        if chunk[0].startswith("#"):
            raw_head = chunk[0].lstrip("# ").strip()
        elif i == 0:
            raw_head = fm.get("title", stem)      # 首页开头是导读段落，用文档标题
        else:
            raw_head = f"第 {i+1} 部分"'''

assert old in t, "锚点未找到"
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("已修正首页标题回退")
