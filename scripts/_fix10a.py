import io
import re

p = "scripts/gen_diagrams10.py"
t = io.open(p, encoding="utf-8").read()

start = t.index("def py_dict():")
end = t.index("def py_mro():")

new_fn = '''def py_dict():
    """Python dict：开放寻址哈希表"""
    fig, ax = plt.subplots(figsize=(10.8, 7.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 9.0)
    ax.set_axis_off()
    ax.text(0.2, 8.6, "Python dict：一个稀疏的哈希表，不是链式桶",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 索引数组
    ax.text(0.4, 7.95, "① 索引数组（大小 = 2 的幂，初始 8）", fontsize=9.4,
            fontweight="bold", color=TEXT)
    n = 8
    for i in range(n):
        x = 0.6 + i * 1.05
        occupied = i in (2, 5, 6)
        color = BLUE if occupied else GREY
        ax.add_patch(Rectangle((x, 7.05), 0.95, 0.6, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 0.475, 7.35, str(i), ha="center", va="center",
                fontsize=9, color=TEXT)
        if occupied:
            ax.text(x + 0.475, 6.85, "→entry %d" % (i - 1), ha="center",
                    fontsize=6.8, color=RED)
    ax.text(9.4, 7.35, "存的是 entries 的下标", fontsize=8, color=RED, va="center")

    # entries 数组（表头 + 3 行）
    ax.text(0.4, 6.35, "② entries 数组（按插入顺序紧凑排列）", fontsize=9.4,
            fontweight="bold", color=TEXT)
    entries = [("hash", "key", "value"), ("h(a)", "a", "1"),
               ("h(b)", "b", "2"), ("h(c)", "c", "3")]
    for i, row in enumerate(entries):
        y = 5.55 - i * 0.44
        for j, cell in enumerate(row):
            x = 0.6 + j * 1.7
            color = PURPLE if i == 0 else GREEN
            ax.add_patch(Rectangle((x, y), 1.6, 0.38, facecolor=color,
                                   edgecolor=DARK, lw=0.9))
            ax.text(x + 0.8, y + 0.19, cell, ha="center", va="center",
                    fontsize=7.6 if i else 8, color=TEXT,
                    fontweight="bold" if i == 0 else "normal")

    # 冲突处理
    ax.text(0.4, 3.5, "③ 哈希冲突：往下一个空位探测（开放寻址，不是链表）",
            fontsize=9.4, fontweight="bold", color=TEXT)
    cues = [
        "hash(a) % 8 = 2  → 放进索引 2",
        "hash(b) % 8 = 2  → 被占了，探测 3、4、5  → 放进 5",
        "hash(c) % 8 = 5  → 被占了，探测 6  → 放进 6",
    ]
    for i, s in enumerate(cues):
        ax.text(0.6, 3.1 - i * 0.34, s, fontsize=8.2, color=TEXT)

    # 右侧要点
    ax.text(8.4, 3.5, "三个必须知道的数字", fontsize=9.6, fontweight="bold", color=TEXT)
    pts = [
        "• 负载因子超过 2/3 就扩容（不是等满）",
        "• 扩容后大小约为已用的 3 倍，且必须是 2 的幂",
        "• 扩容时全部元素重新插入 → 偶发 O(n) 卡顿",
    ]
    for i, s in enumerate(pts):
        ax.text(8.4, 3.1 - i * 0.34, s, fontsize=7.8, color=TEXT)

    # 底部对比
    ax.text(0.4, 1.95, "和 Java HashMap 的关键差异", fontsize=9.4,
            fontweight="bold", color=TEXT)
    rows = [
        ("冲突处理", "开放寻址（往后探测）", "链式桶 + 红黑树"),
        ("内存布局", "两个紧凑数组（缓存友好）", "节点分散 + 指针"),
        ("插入顺序", "保持（3.6+ 的实现副产品）", "不保证"),
    ]
    for i, (k, a, b) in enumerate(rows):
        y = 1.5 - i * 0.36
        ax.text(0.6, y, k, fontsize=8, color=TEXT, fontweight="bold")
        ax.text(2.6, y, "Python: " + a, fontsize=8, color="#1e8449")
        ax.text(7.6, y, "Java: " + b, fontsize=8, color=LINE)

    ax.text(0.4, 0.25,
            "dict 的插入顺序是 entries 数组的副产品，不要把它当成哈希表语言的必然性质。",
            fontsize=8.2, color=LINE)

    _save(fig, "py-dict-hashtable.svg")


'''

t = t[:start] + new_fn + t[end:]
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("rewrote py_dict")