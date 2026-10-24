import io
p = "scripts/gen_diagrams9.py"
t = io.open(p, encoding="utf-8").read()

# 1) eBPF：分界线下移，不穿 VFS 框
t = t.replace('ax.plot([0.4, 13.2], [4.75, 4.75], color=LINE, lw=1.2, ls="--")',
              'ax.plot([0.4, 6.9], [5.25, 5.25], color=LINE, lw=1.2, ls="--")')
t = t.replace('ax.text(0.4, 4.9, "用户态", fontsize=9, color=LINE)',
              'ax.text(0.4, 5.38, "用户态", fontsize=9, color=LINE)')
t = t.replace('ax.text(0.4, 4.45, "内核态", fontsize=9, color=LINE)',
              'ax.text(0.4, 5.02, "内核态", fontsize=9, color=LINE)')

# 2) ADC：右侧框上移/下移，箭头方向理顺
t = t.replace('box(ax, 9.0, 5.8, 3.8, 0.9, "WiFi 开着时", "ADC2 返回错误或乱数", RED, fs=9, sfs=7.4)',
              'box(ax, 9.6, 5.5, 3.4, 0.85, "WiFi 开着时", "ADC2 返回错误或乱数", RED, fs=8.8, sfs=7.2)')
t = t.replace('box(ax, 9.0, 3.2, 3.8, 0.9, "WiFi 关闭时", "ADC2 正常工作", GREEN, fs=9, sfs=7.4)',
              'box(ax, 9.6, 3.35, 3.4, 0.85, "WiFi 关闭时", "ADC2 正常工作", GREEN, fs=8.8, sfs=7.2)')
t = t.replace('arrow(ax, (7.85, 5.15), (8.95, 6.0), color=RED, lw=1.4)',
              'arrow(ax, (7.85, 5.0), (9.55, 5.75), color=RED, lw=1.4)')
t = t.replace('arrow(ax, (7.85, 4.65), (8.95, 3.8), color="#1e8449", lw=1.4)',
              'arrow(ax, (7.85, 4.55), (9.55, 3.95), color="#1e8449", lw=1.4)')
# WiFi 射频框下移，避免贴边
t = t.replace('box(ax, 1.0, 5.8, 3.2, 0.9, "WiFi 射频", "优先级更高", PINK, fs=9, sfs=7.4)',
              'box(ax, 0.8, 5.65, 3.2, 0.85, "WiFi 射频", "优先级更高", PINK, fs=9, sfs=7.4)')
t = t.replace('arrow(ax, (2.6, 5.75), (5.2, 5.45))', 'arrow(ax, (4.05, 5.85), (5.15, 5.35))')

# 3) RAII：第三第四框重叠，改布局（两行各 3 框）
t = t.replace('''    steps = [
        ("lock_guard 构造", 0.6, GREEN),
        ("临界区代码", 3.0, GREEN),
        ("return", 5.4, GREEN),
        ("lock_guard 析构 → 解锁", 7.2, GREEN),
    ]
    for label, x, c in steps:
        box(ax, x, 5.4, 1.9, 0.72, label, None, c, fs=7.8)
    for i in range(3):
        arrow(ax, (0.6 + [0, 2.4, 4.8][i] + 1.9, 5.76),
              (0.6 + [0, 2.4, 4.8][i] + 2.35, 5.76), lw=1.3)''',
'''    steps = [
        ("lock_guard 构造", 0.6, GREEN),
        ("临界区代码", 3.4, GREEN),
        ("return", 6.2, GREEN),
        ("∽ 析构 → 解锁", 8.6, GREEN),
    ]
    for label, x, c in steps:
        box(ax, x, 5.4, 2.4, 0.72, label, None, c, fs=7.6)
    for x in (3.0, 5.8, 8.6):
        arrow(ax, (x, 5.76), (x + 0.4, 5.76), lw=1.3)''')

t = t.replace('''    steps2 = [
        ("lock_guard 构造", 0.6, ORANGE),
        ("临界区抛出异常", 3.0, RED),
        ("栈展开（unwind）", 5.4, PINK),
        ("析构仍被调用 → 解锁", 7.2, GREEN),
    ]
    for label, x, c in steps2:
        box(ax, x, 3.9, 1.9, 0.72, label, None, c, fs=7.8)
    for i in range(3):
        arrow(ax, (0.6 + [0, 2.4, 4.8][i] + 1.9, 4.26),
              (0.6 + [0, 2.4, 4.8][i] + 2.35, 4.26), lw=1.3)''',
'''    steps2 = [
        ("lock_guard 构造", 0.6, ORANGE),
        ("临界区抛异常", 3.4, RED),
        ("栈展开 unwind", 6.2, PINK),
        ("∽ 析构 → 解锁", 8.6, GREEN),
    ]
    for label, x, c in steps2:
        box(ax, x, 3.9, 2.4, 0.72, label, None, c, fs=7.6)
    for x in (3.0, 5.8, 8.6):
        arrow(ax, (x, 4.26), (x + 0.4, 4.26), lw=1.3)''')

t = t.replace('ax.text(9.5, 4.26, "这是语言保证"', 'ax.text(11.2, 4.26, "这是语言保证"')

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("patched")
