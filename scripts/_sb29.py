import io
p = "sidebars.ts"
t = io.open(p, encoding="utf-8").read()
adds = [
    ("            'software/python/engineering-03',",
     ["software/python/contextlib", "software/python/weakref", "software/python/subprocess"]),
    ("            'software/c/pitfalls-03',", ["software/c/bit-manipulation"]),
]
for anchor, ids in adds:
    if anchor not in t:
        print("MISS:", anchor); continue
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    block = anchor + "".join(chr(10) + indent + "'" + i + "'," for i in ids)
    t = t.replace(anchor, block, 1)
    print("added", len(ids), "after", anchor.strip()[:40])
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
