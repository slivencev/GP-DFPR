# Budgeted certification of structural reconfiguration under delayed execution

## Research question and scope

The controller must decide both **what to evaluate** and **what can safely be concluded from the available evaluations**. A lexicographic selector supplied with all exact candidate KPIs does not solve the information-acquisition problem. Once the same information is supplied, depth ordering itself remains lexicographic. The research target is the acquisition/certification contract under stale information and action delay, not a rebranding of the final ordering.

This note specifies a finite-action, bounded-error model. The claims below are conditional elementary results based on interval/set-membership reasoning. They are not claimed as new general theorems in safe optimization. Scholarly novelty of their application and combination remains to be established against the related methods listed below.

## 1 Observations and propagated intervals

For action a and goal coordinate i, let m_i(a,t) be a normalized margin; feasibility means m_i(a,t) >= 0 for every i. The action inventory A is complete for the modeled decision. An evaluation at time s returns z_i(a,s) with |z_i − m_i(a,s)| <= eta_i. Assume a known bound |m_i(a,t+1) − m_i(a,t)| <= L_i and known coordinate range [-1,1].

An observation yields, for any t >= s,

    lower_i(a,t) = max(-1, z_i(a,s) − eta_i − L_i(t−s)),
    upper_i(a,t) = min( 1, z_i(a,s) + eta_i + L_i(t−s)).

Intersect all sound propagated observation intervals for the same action. Unobserved candidates retain [-1,1]. The implementation propagates the previous intersection and intersects a fresh observation; this is valid because expansion by the same coordinatewise drift radius commutes with taking the maximum lower endpoint and minimum upper endpoint.

**P1 Interval inclusion.** Every true margin remains within these bounds if the observation, range and drift assumptions hold. Proof: the triangle inequality bounds the change since observation; intersecting sets that all contain the true value preserves containment. An empty intersection is inconsistent with the assumed model and observations. It is not a certificate that the physical action is infeasible. Conversely, nonempty intervals do not prove that the assumptions hold; some misspecifications remain undetected.

## 2 Three-valued feasibility and global infeasibility

Define the certainly feasible and possibly feasible sets at a common time:

    F_minus(t) = {a : lower_i(a,t) >= 0 for every i},
    F_plus(t)  = {a : upper_i(a,t) >= 0 for every i}.

**P2 Sound classification.** F_minus(t) is a subset of the true feasible set F(t), which is a subset of F_plus(t). Thus:

- F_minus nonempty confirms existence of a feasible action.
- F_plus empty confirms physical infeasibility within the complete modeled inventory.
- F_minus empty and F_plus nonempty means insufficient information to conclude either way.

Proof follows coordinatewise from P1. The two latter states must not share the word “infeasible.” If the modeled inventory omits reachable actions, the conclusion is only inventory-relative infeasibility. Exhausting the query budget is not a mathematical infeasibility certificate.

**Information lower bound.** Without cross-candidate information, if an unevaluated action retains an interval containing both a feasible and an infeasible margin vector, a correct algorithm cannot certify global infeasibility. There are two indistinguishable plants consistent with the queried observations: in one, the unqueried action is feasible; in the other it is not. Hence a cold-start worst-case global-infeasibility certificate requires evaluating all N candidates. This result rules out any promise that a budget B < N always decides feasibility in one instant. Old evaluations can help only while their propagated bounds remain informative.

## 3 Completion-time certificates and minimum-depth brackets

Let a_minus be the active configuration and d(a_minus,a) its change depth. A switch has a known delay tau(a_minus,a). Holding is treated as a one-step commitment (h=1), whereas a different action uses h=tau. These horizons differ by candidate: completion feasibility is not feasibility at one common future time.

Propagate each candidate's current interval for its own h(a). Let F_minus_arr and F_plus_arr be its corresponding certain/possible completion sets. For the actual future outcomes define F_arr = {a : all m_i(a,t+h(a)) >=0}. Under P1,

    F_minus_arr ⊆ F_arr ⊆ F_plus_arr.

Define D_lower as the minimum change depth among F_plus_arr, and D_upper as the minimum among F_minus_arr. Use infinity for an empty set.

**P3 Depth bracket.** D_lower <= D_true <= D_upper, where D_true is the minimum depth in F_arr, also infinity if empty. Proof: taking a minimum over a superset cannot increase it; taking a minimum over a subset cannot decrease it. If both bounds are finite and equal, the minimum feasible completion depth is certified. If no certified action exists, D_upper is infinity and must not be replaced by the deepest available level. The code uses sentinel 4 for infinity because modeled depths are 0..3.

The bracket does not establish optimality of a secondary score over unresolved candidates of the same depth. The prototype breaks ties among certified actions by conservative margin and ID only; it does not claim a globally best secondary score.

**P4 Arrival guarantee.** Executing an action in F_minus_arr guarantees its goal feasibility at arrival, conditional on the stated bounds and actual execution delay not exceeding the assumed horizon. A larger-than-assumed delay invalidates this argument unless the interval is recomputed for that delay. The simulation evaluates every command at its scheduled arrival, including a short tail after the scored horizon.

During a nonzero delay the old configuration stays active. To certify uninterrupted feasibility before arrival, additionally require

    lower_i(a_minus,t) − L_i max(0,tau−1) >= 0 for every i.

