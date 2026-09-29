"""Table 9: ability-level decomposition of the 2026 BAIOE score for the two most- and two least-exposed occupations.
Occupation score = sum(exposure x weight) / sum(weight) over the abilities kept by the 90% coverage filter:
abilities with a 2026 exposure value are taken in descending weight order until 90% of their total weight is covered."""
from _common import *
def decompose(soc):
    ab = ability_exposure(LATEST); w = onet_weights()[soc]
    cand = [(a, float(ab[a]['exposure']), w[a]) for a in w if a in ab and ab[a]['exposure'] != '']
    cand.sort(key=lambda x: -x[2][2])  # stable: equal weights keep O*NET element order
    total = sum(x[2][2] for x in cand); cum = 0.0; kept = []
    for a, e, (i, l, wt) in cand:
        if total > 0 and cum / total >= 0.9: break
        kept.append((a, e, i, l, wt, e * wt)); cum += wt
    score = sum(k[5] for k in kept) / sum(k[4] for k in kept)
    return kept, score
def rows():
    occ = occupation_exposure(LATEST); order = sorted(occ, key=lambda s: occ[s][1], reverse=True)
    picks = [('Highest exposure', order[0]), ('Second-highest exposure', order[1]), ('Second-lowest exposure', order[-2]), ('Lowest exposure', order[-1])]
    out = []
    for label, soc in picks:
        kept, score = decompose(soc)
        assert abs(round(score, 2) - occ[soc][1]) < 0.011, (soc, score, occ[soc][1])
        out += [(label, occ[soc][0], occ[soc][1], a, f'{e:.2f}', f'{i:.4f}', f'{l:.4f}', f'{wt:.4f}', f'{c:.2f}') for a, e, i, l, wt, c in kept]
    return out
if __name__ == '__main__':
    R = rows(); write_csv('table09_decomposition.csv', ['Panel', 'Occupation', f'BAIOE {LATEST}', 'Ability', 'Ability exposure', 'Importance (normalized)', 'Level (normalized)', 'BAIOE weight', 'Contribution'], R)
    L = ['\\begin{longtable}{lrrrrr}', '\\caption{Ability-level decomposition for the two most- and least-exposed occupations, 2026}\\label{tab:decomp} \\\\ \\toprule', 'O*NET ability & Ability exposure & Importance & Level & BAIOE weight & Contribution \\\\ \\midrule \\endfirsthead', '\\toprule O*NET ability & Ability exposure & Importance & Level & BAIOE weight & Contribution \\\\ \\midrule \\endhead', '\\midrule \\multicolumn{6}{r}{\\textit{Continued on next page}} \\\\ \\endfoot', '\\bottomrule \\endlastfoot']
    cur = None
    for p, t, sc, a, e, i, l, wt, c in R:
        if (p, t) != cur:
            if cur is not None: L.append('\\addlinespace[0.5em]')
            L.append(f'\\multicolumn{{6}}{{@{{}}p{{0.95\\textwidth}}@{{}}}}{{\\textbf{{{p}: {tex_escape(t)}}} \\hfill \\textbf{{Final BAIOE score: {sc:.2f}}}}}\\\\'); L.append('\\midrule'); cur = (p, t)
        L.append(f'  {tex_escape(a)} & {e} & {i} & {l} & {wt} & {c} \\\\')
    L += [f'\\multicolumn{{6}}{{p{{0.95\\linewidth}}}}{{\\footnotesize \\textit{{Notes:}} The table reports the ability-level decomposition for the two occupations with the highest and lowest 2026 BAIOE scores. Ability exposure is the 2026 BAIOE ability-level exposure score, measured on the same scale used throughout the paper. Importance and level weights are normalized O*NET occupation--ability ratings. The BAIOE weight is the product of the normalized importance and level weights. The contribution column reports the raw numerator term, equal to ability exposure multiplied by the BAIOE weight. The final occupation score is the weighted average of ability exposure across abilities, obtained by dividing the sum of raw contributions by the sum of BAIOE weights. Values are rounded to two decimals.{vintage_note()}}} \\', '\\end{longtable}']
    write_tex('table09_decomposition.tex', '\n'.join(L)); print('Table 9:', len(R), 'rows;', {(p, t): sc for p, t, sc, *_ in R})
