import io
p = "scripts/gen_diagrams14.py"
t = io.open(p, encoding="utf-8").read()
if "stm32_deadtime()" not in t.split("if __name__")[-1]:
    t = t.rstrip() + chr(10) + chr(10) + "if __name__ == " + chr(34) + "__main__" + chr(34) + ":" + chr(10)
    for fn in ["iterator_protocol", "template_instantiation", "security_boundary",
               "esp32_sleep_current", "stm32_deadtime", "shell_pipeline"]:
        t += "    " + fn + "()" + chr(10)
    t += "    print(" + chr(34) + "done" + chr(34) + ")" + chr(10)
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
    print("added main block")
else:
    print("main block exists")