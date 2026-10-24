import io
BT = chr(96)
FIX = [
    ("docs/chips/stm32/interrupt-deep.mdx", "## 优先级：4 位，16 级",
     "stm32-nvic-priority.svg",
     "NVIC 优先级分组：4 位如何在五种分组下切成抢占位与子优先级位，Group 4 为 16 级抢占"),
    ("docs/software/c/dynamic-memory.mdx", "## " + BT + "malloc" + BT + " 到底做了什么",
     "c-malloc-layout.svg",
     "malloc 内存块布局：块头元数据 + 用户数据区 + 对齐填充，返回值跳过块头，所以小分配开销远大于请求"),
]
for path, anchor, img, alt in FIX:
    lines = io.open(path, encoding="utf-8").read().split(chr(10))
    idx = None
    for i, l in enumerate(lines):
        if l.strip() == anchor.strip():
            idx = i
            break
    if idx is None:
        print("NOT FOUND", path, anchor)
        continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path)