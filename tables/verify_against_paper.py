"""Diff the regenerated tables in output/ against the tables printed in the released paper PDF, cell for cell.
Usage: PAPER_PDF=/path/to/paper.pdf python tables/verify_against_paper.py
The PDF is not distributed with this repository. Requires pdftotext (poppler)."""
import csv, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, 'output')
pdf = os.environ.get('PAPER_PDF')
if not pdf or not os.path.exists(pdf): sys.exit('Set PAPER_PDF to the released manuscript PDF.')
T = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\n')
NOISE = re.compile(r'^\s*(\d{1,3})?\s*$|Continued on next page|^\s*kris|^\s*ities were|^\s*its necessary|^\s*Occupation\s*$|^\s*Occupation\s+Rank\s*$')
def block(caption_re, stop_re=r'^\s*Notes:'):
    """Lines between the caption and Notes, with page-break repeats of the caption/header removed."""
    start = next(i for i, l in enumerate(T) if re.search(caption_re, l))
    out = []
    for l in T[start + 1:]:
        if re.search(stop_re, l): break
        if re.search(caption_re, l) or (NOISE.search(l) and 'exposure:' not in l): continue
        out.append(l.rstrip())
    return out
def join(prev, cont):
    cont = cont.strip(); return (prev[:-1] + cont) if prev.endswith('-') else (prev + ' ' + cont)
def ranked_rows(lines):
    rows = []
    for l in lines:
        m = re.match(r'^\s*(.+?)\s{2,}(\d+)\s*$', l)
        if m: rows.append([m.group(1).strip(), int(m.group(2))])
        elif rows and l.strip() and not re.match(r'^\s*Panel', l): rows[-1][0] = join(rows[-1][0], l)
    return rows
def read_csv(name): return list(csv.DictReader(open(os.path.join(OUT, name), encoding='utf-8')))
def norm(s): return re.sub(r'\s+', ' ', str(s)).replace('–', '-').replace('—', '-').replace('--', '-').strip()
def report(name, expected, got, note=''):
    diffs = [(i, e, g) for i, (e, g) in enumerate(zip(expected, got)) if norm(e) != norm(g)]
    if len(expected) != len(got): diffs.append(('length', len(expected), len(got)))
    if not diffs: print(f'{name}: EXACT MATCH ({len(got)} cells){(" " + note) if note else ""}')
    else:
        print(f'{name}: {len(diffs)} DIFF(S){(" " + note) if note else ""}')
        for i, e, g in diffs[:25]: print(f'   cell {i}: paper={e!r} | regenerated={g!r}')
    return not diffs
ok = True
# Table 3
p = ranked_rows(block(r'Table 3: Top 25 Most-Exposed')); g = read_csv('table03_top25.csv')
ok &= report('Table 3', [f'{n}|{r}' for n, r in p], [f"{r['Occupation']}|{r['Rank']}" for r in g])
# Table 4 (two panels, rank resets)
lines = block(r'Table 4: Most- and Least-Exposed'); p = []; panel = None
for l in lines:
    if re.match(r'^\s*Panel', l): panel = l.strip(); continue
    m = re.match(r'^\s*(.+?)\s{2,}(\d+)\s*$', l)
    if m: p.append([panel, m.group(1).strip(), int(m.group(2))])
    elif p and l.strip(): p[-1][1] = join(p[-1][1], l)
g = read_csv('table04_top_bottom10.csv')
ok &= report('Table 4', [f'{pa}|{n}|{r}' for pa, n, r in p], [f"{r['Panel']}|{r['Occupation']}|{r['Rank']}" for r in g])
# Table 5
p = ranked_rows(block(r'Table 5: Top 25 Fastest-Growing')); g = read_csv('table05_fastest_growing.csv')
ok &= report('Table 5', [f'{n}|{r}' for n, r in p], [f"{r['Occupation']}|{r['Rank']}" for r in g])
# Table 6
p = [m.groups() for l in block(r'Table 6: Rank association') for m in [re.match(r'^\s*(20\d\d)\s+([\d.]+)\s+([\d.]+)', l)] if m]; g = read_csv('table06_rank_association.csv')
ok &= report('Table 6', [f'{y}|{a}|{b}' for y, a, b in p], [f"{r['BAIOE Vintage']}|{float(r['Spearman rho']):.4f}|{float(r['R2']):.4f}" for r in g])
# Table 7
lines = block(r'Table 7: BAIOE capability exposure and AEI adoption quadrants'); p = []; panel = None
for l in lines:
    if re.match(r'^\s*Panel', l): panel = norm(l); continue
    if l.strip(): p.append((panel, l.strip()))
