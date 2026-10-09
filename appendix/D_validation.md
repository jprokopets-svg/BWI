# D. Validation against observed AI use

Two waves of the Anthropic Economic Index (AEI) are used. **Wave 1, early 2025**: for each occupation, the share of its O*NET tasks that appear in Claude conversations (`observed_exposure` in [data/aei_job_exposure.csv](../data/aei_job_exposure.csv)); 744 occupations match the exposure data, 405 of them with no recorded usage. **Wave 2, April to May 2026**: the share of all Claude.ai conversations mapped to each occupation, from the Anthropic/EconomicIndex release of 26 June 2026 ([data/aei_usage_2026_apr_may.csv](../data/aei_usage_2026_apr_may.csv), provenance in [data/aei_usage_2026_apr_may_PROVENANCE.json](../data/aei_usage_2026_apr_may_PROVENANCE.json)); occupations absent from the release are suppressed, not zero. The two waves are different metrics, so they are compared in rank terms only.

## D1. Rank correlation between each BWI vintage and observed use

| BWI vintage | Usage early 2025: Spearman | n | Usage Apr-May 2026: Spearman | n |
|---|---|---|---|---|
| 2023 | 0.627 | 744 | 0.442 | 592 |
| 2024 | 0.615 | 744 | 0.446 | 592 |
| 2025 | 0.633 | 744 | 0.468 | 592 |
| 2026 | 0.620 | 744 | 0.438 | 592 |

The 2026 vintage is year-to-date: it uses benchmark results published up to 28 September 2026. Where a mapped ability had no verifiable 2026 result, its 2025 value is carried forward (one year only).

Source: [D1_rank_association_two_waves.csv](D1_rank_association_two_waves.csv).

## D2. Predicting 2026 usage: past usage, BWI, or both

Outcome: percentile rank of April to May 2026 usage. Regressors are percentile ranks. Standard errors (HC1) in parentheses. CV = 5-fold cross-validation with a fixed seed and the same folds for every model.

| Model | Past usage (2025) | BWI 2025 | R² | CV R² | CV RMSE | n |
|---|---|---|---|---|---|---|
| M1: past usage only | 0.571 (0.035) |  | 0.311 | 0.307 | 23.69 | 566 |
| M2: BWI 2025 only |  | 0.461 (0.033) | 0.219 | 0.217 | 25.18 | 566 |
| M3: past usage + BWI 2025 | 0.441 (0.040) | 0.225 (0.035) | 0.348 | 0.340 | 23.11 | 566 |

Source: [D2_prediction_horserace.csv](D2_prediction_horserace.csv) (also has a log-scale version).

## D3. BWI 2024 against Felten and Eloundou as predictors of 2025 usage

Outcome: percentile rank of early-2025 usage. Exposure measures as percentile ranks. Controls: log median wage and log employment (OEWS May 2024) and the share of workers with a bachelor's degree or higher (O*NET). HC1 standard errors in parentheses.

| Specification | BWI 2024 | Felten AIOE | Eloundou | R² | n |
|---|---|---|---|---|---|
| (a) BWI alone | 0.563 (0.024) |  |  | 0.378 | 744 |
| (b) + Felten | 0.115 (0.101) | 0.456 (0.103) |  | 0.391 | 668 |
| (c) + Felten + occupation-group effects | 0.208 (0.118) | 0.269 (0.113) |  | 0.485 | 668 |
| (d) + Felten + group effects + wage, employment, education | 0.085 (0.114) | 0.353 (0.114) |  | 0.520 | 659 |
| (e) + Eloundou | 0.081 (0.049) |  | 0.571 (0.046) | 0.490 | 744 |
| (f) + Eloundou + group effects + controls | 0.061 (0.067) |  | 0.498 (0.053) | 0.585 | 732 |
| (g) + Felten + Eloundou + group effects + controls | -0.040 (0.110) | 0.132 (0.111) | 0.462 (0.059) | 0.563 | 659 |

Source: [D3_incremental_regressions.csv](D3_incremental_regressions.csv).

## D4. Capability-adoption quadrants, BWI 2024 against usage in early 2025

Among the 339 occupations with recorded usage, high and low are relative to the median rank on each measure; the ten occupations with the largest gap between their two ranks are listed per quadrant. Low use includes use that is unobserved on the Claude platform; low BWI means low measured exposure, not immunity to AI. The paper's Figure 3 and Table 7 use the 2026 vintage; 32 of their 40 occupations fall in the same quadrant here.

