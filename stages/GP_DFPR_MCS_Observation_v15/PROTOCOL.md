# v15 — shared-channel observation experiment

Fixed before execution, 2026-09-20. Scope: test uncertainty propagation from ONE noisy SINR observation into predictions for MCS 4/10/15. No independent packet-level simulator or physical hardware is available in this package. This is a conditional component-model experiment, not the external validation still required by v14.

Use the already extracted 5G-LENA Table1, BG1, CBS3840 SINR/code-BLER arrays, with original provenance and license. Piecewise-linear interpolation is part of our declared surrogate; extend with BLER=1 below the first knot and 0 above the last knot. These plateaus are model assumptions, NOT validated extrapolation. Report the fraction of intervals entirely inside the published knot range separately. A zero table value is not evidence of zero physical packet-error probability.

MCS efficiencies Qm*R are 2*308/1024, 4*340/1024, 4*616/1024. The success-weighted nominal efficiency g=efficiency*(1−code_BLER) is a toy component KPI, NOT measured throughput or end-to-end goodput. No HARQ, segmentation, PHY overhead, queueing, resource redistribution, path change or action-dependent channel is simulated.

Generate 30 synthetic scalar SINR trajectories, seed components [2026092090,run], run IDs 7000..7029. Start 6.4 dB. At each step target=6.4+5*sin(2*pi*t/240+phase), update by clip(0.15*(target−previous)+U[−0.03,0.03],−0.08,0.08) dB. Phase uniform [0,2pi). Observation noise U[−0.2,0.2] dB. Time is in simulator steps. T=400, extra five steps for prediction horizons.

Measurement periods 1/4/8, delivery latency 2, prediction/actuation horizons 1/3. At decision t, only observations with sample time s+2<=t are available; use the latest scheduled one. A SINGLE observation supports all three MCS. Budget accounting is by observation ID, not three per-action queries.

Evaluator-only effective-SINR shift: delta=0,0.35,0.70 dB, same trace/noise for all cases. This is designed model misspecification, not an experimentally estimated radio discrepancy. Three predictors: point estimate z(s); interval with radius 0.2+0.08*(t+h−s); interval with additional declared model-shift budget 0.4 dB. Predictor never receives delta or true future SINR. Monotonicity gives BLER interval [b(gamma_upper),b(gamma_lower)] and reversed success-efficiency bounds.

Claims: sensor-only intervals must contain surrogate truth for delta=0; shift-budget intervals must contain it for delta<=0.4. Assertions test those cases. Delta=0.70 violates the declared shift bound; failures are recorded rather than suppressed. Point predictions are an intentionally unguarded comparator, not a strong control baseline.

Constraints: code-BLER<=0.1 and success-weighted nominal efficiency>=0.5. Evaluate all three candidates at each scored decision (t=2..399), reporting interval containment, uncertainty, predicted feasible fraction, false feasibility and false infeasibility. No deployed policy/GPR claim. Intervals outside the knot range remain conditional on the surrogate plateau assumption; they must not be promoted to physical certificates.

All 30×3×2×3×3=1620 predictor-case rows retained. Shared trajectories across settings and three derived MCS are correlated; pooled rates are descriptive, not independent-trial inference. No parameter tuning or claimed empirical hard-bound calibration. v14 remains unchanged; v15 does not retrofit real observation semantics onto v3–v12 results.
