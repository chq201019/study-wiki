"""调整 gen_diagrams6.py 中 3 张图的垂直间距。"""
import io

P = "scripts/gen_diagrams6.py"
t = io.open(P, encoding="utf-8").read()

# ---------- 1) 深浅拷贝：加高画布、重排 y ----------
t = t.replace(
    '''    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.4)
    ax.set_axis_off()
    ax.text(0.2, 8.0, "浅拷贝 vs 深拷贝：嵌套结构只复制了第一层",''',
    '''    fig, ax = plt.subplots(figsize=(10.8, 7.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 10.3)
    ax.set_axis_off()
    ax.text(0.2, 9.9, "浅拷贝 vs 深拷贝：嵌套结构只复制了第一层",''')

t = t.replace('    ax.text(0.4, 7.45, "原始：a = [[1, 2], [3, 4]]',
              '    ax.text(0.4, 9.35, "原始：a = [[1, 2], [3, 4]]')
t = t.replace('    draw_row(6.3, "a", "list", ORANGE,',
              '    draw_row(8.55, "a", "list", ORANGE,')
t = t.replace('    ax.text(0.4, 5.5, "① 浅拷贝',
              '    ax.text(0.4, 7.5, "① 浅拷贝')
t = t.replace('    draw_row(4.35, "b", "新 list", ORANGE,',
              '    draw_row(6.25, "b", "新 list", ORANGE,')
t = t.replace('    ax.text(0.4, 3.9, "b[0].append(99)  →  a 也变了',
              '    ax.text(0.4, 5.25, "b[0].append(99)  →  a 也变了')
t = t.replace('    ax.text(0.4, 3.3, "② 深拷贝',
              '    ax.text(0.4, 4.65, "② 深拷贝')
t = t.replace('    draw_row(2.15, "b", "新 list", ORANGE,',
              '    draw_row(3.35, "b", "新 list", ORANGE,')
t = t.replace('    ax.text(0.4, 1.7, "b[0].append(99)  →  a 完全不受影响"',
              '    ax.text(0.4, 2.35, "b[0].append(99)  →  a 完全不受影响"')
t = t.replace('    ax.text(0.4, 1.15, "另一种更隐蔽的浅拷贝来源',
              '    ax.text(0.4, 1.75, "另一种更隐蔽的浅拷贝来源')
t = t.replace('    ax.text(0.4, 0.78, "b = a[:]',
              '    ax.text(0.4, 1.38, "b = a[:]')
t = t.replace('    ax.text(0.4, 0.3,\n            "记忆法：元素是不可变类型',
              '    ax.text(0.4, 0.65,\n            "记忆法：元素是不可变类型')

# ---------- 2) OTA：底部两行错开 ----------
t = t.replace('        ax.text(0.5, 2.1 - i * 0.36, s, fontsize=8.4, color=TEXT)',
              '        ax.text(0.5, 2.55 - i * 0.34, s, fontsize=8.4, color=TEXT)')
t = t.replace('    ax.text(0.5, 0.55, "分区表要求：必须有两个 app 分区',
              '    ax.text(0.5, 0.62, "分区表要求：必须有两个 app 分区')
t = t.replace('    ax.text(0.5, 0.2, "默认 singleapp 分区表',
              '    ax.text(0.5, 0.25, "默认 singleapp 分区表')

# ---------- 3) 虚拟内存：地址布局上移、底部说明下移 ----------
t = t.replace('    ax.text(0.5, 3.35, "每个进程的虚拟地址空间布局（示意，从高到低）"',
              '    ax.text(0.5, 3.62, "每个进程的虚拟地址空间布局（示意，从高到低）"')
t = t.replace('        y = 2.95 - i * 0.42', '        y = 3.20 - i * 0.40')
t = t.replace('    ax.text(0.4, 0.5, "查证：cat /proc/<pid>/maps 看地址空间',
              '    ax.text(0.4, 0.55, "查证：cat /proc/<pid>/maps 看地址空间')

io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("已调整 3 张图的间距")
