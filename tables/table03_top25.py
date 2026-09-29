"""Table 3: the 25 occupations with the highest BAIOE exposure in 2025."""
from _common import *
def rows():
    occ = occupation_exposure('2025'); order = sorted(occ, key=lambda s: occ[s][1], reverse=True)  # stable; ties keep SOC-code order
    return [(i + 1, occ[s][0], occ[s][1]) for i, s in enumerate(order[:25])]
if __name__ == '__main__':
    R = rows(); write_csv('table03_top25.csv', ['Rank', 'Occupation', 'Exposure 2025'], R)
    L = ['\\begin{table}[htbp]\\centering', '\\caption{Top 25 Most-Exposed Occupations by BAIOE, 2025}\\label{tab:top25}', '\\begin{tabular}{lr}\\toprule', 'Occupation & Rank \\\\ \\midrule']
    L += [f'{tex_escape(t)} & {r} \\\\' for r, t, _ in R]
    L += ['\\bottomrule\\end{tabular}', '\\begin{minipage}{0.95\\linewidth}\\footnotesize \\textit{Notes:} This table reports the 25 occupations with the highest BAIOE exposure in 2025. Occupations are listed in descending order of exposure, so Rank 1 indicates the most-exposed occupation. BAIOE scores are omitted for readability.\\end{minipage}', '\\end{table}']
    write_tex('table03_top25.tex', '\n'.join(L)); print('Table 3:', len(R), 'rows; #1', R[0][1], R[0][2])
