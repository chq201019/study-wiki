"""修正 gen_diagrams4.py 里 4 处版面问题。"""
import io

p = "scripts/gen_diagrams4.py"
t = io.open(p, encoding="utf-8").read()

# ---------- 1) 栈帧：右侧说明右移，rsp/rbp 标注贴近方框 ----------
t = t.replace(
    '''    ax.annotate("rsp（栈顶）", xy=(6.85, 1.45), xytext=(7.6, 1.45),''',
    '''    ax.annotate("rsp（栈顶）", xy=(6.85, 1.45), xytext=(6.95, 1.45),''')
t = t.replace(
    '''    ax.annotate("rbp（栈基址）", xy=(6.85, 3.6), xytext=(7.6, 3.6),''',
    '''    ax.annotate("rbp（栈基址）", xy=(6.85, 3.6), xytext=(6.95, 3.6),''')
t = t.replace('''    ax.text(8.6, 6.6, "三个关键结论"''', '''    ax.text(9.5, 6.6, "三个关键结论"''')
t = t.replace('''        ax.text(8.6, 6.15 - i * 0.42, t, fontsize=8.5, color=TEXT)''',
              '''        ax.text(9.5, 6.15 - i * 0.42, t, fontsize=8.5, color=TEXT)''')

# ---------- 2) 移动语义：buf 方框加宽，避免 nullptr 折行 ----------
t = t.replace('''    box(ax, 0.4, 5.5, 1.5, 0.9, "buf_a", "指针", ORANGE, fs=9)''',
              '''    box(ax, 0.4, 5.5, 1.75, 0.9, "buf_a", "指针", ORANGE, fs=9)''')
t = t.replace('''    arrow(ax, (1.95, 5.95), (3.15, 5.95))''',
              '''    arrow(ax, (2.2, 5.95), (3.15, 5.95))''')
t = t.replace('''    box(ax, 0.4, 4.3, 1.5, 0.9, "buf_b", "指针", ORANGE, fs=9)''',
              '''    box(ax, 0.4, 4.3, 1.75, 0.9, "buf_b", "指针", ORANGE, fs=9)''')
t = t.replace('''    arrow(ax, (1.95, 4.75), (3.15, 4.75))''',
              '''    arrow(ax, (2.2, 4.75), (3.15, 4.75))''')
t = t.replace('''    box(ax, 0.4, 2.35, 1.5, 0.9, "buf_a", "变成 nullptr", GREY, fs=9, sfs=7.5)''',
              '''    box(ax, 0.4, 2.35, 1.75, 0.9, "buf_a", "变成 nullptr", GREY, fs=9, sfs=7.5)''')
t = t.replace('''    box(ax, 0.4, 1.15, 1.5, 0.9, "buf_b", "接管指针", ORANGE, fs=9)''',
              '''    box(ax, 0.4, 1.15, 1.75, 0.9, "buf_b", "接管指针", ORANGE, fs=9)''')
t = t.replace('''    arrow(ax, (1.95, 1.6), (3.15, 1.6))''',
              '''    arrow(ax, (2.2, 1.6), (3.15, 1.6))''')
t = t.replace('''    arrow(ax, (1.95, 2.8), (3.15, 2.8), color=LINE, lw=1.2, ls=":")''',
              '''    arrow(ax, (2.2, 2.8), (3.15, 2.8), color=LINE, lw=1.2, ls=":")''')

# ---------- 3) 进程状态：标签错开 + 标题改成五种 ----------
t = t.replace(
    '''    arrow(ax, (5.0, 5.55), (5.0, 4.35), color=PURPLE)
    ax.text(5.15, 4.9, "Ctrl+Z / SIGSTOP", fontsize=8, color=PURPLE)
    arrow(ax, (6.2, 4.35), (6.2, 5.55), color=LINE)
    ax.text(6.35, 4.9, "SIGCONT", fontsize=8, color=LINE)''',
    '''    arrow(ax, (4.9, 5.55), (4.9, 4.35), color=PURPLE)
    ax.text(3.55, 4.95, "Ctrl+Z / SIGSTOP", fontsize=8, color=PURPLE)
    arrow(ax, (6.3, 4.35), (6.3, 5.55), color=LINE)
    ax.text(6.45, 4.95, "SIGCONT", fontsize=8, color=LINE)''')
t = t.replace('''    ax.text(0.6, 2.5, "三种状态各自的现实含义"''',
              '''    ax.text(0.6, 2.5, "五种状态各自的现实含义"''')

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("已修：栈帧标注 / nullptr 折行 / 进程状态标签与标题")
