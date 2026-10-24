"""第十二批：A 批剩余（异常树 / 运算符重载 / 容器隔离）"""
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


def arrow(ax, p1, p2, color=LINE, lw=1.4, style="-|>", ms=13):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw))


def py_exception_tree():
    fig, ax = plt.subplots(figsize=(10.8, 7.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.8)
    ax.set_axis_off()
    ax.text(0.2, 8.4, "Python 异常继承树：except 能捕获谁",
            fontsize=12.5, fontweight="bold", color=TEXT)

    box(ax, 5.0, 7.3, 3.4, 0.7, "BaseException", "所有异常的根", GREY, fs=9.5, sfs=7.4)
    box(ax, 0.6, 5.9, 3.0, 0.7, "SystemExit", "sys.exit()", PURPLE, fs=9, sfs=7.2)
    box(ax, 4.2, 5.9, 3.0, 0.7, "KeyboardInterrupt", "Ctrl+C", PURPLE, fs=9, sfs=7.2)
    box(ax, 7.8, 5.9, 3.0, 0.7, "Exception", "业务代码的根", GREEN, fs=9, sfs=7.2)

    for x in (2.1, 5.7, 9.3):
        arrow(ax, (6.7, 7.25), (x, 6.62))

    leaves = [
        ("ValueError", 0.6, BLUE),
        ("TypeError", 3.5, BLUE),
        ("KeyError", 6.4, BLUE),
        ("OSError", 9.3, PINK),
    ]
    for name, x, color in leaves:
        box(ax, x, 4.5, 2.5, 0.62, name, None, color, fs=8.6)
        arrow(ax, (9.3, 5.85), (x + 1.25, 5.15))

    sub2 = [("FileNotFoundError", 9.0), ("PermissionError", 11.2)]
    for name, x in sub2:
        box(ax, x, 3.4, 2.1, 0.55, name, None, ORANGE, fs=7.6)
        arrow(ax, (x + 1.05, 4.45), (x + 1.05, 3.98))

    ax.text(0.4, 2.75, "三个必须记住的事实", fontsize=9.8, fontweight="bold", color=TEXT)
    pts = [
        "① except Exception 抓不到 SystemExit / KeyboardInterrupt",
        "② 裸 except 会连 Ctrl+C 都吞掉，等于让程序无法中断",
        "③ 自定义异常应该继承 Exception（而不是 BaseException）",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 2.35 - i * 0.36, s, fontsize=8.4, color=TEXT)

    ax.text(0.4, 1.15, "捕获顺序：越具体的越要先写", fontsize=9.4,
            fontweight="bold", color=RED)
    code = [
        "try:    ...",
        "except FileNotFoundError:   # 先写具体的",
        "    ...",
        "except OSError:             # 再写父类",
        "    ...",
    ]
    for i, s in enumerate(code):
        ax.text(0.6, 0.78 - i * 0.22, s, fontsize=7.8, color=TEXT)
    ax.text(5.6, 0.34, "反过来写的话，父类先捕获，具体分支永远不执行",
            fontsize=8, color=RED)

    _save(fig, "py-exception-tree.svg")



def cpp_operator_resolution():
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "运算符重载：编译器怎么选出该调哪个函数",
            fontsize=12.5, fontweight="bold", color=TEXT)

    steps = [
        ("① 收集候选", "所有名为 operator+ 的函数", ORANGE, "成员 + 非成员 + 内建"),
        ("② 模板推导", "为每个候选推出具体类型", PINK, "失败就剔除（SFINAE）"),
        ("③ 可行函数", "参数能转换过去的留下", PURPLE, "看隐式转换序列"),
        ("④ 最佳匹配", "转换代价最小的那个", GREEN, "多个都最佳则二义性"),
    ]
    for i, (name, desc, color, note) in enumerate(steps):
        y = 6.5 - i * 1.15
        ax.add_patch(Rectangle((0.6, y), 3.4, 0.72, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(2.3, y + 0.47, name, ha="center", va="center",
                fontsize=9.2, color=TEXT, fontweight="bold")
        ax.text(2.3, y + 0.2, desc, ha="center", va="center",
                fontsize=7.6, color=TEXT)
        ax.text(4.3, y + 0.36, "← " + note, fontsize=7.6, color=LINE, va="center")
        if i < len(steps) - 1:
            arrow(ax, (2.3, y), (2.3, y - 0.4))

    ax.text(8.4, 6.9, "一个真实的选择过程", fontsize=9.6, fontweight="bold", color=TEXT)
    ex = [
        "struct Vec {",
        "    Vec operator+(const Vec&);   // 候选 A（成员）",
        "};",
        "Vec operator+(const Vec&, const Vec&);   // 候选 B（非成员）",
        "",
        "Vec a, b;",
        "a + b;      // A 和 B 都可行，结果是二义性错误",
    ]
    for i, s in enumerate(ex):
        ax.text(8.4, 6.45 - i * 0.28, s, fontsize=7.2, color=TEXT)

    ax.text(8.4, 3.15, "四个容易踩的点", fontsize=9.6, fontweight="bold", color=TEXT)
    pts = [
        "• 不要同时提供成员和非成员版本（会二义性）",
        "• operator& 重载后取地址行为会变，慎用",
        "• == 和 != 要成对提供（C++20 可用 = default）",
        "• 流运算符 << 必须是非成员函数",
    ]
    for i, s in enumerate(pts):
        ax.text(8.4, 2.72 - i * 0.36, s, fontsize=7.6, color=TEXT)

    ax.text(0.4, 1.35, "为什么内建运算符也算候选", fontsize=9.2,
            fontweight="bold", color=TEXT)
    ax.text(0.4, 0.95,
            "int 的 + 是编译器内建的，不算函数。但重载解析时会一起参与比较，",
            fontsize=8, color=TEXT)
    ax.text(0.4, 0.62,
            "所以对指针、整数等类型重载运算符时，可能出现意外匹配。",
            fontsize=8, color=TEXT)
    ax.text(0.4, 0.18,
            "排查手段：用 -fsyntax-only 看完整报错，或用 concept 提前约束，把候选范围收紧。",
            fontsize=8, color=LINE)

    _save(fig, "cpp-operator-resolution.svg")



def container_isolation():
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "容器隔离的三层：namespace / cgroup / overlayfs",
            fontsize=12.5, fontweight="bold", color=TEXT)

    for i, (name, color) in enumerate([("容器 A", BLUE), ("容器 B", PINK),
                                       ("容器 C", ORANGE)]):
        x = 0.6 + i * 1.9
        ax.add_patch(Rectangle((x, 6.2), 1.7, 0.9, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(x + 0.85, 6.65, name, ha="center", va="center",
                fontsize=9, color=TEXT, fontweight="bold")

    layers = [
        ("NAMESPACE", "看得见什么", "PID / 网络 / 挂载 / 用户 …", GREEN, 4.5),
        ("CGROUP", "能用多少", "CPU / 内存 / IO / 进程数", PURPLE, 2.9),
        ("OVERLAYFS", "文件从哪来", "只读镜像层 + 可写容器层", GREY, 1.3),
    ]
    for name, what, detail, color, y in layers:
        ax.add_patch(Rectangle((0.6, y), 5.8, 1.2, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(0.9, y + 0.82, name, fontsize=9.2, color=TEXT, fontweight="bold")
        ax.text(0.9, y + 0.5, what, fontsize=8.6, color=TEXT)
        ax.text(0.9, y + 0.18, detail, fontsize=7.6, color=LINE)
        for i in range(3):
            x = 1.45 + i * 1.9
            arrow(ax, (x, 6.15), (x, y + 1.28), color=LINE, lw=1.0)

    ax.text(7.4, 6.7, "容器不是轻量虚拟机", fontsize=9.8, fontweight="bold", color=TEXT)
    rows = [
        ("", "虚拟机", "容器"),
        ("内核", "独立内核", "共享宿主内核"),
        ("启动", "几十秒", "毫秒级"),
        ("体积", "GB 级", "MB 级"),
        ("隔离强度", "硬件级", "进程级"),
    ]
    for i, (k, a, b) in enumerate(rows):
        y = 6.25 - i * 0.44
        bold = "bold" if i == 0 else "normal"
        ax.text(7.4, y, k, fontsize=8, color=TEXT, fontweight=bold)
        ax.text(9.2, y, a, fontsize=8, color=LINE if i else TEXT, fontweight=bold)
        ax.text(11.2, y, b, fontsize=8, color="#1e8449" if i else TEXT, fontweight=bold)

    ax.text(7.4, 3.4, "三个常见误解", fontsize=9.4, fontweight="bold", color=RED)
    pts = [
        "① 容器里 uname -r 看到的是宿主内核",
        "② 容器里不能加载内核模块（那是宿主的事）",
        "③ 容器里 PID 1 会忽略未注册的信号",
    ]
    for i, s in enumerate(pts):
        ax.text(7.4, 3.0 - i * 0.36, s, fontsize=7.8, color=TEXT)

    ax.text(0.4, 0.72, "验证手段", fontsize=8.6, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.38,
            "ls -l /proc/$$/ns/  看 namespace；cat /sys/fs/cgroup/cgroup.controllers 看 cgroup 版本",
            fontsize=7.6, color=TEXT)
    ax.text(0.4, 0.06,
            "mount | grep overlay  看 overlayfs；三方对照才能确认隔离真的生效。",
            fontsize=7.6, color=TEXT)

    _save(fig, "linux-container-isolation.svg")


if __name__ == "__main__":
    py_exception_tree()
    cpp_operator_resolution()
    container_isolation()
    print("done")
