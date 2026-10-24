import io
import re

p = "scripts/auto_split.py"
t = io.open(p, encoding="utf-8").read()

# 1) 清理标题：去掉原小节标题开头的编号
helper = '''
def clean_title(raw):
    """去掉标题开头的编号（如 '6. '、'3 '、'二、'），保留实质内容。"""
    s = raw.strip()
    s = re.sub(r"^[0-9]+(\\.[0-9]+)*[\\.、\\s]+", "", s)
    s = re.sub(r"^[一二三四五六七八九十]+、", "", s)
    return s.strip() or raw.strip()


'''
t = t.replace("def read(path):", helper + "def read(path):", 1)

# 2) 页面标题与去重
old = '''        title = chunk[0].lstrip("# ").strip() if chunk[0].startswith("#") else f"{i+1}"
        # 页面标题用「NN 原标题」
        title = f"{i+1:02d} {title}" if not title[:2].isdigit() else title

        desc = f"{fm.get('title', stem)} 第 {i+1} 部分：{title}"
'''
new = '''        raw_head = chunk[0].lstrip("# ").strip() if chunk[0].startswith("#") else f"第 {i+1} 部分"
        core = clean_title(raw_head)
        title = f"{i+1:02d} {core}"

        # 首个标题行与页面 H1 重复，去掉
        if chunk and chunk[0].startswith("#"):
            chunk.pop(0)
            while chunk and chunk[0].strip() == "":
                chunk.pop(0)

        desc = f"{fm.get('title', stem)} 第 {i+1} 部分：{core}"
        titles.append(core)
'''
assert old in t, "title 锚点未找到"
t = t.replace(old, new, 1)

# 3) titles 列表初始化
t = t.replace("    ids = [f\"{stem}-{i:02d}\" for i in range(1, len(pages) + 1)]",
              "    ids = [f\"{stem}-{i:02d}\" for i in range(1, len(pages) + 1)]\n    titles = []", 1)

# 4) 导读表带标题
old_hub = '''    for i in range(len(pages)):
        hub.append(f"| {i+1} | [第 {i+1} 部分](./{ids[i]}) |")'''
new_hub = '''    for i in range(len(pages)):
        name = titles[i] if i < len(titles) else f"第 {i+1} 部分"
        hub.append(f"| {i+1} | [{name}](./{ids[i]}) |")'''
assert old_hub in t, "hub 表锚点未找到"
t = t.replace(old_hub, new_hub, 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("脚本已改进：标题去编号 / 去重复标题 / 导读表带标题")
