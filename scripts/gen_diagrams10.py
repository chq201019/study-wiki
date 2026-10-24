"""第十批示意图：数据结构与内存布局（A 批）。

用法: python scripts/gen_diagrams10.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
from matplotlib import font_manager, rcParams

OUT = os.path.join("static", "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

for _f in ["Microsoft YaHei", "Noto Sans SC", "SimHei", "Source Han Sans SC"]:
    if any(x.name == _f for x in font_manager.fontManager.ttflist):
        rcParams["font.sans-serif"] = [_f]
        break
rcParams["axes.unicode_minus"] = False
rcParams["text.parse_math"] = False

BLUE, PINK, ORANGE = "#7fb3d5", "#e8b4b8", "#f5cba7"
GREEN, PURPLE, GREY = "#a9dfbf", "#d2b4de", "#d5dbdb"
TEXT, LINE, RED, DARK = "#1b2631", "#5d6d7e", "#c0392b", "#2c3e50"


def _save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, label, sub=None, color=BLUE, fs=10, sfs=8, lw=1.2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=DARK,
                           linewidth=lw, alpha=0.92))
    if sub:
        ax.text(x + w / 2, y + h * 0.66, label, ha="center", va="center",
                fontsize=fs, color=TEXT, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center",
                fontsize=sfs, color=TEXT, linespacing=1.3)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=TEXT, fontweight="bold")


def arrow(ax, p1, p2, color=RED, lw=1.6, style="-|>", ms=14, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls))


def py_dict():
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


def py_mro():
    """Python MRO 线性化"""
    fig, ax = plt.subplots(figsize=(10.8, 7.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 9.4)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "菱形继承：MRO 让查找顺序唯一且可预测",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 菱形
    box(ax, 3.4, 6.3, 2.6, 0.7, "object", None, GREY, fs=9)
    box(ax, 1.4, 4.9, 2.6, 0.7, "A", "def hello()", BLUE, fs=9, sfs=7.4)
    box(ax, 5.4, 4.9, 2.6, 0.7, "B", "def hello()", PINK, fs=9, sfs=7.4)
    box(ax, 3.4, 3.5, 2.6, 0.7, "C(A, B)", None, GREEN, fs=9)
    arrow(ax, (4.7, 5.6), (4.7, 6.25), color=LINE, lw=1.3)
    arrow(ax, (6.7, 5.6), (6.7, 6.25), color=LINE, lw=1.3)
    arrow(ax, (4.7, 4.2), (3.0, 4.85), color=LINE, lw=1.3)
    arrow(ax, (4.9, 4.2), (6.5, 4.85), color=LINE, lw=1.3)

    # MRO 序列
    ax.text(9.2, 6.3, "C.__mro__", fontsize=9.6, fontweight="bold", color=TEXT)
    seq = ["C", "A", "B", "object"]
    for i, s in enumerate(seq):
        y = 5.75 - i * 0.52
        ax.add_patch(Rectangle((9.2, y), 1.0, 0.42, facecolor=ORANGE,
                               edgecolor=DARK, lw=1.0))
        ax.text(9.7, y + 0.21, s, ha="center", va="center", fontsize=8.6,
                color=TEXT, fontweight="bold")
        if i < len(seq) - 1:
            ax.text(9.55, y - 0.14, "↓", fontsize=8, color=LINE)

    ax.text(10.5, 5.75, "第一个找到的", fontsize=7.8, color=RED)
    ax.text(10.5, 5.45, "hello() 就用它", fontsize=7.8, color=RED)

    # 解释
    ax.text(0.4, 2.85,"为什么不是简单的深度优先", fontsize=9.8,
            fontweight="bold", color=TEXT)
    pts = [
        "朴素深度优先会得到 C → A → object → B —— 但 object 在 B 之前，",
        "会破坏 B 的约定（B 也应该在 object 之前被检查）。",
        "",
        "C3 线性化保证：",
        "① 子类永远在父类之前",
        "② 多个父类的相对顺序保持不变（C(A,B) 里 A 在 B 前）",
        "③ 单调性：父类的 MRO 顺序在子类里不被破坏",
        "",
        "所以正确结果是 C → A → B → object，C.hello() 调用的是 A 的版本。",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 2.50 - i * 0.28, s, fontsize=8.2, color=TEXT)

    ax.text(0.4, -0.25,
            "查 C.__mro__ 就能看到实际顺序；super() 就是在 MRO 上「往后找一个」。",
            fontsize=8.2, color=LINE)

    _save(fig, "py-mro.svg")


def c_enum_union():
    """enum / union / struct 的内存对比"""
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "enum / union / struct：三种聚合，三种内存布局",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # struct
    ax.text(0.4, 6.6, "struct：各成员依次排列（含填充）", fontsize=9.4,
            fontweight="bold", color=TEXT)
    fields = [("int a", 2.2, BLUE), ("(填充)", 0.7, GREY), ("char b", 1.0, PINK),
              ("(填充)", 0.7, GREY), ("int c", 2.2, BLUE)]
    x = 0.6
    for label, w, color in fields:
        ax.add_patch(Rectangle((x, 5.75), w, 0.62, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        fs = 7.4 if len(label) > 5 else 8
        ax.text(x + w / 2, 6.06, label, ha="center", va="center",
                fontsize=fs, color=TEXT)
        x += w
    ax.text(x + 0.2, 6.06, "= 12 字节", fontsize=8.6, color=RED, va="center")

    # union
    ax.text(0.4, 5.15, "union：所有成员共用同一块内存（大小 = 最大成员）",
            fontsize=9.4, fontweight="bold", color=TEXT)
    for i, (label, color) in enumerate([("int i", BLUE), ("float f", PINK),
                                        ("char s[8]", ORANGE)]):
        y = 4.55 - i * 0.36
        ax.add_patch(Rectangle((0.6, y), 2.2, 0.3, facecolor=color,
                               edgecolor=DARK, lw=0.9, alpha=0.75))
        ax.text(3.0, y + 0.15, label + "（重叠在同一块）", fontsize=7.6,
                color=TEXT, va="center")
    ax.add_patch(Rectangle((0.6, 4.55 - 2 * 0.36), 2.2, 0.3 + 2 * 0.36,
                           facecolor="none", edgecolor=RED, lw=1.6, ls="--"))
    ax.text(0.6, 3.35, "union 大小 = 8 字节（char s[8] 最大）", fontsize=8.4,
            color=RED)

    # enum
    ax.text(0.4, 2.95, "enum：本质就是整数，大小通常等于 int",
            fontsize=9.4, fontweight="bold", color=TEXT)
    vals = [("RED", "0"), ("GREEN", "1"), ("BLUE", "2")]
    for i, (name, v) in enumerate(vals):
        x = 0.6 + i * 2.2
        ax.add_patch(Rectangle((x, 2.25), 1.9, 0.5, facecolor=GREEN,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 0.95, 2.5, name + " = " + v, ha="center", va="center",
                fontsize=8, color=TEXT)
    ax.text(7.4, 2.5, "sizeof(enum) 通常 = 4 字节", fontsize=8.4,
            color=TEXT, va="center")

    # 三个陷阱
    ax.text(0.4, 1.75, "三个最常见的错", fontsize=9.6, fontweight="bold", color=RED)
    pts = [
        "① 用 union 读「另一个成员」= 类型双关，C 里是未定义行为（C++ 更严格）",
        "② struct 忘了对齐，从 12 字节变成理论上的 9 字节 —— 用 pack 会牺牲访问速度",
        "③ enum 的底层类型由实现决定，负数或超大值可能改变大小",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 1.35 - i * 0.32, s, fontsize=8, color=TEXT)

    ax.text(0.4, 0.25,
            "验证手段：sizeof 三个类型 + offsetof 每个成员，自己量一遍比记规则可靠。",
            fontsize=8.2, color=LINE)

    _save(fig, "c-enum-union.svg")


if __name__ == "__main__":
    py_dict()
    py_mro()
    c_enum_union()
    print("done")