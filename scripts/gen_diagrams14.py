"""第十五批：D 批（迭代器协议 / 模板实例化 / 安全边界 / 睡眠电流 / 死区 / 管道流）"""
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


# ---------- Python 迭代器协议 ----------
def iterator_protocol():
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "可迭代对象 vs 迭代器：一个能反复遍历，一个只能一次",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 可迭代对象
    box(ax, 0.6, 5.9, 3.0, 0.9, "可迭代对象", "[1, 2, 3]", BLUE, fs=9, sfs=7.4)
    ax.text(0.6, 5.55, "有 __iter__，没有 __next__", fontsize=7.6, color=TEXT)
    ax.text(0.6, 5.22, "每次 iter() 都产生新迭代器", fontsize=7.6, color="#1e8449")

    # 两个迭代器
    box(ax, 4.6, 6.3, 2.6, 0.75, "迭代器 1", "遍历完就废", PINK, fs=8.6, sfs=7.2)
    box(ax, 4.6, 5.2, 2.6, 0.75, "迭代器 2", "又一个新的", PINK, fs=8.6, sfs=7.2)
    arrow(ax, (3.65, 6.45), (4.55, 6.67))
    arrow(ax, (3.65, 6.05), (4.55, 5.57))

    ax.text(4.6, 4.75, "有 __iter__ 和 __next__", fontsize=7.6, color=TEXT)

    # next() 调用
    ax.text(8.0, 6.7, "next(it) 的返回序列", fontsize=9.2, fontweight="bold", color=TEXT)
    seq = [("next → 1", GREEN), ("next → 2", GREEN), ("next → 3", GREEN),
           ("next → StopIteration", RED)]
    for i, (s, c) in enumerate(seq):
        y = 6.3 - i * 0.44
        ax.add_patch(Rectangle((8.0, y - 0.16), 3.4, 0.34, facecolor=c,
                               edgecolor=DARK, lw=0.9, alpha=0.6))
        ax.text(8.15, y, s, fontsize=7.8, color=TEXT, va="center")

    # 关键陷阱
    ax.text(0.4, 4.2, "最容易踩的坑：迭代器被消耗后第二次遍历是空的",
            fontsize=9.4, fontweight="bold", color=RED)
    code = [
        "nums = (x for x in range(5))    # 生成器表达式 = 迭代器",
        "sum(nums)      # 10",
        "sum(nums)      # 0   ← 已经耗尽了",
    ]
    for i, s in enumerate(code):
        ax.text(0.6, 3.8 - i * 0.3, s, fontsize=8, color=TEXT)

    ax.text(0.4, 2.6, "什么时候该用生成器", fontsize=9.4, fontweight="bold", color=TEXT)
    rows = [
        ("数据只用一次", "用生成器（省内存）", GREEN),
        ("数据要用多次", "先 list() 存下来（但这又占内存）", ORANGE),
        ("读超大文件", "文件对象本身就是迭代器，逐行读", BLUE),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 2.2 - i * 0.4
        ax.add_patch(Rectangle((0.6, y - 0.13), 0.22, 0.26, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(0.95, y, k, fontsize=8.2, color=TEXT, va="center", fontweight="bold")
        ax.text(3.0, y, v, fontsize=8, color=TEXT, va="center")

    ax.text(0.4, 0.55,
            "判断方法：问自己「这份数据会被用几次」。最容易出的 bug 是以为一次、实际用了两次。",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.2,
            "另外：迭代器没有 len()，也不能切片 —— 它们是「流」，不是「容器」。",
            fontsize=8.2, color=TEXT)

    _save(fig, "py-iterator-protocol.svg")


# ---------- C++ 模板实例化 ----------
def template_instantiation():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "模板不是代码：它是一张「生成代码的图纸」",
            fontsize=12.5, fontweight="bold", color=TEXT)

    box(ax, 0.6, 5.9, 3.6, 0.9, "template <typename T>", "T max(T a, T b) {…}", PURPLE, fs=8.6, sfs=7.2)
    ax.text(0.6, 5.55, "这里没有生成任何机器码", fontsize=7.6, color=RED)

    # 三个实例化
    insts = [
        ("max<int>", "int max(int, int)", BLUE, 5.2),
        ("max<double>", "double max(double, double)", GREEN, 3.9),
        ("max<char>", "char max(char, char)", ORANGE, 2.6),
    ]
    for name, code, color, y in insts:
        box(ax, 5.4, y, 2.4, 0.7, name, None, color, fs=8.4)
        arrow(ax, (4.35, 6.35), (5.35, y + 0.35), color=LINE, lw=1.2)
        ax.text(8.1, y + 0.35, "→ " + code, fontsize=7.8, color=TEXT, va="center")

    ax.text(5.4, 2.1, "每个实例都是独立的机器码", fontsize=8.4, color=RED)

    # 说明
    ax.text(0.4, 1.6, "三个直接后果", fontsize=9.6, fontweight="bold", color=TEXT)
    pts = [
        "① 模板定义必须放头文件 —— 编译器要在使用处看到完整定义才能实例化",
        "② 实例化越多，二进制越大 —— 每种类型一份机器码",
        "③ 报错发生在实例化时，不是定义时 —— 所以「定义了但没用的模板不会报错」",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 1.2 - i * 0.36, s, fontsize=8.2, color=TEXT)

    ax.text(0.4, 0.15,
            "想控制体积：显式实例化（template class Foo<int>;）只编需要的类型，或改用虚函数。",
            fontsize=8, color=LINE)

    _save(fig, "cpp-template-instantiation.svg")


# ---------- Linux 信任边界 ----------
def security_boundary():
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "安全加固：把攻击面一层层收窄",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 公网 -> 防火墙 -> SSH -> 服务 -> 数据
    layers = [
        ("公网", "任何人", GREY, 0.5, "最外层"),
        ("防火墙", "只放 22/80/443", ORANGE, 3.0, "默认拒绝"),
        ("SSH", "只密钥、禁 root", PINK, 5.5, "第一道门"),
        ("服务", "专用用户 + 沙箱", BLUE, 8.0, "最小权限"),
        ("数据", "只本机可连", GREEN, 10.5, "最后防线"),
    ]
    for name, desc, color, x, tag in layers:
        ax.add_patch(Rectangle((x, 5.2), 2.3, 1.2, facecolor=color,
                               edgecolor=DARK, lw=1.3))
        ax.text(x + 1.15, 6.0, name, ha="center", va="center",
                fontsize=9.2, color=TEXT, fontweight="bold")
        ax.text(x + 1.15, 5.6, desc, ha="center", va="center",
                fontsize=7.2, color=TEXT)
        ax.text(x + 1.15, 4.9, tag, ha="center", fontsize=7, color=LINE)
        if x < 10.5:
            arrow(ax, (x + 2.35, 5.8), (x + 2.95, 5.8), color=RED, lw=1.6)

    # 六个常见错误
    ax.text(0.4, 4.2, "六个最常见的错误（按被攻破概率排序）", fontsize=9.6,
            fontweight="bold", color=RED)
    errs = [
        ("① SSH 允许密码登录", "暴力破解的第一目标", RED),
        ("② 数据库监听 0.0.0.0", "全世界都能连", RED),
        ("③ Redis 无密码且暴露公网", "最经典的入侵入口", RED),
        ("④ 用 root 跑 Web 应用", "一旦 RCE 直接是 root", ORANGE),
        ("⑤ 密钥写死在代码里", "提交 git 就永久泄露", ORANGE),
        ("⑥ 不备份", "被加密/误删就彻底没了", ORANGE),
    ]
    for i, (k, v, c) in enumerate(errs):
        col = i // 3
        row = i % 3
        x = 0.5 + col * 6.3
        y = 3.7 - row * 0.52
        ax.text(x, y, k, fontsize=8.2, color=c, fontweight="bold")
        ax.text(x, y - 0.24, v, fontsize=7.4, color=TEXT)

    ax.text(0.4, 1.55, "三个反直觉的结论", fontsize=9.4, fontweight="bold", color=TEXT)
    pts = [
        "• 改 SSH 配置前必须先在另一个终端验证密钥能登录 —— 否则会把自己锁在外面",
        "• 被入侵后「重装」比「清理」更可靠 —— rootkit 可以藏在任何地方",
        "• 泄露后第一步是轮换密钥，不是清理 git 历史 —— 别人可能早就 clone 了",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 1.15 - i * 0.34, s, fontsize=8.2, color=TEXT)

    ax.text(0.4, 0.1,
            "顺序很重要：先放行 SSH 再开防火墙；先 sshd -t 检查语法再 reload。",
            fontsize=8, color=LINE)

    _save(fig, "linux-security-boundary.svg")


# ---------- ESP32 深度睡眠电流 ----------
def esp32_sleep_current():
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "ESP32 深度睡眠：一次唤醒周期的电流曲线",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 坐标轴
    ax.annotate("", xy=(12.6, 3.4), xytext=(0.8, 3.4),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.3))
    ax.annotate("", xy=(0.8, 6.5), xytext=(0.8, 3.4),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.3))
    ax.text(0.5, 6.2, "电流", fontsize=8, color=LINE)
    ax.text(12.3, 3.1, "时间", fontsize=8, color=LINE)

    # 波形：唤醒峰值 -> 工作 -> 睡眠长平台
    pts = [(0.9, 3.4), (1.2, 6.1), (2.0, 5.6), (2.6, 4.4),
           (3.4, 4.2), (4.0, 3.55), (12.4, 3.5)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=RED, lw=2.0)

    # 标注
    ax.annotate("唤醒峰值 约 40mA", xy=(1.3, 6.0), xytext=(1.5, 6.5),
                fontsize=7.6, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.9))
    ax.annotate("工作时间 几百 ms", xy=(2.8, 4.5), xytext=(3.0, 5.3),
                fontsize=7.6, color=TEXT,
                arrowprops=dict(arrowstyle="-", color=TEXT, lw=0.9))
    ax.annotate("深度睡眠 10~150µA", xy=(8.0, 3.55), xytext=(8.0, 4.3),
                fontsize=7.6, color="#1e8449",
                arrowprops=dict(arrowstyle="-", color="#1e8449", lw=0.9))

    # 三段说明
    ax.text(0.4, 2.6, "平均电流要按面积算，不是峰谷平均", fontsize=9.4,
            fontweight="bold", color=RED)
    ax.text(0.9, 2.2, "每小时醒一次，醒时 100mA 持续 1 秒，其余 20µA：",
            fontsize=8)
    ax.text(0.9, 1.85, "正确 (100×1 + 0.02×3599) / 3600 = 0.048 mA",
            fontsize=8, color="#1e8449")
    ax.text(0.9, 1.52, "错误 (100 + 0.02) / 2 = 50 mA　← 差 1000 倍",
            fontsize=8, color=RED)

    ax.text(0.4, 0.95, "测不准的三个原因", fontsize=9.2, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.6,
            "① 万用表内阻大、采样率低　② 开发板的 LED 与串口芯片吃掉 1~5mA　③ 探头接地夹引入电感",
            fontsize=7.8, color=TEXT)
    ax.text(0.4, 0.22,
            "正确做法：串一个 10Ω 采样电阻，用示波器测压降；或用 PPK2/Joulescope 这类功耗分析仪。",
            fontsize=7.8, color=LINE)

    _save(fig, "esp32-sleep-current.svg")


