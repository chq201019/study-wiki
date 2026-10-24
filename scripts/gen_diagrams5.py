"""第五批示意图：协议时序 / 运行时机制 / 构建规则 / 初始化流程。

用法: python scripts/gen_diagrams5.py
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

BLUE = "#7fb3d5"
PINK = "#e8b4b8"
ORANGE = "#f5cba7"
GREEN = "#a9dfbf"
PURPLE = "#d2b4de"
GREY = "#d5dbdb"
TEXT = "#1b2631"
LINE = "#5d6d7e"
RED = "#c0392b"
DARK = "#2c3e50"


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


def tcp_handshake():
    """TCP 三次握手与四次挥手"""
    fig, ax = plt.subplots(figsize=(10.6, 7.0))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 9.6)
    ax.set_axis_off()
    ax.text(0.2, 9.2, "TCP 三次握手与四次挥手：为什么是 3 和 4", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 两端
    box(ax, 0.8, 7.7, 2.3, 0.85, "客户端", "主动发起", BLUE, fs=9.5, sfs=7.4)
    box(ax, 9.6, 7.7, 2.3, 0.85, "服务器", "被动接受", GREEN, fs=9.5, sfs=7.4)
    ax.plot([1.95, 1.95], [7.65, 0.9], color=LINE, lw=1.2, ls=":")
    ax.plot([10.75, 10.75], [7.65, 0.9], color=LINE, lw=1.2, ls=":")

    steps = [
        (7.0, "→", "① SYN  seq=x", "我想连你，我的序号是 x", RED),
        (6.15, "←", "② SYN+ACK  seq=y, ack=x+1", "收到，我也想连你，序号 y", "#1e8449"),
        (5.3, "→", "③ ACK  ack=y+1", "收到你的，连接建立", RED),
    ]
    for y, d, label, sub, color in steps:
        if d == "→":
            arrow(ax, (2.05, y), (10.6, y), color=color, lw=1.8)
            ax.text(3.0, y + 0.16, label, fontsize=8.8, color=color, fontweight="bold")
            ax.text(3.0, y - 0.28, sub, fontsize=7.8, color=TEXT)
        else:
            arrow(ax, (10.6, y), (2.05, y), color=color, lw=1.8)
            ax.text(4.4, y + 0.16, label, fontsize=8.8, color=color, fontweight="bold")
            ax.text(4.4, y - 0.28, sub, fontsize=7.8, color=TEXT)

    ax.text(0.8, 4.72, "上面：三次握手　｜　下面：四次挥手", fontsize=8.4, color=LINE)

    fin = [
        (4.35, "→", "④ FIN", "我要关了", RED),
        (3.5, "←", "⑤ ACK", "知道了", "#1e8449"),
        (2.65, "←", "⑥ FIN", "我也关了", "#1e8449"),
        (1.8, "→", "⑦ ACK", "知道了，再见", RED),
    ]
    for y, d, label, sub, color in fin:
        if d == "→":
            arrow(ax, (2.05, y), (10.6, y), color=color, lw=1.6)
            ax.text(3.0, y + 0.14, label, fontsize=8.4, color=color, fontweight="bold")
            ax.text(4.6, y + 0.14, sub, fontsize=7.6, color=TEXT)
        else:
            arrow(ax, (10.6, y), (2.05, y), color=color, lw=1.6)
            ax.text(4.4, y + 0.14, label, fontsize=8.4, color=color, fontweight="bold")
            ax.text(5.6, y + 0.14, sub, fontsize=7.6, color=TEXT)

    # 右栏说明
    ax.text(11.2, 4.78, "为什么不是 2 次", fontsize=9.5, fontweight="bold", color=RED)
    notes = [
        "两次不够：",
        "客户端发的 SYN 若超时重传，",
        "服务器可能收到两份，误以为",
        "要建两个连接。三次能确认",
        "「对方确实收到了我的应答」。",
        "",
        "为什么挥手要 4 次：",
        "TCP 是全双工，两个方向要",
        "各自关闭。收到 FIN 只代表",
        "对方没数据发了，我这边",
        "还可以继续发 —— 所以 ACK",
        "和 FIN 要分两次发。",
        "",
        "TIME_WAIT 等 2MSL：",
        "最后那个 ACK 可能丢，",
        "留着才能重发。",
    ]
    for i, s in enumerate(notes):
        ax.text(11.2, 4.35 - i * 0.245, s, fontsize=7.4, color=TEXT)

    ax.text(0.4, 0.28,
            "排查工具：ss -tan 看连接状态；tcpdump -i any port 80 看握手过程。",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.02,
            "大量 TIME_WAIT 通常是短连接太多 —— 改用长连接，或调内核参数。",
            fontsize=8.2, color=LINE)

    _save(fig, "net-tcp-handshake.svg")


def python_gil():
    """Python GIL：为什么多线程不能并行算"""
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "GIL：同一时刻只有一个线程在执行 Python 字节码",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 时间轴
    ax.plot([0.8, 12.6], [6.5, 6.5], color=LINE, lw=1.2)
    for i in range(0, 13):
        ax.plot([0.8 + i * 0.95, 0.8 + i * 0.95], [6.4, 6.6], color=LINE, lw=0.8)
    ax.text(0.8, 6.75, "时间 →", fontsize=8.5, color=LINE)

    # CPU 密集：交替执行
    ax.text(0.4, 5.85, "① CPU 密集（算数）：线程轮流用 CPU，总耗时 ≈ 串行",
            fontsize=9.8, fontweight="bold", color=TEXT)
    seg = [(BLUE, "T1"), (ORANGE, "T2"), (BLUE, "T1"), (ORANGE, "T2"),
           (BLUE, "T1"), (ORANGE, "T2")]
    for i, (c, lb) in enumerate(seg):
        x = 0.8 + i * 1.9
        ax.add_patch(Rectangle((x, 4.9), 1.85, 0.72, facecolor=c,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 0.92, 5.26, lb, ha="center", va="center", fontsize=8.5,
                color=TEXT, fontweight="bold")
    ax.text(12.4, 5.26, "并行度 1", fontsize=8.5, color=RED, va="center")

    # IO 密集：真实并行
    ax.text(0.4, 4.15, "② IO 密集（等网络/磁盘）：等待时释放 GIL，其他线程能跑",
            fontsize=9.8, fontweight="bold", color=TEXT)
    # T1 等待
    ax.add_patch(Rectangle((0.8, 3.2), 4.0, 0.72, facecolor=GREY, edgecolor=DARK, lw=1.0))
    ax.text(2.8, 3.56, "T1 等待网络（已释放 GIL）", ha="center", va="center",
            fontsize=8.2, color=TEXT)
    # T2 计算
    ax.add_patch(Rectangle((5.0, 3.2), 6.6, 0.72, facecolor=ORANGE, edgecolor=DARK, lw=1.0))
    ax.text(8.3, 3.56, "T2 用 CPU（拿到 GIL）", ha="center", va="center",
            fontsize=8.5, color=TEXT, fontweight="bold")
    ax.text(12.4, 3.56, "并行度 2", fontsize=8.5, color="#1e8449", va="center")

    # 说明
    ax.text(0.4, 2.5, "所以结论很明确", fontsize=10.5, fontweight="bold", color=TEXT)
    rows = [
        ("CPU 密集（计算、图像处理）", "多线程没用，用 多进程 或 C 扩展", RED),
        ("IO 密集（网络、文件、数据库）", "多线程有效，因为等待时释放 GIL", "#1e8449"),
        ("想真正并行算", "multiprocessing / 子进程 / numpy 等释放 GIL 的库", ORANGE),
    ]
    for i, (k, v, c) in enumerate(rows):
        yy = 2.0 - i * 0.52
        ax.add_patch(Rectangle((0.5, yy - 0.14), 0.3, 0.3, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.0, yy, k, fontsize=8.8, color=TEXT, va="center", fontweight="bold")
        ax.text(4.9, yy, v, fontsize=8.6, color=TEXT, va="center")

    ax.text(0.4, 0.35,
            "GIL 是 CPython 的实现选择，不是 Python 语言规范。Jython / IronPython 没有 GIL。"
            "CPython 3.13 起提供了可选的 free-threading 构建。",
            fontsize=8.2, color=LINE)

    _save(fig, "python-gil.svg")


def cpp_vector_growth():
    """vector 扩容与迭代器失效"""
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "vector 扩容：为什么 push_back 会让迭代器全部失效",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 扩容前
    ax.text(0.4, 7.0, "扩容前：size=3, capacity=4，data 指向一块内存",
            fontsize=9.8, fontweight="bold", color=TEXT)
    box(ax, 0.4, 5.75, 1.5, 0.8, "vector", "size=3\ncap=4", ORANGE, fs=8.5, sfs=7)
    for i, v in enumerate(["a", "b", "c", None]):
        x = 3.0 + i * 0.9
        c = BLUE if v else GREY
        ax.add_patch(Rectangle((x, 5.75), 0.8, 0.8, facecolor=c,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 0.4, 6.15, v if v else "空", ha="center", va="center",
                fontsize=9.5, color=TEXT, fontweight="bold")
    arrow(ax, (1.95, 6.15), (2.95, 6.15))
    ax.text(3.0, 5.45, "旧内存（it 指向这里）", fontsize=8, color=RED)

    # 扩容动作
    ax.text(0.4, 4.85, "push_back 时发现 cap 满了 → 申请一块更大的新内存，"
                       "把元素搬过去，释放旧的",
            fontsize=9.2, color=TEXT)

    # 扩容后
    ax.text(0.4, 4.15, "扩容后：capacity 变成 8，data 指向另一块地址",
            fontsize=9.8, fontweight="bold", color=TEXT)
    box(ax, 0.4, 2.9, 1.5, 0.8, "vector", "size=4\ncap=8", ORANGE, fs=8.5, sfs=7)
    for i in range(8):
        x = 3.0 + i * 0.9
        v = ["a", "b", "c", "d"][i] if i < 4 else None
        c = GREEN if i < 4 else GREY
        ax.add_patch(Rectangle((x, 2.9), 0.8, 0.8, facecolor=c,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 0.4, 3.3, v if v else "空", ha="center", va="center",
                fontsize=9.5, color=TEXT, fontweight="bold")
    arrow(ax, (1.95, 3.3), (2.95, 3.3))
    ax.text(3.0, 2.6, "新内存（地址变了！旧迭代器全部悬空）", fontsize=8, color=RED)

    # 说明
    ax.text(0.4, 2.0, "三条实战规则", fontsize=10.5, fontweight="bold", color=TEXT)
    rules = [
        "① 循环里 push_back 后不要再用之前的迭代器 / 引用 / 指针",
        "② 要频繁 push_back 就先 reserve，一次性分配好",
        "③ 删除元素要用 it = v.erase(it) 接返回值，不能 ++it",
    ]
    for i, s in enumerate(rules):
        ax.text(0.5, 1.55 - i * 0.4, s, fontsize=8.8, color=TEXT)

    ax.text(0.4, 0.15,
            "实测增长倍数：MSVC ≈1.5 倍，libstdc++ / libc++ 是 2 倍。标准只要求均摊 O(1)，"
            "不规定倍数。",
            fontsize=8.2, color=LINE)

    _save(fig, "cpp-vector-growth.svg")


def python_generator():
    """生成器的暂停与恢复"""
    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "生成器：yield 把函数的执行状态「冻住」",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 函数体
    body = [
        ("def gen():", GREY, "定义时不执行"),
        ("    print(1)", BLUE, "第一次 next 执行到这里"),
        ("    yield 10", ORANGE, "产出 10，暂停（保留现场）"),
        ("    print(2)", BLUE, "第二次 next 从这里继续"),
        ("    yield 20", ORANGE, "产出 20，暂停"),
        ("    print(3)", BLUE, "第三次 next 继续"),
        ("    （函数结束）", GREY, "抛 StopIteration"),
    ]
    for i, (code, color, note) in enumerate(body):
        y = 6.7 - i * 0.72
        ax.add_patch(Rectangle((0.5, y), 4.3, 0.6, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        ax.text(0.7, y + 0.3, code, fontsize=9, color=TEXT, va="center")
        ax.text(5.0, y + 0.3, note, fontsize=8.4, color=TEXT, va="center")

    # 调用侧
    ax.text(10.0, 6.95, "调用侧的三个 next", fontsize=10, fontweight="bold", color=TEXT)
    calls = [
        ("next(g)  → 10", ORANGE),
        ("next(g)  → 20", ORANGE),
        ("next(g)  → StopIteration", PINK),
    ]
    for i, (c, color) in enumerate(calls):
        y = 6.3 - i * 0.62
        ax.add_patch(Rectangle((10.0, y - 0.05), 2.9, 0.5, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        ax.text(10.15, y + 0.2, c, fontsize=8.4, color=TEXT, va="center")

    # 箭头
    arrow(ax, (9.95, 6.50), (4.72, 5.56), color=RED, lw=1.4)
    arrow(ax, (9.95, 5.88), (4.72, 4.12), color=RED, lw=1.4)
    arrow(ax, (9.95, 5.26), (4.72, 2.68), color=RED, lw=1.4)

    # 关键点
    ax.text(0.5, 1.62, "三个必须记住的点", fontsize=10.5, fontweight="bold", color=TEXT)
    pts = [
        "• 调用 gen() 只创建生成器对象，函数体一行都不执行",
        "• yield 时保存了局部变量和执行位置 —— 所以下次能接着跑，这是它和普通 return 的本质区别",
        "• 好处是惰性 + 省内存：100 万个数不会一次性算完，用一个取一个",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 1.20 - i * 0.32, s, fontsize=8.6, color=TEXT)

    ax.text(0.5, 0.14, "常见的坑：生成器只能迭代一次；要重复用就先 list() 存下来（但这又失去省内存的意义了）。",
            fontsize=8.2, color=RED)

    _save(fig, "python-generator.svg")


def cpp_odr():
    """C++ 声明 / 定义 / ODR"""
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "声明与定义：什么能放头文件，什么必须放 cpp",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 三栏
    ax.text(0.5, 6.8, "声明（declaration）", fontsize=9.8, fontweight="bold", color=TEXT)
    ax.text(4.9, 6.8, "定义（definition）", fontsize=9.8, fontweight="bold", color=TEXT)
    ax.text(9.1, 6.8, "能放头文件吗", fontsize=9.8, fontweight="bold", color=TEXT)

    rows = [
        ("int f(int);", "只在 .cpp 写一次 int f(int){...}", "声明可以，定义不行", ORANGE),
        ("void g() {}", "这是定义，不能放头文件（除非 inline）", "不能 → 加 inline", PINK),
        ("class A { ... };", "类定义本身就是定义，但允许多份相同", "可以", GREEN),
        ("extern int x;", "int x = 0; 才是定义", "声明可以，定义不行", ORANGE),
        ("inline void h() {}", "inline 函数允许多份相同定义", "可以", GREEN),
        ("template<class T> ...", "模板必须让编译器看到完整定义", "必须放头文件", GREEN),
    ]
    for i, (decl, defi, ok, color) in enumerate(rows):
        y = 6.15 - i * 0.78
        ax.add_patch(Rectangle((0.5, y - 0.15), 3.8, 0.56, facecolor=color,
                               edgecolor=DARK, lw=0.9, alpha=0.85))
        ax.text(0.65, y + 0.13, decl, fontsize=8.2, color=TEXT, va="center")
        ax.text(4.9, y + 0.13, defi, fontsize=8.2, color=TEXT, va="center")
        ax.text(9.1, y + 0.13, ok, fontsize=8.2, color=RED, va="center",
                fontweight="bold")

    # ODR 解释
    ax.text(0.5, 1.45, "ODR（One Definition Rule）：同一个实体在整个程序里只能有一个定义",
            fontsize=9.8, fontweight="bold", color=RED)
    ax.text(0.5, 1.02, "违反的典型后果：", fontsize=9, color=TEXT)
    ax.text(2.5, 1.02, "multiple definition of f()   ← 头文件里放了普通函数定义，被多个 .cpp 包含",
            fontsize=8.5, color=TEXT)
    ax.text(0.5, 0.62, "另一个方向：", fontsize=9, color=TEXT)
    ax.text(2.5, 0.62, "undefined reference to f()  ← 声明了但没链接到定义（忘了加 .cpp 或写成 extern C）",
            fontsize=8.5, color=TEXT)
    ax.text(0.5, 0.2,
            "记忆法：头文件是「说明书」，.cpp 是「实现」。说明书可以复印很多份，实现只能有一份。",
            fontsize=8.4, color=LINE)

    _save(fig, "cpp-odr.svg")


def stm32_init_flow():
    """STM32 上电后的初始化流程"""
    fig, ax = plt.subplots(figsize=(10.4, 6.6))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "STM32 上电后发生了什么：main() 之前和之后",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 启动文件部分
    ax.text(0.4, 7.2, "① 启动文件（startup_xxx.s，汇编，你看不到）",
            fontsize=9.6, fontweight="bold", color=TEXT)
    asm = [
        ("初始化栈指针 SP", GREY),
        ("把 .data 从 Flash 拷到 RAM", GREY),
        ("把 .bss 段清零", GREY),
        ("调用 SystemInit()", GREY),
        ("跳转到 main()", GREY),
    ]
    for i, (s, c) in enumerate(asm):
        y = 6.6 - i * 0.42
        ax.add_patch(Rectangle((0.6, y - 0.13), 0.2, 0.28, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(0.95, y, s, fontsize=8.4, color=TEXT, va="center")

    # main 部分
    ax.text(6.0, 7.2, "② main() 里的四条初始化", fontsize=9.6,
            fontweight="bold", color=TEXT)
    mainc = [
        ("HAL_Init()", "SysTick 配成 1ms\nNVIC 优先级分组", BLUE),
        ("SystemClock_Config()", "HSE 8MHz × PLL9\n= 72MHz", ORANGE),
        ("MX_xxx_Init()", "CubeMX 生成：\nGPIO/USART/TIM…", GREEN),
        ("while (1) { ... }", "你的业务\n永不返回", PINK),
    ]
    for i, (name, sub, color) in enumerate(mainc):
        y = 6.15 - i * 1.12
        ax.add_patch(Rectangle((6.0, y), 6.6, 0.95, facecolor=color,
                               edgecolor=DARK, lw=1.1))
        ax.text(6.15, y + 0.66, name, fontsize=9, color=TEXT, va="center",
                fontweight="bold")
        ax.text(6.15, y + 0.24, sub, fontsize=7.6, color=TEXT, va="center",
                linespacing=1.35)
        if i < len(mainc) - 1:
            arrow(ax, (5.85, y), (5.85, y - 0.14), color=LINE, lw=1.2)

    # 关键提示
    ax.text(0.4, 3.5, "三个最常见的卡点", fontsize=10.2, fontweight="bold", color=RED)
    pts = [
        "① 程序根本不动 → 卡在 Error_Handler",
        "   （HSE 起振失败，或时钟配置非法）",
        "",
        "② 能跑但慢 9 倍 → 没配 SystemClock_Config",
        "   默认 HSI 8MHz，不是 72MHz",
        "",
        "③ 外设没反应 → 忘了 __HAL_RCC_xxx_CLK_ENABLE",
        "   不开外设时钟，配置全部静默失效",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 3.10 - i * 0.32, s, fontsize=8.4, color=TEXT)

    ax.text(0.4, 0.12,
            "调试技巧：在 Error_Handler 里打断点，谁跳进来就是谁初始化失败。"
            "这比一路 printf 快得多。",
            fontsize=8.4, color=LINE)

    _save(fig, "stm32-init-flow.svg")


if __name__ == "__main__":
    tcp_handshake()
    python_gil()
    cpp_vector_growth()
    python_generator()
    cpp_odr()
    stm32_init_flow()
    print("done")
