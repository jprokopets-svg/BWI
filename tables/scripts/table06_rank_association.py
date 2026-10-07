"""Table 6: rank association between BWI vintages (2023 to 2026) and realized AI use (Anthropic Economic Index).
Both measures are converted to percentile ranks over all matched 6-digit SOC occupations (including zero-use ones)."""
from _common import *
from scipy import stats
def rows():
    a = aei(); out = []
    for y in ('2023', '2024', '2025', '2026'):
        b = occupation_exposure_6digit(y); m = sorted(set(a) & set(b))
        x = [b[s][1] for s in m]; z = [a[s][1] for s in m]
        rho = stats.spearmanr(x, z)[0]
        px = [r / len(m) for r in stats.rankdata(x)]; pz = [r / len(m) for r in stats.rankdata(z)]
        r2 = stats.linregress(px, pz).rvalue ** 2
        out.append((y, len(m), round(rho, 4), round(r2, 4)))
    return out
if __name__ == '__main__':
    R = rows(); write_csv('table06_rank_association.csv', ['BWI Vintage', 'N', 'Spearman rho', 'R2'], R)
    L = ['\\begin{table}[htbp]\\centering', '\\caption{Rank association between BWI vintage and realized AI use}\\label{tab:rankassoc}', '\\begin{tabular}{lrr}\\toprule', 'BWI Vintage & Spearman $\\rho$ & $R^2$ \\\\ \\midrule']
    L += [f'{y} & {rho:.4f} & {r2:.4f} \\\\' for y, _, rho, r2 in R]
    L += ['\\bottomrule\\end{tabular}', '\\begin{minipage}{0.95\\linewidth}\\footnotesize \\textit{Notes:} The table reports rank-based associations between BWI and realized AI use measured using AEI. Both measures are converted to occupation-level percentile ranks before comparison. Observed use is measured in 2025, so the 2025 vintage is contemporaneous, the 2023 and 2024 vintages test forward-looking exposure, and the 2026 vintage post-dates the usage data. Earlier BWI vintages from 2020--2022 are omitted for readability.\\end{minipage}', '\\end{table}']
    write_tex('table06_rank_association.tex', '\n'.join(L)); print('Table 6:', R)
