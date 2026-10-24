"""第九批示意图：eBPF 挂载点 / ADC2 与 WiFi 冲突 / RAII 异常路径。"""
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


def ebpf_hooks():
    """eBPF 的挂载点分布"""
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "eBPF 挂在哪：从系统调用到内核函数的每一层",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 用户态 / 内核态分隔
    ax.plot([0.4, 6.9], [5.25, 5.25], color=LINE, lw=1.2, ls="--")
    ax.text(0.4, 5.38, "用户态", fontsize=9, color=LINE)
    ax.text(0.4, 5.02, "内核态", fontsize=9, color=LINE)

    # 用户态
    box(ax, 0.6, 5.6, 2.6, 0.9, "应用程序", "read / write", BLUE, fs=8.8, sfs=7.2)
    box(ax, 4.0, 5.6, 2.6, 0.9, "库函数", "glibc", BLUE, fs=8.8, sfs=7.2)
    arrow(ax, (3.25, 6.05), (3.95, 6.05))

    # 内核态各层
    box(ax, 7.4, 5.6, 3.0, 0.9, "系统调用入口", "sys_enter / sys_exit", ORANGE, fs=8.8, sfs=7.2)
    arrow(ax, (6.65, 6.05), (7.35, 6.05))

    box(ax, 7.4, 4.0, 3.0, 0.9, "VFS 层", "vfs_read / vfs_write", GREEN, fs=8.8, sfs=7.2)
    box(ax, 7.4, 2.7, 3.0, 0.9, "文件系统", "ext4_* / xfs_*", GREEN, fs=8.8, sfs=7.2)
    box(ax, 7.4, 1.4, 3.0, 0.9, "块设备 / 驱动", "提交 IO 请求", PURPLE, fs=8.8, sfs=7.2)
    arrow(ax, (8.9, 5.55), (8.9, 4.95))
    arrow(ax, (8.9, 3.95), (8.9, 3.65))
    arrow(ax, (8.9, 2.65), (8.9, 2.35))

    # 挂载点标注
    hooks = [
        (5.85, "tracepoint", "静态埋点，稳定"),
        (4.25, "kprobe", "函数入口，灵活"),
        (2.95, "kretprobe", "函数返回"),
        (1.65, "tracepoint", "块层埋点"),
    ]
    for y, name, note in hooks:
        ax.text(11.0, y, name, fontsize=8.4, color=RED, fontweight="bold", va="center")
        ax.text(11.0, y - 0.26, note, fontsize=7.2, color=TEXT, va="center")

    # 左侧要点
    ax.text(0.4, 3.9, "程序跑在内核里，只把汇总结果传回用户态", fontsize=9.4,
            fontweight="bold", color=TEXT)
    pts = [
        "• 开销接近零 —— 可以上生产，不像 strace 慢几十倍",
        "",
        "• 三重安全保护：",
        "  ① 验证器静态检查（无死循环、无越界）",
        "  ② 只能调白名单里的 helper",
        "  ③ 执行时间受限",
        "",
        "• 不能改内核数据，只能读和统计",
        "• 容器里需要 CAP_BPF 或特权",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 3.5 - i * 0.31, s, fontsize=8, color=TEXT)

    _save(fig, "linux-ebpf-hooks.svg")


