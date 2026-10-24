"""按行号边界替换函数，修正 gen_diagrams6.py 的 4 张图。"""
import io
import re

P = "scripts/gen_diagrams6.py"


def load():
    return io.open(P, encoding="utf-8").read().split("\n")


def fn_range(lines, name):
    """返回 (start, end) 行号：从 'def name(' 到下一个顶层 def 之前。"""
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(f"def {name}("):
            start = i
            break
    if start is None:
        raise SystemExit(f"未找到 def {name}(")
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("def "):
            return start, j
    return start, len(lines)


NEW_COPY = '''def python_copy():
    """深拷贝与浅拷贝的差别"""
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.4)
    ax.set_axis_off()
    ax.text(0.2, 8.0, "浅拷贝 vs 深拷贝：嵌套结构只复制了第一层",
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

    ax.text(0.4, 7.45, "原始：a = [[1, 2], [3, 4]]　两个内层列表各自独立",
            fontsize=9.6, fontweight="bold", color=TEXT)
    draw_row(6.3, "a", "list", ORANGE,
             "内层[0]", "对象 [1,2]", GREEN,
             "内层[1]", "对象 [3,4]", GREEN)

    ax.text(0.4, 5.5, "① 浅拷贝 b = copy.copy(a) —— 只新建外层，内层仍指向原来两个对象",
            fontsize=9.4, fontweight="bold", color=RED)
    draw_row(4.35, "b", "新 list", ORANGE,
             "新槽位[0]", "指向上面那个", PINK,
             "新槽位[1]", "指向上面那个", PINK,
             note="← 新槽位装的是旧引用")
    ax.text(0.4, 3.9, "b[0].append(99)  →  a 也变了！这就是「头号坑」",
            fontsize=8.8, color=RED, fontweight="bold")

    ax.text(0.4, 3.3, "② 深拷贝 b = copy.deepcopy(a) —— 内层也复制成全新的对象",
            fontsize=9.4, fontweight="bold", color="#1e8449")
    draw_row(2.15, "b", "新 list", ORANGE,
             "新槽位[0]", "全新的 [1,2]", GREEN,
             "新槽位[1]", "全新的 [3,4]", GREEN,
             note="← 全是新对象，彻底独立")
    ax.text(0.4, 1.7, "b[0].append(99)  →  a 完全不受影响", fontsize=8.8,
            color="#1e8449", fontweight="bold")

    ax.text(0.4, 1.15, "另一种更隐蔽的浅拷贝来源（不需要 copy 模块）：",
            fontsize=9, fontweight="bold", color=TEXT)
    ax.text(0.4, 0.78, "b = a[:]　　　b = list(a)　　　b = a * 1"
                       "　　—— 切片、构造函数、重复运算都是浅拷贝",
            fontsize=8.4, color=TEXT)
    ax.text(0.4, 0.3,
            "记忆法：元素是不可变类型（int/str/tuple）时浅拷贝就够；元素是可变类型（list/dict）时必须深拷贝。",
            fontsize=8.2, color=LINE)

    _save(fig, "python-copy-depth.svg")
'''

NEW_OTA = '''def esp32_ota_partition():
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

    ax.text(0.5, 2.5, "自检与回滚（产品必须实现）", fontsize=10,
            fontweight="bold", color=RED)
    pts = [
        "• 新固件首次启动状态是 ESP_OTA_IMG_PENDING_VERIFY",
        "• 自检通过后调 esp_ota_mark_app_valid_cancel_rollback() 确认",
        "• 自检失败则调 esp_ota_mark_app_invalid_rollback_and_reboot()",
        "  → Bootloader 自动回滚到上一个正常分区",
        "• 不实现这一步，坏固件会一直重启，只能拆机重烧",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 2.1 - i * 0.36, s, fontsize=8.4, color=TEXT)

    ax.text(0.5, 0.55, "分区表要求：必须有两个 app 分区（ota_0 / ota_1），Flash 至少 8MB 才宽裕。",
            fontsize=8.4, color=TEXT)
    ax.text(0.5, 0.2, "默认 singleapp 分区表只有一个 factory 分区 —— OTA 直接失败（update 句柄为 NULL）。",
            fontsize=8.4, color=RED)

    _save(fig, "esp32-ota-partition.svg")
'''


def main():
    lines = load()

    for name, new in [("python_copy", NEW_COPY),
                      ("esp32_ota_partition", NEW_OTA)]:
        s, e = fn_range(lines, name)
        lines = lines[:s] + new.split("\n") + lines[e:]
        print(f"已替换 {name}（{e - s} 行 -> {len(new.split(chr(10)))} 行）")

    t = "\n".join(lines)

    # fork 注解移到方框下方
    old = '    ax.text(6.6, 3.97, "← 没有真正复制任何数据", fontsize=8.2, color="#1e8449")'
    new_txt = '    ax.text(3.45, 3.22, "只增加引用计数，没有复制任何数据", fontsize=7.8, color="#1e8449")'
    if old in t:
        t = t.replace(old, new_txt, 1)
        print("已修 fork 注解")
    else:
        print("fork 注解未匹配")

    # 虚拟内存右栏压缩
    t = t.replace('ax.text(7.0, 3.2, "虚拟内存带来什么"',
                  'ax.text(7.0, 3.05, "虚拟内存带来什么"', 1)
    t = t.replace('        ax.text(7.0, 2.8 - i * 0.31, s, fontsize=8, color=TEXT)',
                  '        ax.text(7.0, 2.62 - i * 0.255, s, fontsize=7.8, color=TEXT)', 1)

    old_note = '''    ax.text(0.4, 0.25,
            "查证：cat /proc/<pid>/maps 看某个进程的地址空间；"
            "pmap <pid> 更易读；cat /proc/<pid>/status | grep Vm 看用量。",
            fontsize=8.2, color=LINE)'''
    new_note = '''    ax.text(0.4, 0.5, "查证：cat /proc/<pid>/maps 看地址空间；pmap <pid> 更易读；",
            fontsize=8.2, color=LINE)
    ax.text(0.4, 0.18, "　　　cat /proc/<pid>/status | grep Vm 看实际用量。",
            fontsize=8.2, color=LINE)'''
    if old_note in t:
        t = t.replace(old_note, new_note, 1)
        print("已修虚拟内存底部说明")
    else:
        print("虚拟内存底部说明未匹配")

    io.open(P, "w", encoding="utf-8", newline="\n").write(t)
    print("写入完成")


if __name__ == "__main__":
    main()
