"""Table 13: every benchmark selected for 2026 with its capability score (C, 0-10), transferability weight (T, 0-10)
and ability exposure (C x T). Carried-forward abilities show the 2025 benchmark and values. Reads only data/."""
from _common import *
def fmt(v, d=2): return '' if v in ('', None) else f'{float(v):.{d}f}'
def rows():
    out = []
    for r in read('benchmark_ability_year.csv'):
        if r['year'] != LATEST: continue
        src = r.get('exposure_source', '')
        if src == 'carry_forward_2025':
            p = next(x for x in read('benchmark_ability_year.csv') if x['onet_ability'] == r['onet_ability'] and x['year'] == '2025')
            out.append([r['onet_ability'], r['ability_category'], p['benchmark_name'], p['human_comparative_score_0_10'], p['transferability_weight'], r['ability_exposure'], 'carried from 2025'])
        elif r['ability_exposure'] and r['benchmark_name']:
            out.append([r['onet_ability'], r['ability_category'], r['benchmark_name'], r['human_comparative_score_0_10'], r['transferability_weight'], r['ability_exposure'], 'measured'])
    return sorted(out, key=lambda x: -float(x[5]))
if __name__ == '__main__':
    R = rows(); write_csv('table13_benchmarks_2026.csv', ['Ability', 'Category', 'Benchmark', 'C', 'T', 'Exposure', 'Status'], R)
    L = ['\\begin{longtable}{llp{5.2cm}rrr}', '\\caption{Benchmarks behind the 2026 ability scores: capability (C), transferability (T) and exposure (C $\\times$ T)}\\label{tab:benchmarks2026} \\\\ \\toprule',
         'Ability & Category & Benchmark & C & T & Exposure \\\\ \\midrule \\endfirsthead', '\\toprule Ability & Category & Benchmark & C & T & Exposure \\\\ \\midrule \\endhead', '\\midrule \\multicolumn{6}{r}{\\footnotesize\\textit{continued on next page}} \\\\ \\endfoot', '\\bottomrule \\endlastfoot']
    for a, c, b, C, T, E, s in R:
        L.append(f"{tex_escape(a)} & {c} & {tex_escape(b)}{' (2025)' if s.startswith('carried') else ''} & {fmt(C,1)} & {fmt(T,1)} & {fmt(E,1)} \\\\")
    L += [f'\\multicolumn{{6}}{{p{{0.95\\linewidth}}}}{{\\footnotesize \\textit{{Notes:}} One benchmark per ability. C is the human-comparative capability score (5 = matches the median relevant worker, 10 = above the entire population); T is the transferability weight (10 = the benchmark score is close to a direct measurement of the ability). Exposure = C $\\times$ T on a 0--100 scale. Abilities marked (2025) carry their 2025 benchmark and values forward because no verifiable 2026 result was found. The eight abilities with no benchmark in any year are not listed and enter the occupation scores at zero exposure.{vintage_note()}}}', '\\end{longtable}']
    write_tex('table13_benchmarks_2026.tex', '\n'.join(L)); print('table13:', len(R), 'rows')
