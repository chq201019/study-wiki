import io, os

ITEMS = [
    ("docs/software/python/datatypes-01.mdx", "### 结构",
     "py-dict-hashtable.svg",
     "Python dict 内部结构：索引数组存 entries 下标，entries 数组按插入顺序排列，冲突用开放寻址探测"),
    ("docs/software/python-basics/22-inherit.mdx", "## 多继承与 MRO",
     "py-mro.svg",
     "Python MRO：菱形继承下 C3 线性化得到的查找顺序 C -> A -> B -> object"),
    ("docs/software/c-basics/23-enum-union.mdx", "## union：共享内存",
     "c-enum-union.svg",
     "enum / union / struct 三种聚合的内存布局对比，struct 有填充、union 成员重叠、enum 就是整数"),
    ("docs/software/python-basics/20-exceptions.mdx", "## 异常继承树",
     "py-exception-tree.svg",
     "Python 异常继承树：BaseException 下分 SystemExit/KeyboardInterrupt/Exception 三支"),
    ("docs/software/cpp-basics/09-operator.mdx", "## 重载的规则",
     "cpp-operator-resolution.svg",
     "运算符重载的解析四步：收集候选、模板推导、可行函数、最佳匹配"),
    ("docs/hardware/linux/containers.mdx", "## 容器的三大支柱",
     "linux-container-isolation.svg",
     "容器隔离三层：namespace 管看得见什么、cgroup 管能用多少、overlayfs 管文件从哪来"),
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
        print("ANCHOR MISS", path, "|", anchor); continue
    if img in chr(10).join(lines):
        print("EXISTS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path)