def adc_wifi_conflict():
    """ESP32 ADC2 与 WiFi 的硬件冲突"""
    fig, ax = plt.subplots(figsize=(10.8, 5.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.2)
    ax.set_axis_off()
    ax.text(0.2, 6.8, "ESP32 的 ADC2 与 WiFi 共用硬件：二选一",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 仲裁器
    box(ax, 4.6, 4.4, 3.2, 1.0, "ADC2 仲裁器", "同一时刻只有一个能用", ORANGE, fs=9.2, sfs=7.4)

    # 两个竞争者
    box(ax, 0.8, 5.65, 3.2, 0.85, "WiFi 射频", "优先级更高", PINK, fs=9, sfs=7.4)
    box(ax, 1.0, 3.2, 3.2, 0.9, "你的 ADC2 调用", "adc2_get_raw", BLUE, fs=9, sfs=7.4)
    arrow(ax, (4.05, 5.85), (5.15, 5.35))
    arrow(ax, (2.6, 3.65), (5.2, 4.35))

    # 结果
    box(ax, 9.6, 5.5, 3.4, 0.85, "WiFi 开着时", "ADC2 返回错误或乱数", RED, fs=8.8, sfs=7.2)
    box(ax, 9.6, 3.35, 3.4, 0.85, "WiFi 关闭时", "ADC2 正常工作", GREEN, fs=8.8, sfs=7.2)
    arrow(ax, (7.85, 5.0), (9.55, 5.75), color=RED, lw=1.4)
    arrow(ax, (7.85, 4.55), (9.55, 3.95), color="#1e8449", lw=1.4)

    # ADC1 独立
    ax.text(0.4, 2.55, "ADC1 不受影响（但要留意噪声）", fontsize=9.4,
            fontweight="bold", color=TEXT)
    box(ax, 0.6, 1.75, 4.4, 0.65, "ADC1（GPIO32~39）", None, GREEN, fs=8.8)
    ax.text(5.2, 2.07, "要用 ADC 就选 ADC1", fontsize=8.4, color="#1e8449", va="center")

    # 关键数字
    ax.text(0.4, 1.2, "三个必须知道的数字", fontsize=9.4, fontweight="bold", color=TEXT)
    pts = [
        "• 标称 12 位，实际有效约 9~10 位",
        "• 11dB 档实际量程约 0.15~3.1V（低于读到 0，高于饱和）",
        "• 输入超 3.3V 会损坏引脚，测 4.2V 电池必须先分压",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 0.8 - i * 0.3, s, fontsize=8.2, color=TEXT)

    _save(fig, "esp32-adc-wifi.svg")


def raii_exception():
    """RAII 在异常路径下的保证"""
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.4)
    ax.set_axis_off()
    ax.text(0.2, 7.0, "RAII 为什么能保证释放：栈展开必调析构",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 正常路径
    ax.text(0.4, 6.35, "正常返回", fontsize=9.6, fontweight="bold", color="#1e8449")
    steps = [
        ("lock_guard 构造", 0.6, GREEN),
        ("临界区代码", 3.4, GREEN),
        ("return", 6.2, GREEN),
        ("∽ 析构 → 解锁", 8.6, GREEN),
    ]
    for label, x, c in steps:
        box(ax, x, 5.4, 2.4, 0.72, label, None, c, fs=7.6)
    for x in (3.0, 5.8, 8.6):
        arrow(ax, (x, 5.76), (x + 0.4, 5.76), lw=1.3)

    # 异常路径
    ax.text(0.4, 4.85, "抛出异常", fontsize=9.6, fontweight="bold", color=RED)
    steps2 = [
        ("lock_guard 构造", 0.6, ORANGE),
        ("临界区抛异常", 3.4, RED),
        ("栈展开 unwind", 6.2, PINK),
        ("∽ 析构 → 解锁", 8.6, GREEN),
    ]
    for label, x, c in steps2:
        box(ax, x, 3.9, 2.4, 0.72, label, None, c, fs=7.6)
    for x in (3.0, 5.8, 8.6):
        arrow(ax, (x, 4.26), (x + 0.4, 4.26), lw=1.3)

    ax.text(11.2, 4.26, "这是语言保证", fontsize=8.6, color="#1e8449",
            fontweight="bold", va="center")

    # 对比
    ax.text(0.4, 3.3, "手写 lock/unlock 的两个失效场景", fontsize=9.6,
            fontweight="bold", color=TEXT)
    rows = [
        ("提前 return", "unlock 那一行永远执行不到"),
        ("抛出异常", "unlock 被跳过，锁永久持有"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 2.85 - i * 0.45
        ax.text(0.6, y, k, fontsize=8.8, color=RED, fontweight="bold")
        ax.text(2.6, y, v, fontsize=8.4, color=TEXT)

    # 关键点
    ax.text(7.2, 3.3, "三个必须坚持的规则", fontsize=9.6, fontweight="bold", color=TEXT)
    pts = [
        "① 析构必须 noexcept（默认就是）",
        "   抛异常会直接 std::terminate",
        "",
        "② 资源只能有一个所有者",
        "   否则重复释放",
        "",
        "③ 禁用拷贝，或实现移动",
        "   不然两个对象析构时释放两次",
    ]
    for i, s in enumerate(pts):
        ax.text(7.2, 2.9 - i * 0.3, s, fontsize=7.9, color=TEXT)

    _save(fig, "cpp-raii-exception.svg")


if __name__ == "__main__":
    ebpf_hooks()
    adc_wifi_conflict()
    raii_exception()
    print("done")
