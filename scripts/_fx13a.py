import io
p = "scripts/gen_diagrams13.py"
t = io.open(p, encoding="utf-8").read()

start = t.index("def makefile_graph():")
end = t.index("# ---------- pytest fixture 作用域 ----------")

new_fn = '''def makefile_graph():
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "Make 怎么判断「要不要重编」：只看时间戳",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 三层结构，纵向排列，对齐清晰
    box(ax, 3.0, 6.3, 3.2, 0.72, "app", "最终可执行", GREEN, fs=9.5, sfs=7.2)
    box(ax, 1.2, 4.8, 2.6, 0.72, "main.o", None, BLUE, fs=9)
    box(ax, 5.0, 4.8, 2.6, 0.72, "util.o", None, BLUE, fs=9)
    box(ax, 9.0, 4.8, 2.2, 0.72, "Makefile", None, PURPLE, fs=8.6)

    box(ax, 1.2, 3.3, 2.6, 0.72, "main.c", None, ORANGE, fs=9)
    box(ax, 5.0, 3.3, 2.6, 0.72, "util.c", None, ORANGE, fs=9)
    box(ax, 1.2, 2.0, 2.6, 0.66, "util.h", None, PINK, fs=9)
    box(ax, 5.0, 2.0, 2.6, 0.66, "config.h", None, PINK, fs=9)

    # app 的依赖
    arrow(ax, (2.5, 5.55), (4.0, 6.25))
    arrow(ax, (6.3, 5.55), (4.9, 6.25))
    arrow(ax, (9.0, 5.16), (6.2, 6.35))

    # .o 来自 .c
    arrow(ax, (2.5, 4.05), (2.5, 4.75))
    arrow(ax, (6.3, 4.05), (6.3, 4.75))

    # .h 被 .c 包含
    arrow(ax, (2.5, 2.66), (2.5, 3.25), color=PINK, ls=":")
    arrow(ax, (5.0, 2.33), (5.0, 3.25), color=PINK, ls=":")

    ax.text(0.4, 1.45, "判断规则", fontsize=9.6, fontweight="bold", color=TEXT)
    ax.text(0.4, 1.12,
            "依赖比目标新（mtime 更晚）就重新生成；什么都不改就跳过。",
            fontsize=8.4, color=TEXT)
    ax.text(0.4, 0.78,
            "改 util.c 会让 util.o 重编、app 重新链接；改 util.h 呢？——只有加了 -MMD 才会。",
            fontsize=8.4, color=RED)

    ax.text(7.6, 2.55, "头文件依赖必须自动生成", fontsize=9.2,
            fontweight="bold", color=RED)
    ax.text(7.6, 2.2, "编译时加 -MMD -MP，", fontsize=7.8, color=TEXT)
    ax.text(7.6, 1.92, "再 -include $(DEPS)", fontsize=7.8, color=TEXT)
    ax.text(7.6, 1.55, "否则改头文件不会触发", fontsize=7.8, color=TEXT)
    ax.text(7.6, 1.27, "任何重编 —— 你看到的是旧行为。", fontsize=7.8, color=TEXT)

    ax.text(0.4, 0.35, "三个最容易踩的坑", fontsize=9, fontweight="bold", color=RED)
    ax.text(0.4, 0.05,
            "① 命令必须 TAB 开头　② 忘了 -MMD 改头文件不重编　③ 改 Makefile 本身不触发重编（要把它加进依赖）",
            fontsize=7.6, color=TEXT)

    _save(fig, "c-makefile-graph.svg")


'''

t = t[:start] + new_fn + t[end:]
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("rewrote makefile_graph")
