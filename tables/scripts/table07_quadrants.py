"""Table 7: capability-adoption quadrants, BWI vs AEI adoption.
VINTAGE is the headline year.
Occupations with observed (nonzero) AEI use are ranked on both measures; a median split defines the quadrants;
the ten most divergent occupations (largest rank gap) are listed per quadrant."""
from _common import *
VINTAGE = LATEST
PANELS = [('latent', 'Panel A: Latent exposure -- high BWI, low adoption'), ('active', 'Panel B: Active transformation -- high BWI, high adoption'),
          ('low', 'Panel C: Low pressure -- low BWI, low adoption'), ('ahead', 'Panel D: Adoption ahead -- low BWI, high adoption')]
def rows():
    a = aei(); b = occupation_exposure_6digit(VINTAGE); m = sorted(s for s in set(a) & set(b) if a[s][1] > 0); n = len(m)
    br = rank_desc({s: b[s][1] for s in m}); ar = rank_desc({s: a[s][1] for s in m}); med = n / 2.0
    q = {k: [] for k, _ in PANELS}
    for s in m:
        hb, ha = br[s] <= med, ar[s] <= med
        key = 'active' if hb and ha else 'latent' if hb else 'ahead' if ha else 'low'
        q[key].append((b[s][0], int(br[s]), int(ar[s]), abs(br[s] - ar[s])))
    out = []
    for k, label in PANELS:
        e = sorted(q[k], key=lambda x: -x[3])[:10]; out += [(label, t, r1, r2) for t, r1, r2, _ in e]
    return out
if __name__ == '__main__':
    R = rows(); write_csv('table07_quadrants.csv', ['Panel', 'Occupation', 'BWI Rank', 'AEI Rank'], R)
    L = ['\\begin{table}[htbp]\\centering', '\\caption{BWI capability exposure and AEI adoption quadrants, 2026}\\label{tab:quadrants}', '\\begin{tabular}{l}\\toprule', 'Occupation \\\\ \\midrule']
    cur = None
    for p, t, *_ in R:
        if p != cur: L.append(f'\\textit{{{tex_escape(p)}}} \\\\'); cur = p
        L.append(f'{tex_escape(t)} \\\\')
    L += ['\\bottomrule\\end{tabular}', '\\begin{minipage}{0.95\\linewidth}\\footnotesize \\textit{Notes:} The table reports representative occupations in each quadrant of the BWI--AEI comparison. The quadrants compare capability-side exposure measured by BWI with realized AI use measured by AEI. Occupations in low-adoption cells should be interpreted as having low or unobserved AEI adoption rather than as precisely ordered within that group. Low BWI should be interpreted as low measured benchmark-based exposure, not necessarily as immunity from future AI effects.' + vintage_note() + '\\end{minipage}', '\\end{table}']
    write_tex('table07_quadrants.tex', '\n'.join(L)); print('Table 7:', len(R), 'rows; first', R[0][1])
