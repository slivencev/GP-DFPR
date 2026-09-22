# GP-DFPR source import pack

Extract `GP_DFPR_GitHub_Source_Import.zip` locally before uploading its `stages/` directory to GitHub. This source-only package contains original author-provided stage files and a SHA-256 manifest (`IMPORT_SHA256.json`). It does **not** replace the complete `Supplementary_Data_S2.zip` archive containing the historical ZIPs, raw results and traces.

Executed checks recorded in [docs/EXECUTION_AUDIT.md](docs/EXECUTION_AUDIT.md): v3 9 tests passed; v14 9 tests passed; v9 3 unit tests passed but its complete run requires the missing v8 predecessor; v15 synthetic experiment matched archived `checks.json` and the 9-row `summary.csv`, with 15/1620 negligible final-digit floating-point differences in `per_case.csv`.

**Licenses:** original author code MIT; original author data and narrative documentation CC BY 4.0; v15 includes GPL-2.0 `SOURCE_LICENSE` and `UPSTREAM_PROVENANCE.md` for third-party material. Preserve all upstream notices; do not relicense third-party components under MIT.

Archive named in the manuscript: https://doi.org/10.5281/zenodo.22893667. The exact public deposit bytes have not yet been checked against the uploaded archive.
