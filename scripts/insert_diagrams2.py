"""把第四批示意图插入对应课程页。"""
import io
import os

ITEMS = [
    ("docs/software/c-basics/03-compile.mdx",
     "## 一条命令 = 四个阶段",
     "c-compile-stages.svg",
     "C 编译四阶段：hello.c 经预处理得 .i、编译得 .s、汇编得 .o、链接得可执行文件，含实测体积与各阶段报错类型"),

    ("docs/software/c-basics/15-functions.mdx",
     "## 调用函数",
     "c-stack-frame.svg",
     "函数调用时的栈帧布局：调用者栈帧、参数、返回地址、保存的 rbp、局部变量，以及 rsp/rbp 的位置"),

    ("docs/software/cpp-basics/16-move.mdx",
     "## 为什么需要移动",
     "cpp-move-semantics.svg",
     "移动语义对比深拷贝：拷贝要分配新内存并复制全部数据，移动只交换指针，代价是源对象被置空"),

    ("docs/hardware/linux-basics/10-process.mdx",
     "## 进程是什么",
     "linux-process-states.svg",
     "Linux 进程状态机：R/S/D/T/Z 五种状态及其转换条件，对应 ps 命令 STAT 列的字母"),

    ("docs/hardware/linux/sysprog-02.mdx",
     "### 2.1 文件描述符 fd 的本质",
     "linux-fd-table.svg",
     "文件描述符的三层结构：进程 fd 表 → 系统打开文件表（offset）→ inode，以及 dup2 如何实现 shell 重定向"),

    ("docs/hardware/esp-basics/29-memory.mdx",
     "## ESP32 的内存地图",
     "esp32-memory-map.svg",
     "ESP32 内存分布：片内 IRAM/DRAM/RTC 内存与片外 Flash/PSRAM 的容量、用途和访问速度差异"),
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
