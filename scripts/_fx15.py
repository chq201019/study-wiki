import io
fixes = [
    ("docs/hardware/linux/testing-strategy.mdx", [
        ("](../software/python/testing)", "](../../software/python/testing)"),
        ("](../software/python/code-review)", "](../../software/python/code-review)"),
    ]),
    ("docs/software/c/error-codes-deep.mdx", [
        ("](../software/cpp/error-handling)", "](./../cpp/error-handling)"),
        ("](../software/c/memory)", "](./memory)"),
    ]),
]
for p, pairs in fixes:
    t = io.open(p, encoding="utf-8").read()
    for a, b in pairs:
        if a in t:
            t = t.replace(a, b); print("fixed", p, a)
        else:
            print("MISS", p, a)
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)