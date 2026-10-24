"""检查 mdx 的 id 字段与文件名一致（不一致会导致侧边栏引用失败）。"""
import io, glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

bad = []
for p in sorted(glob.glob("docs/**/*.mdx", recursive=True)):
    stem = os.path.basename(p)[:-4]
    txt = io.open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        continue
    fm = m.group(1)
    idm = re.search(r"^id:\s*(\S+)", fm, re.M)
    if idm and idm.group(1) != stem:
        bad.append((p, idm.group(1), stem))

if bad:
    print("id 与文件名不一致 %d 处：" % len(bad))
    for p, got, want in bad:
        print("  %s: id=%s, 文件名=%s" % (p, got, want))
    sys.exit(1)
print("所有 id 与文件名一致")
