"""Render the online appendix markdown pages from the CSVs in data/ and appendix/. Presentation only: no numbers are computed here beyond counts and formatting."""
import csv,os,random,collections,statistics as st
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A=f'{R}/appendix'; D=f'{R}/data'
YEARS=[str(y) for y in range(2020,2027)]
YTD='The 2026 vintage is year-to-date: it uses benchmark results published up to 28 September 2026. Where a mapped ability had no verifiable 2026 result, its 2025 value is carried forward (one year only).'
def rd(p): return list(csv.DictReader(open(p)))
def md_table(header,rows): return '\n'.join(['| '+' | '.join(header)+' |','|'+'---|'*len(header)]+['| '+' | '.join(str(c) for c in r)+' |' for r in rows])
def fmt(v,d=2): return '' if v in ('',None) else f'{float(v):.{d}f}'
# gate
occ=rd(f'{D}/occupation_exposure.csv'); o26=[r for r in occ if r['year']=='2026' and r['exposure_raw']]
top=max(o26,key=lambda r:float(r['exposure_raw'])); mean26=st.mean(float(r['exposure_raw']) for r in o26)
assert top['occupation_title']=='Economists' and top['exposure_raw']=='29.72' and round(mean26,2)==26.66,'PROVENANCE FAILED'; print('gate OK')
# ---- A ----
E=collections.defaultdict(dict); title={}
for r in occ:
    if r['exposure_raw']: E[r['soc_code']][r['year']]=r['exposure_raw']; title[r['soc_code']]=r['occupation_title']
socs=sorted(E,key=lambda s:-float(E[s].get('2026',-1)))
rows=[[title[s],s]+[fmt(E[s].get(y)) for y in YEARS] for s in socs]
open(f'{A}/A_occupation_exposure.md','w').write('\n'.join(['# A. Occupation exposure, 2020 to 2026','',f'All {len(socs)} O*NET-SOC occupations, sorted by 2026 exposure. Exposure is the weighted average of ability-level exposure over the abilities an occupation relies on most (O*NET importance × level weights, kept until 90% of the measured weight is covered). Higher means the abilities the job needs overlap more with what frontier AI can demonstrably do.',YTD,'',md_table(['Occupation','SOC code']+YEARS,rows),'','Source: [data/occupation_exposure.csv](../data/occupation_exposure.csv) (also has standardized scores and the share of each occupation\'s ability weight that is unmeasured).'])+'\n')
random.seed(2026); cells=[(random.choice(socs),random.choice(YEARS)) for _ in range(10)]; raw={(r['soc_code'],r['year']):r['exposure_raw'] for r in occ}
print('Spot-check, 10 cells of table A vs data/occupation_exposure.csv:'); [print(f"  {title[s][:40]:<40} {s} {y}: page {fmt(E[s][y])} | csv {raw[(s,y)]} | {'OK' if float(E[s][y])==float(raw[(s,y)]) else 'MISMATCH'}") for s,y in cells]
# ---- B ----
ab=rd(f'{D}/ability_year_exposure.csv'); A_=collections.defaultdict(dict); cat={}; res=collections.defaultdict(dict)
for r in ab: cat[r['onet_ability']]=r['ability_category']; A_[r['onet_ability']][r['year']]=r['exposure']; res[r['onet_ability']][r['year']]=r['resolution']
CATS=['cognitive','psychomotor','physical','sensory']; abil=sorted(cat,key=lambda a:(CATS.index(cat[a]),a))
rows=[[a,cat[a]]+[('no benchmark observed' if not A_[a].get(y) else fmt(A_[a][y])+(' (carried from 2025)' if res[a][y]=='carry_forward_2025' else '')) for y in YEARS] for a in abil]
never=[a for a in abil if all(not A_[a].get(y) for y in YEARS)]; measured26=[a for a in abil if A_[a].get('2026')]
W=rd(f'{D}/onet_ability_weights.csv'); print('weights columns:',list(W[0].keys()))
open(f'{A}/B_abilities.md','w').write('\n'.join(['# B. Ability-level exposure, all 52 O*NET abilities','','Ability exposure is the capability score of the selected benchmark (0 to 10, where 5 means the AI matches the median worker who uses the ability) multiplied by its transferability to real work (0 to 10), giving a 0 to 100 scale. "No benchmark observed" means the judge found no adequate public benchmark for that ability and year, or the selected benchmark had no verifiable score.',YTD,'',md_table(['Ability','Category']+YEARS,rows),'','## Abilities never measured','',f'{len(never)} abilities returned "no adequate benchmark" in every year: '+', '.join(never)+'.','','## Abilities measured in 2026','',f'{len(measured26)} abilities have a 2026 value, including the five carried forward from 2025. They are the abilities that can enter an occupation\'s score; which ones actually count for a given occupation depends on its O*NET weights (see [data/onet_ability_weights.csv](../data/onet_ability_weights.csv)).','',md_table(['Ability','Category','Exposure 2026','How resolved'],[[a,cat[a],fmt(A_[a]['2026']),res[a]['2026']] for a in sorted(measured26,key=lambda a:-float(A_[a]['2026']))]),'','Source: [data/ability_year_exposure.csv](../data/ability_year_exposure.csv).'])+'\n')
# ---- C ----
B=rd(f'{D}/benchmark_ability_year.csv'); first={}
for r in B:
    if r['benchmark_name']: first[r['benchmark_name']]=min(first.get(r['benchmark_name'],9999),int(r['year']))
