# Ziele & Wirkung: OKR

Use OKR when the user wants measurable goals, strategy-linked tasks or a progress review. Keep operational tasks optional: everyday tasks need no OKR. Start with one cycle, two or three objectives and two to four measurable key results each; these counts are guidance, not rigid schema restrictions.

## Conversation workflow

1. Establish the desired outcome, owner, start/end dates and committed versus aspirational intent. Distinguish outcome from activity. Propose the actual objective and KRs before writing.
2. For each KR agree the baseline, target, unit and measurement method; choose increase, decrease or binary. Mark critical KRs explicitly. Link supporting tasks/projects; never count completed tasks as proof of impact unless the explicitly agreed metric actually measures that count.
3. Register faithful measurement source text. Each measurement carries value, date, sourceId and locator. Check that the source supports the exact value and method. Structural validation alone cannot establish evidence quality. Missing values remain unknown. Ask for missing evidence instead of estimating it.
4. Generate the normal hash-bound plan and preview. Use existing authorization for requested changes. Apply, verify and run `okr --today YYYY-MM-DD`. Report measured progress, coverage, critical gaps, freshness and confidence separately.
5. Weekly check-in: review measurements, blockers, stale evidence and next tasks. Store a review with obstacles, learnings and nextTaskIds. At cycle end, store a closeout review with explicit outcome and set objective status=closed through the same reviewed plan. Do not automatically judge success from the average.

## Records (internal JSON actions)

All use the usual upsert action and common id/title/notes/position/timestamps fields.

| Kind / ID prefix | Required and optional fields |
|---|---|
| objective / obj_ | owner, startDate, endDate; goalType=committed or aspirational (default committed); status=draft/active/closed |
| key-result / kr_ | objectiveId, direction=increase/decrease/binary, baseline, target, unit, method; critical=false, taskIds=[], projectIds=[], freshnessDays=14 |
| measurement / msr_ | keyResultId, date, value, sourceId, locator; confidence=null or 0–1; supersedes=null or a replaced measurement ID |
| review / rev_ | objectiveId, date; reviewType=check-in/closeout, obstacles, learnings, nextTaskIds; outcome=pending/achieved/partially-achieved/not-achieved |

Examples:

```json
[
 {"op":"upsert","kind":"objective","record":{"id":"obj_entry","title":"Reliable onboarding","owner":"Team","startDate":"2026-10-01","endDate":"2026-12-31","status":"active"}},
 {"op":"upsert","kind":"key-result","record":{"id":"kr_success","title":"Setup success","objectiveId":"obj_entry","direction":"increase","baseline":40,"target":80,"unit":"%","method":"Same user-test protocol","critical":true}},
 {"op":"upsert","kind":"source","record":{"id":"src_test","title":"User test","reference":"test-results.md","text":"Synthetic example: 12 of 20 participants completed setup = 60%."}},
 {"op":"upsert","kind":"measurement","record":{"id":"msr_success","title":"October check-in","keyResultId":"kr_success","date":"2026-10-09","value":60,"sourceId":"src_test","locator":"Sentence 1","confidence":0.7}}
]
```

Measurements are immutable. A correction is a new ID with supersedes pointing at the same KR/date; the earlier point remains. Ambiguous same-day measurements, multiple competing corrections and correction cycles are rejected. A recorded correction becomes visible to as-of reports from its createdAt date. Intraday reconstruction is not supported because this runtime uses day dates.

After a KR has measurements its objectiveId/direction/baseline/target/unit/method cannot be changed. Create a new explicitly explained KR or cycle instead. A repeat import of identical measurement values is allowed; changing them requires a correction. Measurements cannot be trashed. Sources, linked tasks and containers must remain reference-valid; no silent cascade.

## Calculation contract

- Increase: `(current - baseline) / (target - baseline)`.
- Decrease: `(baseline - current) / (baseline - target)` (equivalent signed formula).
- Binary: baseline 0, target 1, measured value 0 or 1; absence still unknown.
- Baseline and target must differ and match direction. Reject non-finite values and invalid units/methods.
- rawProgress preserves negative regression and overachievement. progress clamps to [0,1]. UI presents fractions as percentages.
- Objective progress is the equal-weight average of displayed KR progress only if all active KRs have measurements. With missing KRs, progress=null; partialMean is explicitly incomplete and coverage is reported.
- A critical KR remains flagged unless its measured progress is 100%. This flag does not itself close the objective.
- Confidence is an optional human-provided fraction, not a forecast computed from progress. Stale means the latest eligible measurement is older than freshnessDays. No fabricated trend prediction or universal linear time-progress comparison.
- As-of considers measurement date AND createdAt no later than the requested date. Historical definitions/tasks still refer to the selected generation; for a complete historical reconstruction select that historical generation or frozen snapshot.

## Compatibility and exports

New state and bundle formats are /2. Old /1 generations are verified with the frozen v1 runtime; they are never rewritten. The next planned mutation upgrades the proposed state to /2, adding empty OKR collections. Preview shows new records; apply remains bound to the original generation. Undo across the boundary republishes old content as /2. Existing frozen v1 skills remain standalone.

New exports include all four OKR collections. Legacy bundles remain accepted. A frozen v2 skill includes a precomputed `snapshot/schema/okr-report.json` and instructs its reader to keep missing evidence, dated state and task progress distinct. The report is verified as part of the generation.

## Method material

Optional background, not a runtime dependency:

- [Google re:Work: Set goals with OKRs](https://rework.withgoogle.com/intl/en/guides/set-goals-with-okrs?product=breeze): measurable key results, transparent scoring and consistent review.
- [What Matters: Key Results and outcomes](https://www.whatmatters.com/faqs/dear-andy-input-vs-outcome-key-results-which-work-best): distinguish activities and desired results.
- [What Matters: committed versus aspirational](https://www.whatmatters.com/faqs/committed-aspirational-okrs-examples-difference): committed goals expect full delivery; around 70% is a contextual aspiration guideline, not a universal success threshold.

The baseline-normalized formulas and missing-data rules above are this module's explicit product contract, not an assertion that every OKR method uses identical arithmetic.
