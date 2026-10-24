import io
p = "scripts/gen_diagrams12.py"
t = io.open(p, encoding="utf-8").read()

# After+Wants 标签移到箭头上方更远处，避免压线
t = t.replace('ax.text(3.9, 5.85, "After + Wants", fontsize=7.4, color=RED)',
              'ax.text(3.95, 6.12, "After + Wants", fontsize=7.4, color=RED)')
t = t.replace('ax.text(3.7, 4.35, "After + Requires", fontsize=7.4, color="#1e8449")',
              'ax.text(3.55, 4.28, "After + Requires", fontsize=7.4, color="#1e8449")')
t = t.replace('ax.text(7.9, 5.45, "WantedBy", fontsize=7.4, color=LINE)',
              'ax.text(7.95, 5.52, "WantedBy", fontsize=7.4, color=LINE)')

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("adjusted labels")