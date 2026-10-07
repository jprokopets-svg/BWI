# D. Validation against observed AI use

Two waves of the Anthropic Economic Index (AEI) are used. **Wave 1, early 2025**: for each occupation, the share of its O*NET tasks that appear in Claude conversations (`observed_exposure` in [data/aei_job_exposure.csv](../data/aei_job_exposure.csv)); 744 occupations match the exposure data, 405 of them with no recorded usage. **Wave 2, April to May 2026**: the share of all Claude.ai conversations mapped to each occupation, from the Anthropic/EconomicIndex release of 26 June 2026 ([data/aei_usage_2026_apr_may.csv](../data/aei_usage_2026_apr_may.csv), provenance in [data/aei_usage_2026_apr_may_PROVENANCE.json](../data/aei_usage_2026_apr_may_PROVENANCE.json)); occupations absent from the release are suppressed, not zero. The two waves are different metrics, so they are compared in rank terms only.

## D1. Rank correlation between each BWI vintage and observed use

| BWI vintage | Usage early 2025: Spearman | n | Usage Apr-May 2026: Spearman | n |
|---|---|---|---|---|
| 2023 | 0.235 | 744 | 0.142 | 592 |
| 2024 | 0.566 | 744 | 0.420 | 592 |
| 2025 | 0.597 | 744 | 0.444 | 592 |
| 2026 | 0.562 | 744 | 0.385 | 592 |

The 2026 vintage is year-to-date: it uses benchmark results published up to 28 September 2026. Where a mapped ability had no verifiable 2026 result, its 2025 value is carried forward (one year only).

Source: [D1_rank_association_two_waves.csv](D1_rank_association_two_waves.csv).

## D2. Predicting 2026 usage: past usage, BWI, or both

Outcome: percentile rank of April to May 2026 usage. Regressors are percentile ranks. Standard errors (HC1) in parentheses. CV = 5-fold cross-validation with a fixed seed and the same folds for every model.

| Model | Past usage (2025) | BWI 2025 | R² | CV R² | CV RMSE | n |
|---|---|---|---|---|---|---|
| M1: past usage only | 0.571 (0.035) |  | 0.311 | 0.307 | 23.69 | 566 |
| M2: BWI 2025 only |  | 0.437 (0.035) | 0.197 | 0.195 | 25.53 | 566 |
| M3: past usage + BWI 2025 | 0.460 (0.039) | 0.205 (0.036) | 0.343 | 0.337 | 23.16 | 566 |

Source: [D2_prediction_horserace.csv](D2_prediction_horserace.csv) (also has a log-scale version).

## D3. BWI 2024 against Felten and Eloundou as predictors of 2025 usage

Outcome: percentile rank of early-2025 usage. Exposure measures as percentile ranks. Controls: log median wage and log employment (OEWS May 2024) and the share of workers with a bachelor's degree or higher (O*NET). HC1 standard errors in parentheses.

| Specification | BWI 2024 | Felten AIOE | Eloundou | R² | n |
|---|---|---|---|---|---|
| (a) BWI alone | 0.519 (0.026) |  |  | 0.321 | 744 |
| (b) + Felten | 0.084 (0.058) | 0.494 (0.057) |  | 0.391 | 668 |
| (c) + Felten + occupation-group effects | 0.123 (0.059) | 0.361 (0.064) |  | 0.485 | 668 |
| (d) + Felten + group effects + wage, employment, education | 0.057 (0.059) | 0.387 (0.068) |  | 0.520 | 659 |
| (e) + Eloundou | 0.074 (0.041) |  | 0.583 (0.037) | 0.490 | 744 |
| (f) + Eloundou + group effects + controls | 0.042 (0.049) |  | 0.510 (0.046) | 0.585 | 732 |
| (g) + Felten + Eloundou + group effects + controls | 0.010 (0.056) | 0.099 (0.076) | 0.457 (0.059) | 0.563 | 659 |

Source: [D3_incremental_regressions.csv](D3_incremental_regressions.csv).

## D4. Capability-adoption quadrants, BWI 2024 against usage in early 2025

Among the 339 occupations with recorded usage, high and low are relative to the median rank on each measure; the ten occupations with the largest gap between their two ranks are listed per quadrant. Low use includes use that is unobserved on the Claude platform; low BWI means low measured exposure, not immunity to AI. The paper's Figure 3 and Table 7 use the 2026 vintage; 32 of their 40 occupations fall in the same quadrant here.

**Active transformation** (high capability, high use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Industrial-Organizational Psychologists | 23.84 | 15.77 |
| Educational, Guidance, and Career Counselors and Advisors | 23.77 | 11.82 |
| Dietitians and Nutritionists | 23.59 | 13.28 |
| Customer Service Representatives | 22.93 | 70.11 |
| Software Quality Assurance Analysts and Testers | 22.81 | 51.95 |
| Database Architects | 22.73 | 57.87 |
| Computer Programmers | 22.70 | 74.51 |
| Receptionists and Information Clerks | 22.67 | 43.38 |
| Interpreters and Translators | 22.63 | 43.04 |
| Curators | 22.61 | 41.23 |

**Latent exposure** (high capability, low use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Sales Managers | 24.08 | 4.33 |
| Education and Childcare Administrators, Preschool and Daycare | 23.91 | 3.95 |
| Genetic Counselors | 23.67 | 1.23 |
| Medical Scientists | 23.66 | 3.81 |
| Financial Examiners | 23.66 | 4.28 |
| Forestry and Conservation Science Teachers, Postsecondary | 23.52 | 2.06 |
| Tax Examiners and Collectors, and Revenue Agents | 23.40 | 2.75 |
| Special Education Teachers, Preschool | 23.20 | 0.58 |
| Funeral Home Managers | 23.14 | 1.08 |
| Child, Family, and School Social Workers | 23.12 | 0.74 |

**Adoption ahead** (low capability, high use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Fine Artists | 20.14 | 35.65 |
| Desktop Publishers | 20.87 | 46.40 |
| Special Effects Artists and Animators | 21.12 | 35.71 |
| Graphic Designers | 21.17 | 36.72 |
| Chemical Technicians | 21.52 | 31.48 |
| Data Entry Keyers | 21.63 | 67.07 |
| Medical Transcriptionists | 21.98 | 63.65 |
| Information Security Analysts | 21.98 | 48.59 |
| Technical Writers | 22.13 | 47.47 |
| Web Developers | 22.17 | 48.02 |

**Low pressure** (low capability, low use)

| Occupation | BWI 2024 exposure | AI usage (% of tasks observed) |
|---|---|---|
| Computer, Automated Teller, and Office Machine Repairers | 20.33 | 10.67 |
| Choreographers | 20.34 | 8.01 |
| Baggage Porters and Bellhops | 20.83 | 7.30 |
| Prepress Technicians and Workers | 20.96 | 10.18 |
| Flight Attendants | 21.40 | 9.13 |
| Occupational Therapists | 22.16 | 0.80 |
| Healthcare Diagnosing or Treating Practitioners | 22.36 | 2.22 |
| Historians | 22.41 | 2.80 |
| Surveyors | 22.57 | 0.22 |
| Library Science Teachers, Postsecondary | 22.58 | 1.80 |

Source: [D4_quadrants_2024.csv](D4_quadrants_2024.csv); the paper's 2026 version is [tables/table07_quadrants.csv](../tables/table07_quadrants.csv).
