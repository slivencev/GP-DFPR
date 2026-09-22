# GP-DFPR reproducibility and provenance

This document describes the status of the companion GitHub repository for the manuscript *Goal-Preserving Network Reconfiguration under Partial Observability and Execution Delays* (Serhii Liventsev).

## Stated archival source

The manuscript cites the version 1.0.0 archive: https://doi.org/10.5281/zenodo.22893667.

It states that the deposit contains simulator source files, frozen experimental protocols, run-level results, synthetic trajectories, checksums, figure data, and a claim-to-evidence index. The manuscript identifies four source-study versions: v3 (earlier acquisition), v9 (periodic control), v12 (matched replay), and v15 (shared observations).

**Verification status:** The content and availability of the Zenodo deposit have not yet been independently checked for this GitHub import. No source code, raw data, or executable reproduction pipeline has yet been imported to this repository. The presence of a DOI in this file is not proof that the listed files have been verified.

## Manuscript-to-experiment map

| Study | Manuscript location | Stated scope |
| --- | --- | --- |
| Periodic closed-loop control | Sections 6–7 | 24 configurations; 768 controller runs, 230,400 scored steps |
| Matched-context acquisition replay | Section 7.1 | 192 reference runs and 776 episode contexts |
| Shared-SINR surrogate component | Section 8 | 30 synthetic SINR trajectories; three MCS configurations |
| Supplementary material | S1, S2 as named in manuscript | Detailed protocols and archived research data |

These studies answer different questions and must not be pooled as independent validation.

## Required checks before declaring the repository reproducible

1. Download and inspect the *actual* Zenodo archive; record deposited filenames, sizes, license notices, and original checksums.
2. Confirm that each of v3, v9, v12, and v15 exists in the deposit and identify its entry point and exact input/output file paths.
3. Preserve the deposited source and provenance; do not silently rewrite the original experiment or substitute synthetic outputs.
4. Record runtime version, operating system, package versions, installation steps, random seeds, and end-to-end execution commands from verified source.
5. Regenerate and compare manuscript claims, tables, and all four figures against deposited result files; document any discrepancy.
6. Identify third-party source, data, and curve licensing separately from the author's original code and data.
7. Run a clean-environment reproduction test and publish the resulting verification log, checksums, and limitations.
8. Publish a versioned GitHub release only after these checks; link it to the corresponding Zenodo version without changing the existing archive retroactively.

## Important interpretation limits

The manuscript's certificates rely on enforced error and drift bounds, valid model assumptions, and the specified execution schedule. Arrival-time certification is not continuous service certification. The closed-loop plant and SINR component study are synthetic; neither represents independent hardware or deployed O-RAN validation.

Contact: Serhii Liventsev, s.liventsev@kpi.ua.
