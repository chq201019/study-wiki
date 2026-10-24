import io
p = 'docs/software/cpp/templates-01.mdx'
lines = io.open(p, encoding='utf-8').read().split(chr(10))
idx = None
for i, l in enumerate(lines):
    if l.strip() == '## 1. 函数模板：实例化机制':
        idx = i; break
alt = '模板实例化：max<T> 是图纸，编译器为 int/double/char 各生成一份独立机器码'
img = 'cpp-template-instantiation.svg'
if idx is None:
    print('MISS')
elif img in chr(10).join(lines):
    print('EXISTS')
else:
    lines[idx+1:idx+1] = ['', '![%s](/img/diagrams/%s)' % (alt, img), '']
    io.open(p, 'w', encoding='utf-8', newline=chr(10)).write(chr(10).join(lines))
    print('OK')