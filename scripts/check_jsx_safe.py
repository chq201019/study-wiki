"""检查指定文件的正文里是否有会被 MDX 当 JSX 的 <。
用法: python scripts/check_jsx_safe.py [file1.mdx file2.mdx ...]
不给参数时检查最近修改的 20 个 mdx。
"""
import io, re, sys, glob, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BAD = re.compile(r"<[A-Za-z_=]")

files = sys.argv[1:]
if not files:
    all_f = glob.glob("docs/**/*.mdx", recursive=True)
    all_f.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    files = all_f[:20]

bad = []
for p in files:
    lines = io.open(p, encoding="utf-8").read().split(chr(10))
    in_fence = False
    for i, l in enumerate(lines, 1):
        if l.lstrip().startswith(chr(96)*3):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = re.sub(chr(96) + "[^" + chr(96) + "]*" + chr(96), "", l)
        if BAD.search(stripped):
            bad.append((p, i, l.strip()[:70]))

if bad:
    print("正文中 JSX 风险的 < 共 %d 处：" % len(bad))
    for p, i, s in bad:
        print("  %s:%d  %s" % (p, i, s))
    sys.exit(1)
print("OK: %d 个文件正文无 JSX 风险的 <" % len(files))
