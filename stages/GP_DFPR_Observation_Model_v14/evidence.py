"""Evidence gate, not a radio measurement backend or a proof of input bounds."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Evidence:
    action: str
    mean: tuple
    radius: tuple
    observed_at: float
    received_at: float
    drift: tuple
    valid_until: float
    domain: str
    bound_kind: str  # hard_assumption, statistical, empirical
    source_id: str
    assumption_ref: str

def strict_interval(e,action,domain,now,horizon):
    if horizon<0:raise ValueError('negative horizon')
    if not e or e.action!=action or e.domain!=domain:return None,'UNSUPPORTED'
    if e.bound_kind!='hard_assumption':return None,'NONDETERMINISTIC_EVIDENCE'
    if not e.source_id or not e.assumption_ref:return None,'MISSING_PROVENANCE'
    if not e.observed_at<=e.received_at<=now:return None,'NOT_AVAILABLE'
    target=now+horizon
    if target>e.valid_until:return None,'OUTSIDE_VALIDITY_DOMAIN'
    if not len(e.mean)==len(e.radius)==len(e.drift) or not e.mean:raise ValueError('dimension mismatch')
    if not all(math.isfinite(x) for x in (*e.mean,*e.radius,*e.drift)):return None,'UNBOUNDED'
    if any(x<0 for x in (*e.radius,*e.drift)):raise ValueError('negative bound')
    radius=[r+l*(target-e.observed_at) for r,l in zip(e.radius,e.drift)]
    return ([v-r for v,r in zip(e.mean,radius)],[v+r for v,r in zip(e.mean,radius)]),'CONDITIONAL_HARD'

def inventory_status(intervals):
    if not intervals:return 'UNKNOWN'  # empty configured inventory is a setup issue
    if any(p is not None and all(x>=0 for x in p[0]) for p in intervals):return 'CERTIFIED_FEASIBLE'
    if all(p is not None and any(x<0 for x in p[1]) for p in intervals):return 'CERTIFIED_INFEASIBLE'
    return 'UNKNOWN'

def propagated_radius(model_error,sensitivities,input_errors):
    if len(sensitivities)!=len(input_errors):raise ValueError('dimension mismatch')
    if any(not math.isfinite(x) or x<0 for x in [model_error,*sensitivities,*input_errors]):raise ValueError('invalid bound')
    return model_error+sum(k*e for k,e in zip(sensitivities,input_errors))

def split_conformal_radius(scores,alpha):
    """Quantile arithmetic only; caller must justify exchangeability and score choice."""
    if not 0<alpha<1:raise ValueError('invalid alpha')
    if any(not math.isfinite(x) or x<0 for x in scores):raise ValueError('invalid score')
    k=math.ceil((len(scores)+1)*(1-alpha))
    return math.inf if k>len(scores) else sorted(scores)[k-1]
