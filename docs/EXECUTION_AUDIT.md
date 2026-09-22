# Independent execution audit — 23 September 2026

Scope: author-uploaded `Supplementary_Data_S2.zip`, not a download from the public DOI. All original source files were inspected in a separate staging directory. The only rerun results described here are generated from those files.

## Local environment

- Python 3.13
- NumPy 2.3.5, matching the frozen `requirements.txt` entries.

## Executed tests and experiments

| Component | Action | Result |
| --- | --- | --- |
| v3 partial-observation prototype | Execute original `test_prototype.py` | 9/9 tests passed |
| v14 observation-model gate | Execute original `test_evidence.py` | 9/9 tests passed |
| v9 periodic controller | Import original `run_study.Tests` and execute unit tests directly | 3/3 tests passed |
| v15 shared-SINR component | Run original `run_study.py` from an isolated copy with the original v14 predecessor ZIP and extracted directory | Complete; archived `checks.json` exactly matched rerun; `summary.csv` exactly matched across all 9 rows |
| v15 candidate-level results | Compare 1,620 `per_case.csv` rows | 1,605 rows textually identical; 15 rows differ only by last-digit floating-point serialization in `mean_bler_width` (example: 0.19389637388188194 vs 0.19389637388188197) |

### v15 independently reproduced audit counts

- 30 synthetic trajectories; 1,620 predictor-case records; 1,934,280 candidate evaluations.
- 644,760 conditional containment checks; 0 hard-assumption failures.
- Reported nine-row summary reproduces **exactly**. The tiny CSV last-digit differences do not affect aggregated counts or reported rates.
- This reproduces a synthetic surrogate experiment, **not** ns-3, O-RAN deployment, physical measurement calibration or independent physical counterfactual validation.

## Reproduction blocker: v9 full study

The v9 `run_study.py` unconditionally verifies its parent archive `GP_DFPR_Periodic_v8.zip` and the corresponding extracted v8 report before starting the experiment. That predecessor is **not present** in the uploaded eight-archive collection. Therefore the full original v9 entry point stops with `FileNotFoundError` when executed from the staged v9 package. Its 3 unit tests can be executed independently (and passed), but full v9 rerun cannot yet be declared successful without v8 or an expressly documented provenance-only bypass. Neither the missing predecessor nor the archived output was fabricated or silently replaced.

## Next verification requirements

1. Obtain the authentic v8 predecessor archive and confirm its digest/checkpoint before the full v9 rerun.
2. Independently rerun v12 matched replay with its v11 predecessor and compare all output tables and matching audits.
3. Compare GitHub-imported source file digests with the original nested ZIPs and keep the GPL-2.0 source license and provenance alongside v15-derived third-party curves.
4. Record clean-environment commands, execution timings and regenerated Figure 2–4 data once all relevant predecessor chains are available.
5. Verify that the actual public Zenodo deposit contains the same bytes as the author-uploaded S2 archive before describing GitHub as a mirror of the DOI record.

No published archived outputs were modified by this audit.
