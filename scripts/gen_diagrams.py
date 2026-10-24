"""
生成技术示意图（SVG）。所有图的数字都必须与对应文档正文的实测输出一致。

用法: python scripts/gen_diagrams.py
输出: static/img/diagrams/*.svg
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import font_manager, rcParams

OUT = os.path.join("static", "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

# 中文字体：按可用性依次回落
for _f in ["Microsoft YaHei", "Noto Sans SC", "SimHei", "Source Han Sans SC"]:
    if any(x.name == _f for x in font_manager.fontManager.ttflist):
        rcParams["font.sans-serif"] = [_f]
        break
rcParams["axes.unicode_minus"] = False

# 配色（深浅两套主题下都可读：中等饱和 + 深色文字）
C_DATA = "#7fb3d5"   # 真正占用数据
C_PAD = "#e8b4b8"    # padding
C_ALIGN = "#f5cba7"  # 对齐浪费/其他
C_TEXT = "#1b2631"
C_GRID = "#5d6d7e"


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", path)


def _cell(ax, x, y, w, h, label, sub=None, color=C_DATA, fs=11, sfs=8):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="#2c3e50",
                           linewidth=1.2, alpha=0.85))
    if sub:
        ax.text(x + w / 2, y + h * 0.62, label, ha="center", va="center",
                fontsize=fs, color=C_TEXT, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center",
                fontsize=sfs, color=C_TEXT)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=C_TEXT, fontweight="bold")


def struct_layouts():
    """结构体 padding 三对比 —— 数据取自 aggregate.mdx 实测输出"""
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.set_xlim(-0.6, 12.6)
    ax.set_ylim(-0.4, 6.4)
    ax.set_axis_off()

    gw = 1.0  # 一字节宽

    def row(y, title, size, cells, note):
        ax.text(-0.55, y + 0.92, title, fontsize=12, fontweight="bold",
                color=C_TEXT, ha="left", va="center")
        ax.text(size + 0.35, y + 0.92, note, fontsize=9.5, color=C_GRID,
                ha="left", va="center")
        for (start, width, label, sub, color) in cells:
            _cell(ax, start * gw, y, width * gw, 0.72, label, sub, color)
        # 字节刻度
        for b in range(0, size + 1):
            ax.plot([b * gw, b * gw], [y - 0.06, y], color=C_GRID, lw=0.8)
            ax.text(b * gw, y - 0.22, str(b), ha="center", va="center",
                    fontsize=7.5, color=C_GRID)
        ax.plot([0, size * gw], [y, y], color=C_GRID, lw=0.8)

    # Packed3: a@0, pad 1-3, b@4-7, c@8-9, pad 10-11, size=12
    row(5.0, "struct Packed3  (a, b, c)", 12, [
        (0, 1, "a", "u8", C_DATA),
        (1, 3, "padding", "对齐 b", C_PAD),
        (4, 4, "b", "u32", C_DATA),
        (8, 2, "c", "u16", C_DATA),
        (10, 2, "padding", "尾部", C_PAD),
    ], "size=12  align=4")

    # Reordered3: b@0-3, c@4-5, a@6, pad 7, size=8
    row(3.2, "struct Reordered3  (b, c, a)", 8, [
        (0, 4, "b", "u32", C_DATA),
        (4, 2, "c", "u16", C_DATA),
        (6, 1, "a", "u8", C_DATA),
        (7, 1, "pad", "尾部", C_PAD),
    ], "size=8  align=4  省 33%")

    # Packed1: a@0, b@1-4, c@5-6, size=7
    row(1.4, "struct Packed1  (#pragma pack(1))", 7, [
        (0, 1, "a", "u8", C_DATA),
        (1, 4, "b", "u32", C_DATA),
        (5, 2, "c", "u16", C_DATA),
    ], "size=7  align=1  对齐降级")

    ax.text(6.0, 0.35, "三种写法成员完全相同（最小 7 字节），大小却是 12 / 8 / 7",
            ha="center", va="center", fontsize=10, color=C_TEXT, style="italic")

    # 图例
    for i, (c, t) in enumerate([(C_DATA, "真实数据"), (C_PAD, "padding（浪费）")]):
        ax.add_patch(Rectangle((0.2 + i * 2.6, 6.05), 0.32, 0.24,
                               facecolor=c, edgecolor="#2c3e50", alpha=0.85))
        ax.text(0.65 + i * 2.6, 6.17, t, fontsize=9, va="center", color=C_TEXT)

    _save(fig, "struct-padding.svg")


def memory_regions():
    """C 程序内存四区 —— 与 memory.mdx 的描述一致（典型 Linux x86-64 布局）"""
    fig, ax = plt.subplots(figsize=(9.2, 7.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_axis_off()

    segs = [
        ("高地址 0x7fff…", "栈 Stack", "局部变量 / 参数 / 返回地址\n向低地址增长 ↓", "#aed6f1"),
        ("", "（未映射的地址空间）", "", "#f2f3f4"),
        ("", "堆 Heap  →  向高地址增长 ↑", "malloc / free 管理（brk / mmap）", "#a9dfbf"),
        ("", ".bss", "未初始化全局与 static\n不占文件，加载时清零", "#f9e79f"),
        ("", ".data", "已初始化全局与 static", "#f9e79f"),
        ("", ".rodata", "字符串字面量、const 全局", "#f5cba7"),
        ("", ".text", "机器指令（只读可执行）", "#d7bde2"),
        ("低地址 0x0040…", "（保留 / 未映射）", "", "#f2f3f4"),
    ]

    y = 11.0
    h = 1.35
    for tag, label, desc, c in segs:
        height = h if desc else 0.62
        ax.add_patch(Rectangle((1.5, y - height), 6.6, height,
                               facecolor=c, edgecolor="#2c3e50", linewidth=1.1))
        if desc:
            ax.text(4.8, y - 0.38, label, ha="center",
                    va="center", fontsize=11, fontweight="bold", color=C_TEXT)
            ax.text(4.8, y - 0.95, desc, ha="center", va="center",
                    fontsize=8.5, color=C_TEXT, linespacing=1.4)
        else:
            ax.text(4.8, y - height / 2, label, ha="center",
                    va="center", fontsize=11, fontweight="bold", color=C_TEXT)
        if tag:
            ax.text(1.3, y - height / 2, tag, ha="right", va="center",
                    fontsize=9, color=C_GRID)
        y -= height + 0.26

    # 增长箭头
    ax.annotate("", xy=(8.55, 9.55), xytext=(8.55, 10.55),
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.8))
    ax.text(8.7, 10.05, "栈增长方向", fontsize=8.5, color="#c0392b", va="center")
    ax.annotate("", xy=(8.55, 8.05), xytext=(8.55, 6.95),
                arrowprops=dict(arrowstyle="->", color="#1e8449", lw=1.8))
    ax.text(8.7, 7.5, "堆增长方向", fontsize=8.5, color="#1e8449", va="center")

    ax.text(4.8, 0.25, "典型 Linux x86-64 布局；C 标准只规定存储期，不规定区域",
            ha="center", fontsize=9, color=C_GRID, style="italic")

    _save(fig, "c-memory-layout.svg")


def vtable_layout():
    """C++ 多态对象内存布局 + vtable"""
    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.2)
    ax.set_axis_off()

    # 对象
    ax.text(2.0, 6.7, "栈上的对象", fontsize=11.5, fontweight="bold", color=C_TEXT,
            ha="center")
    ax.add_patch(Rectangle((0.6, 5.0), 3.0, 1.25, facecolor="#aed6f1",
                           edgecolor="#2c3e50", lw=1.3))
    ax.plot([0.6, 3.6], [5.62, 5.62], color="#2c3e50", lw=0.9)
    ax.text(2.1, 5.94, "vptr  (8 字节)", ha="center", va="center", fontsize=9.5,
            color=C_TEXT, fontweight="bold")
    ax.text(2.1, 5.31, "指向所属类的 vtable", ha="center", va="center", fontsize=8.5,
            color=C_TEXT)
    for i, m in enumerate(["成员变量 x", "成员变量 y"]):
        ax.add_patch(Rectangle((0.6, 4.0 - i * 0.62), 3.0, 0.62, facecolor="#d6eaf8",
                               edgecolor="#2c3e50", lw=1.1))
        ax.text(2.1, 4.31 - i * 0.62, m, ha="center", va="center", fontsize=9,
                color=C_TEXT)

    # vtable
    ax.text(8.6, 6.7, "只读数据段的 vtable", fontsize=11.5, fontweight="bold",
            color=C_TEXT, ha="center")
    ax.add_patch(Rectangle((6.2, 5.0), 4.8, 1.25, facecolor="#d7bde2",
                           edgecolor="#2c3e50", lw=1.3))
    ax.text(8.6, 5.62, "Derived 的 vtable", ha="center", va="center", fontsize=9.5,
            color=C_TEXT, fontweight="bold")
    rows = [("+0", "&Derived::f()"), ("+8", "&Derived::g()"), ("+16", "&Derived::~Derived()")]
    for i, (off, fn) in enumerate(rows):
        yy = 4.62 - i * 0.66
        ax.add_patch(Rectangle((6.2, yy), 1.0, 0.6, facecolor="#f5cba7",
                               edgecolor="#2c3e50", lw=1.0))
        ax.text(6.7, yy + 0.3, off, ha="center", va="center", fontsize=8.5,
                color=C_TEXT, fontweight="bold")
        ax.add_patch(Rectangle((7.2, yy), 3.8, 0.6, facecolor="#eaecee",
                               edgecolor="#2c3e50", lw=1.0))
        ax.text(9.1, yy + 0.3, fn, ha="center", va="center", fontsize=9, color=C_TEXT)

    # 指针
    ax.add_patch(FancyArrowPatch((3.7, 5.62), (6.1, 5.62),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color="#c0392b", lw=1.8))
    ax.text(4.9, 5.82, "vptr", ha="center", fontsize=8.5, color="#c0392b",
            fontweight="bold")

    # 调用路径
    ax.text(0.5, 2.35, "p->f()  的运行期路径：", fontsize=10.5, fontweight="bold",
            color=C_TEXT, ha="left")
    steps = [
        "① 取 p 指向对象首部的 vptr",
        "② 通过 vptr 找到 vtable",
        "③ 按 f() 在表中的固定偏移取函数地址",
        "④ 间接调用 → 落到 Derived::f()",
    ]
    for i, s in enumerate(steps):
        ax.text(0.9, 1.85 - i * 0.42, s, fontsize=9, color=C_TEXT, ha="left")

    ax.text(12.7, 1.0, "代价：一次间接跳转\n（无法内联）", fontsize=8.5,
            color="#c0392b", ha="right", va="center")

    _save(fig, "cpp-vtable.svg")


def pointer_array():
    """指针与数组的本质区别"""
    fig, ax = plt.subplots(figsize=(10.0, 5.4))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6.6)
    ax.set_axis_off()

    # 数组
    ax.text(2.4, 6.2, "int arr[4]", fontsize=11.5, fontweight="bold", color=C_TEXT,
            ha="center")
    ax.text(2.4, 5.85, "数组名 = 整块内存本身（sizeof = 16）", fontsize=8.5,
            color=C_GRID, ha="center")
    for i in range(4):
        ax.add_patch(Rectangle((0.5 + i * 1.0, 4.5), 1.0, 0.85, facecolor="#a9dfbf",
                               edgecolor="#2c3e50", lw=1.2))
        ax.text(1.0 + i * 1.0, 4.93, f"arr[{i}]", ha="center", va="center",
                fontsize=8.8, color=C_TEXT)

    # 指针
    ax.text(9.0, 6.2, "int *p = arr", fontsize=11.5, fontweight="bold", color=C_TEXT,
            ha="center")
    ax.text(9.0, 5.85, "指针 = 一个存地址的变量（sizeof = 8，64 位）", fontsize=8.5,
            color=C_GRID, ha="center")
    ax.add_patch(Rectangle((8.0, 4.5), 2.0, 0.85, facecolor="#f5cba7",
                           edgecolor="#2c3e50", lw=1.2))
    ax.text(9.0, 4.93, "0x7ffd…（地址）", ha="center", va="center", fontsize=8.8,
            color=C_TEXT, fontweight="bold")
    ax.add_patch(FancyArrowPatch((8.0, 4.92), (4.6, 4.92), arrowstyle="-|>",
                                 mutation_scale=15, color="#c0392b", lw=1.7))

    # 关键差异
    ax.text(0.5, 3.35, "四个必须分清的差异", fontsize=11, fontweight="bold",
            color=C_TEXT, ha="left")
    rows = [
        ("sizeof", "数组：整块大小 16", "指针：指针自身大小 8"),
        ("&arr[0] 与 &arr", "数组：&arr 是「整个数组的指针」，+1 跳 16 字节", "指针：+1 跳一个元素"),
        ("可否赋值", "数组名不是左值，arr = p 编译错误", "p = arr 合法"),
        ("函数传参", "退化为指针，sizeof 变成 8（最经典陷阱）", "本来就是指针"),
    ]
    ax.text(1.0, 2.85, "维度", fontsize=9, fontweight="bold", color=C_TEXT)
    ax.text(4.3, 2.85, "数组", fontsize=9, fontweight="bold", color=C_TEXT)
    ax.text(9.2, 2.85, "指针", fontsize=9, fontweight="bold", color=C_TEXT)
    for i, (a, b, c) in enumerate(rows):
        yy = 2.35 - i * 0.55
        ax.text(1.0, yy, a, fontsize=8.8, color=C_TEXT)
        ax.text(4.3, yy, b, fontsize=8.5, color=C_TEXT)
        ax.text(9.2, yy, c, fontsize=8.5, color=C_TEXT)

    _save(fig, "c-pointer-vs-array.svg")


def esp32_flash_partition():
    """ESP32-S3 Flash 双 OTA 分区布局 —— 偏移取自 partition-ota.mdx 的分区表"""
    fig, ax = plt.subplots(figsize=(11.4, 5.9))
    ax.set_xlim(-0.35, 10.9)
    ax.set_ylim(-0.6, 7.0)
    ax.set_axis_off()

    # (起始比例, 结束比例, 名称, 副标题, 颜色)
    parts = [
        (0.0, 0.055, "bootloader", "0x0", "#d5d8dc"),
        (0.055, 0.083, "分区表", "0x8000", "#d5d8dc"),
        (0.083, 0.104, "nvs", "0x9000", "#aed6f1"),
        (0.104, 0.120, "otadata", "0xf000", "#f5cba7"),
        (0.120, 0.517, "app0  (ota_0)", "0x10000\n0x1D0000 ≈1.78MB", "#a9dfbf"),
        (0.517, 0.914, "app1  (ota_1)", "0x1E0000\n0x1D0000 ≈1.78MB", "#abebc6"),
        (0.914, 0.984, "spiffs", "0x3B0000", "#f9e79f"),
        (0.984, 1.0, "coredump", "0x3F0000", "#e8daef"),
    ]

    x0, W = 0.35, 10.2
    y, h = 5.3, 1.5
    for (s, e, name, sub, color) in parts:
        w = (e - s) * W
        ax.add_patch(Rectangle((x0 + s * W, y), w, h, facecolor=color,
                               edgecolor="#2c3e50", lw=1.2))
        if w > 1.1:  # 宽分区直接标注
            ax.text(x0 + s * W + w / 2, y + h * 0.65, name, ha="center",
                    va="center", fontsize=8.8, fontweight="bold", color=C_TEXT)
            ax.text(x0 + s * W + w / 2, y + h * 0.24, sub, ha="center",
                    va="center", fontsize=6.8, color=C_TEXT, linespacing=1.3)

    ax.text(x0, y + h + 0.34, "ESP32-S3 Flash（16MB）双 OTA 布局",
            fontsize=12, fontweight="bold", color=C_TEXT)

    # 窄分区用引线向下标注。左侧四个分区挤在一起，统一排成两行：
    # 第 1 行 bootloader / nvs，第 2 行 分区表 / otadata（水平也拉开）
    left = [(0, "bootloader", "0x0"), (2, "nvs", "0x9000"),
            (1, "分区表", "0x8000"), (3, "otadata", "0xf000")]
    slots = {  # name -> (行, 水平中心偏移量)
        "bootloader": (0, 0.0), "nvs": (0, 1.35),
        "分区表": (1, 0.55), "otadata": (1, 2.15),
    }
    center = {name: x0 + (s + e) / 2 * W for (s, e, name, _sub, _c) in parts}
    for _idx, name, sub in left:
        cx_real = center[name]
        row, dx = slots[name]
        lx = cx_real + dx
        ly = y - 0.55 - row * 0.80
        ax.plot([cx_real, cx_real, lx], [y, ly + 0.46, ly + 0.46],
                color=C_GRID, lw=0.8, ls=":")
        ax.text(lx, ly + 0.24, name, ha="center", va="center", fontsize=7.8,
                fontweight="bold", color=C_TEXT)
        ax.text(lx, ly - 0.04, sub, ha="center", va="center", fontsize=6.8,
                color=C_TEXT)

    # 右侧 spiffs / coredump
    for name, sub, row in [("spiffs", "0x3B0000", 0), ("coredump", "0x3F0000", 1)]:
        cx_real = center[name]
        ly = y - 0.55 - row * 0.80
        ax.plot([cx_real, cx_real], [y, ly + 0.46], color=C_GRID, lw=0.8, ls=":")
        ax.text(cx_real, ly + 0.24, name, ha="center", va="center", fontsize=7.8,
                fontweight="bold", color=C_TEXT)
        ax.text(cx_real, ly - 0.04, sub, ha="center", va="center", fontsize=6.8,
                color=C_TEXT)

    # OTA 流程
    ax.text(x0, 3.35, "OTA 升级为什么必须有 app0 + app1", fontsize=11,
            fontweight="bold", color=C_TEXT)
    steps = [
        "① 当前从 ota_0 启动，正在运行旧固件",
        "② 新固件下载并写入 ota_1 —— ota_0 里的旧固件完好无损",
        "③ 校验通过后，只改 otadata 的几字节：下次从 ota_1 启动",
        "④ 重启进新固件；若是坏固件未通过自检，改回 otadata 即可回滚 ota_0",
    ]
    for i, s in enumerate(steps):
        ax.text(x0 + 0.15, 2.85 - i * 0.44, s, fontsize=9, color=C_TEXT)

    ax.text(x0, 0.55,
            "任一时刻 Flash 里都有一个可启动固件 —— 这是 OTA 可靠性的全部根基",
            fontsize=9, color="#7b241c", style="italic")
    ax.text(x0, 0.12,
            "单 factory 分区做不到：升级就是往自己脚下拆砖",
            fontsize=8.5, color=C_GRID)

    _save(fig, "esp32-flash-partition.svg")


def esp32_boot_chain():
    """ESP32-S3 上电启动链"""
    fig, ax = plt.subplots(figsize=(10.6, 6.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.6)
    ax.set_axis_off()

    steps = [
        ("① 上电 / 复位", "ROM BootROM 固化在芯片内，无法修改\n读取 strapping 引脚决定启动模式", "#d5d8dc"),
        ("② Bootloader（0x0 开始）", "初始化 Flash 与基础时钟\n校验分区表、选择可启动 app 分区", "#aed6f1"),
        ("③ 校验并加载 app", "校验镜像头部与 SHA256\n把 .text / .rodata 映射到地址空间", "#a9dfbf"),
        ("④ 运行时初始化", "C 运行时：清零 .bss、拷贝 .data 到 RAM\n调用 app_main()", "#f9e79f"),
        ("⑤ 应用运行", "FreeRTOS 调度器启动\n你的任务开始并发执行", "#f5cba7"),
    ]

    y = 7.7
    for i, (title, desc, color) in enumerate(steps):
        ax.add_patch(Rectangle((1.2, y - 1.05), 7.0, 1.05, facecolor=color,
                               edgecolor="#2c3e50", lw=1.2))
        ax.text(4.7, y - 0.32, title, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=C_TEXT)
        ax.text(4.7, y - 0.76, desc, ha="center", va="center", fontsize=8.2,
                color=C_TEXT, linespacing=1.35)
        if i < len(steps) - 1:
            ax.annotate("", xy=(4.7, y - 1.32), xytext=(4.7, y - 1.06),
                        arrowprops=dict(arrowstyle="-|>", color=C_GRID, lw=1.4))
        y -= 1.55

    # 旁注：失败表现要与所处的阶段对应
    ax.text(8.55, 7.15, "失败 → 停在这里\n串口无任何输出", fontsize=8, color="#7b241c")
    ax.text(8.55, 5.60, "分区表坏了 →\nInvalid partition table", fontsize=8, color="#7b241c")
    ax.text(8.55, 4.05, "镜像校验失败 →\n回退到另一分区 / 反复重启", fontsize=8, color="#7b241c")
    ax.text(8.55, 2.50, "此时才能用\nprintf 调试", fontsize=8, color="#1e8449")

    _save(fig, "esp32-boot-chain.svg")


if __name__ == "__main__":
    struct_layouts()
    memory_regions()
    vtable_layout()
    pointer_array()
    esp32_flash_partition()
    esp32_boot_chain()
    print("done")
