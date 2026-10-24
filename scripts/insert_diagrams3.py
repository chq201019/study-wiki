"""把第五批示意图插入对应课程页。"""
import io
import os

ITEMS = [
    ("docs/hardware/linux-basics/14-network.mdx",
     "## 网络故障排查流程",
     "net-tcp-handshake.svg",
     "TCP 三次握手与四次挥手：SYN/SYN+ACK/ACK 建立连接，FIN/ACK/FIN/ACK 双向关闭，以及为什么是 3 和 4"),

    ("docs/software/python/concurrency-01.mdx",
     "## 1. GIL 是什么",
     "python-gil.svg",
     "GIL 对两种负载的影响：CPU 密集时线程轮流用 CPU（并行度 1），IO 密集时等待会释放 GIL（并行度 2）"),

    ("docs/software/cpp/stl-containers-01.mdx",
     "### 扩容策略：实测增长倍数",
     "cpp-vector-growth.svg",
     "vector 扩容导致迭代器失效：capacity 满后申请新内存并搬移元素，旧地址上的迭代器/引用/指针全部悬空"),

    ("docs/software/python/adv-02-generator.mdx",
     "### 原理",
     "python-generator.svg",
     "生成器执行流程：yield 处暂停并保留现场，每次 next 从上次暂停点继续，函数结束时抛 StopIteration"),

    ("docs/software/cpp-basics/24-build.mdx",
     "## C++ 特有第二点：ODR 规则",
     "cpp-odr.svg",
     "声明与定义的区别及能否放头文件：普通函数定义不能进头文件，inline/模板/类定义可以；ODR 违反的两种典型报错"),

    ("docs/hardware/stm-basics/07-understand-code.mdx",
     "## 逐行拆解",
     "stm32-init-flow.svg",
     "STM32 上电流程：启动文件做栈指针/段拷贝/bss 清零后跳 main，main 里依次 HAL_Init、SystemClock_Config、MX_xxx_Init、while(1)"),
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

        lines[idx + 1:idx + 1] = ["", f"![{alt}](/img/diagrams/{img})", ""]
        io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        print("已插入:", path, "<-", img)


if __name__ == "__main__":
    main()
