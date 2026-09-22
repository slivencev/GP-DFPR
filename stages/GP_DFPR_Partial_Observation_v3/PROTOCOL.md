# Partial observation and delayed execution prototype v3

Frozen before benchmark execution, 2026-09-20. This is a NEW abstract decision-layer experiment. No NR fidelity, external validation, first-in-literature claim, or guaranteed continuous service is asserted. v1/v2 records remain unchanged.

## Information and physical assumptions

24 configurations: PHY setting 0..2, LINK setting 0..1, route 0..3. Two normalized goal margins in [-1,1], both feasible iff nonnegative. Deepest changed component defines depth 0/1/2/3. A noninvasive evaluation returns the two current margins of one candidate with bounded coordinatewise error eta=0.01. Evaluations are synchronous and do not apply the action. Their cost is one budget unit each. This information interface is an assumption, not something supplied by the existing ColO-RAN traces.

The controller receives no latent plant state or unqueried candidate outcome. It knows a valid per-step margin drift bound L=0.04 for both coordinates and the range [-1,1]. Query errors and all candidate truth are pre-generated independently of controllers and shared across policies. Cached interval bounds propagate by L per elapsed step; a fresh observation interval intersects the propagated interval. Empty intersection is reported as a violated modeling assumption, not physical infeasibility.

Delays are [0,1,2,3] steps by depth, tested also at multipliers 0 and 2. While a command is pending, the old configuration remains active until arrival; there is no preemption and no further command or query. At arrival the new action becomes active before satisfaction is scored. A selected target must have all lower margins nonnegative at its own arrival horizon. This certifies arrival only. If the current action cannot be certified through the waiting period, the command is labeled a recovery action; no uninterrupted-feasibility promise is made.

## Decision contract

For an instant t, certainly feasible actions have all lower bounds >=0; certainly infeasible actions have at least one upper bound <0; all others are unresolved. Global confirmed infeasibility requires every action to be certainly infeasible. The absence of a certainly feasible action is not sufficient.

For command completion, each candidate uses its depth-dependent delay; propagate both bounds to that horizon. This creates a distinct completion-feasibility classification, which must not be confused with common-time physical feasibility. The minimum possible completion depth and minimum certified completion depth form a depth bracket; a singleton bracket certifies minimum true completion depth under the declared bounds.

If the current action is certified to remain feasible for one further step, retain it and issue no action. Otherwise, acquire up to B evaluations and select the shallowest certified completion-feasible alternative, breaking ties by larger minimum lower margin and then ID. If no such alternative is known, report unknown or confirmed completion infeasibility as appropriate and retain current as an UNCERTIFIED fallback. Never label that fallback safe. Query policies share identical certificates, action selection and timing.

## Acquisition policies and budget

Budgets B={1,2,4,8}; current-action evaluation counts toward B. Each non-pending decision first tries one fresh query of the current action, unless its cache already certifies a one-step hold. Stop early on a certified one-step hold or fully certified completion infeasibility. Also stop when a certified switching target has proven minimum completion depth. Remaining acquisition differs:

- Certificate-directed: unresolved candidates at the smallest depth that could improve the certified depth bracket; choose the widest uncertainty interval, then lowest ID. Do not query a candidate twice in one instant.
- Round-robin: persistent cyclic index among unqueried candidates.
- Uniform: seeded uniform choice among unqueried candidates.

No policy reads actual unqueried feasibility to choose a query. A full-information interval reference observes all current candidates exactly, but still applies the same drift-based future bound and delays. It is an information upper reference, not an equal-budget comparator or a future-aware oracle.

## Synthetic environments and analysis

Two predefined processes: Local (slowly changing preferred route) and Outage (includes a common adverse target interval). Margins evolve toward structured targets with bounded drift, all per-step changes clipped at L. 30 paired independent seeds per scenario, 300 scored steps plus enough tail steps to resolve every issued command. Master seed 2026092004; bootstrap seed 2026092005; 5000 paired run resamples. All settings are fixed before test results. No test-driven tuning or selective reruns.

Primary integrity checks: actual queried observations lie in noise bounds; actual margins stay inside propagated intervals; no certified infeasible action is actually feasible; no issued arrival certificate fails under the valid model; depth brackets contain the oracle minimum completion depth when it exists; no budget overrun. These are conditional invariants, not empirical novelty claims.

Report GPR across every scored step including pending execution, actual changes, mean queries per scored step, unresolved-state rate, confirmed-infeasibility rate, command count, certified-arrival violations, recovery-command fraction, minimum-depth certification fraction and interval width. Paired differences compare acquisition policies at equal B and delay. All outcomes, including worse cases, are retained. The current-time negative oracle test checks that empty certified-safe set is never mistaken for physical infeasibility. A separate adversarial delay test demonstrates that ignoring action delay can give a false arrival guarantee; this negative control is not presented as a tuned baseline.

## Attribution boundary

Set-membership intervals, safe exploration, and reachability under delayed observations are established ideas. The proposed research object is their explicit combination with a structural depth bracket, query budget and delayed command contract. Its scholarly novelty requires comparison with SafeOpt/GoOSE, interval estimation and active feasibility determination. This initial benchmark alone cannot establish that priority.

## Post-run implementation clarification

The code checks its stated early-stop conditions before every query, including the first. Therefore a cached proof of completion infeasibility or a finite collapsed depth bracket can also skip the fresh current-action observation, not only a certified hold. If any query is required, its first candidate is current. This clarifies the prose above; no implementation, selected setting, or result was changed after inspection. Acquisition cannot certify optimality of the secondary score among same-depth unqueried actions. Per-run fractions for recovery and depth certification use zero as a storage convention when commands=0; the command count must accompany their interpretation.
