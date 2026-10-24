"""把第六批示意图插入对应课程页。"""
import io
import os

ITEMS = [
    ("docs/software/python/datatypes-01.mdx",
     "## 3. 深浅拷贝：嵌套结构的头号坑",
     "python-copy-depth.svg",
     "浅拷贝与深拷贝对比：浅拷贝只新建外层容器，内层仍指向原对象；深拷贝递归复制成全新对象"),

    ("docs/hardware/esp-basics/25-ota.mdx",
     "## 核心机制：双分区（A/B 分区）",
     "esp32-ota-partition.svg",
     "ESP32 OTA 双分区三阶段：正常运行 ota_0、下载写入 ota_1、改 otadata 指向 ota_1 后重启，失败可回滚"),

    ("docs/hardware/linux/sysprog-03.mdx",
     "### 4.4 epoll：真正的 O(就绪数)",
     "linux-epoll.svg",
     "select / poll / epoll 监听大量 fd 的差别：前两者每次全量扫描，epoll 靠回调把就绪 fd 放进链表"),

    ("docs/hardware/linux/process-02.mdx",
     "### 3.2 fork 与写时复制 COW",
     "linux-fork-cow.svg",
     "fork 与写时复制：fork 后父子指向同一物理页，子进程写入时才真正复制该页"),

    ("docs/software/cpp/classes-01.mdx",
     "### 成员与基类的构造顺序",
     "cpp-ctor-dtor-order.svg",
     "C++ 构造与析构顺序相反：构造是基类→成员→函数体，析构是函数体→成员逆序→基类"),

    ("docs/hardware/linux/process-01.mdx",
     "### 1.2 每个进程拥有的资源",
     "linux-virtual-memory.svg",
     "虚拟内存与页表：两个进程的同一虚拟地址映射到不同物理页，附虚拟地址空间布局"),
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