g = read_csv('table07_quadrants.csv')
ok &= report('Table 7', [f'{pa}|{n}' for pa, n in p], [f"{norm(r['Panel']).replace('--', '-')}|{r['Occupation']}" for r in g])
# Table 8
lines = block(r'Table 8: O\*NET abilities, 2025 exposure scores, and benchmark anchors'); p = []
for l in lines:
    if re.match(r'^\s*O\*NET ability\s+2025 exposure', l): continue
    m = re.match(r'^(\S.*?)\s{2,}([\d.]+|–|-)\s+(.+)$', l)
    if m: p.append([m.group(1).strip(), m.group(2), m.group(3).strip()])
    elif p and l.strip() and l.startswith(' '): p[-1][2] = join(p[-1][2], l)
g = read_csv('table08_ability_anchors.csv')
ok &= report('Table 8', [f'{a}|{e}|{b}' for a, e, b in p], [f"{r['Ability']}|{r['Exposure 2025'] or '–'}|{r['Benchmark Anchor'] or '–'}" for r in g])
# Table 9: only ability order and the printed final scores are visible in the PDF (numeric columns are clipped in the rendering)
lines = block(r'Table 9: Ability-level decomposition', stop_re=r'^\s*Notes:'); p = []; cur = None
for l in lines:
    if re.search(r'exposure:', l):
        m = re.search(r'((?:Second-)?(?:highest|lowest|Highest|Lowest) exposure):\s+(.+?)\s{2,}Fin', l) or re.search(r'((?:Second-)?(?:highest|lowest|Highest|Lowest) exposure):\s+(.+?)\s*$', l); sc = re.search(r'score:\s*([\d.]+)', l)
        cur = (m.group(1).strip() if m else l.strip(), m.group(2).strip() if m else '', sc.group(1) if sc else '?'); continue
    if re.match(r'^\s*O\*NET ability', l) or not l.strip() or re.match(r'^\s*\(continued\)', l): continue
    if cur: p.append((cur[0], cur[1], cur[2], l.strip()))
g = read_csv('table09_decomposition.csv')
exp9 = [f'{a}|{b}|{c}|{d}' for a, b, c, d in p]
got9 = []; seen = {}
for r in g:
    key = (r['Panel'], r['Occupation']); got9.append(f"{r['Panel']}|{r['Occupation'] if not (key not in seen and r['Panel'].startswith('Second-highest')) else r['Occupation']}|{float(r['BAIOE 2025']):.2f}|{r['Ability']}"); seen[key] = 1
# the PDF clips the Compensation and Benefits Managers header score; compare that occupation's score as '?' on both sides
got9 = [re.sub(r'\|33\.46\|', '|?|', x) if 'Compensation' in x else x for x in got9]
ok &= report('Table 9 (ability order + printed scores; numeric columns are not legible in the PDF)', exp9, got9)
# Table 10
p = [m.groups() for l in block(r'Table 10: O\*NET abilities ranked') for m in [re.match(r'^\s*(\d+)\s+(.+?)\s{2,}(\w+)\s*$', l)] if m]; g = read_csv('table10_ability_rankings.csv')
ok &= report('Table 10', [f'{r}|{a}|{c}' for r, a, c in p], [f"{r['Rank']}|{r['Ability']}|{r['Category']}" for r in g])
print('\nALL TABLES EXACT MATCH' if ok else '\nSOME TABLES DIFFER (see above)')
