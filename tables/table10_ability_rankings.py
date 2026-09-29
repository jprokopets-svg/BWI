"""Table 10: O*NET abilities ranked by 2025 exposure (abilities without a 2025 value are excluded)."""
from _common import *
CAT = {'cognitive': 'Cognitive', 'psychomotor': 'Psychomotor', 'physical': 'Physical', 'sensory': 'Sensory'}
def rows():
    ab = ability_exposure('2025'); m = [(a, float(r['exposure']), CAT[r['ability_category']]) for a, r in ab.items() if r['exposure'] != '']
    m.sort(key=lambda x: (-x[1], x[0])); return [(i + 1, a, c, e) for i, (a, e, c) in enumerate(m)]
if __name__ == '__main__':
    R = rows(); write_csv('table10_ability_rankings.csv', ['Rank', 'Ability', 'Category', 'Exposure 2025'], R)
    L = ['\\begin{table}[htbp]\\centering', '\\caption{O*NET abilities ranked by AI exposure, 2025}\\label{tab:abilityrank}', '\\begin{tabular}{rll}\\toprule', 'Rank & Ability & Category \\\\ \\midrule']
    L += [f'{r} & {tex_escape(a)} & {c} \\\\' for r, a, c, _ in R]
    L += ['\\bottomrule\\end{tabular}', '\\begin{minipage}{0.95\\linewidth}\\footnotesize \\textit{Notes:} Abilities are ranked in descending order of measured AI exposure in 2025. Rank 1 denotes the ability with the highest measured exposure. Quantitative exposure scores are omitted for readability. Abilities without a measured 2025 exposure value are excluded.\\end{minipage}', '\\end{table}']
    write_tex('table10_ability_rankings.tex', '\n'.join(L)); print('Table 10:', len(R), 'rows; #1', R[0][1])
