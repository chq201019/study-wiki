import io
p = "docs/hardware/esp-basics/36-ble.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("id: 23-ble", "id: 36-ble", 1)
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed id")