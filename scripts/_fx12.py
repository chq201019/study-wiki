import io
p = "docs/software/python/argparse.mdx"
lines = io.open(p, encoding="utf-8").read().split(chr(10))
BT = chr(96)
lines[243] = "- [ ] **知道 " + BT + "store_true" + BT + " 默认 False，要 True 用 " + BT + "store_false" + BT + " + " + BT + "dest" + BT + "**"
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
print("fixed:", lines[243][:60])