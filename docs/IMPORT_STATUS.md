# Source import status — 23 September 2026

Author-supplied source: `GP_DFPR_GitHub_Source_Import.zip`, extracted from the author's GP-DFPR Supplementary Data S2 package. Import is **in progress**.

## Verified original-byte uploads

The following eight GitHub files have been compared against the corresponding original ZIP entries using Git blob SHA-1 and match **exactly**:

- `stages/GP_DFPR_Observation_Model_v14/evidence.py`
- `stages/GP_DFPR_Observation_Model_v14/test_evidence.py`
- `stages/GP_DFPR_Observation_Model_v14/README.md`
- `stages/GP_DFPR_MCS_Observation_v15/curves.json`
- `stages/GP_DFPR_MCS_Observation_v15/observation.py`
- `stages/GP_DFPR_MCS_Observation_v15/PROTOCOL.md`
- `stages/GP_DFPR_MCS_Observation_v15/UPSTREAM_PROVENANCE.md`
- `stages/GP_DFPR_Periodic_v9/periodic.py`

Five `requirements.txt` files for v3, v9, v11, v12 and v15 were imported in the preceding step; they state `numpy==2.3.5`. Full source and dependency-chain import is not yet complete.

The original uploaded v14 `evidence.py` and `test_evidence.py` were extracted and run locally with Python's unittest: **9 tests passed**. This checks the evidence-interface semantics, not real radio performance or correctness of unverified input bounds.

## Missing for runnable stage packages

- v9: `model.py`, `run_study.py`, and the original v8 predecessor archive needed by its full run.
- v12: `model.py`, `run_compare.py`, `scheduler.py`, reference contexts and its verified predecessor materials.
- v15: `run_study.py` and **original `SOURCE_LICENSE` GPL-2.0 notice** must be imported before representing this as a complete redistributable component. A provenance Markdown file alone is not the full license.
- Stage-specific remaining protocols and checksums; full archival trace/data remain in the original S2 package.

Do not tag a complete GitHub release or claim full reproducibility until all required files are imported, their source digests checked and the relevant tests rerun. Preserve third-party restrictions.
