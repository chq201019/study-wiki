"""第七批示意图：调度模型 / 对象关系 / 图表解读 / 状态机。

用法: python scripts/gen_diagrams7.py
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


def asyncio_loop():
    """事件循环调度：一个线程轮流推进多个协程"""
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "asyncio：单线程轮流推进多个协程", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 事件循环核心
    box(ax, 0.5, 5.6, 3.4, 1.1, "事件循环", "单线程，一个 while", PURPLE, fs=10, sfs=7.6)
    box(ax, 4.6, 6.15, 3.0, 0.75, "就绪队列", "可以立刻推进", GREEN, fs=9, sfs=7.2)
    box(ax, 4.6, 5.15, 3.0, 0.75, "等待队列", "等 IO / 等定时器", ORANGE, fs=9, sfs=7.2)
    arrow(ax, (3.95, 6.4), (4.55, 6.5))
    arrow(ax, (3.95, 5.9), (4.55, 5.55), color=LINE)

    # 协程
    coros = [("协程 A", BLUE), ("协程 B", PINK), ("协程 C", GREY)]
    for i, (name, c) in enumerate(coros):
        y = 6.85 - i * 0.85
        box(ax, 9.6, y, 3.2, 0.62, name, None, c, fs=9)
        arrow(ax, (7.65, 6.5), (9.55, y + 0.31), color=LINE, lw=1.2)
    ax.text(9.6, 4.75, "每个协程都保存着自己的栈帧与执行位置",
            fontsize=7.6, color=LINE)

    # 时间轴演示
    ax.text(0.5, 4.35, "一次 await 发生了什么（这就是全部秘密）",
            fontsize=9.8, fontweight="bold", color=TEXT)
    steps = [
        ("协程 A 执行到 await", GREY),
        ("A 让出控制权，把自己挂到等待队列", ORANGE),
        ("循环去就绪队列取下一个（比如 B）", GREEN),
        ("A 的 IO 完成 → 被移回就绪队列", BLUE),
        ("下次循环轮到 A，从暂停处继续", PINK),
    ]
    for i, (s, c) in enumerate(steps):
        y = 3.85 - i * 0.46
        ax.add_patch(Rectangle((0.6, y - 0.15), 0.26, 0.3, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.0, y, s, fontsize=8.6, color=TEXT, va="center")

    # 右侧要点
    ax.text(6.6, 3.85, "三个必须记住的点", fontsize=9.8, fontweight="bold", color=TEXT)
    pts = [
        "• 全程只有一个线程，没有线程切换",
        "• 并发的本质是「等的时候去干别的」",
        "• 任何一个阻塞调用都会卡住所有协程",
        "  （实测：混一个 time.sleep 让 0.2s 变 0.4s）",
        "",
        "所以：",
        "  适合 IO 密集，不适合 CPU 密集",
        "  （CPU 密集要靠多进程绕开 GIL）",
    ]
    for i, s in enumerate(pts):
        ax.text(6.6, 3.45 - i * 0.34, s, fontsize=8, color=TEXT)

    ax.text(0.5, 0.55,
            "协程切换的开销远小于线程切换：不需要进内核、不用保存寄存器组，只保存 Python 栈帧。",
            fontsize=8.2, color=LINE)
    ax.text(0.5, 0.2,
            "代价：一个协程写错（阻塞或吞掉 CancelledError）会影响整个事件循环里的所有协程。",
            fontsize=8.2, color=RED)

    _save(fig, "python-asyncio-loop.svg")


def git_objects():
    """Git 四种对象的关系"""
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "Git 对象：commit 指向 tree，tree 指向 blob",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # commit 链
    box(ax, 0.5, 5.9, 2.9, 0.95, "commit C2", "tree / parent", PINK, fs=9.5, sfs=7.4)
    box(ax, 0.5, 4.6, 2.9, 0.95, "commit C1", "tree / parent", PINK, fs=9.5, sfs=7.4)
    arrow(ax, (1.95, 5.85), (1.95, 5.6), color=LINE, lw=1.4)
    ax.text(2.1, 5.72, "parent", fontsize=7.4, color=LINE)

    # 根 tree
    box(ax, 4.3, 5.9, 2.7, 0.95, "tree（根目录）", "a.txt  b.txt  src/", GREEN, fs=9, sfs=7.2)
    arrow(ax, (3.45, 6.37), (4.25, 6.37))

    # 子 tree 与 blob（纵向排列，避免连线穿越方框）
    box(ax, 7.9, 6.55, 2.4, 0.75, "tree src/", "parser.c", GREEN, fs=8.5, sfs=7)
    box(ax, 10.9, 6.55, 2.4, 0.75, "blob parser.c", None, BLUE, fs=8.5)
    arrow(ax, (10.35, 6.92), (10.85, 6.92), color=LINE, lw=1.3)

    box(ax, 7.9, 5.6, 2.4, 0.62, "blob a.txt", None, BLUE, fs=8.5)
    box(ax, 7.9, 4.75, 2.4, 0.62, "blob b.txt", None, BLUE, fs=8.5)

    arrow(ax, (7.05, 6.75), (7.85, 6.9), color=LINE, lw=1.3)
    arrow(ax, (7.05, 6.35), (7.85, 5.91), color=LINE, lw=1.3)
    arrow(ax, (7.05, 6.15), (7.85, 5.06), color=LINE, lw=1.3)

    # 内容去重示意
    ax.text(0.5, 4.05, "内容寻址带来的自动去重（实测）", fontsize=9.8,
            fontweight="bold", color=RED)
    box(ax, 0.5, 2.65, 2.2, 0.8, "blob a.txt", "内容 hello", BLUE, fs=8.5, sfs=7)
    box(ax, 3.2, 2.65, 2.2, 0.8, "blob c.txt", "内容 hello", BLUE, fs=8.5, sfs=7)
    ax.text(5.6, 3.05, "→ 同一个 SHA，磁盘上只存一份", fontsize=8.4,
            color="#1e8449", va="center")
    ax.text(5.6, 2.72, "（实测：两个文件内容相同时 blob 总数不增加）",
            fontsize=7.6, color=LINE, va="center")

    # 要点
    ax.text(0.5, 2.05, "四个关键结论", fontsize=9.8, fontweight="bold", color=TEXT)
    pts = [
        "• blob 只存内容，不含文件名 —— 所以文件名改了不会产生新 blob",
        "• tree 存「名字 → blob」映射，所以文件名是有成本的",
        "• commit 存的是完整快照（一个 tree 的 SHA），不是 diff",
        "• 改一个字节就产生全新 blob，空间靠 packfile 的增量压缩省回来",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 1.62 - i * 0.34, s, fontsize=8.4, color=TEXT)

    ax.text(0.5, 0.2,
            "实测：一个只有两个文件的首次提交 = 1 tree + 2 blob + 1 commit，共 4 个对象。",
            fontsize=8.2, color=LINE)

    _save(fig, "git-objects.svg")
def flame_graph():
    """火焰图怎么读"""
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "火焰图怎么读：宽度是时间占比，不是时间轴",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 火焰图层级
    layers = [
        ("main  (100%)", 0.6, 12.4, GREEN),
        ("process_request  (85%)", 0.6, 10.5, ORANGE),
        ("parse_json  (60%)", 0.6, 6.3, PINK),
        ("query_db  (20%)", 7.2, 3.9, PURPLE),
        ("dict_lookup  (45%)", 0.6, 4.7, BLUE),
        ("memcpy  (12%)", 5.5, 1.75, GREY),
    ]
    y = 6.6
    for i, (name, x, w, c) in enumerate(layers):
        yy = 6.4 - i * 0.78
        ax.add_patch(Rectangle((x, yy), w, 0.62, facecolor=c,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 0.12, yy + 0.31, name, fontsize=8.2, color=TEXT, va="center")

    ax.annotate("", xy=(0.45, 6.1), xytext=(0.45, 2.75),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.3))
    ax.text(0.15, 4.4, "调用栈越往上越深", fontsize=8, color=LINE, rotation=90,
            va="center")

    ax.annotate("", xy=(13.1, 7.35), xytext=(0.6, 7.35),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.2))
    ax.text(6.5, 7.05, "宽度 = 占用的 CPU 时间比例", fontsize=8.6,
            color=RED, ha="center")

    # 右侧说明
    ax.text(0.5, 1.95, "三个读法", fontsize=10, fontweight="bold", color=TEXT)
    pts = [
        "① 找「塔顶的宽块」—— 那里才是真正在干活的地方",
        "   （不是最底层，底层通常只是调用者）",
        "② 平坦的一大片 = 采样分散在很多小函数里，没有单一瓶颈",
        "③ 锯齿状的顶 = 正常；突然一段极宽的 = 就是它了",
        "",
        "重要：火焰图是聚合视图，看不到「什么时候发生的」",
        "  要查抖动/尖峰，得分时间段采样，或者看时间序列指标",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 1.55 - i * 0.305, s, fontsize=8.4, color=TEXT)

    ax.text(0.5, -0.75,
            "生成：perf record -F 99 -g -p <pid> -- sleep 30  →  perf script  →  flamegraph.pl",
            fontsize=8.2, color=LINE)

    _save(fig, "linux-flamegraph.svg")


def tcp_states():
    """TCP 状态机（简化）"""
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.4)
    ax.set_axis_off()
    ax.text(0.2, 8.0, "TCP 状态：左边是主动关闭方，右边是被动关闭方",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 顶部主线
    box(ax, 0.6, 6.4, 2.4, 0.8, "CLOSED", None, GREY, fs=9.5)
    box(ax, 4.0, 6.4, 3.0, 0.8, "ESTABLISHED", None, GREEN, fs=9.5)
    box(ax, 8.4, 6.4, 2.4, 0.8, "CLOSED", None, GREY, fs=9.5)
    arrow(ax, (3.05, 6.8), (3.95, 6.8))
    ax.text(3.12, 7.0, "三次握手", fontsize=7.8, color=RED)
    arrow(ax, (7.05, 6.8), (8.35, 6.8))
    ax.text(7.15, 7.0, "四次挥手", fontsize=7.8, color=RED)

    # 段落标题（放在最左/最右，避开连线）
    ax.text(0.6, 5.98, "主动关闭方", fontsize=9.4, fontweight="bold", color=RED)
    ax.text(11.5, 5.98, "被动关闭方", fontsize=9.4, fontweight="bold", color="#1e8449")

    # 主动关闭链
    act = [("FIN_WAIT_1", 5.25, PINK), ("FIN_WAIT_2", 4.35, PINK),
           ("TIME_WAIT（等 2MSL）", 3.45, ORANGE)]
    for i, (name, y, c) in enumerate(act):
        box(ax, 0.6, y, 3.6, 0.62, name, None, c, fs=8.6)
        if i > 0:
            arrow(ax, (1.2, y + 0.95), (1.2, y + 0.65), color=LINE, lw=1.2)

    # 被动关闭链
    pas = [("CLOSE_WAIT", 5.25, PURPLE), ("LAST_ACK", 4.35, PURPLE)]
    for i, (name, y, c) in enumerate(pas):
        box(ax, 9.3, y, 3.6, 0.62, name, None, c, fs=8.6)
        if i > 0:
            arrow(ax, (11.1, y + 0.95), (11.1, y + 0.65), color=LINE, lw=1.2)

    # 从 ESTABLISHED 分叉下去
    arrow(ax, (4.6, 6.35), (2.4, 5.9), color=RED, lw=1.4)
    arrow(ax, (6.4, 6.35), (11.0, 5.9), color="#1e8449", lw=1.4)

    # 关键提示
    ax.text(0.6, 2.95, "两个必须分清的状态", fontsize=10, fontweight="bold", color=TEXT)
    box(ax, 0.6, 1.85, 5.8, 0.85, "CLOSE_WAIT 堆积 = 应用忘了 close()", None, PINK, fs=9)
    ax.text(0.75, 1.55, "对端已关，我也回了 ACK，但我的代码还没关 → TCP 不会自己关。",
            fontsize=7.9, color=TEXT)
    ax.text(0.75, 1.25, "这是纯应用层的 bug，调内核参数一点用都没有。",
            fontsize=7.9, color=RED, fontweight="bold")

    box(ax, 7.0, 1.85, 6.0, 0.85, "TIME_WAIT 是正常的，别急着改内核", None, ORANGE, fs=9)
    ax.text(7.15, 1.55, "存在的两个理由：① 保证最后一个 ACK 能重发",
            fontsize=7.9, color=TEXT)
    ax.text(7.15, 1.25, "② 让旧连接的残留报文在网络中消亡，不串到新连接。",
            fontsize=7.9, color=TEXT)

    ax.text(0.6, 0.6,
            "排查：ss -tan | awk 'NR>1{print $1}' | sort | uniq -c | sort -rn",
            fontsize=8.4, color=LINE)
    ax.text(0.6, 0.25,
            "真正的解法是减少短连接（连接池 / 长连接），而不是调 tcp_fin_timeout。",
            fontsize=8.4, color=LINE)

    _save(fig, "net-tcp-states.svg")
if __name__ == "__main__":
    asyncio_loop()
    git_objects()
    flame_graph()
    tcp_states()
    print("done")
