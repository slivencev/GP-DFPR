# Independent v12 and v15 synthetic reruns; manuscript consistency — 23 September 2026

**Scope:** original author-supplied `Supplementary_Data_S2.zip`, recovered v8/v9 audit bundle and `GP_DFPR_Main_v19.docx`. This is an independent local execution of archived **synthetic** scripts, not validation against a live Zenodo download or real O-RAN hardware. Original historical archives were not edited.

## v12 matched replay

The original v12 `run_compare.py` was executed in a clean output directory with the authentic v11 predecessor ZIP and its extracted report, and original v9 synthetic traces. The original four unit tests passed. Rerun `checks.json`: **192** reference runs, **776** episode contexts, **14,168** target problems, **14,168** reference-cache replay checks, **28,336** online-implies-oracle checks; status PASS.

`episodes.csv`, `targets.csv`, `summary.csv` and `paired.csv` were **byte-identical** to the historical v12 files. `checks.json` was parsed-identical (formatting differs). `contexts.json` contains **252** differences in float64 `lo`/`hi` entries across 776 contexts, maximum absolute difference **1.1102230246251565e-16**; no other context fields differed. These are rounding differences, not byte-identical context archives.

v12 reuses existing v9 trajectories, initial caches, reference execution pauses and current-action paths. It measures information acquisition under matched contexts, **not** a new closed-loop GPR.

## v15 shared-SINR component

The original v15 `run_study.py` was executed using the authentic v14 predecessor ZIP and its extracted `OBSERVATION_MODEL_RU.md`. Rerun: **30** synthetic trajectories, **1,620** case rows, **1,934,280** candidate evaluations, **644,760** conditional containment checks, **zero** hard-assumption failures. `summary.csv` was **byte-identical**; `checks.json` parsed-identical; **15/1,620** `per_case.csv` rows differed only in the last floating-point digits of `mean_bler_width`. All remaining per-case fields matched.

The predictor and evaluator share the same tabulated component curves; this is **not** independent RF model calibration or a full network deployment.

## Main manuscript quantitative audit

The author-supplied `GP_DFPR_Main_v19.docx` reports v9 totals (768 controller runs, 230,400 steps, 23,059 arrival certificates) and v12 totals (192 reference runs, 776 contexts, 14,168 target problems, 14,168 replay checks, 28,336 implication checks); these agree with the rerun checks. All four selected rows of the manuscript's main-text Table 3 (duration 12/36; B=4/8; delay multiplier 2) agree at displayed precision with the independently reproduced v9 `summary.csv` and `paired.csv`, including the paired bootstrap intervals.

These are pointwise intervals over **12 source runs** and are not independent step-level samples or multiplicity-adjusted inference. Mixed or unfavorable GPR outcomes are preserved.

## Remaining gates

The author has retained the full compact audit bundle `GP_DFPR_Automated_Final_Audit_20260923.zip` and original v8/v9 audit bundle in Library `/Программы/GP-DFPR/`. The compact bundle includes the detailed audit report, claim-to-evidence CSV, comparison JSONs, rerun logs, and key regenerated v12/v15 tables. **It is not itself uploaded to this GitHub source checkout.**

Figure-by-figure visual audit, live Zenodo deposit byte verification, final submission-guideline check and any real-radio validation remain separate tasks. No new DOI or versioned public release is asserted by this audit. Preserve the original v15 GPL-2.0 source notice and other license boundaries.

See also [v8 recovery and v9 rerun](V8_RECOVERY_AND_V9_RERUN.md) and [final v8/v9 reproducibility status](FINAL_REPRODUCIBILITY_STATUS_20260923.md).
