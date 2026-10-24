import io
p = "docs/software/python/argparse.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("](../hardware/linux/secrets)", "](../../hardware/linux/secrets)")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed argparse link")