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
        self.multi_domain_comparator.operators["diff"] = lambda a, b: a - b
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
        self.multi_domain_comparator.operators["diff"] = lambda a, b: a - b
        ret = self.multi_domain_comparator(a, b, c)
        self.assertTrue(len(ret) == 2)

    def test_domain(self):
        comp = self.multi_domain_comparator
        comp.domain = [0, 10]
        self.assertTrue(comp._operation_domain.start == 0)
        self.assertTrue(comp._operation_domain.stop == 10)
        for name in comp._domains:
            domain = comp._domains[name]
            self.assertTrue(domain._operation_domain.start == 0)
            self.assertTrue(domain._operation_domain.stop == 10)


if __name__ == "__main__":
    unittest.main()
