import io
p = "scripts/gen_diagrams13.py"
t = io.open(p, encoding="utf-8").read()

old = '''        ("≤ 24 MHz", "0 等待", GREEN),
        ("24 ~ 48 MHz", "1 等待", ORANGE),
        ("48 ~ 72 MHz", "2 等待", RED),'''
new = '''        ("≤ 24 MHz", "0 等待", "#1e8449"),
        ("24 ~ 48 MHz", "1 等待", "#b9770e"),
        ("48 ~ 72 MHz", "2 等待", "#a93226"),'''
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("darkened colors")
