# Authentic v8 recovered; full v9 synthetic study rerun

**Audit date:** 23 September 2026. **Author:** Serhii Liventsev.

The original `GP_DFPR_Periodic_v8.zip` was supplied by the author as a separate chat attachment and verified against the authentic `V8_CHECKPOINT.json` embedded in the original v9 archive from Supplementary Data S2. **The original v8 binary is not yet present in this GitHub repository**, so do not assume cloning alone supplies it.

## Authentic predecessor

- SHA-256 of recovered v8 ZIP: `8fa8781be55c86fa1ba1dde43c187a1b746f0bae4589c1d1af8b7a15491c7230`.
- The v9 historical checkpoint contains the exact same SHA-256 and the expected filename.
- v8 ZIP integrity passed; 37 archive entries and 36/36 original internal `MANIFEST.json` SHA-256 entries matched (Windows separators in original manifest were normalized for reading).
- The original v9 predecessor check, comparing the ZIP-embedded v8 `REPORT_RU.md` with the separately extracted report, passed.

v8's **historical** `checks.json` records 432 controller runs, 129,600 scored steps, 10,038 arrival certificates, five scenario tests, and zero recorded certificate failures. **v8 itself was not rerun in this audit**.

## Full v9 rerun

The original v9 model, periodic generator, experiment configuration, seeds and simulation calls were used unchanged. Four duration variants were computed in isolated parallel workers (global-d6/d12/d24/d36), 12 runs each (6000–6011), two execution-delay multipliers, four query budgets and both original policies. The original downstream v9 statistics/bootstrap code was then executed against these rows in its original variant order. The original public v9 source and archived outputs were preserved; the orchestration-only audit harness is a distinct local file.

**Recomputed:** 768 controller runs; 230,400 scored time steps; 23,059 arrival certificates; zero arrival-certificate failures, false infeasibility certificates or hold-certificate failures, conditional on the synthetic model. All **3/3** original v9 unit tests passed (Python 3.13, NumPy 2.3.5).

### Comparison to original archived v9 in Supplementary Data S2

| Artifact | Comparison |
| --- | --- |
| `environment.csv` | Byte-identical |
| `per_run.csv` | Byte-identical |
| `summary.csv` | Byte-identical |
| `paired.csv` | Byte-identical, including deterministic paired bootstrap |
| `checks.json` | Parsed JSON identical; archived file has CRLF line endings |
| 48 environment `.npz` traces | All 144 arrays equal within `1e-14` absolute tolerance; 96 arrays exact; 48 float64 truth arrays differ only by roundoff, maximum `5.551115123125783e-17` |
| `REPORT_RU.md` | Regenerated numeric tables agree, but historical report has additional manually written interpretive paragraphs; not byte-identical |

The original v8 source ZIP and local complete audit bundle are retained separately. For independent replication, obtain the author-supplied v8 ZIP and check its recorded SHA-256; do not fabricate a predecessor or bypass the checkpoint.

## Scope and unresolved dependencies

This recovers the authentic v8 predecessor and successfully reexecutes the complete **v9 synthetic experiment**. It does **not** establish physical-radio or deployed O-RAN validation. It also does not claim independent reruns of v8 or the entire v3–v16 development chain. The v8 package contains a `V7_CHECKPOINT.json`; an original v7 predecessor would be needed if an independent historical v8 rerun were required. The originally deposited S2 archive remains authoritative for full historical result/traces packages.
