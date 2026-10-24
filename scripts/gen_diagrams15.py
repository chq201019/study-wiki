"""第十六批：E 批（list 扩容 / dict 结构 / 指针数组 / 结构体指针 / 正则引擎 / CI 流程）"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import font_manager, rcParams

OUT = os.path.join("static", "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

for _f in ["Microsoft YaHei", "Noto Sans SC", "SimHei"]:
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
    try:
        os.makedirs("_preview", exist_ok=True)
        fig.savefig(os.path.join("_preview", name.replace(".svg", ".png")),
                    format="png", bbox_inches="tight", transparent=True, dpi=150)
    except Exception:
        pass
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


def arrow(ax, p1, p2, color=LINE, lw=1.4, style="-|>", ms=13, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls))


# ---------- Python list 扩容 ----------
def py_list_growth():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "Python list 扩容：为什么 append 说是 O(1) 却偶尔变慢",
            fontsize=12.5, fontweight="bold", color=TEXT)

    capacities = [(0, 0), (1, 4), (5, 8), (9, 16), (17, 25), (26, 35)]
    ax.text(0.4, 6.75, "插入第 N 个元素时的容量变化", fontsize=9.4,
            fontweight="bold", color=TEXT)
    for i, (n, cap) in enumerate(capacities):
        x = 0.6 + i * 2.1
        h = cap / 40.0
        ax.add_patch(Rectangle((x, 5.6), 1.5, h if h > 0.05 else 0.05,
                               facecolor=BLUE, edgecolor=DARK, lw=1.0))
        ax.text(x + 0.75, 5.5, n, ha="center", fontsize=7.6, color=TEXT)
        ax.text(x + 0.75, 5.6 + (h if h > 0.05 else 0.05) + 0.12, "%d" % cap,
                ha="center", fontsize=7.4, color=RED)
    ax.text(0.6, 5.15, "蓝柱高度 = 已分配的槽位数（capacity），下方数字 = 当前元素个数",
            fontsize=7.8, color=LINE)

    ax.text(0.4, 4.5, "扩容规则：不是翻倍，而是约 1.125 倍 + 常数", fontsize=9.4,
            fontweight="bold", color=TEXT)
    rows = [
        ("已用 0 → 4", "第一次 append 就分配 4 个槽位"),
        ("已用 4 → 8", "满了再扩，按 1.125n + 常数算"),
        ("均摊成本", "每次 append 平均 O(1)，但偶尔一次 O(n)"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 4.1 - i * 0.4
        ax.text(0.6, y, k, fontsize=8.2, color=TEXT, fontweight="bold")
        ax.text(2.8, y, v, fontsize=8, color=TEXT)

    ax.text(0.4, 2.6, "三个实用结论", fontsize=9.4, fontweight="bold", color=TEXT)
    pts = [
        "① len(lst) 是元素个数，不是容量 —— 多出来的槽位是给 append 留的",
        "② 扩容时要重新分配并拷贝全部元素，这是唯一会卡顿的时刻",
        "③ 已知大小就先 [None]*n 或 list 预占，能省掉所有扩容拷贝",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 2.2 - i * 0.36, s, fontsize=8.2, color=TEXT)

    ax.text(0.4, 0.8, "为什么不用翻倍（像 C++ vector）", fontsize=9,
            fontweight="bold", color=RED)
    ax.text(0.4, 0.45,
            "CPython 用 1.125 倍是为了让「扩容后残留的内存块」更容易被复用到其他 list 上，减少碎片。",
            fontsize=7.8, color=TEXT)
    ax.text(0.4, 0.15,
            "代价是扩容更频繁，但每次拷贝量更小 —— 实测总拷贝量反而更低。",
            fontsize=7.8, color=LINE)

    _save(fig, "py-list-growth-curve.svg")


# ---------- C 指针与数组 ----------
def c_pointer_array():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "数组名不是指针：sizeof 和取地址会暴露真相",
            fontsize=12.5, fontweight="bold", color=TEXT)

    ax.text(0.4, 6.75, "int arr[5] = {1,2,3,4,5};", fontsize=8.6,
            fontweight="bold", color=TEXT)

    # 内存块
    for i in range(5):
        x = 0.6 + i * 1.15
        ax.add_patch(Rectangle((x, 5.6), 1.05, 0.65, facecolor=BLUE,
                               edgecolor=DARK, lw=1.1))
        ax.text(x + 0.525, 5.92, str(i + 1), ha="center", va="center",
                fontsize=9, color=TEXT, fontweight="bold")
        ax.text(x + 0.525, 5.42, "0x%X" % (0x1000 + i * 4), ha="center",
                fontsize=6.8, color=LINE)
    ax.text(0.6, 5.15, "arr 本身在栈上占 20 字节（5 × 4）", fontsize=7.8, color="#1e8449")

    # 对比
    ax.text(0.4, 4.5, "三个关键差异", fontsize=9.4, fontweight="bold", color=TEXT)
    rows = [
        ("sizeof(arr)", "20（整个数组）"),
        ("sizeof(&arr[0])", "8（指针大小）"),
        ("&arr 与 &arr[0]", "值相同但类型不同：int(*)[5] vs int*"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 4.1 - i * 0.44
        ax.text(0.6, y, k, fontsize=8.4, color=TEXT)
        ax.text(3.4, y, v, fontsize=8.2, color=RED)

    ax.text(0.4, 2.5, "最容易出错的场景：数组传参会退化成指针", fontsize=9.4,
            fontweight="bold", color=RED)
    ax.text(0.6, 2.1, "void f(int a[10]) { sizeof(a); }   // 得到 8，不是 40",
            fontsize=8.2, color=TEXT)
    ax.text(0.6, 1.75, "所以必须额外传长度，或用「数组引用」保留大小信息：",
            fontsize=8.2, color=TEXT)
    ax.text(0.6, 1.4, "void f(int (&a)[10]) { sizeof(a); }   // 40，C++ 才行",
            fontsize=8.2, color="#1e8449")

    ax.text(0.4, 0.65, "验证手段：编译时用 -Wall -Wextra，很多数组/指针混用会直接告警；",
            fontsize=8)
    ax.text(0.4, 0.32,
            "或者写一个 _Static_assert(sizeof(arr) == 20) 把假设钉死。",
            fontsize=8, color=LINE)

    _save(fig, "c-pointer-array-detail.svg")

if __name__ == "__main__":
    py_list_growth()
    c_pointer_array()
    print("done")
