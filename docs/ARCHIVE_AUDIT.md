# Supplementary Data S2 — intake audit (23 September 2026)

Source: files supplied by the author in this conversation, `Supplementary_Data_S2.zip` and `LICENSES_AND_REUSE.txt`.

## Integrity verification

- Uploaded outer ZIP SHA-256: `846419b0187d70a04d7572debbcecd58015f15369e3b1683b7efa8e4bec25682`.
- The outer ZIP contains **8 nested historical research ZIP archives**, `SOURCE_ARCHIVES.json`, `EVIDENCE_INDEX.md`, `README.md`, and **5 figure-data CSVs**.
- **8/8** nested ZIP SHA-256 digests match `SOURCE_ARCHIVES.json`.
- Internal file checksums match the nested manifests for v9 (**62/62**), v11 (**37/37**), v12 (**39/39**), v13 (**5/5**), v14 (**8/8**), v15 (**43/43**), and v16 (**4/4**). The v3 `MANIFEST.json` instead records `date`, `python`, `numpy`, and `platform` metadata; it is **not** a file-checksum manifest, and no file integrity conclusion is drawn from it.

## Confirmed archive contents

| Archive | Role |
| --- | --- |
| `GP_DFPR_Partial_Observation_v3.zip` | Earlier acquisition baselines, results and prototype |
| `GP_DFPR_Periodic_v9.zip` | Periodic delayed-control simulator, 48 compressed synthetic traces, code and results |
| `GP_DFPR_Scheduling_v11.zip` | Retrospective scheduling audit and theory |
| `GP_DFPR_Matched_Schedules_v12.zip` | Matched-context acquisition replay |
| `GP_DFPR_Positioning_v13.zip` | Research positioning and source audit |
| `GP_DFPR_Observation_Model_v14.zip` | Shared-observation interface and unit tests |
| `GP_DFPR_MCS_Observation_v15.zip` | Shared-SINR component simulation, code, derived curves, original provenance and GPL-2.0 notice |
| `GP_DFPR_Research_Objective_v16.zip` | Research-objective record |

## First-pass claim checks (archived artifacts, not rerun simulations)

- v9 `checks.json`: **768** controller runs, **230,400** scored steps, **23,059** arrival certificates, **0** reported certificate failures, **3** reported tests, `all_invariants=PASS`.
- v12 `checks.json`: **192** reference runs, **776** episode contexts, **14,168** target-time matching problems, **28,336** reported online-to-oracle checks, **4** reported unit tests and `status=PASS`.
- v15 `checks.json`: **30** trajectories, **1,620** predictor-case rows and **0** reported hard-assumption failures in **644,760** containment checks.
- Extracted figure tables: `closed_loop.csv` 64 data rows, `matched.csv` 48 data rows, and `shared_sinr.csv` 9 data rows; `closed_loop_paired.csv` and `matched_paired.csv` are also present.

These values agree at the reported-count level with the relevant manuscript claims. **No simulation was rerun** in this intake audit, and self-reported test flags must not be mistaken for an independent execution check.

## Release and licensing precautions

The uploaded `LICENSES_AND_REUSE.txt` authorizes original code under MIT, original data and narrative documentation under CC BY 4.0, and preserves third-party licenses. In v15, `SOURCE_LICENSE` contains GPL-2.0 text and `UPSTREAM_PROVENANCE.md` documents external numerical arrays. Do not relicense this third-party material under MIT.

The nested outer `README.md` describes a pre-deposit editorial snapshot accompanying manuscript **v18** and says its local archive had not yet been deposited. The author's separately uploaded licensing statement identifies release **1.0.0** and the Zenodo DOI; these describe different historical stages. **Do not silently modify original archived READMEs** when assembling the GitHub release.

## Remaining checks

1. Compare the uploaded outer ZIP with the actual Zenodo deposit file and metadata; matching an internal checksum manifest does not establish identity with the public DOI.
2. Execute original scripts and unit tests in a controlled environment from the archived sources, recording Python and library versions.
3. Recompute Table 3 and Figures 2–4 from run-level data; inspect the complete figure-data index and the independent-vs-correlated sampling assumptions.
4. Preserve original ZIP archives, their original metadata, GPL-2.0 terms and upstream notices when publishing source.
5. Create a version-tagged GitHub release **only after** deciding whether the repository holds actual verified source files or is explicitly a companion documentation repository.

