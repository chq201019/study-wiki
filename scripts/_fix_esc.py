import io, glob
paths = ["docs/software/c/filelock.mdx", "docs/chips/stm32/profiler.mdx", "docs/hardware/linux/security.mdx"]
for p in paths:
    t = io.open(p, encoding="utf-8").read()
    o = t
    t = t.replace(chr(92)*2 + "n", chr(92) + "n")
    t = t.replace(chr(92)*2 + ";", chr(92) + ";")
    if t != o:
        io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
        print("fixed", p)
print("done")
