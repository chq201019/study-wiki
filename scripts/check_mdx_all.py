"""全站检查 MDX admonition（:::）开闭配对与嵌套。

Docusaurus 对未闭合的 ::: 不会报错，但会把后续大量内容吞进提示框，
渲染结果严重错乱——肉眼很难发现，必须靠程序检查。

用法:
    python scripts/check_mdx_all.py

输出：有问题的文件与行号；全部正常时打印 0 个文件有问题。
"""
import io
import re
import glob

FENCE = "`" * 3
OPEN_RE = re.compile(r"^:::[a-z]+(\[.*\])?\s*$")


def check(path):
    lines = io.open(path, encoding="utf-8").read().split("\n")
    depth = 0
    bad = []
    infence = False

    for i, line in enumerate(lines, 1):
        s = line.strip()

        # 代码块内的 ::: 不算
        if s.startswith(FENCE):
            infence = not infence
            continue
        if infence:
            continue

        if OPEN_RE.match(s):
            depth += 1
            if depth > 1:
                bad.append((i, s[:48]))
        elif s == ":::":
            depth -= 1
            if depth < 0:
                bad.append((i, "多余的闭合"))
                depth = 0

    return depth, bad


def main():
    problems = 0
    total = 0
    for p in sorted(glob.glob("docs/**/*.mdx", recursive=True)):
        total += 1
        d, b = check(p)
        if d != 0 or b:
            problems += 1
            print(f"{p}  depth={d}")
            for ln, s in b[:5]:
                print(f"   行{ln}: {s}")
    print(f"\n扫描 {total} 个文件，{problems} 个有问题")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
