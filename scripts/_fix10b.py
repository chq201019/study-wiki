import io
p = "scripts/gen_diagrams10.py"
t = io.open(p, encoding="utf-8").read()

old_head = """def py_mro():
    \"\"\"Python MRO 线性化\"\"\"
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)"""
new_head = """def py_mro():
    \"\"\"Python MRO 线性化\"\"\"
    fig, ax = plt.subplots(figsize=(10.8, 7.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 9.2)"""
assert old_head in t
t = t.replace(old_head, new_head, 1)

# 整体上移文字块，底部说明下移到 y=0.18 以下留白
t = t.replace('ax.text(0.4, 2.85, "为什么不是简单的深度优先",
              'ax.text(0.4, 2.55, "为什么不是简单的深度优先",
t = t.replace("        ax.text(0.4, 2.45 - i * 0.28, s, fontsize=8.2, color=TEXT)",
              "        ax.text(0.4, 2.15 - i * 0.28, s, fontsize=8.2, color=TEXT)")
t = t.replace('''    ax.text(0.4, 0.3,
            "查 C.__mro__ 就能看到实际顺序；super() 就是在 MRO 上「往后找一个」。",
            fontsize=8.2, color=LINE)''',
              '''    ax.text(0.4, 0.12,
            "查 C.__mro__ 就能看到实际顺序；super() 就是在 MRO 上「往后找一个」。",
            fontsize=8.2, color=LINE)''')

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("patched py_mro")