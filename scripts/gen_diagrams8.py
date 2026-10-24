"""第八批示意图：优先级分组 / 时基单元 / 堆块布局 / eBPF 挂载点 / ADC 冲突 / RAII 异常路径。

用法: python scripts/gen_diagrams8.py
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


def nvic_priority():
    """NVIC 优先级分组的五种配置"""
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "NVIC 优先级分组：4 位怎么切成抢占和子优先级",
            fontsize=12.5, fontweight="bold", color=TEXT)

    ax.text(0.4, 6.55, "一个中断有 4 位优先级（STM32F103 只实现了 4 位，不是 8 位）",
            fontsize=9.4, color=TEXT)

    groups = [
        ("Group 0", 0, 4, "不能抢占，全部排队"),
        ("Group 1", 1, 3, "2 级抢占"),
        ("Group 2", 2, 2, "4 级抢占"),
        ("Group 3", 3, 1, "8 级抢占"),
        ("Group 4", 4, 0, "16 级抢占（HAL 默认）"),
    ]

    for i, (name, pre, sub, note) in enumerate(groups):
        y = 5.85 - i * 0.92
        ax.text(0.4, y + 0.22, name, fontsize=9, color=TEXT, fontweight="bold")

        # 四个位格
        cell = 0.62
        x0 = 2.3
        for bit in range(4):
            is_pre = bit < pre
            color = PINK if is_pre else GREEN
            ax.add_patch(Rectangle((x0 + bit * cell, y), cell, 0.46,
                                   facecolor=color, edgecolor=DARK, lw=1.0))
        # 标注抢占/子
        if pre > 0:
            ax.annotate("", xy=(x0, y - 0.12), xytext=(x0 + pre * cell, y - 0.12),
                        arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.1))
            ax.text(x0 + pre * cell / 2, y - 0.32, "抢占 %d 位" % pre,
                    ha="center", fontsize=7.4, color=RED)
        if sub > 0:
            ax.annotate("", xy=(x0 + pre * cell, y - 0.12),
                        xytext=(x0 + 4 * cell, y - 0.12),
                        arrowprops=dict(arrowstyle="<|-|>", color="#1e8449", lw=1.1))
            ax.text(x0 + pre * cell + sub * cell / 2, y - 0.32, "子 %d 位" % sub,
                    ha="center", fontsize=7.4, color="#1e8449")

        ax.text(x0 + 4 * cell + 0.3, y + 0.22, note, fontsize=8.4, color=TEXT)

    # 右侧说明
    ax.text(0.4, 1.35, "三个关键结论", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "• 分组是全局设置（整个系统只设一次），改了影响所有中断",
        "• 抢占优先级决定能否嵌套；子优先级只在同级排队时起作用",
        "• Group 4（HAL 默认）= 16 级抢占、子优先级完全无效",
        "• 抢占优先级数字越小越高 —— 和 FreeRTOS 任务优先级方向相反",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 0.95 - i * 0.32, s, fontsize=8.4, color=TEXT)

    _save(fig, "stm32-nvic-priority.svg")


def timer_base():
    """定时器时基单元：PSC -> CNT -> ARR/CCR"""
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.4)
    ax.set_axis_off()
    ax.text(0.2, 7.0, "定时器时基：从时钟到频率的每一级分频", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 主链
    box(ax, 0.4, 5.5, 2.4, 0.9, "定时器时钟", "72 MHz", ORANGE, fs=9.5, sfs=7.6)
    box(ax, 3.6, 5.5, 2.2, 0.9, "PSC 预分频", "寄存器值 +1", PINK, fs=9.5, sfs=7.6)
    box(ax, 6.6, 5.5, 2.2, 0.9, "CNT 计数器", "每个时钟 ±1", BLUE, fs=9.5, sfs=7.6)
    box(ax, 9.6, 5.5, 2.2, 0.9, "ARR 自动重装", "计数到这里归零", GREEN, fs=9.5, sfs=7.6)

    arrow(ax, (2.85, 5.95), (3.55, 5.95))
    arrow(ax, (5.85, 5.95), (6.55, 5.95))
    arrow(ax, (8.85, 5.95), (9.55, 5.95))

    ax.text(4.7, 6.55, "÷(PSC+1)", fontsize=8.6, color=RED, ha="center")
    ax.text(4.7, 5.25, "72MHz ÷ 72 = 1MHz", fontsize=7.8, color=LINE, ha="center")

    # 公式
    ax.text(0.4, 4.65, "更新频率 = 定时器时钟 / ((PSC+1) × (ARR+1))",
            fontsize=10.5, fontweight="bold", color=RED)

    # 算例
    ax.text(0.4, 4.05, "算一个 1 kHz 中断（72 MHz 时钟）：", fontsize=9.4,
            fontweight="bold", color=TEXT)
    rows = [
        ("选 PSC = 71", "72 MHz / 72 = 1 MHz（计数频率）"),
        ("选 ARR = 999", "1000 个计数溢出一次"),
        ("结果", "1 MHz / 1000 = 1000 Hz"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 3.65 - i * 0.42
        ax.text(0.6, y, k, fontsize=8.6, color=TEXT, fontweight="bold")
        ax.text(2.9, y, v, fontsize=8.6, color=TEXT)

    # 输出比较
    ax.text(0.4, 2.05, "PWM 就在这条链上多一个比较器", fontsize=9.8,
            fontweight="bold", color=TEXT)
    box(ax, 0.6, 1.05, 3.0, 0.75, "CNT 与 CCR 比较", "小于 CCR 输出高", PURPLE, fs=8.6, sfs=7.2)
    box(ax, 4.1, 1.05, 3.0, 0.75, "占空比 = CCR / (ARR+1)", "改 CCR 就改占空比", GREEN, fs=8.6, sfs=7.2)
    arrow(ax, (3.65, 1.42), (4.05, 1.42), lw=1.3)

    # 关键陷阱
    ax.text(7.6, 2.05, "两个最容易错的地方", fontsize=9.8,
            fontweight="bold", color=TEXT)
    pts = [
        "① PSC 和 ARR 在寄存器里存的",
        "   是减一后的值 —— 忘了 +1",
        "   频率会差一点点",
        "",
        "② APB 分频 ≠ 1 时，定时器",
        "   时钟自动 ×2（APB1 = 36MHz",
        "   但 TIM2~7 实际按 72MHz 计）",
    ]
    for i, s in enumerate(pts):
        ax.text(7.6, 1.65 - i * 0.29, s, fontsize=8, color=TEXT)

    _save(fig, "stm32-timer-base.svg")


def malloc_layout():
    """malloc 块头与元数据布局"""
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "malloc(100) 实际占用了多少内存", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 内存块
    segs = [
        ("块头元数据", "8~16 字节", PURPLE, 0.4, 2.6),
        ("用户数据区", "100 字节（你请求的）", BLUE, 3.0, 4.6),
        ("对齐填充 + 下一块块头", "至少 8 字节", GREY, 7.6, 3.2),
    ]
    for label, sub, color, x, w in segs:
        ax.add_patch(Rectangle((x, 4.6), w, 1.1, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(x + w / 2, 5.32, label, ha="center", fontsize=9,
                color=TEXT, fontweight="bold")
        ax.text(x + w / 2, 4.92, sub, ha="center", fontsize=7.6, color=TEXT)

    # 返回指针
    ax.annotate("", xy=(3.0, 4.4), xytext=(3.0, 3.9),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
    ax.text(3.1, 4.1, "malloc 返回的是这里（跳过块头）", fontsize=8.6, color=RED)

    # 实际占用
    ax.text(0.4, 3.4, "实际占用 ≈ 100 + 8~16（块头）+ 对齐填充", fontsize=9.6,
            fontweight="bold", color=TEXT)
    ax.text(0.4, 3.02, "所以 malloc(1) 也至少占 16~32 字节 —— 小对象用 malloc 极不划算",
            fontsize=8.8, color=RED)

    # free 之后
    ax.text(0.4, 2.45, "free 之后发生什么", fontsize=9.8, fontweight="bold", color=TEXT)
    steps = [
        ("把块标记为空闲", GREY),
        ("尝试与前后空闲块合并（减少碎片）", ORANGE),
        ("大块可能 munmap 归还给内核", GREEN),
        ("小块留在 arena 里等复用 —— RSS 不会下降", PINK),
    ]
    for i, (s, c) in enumerate(steps):
        y = 2.05 - i * 0.38
        ax.add_patch(Rectangle((0.6, y - 0.12), 0.24, 0.26, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(0.95, y, s, fontsize=8.6, color=TEXT, va="center")

    # 右侧
    ax.text(7.4, 2.45, "三个实用结论", fontsize=9.8, fontweight="bold", color=TEXT)
    pts = [
        "• malloc(0) 行为由实现定义，别写",
        "• free 不会把指针置空，要手动 NULL",
        "• free(NULL) 是安全的空操作",
        "",
        "realloc 的两个陷阱：",
        "• 失败时原指针仍有效 —— 不直接覆盖",
        "• 可能搬移内存 —— 旧指针全悬垂",
    ]
    for i, s in enumerate(pts):
        ax.text(7.4, 2.05 - i * 0.29, s, fontsize=8, color=TEXT)

    _save(fig, "c-malloc-layout.svg")


if __name__ == "__main__":
    nvic_priority()
    timer_base()
    malloc_layout()
    print("done")
