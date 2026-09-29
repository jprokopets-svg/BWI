# BAIOE replication package, version 2 pipeline

BAIOE (Benchmark-based AI Occupational Exposure) measures how far demonstrated AI capability, as recorded on public AI benchmarks, overlaps with the abilities each U.S. occupation requires. It scores public benchmarks against the 52 O*NET abilities for every year from 2020 to 2026, then rolls the ability scores up to 894 occupations. The 2026 vintage uses benchmark results published up to 28 September 2026, the date of the run.

This repository holds the **version 2** pipeline: a single judge model selects one benchmark per ability and year and extracts its score in the same call, a second pass rates the AI result against the median human who uses that ability at work, and a third pass rates how well the benchmark transfers to real work. The version 1 pipeline behind the released paper (three judges, up to three benchmarks per cell) is on the `v1-release` branch of this repository.

## What changed from version 1

- Benchmark selection and score extraction are one call per ability and year, made by Claude Opus 5.5 with live web search, using `prompts/step1_2_benchmark_selection_and_score_extraction.txt`. Each ability-year gets one selected benchmark or "no adequate benchmark".
- Capability scores (0-10) are anchored to the median relevant human, rated by Claude Opus 5.5 with `prompts/step3_capability_rating.txt`.
- Transferability (0-10, four factors) is rated by GPT-5.6 Luna with `prompts/step4_transferability.txt`, once per benchmark-ability pair.
- Ability exposure is capability × transferability for the single selected benchmark. This is the per-benchmark form of the version 1 formula, which weighted several benchmarks by transferability; with one benchmark the weighting reduces to the product.
- Where a mapped ability has no verifiable result in the current year, the most recent prior year's value is carried forward, as in earlier vintages (one year back only; abilities that were also unmeasured the year before, and abilities with no benchmark at all, stay empty). Carried cells are labelled `carry_forward_2025` in `resolution` and `exposure_source`.
- Occupation aggregation is unchanged: O*NET importance × level weights, abilities without a value excluded, and only the highest-weighted abilities used until 90% of the available weight is covered. The share of an occupation's ability weight that has no measurement is reported alongside the score.

## What is in each file

**data/benchmark_ability_year.csv** (364 rows, 52 abilities × 7 years). The selected benchmark for each ability and year, its selection rubric score, the extracted result (system, score, metric, provenance), the capability score with the human reference group the rater used, the transferability weight, and the resulting ability exposure. Rows with no benchmark are empty beyond the year.

**data/ability_year_exposure.csv** (364 rows). The exposure score per ability and year, the selected benchmark, and how the value was resolved: `single judge`, `carry_forward_2025`, `no adequate benchmark`, `no extracted score`, or `ungradable`.

**data/occupation_exposure.csv** (6,258 rows, 894 occupations × 7 years). `exposure_raw` on the 0-100 scale, three standardized versions (within year, anchored to the 2026 distribution, within SOC major group), the number of abilities used, and the share of the occupation's ability weight that was unmeasured.

**data/onet_ability_weights.csv**. Normalized O*NET importance and level ratings and their product for every occupation and ability. Derived from the O*NET 30.3 Database; no raw O*NET files are included.

**data/aei_job_exposure.csv**. Occupation-level observed AI use from the Anthropic Economic Index, used for the validation tables.

**data/oews_employment_2024.csv** (831 rows). National employment by detailed occupation from the BLS Occupational Employment and Wage Statistics survey, May 2024, used to weight the postsecondary-teacher bundle in the extra tables.

**prompts/**. The three prompts used by the version 2 pipeline.

**tables/**. The paper's tables with version 2 values, anchored on the 2026 vintage (benchmark results up to 28 September 2026), as CSV files (LaTeX versions in `tables/tex/`, generating scripts in `tables/scripts/`). Each script reads only `data/`.

| Table | What it shows | CSV |
|---|---|---|
| 3 | The 25 occupations with the highest exposure in 2026 | [table03_top25.csv](tables/table03_top25.csv) |
| 4 | The ten most- and ten least-exposed occupations in 2026 | [table04_top_bottom10.csv](tables/table04_top_bottom10.csv) |
| 5 | The 25 occupations whose exposure grew most from 2020 to 2026 | [table05_fastest_growing.csv](tables/table05_fastest_growing.csv) |
| 6 | Rank correlation between the 2023, 2024, and 2025 exposure vintages and observed AI use (Anthropic Economic Index, measured in 2025) | [table06_rank_association.csv](tables/table06_rank_association.csv) |
| 7 | Occupations where 2026 exposure and observed use agree or diverge, in four quadrants | [table07_quadrants.csv](tables/table07_quadrants.csv) |
| 8 | All 52 abilities with their 2026 exposure score and the benchmark behind it | [table08_ability_anchors.csv](tables/table08_ability_anchors.csv) |
| 9 | How the 2026 score of the two most- and two least-exposed occupations is built from their abilities | [table09_decomposition.csv](tables/table09_decomposition.csv) |
| 10 | The abilities with a 2026 value, ranked by exposure | [table10_ability_rankings.csv](tables/table10_ability_rankings.csv) |
| extra | Top 25 by 2026 exposure with the 35 postsecondary teaching occupations (SOC 25-1xxx) removed | [table_top25_no_teachers.csv](tables/table_top25_no_teachers.csv) |
| extra | Top 25 by 2020-2026 growth with postsecondary teachers removed | [table_fastest25_no_teachers.csv](tables/table_fastest25_no_teachers.csv) |
| extra | Top 25 by 2026 exposure with all postsecondary teachers collapsed into one employment-weighted row | [table_top25_teachers_bundled.csv](tables/table_top25_teachers_bundled.csv) |
| extra | Top 25 by growth with the same teacher bundle | [table_fastest25_teachers_bundled.csv](tables/table_fastest25_teachers_bundled.csv) |

Tables 2, 11, and 12 are descriptive and exist only as LaTeX in `tables/tex/`; they describe the version 1 pipeline as printed in the paper.

## Rerunning the tables

Requires Python 3.9 or later and `scipy` (`pip install -r requirements.txt`). `make tables` regenerates every CSV in `tables/` and every LaTeX file in `tables/tex/`.

## Tables that need more than this data

All tables are anchored on 2026, the latest vintage. Table 6 reports the 2023, 2024, and 2025 vintages against observed AI use measured in 2025; a 2026 row would need a later release of the usage data. Table 6 (rank association with observed AI use) reports the 2023 and 2024 vintages as in the paper; Table 7 (quadrants) uses the 2024 vintage named in the paper's caption.

## Citation

Prokopets, J. and Gulati, K. (2026). *From AI Benchmarks to Occupational Exposure: Tracking the Evolving AI Frontier.* See `CITATION.cff`.

## License and attribution

Data: CC BY 4.0. Code: MIT. See `LICENSE`. This product includes derived values computed from the O*NET 30.3 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 license; O*NET is a trademark of USDOL/ETA. The Anthropic Economic Index file is redistributed under CC BY; cite Handa et al. (2025), arXiv:2503.04761. Employment counts are from the U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics, May 2024 (public domain).
