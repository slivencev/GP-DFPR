# v11 protocol, fixed before audit

First verify v10 archived report; leave v3–v10 unchanged. This stage formalizes known-lifetime scheduling and validates an exact matching solver. It does not alter or benchmark a new online policy.

Exhaustively enumerate all 3-job/3-slot graphs (512 graphs) and compare matching with brute force; check reported Hall witnesses. Also compare nested-window greedy schedules with general matching for 500 seeded random instances with releases, unequal lifetimes, capacities and blackouts. Test expiry equality and empty inventory cases.

Audit saved v9 global-d12 and global-d36 environments, runs 6000..6011, budgets 1/4/8. For each truly empty target time T, allow cold-start queries from the beginning of its true-empty episode, using realized noisy counterfactual observations. No cached pre-episode evidence, no actuation blackouts, no online future access. The model and limits are detailed in THEORY.md. No causal-policy or achieved-recall claim will be made.

Report every duration/budget pair, by run and aggregated. Targets within a run are dependent; no statistical superiority inference. Save input traces, exact test results, feasible witness examples and obstruction examples. Check any reported feasible matching has <=B measurements per step and every chosen negative witness remains valid at T; assert target truth is empty. Fixed-target feasibility across multiple T does not imply a jointly executable schedule across those T.
