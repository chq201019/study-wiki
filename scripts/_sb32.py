import io
p = "sidebars.ts"
s = io.open(p, encoding="utf-8").read()
adds = [
    ("            'software/python/engineering-03',", ["software/python/argparse"]),
    ("            'software/cpp/embedded-cpp-03',", ["software/cpp/design-patterns"]),
    ("            'chips/stm32/debug-advanced',", ["chips/stm32/link-script"]),
    ("        'hardware/linux/tools-process',", ["hardware/linux/secrets"]),
    ("            'hardware/esp-basics/29-memory',", ["hardware/esp-basics/34-spi-deep", "hardware/esp-basics/35-adc-esp"]),
]
for anchor, ids in adds:
    if anchor not in s:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + "'" + i + "'," for i in ids)
    s = s.replace(anchor, block, 1)
    print("added", len(ids), "after", anchor.strip()[:45])
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(s)