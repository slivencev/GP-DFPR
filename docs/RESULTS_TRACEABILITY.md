# GP-DFPR: manuscript claim-to-evidence verification register

Source: author-provided manuscript `GP_DFPR_Main_v19.docx`. This is a **verification plan**, not an assertion that the evidence files have been inspected. All numerical values below are reported by the manuscript. Locate the exact archived source files and check them before marking an item verified.

| ID | Manuscript claim | Location | Expected evidence to locate | Status |
| --- | --- | --- | --- | --- |
| C01 | Periodic study: 24 actions, four impairment durations, budgets 1/2/4/8, delay multipliers 1/2, two policies; 12 traces per duration and 768 controller runs | Table 2; Sections 6–7 | v9 frozen configurations, trace identifiers, per-run metadata | Not yet verified |
| C02 | Periodic study: 230,400 scored steps; 23,059 issued arrival certificates satisfy conditional completion checks | Section 7 | v9 step-level logs, certificate audit and recount script | Not yet verified |
| C03 | Duration 12, delay multiplier 2, budget 8: Pure-sweep GPR 0.7606, Uncovered-first 0.7853, paired difference +0.0247 with pointwise 95% bootstrap CI [+0.0064,+0.0461] | Table 3 | v9 paired run-level records, bootstrap seed and script | Not yet verified |
| C04 | Matched replay: 192 reference runs, 776 episode contexts, 14,168 target-time matching problems | Section 7.1 | v12 context inventory, replay audit, matching log | Not yet verified |
| C05 | Matched replay (duration 12, delay 1, budget 8; Pure-sweep reference context): pooled recall 7.69% vs 82.84%; retrospective bound 83.43% | Section 7.1; Figure 3 | v12 replay outcomes and matcher inputs, denominator audit | Not yet verified |
| C06 | Shared SINR: 30 synthetic trajectories; three MCS choices (4, 10, 15); three sampling periods, two horizons and three shifts | Table 2; Section 8 | v15 protocol, trajectory-generation code, predictor inputs | Not yet verified |
| C07 | Shared-SINR interval predictor at zero shift: 0 / 93,098 false admissions; at 0.35 dB unaccounted shift: 1,262 / 93,098 | Section 8; Figure 4 | v15 candidate-level admission audit and plotting data | Not yet verified |
| C08 | Model-aware 0.4 dB allowance at 0.70 dB shift: 877 / 86,445 false admissions | Section 8; Figure 4 | v15 discrepancy settings and admission audit | Not yet verified |
| C09 | Earlier 30-run Outage study: Certificate-directed below Round-robin by 0.0143 GPR at budget 2, CI [-0.0210,-0.0074] | Section 9.4 | v3 paired run-level data and bootstrap implementation | Not yet verified |
| C10 | Full protocols in Supplementary Material S1 and original research archive in Supplementary Data S2 | Sections 5–6 and availability statement | Actual S1/S2 attachments, checksums, archive inventory | Not yet verified |

## Verification procedure

1. Receive the original Zenodo files or the author's original source archive; record filenames, byte sizes, hashes, version identifiers and applicable licenses.
2. Match v3/v9/v12/v15 scripts and run-level data to claim IDs C01–C10. Preserve source versions without editing original results.
3. Check whether common random traces and observation-noise arrays were used for the paired v9 comparisons, as stated in Section 6.1.
4. Recompute pooled event rates separately from paired run-level mean differences. The manuscript explicitly distinguishes these weighting schemes.
5. Check the bootstrap implementation: 10,000 resamples over **12 independent source runs**, fixed seed, percentile intervals, and no multiplicity correction.
6. Regenerate Figures 1–4 where code and figure data permit; verify legends, axis units and caption-level interpretation.
7. Record any deviation as an open discrepancy; do not substitute manuscript numbers into generated output.

## Interpretation controls

- Arrival certificates are conditional on the enforced noise, drift, model-range and delay assumptions; they do **not** establish field safety.
- Minimum depth among certified alternatives is not necessarily the true feasible minimum depth.
- Matched replay reuses the periodic synthetic environments and is not independent external validation.
- Shared-SINR predictions and evaluator outcomes use a shared surrogate curve family; mismatch tests sensitivity, not measured hardware error.
- Diagnostic recall improvement does not automatically imply better goal preservation.

**Status of register:** all claims await archived-file inspection and independent reproduction.
