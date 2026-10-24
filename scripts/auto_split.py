"""自动把过长 MDX 按标题边界拆成 150~300 行的小页。

安全约束（缺一不可）：
1. 只在代码块之外断开
2. 只在 admonition（:::）之外断开
3. 优先按 ## 断；单节过大时退到 ### 断
4. 原文件改写为导读页，id 不变，既有 URL 与外部链接继续有效

用法:
    python scripts/auto_split.py <文件> [--target 250] [--max 320] [--dry]
"""
import io
import os
import re
import sys

OPEN_RE = re.compile(r"^:::[a-z]+(\[.*\])?\s*$")



def clean_title(raw):
    """去掉标题开头的编号（如 '6. '、'3 '、'二、'），保留实质内容。"""
    s = raw.strip()
    s = re.sub(r"^[0-9]+(\.[0-9]+)*[\.、\s]+", "", s)
    s = re.sub(r"^[一二三四五六七八九十]+、", "", s)
    return s.strip() or raw.strip()


def read(path):
    text = io.open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit(f"没有 frontmatter: {path}")
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def scan(lines):
    """返回每行的状态：是否在代码块内、admonition 深度。"""
    fence = False
    depth = 0
    states = []
    for line in lines:
        s = line.strip()
        in_fence = fence
        if s.startswith("```"):
            fence = not fence
            states.append((True, depth))       # 围栏行本身不算可断点
            continue
        if not fence:
            if OPEN_RE.match(s):
                depth += 1
            elif s == ":::":
                depth = max(0, depth - 1)
        states.append((fence, depth))
    return states


def find_breaks(lines, states):
    """返回可作为切分点的行号（该行是标题行，且上一行状态安全）。"""
    h2, h3 = [], []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        if not line.startswith("#"):
            continue
        # 上一行必须不在代码块/admonition 内
        pf, pd = states[i - 1]
        if pf or pd:
            continue
        if line.startswith("## "):
            h2.append(i)
        elif line.startswith("### "):
            h3.append(i)
    return h2, h3


def split_blocks(lines, states):
    """先按 ## 切；单块超过 350 行则尝试按 ### 再切。返回 [(start,end)]。"""
    h2, h3 = find_breaks(lines, states)
    bounds = [0] + h2 + [len(lines)]
    blocks = []
    for a, b in zip(bounds, bounds[1:]):
        if b <= a:
            continue
        size = b - a
        if size > 350:
            inner = [x for x in h3 if a < x < b]
            if inner:
                ib = [a] + inner + [b]
                for x, y in zip(ib, ib[1:]):
                    if y > x:
                        blocks.append((x, y))
                continue
        blocks.append((a, b))
    return blocks


def refine(blocks, lines, states, maxsize):
    """把超过 maxsize 的单块在"安全空白行"处再切。"""
    out = []
    for a, b in blocks:
        if b - a <= maxsize:
            out.append((a, b))
            continue
        # 找安全切点：空白行，且该行与前一行都不在 fence / admonition 内
        cuts = []
        for i in range(a + 1, b):
            if lines[i].strip() != "":
                continue
            pf, pd = states[i - 1]
            cf, cd = states[i]
            if not pf and not pd and not cf and not cd:
                cuts.append(i)
        if not cuts:
            out.append((a, b))
            continue
        cur = a
        while b - cur > maxsize:
            # 选不超过 cur+maxsize 的最远切点
            cand = [c for c in cuts if c <= cur + maxsize and c > cur]
            if not cand:
                cand = [c for c in cuts if c > cur]
                if not cand:
                    break
            nxt = max(cand)
            out.append((cur, nxt))
            cur = nxt
        if b > cur:
            out.append((cur, b))
    return out


def group(blocks, sizes, target, maxsize, minsize):
    """贪心合并，尽量接近 target。"""
    pages = []
    cur = []
    cur_size = 0
    for blk, sz in zip(blocks, sizes):
        if cur and cur_size + sz > maxsize:
            pages.append(cur)
            cur, cur_size = [], 0
        cur.append(blk)
        cur_size += sz
        if cur_size >= target:
            pages.append(cur)
            cur, cur_size = [], 0
    if cur:
        # 末页太小就并入上一页，但不能超过 maxsize
        if pages:
            prev_size = pages[-1][-1][1] - pages[-1][0][0]
        else:
            prev_size = 0
        if pages and cur_size < minsize and prev_size + cur_size <= maxsize:
            pages[-1].extend(cur)
        else:
            pages.append(cur)
    return pages


