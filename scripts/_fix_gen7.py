"""修正 gen_diagrams7.py 的三张图。"""
import io
import re

P = "scripts/gen_diagrams7.py"
t = io.open(P, encoding="utf-8").read()


def replace_fn(text, name, new_code):
    start = text.index(f"def {name}(")
    rest = text[start + 5:]
    m = re.search(r"\n(?:def [a-z_]+\(\):|if __name__)", rest)
    if not m:
        raise SystemExit("找不到下一个边界")
    end = start + 5 + m.start() + 1
    return text[:start] + new_code + text[end:]


NEW_GIT = '''def git_objects():
    """Git 四种对象的关系"""
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.0)
    ax.set_axis_off()
    ax.text(0.2, 7.6, "Git 对象：commit 指向 tree，tree 指向 blob",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # commit 链
    box(ax, 0.5, 5.9, 2.9, 0.95, "commit C2", "tree / parent", PINK, fs=9.5, sfs=7.4)
    box(ax, 0.5, 4.6, 2.9, 0.95, "commit C1", "tree / parent", PINK, fs=9.5, sfs=7.4)
    arrow(ax, (1.95, 5.85), (1.95, 5.6), color=LINE, lw=1.4)
    ax.text(2.1, 5.72, "parent", fontsize=7.4, color=LINE)

    # 根 tree
    box(ax, 4.3, 5.9, 2.7, 0.95, "tree（根目录）", "a.txt  b.txt  src/", GREEN, fs=9, sfs=7.2)
    arrow(ax, (3.45, 6.37), (4.25, 6.37))

    # 子 tree 与 blob（纵向排列，避免连线穿越方框）
    box(ax, 7.9, 6.55, 2.4, 0.75, "tree src/", "parser.c", GREEN, fs=8.5, sfs=7)
    box(ax, 10.9, 6.55, 2.4, 0.75, "blob parser.c", None, BLUE, fs=8.5)
    arrow(ax, (10.35, 6.92), (10.85, 6.92), color=LINE, lw=1.3)

    box(ax, 7.9, 5.6, 2.4, 0.62, "blob a.txt", None, BLUE, fs=8.5)
    box(ax, 7.9, 4.75, 2.4, 0.62, "blob b.txt", None, BLUE, fs=8.5)

    arrow(ax, (7.05, 6.75), (7.85, 6.9), color=LINE, lw=1.3)
    arrow(ax, (7.05, 6.35), (7.85, 5.91), color=LINE, lw=1.3)
    arrow(ax, (7.05, 6.15), (7.85, 5.06), color=LINE, lw=1.3)

    # 内容去重示意
    ax.text(0.5, 4.05, "内容寻址带来的自动去重（实测）", fontsize=9.8,
            fontweight="bold", color=RED)
    box(ax, 0.5, 2.65, 2.2, 0.8, "blob a.txt", "内容 hello", BLUE, fs=8.5, sfs=7)
    box(ax, 3.2, 2.65, 2.2, 0.8, "blob c.txt", "内容 hello", BLUE, fs=8.5, sfs=7)
    ax.text(5.6, 3.05, "→ 同一个 SHA，磁盘上只存一份", fontsize=8.4,
            color="#1e8449", va="center")
    ax.text(5.6, 2.72, "（实测：两个文件内容相同时 blob 总数不增加）",
            fontsize=7.6, color=LINE, va="center")

    # 要点
    ax.text(0.5, 2.05, "四个关键结论", fontsize=9.8, fontweight="bold", color=TEXT)
    pts = [
        "• blob 只存内容，不含文件名 —— 所以文件名改了不会产生新 blob",
        "• tree 存「名字 → blob」映射，所以文件名是有成本的",
        "• commit 存的是完整快照（一个 tree 的 SHA），不是 diff",
        "• 改一个字节就产生全新 blob，空间靠 packfile 的增量压缩省回来",
    ]
    for i, s in enumerate(pts):
        ax.text(0.5, 1.62 - i * 0.34, s, fontsize=8.4, color=TEXT)

    ax.text(0.5, 0.2,
            "实测：一个只有两个文件的首次提交 = 1 tree + 2 blob + 1 commit，共 4 个对象。",
            fontsize=8.2, color=LINE)

    _save(fig, "git-objects.svg")
'''


