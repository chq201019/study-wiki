import io, os, glob

ITEMS = [
    ("docs/chips/stm32/interrupt-deep.mdx", "## 抢占优先级 vs 子优先级",
     "stm32-nvic-priority.svg",
     "NVIC 优先级分组：4 位如何在五种分组下切成抢占位与子优先级位，Group 4 为 16 级抢占"),
    ("docs/chips/stm32/timer-advanced.mdx", "## 时基计算：先算对再谈别的",
     "stm32-timer-base.svg",
     "定时器时基链：时钟经 PSC 分频到计数频率，CNT 计数到 ARR 归零，更新频率为两者乘积的倒数"),
    ("docs/software/c/dynamic-memory.mdx", "## malloc 到底做了什么",
     "c-malloc-layout.svg",
     "malloc 内存块布局：块头元数据 + 用户数据区 + 对齐填充，返回值跳过块头，所以小分配开销远大于请求"),
    ("docs/hardware/linux/ebpf.mdx", "## 它解决了什么问题",
     "linux-ebpf-hooks.svg",
     "eBPF 挂载点分布：从系统调用入口到 VFS、文件系统、块设备各层，对应 tracepoint/kprobe/kretprobe"),
    ("docs/hardware/esp-basics/35-adc-esp.mdx", "## WiFi 干扰：这是真实存在的严重问题",
     "esp32-adc-wifi.svg",
     "ESP32 ADC2 与 WiFi 共用硬件：WiFi 开启时 ADC2 不可用，ADC1 不受影响"),
    ("docs/software/cpp/raii-extended.mdx", "## RAII 只有两条规则",
     "cpp-raii-exception.svg",
     "RAII 在异常路径下的保证：栈展开时析构仍会被调用，所以手写 lock/unlock 在提前 return 和抛异常时都会漏"),
]

for path, anchor, img, alt in ITEMS:
    if not os.path.exists(path):
        print("MISSING", path); continue
    lines = io.open(path, encoding="utf-8").read().split(chr(10))
    idx = None
    for i, l in enumerate(lines):
        if l.strip() == anchor.strip():
            idx = i; break
    if idx is None:
        print("ANCHOR NOT FOUND", path, "->", anchor); continue
    body = chr(10).join(lines)
    if img in body:
        print("EXISTS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path, "<-", img)
