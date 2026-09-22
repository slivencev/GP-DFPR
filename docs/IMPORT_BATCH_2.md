# Direct import batch 2 — 23 September 2026

Original source: author-uploaded `GP_DFPR_GitHub_Source_Import.zip`, itself assembled from the author-uploaded `Supplementary_Data_S2.zip`. No source modifications are made in this batch. The original archive is the authoritative source; do not infer independent public-Zenodo byte identity from this log.

## New files in this batch

| Path under `stages/` | Purpose | Exact match to original Git blob |
| --- | --- | --- |
| `GP_DFPR_Scheduling_v11/scheduler.py` | Exact unit-capacity matching and nested-window scheduling | Yes |
| `GP_DFPR_Matched_Schedules_v12/scheduler.py` | Same archived scheduler source in the replay package | Yes |
| `GP_DFPR_Observation_Model_v14/package.py` | Historical packaging/checkpoint script; requires predecessors | Yes |
| `GP_DFPR_Periodic_v9/PROTOCOL.md` | Frozen periodic-control protocol | Yes |
| `GP_DFPR_Scheduling_v11/PROTOCOL.md` | Frozen matching-audit protocol | Yes |
| `GP_DFPR_MCS_Observation_v15/run_study.py` | Original shared-SINR experiment entry point | Yes |

For each item, the uploaded Git blob SHA was checked against a Git blob SHA computed from the corresponding original ZIP entry. These are identity checks of files, **not** proof that any complete stage package can yet run from the GitHub checkout.

## Critical next files

- v15 `SOURCE_LICENSE` (original GNU GPL-2.0 full text), which **must** accompany the original third-party-derived curves and their provenance; do not omit it when packaging for redistribution.
- v14 `OBSERVATION_MODEL_RU.md` and companion test metadata, needed for the original v15 predecessor check.
- v9/v12 `model.py` (identical original bytes), the v9 `run_study.py`, and the v12 `run_compare.py`.
- v11 `run_audit.py` and historical predecessor material.
- v12 `contexts.json` is ~2.1 MB: retain in the archival data package and avoid claiming it has been copied to GitHub until uploaded and verified.

The v9 full experiment also requires the authentic v8 predecessor, which is absent from the author's supplied S2 archive; no replacement is invented. v15 original `run_study.py` also checks for the historical v14 ZIP and corresponding v14 model document.

**Publication status:** partial source import. No GitHub reproducibility release or tag is issued.
