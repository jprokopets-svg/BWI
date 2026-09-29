"""2026 extension: the same top-25 and fastest-growing tables using the 2026 vintage (cutoff = the run date, 28 September 2026).
  table_top25_2026        top 25 by 2026 exposure
  table_fastest25_2020_2026  top 25 by 2020-2026 growth"""
from _common import *
def top25(occ):
    order = sorted(occ, key=lambda s: occ[s][1], reverse=True); return [(i + 1, occ[s][0], occ[s][1]) for i, s in enumerate(order[:25])]
def fastest25(o0, o5):
    d = {s: o5[s][1] - o0[s][1] for s in o5 if s in o0}; order = sorted(d, key=lambda s: d[s], reverse=True)
    return [(i + 1, o5[s][0], o0[s][1], o5[s][1], round(d[s], 2)) for i, s in enumerate(order[:25])]
def tex(name, caption, rows, notes):
    L = ['\\begin{table}[htbp]\\centering', f'\\caption{{{caption}}}\\label{{tab:{name}}}', '\\begin{tabular}{lr}\\toprule', 'Occupation & Rank \\\\ \\midrule']
    L += [f'{tex_escape(r[1])} & {r[0]} \\\\' for r in rows]
    L += ['\\bottomrule\\end{tabular}', f'\\begin{{minipage}}{{0.95\\linewidth}}\\footnotesize \\textit{{Notes:}} {notes}\\end{{minipage}}', '\\end{table}']
    write_tex(f'{name}.tex', '\n'.join(L))
if __name__ == '__main__':
    o0, o6 = occupation_exposure('2020'), occupation_exposure('2026')
    if not o6: raise SystemExit('no 2026 rows in data/occupation_exposure.csv')
    R = top25(o6); write_csv('table_top25_2026.csv', ['Rank', 'Occupation', 'Exposure 2026'], R)
    tex('table_top25_2026', 'Top 25 Most-Exposed Occupations by BAIOE, 2026', R, 'This table reports the 25 occupations with the highest BAIOE exposure in 2026, using benchmark results published up to 28 September 2026. Rank 1 indicates the most-exposed occupation. BAIOE scores are omitted for readability.')
    R2 = fastest25(o0, o6); write_csv('table_fastest25_2020_2026.csv', ['Rank', 'Occupation', 'Exposure 2020', 'Exposure 2026', 'Delta'], R2)
    tex('table_fastest25_2020_2026', 'Top 25 Fastest-Growing Occupations by BAIOE Exposure, 2020--2026', R2, 'This table reports the 25 occupations with the largest increase in BAIOE exposure between 2020 and 2026 (2026 cutoff: 28 September 2026). Rank 1 indicates the fastest-growing occupation. BAIOE levels and growth values are omitted for readability.')
    print('2026 top 5:'); [print(f'  {r[0]}. {r[1]} {r[2]}') for r in R[:5]]; print('2020-2026 growth top 5:'); [print(f'  {r[0]}. {r[1]} {r[4]:+.2f}') for r in R2[:5]]
