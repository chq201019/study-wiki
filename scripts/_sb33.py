import io
p = "sidebars.ts"
s = io.open(p, encoding="utf-8").read()
Q = chr(39)
adds = [
    ("            " + Q + "software/python/engineering-03" + Q + ",", ["software/python/memory-profiling"]),
    ("            " + Q + "software/cpp/embedded-cpp-03" + Q + ",", ["software/cpp/type-traits-in-practice"]),
    ("            " + Q + "chips/stm32/debug-advanced" + Q + ",", ["chips/stm32/profiling-embedded"]),
    ("        " + Q + "hardware/linux/tools-process" + Q + ",", ["hardware/linux/shell-tools", "hardware/linux/sockets"]),
    ("            " + Q + "hardware/esp-basics/29-memory" + Q + ",", ["hardware/esp-basics/36-ble"]),
]
for anchor, ids in adds:
    if anchor not in s:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + Q + i + Q + "," for i in ids)
    s = s.replace(anchor, block, 1)
    print("added", len(ids))
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(s)