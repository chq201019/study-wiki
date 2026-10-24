"""修正 gen_diagrams5.py 里 4 张图的版面问题。"""
import io

p = "scripts/gen_diagrams5.py"
t = io.open(p, encoding="utf-8").read()

# ============ 1) TCP：去掉压字的分隔文字；右栏上移压缩 ----------
t = t.replace(
    '''    ax.text(0.8, 4.85, "—— 上面是三次握手，下面是四次挥手 ——", fontsize=8.6, color=LINE)''',
    '''    ax.text(0.8, 4.72, "上面：三次握手　｜　下面：四次挥手", fontsize=8.4, color=LINE)''')

t = t.replace(
    '''        ax.text(11.2, 3.95 - i * 0.26, s, fontsize=7.5, color=TEXT)''',
    '''        ax.text(11.2, 4.35 - i * 0.245, s, fontsize=7.4, color=TEXT)''')

# 底部说明收窄，避免与右栏最后几行相撞
t = t.replace(
    '''    ax.text(0.4, 0.35,
            "排查工具：ss -tan 看连接状态；tcpdump -i any port 80 看握手过程；"
            "大量 TIME_WAIT 通常是短连接太多，改用长连接或调内核参数。",
            fontsize=8.2, color=LINE)''',
    '''    ax.text(0.4, 0.28,
            "排查工具：ss -tan 看连接状态；tcpdump -i any port 80 看握手过程。",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.02,
            "大量 TIME_WAIT 通常是短连接太多 —— 改用长连接，或调内核参数。",
            fontsize=8.2, color=LINE)''')

# ============ 2) 生成器：箭头指向正确的行；底部文字上移 ----------
t = t.replace(
    '''    arrow(ax, (9.95, 6.55), (4.9, 6.55), color=RED, lw=1.4)
    arrow(ax, (9.95, 5.93), (4.9, 5.0), color=RED, lw=1.4)
    arrow(ax, (9.95, 5.31), (4.9, 3.56), color=RED, lw=1.4)''',
    '''    arrow(ax, (9.95, 6.50), (4.9, 5.56), color=RED, lw=1.4)
    arrow(ax, (9.95, 5.88), (4.9, 4.12), color=RED, lw=1.4)
    arrow(ax, (9.95, 5.26), (4.9, 2.68), color=RED, lw=1.4)''')

t = t.replace(
    '''    ax.text(0.5, 1.3, "三个必须记住的点"''',
    '''    ax.text(0.5, 1.62, "三个必须记住的点"''')
t = t.replace(
    '''        ax.text(0.5, 0.9 - i * 0.34, s, fontsize=8.6, color=TEXT)''',
    '''        ax.text(0.5, 1.20 - i * 0.32, s, fontsize=8.6, color=TEXT)''')
t = t.replace(
    '''    ax.text(0.5, -0.1, "常见的坑：生成器只能迭代一次；要重复用就先 list() 存下来（但这又失去省内存的意义了）。",
            fontsize=8.2, color=RED)''',
    '''    ax.text(0.5, 0.14, "常见的坑：生成器只能迭代一次；要重复用就先 list() 存下来（但这又失去省内存的意义了）。",
            fontsize=8.2, color=RED)''')

# ============ 3) ODR：标签与内容拉开 ----------
t = t.replace(
    '''    ax.text(1.9, 1.02, "multiple definition of 'f()'   ← 头文件里放了普通函数定义，被多个 .cpp 包含",
            fontsize=8.5, color=TEXT)''',
    '''    ax.text(2.5, 1.02, "multiple definition of f()   ← 头文件里放了普通函数定义，被多个 .cpp 包含",
            fontsize=8.5, color=TEXT)''')
t = t.replace(
    '''    ax.text(1.9, 0.62, "undefined reference to 'f()'  ← 声明了但没链接到定义（忘了加 .cpp 或写成 extern C）",
            fontsize=8.5, color=TEXT)''',
    '''    ax.text(2.5, 0.62, "undefined reference to f()  ← 声明了但没链接到定义（忘了加 .cpp 或写成 extern C）",
            fontsize=8.5, color=TEXT)''')

# ============ 4) STM32：加高方框；底部文字错开 ----------
t = t.replace(
    '''    for i, (name, sub, color) in enumerate(mainc):
        y = 6.35 - i * 1.05
        ax.add_patch(Rectangle((6.0, y), 6.6, 0.82, facecolor=color,
                               edgecolor=DARK, lw=1.1))
        ax.text(6.15, y + 0.55, name, fontsize=9, color=TEXT, va="center",
                fontweight="bold")
        ax.text(6.15, y + 0.2, sub, fontsize=7.6, color=TEXT, va="center")
        if i < len(mainc) - 1:
            arrow(ax, (6.3, y), (6.3, y - 0.22), color=LINE, lw=1.2)''',
    '''    for i, (name, sub, color) in enumerate(mainc):
        y = 6.15 - i * 1.12
        ax.add_patch(Rectangle((6.0, y), 6.6, 0.95, facecolor=color,
                               edgecolor=DARK, lw=1.1))
        ax.text(6.15, y + 0.66, name, fontsize=9, color=TEXT, va="center",
                fontweight="bold")
        ax.text(6.15, y + 0.24, sub, fontsize=7.6, color=TEXT, va="center",
                linespacing=1.35)
        if i < len(mainc) - 1:
            arrow(ax, (6.3, y), (6.3, y - 0.14), color=LINE, lw=1.2)''')

t = t.replace(
    '''    for i, s in enumerate(pts):
        ax.text(0.4, 3.05 - i * 0.34, s, fontsize=8.4, color=TEXT)''',
    '''    for i, s in enumerate(pts):
        ax.text(0.4, 3.10 - i * 0.32, s, fontsize=8.4, color=TEXT)''')

t = t.replace(
    '''    ax.text(0.4, 0.35,
            "调试技巧：在 Error_Handler 里打断点，谁跳进来就是谁初始化失败。"
            "这比一路 printf 快得多。",
            fontsize=8.4, color=LINE)''',
    '''    ax.text(0.4, 0.12,
            "调试技巧：在 Error_Handler 里打断点，谁跳进来就是谁初始化失败。"
            "这比一路 printf 快得多。",
            fontsize=8.4, color=LINE)''')

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("已修 4 张图的版面问题")
