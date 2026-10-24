import io
p = "scripts/gen_diagrams13.py"
t = io.open(p, encoding="utf-8").read()

# 方框宽 2.5，间距改为 2.9；箭头从 x+2.5 到 x+2.85（留 0.35 空隙）
t = t.replace('("源文件", "main.c（10 行）", BLUE, 0.6),',
              '("源文件", "main.c（10 行）", BLUE, 0.5),')
t = t.replace('("展开 #include", "stdio.h 递归展开", ORANGE, 3.4),',
              '("展开 #include", "stdio.h 递归展开", ORANGE, 3.3),')
t = t.replace('("展开 #define", "宏文本替换（可能嵌套）", PINK, 6.2),',
              '("展开 #define", "宏文本替换（可能嵌套）", PINK, 6.1),')
t = t.replace('("输出 .i", "约 1750 行", GREEN, 9.0),',
              '("输出 .i", "约 1750 行", GREEN, 8.9),')
t = t.replace('        if x < 9.0:\n            arrow(ax, (x + 2.55, 5.65), (x + 3.3, 5.65), color=RED, lw=1.5)',
              '        if x < 8.9:\n            arrow(ax, (x + 2.55, 5.65), (x + 2.75, 5.65), color=RED, lw=1.5)')
# 方框宽改 2.4
t = t.replace('        ax.add_patch(Rectangle((x, 5.1), 2.5, 1.1, facecolor=color,',
              '        ax.add_patch(Rectangle((x, 5.1), 2.4, 1.1, facecolor=color,')
t = t.replace('        ax.text(x + 1.25, 5.85, name,', '        ax.text(x + 1.2, 5.85, name,')
t = t.replace('        ax.text(x + 1.25, 5.42, desc,', '        ax.text(x + 1.2, 5.42, desc,')

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("adjusted spacing")
