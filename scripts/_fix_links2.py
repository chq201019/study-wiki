import io
fixes = [
    ("docs/chips/stm32/profiler.mdx", [
        ("](../chips/stm32/clock-deep)", "](./clock-deep)"),
        ("](../hardware/linux/memory-deep)", "](../../hardware/linux/memory-deep)"),
    ]),
    ("docs/software/c/filelock.mdx", [
        ("](../hardware/linux/tools-process)", "](../../hardware/linux/tools-process)"),
    ]),
]
for p, pairs in fixes:
    t = io.open(p, encoding="utf-8").read()
    for a, b in pairs:
        if a in t:
            t = t.replace(a, b)
            print("fixed", p, a, "->", b)
        else:
            print("MISS", p, a)
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
