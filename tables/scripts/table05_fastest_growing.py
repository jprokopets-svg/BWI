"""Table 5: the 25 occupations with the largest increase in BAIOE exposure, 2020 to 2025."""
from _common import *
def rows():
    e0, e5 = occupation_exposure(BASE), occupation_exposure(LATEST)
    d = {s: e5[s][1] - e0[s][1] for s in e5 if s in e0}; order = sorted(d, key=lambda s: d[s], reverse=True)  # stable; ties keep SOC-code order
    return [(i + 1, e5[s][0], e0[s][1], e5[s][1], round(d[s], 2)) for i, s in enumerate(order[:25])]
if __name__ == '__main__':
    R = rows(); write_csv('table05_fastest_growing.csv', ['Rank', 'Occupation', f'Exposure {BASE}', f'Exposure {LATEST}', 'Delta'], R)
    L = ['\\begin{table}[htbp]\\centering', '\\caption{Top 25 Fastest-Growing Occupations by BAIOE Exposure, 2020--2026}\\label{tab:fastest}', '\\begin{tabular}{lr}\\toprule', 'Occupation & Rank \\\\ \\midrule']
    L += [f'{tex_escape(t)} & {r} \\\\' for r, t, *_ in R]
    L += ['\\bottomrule\\end{tabular}', f'\\begin{{minipage}}{{0.95\\linewidth}}\\footnotesize \\textit{{Notes:}} This table reports the 25 occupations with the largest increase in BAIOE exposure between 2020 and 2026. Occupations are listed in descending order of exposure growth, so Rank 1 indicates the fastest-growing occupation. BAIOE levels and growth values are omitted for readability.{vintage_note()}\end{{minipage}}', '\\end{table}']
    write_tex('table05_fastest_growing.tex', '\n'.join(L)); print('Table 5:', len(R), 'rows; #1', R[0][1], f'{R[0][4]:+.2f}')
