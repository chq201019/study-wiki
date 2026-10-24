import io
p = "docs/hardware/esp-basics/32-i2c-deep.mdx"
t = io.open(p, encoding="utf-8").read()
old = "**因为大多数小板子总线电容很小（< 50pF），4.7k 就够。**"
new = "**因为大多数小板子总线电容很小（小于 50pF），4.7k 就够。**"
if old in t:
    t = t.replace(old, new); print("fixed")
else:
    print("MISS")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
