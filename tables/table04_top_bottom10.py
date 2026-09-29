"""Table 4: the ten most- and ten least-exposed occupations in 2025 (Panel B rank 1 = least exposed)."""
from _common import *
def rows():
    occ = occupation_exposure('2025')
    # stable descending sort over occupations in SOC-code (file) order; ties keep that order, as in the pipeline
    order = sorted(occ, key=lambda s: occ[s][1], reverse=True)
    top = [('Panel A: Most-exposed occupations', i + 1, occ[s][0], occ[s][1]) for i, s in enumerate(order[:10])]
    bot = [('Panel B: Least-exposed occupations', i + 1, occ[s][0], occ[s][1]) for i, s in enumerate(reversed(order[-10:]))]
    return top + bot
if __name__ == '__main__':
    R = rows(); write_csv('table04_top_bottom10.csv', ['Panel', 'Rank', 'Occupation', 'Exposure 2025'], R)
    L = ['\\begin{table}[htbp]\\centering', '\\caption{Most- and Least-Exposed Occupations by BAIOE, 2025}\\label{tab:topbottom10}', '\\begin{tabular}{lr}\\toprule', 'Occupation & Rank \\\\ \\midrule']
    cur = None
    for p, r, t, _ in R:
        if p != cur: L.append(f'\\multicolumn{{2}}{{l}}{{\\textit{{{p}}}}} \\\\'); cur = p
        L.append(f'{tex_escape(t)} & {r} \\\\')
    L += ['\\bottomrule\\end{tabular}', '\\begin{minipage}{0.95\\linewidth}\\footnotesize \\textit{Notes:} This table reports the ten most-exposed and ten least-exposed occupations according to BAIOE exposure in 2025. In Panel A, Rank 1 denotes the most-exposed occupation. In Panel B, Rank 1 denotes the least-exposed occupation. BAIOE scores are omitted for readability.\\end{minipage}', '\\end{table}']
    write_tex('table04_top_bottom10.tex', '\n'.join(L)); print('Table 4:', len(R), 'rows; least exposed #1', R[10][2], R[10][3])