prev={(r['onet_ability'],r['year']):r for r in B}; rows=[]
for a in abil:
    for y in YEARS:
        r=prev.get((a,y))
        if not r or not r['ability_exposure']: continue
        q=prev[(a,'2025')] if r['exposure_source']=='carry_forward_2025' else r
        rows.append([a,y,q['benchmark_name'],fmt(q['human_comparative_score_0_10'],1),fmt(q['transferability_weight'],1),fmt(r['ability_exposure']),first[q['benchmark_name']],'yes' if r['exposure_source']=='carry_forward_2025' else ''])
cnt=collections.Counter((r['year'],r['resolution']) for r in ab)
rc=[[y,cnt[(y,'single judge')],cnt[(y,'no adequate benchmark')],cnt[(y,'no extracted score')],cnt[(y,'carry_forward_2025')],cnt[(y,'single judge')]+cnt[(y,'carry_forward_2025')]] for y in YEARS]
open(f'{A}/C_benchmarks.md','w').write('\n'.join(['# C. Benchmarks','','One row for every ability and year that has a value (220 rows). Capability is the human-comparative score (0 to 10; 5 = matches the median worker); transferability is the mean of four factors (task realism, evaluation conditions, construct coverage, format match), 0 to 10; exposure is their product. "Entered" is the first year the benchmark was selected for any ability.',YTD,'',md_table(['Ability','Year','Benchmark','Capability','Transferability','Exposure','Entered','Carried forward'],rows),'','## How the 52 ability cells were resolved, by year','','Version 2 uses a single judge per ability and year, so a cell is either populated (benchmark selected and a verifiable score found), empty because no adequate benchmark exists, or empty because the selected benchmark had no verifiable score for that year.','',md_table(['Year','Selected and scored','No adequate benchmark','Selected, no verifiable score','Carried forward from 2025','Measured abilities'],rc),'','Source: [data/benchmark_ability_year.csv](../data/benchmark_ability_year.csv) (includes the model or system, raw score, metric, provenance, and the human reference group the rater used) and [data/ability_year_exposure.csv](../data/ability_year_exposure.csv).'])+'\n')
# ---- D ----
t=rd(f'{A}/D1_rank_association_two_waves.csv'); h=[r for r in rd(f'{A}/D2_prediction_horserace.csv') if r['transform']=='rank']; f=rd(f'{A}/D3_incremental_regressions.csv'); q=rd(f'{A}/D4_quadrants_2024.csv')
def coef(r,c): return f"{float(r['coef_'+c]):.3f} ({float(r['se_'+c]):.3f})" if r.get('coef_'+c) else ''
def cell(r,c): return f"{float(r[c+' beta']):.3f} ({float(r[c+' se']):.3f})" if r.get(c+' beta') else ''
SPEC={'(a) BWI alone':'(a) BWI alone','(b) + Felten':'(b) + Felten','(c) + Felten + SOC major-group FE':'(c) + Felten + occupation-group effects','(d) + Felten + FE + wage, employment, education':'(d) + Felten + group effects + wage, employment, education','(e) + Eloundou':'(e) + Eloundou','(f) + Eloundou + FE + controls':'(f) + Eloundou + group effects + controls','(g) + Felten + Eloundou + FE + controls':'(g) + Felten + Eloundou + group effects + controls'}
qrows=collections.defaultdict(list)
for r in q: qrows[r['Quadrant']].append(r)
qmd=[]
for name,desc in (('Active transformation','high capability, high use'),('Latent exposure','high capability, low use'),('Adoption ahead','low capability, high use'),('Low pressure','low capability, low use')):
    qmd+=[f'**{name}** ({desc})','',md_table(['Occupation','BWI 2024 exposure','AI usage (% of tasks observed)'],[[r['Occupation'],fmt(r['BWI 2024 exposure']),fmt(r['AEI usage share (%)'])] for r in qrows[name]]),'']
