import os
src = open("scripts/gen_diagrams10.py", encoding="utf-8").read()
src = src.replace('format="svg"', 'format="png", dpi=150')
src = src.replace('OUT = os.path.join("static", "img", "diagrams")', 'OUT = "_preview"')
src = src.replace('p = os.path.join(OUT, name)', 'p = os.path.join(OUT, name.replace(".svg", ".png"))')
exec(compile(src, "prev", "exec"))