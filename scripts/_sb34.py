import io
p = "sidebars.ts"
s = io.open(p, encoding="utf-8").read()
Q = chr(39)
adds = [
    ("            " + Q + "software/python/engineering-03" + Q + ",", ["software/python/code-review"]),
    ("            " + Q + "software/c/pitfalls-03" + Q + ",", ["software/c/error-codes-deep"]),
    ("            " + Q + "chips/stm32/debug-advanced" + Q + ",", ["chips/stm32/pool-allocator"]),
    ("        " + Q + "hardware/linux/tools-process" + Q + ",", ["hardware/linux/testing-strategy"]),
    ("            " + Q + "hardware/esp-basics/29-memory" + Q + ",", ["hardware/esp-basics/37-mqtt", "hardware/esp-basics/38-wifi-deep"]),
]
for anchor, ids in adds:
    if anchor not in s:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + Q + i + Q + "," for i in ids)
    s = s.replace(anchor, block, 1)
    print("added", len(ids))
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(s)