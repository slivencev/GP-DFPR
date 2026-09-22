from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parent
CURVES=json.loads((ROOT/'curves.json').read_text())
MCS=[4,10,15];EFF=np.array([2*308/1024,4*340/1024,4*616/1024])
T=400;ETA=.2;DRIFT=.08;LATENCY=2
def bler(gamma):
    return np.stack([np.interp(gamma,CURVES[str(a)]['sinr_db'],CURVES[str(a)]['code_bler'],left=1,right=0) for a in MCS],axis=-1)
def predict(measured,sampled_at,now,horizon,method):
    age=np.asarray(now)+horizon-np.asarray(sampled_at)
    assert np.all(np.asarray(sampled_at)+LATENCY<=now) and np.all(age>=0)
    radius=np.zeros_like(age,dtype=float) if method=='Point' else ETA+DRIFT*age+(.4 if method=='Interval-plus-model' else 0.)
    if method not in ['Point','Interval','Interval-plus-model']:raise ValueError(method)
    low=measured-radius;high=measured+radius
    b_low=bler(high);b_high=bler(low)
    support=np.stack([(low>=CURVES[str(a)]['sinr_db'][0])&(high<=CURVES[str(a)]['sinr_db'][-1]) for a in MCS],axis=-1)
    return b_low,b_high,EFF*(1-b_high),EFF*(1-b_low),support
def plant(run):
    rng=np.random.default_rng(np.random.SeedSequence([2026092090,run]));phase=rng.uniform(0,2*np.pi);gamma=np.empty(T+5);gamma[0]=6.4
    for t in range(1,len(gamma)):
        target=6.4+5*np.sin(2*np.pi*t/240+phase)
        gamma[t]=gamma[t-1]+np.clip(.15*(target-gamma[t-1])+rng.uniform(-.03,.03),-DRIFT,DRIFT)
    noise=rng.uniform(-ETA,ETA,len(gamma));assert np.max(np.abs(np.diff(gamma)))<=DRIFT+1e-12
    return gamma,noise