For zero-delay switches this bridge condition is unnecessary. A command with certified target but uncertified bridge is explicitly marked recovery; continuous service is not guaranteed. If no certified target exists, the retained current action is an uncertified fallback, not a safe action. Initial feasibility, recurrence of a safe action, stability and zero overall violations are not guaranteed by P4.

## 4 Budgeted acquisition rule

At each non-pending instant, propagate the cache. If existing intervals already certify a one-step hold, complete completion-infeasibility, or a finite collapsed depth bracket, stop acquisition without a new query. Otherwise, the first evaluation is the current action and consumes one of B budget units. Recompute completion intervals after every evaluation.

Certificate-directed acquisition prioritizes unresolved candidates at the lowest depth that could lower the certified upper depth bound. Among equal-depth candidates, select the widest current interval and then lowest ID. Never repeat a query of the same action within the instant. Stop on a certified hold, proven completion infeasibility, a finite collapsed depth bracket, or exhausted budget. Select the minimum-depth certified completion action if one is available; otherwise retain with an explicit uncertified status.

The exact implemented tie-break is in prototype.py. This is a heuristic acquisition schedule with sound conditional certificates. No optimality of its query allocation, finite discovery time, or superiority over all active-learning rules is claimed. B=1 may leave no capacity to inspect alternatives because the current observation consumes the whole budget. The benchmark includes that regime rather than concealing it.

## 5 When more evaluations can and cannot resolve the uncertainty

**P5 Delay and noise floor.** With one fresh observation and no stronger prior interval, the arrival lower bound is z_i − eta_i − L_i h. A sufficient condition for every bounded-noise realization to certify a true margin m_i is m_i >= 2 eta_i + L_i h. For this one-observation rule the condition is also necessary for a guarantee over all allowed noise values: choosing z_i = m_i − eta_i makes the lower bound m_i − 2 eta_i − L_i h. More queries of other actions cannot remove this candidate's delay radius. Thus increasing B does not in itself remove uncertainty caused by long execution delays or a small margin.

**P6 Refresh-window sufficiency for outage certification.** Suppose every candidate has, at its last observation, at least one true margin no greater than −gamma, observation error bounded by eta, drift bounded by L, and observation age at most A_max. If gamma > 2 eta + L A_max, each candidate has a strictly negative current upper bound in that coordinate; the inventory is certified currently infeasible. Replacing A_max by A_max+h_max gives a sufficient condition for confirmed completion infeasibility. Proof: z+eta+L age <= −gamma+2 eta+L age. In a schedule that can devote all B evaluations each step to a complete sweep, A_max <= ceil(N/B)−1 at the sweep end. A mandatory current-action refresh, early stopping, query latency or pending commands can increase this age; therefore this sweep bound is not asserted automatically for the prototype's acquisition policy.

These bounds explain why UNKNOWN is a necessary operational outcome even under a correct model. They are simple consequences of the assumed intervals and do not establish that the acquisition heuristic is sample-optimal.

## 6 What differs from the previous paper

The previous formulation supplied every candidate outcome at every instant and applied actions immediately. Here three additional costs and uncertainties are explicit: limited evaluation opportunities, loss of information as cached observations age, and drift between decision and command completion. “No known safe alternative” and “no possible safe alternative” become different observable states. An exhausted evaluation budget cannot be reported as an empty physical feasible set.

The final ordering still has a lexicographic interpretation. The potential contribution is the decision contract tying acquisition, depth uncertainty and delayed execution together. The currently implemented conditional proofs and synthetic benchmark are a first research artifact, not evidence that this combination has no prior art.

## 7 Closest literature to address

- Sui et al., Safe Exploration for Optimization with Gaussian Processes, ICML 2015: https://proceedings.mlr.press/v37/sui15.html . Safe exploration of an unknown function under regularity assumptions is established. Our noninvasive candidate-evaluation interface differs from applying an uncertain configuration to obtain its response; this assumption needs operational justification in a RAN.
- Turchetta, Berkenkamp and Krause, Safe Exploration for Interactive Machine Learning, NeurIPS 2019 (GoOSE): https://proceedings.neurips.cc/paper/2019/hash/4f398cb9d6bc79ae567298335b51ba8a-Abstract.html . The primary abstract and paper identify goal-directed safety exploration as established work. GoOSE uses regularity expressed through a Gaussian-process prior; our prototype uses bounded coordinate drift and noninvasive queries. No numerical comparison or detailed equivalence analysis with GoOSE has yet been performed.
- Safe Online Dynamics Learning with Initially Unknown Models and Infeasible Safety Certificates: https://arxiv.org/abs/2311.02133 . The available abstract already distinguishes limitations of robust certification caused by model uncertainty. Full-text retrieval was unavailable; this prevents a priority claim for that distinction.
- Event-triggered and self-triggered control for linear systems based on reachable sets: https://www.sciencedirect.com/science/article/pii/S0005109818305697 . Propagating uncertainty to reason about future control is established. The present bounded finite-action prototype is not a replacement for dynamical reachability or stability analysis.

Before a journal submission, compare acquisition with a credible active feasibility/safe exploration method under a compatible query interface; evaluate delay-model misspecification and correlated errors; and identify an external data source or simulator that exposes the actual alternative-action evaluations assumed here. Existing single-action ColO-RAN traces do not provide that interface by themselves.
