"""第三批示意图：结构/时序/流程类。

设计原则：只画 mermaid 表达不了、或文字描述效率极低的内容。
用法: python scripts/gen_diagrams3.py
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

BLUE = "#7fb3d5"
PINK = "#e8b4b8"
ORANGE = "#f5cba7"
GREEN = "#a9dfbf"
PURPLE = "#d2b4de"
GREY = "#d5dbdb"
TEXT = "#1b2631"
LINE = "#5d6d7e"
RED = "#c0392b"


def _save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, label, sub=None, color=BLUE, fs=10, sfs=8, lw=1.2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="#2c3e50",
                           linewidth=lw, alpha=0.92))
    if sub:
        ax.text(x + w / 2, y + h * 0.66, label, ha="center", va="center",
                fontsize=fs, color=TEXT, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center",
                fontsize=sfs, color=TEXT)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=TEXT, fontweight="bold")


def arrow(ax, p1, p2, color=RED, lw=1.6, style="-|>", ms=14):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw))


def stm32_clock_tree():
    """STM32F103 时钟树：从晶振到各总线的分频倍频关系"""
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 14.0)
    ax.set_ylim(0, 8.6)
    ax.set_axis_off()
    ax.text(0.2, 8.2, "STM32F103 时钟树：8MHz 晶振怎么变成 72MHz",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # HSE
    box(ax, 0.4, 6.6, 2.5, 0.95, "HSE 外部晶振", "8 MHz", ORANGE)
    # PLL
    box(ax, 3.6, 6.6, 2.3, 0.95, "PLL 倍频", "×9", PINK)
    arrow(ax, (2.9, 7.07), (3.55, 7.07))
    ax.text(3.2, 7.3, "×9", fontsize=8.5, color=RED, fontweight="bold")

    # SYSCLK
    box(ax, 6.6, 6.6, 2.6, 0.95, "SYSCLK", "72 MHz", GREEN)
    arrow(ax, (5.9, 7.07), (6.55, 7.07))

    # AHB
    box(ax, 10.0, 6.6, 2.6, 0.95, "AHB /1", "HCLK 72 MHz", BLUE)
    arrow(ax, (9.2, 7.07), (9.95, 7.07))

    # APB1 / APB2
    box(ax, 1.6, 4.3, 4.3, 0.95, "APB1 分频 /2", "PCLK1 = 36 MHz（上限！）", PINK)
    box(ax, 9.0, 4.3, 4.3, 0.95, "APB2 分频 /1", "PCLK2 = 72 MHz", BLUE)

    arrow(ax, (7.9, 6.55), (3.75, 5.3))
    arrow(ax, (7.9, 6.55), (11.15, 5.3))

    # 挂在 APB1 上的外设
    apb1 = ["TIM2~TIM7", "USART2/3", "I2C1/2", "SPI2", "CAN"]
    for i, name in enumerate(apb1):
        x = 0.6 + i * 1.18
        ax.add_patch(Rectangle((x, 2.9), 1.05, 0.62, facecolor=GREY,
                               edgecolor="#2c3e50", lw=1.0))
        ax.text(x + 0.525, 3.21, name, ha="center", va="center",
                fontsize=7.2, color=TEXT)
    arrow(ax, (3.75, 4.25), (3.75, 3.55))

    # 挂在 APB2 上的外设
    apb2 = ["TIM1", "USART1", "SPI1", "ADC1/2", "GPIO"]
    for i, name in enumerate(apb2):
        x = 8.0 + i * 1.18
        ax.add_patch(Rectangle((x, 2.9), 1.05, 0.62, facecolor=GREY,
                               edgecolor="#2c3e50", lw=1.0))
        ax.text(x + 0.525, 3.21, name, ha="center", va="center",
                fontsize=7.2, color=TEXT)
    arrow(ax, (11.15, 4.25), (11.15, 3.55))

    # 定时器 ×2 的提示
    ax.text(0.4, 2.35,
            "注意 隐藏倍频：APB1 分频 ≠ 1 时，挂在 APB1 上的定时器时钟自动 ×2",
            fontsize=8.8, color=RED)
    ax.text(0.4, 2.02, "   即 APB1 = 36 MHz → TIM2~TIM7 实际按 72 MHz 计数",
            fontsize=8.8, color=RED)

    # HSI 旁路
    box(ax, 0.4, 0.75, 2.5, 0.85, "HSI 内部 RC", "8 MHz（上电默认）", GREY, fs=9, sfs=7.5)
    ax.text(3.2, 1.17, "→ 不配时钟树就跑在 8MHz，慢 9 倍", fontsize=8.8, color=TEXT)

    # 检查上限
    ax.text(0.4, 0.25, "硬性限制：APB1 ≤ 36 MHz，APB2 ≤ 72 MHz，Flash 等待周期 = 2",
            fontsize=8.8, color=LINE)

    _save(fig, "stm32-clock-tree.svg")


def linux_boot_chain():
    """Linux 启动链：从加电到用户进程"""
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 8.4)
    ax.set_axis_off()
    ax.text(0.2, 8.0, "Linux 启动链：从加电到能用 shell", fontsize=12.5,
            fontweight="bold", color=TEXT)

    stages = [
        ("① BootROM", "芯片固化、不可改\n上电第一条指令", ORANGE),
        ("② SPL / U-Boot", "初始化 DDR\n加载内核到内存", PINK),
        ("③ Kernel", "解压、初始化驱动\n挂载根文件系统", BLUE),
        ("④ init (PID 1)", "systemd / busybox init\n启动各类服务", GREEN),
        ("⑤ 用户进程", "getty / sshd / shell\n你能登录了", PURPLE),
    ]

    w, h, y = 2.35, 1.5, 5.4
    for i, (name, sub, color) in enumerate(stages):
        x = 0.4 + i * 2.55
        box(ax, x, y, w, h, name, sub, color, fs=9.5, sfs=7.6)
        if i < len(stages) - 1:
            arrow(ax, (x + w, y + h / 2), (x + w + 0.2, y + h / 2))

    # 关键分界
    ax.text(0.4, 7.15, "上电", fontsize=9, color=RED, fontweight="bold")
    ax.plot([0.4, 0.4], [6.95, 7.05], color=RED, lw=1.2)
    ax.text(7.85, 7.15, "内核接管硬件", fontsize=9, color=RED, fontweight="bold")
    ax.text(12.1, 7.15, "用户态", fontsize=9, color=RED, fontweight="bold")

    # 各阶段存在哪
    ax.text(0.4, 4.75, "各阶段代码存在哪里：", fontsize=10, fontweight="bold", color=TEXT)
    rows = [
        ("BootROM", "芯片内部掩膜 ROM —— 改不了，也删不掉", ORANGE),
        ("SPL / U-Boot", "Flash 或 SD 卡第一个分区", PINK),
        ("Kernel（zImage/uImage）", "独立分区（通常 4~16 MB）", BLUE),
        ("设备树（.dtb）", "独立分区或拼在内核后面", BLUE),
        ("rootfs（根文件系统）", "另一个分区，ext4 / squashfs / UBIFS", GREEN),
    ]
    for i, (k, v, color) in enumerate(rows):
        yy = 4.2 - i * 0.62
        ax.add_patch(Rectangle((0.4, yy - 0.2), 0.28, 0.42, facecolor=color,
                               edgecolor="#2c3e50", lw=0.8))
        ax.text(0.85, yy, k, fontsize=8.8, color=TEXT, va="center",
                fontweight="bold")
        ax.text(4.6, yy, v, fontsize=8.5, color=TEXT, va="center")

    # 常见的失败点
    ax.text(0.4, 0.95, "嵌入式调试最常卡在这三处：", fontsize=9.5,
            fontweight="bold", color=RED)
    ax.text(0.4, 0.58,
            "① U-Boot 串口无输出 → DDR 初始化参数不对    ② 内核 panic: 找不到 rootfs → 启动参数 root= 写错",
            fontsize=8.5, color=TEXT)
    ax.text(0.4, 0.24, "③ 内核启动完卡住 → init 程序路径不对或 rootfs 缺文件",
            fontsize=8.5, color=TEXT)

    _save(fig, "linux-boot-chain.svg")


def python_list_growth():
    """Python list 的 ob_item + 预分配策略"""
    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "Python list：长度 3，但已申请 4 个槽位", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # list 对象头
    box(ax, 0.4, 5.5, 3.6, 1.2, "list 对象", "ob_refcnt / ob_type\nob_size = 3", PINK, fs=9.5, sfs=7.5)
    ax.text(2.2, 5.25, "PyListObject", ha="center", fontsize=8, color=LINE)

    # ob_item 指针
    box(ax, 4.6, 5.65, 2.1, 0.9, "ob_item", "指针", ORANGE, fs=9)
    arrow(ax, (4.05, 6.1), (4.55, 6.1))

    # 槽位数组
    ax.text(7.4, 6.85, "已分配的槽位数组（allocated = 4）", fontsize=9.5,
            fontweight="bold", color=TEXT)
    vals = ["a", "b", "c", None]
    labels = ["[0]", "[1]", "[2]", "[3]"]
    for i, (v, lb) in enumerate(zip(vals, labels)):
        x = 7.4 + i * 1.25
        color = BLUE if v is not None else GREY
        ax.add_patch(Rectangle((x, 5.55), 1.1, 0.85, facecolor=color,
                               edgecolor="#2c3e50", lw=1.1))
        ax.text(x + 0.55, 5.97, v if v else "空", ha="center", va="center",
                fontsize=11, color=TEXT, fontweight="bold")
        ax.text(x + 0.55, 5.3, lb, ha="center", fontsize=8, color=LINE)
    arrow(ax, (6.75, 6.1), (7.35, 5.97))

    # 说明
    ax.text(0.4, 4.55, "为什么 len 是 3 却有 4 个槽位？", fontsize=10.5,
            fontweight="bold", color=TEXT)
    notes = [
        "• len(list) 读的是 ob_size（3），不是分配容量",
        "• 实际容量 allocated 可能是 4 —— 多出的槽位留给 append",
        "• append 时若 ob_size < allocated，直接写入空槽，O(1)",
        "• 槽位满了才 realloc，并按 ~1.125 倍 + 常数扩容（不是翻倍）",
        "• 所以 append 的均摊成本是 O(1)，但内存会略多于元素个数",
    ]
    for i, t in enumerate(notes):
        ax.text(0.4, 4.05 - i * 0.44, t, fontsize=9, color=TEXT)

    ax.text(0.4, 1.0, "同样 100 万个元素：", fontsize=9.5, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.6, "list 存的是指针（8 字节/个）+ 槽位开销 → 约 8 MB 以上",
            fontsize=9, color=TEXT)
    ax.text(0.4, 0.24, "array('i') 或 numpy 存的是值本身（4 字节/个）→ 约 4 MB，差距一倍以上",
            fontsize=9, color=RED)

    _save(fig, "python-list-growth.svg")


def i2c_vs_spi():
    """I2C 与 SPI 的接线与数据方向对比"""
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "I2C 与 SPI：省引脚 vs 要带宽", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # ---- I2C ----
    ax.text(0.4, 6.75, "I2C：2 根线，靠地址区分（可接很多设备）",
            fontsize=10.5, fontweight="bold", color=TEXT)
    box(ax, 0.4, 5.1, 1.9, 1.0, "主机", "MCU", PINK, fs=9)
    for i, (name, addr) in enumerate([("从机 A", "0x3C"), ("从机 B", "0x68")]):
        box(ax, 5.2 + i * 2.6, 5.1, 1.9, 1.0, name, addr, BLUE, fs=9, sfs=7.5)
    # SDA / SCL
    ax.plot([2.3, 11.4], [6.0, 6.0], color=RED, lw=1.8)
    ax.plot([2.3, 11.4], [5.6, 5.6], color="#2c3e50", lw=1.8)
    ax.text(11.55, 6.0, "SDA", fontsize=8.5, color=RED, va="center")
    ax.text(11.55, 5.6, "SCL", fontsize=8.5, color="#2c3e50", va="center")
    # 上拉
    ax.text(3.4, 6.15, "两线都要上拉电阻（4.7k）", fontsize=8, color=RED)

    # ---- SPI ----
    ax.text(0.4, 4.35, "SPI：4 根线 + 每个从机一根 CS（要带宽）",
            fontsize=10.5, fontweight="bold", color=TEXT)
    box(ax, 0.4, 2.5, 1.9, 1.0, "主机", "MCU", PINK, fs=9)
    box(ax, 5.2, 2.95, 1.9, 1.0, "从机 A", "屏幕", BLUE, fs=9, sfs=7.5)
    box(ax, 5.2, 1.55, 1.9, 1.0, "从机 B", "Flash", BLUE, fs=9, sfs=7.5)

    for y, lb in [(3.45, "SCLK"), (3.05, "MOSI"), (2.65, "MISO")]:
        ax.plot([2.3, 5.15], [y, y], color="#2c3e50", lw=1.4)
        ax.text(2.42, y + 0.1, lb, fontsize=7.5, color=LINE)
    # 数据线延伸到从机 B
    for y in (3.05, 2.65):
        ax.plot([5.15, 5.15], [y, y], lw=0)
    ax.plot([7.1, 7.1], [3.45, 2.05], color="#2c3e50", lw=1.0, ls=":")
    ax.text(7.2, 2.75, "SCLK/MOSI/MISO\n共用（并联）", fontsize=7.5, color=LINE)

    # CS
    ax.plot([2.3, 5.15], [2.35, 2.35], color=RED, lw=1.6)
    ax.text(2.42, 2.2, "CS_A", fontsize=7.5, color=RED)
    ax.plot([2.3, 5.15], [1.75, 1.75], color=RED, lw=1.6)
    ax.text(2.42, 1.6, "CS_B", fontsize=7.5, color=RED)

    # 对比表
    rows = [
        ("线数", "2（与设备数无关）", "4 + 每个从机 1 根 CS"),
        ("速度", "100k / 400k / 1M", "几 MHz ~ 36 MHz"),
        ("多设备", "靠 7 位地址", "靠 CS 片选（低有效）"),
        ("上拉电阻", "必须", "不需要"),
        ("典型用途", "传感器、小 OLED", "彩屏、SD 卡、Flash"),
    ]
    ax.text(0.4, 1.05, "怎么选：", fontsize=9.5, fontweight="bold", color=TEXT)
    for i, (k, a, b) in enumerate(rows):
        yy = 0.72 - i * 0.31
        ax.text(1.5, yy, k, fontsize=8, color=TEXT, fontweight="bold")
        ax.text(3.4, yy, a, fontsize=8, color=TEXT)
        ax.text(7.6, yy, b, fontsize=8, color=TEXT)
        if i == 0:
            ax.text(3.4, yy + 0.22, "I2C", fontsize=7.5, color=RED)
            ax.text(7.6, yy + 0.22, "SPI", fontsize=7.5, color=RED)

    _save(fig, "i2c-vs-spi.svg")


def python_decorator():
    """装饰器：函数被"套一层"的过程"""
    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 7.4)
    ax.set_axis_off()
    ax.text(0.2, 7.0, "装饰器：把函数传进去，换一个新函数出来", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 定义阶段
    ax.text(0.4, 6.3, "① 定义时（只发生一次）", fontsize=10.5,
            fontweight="bold", color=TEXT)
    box(ax, 0.4, 4.9, 2.7, 0.95, "@timer", "装饰器函数", PINK, fs=9.5, sfs=7.5)
    box(ax, 4.2, 4.9, 2.7, 0.95, "def work()", "原函数", BLUE, fs=9.5, sfs=7.5)
    box(ax, 8.0, 4.9, 3.4, 0.95, "wrapper", "包了一层的新函数", GREEN, fs=9.5, sfs=7.5)
    arrow(ax, (3.15, 5.37), (4.15, 5.37))
    arrow(ax, (6.95, 5.37), (7.95, 5.37))
    ax.text(3.45, 5.55, "接收", fontsize=8, color=RED)
    ax.text(7.15, 5.55, "返回", fontsize=8, color=RED)

    ax.text(0.4, 4.5, "等价于：work = timer(work)", fontsize=9,
            color=RED, fontweight="bold")
    ax.text(0.4, 4.15, "从此 work 这个名字指向 wrapper，原函数被捕获在闭包里",
            fontsize=8.8, color=TEXT)

    # 调用阶段
    ax.text(0.4, 3.55, "② 调用时（每次调用都走 wrapper）", fontsize=10.5,
            fontweight="bold", color=TEXT)
    calls = [
        ("work()", ORANGE),
        ("wrapper 开始", GREEN),
        ("t0 = time()", GREY),
        ("调用真正的原函数", BLUE),
        ("t1 = time()", GREY),
        ("print 耗时", GREEN),
        ("返回结果", ORANGE),
    ]
    for i, (c, color) in enumerate(calls):
        y = 2.85 - i * 0.36
        ax.add_patch(Rectangle((0.6, y - 0.13), 0.22, 0.28,
                               facecolor=color, edgecolor="#2c3e50", lw=0.8))
        ax.text(1.0, y, c, fontsize=8.8, color=TEXT, va="center")

    # 右侧说明
    ax.text(6.2, 2.85, "关键点", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "• 装饰器本身就是「接收函数、返回函数」",
        "• @ 语法只是 work = timer(work) 的糖",
        "• 原函数没变，只是被包在 wrapper 里",
        "• 不加 functools.wraps，work.__name__",
        "  会变成「wrapper」，调试时很迷惑",
        "",
        "带参数的装饰器要多一层：",
        "  @timer(unit=ms) → 先调用拿到真装饰器",
    ]
    for i, t in enumerate(pts):
        ax.text(6.2, 2.45 - i * 0.33, t, fontsize=8.6, color=TEXT)

    _save(fig, "python-decorator.svg")


def freertos_states():
    """FreeRTOS 任务状态与切换"""
    fig, ax = plt.subplots(figsize=(10.2, 6.2))
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "FreeRTOS 任务状态：同一时刻只有一个在跑",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 四个状态
    box(ax, 0.5, 5.4, 2.9, 1.2, "Running", "正在占用 CPU（单核只有一个）", GREEN, fs=10, sfs=7.2)
    box(ax, 5.3, 5.4, 2.9, 1.2, "Ready", "就绪，等着被调度", BLUE, fs=10, sfs=7.2)
    box(ax, 0.5, 2.6, 2.9, 1.2, "Blocked", "等事件/等延时（不占 CPU）", ORANGE, fs=10, sfs=7.2)
    box(ax, 5.3, 2.6, 2.9, 1.2, "Suspended", "被 vTaskSuspend 挂起", GREY, fs=10, sfs=7.2)

    # 箭头
    arrow(ax, (3.45, 6.2), (5.25, 6.2), color=RED, lw=1.8)
    ax.text(3.7, 6.42, "被更高优先级抢占\n或时间片用完", fontsize=7.6, color=RED)

    arrow(ax, (5.25, 5.7), (3.45, 5.7), color="#2c3e50", lw=1.6)
    ax.text(3.7, 5.28, "调度器选它", fontsize=7.6, color="#2c3e50")

    arrow(ax, (2.0, 5.35), (2.0, 3.85), color="#c0392b", lw=1.8)
    ax.text(2.15, 4.55, "vTaskDelay / 等队列\n等信号量", fontsize=7.6, color="#c0392b")

    arrow(ax, (1.4, 3.85), (1.4, 5.35), color="#1e8449", lw=1.6)
    ax.text(0.28, 4.55, "事件到达\n或延时到", fontsize=7.6, color="#1e8449")

    arrow(ax, (6.75, 5.35), (6.75, 3.85), color=LINE, lw=1.4, style="-|>")
    arrow(ax, (7.3, 3.85), (7.3, 5.35), color=LINE, lw=1.4, style="-|>")
    ax.text(7.5, 4.6, "挂起/恢复", fontsize=7.6, color=LINE)

    # 要点
    ax.text(9.0, 5.9, "几个必须记住的点", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "• 单核：Running 永远只有一个",
        "• Blocked 不占 CPU（vTaskDelay 就在这里）",
        "• 优先级数字越大越高（和 NVIC 中断相反）",
        "• 同优先级 + 时间片 → 轮转",
        "• 就绪的最高优先级任务一定在跑",
        "• 任务里没有 vTaskDelay/阻塞等待",
        "  → 低优先级任务永远得不到 CPU（饿死）",
    ]
    for i, t in enumerate(pts):
        ax.text(9.0, 5.5 - i * 0.42, t, fontsize=8.4, color=TEXT)

    # 底部说明
    ax.text(0.4, 1.5, "最常见的两个错误：", fontsize=9.5, fontweight="bold", color=RED)
    ax.text(0.4, 1.1, "① 最高优先级任务写成死循环且不 vTaskDelay → 整个系统只剩它在跑",
            fontsize=8.6, color=TEXT)
    ax.text(0.4, 0.72, "② 在中断里调用非 FromISR 版本的 API → 内核状态被破坏，随机死机",
            fontsize=8.6, color=TEXT)
    ax.text(0.4, 0.3, "排查手段：uxTaskGetStackHighWaterMark 看栈、vTaskList 打任务表",
            fontsize=8.6, color=LINE)

    _save(fig, "freertos-states.svg")


if __name__ == "__main__":
    stm32_clock_tree()
    linux_boot_chain()
    python_list_growth()
    i2c_vs_spi()
    python_decorator()
    freertos_states()
    print("done")
