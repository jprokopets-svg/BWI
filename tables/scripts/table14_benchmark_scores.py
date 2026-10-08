"""Table 14: every benchmark-ability pair that was selected in any year, with its transferability weight (T, 0-10)
and its capability score (C, 0-10) in each year it was selected. Blank = not selected or no verifiable score that year.
Reads only data/."""
from _common import *
def fmt(v, d=1): return '' if v in ('', None) else f'{float(v):.{d}f}'
def rows():
    T, C, cat = {}, {}, {}
    for r in read('benchmark_ability_year.csv'):
        if not r['benchmark_name'] or r.get('exposure_source') == 'carry_forward_2025': continue
        k = (r['onet_ability'], r['benchmark_name']); cat[k] = r['ability_category']
        if r['transferability_weight']: T[k] = r['transferability_weight']
        if r['human_comparative_score_0_10']: C[(k, r['year'])] = r['human_comparative_score_0_10']
    out = [[a, cat[(a, b)], b, fmt(T.get((a, b)))] + [fmt(C.get(((a, b), y))) for y in YEARS] for a, b in sorted(T, key=lambda k: (k[0], k[1]))]
    return out
if __name__ == '__main__':
    R = rows(); write_csv('table14_benchmark_scores.csv', ['Ability', 'Category', 'Benchmark', 'T'] + [f'C {y}' for y in YEARS], R)
    L = ['\\begin{longtable}{lp{4.6cm}r' + 'r' * len(YEARS) + '}', '\\caption{All selected benchmarks: transferability (T) and capability (C) by year}\\label{tab:benchmarkscores} \\\\ \\toprule',
         'Ability & Benchmark & T & ' + ' & '.join(YEARS) + ' \\\\ \\midrule \\endfirsthead', '\\toprule Ability & Benchmark & T & ' + ' & '.join(YEARS) + ' \\\\ \\midrule \\endhead',
         '\\midrule \\multicolumn{' + str(3 + len(YEARS)) + '}{r}{\\footnotesize\\textit{continued on next page}} \\\\ \\endfoot', '\\bottomrule \\endlastfoot']
    for r in R: L.append(f"{tex_escape(r[0])} & {tex_escape(r[2])} & {r[3]} & " + ' & '.join(r[4:]) + ' \\\\')
    L += [f'\\multicolumn{{{3 + len(YEARS)}}}{{p{{0.95\\linewidth}}}}{{\\footnotesize \\textit{{Notes:}} One row per benchmark-ability pair ({len(R)} pairs). T is rated once per pair; C is rated for each year the benchmark was selected and had a verifiable result. Columns are the capability score in that year. Carried-forward 2026 cells are not shown.{vintage_note()}}}', '\\end{longtable}']
    write_tex('table14_benchmark_scores.tex', '\n'.join(L)); print('table14:', len(R), 'pairs')
