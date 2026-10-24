import io, glob, os

p = "PROJECT.md"
t = io.open(p, encoding="utf-8").read()

pages = len(glob.glob("docs/**/*.mdx", recursive=True))
imgs = len(glob.glob("static/img/diagrams/*.svg"))
lines = sum(len(io.open(f, encoding="utf-8").read().split(chr(10))) for f in glob.glob("docs/**/*.mdx", recursive=True))

def count(d):
    return len([f for f in glob.glob(d + "/**/*.mdx", recursive=True)])

stats = [
    "",
    "---",
    "",
    "## 站点现状（自动统计）",
    "",
    "| 指标 | 数值 |",
    "| --- | --- |",
    "| 总页数 | **%d** |" % pages,
    "| 总行数 | %d |" % lines,
    "| 示意图 | **%d 张** |" % imgs,
    "",
    "### 六条课程线",
    "",
    "| 课程线 | 零基础 | 进阶 |",
    "| --- | --- | --- |",
]

tracks = [
    ("Python", "docs/software/python-basics", "docs/software/python"),
    ("C", "docs/software/c-basics", "docs/software/c"),
    ("C++", "docs/software/cpp-basics", "docs/software/cpp"),
    ("Linux", "docs/hardware/linux-basics", "docs/hardware/linux"),
    ("ESP32", "docs/hardware/esp-basics", "docs/course"),
    ("STM32", "docs/hardware/stm-basics", "docs/chips/stm32"),
]
for name, beg, adv in tracks:
    nb = count(beg) - 1
    na = count(adv)
    stats.append("| %s | %d 课 | %d 页 |" % (name, max(nb, 0), na))

stats += [
    "",
    "## 质量校验脚本",
    "",
    "每次提交前固定跑这五个检查（各几秒，能拦下绝大多数构建失败）：",
    "",
    "```bash",
    "node scripts/check_sidebar.js            # sidebars.ts 语法（TypeScript 编译验证）",
    "python scripts/check_docid.py            # mdx 的 id 与文件名一致",
    "python scripts/check_jsx_safe.py         # 正文裸 < 会被当 JSX",
    "python scripts/check_links.py            # 相对链接是否指向真实页面",
    "python scripts/check_mdx_all.py          # admonition ::: 配对",
    "python scripts/check_frontmatter.py      # frontmatter 合法性",
    "```",
    "",
    "构建在服务器上执行（本地 Windows 构建慢一个数量级）：",
    "",
    "```bash",
    "tar -czf /tmp/w.tar.gz docs src static docusaurus.config.ts sidebars.ts scripts package.json package-lock.json",
    "npm run build",
    "# 然后把 build/ 整个目录同步到你的静态服务器",
    "```",
    "",
    "**解包前必须先 `rm -rf docs src static`** —— tar 只覆盖不删除，旧文件残留会导致断链。",
    "",
]

block = chr(10).join(stats)
if "## 站点现状（自动统计）" in t:
    i = t.index("## 站点现状（自动统计）")
    j = t.index("## ", i + 5) if "## " in t[i+5:] else len(t)
    t = t[:i] + block[4:] + t[j:]
    print("updated existing section")
else:
    t = t.rstrip() + chr(10) + block
    print("appended new section")

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("pages=%d lines=%d imgs=%d" % (pages, lines, imgs))