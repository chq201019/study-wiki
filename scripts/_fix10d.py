import io
p = "scripts/gen_diagrams10.py"
lines = io.open(p, encoding="utf-8").read().split(chr(10))

for i, l in enumerate(lines):
    if "ax.text(0.4, 2.55," in l:
        lines[i] = l.replace("2.55", "2.85")
    elif "ax.text(0.4, 2.15 - i * 0.28, s" in l:
        lines[i] = l.replace("2.15", "2.50")
    elif "ax.text(0.4, 0.12," in l:
        lines[i] = "    ax.text(0.4, -0.25,"

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
print("adjusted")