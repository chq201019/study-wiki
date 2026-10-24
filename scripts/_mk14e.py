import io
p = "scripts/gen_diagrams14.py"
lines = io.open(p, encoding="utf-8").read().split(chr(10))
out = []
skip = False
for i, l in enumerate(lines):
    if l.startswith("if __name__ =="):
        skip = True
        continue
    if skip:
        # 跳过原来的 main 块（缩进的语句和 print）
        if l.startswith("    ") or l.strip() == "" or l.strip().startswith("print"):
            continue
        skip = False
    out.append(l)

while out and out[-1].strip() == "":
    out.pop()

out.append("")
out.append("")
out.append("    _save(fig, " + chr(34) + "stm32-deadtime.svg" + chr(34) + ")")
out.append("")
out.append("")
out.append("    _save(fig, " + chr(34) + "linux-shell-pipeline.svg" + chr(34) + ")")
out.append("")
out.append("")
out.append("if __name__ == " + chr(34) + "__main__" + chr(34) + ":")
for fn in ["iterator_protocol", "template_instantiation", "security_boundary",
           "esp32_sleep_current", "stm32_deadtime", "shell_pipeline"]:
    out.append("    " + fn + "()")
out.append("    print(" + chr(34) + "done" + chr(34) + ")")
out.append("")

io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(out))
print("restructured")