# BAIOE replication package, version 2 pipeline

BAIOE (Benchmark-based AI Occupational Exposure) measures how far demonstrated AI capability, as recorded on public AI benchmarks, overlaps with the abilities each U.S. occupation requires. It scores public benchmarks against the 52 O*NET abilities for every year from 2020 to 2025, then rolls the ability scores up to 894 occupations.

This repository holds the **version 2** pipeline: a single judge model selects one benchmark per ability and year and extracts its score in the same call, a second pass rates the AI result against the median human who uses that ability at work, and a third pass rates how well the benchmark transfers to real work. The version 1 pipeline behind the released paper (three judges, up to three benchmarks per cell) is on the `v1-release` branch of this repository.

## What changed from version 1

- Benchmark selection and score extraction are one call per ability and year, made by Claude Opus 5.5 with live web search, using `prompts/step1_2_benchmark_selection_and_score_extraction.txt`. Each ability-year gets one selected benchmark or "no adequate benchmark".
- Capability scores (0-10) are anchored to the median relevant human, rated by Claude Opus 5.5 with `prompts/step3_capability_rating.txt`.
- Transferability (0-10, four factors) is rated by GPT-5.6 Luna with `prompts/step4_transferability.txt`, once per benchmark-ability pair.
- Ability exposure is capability × transferability for the single selected benchmark. This is the per-benchmark form of the version 1 formula, which weighted several benchmarks by transferability; with one benchmark the weighting reduces to the product.
- Occupation aggregation is unchanged: O*NET importance × level weights, abilities without a value excluded, and only the highest-weighted abilities used until 90% of the available weight is covered. The share of an occupation's ability weight that has no measurement is reported alongside the score.

## What is in each file

**data/benchmark_ability_year.csv** (312 rows, 52 abilities × 6 years). The selected benchmark for each ability and year, its selection rubric score, the extracted result (system, score, metric, provenance), the capability score with the human reference group the rater used, the transferability weight, and the resulting ability exposure. Rows with no benchmark are empty beyond the year.

**data/ability_year_exposure.csv** (312 rows). The exposure score per ability and year, the selected benchmark, and how the value was resolved: `single judge`, `no adequate benchmark`, `no extracted score`, or `ungradable`.

**data/occupation_exposure.csv** (5,364 rows, 894 occupations × 6 years). `exposure_raw` on the 0-100 scale, three standardized versions (within year, anchored to the 2025 distribution, within SOC major group), the number of abilities used, and the share of the occupation's ability weight that was unmeasured.

**data/onet_ability_weights.csv**. Normalized O*NET importance and level ratings and their product for every occupation and ability. Derived from the O*NET 30.3 Database; no raw O*NET files are included.

**data/aei_job_exposure.csv**. Occupation-level observed AI use from the Anthropic Economic Index, used for the validation tables.

**prompts/**. The three prompts used by the version 2 pipeline.

**tables/**. One script per data table in the paper (Tables 3 to 10), each reading only `data/` and writing a `.csv` and a `.tex` to `output/`, in the paper's format with version 2 values. Tables 2, 11, and 12 are descriptive; their `.tex` files in `tables/static/` describe the version 1 pipeline as printed in the paper.

## Rerunning the tables

Requires Python 3.9 or later and `scipy` (`pip install -r requirements.txt`). `make tables` writes every table to `output/`.

## Tables that need more than this data

All eight data tables can be produced because version 2 covers all six years. Table 6 (rank association with observed AI use) reports the 2023 and 2024 vintages as in the paper; Table 7 (quadrants) uses the 2024 vintage named in the paper's caption.

## Citation

Prokopets, J. and Gulati, K. (2026). *From AI Benchmarks to Occupational Exposure: Tracking the Evolving AI Frontier.* See `CITATION.cff`.

## License and attribution

Data: CC BY 4.0. Code: MIT. See `LICENSE`. This product includes derived values computed from the O*NET 30.3 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 license; O*NET is a trademark of USDOL/ETA. The Anthropic Economic Index file is redistributed under CC BY; cite Handa et al. (2025), arXiv:2503.04761.
