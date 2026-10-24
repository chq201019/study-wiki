import io, os

ITEMS = [
    ("docs/software/python/iterators.mdx", "## 三个概念别混",
     "py-iterator-protocol.svg",
     "可迭代对象与迭代器的区别：前者每次 iter() 产生新迭代器可反复遍历，后者只能一次；右侧是 next() 的返回序列"),
    ("docs/software/cpp/templates.mdx", "## 函数模板",
     "cpp-template-instantiation.svg",
     "模板实例化：max<T> 是图纸，编译器为 int/double/char 各生成一份独立机器码"),
    ("docs/hardware/linux/security.mdx", "## 清单：从高到低",
     "linux-security-boundary.svg",
     "安全加固的五层攻击面收窄：公网→防火墙→SSH→服务→数据，以及六个最常见错误"),
    ("docs/hardware/esp-basics/31-lowpower.mdx", "## 五种功耗模式",
     "esp32-sleep-current.svg",
     "ESP32 一次唤醒周期的电流曲线：唤醒峰值 40mA、工作几百 ms、深度睡眠 10~150µA"),
    ("docs/chips/stm32/timer-advanced.mdx", "## 互补输出与死区时间",
     "stm32-deadtime.svg",
     "互补 PWM 与死区：无死区时上下管导通区重叠会短路，加死区后两管都为低"),
    ("docs/hardware/linux/shell-tools.mdx", "## 进程替换",
     "linux-shell-pipeline.svg",
     "Shell 管道的三个进程与两个内核缓冲区，以及 pipefail/缓冲/子 shell 三个坑"),
]

ok = 0
for path, anchor, img, alt in ITEMS:
    if not os.path.exists(path):
        print("MISSING", path); continue
    lines = io.open(path, encoding="utf-8").read().split(chr(10))
    idx = None
    for i, l in enumerate(lines):
        if l.strip() == anchor.strip():
            idx = i; break
    if idx is None:
        print("ANCHOR MISS", path); continue
    if img in chr(10).join(lines):
        print("EXISTS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path); ok += 1
print("inserted", ok, "/", len(ITEMS))