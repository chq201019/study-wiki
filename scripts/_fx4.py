import io
p = "docs/software/python/weakref.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("](../hardware/linux/memory-deep)", "](../../hardware/linux/memory-deep)")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed")
