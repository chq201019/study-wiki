"""
第十六批（gen16）：ESP32-S3 主线补图——接线示意 / 引脚分区 / 时序 / 内存。

规矩：图里每一个数字都必须能在 docs/ 里找到出处；出处写在每个函数的注释里，
完整对照表见交付报告。找不到出处的数值一律不画。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon, Circle, FancyBboxPatch
from matplotlib import font_manager, rcParams

OUT = os.path.join("static", "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

for _f in ["Microsoft YaHei", "Noto Sans SC", "SimHei", "Source Han Sans SC"]:
    if any(x.name == _f for x in font_manager.fontManager.ttflist):
        rcParams["font.sans-serif"] = [_f]
        break
rcParams["axes.unicode_minus"] = False
rcParams["text.parse_math"] = False

C_DATA = "#7fb3d5"
C_PAD = "#e8b4b8"
C_ALIGN = "#f5cba7"
C_TEXT = "#1b2631"
C_GRID = "#5d6d7e"

BLUE, PINK, ORANGE = "#7fb3d5", "#e8b4b8", "#f5cba7"
GREEN, PURPLE, GREY = "#a9dfbf", "#d2b4de", "#d5dbdb"
TEXT, LINE, RED, DARK = C_TEXT, C_GRID, "#c0392b", "#2c3e50"
YELLOW = "#f9e79f"


def _save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, format="svg", bbox_inches="tight", transparent=True)
    try:
        os.makedirs("_preview", exist_ok=True)
        fig.savefig(os.path.join("_preview", name.replace(".svg", ".png")),
                    format="png", bbox_inches="tight", transparent=True, dpi=130)
    except Exception:
        pass
    plt.close(fig)
    print("wrote", p)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_axis_off()
    return fig, ax


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


def wire(ax, pts, color=LINE, lw=1.8, ls="-"):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, linestyle=ls,
            solid_capstyle="round", solid_joinstyle="round")


def pin_stub(ax, x, y, w, h, name, color=YELLOW, fs=8.2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=DARK, lw=1.0))
    ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=fs,
            color=TEXT, fontweight="bold")


def gnd_symbol(ax, x, y, label="GND", fs=8.2):
    ax.plot([x - 0.34, x + 0.34], [y, y], color=LINE, lw=1.8)
    ax.plot([x - 0.22, x + 0.22], [y - 0.16, y - 0.16], color=LINE, lw=1.6)
    ax.plot([x - 0.10, x + 0.10], [y - 0.30, y - 0.30], color=LINE, lw=1.4)
    ax.text(x, y - 0.55, label, ha="center", va="center", fontsize=fs, color=LINE)


def vcc_symbol(ax, x, y, label="3.3V", fs=8.2):
    ax.plot([x, x], [y, y + 0.30], color=LINE, lw=1.8)
    ax.plot([x - 0.34, x + 0.34], [y + 0.30, y + 0.30], color=LINE, lw=1.8)
    ax.text(x, y + 0.55, label, ha="center", va="center", fontsize=fs,
            color=LINE, fontweight="bold")


def resistor(ax, x, y, w=1.55, h=0.52, label="220Ω", fs=8.4):
    ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor=DARK, lw=1.4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
            color=TEXT, fontweight="bold")


def led_symbol(ax, x, y, s=0.55):
    ax.add_patch(Polygon([(x, y - s), (x, y + s), (x + s * 1.35, y)],
                         closed=True, facecolor=ORANGE, edgecolor=DARK, lw=1.3))
    ax.plot([x + s * 1.35, x + s * 1.35], [y - s, y + s], color=DARK, lw=1.8)


def board(ax, x, y, w, h, title_text="ESP32-S3\nDevKitC-1", fs=9.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.18",
                                facecolor="#eaf2f8", edgecolor=DARK, lw=1.6))
    ax.text(x + w / 2, y + h - 0.34, title_text, ha="center", va="center", fontsize=fs,
            color=TEXT, fontweight="bold", linespacing=1.25)


def note(ax, x, y, text, fs=8.0, color=LINE, ls=1.2):
    ax.text(x, y, text, fontsize=fs, color=color, linespacing=ls, va="center")


def title(ax, x, y, text, fs=12.5):
    ax.text(x, y, text, fontsize=fs, fontweight="bold", color=TEXT)




# ============================================================
# 1. 接线示意：GPIO 按键 + LED
#    GPIO5 → 按键 → GND（docs/quickstart/arduino-basics.mdx:67,93）
#    内部上拉约 45kΩ（docs/course/l4-peripherals/gpio.mdx:73,91；
#                    docs/hardware/esp-basics/09-gpio-input.mdx:60）
#    GPIO4 → 220Ω → LED 阳极，阴极 → GND（docs/quickstart/arduino-basics.mdx:92）
#    板载 BOOT 键 = GPIO0（docs/quickstart/arduino-basics.mdx:46）
# ============================================================
def esp32_wire_button_led():
    fig, ax = canvas(12.6, 7.2, 13.0, 7.8)
    title(ax, 0.4, 7.45, "按键与 LED 接线：一根信号线 + 一根地线就够了")

    board(ax, 0.5, 2.05, 3.20, 5.15, "ESP32-S3\nDevKitC-1")
    for yc, name, col in [(6.35, "GPIO5", C_DATA), (4.85, "GPIO4", C_DATA),
                          (3.55, "GPIO0", GREY), (2.85, "3.3V", "#fadbd8"),
                          (2.30, "GND", "#d5d8dc")]:
        pin_stub(ax, 2.35, yc - 0.22, 1.15, 0.44, name, color=col, fs=8.2)

    # 按键支路
    wire(ax, [(3.7, 6.35), (6.05, 6.35)])
    ax.add_patch(Circle((6.18, 6.35), 0.095, facecolor="white", edgecolor=DARK, lw=1.4, zorder=5))
    ax.add_patch(Circle((7.55, 6.35), 0.095, facecolor="white", edgecolor=DARK, lw=1.4, zorder=5))
    ax.plot([6.26, 7.48], [6.42, 6.92], color=DARK, lw=2.0, solid_capstyle="round")
    ax.text(6.86, 6.05, "按键", ha="center", fontsize=8.4, color=TEXT, fontweight="bold")
    wire(ax, [(7.65, 6.35), (9.35, 6.35), (9.35, 5.60)])
    gnd_symbol(ax, 9.35, 5.60)
    ax.text(9.90, 6.60, "内部上拉 45kΩ 把引脚拴在 3.3V\n→ 松开读 1，按下被拉到 GND 读 0",
            fontsize=7.8, color="#1e8449", va="center", linespacing=1.35)

    # LED 支路
    wire(ax, [(3.7, 4.85), (5.35, 4.85)])
    resistor(ax, 5.35, 4.59, 1.55, 0.52, "220Ω")
    wire(ax, [(6.90, 4.85), (8.20, 4.85)])
    led_symbol(ax, 8.20, 4.85, 0.52)
    wire(ax, [(8.90, 4.85), (11.05, 4.85), (11.05, 3.95)])
    gnd_symbol(ax, 11.05, 3.95)
    ax.text(8.05, 5.55, "LED\n阳极→阴极", ha="center", fontsize=7.6, color=TEXT, linespacing=1.25)
    ax.text(9.95, 4.35, "限流电阻 220Ω\n把 GPIO 电流限在安全范围", fontsize=7.6, color=LINE,
            va="center", linespacing=1.35)

    ax.add_patch(FancyBboxPatch((0.5, 0.30), 12.10, 1.30,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.78, 1.30, "接线清单：GPIO5 → 按键 → GND；GPIO4 → 220Ω → LED 阳极，阴极 → GND",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.78, 0.94, "不用外接上拉电阻：内部上拉 45kΩ 短线够用，线长超过 30cm 或电机旁要外接 10kΩ",
            fontsize=7.9, color=TEXT)
    ax.text(0.78, 0.60, "板载 BOOT 键已经接在 GPIO0 上，什么都不用接；板载 RGB 灯是 WS2812，digitalWrite 点不亮",
            fontsize=7.9, color=LINE)
    ax.text(0.78, 0.36, "注意：GPIO35 / 36 / 37 被模组内部 Flash/PSRAM 占用，任何情况下都不要外接",
            fontsize=7.9, color=RED)

    _save(fig, "esp32-wire-button-led.svg")


# ============================================================
# 2. 引脚能力分区图
#    纯 GPIO 1～18 / Flash-PSRAM 35,36,37 / 模组内部 33,34 /
#    USB 19,20 / UART0 43,44 / strapping 0,3,45,46
#    S3 没有任何仅输出脚（那是 S2 / 经典 ESP32 的特性）：docs/reference/porting.mdx:37、docs/course/l4-peripherals/gpio.mdx:243
#      （docs/course/l4-peripherals/gpio.mdx:37-45）
#    ADC1: GPIO1～10，ADC2: GPIO11～20（docs/course/l4-peripherals/adc-dac.mdx:59）
#    RGB: v1.0 GPIO48 / v1.1 GPIO38（docs/reference/pinout.mdx:85-86）
#    GPIO45 选 Flash 供电电压（docs/course/l1-hardware/board.mdx:191,202-204）
# ============================================================
def esp32_pin_capability_map():
    fig, ax = canvas(13.0, 7.6, 14.6, 8.2)
    title(ax, 0.4, 7.85, "ESP32-S3 引脚能力分区：先认禁区，再排外设")
    note(ax, 0.4, 7.50, "同一个编号可能同时属于两类（如 GPIO3 既是首选区也是 strapping），图里按「最需要注意的限制」上色", fs=7.9)

    x0, cw, gap = 0.75, 0.250, 0.038
    def cx(n):
        return x0 + n * (cw + gap)

    colors = {}
    for n in range(1, 19):
        colors[n] = GREEN
    for n in (19, 20):
        colors[n] = PURPLE
    for n in (33, 34, 35, 36, 37):
        colors[n] = PINK
    colors[43] = colors[44] = BLUE
    for n in list(range(21, 33)) + [38, 39, 40, 41, 42, 47, 48]:
        colors[n] = "#eaeded"
    colors[0] = colors[3] = colors[45] = colors[46] = YELLOW

    yb, hh = 5.35, 0.72
    for n in range(0, 49):
        ax.add_patch(Rectangle((cx(n), yb), cw, hh, facecolor=colors[n],
                               edgecolor=DARK, lw=0.8))
        if n % 2 == 0:
            ax.text(cx(n) + cw / 2, yb - 0.26, str(n), ha="center", va="center",
                    fontsize=6.4, color=LINE)

    ax.add_patch(Rectangle((cx(1), yb + hh + 0.10), cx(10) + cw - cx(1), 0.30,
                           facecolor=C_DATA, edgecolor=DARK, lw=1.0, alpha=0.75))
    ax.text((cx(1) + cx(10) + cw) / 2, yb + hh + 0.25, "ADC1  GPIO1～10",
            ha="center", va="center", fontsize=7.6, color=TEXT, fontweight="bold")
    ax.add_patch(Rectangle((cx(11), yb + hh + 0.10), cx(20) + cw - cx(11), 0.30,
                           facecolor=C_PAD, edgecolor=DARK, lw=1.0, alpha=0.75))
    ax.text((cx(11) + cx(20) + cw) / 2, yb + hh + 0.25, "ADC2  GPIO11～20",
            ha="center", va="center", fontsize=7.6, color=TEXT, fontweight="bold")

    for n in (0, 3, 45, 46):
        ax.add_patch(Polygon([[cx(n) + cw / 2, yb - 0.42],
                              [cx(n) + cw / 2 - 0.11, yb - 0.60],
                              [cx(n) + cw / 2 + 0.11, yb - 0.60]],
                             closed=True, facecolor=BLUE, edgecolor=DARK, lw=0.8))
    ax.text(x0 - 0.15, yb - 0.85, "▲ = strapping 引脚：只在复位释放的瞬间被采样（0 / 3 / 45 / 46）",
            fontsize=7.7, color=TEXT)

    for n, tag in ((38, "v1.1"), (48, "v1.0")):
        ax.add_patch(Rectangle((cx(n) - 0.02, yb - 0.02), cw + 0.04, hh + 0.04,
                               facecolor="none", edgecolor="#b7950b", lw=2.0))
        ax.text(cx(n) + cw / 2, yb + hh + 0.60, "RGB\n" + tag, ha="center",
                va="center", fontsize=6.8, color="#7d6608", linespacing=1.15)

    legend = [
        ("纯 GPIO，常规使用首选（GPIO1～18）", GREEN),
        ("Flash / PSRAM 内部占用，禁止外接（35 / 36 / 37）", PINK),
        ("模组内部用，建议避开（33 / 34）", PINK),
        ("复位瞬间被采样（0 / 3 / 45 / 46）", YELLOW),
        ("原生 USB 时被占用（19 / 20）", PURPLE),
        ("调试串口 UART0，占了就看不到日志（43 / 44）", BLUE),
        ("本教程未列特殊限制", "#eaeded"),
    ]
    for i, (txt, col) in enumerate(legend):
        yy = 3.95 - i * 0.40
        ax.add_patch(Rectangle((0.80, yy - 0.13), 0.32, 0.26, facecolor=col,
                               edgecolor=DARK, lw=0.8))
        ax.text(1.28, yy, txt, fontsize=8.0, va="center", color=TEXT)

    ax.text(0.80, 1.18, "S3 没有「仅输出脚」（那是 S2 的特性）；四个 strapping 脚采样结束后就是普通 GPIO",
            fontsize=7.7, color=LINE)

    ax.add_patch(FancyBboxPatch((7.55, 0.55), 6.85, 3.45,
                                boxstyle="round,pad=0.10,rounding_size=0.15",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.3))
    ax.text(7.85, 3.70, "三条硬约束", fontsize=9.4, fontweight="bold", color=RED)
    for i, t in enumerate([
        "① GPIO35 / 36 / 37 被 Octal Flash/PSRAM 占用",
        "    接了轻则程序崩溃，重则写坏 Flash、芯片变砖",
        "② GPIO45 决定 Flash 供电电压（3.3V / 1.8V）",
        "    上电被拉错：轻则读不出数据开不了机，重则损坏 Flash",
        "③ GPIO46 同样是 strapping 脚：复位瞬间也被采样",
    ]):
        ax.text(7.85, 3.28 - i * 0.46, t, fontsize=7.9, color=TEXT)
    ax.text(7.85, 0.80, "规划口诀：先排挑食的（摄像头 15+ 脚、禁用脚、strapping 脚），",
            fontsize=7.9, color="#1e8449")
    ax.text(7.85, 0.58, "剩下的才是自由引脚", fontsize=7.9, color="#1e8449")

    _save(fig, "esp32-pin-capability-map.svg")




# ============================================================
# 3. 接线示意：I2C OLED（含上拉电阻与地址）
#    SDA=GPIO8 / SCL=GPIO9（docs/reference/pinout.mdx:27,30；
#      docs/quickstart/bus.mdx:30-31,52；docs/course/l4-peripherals/i2c-spi-uart.mdx:82-83）
#    SSD1306 地址 0x3C（少数 0x3D）（docs/quickstart/bus.mdx:62；
#      docs/hardware/esp-basics/12-i2c.mdx:48）
#    上拉 4.7kΩ（docs/course/l4-peripherals/i2c-spi-uart.mdx:112；
#      docs/hardware/esp-basics/12-i2c.mdx:37,114）
#    速率 100kHz 标准 / 400kHz 快速（docs/course/l4-peripherals/i2c-spi-uart.mdx:67,94,115）
#    扫描范围 0x08～0x77（docs/hardware/esp-basics/12-i2c.mdx:42,89）
# ============================================================
def esp32_wire_i2c_oled():
    fig, ax = canvas(12.6, 7.6, 13.0, 8.2)
    title(ax, 0.4, 7.90, "I2C 接 OLED：两根信号线 + 两根电源线，上拉是命门")

    board(ax, 0.5, 2.30, 3.00, 4.35, "ESP32-S3")
    for yc, name, col in [(5.95, "3V3", "#fadbd8"), (4.95, "GPIO8 SDA", C_DATA),
                          (3.95, "GPIO9 SCL", C_DATA), (2.75, "GND", "#d5d8dc")]:
        pin_stub(ax, 2.15, yc - 0.22, 1.35, 0.44, name, color=col, fs=8.0)

    ax.add_patch(FancyBboxPatch((9.15, 2.30), 3.45, 4.35,
                                boxstyle="round,pad=0.06,rounding_size=0.16",
                                facecolor="#eaf2f8", edgecolor=DARK, lw=1.6))
    ax.text(10.87, 6.28, "SSD1306 OLED\n128×64", ha="center", va="center",
            fontsize=9.2, fontweight="bold", color=TEXT, linespacing=1.25)
    for yc, name, col in [(5.95, "VCC", "#fadbd8"), (4.95, "SDA", C_DATA),
                          (3.95, "SCL", C_DATA), (2.75, "GND", "#d5d8dc")]:
        pin_stub(ax, 9.15, yc - 0.20, 0.90, 0.40, name, color=col, fs=7.6)

    wire(ax, [(3.5, 5.95), (8.55, 5.95), (8.55, 5.95), (9.15, 5.95)], color="#c0392b", lw=1.9)
    wire(ax, [(3.5, 4.95), (9.15, 4.95)], color="#2471a3", lw=2.0)
    wire(ax, [(3.5, 3.95), (9.15, 3.95)], color="#1a5276", lw=2.0)
    wire(ax, [(3.5, 2.75), (9.15, 2.75)], color="#5d6d7e", lw=1.9)

    # SDA 上拉
    ax.add_patch(Circle((6.10, 4.95), 0.075, facecolor="#c0392b", edgecolor=DARK, lw=0.8, zorder=6))
    wire(ax, [(6.10, 4.95), (6.10, 5.10)], color="#c0392b", lw=1.5)
    resistor(ax, 5.38, 5.10, 1.45, 0.42, "4.7kΩ", fs=7.6)
    wire(ax, [(6.10, 5.52), (6.10, 5.64)], color="#c0392b", lw=1.5)
    ax.plot([5.50, 6.70], [5.64, 5.64], color="#c0392b", lw=1.8)
    ax.text(6.85, 5.64, "3.3V", fontsize=7.6, color="#c0392b", va="center")

    # SCL 上拉
    ax.add_patch(Circle((7.55, 3.95), 0.075, facecolor="#c0392b", edgecolor=DARK, lw=0.8, zorder=6))
    wire(ax, [(7.55, 3.95), (7.55, 4.08)], color="#c0392b", lw=1.5)
    resistor(ax, 6.83, 4.08, 1.45, 0.42, "4.7kΩ", fs=7.6)
    wire(ax, [(7.55, 4.50), (7.55, 4.62)], color="#c0392b", lw=1.5)
    ax.plot([6.95, 8.15], [4.62, 4.62], color="#c0392b", lw=1.8)
    ax.text(8.30, 4.62, "3.3V", fontsize=7.6, color="#c0392b", va="center")

    ax.text(0.55, 7.72, "开漏输出只会把线拉低，松手后靠这两只 4.7kΩ 把线抬回 3.3V；模块一般已自带，没有就外接",
            fontsize=7.9, color=RED, va="center")
    ax.text(0.55, 7.40, "两根线上都可以挂多台设备，靠 7 位地址区分（0x08～0x77）；量 SDA/SCL 空闲电压应接近 3.3V",
            fontsize=7.9, color=TEXT, va="center")

    ax.add_patch(FancyBboxPatch((0.5, 0.35), 12.10, 1.32,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.78, 1.36, "接线四根：VCC→3.3V，GND→GND，SCL→GPIO9，SDA→GPIO8；设备地址 0x3C（少数 0x3D）",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.78, 1.00, "接完第一件事是跑地址扫描器：一个都扫不到 = 接线 / 供电 / 上拉问题，别急着写业务代码",
            fontsize=7.9, color=TEXT)
    ax.text(0.78, 0.64, "速率：标准模式 100kHz / 快速模式 400kHz；杜邦线超过 30cm 就降到 100kHz",
            fontsize=7.9, color=LINE)

    _save(fig, "esp32-wire-i2c-oled.svg")


def esp32_i2c_timing():
    fig, ax = canvas(13.0, 7.6, 13.4, 8.4)
    title(ax, 0.4, 8.05, "I2C 起始、地址、应答的波形：SDA 只能在 SCL 低电平时变")
    note(ax, 0.4, 7.70, "以 SCL 为参考线，看 SDA 在「时钟高电平中间」是什么状态，就是哪一位", fs=8.2)

    left, right = 2.45, 12.75
    pre, post = 0.95, 0.75
    sw = (right - left - pre - post) / 9.0
    lo, hi = sw * 0.30, sw * 0.78
    bs, bd, hh = 4.95, 2.95, 0.80

    ax.text(1.15, bs + hh / 2, "SCL", fontsize=10, fontweight="bold", color=TEXT,
            ha="center", va="center")
    ax.text(1.15, bd + hh / 2, "SDA", fontsize=10, fontweight="bold", color=TEXT,
            ha="center", va="center")

    scl = [(left, bs + hh), (left + pre - 0.32, bs + hh), (left + pre - 0.32, bs)]
    for i in range(9):
        a = left + pre + i * sw
        scl += [(a + lo, bs), (a + lo, bs + hh), (a + hi, bs + hh), (a + hi, bs)]
    last = left + pre + 9 * sw
    scl += [(last + 0.22, bs), (last + 0.22, bs + hh), (right, bs + hh)]
    ax.plot([p[0] for p in scl], [p[1] for p in scl], color="#1a5276", lw=1.9,
            solid_joinstyle="miter")

    bits = "01111000"
    sda = [(left, bd + hh), (left + 0.50, bd + hh)]
    sda += [(left + 0.50, bd)]
    prev = 0
    for i, b in enumerate(bits + "0"):
        x = left + pre + i * sw + sw * 0.10
        v = int(b)
        if v != prev:
            sda += [(x, bd if prev == 0 else bd + hh), (x, bd + hh if v else bd)]
            prev = v
    tail = left + pre + 9 * sw
    sda += [(tail + 0.45, bd), (tail + 0.45, bd + hh), (right, bd + hh)]
    ax.plot([p[0] for p in sda], [p[1] for p in sda], color="#7d6608", lw=1.9,
            solid_joinstyle="miter")

    for i, lab in enumerate(["A6", "A5", "A4", "A3", "A2", "A1", "A0", "W", "ACK"]):
        a = left + pre + i * sw
        ax.plot([a + sw * 0.55, a + sw * 0.55], [bd - 0.12, bd - 0.30],
                color=LINE, lw=0.9)
        ax.text(a + sw * 0.55, bd - 0.52, lab, ha="center", va="center",
                fontsize=7.6, color=RED if lab == "ACK" else LINE,
                fontweight="bold" if lab == "ACK" else "normal")

    ax.annotate("START\nSCL 高时把 SDA 拉低", xy=(left + 0.50, bd + hh / 2),
                xytext=(left - 0.70, bd + hh + 1.05), fontsize=8.0, color=RED, ha="left",
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    ax.annotate("STOP\nSCL 高时释放 SDA", xy=(tail + 0.45, bd + hh / 2),
                xytext=(right - 1.60, bd + hh + 1.05), fontsize=8.0, color=RED, ha="left",
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    ax.annotate("地址 7 位 + 读写位：0x3C 左移一位、写 = 0 → 0111 1000",
                xy=(left + pre + 3.6 * sw, bd + hh + 0.08),
                xytext=(left + pre + 3.4 * sw, bd - 1.55),
                fontsize=8.0, color=TEXT, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.1))
    ax.annotate("ACK：接收方拉低 SDA\n第 9 拍不下降 = 没有应答",
                xy=(left + pre + 8.55 * sw, bd + 0.12),
                xytext=(right - 2.85, bd - 1.55),
                fontsize=8.0, color="#1e8449", ha="center", linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color="#1e8449", lw=1.1))

    ax.add_patch(FancyBboxPatch((0.5, 0.30), 12.45, 0.92,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.78, 1.02, "「没有 ACK」是 I2C 最好用的诊断信息：设备没接好、地址不对、缺上拉，都表现为第 9 拍 SDA 不动",
            fontsize=8.1, color=TEXT, fontweight="bold")
    ax.text(0.78, 0.64, "一帧之后还有数据字节，每个字节后面都跟着一个 ACK；读方向则是「重复起始」不发 STOP",
            fontsize=7.9, color=TEXT)

    _save(fig, "esp32-i2c-timing.svg")


# ============================================================
# 5. 接线示意：电位器 → ADC
#    电位器两边接 3.3V 和 GND，中间脚接 GPIO1（docs/quickstart/adc-dac.mdx:70）
#    ADC1_CH0 = GPIO1（docs/quickstart/adc-dac.mdx:80；
#      docs/reference/pinout.mdx:46）
#    12 位 = 4096 级；电压 = 读数 / 4095 × 量程
#      （docs/course/l4-peripherals/adc-dac.mdx:57,62）
#    DB_11/DB_12 有效量程 0～3.1V（上限 3100mV），每格约 0.76mV = 3100/4096
#      （docs/course/l4-peripherals/adc-dac.mdx:53,75,130；docs/hardware/esp-basics/10-adc.mdx:51-52）
#    3.3V 只是引脚耐压上限，不是有效测量上限（同文件 :62；10-adc.mdx:260）
#    读数在 0～4095 之间（docs/quickstart/adc-dac.mdx:145）
#    输入上限 3.3V，绝不能接 5V（docs/course/l4-peripherals/adc-dac.mdx:60）
#    ADC2 与 WiFi 冲突（docs/course/l4-peripherals/adc-dac.mdx:177-180）
# ============================================================
def esp32_wire_adc_pot():
    fig, ax = canvas(12.6, 7.2, 13.0, 7.8)
    title(ax, 0.4, 7.42, "电位器接 ADC：三根线把「旋钮位置」变成 0～4095")

    board(ax, 0.5, 2.30, 2.85, 4.85, "ESP32-S3")
    for yc, name, col in [(6.45, "3V3", "#fadbd8"), (4.75, "GPIO1", C_DATA),
                          (2.95, "GND", "#d5d8dc")]:
        pin_stub(ax, 2.00, yc - 0.22, 1.25, 0.44, name, color=col, fs=8.2)

    ax.add_patch(FancyBboxPatch((6.95, 3.55), 1.55, 3.35,
                                boxstyle="round,pad=0.05,rounding_size=0.12",
                                facecolor="#f6ddcc", edgecolor=DARK, lw=1.5))
    ax.text(7.73, 6.60, "电位器", ha="center", fontsize=8.6, color=TEXT, fontweight="bold")
    ax.text(7.73, 6.24, "10kΩ", ha="center", fontsize=8.4, color=TEXT)
    ax.plot([7.73, 7.73], [4.75, 5.30], color=DARK, lw=2.0)
    ax.add_patch(Polygon([[7.59, 5.30], [7.87, 5.30], [7.73, 5.58]], closed=True,
                         facecolor=LINE, edgecolor=DARK, lw=0.8))
    wire(ax, [(3.25, 6.45), (6.95, 6.45)])
    wire(ax, [(3.25, 4.75), (6.95, 4.75)])
    wire(ax, [(3.25, 2.95), (7.73, 2.95), (7.73, 3.55)])
    ax.text(3.45, 6.73, "① 一端", fontsize=7.7, color=TEXT)
    ax.text(3.45, 5.03, "② 中间脚（抽头）", fontsize=7.7, color=TEXT)
    ax.text(3.45, 3.23, "③ 另一端", fontsize=7.7, color=TEXT)

    ax.add_patch(FancyBboxPatch((10.35, 3.15), 0.62, 4.05,
                                boxstyle="round,pad=0.04,rounding_size=0.06",
                                facecolor="#eaf2f8", edgecolor=DARK, lw=1.3))
    for yy, volts, raw in [(3.45, "0V", "0"), (4.85, "约 1.55V", "约 2048"),
                           (6.25, "3.1V", "4095")]:
        ax.plot([10.35, 10.97], [yy, yy], color=LINE, lw=0.9)
        ax.text(11.12, yy, raw, fontsize=7.6, va="center", color=TEXT)
        ax.text(10.18, yy, volts, fontsize=7.6, va="center", ha="right", color=TEXT)
    ax.text(10.20, 7.55, "读数 ← 电压", fontsize=8.0, color=TEXT, fontweight="bold")
    ax.text(10.10, 2.80, "电压 = 读数 / 4095 × 量程", fontsize=7.8, color=RED)

    ax.add_patch(FancyBboxPatch((0.5, 0.32), 12.10, 1.42,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.78, 1.45, "接线：两端接 3.3V 与 GND（就是个可调分压器），中间脚（抽头）接 GPIO1 = ADC1_CH0",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.78, 1.06, "为什么用 GPIO1：它属于 ADC1（GPIO1～10），WiFi 开着也能读；ADC2（GPIO11～20）与 WiFi 抢资源，联网时可能恒为 0",
            fontsize=7.9, color=TEXT)
    ax.text(0.78, 0.70, "12 位 = 4096 格；有效量程 0～3.1V，每格约 0.76mV（超过 3.1V 只饱和到 4095）；引脚耐压上限 3.3V，绝对不要接 5V",
            fontsize=7.9, color=TEXT)
    ax.text(0.78, 0.44, "读数偏低的典型原因：输入源内阻太大（采样电容充不满），加 0.1µF 电容或运放缓冲",
            fontsize=7.9, color=LINE)

    _save(fig, "esp32-wire-adc-pot.svg")


# ============================================================
# 6. ADC 采样时序：逐次逼近 12 猜
#    12 位 → 12 次猜测；第 1 猜理论满量程 3.3V 的一半 = 1.65V（3.3V 是理论满量程）
#      （docs/course/l4-peripherals/adc-dac.mdx:36-45；10-adc.mdx:49 理论满量程 3.30V）
#    单次采样几十微秒（同文件 :49）
#    采样靠内部小电容，源内阻大会充不满 → 读数偏低；加 0.1µF 或运放缓冲（:50）
#    转换期间输入不能变（:51）；平均滤波 16 次（:268）
#    12 位 = 4096 格；DB_11/DB_12 有效量程 0～3.1V，每格约 0.76mV（:53,:75,:130）
#    3.3V = 引脚耐压上限（超了会烧），3.1V = 有效测量上限（超了只饱和到 4095）
#      （docs/hardware/esp-basics/10-adc.mdx:51-52,260；adc-dac.mdx:62）
#    读数 0～4095（quickstart/adc-dac.mdx:145）
# ============================================================
def esp32_adc_sample_timing():
    fig, ax = canvas(12.8, 7.2, 13.2, 7.8)
    title(ax, 0.4, 7.45, "一次 ADC 转换：12 次二分猜测，猜完才有一个读数")
    note(ax, 0.4, 7.10, "12 位 = 4096 格；每猜一次排除一半可能，12 次正好锁定其中一格——这就是「逐次逼近（SAR）」", fs=8.2)

    rows = [
        ("第 1 猜", "先产生理论满量程（3.3V）的一半 = 1.65V，问比较器「输入比它大吗？」"),
        ("第 2 猜", "在剩下的一半范围里再取中点"),
        ("……", "每猜一次排除一半可能"),
        ("第 12 猜", "范围缩到 1 个格子，锁定读数"),
    ]
    for i, (k, v) in enumerate(rows):
        yy = 6.35 - i * 0.72
        ax.add_patch(Rectangle((0.60, yy), 1.85, 0.56, facecolor=YELLOW,
                               edgecolor=DARK, lw=1.1))
        ax.text(1.52, yy + 0.28, k, ha="center", va="center", fontsize=8.6,
                color=TEXT, fontweight="bold")
        ax.add_patch(Rectangle((2.45, yy), 10.35, 0.56, facecolor="#eaf2f8",
                               edgecolor=DARK, lw=1.1))
        ax.text(2.72, yy + 0.28, v, ha="left", va="center", fontsize=8.2, color=TEXT)

    # 三条脾气
    cards = [
        ("脾气一：靠一只内部小电容「存」电压", "#fdf2e9", "#b7950b",
         ["源内阻太大（如串了 1MΩ）→ 采样窗口内充不满", "→ 读数偏低",
          "解法：输入端加 0.1µF 电容、或加运放缓冲"]),
        ("脾气二：转换期间输入不能变", "#eafaf1", "#1e8449",
         ["猜到第 6 次时输入还在跳，结果就作废", "变化快的波形换连续模式（DMA 搬运）"]),
        ("脾气三：单次转换有固定开销", "#eaf2f8", "#2471a3",
         ["单次采样几十微秒——测旋钮、电池绰绰有余", "要看音频波形远远不够，得用连续模式"]),
    ]
    for i, (head, fc, ec, lines) in enumerate(cards):
        x0 = 0.60 + i * 4.32
        ax.add_patch(FancyBboxPatch((x0, 1.95), 4.10, 1.95,
                                    boxstyle="round,pad=0.08,rounding_size=0.12",
                                    facecolor=fc, edgecolor=ec, lw=1.2))
        ax.text(x0 + 0.22, 3.62, head, fontsize=8.4, color=TEXT, fontweight="bold")
        for j, t in enumerate(lines):
            ax.text(x0 + 0.22, 3.18 - j * 0.42, t, fontsize=7.8, color=TEXT)

    ax.add_patch(FancyBboxPatch((0.60, 0.40), 12.20, 1.25,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.88, 1.42, "换算：电压 = 读数 / 4095 × 有效量程；DB_11/DB_12 有效量程 0～3.1V，每格约 0.76mV，读数 0～4095",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.88, 1.04, "读数在跳不是坏了：ADC 天然带噪声，平均滤波 16 次是常用做法",
            fontsize=7.9, color=TEXT)
    ax.text(0.88, 0.68, "量程由衰减档位决定：DB_11 / DB_12 ≈ 0～3.1V；引脚耐压上限仍是 3.3V——超过 3.1V 只饱和到 4095，超过 3.3V 会烧",
            fontsize=7.9, color=LINE)

    _save(fig, "esp32-adc-sample-timing.svg")




# ============================================================
# 7. PWM 占空比 / 分辨率 / 舵机脉宽
#    平均电压 = 占空比 × 电源电压；50% × 3.3V = 1.65V
#      （docs/course/l4-peripherals/pwm.mdx:38-39）
#    duty = 占空比 × (2^分辨率 − 1)；12 位 = 4096 份，50% = 2048/4096（同文件 :127）
#    人眼视觉暂留约 20ms，高于 100Hz 就看不出闪（同文件 :46）
#    舵机 50Hz（20ms），脉宽 500～2500µs ↔ 0°～180°，1500µs = 90°（同文件 :168-193）
#    50Hz + 14 位 = 16384 级，1µs ≈ 0.82 级（同文件 :181）
#    S3 一共 8 个 LEDC 通道（0～7）（docs/quickstart/pwm.mdx:43,216）
# ============================================================
def esp32_pwm_duty_servo():
    fig, ax = canvas(13.0, 7.6, 13.4, 8.2)
    title(ax, 0.4, 7.88, "PWM 三件事：占空比是平均值、分辨率是份数、舵机看脉宽")

    ax.text(0.45, 7.35, "① 占空比决定平均电压（负载要有「惯性」才对它无感）", fontsize=9.2,
            fontweight="bold", color=TEXT)
    for i, (lab, ratio, vavg) in enumerate([("0%", 0.0, "0V"), ("25%", 0.25, "0.83V"),
                                            ("50%", 0.5, "1.65V"), ("100%", 1.0, "3.3V")]):
        x0 = 0.75 + i * 3.20
        base, hh, per = 5.95, 0.80, 2.55
        ax.plot([x0, x0 + per], [base, base], color=LINE, lw=0.9, ls=":")
        ax.plot([x0, x0 + per], [base + hh, base + hh], color=LINE, lw=0.9, ls=":")
        ax.plot([x0, x0 + per * ratio] if ratio > 0 else [x0, x0],
                [base + hh, base + hh], color=BLUE, lw=2.2)
        if ratio < 1:
            ax.plot([x0 + per * ratio, x0 + per], [base, base], color=BLUE, lw=2.2)
        if 0 < ratio < 1:
            ax.plot([x0 + per * ratio, x0 + per * ratio], [base, base + hh],
                    color=BLUE, lw=2.2)
        ax.text(x0 + per / 2, base + hh + 0.30, lab, ha="center", fontsize=8.8,
                color=TEXT, fontweight="bold")
        ax.text(x0 + per / 2, base - 0.32, "平均 " + vavg, ha="center", fontsize=8.2, color=RED)
    ax.text(0.45, 5.28, "平均电压 = 占空比 × 电源电压（3.3V）", fontsize=7.9, color=LINE)

    ax.text(0.45, 4.85, "② 分辨率决定「份数」，占空比是用份数表达的", fontsize=9.2,
            fontweight="bold", color=TEXT)
    for i, (bit, cnt) in enumerate([("8 位", 256), ("10 位", 1024), ("12 位", 4096)]):
        x0 = 0.75 + i * 3.20
        ax.add_patch(Rectangle((x0, 4.05), 2.55, 0.58, facecolor="#eaf2f8",
                               edgecolor=DARK, lw=1.2))
        ax.text(x0 + 0.95, 4.34, bit, ha="center", va="center", fontsize=8.6,
                color=TEXT, fontweight="bold")
        ax.text(x0 + 1.75, 4.34, "%d 份" % cnt, ha="center", va="center", fontsize=8.4,
                color=TEXT)
    ax.text(0.45, 3.72, "duty = 占空比 × (2^分辨率 − 1)：12 位下 50% 就是 2048 / 4096，不是 50",
            fontsize=7.9, color=RED)
    ax.text(0.45, 3.38, "S3 一共 8 个 LEDC 通道（0～7），同一时刻最多 8 路独立 PWM",
            fontsize=7.9, color=LINE)

    ax.text(0.45, 2.95, "③ 舵机不看占空比百分比，只看每 20ms 的脉宽", fontsize=9.2,
            fontweight="bold", color=TEXT)
    sy, sx0 = 2.05, 0.75
    ax.plot([sx0, sx0 + 7.85], [sy, sy], color=LINE, lw=0.9, ls=":")
    ax.plot([sx0, sx0 + 7.85], [sy + 0.50, sy + 0.50], color=LINE, lw=0.9, ls=":")
    for i, (pw, ang) in enumerate([(0.5, "0°"), (1.5, "90°"), (2.5, "180°")]):
        xx = sx0 + i * 2.60
        ax.plot([xx, xx + pw * 0.52], [sy + 0.50, sy + 0.50], color=GREEN, lw=2.6)
        ax.plot([xx, xx + pw * 0.52], [sy, sy], color=GREEN, lw=2.6)
        ax.plot([xx + pw * 0.52, xx + pw * 0.52], [sy, sy + 0.50], color=GREEN, lw=2.6)
        ax.text(xx + pw * 0.26, sy + 0.70, "%dµs" % int(pw * 1000), ha="center",
                fontsize=7.8, color=TEXT)
        ax.text(xx + 1.00, sy - 0.30, ang, ha="center", fontsize=8.6, color=TEXT,
                fontweight="bold")
    ax.text(sx0 + 7.90, sy + 0.30, "周期 50Hz = 20ms", fontsize=7.6, color=LINE,
            ha="left", va="center")

    ax.add_patch(FancyBboxPatch((9.05, 1.10), 4.05, 2.20,
                                boxstyle="round,pad=0.09,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(9.32, 3.00, "换算要留个心眼", fontsize=8.4, color=RED, fontweight="bold")
    for j, t in enumerate(["50Hz + 14 位 = 16384 级 / 20ms", "→ 1µs ≈ 0.82 级",
                           "别直接给满 500 / 2500µs：", "先 1500µs 居中，再往两边试",
                           "顶到机械限位会咔咔响甚至烧舵机"]):
        ax.text(9.32, 2.60 - j * 0.34, t, fontsize=7.8,
                color=RED if j == 4 else TEXT)

    ax.add_patch(FancyBboxPatch((0.45, 0.35), 8.30, 0.95,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.72, 1.02, "常用频率：LED 1k～5kHz、舵机 50Hz、电机 1～20kHz", fontsize=8.1,
            color=TEXT, fontweight="bold")
    ax.text(0.72, 0.66, "人眼视觉暂留约 20ms——PWM 高于 100Hz 就看不出闪", fontsize=7.9, color=TEXT)

    _save(fig, "esp32-pwm-duty-servo.svg")


# ============================================================
# 8. 接线示意：TB6612 驱动直流电机
#    PWM→PWMA 调速；AIN1/AIN2 决定正转/反转/停止；STBY 拉高才工作；
#    电机电源 VM 必须外接、和开发板只共地不共电（docs/course/l4-peripherals/pwm.mdx:297）
#    示例引脚 AIN1=GPIO5 / AIN2=GPIO6 / STBY=GPIO7（同文件 :300-302）
#    TB6612FNG 是最常用的一款（同文件 :284）
#    L298N 压降 1.8～2V，3.3V 系统一律用 TB6612 或 DRV8833（docs/quickstart/pwm.mdx:194）
#    电机/舵机单独 5V/2A 以上并共地（docs/quickstart/pwm.mdx:137；docs/quickstart/board.mdx:76）
# ============================================================
def esp32_wire_tb6612_motor():
    fig, ax = canvas(13.0, 7.8, 13.4, 8.4)
    title(ax, 0.4, 8.05, "TB6612 驱动直流电机：PWM 调速、两个方向脚、一个总开关")

    board(ax, 0.45, 2.45, 2.90, 4.85, "ESP32-S3")
    for yc, name, col in [(6.50, "GPIO4 PWM", C_DATA), (5.45, "GPIO5 AIN1", YELLOW),
                          (4.40, "GPIO6 AIN2", YELLOW), (3.35, "GPIO7 STBY", YELLOW)]:
        pin_stub(ax, 1.85, yc - 0.22, 1.55, 0.44, name, color=col, fs=7.9)
    pin_stub(ax, 1.85, 2.05, 1.55, 0.44, "GND", color="#d5d8dc", fs=7.9)

    ax.add_patch(FancyBboxPatch((5.95, 3.05), 2.70, 4.05,
                                boxstyle="round,pad=0.06,rounding_size=0.14",
                                facecolor="#eaf2f8", edgecolor=DARK, lw=1.6))
    ax.text(7.30, 6.72, "TB6612FNG", ha="center", fontsize=9.4, fontweight="bold", color=TEXT)
    ax.text(7.30, 6.34, "H 桥功率放大", ha="center", fontsize=7.8, color=LINE)
    for yc, name in [(6.50, "PWMA"), (5.45, "AIN1"), (4.40, "AIN2"), (3.35, "STBY")]:
        ax.text(6.20, yc, name, ha="left", va="center", fontsize=7.9, color=TEXT)
        wire(ax, [(3.40, yc), (5.95, yc)])
    ax.text(6.20, 5.95, "VM", ha="left", va="center", fontsize=7.9, color="#c0392b")
    ax.text(6.20, 3.65, "GND", ha="left", va="center", fontsize=7.9, color=LINE)

    # VM 电源
    ax.add_patch(Rectangle((9.25, 5.60), 1.95, 0.78, facecolor="#fadbd8",
                           edgecolor=DARK, lw=1.4))
    ax.text(10.22, 5.99, "VM 电源 5V/2A", ha="center", va="center", fontsize=7.9,
            color=TEXT, fontweight="bold")
    wire(ax, [(9.25, 5.99), (8.65, 5.99)], color="#c0392b", lw=2.0)


    # 电机
    ax.add_patch(FancyBboxPatch((9.25, 3.20), 1.95, 1.55,
                                boxstyle="round,pad=0.05,rounding_size=0.16",
                                facecolor=GREY, edgecolor=DARK, lw=1.5))
    ax.text(10.22, 3.97, "M", ha="center", va="center", fontsize=12, fontweight="bold",
            color=TEXT)
    wire(ax, [(8.65, 4.35), (9.25, 4.35)])
    wire(ax, [(8.65, 3.55), (9.25, 3.55)])

    # 共地母线
    wire(ax, [(3.40, 2.27), (12.60, 2.27)], color="#5d6d7e", lw=1.7, ls="--")
    wire(ax, [(8.65, 3.65), (8.65, 2.27)], color="#5d6d7e", lw=1.7, ls="--")
    wire(ax, [(10.22, 3.20), (10.22, 2.27)], color="#5d6d7e", lw=1.7, ls="--")
    wire(ax, [(10.22, 5.60), (10.22, 5.20), (11.40, 5.20), (11.40, 2.27)], color="#5d6d7e", lw=1.7, ls="--")
    ax.text(4.05, 1.95, "共地母线：开发板、驱动、电机电源的 GND 全部接在一起——只共地、不共电",
            fontsize=7.7, color="#5d6d7e")

    ax.add_patch(FancyBboxPatch((0.45, 0.35), 12.45, 1.30,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.72, 1.36, "接线规则：PWM→PWMA 调速；AIN1/AIN2 决定正转 / 反转 / 停止；STBY 拉高才工作（总开关）",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.72, 1.00, "电机电源 VM 必须外接，和开发板只共地不共电——启动瞬间的电流冲击会把板子拉复位",
            fontsize=7.9, color=RED)
    ax.text(0.72, 0.65, "别用 L298N：压降 1.8～2V，3.3V 系统下电机只剩 1.5V 左右，基本转不动；用 TB6612 或 DRV8833",
            fontsize=7.9, color=TEXT)

    _save(fig, "esp32-wire-tb6612-motor.svg")


# ============================================================
# 9. 接线示意：板载 WS2812 RGB 灯
#    v1.0 = GPIO48，v1.1 = GPIO38（docs/reference/pinout.mdx:85-86；
#      docs/quickstart/mixly-setup.mdx:162）
#    WS2812 靠特定时序脉冲通信，普通 digitalWrite 点不亮
#      （docs/quickstart/mixly-setup.mdx:139；docs/quickstart/arduino-ide.mdx:64）
#    字节序 NEO_GRB、板载灯数 1（docs/quickstart/mixly-setup.mdx:124,133）
# ============================================================
def esp32_wire_rgb_led():
    fig, ax = canvas(12.2, 6.2, 12.6, 6.8)
    title(ax, 0.4, 6.42, "板载 RGB 灯：一根数据线，但数字输出点不亮它")
    note(ax, 0.4, 6.06, "WS2812 是「可寻址」灯珠：颜色和亮度被编码成一段特定时序的脉冲，不是一个电平", fs=8.2)

    board(ax, 0.45, 1.75, 3.10, 3.95, "ESP32-S3\nDevKitC-1")
    pin_stub(ax, 1.95, 4.55, 1.35, 0.44, "GPIO48", color=C_DATA, fs=8.4)
    pin_stub(ax, 1.95, 3.35, 1.35, 0.44, "GPIO38", color=C_PAD, fs=8.4)
    ax.text(3.05, 4.28, "v1.0 板", fontsize=7.6, color="#1e8449")
    ax.text(3.05, 3.08, "v1.1 板", fontsize=7.6, color="#1e8449")

    ax.add_patch(Circle((8.05, 4.05), 0.85, facecolor="#f9e79f", edgecolor=DARK, lw=1.6))
    ax.text(8.05, 4.05, "RGB\nWS2812", ha="center", va="center", fontsize=8.2,
            color=TEXT, fontweight="bold", linespacing=1.2)
    wire(ax, [(3.30, 4.77), (6.85, 4.77), (6.85, 4.05)], color="#c0392b", lw=2.0)
    wire(ax, [(3.30, 3.57), (5.85, 3.57), (5.85, 3.45), (7.20, 3.45)],
         color="#c0392b", lw=2.0, ls="--")
    ax.text(4.55, 5.05, "数据线（DIN）", fontsize=7.8, color="#c0392b")
    ax.text(4.35, 3.10, "两个批次只差这一根线接哪个脚", fontsize=7.7, color=LINE)

    ax.add_patch(FancyBboxPatch((0.45, 0.35), 11.65, 1.05,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.72, 1.12, "拿不准批次：程序里两个都写上，选一个不亮就换另一个（48 与 38 互换）",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.72, 0.76, "初始化要选对字节序 NEO_GRB（板载灯数 = 1）；亮出绿色或蓝色说明字节序不匹配，换 NEO_RGB 再试",
            fontsize=7.9, color=TEXT)
    ax.text(0.72, 0.48, "最典型的误判：用「数字输出」积木点 GPIO48 怎么做灯都不亮——不是板子坏了，是协议不对",
            fontsize=7.9, color=RED)

    _save(fig, "esp32-wire-rgb-led.svg")


# ============================================================
# 10. GPIO 矩阵：外设信号 ↔ 任意引脚
#     信号路由矩阵（docs/course/l4-peripherals/gpio.mdx:16-31）
#     例：串口想用 17/18 还是 43/44 随意（同文件 :27）
#     UART0 = GPIO43/44（docs/course/l4-peripherals/i2c-spi-uart.mdx:224；
#       docs/reference/pinout.mdx:44-45）
#     I2C 默认 8 / 9（docs/reference/pinout.mdx:27,30,94）
#     SPI 默认 12/11/13/10（docs/reference/pinout.mdx:95）
#     输出侧一个引脚同一时刻只能被一个信号驱动（gpio.mdx:29）
#     代价：路由经过矩阵有几纳秒额外延迟（gpio.mdx:31）
# ============================================================
def esp32_gpio_matrix():
    fig, ax = canvas(12.6, 6.8, 13.0, 7.4)
    title(ax, 0.4, 7.05, "GPIO 矩阵：外设信号不焊死在某个脚上")
    note(ax, 0.4, 6.70, "老 51 单片机「3 号脚天生是串口 TX」；ESP32 把这件事变成了软件里的一行配置", fs=8.2)

    periph = [("UART0 TX", 5.55), ("UART0 RX", 4.90), ("I2C SDA", 4.25),
              ("I2C SCL", 3.60), ("SPI MOSI", 2.95), ("SPI SCK", 2.30)]
    for name, yc in periph:
        ax.add_patch(Rectangle((0.55, yc - 0.23), 2.35, 0.46, facecolor=BLUE,
                               edgecolor=DARK, lw=1.1))
        ax.text(1.72, yc, name, ha="center", va="center", fontsize=8.2,
                color=TEXT, fontweight="bold")
        wire(ax, [(2.90, yc), (4.75, yc)], color=LINE, lw=1.5)

    ax.add_patch(FancyBboxPatch((4.75, 1.75), 2.45, 4.35,
                                boxstyle="round,pad=0.06,rounding_size=0.14",
                                facecolor=ORANGE, edgecolor=DARK, lw=1.6, alpha=0.92))
    ax.text(5.97, 5.78, "GPIO 矩阵", ha="center", fontsize=9.6, fontweight="bold", color=TEXT)
    ax.text(5.97, 2.55, "可编程\n交换机", ha="center", va="center", fontsize=8.2,
            color=TEXT, linespacing=1.3)

    for name, yc in [("GPIO43", 5.55), ("GPIO44", 4.90), ("GPIO8", 4.25),
                     ("GPIO9", 3.60), ("GPIO11", 2.95), ("GPIO12", 2.30)]:
        wire(ax, [(7.20, yc), (8.65, yc)], color=LINE, lw=1.5)
        ax.add_patch(Rectangle((8.65, yc - 0.23), 1.45, 0.46, facecolor=GREEN,
                               edgecolor=DARK, lw=1.1))
        ax.text(9.37, yc, name, ha="center", va="center", fontsize=8.2,
                color=TEXT, fontweight="bold")

    ax.text(0.55, 6.15, "左：外设硬件", fontsize=8.0, color=TEXT)
    ax.text(8.65, 6.15, "右：封装上的物理引脚", fontsize=8.0, color=TEXT)
    ax.text(10.35, 5.40, "示例：UART0 用 43/44，\nI2C 用 8/9，SPI 用 11/12", fontsize=7.8,
            color=LINE, linespacing=1.35, va="top")

    ax.add_patch(FancyBboxPatch((0.45, 0.35), 12.10, 1.20,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.72, 1.36, "输入侧几乎无限制：一个引脚的输入可以同时喂给多个外设", fontsize=8.1,
            color=TEXT, fontweight="bold")
    ax.text(0.72, 1.00, "输出侧有冲突规则：一个引脚同一时刻只能被一个输出信号驱动，两个外设抢同一个脚会打架",
            fontsize=7.9, color=RED)
    ax.text(0.72, 0.66, "代价：路由经过矩阵有几纳秒的额外延迟——对点灯、按键毫无影响", fontsize=7.9, color=LINE)

    _save(fig, "esp32-gpio-matrix.svg")


# ============================================================
# 11. strapping 引脚：复位释放那一瞬间被采样
#     strapping = GPIO0 / GPIO3 / GPIO45 / GPIO46
#       GPIO0  : 0 = 正常启动；1 = 下载模式
#       GPIO3  : JTAG 调试口来源选择
#       GPIO45 : Flash 供电电压选择（3.3V / 1.8V）
#       GPIO46 : 启动模式相关
#       （docs/course/l1-hardware/board.mdx:187-192）
#     采样只发生在复位释放的那一瞬间（毫秒级），之后恢复普通 GPIO（同文件 :181-183）
#     EN 上挂 RC：上电时先让电源稳定一小会儿再放开复位（同文件 :56）
#     排查口诀（同文件 :206）；GPIO46 同样是 strapping（gpio.mdx:46、pinout.mdx:75）
#     S3 无「仅输出脚」（porting.mdx:37），旧说法来自 S2
# ============================================================
def esp32_strapping_boot():
    fig, ax = canvas(12.8, 7.6, 13.2, 8.2)
    title(ax, 0.4, 7.88, "strapping：上电那一瞬间被「偷看」的四个脚")
    note(ax, 0.4, 7.52, "采样只在复位释放的瞬间发生（毫秒级），此前引脚上的电平决定「这次以什么模式启动」", fs=8.2)

    # ---- 上半：四个脚各决定什么 ----
    ax.text(0.50, 7.05, "这四个脚各自决定什么", fontsize=9.2, fontweight="bold", color=TEXT)
    rows = [("GPIO0", "0 = 正常启动；1 = 下载模式", "BOOT 键就接在它上面"),
            ("GPIO3", "JTAG 调试口来源选择", "接外设前想清楚"),
            ("GPIO45", "Flash 供电电压选择（3.3V / 1.8V）", "最危险：拉错轻则开不了机，重则损坏 Flash"),
            ("GPIO46", "启动模式相关", "它同时是 strapping 脚：复位瞬间同样被采样")]
    for i, (pin, what, warn) in enumerate(rows):
        yy = 6.58 - i * 0.48
        ax.add_patch(Rectangle((0.50, yy - 0.20), 1.30, 0.40, facecolor=YELLOW,
                               edgecolor=DARK, lw=1.0))
        ax.text(1.15, yy, pin, ha="center", va="center", fontsize=8.2, color=TEXT,
                fontweight="bold")
        ax.text(1.98, yy, what, fontsize=8.0, va="center", color=TEXT)
        ax.text(7.20, yy, warn, fontsize=7.8, va="center",
                color=RED if pin in ("GPIO45", "GPIO46") else LINE)

    # ---- 中间：EN 波形 ----
    left, right = 1.60, 12.55
    base, hh = 3.35, 0.70
    ax.text(0.50, base + hh / 2, "EN", fontsize=8.6, color=TEXT, ha="center",
            va="center", fontweight="bold")
    ax.text(left - 0.18, base + hh + 0.16, "3.3V", fontsize=7.6, color=LINE, ha="left")
    ax.text(left - 0.18, base - 0.16, "0V", fontsize=7.6, color=LINE, ha="left")

    t_up, t_rel, t_end = left + 0.70, left + 3.30, left + 4.45
    pts = [(left, base), (t_up, base), (t_up, base + hh * 0.50), (t_rel, base + hh * 0.50),
           (t_rel, base + hh), (right, base + hh)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color="#1a5276", lw=2.0)

    ax.add_patch(Rectangle((t_rel, base - 0.34), t_end - t_rel, hh + 0.68,
                           facecolor=YELLOW, edgecolor="#b7950b", lw=1.2, alpha=0.55))
    ax.text((t_rel + t_end) / 2, base + hh + 0.22, "采样窗口", ha="center",
            fontsize=8.2, color="#7d6608", fontweight="bold")
    ax.text((t_rel + t_end) / 2, base - 0.55, "毫秒级", ha="center", fontsize=7.6,
            color="#7d6608")

    ax.annotate("上电", xy=(t_up, base + hh * 0.18), xytext=(t_up + 0.85, base - 0.32),
                fontsize=7.8, color=TEXT, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.1))
    ax.annotate("EN 上的 RC 延时后复位释放", xy=(t_rel, base + hh * 0.74),
                xytext=(t_rel - 1.90, base + hh + 0.42), fontsize=7.8, color=TEXT,
                ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.1))
    ax.annotate("之后恢复普通 GPIO，可以正常读写",
                xy=(t_end + 1.30, base + hh), xytext=(t_end + 1.05, base + hh + 0.42),
                fontsize=7.8, color="#1e8449", ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-|>", color="#1e8449", lw=1.1))

    # ---- 下半：两个说明块 ----
    ax.add_patch(FancyBboxPatch((0.50, 1.30), 12.15, 1.28,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(0.78, 2.30, "排查口诀：「不接外设一切正常，接上外设启动怪异」——先查那个模块的输出脚是不是接在 strapping 脚上",
            fontsize=8.1, color=TEXT, fontweight="bold")
    ax.text(0.78, 1.94, "典型现场：传感器自带上电默认高电平，恰好接在 GPIO0 上，芯片「以为你要下载固件」，正常程序根本不跑",
            fontsize=7.9, color=TEXT)
    ax.text(0.78, 1.58, "后果不对称：采样窗口只有毫秒级，之后这几个脚完全可以当普通 GPIO 用——坑只在开机那一下",
            fontsize=7.9, color=LINE)

    ax.add_patch(FancyBboxPatch((0.50, 0.28), 12.15, 0.88,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.78, 0.96, "要记住的一件事：strapping 不是「不能用的脚」，而是「上电瞬间不能给错电平的脚」",
            fontsize=8.1, color=TEXT, fontweight="bold")
    ax.text(0.78, 0.62, "实际工程做法：外设尽量避开这四个脚；避不开就确认它复位期间的默认电平是安全的（GPIO45 尤其保守）",
            fontsize=7.9, color=TEXT)


    _save(fig, "esp32-strapping-boot.svg")


# ============================================================
# 12. 按键抖动与三种消抖
#     机械触点在闭合瞬间弹跳几十微秒到几十毫秒，抖动段 5~20ms
#       （docs/hardware/esp-basics/09-gpio-input.mdx:83,91）
#     ① 延时消抖 vTaskDelay(20)（同文件 :105,114）
#     ② 状态机消抖：每 10ms 采样、连续 3 次一致才稳定（同文件 :122-127,150）
#     ③ 边沿检测：1→0 下降沿，抖动期间可能产生多个下降沿（同文件 :162,169-170）
#     实践中最常用：边沿检测 + 20ms 延时确认（同文件 :172）
#     按下 = 低电平（同文件 :44-45,63）
# ============================================================
def esp32_button_debounce():
    fig, ax = canvas(12.8, 7.0, 13.2, 7.6)
    title(ax, 0.4, 7.22, "按键抖动：一次按下，程序却可能看到几十次跳变")
    note(ax, 0.4, 6.86, "机械触点在闭合瞬间会弹跳几十微秒到几十毫秒——这是物理问题，不是代码 bug", fs=8.2)

    ax.text(0.45, 6.35, "理想", fontsize=8.4, color=TEXT, fontweight="bold")
    ax.plot([1.35, 4.05, 4.05, 9.85, 9.85, 12.55], [5.95, 5.95, 6.55, 6.55, 5.95, 5.95],
            color=GREEN, lw=2.2)
    ax.plot([1.35, 12.55], [5.95, 5.95], color=LINE, lw=0.8, ls=":")
    ax.plot([1.35, 12.55], [6.55, 6.55], color=LINE, lw=0.8, ls=":")
    ax.text(1.10, 5.95, "1", fontsize=7.6, color=LINE, ha="center", va="center")
    ax.text(1.10, 6.55, "0", fontsize=7.6, color=LINE, ha="center", va="center")

    ax.text(0.45, 4.95, "实际", fontsize=8.4, color=TEXT, fontweight="bold")
    hi, lo = 5.20, 4.45
    pts = [(1.35, hi), (3.90, hi), (3.90, lo)]
    for x, v in [(4.02, hi), (4.12, lo), (4.24, hi), (4.34, lo),
                 (4.46, hi), (4.58, lo), (4.70, hi), (4.82, lo), (4.96, hi),
                 (5.08, lo), (5.24, hi), (5.38, lo), (5.52, lo)]:
        pts += [(x, v)]
    pts += [(9.85, lo)]
    for x, v in [(10.30, hi), (10.42, lo), (10.54, hi), (10.66, lo), (10.80, hi),
                 (10.94, lo), (11.10, hi), (11.30, lo), (11.60, hi)]:
        pts += [(x, v)]
    pts += [(12.55, hi)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=RED, lw=2.0)
    ax.add_patch(Rectangle((3.90, lo - 0.14), 1.62, (hi - lo) + 0.28,
                           facecolor=YELLOW, edgecolor="#b7950b", lw=1.0, alpha=0.45))
    ax.annotate("抖动段 5~20ms", xy=(4.72, hi + 0.12), xytext=(6.60, hi + 0.62),
                fontsize=7.9, color="#7d6608",
                arrowprops=dict(arrowstyle="-|>", color="#b7950b", lw=1.1))
    ax.plot([1.35, 12.55], [hi, hi], color=LINE, lw=0.8, ls=":")
    ax.plot([1.35, 12.55], [lo, lo], color=LINE, lw=0.8, ls=":")
    ax.text(1.10, hi, "1", fontsize=7.6, color=LINE, ha="center", va="center")
    ax.text(1.10, lo, "0", fontsize=7.6, color=LINE, ha="center", va="center")

    ax.text(0.45, 4.00, "三种消抖写法（上拉接法：按下 = 低电平）", fontsize=9.2,
            fontweight="bold", color=TEXT)
    cards = [
        ("① 延时消抖", ["vTaskDelay(20) 等抖动过去", "再读一次确认"],
         "简单；但会阻塞当前任务 20ms", YELLOW),
        ("② 状态机消抖", ["每 10ms 采样一次", "连续 3 次一致才算稳定"],
         "推荐：不阻塞，只在真变化时返回一次", GREEN),
        ("③ 边沿检测", ["只在 1→0 的下降沿触发一次", "toggle 一次状态"],
         "最省事；但抖动期间可能产生多个下降沿", ORANGE),
    ]
    for i, (k, mids, tail, col) in enumerate(cards):
        x0 = 0.45 + i * 4.22
        ax.add_patch(FancyBboxPatch((x0, 2.25), 4.00, 1.55,
                                    boxstyle="round,pad=0.07,rounding_size=0.12",
                                    facecolor=col, edgecolor=DARK, lw=1.3, alpha=0.55))
        ax.text(x0 + 2.00, 3.55, k, ha="center", fontsize=8.8, color=TEXT, fontweight="bold")
        ax.text(x0 + 2.00, 3.05, mids[0] + "\n" + mids[1], ha="center", va="center",
                fontsize=7.8, color=TEXT, linespacing=1.35)
        ax.text(x0 + 2.00, 2.55, tail, ha="center", va="center", fontsize=7.6,
                color="#7b241c")

    ax.add_patch(FancyBboxPatch((0.45, 0.40), 12.10, 1.45,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.72, 1.62, "实践中最常用：边沿检测 + 20ms 延时确认；中断里只投递事件，消抖放到任务里做",
            fontsize=8.2, color=TEXT, fontweight="bold")
    ax.text(0.72, 1.24, "不消抖的后果很具体：按一下灯切换了 7 次，看起来像「没反应」或者「随机」", fontsize=7.9,
            color=TEXT)
    ax.text(0.72, 0.88, "还有一种反直觉的坑：接法是上拉时「按下」读到的是 0，判断条件写成 == 1 就永远不触发",
            fontsize=7.9, color=LINE)

    _save(fig, "esp32-button-debounce.svg")




# ============================================================
# 13. 内存预算：200~300KB 的堆能装下什么
#     IRAM 约 200KB / DRAM 约 300KB / RTC 约 8KB / PSRAM 2~8MB / Flash 4~16MB
#       （docs/hardware/esp-basics/29-memory.mdx:19-23）
#     WiFi 启动后堆减少 50~80KB；BLE 约 50~70KB；HTTPS 请求 40~60KB；
#     单次 malloc 上限约 100~160KB（连续块）（同文件 :88-94）
#     PSRAM 适合图像/音频/字库/大 JSON，不适合任务栈（同文件 :169-175）
#     N16R8 = 16MB Flash + 8MB PSRAM（docs/reference/pinout.mdx:120；
#       docs/hardware/esp-basics/29-memory.mdx:23）
#     malloc(150*1024) 可能失败（同文件 :99）
# ============================================================
def esp32_memory_budget():
    fig, ax = canvas(12.8, 7.4, 13.2, 8.0)
    title(ax, 0.4, 7.62, "内存预算：200~300KB 的堆能装下什么，装不下什么")
    note(ax, 0.4, 7.26, "在电脑上随手 new 一个 10MB 数组，在这里直接失败——先算账，再动手", fs=8.2)

    ax.text(0.45, 6.75, "可用堆 ≈ 200~300KB（WiFi 启动后还要再少 50~80KB）", fontsize=8.8,
            color=TEXT, fontweight="bold")
    bx, by, bw, bh = 0.45, 5.90, 11.55, 0.55
    ax.add_patch(Rectangle((bx, by), bw, bh, facecolor="#eaf2f8", edgecolor=DARK, lw=1.4))
    segs = [("WiFi 启动 50~80KB", 70, "#e8b4b8"), ("BLE 协议栈 50~70KB", 60, "#d2b4de"),
            ("HTTPS 请求 40~60KB", 50, "#f5cba7"),
            ("单次 malloc 上限约 100~160KB", 130, "#7fb3d5")]
    x = bx
    for name, kb, col in segs:
        w = bw * kb / 310.0
        ax.add_patch(Rectangle((x, by), w, bh, facecolor=col, edgecolor=DARK, lw=0.9))
        ax.text(x + w / 2, by + bh / 2, name, ha="center", va="center", fontsize=7.3,
                color=TEXT)
        x += w
    ax.text(bx + 0.10, by - 0.32, "每一块都是同一份 300KB 里的开销——它们会叠加，不是各自独立",
            fontsize=7.8, color=LINE)

    ax.text(0.45, 5.05, "哪些东西要你真金白银掏内存", fontsize=9.2, fontweight="bold", color=TEXT)
    rows = [("单个任务栈", "建议 2~8 KB", "超了就是栈溢出，直接崩"),
            ("单次 malloc", "约 100~160 KB（连续块）", "总量够但没有连续的 150KB 一样失败"),
            ("HTTPS 请求", "40~60 KB", "TLS 握手很吃内存"),
            ("WiFi 启动后", "堆减少 50~80 KB", "同一份代码联网前后表现不同"),
            ("BLE 协议栈", "约 50~70 KB", "WiFi + BLE 同时开要提前留量")]
    for i, (k, v, why) in enumerate(rows):
        yy = 4.60 - i * 0.46
        ax.text(0.62, yy, k, fontsize=8.2, color=TEXT, fontweight="bold")
        ax.text(2.45, yy, v, fontsize=8.2, color=RED)
        ax.text(6.55, yy, why, fontsize=7.9, color=LINE)

    ax.add_patch(FancyBboxPatch((0.45, 0.52), 5.95, 1.55,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.72, 1.83, "PSRAM 适合「大而慢」", fontsize=8.4, color=TEXT, fontweight="bold")
    ax.text(0.72, 1.45, "N16R8 = 16MB Flash + 8MB PSRAM", fontsize=8.0, color=TEXT)
    ax.text(0.72, 1.09, "适合：图像帧缓冲 / 音频缓冲 / 字库 / 大 JSON", fontsize=8.0,
            color="#1e8449")
    ax.text(0.72, 0.75, "不适合：任务栈——太慢，不要放进来", fontsize=8.0, color=RED)

    ax.add_patch(FancyBboxPatch((6.65, 0.52), 5.95, 1.55,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#fdf2e9", edgecolor="#b7950b", lw=1.2))
    ax.text(6.92, 1.83, "碎片化：总量够 ≠ 能分配出来", fontsize=8.4, color=TEXT,
            fontweight="bold")
    ax.text(6.92, 1.45, "malloc(150 * 1024) 可能失败，而一堆小块都能成功", fontsize=8.0,
            color=TEXT)
    ax.text(6.92, 1.09, "大缓冲区一次分配好、用完就放，别反复 malloc/free", fontsize=8.0,
            color=TEXT)
    ax.text(6.92, 0.75, "看泄漏趋势用 esp_get_minimum_free_heap_size()", fontsize=8.0,
            color=LINE)

    ax.text(0.60, 0.20, "片内：IRAM 约 200KB、DRAM 约 300KB、RTC 约 8KB；片外 Flash 4~16MB、PSRAM 2~8MB",
            fontsize=7.9, color=LINE)

    _save(fig, "esp32-memory-budget.svg")


# ============================================================
# 14. NVS 布局：24KB 分区里怎么放键值对
#     默认 NVS 分区 0x6000 = 24 KB（docs/hardware/esp-basics/22-nvs.mdx:39,48,53；
#       docs/course/l2-programming-model/partition-ota.mdx:44,68）
#     0x0 起是 bootloader、0x8000 是分区表、0x9000 起才能放自己的分区
#       （docs/course/l2-programming-model/partition-ota.mdx:63-65）
#     命名空间名 / 键名最长 15 字节（docs/hardware/esp-basics/22-nvs.mdx:151）
#     单值最大 97% 分区大小，默认分区下大约 4 KB（同文件 :271）
#     不适合大数据 / 不适合高频写 / 写入几十毫秒级（同文件 :272-274）
#     掉电安全：有磨损均衡和电源丢失保护（同文件 :41）
#     写满返回 ESP_ERR_NVS_NO_FREE_PAGES（同文件 :80）
# ============================================================
def esp32_nvs_layout():
    fig, ax = canvas(12.8, 7.8, 13.2, 8.6)
    title(ax, 0.4, 8.22, "NVS 布局：24KB 的分区里，命名空间装着键值对")
    note(ax, 0.4, 7.86, "NVS 是 Flash 上的一个 data 分区，掉电保留、有磨损均衡——但它是「小本子」，不是硬盘", fs=8.2)

    ax.text(0.45, 7.35, "16MB Flash 里的位置（切片示意，不按真实比例）", fontsize=8.4,
            color=TEXT, fontweight="bold")
    bx, by, bh = 0.45, 6.55, 0.58
    slices = [("bootloader\n0x0 起", 1.70, "#d5d8dc"), ("分区表\n0x8000", 1.35, "#d5dbdb"),
              ("nvs\n0x9000 · 24KB", 2.40, YELLOW), ("phy_init", 1.15, "#eaf2f8"),
              ("factory / app", 2.45, BLUE), ("spiffs 等", 1.55, GREEN),
              ("…", 1.60, "#eaeded")]
    x = bx
    for name, w, col in slices:
        ax.add_patch(Rectangle((x, by), w, bh, facecolor=col, edgecolor=DARK, lw=1.1))
        ax.text(x + w / 2, by + bh / 2, name, ha="center", va="center", fontsize=7.5,
                color=TEXT, linespacing=1.2)
        x += w
    ax.annotate("0x9000 起才轮得到你的分区",
                xy=(bx + 1.70 + 1.35 + 1.20, by - 0.05),
                xytext=(bx + 1.70 + 1.35 + 1.20, by - 0.62),
                fontsize=7.8, color="#7d6608", ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#b7950b", lw=1.3))

    ax.text(0.45, 5.35, "分区内部：命名空间（相当于文件夹）→ 键 → 值", fontsize=9.2,
            fontweight="bold", color=TEXT)
    ns = [("wifi_cfg", [("ssid", "字符串"), ("pass", "字符串")]),
          ("dev_state", [("boot_cnt", "整数"), ("last_ver", "整数")]),
          ("calib", [("offset", "二进制块")])]
    for i, (nsname, kvs) in enumerate(ns):
        x0 = 0.55 + i * 4.15
        ax.add_patch(FancyBboxPatch((x0, 3.70), 3.85, 1.38,
                                    boxstyle="round,pad=0.06,rounding_size=0.12",
                                    facecolor="#eaf2f8", edgecolor=DARK, lw=1.3))
        ax.text(x0 + 1.92, 4.80, "命名空间 " + nsname, ha="center", fontsize=8.4,
                color=TEXT, fontweight="bold")
        for j, (k, t) in enumerate(kvs):
            yy = 4.42 - j * 0.38
            ax.text(x0 + 0.22, yy, "键 " + k, fontsize=7.8, color=TEXT)
            ax.text(x0 + 2.10, yy, t, fontsize=7.8, color="#1e8449")

    rows = [("分区大小", "默认 24 KB（0x6000）", "由分区表决定"),
            ("命名空间名", "最长 15 字节", "超了直接失败"),
            ("键名", "最长 15 字节", "用短名"),
            ("单个值", "最大 97% 分区大小 ≈ 4 KB", "存图片、日志请用文件系统"),
            ("写入速度", "几十毫秒级", "不适合高频写，Flash 寿命有限")]
    for i, (k, v, why) in enumerate(rows):
        yy = 3.28 - i * 0.40
        ax.text(0.62, yy, k, fontsize=8.2, color=TEXT, fontweight="bold")
        ax.text(2.25, yy, v, fontsize=8.2, color=RED)
        ax.text(6.30, yy, why, fontsize=7.9, color=LINE)

    ax.add_patch(FancyBboxPatch((0.45, 0.25), 12.20, 1.05,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#eafaf1", edgecolor="#1e8449", lw=1.2))
    ax.text(0.72, 1.24, "掉电安全来自磨损均衡 + 电源丢失保护：写一半断电，旧值还在——但它只适合「少量、低频、必须记住」的配置",
            fontsize=8.0, color=TEXT)
    ax.text(0.72, 0.86, "分区写满会返回 ESP_ERR_NVS_NO_FREE_PAGES：要么精简键值，要么在分区表里把 nvs 分区调大",
            fontsize=7.9, color=TEXT)
    ax.text(0.72, 0.52, "别把 NVS 当文件系统用：存图片、日志、大批量数据请走 spiffs / LittleFS",
            fontsize=7.9, color=LINE)

    _save(fig, "esp32-nvs-layout.svg")


if __name__ == "__main__":
    esp32_wire_button_led()
    esp32_pin_capability_map()
    esp32_wire_i2c_oled()
    esp32_i2c_timing()
    esp32_wire_adc_pot()
    esp32_adc_sample_timing()
    esp32_pwm_duty_servo()
    esp32_wire_tb6612_motor()
    esp32_wire_rgb_led()
    esp32_gpio_matrix()
    esp32_strapping_boot()
    esp32_button_debounce()
    esp32_memory_budget()
    esp32_nvs_layout()
    print("done")


