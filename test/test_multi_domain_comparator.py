import unittest

import numpy as np

from comparator.multi_domain import MultiDomainComparator
from comparator.single_domain import SingleDomainComparator


class TestMultiDomainComparator(unittest.TestCase):

    def setUp(self):

        self.multi_domain_comparator = MultiDomainComparator(
            name="test",
            domains={
                "domain0": SingleDomainComparator("domain"),
                "domain1": SingleDomainComparator("domain")
            }
        )

    def test_add_operator(self):
        self.multi_domain_comparator.operators["diff"] = np.subtract
        self.assertTrue("diff" in
                        self.multi_domain_comparator.domain0.operators)
        self.assertTrue("diff" in
                        self.multi_domain_comparator.domain1.operators)

    def test_add_product(self):
        self.multi_domain_comparator.products["mean"] = np.mean
        self.assertTrue("mean" in
                        self.multi_domain_comparator.domain0.products)
        self.assertTrue("mean" in
                        self.multi_domain_comparator.domain1.products)

    def test_call(self):
        a, b, c = [np.random.rand(10) for i in range(3)]
        self.multi_domain_comparator.operators["diff"] = np.subtract
        ret = self.multi_domain_comparator(a, b, c)
        self.assertTrue(len(ret) == 2)


if __name__ == "__main__":
    unittest.main()
