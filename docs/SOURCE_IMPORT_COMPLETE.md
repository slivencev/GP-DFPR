# Completed transfer of the original GP-DFPR source package

**Date:** 23 September 2026

**Result:** The automatic importer committed all **50 original stage files** from the author-selected source package to the repository, along with their SHA-256 index `IMPORT_SHA256.json`. The previously imported `LICENSES_AND_REUSE.txt` was also checked against the uploaded original. This is a completed **source-package transfer**, not a claim that the full historical research-data archive or every predecessor has been copied.

**Verified provenance:** The importer retrieved the author's referenced `Supplementary_Data_S2.zip` from the DOI-linked Zenodo record only after checking that its SHA-256 matched the author's uploaded file:
`846419b0187d70a04d7572debbcecd58015f15369e3b1683b7efa8e4bec25682`.
All eight nested archive digests were then compared with the frozen `SOURCE_ARCHIVES.json`. Existing GitHub source files were required to match the original bytes; otherwise the import would abort. The successful commit was `a82f8c4310709172e8593012373030c5e304eb8e`.

## Imported stages and contents

| Stage | Files | Included |
| --- | ---: | --- |
| v3 | 8 | prototype, tests, protocol and report |
| v9 | 8 | model, periodic generator, executable study and protocol |
| v11 | 9 | scheduler, audit script, theory and report |
| v12 | 9 | replay program, original model, scheduler and 2.1 MB contexts file |
| v14 | 7 | evidence gate, tests and observation-model description |
| v15 | 9 | shared-SINR simulator, curve table, protocol, upstream provenance and original GPL-2.0 `SOURCE_LICENSE` |
| **Total** | **50** | SHA-256 indexed |

The author's original `LICENSES_AND_REUSE.txt` accompanies the stage files. Original research code and original data/documentation have different licenses; third-party materials are **not** relicensed by the author's original-work grants.

## Scope and outstanding validation

- The complete original bulk output/trace ZIP archives and supplementary figure-data CSVs remain in Supplementary Data S2, rather than being duplicated into GitHub.
- The previously recorded local tests and v15 reproduction are documented in `EXECUTION_AUDIT.md`; source import does **not** constitute a new end-to-end execution or independent hardware validation.
- The complete original v9 entry point requires an authentic v8 predecessor missing from the supplied S2 collection. Do not remove or bypass this provenance check without documenting the intervention.
- The numerical studies remain synthetic and their guarantees are conditional on their stated assumptions.
- No GitHub versioned release or publication-status claim has been issued solely on the strength of this import.

**Source reference:** https://doi.org/10.5281/zenodo.22893667 (version 1.0.0, as stated in the manuscript).
