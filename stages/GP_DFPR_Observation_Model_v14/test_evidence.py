import unittest,math
from dataclasses import replace
from evidence import *

class Tests(unittest.TestCase):
    def setUp(self):
        self.e=Evidence('a',(.3,.2),(.02,.02),0,2,(.04,.04),10,'lab-domain','hard_assumption','test-only','synthetic-test-assumption')
    def test_delivery_age_and_execution(self):
        p,_=strict_interval(self.e,'a','lab-domain',2,1)
        self.assertAlmostEqual(p[0][0],.16)
    def test_statistical_is_not_hard(self):
        p,why=strict_interval(replace(self.e,bound_kind='statistical'),'a','lab-domain',2,0)
        self.assertIsNone(p);self.assertEqual(why,'NONDETERMINISTIC_EVIDENCE')
    def test_unsupported_action_and_domain(self):
        self.assertIsNone(strict_interval(self.e,'b','lab-domain',2,0)[0])
        self.assertIsNone(strict_interval(self.e,'a','field',2,0)[0])
    def test_undelivered_and_expired(self):
        self.assertIsNone(strict_interval(self.e,'a','lab-domain',1,0)[0])
        self.assertIsNone(strict_interval(self.e,'a','lab-domain',9,2)[0])
    def test_unknown_blocks_global_infeasibility(self):
        self.assertEqual(inventory_status([([-1],[-.1]),None]),'UNKNOWN')
        self.assertEqual(inventory_status([([-1],[-.1]),([-1],[-.2])]),'CERTIFIED_INFEASIBLE')
    def test_zero_is_feasible(self):
        self.assertEqual(inventory_status([([0],[.1])]),'CERTIFIED_FEASIBLE')
        self.assertEqual(inventory_status([([-.1],[0])]),'UNKNOWN')
    def test_quantile_insufficient_sample(self):
        self.assertTrue(math.isinf(split_conformal_radius([.1]*9,.05)))
        self.assertAlmostEqual(split_conformal_radius(list(range(19)),.05),18)
    def test_error_propagation(self):
        self.assertAlmostEqual(propagated_radius(.1,[2,3],[.01,.02]),.18)
    def test_provenance_required(self):
        self.assertIsNone(strict_interval(replace(self.e,assumption_ref=''),'a','lab-domain',2,0)[0])
if __name__=='__main__':unittest.main(verbosity=2)
