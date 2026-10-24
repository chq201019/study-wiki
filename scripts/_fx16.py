import io
p = "docs/chips/stm32/pool-allocator.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("](../software/c/memory)", "](../../software/c/memory)")
t = t.replace("](./link-script)", "](./link-script)")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed")