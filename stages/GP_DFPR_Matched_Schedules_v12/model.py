"""Budgeted interval certificates and delayed structural control. NumPy only.

Research prototype, not a validated radio simulator. See PROTOCOL.md and THEORY.md.
"""
from pathlib import Path
import itertools,json,csv,hashlib,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
A=np.array(list(itertools.product(range(3),range(2),range(4))),int)
N=len(A);L=.04;ETA=.01;T=300;SEED=2026092004
DIFF=np.any(A[:,None,:]!=A[None,:,:],axis=2)
DEP=np.where(A[:,None,2]!=A[None,:,2],3,np.where(A[:,None,1]!=A[None,:,1],2,DIFF.astype(int)))

def classify(lo,hi):
    safe=(lo>=0).all(axis=1);impossible=(hi<0).any(axis=1)
    return safe,impossible,~(safe|impossible)

class Cache:
    def __init__(self):
        self.lo=np.full((N,2),-1.);self.hi=np.full((N,2),1.);self.time=0
    def propagate(self,t):
        dt=t-self.time;assert dt>=0
        self.lo=np.maximum(-1,self.lo-L*dt);self.hi=np.minimum(1,self.hi+L*dt);self.time=t
    def observe(self,a,y,eta=ETA):
        low=np.maximum(self.lo[a],y-eta);high=np.minimum(self.hi[a],y+eta)
        if np.any(low>high+1e-12):raise ValueError('BOUND_BREACH: inconsistent observation and assumed drift/noise bounds')
        self.lo[a]=low;self.hi[a]=high
    def completion(self,current,multiplier):
        # Holding is a one-step commitment; switching horizon equals physical delay.
        h=np.where(DEP[current]==0,1,DEP[current]*multiplier)
        return np.maximum(-1,self.lo-L*h[:,None]),np.minimum(1,self.hi+L*h[:,None]),h

