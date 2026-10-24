"""批量拆分所有超过阈值的 MDX，并同步侧边栏。

用法: python scripts/batch_split.py [--threshold 600] [--dry]
"""
import io
import os
import glob
import shutil
import subprocess
import sys
import tempfile


def long_files(threshold):
    rows = []
    for p in glob.glob("docs/**/*.mdx", recursive=True):
        n = io.open(p, encoding="utf-8").read().count("\n")
        if n > threshold:
            rows.append((n, p.replace("\\", "/")))
    rows.sort(reverse=True)
    return rows


def main():
    threshold = 600
    if "--threshold" in sys.argv:
        threshold = int(sys.argv[sys.argv.index("--threshold") + 1])
    dry = "--dry" in sys.argv

    rows = long_files(threshold)
    print(f"超过 {threshold} 行的文件: {len(rows)} 个")
    if dry:
        for n, p in rows:
            print(f"  {n:5d}  {p}")
        return

    bak = os.path.join(tempfile.gettempdir(), "splitbak2")
    os.makedirs(bak, exist_ok=True)

    ok, fail, total_new = 0, [], 0
    done = []

    for n, p in rows:
        # 备份
        flat = p.replace("docs/", "").replace("/", "_")
        shutil.copy(p, os.path.join(bak, flat))

        before = set(glob.glob(os.path.join(os.path.dirname(p), os.path.basename(p)[:-4] + "-*.mdx")))
        r = subprocess.run([sys.executable, "scripts/auto_split.py", p],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail.append((p, r.stderr.strip()[:200]))
            continue
        after = set(glob.glob(os.path.join(os.path.dirname(p), os.path.basename(p)[:-4] + "-*.mdx")))
        new = sorted(after - before)
        if not new:
            fail.append((p, "未产出分页"))
            continue
        ok += 1
        total_new += len(new)
        done.append((p, len(new)))

    print(f"\n成功 {ok} / {len(rows)}，共产出 {total_new} 个分页")
    for p, k in done:
        print(f"  {p}  -> {k} 页")
    for p, e in fail:
        print(f"  FAIL {p}: {e}")

    # 同步侧边栏
    sp = "sidebars.ts"
    t = io.open(sp, encoding="utf-8").read()
    inserted = 0
    for p, _ in done:
        rel = p.replace("docs/", "")[:-4]          # 如 software/python/oop
        stem = os.path.basename(p)[:-4]
        pats = sorted(glob.glob(os.path.join(os.path.dirname(p), stem + "-*.mdx")))
        newids = [rel.rsplit("/", 1)[0] + "/" + os.path.basename(x)[:-4] for x in pats]
        needle = "'" + rel + "',\n"
        if needle in t:
            block = needle + "".join("            '" + i + "',\n" for i in newids)
            t = t.replace(needle, block, 1)
            inserted += len(newids)
        else:
            print("  侧边栏未找到:", rel)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(t)
    print(f"侧边栏插入 {inserted} 个条目")


if __name__ == "__main__":
    main()
