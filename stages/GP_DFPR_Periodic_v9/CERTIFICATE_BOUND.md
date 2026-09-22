# Common-time certificate: elementary coverage and freshness bounds

These are elementary consequences of the bounded model, not a novelty claim. They clarify the interpretation of v9 and refine the earlier v3 coverage discussion. A theorem about one sufficient probing schedule is not a guarantee for every implemented controller.

Let N independent alternatives be initially unresolved, with no side information that certifies any alternative infeasible. A query observes one alternative; at most B distinct alternatives can be queried per decision step.

**Coverage lower bound.** In the worst case, an exact certificate that the feasible inventory is empty requires observing all N alternatives. Otherwise two environments can agree on every observation but differ in whether an unobserved alternative is feasible. Thus at least ceil(N/B) query rounds are necessary under these assumptions. For an episode sampled at t0,...,t0+D−1, this implies D>=ceil(N/B) if the certificate must be constructed from scratch inside that episode. Cached valid evidence or structural coupling invalidates this cold-start premise; pending execution may increase elapsed time beyond query-round count.

**A sufficient freshness condition for a full sweep.** Suppose during a sweep each alternative has an observed constraint coordinate with true margin at most −gamma, all coordinate observation errors are bounded by eta, and drift is bounded by L>0. Assume no pauses and B new alternatives queried every step until coverage. Let q=ceil(N/B). At the end of the qth round the oldest observation has age at most q−1. The propagated upper margin for its witness is at most −gamma+2*eta+L*(q−1). Therefore gamma>2*eta+L*(q−1) suffices for all alternatives to be simultaneously certified infeasible. Equality is insufficient because margin zero is feasible. Intersecting old and new intervals can only tighten the bound.

For nonuniform witness margins/noise/drift and arbitrary actual observation times t_a, the corresponding sufficient inequalities are gamma_a>2*eta_a+L_a*(t_end−t_a) for every alternative a, using its negative witness coordinate. These inequalities do not predict whether future measurements will actually supply the assumed negative margins.

At N=24, eta=0.01, L=0.04, this full-sweep sufficient margin threshold is 0.94 for B=1, 0.46 for B=2, 0.22 for B=4 and 0.10 for B=8. These are analytical sufficient thresholds for the stated schedule, not estimated phase transitions in v9 and not necessary thresholds for every possible method. A weaker negative witness can still succeed through a better schedule, useful cached information or tighter models.

Next validation should record actual witness margins and ages, and distinguish lack of coverage from loss of freshness. Prediction of periodicity may help schedule measurements but must not be substituted for a verified negative witness in an exact infeasibility certificate.
