import io
p = 'docs/software/c/pointers-01.mdx'
lines = io.open(p, encoding='utf-8').read().split(chr(10))
idx = None
for i, l in enumerate(lines):
    if l.strip() == '## 三、数组与指针：必须分清的三件事':
        idx = i; break
alt = '数组名不是指针：sizeof(arr) 是 20 而 sizeof(&arr[0]) 是 8，数组传参会退化成指针丢失长度信息'
img = 'c-pointer-array-detail.svg'
if idx is None:
    print('MISS')
elif img in chr(10).join(lines):
    print('EXISTS')
else:
    lines[idx+1:idx+1] = ['', '![%s](/img/diagrams/%s)' % (alt, img), '']
    io.open(p, 'w', encoding='utf-8', newline=chr(10)).write(chr(10).join(lines))
    print('OK')