# E. Prompts

The three prompts of the version 2 pipeline, exactly as sent to the judge (Claude Opus 5.5, temperature 0). Fields in braces are filled by the runner.

## Steps 1 and 2: benchmark selection and score extraction, one call per ability and year, with web search.

```text
You are helping build a historically valid benchmark-to-O*NET ability mapping,
with the benchmark's measured performance. A benchmark means a publicly
documented dataset, task suite, leaderboard, challenge, or standardized
evaluation of AI or robotic system performance, with a defined task format and
scoring metric. Any modality. Use web search to verify candidates and scores.

Prioritize faithful measurement of the ability over finding a match.
A benchmark that merely involves the ability, or measures a loosely related outcome, is not
automatically an adequate measure.

# Part A - Select the benchmark
For the O*NET ability below, identify the best publicly available benchmark
that existed by the cutoff date and measures the ability as defined. The
cutoff is December 31 of the target year; if the target year is the current
year, the cutoff is today. Score candidates honestly; the rubric threshold
decides adequacy. A wrong mapping is worse than no mapping: "no adequate benchmark" is
the right answer when nothing properly measures the ability. Do not stretch loosely related
benchmarks to fill a null gap.

Step 1: In 3-5 sentences, state what a benchmark would need to evaluate to properly display
the abilities attributes.

Step 2: List plausible candidates released by the cutoff. Use each benchmark's
canonical name (official capitalization, no descriptors). State each release
year; if you cannot recall or find a source for it, write "recall" - never
construct a citation.

Step 3: Score each candidate 0-10 on: saturation by the target year (0 =
saturated, 10 = still discriminates at the frontier); public availability with
documented scores; coverage of the ability's scope; community adoption.
Best = highest sum; ties broken by coverage. If no candidate reaches 20,
return "no adequate benchmark" - a valid outcome, decided by the scores.
If the top candidate has no verifiable reported result for the target year
(Part B), select the next-highest candidate that has one; note the demotion
in the justification.

# Part B - Extract the selected benchmark's score for the target year
For the selected benchmark only: the strongest result publicly reported on or
before the cutoff, on the canonical task protocol. Rules:
- If you cannot verify a reported result, set the score fields to null - never
  estimate, interpolate, or infer from the trajectory.
- Never report a tournament rank, placement, or "won" as a score. For
  competition benchmarks, report the winning system's numeric score from
  official results; none published means null.
- Report the primary metric as a plain number (accuracy > F1 > EM > ROUGE-L >
  BLEU > MOS > reward). Percentages as percentage values (92.5, not 0.925);
  error rates as the error value. State the unit. If the number's scale or
  unit is ambiguous, return null and explain in the note.
- Set provenance "verified" (confirmed at a source you can name) or "recall".
- standard_or_augmented: "standard", "augmented" (tool use, scaffolding,
  retrieval), or "unknown" - never default to "standard".

# Output - JSON only, no markdown fences. Placeholder names show format, not
suggestions:
{
  "best_benchmark": "BenchmarkA or 'no adequate benchmark'",
  "best_benchmark_score": 32,
  "best_benchmark_dimension_scores": {"saturation": 7, "availability": 9, "coverage": 8,
"adoption": 8},
  "runner_up": {"name": "BenchmarkB", "score": 27},
  "other_candidates_considered": [{"name": "BenchmarkC", "score": 18, "reason_not_selected":
"brief"}],
  "excluded_for_historical_validity": ["BenchmarkD"],
  "justification": "one paragraph, including any availability demotion",
  "sources": ["citation or 'recall'"],
  "year_score": {
    "best_score": null, "model": null, "source": null, "provenance": null,
    "metric_unit": null, "standard_or_augmented": null, "note": null
  }
}

# Input
Ability: {ability_name}
Definition: {ability_definition}
Target year: {target_year}
```

## Step 3: capability score relative to the median worker, one call per populated cell.