# ---------- STM32 互补 PWM 与死区 ----------
def stm32_deadtime():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "互补 PWM 与死区：为什么必须有「都为低」的间隙",
            fontsize=12.5, fontweight="bold", color=TEXT)

    def wave(y, xr, label, color):
        """在 y 高度画一段方波：xr 是 (低起, 高起, 高止, 低止)"""
        l0, h0, h1, l1 = xr
        ax.text(0.4, y + 0.18, label, fontsize=7.8, color=TEXT)
        ax.plot([l0, h0], [y, y], color=color, lw=2.4)
        ax.plot([h0, h0], [y, y + 0.42], color=color, lw=2.4)
        ax.plot([h0, h1], [y + 0.42, y + 0.42], color=color, lw=2.4)
        ax.plot([h1, h1], [y + 0.42, y], color=color, lw=2.4)
        ax.plot([h1, l1], [y, y], color=color, lw=2.4)

    ax.text(0.4, 6.85, "没有死区时", fontsize=9.4, fontweight="bold", color=RED)
    wave(6.0, (2.6, 3.6, 4.8, 5.8), "上管 CH1", BLUE)
    wave(5.1, (2.6, 3.6, 4.8, 5.8), "下管 CH1N", PINK)
    ax.add_patch(Rectangle((3.6, 4.95), 0.5, 1.6, facecolor=RED, alpha=0.30, lw=0))
    ax.text(4.2, 5.55, "重叠区：两管同时导通，短路", fontsize=7.4, color=RED)
    ax.text(0.4, 4.62, "关断比开通慢，所以切换瞬间两个管子都短暂处于导通状态",
            fontsize=7.8, color=TEXT)

    ax.text(0.4, 4.15, "加了死区之后", fontsize=9.4, fontweight="bold", color="#1e8449")
    wave(3.4, (2.6, 3.5, 4.6, 5.8), "上管 CH1", BLUE)
    wave(2.5, (2.6, 3.9, 4.9, 5.8), "下管 CH1N", PINK)
    ax.add_patch(Rectangle((3.5, 2.35), 0.4, 1.6, facecolor=GREEN, alpha=0.45, lw=0))
    ax.text(4.0, 3.05, "死区：两管都为低，安全", fontsize=7.4, color="#1e8449")

    ax.text(7.0, 4.15, "配置要点", fontsize=9.4, fontweight="bold", color=TEXT)
    rows = [
        ("只有 TIM1/TIM8", "F103 上仅高级定时器支持互补输出与死区"),
        ("DeadTime", "CubeMX 里填纳秒，它算 DTG 编码"),
        ("AutomaticOutput", "不开则互补输出完全没波形，也不报错"),
        ("BreakInput", "刹车输入，硬件级急停，纳秒级响应"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 3.72 - i * 0.56
        ax.text(7.0, y, k, fontsize=8, color=TEXT, fontweight="bold")
        ax.text(7.0, y - 0.22, v, fontsize=7.3, color=LINE)

    ax.text(0.4, 1.65, "死区时间怎么算", fontsize=9.2, fontweight="bold", color=TEXT)
    ax.text(0.4, 1.3,
            "DTG[7:0] 不是直接的时间值而是分段编码；CubeMX 里填 ns 会自动换算。",
            fontsize=7.8, color=TEXT)
    ax.text(0.4, 0.92,
            "典型：MOS 管开关延迟 100~500ns，死区取 1~2 倍即 200ns~1us，要与驱动电路匹配。",
            fontsize=7.8, color=TEXT)
    ax.text(0.4, 0.45,
            "死区太大则波形失真效率下降；太小则直通烧管。查 MOS 手册的 td(off) 与 td(on)。",
            fontsize=7.8, color=RED)

    _save(fig, "stm32-deadtime.svg")


def shell_pipeline():
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "管道：三个进程用两个内核缓冲区串起来",
            fontsize=12.5, fontweight="bold", color=TEXT)

    procs = [("grep ERROR", "进程 1", BLUE, 0.5),
             ("sort -u", "进程 2", GREEN, 4.4),
             ("head -5", "进程 3", ORANGE, 8.3)]
    for cmd, tag, color, x in procs:
        ax.add_patch(Rectangle((x, 5.5), 2.5, 0.85, facecolor=color,
                               edgecolor=DARK, lw=1.3))
        ax.text(x + 1.25, 5.95, cmd, ha="center", va="center",
                fontsize=8.6, color=TEXT, fontweight="bold")
        ax.text(x + 1.25, 5.3, tag, ha="center", fontsize=7.2, color=LINE)

    box(ax, 3.15, 5.6, 1.05, 0.65, "pipe", None, PURPLE, fs=7.4)
    box(ax, 7.05, 5.6, 1.05, 0.65, "pipe", None, PURPLE, fs=7.4)
    arrow(ax, (3.02, 5.92), (3.13, 5.92), color=RED, lw=1.4)
    arrow(ax, (4.22, 5.92), (4.33, 5.92), color=RED, lw=1.4)
    arrow(ax, (6.92, 5.92), (7.03, 5.92), color=RED, lw=1.4)
    arrow(ax, (8.12, 5.92), (8.23, 5.92), color=RED, lw=1.4)

    ax.text(0.5, 4.85, "内核缓冲区默认 64KB，满了写者阻塞、空了读者阻塞",
            fontsize=7.8, color=LINE)

    ax.text(0.4, 4.25, "三个实用结论", fontsize=9.6, fontweight="bold", color=TEXT)
    pts = [
        "① 每一环都可能影响退出码：默认只看最后一条，加 set -o pipefail 才看全部",
        "② 每一环都有缓冲：grep 检测到 stdout 是管道就变全缓冲，日志不实时",
        "③ 每一环是独立进程：cd 与变量赋值在管道里不生效（子 shell）",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 3.85 - i * 0.42, s, fontsize=8.2, color=TEXT)

    ax.text(0.4, 2.35, "两个最容易踩的坑", fontsize=9.2, fontweight="bold", color=RED)
    ax.text(0.4, 2.0,
            "pipefail 前：false | true 的退出码是 0（最后一条的），你察觉不到前面的失败。",
            fontsize=7.8, color=TEXT)
    ax.text(0.4, 1.62,
            "变量不传递：count=0; cat f | while read l; do count=$((count+1)); done; echo $count 得 0",
            fontsize=7.8, color=RED)
    ax.text(0.4, 1.2,
            "解法：改成重定向  while read l; do ... done < f  就不在子 shell 里了。",
            fontsize=7.8, color="#1e8449")

    ax.text(0.4, 0.45, "排查手段：strace -f -e trace=pipe,read,write 能看到每个进程怎么读写管道。",
            fontsize=7.8, color=LINE)

    _save(fig, "linux-shell-pipeline.svg")

if __name__ == "__main__":
    iterator_protocol()
    template_instantiation()
    security_boundary()
    esp32_sleep_current()
    stm32_deadtime()
    shell_pipeline()
    print("done")
