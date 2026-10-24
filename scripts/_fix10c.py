import io
p = "scripts/gen_diagrams10.py"
lines = io.open(p, encoding="utf-8").read().split(chr(10))

# 行号是 1-based，转成 0-based
lines[137] = "    fig, ax = plt.subplots(figsize=(10.8, 7.4))"
lines[139] = "    ax.set_ylim(0, 9.4)"
lines[170] = "    ax.text(0.4, 2.55," + chr(34) + chr(20026) + chr(20160) + chr(20040) + chr(19981) + chr(26159) + chr(31616) + chr(21333) + chr(30340) + chr(28145) + chr(24230) + chr(20248) + chr(20808) + chr(34) + ", fontsize=9.8,"
lines[184] = "        ax.text(0.4, 2.15 - i * 0.28, s, fontsize=8.2, color=TEXT)"
lines[186] = "    ax.text(0.4, 0.12,"

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
print("patched by line")