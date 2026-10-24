import io

p = "scripts/gen_diagrams3.py"
t = io.open(p, encoding="utf-8").read()

fixes = [
    ('"• 装饰器本身就是"接收函数、返回函数"",',
     '"• 装饰器本身就是「接收函数、返回函数」",'),
    ('"  会变成 "wrapper"，调试时很迷惑",',
     '"  会变成「wrapper」，调试时很迷惑",'),
    ('"  @timer(unit="ms") → 先调用拿到真装饰器",',
     '"  @timer(unit=ms) → 先调用拿到真装饰器",'),
]
for a, b in fixes:
    if a in t:
        t = t.replace(a, b)
    else:
        print("未匹配:", a[:40])

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("已替换中文里的英文引号")