NEW_TCP = '''def tcp_states():
    """TCP 状态机（简化）"""
    fig, ax = plt.subplots(figsize=(10.8, 6.8))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8.4)
    ax.set_axis_off()
    ax.text(0.2, 8.0, "TCP 状态：左边是主动关闭方，右边是被动关闭方",
            fontsize=12.5, fontweight="bold", color=TEXT)

    # 顶部主线
    box(ax, 0.6, 6.4, 2.4, 0.8, "CLOSED", None, GREY, fs=9.5)
    box(ax, 4.0, 6.4, 3.0, 0.8, "ESTABLISHED", None, GREEN, fs=9.5)
    box(ax, 8.4, 6.4, 2.4, 0.8, "CLOSED", None, GREY, fs=9.5)
    arrow(ax, (3.05, 6.8), (3.95, 6.8))
    ax.text(3.12, 7.0, "三次握手", fontsize=7.8, color=RED)
    arrow(ax, (7.05, 6.8), (8.35, 6.8))
    ax.text(7.15, 7.0, "四次挥手", fontsize=7.8, color=RED)

    # 段落标题（放在最左/最右，避开连线）
    ax.text(0.6, 5.98, "主动关闭方", fontsize=9.4, fontweight="bold", color=RED)
    ax.text(11.5, 5.98, "被动关闭方", fontsize=9.4, fontweight="bold", color="#1e8449")

    # 主动关闭链
    act = [("FIN_WAIT_1", 5.25, PINK), ("FIN_WAIT_2", 4.35, PINK),
           ("TIME_WAIT（等 2MSL）", 3.45, ORANGE)]
    for i, (name, y, c) in enumerate(act):
        box(ax, 0.6, y, 3.6, 0.62, name, None, c, fs=8.6)
        if i > 0:
            arrow(ax, (1.2, y + 0.95), (1.2, y + 0.65), color=LINE, lw=1.2)

    # 被动关闭链
    pas = [("CLOSE_WAIT", 5.25, PURPLE), ("LAST_ACK", 4.35, PURPLE)]
    for i, (name, y, c) in enumerate(pas):
        box(ax, 9.3, y, 3.6, 0.62, name, None, c, fs=8.6)
        if i > 0:
            arrow(ax, (11.1, y + 0.95), (11.1, y + 0.65), color=LINE, lw=1.2)

    # 从 ESTABLISHED 分叉下去
    arrow(ax, (4.6, 6.35), (2.4, 5.9), color=RED, lw=1.4)
    arrow(ax, (6.4, 6.35), (11.0, 5.9), color="#1e8449", lw=1.4)

    # 关键提示
    ax.text(0.6, 2.95, "两个必须分清的状态", fontsize=10, fontweight="bold", color=TEXT)
    box(ax, 0.6, 1.85, 5.8, 0.85, "CLOSE_WAIT 堆积 = 应用忘了 close()", None, PINK, fs=9)
    ax.text(0.75, 1.55, "对端已关，我也回了 ACK，但我的代码还没关 → TCP 不会自己关。",
            fontsize=7.9, color=TEXT)
    ax.text(0.75, 1.25, "这是纯应用层的 bug，调内核参数一点用都没有。",
            fontsize=7.9, color=RED, fontweight="bold")

    box(ax, 7.0, 1.85, 6.0, 0.85, "TIME_WAIT 是正常的，别急着改内核", None, ORANGE, fs=9)
    ax.text(7.15, 1.55, "存在的两个理由：① 保证最后一个 ACK 能重发",
            fontsize=7.9, color=TEXT)
    ax.text(7.15, 1.25, "② 让旧连接的残留报文在网络中消亡，不串到新连接。",
            fontsize=7.9, color=TEXT)

    ax.text(0.6, 0.6,
            "排查：ss -tan | awk 'NR>1{print $1}' | sort | uniq -c | sort -rn",
            fontsize=8.4, color=LINE)
    ax.text(0.6, 0.25,
            "真正的解法是减少短连接（连接池 / 长连接），而不是调 tcp_fin_timeout。",
            fontsize=8.4, color=LINE)

    _save(fig, "net-tcp-states.svg")
'''


t = replace_fn(t, "git_objects", NEW_GIT)
print("已重写 git_objects")

t = replace_fn(t, "tcp_states", NEW_TCP)
print("已重写 tcp_states")

# 火焰图：底部文字下移，避免与说明重叠
t = t.replace('        ax.text(0.5, 1.55 - i * 0.32, s, fontsize=8.4, color=TEXT)',
              '        ax.text(0.5, 1.55 - i * 0.305, s, fontsize=8.4, color=TEXT)')
t = t.replace('''    ax.text(0.5, 0.15,
            "生成：perf record -F 99 -g -p <pid> -- sleep 30  →  perf script  →  flamegraph.pl",
            fontsize=8.2, color=LINE)''',
              '''    ax.text(0.5, -0.75,
            "生成：perf record -F 99 -g -p <pid> -- sleep 30  →  perf script  →  flamegraph.pl",
            fontsize=8.2, color=LINE)''')
print("已调整火焰图底部文字")

io.open(P, "w", encoding="utf-8", newline="\n").write(t)
