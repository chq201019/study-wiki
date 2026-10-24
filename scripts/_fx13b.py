import io
p = "scripts/gen_diagrams13.py"
t = io.open(p, encoding="utf-8").read()

# 右侧说明整体下移，避开 config.h（y 2.0~2.66）
t = t.replace('ax.text(7.6, 2.55, "头文件依赖必须自动生成", fontsize=9.2,',
              'ax.text(8.0, 1.72, "头文件依赖必须自动生成", fontsize=9.2,')
t = t.replace('ax.text(7.6, 2.2, "编译时加 -MMD -MP，", fontsize=7.8, color=TEXT)',
              'ax.text(8.0, 1.40, "编译时加 -MMD -MP，再 -include $(DEPS)，", fontsize=7.6, color=TEXT)')
t = t.replace('ax.text(7.6, 1.92, "再 -include $(DEPS)", fontsize=7.8, color=TEXT)',
              'ax.text(8.0, 1.12, "否则改头文件不会触发任何重编 ——", fontsize=7.6, color=TEXT)')
t = t.replace('ax.text(7.6, 1.55, "否则改头文件不会触发", fontsize=7.8, color=TEXT)',
              'ax.text(8.0, 0.86, "你看到的是旧行为，调试很久也找不到原因。", fontsize=7.6, color=RED)')
t = t.replace('ax.text(7.6, 1.27, "任何重编 —— 你看到的是旧行为。", fontsize=7.8, color=TEXT)', '')

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("moved right text")
