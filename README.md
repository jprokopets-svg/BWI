# BWI: Benchmark Work Index

BWI (Benchmark Work Index) measures how far the abilities a job requires overlap with what frontier AI can demonstrably do. For every year from 2020 to 2026 it selects the best public AI benchmark for each of the 52 O*NET abilities, scores the AI result against the median worker who uses that ability, discounts by how well the benchmark transfers to real work, and rolls the ability scores up to 894 occupations using O*NET importance and level weights. The result is a yearly exposure score per occupation that moves as benchmarks move.

- Paper: [From AI Benchmarks to Occupational Exposure (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5452354)
- Interactive explorer: [benchmarkexposure.work](https://benchmarkexposure.work)
- The 2026 vintage is year-to-date (benchmark results to 28 September 2026); where an ability had no verifiable 2026 result, its 2025 value is carried forward.

## Online appendix

Every table below renders in the browser; the CSV behind each is linked at the bottom of its page.

| Section | Contents |
|---|---|
| [A. Occupation exposure](appendix/A_occupation_exposure.md) | All 894 occupations, 2020 to 2026, sorted by 2026 |
| [B. Abilities](appendix/B_abilities.md) | All 52 abilities by year, unmeasured ones marked, and the abilities that enter the 2026 scores |
| [C. Benchmarks](appendix/C_benchmarks.md) | Every selected benchmark with capability, transferability, year entered and carry-forward flag; resolution counts per year |
| [D. Validation](appendix/D_validation.md) | Rank correlation with observed AI use in two waves, the prediction horse race, the Felten and Eloundou comparison, and the capability-adoption quadrants |
| [E. Prompts](appendix/E_prompts.md) | The three prompts, verbatim |
| [Figures](figures/README.md) | Final figures with one-line captions |
| [Paper tables](#paper-tables) | Tables 3 to 10 of the paper as CSV |

## How the index is built

### Judge prompts, revised 7 October 2026

The capability and transferability prompts in `prompts/` are the revised versions used for the current data. Benchmark selection and score extraction (Step 1 and 2) are unchanged. Capability (Step 3) now scores against a fixed reference population per ability, records validity concerns as flags instead of deducting them from the score, and flags abilities where the median worker is near the benchmark ceiling. Transferability (Step 4) now asks whether strong performance on the benchmark shows the ability, with deductions only for construct contamination, narrow coverage and ceiling or floor effects; abstract or academic material is not a deduction. Against the earlier prompts, capability scores are nearly unchanged (rank correlation 0.97) and transferability scores are higher and more spread (mean 4.3 to 5.8, range 2.5 to 8.5), so ability and occupation exposures are higher in level; occupation rank order is 95% correlated with the previous data. Rank correlations with observed AI usage are unchanged to two decimals.

### What changed from version 1

- Benchmark selection and score extraction are one call per ability and year, made by Claude Opus 5.5 with live web search, using `prompts/step1_2_benchmark_selection_and_score_extraction.txt`. Each ability-year gets one selected benchmark or "no adequate benchmark".
- Capability scores (0-10) are anchored to the median relevant human, rated by Claude Opus 5.5 with `prompts/step3_capability_rating.txt`.
- Transferability (0-10, four factors) is rated by Claude Opus 5.5 with `prompts/step4_transferability.txt`, once per benchmark-ability pair.
- Ability exposure is capability × transferability for the single selected benchmark. This is the per-benchmark form of the version 1 formula, which weighted several benchmarks by transferability; with one benchmark the weighting reduces to the product.
- Where a mapped ability has no verifiable result in the current year, the most recent prior year's value is carried forward, as in earlier vintages (one year back only; abilities that were also unmeasured the year before, and abilities with no benchmark at all, stay empty). Carried cells are labelled `carry_forward_2025` in `resolution` and `exposure_source`.
- Occupation aggregation is unchanged: O*NET importance × level weights, abilities without a value excluded, and only the highest-weighted abilities used until 90% of the available weight is covered. The share of an occupation's ability weight that has no measurement is reported alongside the score.

## What is in each file

**data/benchmark_ability_year.csv** (364 rows, 52 abilities × 7 years). The selected benchmark for each ability and year, its selection rubric score, the extracted result (system, score, metric, provenance), the capability score with the human reference group the rater used, the transferability weight, and the resulting ability exposure. Rows with no benchmark are empty beyond the year.

**data/ability_year_exposure.csv** (364 rows). The exposure score per ability and year, the selected benchmark, and how the value was resolved: `single judge`, `carry_forward_2025`, `no adequate benchmark`, `no extracted score`, or `ungradable`.

**data/occupation_exposure.csv** (6,258 rows, 894 occupations × 7 years). `exposure_raw` on the 0-100 scale, three standardized versions (within year, anchored to the 2026 distribution, within SOC major group), the number of abilities used, and the share of the occupation's ability weight that was unmeasured.

**data/onet_ability_weights.csv**. Normalized O*NET importance and level ratings and their product for every occupation and ability. Derived from the O*NET 30.3 Database; no raw O*NET files are included.

**data/aei_job_exposure.csv**. Occupation-level observed AI use from the Anthropic Economic Index, early 2025 wave (share of an occupation's tasks observed in use), used for the validation tables.

**data/aei_usage_2026_apr_may.csv**. The second usage wave: share of usage by occupation from the Anthropic Economic Index release of 26 June 2026, averaged over April and May 2026. Source and construction are in `data/aei_usage_2026_apr_may_PROVENANCE.json`.

**data/oews_employment_2024.csv** (831 rows). National employment by detailed occupation from the BLS Occupational Employment and Wage Statistics survey, May 2024, used to weight the postsecondary-teacher bundle in the extra tables.

**prompts/**. The three prompts used by the version 2 pipeline.

## Paper tables

**tables/**. The paper's tables with version 2 values, anchored on the 2026 vintage (benchmark results up to 28 September 2026), as CSV files (LaTeX versions in `tables/tex/`, generating scripts in `tables/scripts/`). Each script reads only `data/`.

| Table | What it shows | CSV |
|---|---|---|
| 3 | The 25 occupations with the highest exposure in 2026 | [table03_top25.csv](tables/table03_top25.csv) |
| 4 | The ten most- and ten least-exposed occupations in 2026 | [table04_top_bottom10.csv](tables/table04_top_bottom10.csv) |
| 5 | The 25 occupations whose exposure grew most from 2020 to 2026 | [table05_fastest_growing.csv](tables/table05_fastest_growing.csv) |
| 6 | Rank correlation between each exposure vintage (2023 to 2026) and observed AI use (Anthropic Economic Index, measured in 2025) | [table06_rank_association.csv](tables/table06_rank_association.csv) |
| 7 | Occupations where 2026 exposure and observed use agree or diverge, in four quadrants | [table07_quadrants.csv](tables/table07_quadrants.csv) |
| 8 | All 52 abilities with their 2026 exposure score and the benchmark behind it | [table08_ability_anchors.csv](tables/table08_ability_anchors.csv) |
| 9 | How the 2026 score of the two most- and two least-exposed occupations is built from their abilities | [table09_decomposition.csv](tables/table09_decomposition.csv) |
| 10 | The abilities with a 2026 value, ranked by exposure | [table10_ability_rankings.csv](tables/table10_ability_rankings.csv) |
| 13 | Every benchmark behind a 2026 ability score with its capability score (C), transferability weight (T) and exposure | [table13_benchmarks_2026.csv](tables/table13_benchmarks_2026.csv) |
| extra | Top 25 by 2026 exposure with the 35 postsecondary teaching occupations (SOC 25-1xxx) removed | [table_top25_no_teachers.csv](tables/table_top25_no_teachers.csv) |
| extra | Top 25 by 2020-2026 growth with postsecondary teachers removed | [table_fastest25_no_teachers.csv](tables/table_fastest25_no_teachers.csv) |
| extra | Top 25 by 2026 exposure with all postsecondary teachers collapsed into one employment-weighted row | [table_top25_teachers_bundled.csv](tables/table_top25_teachers_bundled.csv) |
| extra | Top 25 by growth with the same teacher bundle | [table_fastest25_teachers_bundled.csv](tables/table_fastest25_teachers_bundled.csv) |

Tables 2, 11, and 12 are descriptive and exist only as LaTeX in `tables/tex/`; they describe the version 1 pipeline as printed in the paper.

## Rerunning the tables

Requires Python 3.9 or later and `scipy` (`pip install -r requirements.txt`). `make tables` regenerates every CSV in `tables/` and every LaTeX file in `tables/tex/`.

## Tables that need more than this data

All tables are anchored on 2026, the latest vintage. Table 6 reports the 2023 to 2026 vintages against observed AI use measured in 2025; the 2026 row post-dates the usage data and should be read as a consistency check rather than a validation. Table 7 (quadrants) uses the 2024 vintage named in the paper's caption. The two-wave comparison is in [appendix D](appendix/D_validation.md).

## Citation

Prokopets, J. and Gulati, K. (2026). *From AI Benchmarks to Occupational Exposure: Tracking the Evolving AI Frontier.* See `CITATION.cff`.

## License and attribution

Data: CC BY 4.0. Code: MIT. See `LICENSE`. This product includes derived values computed from the O*NET 30.3 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 license; O*NET is a trademark of USDOL/ETA. The Anthropic Economic Index file is redistributed under CC BY; cite Handa et al. (2025), arXiv:2503.04761. Employment counts are from the U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics, May 2024 (public domain).
