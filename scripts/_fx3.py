import io
p = "docs/chips/stm32/profiler.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("](./concurrency)", "](../../software/c/concurrency)")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed")
