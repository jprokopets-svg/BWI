"""Shared loaders and writers for the BAIOE table scripts. Reads only files under data/."""
import csv, os
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, 'data'); OUT = os.path.join(ROOT, 'tables'); TEX = os.path.join(OUT, 'tex')
YEARS = ['2020', '2021', '2022', '2023', '2024', '2025']

def read(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f: return list(csv.DictReader(f))

def occupation_exposure(year):
    """{soc_8digit: (title, exposure)} for one year."""
    return {r['soc_code']: (r['occupation_title'], float(r['exposure_raw'])) for r in read('occupation_exposure.csv') if r['year'] == year and r['exposure_raw'] != ''}

def occupation_exposure_6digit(year):
    """Collapse 8-digit O*NET-SOC codes to 6-digit SOC by averaging; title = first sub-occupation's title."""
    by6 = defaultdict(list)
    for r in read('occupation_exposure.csv'):
        if r['year'] == year and r['exposure_raw'] != '': by6[r['soc_code'][:7]].append((r['occupation_title'], float(r['exposure_raw'])))
    return {k: (v[0][0], round(sum(x for _, x in v) / len(v), 4)) for k, v in by6.items()}

def ability_exposure(year):
    """{ability: exposure or None} plus metadata rows for one year."""
    return {r['onet_ability']: r for r in read('ability_year_exposure.csv') if r['year'] == year}

def aei():
    return {r['occ_code'].strip(): (r['title'].strip(), float(r['observed_exposure'])) for r in read('aei_job_exposure.csv')}

def onet_weights():
    """{soc: {ability: (importance_norm, level_norm, weight)}}"""
    w = defaultdict(dict)  # insertion order = O*NET element order, which the pipeline uses to break weight ties
    for r in read('onet_ability_weights.csv'): w[r['soc_code']][r['onet_ability']] = (float(r['importance_norm']), float(r['level_norm']), float(r['weight']))
    return w

def tex_escape(s):
    return str(s).replace('&', '\\&').replace('%', '\\%').replace('_', '\\_').replace('#', '\\#').replace('$', '\\$')

def write_csv(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def write_tex(name, text):
    os.makedirs(TEX, exist_ok=True)
    with open(os.path.join(TEX, name), 'w', encoding='utf-8') as f: f.write(text.rstrip() + '\n')

def rank_desc(values):
    """Descending ranks (1 = highest) with fractional ties. values: {key: number}."""
    keys = sorted(values, key=lambda k: -values[k]); ranks = {}; i = 0; n = len(keys)
    while i < n:
        j = i
        while j + 1 < n and values[keys[j + 1]] == values[keys[i]]: j += 1
        for k in range(i, j + 1): ranks[keys[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks
