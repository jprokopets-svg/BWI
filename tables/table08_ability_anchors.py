"""Table 8: all 52 O*NET abilities with their 2025 exposure score and benchmark anchor.
Measured abilities first (descending exposure, ties alphabetical), then abilities mapped but without a 2025 value, then never-mapped abilities."""
from _common import *
def rows():
    ab = ability_exposure('2025'); mapped_any = {r['onet_ability'] for r in read('ability_year_exposure.csv')}
    universe = {r['onet_ability']: r['ability_category'] for r in read('ability_year_exposure.csv')}
    # abilities never mapped do not appear in ability_year_exposure.csv; recover the full 52 from the O*NET weights file
    all52 = sorted({r['onet_ability'] for r in read('onet_ability_weights.csv')})
    measured = [(a, float(ab[a]['exposure']), ab[a]['anchor_benchmark']) for a in all52 if a in ab and ab[a]['exposure'] != '']
    measured.sort(key=lambda x: (-x[1], x[0]))
    null25 = [(a, None, None) for a in all52 if a in ab and ab[a]['exposure'] == '']
    never = [(a, None, None) for a in all52 if a not in mapped_any]
    return measured + null25 + never
if __name__ == '__main__':
    R = rows(); write_csv('table08_ability_anchors.csv', ['Ability', 'Exposure 2025', 'Benchmark Anchor'], [(a, '' if e is None else f'{e:.2f}', b or '') for a, e, b in R])
    L = ['\\begin{longtable}{lrp{7cm}}', '\\caption{O*NET abilities, 2025 exposure scores, and benchmark anchors}\\label{tab:anchors} \\\\ \\toprule', 'O*NET ability & 2025 exposure & Benchmark anchor \\\\ \\midrule \\endfirsthead', '\\toprule O*NET ability & 2025 exposure & Benchmark anchor \\\\ \\midrule \\endhead', '\\midrule \\multicolumn{3}{r}{\\textit{Continued on next page}} \\\\ \\endfoot', '\\bottomrule \\endlastfoot']
    L += [f'{tex_escape(a)} & {"--" if e is None else f"{e:.2f}"} & {tex_escape(b) if b else "--"} \\\\' for a, e, b in R]
    L += ['\\multicolumn{3}{p{0.95\\linewidth}}{\\footnotesize \\textit{Notes:} The table reports the benchmark anchor and 2025 ability-level exposure score for each O*NET ability. Exposure scores are measured on the BAIOE ability-level exposure scale. Benchmark anchors indicate the benchmark used as the most direct public signal for the corresponding ability in 2025. Dashes indicate abilities for which no credible or gradable benchmark analogue was identified. Values are rounded to two decimals.} \\\\', '\\end{longtable}']
    write_tex('table08_ability_anchors.tex', '\n'.join(L)); print('Table 8:', len(R), 'rows;', sum(1 for r in R if r[1] is not None), 'measured; #1', R[0])
