# v9: duration/budget boundary study

Fixed before execution, 2026-09-20. Unchanged Pure-sweep and Uncovered-first policies. New independent run IDs 6000..6011, paired between all cells. No algorithm fitting or selection. The results extend the same synthetic generator, not external validation.

Global periodic impairment only; period 60, warm-up 60, target amplitude 0.65. Scheduled durations 6/12/24/36 steps. Actual infeasible episodes are computed from truth and may be absent or differ from the schedule. Same bounded drift/noise and margin dynamics as v8. Delays 1/2 times intervention depth; budgets 1/2/4/8. Four durations × two delays × four budgets × two policies × 12 seeds = 768 controller runs, 230400 scored steps.

Primary diagnostic quantities: common-grid recall of physical-infeasibility certificates, missed episodes, restricted detection waiting time. Recall is undefined for zero actual-empty steps. Report all cells including absent events. Unit of independent replication is the run, not an individual pulse or time step.

Operational quantities: GPR, queries, commands, and violations when some physically feasible alternative exists. With E=empty_steps/T, this last fraction is 1−E−GPR because all times with empty inventory necessarily violate the current-action constraints. This is an oracle descriptive decomposition, NOT a claim that violations could have been avoided given the available observations or execution delays. 1−E is an instantaneous physical feasibility ceiling; it is not an achievable causal control guarantee.

Paired pointwise 95% bootstrap intervals, 10000 draws, seed 2026092060, for Uncovered-first minus Pure-sweep per cell and metric. Exclude undefined recall pairs and record n. No multiplicity adjustment or global superiority claim. Independent seed validation of one fixed comparison, but synthetic cases and analysis objectives were chosen using earlier findings; do not call the complete study externally validated or an untouched model family.

Save raw truth/noise/scope arrays, all results, assumptions and tests. No post-result changes to algorithms or scenario parameters. Tests cover duration boundaries, matched streams, drift/noise and the violation decomposition; all inherited certificate assertions remain active. No inference of a universal detection threshold from a finite grid.
