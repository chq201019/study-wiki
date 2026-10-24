import io

p = "scripts/gen_diagrams4.py"
t = io.open(p, encoding="utf-8").read()

anchor = 'rcParams["axes.unicode_minus"] = False'
addition = anchor + '\nrcParams["text.parse_math"] = False   # 避免 $ 被当成 mathtext 分隔符'

if "text.parse_math" in t:
    print("已存在，跳过")
else:
    assert anchor in t, "锚点未找到"
    t = t.replace(anchor, addition, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("已关闭 mathtext 解析")
