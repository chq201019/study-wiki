"""第十三批：B 批（systemd / 分区表 / BLE / 看门狗 / FreeRTOS 同步 / 数据竞争）"""
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


# ---------------- systemd 依赖图 ----------------
def systemd_units():
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "systemd：After 管顺序，Requires 管依赖",
            fontsize=12.5, fontweight="bold", color=TEXT)

    box(ax, 0.6, 5.6, 3.2, 0.85, "network-online.target", "网络可用", GREY, fs=8.6, sfs=7.2)
    box(ax, 0.6, 4.2, 3.2, 0.85, "postgresql.service", "数据库", GREEN, fs=8.6, sfs=7.2)
    box(ax, 4.8, 4.9, 3.0, 0.85, "myapp.service", "你的服务", BLUE, fs=9, sfs=7.2)
    box(ax, 8.8, 4.9, 2.6, 0.85, "multi-user.target", "启动终点", ORANGE, fs=8.4, sfs=7.2)

    arrow(ax, (3.85, 6.0), (4.75, 5.45), color=RED, lw=1.6)
    ax.text(3.95, 6.12, "After + Wants", fontsize=7.4, color=RED)

    arrow(ax, (3.85, 4.6), (4.75, 5.1), color="#1e8449", lw=1.6)
    ax.text(2.55, 3.95, "After + Requires", fontsize=7.4, color="#1e8449")

    arrow(ax, (7.85, 5.3), (8.75, 5.3), color=LINE, lw=1.4)
    ax.text(7.95, 5.52, "WantedBy", fontsize=7.4, color=LINE)

    ax.text(0.4, 3.4, "四个指令的区别", fontsize=9.6, fontweight="bold", color=TEXT)
    rows = [
        ("After=X", "顺序：X 先启动，我再启动", "#1e8449"),
        ("Requires=X", "依赖：X 起不来我也不起；X 停我也停", RED),
        ("Wants=X", "弱依赖：X 起不来我照样起（推荐）", ORANGE),
        ("BindsTo=X", "强绑定：X 一停我立刻停", RED),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 3.0 - i * 0.42
        ax.text(0.6, y, k, fontsize=8.8, color=c, fontweight="bold")
        ax.text(2.8, y, v, fontsize=8.4, color=TEXT)

    ax.text(0.4, 1.15, "最容易犯的错：只写 Requires 不写 After",
            fontsize=9.4, fontweight="bold", color=RED)
    ax.text(0.4, 0.78,
            "两个服务会同时启动 —— 你的程序可能比数据库起得还快，于是连接失败。",
            fontsize=8.2, color=TEXT)
    ax.text(0.4, 0.42,
            "正确写法是两个都写；除真正「没有它就没法工作」的依赖外，其余一律用 Wants 而不是 Requires。",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.1,
            "另外：改完 unit 文件必须 daemon-reload，否则 systemd 用的还是旧配置且不报错。",
            fontsize=8.2, color=RED)

    _save(fig, "linux-systemd-dep.svg")


# ---------------- MBR vs GPT ----------------
def disk_partition_tables():
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.6)
    ax.set_axis_off()
    ax.text(0.2, 7.2, "MBR 与 GPT：分区表放在磁盘最前面",
            fontsize=12.5, fontweight="bold", color=TEXT)

    ax.text(0.4, 6.6, "MBR（老，上限 2 TiB）", fontsize=9.6, fontweight="bold", color=TEXT)
    segs = [("MBR 512B", 0.9, PURPLE), ("分区1", 2.4, BLUE), ("分区2", 2.0, GREEN),
            ("分区3", 2.0, ORANGE), ("分区4 或 扩展", 3.2, PINK)]
    x = 0.6
    for label, w, color in segs:
        ax.add_patch(Rectangle((x, 5.75), w, 0.62, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + w / 2, 6.06, label, ha="center", va="center",
                fontsize=7.8, color=TEXT)
        x += w
    ax.text(0.6, 5.42, "主分区最多 4 个；用「扩展分区 + 逻辑分区」才能更多",
            fontsize=7.8, color=LINE)
    ax.text(0.6, 5.05, "分区表用 32 位 LBA 记录扇区号 → 2 TiB 是硬上限",
            fontsize=7.8, color=RED)

    ax.text(0.4, 4.45, "GPT（新，UEFI 时代标准）", fontsize=9.6, fontweight="bold", color=TEXT)
    segs2 = [("保护MBR", 1.0, GREY), ("GPT 头", 1.1, PURPLE), ("分区表项 (128 项)", 3.4, BLUE),
             ("分区1", 2.0, GREEN), ("…", 1.2, GREY)]
    x = 0.6
    for label, w, color in segs2:
        ax.add_patch(Rectangle((x, 3.6), w, 0.62, facecolor=color,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + w / 2, 3.91, label, ha="center", va="center",
                fontsize=7.6, color=TEXT)
        x += w
    ax.text(0.6, 3.27, "64 位 LBA → 上限极大；有备份表 + CRC 校验；默认支持 128 个分区",
            fontsize=7.8, color="#1e8449")

    ax.text(0.4, 2.6, "对比", fontsize=9.6, fontweight="bold", color=TEXT)
    rows = [
        ("最大磁盘", "2 TiB", "极大"),
        ("分区数", "4 主（或 3 主 + 扩展）", "128"),
        ("启动方式", "BIOS", "UEFI"),
        ("冗余", "无备份", "备份表 + CRC"),
    ]
    for i, (k, a, b) in enumerate(rows):
        y = 2.2 - i * 0.36
        ax.text(0.6, y, k, fontsize=8, color=TEXT, fontweight="bold")
        ax.text(2.6, y, a, fontsize=8, color=RED)
        ax.text(6.4, y, b, fontsize=8, color="#1e8449")
    ax.text(2.6, 2.55, "MBR", fontsize=7.6, color=RED)
    ax.text(6.4, 2.55, "GPT", fontsize=7.6, color="#1e8449")

    ax.text(0.4, 0.55, "判断当前磁盘用哪种：parted -l 会直接写 Partition Table: gpt 或 msdos",
            fontsize=8.2, color=TEXT)
    ax.text(0.4, 0.2,
            "超过 2TB 的盘必须用 GPT，否则剩余空间无法使用；改分区表会清空磁盘。",
            fontsize=8.2, color=RED)

    _save(fig, "linux-partition-tables.svg")


if __name__ == "__main__":
    systemd_units()
    disk_partition_tables()
    print("done")


# ---------------- BLE GATT 四层 ----------------
def ble_gatt():
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "BLE 的 GATT：数据用四层结构组织",
            fontsize=12.5, fontweight="bold", color=TEXT)

    layers = [
        ("Profile", "规范（如心率、HID）", GREY, 6.4, 0.8),
        ("Service", "一组相关特征，带 UUID", PURPLE, 5.2, 0.8),
        ("Characteristic", "一个数据点，带 UUID 与权限", BLUE, 4.0, 0.8),
        ("Descriptor", "描述的元数据（单位/格式/CCCD）", GREEN, 2.8, 0.8),
    ]
    for name, desc, color, y, h in layers:
        ax.add_patch(Rectangle((0.8, y), 5.4, h, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(1.0, y + h * 0.66, name, fontsize=9.2, color=TEXT, fontweight="bold")
        ax.text(1.0, y + h * 0.25, desc, fontsize=7.6, color=TEXT)
        arrow(ax, (6.6, y + h / 2), (7.6, y + h / 2), color=LINE, lw=1.2)

    # 右侧具体例子
    ax.text(7.8, 7.1, "一个心率传感器的实际结构", fontsize=9.4, fontweight="bold", color=TEXT)
    tree = [
        "Profile: Heart Rate",
        " └─ Service 0x180D",
        "     ├─ Char 0x2A37 心率测量值",
        "     │   ├─ Desc: 数值格式",
        "     │   └─ Desc: CCCD (0x2902)",
        "     └─ Char 0x2A38 传感器位置",
    ]
    for i, s in enumerate(tree):
        ax.text(7.8, 6.6 - i * 0.3, s, fontsize=7.6, color=TEXT)

    # 三种操作
    ax.text(0.4, 2.1, "三种操作方式", fontsize=9.6, fontweight="bold", color=TEXT)
    ops = [
        ("Read", "客户端来问，需要连接", ORANGE),
        ("Write", "客户端写入，需要连接", BLUE),
        ("Notify", "服务端主动推，需客户端先订阅 CCCD", PINK),
    ]
    for i, (name, desc, color) in enumerate(ops):
        y = 1.7 - i * 0.42
        ax.add_patch(Rectangle((0.6, y - 0.14), 0.24, 0.28, facecolor=color,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.0, y, name, fontsize=8.6, color=TEXT, va="center", fontweight="bold")
        ax.text(2.4, y, desc, fontsize=8.2, color=TEXT, va="center")

    ax.text(7.8, 0.55,
            "传感器周期数据用 Notify 更省电；但客户端必须先写 CCCD 订阅，",
            fontsize=8, color=TEXT)
    ax.text(7.8, 0.22,
            "否则服务端推了也收不到 —— 这是 BLE 最常见的坑。",
            fontsize=8, color=RED)

    _save(fig, "esp32-ble-gatt.svg")


# ---------------- WWDG 窗口 ----------------
def wwdg_window():
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.4)
    ax.set_axis_off()
    ax.text(0.2, 7.0, "WWDG 窗口看门狗：喂早了也会复位",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 计数器递减轴（左边是计数值小=快到期，右边是0x7F刚开始）
    ax.annotate("", xy=(12.4, 5.0), xytext=(0.8, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.4))
    ax.text(12.5, 4.65, "时间", fontsize=8, color=LINE)

    zones = [
        (0.8, 2.0, PINK, "0x3F 复位"),
        (2.8, 5.6, GREEN, "允许喂的窗口"),
        (8.4, 4.0, RED, "太早喂 也复位"),
    ]
    for x, w, color, label in zones:
        ax.add_patch(Rectangle((x, 4.55), w, 0.9, facecolor=color,
                               edgecolor=DARK, lw=1.2, alpha=0.85))
        ax.text(x + w / 2, 3.92, label, ha="center", fontsize=8.2,
                color=TEXT, fontweight="bold")

    ticks = [("0x3F 复位", 2.0), ("0x40 下限", 2.85),
             ("0x50 窗口上限", 8.35), ("0x7F 起始", 12.3)]
    for label, x in ticks:
        ax.plot([x, x], [4.4, 5.6], color=DARK, lw=1.0, ls=":")
        ax.text(x, 5.72, label, ha="center", fontsize=7.2, color=TEXT)

    ax.text(0.8, 3.55, "← 计数递减方向", fontsize=7.6, color=LINE)
    # 说明
    ax.text(0.4, 3.1, "为什么要有窗口", fontsize=9.6, fontweight="bold", color=TEXT)
    pts = [
        "IWDG 只看「有没有喂」—— 程序跑飞但恰好跳到喂狗代码时，看不出异常。",
        "WWDG 还看「什么时候喂」—— 时序不对就复位，能抓住跑飞的情况。",
    ]
    for i, s in enumerate(pts):
        ax.text(0.4, 2.7 - i * 0.34, s, fontsize=8.4, color=TEXT)

    ax.text(0.4, 1.75, "配置要点", fontsize=9.4, fontweight="bold", color=TEXT)
    rows = [
        ("Window", "窗口上限，喂狗时计数器必须 ≤ 它"),
        ("Counter", "起始值 0x7F，递减到 0x40 以下就复位"),
        ("EWI", "早期唤醒中断，可在复位前抢救数据"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 1.35 - i * 0.36
        ax.text(0.6, y, k, fontsize=8.2, color=TEXT, fontweight="bold")
        ax.text(2.3, y, v, fontsize=8, color=TEXT)

    ax.text(0.4, 0.15,
            "口诀：早也不行，晚也不行，只有在窗口里喂才算数。",
            fontsize=8.2, color=RED)

    _save(fig, "stm32-wwdg-window.svg")


# ---------------- FreeRTOS 同步原语 ----------------
def freertos_sync():
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.2)
    ax.set_axis_off()
    ax.text(0.2, 7.8, "六种同步原语：按「解决什么问题」来选",
            fontsize=12.5, fontweight="bold", color=TEXT)

    rows = [
        ("队列 Queue", "传数据（值拷贝）", "生产者-消费者", BLUE),
        ("二值信号量", "通知「事件发生」", "中断唤醒任务", GREEN),
        ("计数信号量", "记录「有几个资源」", "资源池/事件计数", ORANGE),
        ("互斥锁 Mutex", "独占资源（有优先级继承）", "保护共享外设", RED),
        ("事件组", "等多个条件同时满足", "等网络+数据都就绪", PURPLE),
        ("任务通知", "点对点通知（最快、省内存）", "替代二值信号量", GREY),
    ]
    y0 = 6.8
    for i, (name, what, use, color) in enumerate(rows):
        y = y0 - i * 0.95
        ax.add_patch(Rectangle((0.6, y), 3.0, 0.74, facecolor=color,
                               edgecolor=DARK, lw=1.2))
        ax.text(2.1, y + 0.37, name, ha="center", va="center",
                fontsize=8.6, color=TEXT, fontweight="bold")
        ax.text(3.9, y + 0.5, what, fontsize=8, color=TEXT, va="center")
        ax.text(3.9, y + 0.2, "典型： " + use, fontsize=7.4, color=LINE, va="center")

    ax.text(0.4, 0.85, "选择顺序（从快到慢）", fontsize=9.6, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.5,
            "任务通知 > 二值信号量 > 队列 > 互斥锁 > 事件组",
            fontsize=8.6, color=TEXT)
    ax.text(0.4, 0.15,
            "任务通知比二值信号量快约 45%，且不占额外内核对象 —— 但只能点对点，不能广播。",
            fontsize=8, color=RED)

    _save(fig, "stm32-freertos-sync.svg")


# ---------------- 数据竞争时序 ----------------
def data_race():
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_axis_off()
    ax.text(0.2, 7.4, "数据竞争：counter++ 为什么会被覆盖",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 两条时间线
    ax.text(0.4, 6.85, "线程 A", fontsize=9.4, fontweight="bold", color=BLUE)
    ax.text(0.4, 5.55, "线程 B", fontsize=9.4, fontweight="bold", color=PINK)
    ax.plot([0.4, 12.8], [6.55, 6.55], color=LINE, lw=1.0)
    ax.plot([0.4, 12.8], [5.25, 5.25], color=LINE, lw=1.0)

    # A 的操作
    a_ops = [("读 counter=5", 1.2), ("加 1 → 6", 4.2), ("写回 6", 9.6)]
    for label, x in a_ops:
        ax.add_patch(Rectangle((x, 6.25), 2.3, 0.6, facecolor=BLUE,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 1.15, 6.55, label, ha="center", va="center",
                fontsize=7.8, color=TEXT)

    # B 的操作（插在中间）
    b_ops = [("读 counter=5", 2.2), ("加 1 → 6", 5.2), ("写回 6", 10.6)]
    for label, x in b_ops:
        ax.add_patch(Rectangle((x, 4.95), 2.3, 0.6, facecolor=PINK,
                               edgecolor=DARK, lw=1.0))
        ax.text(x + 1.15, 5.25, label, ha="center", va="center",
                fontsize=7.8, color=TEXT)

    # 结果
    ax.text(0.4, 4.3, "结果：最终 counter = 6，但期望是 7", fontsize=10,
            fontweight="bold", color=RED)
    ax.text(0.4, 3.9,
            "因为 B 读到的是 A 写回之前的旧值 —— 两次自增丢了一次。",
            fontsize=8.6, color=TEXT)

    # 三种解法
    ax.text(0.4, 3.3, "三种解法", fontsize=9.6, fontweight="bold", color=TEXT)
    rows = [
        ("互斥锁", "最通用，但开销大（几十~几百周期）", RED),
        ("原子操作", "单条 CPU 指令，只适合单变量", GREEN),
        ("批量提交", "局部累加后一次性加锁合并", ORANGE),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 2.9 - i * 0.44
        ax.add_patch(Rectangle((0.6, y - 0.13), 0.24, 0.26, facecolor=c,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.0, y, k, fontsize=8.6, color=TEXT, va="center", fontweight="bold")
        ax.text(2.6, y, v, fontsize=8.2, color=TEXT, va="center")

    ax.text(0.4, 0.75, "排查工具：gcc -fsanitize=thread -g 能让 ThreadSanitizer 直接指出",
            fontsize=8.2, color=TEXT)
    ax.text(0.4, 0.42,
            "哪两行代码发生了竞争，不用靠猜。",
            fontsize=8.2, color=TEXT)
    ax.text(0.4, 0.1,
            "注意：volatile 不能解决原子性问题 —— 它只保证每次都读内存，不保证读-改-写不被插入。",
            fontsize=8.2, color=RED)

    _save(fig, "c-data-race.svg")


if __name__ == "__main__":
    ble_gatt()
    wwdg_window()
    freertos_sync()
    data_race()
    print("done")
