"""把新生成的示意图插入对应课程页。

每个条目：(文件, 锚点标题行, 图片文件名, alt 文本)
在锚点标题行之后插入图片，紧跟标题、正文之前。
"""
import io
import os

ITEMS = [
    ("docs/hardware/stm-basics/10-clock.mdx",
     '## 为什么需要"时钟树"',
     "stm32-clock-tree.svg",
     "STM32F103 时钟树：8MHz 外部晶振经 PLL 倍频到 72MHz，再分频给 AHB/APB1/APB2 及各外设"),

    ("docs/hardware/linux/boot-01.mdx",
     "## 1. 完整链路总览",
     "linux-boot-chain.svg",
     "Linux 启动链：BootROM → SPL/U-Boot → Kernel → init(PID 1) → 用户进程，含各阶段存放位置与常见失败点"),

    ("docs/software/python/datatypes-01.mdx",
     "## 1. list：CPython 的动态数组",
     "python-list-growth.svg",
     "Python list 内部结构：list 对象 → ob_item 指针 → 已分配槽位数组，len 与实际容量的区别"),

    ("docs/hardware/stm-basics/16-spi.mdx",
     "## SPI 回顾",
     "i2c-vs-spi.svg",
     "I2C 与 SPI 对比：I2C 两根线靠地址多设备，SPI 四根线加片选换带宽"),

    ("docs/software/python/adv-01-decorator.mdx",
     "## 1. 装饰器：接收函数、返回函数",
     "python-decorator.svg",
     "装饰器原理：@timer 接收原函数并返回 wrapper，调用时每次都经过 wrapper"),

    ("docs/hardware/stm-basics/18-freertos.mdx",
     "## RTOS 带来什么",
     "freertos-states.svg",
     "FreeRTOS 任务状态机：Running / Ready / Blocked / Suspended 的转换条件"),
]


def main():
    for path, anchor, img, alt in ITEMS:
        if not os.path.exists(path):
            print("文件不存在:", path)
            continue
        lines = io.open(path, encoding="utf-8").read().split("\n")

        idx = None
        for i, line in enumerate(lines):
            if line.strip() == anchor.strip():
                idx = i
                break
        if idx is None:
            print("锚点未找到:", path, "->", anchor)
            continue

        if img in "\n".join(lines):
            print("已存在，跳过:", path)
            continue

        snippet = ["", f"![{alt}](/img/diagrams/{img})", ""]
        lines[idx + 1:idx + 1] = snippet

        io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        print("已插入:", path, "<-", img)


if __name__ == "__main__":
    main()
