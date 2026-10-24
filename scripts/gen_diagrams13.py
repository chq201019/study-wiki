"""第十四批：C 批（Makefile / fixture / Git 分支 / 预处理 / DMA 双缓冲 / 预取）"""
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


# ---------- Makefile 依赖图 ----------
def makefile_graph():
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

    ax.text(8.0, 1.72, "头文件依赖必须自动生成", fontsize=9.2,
            fontweight="bold", color=RED)
    ax.text(8.0, 1.40, "编译时加 -MMD -MP，再 -include $(DEPS)，", fontsize=7.6, color=TEXT)
    ax.text(8.0, 1.12, "否则改头文件不会触发任何重编 ——", fontsize=7.6, color=TEXT)
    ax.text(8.0, 0.86, "你看到的是旧行为，调试很久也找不到原因。", fontsize=7.6, color=RED)
    

    ax.text(0.4, 0.35, "三个最容易踩的坑", fontsize=9, fontweight="bold", color=RED)
    ax.text(0.4, 0.05,
            "① 命令必须 TAB 开头　② 忘了 -MMD 改头文件不重编　③ 改 Makefile 本身不触发重编（要把它加进依赖）",
            fontsize=7.6, color=TEXT)

    _save(fig, "c-makefile-graph.svg")


# ---------- pytest fixture 作用域 ----------
def pytest_scope():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "pytest fixture 的四种作用域：创建几次",
            fontsize=12.5, fontweight="bold", color=TEXT)

    scopes = [
        ("function", "每个测试一次", GREEN, "默认，最安全"),
        ("class", "每个类一次", BLUE, "同类共享"),
        ("module", "每个模块一次", ORANGE, "整文件共享"),
        ("session", "整个会话一次", PINK, "全局共享，最快"),
    ]
    for i, (name, desc, color, note) in enumerate(scopes):
        y = 6.4 - i * 1.05
        ax.add_patch(Rectangle((0.6, y), 2.4, 0.72, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(1.8, y + 0.36, name, ha="center", va="center",
                fontsize=9, color=TEXT, fontweight="bold")
        ax.text(3.2, y + 0.36, desc + "　（" + note + "）", fontsize=8.2,
                color=TEXT, va="center")

    # 示意：三个测试用同一个 fixture
    ax.text(0.4, 2.1, "三个测试函数共用一个 fixture 时的创建次数", fontsize=9.4,
            fontweight="bold", color=TEXT)
    tests = ["test_a", "test_b", "test_c"]
    for i, t in enumerate(tests):
        x = 0.6 + i * 2.4
        ax.add_patch(Rectangle((x, 1.0), 2.0, 0.6, facecolor=GREY,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 1.0, 1.3, t, ha="center", va="center", fontsize=8.2, color=TEXT)

    ax.text(7.8, 2.1, "关键风险", fontsize=9.4, fontweight="bold", color=RED)
    ax.text(7.8, 1.7, "放大作用域能提速，但如果 fixture 有可变状态，", fontsize=8, color=TEXT)
    ax.text(7.8, 1.38, "测试之间会互相污染 —— 表现为「单独跑过、一起跑挂」。", fontsize=8, color=TEXT)
    ax.text(7.8, 0.95, "规矩：默认 function，只有确实无状态且创建很贵时才放宽。", fontsize=8, color=RED)

    ax.text(0.4, 0.4, "另外：yield 之前的代码是准备，之后是清理；即使测试失败，清理也会执行。",
            fontsize=8, color=LINE)

    _save(fig, "py-pytest-scope.svg")


if __name__ == "__main__":
    makefile_graph()
    pytest_scope()
    print("done")


# ---------- Git 分支指针 ----------
def git_branches():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "Git 分支只是一个存着 SHA 的文件", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 提交链
    commits = [("c1", 1.4), ("c2", 3.4), ("c3", 5.4), ("c4", 7.4)]
    for name, x in commits:
        ax.add_patch(plt.Circle((x, 5.2), 0.42, facecolor=BLUE,
                                edgecolor=DARK, lw=1.4))
        ax.text(x, 5.2, name, ha="center", va="center", fontsize=8, color=TEXT)
        if name != "c1":
            arrow(ax, (x - 0.85, 5.2), (x - 0.45, 5.2), color=LINE, lw=1.4)

    # main 分支指针
    ax.annotate("", xy=(7.4, 5.75), xytext=(7.4, 5.7),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
    box(ax, 6.5, 5.95, 1.8, 0.55, "main", None, GREEN, fs=8.6)
    ax.text(8.5, 6.22, "指向 c4", fontsize=7.6, color=RED, va="center")

    # feature 分支
    ax.add_patch(plt.Circle((7.4, 3.6), 0.42, facecolor=PINK,
                            edgecolor=DARK, lw=1.4))
    ax.text(7.4, 3.6, "f1", ha="center", va="center", fontsize=8, color=TEXT)
    arrow(ax, (5.4, 4.85), (7.0, 3.9), color=PINK, lw=1.4)
    box(ax, 8.2, 3.35, 1.9, 0.55, "feature", None, PINK, fs=8.4)
    ax.text(10.3, 3.62, "指向 f1", fontsize=7.6, color=RED, va="center")

    # HEAD
    ax.text(0.4, 6.9, "HEAD 是个「指向引用的引用」", fontsize=9.2,
            fontweight="bold", color=TEXT)
    ax.text(0.4, 6.55, "cat .git/HEAD  →  ref: refs/heads/main", fontsize=8,
            color=TEXT)
    ax.text(0.4, 6.2, "cat .git/refs/heads/main  →  c4 的 SHA", fontsize=8,
            color=TEXT)

    # 操作
    ax.text(0.4, 2.6, "三个操作的本质", fontsize=9.6, fontweight="bold", color=TEXT)
    rows = [
        ("切换分支", "只改 HEAD 里那一行指向", GREEN),
        ("提交", "新建 commit 对象，改分支文件里的 SHA", BLUE),
        ("reset --hard", "只移动指向，旧 commit 还在（能被 reflog 找回）", ORANGE),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 2.2 - i * 0.45
        ax.add_patch(Rectangle((0.6, y - 0.14), 0.24, 0.28, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.0, y, k, fontsize=8.6, color=TEXT, va="center", fontweight="bold")
        ax.text(2.6, y, v, fontsize=8.2, color=TEXT, va="center")

    ax.text(0.4, 0.5,
            "所以分支切换是 O(1) —— 不涉及任何文件内容重算。这是 Git 快的根本原因。",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.15,
            "reflog 记录每次 HEAD 移动，所以 reset --hard 之后还能救回来；但它默认 90 天过期且不随 push。",
            fontsize=8.2, color=RED)

    _save(fig, "git-branches.svg")


# ---------- C 预处理流程 ----------
def c_preprocess():
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "C 预处理：纯文本替换，没有任何语法理解",
            fontsize=12.5, fontweight="bold", color=TEXT)

    stages = [
        ("源文件", "main.c（10 行）", BLUE, 0.5),
        ("展开 #include", "stdio.h 递归展开", ORANGE, 3.3),
        ("展开 #define", "宏文本替换（可能嵌套）", PINK, 6.1),
        ("输出 .i", "约 1750 行", GREEN, 8.9),
    ]
    for name, desc, color, x in stages:
        ax.add_patch(Rectangle((x, 5.1), 2.4, 1.1, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(x + 1.2, 5.85, name, ha="center", va="center",
                fontsize=8.8, color=TEXT, fontweight="bold")
        ax.text(x + 1.2, 5.42, desc, ha="center", va="center",
                fontsize=7.4, color=TEXT)
        if x < 8.9:
            arrow(ax, (x + 2.55, 5.65), (x + 2.75, 5.65), color=RED, lw=1.5)

    ax.text(0.4, 4.5, "为什么 .i 有 1750 行", fontsize=9.4, fontweight="bold", color=TEXT)
    ax.text(0.4, 4.15,
            "stdio.h 会递归带进几十个头文件 —— 你只写了 10 行，但编译器看到的是几千行。",
            fontsize=8.2, color=TEXT)

    ax.text(0.4, 3.5, "四个容易踩的坑", fontsize=9.4, fontweight="bold", color=RED)
    pts = [
        "① 宏没有类型检查：SQUARE(1+2) 展开成 1+2*1+2 = 5，不是 9",
        "② 宏参数要加括号：#define SQ(x) ((x)*(x))",
        "③ #include 顺序影响结果：后面的宏能覆盖前面的",
        "④ 头文件重复包含要靠 include guard 或 #pragma once",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 3.1 - i * 0.36, s, fontsize=8, color=TEXT)

    ax.text(0.4, 1.4, "验证手段", fontsize=9.2, fontweight="bold", color=TEXT)
    ax.text(0.4, 1.05,
            "gcc -E main.c > main.i　　然后看 .i 文件里那行变成了什么。",
            fontsize=8.4, color=TEXT)
    ax.text(0.4, 0.68,
            "比读文档可靠得多 —— 宏的真实展开形式只能这样看到。",
            fontsize=8.4, color=LINE)
    ax.text(0.4, 0.25,
            "注意：预处理不报语法错，只报 #include 找不到、#if 不配对这类问题。",
            fontsize=8.2, color=RED)

    _save(fig, "c-preprocess-flow.svg")


if __name__ == "__main__":
    git_branches()
    c_preprocess()
    print("done")



# ---------- DMA 双缓冲 ----------
def dma_double_buffer():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "DMA 双缓冲：CPU 处理和 DMA 搬运交替进行",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # buffer 分两半
    ax.text(0.4, 6.8, "缓冲区（大小 2N，分前后两半）", fontsize=9.4,
            fontweight="bold", color=TEXT)
    ax.add_patch(Rectangle((0.6, 5.9), 5.5, 0.8, facecolor=BLUE,
                           edgecolor=DARK, lw=1.2))
    ax.text(3.35, 6.3, "前半 [0 .. N-1]", ha="center", va="center",
            fontsize=9, color=TEXT, fontweight="bold")
    ax.add_patch(Rectangle((6.1, 5.9), 5.5, 0.8, facecolor=PINK,
                           edgecolor=DARK, lw=1.2))
    ax.text(8.85, 6.3, "后半 [N .. 2N-1]", ha="center", va="center",
            fontsize=9, color=TEXT, fontweight="bold")

    # 时间轴：四段
    ax.text(0.4, 5.3, "时间线", fontsize=9.4, fontweight="bold", color=TEXT)
    phases = [
        ("第 1 段", "DMA 填前半", "CPU 空闲", 0.6, 3.0),
        ("第 2 段", "DMA 填后半", "CPU 处理前半", 3.8, 3.0),
        ("第 3 段", "DMA 填前半", "CPU 处理后半", 7.0, 3.0),
        ("第 4 段", "循环重复…", "", 10.2, 2.6),
    ]
    for name, dma, cpu, x, w in phases:
        ax.text(x, 4.9, name, fontsize=7.8, color=TEXT, fontweight="bold")
        ax.add_patch(Rectangle((x, 4.05), w, 0.55, facecolor=ORANGE,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + w / 2, 4.32, dma, ha="center", va="center",
                fontsize=7.6, color=TEXT)
        if cpu:
            ax.add_patch(Rectangle((x, 3.4), w, 0.55, facecolor=GREEN,
                                   edgecolor=DARK, lw=1.0))
            ax.text(x + w / 2, 3.67, cpu, ha="center", va="center",
                    fontsize=7.6, color=TEXT)

    ax.text(0.4, 3.0, "橙色 = DMA 在搬数据　绿色 = CPU 在处理", fontsize=7.8, color=LINE)

    # 两个中断
    ax.text(0.4, 2.5, "靠两个中断驱动", fontsize=9.4, fontweight="bold", color=TEXT)
    rows = [
        ("HT（半传输）", "前半填满 → 处理前半，此时 DMA 自动填后半", BLUE),
        ("TC（传输完成）", "后半填满 → 处理后半，此时 DMA 自动填前半", PINK),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 2.1 - i * 0.44
        ax.add_patch(Rectangle((0.6, y - 0.14), 0.24, 0.28, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.0, y, k, fontsize=8.4, color=TEXT, va="center", fontweight="bold")
        ax.text(3.2, y, v, fontsize=8, color=TEXT, va="center")

    ax.text(0.4, 0.95, "为什么需要双缓冲", fontsize=9.2, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.6,
            "单缓冲时 CPU 处理期间 DMA 无处可写，会丢数据；双缓冲让两者交替进行，没有空档。",
            fontsize=8.2, color=TEXT)
    ax.text(0.4, 0.22,
            "配置要点：DMA 用 Circular 模式，同时在 CubeMX 里使能 HT 中断（默认常常只开了 TC）。",
            fontsize=8.2, color=RED)

    _save(fig, "stm32-dma-double-buffer.svg")


# ---------- STM32 Flash 等待周期与预取 ----------
def stm32_flash_wait():
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "Flash 等待周期与预取：为什么顺序代码能快近一倍",
            fontsize=12.5, fontweight="bold", color=TEXT)

    ax.text(0.4, 6.6, "CPU 比 Flash 快，必须插等待周期", fontsize=9.4,
            fontweight="bold", color=TEXT)
    rows = [
        ("≤ 24 MHz", "0 等待", "#1e8449"),
        ("24 ~ 48 MHz", "1 等待", "#b9770e"),
        ("48 ~ 72 MHz", "2 等待", "#a93226"),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 6.2 - i * 0.46
        ax.text(0.6, y, k, fontsize=8.4, color=TEXT, fontweight="bold")
        ax.text(3.0, y, v, fontsize=8.4, color=c)

    ax.text(0.4, 4.6, "预取缓冲（Prefetch Buffer）能救回多少", fontsize=9.4,
            fontweight="bold", color=TEXT)

    # 无预取 vs 有预取
    for i, (title, color, gain) in enumerate([
        ("关闭预取", GREY, "每条取指都要等 2 个周期"),
        ("开启预取", GREEN, "一次读 64 位（2 条指令），下一条直接命中"),
    ]):
        y = 3.9 - i * 1.0
        ax.text(0.4, y + 0.32, title, fontsize=8.8, color=TEXT, fontweight="bold")
        ax.text(2.4, y + 0.32, gain, fontsize=7.8, color=TEXT)
        for j in range(6):
            x = 0.6 + j * 1.0
            ax.add_patch(Rectangle((x, y - 0.2), 0.9, 0.4, facecolor=color,
                                   edgecolor=DARK, lw=0.9))
            ax.text(x + 0.45, y, "指令", ha="center", va="center",
                    fontsize=6.8, color=TEXT)

    ax.text(0.4, 2.1, "由此得出的三条优化直觉", fontsize=9.2, fontweight="bold", color=TEXT)
    pts = [
        "① 循环比展开好 —— 循环体顺序执行，预取命中率高",
        "② 减少函数调用和分支 —— 跳转会打断预取",
        "③ 把热点循环放到 RAM 跑 —— RAM 没有等待周期（F1 用 .ramfunc 段）",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 1.7 - i * 0.36, s, fontsize=8.2, color=TEXT)

    ax.text(0.4, 0.45,
            "别忘了配置 FLASH_LATENCY：72MHz 必须用 LATENCY_2，配少了会读到错误指令（随机死机）。",
            fontsize=8, color=RED)
    ax.text(0.4, 0.12,
            "开启预取：FLASH->ACR |= FLASH_ACR_PRFTBE;",
            fontsize=8, color=LINE)

    _save(fig, "stm32-flash-wait.svg")


if __name__ == "__main__":
    git_branches()
    c_preprocess()
    dma_double_buffer()
    stm32_flash_wait()
    print("done")
