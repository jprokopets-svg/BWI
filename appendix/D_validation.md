# D. Validation against observed AI use

Two waves of the Anthropic Economic Index (AEI) are used. **Wave 1, early 2025**: for each occupation, the share of its O*NET tasks that appear in Claude conversations (`observed_exposure` in [data/aei_job_exposure.csv](../data/aei_job_exposure.csv)); 744 occupations match the exposure data, 405 of them with no recorded usage. **Wave 2, April to May 2026**: the share of all Claude.ai conversations mapped to each occupation, from the Anthropic/EconomicIndex release of 26 June 2026 ([data/aei_usage_2026_apr_may.csv](../data/aei_usage_2026_apr_may.csv), provenance in [data/aei_usage_2026_apr_may_PROVENANCE.json](../data/aei_usage_2026_apr_may_PROVENANCE.json)); occupations absent from the release are suppressed, not zero. The two waves are different metrics, so they are compared in rank terms only.

## D1. Rank correlation between each BWI vintage and observed use

| BWI vintage | Usage early 2025: Spearman | n | Usage Apr-May 2026: Spearman | n |
|---|---|---|---|---|
| 2023 | 0.536 | 744 | 0.369 | 592 |
| 2024 | 0.559 | 744 | 0.408 | 592 |
| 2025 | 0.593 | 744 | 0.432 | 592 |
| 2026 | 0.543 | 744 | 0.360 | 592 |

The 2026 vintage is year-to-date: it uses benchmark results published up to 28 September 2026. Where a mapped ability had no verifiable 2026 result, its 2025 value is carried forward (one year only).

Source: [D1_rank_association_two_waves.csv](D1_rank_association_two_waves.csv).

## D2. Predicting 2026 usage: past usage, BWI, or both

Outcome: percentile rank of April to May 2026 usage. Regressors are percentile ranks. Standard errors (HC1) in parentheses. CV = 5-fold cross-validation with a fixed seed and the same folds for every model.

| Model | Past usage (2025) | BWI 2025 | R² | CV R² | CV RMSE | n |
|---|---|---|---|---|---|---|
| M1: past usage only | 0.571 (0.035) |  | 0.311 | 0.307 | 23.69 | 566 |
| M2: BWI 2025 only |  | 0.425 (0.035) | 0.186 | 0.184 | 25.70 | 566 |
| M3: past usage + BWI 2025 | 0.468 (0.040) | 0.193 (0.035) | 0.340 | 0.333 | 23.24 | 566 |

Source: [D2_prediction_horserace.csv](D2_prediction_horserace.csv) (also has a log-scale version).

## D3. BWI 2024 against Felten and Eloundou as predictors of 2025 usage

Outcome: percentile rank of early-2025 usage. Exposure measures as percentile ranks. Controls: log median wage and log employment (OEWS May 2024) and the share of workers with a bachelor's degree or higher (O*NET). HC1 standard errors in parentheses.

| Specification | BWI 2024 | Felten AIOE | Eloundou | R² | n |
|---|---|---|---|---|---|
| (a) BWI alone | 0.512 (0.025) |  |  | 0.313 | 744 |
| (b) + Felten | 0.018 (0.060) | 0.551 (0.060) |  | 0.389 | 668 |
| (c) + Felten + occupation-group effects | 0.072 (0.067) | 0.389 (0.071) |  | 0.482 | 668 |
| (d) + Felten + group effects + wage, employment, education | -0.007 (0.067) | 0.423 (0.073) |  | 0.519 | 659 |
| (e) + Eloundou | 0.038 (0.041) |  | 0.610 (0.038) | 0.488 | 744 |
| (f) + Eloundou + group effects + controls | 0.004 (0.054) |  | 0.525 (0.047) | 0.584 | 732 |
| (g) + Felten + Eloundou + group effects + controls | -0.054 (0.063) | 0.132 (0.079) | 0.463 (0.059) | 0.564 | 659 |

Source: [D3_incremental_regressions.csv](D3_incremental_regressions.csv).

## D4. Capability-adoption quadrants, BWI 2024 against usage in early 2025

Among the 339 occupations with recorded usage, high and low are relative to the median rank on each measure; the ten occupations with the largest gap between their two ranks are listed per quadrant. Low use includes use that is unobserved on the Claude platform; low BWI means low measured exposure, not immunity to AI. The paper's Figure 3 and Table 7 use the 2026 vintage; 32 of their 40 occupations fall in the same quadrant here.

**Active transformation** (high capability, high use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Credit Analysts | 37.68 | 16.85 |
| Loan Officers | 36.99 | 18.57 |
| Industrial-Organizational Psychologists | 36.89 | 15.77 |
| Logisticians | 36.34 | 15.71 |
| Dietitians and Nutritionists | 36.27 | 13.28 |
| Web Developers | 34.80 | 48.02 |
| Social Science Research Assistants | 34.71 | 43.93 |
| Customer Service Representatives | 34.57 | 70.11 |
| Office Clerks, General | 34.44 | 45.04 |
| Information Security Analysts | 34.31 | 48.59 |

**Latent exposure** (high capability, low use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Actuaries | 39.00 | 5.39 |
| Financial Examiners | 37.42 | 4.28 |
| Physical Scientists | 36.83 | 3.79 |
| Medical Scientists | 36.60 | 3.81 |
| Sales Managers | 36.42 | 4.33 |
| Tax Examiners and Collectors, and Revenue Agents | 36.26 | 2.75 |
| Genetic Counselors | 36.21 | 1.23 |
| Geoscientists | 36.13 | 4.30 |
| Industrial Engineers | 35.86 | 3.67 |
| Civil Engineers | 35.78 | 0.81 |

**Adoption ahead** (low capability, high use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Fine Artists | 29.66 | 35.65 |
| Court Reporters and Simultaneous Captioners | 30.66 | 34.31 |
| Desktop Publishers | 31.70 | 46.40 |
| Graphic Designers | 31.94 | 36.72 |
| Switchboard Operators | 31.99 | 38.63 |
| Medical Transcriptionists | 32.12 | 63.65 |
| Special Effects Artists and Animators | 32.39 | 35.71 |
| Secretaries and Administrative Assistants | 32.67 | 45.28 |
| Interpreters and Translators | 32.70 | 43.04 |
| Data Entry Keyers | 32.93 | 67.07 |

**Low pressure** (low capability, low use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Computer, Automated Teller, and Office Machine Repairers | 29.75 | 10.67 |
| Baggage Porters and Bellhops | 29.86 | 7.30 |
| Choreographers | 29.93 | 8.01 |
| Actors | 31.36 | 10.11 |
| Prepress Technicians and Workers | 32.06 | 10.18 |
| Occupational Therapists | 33.34 | 0.80 |
| Cargo and Freight Agents | 33.47 | 1.65 |
| Pharmacy Aides | 33.61 | 2.20 |
| Library Science Teachers, Postsecondary | 33.71 | 1.80 |
| Historians | 33.78 | 2.80 |

Source: [D4_quadrants_2024.csv](D4_quadrants_2024.csv); the paper's 2026 version is [tables/table07_quadrants.csv](../tables/table07_quadrants.csv).
