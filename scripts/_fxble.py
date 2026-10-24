import io
p = "docs/hardware/esp-basics/36-ble.mdx"
t = io.open(p, encoding="utf-8").read()
BT = chr(96)
n = t.count(chr(92) + BT)
t = t.replace(chr(92) + BT, BT)
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("replaced escaped backticks:", n)