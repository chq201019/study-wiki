import io
p = "sidebars.ts"
t = io.open(p, encoding="utf-8").read()
adds = [
    ("            'software/c/pitfalls-03',", ["software/c/filelock"]),
    ("            'chips/stm32/debug-advanced',", ["chips/stm32/profiler"]),
    ("        'hardware/linux/tools-process',", ["hardware/linux/security"]),
]
for anchor, ids in adds:
    if anchor not in t:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + "'" + i + "'," for i in ids)
    t = t.replace(anchor, block, 1)
    print("added after:", anchor.strip())
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
