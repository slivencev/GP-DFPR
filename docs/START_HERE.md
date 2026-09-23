# Start here: GP-DFPR

Repository for the manuscript *Goal-Preserving Network Reconfiguration under Partial Observability and Execution Delays*, Serhii Liventsev.

## Source import status

**Completed:** all 50 author-selected source-package files were imported directly from the checksum-verified original Supplementary Data S2 archive. The verified package includes experimental stages v3, v9, v11, v12, v14 and v15, the v12 saved replay contexts, and the original v15 GPL-2.0 source license. The author's original `LICENSES_AND_REUSE.txt` accompanies the files.

- [Source import report](SOURCE_IMPORT_COMPLETE.md)
- [SHA-256 manifest](../IMPORT_SHA256.json)
- [Import script](../scripts/import_verified_s2.py) and [GitHub Actions workflow](../.github/workflows/import-verified-s2.yml)
- [Independent execution audit](EXECUTION_AUDIT.md) and [reproducibility limitations](REPRODUCIBILITY.md)
- [Results traceability](RESULTS_TRACEABILITY.md), [CITATION.cff](../CITATION.cff), [licensing](../LICENSES_AND_REUSE.txt)

Research archive version 1.0.0 identified by the author: https://doi.org/10.5281/zenodo.22893667.

## What remains outside GitHub

The full historical ZIP archives, raw traces, archived result tables and figure-data CSVs belong to the complete Supplementary Data S2 deposit, rather than this selected source-package import. The authentic v8 predecessor was subsequently provided separately by the author; its SHA-256 matched the original v9 checkpoint and the complete synthetic v9 study was rerun. The v8 binary is retained outside the public GitHub source checkout. See [v8 recovery and v9 rerun](V8_RECOVERY_AND_V9_RERUN.md).

An imported runnable-looking script is not itself an independently reproduced study or a deployed-network guarantee. The completed historical tests and separately rerun v15 component experiment are documented in [EXECUTION_AUDIT.md](EXECUTION_AUDIT.md). The full synthetic v9 computation has since been rerun; no new end-to-end re-execution of every other stage is claimed.
