import io
sb = "sidebars.ts"
s = io.open(sb, encoding="utf-8").read()
adds = [
    ("            'software/python/engineering-03',", ["software/python/sqlite"]),
    ("            'software/cpp/embedded-cpp-03',", ["software/cpp/raii-extended"]),
    ("        'hardware/linux/tools-process',", ["hardware/linux/ebpf"]),
    ("            'hardware/esp-basics/29-memory'", ["hardware/esp-basics/32-i2c-deep", "hardware/esp-basics/33-uart-deep"]),
]
for anchor, ids in adds:
    if anchor not in s:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + "'" + i + "'," for i in ids)
    s = s.replace(anchor, block, 1)
    print("added", len(ids), "after", anchor.strip()[:45])
io.open(sb, "w", encoding="utf-8", newline=chr(10)).write(s)
