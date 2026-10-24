import io, re
p = "scripts/gen_diagrams14.py"
t = io.open(p, encoding="utf-8").read()

# 1) 移除末尾两个错位的 _save
t = t.replace("    _save(fig, " + chr(34) + "stm32-deadtime.svg" + chr(34) + ")", "@@DEADTIME_SAVE@@")
t = t.replace("    _save(fig, " + chr(34) + "linux-shell-pipeline.svg" + chr(34) + ")", "@@PIPE_SAVE@@")

# 2) deadtime：在其函数体最后一段文字后插入（"死区太大" 那句）
dead_anchor = chr(34) + "死区太大则波形失真效率下降；太小则直通烧管。查 MOS 手册的 td(off) 与 td(on)。" + chr(34)
idx = t.index(dead_anchor)
end_of_dead = t.index(chr(10) + chr(10), idx)
t = t[:end_of_dead] + chr(10) + chr(10) + "    _save(fig, " + chr(34) + "stm32-deadtime.svg" + chr(34) + ")" + t[end_of_dead:]
t = t.replace("@@DEADTIME_SAVE@@", "")

# 3) pipeline：在其函数最后一行后插入
pipe_anchor = chr(34) + "排查手段：strace -f -e trace=pipe,read,write 能看到每个进程怎么读写管道。" + chr(34)
idx2 = t.index(pipe_anchor)
end_of_pipe = t.index(chr(10) + chr(10), idx2)
t = t[:end_of_pipe] + chr(10) + chr(10) + "    _save(fig, " + chr(34) + "linux-shell-pipeline.svg" + chr(34) + ")" + t[end_of_pipe:]
t = t.replace("@@PIPE_SAVE@@", "")

# 4) 清理多余空行
t = re.sub(r"\n{4,}", chr(10)+chr(10), t)
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
print("repositioned saves")