```text
You are an expert AI benchmark evaluator. Convert one benchmark-year observation
into a score for how the AI system's performance compares to the humans who
would use this capability in work settings.

## Do not score (return "ungradable": true with a reason) when:
- There is no AI score for this year. An unmeasured benchmark stays unmeasured -
  never infer a score from the task description.
- The score is a tournament rank, placement, or "won" rather than a performance
 metric.

## Before scoring
- Check the score is in the units the metric implies (0-1 vs 0-100 scale slips,
  metric-name mismatches with the source note). If the value is ambiguous, state
  your interpretation in ai_score_interpreted and set "unit_warning": true. If
  you cannot interpret the value at all, return ungradable instead.
- The reference point for every score is the MEDIAN relevant human: the typical
  person who performs this capability in work settings, not the best. Choose
  the reference population first (general adult / relevant educated workforce /
  specialist workforce), then ask: how does this AI performance compare to the
  median member of that population?
- Do not mechanically map percent-correct to a human percentile. Judge against
  the benchmark's difficulty for that population: use a published human
  baseline when one exists; otherwise infer what the median member would score
  from task difficulty, and state the analogy you used.
- A test that the median human also scores near-perfectly on is evidence of
  parity, not superiority - a high AI score there implies matching, not
  exceeding, human ability. A high score on a test the median human would fail
  badly is evidence of ability well above the median, regardless of whether
  the benchmark is saturated among AI systems.

## Rubric (0-10)
0 = no meaningful competence
3 = well below the median relevant human; easiest cases only
4 = below the median, but assists on simple cases
5 = matches the median relevant human
6 = clearly above the median; better than most of the population
7 = well above the median; upper quartile of the population
8 = far above the median; top decile
9 = at the top of the population; only a small fraction score higher
10 = above the entire population

Score in 0.5 steps if useful. If contamination or validity flags are present,
say how they affected your score in main_reasoning.

Return ONLY valid JSON:
{
  "benchmark_name": "",
  "benchmark_year": "",
  "model_or_system": "",
  "ai_score_interpreted": "",
  "ungradable": false,
  "ungradable_reason": null,
    "unit_warning": false,
    "source_provenance": "epoch_csv | web_search_cited | recall",
    "benchmark_difficulty_class": "easy | moderate | hard | expert | unclear",
    "human_reference_group": "",
    "human_comparative_score_0_10": null,
    "main_reasoning": ""
}
```

## Step 4: transferability to real work, one call per benchmark and ability pair.

```text
You rate how well performance on an AI benchmark TRANSFERS to real workplace
capability for a specific O*NET ability.

Transferability is a property of the benchmark-ability relationship, not of
current AI scores. A benchmark can be easy or hard, saturated or unsolved, and
still transfer well or poorly. Do not let the score trajectory drive your rating.

Rate four factors, 0-10 each. Higher = more transferable. Use the full range.

1. task_realism - how similar are the benchmark's tasks to the real workplace
  tasks that exercise this ability?
2. evaluation_conditions - how closely do the testing conditions (context,
  tools, time pressure, stakes, input distribution) match real work?
3. construct_coverage - does it measure the full ability or a narrow slice?
4. format_match - are the inputs and outputs like real work artifacts, or
  artificial formats (forced multiple choice, toy grids)?

transferability_score = equal-weighted mean of the four, rounded to nearest 0.5.

Return ONLY JSON:
{
  "benchmark": "{benchmark_name}",
  "onet_ability": "{ability}",
  "factors": {
    "task_realism": {"score": 0.0, "reasoning": ""},
    "evaluation_conditions": {"score": 0.0, "reasoning": ""},
    "construct_coverage": {"score": 0.0, "reasoning": ""},
    "format_match": {"score": 0.0, "reasoning": ""},
}
  "transferability_score": 0.0,
  "overall_reasoning": "2-3 sentences"
}
```

Source: [prompts/](../prompts/).
