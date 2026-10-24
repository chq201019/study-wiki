import io
fixes = [
    ("docs/hardware/esp-basics/37-mqtt.mdx", "id: 24-mqtt", "id: 37-mqtt"),
    ("docs/hardware/esp-basics/38-wifi-deep.mdx", "id: 25-wifi-deep", "id: 38-wifi-deep"),
]
for p, a, b in fixes:
    t = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t.replace(a, b, 1))
    print("fixed", p)