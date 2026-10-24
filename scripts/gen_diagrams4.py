"""第四批示意图：内存布局 / 状态机 / 调用约定 / 分层结构。

用法: python scripts/gen_diagrams4.py
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
rcParams["text.parse_math"] = False   # 避免 $ 被当成 mathtext 分隔符

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


def c_compile_stages():
    """C 编译四阶段（带实测数字）"""
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "C 从源码到可执行文件：四个阶段（附实测体积）",
            fontsize=12.5, fontweight="bold", color=TEXT)

    stages = [
        ("hello.c", "你写的源码", 0.4, BLUE),
        ("hello.i", "预处理后\n展开头文件与宏", 3.1, ORANGE),
        ("hello.s", "汇编代码\n人类还能看懂", 5.8, PURPLE),
        ("hello.o", "目标文件\n机器码 + 符号表", 8.5, PINK),
        ("a.out", "可执行文件\n链接库之后", 11.2, GREEN),
    ]
    w, h, y = 2.1, 1.25, 5.6
    for name, sub, x, color in stages:
        box(ax, x, y, w, h, name, sub, color, fs=10, sfs=7.4)
    for i in range(len(stages) - 1):
        x1 = stages[i][2] + w
        x2 = stages[i + 1][2]
        arrow(ax, (x1, y + h / 2), (x2, y + h / 2))

    # 阶段名
    labels = ["① 预处理", "② 编译", "③ 汇编", "④ 链接"]
    for i, lb in enumerate(labels):
        xm = (stages[i][2] + w + stages[i + 1][2]) / 2
        ax.text(xm, y + h + 0.22, lb, ha="center", fontsize=8.5,
                color=RED, fontweight="bold")

    # 命令
    cmds = ["gcc -E", "gcc -S", "gcc -c", "gcc（不带 -c）"]
    for i, c in enumerate(cmds):
        ax.text(stages[i][2] + w / 2, y - 0.28, c, ha="center",
                fontsize=8, color=LINE)

    # 实测数字
    ax.text(0.4, 4.55, "本机实测（一个 hello world）", fontsize=10.5,
            fontweight="bold", color=TEXT)
    rows = [
        ("hello.c", "源码", "10 行左右"),
        ("hello.i", "预处理后", "约 1750 行（stdio.h 展开进来）"),
        ("hello.s", "汇编", "约 76 行"),
        ("hello.o", "目标文件", "约 1053 字节"),
        ("a.out", "可执行", "约 67072 字节（静态链接更多）"),
    ]
    for i, (k, kind, v) in enumerate(rows):
        yy = 4.05 - i * 0.42
        ax.text(0.6, yy, k, fontsize=9, color=TEXT, fontweight="bold")
        ax.text(2.6, yy, kind, fontsize=8.6, color=LINE)
        ax.text(5.2, yy, v, fontsize=8.6, color=TEXT)

    ax.text(0.4, 1.35, "四阶段各自会报什么错（这个对应关系很有用）",
            fontsize=10, fontweight="bold", color=TEXT)
    errs = [
        ("① 预处理", "#include 找不到 / 宏定义写错"),
        ("② 编译", "语法错误，有行号 —— 最常见的报错都在这一步"),
        ("③ 汇编", "极少报错"),
        ("④ 链接", "undefined reference（函数声明了但没定义）"),
    ]
    for i, (k, v) in enumerate(errs):
        yy = 0.92 - i * 0.24
        ax.text(0.6, yy, k, fontsize=8.4, color=RED, fontweight="bold")
        ax.text(2.4, yy, v, fontsize=8.4, color=TEXT)

    _save(fig, "c-compile-stages.svg")


def c_stack_frame():
    """函数调用时的栈帧布局"""
    fig, ax = plt.subplots(figsize=(10.4, 6.6))
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "函数调用时的栈帧：局部变量住在哪", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 栈方向
    ax.text(0.4, 7.25, "高地址（栈底）", fontsize=8.8, color=LINE)
    ax.annotate("", xy=(0.9, 1.2), xytext=(0.9, 7.05),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.4))
    ax.text(1.05, 3.9, "栈向下增长", fontsize=9, color=LINE, rotation=90,
            va="center")

    # 各层
    frame = [
        ("调用者的栈帧", "……", GREY, 6.1, 0.85),
        ("函数参数", "a, b（部分通过寄存器传递）", ORANGE, 5.15, 0.85),
        ("返回地址", "调用结束后跳回哪里", PINK, 4.2, 0.85),
        ("保存的 rbp", "调用者的栈基址", PURPLE, 3.25, 0.85),
        ("局部变量", "int x; char buf[16];", BLUE, 2.3, 0.85),
        ("……", "（向下还有空间给更深调用）", GREY, 1.35, 0.85),
    ]
    for label, sub, color, y, h in frame:
        ax.add_patch(Rectangle((1.6, y), 5.2, h, facecolor=color,
                               edgecolor=DARK, lw=1.1, alpha=0.92))
        ax.text(2.0, y + h / 2, label, fontsize=9.2, color=TEXT,
                va="center", fontweight="bold")
        ax.text(4.4, y + h / 2, sub, fontsize=8.2, color=TEXT, va="center")

    # rsp / rbp 指示
    ax.annotate("rsp（栈顶）", xy=(6.85, 1.45), xytext=(7.25, 1.45),
                fontsize=8.8, color=RED, va="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.annotate("rbp（栈基址）", xy=(6.85, 3.6), xytext=(7.25, 3.6),
                fontsize=8.8, color=RED, va="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))

    # 右侧说明
    ax.text(9.5, 6.6, "三个关键结论", fontsize=10.5, fontweight="bold", color=TEXT)
    pts = [
        "• 局部变量在栈上，函数返回就失效",
        "  （所以绝不能返回局部变量的地址）",
        "",
        "• 每次调用都会新建一帧，递归深了",
        "  就会栈溢出 —— 单片机栈只有几 KB",
        "",
        "• 返回地址也在栈上，被缓冲区溢出",
        "  覆盖时会跳到任意地址 —— 这是",
        "  经典攻击手法，也是为什么 scanf",
        "  要限制长度",
    ]
    for i, t in enumerate(pts):
        ax.text(9.5, 6.15 - i * 0.42, t, fontsize=8.5, color=TEXT)

    ax.text(0.4, 0.45,
            "注：参数和返回值优先走寄存器（x86-64 前 6 个整数参数用 rdi/rsi/rdx…），"
            "放不下的才压栈。上图是概念示意。",
            fontsize=8.2, color=LINE)

    _save(fig, "c-stack-frame.svg")


def cpp_move():
    """C++ 移动语义：深拷贝 vs 偷指针"""
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "移动语义：把大块数据「偷」过来，而不是复制一遍",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # ---- 拷贝 ----
    ax.text(0.4, 6.75, "拷贝（copy）：分配新内存，逐个字节复制",
            fontsize=10.5, fontweight="bold", color=TEXT)
    box(ax, 0.4, 5.5, 1.75, 0.9, "buf_a", "指针", ORANGE, fs=9)
    box(ax, 3.2, 5.5, 3.0, 0.9, "堆内存（已分配）", "100 万字节数据", BLUE, fs=9, sfs=7.5)
    arrow(ax, (2.2, 5.95), (3.15, 5.95))

    box(ax, 0.4, 4.3, 1.75, 0.9, "buf_b", "指针", ORANGE, fs=9)
    box(ax, 3.2, 4.3, 3.0, 0.9, "新堆内存", "又复制了一份 100 万字节", PINK, fs=9, sfs=7.5)
    arrow(ax, (2.2, 4.75), (3.15, 4.75))
    ax.text(6.45, 4.75, "慢：要 alloc + memcpy", fontsize=8.6, color=RED, va="center")

    # ---- 移动 ----
    ax.text(0.4, 3.6, "移动（move）：只交换指针，O(1)",
            fontsize=10.5, fontweight="bold", color=TEXT)
    box(ax, 0.4, 2.35, 1.75, 0.9, "buf_a", "变成 nullptr", GREY, fs=9, sfs=7.5)
    box(ax, 3.2, 2.35, 3.0, 0.9, "堆内存（原封不动）", "数据一个字节都没动", GREEN, fs=9, sfs=7.5)

    box(ax, 0.4, 1.15, 1.75, 0.9, "buf_b", "接管指针", ORANGE, fs=9)
    arrow(ax, (2.2, 1.6), (3.15, 1.6))
    ax.text(6.45, 1.6, "快：只赋值一个指针", fontsize=8.6, color="#1e8449", va="center")
    arrow(ax, (2.2, 2.8), (3.15, 2.8), color=LINE, lw=1.2, ls=":")

    # 右侧要点
    ax.text(9.2, 5.9, "为什么快", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "• std::move 本身不搬任何数据",
        "  它只是把左值转成右值引用",
        "• 真正干活的是移动构造函数",
        "",
        "必须记住两条：",
        "• 移动构造要标 noexcept",
        "  否则 vector 扩容宁可用拷贝",
        "• 必须把源对象指针置空",
        "  否则 double free",
    ]
    for i, t in enumerate(pts):
        ax.text(9.2, 5.45 - i * 0.4, t, fontsize=8.4, color=TEXT)
        if t.startswith("必须"):
            pass

    ax.text(0.4, 0.45,
            "代价：移动之后源对象处于「有效但未指定」状态，不要再读它的值。",
            fontsize=8.4, color=RED)

    _save(fig, "cpp-move-semantics.svg")


def linux_process_states():
    """Linux 进程状态机（ps 的 STAT 列）"""
    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "Linux 进程状态：ps 命令 STAT 列那些字母什么意思",
            fontsize=12.5, fontweight="bold", color=TEXT)

    box(ax, 0.6, 5.6, 2.5, 1.1, "R", "Running / Runnable\n运行或就绪", GREEN, fs=14, sfs=7.4)
    box(ax, 4.3, 5.6, 2.5, 1.1, "S", "Interruptible sleep\n可中断睡眠（最常见）", BLUE, fs=14, sfs=7.4)
    box(ax, 8.0, 5.6, 2.5, 1.1, "D", "Uninterruptible\n不可中断（等 IO）", ORANGE, fs=14, sfs=7.4)
    box(ax, 4.3, 3.2, 2.5, 1.1, "T", "Stopped\n被暂停（Ctrl+Z）", PURPLE, fs=14, sfs=7.4)
    box(ax, 8.0, 3.2, 2.5, 1.1, "Z", "Zombie\n已退出但父进程没回收", PINK, fs=14, sfs=7.4)

    arrow(ax, (3.15, 6.15), (4.25, 6.15))
    ax.text(3.2, 6.4, "等事件", fontsize=8, color=RED)
    arrow(ax, (4.25, 5.75), (3.15, 5.75), color=LINE)
    ax.text(3.2, 5.42, "事件到达", fontsize=8, color=LINE)

    arrow(ax, (6.85, 6.15), (7.95, 6.15))
    ax.text(7.0, 6.4, "等磁盘 IO", fontsize=8, color=RED)

    arrow(ax, (4.9, 5.55), (4.9, 4.35), color=PURPLE)
    ax.text(3.55, 4.95, "Ctrl+Z / SIGSTOP", fontsize=8, color=PURPLE)
    arrow(ax, (6.3, 4.35), (6.3, 5.55), color=LINE)
    ax.text(6.45, 4.95, "SIGCONT", fontsize=8, color=LINE)

    arrow(ax, (9.25, 5.55), (9.25, 4.35), color=PINK)
    ax.text(9.4, 4.9, "退出但父进程\n没 wait()", fontsize=7.8, color=PINK)

    # 说明
    ax.text(0.6, 2.5, "五种状态各自的现实含义", fontsize=10.5,
            fontweight="bold", color=TEXT)
    rows = [
        ("R", "真的在占 CPU，或排队等着。系统卡顿时这个状态很多。", GREEN),
        ("S", "在等某个事件（sleep、等输入、等网络）。绝大多数进程都是 S，正常。", BLUE),
        ("D", "在等不能被打断的 IO（通常是磁盘）。杀不掉！只能等 IO 完成或重启。", ORANGE),
        ("T", "被人为暂停了。用 kill -CONT 恢复。", PURPLE),
        ("Z", "已经死了，但父进程没调用 wait() 收尸。占着 PID 不释放。", PINK),
    ]
    for i, (k, v, color) in enumerate(rows):
        yy = 2.05 - i * 0.42
        ax.add_patch(Rectangle((0.6, yy - 0.13), 0.4, 0.3, facecolor=color,
                               edgecolor=DARK, lw=0.9))
        ax.text(0.8, yy, k, ha="center", fontsize=9, color=TEXT,
                va="center", fontweight="bold")
        ax.text(1.25, yy, v, fontsize=8.4, color=TEXT, va="center")

    ax.text(0.6, -0.15, "另外常见的修饰符：s = 会话首进程，l = 多线程，+ = 在前台进程组，< = 高优先级",
            fontsize=8.2, color=LINE)

    _save(fig, "linux-process-states.svg")


def linux_fd_table():
    """文件描述符的三层结构"""
    fig, ax = plt.subplots(figsize=(10.6, 6.8))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 9.4)
    ax.set_axis_off()
    ax.text(0.2, 9.0, "文件描述符：一个整数背后的三层结构", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 层标题
    ax.text(0.5, 8.35, "① 进程的 fd 表", fontsize=9.5, fontweight="bold", color=TEXT)
    ax.text(4.2, 8.35, "② 系统打开文件表", fontsize=9.5, fontweight="bold", color=TEXT)
    ax.text(8.6, 8.35, "③ inode（磁盘上）", fontsize=9.5, fontweight="bold", color=TEXT)

    # fd 表：4 项，间距 0.78
    fds = [("0", "stdin"), ("1", "stdout"), ("2", "stderr"), ("3", "你的文件")]
    for i, (n, name) in enumerate(fds):
        y = 7.5 - i * 0.78
        ax.add_patch(Rectangle((0.5, y), 0.55, 0.58, facecolor=ORANGE,
                               edgecolor=DARK, lw=1.0))
        ax.text(0.775, y + 0.29, n, ha="center", va="center", fontsize=10,
                color=TEXT, fontweight="bold")
        ax.add_patch(Rectangle((1.1, y), 1.7, 0.58,
                               facecolor=PINK if i < 3 else BLUE,
                               edgecolor=DARK, lw=1.0))
        ax.text(1.95, y + 0.29, name, ha="center", va="center", fontsize=8.2,
                color=TEXT)

    # 文件表 / inode 对准第 4 项
    box(ax, 4.2, 4.95, 3.0, 1.0, "打开文件表项", "读写位置 offset\n打开模式 O_RDWR", GREEN, fs=9, sfs=7.4)
    arrow(ax, (2.85, 5.45), (4.15, 5.45))

    box(ax, 8.6, 4.95, 4.2, 1.0, "inode", "权限、大小、时间、数据块位置", PURPLE, fs=9.5, sfs=7.4)
    arrow(ax, (7.25, 5.45), (8.55, 5.45))

    # 说明
    ax.text(0.5, 4.2, "为什么要有中间这一层？", fontsize=10.5,
            fontweight="bold", color=TEXT)
    pts = [
        "• fd 只是进程内数组的下标 —— 所以每个进程的 0/1/2 互不相干",
        "• 中间的 offset 是「一次打开」的状态：同一文件两次 open 得到两个独立",
        "  offset，各读各的，互不干扰",
        "• fork 出来的子进程共享文件表项 —— 父子俩「抢着读」，offset 是同一个",
        "• dup / dup2 让两个 fd 指向同一个表项 —— 这是 shell 重定向的实现",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 3.72 - i * 0.42, s, fontsize=8.6, color=TEXT)

    # 重定向例子
    ax.text(0.5, 1.35, "shell 重定向是怎么实现的：", fontsize=10,
            fontweight="bold", color=TEXT)
    ax.text(0.5, 0.95,
            "命令 > out.txt   等价于   先 open(out.txt) 得到 fd 3，"
            "再 dup2(3, 1) 把 1 号改指向它，然后 close(3)",
            fontsize=8.6, color=TEXT)
    ax.text(0.5, 0.55, "所以程序里 printf 写 1 号 fd，数据就进了文件 —— 程序自己毫不知情。",
            fontsize=8.6, color=RED)
    ax.text(0.5, 0.15, "常用命令：ls -l /proc/$$/fd    查看当前 shell 打开了哪些 fd",
            fontsize=8.4, color=LINE)

    _save(fig, "linux-fd-table.svg")


def esp32_memory():
    """ESP32 内存分区"""
    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "ESP32 的内存：三种存储，各管各的", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 片内
    ax.text(0.4, 7.05, "片内（芯片里，最快）", fontsize=9.8, fontweight="bold", color=TEXT)
    box(ax, 0.4, 5.6, 3.0, 1.15, "IRAM  约 200 KB", "代码 + 中断处理函数\nIRAM_ATTR 放这里", PURPLE, fs=9, sfs=7.2)
    box(ax, 3.7, 5.6, 3.0, 1.15, "DRAM  约 300 KB", "全局变量 + 堆\n（可用堆约 200~300KB）", BLUE, fs=9, sfs=7.2)
    box(ax, 7.0, 5.6, 2.6, 1.15, "RTC 内存  8 KB", "深睡保留\nRTC_DATA_ATTR", GREEN, fs=9, sfs=7.2)

    # 片外
    ax.text(0.4, 4.85, "片外（通过 SPI 访问，慢一些但大）", fontsize=9.8,
            fontweight="bold", color=TEXT)
    box(ax, 0.4, 3.4, 4.2, 1.15, "Flash  4~16 MB", "存放固件、文件系统、NVS\n掉电不丢", ORANGE, fs=9.5, sfs=7.2)
    box(ax, 5.1, 3.4, 3.6, 1.15, "PSRAM  2~8 MB", "大缓冲（图像/音频）\n比 DRAM 慢 3~10 倍", PINK, fs=9.5, sfs=7.2)

    # 说明
    ax.text(0.4, 2.7, "最容易踩的三个坑", fontsize=10.5, fontweight="bold", color=RED)
    pts = [
        ("栈溢出", "每个任务的栈是独立的几 KB，在任务里开 8KB 局部数组直接崩。报错：stack overflow in task xxx"),
        ("堆碎片", "总量够但最大连续块很小。用 heap_caps_get_largest_free_block 查，而不是只看 free"),
        ("把 PSRAM 当栈", "PSRAM 走 SPI，访问慢 3~10 倍。它只适合放大缓冲，不适合放栈和高频访问的变量"),
    ]
    for i, (k, v) in enumerate(pts):
        yy = 2.25 - i * 0.55
        ax.text(0.5, yy, "· " + k + "：", fontsize=9, color=RED, fontweight="bold")
        ax.text(2.55, yy, v, fontsize=8.3, color=TEXT)

    ax.text(0.4, 0.5, "查内存的三个函数：", fontsize=9, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.18,
            "esp_get_free_heap_size()   esp_get_minimum_free_heap_size()（持续下降=泄漏）   "
            "heap_caps_get_largest_free_block()（看碎片）",
            fontsize=8.2, color=TEXT)

    _save(fig, "esp32-memory-map.svg")


if __name__ == "__main__":
    c_compile_stages()
    c_stack_frame()
    cpp_move()
    linux_process_states()
    linux_fd_table()
    esp32_memory()
    print("done")
