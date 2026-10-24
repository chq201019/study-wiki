import io, os

ITEMS = [
    ("docs/software/c/makefile.mdx", "## 目标、依赖、命令",
     "c-makefile-graph.svg",
     "Make 依赖图：app 依赖 main.o/util.o/Makefile，.o 依赖 .c，头文件依赖需要 -MMD 自动生成"),
    ("docs/software/python/testing.mdx", "## fixture：准备与清理",
     "py-pytest-scope.svg",
     "pytest fixture 四种作用域：function 每个测试一次、class/module/session 逐级放大；放大能提速但有状态污染风险"),
    ("docs/hardware/linux/git.mdx", "## 引用（ref）：分支和标签的真相",
     "git-branches.svg",
     "Git 分支本质：main 和 feature 只是存着 commit SHA 的文件，HEAD 指向其中一个；切换分支只改一行"),
    ("docs/software/c/preprocessor.mdx", "## 从源码到可执行文件",
     "c-preprocess-flow.svg",
     "C 预处理流程：10 行源文件经 include 递归展开与宏替换后变成约 1750 行的 .i 文件"),
    ("docs/chips/stm32/dma-deep.mdx", "## 优先级与仲裁",
     "stm32-dma-double-buffer.svg",
     "DMA 双缓冲时序：DMA 填前半时 CPU 处理后半，靠半传输与传输完成两个中断交替驱动"),
    ("docs/chips/stm32/performance.mdx", "## Flash 等待周期与预取",
     "stm32-flash-wait.svg",
     "STM32 Flash 等待周期与预取缓冲：72MHz 需 2 个等待周期，开启预取后顺序代码速度提升接近一倍"),
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
        print("ANCHOR MISS", path, "|", anchor); continue
    if img in chr(10).join(lines):
        print("EXISTS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path); ok += 1
print("inserted", ok, "/", len(ITEMS))