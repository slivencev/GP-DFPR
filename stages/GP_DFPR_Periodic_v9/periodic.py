"""Synthetic recurrent impairment; not an RF jammer or UAV-paper reproduction."""
import numpy as np
import model as m
VARIANTS=['global-d6','global-d12','global-d24','global-d36']
PERIOD=60;WARMUP=60;AMPLITUDE=.65;MASTER=2026092050

def schedule(variant,length):
    scope,duration=variant.split('-');assert variant in VARIANTS
    on=int(duration[1:])
    mask=np.zeros((length,m.N),bool)
    for t in range(WARMUP,length):
        cycle,phase=divmod(t-WARMUP,PERIOD)
        if phase<on:mask[t]=True if scope=='global' else m.A[:,2]==cycle%4
    return mask

def plant(variant,run):
    length=m.T+8;rng=np.random.default_rng(np.random.SeedSequence([MASTER,run,0]))
    bias=rng.uniform(-.035,.035,(m.N,2));innovation=rng.uniform(-.012,.012,(length-1,m.N,2))
    mask=schedule(variant,length);truth=np.empty((length,m.N,2));phy,link,route=m.A.T
    def target(t):
        quality=.06+.065*phy+.07*link+np.where(route==(t//75)%4,.20,-.08)-AMPLITUDE*mask[t]
        headroom=.27-.11*phy-.10*link+.025*np.sin(t/35+route)
        return np.stack([quality,headroom],axis=1)+bias
    truth[0]=np.clip(target(0),-1,1)
    for t in range(1,length):
        truth[t]=np.clip(truth[t-1]+np.clip(.15*(target(t)-truth[t-1])+innovation[t-1],-m.L,m.L),-1,1)
    noise=np.random.default_rng(np.random.SeedSequence([MASTER,run,1])).uniform(-m.ETA,m.ETA,truth.shape)
    assert np.max(np.abs(np.diff(truth,axis=0)))<=m.L+1e-12
    return truth,noise,mask
