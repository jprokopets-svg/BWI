"""Four variants of the top-25 tables that handle postsecondary teachers explicitly.
Teacher set = every occupation with SOC code 25-1xxx ("..., Postsecondary").
  table_top25_no_teachers          top 25 by 2026 exposure, teacher set excluded
  table_fastest25_no_teachers      top 25 by 2020-2025 growth, teacher set excluded
  table_top25_teachers_bundled     top 25 by 2026 exposure with all teachers collapsed into one row
  table_fastest25_teachers_bundled top 25 by growth, same bundle
The bundle's exposure per year is the employment-weighted mean over teacher occupations, using BLS OEWS May 2024
national employment (data/oews_employment_2024.csv). O*NET occupations without an OEWS match get the mean employment
of the matched teacher occupations."""
from _common import *
BUNDLE = 'Postsecondary Teachers (all fields)'
def is_teacher(soc): return soc.startswith('25-1')
def employment():
    e = {r['soc_code']: float(r['employment_2024']) for r in read('oews_employment_2024.csv') if r['employment_2024'] not in ('', 'nan')}
    return e
def panel(year):
    return occupation_exposure(year)
def bundled(year, emp):
    occ = panel(year); teachers = {s: v for s, v in occ.items() if is_teacher(s)}
    matched = {s: emp[s[:7]] for s in teachers if s[:7] in emp}; fill = sum(matched.values()) / len(matched)
    w = {s: matched.get(s, fill) for s in teachers}
    bundle = sum(occ[s][1] * w[s] for s in teachers) / sum(w.values())
    out = {s: v for s, v in occ.items() if not is_teacher(s)}; out['25-1000.00'] = (BUNDLE, round(bundle, 2))
    return out, len(teachers), len(matched)
def top25(occ):
    order = sorted(occ, key=lambda s: occ[s][1], reverse=True); return [(i + 1, occ[s][0], occ[s][1]) for i, s in enumerate(order[:25])]
def fastest25(o0, o5):
    d = {s: o5[s][1] - o0[s][1] for s in o5 if s in o0}; order = sorted(d, key=lambda s: d[s], reverse=True)
    return [(i + 1, o5[s][0], o0[s][1], o5[s][1], round(d[s], 2)) for i, s in enumerate(order[:25])]
def tex(name, caption, rows, notes, growth=False):
    L = ['\\begin{table}[htbp]\\centering', f'\\caption{{{caption}}}\\label{{tab:{name}}}', '\\begin{tabular}{lr}\\toprule', 'Occupation & Rank \\\\ \\midrule']
    L += [f'{tex_escape(r[1])} & {r[0]} \\\\' for r in rows]
    L += ['\\bottomrule\\end{tabular}', f'\\begin{{minipage}}{{0.95\\linewidth}}\\footnotesize \\textit{{Notes:}} {notes}\\end{{minipage}}', '\\end{table}']
    write_tex(f'{name}.tex', '\n'.join(L))
if __name__ == '__main__':
    emp = employment(); o0, o5 = panel(BASE), panel(LATEST); teachers = sorted(s for s in o5 if is_teacher(s)); print(f'Teacher set (SOC 25-1xxx): {len(teachers)} occupations')
    ex0 = {s: v for s, v in o0.items() if not is_teacher(s)}; ex5 = {s: v for s, v in o5.items() if not is_teacher(s)}
    n_ex = f'All {len(teachers)} postsecondary teaching occupations (SOC 25-1xxx) are excluded.'
    R = top25(ex5); write_csv('table_top25_no_teachers.csv', ['Rank', 'Occupation', f'Exposure {LATEST}'], R)
    tex('table_top25_no_teachers', 'Top 25 Most-Exposed Occupations by BAIOE, 2026, excluding postsecondary teachers', R, f'This table reports the 25 occupations with the highest BAIOE exposure in 2026. {n_ex} Rank 1 indicates the most-exposed remaining occupation. BAIOE scores are omitted for readability.{vintage_note()}')
    R2 = fastest25(ex0, ex5); write_csv('table_fastest25_no_teachers.csv', ['Rank', 'Occupation', f'Exposure {BASE}', f'Exposure {LATEST}', 'Delta'], R2)
    tex('table_fastest25_no_teachers', 'Top 25 Fastest-Growing Occupations by BAIOE Exposure, 2020--2026, excluding postsecondary teachers', R2, f'This table reports the 25 occupations with the largest increase in BAIOE exposure between 2020 and 2026. {n_ex} Rank 1 indicates the fastest-growing remaining occupation. BAIOE levels and growth values are omitted for readability.{vintage_note()}')
    b0, nt, nm = bundled(BASE, emp); b5, _, _ = bundled(LATEST, emp)
    n_b = f'All {nt} postsecondary teaching occupations (SOC 25-1xxx) are collapsed into one row, "{BUNDLE}", whose exposure is the employment-weighted mean of the teaching occupations using BLS OEWS May 2024 national employment ({nm} of {nt} matched; unmatched occupations receive the mean employment of the matched ones). All other occupations are unchanged.'
    R3 = top25(b5); write_csv('table_top25_teachers_bundled.csv', ['Rank', 'Occupation', f'Exposure {LATEST}'], R3)
    tex('table_top25_teachers_bundled', 'Top 25 Most-Exposed Occupations by BAIOE, 2026, postsecondary teachers bundled', R3, f'This table reports the 25 occupations with the highest BAIOE exposure in 2026. {n_b} Rank 1 indicates the most-exposed occupation. BAIOE scores are omitted for readability.{vintage_note()}')
    R4 = fastest25(b0, b5); write_csv('table_fastest25_teachers_bundled.csv', ['Rank', 'Occupation', f'Exposure {BASE}', f'Exposure {LATEST}', 'Delta'], R4)
    tex('table_fastest25_teachers_bundled', 'Top 25 Fastest-Growing Occupations by BAIOE Exposure, 2020--2026, postsecondary teachers bundled', R4, f'This table reports the 25 occupations with the largest increase in BAIOE exposure between 2020 and 2026. {n_b} Rank 1 indicates the fastest-growing occupation. BAIOE levels and growth values are omitted for readability.{vintage_note()}')
    for name, R in (('top25_no_teachers', R), ('fastest25_no_teachers', R2), ('top25_teachers_bundled', R3), ('fastest25_teachers_bundled', R4)):
        print(f'\n{name}: top 5'); [print(f'  {r[0]:2}. {r[1][:55]:55} {r[-1]}') for r in R[:5]]
    allb = sorted(b5, key=lambda s: b5[s][1], reverse=True); rb = allb.index('25-1000.00') + 1
    d = {s: b5[s][1] - b0[s][1] for s in b5 if s in b0}; allg = sorted(d, key=lambda s: d[s], reverse=True); rg = allg.index('25-1000.00') + 1
    print(f'\nBundle "{BUNDLE}": 2026 exposure {b5["25-1000.00"][1]:.2f}, rank {rb} of {len(allb)}; growth {d["25-1000.00"]:+.2f}, rank {rg} of {len(allg)}')
