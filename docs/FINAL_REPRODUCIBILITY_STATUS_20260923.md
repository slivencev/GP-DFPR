# GP-DFPR reproducibility finalization — 23 September 2026

**Status:** source-package transfer complete; authentic historical v8 recovered; full original v9 *synthetic* experiment reproduced. This finalizes the **v8→v9 audit milestone**, not the entire historical v3–v16 chain or real-network validation.

## Author-controlled archival chain

- Original Supplementary Data S2: [Zenodo record 10.5281/zenodo.22893667](https://doi.org/10.5281/zenodo.22893667); the repository's checksum-pinned importer validated S2 prior to its 50-file source transfer. The 50-file manifest is [IMPORT_SHA256.json](../IMPORT_SHA256.json).
- Authentic recovered `GP_DFPR_Periodic_v8.zip` (separate author-supplied attachment): SHA-256 `8fa8781be55c86fa1ba1dde43c187a1b746f0bae4589c1d1af8b7a15491c7230`. Its internal 36/36 manifest digests, ZIP integrity and original v9 `V8_CHECKPOINT.json` reference passed.
- Original archived `GP_DFPR_Periodic_v9.zip` in S2: SHA-256 `e4965a1a1615b341d94a1b4267024d618d51f506e2c931c1a4ae41a1c76af339`.
- Final local audit bundle, retained in the author's Library at `/Программы/GP-DFPR/GP_DFPR_v8_v9_Verified_Audit_20260923.zip`: SHA-256 `945c68e8fb90f01a1f3872f30525449973c683dcd9623a1b1f928d5f9c4a5c99`; ZIP integrity verified; 57 entries, including original v8 ZIP, complete rerun CSVs, 48 synthetic traces, comparison JSON, test log and narrative audit. The original v8 ZIP is also separately retained in that Library folder.

These two local Library items are **not** represented as files already committed to this public GitHub repository. Do not fabricate a GitHub download URL for them.

## Verified v9 rerun

- Python 3.13; NumPy 2.3.5; original study source, configurations, seeds and downstream aggregations. Isolated four-worker orchestration did not modify the archived source.
- **768** controller runs; **230,400** scored steps; **23,059** conditional arrival certificates; **0** recorded arrival/false-infeasibility/hold-certificate failures in the synthetic environment.
- **3/3** original v9 unit tests passed.
- **Four CSVs byte-identical** to original v9: `environment.csv`, `per_run.csv`, `summary.csv`, `paired.csv` (including deterministic paired bootstrap).
- `checks.json`: semantically identical after parsing; archived newline formatting differs.
- 48 trace ZIPs / 144 arrays: all within absolute `1e-14`, 96 exactly equal; maximum float64 truth difference `5.551115123125783e-17`. Regenerated `REPORT_RU.md` does **not** reproduce the archived report's extra manually written interpretive paragraphs byte-for-byte.

[Full v8/v9 recovery report](V8_RECOVERY_AND_V9_RERUN.md) · [Prior execution audit](EXECUTION_AUDIT.md) · [Source transfer record](SOURCE_IMPORT_COMPLETE.md) · [Scope and limitations](REPRODUCIBILITY.md)

## Explicit limits and release status

1. Authentic v8 **archive** was verified; its original complete v8 experiment has not been independently rerun. It references an earlier v7 checkpoint.
2. The archive import and v9 rerun do not constitute independent v12 replay, every-stage reproduction or real RF/O-RAN validation.
3. Preserve original data, historical outputs, third-party GPL-2.0 licensing, original MIT/CC BY 4.0 scope and original DOI metadata.
4. A separately scoped, tagged GitHub release or new Zenodo deposition is **not** implied by this completed audit; publication of a new release should be an explicit separate action.

**Final decision for this milestone:** close the missing-v8 provenance and full-v9-rerun issues in the research audit; leave broader experimental validation open.
