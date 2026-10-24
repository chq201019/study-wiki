"""重写 linux_fd_table()，解决方框与说明文字重叠。"""
import io
import re

p = "scripts/gen_diagrams4.py"
t = io.open(p, encoding="utf-8").read()

start = t.index("def linux_fd_table():")
end = t.index("def esp32_memory():")

new_fn = '''def linux_fd_table():
    """文件描述符的三层结构"""
    fig, ax = plt.subplots(figsize=(10.6, 6.8))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 9.4)
    ax.set_axis_off()
    ax.text(0.2, 9.0, "文件描述符：一个整数背后的三层结构", fontsize=12.5,
            fontweight="bold", color=TEXT)

    # 层标题
    ax.text(0.5, 8.35, "① 进程的 fd 表", fontsize=9.5, fontweight="bold", color=TEXT)
    ax.text(4.2, 8.35, "② 系统打开文件表", fontsize=9.5, fontweight="bold", color=TEXT)
    ax.text(8.6, 8.35, "③ inode（磁盘上）", fontsize=9.5, fontweight="bold", color=TEXT)

    # fd 表：4 项，间距 0.78
    fds = [("0", "stdin"), ("1", "stdout"), ("2", "stderr"), ("3", "你的文件")]
    for i, (n, name) in enumerate(fds):
        y = 7.5 - i * 0.78
        ax.add_patch(Rectangle((0.5, y), 0.55, 0.58, facecolor=ORANGE,
                               edgecolor=DARK, lw=1.0))
        ax.text(0.775, y + 0.29, n, ha="center", va="center", fontsize=10,
                color=TEXT, fontweight="bold")
        ax.add_patch(Rectangle((1.1, y), 1.7, 0.58,
                               facecolor=PINK if i < 3 else BLUE,
                               edgecolor=DARK, lw=1.0))
        ax.text(1.95, y + 0.29, name, ha="center", va="center", fontsize=8.2,
                color=TEXT)

    # 文件表 / inode 对准第 4 项
    box(ax, 4.2, 4.95, 3.0, 1.0, "打开文件表项", "读写位置 offset\\n打开模式 O_RDWR", GREEN, fs=9, sfs=7.4)
    arrow(ax, (2.85, 5.45), (4.15, 5.45))

    box(ax, 8.6, 4.95, 4.2, 1.0, "inode", "权限、大小、时间、数据块位置", PURPLE, fs=9.5, sfs=7.4)
    arrow(ax, (7.25, 5.45), (8.55, 5.45))

    # 说明
    ax.text(0.5, 4.2, "为什么要有中间这一层？", fontsize=10.5,
            fontweight="bold", color=TEXT)
    pts = [
        "• fd 只是进程内数组的下标 —— 所以每个进程的 0/1/2 互不相干",
        "• 中间的 offset 是「一次打开」的状态：同一文件两次 open 得到两个独立",
        "  offset，各读各的，互不干扰",
        "• fork 出来的子进程共享文件表项 —— 父子俩「抢着读」，offset 是同一个",
        "• dup / dup2 让两个 fd 指向同一个表项 —— 这是 shell 重定向的实现",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 3.72 - i * 0.42, s, fontsize=8.6, color=TEXT)

    # 重定向例子
    ax.text(0.5, 1.35, "shell 重定向是怎么实现的：", fontsize=10,
            fontweight="bold", color=TEXT)
    ax.text(0.5, 0.95,
            "命令 > out.txt   等价于   先 open(out.txt) 得到 fd 3，"
            "再 dup2(3, 1) 把 1 号改指向它，然后 close(3)",
            fontsize=8.6, color=TEXT)
    ax.text(0.5, 0.55, "所以程序里 printf 写 1 号 fd，数据就进了文件 —— 程序自己毫不知情。",
            fontsize=8.6, color=RED)
    ax.text(0.5, 0.15, "常用命令：ls -l /proc/$$/fd    查看当前 shell 打开了哪些 fd",
            fontsize=8.4, color=LINE)

    _save(fig, "linux-fd-table.svg")


'''

t = t[:start] + new_fn + t[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("已重写 linux_fd_table()")
