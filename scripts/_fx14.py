import io
p = "docs/software/python/code-review.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("](../hardware/linux/git)", "](../../hardware/linux/git)")
t = t.replace("](./testing)", "](./testing)")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed")