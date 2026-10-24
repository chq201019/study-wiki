import io
fixes = [
    ("docs/hardware/esp-basics/34-spi-deep.mdx", "id: 32-spi-deep", "id: 34-spi-deep"),
    ("docs/hardware/esp-basics/35-adc-esp.mdx", "id: 22-adc-esp", "id: 35-adc-esp"),
]
for p, a, b in fixes:
    t = io.open(p, encoding="utf-8").read()
    if a in t:
        io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t.replace(a, b, 1))
        print("fixed", p)
    else:
        print("MISS", p)