import io, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = "sidebars.ts"
t = io.open(p, encoding="utf-8").read()
orig = t

n1 = t.count("',,")
t = t.replace("',,", "',")
print("double comma fixed:", n1)

t, n2 = re.subn(r"('[^'\n]+')(\n\s+')", r"\1,\2", t)
print("missing comma added:", n2)

if t != orig:
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(t)
    print("written")
else:
    print("no change")
