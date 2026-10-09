"""Table 8: all 52 O*NET abilities with their 2026 exposure score and benchmark anchor.
Measured abilities first (descending exposure, ties alphabetical), then abilities mapped but without a 2026 value, then the eight abilities with no benchmark in any year, which enter the occupation scores at zero exposure."""
from _common import *
ZF = 'no benchmark observed (counted as zero)'
def rows():
    ab = ability_exposure(LATEST); all52 = sorted({r['onet_ability'] for r in read('onet_ability_weights.csv')})
    measured = [(a, float(ab[a]['exposure']), ab[a]['anchor_benchmark']) for a in all52 if a in ab and ab[a]['exposure'] != '' and ab[a]['resolution'] != ZF]
    measured.sort(key=lambda x: (-x[1], x[0]))
    # abilities without a 2026 value: mapped-but-unscored first, then never mapped in 2026, each alphabetical
    null_mapped = [(a, None, None) for a in all52 if a in ab and ab[a]['exposure'] == '' and ab[a]['resolution'] != 'no adequate benchmark']
    never = [(a, 0.0, 'no benchmark observed (counted as zero)') for a in all52 if a in ab and ab[a]['resolution'] == ZF]
    return measured + null_mapped + never
if __name__ == '__main__':
    R = rows(); write_csv('table08_ability_anchors.csv', ['Ability', f'Exposure {LATEST}', 'Benchmark Anchor'], [(a, '' if e is None else f'{e:.2f}', b or '') for a, e, b in R])
    L = ['\\begin{longtable}{lrp{7cm}}', '\\caption{O*NET abilities, 2026 exposure scores, and benchmark anchors}\\label{tab:anchors} \\\\ \\toprule', 'O*NET ability & 2026 exposure & Benchmark anchor \\\\ \\midrule \\endfirsthead', '\\toprule O*NET ability & 2026 exposure & Benchmark anchor \\\\ \\midrule \\endhead', '\\midrule \\multicolumn{3}{r}{\\textit{Continued on next page}} \\\\ \\endfoot', '\\bottomrule \\endlastfoot']
    L += [(f'{tex_escape(a)} & {e:.2f} & {tex_escape(b)} \\\\' if e is not None else f'{tex_escape(a)} & \\multicolumn{{1}}{{c}}{{--}} & \\multicolumn{{1}}{{c}}{{--}} \\\\') for a, e, b in R]
    L += [f'\\multicolumn{{3}}{{p{{0.95\\linewidth}}}}{{\\footnotesize \\textit{{Notes:}} The table reports the benchmark anchor and 2026 ability-level exposure score for each O*NET ability. Exposure scores are measured on the BWI ability-level exposure scale. Benchmark anchors indicate the benchmark used as the most direct public signal for the corresponding ability in 2026. Dashes indicate abilities for which no credible or gradable benchmark analogue was identified. Values are rounded to two decimals.{vintage_note()}}} \\', '\\end{longtable}']
    write_tex('table08_ability_anchors.tex', '\n'.join(L)); print('Table 8:', len(R), 'rows;', sum(1 for r in R if r[1] is not None), 'measured; #1', R[0])
