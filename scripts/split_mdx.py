"""按 ## 小节边界拆分过长 MDX 页面。

保留原文字节内容（不重写正文），只为每页生成 frontmatter、
上一页/下一页导航，并把原文件改写为导读页。

用法:
    python scripts/split_mdx.py <源文件> <输出目录> <配置模块.py>
配置模块需提供 GROUPS 列表：每项是 (文件名, id, 标题, description, [小节序号...])
以及 HUB_TITLE / HUB_DESC。
"""
import io
import os
import re
import sys
import importlib.util


def load_groups(path):
    spec = importlib.util.spec_from_file_location("cfg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse(path):
    """返回 (frontmatter_dict, sections)；sections 为 [(heading, [lines])]。"""
    text = io.open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit("没有 frontmatter")
    fm_raw = m.group(1)
    body = text[m.end():]

    fm = {}
    for line in fm_raw.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()

    # 以 "## " 开头的行为切分点；"# " 一级标题单独处理
    lines = body.split("\n")
    sections = []
    cur = None
    preamble = []
    for line in lines:
        if line.startswith("## "):
            if cur is not None:
                sections.append(cur)
            cur = (line[3:].strip(), [line])
        elif cur is None and not line.startswith("# "):
            preamble.append(line)
        elif cur is not None:
            cur[1].append(line)

    if cur is not None:
        sections.append(cur)
    return fm, sections, preamble


def trim(lines):
    """去掉尾部多余空行，返回去尾后的行列表。"""
    out = list(lines)
    while out and out[-1].strip() == "":
        out.pop()
    return out


def main():
    src, outdir, cfgpath = sys.argv[1], sys.argv[2], sys.argv[3]
    cfg = load_groups(cfgpath)

    fm, sections, _ = parse(src)
    print(f"解析出 {len(sections)} 个小节")

    os.makedirs(outdir, exist_ok=True)
    groups = cfg.GROUPS

    # 记录每页 id 用于导航
    ids = [g[1] for g in groups]

    for i, (fname, doc_id, title, desc, idxs) in enumerate(groups):
        picked = [sections[j] for j in idxs]
        parts = []
        for heading, body in picked:
            parts.extend(trim(body))
            parts.append("")
        body_text = "\n".join(parts).rstrip() + "\n"

        prev_link = ""
        nxt_link = ""
        if i > 0:
            prev_link = f"[← {groups[i-1][2]}](./{groups[i-1][1]})"
        if i < len(groups) - 1:
            nxt_link = f"[{groups[i+1][2]} →](./{groups[i+1][1]})"

        nav = []
        if prev_link or nxt_link:
            nav.append("")
            nav.append("---")
            bits = [b for b in (prev_link, nxt_link) if b]
            nav.append("")
            nav.append("**翻页**：" + " · ".join(bits) + " · [返回目录](./)")
            nav.append("")

        head = (
            "---\n"
            f"id: {doc_id}\n"
            f"title: {title}\n"
            f"sidebar_position: {i + 2}\n"
            f"description: {desc}\n"
            "---\n\n"
            f"# {title}\n"
        )

        content = head + body_text + "\n".join(nav)
        path = os.path.join(outdir, fname)
        io.open(path, "w", encoding="utf-8", newline="\n").write(content)
        n = len(content.split("\n"))
        print(f"  {fname:34s} {n:4d} 行  <- 小节 {idxs}")

    # 改写原文件为导读页
    hub = [
        "---",
        f"id: {fm.get('id', os.path.basename(src)[:-4])}",
        f"title: {cfg.HUB_TITLE}",
        f"sidebar_position: {fm.get('sidebar_position', '3')}",
        f"description: {cfg.HUB_DESC}",
        "---",
        "",
        f"# {cfg.HUB_TITLE}",
        "",
        cfg.HUB_INTRO.strip(),
        "",
        "## 分页目录",
        "",
        "| # | 页面 | 内容 |",
        "| --- | --- | --- |",
    ]
    for i, (fname, doc_id, title, desc, idxs) in enumerate(groups):
        short = desc.split("。")[0]
        hub.append(f"| {i+1} | [{title}](./{doc_id}) | {short} |")
    hub.append("")
    hub.append(cfg.HUB_OUTRO.strip())
    hub.append("")

    io.open(src, "w", encoding="utf-8", newline="\n").write("\n".join(hub))
    print(f"导读页已写入 {src}（{len(hub)} 行）")


if __name__ == "__main__":
    main()
