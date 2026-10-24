import io
p = "scripts/gen_diagrams15.py"
lines = io.open(p, encoding="utf-8").read().split(chr(10))
lines[154] = '    ax.text(0.4, 0.65, "验证手段：编译时用 -Wall -Wextra，很多数组/指针混用会直接告警；",'
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
print("fixed line 155")