open(f'{A}/D_validation.md','w').write('\n'.join(['# D. Validation against observed AI use','','Two waves of the Anthropic Economic Index (AEI) are used. **Wave 1, early 2025**: for each occupation, the share of its O*NET tasks that appear in Claude conversations (`observed_exposure` in [data/aei_job_exposure.csv](../data/aei_job_exposure.csv)); 744 occupations match the exposure data, 405 of them with no recorded usage. **Wave 2, April to May 2026**: the share of all Claude.ai conversations mapped to each occupation, from the Anthropic/EconomicIndex release of 26 June 2026 ([data/aei_usage_2026_apr_may.csv](../data/aei_usage_2026_apr_may.csv), provenance in [data/aei_usage_2026_apr_may_PROVENANCE.json](../data/aei_usage_2026_apr_may_PROVENANCE.json)); occupations absent from the release are suppressed, not zero. The two waves are different metrics, so they are compared in rank terms only.','',
'## D1. Rank correlation between each BWI vintage and observed use','',md_table(['BWI vintage','Usage early 2025: Spearman','n','Usage Apr-May 2026: Spearman','n'],[[r['vintage'],fmt(r['spearman_2025'],3),r['n_2025'],fmt(r['spearman_2026'],3),r['n_2026']] for r in t]),'',YTD,'','Source: [D1_rank_association_two_waves.csv](D1_rank_association_two_waves.csv).','',
'## D2. Predicting 2026 usage: past usage, BWI, or both','','Outcome: percentile rank of April to May 2026 usage. Regressors are percentile ranks. Standard errors (HC1) in parentheses. CV = 5-fold cross-validation with a fixed seed and the same folds for every model.','',md_table(['Model','Past usage (2025)','BWI 2025','R²','CV R²','CV RMSE','n'],[[r['model'].replace('AEI_2025','past usage').replace('BWI_2025','BWI 2025'),coef(r,'aei'),coef(r,'bwi'),fmt(r['r2'],3),fmt(r['cv_r2'],3),fmt(r['cv_rmse']),r['n']] for r in h]),'','Source: [D2_prediction_horserace.csv](D2_prediction_horserace.csv) (also has a log-scale version).','',
'## D3. BWI 2024 against Felten and Eloundou as predictors of 2025 usage','','Outcome: percentile rank of early-2025 usage. Exposure measures as percentile ranks. Controls: log median wage and log employment (OEWS May 2024) and the share of workers with a bachelor\'s degree or higher (O*NET). HC1 standard errors in parentheses.','',md_table(['Specification','BWI 2024','Felten AIOE','Eloundou','R²','n'],[[SPEC.get(r['spec'],r['spec']),cell(r,'BWI 2024'),cell(r,'Felten AIOE'),cell(r,'Eloundou beta'),fmt(r['R2'],3),r['N']] for r in f]),'','Source: [D3_incremental_regressions.csv](D3_incremental_regressions.csv).','',
'## D4. Capability-adoption quadrants, BWI 2024 against usage in early 2025','','Among the 339 occupations with recorded usage, high and low are relative to the median rank on each measure; the ten occupations with the largest gap between their two ranks are listed per quadrant. Low use includes use that is unobserved on the Claude platform; low BWI means low measured exposure, not immunity to AI. The paper\'s Figure 3 and Table 7 use the 2026 vintage; 32 of their 40 occupations fall in the same quadrant here.','']+qmd+['Source: [D4_quadrants_2024.csv](D4_quadrants_2024.csv); the paper\'s 2026 version is [tables/table07_quadrants.csv](../tables/table07_quadrants.csv).'])+'\n')
# ---- E ----
P={'step1_2_benchmark_selection_and_score_extraction.txt':'Steps 1 and 2: benchmark selection and score extraction, one call per ability and year, with web search.','step3_capability_rating.txt':'Step 3: capability score relative to the median worker, one call per populated cell.','step4_transferability.txt':'Step 4: transferability to real work, one call per benchmark and ability pair.'}
L=['# E. Prompts','','The three prompts of the version 2 pipeline, exactly as sent to the judge (Claude Opus 5.5, temperature 0). Fields in braces are filled by the runner.','']
for fn,intro in P.items(): L+=[f'## {intro}','','```text',open(f'{R}/prompts/{fn}').read().rstrip(),'```','']
L.append('Source: [prompts/](../prompts/).'); open(f'{A}/E_prompts.md','w').write('\n'.join(L)+'\n')
print('wrote A-E; A rows',len(socs),'C rows',len(rows))
