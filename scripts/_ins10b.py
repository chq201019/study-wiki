import io
BT = chr(96)
FIX = [
    ("docs/software/python-basics/22-inherit.mdx", "## 多态：同一个调用，不同行为",
     "py-mro.svg",
     "Python MRO：菱形继承下 C3 线性化得到的查找顺序 C -> A -> B -> object，super() 就是沿 MRO 往后找"),
    ("docs/software/c-basics/23-enum-union.mdx", "## union：所有成员共享同一块内存",
     "c-enum-union.svg",
     "enum / union / struct 三种聚合的内存布局对比：struct 有对齐填充、union 成员重叠共用、enum 本质是整数"),
    ("docs/software/python-basics/20-exceptions.mdx", "## 捕获多种异常",
     "py-exception-tree.svg",
     "Python 异常继承树：BaseException 下分 SystemExit / KeyboardInterrupt / Exception 三支，except Exception 抓不到前两支"),
    ("docs/software/cpp-basics/09-operator.mdx", "## 基本写法",
     "cpp-operator-resolution.svg",
     "运算符重载的解析四步：收集候选、模板推导、筛出可行函数、选最佳匹配；同时提供成员与非成员版本会导致二义性"),
    ("docs/hardware/linux/containers.mdx", "## 七种 namespace",
     "linux-container-isolation.svg",
     "容器隔离三层：namespace 决定看得见什么、cgroup 决定能用多少、overlayfs 决定文件从哪来；容器共享宿主内核而非独立内核"),
]

for path, anchor, img, alt in FIX:
    lines = io.open(path, encoding="utf-8").read().split(chr(10))
    idx = None
    for i, l in enumerate(lines):
        if l.strip() == anchor.strip():
            idx = i; break
    if idx is None:
        print("STILL MISS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path)