**Active transformation** (high capability, high use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Credit Analysts | 37.68 | 16.85 |
| Loan Officers | 36.99 | 18.57 |
| Industrial-Organizational Psychologists | 36.89 | 15.77 |
| Dietitians and Nutritionists | 36.27 | 13.28 |
| Educational, Guidance, and Career Counselors and Advisors | 35.83 | 11.82 |
| Agents and Business Managers of Artists, Performers, and Athletes | 35.81 | 11.80 |
| Customer Service Representatives | 34.46 | 70.11 |
| Office Clerks, General | 34.19 | 45.04 |
| Public Relations Specialists | 34.14 | 45.30 |
| Medical Secretaries and Administrative Assistants | 33.99 | 36.23 |

**Latent exposure** (high capability, low use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Actuaries | 39.00 | 5.39 |
| Financial Examiners | 37.42 | 4.28 |
| Medical Scientists | 36.60 | 3.81 |
| Physical Scientists | 36.43 | 3.79 |
| Sales Managers | 36.42 | 4.33 |
| Tax Examiners and Collectors, and Revenue Agents | 36.26 | 2.75 |
| Genetic Counselors | 36.21 | 1.23 |
| Atmospheric and Space Scientists | 35.84 | 3.80 |
| Atmospheric, Earth, Marine, and Space Sciences Teachers, Postsecondary | 35.84 | 3.96 |
| Civil Engineers | 35.78 | 0.81 |

**Adoption ahead** (low capability, high use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Fine Artists | 26.75 | 35.65 |
| Desktop Publishers | 31.06 | 46.40 |
| Graphic Designers | 31.10 | 36.72 |
| Court Reporters and Simultaneous Captioners | 31.13 | 34.31 |
| Special Effects Artists and Animators | 31.44 | 35.71 |
| Medical Transcriptionists | 31.52 | 63.65 |
| Switchboard Operators | 31.89 | 38.63 |
| Interpreters and Translators | 32.37 | 43.04 |
| Computer User Support Specialists | 32.49 | 46.85 |
| Data Entry Keyers | 33.04 | 67.07 |

**Low pressure** (low capability, low use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Choreographers | 24.46 | 8.01 |
| Baggage Porters and Bellhops | 25.07 | 7.30 |
| Computer, Automated Teller, and Office Machine Repairers | 27.78 | 10.67 |
| Occupational Therapists | 32.52 | 0.80 |
| Surveyors | 33.26 | 0.22 |
| Industrial Production Managers | 33.43 | 1.32 |
| Cargo and Freight Agents | 33.44 | 1.65 |
| Special Education Teachers, Preschool | 33.61 | 0.58 |
| Funeral Home Managers | 33.61 | 1.08 |
| Library Science Teachers, Postsecondary | 33.71 | 1.80 |

Source: [D4_quadrants_2024.csv](D4_quadrants_2024.csv); the paper's 2026 version is [tables/table07_quadrants.csv](../tables/table07_quadrants.csv).

## D5. What the judge scores add: component ablation

Occupation exposure rebuilt four ways from the same benchmark selections: the share of an occupation's ability weight that has any benchmark (no judge scores at all), capability alone (C x 10), transferability alone (T x 10), and the index (C x T). The first block uses the current Step 6 rule, under which abilities with no benchmark are left out of the weighted mean. The second block sets the eight abilities that have never had a benchmark (Arm-Hand Steadiness, Response Orientation, Reaction Time, Dynamic Strength, Trunk Strength, Extent Flexibility, Dynamic Flexibility, Peripheral Vision) to zero exposure instead. Spearman rank correlations with AEI usage; the last two columns are from the D2 horse race (coefficient on the measure when added to 2025 usage in predicting 2026 usage, and 5-fold cross-validated R-squared, same folds and seed).

| Step 6 rule | Measure | 2024 vs usage 2025 (n=744) | nonzero only (n=339) | 2024 vs usage 2026 (n=592) | 2025 vs usage 2025 | 2025 vs usage 2026 | g | CV R-squared |
|---|---|---|---|---|---|---|---|---|
| baseline (no judge scores) | share of ability weight with any benchmark | 0.633 | 0.480 | 0.468 |  |  |  |  |
| unmeasured abilities excluded (current data) | C only | 0.576 | 0.309 | 0.416 |  |  |  |  |
| unmeasured abilities excluded (current data) | T only | 0.269 | 0.152 | 0.187 |  |  |  |  |
| unmeasured abilities excluded (current data) | C x T (shipped index) | 0.559 | 0.284 | 0.408 | 0.593 | 0.432 | 0.193 | 0.333 |
| never-mapped abilities set to zero | C x T | 0.615 | 0.373 | 0.446 | 0.633 | 0.468 | 0.225 | 0.340 |
| never-mapped abilities set to zero | C only | 0.621 | 0.403 | 0.450 | 0.636 | 0.471 | 0.230 | 0.342 |
| never-mapped abilities set to zero | T only | 0.625 | 0.406 | 0.464 | 0.627 | 0.467 | 0.229 | 0.340 |

Read: under the current rule, leaving unmeasured abilities out of the mean lets physical occupations score on their cognitive abilities alone, and the judge scores then correlate less with usage than benchmark coverage does. Setting never-mapped abilities to zero removes that artefact; the index then exceeds the coverage baseline by about 0.05, and capability, transferability and their product are within 0.01 of one another. The zero-fill variant is reported here for comparison and is not the rule used in the released data.

Source: [D5_component_ablation.csv](D5_component_ablation.csv).
