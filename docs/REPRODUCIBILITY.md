# GP-DFPR reproducibility and provenance

## Imported code: verification complete

The repository contains the complete **50-file author-selected source import** for stages v3, v9, v11, v12, v14 and v15. The checksum-pinned GitHub Actions importer downloaded the referenced S2 ZIP only after verifying its SHA-256 against the author's uploaded original and validating the nested source archives. The import committed [the 50-file source set](SOURCE_IMPORT_COMPLETE.md) and [SHA-256 manifest](../IMPORT_SHA256.json), preserving original source bytes and the v15 GPL-2.0 notice.

Reference: Serhii Liventsev, *GP-DFPR: Simulator and Experimental Data for Goal-Preserving Network Reconfiguration under Partial Observability and Execution Delays*, version 1.0.0. https://doi.org/10.5281/zenodo.22893667.

## Reproducibility is narrower than source transfer

The full archived raw traces, result CSVs, nested source ZIP archives and supplementary figure data remain in Supplementary Data S2. A source-package checkout by itself does not include all the historical input/output data. The authentic v8 predecessor was subsequently supplied separately by the author, passed its original archive manifest and historical v9 checkpoint, and enabled a complete rerun of v9. The four archived v9 CSV outputs were reproduced byte-for-byte. The v8 binary remains outside this public GitHub checkout; see [v8 recovery and v9 rerun](V8_RECOVERY_AND_V9_RERUN.md). Never bypass the original checkpoint.

Previously executed tests and local reproduction of the v15 synthetic component experiment are separately documented in [EXECUTION_AUDIT.md](EXECUTION_AUDIT.md). The complete synthetic v9 experiment was separately rerun after recovery of authentic v8. Successful synthetic tests and v9 reproduction do not establish end-to-end field validity, closed-loop stability or calibrated physical safety.

## Before an additional reproducibility release

1. For any independent v9 recheck, obtain the original author-supplied v8 binary separately and verify its documented SHA-256 before execution.
2. Re-run v12 from its complete documented predecessor and original reference contexts; compare all recorded outputs.
3. Regenerate the manuscript's tabular and plotted figures from the archived primary result data; independently check bootstrap implementation and independent-run sample counts.
4. Preserve all third-party licensing, particularly v15 GPL-2.0 and the curve-provenance documentation.
5. Record exact runtime versions, commands, seeds, outputs, discrepancies and original-data hash digests. Tag a versioned GitHub release only after its scope has been explicitly defined and verified.

## Interpretation

The manuscript's certificates rely on enforced measurement-error, drift, model-range and execution-delay bounds. Certification at command completion does not guarantee uninterrupted service. The source studies are synthetic; the shared-SINR component uses the same surrogate curve family for prediction and evaluation. Do not present the deposited package as hardware or deployed O-RAN validation.