def plant(scenario,run):
    rng=np.random.default_rng(np.random.SeedSequence([SEED,0 if scenario=='Local' else 1,run,0]))
    # Enough future samples to audit arrivals from the final scored instant.
    length=T+8;truth=np.empty((length,N,2));bias=rng.uniform(-.035,.035,(N,2))
    phy,link,route=A.T
    def target(t):
        preferred=(t//75)%4
        route_bonus=np.where(route==preferred,.20,-.08)
        quality=.06+.065*phy+.07*link+route_bonus
        headroom=.27-.11*phy-.10*link+.025*np.sin((t/35)+route)
        result=np.stack([quality,headroom],axis=1)+bias
        if scenario=='Outage' and 110<=t<180:result[:,0]-=.65
        return result
    truth[0]=np.clip(target(0),-1,1)
    for t in range(1,length):
        velocity=.15*(target(t)-truth[t-1])+rng.uniform(-.012,.012,(N,2))
        truth[t]=np.clip(truth[t-1]+np.clip(velocity,-L,L),-1,1)
    nrng=np.random.default_rng(np.random.SeedSequence([SEED,0 if scenario=='Local' else 1,run,1]))
    noise=nrng.uniform(-ETA,ETA,truth.shape)
    assert np.max(np.abs(np.diff(truth,axis=0)))<=L+1e-12
    return truth,noise

def outcome_proxy(lo,hi,h):
    """Independent uniform observation surrogate; not a calibrated posterior."""
    lower=lo-ETA;upper=hi+ETA;width=upper-lower
    threshold=ETA+L*np.asarray(h)[:,None]
    positive=np.clip((upper-threshold)/width,0,1)
    negative=np.clip((-threshold-lower)/width,0,1)
    feasible=np.prod(positive,axis=1)
    infeasible=1-np.prod(1-negative,axis=1)
    unresolved=np.maximum(0,1-feasible-infeasible)
    return np.stack([feasible,infeasible,unresolved],axis=1)

def expiry_offset(upper):
    # A witness remains strict only for offsets d < expiry.
    return np.maximum(0,np.max(-upper/L,axis=1))

def episode_metrics(empty,detected):
    empty=np.asarray(empty,bool);detected=np.asarray(detected,bool)
    assert not np.any(detected & ~empty)
    starts=np.flatnonzero(empty & ~np.r_[False,empty[:-1]])
    lengths=[];waits=[];missed=0
    for start in starts:
        end=int(start)
        while end<len(empty) and empty[end]:end+=1
        hit=np.flatnonzero(detected[start:end]);lengths.append(end-start)
        waits.append(int(hit[0]) if len(hit) else end-start);missed+=not len(hit)
    return dict(empty_steps=int(empty.sum()),detected_empty_steps=int(detected.sum()),empty_episodes=len(starts),missed_episodes=int(missed),restricted_detection_wait_sum=sum(waits))

class Controller:
    """Acquisition sees only cache, current ID, time and query responses."""
    def __init__(self,policy,budget,multiplier,run):
        self.policy=policy;self.budget=budget;self.multiplier=multiplier;self.cache=Cache();self.pointer=0
        self.rng=np.random.default_rng(np.random.SeedSequence([SEED,run,23]))
        self.last_query=np.full(N,-1,int)
    def decision(self,t,current,query):
        self.cache.propagate(t);seen=set();count=0
        if self.policy=='Full-information':
            for a in range(N):self.cache.observe(a,query(a,True),0)
            count=N
        else:
            for k in range(self.budget):
                lo,hi,h=self.cache.completion(current,self.multiplier)
                safe,impossible,unknown=classify(lo,hi)
                dp=DEP[current]
                dlow=int(dp[~impossible].min()) if (~impossible).any() else 4
                dup=int(dp[safe].min()) if safe.any() else 4
                if safe[current] or impossible.all() or (dup<4 and dlow==dup):break
                if self.policy in ['Expiry-first','Uncovered-first']:
                    candidates=np.array([a for a in range(N) if a not in seen],int)
                    if not len(candidates):break
                    expiry=expiry_offset(self.cache.hi)
                    uncovered=candidates[expiry[candidates]<=0]
                    urgent=candidates[(expiry[candidates]>0)&(expiry[candidates]<=1)]
                    if self.policy=='Expiry-first' and len(urgent):
                        a=int(urgent[np.lexsort((urgent,self.last_query[urgent],expiry[urgent]))[0]])
                    elif len(uncovered):
                        a=int(uncovered[np.lexsort((uncovered,self.last_query[uncovered]))[0]])
                    else:
                        a=int(candidates[np.lexsort((candidates,self.last_query[candidates],expiry[candidates]))[0]])
                elif self.policy in ['Feasibility-first','Outcome-entropy']:
                    candidates=np.array([a for a in range(N) if a not in seen],int)
                    if not len(candidates):break
                    probabilities=outcome_proxy(self.cache.lo,self.cache.hi,h)
                    if self.policy=='Feasibility-first':score=probabilities[:,0]/(1+h)
                    else:score=-np.sum(probabilities*np.log(np.maximum(probabilities,1e-15)),axis=1)
                    a=int(candidates[np.lexsort((candidates,self.last_query[candidates],-score[candidates]))[0]])
                elif k==0 and self.policy not in ['Pure-sweep','Pure-uniform'] and (self.policy!='Balanced-sweep' or t%2==0):
                    a=current
                elif self.policy=='Certificate-directed':
                    eligible=np.flatnonzero(unknown)
                    eligible=np.array([a for a in eligible if a not in seen and dp[a]<=dup],int)
                    if not len(eligible):break
                    width=(self.cache.hi-self.cache.lo).max(axis=1)
                    a=int(eligible[np.lexsort((eligible,-width[eligible],dp[eligible]))[0]])
                elif self.policy in ['Round-robin','Balanced-sweep','Pure-sweep']:
                    candidates=[(self.pointer+j)%N for j in range(N) if (self.pointer+j)%N not in seen]
                    if not candidates:break
                    a=candidates[0];self.pointer=(a+1)%N
                elif self.policy in ['Uniform','Pure-uniform']:
                    candidates=[a for a in range(N) if a not in seen]
                    if not candidates:break
                    a=int(self.rng.choice(candidates))
                else:raise ValueError(self.policy)
                self.cache.observe(a,query(a,False));seen.add(a);count+=1;self.last_query[a]=t
        lo,hi,h=self.cache.completion(current,self.multiplier);safe,impossible,unknown=classify(lo,hi);dp=DEP[current]
        dlow=int(dp[~impossible].min()) if (~impossible).any() else 4
        dup=int(dp[safe].min()) if safe.any() else 4
        now_safe,now_bad,now_unknown=classify(self.cache.lo,self.cache.hi)
        state='FEASIBLE' if now_safe.any() else ('INFEASIBLE' if now_bad.all() else 'UNKNOWN')
        completion='FEASIBLE' if safe.any() else ('INFEASIBLE' if impossible.all() else 'UNKNOWN')
        if safe[current]:chosen=current;certificate='CERTIFIED_HOLD'
        elif safe.any():
            ix=np.flatnonzero(safe);chosen=int(ix[np.lexsort((ix,-lo[ix].min(axis=1),dp[ix]))[0]])
            certificate='CERTIFIED_ARRIVAL'
        else:chosen=current;certificate='UNCERTIFIED_RETAIN'
        return dict(action=chosen,queries=count,state=state,completion=completion,certificate=certificate,
            dlow=dlow,dup=dup,delay=int(h[chosen]) if chosen!=current else 0,
            lower=lo.copy(),upper=hi.copy(),horizon=h.copy(),depth_certified=(dup<4 and dlow==dup))

def simulate(truth,noise,policy,budget,multiplier,run,keep_events=False):
    ctl=Controller(policy,budget,multiplier,run);current=0;pending=None;events=[]
    queries=commands=changes=arrival_bad=arrival_checks=recovery=depth_cert=unknown=infeasible=completion_unknown=decisions=hold_bad=false_infeasible=0
    gpr=[];bracket_widths=[];empty_grid=[];detected_grid=[]
    for t in range(T):
        if pending is not None and pending[0]==t:
            current=pending[1];pending=None;changes+=1
        if pending is None:
            def query(a,exact):return truth[t,a].copy() if exact else truth[t,a]+noise[t,a]
            r=ctl.decision(t,current,query);decisions+=1;queries+=r['queries'];unknown+=r['state']=='UNKNOWN';infeasible+=r['state']=='INFEASIBLE';completion_unknown+=r['completion']=='UNKNOWN'
            assert r['queries']<= (N if policy=='Full-information' else budget)
            assert np.all(ctl.cache.lo<=truth[t]+1e-10) and np.all(truth[t]<=ctl.cache.hi+1e-10)
            _,certbad,_=classify(ctl.cache.lo,ctl.cache.hi)
            assert not np.any(certbad & (truth[t]>=0).all(axis=1))
            if r['state']=='INFEASIBLE':false_infeasible+=int((truth[t]>=0).all(axis=1).any())
            future=truth[t+r['horizon'],np.arange(N)]
            assert np.all(r['lower']<=future+1e-10) and np.all(future<=r['upper']+1e-10)
            truefeas=(future>=0).all(axis=1)
            oracledepth=int(DEP[current,truefeas].min()) if truefeas.any() else 4
            assert r['dlow']<=oracledepth<=r['dup']
            assert r['completion']!='INFEASIBLE' or not truefeas.any()
            if r['dup']<4:bracket_widths.append(r['dup']-r['dlow'])
            if r['certificate']=='CERTIFIED_HOLD':
                hold_bad+=int(not (truth[t+1,current]>=0).all());assert not hold_bad
            nxt=r['action']
            if nxt!=current:
                commands+=1;arrival_checks+=1;arrival_bad+=int(not (truth[t+r['delay'],nxt]>=0).all())
                depth_cert+=r['depth_certified']
                # Old action remains active at t..t+delay-1; zero delay has no bridge.
                bridge_safe=r['delay']==0 or np.all(ctl.cache.lo[current]-L*max(0,r['delay']-1)>=0)
                recovery+=not bridge_safe
                if r['delay']==0:current=nxt;changes+=1
                else:pending=(t+r['delay'],nxt)
            if keep_events:events.append(dict(t=t,**{k:v for k,v in r.items() if k not in ['lower','upper','horizon']}))
        # Read-only audit on a common wall-clock grid, including pending execution.
        audit_hi=np.minimum(1,ctl.cache.hi+L*(t-ctl.cache.time))
        true_empty=not (truth[t]>=0).all(axis=1).any()
        detected=bool((audit_hi<0).any(axis=1).all())
        assert not detected or true_empty
        empty_grid.append(true_empty);detected_grid.append(detected)
        gpr.append(bool((truth[t,current]>=0).all()))
    assert arrival_bad==0 and false_infeasible==0
    metrics=dict(GPR=float(np.mean(gpr)),queries_per_step=queries/T,commands=commands,completed_changes=changes,
        decision_instants=decisions,unknown_rate=unknown/decisions,infeasible_rate=infeasible/decisions,
        completion_unknown_rate=completion_unknown/decisions,arrival_certificates=arrival_checks,arrival_certificate_failures=arrival_bad,
        false_infeasibility_certificates=false_infeasible,hold_certificate_failures=hold_bad,
        recovery_fraction=recovery/commands if commands else 0.,depth_certified_fraction=depth_cert/commands if commands else 0.,
        mean_finite_depth_bracket_width=float(np.mean(bracket_widths)) if bracket_widths else 0.)
    metrics.update(episode_metrics(empty_grid,detected_grid))
    return metrics,events

def write_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def benchmark():
    out=ROOT/'results';out.mkdir(exist_ok=True);rows=[]
    for scenario in ['Local','Outage']:
        for mult in [0,1,2]:
            for run in range(30):
                truth,noise=plant(scenario,run)
                for budget in [1,2,4,8]:
                    for policy in ['Certificate-directed','Round-robin','Uniform']:
                        met,ev=simulate(truth,noise,policy,budget,mult,run,keep_events=run==0 and budget==4 and mult==1)
                        rows.append(dict(scenario=scenario,delay_multiplier=mult,budget=budget,run=run,policy=policy,**met))
                        if ev:(out/f'events_{scenario}_{policy}.json').write_text(json.dumps(ev,indent=2))
                met,_=simulate(truth,noise,'Full-information',N,mult,run)
                rows.append(dict(scenario=scenario,delay_multiplier=mult,budget=N,run=run,policy='Full-information',**met))
            print(scenario,'delay',mult,'complete',flush=True)
    write_csv(out/'per_run.csv',rows)
    rng=np.random.default_rng(2026092005);ix=rng.integers(0,30,(5000,30));summary=[];paired=[]
    metrics=['GPR','queries_per_step','unknown_rate','infeasible_rate','completion_unknown_rate','commands','recovery_fraction','depth_certified_fraction','mean_finite_depth_bracket_width']
    groups={}
    for r in rows:groups.setdefault((r['scenario'],r['delay_multiplier'],r['budget'],r['policy']),[]).append(r)
    for key,rr in groups.items():
        for m in metrics:
            x=np.array([r[m] for r in rr]);lo,hi=np.quantile(x[ix].mean(axis=1),[.025,.975]);summary.append(dict(zip(['scenario','delay_multiplier','budget','policy'],key),metric=m,mean=float(x.mean()),ci_low=float(lo),ci_high=float(hi),n=30))
    for scenario in ['Local','Outage']:
        for mult in [0,1,2]:
            for budget in [1,2,4,8]:
                lhs=groups[(scenario,mult,budget,'Certificate-directed')]
                for policy in ['Round-robin','Uniform']:
                    rhs=groups[(scenario,mult,budget,policy)]
                    for m in ['GPR','queries_per_step','unknown_rate','commands']:
                        x=np.array([a[m]-b[m] for a,b in zip(lhs,rhs)]);lo,hi=np.quantile(x[ix].mean(axis=1),[.025,.975]);paired.append(dict(scenario=scenario,delay_multiplier=mult,budget=budget,comparison='Certificate-directed minus '+policy,metric=m,mean=float(x.mean()),ci_low=float(lo),ci_high=float(hi)))
    write_csv(out/'summary.csv',summary);write_csv(out/'paired.csv',paired)
    report={'controller_runs':len(rows),'scored_steps':len(rows)*T,'arrival_certificates':sum(r['arrival_certificates'] for r in rows),'arrival_certificate_failures':sum(r['arrival_certificate_failures'] for r in rows),'false_infeasibility_certificates':sum(r['false_infeasibility_certificates'] for r in rows),'hold_certificate_failures':sum(r['hold_certificate_failures'] for r in rows),'all_interval_inclusions_depth_brackets_and_budgets':'PASS','scope':'Synthetic bounded-margin environment, no NR or external control validation'}
    (out/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':benchmark()