def main():
    path = sys.argv[1]
    target = int(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 250
    maxsize = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 320
    dry = "--dry" in sys.argv

    fm, body = read(path)
    lines = body.split("\n")
    states = scan(lines)
    blocks = split_blocks(lines, states)
    blocks = refine(blocks, lines, states, maxsize)
    sizes = [b - a for a, b in blocks]
    pages = group(blocks, sizes, target, maxsize, 150)

    stem = os.path.basename(path)[:-4]
    d = os.path.dirname(path)

    print(f"{path}")
    print(f"  frontmatter: id={fm.get('id')} title={fm.get('title')}")
    print(f"  {len(blocks)} 个块 → {len(pages)} 页")
    for i, pg in enumerate(pages, 1):
        a = pg[0][0]
        b = pg[-1][1]
        head = ""
        for x in range(a, min(b, a + 40)):
            if lines[x].startswith("#"):
                head = lines[x].lstrip("# ").strip()
                break
        print(f"    第 {i} 页: {b - a:4d} 行  起于「{head[:36]}」")

    if dry:
        return

    ids = [f"{stem}-{i:02d}" for i in range(1, len(pages) + 1)]
    titles = []

    for i, pg in enumerate(pages):
        a = pg[0][0]
        b = pg[-1][1]
        chunk = lines[a:b]
        # 去掉开头多余的 # 一级标题（页面会自己生成）
        while chunk and (chunk[0].strip() == "" or chunk[0].startswith("# ")):
            chunk.pop(0)
        while chunk and chunk[-1].strip() == "":
            chunk.pop()
        if not chunk:
            continue

        if chunk[0].startswith("#"):
            raw_head = chunk[0].lstrip("# ").strip()
        elif i == 0:
            raw_head = fm.get("title", stem)      # 首页开头是导读段落，用文档标题
        else:
            raw_head = f"第 {i+1} 部分"
        core = clean_title(raw_head)
        title = f"{i+1:02d} {core}"

        # 首个标题行与页面 H1 重复，去掉
        if chunk and chunk[0].startswith("#"):
            chunk.pop(0)
            while chunk and chunk[0].strip() == "":
                chunk.pop(0)

        desc = f"{fm.get('title', stem)} 第 {i+1} 部分：{core}"
        titles.append(core)

        prev = f"[← {i:02d} {pages[i-1][0][0] and ''}](./{ids[i-1]})" if i > 0 else ""

        safe_title = title.replace('"', "'")
        safe_desc = desc.replace('"', "'")
        head = ["---", f"id: {ids[i]}", f'title: "{safe_title}"',
                f"sidebar_position: {i + 2}",
                f'description: "{safe_desc}"', "---", "", f"# {title}", ""]
        body_txt = "\n".join(chunk)

        nav = ["", "---", ""]
        bits = []
        if i > 0:
            bits.append(f"[← 上一页](./{ids[i-1]})")
        if i < len(pages) - 1:
            bits.append(f"[下一页 →](./{ids[i+1]})")
        bits.append("[返回目录](./)")
        nav.append("**翻页**：" + " · ".join(bits))
        nav.append("")

        out = "\n".join(head) + body_txt + "\n" + "\n".join(nav)
        p = os.path.join(d, f"{ids[i]}.mdx")
        io.open(p, "w", encoding="utf-8", newline="\n").write(out)
        print(f"    wrote {p}  ({out.count(chr(10))} 行)")

    # 导读页
    hub_title = fm.get('title', stem).replace('"', "'")
    hub_desc = (fm.get('description', '').strip() or fm.get('title', stem)).replace('"', "'")
    hub = ["---",
           f"id: {fm.get('id', stem)}",
           f'title: "{hub_title}（分页版）"',
           f"sidebar_position: {fm.get('sidebar_position', '1')}",
           f'description: "{hub_desc}"',
           "---", "", f"# {fm.get('title', stem)}（分页版）", "",
           f"本页原为 {len(lines)} 行的长文，已按主题拆成 {len(pages)} 个小页，每页 15 分钟。", "",
           "| # | 页面 |", "| --- | --- |"]
    for i in range(len(pages)):
        name = titles[i] if i < len(titles) else f"第 {i+1} 部分"
        hub.append(f"| {i+1} | [{name}](./{ids[i]}) |")
    hub.append("")
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(hub))
    print(f"    导读页 -> {path}")


if __name__ == "__main__":
    main()
