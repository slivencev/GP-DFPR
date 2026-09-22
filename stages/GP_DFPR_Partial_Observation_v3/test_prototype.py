import unittest
import numpy as np
from prototype import Cache,classify,Controller,DEP,N,L,plant,simulate

class Verification(unittest.TestCase):
    def test_no_safe_does_not_mean_infeasible(self):
        lo=np.full((N,2),-.1);hi=np.full((N,2),.1)
        safe,bad,unknown=classify(lo,hi)
        self.assertFalse(safe.any());self.assertFalse(bad.all());self.assertTrue(unknown.all())
        hi[:,0]=-.01;self.assertTrue(classify(lo,hi)[1].all())
    def test_unobserved_candidate_blocks_global_certificate(self):
        c=Cache()
        for a in range(N-1):c.observe(a,np.array([-.5,.2]))
        self.assertFalse(classify(c.lo,c.hi)[1].all())
        self.assertTrue(classify(c.lo,c.hi)[2][-1])
    def test_delay_negative_control(self):
        c=Cache();target=int(np.flatnonzero(DEP[0]==3)[0]);c.observe(target,np.array([.05,.2]),eta=0)
        self.assertTrue(classify(c.lo,c.hi)[0][target])
        lo,hi,h=c.completion(0,1)
        self.assertFalse(classify(lo,hi)[0][target])
        actual=.05-L*3
        self.assertLess(actual,0) # Ignoring delay would have issued a false guarantee.
        self.assertLessEqual(lo[target,0],actual)
    def test_bound_breach_is_not_physical_infeasibility(self):
        c=Cache();c.observe(0,np.array([.5,.5]),eta=0)
        with self.assertRaisesRegex(ValueError,'BOUND_BREACH'):c.observe(0,np.array([-.5,.5]),eta=0)
    def test_depth_bracket(self):
        c=Cache();current=0
        # Certify all NONE/PHY alternatives impossible; leave one LINK action feasible.
        for a in range(N):c.observe(a,np.array([-.6,-.6]),eta=0)
        target=int(np.flatnonzero(DEP[current]==2)[0]);c.lo[target]=[.4,.4];c.hi[target]=[.4,.4]
        low,high,h=c.completion(current,1);safe,bad,_=classify(low,high)
        self.assertEqual(DEP[current,~bad].min(),2);self.assertEqual(DEP[current,safe].min(),2)
    def test_cold_start_budget(self):
        for budget in [1,2,4,8]:
            ctl=Controller('Certificate-directed',budget,1,3);calls=[]
            def query(a,exact):calls.append(a);return np.array([-.8,-.8])
            r=ctl.decision(0,0,query)
            self.assertEqual(len(calls),budget);self.assertEqual(r['state'],'UNKNOWN')
            self.assertEqual(r['certificate'],'UNCERTIFIED_RETAIN')
    def test_replay_all_policies_and_delays(self):
        truth,noise=plant('Outage',99)
        for policy in ['Certificate-directed','Round-robin','Uniform','Full-information']:
            for mult in [0,1,2]:
                met,_=simulate(truth,noise,policy,4,mult,99)
                self.assertEqual(met['arrival_certificate_failures'],0)
                self.assertEqual(met['false_infeasibility_certificates'],0)
    def test_noise_and_delay_floor(self):
        eta=.01;h=3;m=2*eta+L*h
        for error in [-eta,0,eta]:self.assertGreaterEqual(m+error-eta-L*h,-1e-12)
        m-=.005;self.assertLess(m-eta-eta-L*h,0)
    def test_refresh_window_certificate(self):
        c=Cache()
        for a in range(N):c.observe(a,np.array([-.5,.2]))
        c.propagate(5)
        self.assertTrue(classify(c.lo,c.hi)[1].all())
        c.propagate(20)
        self.assertFalse(classify(c.lo,c.hi)[1].all())

if __name__=='__main__':unittest.main(verbosity=2)
