import io
p = "scripts/gen_diagrams15.py"
t = io.open(p, encoding="utf-8").read()
if "__main__" not in t:
    t = t.rstrip() + chr(10) + chr(10) + "if __name__ == " + chr(34) + "__main__" + chr(34) + ":" + chr(10)
    t += "    py_list_growth()" + chr(10)
    t += "    c_pointer_array()" + chr(10)
    t += "    print(" + chr(34) + "done" + chr(34) + ")" + chr(10)
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
    print("added main")
else:
    print("has main")