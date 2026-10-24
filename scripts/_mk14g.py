import io
p = "scripts/gen_diagrams14.py"
t = io.open(p, encoding="utf-8").read()

start = t.index("def stm32_deadtime():")
end = t.index("def shell_pipeline():")

new_fn = '''def stm32_deadtime():
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


'''

t = t[:start] + new_fn + t[end:]
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("rewrote deadtime")
