# GP-DFPR source import — completed

The author-selected source package has been transferred directly into this GitHub repository. **No PowerShell script or local archive download is required.**

All 50 stage files from the six source-package study stages (v3, v9, v11, v12, v14, v15) are checked in under [stages/](stages/). The original v12 replay contexts and v15 GPL-2.0 source license are included. The SHA-256 record is [IMPORT_SHA256.json](IMPORT_SHA256.json); [the import report](docs/SOURCE_IMPORT_COMPLETE.md) explains its origin and the verified public-deposit checksum.

A pinned [import script](scripts/import_verified_s2.py) and [one-off GitHub Actions workflow](.github/workflows/import-verified-s2.yml) provide an auditable source-import method. [CI](.github/workflows/validate-import.yml) checks all 50 hashes and runs the original v3, v9 and v14 unit tests.

**Important:** the raw historical output/trace ZIP archives and supplementary figure-data CSVs are housed in the research archive, not duplicated in the selected GitHub source package. An authentic v8 predecessor is still needed to rerun the original full v9 entry point. This completed transfer does not by itself imply new independent validation or justify a release declaring all experiments reproduced.

Archive DOI: https://doi.org/10.5281/zenodo.22893667. The author's original source and data licensing is in [LICENSES_AND_REUSE.txt](LICENSES_AND_REUSE.txt); third-party source retains its original licensing.
