import io
p = 'docs/software/c/preprocessor-01.mdx'
lines = io.open(p, encoding='utf-8').read().split(chr(10))
idx = None
for i, l in enumerate(lines):
    if l.strip() == '## 一、预处理器做的事':
        idx = i; break
alt = 'C 预处理流程：10 行源文件经 include 递归展开与宏替换后变成约 1750 行的 .i 文件'
img = 'c-preprocess-flow.svg'
if idx is None:
    print('MISS')
elif img in chr(10).join(lines):
    print('EXISTS')
else:
    lines[idx+1:idx+1] = ['', '![%s](/img/diagrams/%s)' % (alt, img), '']
    io.open(p, 'w', encoding='utf-8', newline=chr(10)).write(chr(10).join(lines))
    print('OK')