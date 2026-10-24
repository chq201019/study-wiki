import io
p = "docs/hardware/esp-basics/32-i2c-deep.mdx"
t = io.open(p, encoding="utf-8").read()
reps = [
    ("**举例**：总线电容 100pF，快速模式要求 t_r <= 300ns",
     "**举例**：总线电容 100pF，快速模式要求 t_r 不大于 300ns"),
]
for a, b in reps:
    if a in t:
        t = t.replace(a, b); print("fixed line 47")
    else:
        print("MISS")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
