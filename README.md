# BAIOE replication package

BAIOE (Benchmark-based AI Occupational Exposure) measures how far demonstrated AI capability, as recorded on public AI benchmarks, overlaps with the abilities each U.S. occupation requires. It scores 369 benchmarks against the 52 O*NET abilities for every year from 2020 to 2025, then rolls the ability scores up to 894 occupations.

This repository holds the data behind the paper *From AI Benchmarks to Occupational Exposure: Tracking the Evolving AI Frontier* (Prokopets and Gulati, 2026) and the code that regenerates every table in it.

## What is in each file

**data/benchmark_ability_year.csv** (1,285 rows). One row per benchmark and year. The 369 benchmarks each map to one O*NET ability. For each year with a published result, the row gives the best reported score, the system that achieved it, the human baseline where one exists, the 0-10 capability rating relative to the people who use that ability at work, the 1-10 transferability weight, and quality flags. Benchmarks with no published score in any year appear once, flagged `missing`.

**data/ability_year_exposure.csv** (258 rows). One row per O*NET ability and year (43 mapped abilities × 6 years; the nine abilities that never received a benchmark do not appear). `exposure` is the ability's score for that year, on a 0-100 scale. `anchor_benchmark` names the benchmark that most directly determined that value. Empty `exposure` means no gradable benchmark result existed for that ability in that year.

**data/occupation_exposure.csv** (5,364 rows). One row per occupation and year (894 occupations × 6 years). `exposure_raw` is the BAIOE score on the 0-100 scale. The z-score columns are standardized versions: across all occupation-years, anchored to the 2025 distribution, and within each SOC major group.

**data/onet_ability_weights.csv** (46,488 rows). For every occupation and ability, the normalized O*NET importance rating (1-5 rescaled to 0-1), the normalized level rating (0-7 rescaled to 0-1), and their product, which is the weight used when combining ability scores into an occupation score. Derived from the O*NET 30.3 Database; no raw O*NET files are included.

**data/aei_job_exposure.csv** (756 rows). Occupation-level observed AI use from the Anthropic Economic Index, used for the validation tables.

**prompts/**. The five prompts used in the LLM-assisted stages, as printed in the paper's appendix: benchmark selection (Step 1), score extraction and its web-search supplement (Step 2), capability rating (Step 3, final version), and transferability rating (Step 4).

**tables/**. One script per data table in the paper (Tables 3 to 10). Each reads only `data/` and writes a `.csv` and a `.tex` file to `output/`. Tables 2, 11, and 12 are descriptive and are provided as static `.tex` files in `tables/static/`.

## How the occupation score is built

An occupation's score is the weighted average of its abilities' exposure scores, using the weights in `onet_ability_weights.csv`. Two rules apply. Abilities without an exposure value in a given year are excluded from the average rather than counted as zero. Among the abilities that do have a value, only the highest-weighted ones are used, taken in descending weight order until 90% of their total weight is covered (the 90% coverage filter). Table 9 shows the calculation in full for four occupations.

## Rerunning the tables

Requires Python 3.9 or later and `scipy` (`pip install -r requirements.txt`).

```
make tables
```

writes every table to `output/`. To check the regenerated tables against the released paper cell for cell:

```
PAPER_PDF=/path/to/paper.pdf make verify
```

This needs `pdftotext` (part of poppler). The PDF is not distributed here.

Two things to know when reading the output. The rows printed in the paper's Table 7 are reproduced by the 2025 BAIOE vintage, although the table's caption says 2024; the script is set to 2025 to reproduce the printed table. Table 9's numeric columns are not legible in the released PDF, so the verifier checks that table's row order and printed totals only.

## Citation

Prokopets, J. and Gulati, K. (2026). *From AI Benchmarks to Occupational Exposure: Tracking the Evolving AI Frontier.* See `CITATION.cff`.

## License and attribution

Data: CC BY 4.0. Code: MIT. See `LICENSE`.

This product includes derived values computed from the O*NET 30.3 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 license; O*NET is a trademark of USDOL/ETA. The Anthropic Economic Index file is redistributed under CC BY; cite Handa et al. (2025), arXiv:2503.04761.
