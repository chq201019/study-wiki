"""全站扫描 MDX frontmatter 的危险写法。

Docusaurus 用 YAML 解析 frontmatter，以下写法会导致构建失败或值被截断：

1. description: #xxx      —— # 被当成注释，值变空
2. description: a << b    —— 裸 < > 未加引号，MDX 会当 JSX 解析
3. 值里含 ": " 而未加引号 —— YAML 会当成新的键

用法:
    python scripts/check_frontmatter.py
"""
import io
import re
import glob

KEY_RE = re.compile(r"^([a-z_]+):\s*(.*)$")


def check_value(key, value):
    """返回问题描述，没问题返回 None。"""
    if not value:
        return None
    if value[0] in ("'", '"'):
        return None                      # 已加引号，安全

    if value.startswith("#"):
        return "# 开头会被 YAML 当注释，值变空"

    if "<" in value or ">" in value:
        return "含 < > 会被 MDX 当 JSX 解析"

    if ": " in value:
        return '含 ": " 可能被 YAML 当新键'

    return None


def main():
    problems = 0
    total = 0

    for path in sorted(glob.glob("docs/**/*.mdx", recursive=True)):
        total += 1

        raw = open(path, "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            print(f"{path}\n    文件开头有 UTF-8 BOM，会导致 frontmatter 解析失败")
            problems += 1
            raw = raw[3:]

        text = raw.decode("utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            print(f"{path}: 没有 frontmatter")
            problems += 1
            continue

        for line in m.group(1).split("\n"):
            km = KEY_RE.match(line)
            if not km:
                continue
            key, value = km.group(1), km.group(2).strip()
            issue = check_value(key, value)
            if issue:
                problems += 1
                print(f"{path}\n    {key}: {issue}\n    值: {value[:70]}")

    print(f"\n扫描 {total} 个文件，{problems} 处问题")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
