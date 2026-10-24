import io
p = "scripts/gen_diagrams12.py"
t = io.open(p, encoding="utf-8").read()

old_a = '''    a_ops = [("读 counter=5", 1.2), ("加 1 → 6", 4.0), ("写回 6", 8.2)]'''
new_a = '''    a_ops = [("读 counter=5", 1.2), ("加 1 → 6", 4.2), ("写回 6", 9.6)]'''
t = t.replace(old_a, new_a, 1)

old_b = '''    b_ops = [("读 counter=5", 2.8), ("加 1 → 6", 5.6), ("写回 6", 9.8)]'''
new_b = '''    b_ops = [("读 counter=5", 2.2), ("加 1 → 6", 5.2), ("写回 6", 10.6)]'''
t = t.replace(old_b, new_b, 1)

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("adjusted timeline")
