"""第六批示意图：拷贝语义 / 分区切换 / IO 多路复用 / 进程创建 / 对象生命周期 / 虚拟内存。

用法: python scripts/gen_diagrams6.py
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


def python_copy():
    """深拷贝与浅拷贝的差别"""
    fig, ax = plt.subplots(figsize=(10.8, 7.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 10.3)
    ax.set_axis_off()
    ax.text(0.2, 9.9, "浅拷贝 vs 深拷贝：嵌套结构只复制了第一层",
            fontsize=12.5, fontweight="bold", color=TEXT)

    def draw_row(y, outer_label, outer_sub, outer_color,
                 in1_label, in1_sub, in1_color,
                 in2_label, in2_sub, in2_color, note=None):
        box(ax, 0.5, y, 1.5, 0.72, outer_label, outer_sub, outer_color, fs=9, sfs=7.2)
        for k, (lb, sb, cc) in enumerate([(in1_label, in1_sub, in1_color),
                                          (in2_label, in2_sub, in2_color)]):
            yy = y + 0.36 - (k * 0.72)
            ax.add_patch(Rectangle((3.0, yy - 0.3), 2.6, 0.6, facecolor=cc,
                                   edgecolor=DARK, lw=1.0))
            ax.text(3.15, yy + 0.09, lb, fontsize=8, color=TEXT, va="center",
                    fontweight="bold")
            ax.text(3.15, yy - 0.17, sb, fontsize=7.2, color=TEXT, va="center")
            arrow(ax, (2.05, y + 0.36), (2.95, yy), lw=1.2)
        if note:
            ax.text(5.8, y + 0.36, note, fontsize=8, color=RED, va="center")

    ax.text(0.4, 9.35, "原始：a = [[1, 2], [3, 4]]　两个内层列表各自独立",
            fontsize=9.6, fontweight="bold", color=TEXT)
    draw_row(8.55, "a", "list", ORANGE,
             "内层[0]", "对象 [1,2]", GREEN,
             "内层[1]", "对象 [3,4]", GREEN)

    ax.text(0.4, 7.5, "① 浅拷贝 b = copy.copy(a) —— 只新建外层，内层仍指向原来两个对象",
            fontsize=9.4, fontweight="bold", color=RED)
    draw_row(6.25, "b", "新 list", ORANGE,
             "新槽位[0]", "指向上面那个", PINK,
             "新槽位[1]", "指向上面那个", PINK,
             note="← 新槽位装的是旧引用")
    ax.text(0.4, 5.25, "b[0].append(99)  →  a 也变了！这就是「头号坑」",
            fontsize=8.8, color=RED, fontweight="bold")

    ax.text(0.4, 4.65, "② 深拷贝 b = copy.deepcopy(a) —— 内层也复制成全新的对象",
            fontsize=9.4, fontweight="bold", color="#1e8449")
    draw_row(3.35, "b", "新 list", ORANGE,
             "新槽位[0]", "全新的 [1,2]", GREEN,
             "新槽位[1]", "全新的 [3,4]", GREEN,
             note="← 全是新对象，彻底独立")
    ax.text(0.4, 2.35, "b[0].append(99)  →  a 完全不受影响", fontsize=8.8,
            color="#1e8449", fontweight="bold")

    ax.text(0.4, 1.75, "另一种更隐蔽的浅拷贝来源（不需要 copy 模块）：",
            fontsize=9, fontweight="bold", color=TEXT)
    ax.text(0.4, 1.38, "b = a[:]　　　b = list(a)　　　b = a * 1"
                       "　　—— 切片、构造函数、重复运算都是浅拷贝",
            fontsize=8.4, color=TEXT)
    ax.text(0.4, 0.65,
            "记忆法：元素是不可变类型（int/str/tuple）时浅拷贝就够；元素是可变类型（list/dict）时必须深拷贝。",
            fontsize=8.2, color=LINE)

    _save(fig, "python-copy-depth.svg")

def esp32_ota_partition():
    """ESP32 OTA 双分区切换"""
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.85, "OTA 双分区：怎么做到升级失败还能回滚", fontsize=12.5,
            fontweight="bold", color=TEXT)

    COLS = [0.5, 4.6, 8.7]
    W = 3.6
    ROWS = [5.55, 4.75, 3.95, 3.15]
    H = 0.62

    stages = [
        ("① 正常运行", "Bootloader 读 otadata", [
            ("Bootloader", GREY),
            ("otadata → ota_0", PURPLE),
            ("ota_0：v1.0 运行中", GREEN),
            ("ota_1：空", GREY),
        ]),
        ("② 下载新固件", "写进另一个分区，不动正在跑的", [
            ("Bootloader", GREY),
            ("otadata → ota_0", PURPLE),
            ("ota_0：v1.0 运行中", GREEN),
            ("ota_1：写入 v1.1", ORANGE),
        ]),
        ("③ 校验通过后重启", "改 otadata 指向 ota_1", [
            ("Bootloader", GREY),
            ("otadata → ota_1", PINK),
            ("ota_0：v1.0 保留着", GREY),
            ("ota_1：v1.1 运行中", GREEN),
        ]),
    ]

    for ci, (title, sub, rows) in enumerate(stages):
        x = COLS[ci]
        ax.text(x, 7.35, title, fontsize=9.4, fontweight="bold", color=TEXT)
        ax.text(x, 7.02, sub, fontsize=7.6, color=LINE)
        for ri, (label, color) in enumerate(rows):
            y = ROWS[ri]
            ax.add_patch(Rectangle((x, y), W, H, facecolor=color,
                                   edgecolor=DARK, lw=1.0))
            ax.text(x + 0.12, y + H / 2, label, fontsize=7.8, color=TEXT,
                    va="center")

    ax.text(0.5, 2.72, "自检与回滚（产品必须实现）", fontsize=10,
            fontweight="bold", color=RED)
    pts = [
        "• 新固件首次启动状态是 ESP_OTA_IMG_PENDING_VERIFY",
        "• 自检通过后调 esp_ota_mark_app_valid_cancel_rollback() 确认",
        "• 自检失败则调 esp_ota_mark_app_invalid_rollback_and_reboot()",
        "  → Bootloader 自动回滚到上一个正常分区",
        "• 不实现这一步，坏固件会一直重启，只能拆机重烧",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 2.30 - i * 0.32, s, fontsize=8.4, color=TEXT)

    ax.text(0.5, 0.48, "分区表要求：必须有两个 app 分区（ota_0 / ota_1），Flash 至少 8MB 才宽裕。",
            fontsize=8.4, color=TEXT)
    ax.text(0.5, 0.14, "默认 singleapp 分区表只有一个 factory 分区 —— OTA 直接失败（update 句柄为 NULL）。",
            fontsize=8.4, color=RED)

    _save(fig, "esp32-ota-partition.svg")

def epoll_vs_select():
    """select / poll / epoll 的监听方式对比"""
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "同时监听 1000 个 fd：select、poll、epoll 的差别",
            fontsize=12.5, fontweight="bold", color=TEXT)

    N = 10   # 画 10 个格子代表 1000 个

    # select
    ax.text(0.4, 7.0, "① select：每次调用都把整个 fd 集合拷进内核，逐位扫描",
            fontsize=9.4, fontweight="bold", color=TEXT)
    for i in range(N):
        x = 0.6 + i * 0.92
        active = i == 8
        c = GREEN if active else GREY
        ax.add_patch(Rectangle((x, 6.15), 0.8, 0.5, facecolor=c,
                               edgecolor=DARK, lw=0.9))
        ax.text(x + 0.4, 6.4, "1" if active else "0", ha="center", va="center",
                fontsize=7.5, color=TEXT)
    ax.text(10.0, 6.4, "扫 1000 次", fontsize=8.4, color=RED, va="center",
            fontweight="bold")
    ax.text(0.5, 5.75, "内核要遍历全部 1000 个，才知道哪些就绪。每次调用都要重新拷一遍集合。",
            fontsize=8.2, color=TEXT)

    # poll
    ax.text(0.4, 5.2, "② poll：改用结构体数组，去掉 1024 上限，但仍要全量扫描",
            fontsize=9.4, fontweight="bold", color=TEXT)
    for i in range(N):
        x = 0.6 + i * 0.92
        active = i == 8
        c = GREEN if active else GREY
        ax.add_patch(Rectangle((x, 4.35), 0.8, 0.5, facecolor=c,
                               edgecolor=DARK, lw=0.9))
        ax.text(x + 0.4, 4.6, "fd" if active else "·", ha="center", va="center",
                fontsize=7.5, color=TEXT)
    ax.text(10.0, 4.6, "还是扫 1000 次", fontsize=8.4, color=RED, va="center",
            fontweight="bold")

    # epoll
    ax.text(0.4, 3.8, "③ epoll：fd 只在注册时拷一次，就绪的放进「就绪链表」",
            fontsize=9.4, fontweight="bold", color=TEXT)
    # 注册树
    box(ax, 0.6, 2.6, 3.2, 0.85, "红黑树（注册过）", "epoll_ctl 时插一次", PURPLE, fs=8.5, sfs=7.2)
    box(ax, 4.6, 2.6, 2.8, 0.85, "回调就绪 →", "放进链表", ORANGE, fs=8.5, sfs=7.2)
    box(ax, 8.2, 2.6, 3.0, 0.85, "就绪链表", "只返回这几个", GREEN, fs=8.5, sfs=7.2)
    arrow(ax, (3.85, 3.02), (4.55, 3.02), lw=1.3)
    arrow(ax, (7.45, 3.02), (8.15, 3.02), lw=1.3)
    ax.text(11.4, 3.02, "O(就绪数)", fontsize=8.6, color="#1e8449", va="center",
            fontweight="bold")

    # 对比
    ax.text(0.4, 2.05, "复杂度对比", fontsize=10, fontweight="bold", color=TEXT)
    rows = [
        ("select", "O(n) 每次全扫", "有 1024 上限", "跨平台好"),
        ("poll", "O(n) 每次全扫", "无上限", "略好于 select"),
        ("epoll", "O(就绪数)", "无上限", "Linux 专用"),
    ]
    for i, (k, a, b, c) in enumerate(rows):
        y = 1.6 - i * 0.36
        ax.text(0.6, y, k, fontsize=8.6, color=TEXT, fontweight="bold")
        ax.text(2.2, y, a, fontsize=8.4, color=RED if i < 2 else "#1e8449")
        ax.text(5.4, y, b, fontsize=8.4, color=TEXT)
        ax.text(8.2, y, c, fontsize=8.4, color=TEXT)

    ax.text(0.4, 0.15,
            "但注意：连接数少（几十个）时 select 完全够用，epoll 的优势要到上千连接才明显。",
            fontsize=8.2, color=LINE)

    _save(fig, "linux-epoll.svg")


def fork_cow():
    """fork 与写时复制"""
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "fork 与写时复制：为什么复制一个进程这么快",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # fork 前
    ax.text(0.4, 6.8, "① fork 之前：父进程独占内存", fontsize=9.6,
            fontweight="bold", color=TEXT)
    box(ax, 0.5, 5.6, 2.0, 0.85, "父进程", "pid=100", BLUE, fs=9, sfs=7.4)
    box(ax, 3.4, 5.6, 3.0, 0.85, "物理内存页", "数据 A", GREEN, fs=9, sfs=7.4)
    arrow(ax, (2.55, 6.02), (3.35, 6.02), lw=1.3)

    # fork 后
    ax.text(0.4, 5.05, "② fork 返回后：两个进程指向同一份物理页，只读共享",
            fontsize=9.6, fontweight="bold", color=TEXT)
    box(ax, 0.5, 4.05, 2.0, 0.75, "父进程", "pid=100", BLUE, fs=9, sfs=7.4)
    box(ax, 0.5, 3.05, 2.0, 0.75, "子进程", "pid=101", ORANGE, fs=9, sfs=7.4)
    box(ax, 3.4, 3.55, 3.0, 0.85, "同一份物理页", "引用计数=2", GREEN, fs=9, sfs=7.4)
    arrow(ax, (2.55, 4.42), (3.35, 4.1), lw=1.3)
    arrow(ax, (2.55, 3.42), (3.35, 3.85), lw=1.3)
    ax.text(3.45, 3.22, "只增加引用计数，没有复制任何数据", fontsize=7.8, color="#1e8449")

    # 写时复制
    ax.text(0.4, 2.55, "③ 子进程要写时：才真的复制那一页（写时复制 COW）",
            fontsize=9.6, fontweight="bold", color=TEXT)
    box(ax, 0.5, 1.55, 2.0, 0.7, "父进程", None, BLUE, fs=9)
    box(ax, 0.5, 0.75, 2.0, 0.7, "子进程", None, ORANGE, fs=9)
    box(ax, 3.4, 1.55, 2.6, 0.7, "物理页（原）", "数据 A", GREEN, fs=8.5, sfs=7.2)
    box(ax, 3.4, 0.75, 2.6, 0.7, "物理页（新）", "数据 A'", PINK, fs=8.5, sfs=7.2)
    arrow(ax, (2.55, 1.9), (3.35, 1.9), lw=1.2)
    arrow(ax, (2.55, 1.1), (3.35, 1.1), lw=1.2, color=PURPLE)

    # 右侧
    ax.text(7.4, 6.4, "所以 shell 跑命令是两步", fontsize=9.8,
            fontweight="bold", color=TEXT)
    pts = [
        "① fork()：复制出一个一模一样的",
        "   子进程（几乎零成本，因为有 COW）",
        "",
        "② execve()：把子进程的地址空间",
        "   整个换掉，装进新程序",
        "",
        "为什么不直接 fork 就完事：",
        "  fork 出来的是同一个程序，",
        "  必须 exec 才能变成 ls / grep。",
        "",
        "常见坑：",
        "• fork 后父子都从 fork 的下一行",
        "  继续执行 —— 忘记判断返回值会",
        "  让父子各跑一遍后续代码",
        "• 子进程退出必须 wait，否则变僵尸",
    ]
    for i, s in enumerate(pts):
        ax.text(7.4, 6.0 - i * 0.33, s, fontsize=8, color=TEXT)

    _save(fig, "linux-fork-cow.svg")


def cpp_ctor_dtor_order():
    """C++ 构造与析构顺序"""
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "构造与析构：顺序正好相反，像搭积木和拆积木",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 构造
    ax.text(0.4, 6.6, "派生类的构造顺序（自顶向下）", fontsize=9.8,
            fontweight="bold", color=TEXT)
    ctor = [
        ("① 基类构造函数", "Base()", GREEN),
        ("② 成员变量（按声明顺序）", "m_a_ 然后 m_b_", BLUE),
        ("③ 自己的构造函数体", "Derived() { ... }", ORANGE),
    ]
    for i, (label, sub, color) in enumerate(ctor):
        y = 5.9 - i * 0.72
        ax.add_patch(Rectangle((0.6, y - 0.28), 5.2, 0.56, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        ax.text(0.75, y, label, fontsize=8.8, color=TEXT, va="center",
                fontweight="bold")
        ax.text(3.5, y, sub, fontsize=8, color=TEXT, va="center")
        if i < 2:
            arrow(ax, (1.0, y - 0.28), (1.0, y - 0.42), lw=1.2)

    # 析构
    ax.text(0.4, 3.55, "析构顺序（自底向上，完全相反）", fontsize=9.8,
            fontweight="bold", color=TEXT)
    dtor = [
        ("① 自己的析构函数体", "~Derived() { ... }", ORANGE),
        ("② 成员变量（逆序）", "m_b_ 然后 m_a_", BLUE),
        ("③ 基类析构函数", "~Base()", GREEN),
    ]
    for i, (label, sub, color) in enumerate(dtor):
        y = 2.85 - i * 0.72
        ax.add_patch(Rectangle((0.6, y - 0.28), 5.2, 0.56, facecolor=color,
                               edgecolor=DARK, lw=1.0, alpha=0.75))
        ax.text(0.75, y, label, fontsize=8.8, color=TEXT, va="center",
                fontweight="bold")
        ax.text(3.5, y, sub, fontsize=8, color=TEXT, va="center")

    # 右侧要点
    ax.text(7.0, 6.3, "三条容易出错的地方", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "① 初始化列表的顺序由声明顺序决定，",
        "   不是你在列表里写的顺序。",
        "   写反了会先用到未初始化的成员。",
        "",
        "② 基类析构必须是 virtual。",
        "   否则 delete 基类指针时，",
        "   子类的析构根本不会被调用，",
        "   资源全部泄漏。",
        "",
        "③ 构造/析构期间虚函数不生效。",
        "   此时对象的派生部分还没建好",
        "   （或已拆掉），虚表指向基类。",
        "",
        "为什么析构要反过来：",
        "  后面的依赖前面的，所以最后建",
        "  的最先拆。",
    ]
    for i, s in enumerate(pts):
        ax.text(7.0, 5.9 - i * 0.31, s, fontsize=8, color=TEXT)

    ax.text(0.4, 0.55,
            "验证手段：在每层的构造/析构里打一行日志，跑一次就能看清顺序。",
            fontsize=8.4, color=LINE)
    ax.text(0.4, 0.2, "类比：先打地基再砌墙，拆的时候必须先拆墙再挖地基。",
            fontsize=8.4, color=LINE)

    _save(fig, "cpp-ctor-dtor-order.svg")


def linux_vm():
    """虚拟内存与页表映射"""
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "虚拟内存：两个进程的同一个地址，落在不同物理页",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 进程 A
    box(ax, 0.5, 5.6, 2.3, 0.8, "进程 A", "虚拟地址 0x400000", BLUE, fs=8.8, sfs=7.2)
    box(ax, 4.0, 5.6, 2.4, 0.8, "页表 A", "VPN → PFN", PURPLE, fs=8.8, sfs=7.2)
    box(ax, 8.0, 5.6, 2.6, 0.8, "物理页 0x7A00", "A 的数据", GREEN, fs=8.8, sfs=7.2)
    arrow(ax, (2.85, 6.0), (3.95, 6.0), lw=1.3)
    arrow(ax, (6.45, 6.0), (7.95, 6.0), lw=1.3)

    # 进程 B
    box(ax, 0.5, 4.3, 2.3, 0.8, "进程 B", "虚拟地址 0x400000", ORANGE, fs=8.8, sfs=7.2)
    box(ax, 4.0, 4.3, 2.4, 0.8, "页表 B", "VPN → PFN", PURPLE, fs=8.8, sfs=7.2)
    box(ax, 8.0, 4.3, 2.6, 0.8, "物理页 0x3C00", "B 的数据", PINK, fs=8.8, sfs=7.2)
    arrow(ax, (2.85, 4.7), (3.95, 4.7), lw=1.3)
    arrow(ax, (6.45, 4.7), (7.95, 4.7), lw=1.3)

    ax.text(0.5, 3.9, "同一个虚拟地址 0x400000，映射到完全不同的物理页 —— 这就是进程隔离的基础。",
            fontsize=8.6, color=RED, fontweight="bold")

    # 地址空间布局
    ax.text(0.5, 3.45, "每个进程的虚拟地址空间布局（示意，从高到低）",
            fontsize=9.6, fontweight="bold", color=TEXT)
    regions = [
        ("内核空间", "用户态访问会段错误", GREY),
        ("栈 stack", "局部变量，向下增长", ORANGE),
        ("（空闲区，mmap 和共享库在这）", "malloc 大块、动态库", "#eaf2f8"),
        ("堆 heap", "malloc 小块，向上增长", BLUE),
        (".bss / .data", "全局变量、静态变量", GREEN),
        (".text", "代码，只读可执行", PURPLE),
    ]
    for i, (name, sub, color) in enumerate(regions):
        y = 3.20 - i * 0.40
        ax.add_patch(Rectangle((0.6, y - 0.18), 5.6, 0.38, facecolor=color,
                               edgecolor=DARK, lw=0.9))
        ax.text(0.75, y, name, fontsize=8, color=TEXT, va="center",
                fontweight="bold")
        ax.text(3.6, y, sub, fontsize=7.6, color=TEXT, va="center")

    # 右侧
    ax.text(7.0, 3.05, "虚拟内存带来什么", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "• 隔离：一个进程崩了不影响别人",
        "  它只能碰到自己页表里的页",
        "",
        "• 可以超额分配（overcommit）",
        "  每个进程都以为自己有 4GB",
        "",
        "• 共享：同一个 .so 只加载一份，",
        "  多个进程的页表都指向它",
        "",
        "• 按需加载：程序启动时并不真的",
        "  把代码全读进内存，用到哪页缺页",
        "  中断才去读（所以首次运行会慢）",
        "",
        "代价：每次内存访问都要查页表。",
        "  靠 TLB 缓存翻译结果才不至于太慢。",
    ]
    for i, s in enumerate(pts):
        ax.text(7.0, 2.62 - i * 0.255, s, fontsize=7.8, color=TEXT)

    ax.text(0.4, 0.55, "查证：cat /proc/<pid>/maps 看地址空间；pmap <pid> 更易读；",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.18, "　　　cat /proc/<pid>/status | grep Vm 看实际用量。",
            fontsize=8.2, color=LINE)

    _save(fig, "linux-virtual-memory.svg")


if __name__ == "__main__":
    python_copy()
    esp32_ota_partition()
    epoll_vs_select()
    fork_cow()
    cpp_ctor_dtor_order()
    linux_vm()
    print("done")
