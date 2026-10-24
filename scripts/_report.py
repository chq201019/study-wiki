import io, glob
rows = []
for p in glob.glob("docs/**/*.mdx", recursive=True):
    n = len(io.open(p, encoding="utf-8").read().split(chr(10)))
    rows.append(n)
rows.sort()
tot = len(rows)
print("总页数:", tot)
print("最短:", rows[0], " 中位:", rows[tot//2], " 最长:", rows[-1])
print("平均:", round(sum(rows)/tot, 1))
bands = [(0,50),(50,100),(100,150),(150,300),(300,600),(600,10000)]
for lo, hi in bands:
    c = sum(1 for n in rows if lo <= n < hi)
    print("  %4d-%-5d : %3d 页 (%4.1f%%)" % (lo, hi, c, c*100/tot))