"""
C 零基础教程配套示意图（第二批）

设计原则：只用 matplotlib 画 mermaid 表达不了或会失真的图——
需要精确的地址/偏移/内存格子的图。

用法: python scripts/gen_diagrams_c.py
输出: static/img/diagrams/*.svg
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import font_manager, rcParams

OUT = os.path.join("static", "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

for _f in ["Microsoft YaHei", "Noto Sans SC", "SimHei", "Source Han Sans SC"]:
    if any(x.name == _f for x in font_manager.fontManager.ttflist):
        rcParams["font.sans-serif"] = [_f]
        break
rcParams["axes.unicode_minus"] = False

C_DATA = "#7fb3d5"
C_PAD = "#e8b4b8"
C_PTR = "#f5cba7"
C_NODE = "#a9dfbf"
C_TEXT = "#1b2631"
C_GRID = "#5d6d7e"
C_RED = "#c0392b"


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", path)


def box(ax, x, y, w, h, label, sub=None, color=C_DATA, fs=10, sfs=8, lw=1.2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="#2c3e50",
                           linewidth=lw, alpha=0.9))
    if sub:
        ax.text(x + w / 2, y + h * 0.64, label, ha="center", va="center",
                fontsize=fs, color=C_TEXT, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.26, sub, ha="center", va="center",
                fontsize=sfs, color=C_TEXT, linespacing=1.25)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=C_TEXT, fontweight="bold")


def linked_list():
    """链表结构：value + next，节点分散在堆上，靠指针串起来"""
    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 6.0)
    ax.set_axis_off()

    ax.text(0.2, 5.5, "链表：节点分散在堆上，用 next 指针串起来",
            fontsize=12, fontweight="bold", color=C_TEXT)

    # head 指针变量
    box(ax, 0.3, 3.4, 1.5, 0.95, "head", "栈上", C_PTR, fs=10, sfs=7.5)

    nodes = [
        (2.6, "1", "0x1A0"), (5.0, "2", "0x240"), (7.4, "3", "0x2E0"),
        (9.8, "4", "0x380"),
    ]
    for i, (x, val, addr) in enumerate(nodes):
        # value 格
        box(ax, x, 3.4, 0.95, 0.95, "value", None, C_NODE, fs=8.5)
        ax.text(x + 0.475, 3.55, val, ha="center", va="center",
                fontsize=13, color=C_TEXT, fontweight="bold")
        # next 格
        box(ax, x + 0.95, 3.4, 1.0, 0.95, "next", None, C_DATA, fs=8.5)
        # 地址标注
        ax.text(x + 0.95, 3.15, addr, ha="center", va="center",
                fontsize=7, color=C_GRID)
        ax.text(x + 0.95, 4.55, f"节点{i+1}", ha="center", va="center",
                fontsize=8.5, color=C_TEXT)

    # 箭头：head -> 节点1
    ax.add_patch(FancyArrowPatch((1.85, 3.88), (2.55, 3.88),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color=C_RED, lw=1.6))
    # 节点间箭头
    for i in range(3):
        x0 = nodes[i][0] + 1.95
        x1 = nodes[i + 1][0]
        ax.add_patch(FancyArrowPatch((x0, 3.88), (x1, 3.88),
                                     arrowstyle="-|>", mutation_scale=14,
                                     color=C_RED, lw=1.6))

    # 最后一个指向 NULL
    ax.text(nodes[-1][0] + 1.95, 3.88, "NULL", ha="left", va="center",
            fontsize=10, color=C_RED, fontweight="bold")
    ax.add_patch(FancyArrowPatch((nodes[-1][0] + 1.95, 3.88),
                                 (11.55, 3.88), arrowstyle="-|>",
                                 mutation_scale=14, color=C_RED, lw=1.6))

    # 说明
    notes = [
        "• 每个节点用 malloc 单独分配，地址不连续（上面是示意地址）",
        "• head 只是一个指针变量，存在栈上，指向第一个节点",
        "• 最后一个节点的 next 必须是 NULL，遍历靠它判断结束",
        "• 插入/删除只需改指针，O(1)；但随机访问要逐个走，O(n)",
    ]
    for i, t in enumerate(notes):
        ax.text(0.3, 2.3 - i * 0.42, t, fontsize=9.2, color=C_TEXT)

    # 对比数组
    ax.text(0.3, 0.15, "对比：数组是连续内存，arr[i] 直接算地址 O(1)",
            fontsize=9, color=C_GRID, style="italic")

    _save(fig, "c-linked-list.svg")


def pointer_memory():
    """指针与内存：变量、地址、解引用的关系"""
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 6.8)
    ax.set_axis_off()

    ax.text(0.2, 6.35, "指针 = 存着「地址」的变量", fontsize=12.5,
            fontweight="bold", color=C_TEXT)

    # 左侧：普通变量 n
    ax.text(1.5, 5.65, "变量 n", fontsize=10.5, fontweight="bold",
            color=C_TEXT, ha="center")
    box(ax, 0.5, 4.3, 2.0, 1.0, "42", None, C_DATA, fs=17)
    ax.text(1.5, 4.05, "地址 0x7ffd…10", ha="center", fontsize=8.5,
            color=C_GRID)

    # 右侧：指针变量 p
    ax.text(7.2, 5.65, "变量 p（指针）", fontsize=10.5, fontweight="bold",
            color=C_TEXT, ha="center")
    box(ax, 5.6, 4.3, 3.2, 1.0, "0x7ffd…10", None, C_PTR, fs=12)
    ax.text(7.2, 4.05, "地址 0x7ffd…40（它自己也有地址）", ha="center",
            fontsize=8.5, color=C_GRID)

    # 箭头 p -> n
    ax.add_patch(FancyArrowPatch((5.55, 4.8), (2.6, 4.8),
                                 arrowstyle="-|>", mutation_scale=17,
                                 color=C_RED, lw=2.0))
    ax.text(4.05, 5.05, "p 存的值就是 n 的地址", fontsize=9,
            color=C_RED, ha="center", fontweight="bold")

    # 三个操作说明
    ops = [
        ("&n", "取地址：得到 n 的地址", "printf(\"%p\", (void*)&n)"),
        ("int *p = &n;", "声明指针并让它指向 n", "p 现在\"认识\"n"),
        ("*p", "解引用：顺着地址找到 n", "*p = 99;  // 改的就是 n"),
    ]
    ax.text(0.3, 3.3, "三个核心操作", fontsize=11, fontweight="bold",
            color=C_TEXT)
    for i, (sym, desc, code) in enumerate(ops):
        y = 2.75 - i * 0.85
        ax.text(0.5, y, sym, fontsize=10.5, color=C_RED,
                fontweight="bold")
        ax.text(2.6, y + 0.1, desc, fontsize=9.5, color=C_TEXT)
        ax.text(2.6, y - 0.27, code, fontsize=8.5, color=C_GRID)

    ax.text(0.3, 0.2,
            "关键：p 自己也是一个变量，占 8 字节；它存的是别人的地址",
            fontsize=9.2, color=C_GRID, style="italic")

    _save(fig, "c-pointer-memory.svg")


def bitops():
    """位运算：置位/清位/掩码提取，逐位对照"""
    fig, ax = plt.subplots(figsize=(10.4, 7.4))
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 10.4)
    ax.set_axis_off()

    ax.text(0.2, 9.95, "位运算：对单个比特操作", fontsize=12.5,
            fontweight="bold", color=C_TEXT)

    BITS = 8
    bw = 0.62
    X0 = 3.4
    ROWH = 0.62

    def draw_row(y, label, bits, highlight=None, note=""):
        ax.text(0.15, y + ROWH / 2, label, fontsize=9.2, color=C_TEXT,
                va="center")
        for i, b in enumerate(bits):
            x = X0 + i * bw
            hl = (highlight is not None and i in highlight)
            color = C_PAD if hl else ("#d6eaf8" if b == "0" else C_DATA)
            ax.add_patch(Rectangle((x, y), bw - 0.05, ROWH,
                                   facecolor=color, edgecolor="#2c3e50",
                                   lw=1.0))
            ax.text(x + (bw - 0.05) / 2, y + ROWH / 2, b, ha="center",
                    va="center", fontsize=10.5, color=C_TEXT,
                    fontweight="bold")
        if note:
            ax.text(X0 + BITS * bw + 0.25, y + ROWH / 2, note,
                    fontsize=8.5, color=C_GRID, va="center")

    def section_title(y, text):
        ax.text(0.15, y, text, fontsize=10, fontweight="bold", color=C_TEXT)

    # 位编号（放在最上面，格子正上方）
    for i in range(BITS):
        ax.text(X0 + i * bw + (bw - 0.05) / 2, 9.05, str(7 - i),
                ha="center", fontsize=8, color=C_GRID)
    ax.text(X0 - 0.25, 9.05, "位:", ha="right", fontsize=8, color=C_GRID)

    # 初始值
    y = 8.2
    draw_row(y, "x", list("11001010"))
    ax.text(0.15, y - 0.35, "x = 0b11001010 = 202", fontsize=9, color=C_GRID)

    # ① 置位
    section_title(7.15, "① 置位第 2 位：  x |= (1u << 2)")
    draw_row(6.35, "1u<<2", list("00000100"))
    draw_row(5.55, "x | 它", list("11001110"), highlight={5},
             note="第2位 0 → 1")

    # ② 清位
    section_title(4.6, "② 清位第 3 位：  x &= ~(1u << 3)")
    draw_row(3.8, "~(1<<3)", list("11110111"))
    draw_row(3.0, "x & 它", list("11000010"), highlight={4},
             note="第3位 1 → 0")

    # ③ 掩码提取
    section_title(2.05, "③ 掩码提取第 2~4 位：  (x >> 2) & 0b111")
    draw_row(1.25, "x>>2", list("00110010"))
    draw_row(0.45, "& 0b111", list("00000010"), highlight={5, 6, 7},
             note="→ 0b010 = 2")

    _save(fig, "c-bitops.svg")


if __name__ == "__main__":
    linked_list()
    pointer_memory()
    bitops()
    print("done")
