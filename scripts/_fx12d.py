import io
p = "scripts/gen_diagrams12.py"
t = io.open(p, encoding="utf-8").read()

old_start = t.index('    # 计数器递减轴')
old_end = t.index('    # 说明', old_start)

new_block = '''    # 计数器递减轴（左边是计数值小=快到期，右边是0x7F刚开始）
    ax.annotate("", xy=(12.4, 5.0), xytext=(0.8, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.4))
    ax.text(12.5, 4.65, "时间", fontsize=8, color=LINE)

    zones = [
        (0.8, 2.0, PINK, "0x3F 复位"),
        (2.8, 5.6, GREEN, "允许喂的窗口"),
        (8.4, 4.0, RED, "太早喂 也复位"),
    ]
    for x, w, color, label in zones:
        ax.add_patch(Rectangle((x, 4.55), w, 0.9, facecolor=color,
                               edgecolor=DARK, lw=1.2, alpha=0.85))
        ax.text(x + w / 2, 3.92, label, ha="center", fontsize=8.2,
                color=TEXT, fontweight="bold")

    ticks = [("0x3F 复位", 2.0), ("0x40 下限", 2.85),
             ("0x50 窗口上限", 8.35), ("0x7F 起始", 12.3)]
    for label, x in ticks:
        ax.plot([x, x], [4.4, 5.6], color=DARK, lw=1.0, ls=":")
        ax.text(x, 5.72, label, ha="center", fontsize=7.2, color=TEXT)

    ax.text(0.8, 3.55, "← 计数递减方向", fontsize=7.6, color=LINE)
'''
t = t[:old_start] + new_block + t[old_end:]
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("rewrote wwdg axis")
