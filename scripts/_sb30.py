import io
p = "docs/hardware/linux/vim.mdx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("](../hardware/linux/shell-advanced)", "](./shell-advanced)")
t = t.replace("](../hardware/linux/git)", "](./git)")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("fixed vim links")

sb = "sidebars.ts"
s = io.open(sb, encoding="utf-8").read()
adds = [
    ("            'software/python/engineering-03',", ["software/python/numpy-basics"]),
    ("            'software/cpp/embedded-cpp-03',", ["software/cpp/chrono"]),
    ("            'software/c/pitfalls-03',", ["software/c/dynamic-memory"]),
    ("        'hardware/linux/tools-process',", ["hardware/linux/vim"]),
]
for anchor, ids in adds:
    if anchor not in s:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + "'" + i + "'," for i in ids)
    s = s.replace(anchor, block, 1)
    print("added after", anchor.strip()[:40])
io.open(sb, "w", encoding="utf-8", newline=chr(10)).write(s)
