import io
paths = ["docs/software/c/filelock.mdx", "docs/chips/stm32/profiler.mdx", "docs/hardware/linux/security.mdx"]
BT = chr(96)
for p in paths:
    t = io.open(p, encoding="utf-8").read()
    o = t
    # 反引号被转义成 \` -> 还原为 `
    t = t.replace(chr(92) + BT, BT)
    if t != o:
        io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
        print("fixed fences:", p)
# 修 <强密码>
q = "docs/hardware/linux/security.mdx"
s = io.open(q, encoding="utf-8").read()
s = s.replace("requirepass <强密码>", BT + "requirepass <强密码>" + BT)
io.open(q, "w", encoding="utf-8", newline=chr(10)).write(s)
print("fixed requirepass")
