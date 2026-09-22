# Simultaneous infeasibility certificates as a scheduling problem

## Scope

This is an exact solution of a restricted certificate-planning problem, not a new online control policy, a novelty claim, or a guarantee that future observations will be negative. It separates scheduling capacity from acquisition uncertainty. No online controller may use the future outcomes employed by the hindsight audit below.

## Known-lifetime model

Fix a target integer time T. Ignore alternatives whose existing negative witness is guaranteed to remain valid at T. For each remaining alternative a, one unit-cost measurement must be scheduled at an available integer time s. Capacity at time s is b_s (zero during blackouts). A measurement of a is ASSUMED to deliver a negative witness valid at s,...,s+ell_a−1, with known positive integer lifetime ell_a. Queries cannot precede release r_a. Thus allowed times satisfy max(r_a,T−ell_a+1)<=s<=T.

This promised lifetime must follow from an explicit model assumption or be treated as an oracle parameter. It is not implied by the current cache. A stale witness gives no guarantee of a renewed negative observation.

Define l_a=max(r_a,T−ell_a+1), and C(s,T)=sum of available capacities at times s,...,T. A target-time certificate can be scheduled **if and only if**

    #{a : l_a >= s} <= C(s,T)

for every distinct release l_a, with jobs whose l_a>T immediately infeasible. Empty job sets are feasible. Capacity before the earliest l_a is irrelevant.

**Necessity.** Jobs released no earlier than s can only occupy slots at or after s. Their number cannot exceed that suffix capacity.

**Sufficiency.** Expand time capacities into identical unit slots and process jobs in descending l_a. Assign each to the latest unused slot with time >=l_a. If assignment fails for a job released at s, every slot at or after s was already used by earlier processed jobs, all of which have release >=s. Adding the failed job violates the displayed suffix inequality. Hence the inequalities prevent failure. The algorithm constructs a valid schedule and is polynomial; this is a standard nested-window scheduling argument, not an asserted new theorem.

With equal release r and lifetime ell, the condition reduces to N_remaining <= sum_{s=max(r,T−ell+1)}^T b_s. With constant budget B and no blackouts, N_remaining <= B*min(ell,T−r+1). This makes explicit why a long episode alone need not suffice when witness lifetimes are short.

Under the earlier bounded-margin assumption, a query with true negative witness margin at most −gamma, noise magnitude eta, and drift L>0 provides a guaranteed fresh upper margin at most −gamma+2eta. Validity at offset d requires L*d<gamma−2eta. If gamma>2eta, the number of certified integer offsets is ell=ceil((gamma−2eta)/L); equality at expiry is excluded. This is a sufficient lifetime from a bound, not the exact lifetime of every realized observation.

## General observation-dependent windows

For known possible measurement outcomes at each (a,s), valid query times need not form a suffix interval. Form a bipartite graph: one job per remaining alternative, one vertex per unit query slot, and an edge when that measurement yields a witness valid at target T. A matching covering every job is exactly a valid schedule. Maximum bipartite matching therefore solves the fixed-T hindsight problem; the simple suffix inequalities are no longer generally sufficient for non-nested windows.

The implementation returns a Hall-deficiency witness when matching fails: a set of jobs whose neighboring query slots are fewer than its size. This identifies a capacity obstruction in the stated graph, not physical infeasibility of the network.

## Hindsight audit on saved v9 data

For a truly empty episode beginning at r, allow queries only at r,...,T, with B slots at every step and no execution blackouts. An edge (a,s) exists when the realized noisy measurement z(a,s) provides a negative interval upper witness at T:

    min_i [z_i(a,s)+eta+L*(T−s)] < 0.

The audit sees all counterfactual query outcomes. It is an exact cold-start, single-target existence test under realized data and the inherited per-query interval rule. It is NOT an executable causal policy. Schedules for different targets may conflict, so the fraction of individually attainable target times is not necessarily attainable by one schedule. Compared with the original controllers, this audit has extra hindsight and no execution blackout, but loses pre-episode cached evidence; it is therefore not an unconditional upper bound on their reported recall. No superiority comparison is made.

Outputs distinguish targets with any feasible matching, unattainable targets, and episodes for which at least one target is attainable. They do not certify that targets lacking a matching were impossible for every richer predictor or model.
