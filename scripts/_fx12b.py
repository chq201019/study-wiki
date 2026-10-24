import io
p = "scripts/gen_diagrams12.py"
t = io.open(p, encoding="utf-8").read()
t = t.replace('ax.text(3.55, 4.28, "After + Requires", fontsize=7.4, color="#1e8449")',
              'ax.text(2.55, 3.95, "After + Requires", fontsize=7.4, color="#1e8449")')
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("moved")