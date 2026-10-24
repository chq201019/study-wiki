import sys, os
sys.path.insert(0, 'scripts')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gen_diagrams11 as g

def save_png(fig, name):
    os.makedirs('_preview', exist_ok=True)
    out = os.path.join('_preview', name.replace('.svg', '.png'))
    fig.savefig(out, format='png', bbox_inches='tight', transparent=True, dpi=150)
    plt.close(fig)
    print('wrote', out)

g._save = save_png
g.py_exception_tree()
g.cpp_operator_resolution()
g.container_isolation()