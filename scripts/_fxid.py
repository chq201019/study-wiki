import io
fixes = [
    ("docs/hardware/esp-basics/32-i2c-deep.mdx", "id: i2c-deep", "id: 32-i2c-deep"),
    ("docs/hardware/esp-basics/33-uart-deep.mdx", "id: uart-deep", "id: 33-uart-deep"),
]
for p, a, b in fixes:
    t = io.open(p, encoding="utf-8").read()
    if a in t:
        t = t.replace(a, b, 1)
        io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
        print("fixed", p)
    else:
        print("MISS", p)
